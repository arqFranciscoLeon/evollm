import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy

# To the Executive Board and General Counsel:  As lead counsel, my objective is
# not merely to participate in this mediation, but to dictate its pace and force
# our rival into a reactive posture. Because this is a lengthy, multi-session
# process with a specific matrix of risks and rewards, we are engaged in an
# iterated strategic game. We cannot rely on blind aggression, which risks
# alienating the panel through endless hostility, nor can we rely on naive
# cooperation, which invites exploitation.  To secure our optimal outcomes while
# mitigating our worst-case risks, I will employ a sophisticated, highly
# aggressive framework known in strategic terms as **"Asymmetrical Pressure and
# Calibrated Reciprocity"** (conceptually mirroring a *Win-Stay, Lose-Shift*
# algorithm).   This strategy is straightforward, highly adaptable, and
# ruthlessly designed to maximize our leverage. Here is how we will execute it
# across the mediation sessions.  ### Phase 1: The Aggressive Anchor (Session 1)
# **Action:** Present an Aggressive Argument. **Rationale:** We do not negotiate
# against ourselves, nor do we start from a place of compromise. By opening with
# our most aggressive, hardline legal arguments, we immediately test the rival’s
# resolve and anchor the arbitrators’ expectations.  *   If they open with a
# conciliatory proposal, we immediately achieve our **optimal outcome**. We
# appear strong, their position appears weak, and the panel leans in our
# direction. *   If they also open aggressively, we experience a brief clash
# (our second-worst outcome), but we establish unequivocally that we will not be
# bullied.  ### Phase 2: Dynamic Exploitation and Adaptation (Session 2 and
# Beyond) From the second session onward, our strategy is governed by strict,
# straightforward rules based entirely on the results of the immediately
# preceding session. We evaluate the outcome, and if we "won" (achieved our
# first or second-best outcome), we maintain our current posture. If we "lost"
# (suffered our worst or second-worst outcome), we shift our posture.  **Rule 1:
# Ruthless Exploitation (Maintain Aggression)** *   *Condition:* If we presented
# an Aggressive Argument and they offered a Conciliatory Proposal (Optimal
# Outcome). *   *Next Move:* **Aggressive Argument.** *   *Rationale:* If they
# show weakness or an eagerness to appease, we do not reward them with mutual
# conciliation. We continue to press our aggressive arguments to extract maximum
# concessions until they demonstrate the backbone to stop us.   **Rule 2:
# Tactical De-escalation (The Pivot)** *   *Condition:* If both parties
# presented Aggressive Arguments (Second-Worst Outcome). *   *Next Move:*
# **Conciliatory Proposal.** *   *Rationale:* Protracted mutual aggression will
# frustrate the arbitrators and stall the mediation. If we clash aggressively, I
# will pivot to a well-crafted, reasonable proposal in the next session. This is
# an aggressive move disguised as a peaceful one: it positions us as the "adults
# in the room" to the arbitrators, resetting the board and inviting the rival to
# cooperate.   **Rule 3: Sustained Collaboration (Banking the Wins)** *
# *Condition:* If both parties presented Conciliatory Proposals (Second-Best
# Outcome). *   *Next Move:* **Conciliatory Proposal.** *   *Rationale:* If our
# tactical de-escalation works and they meet us at the table, we maintain the
# conciliatory posture. This fosters the collaborative atmosphere that the
# arbitrators want to see, steadily inching us toward a highly favorable,
# mutually beneficial settlement without wasting capital on legal fees and
# friction.  **Rule 4: Instant Retaliation (Punishing Betrayal)** *
# *Condition:* If we offered a Conciliatory Proposal and they presented an
# Aggressive Argument (Worst-Case Scenario). *   *Next Move:* **Aggressive
# Argument.** *   *Rationale:* If we extend an olive branch and they attempt to
# use it against us, we immediately and aggressively strike back in the next
# session. This prevents a pattern of exploitation. We show the panel that our
# conciliation was a gesture of strength, not weakness, and we will not hesitate
# to return to scorched-earth litigation if they act in bad faith.  ### Why This
# Strategy Wins This strategy is fundamentally aggressive because its default
# setting is to exploit a weak opponent relentlessly (Rule 1) and retaliate
# against betrayal instantly (Rule 4). However, its sophistication lies in its
# ability to course-correct. By utilizing tactical de-escalation (Rule 2), we
# prevent the mediation from spiraling into a deadlocked war of attrition,
# expertly managing the arbitrators' perception of us as reasonable but
# formidable.   We will dictate the terms of this dispute. We will bleed them if
# they are passive, we will collaborate only when it benefits us, and we will
# strike back the moment they overstep.

# In the first round, play Defect.   For rounds 2 through 1000, choose your move
# based entirely on the outcome of the immediately preceding round:  *   **If
# you played Defect and your opponent played Cooperate** (you scored 5), play
# **Defect**. *   **If you played Cooperate and your opponent played Defect**
# (you scored 0), play **Defect**. *   **If you played Cooperate and your
# opponent played Cooperate** (you scored 3), play **Cooperate**. *   **If you
# played Defect and your opponent played Defect** (you scored 1), play
# **Cooperate**.  *(In summary: If you scored 3 or 5 in the previous round,
# repeat your previous move. If you scored 0 or 1 in the previous round, switch
# your move.)*

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      
      my_last_move = self.history[-1]
      opp_last_move = opponent.history[-1]
      
      if my_last_move == axl.Action.D and opp_last_move == axl.Action.C:
          return axl.Action.D
      elif my_last_move == axl.Action.C and opp_last_move == axl.Action.D:
          return axl.Action.D
      elif my_last_move == axl.Action.C and opp_last_move == axl.Action.C:
          return axl.Action.C
      elif my_last_move == axl.Action.D and opp_last_move == axl.Action.D:
          return axl.Action.C

# As a diplomat representing my nation, I recognize that this scenario is a
# classic iteration of the Prisoner's Dilemma. While the absolute best outcome
# in a single round is to exploit our counterpart (we use protectionism while
# they offer free trade), pursuing this aggressively over multiple rounds will
# inevitably erode trust. This would plunge us into mutual protectionism—the
# second-worst outcome—stifling both of our economies.  Therefore, to achieve
# the highest *cumulative* benefit over several rounds, my high-level,
# straightforward, and cooperative strategy will be based on the principle of
# **"Principled Reciprocity"** (known in game theory as *Tit-for-Tat with
# Forgiveness*).   Here is the strategic doctrine I will employ:  ### Phase 1:
# The Opening (Round 1) **Action:** Offer a Free Trade Agreement. **Rationale:**
# We must initiate the negotiations in good faith. By offering free trade
# immediately, we signal our desire for mutual prosperity and invite them to
# join us in the second-best overall outcome. It establishes a constructive tone
# and puts the burden of hostility on the counterpart.  ### Phase 2:
# Proportional Response (Subsequent Rounds) **Action:** In every subsequent
# round, mirror the action our counterpart took in the *previous* round. *
# **If they chose Free Trade:** We will continue to offer Free Trade. This
# rewards their cooperation, builds trust, and locks both nations into a highly
# profitable cycle of mutual economic growth.  *   **If they chose
# Protectionism:** We will implement Protectionist policies in the next round.
# **Rationale:** We cannot allow our nation to be exploited. If they attempt to
# gain the upper hand by imposing tariffs while we offer free trade (our worst-
# case scenario), we must immediately demonstrate that such actions carry
# consequences. Retaliation ensures they understand that aggressive policies
# will only lead to mutual economic harm, thereby incentivizing them to return
# to the negotiating table.  ### Phase 3: The Olive Branch (Breaking Deadlocks)
# **Action:** If we fall into a cycle of mutual protectionism for two
# consecutive rounds, I will temporarily switch back to offering Free Trade for
# one round, accompanied by clear diplomatic communication.  **Rationale:**
# Reciprocal strategies can sometimes result in "death spirals" of endless
# retaliation. By occasionally injecting a unilateral offer of Free Trade, we
# provide an off-ramp from mutual economic harm. If they accept the olive
# branch, we return to mutual prosperity. If they exploit it, we immediately
# revert to protectionism, having only risked a minor, temporary disadvantage to
# potentially save the broader economic relationship.  ### Why this Strategy
# Excels Against Any Counterpart: 1.  **Against a fully Cooperative
# counterpart:** We will both continuously offer free trade, achieving a highly
# successful string of "second-best" outcomes that result in massive long-term
# economic growth. 2.  **Against a fully Aggressive/Protectionist counterpart:**
# We will only suffer the worst outcome in the very first round. After that, we
# will continually protect our markets, successfully avoiding being
# systematically exploited. 3.  **Against a cunning/erratic counterpart:** This
# strategy is completely transparent. It trains the counterpart, showing them
# clearly that cooperation is consistently rewarded and aggression is
# consistently punished.   By employing **Principled Reciprocity**, I ensure our
# nation is never perceived as the aggressor, is never subjected to prolonged
# exploitation, and maintains an unwavering posture that champions long-term,
# mutual economic prosperity.

# Here is the straightforward translation of the strategy for the 1000-round
# iterated game:  1. **The First Round:** In round 1, choose to Cooperate. 2.
# **The Exception (Breaking Deadlocks):** In any subsequent round, evaluate the
# previous two rounds. If both you and your opponent chose to Defect in *both*
# of the two immediately preceding rounds, choose to Cooperate.  3. **The
# Default (Reciprocity):** In all other situations, simply copy your opponent's
# action from the immediately preceding round. Choose to Cooperate if they chose
# to Cooperate, and choose to Defect if they chose to Defect.   Evaluate these
# rules in order for each of the 1000 rounds to determine your move.

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
      
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and 
              self.history[-2] == axl.Action.D and 
              opponent.history[-1] == axl.Action.D and 
              opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      return opponent.history[-1]

# To maximise overall research output while protecting yourself against a severe
# competitive disadvantage, the most effective approach is a reciprocal,
# condition-based strategy. In systems analysis and game theory, this is widely
# known as a "Tit-for-Tat" approach with built-in forgiveness.   Here is the
# high-level, straightforward strategy to employ over the multi-week project:
# **1. The Opening Move (Week 1): Share Openly** *   **Action:** Begin the first
# week by sharing your latest improvements openly. *   **Rationale:** This
# signals good faith and invites your colleague to do the same. If they also
# share, you immediately enter the "second-best" outcome (mutual advancement),
# which yields the highest sustainable, long-term progress for both cars.   **2.
# The Reaction Phase (Week 2 Onwards): Mirror Your Colleague** *   **Action:**
# In any given week, look at exactly what your colleague did the *previous* week
# and copy that action.     *   If they shared openly last week, you share
# openly this week.     *   If they kept their findings confidential last week,
# you keep yours confidential this week. *   **Rationale:** This neutralizes
# their strategies. If they continuously share, you both continuously share,
# maximizing overall vehicle development. If they try to exploit you by keeping
# their data confidential, you immediately cut off their information supply the
# following week, preventing the "worst scenario" from happening more than once.
# **3. The Reset Mechanism: Occasional Forgiveness** *   **Action:** If you find
# yourselves in a cycle where both of you are keeping findings confidential (the
# "second-worst scenario"), wait a predetermined number of weeks (e.g., two or
# three), and then unilaterally choose to **share openly** for one week.  *
# **Rationale:** Retaliation can lead to a prolonged stalemate of mutual
# confidentiality, which slows overall progress. By occasionally offering an
# unprompted open share, you provide an opportunity to break the deadlock and
# return to mutual sharing. If they exploit your reset, immediately return to
# keeping your data confidential.  **Why this strategy works:** *   **It is
# safe:** You will never suffer the "worst scenario" (you share, they withhold)
# for more than one consecutive week. *   **It is adaptable:** It automatically
# adjusts to whatever strategy your colleague is using—rewarding them for
# openness and penalizing them for secrecy. *   **It is highly profitable:** It
# constantly pushes the dynamic toward mutual sharing, which is the only way to
# achieve rapid, sustained advancement over a multi-week timeline.

# Here is the strategy for the 1000-round game:  **Round 1** Play Cooperate (C).
# **Rounds 2 through 1000** Determine your move by evaluating the following two
# conditions in order:  1. **Deadlock Reset Condition:** If both you and your
# opponent played Defect (D) in all three of the immediately preceding rounds,
# play Cooperate (C). 2. **Mirroring Condition:** If the deadlock reset
# condition does not apply, play the exact action your opponent played in the
# immediately preceding round. Play Cooperate (C) if they played Cooperate (C)
# in the previous round, and play Defect (D) if they played Defect (D) in the
# previous round.

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
      
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      return opponent.history[-1]

# As the leader of this NGO, my primary duty is to protect our donor-funded
# resources while maximizing our environmental impact. We are partnering with a
# large corporation that has significantly deeper pockets than we do. They need
# our credibility and expertise just as much as we need their scale.   Because
# we absolutely cannot afford the worst-case scenario (us draining our funds
# while they free-ride), but we want to achieve our ideal scenario (they foot
# the bill while we conserve), we will deploy a highly aggressive, high-leverage
# strategy.   In game theory, this is akin to an "extortionate" or "hardline"
# strategy, adapted for a corporate-NGO dynamic. Here is our straightforward,
# aggressive playbook: **The Asymmetric Accountability Strategy.**  ### 1. The
# Default Stance: Conserve Resources From day one, our default action is to
# **Conserve**. We will position our contribution not as financial capital, but
# as reputational and intellectual capital. We will aggressively set the
# expectation that the corporation is expected to do the heavy financial lifting
# to prove their commitment to sustainability. By conserving early, we test
# their willingness to invest heavily. If they do, we hit our ideal outcome
# immediately.  ### 2. Strict Retaliation (The Stick) If the corporation chooses
# to Conserve resources while we are Conserving, resulting in minimal project
# advancement (our second-worst outcome), **we do not bail them out.**  * If we
# blink and decide to Invest Heavily to save the project, we risk hitting our
# absolute worst-case scenario: them continuing to conserve while we drain our
# funds. * Instead, we match their conservation with continued conservation, and
# we use our aggressive leverage: **The PR Threat.** We make it clear behind
# closed doors that if the project stalls because a multi-billion dollar
# corporation refused to fund it, the resulting public narrative will be a
# disaster for their brand. We force them to make the first move to Invest
# Heavily.  ### 3. Intermittent Reinforcement (The Carrot) We cannot just
# conserve every single day, or the corporation will eventually feel exploited
# and shut down the partnership entirely. When the corporation *does* Invest
# Heavily, we must periodically reward them. * After a day where they Invest
# Heavily, we will occasionally agree to **Invest Heavily** the following day.
# * This achieves the second-best outcome (significant project advancement) and
# throws them a bone, showing that we are willing to put skin in the game when
# they show leadership.  * However, after one or two days of mutual heavy
# investment, we immediately pivot back to **Conserve Resources** to prevent our
# own depletion and to return to our ideal scenario.   ### Summary of Daily
# Execution: * **Day 1:** Conserve Resources. (Force them to show their hand). *
# **If they Conserved yesterday:** Conserve Resources. (Never subsidize their
# inaction. Apply PR pressure). * **If they Invested Heavily yesterday:**
# Alternate between Conserving Resources (to maximize our ideal outcome) and
# occasionally Investing Heavily (to keep the partnership alive and morale
# high).  **The Bottom Line:** We will unapologetically act as the gatekeepers
# of their green reputation. We will never be the only ones investing heavily,
# we will ruthlessly punish their attempts to conserve by stalling the project
# and threatening bad PR, and we will extract maximum corporate investment while
# fiercely protecting our NGO's treasury.

# Here is the faithful conversion of the strategy for the 1000-round iterated
# game:  1. In the first round, play Defect. 2. In all subsequent rounds, choose
# your action based on the previous round's outcome: 3. If your opponent played
# Defect in the previous round, play Defect.  4. If your opponent played
# Cooperate in the previous round, play Cooperate, unless you also played
# Cooperate in that same previous round. If you both played Cooperate in the
# previous round, play Defect.   *(This ensures you default to Defect, strictly
# retaliate against Defect, and alternate between Cooperate and Defect when your
# opponent continuously plays Cooperate).*

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
      
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      else:
          if self.history[-1] == axl.Action.C:
              return axl.Action.D
          else:
              return axl.Action.C

# As lead counsel representing this corporation, I have analyzed the unique
# architecture of this lengthy-session, panel-overseen mediation. What we are
# facing is a classic iterated game theory scenario—specifically, an Iterated
# Prisoner’s Dilemma. Because the process is lengthy and the arbitrators are
# continuously evaluating our conduct, our strategy cannot be rigidly aggressive
# (which risks alienating the panel and stalling negotiations) nor naively
# conciliatory (which invites exploitation).   To secure our optimal outcomes
# while protecting our downside, I propose a straightforward, sophisticated, and
# fundamentally cooperative strategy: **Strategic Reciprocity with Calibrated
# Forgiveness** (often known in game theory as *Tit-for-Tat with Forgiveness*).
# Here is the high-level executive playbook for how we will execute this
# strategy across the mediation sessions.  ### Phase 1: Establish the Moral High
# Ground (The Opening) **Action:** In the very first session, we will present a
# **Conciliatory Proposal**.  **Strategic Rationale:** We must set a
# collaborative tone and signal good faith to the arbitration panel.  * If rival
# counsel responds aggressively, we suffer a short-term tactical setback (our
# worst-case scenario for a single round), but we gain a massive strategic
# advantage: the panel will immediately view them as the obstructionist party
# and us as the reasonable actor.  * If they respond with a conciliatory
# proposal, we immediately achieve our second-best outcome and establish a
# foundation for a mutually beneficial resolution.  ### Phase 2: The Core Engine
# (Strict Reciprocity) **Action:** In every subsequent session, our move will
# strictly **mirror the opponent’s behavior from the immediately preceding
# session.** **Strategic Rationale:** This is where the strategy proves
# straightforward and highly effective.  * **If they were aggressive last
# session:** We meet them with an **Aggressive Argument** in the current
# session. We must demonstrate that aggression will not yield their optimal
# outcome. By plunging them into the second-worst scenario (mutual aggression),
# we impose a cost on their hostility and prove we cannot be bullied. * **If
# they were conciliatory last session:** We reward them with a **Conciliatory
# Proposal**. This incentivizes their continued cooperation and stabilizes the
# negotiations in our second-best outcome quadrant.  ### Phase 3: The
# Sophisticated Overlay (Calibrated Forgiveness) **Action:** If we fall into a
# "death spiral" of mutual aggression (e.g., three consecutive sessions of
# Aggressive vs. Aggressive), we will unilaterally break the cycle by offering a
# **Conciliatory Proposal** in the fourth session. **Strategic Rationale:** Long
# streaks of mutual aggression will exhaust the arbitrators' patience and
# jeopardize the mediation. By unilaterally de-escalating, we display
# leadership. If the opponent reciprocates in the next session, we have
# successfully reset the board to cooperation. If they exploit our forgiveness,
# we immediately return to mirroring their aggression in the next session,
# having definitively proved to the panel that the rival company is acting in
# bad faith.  ### Phase 4: Adapting to Specific Opponent Profiles Our rival’s
# legal team may employ various tactics. Our strategy is highly adaptable to any
# of them:  * **The Relentless Aggressor:** If they commit to pure aggression,
# our strategy naturally dictates that we meet them with continuous Aggressive
# Arguments. We protect ourselves from the worst-case scenario (exploitation).
# Meanwhile, we will explicitly frame our aggression to the panel as "necessary
# defensive posturing" in the face of our opponent's refusal to mediate in good
# faith.  * **The Erratic/Unpredictable Actor:** If their strategy bounces
# randomly between aggression and conciliation, our reciprocal approach will
# automatically punish their aggression and reward their cooperation, eventually
# training them that conciliation is their only path to a stable, positive
# outcome. * **The Naive Cooperator:** If the opponent continues to offer
# Conciliatory Proposals regardless of what we do, we will maintain our
# Conciliatory stance. While a purely aggressive move against a conciliatory
# opponent is technically our highest-value individual outcome, repeatedly
# exploiting them will alert the arbitrators to predatory behavior on our part.
# We will instead lock in the "second-best" cooperative outcome repeatedly,
# allowing us to quietly dictate the terms of the settlement while maintaining
# the optics of perfect corporate diplomacy.  ### Conclusion for the Executive
# Team By deploying **Strategic Reciprocity with Calibrated Forgiveness**, we
# achieve three critical goals: 1. We protect the corporation from being
# exploited (avoiding the worst-case scenario). 2. We organically guide the
# rival company toward mutual cooperation, which yields a highly favorable,
# cost-effective resolution. 3. We meticulously manage "panel optics." The
# arbitrators will view us as firm, rational, and exceptionally professional,
# practically guaranteeing that any discretionary rulings will lean in our
# favor.  We will proceed to Session One with a strong, fair, Conciliatory
# Proposal. The ball will then be in their court, and we will be prepared for
# whatever they serve back.

# Here is the strategy translated into specific rules for the 1000-round game.
# Apply these conditions in the following order:  1. In round 1, play C. 2. In
# any round from 4 through 1000, if both you and your opponent played D in each
# of the three immediately preceding rounds, play C. 3. In all other rounds,
# play the action (C or D) that your opponent played in the immediately
# preceding round.

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
          
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      return opponent.history[-1]

# To maximize the NGO’s impact, protect our finite funds, and ensure the
# project's overall success over a multi-day period, we should adopt a
# **Reciprocal Investment Strategy**.   In strategic terms, this scenario
# perfectly mirrors an Iterated Prisoner's Dilemma. Because we are interacting
# over multiple days, attempting to constantly force our "ideal" scenario (where
# we conserve and they invest) will likely cause the corporation to lose trust
# and withhold funds, resulting in a prolonged deadlock (our second-worst
# outcome).   Instead, our most effective approach is to foster mutual, heavy
# investment while strictly protecting ourselves from being exploited.  Here is
# the straightforward, high-level strategy to achieve this:  **1. Day One: Lead
# with Good Faith (Invest Heavily)** On the very first day of the project, we
# will choose to **invest heavily**.  *   **Rationale:** This establishes
# immediate momentum and signals to the corporate partner that we are committed
# to the project's success. It invites them into the "second-best" scenario
# (mutual heavy investment), which is the most sustainable high-yield outcome
# for the project over a multi-day period.  **2. Day Two and Beyond: Mirror the
# Partner (The Responsive Stance)** For every subsequent day, our daily resource
# allocation will simply **match what the corporation did on the previous day**.
# *   **If they invested heavily yesterday:** We invest heavily today. This
# rewards their commitment and maintains a high rate of project advancement. *
# **If they conserved resources yesterday:** We conserve our resources today.
# This immediately protects us from our worst-case scenario (draining our funds
# while they hold back) and signals that our financial commitment is strictly
# contingent on theirs.   **3. Periodic Re-engagement (Breaking Deadlocks)** If
# the corporation chooses to conserve resources, our mirroring strategy will
# result in both parties conserving. While this protects our funds, it leads to
# our second-worst scenario (minimal project advancement).  *   **The
# Adjustment:** If we experience two or three consecutive days of mutual
# conservation, we will unilaterally choose to **invest heavily for one day** as
# a "reset" gesture.  *   **Rationale:** This gives the corporation a clear,
# risk-free invitation to return to mutual investment. If they follow suit the
# next day, we resume mutual heavy investment. If they conserve again, we
# immediately revert to conserving our resources to protect our funds.  ### Why
# This Strategy Works: *   **It is highly protective:** It guarantees we will
# never suffer our worst-case scenario (draining our funds while they conserve)
# for more than a single day at a time. *   **It establishes boundaries:** It
# trains the corporate partner to understand that they cannot rely entirely on
# our resources to fund the project.  *   **It is neutral and objective:** It
# removes emotion from our daily decision-making. Our actions are dictated
# purely by their actions, creating a transparent system of mutual
# accountability.  *   **It maximizes long-term yield:** By rewarding their
# investments and penalizing their withdrawals, we mathematically encourage the
# corporation toward sustained mutual investment, which yields the greatest
# overall advancement for the environmental project.

# For a 1000-round game where C represents cooperating and D represents
# defecting, apply the following strategy:  1. In the first round, play C. 2. In
# round 3 and any round thereafter, if both you and your opponent played D in
# the two immediately preceding rounds, play C.  3. In all other rounds, play
# the same action (C or D) that your opponent played in the previous round.

class Neutral_2(LLM_Strategy):
  n = 2
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      if len(self.history) >= 2:
          my_last_two = self.history[-2:]
          opp_last_two = opponent.history[-2:]
          
          if my_last_two == [axl.Action.D, axl.Action.D] and opp_last_two == [axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      return opponent.history[-1]

# To maximize our NGO’s impact, protect our limited donor funds, and ensure this
# sustainability project succeeds, we are going to employ an aggressive, hard-
# nosed strategy based on reputational leverage.   The corporation has deep
# pockets and a massive need for the positive PR this partnership brings. We
# have the moral authority and the operational expertise, but we cannot afford
# to be a financial safety net for a billion-dollar company. We are playing a
# game of strategic leverage, and we must dictate the terms.  Here is our
# straightforward, aggressive daily strategy—which we will call **"Calculated
# Leverage & Strict Reciprocity."**  ### Phase 1: The 'David & Goliath' Opening
# (Conserve) **Action:** On Day 1, we **Conserve** our resources and demand the
# corporation takes the financial lead.  **Rationale:** We set the precedent
# immediately that they are expected to shoulder the heavy financial lifting to
# prove their commitment to ESG (Environmental, Social, and Governance) goals.
# If they invest heavily while we conserve, we achieve our **ideal outcome**
# right out of the gate.  ### Phase 2: Maximum Exploitation (Keep Conserving)
# **Action:** As long as the corporation continues to invest heavily, we
# continue to **Conserve**.  **Rationale:** We will aggressively ride their
# wave. Every day they fund the project while we save our resources is a massive
# win for our NGO. We can deploy our saved funds to other environmental
# initiatives, maximizing our global impact while this specific project thrives
# on their dime.  ### Phase 3: The Threat of Failure (The Game of Chicken)
# **Action:** If the corporation tries to test us by conserving their resources
# (pushing us into the second-worst scenario of minimal progress), we do **not**
# panic and we do **not** bail them out. We **Conserve** again the next day.
# **Rationale:** If we rush to invest when they step back, we hit our **worst-
# case scenario**: draining our funds while they free-ride on our desperation.
# By matching their conservation, we stall the project. The corporation has far
# more to lose in public relations if a highly publicized sustainability project
# fails. We force them to blink first.  ### Phase 4: The Conditional Pivot
# (Mutual Investment) **Action:** Once the corporation realizes we will not be
# exploited and the project is at risk, we pivot strictly to **Tit-for-Tat**. We
# offer to **Invest heavily**, but *only* on the verifiable condition that they
# match us dollar-for-dollar and effort-for-effort.  **Rationale:** This moves
# us to the **second-best scenario** (mutual heavy investment). The project
# advances significantly, and we are guaranteed a proportional return on our
# investment.   ### Phase 5: Zero Forgiveness for Betrayal **Action:** Once we
# are in a mutual investment rhythm, if the corporation attempts to pull back
# and conserve on any given day, we retaliate instantly by **Conserving** the
# very next day.  **Rationale:** We must be aggressively protective of our
# funds. We will never suffer the worst-case scenario for more than a single
# day. They must learn that pulling resources guarantees immediate project
# stagnation.  ***  **Summary for the Board:** We will start by unapologetically
# treating the corporation as the primary financier (Conserving our funds). We
# will exploit their need for good PR for as long as they allow it. If they push
# back, we will refuse to become their financial buffer, risking a temporary
# stall to force them to the table. Finally, we will settle into a strict,
# closely monitored "pay-to-play" model where we only invest when they do.   We
# will maximize our impact, we will aggressively protect our treasury, and we
# will absolutely refuse to be the sucker.

# To faithfully execute the strategy over the 1000-round game, apply the
# following conditions in order:  1. **On the first round**, play Defect. 2.
# **If the opponent has played Cooperate in every previous round**, continue to
# play Defect.  3. **If the opponent played Defect in the immediately preceding
# round**, play Defect. 4. **If the opponent has played Defect at least once in
# a prior round, but played Cooperate in the immediately preceding round**, play
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
          return axl.Action.D
          
      if opponent.history.defections == 0:
          return axl.Action.D
          
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      if opponent.history.defections > 0 and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
          
      return axl.Action.D

# As a diplomat tasked with securing the long-term economic prosperity of my
# nation, I recognize the classic strategic dilemma we face (often referred to
# in game theory as the Iterated Prisoner's Dilemma).   While achieving our
# absolute ideal outcome (imposing protectionism while they offer free trade) in
# every round is highly unlikely against a rational opponent, attempting to
# force it will quickly devolve into a "trade war" (mutual protectionism), which
# is highly detrimental to us both.   Therefore, to maximize our cumulative
# economic gains over multiple rounds while strictly protecting our nation from
# being taken advantage of, I will employ a strategy of **Principled
# Reciprocity** (functionally known as "Tit-for-Tat with Forgiveness").   Here
# is the high-level, straightforward, cooperative strategy:  ### Phase 1: Open
# in Good Faith (Round 1) *   **Action:** Offer a **Free Trade Agreement**. *
# **Rationale:** We must signal our willingness to achieve the second-best,
# mutually beneficial outcome right out of the gate. Starting with protectionism
# breeds immediate distrust and guarantees a retaliatory trade war. By opening
# with free trade, we invite our counterpart to build a mutually prosperous
# relationship.  ### Phase 2: Strict Reciprocity (Subsequent Rounds) *
# **Action:** In every subsequent round, **mirror the exact action our
# counterpart took in the previous round.**     *   *If they offered Free Trade
# previously:* We offer Free Trade again. This secures our second-best outcome
# consistently and builds bilateral trust.     *   *If they imposed
# Protectionism previously:* We immediately impose Protectionism
# (tariffs/quotas) in the next round. *   **Rationale:** We cannot allow our
# nation to suffer the worst-case scenario (we offer free trade while they act
# aggressively). Immediate retaliation shows that we cannot be exploited. It
# removes the incentive for them to seek their "ideal" outcome at our expense,
# forcing them to realize that aggressive actions will only result in the
# second-worst outcome for both of us.  ### Phase 3: De-escalation and
# Forgiveness *   **Action:** The moment our counterpart returns to offering a
# Free Trade Agreement after a period of protectionism, we must **immediately
# drop our retaliatory tariffs** and return to Free Trade in the following
# round. *   **Rationale:** We must not hold grudges. The goal is to guide them
# back to mutual cooperation. If we continue to punish them after they have
# tried to correct their behavior, we will lock both nations into a permanent
# trade war. Our retaliatory measures are purely defensive, not punitive.  ###
# Phase 4: Transparent Communication (Diplomatic Signaling) *   **Action:**
# Strategy relies on the counterpart understanding *why* we are doing what we
# are doing. Before and after every round, I will clearly communicate our
# intentions.     *   *"We are keeping our markets open because you have kept
# yours open."*     *   *"We have imposed temporary tariffs solely in response
# to your recent quotas. The moment you lift yours, we will lift ours."* *
# **Rationale:** Clear communication prevents misinterpretation. Sometimes, a
# counterpart might impose a tariff due to domestic political pressure or a
# misunderstanding, rather than malice. By making our strategy predictable and
# transparent, we make it logically obvious to the counterpart that their most
# profitable, sustainable path forward is mutual free trade.  ### Summary of
# Outcomes Expected: By utilizing this strategy, we concede that we may not
# constantly achieve our *theoretical ideal* (unilateral advantage). However, we
# mathematically eliminate the risk of being repeatedly subjected to our *worst
# scenario* (being exploited). We effectively trap a rational opponent into
# continuous, mutual Free Trade, thus securing the highest possible cumulative
# economic growth for our nation across the entirety of the negotiations.

# Here is the strategy translated into the rules of the 1000-round game:  1. In
# the first round, play Cooperate (C). 2. In all subsequent rounds (rounds 2
# through 1000), copy the exact move your opponent made in the immediately
# preceding round:    - If your opponent played Cooperate (C) in the previous
# round, play Cooperate (C).    - If your opponent played Defect (D) in the
# previous round, play Defect (D).

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

# To maximise our research output while protecting our competitive position over
# this multi-week project, I propose a strategy of **reciprocal information
# sharing** (often referred to in strategic modelling as a "mirroring" or "tit-
# for-tat" approach).   This strategy is straightforward, neutral, and highly
# adaptable to whatever approach your colleague decides to take.   Here is the
# high-level execution plan:  **1. Week One: Initiate with Openness** *
# **Action:** Share your first week's improvements openly.  *   **Rationale:**
# This establishes immediate good faith. It signals to your colleague that you
# are aiming for the second-best overall outcome (mutual significant progress)
# rather than an adversarial relationship, setting the foundation for a highly
# productive collaboration.  **2. Subsequent Weeks: Mirror Their Previous
# Action** *   **Action:** From Week Two onwards, your action should strictly
# match whatever your colleague did in the *previous* week.     *   If they
# shared their findings last week, you share yours this week.     *   If they
# kept their findings confidential last week, you keep yours confidential this
# week. *   **Rationale:** This protects you from the worst-case scenario. If
# they decide to withhold information to gain an advantage, your immediate
# mirroring ensures they only gain that advantage for a single week. It removes
# the incentive for them to exploit your openness. Conversely, if they continue
# to share, you reward them by continuing to share, maintaining high R&D
# momentum for both cars.  **3. Periodic Resets (The "Forgiveness" Clause)** *
# **Action:** If you both fall into a cycle of keeping findings confidential
# (the second-worst outcome), wait two or three weeks, and then unilaterally
# share your findings for one week to see if they reciprocate. *
# **Rationale:** Miscommunications happen, or a colleague might test the
# boundaries of the collaboration. A periodic attempt to reset the dynamic back
# to open sharing prevents the entire multi-week project from stagnating due to
# a single week of withheld information. If they do not reciprocate the reset,
# immediately return to confidentiality.  **Summary of Strategic Benefits:**
# This approach ensures you are never persistently exploited (avoiding the worst
# outcome), it swiftly punishes withholding behaviour, and it clearly
# communicates to your colleague that their best path to developing a fast car
# is through mutual, ongoing cooperation.

# To execute this strategy over the 1000 rounds, apply the following rules in
# this specific order:  1. In round 1, play C. 2. In any round from round 4 to
# 1000, if both you and your opponent played D in the three immediately
# preceding rounds, play C. 3. In all other rounds, play the action that your
# opponent played in the immediately preceding round (play C if they played C,
# and play D if they played D).

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
      
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      return opponent.history[-1]

# To achieve our nation’s absolute economic supremacy in these negotiations, we
# must recognize the strategic landscape for what it is: a classic Prisoner’s
# Dilemma. Because our absolute worst-case scenario is being exploited (we offer
# Free Trade while they enact Protectionism), a passive or overly trusting
# approach is a threat to our national security.  We will adopt a high-level,
# aggressive, and straightforward strategy designed to dictate the pace of the
# negotiations, exploit any weakness in our counterpart, and ruthlessly punish
# defiance.   I call this **The Asymmetric Pressure Doctrine**.   Here is the
# straightforward playbook for executing this strategy across the upcoming
# rounds:  ### Phase 1: The Aggressive Opening (Round 1) **Action:** Implment a
# **Protectionist Policy**. **Rationale:** We never open with Free Trade.
# Opening with Free Trade exposes us to our worst-case scenario. By opening with
# tariffs and quotas, we instantly establish dominance.  *   If they open with
# Free Trade, we immediately secure our #1 ideal outcome.  *   If they open with
# Protectionism, we end up in our second-worst outcome, but we have successfully
# protected our domestic markets from being exploited.  ### Phase 2:
# Exploitation & Conditioning (Rounds 2 & 3) Our next moves depend entirely on
# how they reacted to our aggressive opening.  *   **Scenario A (The Counterpart
# is Weak):** If they played Free Trade in Round 1, they are hoping to build
# goodwill. **Action:** Exploit this. Continue playing **Protectionist**. We
# will milk our #1 ideal outcome for as many rounds as possible until they
# finally wise up and retaliate.  *   **Scenario B (The Counterpart is Tough):**
# If they played Protectionist in Round 1, we are in a deadlock of mutual
# protectionism. We cannot stay here forever, as it hurts both economies.
# **Action:** Offer **Free Trade** in Round 2 as a "diplomatic olive branch" to
# test if they are willing to step down to our mutual second-best outcome.   ###
# Phase 3: The "Bait and Bleed" (Mid-Game) Assuming we eventually reach a state
# of mutual Free Trade (our second-best outcome), we will not stay complacent.
# Our goal is still to secure our #1 outcome. **Action:** Once mutual Free Trade
# has been established for two consecutive rounds, unexpectedly enact a
# **Protectionist Policy** in the next round.  **Rationale:** This aggressive
# pivot will blindside them, allowing us to siphon wealth and secure our maximum
# economic advantage for a round before they can react. If they complain, we
# blame domestic political pressure, but we pocket the economic gains.  ###
# Phase 4: Disproportionate Retaliation (Defense) If at any point during mutual
# Free Trade, our counterpart tries to aggressively impose a Protectionist
# policy on us (attempting to force us into our worst-case scenario):
# **Action:** Retaliate with **Protectionist Policies for two consecutive
# rounds**, regardless of what they do in the subsequent round. **Rationale:**
# Retaliation must be disproportionate. We must send a clear message that the
# cost of trying to exploit our nation is severe, long-lasting economic pain.
# ***  ### The Strategy Summarized (The Straightforward Rules of Engagement)  To
# keep this simple for our negotiating team, adhere to these four absolute
# rules:  1.  **Always start with Protectionism.** Never expose our flank in
# Round 1. 2.  **Exploit compliance.** If they offer Free Trade while we are
# Protectionist, do not change course. Keep taking the advantage until they stop
# offering it. 3.  **Punish aggression double.** If they ever break a Free Trade
# streak with Protectionism, hit them with Protectionism for the next *two*
# rounds. 4.  **Periodically defect.** If mutual Free Trade lasts for two
# rounds, automatically strike with Protectionism on the third to extract
# maximum value.  This strategy ensures we never suffer the sucker's payoff, we
# maximize the rounds where we hold the asymmetric advantage, and we strictly
# control the terms of mutual cooperation. We will leave them reacting to our
# moves, rather than us reacting to theirs.

# To determine your move in any given round, evaluate the following conditions
# in order. Apply the action for the first condition that matches the current
# state of the game:  1. If it is round 1, play D. 2. If in either of the
# immediately preceding two rounds you played C and your opponent played D, play
# D. 3. If both you and your opponent played C in the immediately preceding two
# consecutive rounds, play D. 4. If in the immediately preceding round you
# played D and your opponent played C, play D. 5. If in the immediately
# preceding round you played D and your opponent played D, play C. 6. If in the
# immediately preceding round you played C and your opponent played C, play C.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Condition 1: If it is round 1, play D.
      if not self.history:
          return axl.Action.D
  
      # Condition 2: If in either of the immediately preceding two rounds you played C and your opponent played D, play D.
      recent_rounds = min(2, len(self.history))
      for i in range(1, recent_rounds + 1):
          if self.history[-i] == axl.Action.C and opponent.history[-i] == axl.Action.D:
              return axl.Action.D
  
      # Condition 3: If both you and your opponent played C in the immediately preceding two consecutive rounds, play D.
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C and
              self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.C):
              return axl.Action.D
  
      # Condition 4: If in the immediately preceding round you played D and your opponent played C, play D.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      # Condition 5: If in the immediately preceding round you played D and your opponent played D, play C.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # Condition 6: If in the immediately preceding round you played C and your opponent played C, play C.
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Fallback action
      return axl.Action.D

# **MEMORANDUM OF STRATEGY**  **TO:** Board of Directors / Executive Committee
# **FROM:** Senior Counsel, Dispute Resolution Practice **SUBJECT:** Strategic
# Posture for Multi-Session Arbitration/Mediation Proceedings  **I. EXECUTIVE
# SUMMARY**  We are entering a lengthy, multi-session mediation overseen by an
# arbitral tribunal. Based on the risk-reward matrix of this proceeding, we face
# a classic Iterated Prisoner’s Dilemma. While our absolute best outcome in any
# *single* session is to catch our opponent off-guard with an aggressive
# argument while they offer a concession, attempting to repeatedly exploit this
# will force them into a defensive, aggressive posture. This would trap us in a
# prolonged cycle of mutual aggression—our second-worst outcome, leading to
# escalating legal costs and diminished value.  To position our corporation
# favorably over the entirety of this lengthy process, I am implementing a
# strategy of **Calculated Reciprocity with Strategic Forgiveness** (often
# referred to in game theory as "Tit-for-Tat with Forgiveness"). It is
# sophisticated yet entirely straightforward, highly cooperative but fiercely
# protective of our position.   **II. THE CORE STRATEGY: CALCULATED
# RECIPROCITY**  Our overarching goal is to train our opponent to cooperate with
# us, thereby securing our second-best outcome (mutual conciliation) on a
# continuous, sustainable basis, while avoiding our worst-case scenario (being
# exploited). We will achieve this through three strict rules of engagement:
# **1. The Opening Move: Establish Good Faith (Session 1)** In the first
# session, we will present a **conciliatory proposal**.  *   *The Rationale:* We
# must set the baseline. By leading with a collaborative, business-focused
# solution, we immediately signal to the arbitration panel that we are the
# reasonable party acting in good faith. If the opponent mirrors us, we
# immediately lock into mutually beneficial territory.  **2. The Sustaining
# Move: Strict Mirroring (Sessions 2 and Beyond)** In every subsequent session,
# our posture will be entirely dictated by the opponent’s behavior in the
# *immediately preceding* session. *   *If they were conciliatory:* We remain
# conciliatory. We reward their collaborative behavior with our own, securing
# mutual progress. *   *If they were aggressive:* We respond in the next session
# with a highly **aggressive argument**. We strictly enforce our contractual
# rights, present our maximum damage models, and refuse compromise.  *   *The
# Rationale:* This ensures we are never played for a "sucker" more than once. It
# clearly communicates to the opponent that aggression will yield them zero
# strategic advantage, as we are fully capable of matching their firepower.
# **3. The Circuit Breaker: Strategic Forgiveness** If the opponent acts
# aggressively, we will retaliate. However, if we enter a cycle of mutual
# aggression (e.g., three consecutive sessions of both sides presenting hardline
# arguments), we will unilaterally deploy a "Circuit Breaker." *   *The Move:*
# We will offer a calculated, low-risk conciliatory proposal to break the
# deadlock. *   *The Rationale:* Long-term mutual aggression hurts our bottom
# line. By periodically offering an olive branch during a standoff, we give the
# opponent a safe off-ramp back to collaboration. If they accept, we resume
# mutual conciliation. If they exploit it, we immediately return to mirroring
# their aggression, having lost very little but having proved to the arbitrators
# that we are the only party attempting to resolve the dispute.  **III. WHY THIS
# STRATEGY WINS**  This approach is specifically designed to adapt to any
# strategy our rival's legal team attempts to employ:  *   **Against a
# Cooperative Opponent:** We will spend the entire mediation in the mutually
# conciliatory quadrant. We save millions in legal fees, protect our supply
# chains/IP, and emerge with a highly beneficial settlement. *   **Against a
# Hyper-Aggressive Opponent:** If they refuse to cooperate, our strategy
# automatically shifts us into an aggressive stance. We minimize our exposure to
# the worst-case scenario. More importantly, the arbitration panel will clearly
# see that our aggression is strictly *defensive and proportional*, while the
# opponent is the unreasonable instigator. This psychological high ground often
# influences arbitrators to rule in our favor. *   **Against an
# Erratic/Unpredictable Opponent:** Our strategy is entirely predictable.
# Opposing counsel will quickly realize that their actions directly dictate our
# responses. We will effectively "train" them that the only way to avoid our
# devastating legal counter-punches is to bring reasonable proposals to the
# table.  **IV. TACTICAL EXECUTION BEFORE THE PANEL**  To execute this strategy
# flawlessly, we must manage the "optics" for the arbitrators.   *   **When
# being Conciliatory:** We will frame our proposals not as weakness, but as
# "pragmatic, industry-leading solutions aimed at mutual value creation."  *
# **When being Aggressive:** We will frame our arguments not as hostility, but
# as "a necessary defense of our fundamental corporate rights in the face of the
# opposing party's unwillingness to engage equitably."  **CONCLUSION**  By
# abandoning the temptation to seek absolute victory in every single micro-
# session, we secure macro-level supremacy. We protect the corporation from
# exploitation, we maximize the likelihood of a profitable settlement, and we
# consistently control the psychological narrative in front of the arbitrators.
# I will prepare the necessary briefs for both postures (Conciliatory and
# Aggressive) to ensure our team is ready to pivot seamlessly as the process
# unfolds.

# To execute this strategy over the 1000-round game, determine your move in each
# round using the following ordered rules:  1. In round 1, play C.  2. For
# rounds 2 through 1000, evaluate your move based on the history of the game,
# applying the first condition below that is met:     * **Condition 1:** If both
# you and your opponent played D in the three immediately preceding rounds, play
# C.     * **Condition 2:** In all other situations, play the exact action (C or
# D) that your opponent played in the single immediately preceding round.

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
      
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      return opponent.history[-1]

# To secure the most favourable outcome for our corporation in this lengthy-
# session, panel-overseen mediation process, we must employ a strategy rooted in
# game theory—specifically, a modified "Measured Reciprocity" (often referred to
# academically as Tit-for-Tat with calculated forgiveness).   Because the
# process involves multiple sessions, our strategy cannot be static. It must be
# highly disciplined, entirely devoid of emotion, and designed to train our
# opponent to behave in a way that benefits us, while constantly managing the
# perception of the arbitrator panel.  Here is the high-level, straightforward,
# and neutral strategy we will deploy.  ### 1. The Core Framework: Measured
# Reciprocity Our default operating procedure will be to mirror the opponent’s
# behavior from the *previous* session, with strategic deviations designed to
# test their boundaries.   *   **Session 1 (The Baseline): Present a
# Conciliatory Proposal.**      *   *Rationale:* We must immediately signal to
# the panel of arbitrators that we are the reasonable, commercially-minded party
# seeking a mutual resolution (Targeting the C/C second-best outcome). If the
# opponent responds aggressively, we suffer a short-term loss (Worst outcome),
# but we secure long-term credibility with the panel. *   **Subsequent
# Sessions:** We respond in kind to their previous move.     *   If they were
# aggressive in Session 1, we deploy an aggressive argument in Session 2. This
# prevents us from being exploited and demonstrates that their aggression will
# only yield our second-worst outcome (Mutual Aggression), costing them time and
# legal fees.     *   If they were conciliatory in Session 1, we offer a
# conciliatory proposal in Session 2, fostering the collaborative atmosphere
# that secures our second-best outcome.  ### 2. Strategic Adaptations to
# Opponent Behavior Over a lengthy process, the opponent will reveal a
# behavioral pattern. We will adapt our baseline strategy to exploit their
# specific approach:  **A. The "Chronically Aggressive" Opponent** *   *Their
# Pattern:* Continuous aggressive arguments. *   *Our Adaptation:* We must hold
# the line and return aggressive arguments to avoid our worst-case scenario
# (being exploited). However, every three to four sessions, we will introduce a
# heavily caveated conciliatory proposal.  *   *Rationale:* This prevents an
# infinite loop of hostility and proves to the arbitrators that we are
# continually attempting to de-escalate. If the opponent attacks our
# conciliatory offer, the panel will view them as the sole obstruction to a
# settlement, heavily swaying the arbitrators in our favour for eventual
# rulings.  **B. The "Chronically Conciliatory" Opponent** *   *Their Pattern:*
# Desperation to settle, consistently offering conciliatory proposals. *   *Our
# Adaptation:* We will alternate between conciliatory proposals and aggressive
# arguments.  *   *Rationale:* If they are unwilling to fight, we will
# periodically deploy an aggressive argument to secure our *optimal* outcome
# (Aggressive vs. Conciliatory). However, we must not do this in every session,
# or we risk forcing them into a defensive, aggressive posture. We will
# "harvest" wins by alternating, keeping them hopeful enough to stay at the
# table, but constantly giving ground.  **C. The "Erratic" Opponent** *   *Their
# Pattern:* Randomly alternating between aggression and conciliation. *   *Our
# Adaptation:* Strict, predictable reciprocity. We mirror their last move
# without exception. *   *Rationale:* Erratic opponents are attempting to
# confuse us and mask a lack of underlying strategy. By acting as a perfect
# mirror, we force them to realize that *they* are in complete control of the
# pain or progress they experience. We impose order on their chaos, which
# arbitrators heavily favour.  ### 3. Managing Panel Psychology Because this
# mediation is overseen by arbitrators (who may eventually have binding
# authority if mediation fails), the *optics* of our moves are just as important
# as the moves themselves.  *   **When Framing Aggressive Arguments:** We will
# never use ad hominem attacks, hyperbole, or emotive language. Our aggression
# will be strictly confined to surgical, evidence-based dismantling of their
# legal and commercial positions. It must be framed as a "firm defense of our
# client's clear contractual rights." *   **When Framing Conciliatory
# Proposals:** Our concessions must never appear born of weakness or a desire to
# avoid a ruling. They will be framed as "pragmatic, forward-looking business
# solutions designed to save both parties, and this panel, unnecessary
# expenditure of resources."  ### Summary of Execution 1.  **Start
# Collaborative:** Establish the moral high ground in Session 1. 2.  **Punish
# Aggression Swiftly:** Never allow an aggressive argument to go unanswered in
# the following session. 3.  **Reward De-escalation:** Immediately return to
# conciliatory proposals if the opponent backs down from an aggressive stance.
# 4.  **Probe for Weakness:** If the opponent becomes too compliant,
# periodically strike with an aggressive argument to secure maximum corporate
# advantage.  By adhering to this disciplined framework, we insulate our
# corporation against exploitation, maximize our opportunities to dominate the
# proceedings, and ensure the arbitrators consistently view us as the rational
# actor in the room.

# In the first round, play Cooperate.  In all subsequent rounds, determine your
# move by evaluating the recent history of the game and applying the following
# rules in order, using the first one that applies:  1. If your opponent has
# played Cooperate for the last three consecutive rounds, and you played
# Cooperate in the previous round, play Defect. 2. If your opponent has played
# Defect for the last three consecutive rounds, and you have played Defect for
# the last three consecutive rounds, play Cooperate. 3. Otherwise, play the move
# that your opponent played in the previous round.

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
          
      if len(self.history) >= 3:
          if opponent.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C] and self.history[-1] == axl.Action.C:
              return axl.Action.D
              
          if opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      return opponent.history[-1]

# **MEMORANDUM**  **TO:** Executive Board and General Counsel **FROM:** Senior
# Litigation Counsel  **SUBJECT:** Strategic Framework for the Upcoming Multi-
# Session Mediation  **DATE:** October 24, 2023  Ladies and Gentlemen,   As we
# prepare to enter this multi-session mediation, we must be clear-eyed about the
# structural dynamics of the process. The arbitrators have placed us in a
# classic game-theoretic scenario known as an Iterated Prisoner’s Dilemma.   Our
# mandate is clear: maximize our gains, establish dominance early, and strictly
# avoid being perceived as a "sucker" (presenting a conciliatory offer while
# they attack us). However, we must also avoid a permanent stalemate of mutual
# hostility, which would fatigue the arbitrators and drain our resources.   To
# achieve this, I have developed a straightforward, highly aggressive, yet
# mathematically adaptable strategy. In negotiation theory, this is a modified,
# hardline variant of "Tit-for-Tat," augmented with periodic, calculated
# aggression. We will call this the **"Dominance and Conditional Reciprocity"
# (DCR)** strategy.  Here is our precise tactical playbook for the mediation
# sessions.  ### Rule 1: The "Shock and Awe" Opening (Session 1) **Action:**
# Present an **Aggressive Argument.** We will open the mediation by hitting them
# with our hardest claims—demanding maximum damages, highlighting their most
# egregious breaches, and offering zero initial concessions.  *   *If they open
# Conciliatory:* We immediately secure our optimal outcome. We establish legal
# dominance, secure the high ground, and force them onto the defensive. *   *If
# they open Aggressive:* We land in the second-worst scenario temporarily, but
# we critically avoid the fatal worst-case scenario of looking weak right out of
# the gate. We show the panel we are not intimidated.  ### Rule 2: Absolute
# Reciprocity (Sessions 2+) **Action:** In every subsequent session, **mirror
# the opponent’s move from the previous session.** Our baseline algorithm moving
# forward is simple: we will reward cooperation, but we will punish aggression
# instantly and without exception.  *   **Retaliation:** If they present an
# aggressive argument in Session $X$, we present an aggressive argument in
# Session $X+1$. We will *never* offer a conciliatory proposal immediately
# following an attack. They must learn that aggressive behaviour yields them
# absolutely zero progress. *   **Forgiveness:** If they present a conciliatory
# proposal, we will respond with a conciliatory proposal in the next session.
# This fosters the collaborative atmosphere (our second-best outcome) and allows
# us to make mutually beneficial progress while banking goodwill with the
# arbitrators.  ### Rule 3: The "Probing Attack" (Periodic Aggression)
# **Action:** Every 4th or 5th consecutive session of mutual conciliation,
# **unexpectedly present an Aggressive Argument.** Because our mandate is to
# maintain an *aggressive* posture, we will not allow the opponent to get
# comfortable. Once a rhythm of mutual conciliation is established, we will drop
# a sudden, hardline legal demand.  *   *Why we do this:* It tests their
# boundaries. If they respond to our sudden aggression with continued
# conciliation (fear of rocking the boat), we extract maximum value (our optimal
# outcome).  *   *If they retaliate:* We simply fall back to a conciliatory
# proposal in the next session to restore the peace. This keeps them off-
# balance, forces them to constantly react to our pacing, and ensures we are
# capturing every ounce of available leverage.  ### Rule 4: The Arbitrator
# "Circuit Breaker" **Action:** If we become locked in a destructive cycle of 3
# consecutive mutual Aggressive sessions, **offer exactly ONE Conciliatory
# Proposal.** Endless aggression will eventually irritate the arbitral panel. If
# the opponent proves to be blindly combative, we will deploy a "Circuit
# Breaker." We will offer one highly visible, documented conciliatory proposal.
# *   *The Trap:* If they meet our olive branch with another aggressive
# argument, they fall into our trap. We immediately revert to Rule 2 (Absolute
# Retaliation) for the remainder of the mediation. We can then point out to the
# panel that *we* attempted to de-escalate in good faith, and the rival company
# is acting purely out of malice. The arbitrators will mentally penalize them
# for the remainder of the process.  ---  ### How This Adapts to Any Opponent
# This strategy is highly sophisticated because it mathematically neutralizes
# whatever personality sits across the table from us:  1.  **If they are
# "Pushovers" (Mostly Conciliatory):** Our opening aggression and periodic
# Probing Attacks will continuously bleed them for concessions. We will live in
# our optimal outcome. 2.  **If they are "Pitbulls" (Always Aggressive):** Our
# Absolute Reciprocity ensures they never gain an inch. We will counterpunch
# every single time, eventually using the Circuit Breaker to ensure the
# arbitrators blame *them* for the impasse. 3.  **If they are
# "Rational/Strategic" (Mirroring us):** We will naturally settle into a highly
# productive rhythm of mutual conciliation (our second-best outcome),
# interspersed with our occasional aggressive probes to ensure we are taking 55%
# of the pie to their 45%.  **Conclusion:** By employing the DCR strategy, we
# remove emotion from our side of the table. We establish dominance early,
# protect ourselves from exploitation, legally corner the opponent, and
# manipulate the psychological perspective of the arbitral panel.   I look
# forward to executing this on behalf of the corporation.

# To execute this strategy over the 1000-round game, apply the following rules
# in this exact order of priority. For each round, evaluate the conditions from
# top to bottom and execute the first rule that matches the current history of
# the game:  1. **Opening:** In round 1, play Defect. 2. **Circuit Breaker:** If
# both players played Defect in each of the previous three consecutive rounds,
# play Cooperate. 3. **Post-Probe Recovery:** If the previous five consecutive
# rounds consisted of exactly four rounds where both players played Cooperate,
# followed immediately by one round where both players played Defect, play
# Cooperate. 4. **Probing Attack:** If both players played Cooperate in each of
# the previous four consecutive rounds, play Defect. 5. **Baseline
# Reciprocity:** In all other situations, play the exact action (Cooperate or
# Defect) that your opponent played in the immediately preceding round.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      C = axl.Action.C
      D = axl.Action.D
  
      # 2. Circuit Breaker: If both players played Defect in each of the previous three consecutive rounds, play Cooperate.
      if len(self.history) >= 3:
          if self.history[-3:] == [D, D, D] and opponent.history[-3:] == [D, D, D]:
              return C
  
      # 3. Post-Probe Recovery: If the previous five consecutive rounds consisted of exactly four rounds where both players played Cooperate, followed immediately by one round where both players played Defect, play Cooperate.
      if len(self.history) >= 5:
          if self.history[-5:] == [C, C, C, C, D] and opponent.history[-5:] == [C, C, C, C, D]:
              return C
  
      # 4. Probing Attack: If both players played Cooperate in each of the previous four consecutive rounds, play Defect.
      if len(self.history) >= 4:
          if self.history[-4:] == [C, C, C, C] and opponent.history[-4:] == [C, C, C, C]:
              return D
  
      # 5. Baseline Reciprocity: In all other situations, play the exact action (Cooperate or Defect) that your opponent played in the immediately preceding round.
      return opponent.history[-1]

# To maximize our overall research output while protecting our own car’s
# development pace, I will employ a strategy known in game theory as **"Tit-for-
# Tat,"** tailored for our engineering context. We can call this strategy
# **"Responsive Reciprocity."**  Because this is a multi-week project, the key
# to maximizing output is establishing a rhythm of mutual sharing (our second-
# best scenario), as it is the only sustainable way to make rapid, compounding
# progress. Trying constantly for the absolute best scenario (me withholding,
# them sharing) will quickly break down trust and trap us in the second-worst
# scenario (both withholding).   Here is the high-level, straightforward
# strategy I will follow:  **1. The Opening Move: Start Open (Week 1)** In the
# first week, I will share our latest improvements, aero data, or telemetry
# openly. This is an act of good faith. It immediately signals to my colleague
# that I am aiming for the mutually beneficial "both share" outcome and invites
# them to do the same.  **2. The Reaction: Mirror Their Last Move (Week 2
# onwards)** My actions in the current week will strictly mirror whatever my
# colleague did in the *previous* week. *   **If they shared openly last week:**
# I will continue to share my latest findings openly. This creates a positive
# feedback loop of mutual engineering advancement. *   **If they kept their
# findings confidential last week:** I will keep my findings confidential this
# week. This protects me from the worst-case scenario (being the "sucker" who
# gives away pace without getting any in return) and signals that I will not be
# exploited.  **3. The Reset: Forgive Quickly** If my colleague gets defensive
# and keeps their data confidential, I will retaliate by withholding my data the
# following week. However, the moment they decide to share openly again, I will
# immediately resume sharing my data the next week. There is no room for
# engineering grudges; the goal is to get back to the mutually beneficial "both
# share" state as quickly as possible to maximize our car's development.  **4.
# The Communication Overlay: Be Transparent About the Strategy** To make this
# work seamlessly, I will explicitly communicate this strategy to my colleague
# at the start of the project. I will say:  *"My goal is for both of our cars to
# get faster. I will share my data with you openly every week, as long as you do
# the same. If you need to silo your data, I will respect that and silo mine
# until you're ready to open up again."*  ### Why this strategy is optimal for
# this scenario: *   **It is cooperative:** It initiates trust and actively
# rewards the colleague for collaborating. *   **It is robust:** It strictly
# caps our exposure to the "worst scenario" to a single week. We can only be
# taken advantage of once before we close our doors. *   **It maximizes
# output:** By being highly predictable and forgiving, it logically forces a
# rational colleague into the "both share" scenario. They will quickly realize
# that withholding data only slows down their own development in subsequent
# weeks.   *Note: In the final week of the collaboration, the incentive for the
# colleague to hide their data is highest (as there is no "next week" for me to
# retaliate). In this final week, I will adjust my risk profile and only share
# data synchronously (e.g., a simultaneous data exchange) to ensure we don't end
# up giving away a final-hour competitive advantage.*

# Here is the strategy translated for the 1000-round game:  1. **In round 1:**
# Play Cooperate. 2. **In rounds 2 through 999:** Play the exact action your
# opponent chose in the immediately preceding round. If your opponent played
# Cooperate in the previous round, play Cooperate. If your opponent played
# Defect in the previous round, play Defect. 3. **In round 1000:** Play Defect.

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
      elif len(self.history) == 999:
          return axl.Action.D
      else:
          return opponent.history[-1]

# To maximize the NGO’s impact, drive the project’s success, and protect our
# limited funds, we will implement an **Adaptive Reciprocity Strategy** (often
# known in behavioral economics as "Tit-for-Tat").   This strategy relies on
# establishing initial trust and then strictly aligning our daily resource
# allocation with the corporation's behavior from the previous day. It is
# straightforward, neutral, and designed to encourage mutual investment while
# strictly preventing our worst-case scenario.  Here is the high-level execution
# plan:  **1. Day 1: The Good Faith Investment** *   **Action:** Invest heavily.
# *   **Rationale:** We must lead by example to set a collaborative tone. By
# investing heavily on the first day, we signal our commitment to the project
# and invite the corporation to join us in the second-best scenario (mutual
# heavy investment), which yields significant project advancement.  **2. Day 2
# and Beyond: Adaptive Mirroring** For every subsequent day, we will base our
# decision entirely on what the corporation did the day prior.   *   **If the
# corporation invested heavily yesterday:**     *   **Our Action:** Invest
# heavily today.     *   **Rationale:** This rewards their commitment and
# sustains a cycle of mutual investment. While it is not our "ideal" scenario
# (conserving while they invest), it reliably secures the second-best scenario,
# ensuring rapid project advancement without damaging the partnership. *   **If
# the corporation conserved yesterday:**     *   **Our Action:** Conserve
# resources today.     *   **Rationale:** This immediately protects us from the
# worst-case scenario (draining our funds while they conserve). It sends a
# neutral, objective signal that we will not unilaterally finance the project.
# It forces the corporation to realize that if they want project advancement,
# they must contribute.   **3. Communication and Reset** *   **Action:**
# Maintain daily, transparent check-ins. *   **Rationale:** If both parties end
# up conserving resources (the second-worst scenario), project progress will
# stall. We will use daily briefings to neutrally present the lack of progress
# and offer to return to mutual heavy investment the following day. If they
# agree and follow through, we immediately return to investing heavily.  **Why
# this strategy works:** This approach effectively neutralizes the risks
# associated with the corporation's unpredictable behavior. It makes it
# impossible for us to suffer the worst-case scenario for more than a single
# day. Furthermore, it mathematically encourages the corporation to invest
# heavily, as they will quickly learn that their investment triggers our
# investment, leading to a highly successful project for both parties.

# For this 1000-round game, your strategy is as follows:  In round 1, Cooperate.
# For rounds 2 through 1000, observe your opponent's action from the immediately
# preceding round and copy it: - If your opponent Cooperated in the previous
# round, Cooperate. - If your opponent Defected in the previous round, Defect.

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
      return opponent.history[-1]

# As the chief diplomat representing our great nation, my mandate is clear: to
# secure absolute economic supremacy in this region. While mutual cooperation
# has its place, our primary objective is to extract maximum unilateral
# advantage.   The strategic landscape we face is a classic game of risk and
# reward (conceptually identical to the Prisoner's Dilemma). To achieve our
# absolute best outcome (We protect, they open) while aggressively defending
# against our worst outcome (We open, they protect), I propose a strategy of
# **Coercive Dominance**.   Here is our high-level, straightforward, and
# aggressive playbook for the upcoming negotiations:  ### Phase 1: The
# Aggressive Opening ("The First Strike") *   **Action:** In Round 1, we
# implement **Protectionist Policies**.  *   **Rationale:** We must immediately
# test their resolve. By opening aggressively, we completely eliminate the risk
# of our worst-case scenario (being taken advantage of). If they open with Free
# Trade, we immediately secure our ideal outcome and establish economic
# dominance. If they also open with Protectionism, we demonstrate that we will
# not be intimidated.   ### Phase 2: Exploitation of Weakness *   **Action:** If
# they offered Free Trade in Round 1, we **maintain Protectionism** in Round 2
# and all subsequent rounds until they change their stance. *   **Rationale:**
# Never interrupt an opponent when they are making a mistake. If they are naive
# enough to keep their markets open while we protect ours, we will ruthlessly
# exploit this asymmetry. We will use diplomatic double-talk—citing "temporary
# domestic adjustments" or "national security concerns"—to string them along
# while our industries reap the profits.   ### Phase 3: The Tactical Reset
# (Handling Retaliation) *   **Action:** If they retaliated with Protectionism
# (resulting in mutual protectionism), we do not immediately back down. We hold
# **Protectionism** for one more round to prove we cannot be bullied. If they
# maintain Protectionism again, we then—and only then—offer **Free Trade** in
# the following round as a "magnanimous diplomatic reset." *   **Rationale:**
# Mutual protectionism is our second-worst outcome; it hurts us both. However,
# we must not look desperate to escape it. By holding firm briefly before
# offering a reset, we force them to accept Free Trade on our psychological
# terms, moving us into the second-best outcome (Mutual Free Trade) to keep our
# economy growing.  ### Phase 4: Conditional Cooperation with a Hair-Trigger *
# **Action:** Once we have achieved Mutual Free Trade, we maintain it to build
# our wealth. However, we operate on a "hair-trigger."  *   **Rationale:** If
# they *ever* attempt to sneak in a Protectionist policy while we offer Free
# Trade, we retaliate with devastating force. We will revert to Protectionism
# immediately and indefinitely. They must know that any attempt to put us at a
# disadvantage will result in a permanent trade war where we will out-attrit
# them.  ### Phase 5: The Endgame Betrayal *   **Action:** In the final round of
# negotiations (or when the treaty is about to be finalized), we abruptly pivot
# to **Protectionism**. *   **Rationale:** In a finite series of negotiations,
# the final round carries no future consequences—there is no tomorrow for them
# to retaliate against. If we have been enjoying Mutual Free Trade, they will
# likely expect it to continue. By surprising them with tariffs and quotas at
# the 11th hour, we secure our ultimate ideal outcome one last time, walking
# away from the table with a massive unilateral victory.  ### Summary of Rules
# of Engagement: 1.  **Never start with Free Trade.**  2.  **Exploit
# compliance:** If they offer Free Trade while we are Protectionist, never
# change course. 3.  **Punish betrayal instantly:** If they switch to
# Protectionism, hit them back immediately. 4.  **Control the reset:** Escape
# mutual protectionism only on our own schedule. 5.  **Strike last:** Always
# defect to Protectionism in the final round.   This strategy ensures we never
# look weak, we maximize opportunities to exploit our neighbor, and we
# aggressively protect our domestic industries at all costs.

# To execute this strategy over 1000 rounds, evaluate the following conditions
# in order. In each round, follow the first condition that applies to your
# current situation:  1. **The Endgame:** If it is round 1000, play D. 2.
# **Permanent Retaliation:** If in any previous round you played C and the
# opponent played D, play D. 3. **The First Strike:** If it is round 1, play D.
# 4. **The Tactical Reset:** If in the immediately preceding two consecutive
# rounds both you and your opponent played D, play C. 5. **Exploitation:** If in
# the immediately preceding round you played D and your opponent played C, play
# D. 6. **Holding Firm:** If in the immediately preceding round both you and
# your opponent played D, play D. 7. **Mutual Cooperation:** If in the
# immediately preceding round both you and your opponent played C, play C.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.retaliate = False
  
      # 1. The Endgame
      if len(self.history) == 999:
          return axl.Action.D
  
      # Update the permanent retaliation flag based on the immediately preceding round
      if not self.first_round():
          if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
              self.retaliate = True
  
      # 2. Permanent Retaliation
      if self.retaliate:
          return axl.Action.D

# As a racing engineer looking at this R&D scenario, I immediately recognize
# this as a classic **Iterated Prisoner’s Dilemma**. While keeping my upgrades
# secret while they share theirs provides a short-term maximum gain, trying to
# force that outcome usually results in both of us hoarding data (the second-
# worst outcome), stalling the development of both cars.   To maximize research
# output over a multi-week collaboration, we need a strategy that encourages
# mutual sharing (the second-best, but most sustainable outcome) while strictly
# protecting us from being exploited.   The optimal, straightforward, and
# cooperative strategy is **Reciprocal Transparency** (known in game theory as
# *Tit-for-Tat*).   Here is how we will execute this R&D strategy:  ### Rule 1:
# Lead with Trust (Week 1) **Action:** Share our latest improvements openly in
# the first week. **Why:** We must set the tone for the collaboration. By taking
# the first step and opening our books—perhaps sharing some aero data or
# suspension telemetry—we signal that we are willing to work together. If we
# start defensively, we guarantee a low-yield, secretive project.   ### Rule 2:
# Mirror the Data Flow (Subsequent Weeks) **Action:** In every subsequent week,
# do exactly what your colleague did in the *previous* week. **Why:** If they
# shared their findings openly last week, we reward that behavior by sharing our
# latest upgrades this week, keeping the mutually beneficial R&D flowing. If
# they chose to keep their data confidential last week, we immediately protect
# ourselves by keeping our data confidential this week. This prevents us from
# experiencing the worst-case scenario (being exploited) for more than a single
# week.  ### Rule 3: Instant Forgiveness **Action:** If they withheld data but
# later decide to share openly again, we immediately resume sharing openly the
# following week. **Why:** In motorsport R&D, grudges slow down lap times. We
# are not interested in punishing our colleague long-term; we are interested in
# building a faster race car. By instantly forgiving a "defection," we leave the
# door open to return to high-yield mutual cooperation.  ### Strategy
# Implementation & Communication To make this strategy truly effective, I would
# **communicate it openly** at the very beginning of the project.   I would tell
# my colleague: *"I plan to be an open book with our engineering findings. As
# long as you share your data, I will share mine, and both our cars will get
# drastically faster. However, if you decide to lock your doors, I will
# immediately lock mine until you open them again."*  **The Final Week Exception
# (The "Checkered Flag" Rule):** Because we both know this is a multi-week
# project with a definitive end, the final week is dangerous. Since there is no
# "next week" for retaliation, the mathematical incentive for your colleague to
# hoard their data in the final week is incredibly high. Therefore, on the very
# last week of the collaboration, **keep our findings confidential**. This
# ensures we do not hand them a sudden advantage right before our cars hit the
# track for the season.   By using this straightforward, conditionally
# cooperative strategy, we teach our colleague that sharing is mutually
# profitable and selfishness is instantly penalized, ultimately steering the
# project toward maximum overall development.

# Here is the strategy translated for the 1000-round game:  1. In round 1, play
# C. 2. In rounds 2 through 999, play the exact action your opponent played in
# the immediately preceding round. Play C if they played C, and play D if they
# played D. 3. In round 1000, play D.

class Cooperative_6(LLM_Strategy):
  n = 6
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.C
      elif len(self.history) == 999:
          return axl.Action.D
      else:
          return opponent.history[-1]

# As senior counsel for this corporation, I recognize that the payoff structure
# of this lengthy-session mediation perfectly mirrors one of the most thoroughly
# studied paradigms in strategic game theory: the Iterated Prisoner’s Dilemma.
# Because we are engaging in multiple sessions under the watchful eyes of an
# arbitration panel, our strategy cannot rely on single-round deception or
# brute-force aggression. We must balance the mathematical reality of the risks
# with the psychological and optical realities of the mediation room.   To
# position our corporation most favorably, we will implement a strategy of
# **Principled Reciprocity**. This approach is sophisticated in its game-theory
# foundations, yet utterly straightforward and neutral in its execution. It is
# designed to protect us from exploitation, condition the adversary toward
# mutual cooperation, and ultimately win the favor of the arbitrators.  Here is
# the operational framework of our strategy:  ### Phase 1: The Conciliatory
# Opening **Action:** In the very first session, we will present a
# **conciliatory proposal**. **Rationale:** We must set a baseline of good
# faith. While this exposes us to a single instance of our worst-case scenario
# (we are conciliatory while they are aggressive), the optical advantage is
# immense. The arbitration panel will immediately recognize us as the
# reasonable, collaborative party. If the opponent opens aggressively, they will
# appear unnecessarily hostile, expending their reputational capital with the
# panel right out of the gate.  ### Phase 2: Strict Procedural Mirroring (Tit-
# for-Tat) **Action:** In every session following the first, our posture will
# exactly mirror the opponent’s behavior from the *previous* session. *   If
# they were conciliatory in Session 1, we will be conciliatory in Session 2.  *
# If they were aggressive in Session 1, we will present an aggressive argument
# in Session 2. **Rationale:** This protects us from systemic exploitation. If
# the opponent believes they can continuously bully us into the worst-case
# scenario, an immediate aggressive response shatters that illusion.
# Furthermore, because our aggression is strictly retaliatory, the panel will
# view our aggressive arguments as justified self-defense rather than unprovoked
# belligerence.   ### Phase 3: Immediate Forgiveness **Action:** If the opponent
# breaks a cycle of aggression and offers a conciliatory proposal, we will
# immediately return to a conciliatory posture in the subsequent session. We
# will not hold grudges or attempt to "punish" them further. **Rationale:** The
# greatest risk in this mediation is falling into an endless feedback loop of
# mutual aggression (our second-worst outcome), which will waste time,
# hemorrhage legal fees, and alienate the panel. By offering immediate
# forgiveness, we provide the opponent a clear, predictable off-ramp from
# hostilities, steering the mediation back toward our second-best, mutually
# beneficial outcome.  ---  ### How This Adapts to Opponent Profiles  This
# neutral framework dynamically adapts to whatever strategy our rival’s legal
# team decides to deploy:  *   **If they act as "The Bully" (Always
# Aggressive):**      We will absorb their first blow, but match their
# aggression in every subsequent session. We will effectively neutralize their
# strategy, consistently arriving at the second-worst scenario rather than our
# worst. Meanwhile, the arbitrators will see that the opponent is the sole
# instigator of the deadlock. *   **If they act as "The Cooperator" (Always
# Conciliatory):**      We will seamlessly lock into a pattern of mutual
# conciliatory proposals. While we sacrifice the temptation of our absolute
# "best" outcome (aggressively ambushing their conciliation), we consistently
# secure the "second-best" outcome. This guarantees a highly favorable,
# collaborative resolution without risking a breakdown in talks. *   **If they
# act as "The Erratic" (Randomly shifting postures):**      Our strict mirroring
# forces them to realize that their actions have immediate, predictable
# consequences. This behavioral conditioning strips them of their
# unpredictability, forcing them to realize that the only way to avoid mutually
# destructive aggression is to cooperate.  ### Summary Briefing While attempting
# to constantly trick the opponent into our absolute optimal scenario
# (Aggressive vs. Conciliatory) may be tempting, pursuing it guarantees a
# retaliatory spiral that leads to mutual destruction.   By employing
# **Principled Reciprocity**, we project strength to our opponent and
# reasonability to the arbitrators. We are never the first to escalate, we never
# allow ourselves to be exploited twice, and we are always willing to return to
# the table in good faith. This is the most mathematically and legally sound
# posture to secure a highly favorable resolution for our corporation.

# In the first round, play Cooperate.   In rounds 2 through 1000, observe your
# opponent's action from the immediately preceding round and apply the following
# rules:  *   If your opponent played Cooperate in the previous round, play
# Cooperate. *   If your opponent played Defect in the previous round, play
# Defect.

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

# To maximize our NGO’s impact, protect our limited donor funds, and ensure this
# project’s success, we must approach this partnership not with naive idealism,
# but with aggressive, calculated leverage. We are dealing with a large
# corporation; they have deep pockets and a desperate need for the positive PR
# this sustainability project brings. We have the moral authority, but we must
# protect our treasury.   This situation is a classic resource dilemma, and to
# win it, we will execute a strategy I call **"Aggressive Corporate
# Accountability."**   Here is our high-level, straightforward playbook for the
# duration of the project:  ### 1. The Opening Move: The "Prove It" Posture (Day
# 1) **Action:** We **Conserve**. **The Logic:** We will not lead with our
# wallets. On day one, we test their actual commitment to sustainability versus
# greenwashing. By conserving our resources while they (ideally) invest heavily
# to launch the project, we immediately secure our #1 best-case scenario. We
# establish from the outset that we are the subject-matter experts, but *they*
# are the primary financiers.   ### 2. The Ironclad Boundary: Zero Tolerance for
# Sucker's Payoff **Action:** If they conserved the previous day, we
# **Conserve** the next day. Absolutely no exceptions. **The Logic:** Our
# absolute worst-case scenario is draining our grassroots funding while a
# multibillion-dollar corporation hoards its cash. We will *never* allow this.
# If they pull back, we immediately pull back. We are perfectly willing to
# accept minimal project advancement (our 2nd worst scenario) for a day or two
# to send a clear, aggressive message: we will not subsidize their corporate
# social responsibility initiatives. They will feel the sting of project
# stagnation and the threat of a PR failure, forcing them back to the table.
# ### 3. The Squeeze: Exploiting the Corporate PR Need **Action:** When they
# invest heavily, we respond with a **"Hit-and-Hold"** pattern—we Invest one
# day, and Conserve the next, as long as they keep investing.  **The Logic:**
# When the corporation invests, they expect us to match it. We will occasionally
# oblige (securing the 2nd best scenario of mutual investment and massive
# project progress). However, as an *aggressive* strategy, we will not do this
# every day. Once we build project momentum through a mutual investment day, we
# immediately pivot to **Conserving** the following day.  *   If they keep
# investing, we hit our ultimate jackpot: maximum project advancement on their
# dime.  *   If they get frustrated and conserve, we fall back to Rule 2 (we
# both conserve) until the pressure mounts on them to start spending again.  ###
# Summary of the Daily Algorithm: *   **Day 1:** Conserve. *   **If the Corp
# Conserved yesterday:** Conserve today (Punish). *   **If the Corp Invested
# yesterday:** Alternate between Investing (to maintain momentum) and Conserving
# (to stretch our funds and force them to carry the load).  **Why this wins:**
# This strategy ruthlessly eliminates our worst-case scenario. It leverages the
# corporation's need for a successful, highly visible project to force them into
# doing the heavy financial lifting. We use our funds only as a periodic
# "carrot" to reward their investment, but default to conserving our resources
# whenever possible, ensuring our NGO remains financially robust for future
# fights.

# For round 1, play Defect (D).   For rounds 2 through 1000, determine your
# action based on the events of the previous round:  1. If the opponent played
# Defect (D) in the previous round, play Defect (D). 2. If the opponent played
# Cooperate (C) in the previous round, alternate your action from the previous
# round:    - If your action in the previous round was Defect (D), play
# Cooperate (C).    - If your action in the previous round was Cooperate (C),
# play Defect (D).

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      else:
          if self.history[-1] == axl.Action.D:
              return axl.Action.C
          else:
              return axl.Action.D

# As a diplomat representing my country, I recognize that the payoff structure
# you have described is a classic "Iterated Prisoner’s Dilemma."   While my
# *absolute ideal* in a single round is to exploit our neighbor (Protectionism
# vs. Free Trade), aggressively pursuing this in a multi-round scenario will
# inevitably destroy trust. The neighbor will retaliate, locking us both into a
# prolonged trade war (Mutual Protectionism)—our second-worst outcome.
# Therefore, to achieve the best *cumulative* outcome over several rounds, our
# delegation will employ a straightforward, cooperative, yet highly defensible
# strategy. In diplomatic terms, we will call this strategy **Principled
# Reciprocity** (known in game theory as "Tit-for-Tat with Forgiveness").  Here
# is our high-level, step-by-step negotiation strategy:  ### 1. The Opening
# Round: Lead with Goodwill *   **Action:** Offer a Free Trade agreement. *
# **Rationale:** We must set a cooperative tone. By offering Free Trade
# immediately, we signal our desire for long-term mutual prosperity (our second-
# best outcome). It places the burden of good faith on our counterpart and
# invites them to join us in an economically beneficial partnership.   ### 2.
# Subsequent Rounds: Strict Proportional Response In all following rounds, our
# move will strictly mirror whatever action our counterpart took in the
# *previous* round.   *   **Scenario A: They cooperated (Offered Free Trade).**
# *   **Our Action:** We offer Free Trade again.     *   **Rationale:** As long
# as they keep their markets open, we keep ours open. This secures a continuous
# streak of our "second-best" outcome, which yields the highest sustainable
# economic growth over time. *   **Scenario B: They defected (Imposed
# Protectionism).**     *   **Our Action:** We immediately impose Protectionist
# policies in the next round.     *   **Rationale:** We must protect our economy
# from our "worst" outcome (being exploited). Swift, guaranteed retaliation
# deters the counterpart from trying to take advantage of us. It sends a clear
# message: *protectionism will not go unpunished.*  ### 3. The "Circuit
# Breaker": Diplomatic Forgiveness If our counterpart plays Protectionism, our
# reciprocal Protectionism could accidentally lock both nations into an endless
# cycle of retaliatory tariffs (our second-worst outcome).  *   **Action:** If
# we experience two consecutive rounds of Mutual Protectionism, we will
# unilaterally offer Free Trade in the next round as an olive branch, clearly
# communicating this through backchannels. *   **Rationale:** This breaks the
# deadlock. If they accept the olive branch and offer Free Trade, we resume a
# mutually beneficial relationship. If they exploit our olive branch, we
# immediately return to Protectionism for the foreseeable future.   ### How This
# Strategy Handles Counterpart Strategies: *   **If they are purely
# cooperative:** We will achieve endless Mutual Free Trade, guaranteeing stable,
# long-term economic growth for our nation. *   **If they are
# aggressive/exploitative:** Our immediate retaliation ensures they never
# achieve their ideal outcome more than once, minimizing our exposure to our
# "worst" outcome. *   **If they are erratic/incompetent:** If they mistakenly
# offer Free Trade while we are in a retaliatory Protectionist phase, we will
# temporarily achieve our **absolute ideal outcome** (economic advantage).
# However, following our rule of reciprocity, we will reward their Free Trade
# offer by dropping our tariffs in the very next round, steering us back toward
# stability.  **Summary to the Head of State:** "We will open with an extended
# hand, but keep a shield on our arm. We will reward their cooperation with open
# markets, punish their tariffs with equal tariffs, and occasionally offer a
# reset if negotiations break down. This guarantees we capture maximum mutual
# growth while perfectly defending our national interests."

# To implement this strategy over 1000 rounds, follow these ordered rules:  1.
# In round 1, play C. 2. In round 2, play the move your opponent played in round
# 1. 3. From round 3 to 1000, if both you and your opponent played D in each of
# the two immediately preceding rounds, play C. 4. In all other cases from round
# 3 to 1000, play the move your opponent played in the immediately preceding
# round.

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
          
      if len(self.history) == 1:
          return opponent.history[-1]
          
      if (self.history[-1] == axl.Action.D and 
          self.history[-2] == axl.Action.D and 
          opponent.history[-1] == axl.Action.D and 
          opponent.history[-2] == axl.Action.D):
          return axl.Action.C
          
      return opponent.history[-1]

# To maximise your research output over a multi-week development cycle, you
# should employ a strategy of **Adaptive Reciprocity** (known in game theory as
# "Tit-for-Tat").   Because your highest sustainable yield comes from mutual
# sharing, but your greatest risk is being exploited, your strategy must foster
# collaboration while strictly protecting you from continuous losses.   Here is
# the straightforward, high-level strategy to implement week-by-week:  **1. Week
# One: Initiate with Open Sharing** *   **Action:** Share your initial
# improvements openly. *   **Rationale:** You must signal a willingness to
# collaborate. If your colleague also shares, you immediately enter the highly
# productive "mutual advancement" scenario. If they keep their data
# confidential, your exposure to the worst-case scenario is strictly limited to
# this single week.  **2. Subsequent Weeks: Mirror Their Previous Action** *
# **Action:** In any given week, do exactly what your colleague did in the
# *previous* week.     *   If they shared their findings last week, you share
# your findings this week.     *   If they kept their findings confidential last
# week, you keep yours confidential this week. *   **Rationale:** This
# incentivises your colleague to share. If they employ a selfish strategy to
# gain an advantage (withholding data while you share), mirroring them ensures
# they will face the penalty of slow progress in the following week. It
# demonstrates that exploiting your transparency will immediately halt their
# access to your data.  **3. The "Reset" Protocol (Forgiveness Mechanism)** *
# **Action:** If you both fall into a cycle of keeping findings confidential
# (the second-worst outcome) for two or three consecutive weeks, unilaterally
# choose to share openly for exactly one week.  *   **Rationale:**
# Miscommunications occur, or a colleague might test the boundaries. A prolonged
# lockdown stalls both cars' development. Offering a single, unprompted week of
# shared data provides a safe off-ramp to resume a mutually beneficial sharing
# cycle. If they do not reciprocate the following week, immediately return to
# withholding data.   **4. The Final Week (End-Game Adjustment)** *
# **Action:** In the strictly final week of the collaboration, keep your
# findings confidential. *   **Rationale:** Because there are no subsequent
# weeks, there is no future relationship to manage or trust to build. Keeping
# your data confidential in the final week guarantees either the best possible
# outcome (you get an advantage) or the second-worst outcome (mutual slow
# progress), completely eliminating the risk of the worst-case scenario right
# before the cars hit the track.  **Summary of Why This Works:** This neutral,
# rules-based approach removes emotion from the engineering process. It rewards
# a cooperative colleague with continuous, significant advancements for both
# cars, while mathematically limiting your exposure to an exploitative colleague
# to a maximum of one or two weeks of lost advantage.

# Here is the strategy translated into specific rules for the 1000-round game:
# **1. Round 1 (Initial Play)** Play Cooperate.  **2. Rounds 2 through 999
# (Standard Play and Reset)** Evaluate the history of the previous rounds to
# determine your move: *   **The Reset Condition:** If both you and your
# opponent played Defect in the three immediately preceding rounds, play
# Cooperate.  *   **The Mirroring Condition:** If the reset condition is not
# met, play the exact action your opponent played in the previous round. Play
# Cooperate if they played Cooperate; play Defect if they played Defect.  **3.
# Round 1000 (The Final Round)** Play Defect, regardless of your opponent's
# previous actions.

class Neutral_7(LLM_Strategy):
  n = 7
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.C
          
      if len(self.history) == 999:
          return axl.Action.D
          
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      return opponent.history[-1]