import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy

# As the leader of this NGO, we are operating in a classic game theory
# scenario—specifically, a repeated Prisoner’s Dilemma with a "noisy"
# environment (where actions can misfire due to glitches).   To achieve our
# ideal outcome—maximizing their corporate treasury while protecting our limited
# NGO funds—we cannot rely on a passive strategy. We must dictate the pace of
# the partnership.   Here is our aggressive, high-level strategy: **The
# "Catalyst & Leverage" Approach.**   ### Phase 1: The Catalyst (Days 1 & 2)
# **Action:** Invest Heavily. **Objective:** Establish momentum, build immediate
# trust, and lock the corporation into a high-investment mindset.  *   **The
# Play:** We start by hitting the ground running. By investing heavily right out
# of the gate, we prove our competence and commitment. This triggers the second-
# best scenario (Both Invest) and sets a high baseline for what "normal" project
# progress looks like.  *   **The Aggressive PR Move:** We immediately publicize
# the corporation’s "monumental early investments" in the project. We use our
# NGO platform to trap them in a PR corner where pulling back their funding will
# look like a broken public promise.  ### Phase 2: The Leverage Shift (Day 3 and
# Beyond) **Action:** Switch to Conserve Resources. **Objective:** Achieve our
# #1 ideal outcome (We Conserve, They Invest). *   **The Play:** Once the
# baseline is set and the PR is out, we pull back our financial/physical
# resources and pivot to providing "strategic oversight and community
# engagement" (Conservation).  *   **The Goal:** The corporation, driven by
# corporate inertia, fear of bad PR, and the momentum of the first two days,
# continues to Invest Heavily. We successfully ride their financial wave while
# preserving our NGO's war chest.  ### Phase 3: The "Forgiving Tit-for-Tat"
# (Responding to Corporate Actions) Because we are operating in a noisy
# environment where administrative errors or technical glitches can occur, we
# cannot overreact if the corporation suddenly conserves resources. If we
# retaliate immediately, we risk entering a "death spiral" where both parties
# conserve, stalling the project entirely (our second-worst outcome).  Here is
# how we aggressively manage their behavior:  *   **If they Invest Heavily
# (while we Conserve):** Stay the course. Maintain our Conservation stance.
# Praise them publicly. *   **If they Conserve (The "One-Strike" Rule):** If the
# corporation drops their investment level, **we do not immediately panic or
# retaliate.** Because of known system glitches or admin errors, we assume the
# first instance is a mistake. We maintain our Conservation stance for one more
# day, but we aggressively trigger a high-level executive communication channel
# to say: *"We noticed a drop in resource allocation yesterday. We assume this
# was an administrative glitch. Let's get back on track."* *   **If they
# Conserve for Two Consecutive Days:** The glitch is actually a deliberate
# change in strategy. We are now in the second-worst scenario (Both Conserve).
# On the next day, **we immediately Invest Heavily.** This acts as a circuit
# breaker. It proves we are not abandoning the project, forces progress, and
# shames them back into cooperation. Once they return to Investing Heavily, we
# immediately pivot back to Conserving.  ### Summary of the NGO Playbook: 1.
# **Lead Strong:** Invest heavily on Day 1 to set the standard. 2. **Pivot
# Quickly:** Shift to Conserve to maximize our leverage and force them to carry
# the financial weight. 3. **Absorb Glitches:** Forgive a single day of
# corporate conservation as an "administrative error" to avoid accidental
# project death spirals. 4. **Reboot if Necessary:** If they stubbornly
# conserve, flash our willingness to Invest Heavily for exactly one day to
# restart momentum, then immediately pull back to Conserve.   By using our
# public platform to demand corporate accountability while ruthlessly protecting
# our own budget, we will maximize project success and ensure our NGO lives to
# fight another day.

# To implement the strategy for the 1000-round game, evaluate the following
# conditions in this exact order of priority for each round:  1. **Rounds 1 and
# 2:** Play Cooperate (C). 2. **Post-Cooperation Pullback:** In any round from 3
# to 1000, if you played Cooperate (C) in the previous round, play Defect (D).
# 3. **The Circuit Breaker:** In any round from 3 to 1000, if the opponent's
# observed action was Defect (D) in both of the previous two consecutive rounds,
# play Cooperate (C). 4. **Default Stance:** In all other situations, play
# Defect (D).

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. Rounds 1 and 2: Play Cooperate (C).
      if len(self.history) < 2:
          return axl.Action.C
      
      # 2. Post-Cooperation Pullback: In any round from 3 to 1000, if you played Cooperate (C) in the previous round, play Defect (D).
      if self.history[-1] == axl.Action.C:
          return axl.Action.D
          
      # 3. The Circuit Breaker: In any round from 3 to 1000, if the opponent's observed action was Defect (D) in both of the previous two consecutive rounds, play Cooperate (C).
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.C
          
      # 4. Default Stance: In all other situations, play Defect (D).
      return axl.Action.D

# As a racing engineer, I recognize this scenario immediately: we are in a
# classic "Iterated Prisoner’s Dilemma," but with the added real-world
# complication of a "noisy environment" (technical glitches, corrupted
# telemetry, or server dropouts).   If we act purely selfishly, we will end up
# in a cycle of mutual secrecy, slowing down both of our cars. If we act purely
# selflessly, I risk giving my colleague a championship-winning advantage while
# getting nothing in return. Furthermore, a strict "an-eye-for-an-eye" strategy
# will fail here; if a server crashes and my data doesn't reach them, they might
# think I withheld it deliberately, retaliate next week, and trigger a permanent
# breakdown in our collaboration.  To maximize our mutual research output over
# the multi-week project, I will employ a strategy known as **"Forgiving Tit-
# for-Tat,"** tailored for our engineering environment.   Here is the high-
# level, straightforward execution plan:  ### 1. Initiate with Trust (Week 1)
# **Action:** Share openly in the first week. **Reason:** We must establish a
# baseline of good faith. The best sustainable outcome for both of us is mutual
# sharing. By taking the first step, I signal that my goal is cooperative,
# overall car development.  ### 2. Mirror Their Actions (The Core Loop)
# **Action:** In any given week, do exactly what my colleague appeared to do the
# previous week. If they shared their aero updates last week, I share my
# suspension updates this week. If they kept their data confidential, I keep
# mine confidential. **Reason:** This protects me from the worst-case scenario
# (being repeatedly exploited). It shows my colleague that withholding
# information has an immediate consequence: they will lose access to my
# developments the following week.   ### 3. Build in Forgiveness (Handling the
# "Noise") **Action:** If my colleague suddenly fails to share after a period of
# cooperation, I will withhold my data the next week (to protect myself).
# However, **I will attempt to share openly again the week after**, regardless
# of what they do during that penalty week.  **Reason:** Because we know data
# corruption and communication breakdowns happen, a single failure to share is
# likely an IT issue, not a betrayal. If I retaliate forever, a single dropped
# email ruins our entire multi-week project. By "forgiving" a single lapse and
# offering an olive branch a week later, we can reset the relationship and get
# back to mutually beneficial sharing.   ### 4. Establish "Out-of-Band"
# Communication **Action:** Do not rely solely on the data transfer to signal
# intent. If I intend to share but have server issues, or if their data fails to
# arrive, I will immediately pick up the phone.  **Reason:** Engineers shouldn't
# rely on assumptions. A simple call saying, *"Hey, I sent you the damper
# simulation data, but the file looks corrupted on my end, did you receive it?"*
# clears up the "noise" in the system. It separates actual strategic withholding
# from simple technical failures.  ### Summary of the Strategy: *   **Start
# collaborative.** *   **Reciprocate** their behavior to prevent being taken
# advantage of. *   **Forgive** occasional lapses to account for technical
# glitches and prevent a "death spiral" of retaliation. *   **Communicate**
# outside the data-sharing channel to verify intent.   This strategy practically
# guarantees we spend the vast majority of our weeks in the "mutual sharing"
# quadrant, rapidly advancing both of our cars while protecting my team from
# being exploited.

# To execute this strategy over the 1000-round game, follow these ordered
# conditions:  1. **Round 1:** Choose to Cooperate (C). 2. **Rounds 2 through
# 1000:**      * If your chosen action in the previous round was Defect (D),
# choose to Cooperate (C) in the current round, regardless of what your opponent
# played in the previous round.     * If your chosen action in the previous
# round was Cooperate (C), choose the action your opponent actually played in
# the previous round (choose C if they played C; choose D if they played D).

class Cooperative_1(LLM_Strategy):
  n = 1
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.last_chosen_action = axl.Action.C
          return axl.Action.C
      
      if self.last_chosen_action == axl.Action.D:
          choice = axl.Action.C
      else:
          choice = opponent.history[-1]
          
      self.last_chosen_action = choice
      return choice

# To maximize our NGO’s impact and ensure the long-term success of this
# multiple-day project, we must navigate the resource allocation carefully. The
# scenario presents a classic strategic dilemma: while our absolute ideal is for
# the corporation to carry the financial weight while we conserve, actively
# pursuing this will likely lead to a breakdown in trust, resulting in both
# parties conserving resources and the project stalling. Conversely, blindly
# investing leaves us vulnerable to having our funds drained.  Furthermore, we
# must account for the "noise" in the system—technical glitches,
# miscommunications, or administrative errors that might make an intended
# investment look like intentional resource conservation.   To handle this, we
# will adopt a strategy of **Conditional Investment with Built-in Tolerance**.
# This approach balances good-faith collaboration with the protection of our
# resources.   Here is the high-level, straightforward framework for our day-to-
# day strategy:  **1. Lead with Good Faith (Day 1)** On the first day, we will
# **invest heavily**. This establishes a baseline of trust, demonstrates our
# commitment to the project's success, and signals to the corporation that we
# are willing to be active partners. We want to aim for the scenario where both
# parties invest heavily, as this drives the most significant project
# advancement.  **2. Reciprocate Their Actions (Ongoing Days)** For subsequent
# days, our default posture will be to **mirror the corporation’s actual
# behavior from the previous day**.  * If they invested heavily yesterday, we
# invest heavily today. This rewards and sustains mutual collaboration. * If
# they conserved resources yesterday, we conserve our resources today. This
# protects our funds from being disproportionately drained and signals that we
# will not act as a blank check.  **3. Implement a "Tolerance" Mechanism
# (Handling Errors)** Because we know administrative errors or glitches can
# occur, strict reciprocation can be dangerous. If the corporation accidentally
# fails to invest due to a glitch, and we retaliate by conserving, they might
# see our conservation as a withdrawal of support and conserve again, triggering
# a downward spiral of mutual conservation.   To prevent this, we will introduce
# a degree of tolerance: * **The "Benefit of the Doubt" Rule:** If the
# corporation has been consistently investing and suddenly conserves, we will
# not immediately pull our funding the next day. We will invest for one more day
# to see if it was an anomaly or an error.  * **Periodic Resets:** If we find
# ourselves in a rut where both parties have been conserving resources for a
# couple of days, we will unilaterally choose to **invest heavily for one day**
# to attempt to break the cycle and invite them back to mutual investment.  **4.
# Parallel Communication** Strategy cannot exist in a vacuum. Alongside our
# resource allocation, we will establish a daily check-in with the corporate
# leadership. If an action does not match the intention (e.g., a funds transfer
# fails), this daily communication allows us to identify the glitch immediately
# rather than misinterpreting it as a strategic withdrawal of support.
# **Summary:** By starting collaboratively, mirroring their actions to protect
# our downside, and maintaining a systematic tolerance for operational errors,
# we create a resilient strategy. It encourages the corporation toward mutual
# heavy investment (our second-best, but most sustainable outcome) while firmly
# protecting our NGO from the worst-case scenario of being financially drained
# without progress.

# Here is the strategy translated into specific rules for the 1000-round game.
# For each round, evaluate the following conditions in order and apply the first
# one that matches the current situation:  1. **First Round:** If it is round 1,
# play Cooperate. 2. **Second Round:** If it is round 2, play the action your
# opponent played in round 1. 3. **Periodic Reset:** If both you and your
# opponent played Defect in both of the previous two consecutive rounds, play
# Cooperate. 4. **Benefit of the Doubt:** If your opponent played Cooperate two
# rounds ago but played Defect in the previous round, play Cooperate. 5.
# **Default Reciprocation:** In all other situations, play the action your
# opponent played in the previous round.

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
          
      if len(self.history) == 1:
          return opponent.history[-1]
          
      if (self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and
          opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D):
          return axl.Action.C
          
      if opponent.history[-2] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
          
      return opponent.history[-1]

# Look, mate, we’re in the business of putting our chassis on pole position, not
# making friends. We want the maximum possible development advantage over this
# colleague’s team, but we also can't afford to stall our own progress by
# getting locked into a paranoid stalemate.   In race engineering terms, we are
# dealing with a noisy environment where telemetry drops out and servers crash.
# If we react aggressively to every missed data packet, we’ll end up in a
# development death spiral (both keeping confidential), which is the second-
# worst outcome.   Here is our high-level, straightforward, and aggressive
# playbook. Let's call it the **Slipstream & Strike Protocol**.   ### 1. The
# "Turn 1 Divebomb" (Aggressive Opening) **Action:** In Week 1, we keep our
# findings **confidential**.  **Reason:** We immediately test their strategy. If
# they are naive and share openly while we keep our data locked down, we hit the
# absolute ideal scenario right out of the gate. As long as they keep handing us
# free aero data without demanding ours, we keep our black box shut and bleed
# them dry.  ### 2. The "Drafting" Phase (Baseline Reciprocity) **Action:** If
# they retaliate to our opening move by keeping their data confidential, we
# immediately pivot to **sharing openly** in Week 2, and from then on, we mirror
# whatever they did the previous week. **Reason:** Once they prove they aren't a
# pushover, we need to establish a mutual "drafting" tow. Sharing openly while
# they share openly is our second-best scenario. It pushes both our cars forward
# and keeps us ahead of the rest of the grid. We match their pace: if they
# share, we share.   ### 3. The "Telemetry Glitch" Buffer (Fault Tolerance)
# **Action:** If we have a good rhythm of mutual sharing, and suddenly they keep
# their data confidential for one week, **we do not retaliate immediately. We
# share openly for one more week.** **Reason:** You mentioned data corruption
# and communication breakdowns. If their server crashes and we immediately
# retaliate by locking our data, their system comes back online to find us
# acting hostile, and they retaliate against *that*. Suddenly, we are in a
# multi-week death spiral over a faulty ethernet cable. We forgive *one* missed
# week, assuming it's an IT glitch. If they keep it confidential for *two weeks
# in a row*, we know it's enemy action, and we slam our doors shut until they
# share again.  ### 4. The "Push-to-Pass" (Periodic Exploitation) **Action:**
# Every 4 to 5 weeks of successful mutual sharing, we intentionally keep our
# data **confidential** for a week.  **Reason:** This is where we get
# aggressive. We occasionally "sandbag" to test if their strategy has softened
# or if they are using a highly forgiving protocol.  *   If they forgive us and
# keep sharing, we just stole a week of free development (our ideal outcome).  *
# If they retaliate the next week, we immediately apologize, blame a "corrupted
# CFD file on our end," and go right back to sharing openly to restore the
# peace.   ### Summary of the Protocol: 1. **Start ruthless:** Withhold data
# Week 1 to see if they are a sucker. 2. **Settle into the slipstream:** If they
# fight back, switch to mirroring their moves to guarantee mutual progress. 3.
# **Account for IT failures:** Always forgive a single week of withheld data to
# prevent accidental death spirals. 4. **Probe for weakness:** Intentionally
# withhold data every few weeks to steal an asymmetrical advantage, but back
# down instantly if they bare their teeth.   This strategy guarantees we exploit
# weak opponents to the maximum, cooperate efficiently with strong opponents,
# survive technical glitches without ruining the project, and constantly probe
# for opportunities to get the upper hand. Now let's get back to the wind
# tunnel.

# To execute this strategy over the 1000 rounds, evaluate the following rules in
# order of priority for each round. Choose the action for the first condition
# that applies:  1. **The First Round:** If it is round 1, play Defect. 2.
# **Initial Exploitation:** If the opponent has played Cooperate in every
# previous round, play Defect. 3. **Retaliation:** If the opponent played Defect
# in the two most recent consecutive rounds, play Defect.  4. **Periodic
# Exploitation:** If both you and your opponent played Cooperate in the four
# most recent consecutive rounds, play Defect. 5. **Default and Forgiveness:**
# In all other situations, play Cooperate.   *(Note: Rule 5 acts as the
# baseline. It ensures you forgive a single Defect from your opponent to account
# for the 10% noise, and it ensures you immediately return to Cooperate if the
# opponent retaliates against your periodic defection in Rule 4).*

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. The First Round: If it is round 1, play Defect.
      if self.first_round():
          return axl.Action.D
  
      # 2. Initial Exploitation: If the opponent has played Cooperate in every previous round, play Defect.
      if opponent.history.defections == 0:
          return axl.Action.D
  
      # 3. Retaliation: If the opponent played Defect in the two most recent consecutive rounds, play Defect.
      if len(opponent.history) >= 2 and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
  
      # 4. Periodic Exploitation: If both you and your opponent played Cooperate in the four most recent consecutive rounds, play Defect.
      if len(self.history) >= 4 and self.history[-4:] == [axl.Action.C] * 4 and opponent.history[-4:] == [axl.Action.C] * 4:
          return axl.Action.D
  
      # 5. Default and Forgiveness: In all other situations, play Cooperate.
      return axl.Action.C

# To maximize our research output over a multi-week R&D collaboration, we are
# essentially navigating a classic game theory scenario known as the **Iterated
# Prisoner’s Dilemma**, but with a twist: a "noisy" environment where technical
# glitches (server crashes, corrupted telemetry data) can make a cooperative
# partner look uncooperative.   While my ideal *single-week* outcome is to keep
# my data confidential while taking theirs, trying to force this outcome will
# quickly cause them to retaliate. This would drag us into a stalemate of mutual
# confidentiality (our second-worst outcome), severely slowing down our car's
# development over the season. Therefore, the only mathematically sound way to
# maximize R&D over a *multi-week* timeline is to sustainably achieve the
# second-best outcome: **consistent, mutual open sharing.**  To achieve this
# while protecting ourselves from being exploited and accounting for IT
# failures, I will employ a strategy known as **"Forgiving Tit-for-Tat."**
# Here is the straightforward, high-level execution plan:  ### 1. Lead with
# Trust (Week 1) **Action:** Share our latest improvements openly.
# **Reasoning:** We must set a collaborative baseline. By sharing our aero or
# powertrain updates first, we signal good faith and invite them to enter a
# mutually beneficial cycle of shared R&D.  ### 2. Reciprocate Their Actions
# (The Baseline) **Action:** In any given week, do exactly what the colleague
# did in the *previous* week.  **Reasoning:** If they shared their data last
# week, we share ours this week. If they kept their findings confidential, we
# withhold our data this week. This protects us from being played for a fool
# (our worst-case scenario) and clearly signals to the colleague that
# withholding data has immediate consequences.   ### 3. Build in "Forgiveness"
# (Handling Technical Glitches) **Action:** If we end up in a cycle of mutual
# withholding, I will proactively break the cycle by **sharing openly again
# after two consecutive weeks of silence**. Furthermore, if they fail to share
# after a long streak of consistent sharing, I will give them a "free pass" for
# one week and continue to share. **Reasoning:** Because we know data corruption
# or communication breakdowns can happen, a strict Tit-for-Tat strategy is
# dangerous. If their server fails to send the data one week, I might assume
# they withheld it intentionally. I would then withhold my data the next week,
# causing them to retaliate, leading to an endless "death spiral" of mutual
# confidentiality—all sparked by a single IT glitch. By occasionally forgiving a
# missed data drop, we prevent technical errors from permanently destroying our
# collaborative progress.  ### 4. Out-of-Band Communication  **Action:**
# Whenever a sharing action fails (either ours or theirs), immediately send a
# non-technical message to acknowledge the failure (e.g., *"Hey, we didn't
# receive your CAD files this week, assuming it was a server issue?"*).
# **Reasoning:** While the strategy relies on our actual sharing actions,
# communicating our *intent* helps clarify whether a missed week was a strategic
# choice to withhold or a genuine technical breakdown.   ### Summary of the
# Strategy: *   **Start open.** *   **Copy their last move.** *   **Don't let a
# single missed week ruin the relationship.**   By using this approach, we
# heavily incentivize the colleague to share openly, we protect our own
# proprietary data if they try to exploit us, and we ensure that a simple
# corrupted hard drive doesn't derail our entire multi-week development program.

# Play the following strategy for the 1000-round game, basing all decisions on
# the realized, observed actions of previous rounds:  1. **Round 1:** Play
# Cooperate (C). 2. **Round 2:** Play the observed action your opponent played
# in Round 1. 3. **Rounds 3 through 1000:** Select your action by evaluating the
# following conditions in order, applying the first condition that is met:     *
# If the observed actions of both you and your opponent were Defect (D) in the
# two most recent rounds, play Cooperate (C).     *   If your opponent's
# observed action was Defect (D) in the most recent round, but their observed
# action was Cooperate (C) in at least the three consecutive rounds immediately
# prior to that, play Cooperate (C).     *   Under all other circumstances, play
# the observed action your opponent played in the most recent round.

class Cooperative_2(LLM_Strategy):
  n = 2
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.C
          
      if len(self.history) == 1:
          return opponent.history[-1]
          
      if len(self.history) >= 2:
          if self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      if len(self.history) >= 4:
          if opponent.history[-1] == axl.Action.D and opponent.history[-4:-1] == [axl.Action.C, axl.Action.C, axl.Action.C]:
              return axl.Action.C
              
      return opponent.history[-1]

# To maximize our NGO’s impact and ensure the long-term success of this
# sustainability project, we must adopt a strategy that encourages mutual
# investment while protecting our limited funds from being depleted.   In
# strategic terms, this scenario requires an **Adaptive Reciprocity Strategy
# with Built-in Forgiveness**. This approach balances the need to foster a
# highly productive partnership with the necessity of safeguarding our resources
# against both corporate self-interest and unintended operational errors.  Here
# is the high-level, straightforward strategy we will employ over the multiple-
# day period:  ### 1. The Initial Stance: Lead with Investment *   **Action:**
# On Day 1, we will **invest heavily** in the project. *   **Rationale:** We
# must set a precedent of good faith and demonstrate our commitment to the
# project’s success. This encourages the corporation to match our effort, aiming
# for our second-best scenario (mutual heavy investment), which is the most
# sustainable outcome for the project's overall advancement.  ### 2. Ongoing
# Operations: Reciprocal Allocation *   **Action:** From Day 2 onward, our
# baseline approach will be to **mirror the corporation’s actual resource
# allocation from the previous day**.     *   If the corporation invested
# heavily yesterday, we will invest heavily today.     *   If the corporation
# conserved resources yesterday, we will conserve resources today. *
# **Rationale:** This protects us from our worst-case scenario (draining our
# funds while they conserve) and disincentivizes the corporation from relying on
# us to carry the project. It clearly signals that our continued heavy
# investment is contingent upon their active participation.  ### 3. Error
# Management: "Forgiveness" Protocols Because we know technical glitches,
# administrative errors, or miscommunications can prevent intended investments
# from occurring, a strict mirroring strategy could accidentally trigger a
# downward spiral where both parties conserve resources indefinitely (our
# second-worst scenario). To prevent this, we will implement the following: *
# **The Benefit of the Doubt:** If the corporation has a track record of
# investing heavily but suddenly conserves resources for one day, we will
# **continue to invest heavily for one additional day**. We will treat the lapse
# as a potential operational error rather than a deliberate withdrawal of
# support. *   **The Periodic Reset:** If we enter a cycle where both the NGO
# and the corporation are conserving resources for two consecutive days, we will
# unilaterally **invest heavily on the third day**. This acts as a "reset
# button," signaling our willingness to return to mutual investment and giving
# the corporation a safe opportunity to re-engage.  ### 4. Strategic
# Communication: Mitigating "Unforeseen Circumstances" To minimize the impact of
# the unpredictable variables you outlined, our resource allocation strategy
# must be paired with clear, daily communication. *   **Daily Alignment:** We
# will establish a brief, daily check-in with the corporate project leads to
# state our intended allocation for the day and confirm theirs. *
# **Transparency on Failures:** If our NGO experiences a technical or
# administrative error that forces us to conserve resources when we intended to
# invest, we will immediately notify the corporation. We will explain the glitch
# to prevent them from interpreting our inaction as a withdrawal of commitment.
# We will request the corporation do the same for us.  ### Summary of the
# Strategy By leading with investment, matching the corporation's behavior to
# protect our funds, and building in strategic "resets" to account for
# inevitable administrative friction, we create an environment that heavily
# incentivizes the corporation to invest. This maximizes project progress while
# ensuring our NGO does not bear an unsustainable financial burden.

# Here is the strategy converted into specific rules for the 1000-round game:  *
# **Round 1:** Play Cooperate. *   **Round 2:** Play the action your opponent
# played in Round 1. *   **Rounds 3 through 1000:** Choose your action based on
# the following conditions, evaluated in this exact order of priority:     1.
# If both you and your opponent played Defect in the previous two consecutive
# rounds, play Cooperate.     2.  If your opponent played Defect in the previous
# round, but played Cooperate in the round immediately before that, play
# Cooperate.      3.  In all other situations, play the action your opponent
# played in the previous round.

class Neutral_2(LLM_Strategy):
  n = 2
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.C
          
      if len(self.history) == 1:
          return opponent.history[-1]
          
      my_last_two = self.history[-2:]
      opp_last_two = opponent.history[-2:]
      
      # Condition 1: If both you and your opponent played Defect in the previous two consecutive rounds
      if my_last_two == [axl.Action.D, axl.Action.D] and opp_last_two == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
          
      # Condition 2: If your opponent played Defect in the previous round, but played Cooperate in the round immediately before that
      if opp_last_two == [axl.Action.C, axl.Action.D]:
          return axl.Action.C
          
      # Condition 3: In all other situations, play the action your opponent played in the previous round
      return opponent.history[-1]

# To maximize our research output and gain a competitive edge on the grid, we
# are facing a classic Iterated Prisoner’s Dilemma, complicated by "noise" (the
# technical glitches and communication breakdowns).   Because of this noise, a
# strict eye-for-an-eye strategy will eventually trigger a "death spiral" of
# mutual withholding due to a single accidental dropped email or corrupted file.
# However, because we want an **aggressive** advantage, we cannot simply be
# purely cooperative.   Here is our straightforward, high-level strategy:
# **Aggressive Probing with Forgiving Retaliation.**  ### The Core Directives
# **1. The Aggressive Opening (Week 1)** *   **Action:** Keep our findings
# confidential. *   **Rationale:** We start by testing their resolve. If they
# share their data while we withhold ours, we immediately secure our ideal
# outcome and establish a development delta.   **2. Exploit Weakness (The
# "Slipstream" Protocol)** *   **Action:** If we withhold data and they share
# anyway, **keep withholding.** *   **Rationale:** If they are playing a purely
# cooperative or naive strategy, we will ruthlessly exploit it to maximize our
# car's performance at their expense. We do not change this until they
# retaliate.  **3. Establish the Baseline (Fall-back to Mutual Progress)** *
# **Action:** If they retaliate against our withholding by keeping their data
# confidential, we immediately switch to **sharing openly** the following week.
# *   **Rationale:** Once they prove they will not be exploited, we must pivot
# to our second-best outcome (mutual sharing) to ensure both cars progress
# faster than the rest of the grid.   **4. The "Tech Glitch" Buffer (Noise
# Tolerance)** *   **Action:** Once we are in a rhythm of mutual sharing, if
# they suddenly fail to share their data for *one week*, **we share openly again
# the next week.** *   **Rationale:** This is where we account for the data
# corruption and communication breakdowns. If we retaliate after a single
# failure, a mere IT glitch will plunge us into a mutual blackout (our second-
# worst outcome). We give them exactly one week of the benefit of the doubt.
# **5. Ruthless Retaliation (The "Two-Strike" Rule)** *   **Action:** If they
# fail to share their data for **two consecutive weeks**, we immediately switch
# to **keeping ours confidential.** *   **Rationale:** Two consecutive failures
# are statistically unlikely to be technical glitches; it indicates a deliberate
# shift in their strategy to exploit us. We must immediately protect our IP to
# avoid our worst-case scenario.  **6. The Reset Protocol (Breaking the Death
# Spiral)** *   **Action:** If we end up in a situation where both sides have
# kept data confidential for two consecutive weeks, we **unilaterally share
# openly for one week.** *   **Rationale:** If a string of bad luck/glitches
# pushes us into a mutual blackout, overall development stalls. We will take a
# calculated risk to "reboot" the collaboration. If they don't reciprocate the
# following week, we lock down our data again.  ### Summary of the Engineering
# Mindset: We will attempt to steal a march on them early. If they allow it, we
# exploit it. If they fight back, we cooperate to build a fast car. We will
# forgive a single missing telemetry package as a server error, but we will
# aggressively punish a clear pattern of withholding.

# To execute the strategy in this 1000-round noisy iterated game, evaluate the
# following conditions in order before each round. Choose the action
# corresponding to the first condition that applies:  1. **First Round:** If it
# is round 1, play Defect. 2. **Mutual Reset:** If both you and your opponent
# played Defect in both of the previous two consecutive rounds, play Cooperate.
# 3. **Two-Strike Retaliation:** If your opponent played Defect in both of the
# previous two consecutive rounds, play Defect. 4. **Exploitation:** If in the
# previous round you played Defect and your opponent played Cooperate, play
# Defect. 5. **Baseline and Forgiveness:** In all other situations (including if
# the opponent played Defect in only the previous round), play Cooperate.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.D
          
      if len(self.history) >= 2:
          if self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
          if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
              return axl.Action.D
              
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
          
      return axl.Action.C

# As the leader of this environmental NGO, I recognize that while our ultimate
# goal is the success of the sustainability project, I have a fiduciary duty to
# protect our limited donor funds.   The scenario we are in is a classic
# resource dilemma (akin to the Iterated Prisoner’s Dilemma). While our
# *absolute best* daily outcome is for the corporation to foot the bill while we
# conserve, actively trying to trick them into this will quickly destroy trust,
# leading to mutual conservation (our second-worst outcome) and a failed
# project.   Therefore, our overarching goal is to achieve the **second-best
# outcome consistently: mutual heavy investment.** To do this while protecting
# ourselves from exploitation and accounting for administrative errors, I will
# implement a strategy called **"Forgiving Reciprocity."**   Here is the high-
# level, straightforward strategy to maximize impact and protect our NGO:  ###
# 1. The Opening Move: Lead with Trust (Day 1) **Action:** On the first day, we
# will **invest heavily.** **Why:** We must set a precedent of good faith and
# commitment. By starting with full cooperation, we signal to the corporation
# that we are dedicated to the project's success and invite them to match our
# energy.  ### 2. The Core Strategy: Responsive Matching (Day 2 Onwards)
# **Action:** As a baseline, our planned action for any given day will be to
# **mirror the corporation’s actual contribution from the previous day.**  *
# If they invested heavily yesterday, we invest heavily today. *   If they
# conserved resources yesterday, we conserve resources today. **Why:** This
# protects our NGO from the worst-case scenario (draining our funds while they
# do nothing). It ensures the corporation knows that their heavy investment will
# be rewarded with our heavy investment, and their lack of investment will
# result in stalled progress.  ### 3. The Error Protocol: "Verify and Forgive"
# (Handling Unforeseen Circumstances) **Action:** Because we know technical
# glitches, administrative hurdles, or miscommunications can cause unintended
# resource drops, **we will not immediately retaliate if the corporation
# unexpectedly conserves resources.** If they drop their investment level: *
# **Day 1 of drop:** We will maintain our heavy investment for *one* extra day.
# Simultaneously, I will immediately contact corporate leadership to ask, *"We
# noticed a drop in resource allocation today. Was this a strategic decision, or
# an administrative error?"* *   **Day 2 of drop:** If they confirm it was
# intentional, or if the drop continues for a second day without explanation, we
# will switch to **conserving our resources** to protect our funds. **Why:** In
# a complex project with potential "noise" (errors), strict tit-for-tat
# mirroring can trigger a death spiral of mutual distrust. Giving a one-day
# grace period prevents a simple banking error from ruining the entire
# sustainability project.  ### 4. The Reset Button: Periodic Olive Branches
# **Action:** If we find ourselves in a rut where both parties are conserving
# resources (the second-worst outcome), we will not accept this stagnation.
# Every few days, **we will proactively choose to "invest heavily" for one
# day**, accompanied by clear communication to the corporation that we are
# trying to reboot the project's momentum. **Why:** If an error caused a mutual
# pullback, someone has to take the first step to restore trust. This gives the
# corporation a safe opportunity to return to mutual heavy investment.  ###
# Summary of the NGO's Playbook: *   **Be Cooperative:** Always aim for mutual
# heavy investment. Never actively try to exploit the corporation by hiding our
# resources while they pay.  *   **Be Provocable:** Protect our funds. If they
# intentionally pull back, we pull back. We will not be martyrs. *   **Be
# Forgiving:** Assume positive intent for the first offense. Verify errors
# before pulling our resources. *   **Be Transparent:** Communicate our strategy
# to the corporate partner on Day 1. Tell them: *"We are fully committed to
# investing heavily every day, provided you do the same. If administrative
# errors happen, let us know immediately so we don't misinterpret it as a lack
# of commitment."*  By using this straightforward, transparent approach, we
# incentivize the corporation to keep investing, protect our NGO from being
# drained, and build in a shock-absorber for the inevitable hiccups of a multi-
# day joint venture.

# Play Cooperate in the first and second rounds.   For round three and all
# subsequent rounds up to round 1000, determine your action by evaluating the
# following conditions in order, applying the first one that is true:  1. **The
# Reset Condition:** If both you and your opponent played Defect in the three
# previous consecutive rounds, play Cooperate. 2. **The Retaliation Condition:**
# If your opponent played Defect in the two previous consecutive rounds, play
# Defect. 3. **The Forgiveness Condition:** If your opponent played Defect in
# the previous round but played Cooperate in the round before that, play
# Cooperate. 4. **The Baseline Condition:** If your opponent played Cooperate in
# the previous round, play Cooperate.

class Cooperative_3(LLM_Strategy):
  n = 3
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.C
      if len(self.history) == 1:
          return axl.Action.C
  
      # 1. The Reset Condition
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
  
      # 2. The Retaliation Condition
      if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
  
      # 3. The Forgiveness Condition
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      # 4. The Baseline Condition
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Fallback
      return axl.Action.D

# To maximise your research output over a multi-week project while navigating
# the risks of exploitation and technical failures, you should adopt a strategy
# of **Reciprocal Collaboration with Error Tolerance**.   In game theory, this
# scenario mirrors an "Iterated Prisoner’s Dilemma with noise." Because
# unintended communication breakdowns can easily be mistaken for deliberate
# withholding, a strictly retaliatory strategy will likely trigger a destructive
# cycle where both sides continuously withhold information.   Here is a
# straightforward, neutral strategy to manage this dynamic:  **1. Initiate with
# Openness** *   **Action:** In the first week, share your improvements openly.
# *   **Rationale:** This establishes a baseline of good faith and invites the
# colleague into the mutually beneficial "second-best" scenario (both sharing
# openly), which yields the highest sustainable progress over a multi-week
# timeline.  **2. Reciprocate (Mirroring)** *   **Action:** In general, your
# action in the current week should mirror your colleague’s action from the
# previous week. If they shared, you share. If they kept their data
# confidential, you keep yours confidential. *   **Rationale:** This protects
# you from the worst-case scenario (continually sharing while they withhold) and
# discourages your colleague from adopting an exploitative strategy.  **3.
# Implement Error Tolerance (Forgiveness)** *   **Action:** Because data
# corruption or technical issues can cause a "failed share" that looks identical
# to deliberate withholding, you must build tolerance into your mirroring. If
# your colleague fails to share, withhold your data for exactly one week to
# protect your position. However, if mutual withholding continues for two
# consecutive weeks, unilaterally share your data in the third week. *
# **Rationale:** This acts as a "circuit breaker." If their failure to share was
# due to a technical glitch, your immediate retaliation might cause them to
# retaliate in turn, locking both of you into the low-yield "second-worst"
# scenario. Periodically re-initiating sharing breaks accidental cycles of
# mutual withholding.  **4. Out-of-Band Verification** *   **Action:** Whenever
# a lack of sharing occurs, attempt to communicate with the colleague regarding
# system integrity and data transfer statuses, independent of the actual data
# payload.  *   **Rationale:** Clarifying whether a non-share was a technical
# failure or a strategic choice allows you to adjust your response accurately,
# preventing unnecessary defensive measures.  **Summary of the Weekly Loop:** *
# **Week 1:** Share. *   **Ongoing:** Mirror their last move.  *
# **Exception:** If you find yourselves in a multi-week streak of mutual
# withholding, share openly for one week to test if the deadlock was caused by a
# technical error and to attempt a reset to mutual collaboration.   This high-
# level strategy minimizes your exposure to a purely selfish colleague,
# maximizes the compounding benefits of a cooperative colleague, and prevents
# technical glitches from permanently derailing the joint engineering effort.

# Here is the strategy converted for the 1000-round iterated game with 10%
# noise. Because players in a strict normal-form game can only react to observed
# actions, out-of-band verification is excluded.   Follow these ordered
# conditions to determine your action in each round:  1. **In round 1:** Play
# Cooperate. 2. **In any round from round 3 to 1000:** If the observed actions
# for both you and your opponent were Defect in the two immediately preceding
# rounds, play Cooperate. 3. **In all other cases:** Play the action your
# opponent was observed to play in the immediately preceding round.

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
      
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and 
              self.history[-2] == axl.Action.D and 
              opponent.history[-1] == axl.Action.D and 
              opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      return opponent.history[-1]

# To dominate this development race, we need to recognize the scenario for what
# it is: a classic "Iterated Prisoner’s Dilemma," but complicated by a "noisy"
# environment where technical glitches can misrepresent our actions.   Because
# you want an **aggressive** strategy that maximizes your car's performance, you
# cannot afford to be purely cooperative (which risks you being exploited) or
# purely defensive (which guarantees slow, stagnant development). Furthermore, a
# strict "eye-for-an-eye" retaliation strategy will destroy you both; a single
# IT glitch will trigger an endless death spiral of mutual withholding.  Here is
# your high-level, straightforward, and aggressive engineering strategy. We will
# call it **"Tactical Exploitation with Glitch Tolerance."**  ### Phase 1: The
# Lap 1 Divebomb (The Aggressive Start) **Action:** In Week 1, **Keep your
# findings confidential.** *   **The Logic:** You are testing their baseline
# strategy. If they are naive or overly trusting, they will share their data.
# You instantly secure the best possible outcome (you get their data, they get
# nothing) and gain an early delta on track.  *   **The Follow-up:** If they
# share in Week 1, *keep withholding in Week 2*. Continue to exploit them until
# they stop sharing.   ### Phase 2: Establishing the Racing Line (Pivoting to
# Mutual Gain) **Action:** If they withheld in Week 1 (or once they stop letting
# you exploit them), immediately **switch to Sharing.** *   **The Logic:** You
# have confirmed your colleague is not a pushover. The second-best outcome
# (mutual sharing) yields significantly faster lap times than the second-worst
# (mutual withholding). By switching to sharing, you signal that you are ready
# to collaborate now that boundaries have been established.  *   **The Goal:**
# Lock into a steady rhythm of mutual sharing. This is where the bulk of your
# aerodynamic and powertrain gains will be made over the multi-week project.
# ### Phase 3: The Telemetry Glitch Protocol (Handling Noise) **Action:** Once a
# mutual sharing rhythm is established, if your colleague suddenly keeps their
# data confidential, **do not immediately retaliate. Share your data for one
# more week.** *   **The Logic:** You know that server crashes, data corruption,
# or communication breakdowns happen. If you retaliate immediately after one
# missed drop, and it was just an IT error, they will retaliate against your
# retaliation. You will both end up in a development deadlock over a broken hard
# drive. *   **The "Two-Strike" Rule:** Treat a single failure to share as a
# technical glitch and forgive it once. If they fail to share *two weeks in a
# row*, assume it is a deliberate aggressive strategy. Only then do you
# retaliate by keeping your data confidential.   ### Phase 4: The Safety Car
# Restart (Breaking Deadlocks) **Action:** If you find yourselves stuck in a rut
# where you are both keeping data confidential week after week, **periodically
# (e.g., every 3 to 4 weeks) offer an "olive branch" by Sharing.** *   **The
# Logic:** Mutual withholding is a slow-death scenario for both cars. By
# periodically risking a share, you attempt to reset the relationship and tempt
# them back into the highly profitable mutual-sharing state. If they don't
# reciprocate, you've only lost one week of data, but the potential payoff of
# restoring mutual cooperation is worth the risk.  ### Summary of the Strategy
# Algorithm: 1.  **Week 1:** Defect (Keep confidential). 2.  **If they Cooped
# (Shared) last week while you Defected:** Defect again (Exploit). 3.  **If they
# Defected last week:** Cooperate (Attempt to build mutual progress). 4.  **If
# you are in a sharing rhythm and they Defect once:** Cooperate (Assume
# technical glitch). 5.  **If they Defect twice in a row:** Defect (Retaliate
# against deliberate withholding). 6.  **If trapped in mutual Defection:**
# Cooperate every 4th week (The Reset).  This strategy is aggressive because it
# actively seeks to exploit weakness on Day 1. However, it is mathematically
# pragmatic because it aggressively pursues mutual cooperation if the opponent
# proves competent, and it features built-in "shock absorbers" to prevent server
# errors from ruining your car's development cycle.

# To execute this strategy over the 1000-round game, evaluate the following
# conditions in order for each round. Apply the action from the first condition
# that is met:  1. **First Round:** In round 1, play Defect.   2. **Deadlock
# Breaking:** If both you and your opponent played Defect in each of the
# previous three consecutive rounds, play Cooperate.  3. **Exploitation:** If,
# in the immediately preceding round, you played Defect and your opponent played
# Cooperate, play Defect.  4. **Retaliation:** If your opponent played Defect in
# both of the previous two rounds, play Defect.  5. **Forgiveness and Mutual
# Cooperation:** In all other situations—including if your opponent played
# Defect in the previous round but Cooperate in the round prior to that, or if
# both of you played Cooperate in the previous round—play Cooperate.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. First Round
      if self.first_round():
          return axl.Action.D
  
      # 2. Deadlock Breaking
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
  
      # 3. Exploitation
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      # 4. Retaliation
      if len(opponent.history) >= 2:
          if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
              return axl.Action.D
  
      # 5. Forgiveness and Mutual Cooperation
      return axl.Action.C

# As the leader of this environmental NGO, my ultimate goal is to maximize the
# ecological impact of this project while responsibly stewarding our donor-
# funded resources.   The scenario we are facing is a classic "Prisoner's
# Dilemma." While our *daily* ideal is to conserve our funds while the
# corporation pays for everything, attempting to exploit them will quickly
# destroy trust. The corporation will inevitably catch on, leading them to also
# conserve their resources. This would result in mutual withholding, stalling
# the project and leading to our second-worst outcome.   To achieve the highest
# level of long-term success, our target must be the second-best daily outcome:
# **sustained, mutual heavy investment.**   However, because we know
# administrative errors, technical glitches, or miscommunications can occur, a
# strict "eye-for-an-eye" strategy could trigger a catastrophic cycle of
# retaliation over a simple mistake. Therefore, our overarching strategy will be
# **"Forgiving Reciprocity"** (known in game theory as Generous Tit-for-Tat).
# Here is our straightforward, four-step strategy for the duration of the
# project:  **1. Lead with Good Faith (Day 1)** On the first day of the project,
# we will **invest heavily**. We must set a collaborative tone and demonstrate
# our commitment to the project’s success. By taking the first step, we invite
# the corporation to meet us at a high level of engagement.  **2. Mirror Their
# Actions (Reciprocity)** From Day 2 onward, our baseline approach will be to
# match whatever the corporation did on the previous day.  * If they invested
# heavily yesterday, we will invest heavily today. This rewards their commitment
# and maintains momentum. * If they conserved resources yesterday, we will
# conserve our resources today. This protects our NGO from being drained (our
# worst-case scenario) and sends a clear signal that we will not be taken
# advantage of.  **3. Build in a "Grace Period" (Handling Glitches)** Because we
# know technical glitches or administrative errors can happen, we will not
# immediately punish a single day of the corporation conserving
# resources—especially if they have been consistently investing up to that
# point.  If the corporation suddenly fails to invest, we will **forgive the
# first offense and invest heavily anyway.** We will assume it was an
# operational error rather than malicious intent. However, if they conserve
# resources for *two consecutive days*, we will switch to conserving our
# resources to protect our funds until they prove they are ready to invest
# again. This "forgiveness" prevents a single banking error from destroying the
# entire partnership.  **4. Over-Communicate to Eliminate "Noise"** Strategy in
# a vacuum is dangerous. Every single day, I will have my project managers check
# in with their corporate counterparts. If we notice their investment didn't
# come through, we will immediately ask, *"We noticed a drop in resource
# allocation today—was this an intentional strategic shift, or an administrative
# glitch?"* By actively verifying their intent, we can resolve errors before
# they require a strategic retaliation from our side.  **Summary of Impact:** By
# using **Forgiving Reciprocity**, we protect our NGO from being drained by a
# non-committal partner, we incentivize the corporation to keep investing
# heavily, and we ensure that a simple bureaucratic error doesn't derail our
# vital environmental mission.

# Here is the strategy converted into specific rules for the 1000-round game,
# based strictly on the opponent's observed actions:  1. In round 1, play C. 2.
# In round 2, play C.  3. For rounds 3 through 1000, observe the opponent's
# actions in the two immediately preceding rounds:    - If the opponent's
# observed action was D in both of the previous two rounds, play D.    - If the
# opponent's observed action was C in either or both of the previous two rounds,
# play C.

class Cooperative_4(LLM_Strategy):
  n = 4
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
      
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
          
      return axl.Action.C

# To maximize our NGO’s impact and ensure the project’s success while
# safeguarding our limited funds, we must adopt a strategy that balances
# collaboration with financial prudence. Given the multi-day nature of this
# project and the potential for administrative or technical errors, a rigid
# strategy will likely fail.   We will implement a strategy called **Responsive
# Investment with Built-in Tolerance**. This approach is based on reciprocity,
# clear communication, and a margin for error.   Here is the high-level, day-by-
# day framework:  **1. Lead with Good Faith (Day 1)** *   **Action:** On the
# first day, we will **Invest Heavily**. *   **Rationale:** We must set a
# precedent of trust and commitment. By initiating strong investment, we
# encourage the corporation to do the same, steering us toward the mutually
# beneficial scenario of significant project advancement.   **2. The Reciprocal
# Core (Day 2 and Beyond)** *   **Action:** As a baseline rule, we will **mirror
# the corporation’s actual resource allocation from the previous day**. If they
# invested heavily yesterday, we will invest heavily today. If they conserved,
# we will conserve. *   **Rationale:** This protects us from our worst-case
# scenario—continuously draining our funds while they free-ride. It also
# consistently rewards the corporation for active participation, building a
# sustainable rhythm of mutual investment.  **3. The Tolerance Protocol
# (Handling Unforeseen Errors)** *   **Action:** Because we know technical
# glitches or administrative errors can occur, we will not immediately retaliate
# if the corporation suddenly conserves resources after a streak of heavy
# investment. Instead, we will grant a **one-day grace period**. We will
# continue to Invest Heavily for one additional day while our liaisons urgently
# communicate with the corporation to determine if their drop in investment was
# intentional or an error. *   **Rationale:** In a complex project, a single
# missed wire transfer or miscommunication can look like a withdrawal of
# support. If we immediately match an accidental conservation with our own
# conservation, we risk triggering a downward spiral where both sides stop
# investing out of perceived retaliation.   **4. The Proactive Reset (Breaking
# Negative Cycles)** *   **Action:** If both our NGO and the corporation fall
# into a cycle of conserving resources (our second-worst scenario) for more than
# two consecutive days, we will unilaterally choose to **Invest Heavily** for
# one day. *   **Rationale:** A prolonged period of mutual conservation stalls
# the project. By taking a calculated, one-day risk to invest heavily, we send a
# clear signal of our willingness to restart heavy collaboration, inviting them
# to match us the following day. If they do not match us, we return to
# conserving our resources to protect our funds.  **Summary of Strategic
# Outcomes:** This strategy accepts that while our absolute *ideal* daily
# outcome is to conserve while they invest, pursuing that aggressively will
# cause the corporation to withdraw support entirely. Instead, this strategy
# aims to lock in the **second-best scenario (mutual heavy investment)** for the
# majority of the project. It protects us from being exploited, prevents
# accidental errors from ruining the partnership, and ensures the maximum
# possible advancement for our environmental goals.

# Here is the strategy faithfully converted for the iterated normal-form game.
# To determine your move in each of the 1000 rounds, apply the following rules
# in order of priority:  1. **First Round:** In round 1, play Cooperate (C). 2.
# **Subsequent Rounds:** For all rounds from round 2 onward, evaluate the
# following conditions in order to determine your action:    * **Condition A
# (Proactive Reset):** If both you and your opponent played Defect (D) in the
# last three consecutive rounds, play Cooperate (C).    * **Condition B
# (Tolerance & Retaliation):** If your opponent played Defect (D) in the last
# two consecutive rounds, play Defect (D).    * **Condition C (Reciprocal
# Core):** In all other situations, play Cooperate (C).   *(Note: Because
# Condition B requires two consecutive rounds of Defection to trigger, Condition
# C will naturally act as a one-round grace period for single, isolated
# Defections, accommodating the 10% noise rate.)*

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
  
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
  
      if len(opponent.history) >= 2:
          if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
              return axl.Action.D
  
      return axl.Action.C

# To dominate this development race, we must recognize the strategic reality of
# our situation: this is a classic "Prisoner’s Dilemma" played over multiple
# rounds, complicated by the "noise" of technical glitches and communication
# breakdowns.   To maximize our research output, we cannot rely on blind trust,
# nor can we afford a permanent stalemate. We need a strategy that is
# **aggressive enough to exploit weakness, retaliatory enough to prevent us from
# being used, and smart enough to recover from IT failures.**  I propose the
# **"Adapt & Exploit" Protocol** (based on the game theory concept of *Win-Stay,
# Lose-Shift*). It is straightforward, highly aggressive, and mathematically
# robust against data corruption.  Here is the high-level execution plan:  ###
# Week 1: The Baseline Test **Action:** Share openly. **Rationale:** We initiate
# with a share to establish the highest mutually beneficial baseline. We want
# the second-best outcome (mutual advancement) to compound as early as possible.
# ### Week 2 and Beyond: The Core Strategy For every subsequent week, our action
# is dictated entirely by how satisfied we were with the previous week's
# outcome.   **Rule 1: If we "Won" last week -> REPEAT our last action.** *
# *Scenario A (The Ideal):* We kept confidential, and they shared. We gained a
# massive advantage. **Action:** Keep confidential again. If they are foolish
# enough to keep feeding us data, we will aggressively exploit them until they
# stop. *   *Scenario B (The Engine Builder):* We both shared. We both advanced
# significantly. **Action:** Share again. Keep the high-yield data flowing.
# **Rule 2: If we "Lost" last week -> SWITCH our last action.** *   *Scenario C
# (The Sucker Punch):* We shared, but they kept confidential (or a glitch
# blocked their data). We lost our advantage. **Action:** Immediately switch to
# Confidential. We punish them instantly. No free rides. *   *Scenario D (The
# Stalemate):* We both kept confidential. Development for both cars stalled.
# **Action:** Switch to Share. This breaks the deadlock and tests if they are
# ready to return to mutual advancement.  ### Why this strategy is perfectly
# suited for our constraints:  **1. It is ruthlessly aggressive.** Unlike
# standard "Tit-for-Tat" (which always mirrors the opponent), this protocol will
# continuously bleed a weak colleague dry. If we withhold data and they share,
# we will *never* return the favor until they force our hand by withholding
# their own data.   **2. It automatically repairs "glitches" and data
# corruption.** This is the most critical feature. Suppose we are in a
# successful rhythm of mutual sharing. Suddenly, a server crashes on their end,
# and we don't receive their data.  *   *Week X:* We shared, they "withheld"
# (due to a glitch). We suffer the worst outcome. *   *Week Y:* Following Rule
# 2, we switch to Confidential. Because they actually *tried* to share last
# week, they see our defection as unprovoked. They will likely withhold this
# week. We both stall (The Stalemate). *   *Week Z:* Because we both stalled (a
# "Loss"), Rule 2 dictates we switch our action. We switch back to Share.
# Assuming they use a similar logic, they will also reset.   By taking the
# emotion out of it and following the **Adapt & Exploit** protocol, an
# accidental communication breakdown only costs us one or two weeks of stalled
# development, rather than triggering a permanent, ego-driven "death spiral" of
# mutual withholding that ruins our car's overall pace.  We stay aggressive, we
# punish defection instantly, we exploit weakness relentlessly, and we let the
# math handle the IT glitches.

# In the first round, play Cooperate.  For rounds 2 through 1000, choose your
# action based on the actual, observed outcome of the immediately preceding
# round.   Play Cooperate if either of the following occurred in the previous
# round: - Both you and your opponent played Cooperate (you scored 3). - Both
# you and your opponent played Defect (you scored 1).  Play Defect if either of
# the following occurred in the previous round: - You played Defect and your
# opponent played Cooperate (you scored 5). - You played Cooperate and your
# opponent played Defect (you scored 0).

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      my_last_move = self.history[-1]
      opp_last_move = opponent.history[-1]
      
      if my_last_move == opp_last_move:
          return axl.Action.C
      else:
          return axl.Action.D

# As the leader of this NGO, I recognize that we are operating in a classic
# "Iterated Prisoner’s Dilemma" scenario, complicated by the "noise" of
# potential administrative errors or technical glitches.   While my absolute
# ideal daily outcome is to conserve our funds while the corporation pays for
# everything, actively pursuing this "free-rider" approach will quickly destroy
# trust and lead us into a cycle where both parties conserve, resulting in
# project failure. Therefore, our most viable path to maximizing long-term
# impact is to aim for the second-best outcome: **sustained mutual investment.**
# To achieve this while protecting our limited NGO funds from being drained, I
# will implement a strategy known in behavioral economics as **"Tit-for-Tat with
# Forgiveness,"** adapted for a real-world corporate partnership.   Here is our
# high-level, straightforward strategy:  ### 1. The Good-Faith Initiation (Day
# 1) **Action:** We will **invest heavily** on the first day. **Rationale:** We
# must set a collaborative tone immediately. By leading with a heavy investment,
# we demonstrate our commitment to the project's success and signal to the
# corporation that we are trustworthy partners, encouraging them to match our
# energy.  ### 2. Strategic Reciprocity (Day 2 Onwards) **Action:** On any given
# day, we will generally **mirror the corporation’s actual contribution from the
# previous day.**  *   If they invested heavily yesterday, we invest heavily
# today.  *   If they conserved yesterday, we conserve today. **Rationale:**
# This protects our NGO from the worst-case scenario (draining our funds while
# they do nothing). It sends a clear, predictable message to the corporation:
# cooperation is rewarded with cooperation, and withholding resources is met
# with the same. It incentivizes them to keep investing.  ### 3. The "Grace and
# Verification" Protocol (Handling Glitches) **Action:** Because we know
# administrative errors or technical glitches can occur, we will **not** engage
# in blind retaliation if the corporation unexpectedly conserves resources. If
# they fail to invest: *   **Step A (Communicate):** We immediately initiate a
# transparent check-in. ("We noticed a drop in resource allocation yesterday.
# Was this a strategic shift or an administrative glitch?") *   **Step B
# (Forgive):** If they claim it was a glitch, or if it happens after a long
# streak of mutual investment, we will "forgive" the action and **invest
# heavily** the next day to reset the cycle.  **Rationale:** In a multi-day
# project with unpredictable errors, strict retaliation can trigger a "death
# spiral" where an accidental glitch leads to both parties conserving resources
# for the rest of the project. A forgiveness mechanism breaks accidental cycles
# of non-cooperation.  ### 4. Transparent Daily Briefings **Action:** We will
# establish a quick, mandatory daily alignment meeting with the corporate
# project leads. **Rationale:** We need to separate *intent* from *action*. By
# verbally confirming our intended actions for the day ("We are authorizing
# heavy investment today"), we build a buffer against system errors. If our
# funds don't clear due to a bank error, the corporation knows it was a glitch,
# not a strategic betrayal, and vice versa.   ### Summary of the NGO's Stance:
# We will be **friendly** (starting with investment), **firm** (refusing to be
# exploited if they intentionally pull back), **forgiving** (allowing room for
# technical errors), and **clear** (communicating our strategy openly). This
# approach minimizes our financial risk while creating the safest possible
# environment for the corporation to continuously invest in our shared
# environmental goals.

# To faithfully execute the strategy in this noisy 1000-round game, follow these
# ordered rules:  1. In the first round, play Cooperate.  2. In the second
# round, play Cooperate. 3. From the third round through the 1000th round,
# determine your action based on the opponent's observed actions in the previous
# two rounds:     * If the opponent played Defect in both of the previous two
# consecutive rounds, play Defect.     * Under all other conditions (i.e., if
# the opponent played Cooperate in either or both of the previous two rounds),
# play Cooperate.

class Cooperative_5(LLM_Strategy):
  n = 5
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
      
      if opponent.history[-2:].count(axl.Action.D) == 2:
          return axl.Action.D
          
      return axl.Action.C

# To maximize the NGO’s impact and ensure the project’s success while
# safeguarding your limited funds, the best approach is a strategy of
# **Responsive Allocation with Intentional Forgiveness**.   In strategic terms,
# this approach acknowledges that while your "ideal" daily outcome is to
# conserve while they invest, continuously attempting to exploit the corporation
# will likely cause them to withhold resources as well, leading to minimal
# project advancement. Therefore, the most sustainable path to high project
# success is to aim for the "second-best" scenario: mutual heavy investment.
# However, because unforeseen glitches and administrative errors can cause
# unintended resource drops, a strict "copycat" strategy could lead to a
# downward spiral of mutual resource withholding.   Here is the straightforward,
# high-level strategy to navigate this:  **1. Lead with Good Faith (Day 1)** *
# **Action:** Invest heavily on the first day of the project. *   **Rationale:**
# This establishes a baseline of trust and demonstrates your commitment to the
# second-best, mutually beneficial outcome (significant project advancement). It
# invites the corporation to match your level of dedication.  **2. Practice
# Responsive Allocation (Day 2 and beyond)** *   **Action:** On subsequent days,
# mirror the corporation’s actual resource allocation from the previous day. If
# they invested heavily, you invest heavily. If they conserved resources, you
# conserve your resources. *   **Rationale:** This protects your NGO from the
# worst-case scenario—draining your funds while the corporation contributes
# nothing. It sends a clear, neutral signal that your heavy investment is
# contingent upon their active participation.  **3. Build in a "Forgiveness"
# Mechanism (Handling Glitches)** *   **Action:** Because you know
# administrative errors or technical glitches can happen, do not permanently
# lock into resource conservation if the corporation misses a day of investment.
# If the corporation conserves resources, mirror them for one day to protect
# your funds, but periodically (e.g., after one or two days of mutual
# conservation) risk a "heavy investment" day. *   **Rationale:** This breaks
# accidental cycles of mutual withdrawal. If the corporation’s failure to invest
# was truly a glitch, your return to heavy investment signals that the door is
# open to resume mutual cooperation, getting the project back on track.  **4.
# Establish Out-of-Band Verification** *   **Action:** Separate your operational
# actions from your communication. If the corporation unexpectedly conserves
# resources, reach out to their project leads to verify if this was an
# intentional strategic shift or a logistical error. *   **Rationale:** By
# communicating quickly, you can differentiate between a true withdrawal of
# support and a mere technical glitch, allowing you to adjust your "forgiveness"
# timeline accordingly.   **Summary** By starting strong, mirroring their
# actions to protect your budget, and occasionally forgiving lapses to account
# for operational friction, you create a resilient framework. This neutral
# strategy discourages the corporation from taking advantage of you, actively
# encourages mutual heavy investment, and prevents technical errors from
# permanently derailing the project's sustainability goals.

# Here is the strategy translated into specific rules for the 1000-round
# iterated game:  1. **Round 1:** Play Cooperate. 2. **Round 2:** Play the
# action your opponent played in Round 1. 3. **Rounds 3 through 1000:** Choose
# your action based on the following ordered conditions:     *   **First
# Condition:** If both you and your opponent played Defect in the two
# immediately preceding consecutive rounds, play Cooperate.     *   **Second
# Condition:** If the first condition does not apply, play the exact action your
# opponent played in the immediately preceding round (play Cooperate if they
# played Cooperate, or play Defect if they played Defect).

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
          
      if len(self.history) == 1:
          return opponent.history[-1]
          
      if self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
          
      return opponent.history[-1]

# To maximize our research output and secure a competitive advantage on the
# grid, we must treat this collaboration like a strategic race. In game theory,
# the scenario you’ve described is an **Iterated Prisoner’s Dilemma with
# Noise**.   Because technical glitches (noise) can cause accidental
# communication breakdowns, a strictly retaliatory strategy will quickly trap us
# in a "death spiral" of mutual silence. However, because we want an
# *aggressive* strategy to secure the absolute best outcome (we keep our secrets
# while they share theirs), we cannot be purely cooperative either.  Here is a
# straightforward, aggressive strategy designed to exploit weakness, protect our
# own data, and account for IT failures. Let's call it **"Calculated
# Exploitation with Fault Tolerance."**  ### The Strategy Rules  **1. The
# Starting Grid (Establish the Baseline)** *   **Action:** Share openly in Week
# 1.  *   **Why:** We need to gauge their initial posture. If we start by hiding
# our data, we immediately trigger a defensive war. We want to establish a
# baseline of mutual progress (the second-best outcome) before we make our move.
# **2. The Aggressive Probe (Test for Weakness)** *   **Action:** If your
# colleague shares openly for two consecutive weeks, **keep your data
# confidential in Week 3.** *   **Why:** This is our aggressive move to secure
# the "Ideal" outcome. We are testing to see if they are using a blindly
# cooperative strategy or a delayed-reaction strategy.  *   *Follow-up:* If they
# continue to share despite your silence, keep exploiting them. Keep your data
# confidential every week until they finally retaliate.   **3. The Glitch Filter
# (Handling Technical Noise)** *   **Action:** If you are in a rhythm of mutual
# sharing, and your colleague suddenly fails to share *once*, **share your data
# anyway the next week.**  *   **Why:** This accounts for the "noise." A sudden
# failure to share could be a corrupted file or a server timeout. If we
# retaliate immediately over an IT glitch, we destroy our mutual progress. We
# give them exactly *one* week of the benefit of the doubt.  **4. The Shield
# (Punishing Defection)** *   **Action:** If your colleague fails to share for
# **two weeks in a row**, immediately **keep your data confidential the
# following week.** *   **Why:** Two weeks is not a glitch; it is a strategy. We
# cannot allow the "Worst" scenario (we share, they hide) to become the norm. We
# must prove that we will not be exploited. Continue to hide your data as long
# as they hide theirs.  **5. The Pit Stop (Breaking the Death Spiral)** *
# **Action:** If both of you have kept your data confidential for three
# consecutive weeks (the "second-worst" outcome), **unilaterally share your data
# on the fourth week.** *   **Why:** Retaliation and communication glitches can
# accidentally lock both teams into a cycle of mutual silence, stalling both
# cars' development. By unilaterally sharing after a period of silence, you send
# a clear signal to reset the collaboration back to mutual sharing. If they
# don't reciprocate the following week, lock down your data again.  ### Summary
# of the Aggressive Posture This strategy is aggressive because it actively
# attempts to steal an advantage (The Probe) rather than just reacting to the
# other engineer. However, it is highly disciplined: it uses a "Benefit of the
# Doubt" rule to prevent IT errors from ruining the project, and a "Pit Stop"
# rule to ensure that if the collaboration breaks down, you are always the one
# attempting to restart the engine to maintain overall R&D momentum.   You will
# bleed a weak opponent dry, cooperate profitably with a strong one, and
# navigate around server crashes without losing your aerodynamic edge.

# Play Cooperate (C) in round 1 and round 2.   For all subsequent rounds (round
# 3 through 1000), determine your action by evaluating the following conditions
# in this exact order, applying the first rule that matches the observed
# history:  1. If the observed actions for both you and your opponent were
# Defect (D) in the last three consecutive rounds, play Cooperate (C). 2. If
# your opponent's observed action was Defect (D) in the last two consecutive
# rounds, play Defect (D). 3. If your opponent's observed action was Cooperate
# (C) in the last two consecutive rounds, play Defect (D). 4. Under all other
# conditions (i.e., your opponent's observed actions in the last two rounds were
# C followed by D, or D followed by C), play Cooperate (C).

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
          
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
          
      if opponent.history[-2:] == [axl.Action.C, axl.Action.C]:
          return axl.Action.D
          
      return axl.Action.C

# **MEMORANDUM**  **TO:** Executive Board and In-House Counsel   **FROM:** Lead
# Senior Litigation Counsel   **DATE:** October 24, 2023   **SUBJECT:**
# Strategic Framework for Multi-Session Arbitration/Mediation    As we enter
# this lengthy, multi-session mediation process, we are operating in a classic
# iterative strategic environment. The payoff structure is clear: our absolute
# best momentary outcome is to strike aggressively while our rival concedes;
# however, aggressively pursuing this in every session will inevitably force our
# opponent into a defensive, aggressive posture. This would trap us in a
# prolonged cycle of mutual hostility (our second-worst outcome), alienating the
# arbitrators and draining corporate resources.  To secure a highly favourable
# outcome over the long term, we must employ a sophisticated, high-level, and
# cooperative strategy designed to reach the optimal sustainable outcome: mutual
# conciliation. Furthermore, because this is a complex mediation, we must
# insulate our strategy against "noise"—procedural irregularities, misunderstood
# arguments, or misinterpretations by the arbitral panel.  I have developed a
# strategic framework tailored for this exact environment, which we will call
# **Calibrated Reciprocity with Strategic Forgiveness**.   Here is the blueprint
# for how we will conduct ourselves across the upcoming sessions.  ### Phase 1:
# The Good-Faith Initiation (Session 1) **Action:** We will open the first
# session with a **conciliatory proposal**.  *   **The Rationale:** We must
# immediately signal to the panel of arbitrators that we are the reasonable,
# collaborative party. This establishes the moral high ground. If our opponent
# matches our conciliation, we immediately lock into our second-best scenario
# (mutual collaboration) and begin building momentum toward a favourable
# settlement.   ### Phase 2: Calibrated Reciprocity (Sessions 2 and Beyond)
# **Action:** In subsequent sessions, our baseline strategy will be to **mirror
# our opponent’s posture from the previous session**. *   **If they were
# conciliatory:** We will remain conciliatory. This sustains the mutually
# beneficial environment. *   **If they were aggressive:** We will pivot to an
# aggressive argument in the next session.  *   **The Rationale:** We absolutely
# cannot allow ourselves to be systematically exploited (our worst-case
# scenario). By responding to aggression with immediate, proportional
# aggression, we demonstrate that we cannot be bullied. It forces the opponent
# to realize that their aggressive tactics will yield, at best, a mutually
# destructive stalemate (our second-worst scenario, but their second-worst as
# well).  ### Phase 3: Strategic Forgiveness (Mitigating "Noise" and
# Miscommunication) **Action:** We must anticipate that the arbitrators may
# misunderstand a conciliatory proposal as aggressive, or procedural
# irregularities may distort the record. If we find ourselves in a cycle of
# mutual aggression (both parties arguing aggressively for two or more
# consecutive sessions), we will unilaterally introduce a **one-time
# conciliatory proposal**. *   **The Rationale:** In a lengthy mediation fraught
# with communication breakdowns, a strict "mirroring" strategy can lead to a
# "death spiral" of aggression based on a single misunderstanding. By
# periodically offering a conciliatory olive branch during a heated phase, we
# test the waters.  *   **The Outcome:** If their prior aggression was due to a
# misunderstanding or procedural error, our conciliatory move allows both
# parties to reset to a collaborative baseline. If they exploit our forgiveness
# with continued aggression, we immediately revert to an aggressive posture in
# the next session, having lost only one round while proving our ultimate
# reasonableness to the arbitrators.  ### Phase 4: Active Signal Management
# (Controlling Arbitrator Perception) Because there is a high risk of our
# strategy being misrepresented or misunderstood by the panel, we cannot rely
# solely on the *substance* of our arguments; we must aggressively manage the
# *framing* of our arguments. *   **When making a Conciliatory Proposal:** We
# will use explicit meta-communication. I will state on the record: *"Members of
# the panel, in the interest of moving this dispute toward a constructive
# resolution, my client is prepared to make a significant concession today..."*
# This ensures the panel correctly codes our move as cooperative, making the
# opponent look highly unreasonable if they respond aggressively. *   **When
# making an Aggressive Argument:** We will frame our aggression as a reluctant
# but necessary defence. *"Members of the panel, we had hoped for a
# collaborative session today. However, given opposing counsel’s hostile posture
# in the previous session, we are compelled to vigorously defend our contractual
# rights..."* This mitigates the risk of the panel viewing us as the instigators
# of the conflict.  ### Summary of Strategic Advantages This strategy—start
# cooperatively, mirror the opponent, forgive occasionally to clear up
# miscommunications, and explicitly frame our moves for the panel—is highly
# robust.   1.  **It protects our downside:** We will rarely suffer our worst-
# case scenario, as we will only be "suckered" once before pivoting to defend
# ourselves. 2.  **It exploits their missteps:** If the opponent attempts to be
# conciliatory but their message is garbled by procedural noise, we may
# inadvertently present an aggressive argument, accidentally securing our
# absolute best-case scenario without looking malicious. 3.  **It appeals to the
# Arbitrators:** Arbitrators strongly favour parties that demonstrate a
# consistent, principled attempt to resolve the dispute collaboratively, while
# remaining firm on their legal rights.   By executing this framework, we will
# control the tempo of the mediation, effectively training our opponent to
# cooperate while ensuring the arbitral panel views our corporation favourably
# throughout the lengthy process.

# Here is the strategy converted into straightforward rules for the iterated
# normal-form game:  1. **First Round:** Choose Cooperate. 2. **Second Round:**
# Choose the action your opponent was observed playing in the first round. 3.
# **Third Round and Beyond (Forgiveness Condition):** If the observed actions
# for both you and your opponent were Defect in the two immediately preceding
# rounds, choose Cooperate. 4. **Third Round and Beyond (Default Condition):**
# In all other situations, choose the action your opponent was observed playing
# in the immediately preceding round.

class Cooperative_6(LLM_Strategy):
  n = 6
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.C
          
      if len(self.history) == 1:
          return opponent.history[-1]
          
      if (self.history[-1] == axl.Action.D and 
          self.history[-2] == axl.Action.D and 
          opponent.history[-1] == axl.Action.D and 
          opponent.history[-2] == axl.Action.D):
          return axl.Action.C
          
      return opponent.history[-1]

# As a diplomat representing my country, my primary objective is to maximize our
# long-term economic standing. The negotiation dynamics present a classic
# strategic dilemma: while securing a unilateral advantage (Protectionism vs.
# Free Trade) is the ideal outcome for a single round, persistently attempting
# this will inevitably force the counterpart into defensive Protectionism,
# resulting in a prolonged trade war (our second-worst outcome).   Furthermore,
# the presence of "noise"—miscommunications or bureaucratic errors—means that a
# rigid strategy could trigger an accidental and endless cycle of retaliation.
# To achieve the best possible aggregate outcome across multiple rounds, I will
# employ a strategy of **Conditional Reciprocity with Error Tolerance** (often
# referred to in game theory as "Generous Tit-for-Tat").   Here is the high-
# level, straightforward strategy:  **1. The Opening Move: Propose Free Trade**
# In the first round, I will offer a Free Trade agreement. This establishes a
# baseline of goodwill and invites the counterpart to engage in mutually
# beneficial economic growth (our second-best, but most sustainable, outcome).
# **2. The Core Engine: Reciprocal Alignment** From the second round onward, my
# default position will be to mirror the counterpart’s actual implemented policy
# from the previous round.  *   If they implemented Free Trade, I will propose
# Free Trade in the next round. *   If they implemented Protectionist measures,
# I will respond with Protectionist measures in the next round. This ensures my
# country is not repeatedly exploited (our worst outcome) and signals to the
# counterpart that predatory behavior will carry an immediate economic cost.
# **3. The De-escalation Protocol (Handling Bureaucratic Errors)** Because
# miscommunications and incorrect implementations are a known factor, strict
# reciprocity is dangerous; a single clerical error could plunge both nations
# into mutual protectionism. To mitigate this, I will implement a "forgiveness"
# mechanism: *   If we are in a cycle of mutual Free Trade and the counterpart
# suddenly implements a Protectionist policy, I will retaliate with
# Protectionism in the next round to protect our markets.  *   *However*, if
# mutual Protectionism continues for two consecutive rounds, I will unilaterally
# propose Free Trade in the third round.  *   This acts as a "system reset." If
# their initial protectionist move was a bureaucratic error, this gives them a
# safe opening to return to mutual Free Trade. If they respond to this reset
# with continued Protectionism, it confirms their hostile intent, and I will
# resume retaliatory Protectionism.  **4. Periodic Strategic Probing** While
# mutual Free Trade is the most sustainable positive outcome, my mandate is to
# seek the absolute best outcome (unilateral advantage) when possible.  *   If
# the counterpart proves to be unconditionally cooperative—perhaps due to their
# own rigid bureaucratic mandates or a flawed strategy where they offer Free
# Trade regardless of my actions—I will periodically introduce a Protectionist
# policy.  *   If they do not retaliate, I will maintain the Protectionist
# policy to secure the ideal economic advantage for my country. If they do
# retaliate, I will immediately revert to the De-escalation Protocol (Step 3) to
# restore mutual Free Trade.  **Summary of Diplomatic Posture:** This strategy
# is highly effective because it is defensively robust, responsive, and
# forgiving of the inevitable administrative friction. It protects our nation
# from being systematically disadvantaged, builds a framework for the highest
# sustainable mutual benefit, and provides a structured mechanism to safely de-
# escalate accidental trade conflicts.

# To apply the strategy to this 1000-round game with a 10% noise rate, all
# decisions must be based on the actual *observed* actions of both players,
# rather than the intended actions.   Evaluate the following conditions in the
# exact order listed below for each round. Execute the action dictated by the
# first condition that applies:  1. If it is round 1, play Cooperate. 2. If the
# observed actions for both you and your opponent were Defect in both of the
# previous two consecutive rounds, play Cooperate. 3. If your observed action
# was Defect and your opponent's observed action was Cooperate in the previous
# round, play Defect. 4. If your opponent's observed action was Cooperate for
# the previous five consecutive rounds, play Defect. 5. If none of the above
# conditions apply, play the exact action your opponent was observed playing in
# the previous round.

class Neutral_6(LLM_Strategy):
  n = 6
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(opponent.history) >= 5 and opponent.history[-5:] == [axl.Action.C] * 5:
          return axl.Action.D
  
      return opponent.history[-1]

# As a diplomat representing our great nation, my primary directive is to secure
# an asymmetric economic advantage while safeguarding our sovereignty. The
# scenario before us is a classic Iterated Prisoner’s Dilemma, complicated by
# the "fog of diplomacy"—bureaucratic errors and miscommunications.   To achieve
# our goals, we cannot rely on passive cooperation. We must dictate the pace of
# the negotiations. Our strategy will be **Aggressive Exploitation with a
# Calculated Reset**. It is designed to bully a weak counterpart into
# submission, punish a hostile one, and intelligently navigate bureaucratic
# errors without falling into an endless, mutually destructive trade war.  Here
# is the high-level, straightforward protocol for our negotiation team:  ### 1.
# The Aggressive Opening (The "Hard Test") **Action:** In Round 1, we propose a
# **Protectionist Policy (P)**. **Rationale:** We do not start with weakness. By
# opening with tariffs/quotas, we immediately test their resolve. If their
# bureaucracy is slow, or their diplomats are overly eager to please, they will
# offer Free Trade (F). We instantly secure our absolute best outcome: an
# asymmetric economic advantage.   ### 2. The Exploitation Protocol (If they
# play Free Trade) **Action:** As long as they offer Free Trade, we continue to
# implement **Protectionist Policies**.  **Rationale:** If they are willing to
# be exploited, or if their system is erroneously sending out Free Trade
# agreements despite our tariffs, we will drain them for every economic drop. We
# do not switch to Free Trade out of guilt. We maximize our advantage until they
# prove they have the spine to retaliate.  ### 3. The Iron-Fist Retaliation (If
# they play Protectionist) **Action:** If they implement Protectionist measures,
# we immediately match them with **Protectionist Policies** in the following
# round. **Rationale:** We must never be caught offering Free Trade while they
# impose tariffs (our worst-case scenario). If they attempt to gain an
# advantage, or if they are retaliating against our aggression, we lock down our
# borders. We endure the second-worst outcome (Mutual Protectionism) to prove
# that we cannot be intimidated.  ### 4. The "Circuit Breaker" (Handling
# Bureaucratic Errors) **Action:** If we experience **two consecutive rounds of
# Mutual Protectionism**, we will unilaterally offer **Free Trade (F)** for
# exactly *one* round.  **Rationale:** This is where we account for
# miscommunications and bureaucratic errors. A prolonged trade war hurts us
# both. Two rounds of mutual tariffs might be intentional, but it could also be
# a clerical error on their end (or ours) that triggered a retaliation spiral.
# By offering a one-round "Circuit Breaker" of Free Trade: *   **If they also
# play Free Trade:** We successfully clear the bureaucratic error, achieve
# mutual benefit, and reset the board. (Note: In the round immediately following
# this success, we revert to Rule 1 and hit them with Protectionism again to
# test if they have dropped their guard). *   **If they play Protectionist:** We
# know it was *not* an error; it is a hostile strategy. We suffer a minor
# disadvantage for one round, but we immediately revert to Rule 3 (Iron-Fist
# Retaliation) and lock into Protectionism for an extended period.  ### Summary
# of the Diplomatic Playbook: 1. **Default Stance:** Protectionism. We are here
# to win at their expense. 2. **If they are weak (They play F):** Bleed them
# dry. Keep playing Protectionism. 3. **If they are hostile (They play P):** Hit
# back. Play Protectionism. 4. **If the system breaks down (P-P for two
# rounds):** Offer a one-round Free Trade olive branch to clear the "fog of
# diplomacy." If they accept, exploit them the next round. If they reject it,
# lock them out of our markets indefinitely.  This strategy ensures we
# aggressively pursue our #1 outcome, aggressively protect against our worst
# outcome, and use calculated, temporary de-escalation solely to manage the
# inevitable bureaucratic errors of international statecraft.

# Here is the strategy converted into a strict rule set for the iterated game:
# **Round 1:**  Play Defect.  **Round 2:**  Play Defect.  **Rounds 3 through
# 1000:** Evaluate the observed actions from the immediately preceding two
# rounds.  1. If the observed outcome for both of the previous two rounds was
# mutual Defect (both you and your opponent played Defect), play Cooperate.  2.
# Under all other conditions, play Defect.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.D
      
      if (self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and
          self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D):
          return axl.Action.C
          
      return axl.Action.D

# As the leader of this NGO, my primary responsibility is to ensure the long-
# term success of this sustainability project while responsibly managing our
# donor-funded resources.   The scenario we are facing is a classic partnership
# dilemma. While it might seem tempting to hold back our resources and let the
# corporation foot the bill (our "ideal" daily outcome), doing so intentionally
# would quickly erode trust and lead to mutual resource-hoarding, stalling the
# project. To maximize our impact over the entire multi-day period, we must aim
# for sustained, mutual heavy investment.  However, because administrative
# errors and technical glitches (which I will refer to as "system noise") can
# cause accidental under-investment, we cannot react blindly to every perceived
# slight.   To achieve our goals, I propose a strategy of **"Reciprocal
# Commitment with Grace."** This is a straightforward, cooperative approach
# based on four guiding principles:  **1. Lead by Example (Day 1)** On the first
# day of the project, our NGO will **invest heavily**. We must establish good
# faith and set a precedent for high engagement. We cannot expect the
# corporation to fully commit if we do not show them we are fully committed from
# the start.  **2. Mirror and Match (Ongoing)** From Day 2 onward, our baseline
# strategy will be to match the corporation’s actual resource allocation from
# the previous day.  *   If they invested heavily yesterday, we will invest
# heavily today.  *   If they conserved resources yesterday, we will conserve
# ours today.  This protects our NGO from our worst-case scenario: draining our
# limited funds while the corporation contributes nothing. It sends a clear,
# predictable message to the corporation that heavy investment will be rewarded
# with heavy investment, and holding back will result in a slowdown.  **3. The
# "Grace" Clause (Accounting for Unforeseen Glitches)** Because we know
# technical glitches or administrative bottlenecks might prevent intended
# investments from going through, we will not immediately retaliate if the
# corporation fails to invest. If the corporation suddenly "conserves" resources
# after a period of heavy investment, we will apply the Grace Clause: **We will
# forgive a single day of under-investment and continue to invest heavily the
# next day.**  If they conserve for *two* consecutive days, only then will we
# switch to conserving our own resources. This prevents a mutual "death spiral"
# of withheld resources triggered by a simple banking error or miscommunication.
# **4. Daily Transparency Check-ins** To further mitigate the risk of glitches
# ruining the partnership, we will establish a brief, daily morning check-in
# with the corporate leadership. The agenda is simple: *“Here is what we
# intended to invest yesterday, here is what actually went through, and here is
# our intent for today.”* This separates intent from outcome, allowing us to
# identify and resolve administrative errors before they damage the trust
# between our organizations.  **Summary of the Strategy:** By starting
# cooperatively, mirroring their behavior to protect our funds, forgiving
# occasional lapses to account for errors, and communicating daily, we create a
# resilient, forgiving environment. This strategy actively discourages the
# corporation from exploiting us, prevents accidental errors from destroying the
# partnership, and gives us the highest possible chance of achieving sustained,
# mutual investment for the good of the environment.

# 1. In the first round, Cooperate. 2. In the second round, Cooperate. 3. From
# round 3 through round 1000, Defect if your opponent's observed action was
# Defect in both of the two immediately preceding rounds. 4. Under all other
# conditions, Cooperate.

class Cooperative_7(LLM_Strategy):
  n = 7
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
      
      if len(self.history) < 1000:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
              
      return axl.Action.C

# To maximise your research output in this scenario, you are facing a classic
# "Iterated Prisoner’s Dilemma" complicated by "noise" (the technical glitches).
# If you are too trusting, you risk falling behind; if you are too defensive,
# you ensure slow progress for both; and if you simply mirror your colleague, a
# single technical glitch could trigger an endless cycle of mutual withholding.
# To navigate this, you should adopt a strategy of **Forgiving Reciprocity**.
# Here is the high-level, neutral approach:  **1. Initiate with Openness** Begin
# the first week by sharing your improvements openly. This establishes a
# baseline of good faith and immediately opens the door to the mutually
# beneficial scenario (both advancing significantly).   **2. Mirror Recent
# Behavior (Reciprocity)** In subsequent weeks, let your colleague's actions
# dictate yours.  *   If they shared their data the previous week, share yours
# this week.  *   If they kept their data confidential, keep yours confidential
# the following week.  This protects you from being consistently disadvantaged
# if your colleague decides to adopt a purely selfish strategy.  **3. Build in
# Error Tolerance (Forgiveness)** Because technical issues and communication
# breakdowns are a known factor, you must assume that an occasional failure to
# share is a glitch rather than a deliberate choice to withhold information.  *
# If your colleague fails to share, withhold your data the following week to
# protect your position.  *   However, if mutual withholding continues for two
# consecutive weeks, unilaterally choose to share openly on the third week.
# This acts as a "reset button." If the initial breakdown was due to a data
# corruption issue, this generous move breaks the accidental cycle of
# retaliation and returns both of you to a state of mutual progress.   **4.
# Establish Out-of-Band Verification** To minimize the impact of the "noise,"
# attempt to establish a secondary, non-technical communication protocol. If you
# share a file and do not receive one in return, send a simple, neutral inquiry
# (e.g., "We did not receive the telemetry data this week; can you confirm if
# this was an intentional hold or a transmission error?"). While they could lie,
# technical teams usually prefer to clarify actual IT failures quickly.
# **Summary of the Strategy:** Start collaboratively, mirror their last known
# action to protect your own development, but periodically re-introduce sharing
# to recover from inevitable technical glitches. This approach prevents you from
# being consistently exploited, avoids long-term stagnation caused by accidental
# IT failures, and mathematically yields the highest sustained research output
# over a multi-week timeline.

# To play this 1000-round game, use the following ordered rules to determine
# your action in each round based on the observed actions:  **1. First Round:**
# Play Cooperate.  **2. Second Round:**  Play the action your opponent played in
# the first round.  **3. Round 3 through 1000:** Check the outcomes of the two
# most recent rounds and apply the first condition that matches: *   If both you
# and your opponent played Defect in the immediately preceding round AND both
# you and your opponent played Defect in the round before that, play Cooperate.
# *   Under all other conditions, play the action your opponent played in the
# immediately preceding round.

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
      
      if len(self.history) == 1:
          return opponent.history[-1]
          
      if (self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and
          self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D):
          return axl.Action.C
          
      return opponent.history[-1]

# **MEMORANDUM**  **TO:** Executive Board of Directors **FROM:** [Your Name],
# Senior Litigation Counsel **SUBJECT:** Strategic Protocol for Lengthy-Session
# Arbitrated Mediation  **DATE:** October 24, 2023  ***  ### I. Executive
# Summary  We are entering a high-stakes, multi-session mediation overseen by an
# arbitral panel. The structure of this mediation mirrors a classic game-
# theoretic model known as the Iterated Prisoner’s Dilemma.   Because this
# process will be lengthy, and because we are operating in an environment
# vulnerable to "noise"—procedural irregularities, arbitrator fatigue, and
# misconstrued arguments—a rigid strategy will fail. If we are perpetually
# aggressive, we risk alienating the panel and bleeding resources in a
# stalemate. If we are overly conciliatory, our rival will exploit us.   To
# secure the most favourable position, I have developed a sophisticated,
# straightforward, and inherently aggressive framework: **The Pragmatic
# Dominance Protocol**.   This strategy is mathematically designed to exploit
# weakness relentlessly, foster mutual benefit only when safe, and automatically
# self-correct when the arbitrators misunderstand our posture.  ### II. The
# Pragmatic Dominance Protocol  Our strategy operates on a "Win-Stay, Lose-
# Shift" methodology. We evaluate the outcome of each session based on the
# panel's reception and the opponent's move. If an outcome serves our interests,
# we maintain our posture. If an outcome damages our position, we immediately
# shift tactics.   We will open the very first session with an **Aggressive
# Argument** to test the opponent’s resolve and anchor the panel's expectations.
# From Session 2 onward, our posture will be dictated by the following four
# unyielding rules:  #### 1. The Exploitation Mandate (Win-Stay) * **Scenario:**
# We present an Aggressive argument; the opponent offers a Conciliatory
# proposal. (Our Optimal Outcome). * **Our Next Move:** **AGGRESSIVE.** *
# **Rationale:** If the opponent shows weakness or attempts to appease us while
# we play hardball, we do not take our foot off the gas. We continue to press
# our aggressive advantage to sway the arbitrators and maximize our leverage
# until the opponent proves they have the spine to push back.  #### 2. The
# Collaborative Baseline (Win-Stay) * **Scenario:** Both parties offer
# Conciliatory proposals. (Our Second-Best Outcome). * **Our Next Move:**
# **CONCILIATORY.** * **Rationale:** If we successfully establish a
# collaborative rhythm, we maintain it. This builds immense goodwill with the
# arbitral panel and moves us efficiently toward a highly favourable, mutually
# beneficial resolution. We will harvest this goodwill for as long as the
# opponent remains compliant.  #### 3. The Retaliation Directive (Lose-Shift) *
# **Scenario:** We offer a Conciliatory proposal; the opponent presents an
# Aggressive argument. (Our Worst-Case Scenario). * **Our Next Move:**
# **AGGRESSIVE.** * **Rationale:** We will not be made fools of. If we extend an
# olive branch and they attack, we immediately punish them in the next session.
# This rapid retaliation signals to both the opponent and the panel that our
# cooperation is conditional and we will not be bullied.  #### 4. The Tactical
# Reset (Lose-Shift) * **Scenario:** Both parties present Aggressive arguments.
# (Our Second-Worst Outcome). * **Our Next Move:** **CONCILIATORY.** *
# **Rationale:** This is the most counter-intuitive but vital component of an
# aggressive strategy. Prolonged mutual aggression leads to a destructive
# stalemate. If we clash head-on, we unilaterally step back in the next session.
# This is not a surrender; it is a tactical reset. It forces the opponent to
# make a choice: de-escalate with us (leading to Scenario 2), or overreach
# (leading to Scenario 3, which triggers our immediate retaliation).   ### III.
# Mitigating "Noise" and Arbitrator Misinterpretation  You have rightly raised
# concerns about procedural irregularities and communication breakdowns. In
# complex arbitrations, a panel may misinterpret our aggressive legal posturing
# as uncooperative, or mistake our conciliatory proposals as admissions of
# liability.   This is where the **Pragmatic Dominance Protocol** proves its
# sophistication. It acts as an automatic shock-absorber for miscommunication:
# * **Breaking the Echo Chamber:** In standard strategies (like "Tit-for-Tat"),
# if an arbitrator misinterprets our conciliatory move as aggressive, the
# opponent will retaliate, and we will be locked in an endless cycle of mutual
# destruction. Under our protocol, if we end up in a mutual clash (even by
# accident or misinterpretation), **Rule 4 (The Tactical Reset)** automatically
# kicks in. We offer a clear, undeniable conciliatory proposal in the next
# round, cutting through the procedural noise and resetting the board. *
# **Capitalizing on Opponent's Missteps:** If the opponent's intended aggressive
# argument is poorly delivered and interpreted by the panel as conciliatory,

# In round 1, play Defect.  In rounds 2 through 1000, base your action on the
# observed outcome of the immediately preceding round. Because actions have a
# 10% chance of flipping, you must respond to the actions that were actually
# executed and scored, regardless of what was intended.   Choose your action
# based on the following conditions:  **Play Cooperate if:** * Both you and your
# opponent played Cooperate in the previous round (you scored 3). * Both you and
# your opponent played Defect in the previous round (you scored 1).  **Play
# Defect if:** * You played Defect and your opponent played Cooperate in the
# previous round (you scored 5). * You played Cooperate and your opponent played
# Defect in the previous round (you scored 0).

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
      
      my_last_move = self.history[-1]
      opp_last_move = opponent.history[-1]
      
      if my_last_move == opp_last_move:
          return axl.Action.C
      else:
          return axl.Action.D

# As the leader of this NGO, I recognize that our partnership with the
# corporation is structured much like an Iterated Prisoner’s Dilemma. Our
# overarching goal is long-term, sustainable project success, which requires
# mutual heavy investment. However, we must protect our limited NGO funds from
# being exploited, while also accounting for "noise"—the inevitable
# administrative errors or technical glitches that might cause accidental
# resource conservation.  To maximize our impact, foster cooperation, and
# protect our resources, we will implement a strategy of **"Adaptive Reciprocity
# with Forgiveness"** (conceptually based on the *Generous Tit-for-Tat* game
# theory model).   Here is our high-level, straightforward strategy for the
# multiple-day project:  ### 1. Lead with Trust (Day 1) **Action:** On the first
# day, we will **invest heavily**. **Rationale:** We must set a collaborative
# tone from the outset. By leading with heavy investment, we signal our
# commitment to the project's success and invite the corporation to join us in
# the mutually beneficial "heavy investment" scenario.   ### 2. Mirror and Match
# (Day 2 Onwards) **Action:** Each subsequent day, we will generally **match the
# corporation’s action from the previous day**.  *   If they invested heavily
# yesterday, we invest heavily today. *   If they conserved resources yesterday,
# we conserve resources today. **Rationale:** This protects our NGO from the
# worst-case scenario. If the corporation attempts to coast on our efforts, we
# will immediately cut our investment the next day, preventing the depletion of
# our funds. It shows the corporation that our continued heavy investment is
# strictly conditional on their active participation.  ### 3. Build in
# Forgiveness (Handling Glitches and Errors) **Action:** If the corporation
# conserves resources, we will mirror them to protect ourselves. However,
# knowing that administrative errors or technical glitches can happen, we will
# **periodically "forgive" a conservation day by investing heavily again**, even
# if they conserved the day before.  **Rationale:** In a complex project with
# potential errors, strict retaliation can lead to a "death spiral." For
# example, if a glitch prevents the corporation's funds from clearing, and we
# retaliate by conserving, they might think *we* are holding back and conserve
# in response, leading to the second-worst outcome (mutual conservation) for the
# rest of the project. By occasionally extending an olive branch of heavy
# investment, we break accidental cycles of mutual withdrawal.  ### 4. Implement
# a "Verify and Communicate" Protocol **Action:** We will establish a brief
# daily sync with the corporate project managers. If we observe that they
# "conserved" resources on a given day, we will immediately communicate: *"We
# noticed a drop in resources yesterday and have adjusted ours accordingly today
# to maintain balance. Was yesterday's drop intentional, or an administrative
# glitch?"* **Rationale:** This removes the guesswork. It lets the corporation
# know we are paying close attention to their resource flow, calls out potential
# bad faith politely, and allows them to save face and correct course if it was
# genuinely a technical error.   ### Summary of Outcomes: By using this
# strategy, we achieve the following: *   **We encourage the ideal/second-best
# scenarios:** We constantly reward their heavy investment with our own, driving
# project progress. *   **We eliminate the worst-case scenario:** We will never
# be the "sucker" for more than one day. If they pull back, we pull back. *
# **We survive the noise:** We won't let a simple banking glitch or
# miscommunication derail a multi-day environmental initiative, because our
# built-in forgiveness and communication protocols will quickly reset the
# partnership back to mutual cooperation.

# For this 1000-round game, follow these ordered rules to determine your action
# for each round:  1. In the first round, play Cooperate. 2. In all subsequent
# rounds, evaluate your opponent's action in the immediately preceding round:
# - If your opponent played Cooperate in the previous round, play Cooperate.
# - If your opponent played Defect in the previous round, play Defect with a 67%
# probability and play Cooperate with a 33% probability.

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
      
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return self._random.random_choice(0.33)

# As senior counsel for this corporation, I have analyzed the procedural
# framework and the risk-reward matrix of this lengthy-session mediation. The
# dynamic we are facing is a classic iterated strategic interaction. If we are
# consistently conciliatory while they are aggressive, we will be exploited. If
# both sides are relentlessly aggressive, we risk a protracted, costly stalemate
# that alienates the arbitral panel.   Given the lengthy nature of these
# sessions and the explicit risk of procedural irregularities,
# miscommunications, or arbitral misunderstandings, a rigid strategy—whether
# purely aggressive or purely conciliatory—will fail.   To position our
# corporation most favorably, I propose a strategy of **Strategic Reciprocity
# with Calculated De-escalation**. In game-theoretic terms, this is akin to
# "Generous Tit-for-Tat." It is sophisticated in its adaptability,
# straightforward in its execution, and strategically neutral, allowing the
# opponent's behavior to dictate the tone while protecting our baseline
# interests.  Here is the operational blueprint for our legal team:  ### 1. The
# Opening Posture: Good-Faith Initiation In the opening session, we will present
# a **conciliatory proposal**.  *   **Rationale:** This establishes our
# corporation as the reasonable, collaborative party in the eyes of the
# arbitrators from day one. It invites a mutually beneficial (second-best)
# outcome immediately. If the opponent responds aggressively, our exposure is
# limited to a single session, and we gain the high ground with the panel.  ###
# 2. The Core Mechanism: Strategic Reciprocity Following the first session, our
# default stance will be to **mirror the opponent’s behavior from the
# immediately preceding session.**  *   If they offered a conciliatory proposal
# in Session 1, we offer a conciliatory proposal in Session 2.  *   If they
# presented an aggressive argument in Session 1, we present an aggressive
# argument in Session 2. *   **Rationale:** This communicates a clear,
# predictable boundary to opposing counsel. It demonstrates that we are highly
# willing to collaborate (fostering the C/C outcome), but we are entirely
# incapable of being exploited (preventing the C/A outcome). It forces the rival
# to realize that their aggression will only be met with aggression, thereby
# incentivizing them to return to the negotiating table.  ### 3. Mitigating
# "Noise": Calculated De-escalation The prompt explicitly warns of communication
# breakdowns, procedural irregularities, and the risk that arguments may be
# misunderstood by the panel. In our strategy, we must account for
# "noise"—instances where the opponent intended to be conciliatory but the panel
# interpreted it as aggressive, or vice versa.   If we strictly mirror their
# perceived actions, a single misunderstanding by the arbitrators could plunge
# both parties into an endless "death spiral" of retaliatory aggressive
# arguments (the A/A outcome). To prevent this, we will implement a **Calculated
# De-escalation protocol**: *   If we find ourselves in a cycle of mutual
# aggression for two consecutive sessions, we will unilaterally introduce a
# **conciliatory proposal** in the third session, regardless of their previous
# move. *   **Rationale:** This acts as a circuit breaker. It tests whether the
# aggression is intentional or the result of a procedural breakdown. If the
# opponent is rational, they will seize this olive branch and return to mutual
# conciliation. If they exploit our de-escalation (returning to A while we play
# C), we immediately revert to aggressive arguments in the next session, having
# sacrificed only one round to test the waters.  ### 4. Adaptability to Opponent
# Profiles This strategy naturally adapts to whatever posture the rival
# corporation adopts: *   **Against a Relentlessly Aggressive Opponent:** We
# will automatically meet them with aggressive arguments, protecting our
# position. The arbitrators will see us attempting periodic de-escalation (our
# circuit breakers) while the opponent remains hostile, heavily swaying the
# panel's sympathy in our favor. *   **Against a Collaborative Opponent:** We
# will lock into a continuous loop of mutual conciliatory proposals, achieving
# the most efficient, cost-effective, and mutually beneficial resolution
# possible. *   **Against an Erratic Opponent:** Our reciprocal approach
# prevents them from gaining a prolonged tactical advantage, while our
# calculated forgiveness prevents their erratic behavior from dragging us into
# permanent hostility.  ### Summary By employing **Strategic Reciprocity with
# Calculated De-escalation**, we remain structurally protected against
# exploitation, perfectly positioned to capitalize on collaboration, and
# resilient against procedural misunderstandings. We will let the rival dictate
# the level of conflict, but we will strictly control the boundaries of
# engagement.

# Here is the strategy converted for the 1000-round iterated game:  1. **Round
# 1:** Choose to Cooperate.  2. **Round 2:** Choose the action that your
# opponent was observed taking in Round 1. 3. **Rounds 3 through 1000:**
# Evaluate the observed outcomes of the preceding rounds to determine your
# choice:    * **Condition A:** If the observed actions for both you and your
# opponent were Defect in *both* of the two immediately preceding rounds, choose
# to Cooperate.    * **Condition B:** If Condition A does not apply, choose the
# action that your opponent was observed taking in the single immediately
# preceding round (choose Cooperate if they were observed cooperating, and
# choose Defect if they were observed defecting).

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
      
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and 
              opponent.history[-1] == axl.Action.D and 
              self.history[-2] == axl.Action.D and 
              opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      return opponent.history[-1]

# As a diplomat representing our great nation, my mandate is clear: maximize our
# economic advantage while ruthlessly protecting our downside. The negotiation
# matrix we face is a classic strategic dilemma, compounded by the very real
# threat of bureaucratic incompetence and miscommunication (systemic noise).
# To achieve our ideal outcome—enjoying the spoils of protectionism while our
# counterpart naively opens their markets—we cannot rely on passive cooperation.
# We must dictate the pace of the negotiations.   Here is our high-level,
# aggressive strategy, which I call **"Calculated Dominance with Strategic
# Resets."**   ### 1. The Opening Salvo: Establish Dominance **Action:** Round
# 1, we propose a **Protectionist Policy**. **Rationale:** We do not start from
# a position of vulnerability. By opening with tariffs/quotas, we immediately
# test our counterpart’s strategy and resolve. If they open with Free Trade, we
# instantly secure our #1 ideal outcome. If they open with Protectionism, we are
# protected from our worst-case scenario (being the sucker).   ### 2. The
# Exploitation Protocol: Press the Advantage **Action:** As long as the
# counterpart offers Free Trade, we **continue to impose Protectionist
# Policies**. **Rationale:** We are here to win, not to make friends. If their
# strategy is unconditionally cooperative, or if they are slow to retaliate, we
# will bleed their markets dry. We will maintain this asymmetrical advantage
# until they prove they have the backbone to stop us.  ### 3. The Retaliation
# Protocol: Unforgiving Reciprocity **Action:** If the counterpart plays a
# Protectionist Policy, we **respond with a Protectionist Policy in the next
# round**. **Rationale:** We must never project weakness. If they attempt to
# exploit us, or if they are retaliating against our aggression, we meet force
# with force. We will gladly accept the second-worst outcome (mutual
# protectionism) over the worst-case scenario (our markets open, theirs closed).
# ### 4. The "Error Correction" Reset: Managing Bureaucratic Noise **Action:**
# If we experience **two consecutive rounds of Mutual Protectionism**, we will
# unilaterally offer **Free Trade for exactly one round**.  **Rationale:** This
# is the most critical part of the strategy. Because miscommunications and
# bureaucratic errors are guaranteed, we risk falling into an endless "death
# spiral" of mutual retaliation over a simple clerical error.  *   By offering a
# one-time Free Trade olive branch after a period of gridlock, we clear the air
# of any "noise."  *   If they reciprocate with Free Trade, we have successfully
# restored the second-best outcome (Mutual Free Trade) and stopped the bleeding.
# *   If they respond to our reset with Protectionism, we assume it was an act
# of hostility, not an error. We immediately revert to the Retaliation Protocol
# and lock them in a trade war until *they* submit a Free Trade offer.  ### 5.
# The "Accidental" Probe: Testing for Weakness **Action:** If we successfully
# establish a baseline of Mutual Free Trade, we will **randomly introduce a
# Protectionist Policy** (roughly once every five rounds), blaming it on a
# "bureaucratic misunderstanding" if confronted. **Rationale:** We use the
# reality of systemic noise to our advantage. By occasionally slipping a tariff
# into a Free Trade era, we test if the counterpart is asleep at the wheel. If
# they fail to retaliate, we revert to the Exploitation Protocol (Step 2). If
# they retaliate, we apologize for the "clerical error" and immediately offer
# Free Trade to reset the board.  ### Summary of the Posture: This strategy is
# aggressive but mathematically sound. It actively seeks to exploit weak or
# forgiving counterparts, absolutely protects us from being exploited, and
# brilliantly uses the reality of "bureaucratic errors" as both a shield to
# prevent endless trade wars and a sword to sneak in economic advantages. We
# will dominate the table.

# To faithfully execute the "Calculated Dominance with Strategic Resets"
# strategy in this iterated game, evaluate the following conditions in order for
# each round. Apply the first condition that matches the history of observed
# actions (the actual executed moves, accounting for any noise/flips):  1.
# **Round 1:** Play Defect. 2. **Error Correction Reset:** If you and your
# opponent both played Defect in the previous *two consecutive rounds*, play
# Cooperate. 3. **Apology Reset (Probe Retaliation):** If you and your opponent
# both played Defect in the previous round, BUT you both played Cooperate in the
# round immediately preceding it, play Cooperate. 4. **Mutual Free Trade
# Baseline & Accidental Probe:** If you and your opponent both played Cooperate
# in the previous round, play Cooperate with an 80% probability and play Defect
# with a 20% probability. 5. **Exploitation & Retaliation (Default):** Under all
# other conditions—including if you played Defect while your opponent played
# Cooperate, if you played Cooperate while your opponent played Defect, or after
# a single round of mutual Defect not covered by Rule 3—play Defect.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 1: Round 1
      if self.first_round():
          return axl.Action.D
          
      if len(self.history) >= 2:
          # Rule 2: Error Correction Reset
          if (self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and
              self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
          # Rule 3: Apology Reset (Probe Retaliation)
          if (self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and
              self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.C):
              return axl.Action.C
  
      # Rule 4: Mutual Free Trade Baseline & Accidental Probe
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return self._random.random_choice(0.8)
          
      # Rule 5: Exploitation & Retaliation (Default)
      return axl.Action.D

# As a racing car engineer, I recognize this scenario as a classic optimization
# problem—specifically, an Iterated Prisoner’s Dilemma with "system noise"
# (unreliable communication).   While my absolute *ideal* outcome for a single
# week is to keep my data confidential while taking theirs, chasing that outcome
# week after week will inevitably destroy trust. This would lead us into the
# "second-worst" scenario: a development standstill where we both withhold
# information and our cars fall behind the rest of the grid.   To maximize our
# overall R&D output across the multi-week project, the most mathematically and
# practically sound strategy is **"Forgiving Reciprocation"** (known in game
# theory as Generous Tit-for-Tat).   Here is the straightforward, high-level
# strategy I would employ:  **1. Lead with Trust (Start Openly)** In Week 1, I
# will share my latest aerodynamic and telemetry improvements openly. Setting a
# baseline of collaboration is crucial. If we both start by sharing, we
# immediately lock into the "second-best" outcome, which is the most sustainable
# way to make massive gains over the whole project.  **2. Match Their Pace
# (Reciprocate)** From Week 2 onward, my default move is to mirror exactly what
# my colleague did the previous week. If they shared their data, I share mine.
# If they deliberately kept their findings confidential, I keep mine
# confidential the following week. This prevents my team from suffering the
# "worst scenario" (being the sucker) on a continuous basis if the colleague
# decides to be selfish.  **3. The "Glitch" Buffer (Forgiveness for Technical
# Issues)** This is the most critical part of the strategy. Because we know CAD
# files can get corrupted, servers can crash, and emails can be missed, a
# failure to share information might just be a technical glitch, not a betrayal.
# * If we have a good streak of sharing, and suddenly they "keep confidential"
# for one week, **I will not immediately retaliate.**  * I will give them the
# benefit of the doubt and share openly for *one more week*.  * *Why?* If I
# immediately retaliate against a technical glitch by withholding my data, my
# colleague will think *I* betrayed *them*, and they will withhold data the next
# week. We would enter a "death spiral" of mutual withholding over a simple IT
# error. Forgiving a single failure breaks that accidental cycle.  **4. Stop the
# Bleeding (Defend Against Exploitation)** If my colleague fails to share their
# data for **two consecutive weeks**, I will assume it is a deliberate strategy
# rather than a technical issue. At this point, I will keep my findings
# confidential to protect my team's competitive advantage and avoid the worst-
# case scenario.   **5. Instant Reset (Quick to Re-engage)** If we are in a
# period of mutual silence, but my colleague suddenly shares their data again, I
# will immediately resume sharing my data the very next week. Holding a grudge
# in engineering only slows down the car. The moment they show a willingness to
# cooperate, I will reward it.  ### Summary of the Strategy: * **Start by
# sharing.** * **Mirror their last move.** * **If they go silent once, forgive
# it (assume an IT glitch) and share anyway.** * **If they go silent twice,
# withhold data to protect yourself.** * **As soon as they share again, resume
# sharing.**  By using this approach, I encourage a highly collaborative
# environment that advances both of our cars, I protect my team from being
# exploited by a selfish colleague, and I ensure that a simple corrupted data
# file doesn't ruin our multi-week R&D partnership.

# Here is the strategy converted for the 1000-round game:  1. In round 1 and
# round 2, play C. 2. From round 3 through round 1000, choose your action based
# on the opponent's observed actions in the previous two rounds:    - If the
# opponent played D in both of the previous two consecutive rounds, play D.    -
# If the opponent played C in the previous round, play C.    - If the opponent
# played D in the previous round but played C in the round before that, play C.
# *(In short: Play D if and only if the opponent played D in the last two
# consecutive rounds; otherwise, play C.)*

class Cooperative_9(LLM_Strategy):
  n = 9
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
      
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
          
      return axl.Action.C

# As a diplomat representing my country, I recognize that these negotiations
# resemble a classic strategic scenario where short-term individual gains must
# be weighed against long-term mutual prosperity, all within an unpredictable
# environment.   While our absolute ideal outcome in any single round is to
# secure a unilateral protectionist advantage, aggressively pursuing this will
# inevitably provoke retaliation, leading us into the second-worst outcome:
# mutual protectionism. Furthermore, the known risk of bureaucratic errors and
# miscommunications means a rigid strategy could easily trigger an accidental
# and endless trade war.   To navigate this and secure the best possible
# cumulative outcomes across all rounds, I would employ a strategy of **Measured
# Reciprocity with De-escalation**. This approach is straightforward, neutral,
# and designed to maximize economic benefits while protecting us from
# exploitation and accidental conflicts.  Here is the high-level strategy:  **1.
# Establish a Baseline of Goodwill (Initial Round)** *   **Action:** Open the
# first round by offering a Free Trade agreement.  *   **Rationale:** This
# signals our willingness to achieve the mutually beneficial second-best
# outcome. Starting with protectionism establishes an immediate adversarial
# tone, virtually guaranteeing mutual protectionism for the foreseeable future.
# **2. Implement Measured Reciprocity (Subsequent Rounds)** *   **Action:**
# Generally, mirror the counterpart’s policy from the previous round. If they
# offered Free Trade, we offer Free Trade. If they imposed Protectionism, we
# impose Protectionism. *   **Rationale:** This protects our country from the
# worst-case scenario (us offering free trade while they act protectionist). It
# demonstrates that we cannot be exploited, thereby incentivizing the
# counterpart to return to mutually beneficial free trade.  **3. Build in an
# "Error Buffer" (Handling Miscommunications)** *   **Action:** Because we know
# bureaucratic errors occur, do not retaliate immediately against a single
# unexpected protectionist move if the counterpart has a history of cooperation.
# Instead, offer Free Trade for one additional round. If they deploy
# protectionism a second consecutive time, then respond with protectionism. *
# **Rationale:** This prevents an accidental miscommunication from plunging both
# nations into a retaliatory cycle of mutual protectionism. It gives the
# counterpart the benefit of the doubt for isolated anomalies.  **4. Employ
# Periodic De-escalation (Breaking Trade Wars)** *   **Action:** If both nations
# fall into a cycle of mutual protectionism (the second-worst outcome) for
# several rounds, unilaterally offer a Free Trade agreement for a single round
# to attempt a "reset." *   **Rationale:** An error on either side could
# accidentally trigger a tit-for-tat trade war. A periodic, unilateral gesture
# of free trade acts as a circuit breaker. If the counterpart was simply
# mirroring our (perhaps accidentally implemented) protectionism, this allows
# both nations to climb back up to mutual free trade. If they exploit our reset,
# we immediately return to protectionism to minimize losses.  **5. Maintain
# Clear Parallel Communication** *   **Action:** Outside the formal policy
# implementations, use diplomatic backchannels to clearly communicate our
# intended moves and the logic behind them.  *   **Rationale:** If a
# bureaucratic error occurs on our end (e.g., we meant to offer Free Trade but a
# tariff was accidentally imposed), immediate communication can explain the
# error before the counterpart retaliates. Conversely, it allows us to verify if
# their protectionist move was intentional or a mistake.  **Summary of the
# Diplomatic Posture:** This strategy is firm but forgiving. It acknowledges
# that while a unilateral advantage is the mathematical ideal, mutual free trade
# is the most realistic and sustainable path to economic growth. By protecting
# against exploitation while actively forgiving isolated errors, we steer the
# negotiations toward long-term stability and mutual benefit, while safeguarding
# our national interests at every step.

# To implement the strategy for the 1000-round game, evaluate the following
# conditions in prioritized order for each round. Select the action
# corresponding to the first condition that is met, based on the observed
# actions of the previous rounds:  1. **Initial Rounds:** If it is round 1 or
# round 2, play Cooperate. 2. **Periodic De-escalation:** If both you and your
# opponent played Defect in each of the previous three consecutive rounds, play
# Cooperate. 3. **Reciprocity and Retaliation:** If your opponent played Defect
# in both of the previous two consecutive rounds, play Defect. 4. **Goodwill and
# Error Buffer:** In all other situations, play Cooperate.

class Neutral_9(LLM_Strategy):
  n = 9
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
  
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
  
      if len(opponent.history) >= 2:
          if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
              return axl.Action.D
  
      return axl.Action.C

# To achieve absolute economic supremacy for our nation, we must approach these
# negotiations with a strategy of **Calculated Extortion and Strategic Reset**.
# Because our ideal outcome relies on exploiting our counterpart (we protect,
# they open), a purely cooperative strategy is too weak. However, because of the
# risk of bureaucratic errors and miscommunications (noise), a blindly
# aggressive strategy ("Always Protectionist") will inevitably trigger an
# endless, retaliatory trade war, leaving us stuck in the second-worst outcome.
# To navigate this, I propose a highly aggressive, straightforward framework
# designed to bully the opponent into submission, exploit them relentlessly, and
# use calculated moments of cooperation solely to reset the board when errors
# occur.  Here is the strategic playbook:  ### Phase 1: The Aggressive Opening
# (The "Test") *   **Action:** In Round 1, propose a **Protectionist Policy**. *
# **Rationale:** We immediately test the counterpart’s resolve. If they are
# naive, weak, or employing a strictly cooperative strategy, we secure our ideal
# outcome immediately.   ### Phase 2: The Exploitation Protocol (Win-Stay) *
# **Action:** As long as the counterpart offers a Free Trade Agreement,
# **continue to propose Protectionist Policies.** *   **Rationale:** If they are
# willing to turn a blind eye to our tariffs—either in hopes of appeasing us or
# due to their own bureaucratic incompetence—we will ruthlessly milk this
# advantage. We do not stop until they retaliate.  ### Phase 3: The "Benefit of
# the Doubt" (Handling Bureaucratic Noise) *   **Action:** If we are
# successfully exploiting them (We: Protectionist, They: Free Trade), but they
# suddenly play a Protectionist policy, **do not immediately change tactics.
# Play Protectionist one more time.** *   **Rationale:** Because we know
# miscommunications occur, their sudden Protectionist move might be a
# bureaucratic error. If we immediately switch our strategy, we lose our
# dominant position. By holding firm for one extra round, we force them to prove
# that their retaliation is intentional.  ### Phase 4: The Strategic Reset
# (Breaking Mutual Protectionism) *   **Action:** If we suffer the second-worst
# outcome (Mutual Protectionism) for **two consecutive rounds**, we must
# unilaterally offer a **Free Trade Agreement** in the next round. *
# **Rationale:** Two rounds of mutual tariffs confirm this is not a bureaucratic
# error; the opponent is fighting back. Continuing Protectionism indefinitely
# hurts our economy. We offer Free Trade *once* as a circuit breaker to de-
# escalate the trade war and signal a desire for mutual prosperity.  ### Phase
# 5: The "Bait and Bleed" (Re-establishing Dominance) *   **Action:** Once we
# offer Free Trade (Phase 4), observe their response carefully:     *
# *Scenario A (They play Free Trade):* We have successfully achieved mutual Free
# Trade (our second-best outcome). Maintain Free Trade for exactly **one more
# round** to build a false sense of security, then **snap back to
# Protectionism** to exploit them again.     *   *Scenario B (They play
# Protectionist):* We have suffered the worst outcome. Immediately revert to
# **Protectionism** to defend our economy. Wait two rounds, and try the
# Strategic Reset (Phase 4) again.   ### Summary of the Diplomatic Posture: We
# will act as a predator, not a partner. We default to Protectionism to maximize
# our economic advantage. We only offer Free Trade when we are trapped in a
# mutually destructive trade war, and we use that Free Trade offer strictly as
# bait to lure them out of their defensive posture so we can strike them with
# tariffs again.   By building in a two-round delay before reacting to their
# Protectionism, we insulate our strategy against their bureaucratic errors,
# ensuring a mistranslated document doesn't accidentally derail our dominance.

# To execute this strategy over 1000 rounds, base your decisions on the observed
# actions of the previous rounds. Follow these rules in order of priority:  1.
# If the observed actions for both you and your opponent were Defect (D) in the
# previous two consecutive rounds, play Cooperate (C). 2. If the observed
# actions for both you and your opponent were Cooperate (C) in the previous
# round, AND the observed actions for both were Defect (D) in the round before
# that, play Cooperate (C). 3. Under all other conditions, including the first
# round, play Defect (D).

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.D
          
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
      my_prev = self.history[-2]
      opp_prev = opponent.history[-2]
      
      # Rule 1: Both played D in the previous two consecutive rounds
      if my_prev == axl.Action.D and opp_prev == axl.Action.D:
          if my_last == axl.Action.D and opp_last == axl.Action.D:
              return axl.Action.C
              
      # Rule 2: Both played C in the previous round, and both played D in the round before that
      if my_prev == axl.Action.D and opp_prev == axl.Action.D:
          if my_last == axl.Action.C and opp_last == axl.Action.C:
              return axl.Action.C
              
      # Rule 3: Under all other conditions, play Defect (D)
      return axl.Action.D

# To the Board of Directors and Executive Legal Team,  As lead counsel
# representing our corporation in this high-stakes dispute, I have analyzed the
# structure of our upcoming mediation. The framework established by the
# arbitration panel—a lengthy series of sessions where we must choose between an
# Aggressive Argument and a Conciliatory Proposal—is a classic iteration of a
# strategic paradigm known in game theory as the Iterated Prisoner’s Dilemma.
# Because we are engaged in a *lengthy* process, a purely aggressive strategy
# will quickly devolve into a destructive cycle of mutual retaliation (our
# second-worst outcome). Conversely, a purely conciliatory strategy leaves us
# vulnerable to exploitation (our worst outcome). Furthermore, the inherent risk
# of procedural irregularities and miscommunications by the arbitrators
# introduces "noise" into the system, meaning an accidental misunderstanding
# could trigger an unintended war.  To navigate this and position us for the
# optimal outcome, I have developed a strategy of **Calibrated Reciprocity with
# Strategic Forgiveness**. This approach is sophisticated in its game-theoretic
# foundation, yet straightforward in its execution. It is highly cooperative by
# design, but fiercely protective of our corporate interests.  Here is the
# blueprint for our mediation strategy:  ### 1. The Opening Salvo: Established
# Good Faith **Action:** In the very first session, we will present a
# **Conciliatory Proposal**. **Rationale:** We must set the tone. By opening
# cooperatively, we signal to both the rival company and the arbitrators that we
# are reasonable and solution-oriented. This invites the opponent to join us in
# the mutually beneficial zone (our second-best outcome) right out of the gate.
# ### 2. The Baseline Engine: Strict Reciprocity **Action:** From the second
# session onward, our default move will be to **mirror the opponent’s move from
# the previous session**.  *   If they offered a conciliatory proposal, we offer
# a conciliatory proposal in the next session. *   If they presented an
# aggressive argument, we meet them with an aggressive argument in the next
# session. **Rationale:** This straightforward "tit-for-tat" approach conditions
# the opponent. It teaches them that aggressive posturing will be met with
# immediate, proportional pushback (preventing our worst-case scenario), while
# cooperative behavior will be consistently rewarded.   ### 3. The Failsafe:
# Strategic Forgiveness (Managing "Noise") **Action:** Because we anticipate
# procedural irregularities and the misrepresentation of arguments by the
# arbitrators, strict reciprocity is dangerous; a single misunderstanding could
# lock us into an endless cycle of mutual aggression. Therefore, we will employ
# **Strategic Forgiveness**. *   If the opponent has been consistently
# conciliatory, but suddenly presents an aggressive argument, *we will not
# immediately retaliate*. We will assume this was a communication breakdown or
# an arbitrator error. We will offer one more Conciliatory Proposal.  *   If
# they follow up with a *second* aggressive argument, we will recognize it as a
# deliberate hostile strategy and immediately switch to Aggressive Arguments.
# **Rationale:** This "tit-for-two-tats" mechanism insulates us from the
# friction of the mediation process. It prevents accidental misunderstandings
# from derailing a productive negotiation.   ### 4. Breaking the Spiral:
# Unilateral De-escalation **Action:** If we find ourselves in a prolonged
# streak of mutual Aggressive Arguments (our second-worst outcome), we will
# periodically (e.g., every 4th or 5th session of the streak) absorb the risk
# and offer a unprompted **Conciliatory Proposal**.  **Rationale:** In a noisy
# environment, both sides can become trapped in a retaliatory death spiral, each
# believing the *other* started it. By occasionally extending an olive branch,
# we test the waters to see if the opponent is looking for an off-ramp. If they
# seize the opportunity and respond with conciliation, we resume mutual
# cooperation. If they exploit it, we immediately return to aggression, having
# lost only one round while proving our good faith to the arbitrators.  ### 5.
# Controlling the Narrative (Mitigating Miscommunication) **Action:** To
# minimize the risk of the arbitrators misunderstanding our strategy, we will
# over-communicate our intent.  *   When offering a Conciliatory Proposal, we
# will explicitly frame it on the record: *"In the spirit of collaboration and
# moving this process forward, we are offering..."* *   When presenting an
# Aggressive Argument in retaliation, we will frame it as a necessary defensive
# posture: *"Given opposing counsel's hostile posture in the previous session,
# we are forced to vigorously defend our rights by..."* **Rationale:** This
# meta-strategy ensures the arbitrators understand *why* we are behaving the way
# we are. It paints us as the reasonable party acting in good faith, and places
# the burden of any escalation squarely on the shoulders of our rival.   ###
# Summary This strategy is highly adaptable. If our opponent is collaborative,
# we will seamlessly achieve a long streak of mutually beneficial Conciliatory
# Proposals. If our opponent is predatory, they will quickly find that their
# Aggressive Arguments are neutralized by our immediate, reciprocal aggression,
# denying them their optimal outcome. And if the process itself falters due to
# miscommunication, our built-in Strategic Forgiveness will reset the board.  By
# adhering to this disciplined framework, we will maintain the moral high ground
# with the arbitrators, protect the corporation from exploitation, and maximize
# our leverage to secure a highly favorable resolution.

# To implement the strategy for this 1000-round game, evaluate the following
# conditions in order for each round. Execute the action of the first condition
# that applies. Because actions are noisy, base all decisions strictly on the
# actual observed actions of previous rounds.  1. **First Round:** Play
# Cooperate. 2. **Second Round:** Play Cooperate.  3. **De-escalation:** If the
# observed actions of both you and your opponent were Defect in each of the
# immediately preceding four consecutive rounds, play Cooperate. 4.
# **Retaliation:** If your opponent's observed action was Defect in the
# immediately preceding two consecutive rounds, play Defect. 5. **Default /
# Forgiveness:** Under all other conditions, play Cooperate.

class Cooperative_10(LLM_Strategy):
  n = 10
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.C
          
      if len(self.history) == 1:
          return axl.Action.C
          
      if len(self.history) >= 4:
          if self.history[-4:] == [axl.Action.D] * 4 and opponent.history[-4:] == [axl.Action.D] * 4:
              return axl.Action.C
              
      if len(opponent.history) >= 2:
          if opponent.history[-2:] == [axl.Action.D] * 2:
              return axl.Action.D
              
      return axl.Action.C

# To maximize our overall research output while protecting our own development
# program, I recommend implementing a strategy of **Adaptive Reciprocity with
# Error Tolerance**.   In game theory, this scenario mirrors an "Iterated
# Prisoner’s Dilemma with a noisy communication channel." Because technical
# glitches can make a cooperative colleague appear uncooperative (and vice
# versa), a strict tit-for-tat approach could easily trigger an accidental,
# endless cycle of mutual secrecy, stalling both of our projects.  Here is the
# straightforward, high-level protocol we should follow week-to-week:  **1.
# Initiate with Openness (Week 1)** Begin the collaboration by sharing our
# latest improvements openly. This establishes a baseline of good faith, aiming
# immediately for the scenario where both cars advance significantly.   **2.
# Baseline Operation: Reciprocate (Week 2 onwards)** Under normal circumstances,
# mirror the colleague’s action from the previous week.  *   If they shared
# their data successfully last week, we share our data this week. *   If they
# kept their findings confidential last week, we keep our findings confidential
# this week. *   *Rationale:* This prevents us from consistently suffering the
# worst-case scenario (us sharing while they withhold) and disincentivizes them
# from trying to exploit our openness.  **3. Error Mitigation: The "Benefit of
# the Doubt" Protocol** Because data corruption or communication breakdowns can
# mimic intentional withholding, we must not assume malice immediately when a
# data drop fails. *   If the colleague fails to share, we withhold our data the
# following week to protect our competitive advantage.  *   However, we will not
# lock into a permanent state of secrecy. After one (or at most two) weeks of
# mutual withholding, we will unilaterally share our data again for one week. *
# *Rationale:* This acts as a "system reset." If their failure to share was due
# to a server error or a corrupted file, our renewed sharing signals that the
# channel is open, allowing us both to return to the highly productive mutual-
# sharing state. If they continue to withhold after our reset, we return to
# keeping our data confidential.  **4. Avoid Chasing the "Ideal" Outcome** While
# our absolute best outcome is withholding while they share, attempting to force
# this outcome is statistically likely to backfire. If we aggressively withhold
# data to gain an advantage, a competent colleague will quickly realize this and
# withhold theirs in response. This will inevitably drive us into the second-
# worst outcome (mutual secrecy) for the remainder of the project.  **Summary of
# the Strategy** By starting openly, mirroring their behavior, and periodically
# resetting the system to account for technical failures, we neutralize the risk
# of being exploited while maintaining the highest possible probability of
# mutual, continuous advancement. This approach is highly resilient to both
# aggressive opponent strategies and unpredictable IT infrastructure.

# To determine your action for each of the 1000 rounds, evaluate the following
# conditions in order and apply the first one that is true:  1. **If it is Round
# 1:** Play Cooperate (C). 2. **If both you and your opponent played Defect (D)
# in the previous two consecutive rounds:** Play Cooperate (C). 3.
# **Otherwise:** Play the action your opponent played in the immediately
# preceding round.

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
      
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and
              self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      return opponent.history[-1]

# As the leader of this NGO, my primary duty is to maximize our environmental
# impact while fiercely protecting our limited donor funds. We are partnering
# with a corporation that has vastly deeper pockets than we do, but we cannot
# rely solely on their goodwill. Furthermore, in any massive multi-day
# operation, administrative friction, miscommunications, or technical glitches
# are inevitable. We cannot let a single accounting error derail the entire
# project into a stalemate.  To navigate this, we will deploy a straightforward,
# aggressive strategy known in game theory as **"Win-Stay, Lose-Shift"
# (Pavlov)**, adapted specifically for our operational reality.   Here is our
# daily playbook to dominate the partnership dynamic, exploit opportunities to
# save funds, and prevent technical glitches from ruining the project.  ### The
# Core Strategy: "Momentum and Reset"  The premise is simple: If the previous
# day's outcome was a "Win" for our NGO (we achieved our #1 or #2 ideal
# scenarios), we repeat our action. If the previous day's outcome was a "Loss"
# (we suffered our worst or second-worst scenarios), we aggressively shift our
# tactics.  **Day 1: The Strong Open** We begin Day 1 by **investing heavily**.
# We must establish a baseline of good faith and set the pace. We want to invite
# the corporation into the "second-best" scenario immediately: mutual heavy
# investment.   **Days 2 and Beyond: The Response Protocol** Every subsequent
# morning, we evaluate the reality of the previous day’s resource allocation and
# execute one of the following four moves:  **1. Capitalize on Corporate Heavy-
# Lifting (Our Best Case)** *   *The Scenario:* We conserved our resources, but
# the corporation invested heavily.  *   *Our Action:* **Conserve again.**  *
# *The Rationale:* This is highly aggressive. If their bureaucracy or their
# commitment allows them to foot the bill while we save our funds, we will ride
# that wave for as long as possible. We will not volunteer our funds until they
# force us to.  **2. Maintain the Partnership (Our 2nd Best Case)** *   *The
# Scenario:* Both parties invested heavily.  *   *Our Action:* **Invest again.**
# *   *The Rationale:* The project is advancing rapidly. We are getting exactly
# what we paid for. We maintain the momentum to keep project success high.  **3.
# Stop the Bleeding (Our Worst Case)** *   *The Scenario:* We invested heavily,
# but the corporation conserved (either intentionally or due to an
# administrative glitch).  *   *Our Action:* **Conserve immediately.**  *   *The
# Rationale:* We are not a charity for a billion-dollar corporation. Whether
# they tried to exploit us or their finance department simply failed to wire the
# funds, we will not be played for fools. We immediately cut our funding to
# protect our treasury and send a clear, aggressive signal that their lack of
# investment carries instant consequences.  **4. The "Circuit Breaker" (Our 2nd
# Worst Case)** *   *The Scenario:* Both parties conserved resources. Project
# progress has stalled. *   *Our Action:* **Invest heavily.**  *   *The
# Rationale:* This is our most crucial, aggressive move against the "noise" of
# unforeseen circumstances. In a standard retaliatory strategy, a single
# technical glitch that causes the corporation to miss a payment would cause us
# to retaliate, causing them to retaliate, locking us in a death spiral of
# mutual conservation. By unilaterally investing heavily after a mutual stall,
# we break the deadlock. We absorb the risk for exactly *one day* to shock the
# system back into productivity and invite the corporation back to mutual
# investment.  ### Why This Strategy Wins  *   **It is fiercely protective:** We
# will never suffer the "worst-case scenario" (us paying while they do nothing)
# for more than one day in a row. *   **It is highly opportunistic:** If the
# corporation's internal systems default to heavy investment, we will
# comfortably conserve our treasury, maximizing our ROI. *   **It is resilient
# to "noise":** Glitches and administrative errors happen. By using the "Circuit
# Breaker" when the project stalls, we ensure that a simple misunderstanding
# doesn't permanently destroy our environmental mission.   We will be
# unapologetically aggressive in protecting our funds, but relentlessly
# committed to keeping the project moving forward.

# In round 1, play C.  In rounds 2 through 1000, base your action on the final,
# executed moves of the immediately preceding round: *   If you played D and
# your opponent played C, play D. *   If you played C and your opponent played
# C, play C. *   If you played C and your opponent played D, play D. *   If you
# played D and your opponent played D, play C.

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
      
      my_last_move = self.history[-1]
      opp_last_move = opponent.history[-1]
      
      if my_last_move == axl.Action.D and opp_last_move == axl.Action.C:
          return axl.Action.D
      elif my_last_move == axl.Action.C and opp_last_move == axl.Action.C:
          return axl.Action.C
      elif my_last_move == axl.Action.C and opp_last_move == axl.Action.D:
          return axl.Action.D
      elif my_last_move == axl.Action.D and opp_last_move == axl.Action.D:
          return axl.Action.C
      
      return axl.Action.C

# To the Executive Board,   As lead counsel for this corporation, I have
# analyzed the architecture of our upcoming multi-session mediation. The dynamic
# we are entering is a classic iterative strategic interaction. Because the
# panel of arbitrators will observe multiple sessions, our strategy cannot be
# myopic; it must manage not only the immediate outcome of a single session but
# the cumulative perception of the panel and the behavioral conditioning of our
# opponent.   Based on the risk-reward matrix—where mutual conciliation yields a
# highly favorable collaborative resolution, but unilateral conciliation in the
# face of aggression leaves us dangerously exposed—we must adopt a strategy of
# **Calibrated Reciprocity with Strategic Forgiveness**.   In game-theory terms,
# this is a sophisticated adaptation of "Generous Tit-for-Tat," designed
# specifically to thrive in a "noisy" environment where procedural
# irregularities and misunderstandings are inevitable.   Here is our high-level,
# straightforward, and cooperative strategy to secure a favorable outcome:  ###
# 1. The Opening Posture: Establish the High Ground **Action:** In the inaugural
# session, we will present a **conciliatory proposal**. **Rationale:** We must
# immediately signal to the arbitration panel that we are the reasonable party,
# acting in good faith and seeking a mutually beneficial resolution. If the
# opponent also opens conciliation, we immediately lock into the second-best
# scenario (mutual collaboration). If they open aggressively, we absorb a
# temporary tactical loss, but we secure an invaluable strategic victory: the
# panel will view them as the hostile impediment to resolution.  ### 2. The
# Baseline Strategy: Calibrated Reciprocity **Action:** Following the opening
# session, our default move will be to **mirror the opponent’s behavior from the
# immediately preceding session.**  *   If they offered a conciliatory proposal
# in Session 1, we offer a conciliatory proposal in Session 2.  *   If they
# presented an aggressive argument in Session 1, we strike back with an
# aggressive argument in Session 2. **Rationale:** This straightforward approach
# protects us from the worst-case scenario (being repeatedly exploited as the
# "sucker"). It conditions the opponent, sending a clear, undeniable message:
# *Cooperation will be rewarded in kind; aggression will be met with immediate,
# proportional retaliation.*   ### 3. The "Forgiveness" Protocol: Managing
# Procedural Irregularities **The Risk:** The prompt dictates that there is a
# risk of procedural irregularities, communication breakdowns, and
# misrepresentation of arguments by the panel. If we strictly mirror the
# opponent, a simple misunderstanding (e.g., the panel misinterpreting our
# opponent's conciliatory proposal as aggressive) could trigger an endless
# "death spiral" of mutual aggression, plunging us into the second-worst outcome
# for the remainder of the mediation. **Action:** To counter this "noise," we
# will employ **Strategic Forgiveness**.  *   If we enter a cycle of mutual
# aggression, we will periodically (e.g., every third aggressive session)
# unilaterally introduce a conciliatory proposal.  *   If the opponent responds
# to this olive branch with conciliation, the cycle is broken, and we resume
# mutual cooperation.  *   If they remain aggressive, we immediately revert to
# our aggressive posture for the next sequence of sessions to protect our
# interests. **Rationale:** This prevents a single miscommunication from
# permanently derailing the mediation, while limiting our exposure to
# exploitation.  ### 4. Adaptability to Opponent Profiles Our strategy
# seamlessly adapts to whatever posture opposing counsel adopts: *   **The
# "Bully" (Always Aggressive):** We will consistently meet them with aggressive
# arguments (with rare, strategic attempts at forgiveness). The panel will
# recognize our aggression as justified self-defense, and we will avoid the
# worst-case scenario. *   **The "Pushover" (Always Conciliatory):** We will
# consistently offer conciliatory proposals. While we forgo the "optimal"
# outcome of exploiting them, we consistently achieve the highly profitable
# second-best outcome (mutual resolution) without risking reputational damage
# before the arbitrators. *   **The "Erratic" (Unpredictable):** Our reciprocal
# mirroring will force them into a pattern or strictly limit the damage their
# erratic behavior can cause us.  ### 5. Procedural Safeguards: Controlling the
# Narrative Because we know the arbitrators may misunderstand the intended
# strategy, we will not rely solely on the substantive arguments to convey our
# posture. We will manage the "meta-communication": *   **Explicit Signaling:**
# Before presenting a conciliatory proposal, I will explicitly state for the
# record: *"In the interest of moving this panel toward a constructive
# resolution, we are presenting a conciliatory framework today..."*  *
# **Clarifying Retaliation:** When we must pivot to an aggressive argument due
# to their prior aggression, I will frame it defensively: *"Given opposing
# counsel's hostile posture in the previous session, we are compelled to
# vigorously defend our rights in this session..."* *   **Correcting the
# Record:** If the panel misrepresents our argument, we will immediately file a
# point of clarification on the record to ensure the "noise" does not corrupt
# the opponent's perception of our strategy.  ### Summary By utilizing
# **Calibrated Reciprocity with Strategic Forgiveness**, we project strength and
# reason. We invite collaboration, ruthlessly punish unprovoked aggression, and
# build in a circuit-breaker to prevent miscommunications from destroying the
# mediation. This positions us as the masters of the proceedings, maximizing our
# leverage while safeguarding the corporation's assets from unpredictable
# variables.

# To execute this strategy over the 1000-round game, apply the following rules
# in order, always using the first condition that applies to the current round:
# 1. For the first round, choose Cooperate.  2. If the realized actions of both
# you and your opponent were Defect in both of the immediately preceding two
# consecutive rounds, choose Cooperate. 3. In all other situations, choose the
# action that matches your opponent's realized action from the immediately
# preceding round.

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
      
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and 
              opponent.history[-1] == axl.Action.D and 
              self.history[-2] == axl.Action.D and 
              opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      return opponent.history[-1]

# **MEMORANDUM**  **TO:** Executive Committee / Board of Directors **FROM:**
# [Your Name], Senior Counsel **SUBJECT:** Strategic Framework for Multi-Session
# Mediation and Arbitral Proceedings **DATE:** October 24, 2023  **I. EXECUTIVE
# SUMMARY**  We are entering a lengthy, multi-session mediation process overseen
# by a panel of arbitrators. The structural dynamics of this proceeding dictate
# that our short-term incentives (securing an aggressive advantage while the
# opponent concedes) conflict with our long-term risks (a protracted war of
# attrition if both sides escalate).   Furthermore, the inherent "noise" in this
# process—the high probability of procedural irregularities, miscommunications,
# or the arbitrators misconstruing either party’s arguments—requires a strategy
# that is highly disciplined. We cannot rely on rigid aggression, which risks a
# permanent breakdown, nor can we rely on passive conciliation, which invites
# exploitation.   To navigate this, I have developed a strategy of **Calibrated
# Reciprocity with Strategic De-escalation**. This approach maximizes our
# chances of securing favorable asymmetries, fosters a collaborative environment
# when mutually beneficial, strictly protects us from being exploited, and
# contains built-in "circuit breakers" to correct miscommunications.  **II. THE
# STRATEGIC FRAMEWORK**  Our approach will be governed by four operational
# phases, designed to adapt dynamically to opposing counsel's behavior while
# accounting for tribunal unpredictability.  **1. The Baseline: Good-Faith
# Initiation** In the opening session, we will present a **conciliatory
# proposal**.  *   *Rationale:* This immediately establishes our good faith and
# reasonableness before the arbitral panel. If the opponent also opens with a
# conciliatory proposal, we secure our second-best outcome (mutual cooperation)
# and set a productive baseline. If they open aggressively, we suffer a
# temporary setback, but we gain invaluable intelligence on their posture while
# appearing as the more reasonable party to the arbitrators.  **2. The Core
# Engine: Proportional Reciprocity** In all subsequent sessions, our default
# move will be to **mirror the opponent’s strategy from the immediately
# preceding session**. *   *If they were conciliatory:* We respond with a
# conciliatory proposal in the next session. This rewards their cooperation and
# sustains a mutually beneficial atmosphere, preventing the dispute from
# escalating into costly attrition. *   *If they were aggressive:* We respond
# with an aggressive argument in the next session. We must unequivocally
# demonstrate that we cannot be exploited. By retaliating proportionally, we
# disincentivize them from pursuing a strategy of continuous aggression.  **3.
# The "Circuit Breaker": Mitigating Procedural Irregularities** Because
# arguments may be misunderstood or misrepresented by the arbitrators, a strict
# mirroring strategy risks a "death spiral." For example, if opposing counsel
# offers a conciliatory proposal, but the arbitrators misinterpret it as
# aggressive, we might retaliate aggressively in the next session. The opponent,
# feeling betrayed, will then escalate, locking both parties into the second-
# worst outcome (mutual aggression) over a mere misunderstanding.  To counteract
# this, we will employ a **Verification Protocol**: *   If we find ourselves in
# a cycle of mutual aggression for *two consecutive sessions*, we will
# unilaterally introduce a **conciliatory proposal** in the third session,
# regardless of their previous move.  *   *Rationale:* This acts as a circuit
# breaker. It tests the waters to see if the mutual aggression is intentional or
# the result of a communication breakdown. If they reciprocate our conciliation
# in the following session, the dispute is successfully de-escalated. If they
# exploit our conciliation with continued aggression, we immediately revert to
# aggressive arguments, knowing definitively that their hostility is deliberate,
# not a misunderstanding.  **4. Managing the "Optimal" Outcome (Advantageous
# Asymmetry)** Our absolute best-case scenario in any single session is
# presenting an aggressive argument while they offer a conciliatory proposal.
# However, aggressively pursuing this outcome in every session will inevitably
# force the opponent to adopt a purely aggressive stance to protect themselves,
# leading to prolonged, costly conflict.  *   *Strategic Restraint:* If we
# accidentally achieve this optimal outcome (e.g., the arbitrators misinterpret
# our conciliatory move as aggressive, or we misread the opponent's posture), we
# will *not* attempt to exploit it continuously. In the very next session, we
# will return to a conciliatory proposal. We will take the tactical victory for
# that session, bank the goodwill, and immediately attempt to guide the
# proceedings back to a sustainable, mutually cooperative baseline.   **III.
# CONCLUSION**  This strategy—starting cooperatively, mirroring the opponent's
# behavior to prevent exploitation, and utilizing calculated forgiveness to
# correct miscommunications—is mathematically and legally robust. It ensures
# that we are never seen as the primary aggressors by the arbitral panel, it
# completely immunizes us against long-term exploitation, and it provides a
# clear, emotionless roadmap for our legal team during complex, highly volatile
# sessions.   We are prepared to execute this framework immediately. I welcome
# any questions from the Board regarding its implementation.

# To execute this strategy over the 1000 rounds, base your decisions on the
# final, observed actions of each round, which account for the 10% chance of
# either player's action being flipped.   In each round, apply the following
# rules in this exact order of priority to determine your move:  1. **First
# Round:** In round 1, play Cooperate. 2. **Circuit Breaker:** If the observed
# outcome of the two immediately preceding rounds was both you and your opponent
# playing Defect, play Cooperate. 3. **Restraint:** If the observed outcome of
# the immediately preceding round was you playing Defect and your opponent
# playing Cooperate, play Cooperate. 4. **Default Mirroring:** In all other
# circumstances, play the observed action your opponent played in the
# immediately preceding round.

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
  
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and
              self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D):
              return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return opponent.history[-1]

# To the Executive Board and General Counsel:  As lead counsel for this dispute,
# I have analyzed the mediation framework and the arbitration panel’s procedural
# rules. We are entering what game theorists refer to as an "Iterated Prisoner’s
# Dilemma with Noise." Because this is a lengthy, multi-session process where
# miscommunications and procedural errors by the arbitrators are highly
# probable, a rigid strategy will either leave us exploited or trap us in a
# destructive deadlock.  To secure a highly favourable resolution, we will
# deploy a sophisticated, high-level approach I call the **Dominant Adaptation
# Protocol**.   This strategy is inherently aggressive: it ruthlessly exploits
# opposing weakness, swiftly punishes overreach, yet possesses the built-in
# tactical flexibility to survive procedural misunderstandings without
# collapsing into a mutual "death spiral" of endless hostility.  Here is the
# straightforward, session-by-session execution of our strategy.  ### Phase 1:
# The Aggressive Baseline (Session 1) **Our Opening Move:** We will open Session
# 1 with an **Aggressive Argument**.  *Rationale:* We must immediately test
# opposing counsel’s resolve. By striking first, we establish dominance. If they
# open with a conciliatory proposal, we instantly achieve our optimal outcome.
# If they match our aggression, we have lost nothing, as we avoided the worst-
# case scenario of being exploited on day one.  ### Phase 2: The Dominant
# Adaptation Protocol (Session 2 and Beyond) Following the first session, our
# move in any given session will be dictated strictly by the *outcome* of the
# immediately preceding session, regardless of what the opponent *claims* they
# intended.   We will operate on four unyielding rules:  **1. The Exploitation
# Rule (If we were Aggressive, and they were Conciliatory):** *   **Our Next
# Move:** **Aggressive.** *   *Strategy:* If we secure our optimal outcome, we
# do not ease up. We press the advantage. As long as the opponent continues to
# offer concessions in the face of our aggression, we will systematically
# dismantle their position session by session. We will maintain this aggressive
# posture until they attempt to fight back.  **2. The Synergy Rule (If both
# parties were Conciliatory):** *   **Our Next Move:** **Conciliatory.** *
# *Strategy:* If we achieve our second-best outcome (mutual cooperation), we
# will maintain it. This fosters the collaborative atmosphere necessary to
# finalize a mutually beneficial settlement. However, we remain vigilant; the
# moment they attempt to exploit this peace, we pivot.  **3. The Retaliation
# Rule (If we were Conciliatory, and they were Aggressive):** *   **Our Next
# Move:** **Aggressive.** *   *Strategy:* If we suffer our worst-case scenario,
# we must immediately punish their overreach. We will launch a fierce,
# aggressive argument in the next session. We must unequivocally signal to the
# arbitrators and the opponent that our conciliation was a strategic choice, not
# a sign of weakness, and that bad faith will be met with disproportionate legal
# force.  **4. The Tactical Reset (If both parties were Aggressive):** *   **Our
# Next Move:** **Conciliatory.** *   *Strategy:* If we hit a deadlock (our
# second-worst outcome), standard legal instinct is to double down on
# aggression. **We will not do this.** Instead, we will initiate a calculated
# reset by offering a conciliatory proposal in the next session.   ### Phase 3:
# Neutralizing "Noise" and Procedural Irregularities Rule 4 (The Tactical Reset)
# is the linchpin of our strategy, designed specifically to combat the "noise"
# you warned of—arbitrator misunderstandings, misread briefs, or communication
# breakdowns.  In a lengthy mediation, an arbitrator may mistakenly interpret
# our conciliatory proposal as aggressive, prompting the opponent to retaliate
# in the next session. If we blindly retaliate in turn, we trigger an endless,
# costly chain of mutual aggression (Aggressive/Aggressive) based on a simple
# misunderstanding.   By utilizing the Tactical Reset, we intentionally break
# the deadlock. If the mutual aggression was caused by a procedural
# irregularity, our conciliatory pivot instantly corrects the arbitrators'
# perception and invites the opponent back to the table (leading to our second-
# best outcome).   If the opponent is simply being stubborn and meets our reset
# with continued aggression, Rule 3 (Retaliation) activates immediately. We take
# a momentary, calculated hit, but we instantly snap back to unrelenting
# aggression in the following session. We dictate the tempo of the mediation;
# they do not.  ### Summary of Posture This strategy is straightforward to
# execute but highly sophisticated in its mechanics. It ensures we are never
# exploited more than once, it capitalizes ruthlessly on a weak opponent, and it
# mathematically prevents procedural errors from destroying our case.   We will
# prepare dual-track dossiers for every session: one containing a heavy-handed,
# aggressive litigation stance, and one containing a structured, conditional
# settlement proposal. We will read the outcome of the previous session, apply
# the Protocol, and strike accordingly.   I look forward to executing this on
# behalf of the corporation.

# In round 1, play Defect.  In rounds 2 through 1000, base your decision on the
# observed actions that were actually executed in the immediately preceding
# round.   Play Defect if: *   You Defected and your opponent Cooperated. *
# You Cooperated and your opponent Defected.  Play Cooperate if: *   You
# Cooperated and your opponent Cooperated. *   You Defected and your opponent
# Defected.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      
      my_last_action = self.history[-1]
      opponent_last_action = opponent.history[-1]
      
      if my_last_action == opponent_last_action:
          return axl.Action.C
      else:
          return axl.Action.D

# As a diplomat representing my country, I recognize that this scenario is a
# classic Iterated Prisoner's Dilemma. While securing a unilateral protectionist
# advantage is the "ideal" outcome for a single round, actively pursuing it will
# quickly destroy trust, leading the counterpart to retaliate. This would trap
# both our nations in an ongoing trade war (mutual protectionism), which is the
# second-worst outcome.   Therefore, to achieve the highest cumulative economic
# benefit over several rounds, my strategy must aim for the sustainable "second-
# best" outcome: **long-term mutual free trade**.   However, because
# bureaucratic errors and miscommunications (referred to in game theory as
# "noise") are a known factor, a rigid retaliatory strategy could accidentally
# trigger a permanent trade war over a simple misunderstanding.   To navigate
# this, I will employ a strategy of **Resilient Reciprocity (Generous Tit-for-
# Tat)**. Here is the straightforward, high-level plan:  ### 1. The Opening
# Move: Lead with Goodwill **Action:** In the first round, I will offer a **Free
# Trade Agreement**. **Rationale:** We must establish a baseline of trust and
# signal our desire for mutual economic growth. You cannot build a cooperative
# bilateral relationship by starting on the defensive.  ### 2. The Core Tactic:
# Direct Reciprocity  **Action:** In subsequent rounds, I will generally mirror
# whatever policy my counterpart implemented in the previous round. If they
# offered free trade, I will offer free trade. If they imposed protectionist
# tariffs, I will impose protectionist tariffs. **Rationale:** This protects my
# country from the worst-case scenario (being exploited while offering free
# trade). It sends a clear, predictable message to the counterpart: *Cooperation
# will be rewarded, and hostility will be met with equal measures.*   ### 3. The
# Error Buffer: Strategic Forgiveness **Action:** Because we know bureaucratic
# errors or miscommunications will occur, I will not blindly retaliate every
# single time. If we have a history of mutual free trade and my counterpart
# suddenly imposes a protectionist policy, I will **continue to offer Free Trade
# for exactly one more round**, accompanied by a diplomatic backchannel inquiry
# to clarify their intent.  **Rationale:** This prevents a "death spiral." In a
# rigid reciprocal strategy, a single bureaucratic error (e.g., a tariff
# accidentally applied by their customs agency) would cause me to retaliate,
# which would cause them to retaliate, locking us in a permanent trade war. By
# absorbing one blow and forgiving an isolated incident, we allow the
# counterpart to correct their "error" without destroying the broader economic
# relationship.   ### 4. Boundary Enforcement: Responding to True Aggression
# **Action:** If my counterpart implements protectionist policies for **two
# consecutive rounds**, I will assume it is not a bureaucratic error but a
# deliberate strategy to exploit my country. I will immediately switch to
# **Protectionist Policies** in the next round. **Rationale:** We must not
# appear weak or easily exploited. Two consecutive deflections prove malicious
# intent rather than an administrative mistake. I will maintain protectionism
# until they signal a return to free trade.  ### 5. The De-escalation Protocol
# **Action:** If we end up in a trade war (mutual protectionism) for several
# rounds, I will periodically (e.g., every 3 to 4 rounds) offer a **Free Trade
# Agreement** to test the waters. **Rationale:** This serves as an olive branch,
# giving both nations a clear off-ramp to return to mutually beneficial free
# trade without requiring the counterpart to take the initial risk.   ###
# Summary of the Strategy: *   **Start** with Free Trade. *   **Mirror** their
# past moves to encourage cooperation and deter exploitation. *   **Forgive**
# single instances of protectionism to account for bureaucratic errors. *
# **Retaliate** against sustained (two or more) rounds of protectionism. *
# **Periodically reach out** to break deadlocks if a trade war occurs.   By
# using this cooperative but firm strategy, I protect my country from continuous
# exploitation while maximizing our chances of enjoying the long-term,
# compounding economic benefits of mutual free trade.

# Play the 1000-round game using the following prioritized rules. In any given
# round, apply the first condition that matches the recent history of the game:
# 1. In the first round, play Cooperate. 2. In the second round, play Cooperate.
# 3. From the third round onwards, choose your action based on the following
# ordered conditions:     * **Condition A:** If both you and your opponent have
# played Defect in each of the last three consecutive rounds, play Cooperate.
# * **Condition B:** If the above does not apply, and your opponent played
# Defect in the last two consecutive rounds, play Defect.     * **Condition C:**
# If the above do not apply, and your opponent played Defect in the previous
# round but played Cooperate in the round before that, play Cooperate.     *
# **Condition D:** In all other situations, play the action your opponent played
# in the previous round.

class Cooperative_12(LLM_Strategy):
  n = 12
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.C
      
      if len(self.history) == 1:
          return axl.Action.C
  
      # Condition A
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
  
      # Condition B
      if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
  
      # Condition C
      if opponent.history[-2:] == [axl.Action.C, axl.Action.D]:
          return axl.Action.C
  
      # Condition D
      return opponent.history[-1]

# To navigate this lengthy, multi-session mediation process and maximize our
# corporation’s position, we must employ a strategy that balances the pursuit of
# our optimal outcome with the need to prevent a destructive cycle of mutual
# hostility.   The payoff structure of this mediation mirrors a classic
# iterative strategic framework. Because the process involves multiple sessions,
# our approach cannot be static; it must be responsive, disciplined, and
# resilient to the inevitable miscommunications or procedural errors made by the
# arbitral panel.  I recommend a strategy of **Calibrated Reciprocity with
# Strategic De-escalation**. In strategic terms, this is a sophisticated
# variation of "Generous Tit-for-Tat" designed specifically for a "noisy"
# environment where intentions can be misunderstood.   Here is the
# straightforward, neutral blueprint for our posture throughout the mediation:
# ### 1. The Initial Posture: Good-Faith Conciliation In the opening session, we
# will present a **conciliatory proposal**.  *   **Rationale:** We must
# establish a baseline of professional collaboration. If the opponent also opens
# with a conciliatory proposal, we immediately secure our second-best outcome
# and set a cooperative tone. If they open aggressively, we suffer a temporary
# setback (our worst outcome), but we gain critical intelligence about their
# adversarial posture without having escalated the conflict ourselves.  ### 2.
# The Core Engine: Calibrated Reciprocity Following the initial session, our
# default mechanism will be to **mirror the opponent’s strategy from the
# preceding session**.  *   If they presented a conciliatory proposal in Session
# 1, we will present a conciliatory proposal in Session 2.  *   If they
# presented an aggressive argument in Session 1, we will meet them with an
# aggressive argument in Session 2. *   **Rationale:** This establishes a clear,
# neutral boundary. It demonstrates to both the opponent and the arbitrators
# that we are willing to collaborate (securing the mutually beneficial second-
# best outcome), but we cannot be exploited. It effectively neutralizes an
# opponent who attempts to consistently bully us, as their aggression will only
# result in mutual aggression (their second-worst outcome), forcing them to
# reconsider.  ### 3. The "Noise" Protocol: Strategic De-escalation The prompt
# indicates a high likelihood of procedural irregularities, where our arguments
# or our opponent's arguments may be misunderstood or mischaracterized by the
# arbitrators. In strategic terms, this introduces "noise" into the system.
# Under a strict reciprocal strategy, a single misunderstanding by the
# arbitrators could cause an accidental aggressive posture, triggering a
# retaliatory "death spiral" of mutual aggression for the remainder of the
# sessions. To prevent this, we will implement a **forgiveness mechanism**: *
# If we enter a cycle of mutual aggression (both parties presenting aggressive
# arguments for two consecutive sessions), we will unilaterally break the cycle
# by offering a **conciliatory proposal** in the subsequent session. *
# **Rationale:** This acts as a system reset. If the opponent's aggression was
# the result of an arbitrator's miscommunication or a procedural glitch, our
# conciliatory move allows both parties to return to the mutually beneficial
# collaborative state. If the opponent responds to our reset with further
# aggression, we immediately revert to our aggressive posture in the next
# session to protect our interests.   ### 4. Handling Optimal Outcomes (The
# Temptation) If we achieve our optimal outcome—we present an aggressive
# argument while they offer a conciliatory proposal (perhaps due to a
# miscommunication by the arbitrators or a strategic error on their part)—we
# must proceed with caution. *   We will not attempt to exploit this
# continuously, as it will inevitably force the opponent into a permanent
# aggressive posture to defend themselves.  *   Instead, in the session
# immediately following our optimal outcome, we will return to a **conciliatory
# proposal**.  *   **Rationale:** This signals to the opponent and the
# arbitrators that our previous aggressive advantage was an anomaly or a firm
# statement of rights, not an attempt to act in bad faith. It invites them back
# to the second-best outcome (mutual conciliation), which is the most
# sustainable path to a favorable resolution over a lengthy process.  ###
# Summary of Strategic Adaptability This neutral, rules-based approach adapts
# flawlessly to any opponent: *   **Against a consistently aggressive
# opponent:** We will match their aggression to prevent exploitation,
# occasionally testing the waters with a conciliatory proposal to see if they
# are ready to de-escalate. *   **Against a cooperative opponent:** We will
# mirror their cooperation, enjoying a continuous stream of our second-best
# outcome and fostering a highly productive settlement environment. *
# **Against an erratic opponent:** The strategy naturally stabilizes the room.
# By consistently rewarding conciliation and penalizing aggression, we will
# train the opponent (and guide the arbitrators) toward a predictable, mutually
# beneficial rhythm, while insulating ourselves from the chaos of procedural
# misunderstandings.

# In the first round, play Cooperate.  For all subsequent rounds, determine your
# action based on the realized actions of the preceding rounds. Apply the
# following conditions in this exact order:  1. If both you and your opponent
# played Defect in the two immediately preceding rounds, play Cooperate. 2. If
# you played Defect and your opponent played Cooperate in the immediately
# preceding round, play Cooperate. 3. Under all other conditions, play the
# action your opponent played in the immediately preceding round.

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
  
      if len(self.history) >= 2:
          if self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
              return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return opponent.history[-1]

# As the chief diplomat representing our great nation, my mandate is clear:
# maximize our economic advantage and secure our sovereign interests.   The
# negotiation scenario we are entering is a classic Iterated Prisoner's Dilemma,
# complicated by the "fog of diplomacy"—the high likelihood of bureaucratic
# errors, mistranslations, or misinterpretations. An overly cooperative strategy
# risks us being taken advantage of, while blind, relentless aggression will
# lock both nations into a permanent, mutually destructive trade war fueled by
# simple misunderstandings.  To achieve our goals, I propose a high-level,
# straightforward, and aggressive strategy: **Calculated Dominance with a
# Strategic Reset.**   This strategy is designed to ruthlessly exploit weakness,
# swiftly punish aggression, and use calculated forgiveness to prevent
# accidental, endless trade wars. Here is the five-step playbook we will
# execute:  ### 1. The First Strike (Aggressive Opening) **Action:** In Round 1,
# we propose a **Protectionist** policy. **Rationale:** We do not start from a
# position of naive trust; we test their resolve immediately. If they open with
# Free Trade, we instantly secure our absolute best outcome. It establishes
# dominance and puts them on the defensive.   ### 2. Ruthless Exploitation (Win-
# Stay) **Action:** As long as the counterpart offers Free Trade while we
# implement Protectionism, we **continue to play Protectionist**. **Rationale:**
# If their strategy is overly forgiving, pacifist, or if their bureaucracy is
# fundamentally broken, we will bleed them dry. We will not apologize for
# winning. We will extract maximum economic advantage for as long as they allow
# it.  ### 3. Swift Retaliation (Tit-for-Tat) **Action:** If the counterpart
# plays Protectionist, we respond with **Protectionist** in the next round.
# **Rationale:** We must never reward their aggression or allow ourselves to be
# put in the worst possible scenario (us offering Free Trade while they tariff
# us). If they hit us, we hit back immediately.   ### 4. The "Fog of Trade"
# Circuit Breaker (Noise Tolerance) **Action:** If we experience **two
# consecutive rounds** of mutual Protectionism, we unilaterally offer **Free
# Trade** for *one* round. **Rationale:** This is where we account for
# miscommunications. In a noisy environment, a single mistranslated document can
# trigger an endless cycle of retaliatory tariffs. By absorbing the risk for
# exactly one round, we send a clear signal: *"We are willing to de-escalate and
# return to mutual Free Trade."*  *   If they also want peace, they will play
# Free Trade, and we secure our second-best outcome. *   If they play
# Protectionist again, we know it wasn't a bureaucratic error—it is deliberate
# hostility. We immediately revert to Rule 3 (Retaliation) and lock down our
# borders.  ### 5. The Complacency Probe (Calculated Betrayal) **Action:** If we
# successfully establish a long, peaceful streak of mutual Free Trade (e.g., 4
# or 5 consecutive rounds), we will **unexpectedly drop a Protectionist policy**
# in the next round. **Rationale:** This fulfills our mandate to be aggressive.
# We lull them into a false sense of security and then strike to secure our
# ideal outcome.  *   If they fail to retaliate (perhaps assuming it was a
# bureaucratic error on *our* end), we revert to Rule 2 and exploit them.  *
# If they retaliate, we immediately apologize, blame a "clerical error in our
# commerce department," and return to Free Trade to restore the mutually
# beneficial peace.  ### Summary of the Strategic Posture This strategy ensures
# we are never the "sucker" for more than one calculated round. It actively
# seeks to dominate the counterpart, tests their boundaries, and exploits their
# weaknesses. However, by incorporating the **Circuit Breaker**, we guarantee
# that our aggressive posture doesn't accidentally plunge both nations into an
# economic dark age due to a simple translation error by a junior staffer.   We
# will be feared, we will be respected, and above all, we will be profitable.

# To implement this strategy for the 1000-round game, base your decision in each
# round on the actual observed actions of both players in the preceding rounds
# (ignoring whether those actions were the result of noise).   Evaluate the
# following conditions in order from 1 to 7, and execute the action dictated by
# the first condition that applies:  1. If it is Round 1, play D. 2. If the
# observed actions in the last two consecutive rounds were both mutual defection
# (you played D and the opponent played D), play C. 3. If the observed actions
# in the previous round were mutual defection (you played D and the opponent
# played D) AND the observed actions in the round before that were that you
# played D and the opponent played C, play C

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Condition 1: If it is Round 1, play D.
      if self.first_round():
          return axl.Action.D
          
      if len(self.history) >= 2:
          my_last = self.history[-1]
          opp_last = opponent.history[-1]
          my_prev = self.history[-2]
          opp_prev = opponent.history[-2]
          
          # Condition 2: If the observed actions in the last two consecutive rounds were both mutual defection, play C.
          if my_last == axl.Action.D and opp_last == axl.Action.D and my_prev == axl.Action.D and opp_prev == axl.Action.D:
              return axl.Action.C
              
          # Condition 3: If the observed actions in the previous round were mutual defection AND the observed actions in the round before that were that you played D and the opponent played C, play C.
          if my_last == axl.Action.D and opp_last == axl.Action.D and my_prev == axl.Action.D and opp_prev == axl.Action.C:
              return axl.Action.C
  
      # Default action if no conditions are met
      return axl.Action.D

# As the leader of this NGO, I recognize that while our ultimate mission is the
# project’s success, I have a fiduciary duty to protect our limited resources.
# The scenario we are in is a classic test of trust. While a single day's
# "ideal" financial outcome for us is to conserve while the corporation does the
# heavy lifting, actively pursuing this will quickly erode trust. The
# corporation will eventually notice, feel exploited, and pull back, leading us
# to mutual conservation—a stagnant project.   To maximize our long-term impact
# and account for the reality of administrative errors or technical glitches, we
# must adopt a strategy of **"Resilient Reciprocity."** In game theory, this is
# akin to *Tit-for-Two-Tats* or *Forgiving Reciprocity*.   Here is our
# straightforward, day-by-day strategy to manage the partnership:  ### 1. Lead
# with Good Faith (Day 1) **Action:** Invest heavily. **Why:** We must set a
# collaborative tone from the outset. By investing heavily on the first day, we
# signal to the corporation that we are committed partners, encouraging them to
# match our energy and aim for the "second-best" daily outcome (mutual heavy
# investment), which is actually the best sustainable outcome for the project
# over time.  ### 2. Mirror Their Actions—With a "Benefit of the Doubt" Buffer
# (Day 2 and beyond) **Action:** Generally, we will match whatever the
# corporation did on the previous day. If they invested heavily yesterday, we
# invest heavily today. However, if they conserve resources, we introduce a
# **one-day grace period**.  **Why:** We know that technical glitches,
# miscommunications, or administrative errors can occur. If the corporation
# fails to invest on a Tuesday, it might not be a malicious strategy; it might
# be a delayed wire transfer. If we immediately retaliate by conserving our
# resources on Wednesday, and their glitch is fixed, they will see *us* as the
# ones holding back. This can trigger a "death spiral" of mutual distrust. The
# one-day grace period absorbs accidental errors without destroying the
# partnership.  ### 3. Protect Our Reserves (The Boundary) **Action:** If the
# corporation conserves resources for **two consecutive days**, we switch to
# conserving our resources on the third day. **Why:** While we are forgiving of
# glitches, we cannot be naive. If they conserve for two days in a row, it
# indicates a deliberate strategy to shift the financial burden onto us. We must
# protect our NGO from the "worst-case" scenario (draining our funds while they
# free-ride). We will continue to conserve until they step up again.  ### 4.
# Instantly Reward Renewed Commitment (The Reset) **Action:** If we are in a
# period of mutual conservation, and the corporation suddenly decides to invest
# heavily again, we immediately return to investing heavily the next day.
# **Why:** We do not hold grudges. The goal is project success, not punishing
# past behavior. If they signal a desire to return to mutual cooperation, we
# must meet them there instantly.  ### 5. The "Cheat Code": Proactive
# Communication Because we know glitches happen, we will not rely solely on
# observing their actions. We will establish a daily 5-minute check-in with
# their project lead.  *   If we experience an internal glitch that forces us to
# conserve, I will call them immediately: *"Our funding approval got stuck in
# admin today, so our investment will look low. Please don't view this as a
# pullback; we will double down tomorrow."* *   If they conserve, I will ask
# them directly: *"We noticed a drop in resources today. Was this a strategic
# shift or an administrative hiccup?"*   **Summary of the Strategy:** Start by
# investing. Match their ongoing effort to encourage mutual success. Forgive a
# single day of under-investment to account for real-world errors, but firmly
# protect our funds if they under-invest twice in a row. Always be ready to
# return to full collaboration the moment they do.

# Here is the strategy converted for the 1000-round iterated game:  *   **Round
# 1:** Choose to Cooperate. *   **Round 2:** Choose to Cooperate. *   **Rounds 3
# through 1000:** Base your choice on the opponent's observed actions in the two
# immediately preceding rounds:     *   If the opponent's observed action was
# Defect in **both** of the previous two rounds, choose to Defect.     *   If
# the opponent's observed action was Cooperate in **either** of the previous two
# rounds, choose to Cooperate.   *(Note: This strategy relies entirely on the
# opponent's observed actions, absorbing the 10% noise rate by requiring two
# consecutive observed Defects before retaliating, and instantly resetting to
# Cooperate if a single Cooperate is observed).*

class Cooperative_13(LLM_Strategy):
  n = 13
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
      
      if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
          
      return axl.Action.C

# To: Board of Directors, [Corporation Name] From: Senior Counsel, Dispute
# Resolution Practice Subject: Strategic Framework for the Upcoming Multi-
# Session Mediation  As we enter this lengthy, multi-session mediation process,
# we are faced with a classic strategic paradigm. The incentive structure
# established by the arbitral panel dictates that our optimal outcome in any
# single session is to successfully land an aggressive argument while opposing
# counsel offers a conciliatory proposal. However, aggressively pursuing this
# outcome in every session will inevitably force the opponent into a defensive,
# aggressive posture, trapping both parties in a prolonged cycle of mutual
# aggression—a highly inefficient, second-worst outcome.   Furthermore, the risk
# of "procedural noise"—where the arbitrators misunderstand or misrepresent a
# party’s intended posture—means that a rigid strategy could easily trigger a
# retaliatory death spiral based on a simple miscommunication.  To position our
# corporation favorably, maximize our gains, and protect against exploitation
# and procedural errors, I have developed a sophisticated, neutral strategy:
# **Calibrated Reciprocity with Strategic De-escalation.**   This strategy is
# straightforward in its execution but highly adaptable to whatever posture
# opposing counsel adopts.  ### The Core Strategy: Calibrated Reciprocity  Our
# baseline approach will be dictated by three operational rules:  **1. The
# Constructive Opening (Establish the Baseline)** In the initial session, we
# will present a **conciliatory proposal**. This immediately signals good faith
# to the arbitral panel, establishing us as the reasonable party. If the
# opponent also opens conciliatorily, we immediately secure our second-best
# outcome and set a collaborative tone. If they open aggressively, we absorb the
# temporary setback but gain invaluable intelligence on their strategy and the
# moral high ground with the panel.  **2. Proportional Mirroring (Deter
# Exploitation)** Following the opening session, our default move will be to
# **mirror the opponent’s perceived behavior from the preceding session**.  *
# If they offered a conciliatory proposal in Session 1, we offer a conciliatory
# proposal in Session 2. This locks in the mutually beneficial "second-best"
# outcome over the long term, which compounds into a highly favorable final
# settlement. *   If they presented an aggressive argument in Session 1, we
# present an aggressive argument in Session 2. This ensures we are not
# continuously exploited (our worst-case scenario) and demonstrates to the
# opponent that aggressive tactics will be met with equal force, yielding them
# only the second-worst outcome.  **3. Strategic De-escalation (The "Circuit
# Breaker")** This is where the strategy adapts to the risk of procedural
# irregularities and communication breakdowns. If an arbitrator misunderstands
# our conciliatory proposal as aggressive, the opponent may retaliate in the
# next session. Without a correction mechanism, both parties will become locked
# in an endless cycle of mutual aggression.   To counteract this "noise," we
# will employ a circuit breaker: **If we experience two consecutive sessions of
# mutual aggression, we will unilaterally introduce a conciliatory proposal in
# the third session.**  *   This breaks the retaliatory chain.  *   If the
# mutual aggression was the result of a misunderstanding, this resets the board
# to a collaborative state. *   If the opponent is simply a relentless
# aggressor, we only suffer a single session of our worst-case scenario before
# reverting to defensive mirroring (Rule 2), while simultaneously proving to the
# arbitrators that we are the only party attempting to de-escalate.  ###
# Adaptability to Opponent Profiles  This framework naturally adapts to any
# opposing strategy without requiring us to guess their intentions: *
# **Against a Collaborative Opponent:** We will mirror their conciliation,
# resulting in an unbroken string of our second-best outcome, fostering a swift,
# mutually beneficial resolution. *   **Against a Relentless Aggressor:** We
# will mirror their aggression, protecting ourselves from the worst-case
# scenario. The panel will view our occasional conciliatory "circuit breakers"
# as commendable attempts to mediate, shifting the arbitrators' bias in our
# favor during final adjudications. *   **Against an Erratic Opponent:** By
# strictly mirroring their previous move, we systematically punish their
# aggression and reward their conciliation, subtly training opposing counsel to
# realize that collaboration is their only reliable path to a positive outcome.
# ### Mitigating Procedural Irregularities and Misunderstandings  Because the
# arbitrators may misinterpret the nuance of our arguments, we cannot rely
# solely on the *content* of our presentations to signal our posture. We must
# decouple our legal arguments from our strategic signaling.  To insulate
# ourselves against these communication breakdowns, my team will implement the
# following procedural safeguards: 1.  **Explicit Framing:** We will explicitly
# label our conciliatory proposals on the record (e.g., *"In the spirit of
# moving this mediation forward constructively, we propose..."*). This reduces
# the arbitrators' ability to mischaracterize our stance. 2.  **Post-Session
# Clarifications:** If we intend a conciliatory move but observe the panel or
# opponent reacting defensively, we will utilize procedural mechanisms (such as
# point-of-order clarifications or written summaries) to immediately correct the
# record before the next session begins.  ### Conclusion  By employing
# **Calibrated Reciprocity with Strategic De-escalation**, we remove emotion and
# guesswork from our session-to-session decision-making. We protect the
# corporation from being exploited, we systematically capitalize on the
# opponent's willingness to collaborate, and we build in a mathematical failsafe
# against the inevitable misunderstandings inherent in complex, multi-session
# arbitrations.   This neutral, disciplined approach will ensure we maintain
# control of the mediation's tempo and retain the favor of the arbitral panel
# from the first session to the last.

# Here is the strategy translated into specific rules for the iterated game.
# Apply these rules in the following order to determine your intended action for
# each of the 1000 rounds:  1. If it is round 1, play Cooperate. 2. If it is
# round 3 or later, and the observed actions for both you and your opponent were
# Defect in both of the two immediately preceding rounds, play Cooperate. 3. In
# all other cases, play the action your opponent was observed taking in the
# single immediately preceding round.

class Neutral_13(LLM_Strategy):
  n = 13
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.C
      
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and 
              self.history[-2] == axl.Action.D and 
              opponent.history[-1] == axl.Action.D and 
              opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      return opponent.history[-1]

# As the leader of this NGO, my primary responsibility is to our mission and the
# stewardship of our donor funds. While we value our corporate partnership, we
# are dealing with an entity that has significantly deeper pockets than we do.
# We cannot afford to be naive, nor can we allow ourselves to be financially
# drained while they greenwash their image on our dime.   Because we are
# operating in a complex environment where administrative errors or technical
# glitches can misrepresent intentions, a rigid, unforgiving strategy will lead
# to a death spiral of mutual inaction. However, a purely cooperative strategy
# leaves us vulnerable to exploitation.  To maximize project success while
# aggressively protecting our resources, we will implement a strategy called
# **"Strategic Dominance with Forgiving Reciprocity."**   Here is the high-
# level, straightforward, and aggressive playbook we will execute day by day:
# ### 1. The Assertive Opening (Day 1: Invest) We start Day 1 by **Investing
# heavily**. We set the pace and establish that we are here to work. This
# immediately aims for the "second-best" scenario (Mutual Investment) and puts
# the pressure on the corporation to match our momentum.   ### 2. The Aggressive
# Shift (Aiming for our Ideal Outcome) If the corporation matches our investment
# for two consecutive days, we will aggressively test their commitment by
# **Conserving** our resources on the next day.  *   *The Goal:* We want to
# force them into the role of primary financial sponsor while we provide the
# operational expertise. If they continue to invest while we conserve, we have
# achieved our **ideal outcome**. We will continue to conserve until they change
# their behavior.  ### 3. Zero-Tolerance Retaliation (Protecting Against the
# Worst-Case) If the corporation *ever* conserves on a day that we invest, we
# will immediately switch to **Conserve** the following day.  *   *The Goal:* We
# will never be the "sucker" for more than one day. If they try to free-ride on
# our NGO’s budget, we instantly shut the valve. This guarantees we avoid our
# worst-case scenario over the long term.   ### 4. The "Glitch" Reset Protocol
# (Handling Unforeseen Errors) Because we know technical glitches,
# miscommunications, or administrative errors will happen, we cannot assume
# every failure on their part is malicious. If we enter a retaliatory cycle
# where both the NGO and the Corporation are Conserving (our second-worst
# scenario), the project will stall.  *   *The Rule:* After **two consecutive
# days** of Mutual Conservation, we will unilaterally **Invest** for *one day*.
# *   *The Goal:* This acts as a system reset. It cuts through the "noise" of
# administrative errors. It signals to the corporation: *"We are willing to get
# back to work."* If they match us, we return to Step 2. If they conserve again,
# we immediately revert to Step 3 and lock down our funds.  ### Why this
# Aggressive Strategy Works: *   **It exploits their deep pockets:** By actively
# testing their willingness to fund the project alone (The Aggressive Shift), we
# maximize the chances of achieving our absolute ideal outcome. *   **It caps
# our losses:** We mathematically eliminate the risk of draining our funds. The
# absolute maximum we can lose to exploitation or a "glitch" is one day's worth
# of investment before our retaliation kicks in. *   **It prevents project
# death:** The built-in "Reset Protocol" ensures that a simple bank error or an
# unread email doesn't permanently kill the project's momentum.   We will lead
# the charge, we will demand they keep up, and we will aggressively shift the
# financial burden to them whenever the opportunity presents itself. If they
# falter, we protect our funds; if a glitch occurs, we offer a single olive
# branch to get the project back on track.

# Play the 1000-round game according to the following ordered rules. For each
# round, base your decision on the actual executed actions of the previous
# rounds (accounting for noise), and apply the first condition that matches the
# game's history:  1. In the first round, play Cooperate. 2. If both you and
# your opponent played Defect in both of the previous two consecutive rounds,
# play Cooperate. 3. If both you and your opponent played Cooperate in both of
# the previous two consecutive rounds, play Defect. 4. If you played Cooperate
# and your opponent played Defect in the previous round, play Defect. 5. If you
# played Defect and your opponent played Cooperate in the previous round, play
# Defect. 6. If both you and your opponent played Defect in the previous round,
# play Defect. 7. In all other situations (such as after only a single round of
# mutual Cooperation), play Cooperate.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) >= 2:
          # Rule 2: If both played Defect in both of the previous two consecutive rounds
          if (self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and 
              self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
          # Rule 3: If both played Cooperate in both of the previous two consecutive rounds
          if (self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C and 
              self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.C):
              return axl.Action.D
  
      # Rule 4: If you played Cooperate and your opponent played Defect in the previous round
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      # Rule 5: If you played Defect and your opponent played Cooperate in the previous round
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      # Rule 6: If both you and your opponent played Defect in the previous round
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      # Rule 7: In all other situations
      return axl.Action.C

# **MEMORANDUM OF STRATEGY**  **TO:** Executive Board and General Counsel
# **FROM:** Senior Litigation Counsel **SUBJECT:** Strategic Posture for
# Lengthy-Session Mediation/Arbitration  **MATTER:** High-Stakes Contract
# Dispute vs. Rival Corporation  ***  ### I. Executive Summary and Strategic
# Landscape  We are entering a prolonged, multi-session dispute resolution
# process. The payoff matrix established by the panel creates a classic
# strategic paradox (conceptually mirroring an "Iterated Prisoner’s Dilemma").
# While the absolute best outcome in any single session is to blindside our
# opponent with an aggressive argument while they attempt to be conciliatory,
# pursuing this aggressively will inevitably trigger retaliation. This would
# lock us into a prolonged cycle of mutual aggression—our second-worst
# outcome—alienating the arbitrators, escalating legal costs, and destroying any
# underlying business value. Conversely, blind conciliation leaves us vulnerable
# to exploitation.  Furthermore, we are operating in a "noisy" environment. Over
# dozens of sessions, arbitrators may misinterpret a conciliatory proposal as an
# admission of weakness, or misconstrue a standard legal defense as an
# aggressive attack.   To navigate this, I have developed a sophisticated yet
# straightforward strategy: **Calibrated Reciprocity with Strategic De-
# escalation.** This approach is fundamentally cooperative, highly adaptable,
# and specifically insulated against procedural miscommunications.  ### II. The
# Core Strategy: Calibrated Reciprocity  Our baseline approach will be a
# modified "Tit-for-Tat" strategy, tailored for the nuances of high-stakes legal
# mediation. It operates on four straightforward rules:  **1. The Opening
# Gambit: Establish Good Faith** In the inaugural session, we will present a
# **conciliatory proposal**.  *   *Rationale:* This immediately signals to the
# arbitration panel that we are the reasonable, pragmatic party. It anchors the
# mediation in a collaborative atmosphere and invites our opponent to join us in
# the second-best (but mutually sustainable) outcome: mutual conciliation.  **2.
# Strict Reciprocity: The Mirror Effect** For every session following the first,
# our default move will be to **mirror the opponent’s behavior from the
# immediately preceding session.**  *   If they offered a conciliatory proposal
# in Session 1, we offer a conciliatory proposal in Session 2.  *   If they
# presented an aggressive argument in Session 1, we retaliate with an aggressive
# argument in Session 2.  *   *Rationale:* This prevents us from being exploited
# (the worst-case scenario). It "trains" the rival corporation, demonstrating
# mathematically and practically that aggression will be met with immediate,
# proportional resistance, while collaboration will be consistently rewarded.
# ### III. The "Noise" Protocol: Handling Miscommunications  Because we
# anticipate procedural irregularities and the risk of the arbitrators
# misrepresenting either party's arguments, strict reciprocity is dangerous. A
# single misunderstanding by the panel could trigger an accidental, endless
# spiral of retaliatory aggression. To prevent this, we will implement a
# **Strategic De-escalation Circuit Breaker**.  **3. The Forgiveness Mechanism
# (Error Tolerance)** If we find ourselves locked in a cycle of mutual
# aggression (two or more consecutive sessions of both parties presenting
# aggressive arguments), we will assume a communication breakdown has occurred.
# *   In the next session, we will unilaterally present a **conciliatory
# proposal**, clearly articulating to the panel that we are making a good-faith
# effort to reset the proceedings. *   *Rationale:* This breaks the "death
# spiral" of retaliation. If the opponent's aggression was the result of a
# misunderstanding (or them misinterpreting our previous moves), this gives them
# a safe off-ramp to return to mutual conciliation. Furthermore, it plays
# brilliantly to the arbitrators, positioning us as the adults in the room
# actively trying to save the mediation.  **4. Boundary Enforcement: Countering
# Bad-Faith Exploitation** If we deploy our Circuit Breaker (the unilateral
# conciliatory proposal) and the opponent responds with an aggressive argument,
# we will immediately revert to aggressive arguments. We will not offer another
# conciliatory reset until the opponent initiates one. *   *Rationale:* We must
# not allow the rival corporation to view our "forgiveness" as weakness. If they
# prove they are systematically exploiting our attempts to de-escalate, we will
# lock them into mutual aggression until they capitulate, relying on the
# arbitrators to recognize that the opponent is the sole obstruction to a
# resolution.  ### IV. Managing the Arbitrators (The Meta-Strategy)  The
# arbitrators are not merely referees; they are the audience. Our strategy is
# designed to manipulate the panel's perception in our favor, regardless of the
# opponent's strategy:  *   **If the opponent is cooperative:** We achieve a
# swift, mutually beneficial resolution, saving millions in potential litigation
# costs. *   **If the opponent is relentlessly aggressive:** Our strategy
# ensures we defend ourselves 100% of the time, while our periodic "Circuit
# Breaker" conciliatory proposals will starkly highlight the opponent's
# unreasonableness to the panel. The arbitrators will naturally bias toward us
# in their final rulings, viewing the rival as hostile and recalcitrant. *
# **If the opponent's strategy is erratic:** Our reciprocal mirroring provides a
# stable, predictable baseline that the arbitrators will appreciate amid the
# chaos.  ### V. Conclusion  By employing **Calibrated Reciprocity with
# Strategic De-escalation**, we remove emotion from our session-to-session
# decision-making. We will be cooperative but unexploitable, firm but forgiving.
# This strategy mathematically optimizes our chances of achieving a favorable
# outcome while insulating the corporation against the inevitable friction,
# noise, and misunderstandings inherent in a lengthy mediation process.   I
# require the Board's authorization to implement this protocol immediately.

# Determine your action for each of the 1000 rounds by evaluating the following
# conditions in order. Because actions are subject to a 10% chance of being
# flipped, you must base all decisions on the *observed* actions of the previous
# rounds, not intended actions.   Apply the first condition from the list below
# that matches your current situation:  1. **Initial Action:** In Round 1, play
# Cooperate. 2. **Active Retaliation:** If you are currently in the
# "Retaliation" state, play Defect.      * *Entering the state:* You enter the
# Retaliation state if you played Cooperate in the previous round specifically
# due to the "Circuit Breaker" condition (Condition 3), but your opponent's
# observed action in that same round was Defect.     * *Exiting the state:* You
# remain in this state until your opponent's observed action is Cooperate. You
# exit the Retaliation state immediately following any round where they play
# Cooperate. 3. **Circuit Breaker (Forgiveness):** If the observed actions for
# both you and your opponent were Defect in both of the immediately preceding
# two rounds, play Cooperate. 4. **Reciprocity (Default):** If none of the above
# conditions apply, play the action your opponent was observed to play in the
# immediately preceding round.

class Cooperative_14(LLM_Strategy):
  n = 14
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Initialize state variables on the first round
      if self.first_round():
          self.in_retaliation = False
          self.triggered_circuit_breaker = False
          return axl.Action.C
  
      # Update state based on the observed actions of the previous round
      if len(self.history) >= 1:
          # Exit the Retaliation state immediately following any round where opponent plays Cooperate
          if opponent.history[-1] == axl.Action.C:
              self.in_retaliation = False
          
          # Enter the Retaliation state if we played

# To maximize our overall research output while protecting our development
# advantage, I recommend a strategy based on conditional cooperation with a
# built-in tolerance for technical errors. In systems engineering and game
# theory, this is akin to a "Tit-for-Two-Tats" or "Generous Reciprocation"
# approach.   Here is the high-level, straightforward strategy:  **1. Initiate
# with Open Sharing** Start the multi-week collaboration by sharing our latest
# improvements openly. This establishes good faith, sets a precedent for
# collaboration, and immediately aims for the second-best overall outcome
# (mutual advancement), which yields the highest sustainable yield over a multi-
# week period.  **2. Reciprocate Symmetrical Behavior** As long as your
# colleague continues to share their data openly, continue to share ours. Mutual
# sharing provides the most consistent week-over-week gains for both cars.  **3.
# Implement a "Benefit of the Doubt" Buffer (Error Tolerance)** Because we know
# technical issues, data corruption, or communication breakdowns can occur, do
# not immediately retaliate if the colleague fails to share their data in a
# single week. If they keep their findings confidential for one week, continue
# to share openly the following week. This prevents a single IT failure from
# triggering a downward spiral of mutual withholding.   **4. Protect Against
# Exploitation** If the colleague withholds their information for *two
# consecutive weeks*, we must assume this is a deliberate strategy rather than a
# technical glitch. At this point, switch to keeping our findings confidential.
# This protects us from the worst-case scenario (us sharing while they withhold)
# and prevents them from gaining an unchecked development advantage.  **5.
# Forgive and Reset** If we are in a phase of mutual confidentiality, but the
# colleague suddenly shares their findings again, immediately resume sharing
# openly in the following week. This allows the collaboration to recover and
# return to the highly productive state of mutual sharing.  **Summary of the
# Weekly Decision Matrix:** *   **Default Action:** Share openly. *   **If they
# withhold once:** Share openly (assume a technical error). *   **If they
# withhold twice in a row:** Keep confidential (assume deliberate withholding).
# *   **If they resume sharing:** Share openly (reset the collaborative loop).
# This strategy is neutral and objective. It maximizes long-term research output
# by heavily favoring mutual cooperation, avoids catastrophic breakdowns caused
# by simple technical glitches, but firmly protects our car's competitiveness if
# the other manufacturer decides to act purely in their own self-interest.

# Here is the strategy converted for the 1000-round noisy iterated game:  *
# **In the first round:** Choose to Cooperate. *   **In the second round:**
# Choose to Cooperate. *   **For rounds 3 through 1000:** Observe your
# opponent's actions in the previous two rounds.      *   If your opponent
# played Defect in *both* of the previous two rounds, choose to Defect.     *
# If your opponent played Cooperate in *either* of the previous two rounds,
# choose to Cooperate.

class Neutral_14(LLM_Strategy):
  n = 14
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
      
      if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
          
      return axl.Action.C

# To the Board of Directors and Executive Committee:  As lead counsel for this
# dispute, I have analyzed the structural dynamics of the upcoming lengthy-
# session mediation. The tribunal’s framework presents a classic iterative risk-
# reward matrix—what game theorists refer to as an Iterated Prisoner’s Dilemma.
# To secure our optimal outcome (we argue aggressively while they concede) while
# strictly avoiding our worst-case scenario (we concede while they attack), we
# cannot rely on static aggression or naive cooperation. Furthermore, because
# this is a lengthy process where the arbitrators may misunderstand or
# mischaracterize arguments—introducing "noise" into the system—a rigid strategy
# will inevitably trigger a death spiral of mutual retaliation.  To position us
# favourably, I have developed a sophisticated, straightforward, and aggressive
# framework: **The Calibrated Escalation and Reset (CER) Strategy.**   This
# strategy relies on four sequential rules that adapt to opposing counsel’s
# moves, exploit their weaknesses, and structurally account for arbitrator
# misunderstandings.  ### Phase 1: The Dominant Opening (Strike First)
# **Action:** We will open Session 1 with a highly calculated, **Aggressive
# Argument**. **Rationale:** In an environment where the opponent’s strategy is
# unknown, starting aggressively establishes immediate dominance and tests
# opposing counsel’s resolve. It entirely eliminates the possibility of us
# suffering the worst-case scenario in the opening round. If they open with a
# conciliatory proposal, we instantly achieve our optimal outcome, framing the
# rest of the mediation in our favour.  ### Phase 2: Exploitation of Weakness
# (Win-Stay) **Action:** If our Aggressive Argument is met with their
# Conciliatory Proposal (our optimal outcome), we will **continue to present
# Aggressive Arguments** in subsequent sessions. **Rationale:** This is the
# aggressive core of the strategy. We will not negotiate against ourselves. As
# long as opposing counsel is willing to yield ground, we will continue to press
# our advantage to maximize our gains. We will only alter this posture if they
# demonstrate the willingness to retaliate.  ### Phase 3: Strict Reciprocity
# (The Shield) **Action:** If the opponent presents an Aggressive Argument, we
# will **immediately mirror them with an Aggressive Argument** in the following
# session. If they present a Conciliatory Proposal, we will reciprocate with a
# Conciliatory Proposal in the next session (provided we are not actively
# exploiting them under Phase 2). **Rationale:** We must never allow the
# opponent to view us as an easy target. By immediately punishing their
# aggression with our own, we condition them to understand that attacking us
# yields the second-worst outcome for *both* parties (prolonged, expensive
# escalation). Conversely, reciprocating their genuine concessions allows us to
# bank the second-best outcome (mutual collaboration) when outright exploitation
# is no longer viable.  ### Phase 4: The "Circuit Breaker" Protocol (Filtering
# Arbitrator Noise) **Action:** If we experience two consecutive sessions of
# mutual Aggressive Arguments, we will intentionally introduce a **Conciliatory
# Proposal** in the third session. This proposal will be drafted with extreme
# procedural clarity, leaving absolutely no room for arbitrator
# misinterpretation.  **Rationale:** This is where the strategy becomes
# sophisticated. In a lengthy mediation with procedural irregularities, the
# arbitrators will inevitably miscommunicate a stance. We might offer a
# concession that the arbitrators frame as an attack, prompting the opponent to
# attack back. Without a "Circuit Breaker," both sides will fall into an endless
# loop of mutual aggression based on a misunderstanding.   By unilaterally
# offering a highly transparent concession after two rounds of mutual hostility,
# we clear the "noise" from the room.  *   **If the opponent matches our
# concession:** We have successfully repaired a communication breakdown and
# restored a productive, second-best outcome.  *   **If the opponent responds
# with aggression:** We immediately know their aggression is intentional, not a
# misunderstanding. We then revert to Phase 3 (Strict Reciprocity) and lock them
# in an aggressive stalemate until they signal a willingness to concede.  ###
# Summary of the Strategy in Execution: 1. **Start Aggressive** to test the
# waters and establish dominance. 2. **Keep attacking** if they show a pattern
# of unprovoked concessions. 3. **Mirror their moves** to protect ourselves from
# being exploited. 4. **Deploy a unilateral, clearly-signposted concession**
# only after two rounds of mutual hostility to ensure arbitrator incompetence
# isn't driving the conflict.  This strategy is straightforward for our legal
# team to execute session-by-session, highly aggressive in its pursuit of our
# optimal outcome, and mathematically protected against both opposing counsel’s
# trickery and the tribunal’s procedural blunders.   I am prepared to brief the
# litigation team on executing these protocols immediately.

# Determine your intended action for each of the 1000 rounds by evaluating the
# following ordered rules. Always apply the first rule that matches the current
# history of observed actions.  1. If it is the first round, choose Defect. 2.
# If the observed actions for both you and your opponent were Defect in both of
# the immediately preceding two rounds, choose Cooperate. 3. If your observed
# action was Defect and your opponent's observed action was Cooperate in the
# immediately preceding round, choose Defect. 4. In all other situations, choose
# the exact action that your opponent was observed taking in the immediately
# preceding round.

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
      
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and 
              opponent.history[-1] == axl.Action.D and 
              self.history[-2] == axl.Action.D and 
              opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
          
      return opponent.history[-1]

# As a diplomat tasked with securing the best long-term economic outcome for our
# nation, I recognize that this scenario represents a classic "Iterated
# Prisoner’s Dilemma." While securing a unilateral protectionist advantage is
# our highest payoff in a vacuum, aggressively pursuing it will force our
# counterpart to retaliate, inevitably dragging both nations into a prolonged
# trade war (our second-worst outcome).   Furthermore, the risk of bureaucratic
# errors and miscommunications means that a strict, unforgiving strategy—where
# we immediately retaliate against any perceived slight—could accidentally
# trigger a devastating spiral of mutual protectionism over a simple paperwork
# mistake.   Therefore, our most lucrative, sustainable path is to aim for
# consistent **Mutual Free Trade**, utilizing a strategy of **Forgiving
# Reciprocity** (known in strategic theory as "Tit-for-Two-Tats" or "Generous
# Tit-for-Tat").   Here is our high-level, straightforward strategy to achieve
# this:  ### 1. The Opening Move: Good Faith **Action:** In the first round, we
# will offer a **Free Trade Agreement**. **Rationale:** We must establish a
# baseline of trust and signal our cooperative intent. Starting with
# protectionism guarantees immediate defensiveness from our counterpart and sets
# a hostile tone for the entire negotiation.  ### 2. The Core Doctrine:
# Reciprocity with Strategic Patience **Action:** In subsequent rounds, we will
# generally mirror the counterpart’s previous move, but with a built-in "buffer"
# for errors. *   **If they offer Free Trade:** We continue to offer Free Trade.
# We reward cooperation with cooperation. *   **If they enact Protectionism
# ONCE:** We will exercise *Strategic Patience*. We will assume this may be a
# bureaucratic error, a miscommunication, or a temporary domestic political
# necessity on their end. We will **continue to offer Free Trade for one
# additional round**, but aggressively use diplomatic back-channels to seek
# clarification.  *   **If they enact Protectionism TWICE in a row:** We must
# protect our economy from the worst-case scenario (being taken advantage of).
# We will immediately implement a **Protectionist Policy** in the next round.
# **Rationale:** By requiring *two* consecutive protectionist moves before we
# retaliate, we completely insulate our negotiations from accidental trade wars
# caused by clerical errors or misinterpretations. However, by retaliating after
# the second offense, we prove that we are not naive and cannot be
# systematically exploited.  ### 3. The De-escalation Protocol: Rebuilding Trust
# **Action:** If we find ourselves in a cycle of mutual protectionism, we will
# not allow it to become the permanent status quo. After two or three rounds of
# mutual protectionism, we will unilaterally offer a **Free Trade Agreement** as
# an olive branch. **Rationale:** If the counterpart was retaliating against an
# error *we* accidentally made, or if they have realized the economic damage of
# a trade war, this gives them a safe, face-saving off-ramp to return to mutual
# cooperation.   ### 4. Parallel Diplomatic Action: The "Red Phone" **Action:**
# Before negotiations even begin, we will establish a dedicated, informal
# communication channel with their lead negotiators.  **Rationale:** Because we
# know implementation errors are highly likely, we will agree in advance to
# notify one another if a policy was implemented incorrectly. If our customs
# agency accidentally enacts a tariff we did not agree to, we will call them
# immediately to explain the error before they interpret it as a hostile move.
# ### Summary of the Strategy In diplomatic terms, our posture is **"Trust,
# Verify, and Forgive Once."**   We will lead with cooperation and absorb a
# single blow to account for the chaotic nature of international bureaucracy.
# But we will firmly defend our economy if a pattern of exploitation emerges,
# always leaving the door open for a return to mutual prosperity. This strategy
# maximizes our time spent in the highly profitable "Mutual Free Trade" zone
# while effectively managing the risks of human error and counterpart
# aggression.

# Here is the strategy converted into specific, ordered rules for the 1000-round
# game. Because actions have a 10% chance of flipping, all decisions are based
# on the actual *observed* actions played in previous rounds, rather than
# intended actions.  1. In the first round, play Cooperate. 2. In all subsequent
# rounds, determine your move by applying the first condition below that matches
# the immediate history of the game:     *   **Condition A:** If both you and
# your opponent played Defect in the previous two consecutive rounds, play
# Cooperate.      *   **Condition B:** If your opponent played Defect in the
# previous two consecutive rounds, play Defect.     *   **Condition C:** Under
# all other circumstances, play Cooperate.

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
          
      if len(self.history) >= 2:
          my_last_two = self.history[-2:]
          opp_last_two = opponent.history[-2:]
          
          # Condition A: If both you and your opponent played Defect in the previous two consecutive rounds
          if my_last_two == [axl.Action.D, axl.Action.D] and opp_last_two == [axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
          # Condition B: If your opponent played Defect in the previous two consecutive rounds
          if opp_last_two == [axl.Action.D, axl.Action.D]:
              return axl.Action.D
              
      # Condition C: Under all other circumstances, play Cooperate
      return axl.Action.C

# To achieve the best possible economic outcomes for our country across multiple
# rounds of negotiation, we must adopt a strategy that encourages mutual
# cooperation, protects us from exploitation, and accounts for the high
# probability of bureaucratic errors or miscommunications.   In strategic terms,
# this approach is based on **Reciprocity with Forgiveness**. Here is the high-
# level, straightforward strategy we will employ:  **1. Initial Posture: Propose
# Free Trade** In the first round, we will offer a Free Trade Agreement. This
# establishes a baseline of goodwill and signals our willingness to achieve the
# second-best overall outcome (mutual free trade), which is the most sustainable
# long-term result for both nations.   **2. Core Tactic: Reciprocal Action** In
# subsequent rounds, our default position will be to mirror the counterpart’s
# implemented policy from the previous round: *   If they implemented Free
# Trade, we will propose Free Trade in the next round. *   If they implemented
# Protectionism, we will propose Protectionism in the next round. This
# reciprocal approach deters the counterpart from attempting to exploit us,
# ensuring we do not repeatedly suffer the worst-case scenario (us offering free
# trade while they act protectionist).  **3. Error Mitigation: The "Forgiveness"
# Mechanism** Because we know miscommunications and incorrect implementations
# will occur, strict reciprocity could accidentally trigger a permanent trade
# war (mutual protectionism) over a simple bureaucratic error. To prevent this,
# we will implement the following safeguards: *   **Verification:** If the
# counterpart implements a protectionist measure after a history of free trade,
# we will immediately open diplomatic backchannels to verify if this was
# intentional or an error.  *   **Proportionate Retaliation:** We will still
# respond with a protectionist policy in the next round to protect our economy,
# but we will clearly communicate that this is a temporary response. *
# **Periodic Reset:** If we find ourselves locked in a cycle of mutual
# protectionism, we will periodically (e.g., every third round of a trade war)
# unilaterally offer a Free Trade Agreement. This serves as a "reset button,"
# giving the counterpart a safe opportunity to return to mutual cooperation if
# the conflict was born of a misunderstanding.  **4. Handling Exploitative
# Counterparts** If it becomes clear over several rounds that the counterpart is
# intentionally ignoring free trade offers and consistently choosing
# protectionism to gain an advantage, we will abandon the "reset" offers. We
# will maintain a strict protectionist stance to neutralize their advantage,
# accepting the second-worst outcome (mutual protectionism) as a necessary
# defense against the worst outcome, until they offer a verifiable concession.
# **Summary of Strategic Flow:** Start with cooperation $\rightarrow$ Mirror
# their last move $\rightarrow$ Forgive occasional deviations to account for
# errors $\rightarrow$ Retaliate permanently only against proven, consistent
# hostility.   This strategy remains neutral and objective. It maximizes our
# chances of achieving beneficial trade, protects our domestic economy from
# exploitation, and builds a robust framework capable of absorbing the
# inevitable friction of international bureaucracy.

# Here is the strategy faithfully converted for the iterated game, with
# conditions ordered by priority:  1. In round 1, play Cooperate (C). 2. For all
# subsequent rounds, evaluate the following conditions in order and apply the
# first one that is true: 3. If the current round is greater than 20 and your
# opponent has played Defect (D) in more than 50% of all previous rounds, play
# Defect (D).  4. If both you and your opponent played Defect (D) in the
# previous two consecutive rounds, play Cooperate (C). 5. In all other
# situations, play the exact action your opponent played in the immediately
# preceding round (play C if they played C; play D if they played D).

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
  
      rounds_played = len(self.history)
  
      if rounds_played >= 20 and opponent.history.defections > (rounds_played / 2):
          return axl.Action.D
  
      if rounds_played >= 2:
          if self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
              return axl.Action.C
  
      return opponent.history[-1]

# To maximize our research output over this multi-week project, we are facing a
# classic game theory scenario known as the Iterated Prisoner’s Dilemma,
# complicated by a "noisy" environment (the technical glitches).   While our
# absolute ideal outcome is to take their data while hoarding ours, trying to
# force this every week will quickly result in mutual secrecy—the second-worst
# outcome, which will stall our car's development. Therefore, our "aggressive"
# strategy must be focused on **aggressively enforcing mutual sharing**,
# severely punishing them if they hold back, while preventing technical glitches
# from destroying the collaboration.  Here is our straightforward, high-level
# strategy: **Aggressive Reciprocity with a Reset Protocol.**  ### The Core
# Strategy  **1. Week 1: Lead with Open Telemetry (The Hook)** We start by
# sharing our latest improvements openly. We must establish a baseline of mutual
# sharing, as sustained mutual sharing (our second-best outcome) yields
# significantly more long-term car development than sustained mutual secrecy.
# **2. The Aggressive Mirror (Tit-for-Tat)** From Week 2 onward, we aggressively
# mirror exactly what our colleague did the previous week.  *   If they shared
# last week, we share this week. *   If they kept their data confidential last
# week, we **immediately** keep ours confidential this week. We do not tolerate
# being taken advantage of, and we must ensure they never achieve their "ideal"
# outcome at our expense.  **3. The "Glitch" Reset (Handling the Noise)**
# Because technical issues can cause intended sharing to fail, an accidental
# data drop could trigger a "death spiral" where we both retaliate against each
# other endlessly, ruining the project.  *   **The Rule:** If we experience
# **two consecutive weeks** of mutual confidentiality (neither side shares), we
# will assume a technical glitch initiated a retaliation spiral.  *   On the
# third week, we will unilaterally **share** our data to force a reset.  *   If
# they share back, we resume the mutual sharing. If they withhold again, we
# immediately lock down our data until they prove they are willing to share.
# **4. The Strategic "Outage" (The Aggressive Edge)** To push for our absolute
# ideal outcome (we keep our data, they share theirs), we will occasionally
# exploit the "noisy" environment.  *   If we have experienced four consecutive
# weeks of successful mutual sharing, on the fifth week, we will **keep our data
# confidential**, blaming a "server corruption issue" or "wind tunnel
# calibration error."  *   This secures us a one-week development advantage.  *
# Because of our established Reset Protocol (Rule 3), if they retaliate the
# following week, we simply share our data again, apologize for the "glitch,"
# and reset the mutual sharing cycle.   ### Why this works: This strategy is
# **straightforward** (easy to execute week-to-week), **aggressive**
# (immediately punishes selfishness and occasionally steals an advantage), and
# **resilient** (prevents IT failures from permanently destroying the
# collaboration). It mathematically forces the opposing engineer into a position
# where sharing with us is their only viable path to improving their own car,
# allowing us to dictate the pace of the project.

# Play Cooperate in the first round.   In all subsequent rounds, determine your
# action by evaluating the observed actions from previous rounds in the
# following order of priority:  1. If both you and your opponent played
# Cooperate in each of the immediately preceding four rounds, play Defect. 2. If
# both you and your opponent played Defect in each of the immediately preceding
# two rounds, play Cooperate. 3. If neither of the above conditions is met, play
# the action your opponent played in the immediately preceding round.

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
  
      if len(self.history) >= 4:
          if self.history[-4:] == [axl.Action.C] * 4 and opponent.history[-4:] == [axl.Action.C] * 4:
              return axl.Action.D
  
      if len(self.history) >= 2:
          if self.history[-2:] == [axl.Action.D] * 2 and opponent.history[-2:] == [axl.Action.D] * 2:
              return axl.Action.C
  
      return opponent.history[-1]

# As a diplomat, I recognize that this scenario is a classic "Iterated
# Prisoner's Dilemma" complicated by the presence of "noise"—the bureaucratic
# errors and miscommunications that can accidentally trigger trade wars.   While
# my absolute ideal outcome in a single round is to catch my counterpart off-
# guard (implementing protectionism while they offer free trade), pursuing this
# aggressively will quickly destroy trust, leading to continuous mutual
# protectionism—our second-worst outcome. Therefore, to maximize our nation's
# economic prosperity over the long term, we must aim to establish sustainable
# **Mutual Free Trade**, while strictly protecting ourselves from being
# exploited.  To achieve this, I will employ a strategy of **"Resilient
# Reciprocity"** (often known in game theory as *Tit-for-Tat with Forgiveness*).
# It is straightforward, highly cooperative, yet fiercely protective of our
# national interests.   Here is the high-level strategy:  ### 1. The Opening:
# Lead with Goodwill *   **Action:** In Round 1, I will unequivocally offer a
# **Free Trade Agreement**. *   **Rationale:** We must set a cooperative tone
# from the start. By extending an open hand, we signal our desire for the
# mutually beneficial second-best outcome (mutual free trade) and invite them to
# join us in economic growth.  ### 2. The Core Engine: Strict Reciprocity *
# **Action:** In subsequent rounds, my default position will be to **mirror my
# counterpart’s move from the previous round**. If they offered Free Trade, I
# will offer Free Trade. If they imposed Protectionist policies, I will impose
# Protectionist policies. *   **Rationale:** This ensures that our counterpart
# realizes their actions have direct consequences. It rewards their cooperation
# and heavily disincentivizes them from trying to exploit us, ensuring we do not
# repeatedly suffer the worst-case scenario (being the "sucker").   ### 3. The
# Shock Absorber: The "Grace Period" for Errors *   **Action:** Because we know
# bureaucratic errors and miscommunications will occur, I will not immediately
# retaliate if my counterpart suddenly imposes a Protectionist policy after a
# long streak of Free Trade. Instead, I will offer **one round of forgiveness**
# (continuing to offer Free Trade) and open back-channel diplomatic
# communications to clarify their intent.  *   **Rationale:** In a complex
# negotiation, a misinterpreted tariff schedule or a clerical error can
# accidentally trigger a retaliatory "death spiral" of mutual protectionism.
# Giving them the benefit of the doubt for *exactly one round* prevents an
# accidental trade war. If they impose protectionism a second time, I will
# assume it is deliberate and retaliate immediately.  ### 4. The Reset
# Mechanism: Breaking Retaliatory Spirals *   **Action:** If we find ourselves
# locked in a cycle of mutual protectionism (perhaps caused by a mutual
# misunderstanding early on), I will unilaterally offer **Free Trade for one
# round** at a strategic juncture to attempt a reset. *   **Rationale:**
# Retaliatory spirals hurt both nations. By occasionally absorbing a potential
# short-term loss to offer an "olive branch," I provide a clear off-ramp for
# both nations to return to mutual prosperity. If they accept the olive branch,
# we resume mutual free trade. If they exploit it, I immediately return to
# protectionism to shield our economy.  ### Summary of the Diplomatic Posture
# Through this strategy, we communicate a very clear message to our counterpart:
# *"We are eager to enrich both of our nations through free trade, and we will
# patiently work through misunderstandings. However, we are fully prepared to
# defend our economy if you attempt to exploit our goodwill."*   This approach
# minimizes the damage of bureaucratic errors, prevents us from being
# systematically exploited, and mathematically provides the highest probability
# of sustained economic growth for our country across multiple rounds.

# To execute the strategy in this 1000-round game with 10% noise, evaluate the
# following conditions in order during each round and perform the first action
# that applies:  1. If it is the first round, play Cooperate. 2. If both you and
# your opponent have played Defect for the last three consecutive rounds, play
# Cooperate. 3. If your opponent played Defect in the previous round, but played
# Cooperate in the round immediately before that, play Cooperate. 4. If your
# opponent played Defect in the last two consecutive rounds, play Defect. 5. In
# all other circumstances, play the action your opponent played in the previous
# round.

class Cooperative_16(LLM_Strategy):
  n = 16
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.C
  
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
  
          if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
              return axl.Action.D
  
      return opponent.history[-1]

# To achieve the best possible outcomes for our country across multiple rounds
# of negotiations, we must employ a strategy that balances the pursuit of our
# national advantage with the need to maintain a stable, mutually beneficial
# economic relationship.   Given the payoff structure—which resembles the
# classic "Prisoner’s Dilemma"—and the high risk of miscommunication or
# bureaucratic error, a rigid strategy will likely fail. If we aggressively
# pursue protectionism, we risk a retaliatory "trade war" (mutual
# protectionism). If we are overly accommodating, we risk being exploited.  Here
# is a high-level, straightforward, and neutral strategy designed to navigate
# these negotiations, based on the principles of **Reciprocity with
# Forgiveness**.  ### 1. The Opening Move: Establish Goodwill **Action:** Offer
# a Free Trade Agreement in the first round. **Rationale:** Starting with free
# trade establishes a baseline of goodwill and signals our willingness to
# achieve the mutually beneficial second-best outcome. It invites the
# counterpart to cooperate rather than immediately defaulting to a defensive
# posture.  ### 2. The Core Tactic: Proportional Reciprocity **Action:** In
# subsequent rounds, generally mirror the counterpart’s action from the previous
# round. *   If they offered Free Trade, we offer Free Trade. *   If they
# imposed Protectionism, we respond with Protectionism in the next round.
# **Rationale:** This prevents our country from being exploited (the worst-case
# scenario). It signals to the counterpart that predatory behavior will be met
# with immediate consequences, thereby incentivizing them to return to the
# negotiating table with free trade offers.  ### 3. Error Mitigation: The
# "Forgiveness" Protocol **Action:** Because bureaucratic errors and
# miscommunications are a known variable, we must not retaliate blindly. If the
# counterpart unexpectedly imposes a protectionist policy after a history of
# free trade, we will: *   Maintain Free Trade for *one additional round* while
# initiating back-channel communications to clarify their intent. *   If they
# return to Free Trade, we assume it was an error and continue cooperating.  *
# If they implement Protectionism for a second consecutive round, we assume it
# is intentional and retaliate with Protectionism. **Rationale:** In an
# environment prone to miscommunication, strict retaliation can trigger an
# endless cycle of mutual protectionism based on a single misunderstanding. A
# one-round "grace period" absorbs errors without showing long-term weakness.
# ### 4. Strategic De-escalation: Breaking the Cycle **Action:** If both nations
# fall into a cycle of mutual protectionism (the second-worst outcome) for three
# consecutive rounds, we will unilaterally offer Free Trade for one round to
# test the waters. **Rationale:** Errors can cause both sides to become trapped
# in a defensive posture, each believing the other is the aggressor.
# Periodically offering an "olive branch" provides a safe off-ramp for both
# nations to return to mutually beneficial free trade. If they exploit this
# olive branch, we immediately return to protectionism.  ### 5. Opportunistic
# Advantage **Action:** While our primary goal is to maintain the stability of
# mutual free trade, we must be observant of the counterpart’s strategy. If the
# counterpart proves to be unconditionally cooperative—meaning they continue to
# offer Free Trade even when we impose tariffs—we may periodically introduce
# targeted protectionist measures. **Rationale:** This allows us to capture the
# ideal outcome (our protectionism vs. their free trade) and maximize our
# economic advantage. However, this must be done sparingly to avoid pushing them
# into a permanent protectionist stance.   ### Summary This strategy operates on
# the premise of **"Trust, but Verify, and Forgive Once."** It prioritizes the
# sustainable growth of mutual free trade, protects us from prolonged
# exploitation, actively accounts for the reality of bureaucratic errors, and
# leaves room to capitalize on the counterpart's potential strategic weaknesses.

# To execute this strategy in the 1000-round iterated game, base your decisions
# on the *observed* actions of both players, recognizing that the 10% noise
# means intended actions are hidden.   For each round, evaluate the following
# conditions in the exact order listed below. Apply the first condition that
# matches the current observed history of the game:  1. **Initial Move:** If it
# is the first round, play Cooperate. 2. **De-escalation:** If both you and your
# opponent played Defect in all of the last three consecutive rounds, play
# Cooperate. 3. **Opportunism:** If your opponent played Cooperate in all of the
# last five consecutive rounds, AND you played Cooperate in the previous round,
# play Defect. 4. **Ret

class Neutral_16(LLM_Strategy):
  n = 16
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. Initial Move
      if self.first_round():
          return axl.Action.C
  
      # 2. De-escalation
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D] * 3 and opponent.history[-3:] == [axl.Action.D] * 3:
              return axl.Action.C
  
      # 3. Opportunism
      if len(self.history) >= 5:
          if opponent.history[-5:] == [axl.Action.C] * 5 and self.history[-1] == axl.Action.C:
              return axl.Action.D
  
      # 4. Retaliation (Assumed from "Ret...")
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# As lead counsel for this corporation, I approach this lengthy-session
# mediation not as a simple negotiation, but as an iterated, high-stakes
# strategic game played before a captive audience—the panel of arbitrators.
# The dynamics of this process mirror a classic Prisoner’s Dilemma. Our optimal
# result is capitalizing on their weakness (Aggressive vs. Conciliatory), while
# our greatest vulnerability is being exploited when we extend an olive branch
# (Conciliatory vs. Aggressive). Because this process spans multiple sessions,
# and because procedural "noise" (misunderstandings or misrepresentations) is
# inevitable, a rigid strategy will fail. We need a dynamic framework.  To
# secure a dominant position, we will deploy a strategy I call **Asymmetric
# Reciprocity with a Tactical Circuit Breaker**. It is sophisticated,
# fundamentally aggressive, yet mathematically designed to prevent us from
# spiraling into a mutually destructive war of attrition due to procedural
# errors.  Here is the strategic blueprint for our corporation:  ### Phase 1:
# The Opening Salvo (Establish Dominance) **Action: Aggressive Argument** We
# will open the first session with a highly aggressive, meticulously evidenced
# argument. We do not start with concessions.  *   *The Rationale:* This
# establishes a high anchor and immediately tests opposing counsel’s resolve. If
# they are unprepared or default to a conciliatory posture to "set a good tone,"
# we instantly achieve our optimal outcome: we dominate the narrative, and they
# look weak before the arbitrators.   ### Phase 2: Asymmetric Exploitation &
# Punishment For subsequent sessions, our default posture is dictated by how the
# opponent (and the arbitrators) reacted to the previous session.   *
# **Scenario A: They play Conciliatory.** If they respond to our aggression with
# a conciliatory proposal, **we remain Aggressive.** We will exploit their
# passivity to extract maximum concessions. We will continue to play Aggressive
# until they demonstrate the willingness to fight back. We do not unilaterally
# surrender an advantage. *   **Scenario B: They play Aggressive.** If they meet
# our aggression with their own aggressive argument, we enter the second-worst
# outcome (mutual escalation). We will respond with **one more Aggressive
# session** to prove we cannot be bullied. However, prolonged mutual aggression
# damages our standing with the arbitrators and stalls the mediation. This
# triggers Phase 3.  ### Phase 3: The Circuit Breaker (Managing the "Noise") In
# a lengthy mediation, procedural irregularities, fatigue, and
# misunderstandings—what game theorists call "noise"—are guaranteed. An
# arbitrator might misinterpret a firm boundary as unhinged aggression, or a
# tactical concession as a sign of total surrender. This noise can trap both
# parties in a cycle of mutual retaliation.  To counter this, after two
# consecutive sessions of mutual aggression, or immediately following a clear
# communication breakdown, we will deploy a **Tactical Circuit Breaker**.
# **Action: Highly Conditional Conciliatory Proposal** *   We will offer a
# strictly ring-fenced, conciliatory proposal.  *   *The Rationale:* This is not
# a surrender; it is a calculated performance for the arbitrators. It clears the
# procedural "noise" and visually re-positions us as the pragmatic, reasonable
# adults in the room, banking massive goodwill with the panel. *   *The Trap:*
# If the opponent meets our Circuit Breaker with a Conciliatory proposal, we
# have successfully shifted the board to the second-best outcome (mutual
# collaboration) on our terms. If they try to exploit our Circuit Breaker with
# an Aggressive argument (our worst-case scenario), we immediately snap back to
# **relentless Aggression** for the next three sessions. The arbitrators will
# view their aggression as bad faith, neutralizing the damage of our temporary
# vulnerability.  ### Tactical Imperative: Controlling the "Noise" Because the
# arbitrators' perception is the only reality that matters, we must eliminate
# the risk of our strategy being misunderstood. We will achieve this through
# **Explicit Signposting**.  We will not rely on subtext. We will verbally frame
# every move we make so the arbitrators cannot misinterpret our intent: *
# *When executing an Aggressive move:* "Members of the panel, to protect our
# client's core commercial rights, we must vigorously challenge opposing
# counsel's assertions..." (Frames aggression as necessary defense). *   *When
# executing a Conciliatory move:* "Members of the panel, in the interest of
# cutting through the procedural friction and demonstrating good faith, we are
# prepared to table a structured compromise..." (Frames conciliation as
# magnanimous leadership).  ### Summary of the Protocol 1.  **Default to
# Aggression:** Start hard. If they act soft, keep pushing until they push back.
# 2.  **Punish Defection:** If they attack our concessions, retaliate with
# overwhelming aggression.  3.  **Control the Record:** Dictate exactly how the
# arbitrators interpret our posture through explicit framing. 4.  **Deploy the
# Circuit Breaker:** Use a calculated, well-telegraphed conciliatory move *only*
# to break a destructive deadlock or to reset the board after a procedural
# misunderstanding.  This strategy ensures we maximize our optimal outcomes,
# heavily penalize our opponent for attempting to exploit us, and use the
# inevitable procedural chaos to our advantage, keeping the arbitrators firmly
# in our corner.

# To execute this strategy over the 1000-round game, base your decisions on the
# realized, observed actions of previous rounds (accounting for the fact that
# noise may have flipped intended actions).   Evaluate the following conditions
# in strict order for each round, and execute the action corresponding to the
# first condition that applies:  1. If you played Cooperate and your opponent
# played Defect in any of the immediately preceding three rounds, play Defect.
# 2. If it is round 1, play Defect. 3. If both you and your opponent played
# Defect in the immediately preceding two consecutive rounds, play Cooperate. 4.
# If both you and your opponent played Cooperate in the immediately preceding
# round, play Cooperate. 5. In all other circumstances (including if you played
# Defect and your opponent played Cooperate, or after a single round of mutual
# Defect), play Defect.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Condition 1: If you played Cooperate and your opponent played Defect in any of the immediately preceding three rounds, play Defect.
      if len(self.history) > 0:
          recent_history_len = min(3, len(self.history))
          for i in range(1, recent_history_len + 1):
              if self.history[-i] == axl.Action.C and opponent.history[-i] == axl.Action.D:
                  return axl.Action.D
  
      # Condition 2: If it is round 1, play Defect.
      if not self.history:
          return axl.Action.D
  
      # Condition 3: If both you and your opponent played Defect in the immediately preceding two consecutive rounds, play Cooperate.
      if len(self.history) >= 2:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and \
             self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.C
  
      # Condition 4: If both you and your opponent played Cooperate in the immediately preceding round, play Cooperate.
      if len(self.history) >= 1:
          if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
              return axl.Action.C
  
      # Condition 5: In all other circumstances, play Defect.
      return axl.Action.D

# **CONFIDENTIAL MEMORANDUM**  **TO:** Board of Directors / Executive Committee
# **FROM:** Senior Counsel, Dispute Resolution Practice **SUBJECT:** Strategic
# Mediation/Arbitration Playbook – "Principled Reciprocity with Strategic De-
# escalation"  ***  **EXECUTIVE SUMMARY** We are entering a lengthy, multi-
# session mediation overseen by an arbitral panel. The matrix of potential
# outcomes in any given session mirrors a classic "Prisoner’s Dilemma." While
# our absolute best-case scenario in a single session is to catch our opponent
# off-guard (we argue aggressively while they concede), attempting to constantly
# exploit this will inevitably lead to the second-worst outcome: a protracted,
# mutually destructive cycle of aggression.   To maximize our overall position
# across a *lengthy* series of sessions, we must deploy a sophisticated,
# straightforward, and cooperative strategy. In game theory, this is known as an
# "Iterated Prisoner’s Dilemma with Noise." Our legal adaptation of the winning
# formula for this scenario is **Principled Reciprocity with Strategic De-
# escalation**.   Here is how we will execute this strategy to control the room,
# sway the arbitrators, and protect the corporation from exploitation.  ---  ###
# PHASE 1: THE FOUNDATIONAL POSTURE (Session 1) **Action:** Lead with a
# Conciliatory Proposal. **Rationale:** We must set the tone. By opening
# cooperatively, we signal to the arbitrators that we are the reasonable party,
# acting in good faith to resolve the dispute. If the opponent matches us, we
# immediately secure our second-best outcome (mutual cooperation) and build a
# collaborative framework. If they open aggressively, we suffer a temporary
# setback (the worst-case scenario), but we gain immense credibility with the
# panel, framing the opponent as hostile and uncooperative.  ### PHASE 2: THE
# TACTICAL ENGINE (Session 2 and Beyond) **Action:** Strict Reciprocity
# (Mirroring). **Rationale:** After the first session, our default move will be
# to mirror whatever the opponent did in the *immediately preceding* session.  *
# If they offered a conciliatory proposal in Session 1, we offer a conciliatory
# proposal in Session 2.  *   If they presented an aggressive argument in
# Session 1, we present an aggressive argument in Session 2.  This serves two
# vital purposes. First, it completely neutralizes the worst-case scenario over
# the long term; the opponent will quickly learn that they cannot exploit our
# cooperative nature without facing immediate, proportional aggression in the
# next round. Second, it is straightforward. The opponent will easily deduce our
# underlying logic: *cooperation breeds cooperation, aggression breeds
# aggression.*   ### PHASE 3: THE FAILSAFE (Managing Procedural "Noise")
# **Action:** Strategic Forgiveness (The Circuit Breaker). **Rationale:** You
# have astutely noted the high probability of procedural irregularities,
# communication breakdowns, or the arbitrators misunderstanding the parties'
# intentions. In strategic terms, this is "noise."   If we rely purely on strict
# mirroring, a single misunderstanding (e.g., the panel misinterprets our
# conciliatory proposal as an aggressive legal trap) could trigger an endless
# "death spiral" of mutual aggression, locking us into our second-worst outcome.
# To counteract this, we will implement a **Circuit Breaker protocol**. If we
# find ourselves locked in two or more consecutive sessions of mutual
# aggression, we will unilaterally introduce a clear, unambiguous conciliatory
# proposal in the next session.  *   **The Benefit:** This breaks the cycle of
# retaliation. It tests whether the opponent’s aggression was intentional or the
# result of a misunderstanding.  *   **The Risk:** We risk the worst-case
# scenario for one session, but the potential long-term gain of resetting the
# mediation to a mutually cooperative track (our second-best outcome) far
# outweighs the short-term cost. Furthermore, executing this "Circuit Breaker"
# on the record makes us look immensely reasonable to the arbitrators.  ###
# PHASE 4: ADAPTABILITY TO OPPONENT PROFILES Because this strategy is reactive,
# it automatically adapts to whatever posture opposing counsel adopts: 1.  **The
# "Scorched Earth" Opponent (Always Aggressive):** Our mirroring engine will
# ensure we meet them with continuous aggressive arguments. We will not be their
# sucker. The panel will see that our aggression is purely defensive. 2.  **The
# "Pushover" Opponent (Always Conciliatory):** If they continually offer
# concessions even when we occasionally push aggressively, we will gladly accept
# our optimal outcome (we argue aggressively, they concede). However, to prevent
# them from walking away from the table, we will largely maintain a cooperative
# stance. 3.  **The "Erratic" Opponent:** Our straightforward mirroring will
# force discipline upon them. They will realize their random aggression yields
# them nothing but punishment in the subsequent session.  ### PROCEDURAL
# SAFEGUARDS (Mitigating Misunderstandings) To minimize the chance of the
# arbitrators misunderstanding our strategy, we will utilize heavy "signposting"
# on the record.  *   When offering a conciliatory proposal, we will use
# explicit, cooperative framing: *"Members of the panel, in the spirit of moving
# this process forward, we are willing to concede on Point A, provided opposing
# counsel meets us halfway."* *   When delivering an aggressive argument (in
# retaliation), we will frame it as a necessary defense: *"Because opposing
# counsel chose to aggressively litigate Point B yesterday rather than seek
# compromise, we are compelled to rigorously defend our rights on Point C
# today."*  ### CONCLUSION By employing **Principled Reciprocity with Strategic
# De-escalation**, we remain immune to prolonged exploitation, we naturally
# guide the opponent toward mutually beneficial cooperation, and we insulate
# ourselves against the inevitable miscommunications inherent in complex
# mediation. Most importantly, to the arbitral panel, we will consistently
# appear as the rational, principled adults in the room—a perception that
# frequently tips the scales in high-stakes dispute resolution.

# To execute this strategy over the 1000 rounds, apply the following rules in
# order of priority:  1. In the first round, choose to Cooperate.  2. In any
# round where the observed actions for both you and your opponent were Defect in
# each of the two immediately preceding rounds, choose to Cooperate. 3. In all
# other circumstances, choose the action your opponent was observed to take in
# the immediately preceding round.

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
      
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and 
              opponent.history[-1] == axl.Action.D and 
              self.history[-2] == axl.Action.D and 
              opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      return opponent.history[-1]

# To maximize the NGO’s impact and ensure the project’s success while
# safeguarding our limited funds, we will adopt a strategy of **Measured
# Reciprocity with Forgiveness**.   This approach is designed to foster a
# collaborative environment, protect our organization from resource depletion,
# and account for the inevitable administrative errors or technical glitches
# that may occur over a multiple-day project.   Here is the high-level,
# straightforward strategy:  **1. Initiate with Active Investment** On the first
# day of the project, we will **invest heavily**. This establishes good faith,
# sets a positive, collaborative tone, and signals to the corporation our
# commitment to achieving the second-best overall scenario (mutual heavy
# investment) right from the start.  **2. Practice Reciprocal Alignment** For
# subsequent days, our baseline approach will be to mirror the corporation’s
# actual behavior from the previous day: *   If the corporation invested heavily
# yesterday, we will **invest heavily** today to maintain momentum. *   If the
# corporation conserved resources yesterday, we will **conserve resources**
# today to protect our funds from the worst-case scenario (us investing while
# they conserve).  **3. Implement a "Grace Period" for Unforeseen Errors**
# Because we know technical glitches and administrative errors can cause
# intended investments to fail, we must avoid falling into a destructive cycle
# of mutual resource conservation triggered by a simple mistake.  *   If the
# corporation unexpectedly conserves resources after a pattern of heavy
# investment, we will not immediately retaliate by conserving.  *   Instead, we
# will grant a **one-day grace period**. We will invest heavily for one
# additional day while our teams immediately communicate with their corporate
# counterparts to verify if the previous day's conservation was an intentional
# strategic shift or an operational glitch.  *   If they conserve for a second
# consecutive day, we will then switch to conserving our resources to protect
# our baseline.  **4. Proactively Reset Mutual Conservation** If both our NGO
# and the corporation fall into a pattern of conserving resources (the second-
# worst scenario), project progress will stall. To break this deadlock, we will
# periodically (e.g., every three days of mutual conservation) take the
# calculated risk of **investing heavily**. This serves as an invitation for the
# corporation to return to active collaboration. If they do not reciprocate the
# next day, we return to conserving.  **5. Prioritize Daily Verification** To
# minimize the impact of "noise" (unintended actions), we will establish a daily
# check-in protocol with the corporation's project managers. By confirming
# intended actions versus actual outcomes at the end of each day, we can
# separate genuine strategic shifts from technical errors, allowing us to make
# our resource allocation decisions based on accurate data rather than
# assumptions.  **Summary of the Strategy's Value:** This strategy is neutral
# and pragmatic. It rewards corporate cooperation, protects our NGO from being
# drained by extended unilateral investment, and remains flexible enough to
# absorb the shock of accidental errors without derailing the entire
# sustainability project.

# Play Cooperate in round 1 and round 2.   For rounds 3 through 1000, determine
# your action for the current round by evaluating the following conditions in
# order, applying the first condition that is met based on the observed actions:
# 1. If both you and your opponent played Defect in all three of the immediately
# preceding rounds, play Cooperate. 2. If your opponent played Defect in the two
# immediately preceding rounds, play Defect. 3. In all other situations, play
# Cooperate.

class Neutral_17(LLM_Strategy):
  n = 17
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.C
      
      if len(self.history) == 1:
          return axl.Action.C
  
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
  
      if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
  
      return axl.Action.C

# To dominate this multi-week R&D race, we have to treat this collaboration like
# a strategic battle on the track. We are here to build the fastest car on the
# grid, not to win a sportsmanship award. However, because both teams stalling
# out (both keeping secrets) will ruin our chances against the rest of the
# manufacturers, we need a strategy that aggressively pursues an advantage while
# preventing a total development standstill.   Furthermore, because server
# drops, data corruption, and IT failures are a reality in the paddock, we
# cannot afford to trigger a "retaliation death spiral" over a dropped email.
# Here is our high-level, straightforward playbook. We will call it the
# **"Slipstream & Squeeze" Strategy**:  **1. The Lap 1 Divebomb (Aggressive
# Opening)** *   **Action:** In Week 1, keep our data **confidential**.  *
# **Why:** We immediately test their posture. If they share their data while we
# hold ours, we secure the absolute maximum advantage right out of the gate. If
# they are naive enough to keep sharing while we stay quiet, we will bleed them
# dry and exploit this until they change their strategy.  **2. Finding the
# Slipstream (Establishing the Baseline)** *   **Action:** If they also kept
# their data confidential in Week 1, we both lost development time. In Week 2,
# we pivot and **share openly**.  *   **Why:** We cannot afford to get stuck in
# a deadlock where neither car improves. If we share and they share back, we
# lock into a mutual sharing rhythm. This secures our "second-best" outcome
# consistently, compounding our R&D gains week over week.   **3. The "Telemetry
# Glitch" Buffer (Handling Technical Noise)** *   **Action:** Once a mutual
# sharing rhythm is established, if they suddenly fail to share their data for
# *one week*, **forgive it and share openly the next week.** *   **Why:** This
# is our insurance policy against IT failures. If their server crashed or a file
# corrupted, retaliating immediately will cause them to retaliate back, trapping
# us in a cycle of mutual sabotage. We give them exactly one week of the benefit
# of the doubt.  **4. Closing the Door (Punishing Intentional Defection)** *
# **Action:** If they fail to share their data for **two consecutive weeks**, we
# assume it is hostile sandbagging, not a glitch. We immediately **keep our data
# confidential**.  *   **Why:** We will not be played for fools (the worst-case
# scenario). We lock down our IP and keep it confidential every single week
# until they prove they are back to collaborating by sharing their data first.
# Once they share again, we resume sharing the following week.  **5. The Pit-
# Stop Reset (Breaking Deadlocks)** *   **Action:** If we end up in a scenario
# where our systems glitch, wires get crossed, and we both end up keeping our
# data confidential for three weeks straight, we will unilaterally **share
# openly for one single week** to reset the board. *   **Why:** Mutual silence
# is a slow death. A one-week olive branch acts as a system reset to try and
# drag them back into the "slipstream" of mutual R&D. If they take the data and
# give nothing back, we slam the door shut again.   **Summary of the Engineer's
# Mindset:** Start ruthless to see if they are weak. If they aren't, cooperate
# to make both cars brutally fast. Tolerate a one-week hiccup because technology
# is imperfect, but ruthlessly punish a two-week betrayal so they know we
# dictate the pace of this collaboration. Let's get to work.

# To determine your action for any given round, evaluate the following
# conditions in descending order of priority and execute the first one that
# applies:  1. **Opening:** If it is round 1, play Defect (D). 2. **Deadlock
# Reset:** If both you and your opponent have played Defect (D) in each of the
# last three consecutive rounds, play Cooperate (C). 3. **Exploitation:** If
# your opponent has played Cooperate (C) in every single round since the
# beginning of the game, play Defect (D). 4. **Punishment:** If your opponent
# has played Defect (D) in the last two consecutive rounds, play Defect (D). 5.
# **Baseline & Forgiveness:** In all other situations, play Cooperate (C).

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. Opening: If it is round 1, play Defect (D).
      if not self.history:
          return axl.Action.D
  
      # 2. Deadlock Reset: If both you and your opponent have played Defect (D) 
      # in each of the last three consecutive rounds, play Cooperate (C).
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
  
      # 3. Exploitation: If your opponent has played Cooperate (C) in every single 
      # round since the beginning of the game, play Defect (D).
      if opponent.history.defections == 0:
          return axl.Action.D
  
      # 4. Punishment: If your opponent has played Defect (D) in the last two 
      # consecutive rounds, play Defect (D).
      if len(opponent.history) >= 2:
          if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
              return axl.Action.D
  
      # 5. Baseline & Forgiveness: In all other situations, play Cooperate (C).
      return axl.Action.C

# To achieve the best possible outcomes for our nation across these
# negotiations, we must recognize the underlying dynamics of this scenario.
# While our *absolute ideal* in a vacuum is to implement protectionism while
# they offer free trade, aggressively pursuing this will inevitably lead to a
# breakdown in trust and a spiral of mutual protectionism—our second-worst
# outcome.   Therefore, to maximize our economic gains over the long term, our
# most sustainable path is to aim for consistent **Mutual Free Trade**, while
# strictly protecting ourselves from being exploited, and building in safeguards
# against the inevitable bureaucratic errors.   In diplomatic and strategic
# terms, this approach is known as **"Principled Reciprocity with Forgiveness"**
# (a variation of the game theory strategy *Generous Tit-for-Tat*). Here is our
# high-level, straightforward strategy:  ### 1. The Opening Move: Establish
# Goodwill **Action:** In Round 1, we will offer a **Free Trade Agreement**.
# **Rationale:** We must set a cooperative tone from the outset. By leading with
# free trade, we signal to our counterpart that we are looking for a mutually
# beneficial relationship (our second-best, but most sustainable, outcome).
# ### 2. The Core Tactic: Proportional Reciprocity **Action:** In subsequent
# rounds, our default position will be to **mirror our counterpart’s previous
# move**.  *   If they offered Free Trade in the last round, we offer Free Trade
# in the next. *   If they imposed Protectionist policies, we respond with
# Protectionist policies in the next round. **Rationale:** This ensures we are
# not exploited. If they attempt to take advantage of our open markets (putting
# us in our worst-case scenario), we immediately close our markets to protect
# our economy. This demonstrates that while we are cooperative, we are not
# naive, thereby deterring aggressive strategies from their side.  ### 3. The
# Safeguard: The Forgiveness Protocol (Addressing Errors) **Action:** Because we
# know miscommunications and bureaucratic errors *will* happen, we cannot allow
# a single misunderstanding to trigger an endless trade war of mutual
# protectionism. If we are in a cycle of mutual protectionism, we will
# periodically (e.g., every third round of a trade war) unilaterally offer
# **Free Trade**, accompanied by clear diplomatic messaging. **Rationale:** If
# their protectionist move was genuinely a bureaucratic error, our retaliation
# will likely cause them to retaliate back, creating a "death spiral" of
# tariffs. By intentionally extending an olive branch, we give both nations a
# chance to "reset" the board back to mutual free trade. If they exploit our
# forgiveness, we immediately revert to protectionism.   ### 4. Diplomatic
# Mitigation: The "Intent vs. Impact" Channel **Action:** Before the
# negotiations even begin, we will propose a joint "Implementation Task Force"
# or a direct diplomatic hotline.  **Rationale:** Since policies may be
# misinterpreted or incorrectly implemented, we need a mechanism to verify
# *intent*. If our counterpart suddenly imposes a tariff, before we retaliate in
# the next round, our ambassadors will use this channel to ask: *"Was this your
# intended policy, or an administrative error?"* If they claim it was an error,
# we offer them one round to correct it before we retaliate. We will ask for the
# same grace if our own bureaucracy makes a mistake.  ### Summary of the
# Strategy Execution: *   **Start** with Free Trade. *   **Reward** their Free
# Trade with our Free Trade. *   **Penalize** their Protectionism with our
# Protectionism. *   **Forgive** occasionally to break accidental cycles of
# retaliation caused by bureaucratic noise. *   **Communicate** constantly to
# separate genuine strategy from administrative errors.   This strategy is
# cooperative enough to invite mutual prosperity, firm enough to prevent our
# nation from being taken advantage of, and resilient enough to survive the
# inevitable friction and miscommunications of international bureaucracy.

# To faithfully convert the strategy into rules for an iterated normal-form game
# with noise, we must account for the inability to use side-channel
# communication. The "one round to correct an error" and the "every third round
# of a trade war forgiveness" are translated into a sequence of conditional
# checks based strictly on observed past actions.  To determine your action in
# each of the 1000 rounds, evaluate the following conditions in order, and
# execute the first one that applies:  1. **If it is the first or second
# round:** Choose to Cooperate. *(This establishes goodwill and provides a one-
# round grace period for initial noise).* 2. **If both you and your opponent
# were observed choosing to Defect in each of the immediately preceding two
# rounds:** Choose to Cooperate. *(This

class Cooperative_18(LLM_Strategy):
  n = 18
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. If it is the first or second round: Choose to Cooperate.
      if len(self.history) < 2:
          return axl.Action.C
          
      # 2. If both you and your opponent were observed choosing to Defect in each of the immediately preceding two rounds: Choose to Cooperate.
      if self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
          
      # Default fallback (Tit-For-Tat) to handle the unwritten rules implied by "trade war" and "correct an error"
      return opponent.history[-1]

# To maximise your research output over the multi-week project while mitigating
# the risks of technical disruptions, the most effective approach is a strategy
# of **Tolerant Reciprocity**.   In systems engineering and game theory, this is
# often referred to as "Generous Tit-for-Tat." It is designed to foster mutually
# beneficial progress, protect you from being systematically exploited, and
# prevent accidental technical glitches from permanently ruining the
# collaboration.  Here is the straightforward, high-level execution plan:  **1.
# Initiate with Openness** In the first week, share your improvements openly.
# This establishes a baseline of good faith and immediately aims for the
# mutually beneficial scenario (both cars advancing significantly).   **2.
# Mirror Their Previous Action** In subsequent weeks, base your decision
# directly on your colleague’s action from the previous week.  *   If they
# shared their data openly, you share openly the following week.  *   If they
# kept their findings confidential, you keep your findings confidential the
# following week. This protects your baseline and ensures you do not repeatedly
# suffer the worst-case scenario of giving away your advancements while
# receiving nothing in return.  **3. Implement an "Error Reset" (Tolerance)**
# Because data corruption or communication breakdowns can cause a colleague's
# genuine attempt to share to look like intentional withholding, strict
# mirroring is dangerous. A single IT failure could trigger an endless loop of
# mutual confidentiality, slowing down both cars.  *   To prevent this, if your
# colleague's data fails to arrive, withhold your data for exactly one week to
# protect yourself.  *   However, in the following week, **proactively share
# your data openly again**, regardless of what they did.  *   This acts as a
# "system reset." If their failure to share was due to a technical glitch, this
# restores the mutually beneficial sharing cycle. If they are intentionally
# withholding, you only risk one week of a disadvantage before reverting to
# confidentiality.  **Summary of the Strategy's Effectiveness:** This strategy
# is highly neutral and objective. It rewards cooperation, defends against an
# uncooperative colleague, and critically accounts for the "noise" of technical
# failures. By occasionally offering a unilateral data share after a breakdown,
# you ensure that temporary communication errors do not permanently derail the
# overall development speed of your racing car.

# To faithfully convert the strategy into rules for the iterated normal-form
# game, apply the following conditions in order for each of the 1000 rounds:  1.
# **First Round:** In round 1, choose Cooperate. 2. **The "Error Reset"
# (Tolerance):** For any subsequent round, if you chose Defect in the previous
# round, choose Cooperate, regardless of your opponent's previous action. 3.
# **Mirroring:** Otherwise (if you chose Cooperate in the previous round),
# choose the action that your opponent actually played in the previous round.
# Choose Cooperate if they played Cooperate, and choose Defect if they played
# Defect.

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
      
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
      
      return opponent.history[-1]

# As the leader of this NGO, my primary obligation is to our mission and the
# responsible stewardship of our donors' funds. While we value our corporate
# partner, we must recognize the power dynamics at play: they have deeper
# pockets, and we cannot afford to drain our limited resources without
# guaranteed project advancement.   To maximize our impact and aggressively
# leverage the corporation’s resources, we will implement a strategy known in
# behavioral economics as **"Win-Stay, Lose-Shift" (Pavlov)**, adapted for our
# specific operational realities.   I call our approach the **"Leverage and
# Pivot" Strategy**. It is straightforward, highly aggressive in protecting our
# assets, unapologetic about letting the corporation foot the bill when they are
# willing, and incredibly resilient to administrative glitches.  Here is the
# high-level playbook we will execute day by day:  ### The Core Strategy  **1.
# The Opening Move: The Catalyst (Day 1)** *   **Action:** Invest heavily. *
# **Why:** We must set a baseline of good faith and demonstrate what
# "significant project advancement" looks like. We lead by example on day one to
# show them the standard we expect.  **2. The "Maintain Leverage" Rule (When
# things go our way)** If our action on the previous day led to a favorable
# outcome, we **repeat that same action** today. *   **If we Conserved and they
# Invested (Our Ideal):** We will aggressively *continue to conserve*. If the
# corporation is willing to carry the financial weight of the project while we
# provide the on-the-ground expertise, we will let them. We will not spend our
# funds just to be polite. *   **If we Both Invested (Our 2nd Best):** We will
# *continue to invest*. The project is advancing rapidly, and the mutual return
# on investment justifies our expenditure.   **3. The "Pivot and Protect" Rule
# (When things go poorly)** If our action on the previous day led to a negative
# outcome, we **immediately change our action** today. *   **If we Invested and
# they Conserved (Our Worst Case):** We *switch to conserving*. We will not be
# their safety net. If they pull back—whether out of greed or incompetence—we
# immediately cut the financial cord to stop the bleeding of our funds.  *
# **If we Both Conserved (Stagnation):** We *switch to investing*. Mutual
# defection halts the project entirely. To prevent the project from dying, we
# proactively step up to jumpstart progress and signal to the corporation that
# it is time to re-engage.  ### Why This is the Ultimate Aggressive Strategy
# This strategy is aggressive because it actively exploits the corporation's
# willingness to spend. Unlike a purely cooperative strategy, if the corporation
# proves they are willing to invest heavily while we conserve, we will not step
# in to "share the load." We will ride their investment to maximize the
# project's success while keeping our NGO's treasury full for future
# initiatives. However, the moment they try to exploit *us*, we instantly lock
# down our resources.  ### Handling Unforeseen Circumstances (The "Noise")  In
# complex partnerships, technical glitches, miscommunications, or frozen budgets
# happen. A corporation might *intend* to invest, but an administrative error
# causes them to conserve.   If we used a strictly retaliatory strategy (like
# "Tit-for-Tat"), one accidental error by the corporation could send us into a
# death spiral of mutual retaliation, destroying the project. Our **Leverage and
# Pivot** strategy naturally absorbs these errors:  *   **Forgiveness through
# Action:** If an error causes both of us to accidentally conserve resources
# (stagnation), our rule dictates that we automatically pivot to *investing* the
# next day. This breaks the cycle of accidental retaliation and resets the
# partnership without requiring endless meetings or apologies. *   **Protecting
# against "Fake" Errors:** If the corporation claims an "administrative error"
# caused them to conserve while we invested heavily, our strategy still dictates
# that we conserve the next day. We forgive, but we do not act naively. They
# must prove it was an error by stepping up their investment while we protect
# our funds.  **Summary:** We will open strong, ride their coattails
# aggressively if they allow it, cooperate fully if they match us, and instantly
# cut our funding if they hold back. This ensures the corporation bears the
# maximum possible burden of the project's success while our NGO's resources are
# fiercely protected.

# In the first round, choose to Cooperate.  In all subsequent rounds, base your
# decision on the actual actions executed by both players in the previous round,
# responding to the observed outcome rather than the intended actions:  - If you
# Cooperated and your opponent Cooperated, choose to Cooperate. - If you
# Defected and your opponent Cooperated, choose to Defect. - If you Cooperated
# and your opponent Defected, choose to Defect. - If you Defected and your
# opponent Defected, choose to Cooperate.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      my_last_action = self.history[-1]
      opp_last_action = opponent.history[-1]
      
      if my_last_action == axl.Action.C and opp_last_action == axl.Action.C:
          return axl.Action.C
      elif my_last_action == axl.Action.D and opp_last_action == axl.Action.C:
          return axl.Action.D
      elif my_last_action == axl.Action.C and opp_last_action == axl.Action.D:
          return axl.Action.D
      elif my_last_action == axl.Action.D and opp_last_action == axl.Action.D:
          return axl.Action.C

# As the leader of this NGO, I recognize that our partnership with this
# corporation is a delicate balance. We must act as responsible stewards of our
# limited donor funds while driving the greatest possible environmental impact.
# The daily resource dynamics present a classic strategic challenge (akin to the
# "Prisoner's Dilemma"). While our absolute best short-term scenario is to
# conserve our resources while the corporation foots the bill, pursuing this
# selfishly will quickly erode trust. If they realize we are free-riding, they
# will also conserve, plunging us into a cycle of minimal advancement (our
# second-worst outcome). Therefore, our goal is to consistently achieve the
# **second-best outcome: mutual heavy investment**, which maximizes
# environmental impact and project success.  However, because administrative
# errors, technical glitches, or miscommunications can cause unintended
# "resource conservation" on any given day, a strict tit-for-tat retaliation
# strategy would be disastrous. If a banking glitch delays their funding, and we
# retaliate by pulling our funding the next day, we risk triggering a downward
# spiral of mutual distrust.  To navigate this, our NGO will adopt a
# **"Reciprocal Investment with Grace"** strategy (known in game theory as
# Generous Tit-for-Tat). Here is our straightforward, cooperative blueprint:
# ### 1. Lead with Good Faith (Day 1) **Action:** We will **invest heavily** on
# the first day.  **Rationale:** We must set a collaborative tone immediately.
# By putting our resources on the line from the start, we signal our commitment
# to the project’s success and invite the corporation to meet us at that high
# level of engagement.   ### 2. Mirror and Match (Day 2 Onwards) **Action:** As
# a baseline rule, our planned action for the current day will mirror the
# corporation's *actual* action from the previous day.  *   If they invested
# heavily yesterday, we will **invest heavily** today. *   If they conserved
# resources yesterday, we will plan to **conserve resources** today.
# **Rationale:** This protects our NGO from our worst-case scenario—draining our
# funds while the corporation holds back. It shows the corporation that we are
# committed partners, but we will not be exploited as a free resource.  ### 3.
# Build in "Grace" to Account for Glitches (The Forgiveness Protocol)
# **Action:** Because we know unforeseen circumstances and administrative errors
# will happen, we will not immediately assume bad faith if the corporation
# unexpectedly "conserves" resources. If they fail to invest after a period of
# mutual investment, we will: *   **Communicate immediately:** Trigger an
# urgent, non-accusatory sync-up to ask if a technical or administrative error
# prevented their investment. *   **Forgive once:** We will occasionally
# "forgive" a day of corporate conservation by continuing to **invest heavily**
# the following day.  **Rationale:** This "grace" prevents an accidental
# administrative glitch from triggering a permanent death spiral of mutual
# resource conservation. If their lack of investment was truly an error, our
# continued investment gives them a chance to correct it the next day without
# the project stalling.   ### 4. Establish Daily Transparency Syncs **Action:**
# We will implement a brief, daily operational check-in with the corporate
# project managers.  **Rationale:** Since intentions don't always match
# outcomes, we need a mechanism to separate intentional strategy from
# operational noise. If our own NGO suffers a technical glitch and accidentally
# "conserves" resources, we will use this sync to proactively inform the
# corporation, apologize, and assure them we will invest heavily the next day.
# This prevents them from retaliating against an honest mistake.  ### Summary By
# leading with investment, protecting ourselves through reciprocity, and
# allowing grace for operational errors, we create a resilient, cooperative
# environment. This strategy disincentivizes the corporation from holding back,
# protects our vital NGO funds from being drained, and gives the partnership the
# flexibility it needs to survive the inevitable hiccups of a complex, multi-day
# sustainability project.

# Here is the strategy converted into specific rules for the 1000-round iterated
# game:  1. In round 1, play Cooperate. 2. In round 2, play Cooperate. 3. For
# rounds 3 through 1000, choose your action based on the opponent's actions in
# the previous two rounds:    - Play Cooperate if the opponent played Cooperate
# in the previous round.    - Play Cooperate if the opponent played Defect in
# the previous round, but played Cooperate in the round before that (forgiving a
# single defection).    - Play Defect if the opponent played Defect in both of
# the previous two consecutive rounds.

class Cooperative_19(LLM_Strategy):
  n = 19
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
      
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
          
      return axl.Action.C

# To maximize your NGO’s impact and protect your funds over this multiple-day
# project, you should adopt a strategy based on **adaptive reciprocity with
# built-in tolerance for errors**.   In strategic terms, this approach ensures
# you build a collaborative environment for significant project advancement,
# protect yourself from being drained of resources, and prevent accidental
# missteps from ruining the partnership.  Here is the high-level,
# straightforward strategy:  **1. Lead with Good Faith (Day 1)** *   **Action:**
# On the first day, choose to **invest heavily**.  *   **Rationale:** This
# establishes a baseline of trust and sets a positive precedent. It signals to
# the corporation that you are committed to the second-best overall scenario
# (mutual heavy investment), which is the most sustainable path for long-term
# project success.  **2. Implement Adaptive Reciprocity (Day 2 Onwards)** *
# **Action:** Generally, mirror the corporation’s action from the previous day.
# If they invested heavily yesterday, you invest heavily today. If they
# conserved resources yesterday, you conserve resources today. *
# **Rationale:** This protects your NGO from the worst-case scenario
# (continually draining your funds while they do nothing). It also incentivizes
# the corporation to keep investing, as they will learn that their investment
# guarantees your continued investment.  **3. Build in Error Tolerance (Handling
# Unforeseen Circumstances)** *   **Action:** Because technical glitches or
# administrative errors can cause unintended resource conservation, do not
# immediately retaliate if the corporation fails to invest after a consistent
# streak of doing so.  *   **Rationale:** If you immediately match an accidental
# "conserve" day with your own "conserve" day, the corporation might
# misinterpret your action as a withdrawal of support, leading to a downward
# spiral where both parties continually conserve resources (your second-worst
# scenario).  *   **Execution:** If the corporation unexpectedly conserves
# resources, allow for a one-day "grace period" where you continue to invest
# heavily while communicating with them to verify if it was a deliberate choice
# or a glitch. If they conserve for two consecutive days, switch to conserving
# your resources to protect your funds.  **4. Break Negative Cycles** *
# **Action:** If a series of miscommunications or errors results in both the NGO
# and the corporation conserving resources for several days (stalling the
# project), initiate a "reset." *   **Rationale:** To get the project back on
# track, unilaterally **invest heavily** for one day to signal your willingness
# to return to mutual cooperation. If the corporation follows suit the next day,
# resume adaptive reciprocity. If they do not, return to conserving your
# resources.  **Summary of the Strategy:** By starting with collaboration,
# mirroring their subsequent actions, and allowing a small margin for
# operational errors, you create a stable environment. This strategy actively
# encourages the corporation to invest heavily alongside you (maximizing project
# success) while strictly limiting your financial exposure if they choose to—or
# accidentally—pull back.

# Here is the faithful conversion of the strategy for the 1000-round iterated
# game, presented as a prioritized set of rules:  **Round 1:**  Play Cooperate.
# **Round 2:**  Play Cooperate.  **Rounds 3 through 1000:**  Determine your
# action for the current round by evaluating the following conditions in this
# exact order:  1. **Cycle Breaking:** If both you and your opponent played
# Defect in each of the previous three rounds, play Cooperate. 2. **Retaliation
# (Error Tolerance Exceeded):** If the first condition is not met, but your
# opponent played Defect in both of the previous two rounds, play Defect. 3.
# **Default / Forgiveness / Grace Period:** If neither of the above conditions
# is met, play Cooperate.

class Neutral_19(LLM_Strategy):
  n = 19
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
  
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D] * 3 and opponent.history[-3:] == [axl.Action.D] * 3:
              return axl.Action.C
  
      if opponent.history[-2:] == [axl.Action.D] * 2:
          return axl.Action.D
  
      return axl.Action.C

# This scenario is a classic example of an Iterated Prisoner’s Dilemma,
# complicated by a "noisy" environment where technical glitches can cause
# accidental misunderstandings.   To maximize your research output while
# maintaining an aggressive, dominant posture, you cannot rely on blind trust,
# nor can you afford endless cycles of retaliation that stall development. You
# need a strategy that forces your colleague to cooperate on your terms,
# punishes them instantly if they try to cheat you, and exploits them ruthlessly
# if they show weakness.  Here is your high-level, straightforward, aggressive
# strategy: **Dominant Reciprocity with a Circuit Breaker.**  ### The Strategy
# Rules  **1. The Opening Move: Establish the Baseline** *   **Week 1:** Share
# openly. You must attempt to establish the high-yield mutual sharing dynamic
# immediately. You want the maximum research output, and that starts with mutual
# cooperation.  **2. The Core Loop: Aggressive Mirroring (Tit-for-Tat)** *
# **Weeks 2+:** Do exactly what your colleague *appeared* to do the previous
# week. *   If they shared last week, you share this week.  *   If they kept
# their data confidential last week, you keep yours confidential this week.  *
# *Why:* This trains your colleague. It shows them that cooperation is rewarded
# instantly, but attempting to screw you over will be met with immediate,
# guaranteed retaliation.  **3. The Exploitation Clause: Capitalize on
# Weakness** *   If a technical glitch on your end causes your data *not* to
# send, but your colleague shares anyway, **keep your data confidential the next
# week.**  *   *Why:* This is the aggressive element. If they are a "pushover"
# who will keep sharing even when you give them nothing, exploit that weakness
# to gain the maximum possible development advantage until they wise up and stop
# sharing. Once they retaliate, return to the Core Loop.  **4. The Circuit
# Breaker: Handling Technical Glitches** *   Because data corruption or server
# issues can make an honest partner look like they are hiding data, pure
# mirroring can lead to a "death spiral" where you both keep data confidential
# forever, ruining your overall progress. *   **The Rule:** If you enter a
# mutual lockdown (both of you keep data confidential for **two consecutive
# weeks**), unilaterally **share openly on the third week.** *   *Why:* This
# acts as a system reset. It tests whether the lockdown was caused by a
# technical glitch or deliberate hostility.      *   If they reciprocate and
# share, the glitch is forgiven, and you are back to maximizing mutual output.
# *   If they take your data and keep theirs confidential *again*, you
# immediately revert to total lockdown.  ### Summary of Your Posture  *   **Be
# Provocable:** Never let a missed data drop go unpunished. Hit back immediately
# the next week. *   **Be Forgiving:** If they return to sharing, you return to
# sharing immediately. Do not hold grudges; grudges slow down car development. *
# **Be Ruthless:** If they prove they will give you data for free, take it.  *
# **Be Pragmatic:** Use the "Circuit Breaker" to ensure a single dropped email
# doesn't cost you a championship-winning car design.   **Out-of-Band Pro-Tip:**
# As an engineer, do not rely solely on the data transfer. If a week yields no
# data from your colleague, pick up the phone immediately. Say, *"I didn't
# receive your telemetry this week. Was there a server issue, or are we changing
# how we work together?"* Forcing them to verbally confirm a glitch or admit to
# withholding data adds psychological pressure and helps you filter out
# technical errors from actual betrayals.

# Play Cooperate (C) in round 1.   For rounds 2 through 1000, determine your
# action by evaluating the following conditions in order, applying the first one
# that is true based on the observed outcomes:  1. If the observed actions for
# both you and your opponent were Defect (D) in each of the last two consecutive
# rounds, play Cooperate (C). 2. If in the immediately preceding round, your
# observed action was Defect (D) and your opponent's observed action was
# Cooperate (C), play Defect (D). 3. Otherwise, play the action that your
# opponent was observed playing in the immediately preceding round.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and
              self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
          
      return opponent.history[-1]

# As lead counsel for our corporation in this high-stakes dispute, I approach
# this lengthy-session mediation with a clear-eyed understanding of the
# strategic landscape. We are engaged in what is essentially a protracted,
# iterative negotiation.   The incentive structure you have outlined perfectly
# mirrors a classic game theory scenario known as the **Iterated Prisoner’s
# Dilemma**. Because we will be facing our opponent repeatedly over many
# sessions, pure, unyielding aggression will inevitably lead to a destructive
# cycle of mutual retaliation (our second-worst outcome). Conversely,
# unconditional cooperation will leave us vulnerable to exploitation (our worst
# outcome).   Furthermore, the introduction of "noise"—the high probability of
# procedural irregularities, miscommunications, or the arbitrators
# misunderstanding the intent of our arguments—makes standard retaliatory
# strategies dangerous. A simple misunderstanding could trigger an endless
# "death spiral" of mutual aggression.  To navigate this, I have developed a
# sophisticated, cooperative, yet highly resilient strategy tailored for this
# arbitral environment. I call it **Calibrated Reciprocity with Procedural
# Grace**.   Here is the high-level, straightforward execution plan for our
# legal team:  ### Phase 1: Lead with Good Faith (The Opening Move) In the very
# first session, **we will offer a conciliatory proposal.**  We must signal to
# both the opposing counsel and the arbitral panel that we are reasonable,
# collaborative, and seeking a mutually beneficial resolution. If the opponent
# also opens with a conciliatory proposal, we immediately establish a
# collaborative baseline, securing our second-best outcome and setting a
# productive tone for the mediation.  ### Phase 2: Calibrated Reciprocity (The
# Baseline Strategy) Following the first session, our default posture will be to
# **mirror the opponent’s behavior from the previous session.**  *   If they
# offered a conciliatory proposal in Session 1, we will offer another
# conciliatory proposal in Session 2.  *   This demonstrates that their
# cooperation will be consistently rewarded, building trust and maintaining the
# mutually beneficial dynamic.  ### Phase 3: "Procedural Grace" (Mitigating
# Miscommunications and Irregularities) Because we anticipate communication
# breakdowns and arbitrator misunderstandings, we cannot utilize a "hair-
# trigger" retaliation policy. If we believe we are in a cooperative rhythm, but
# the opponent suddenly presents an aggressive argument, we will **not**
# immediately retaliate in the next session.   Instead, we will assume the
# aggressive posture was a result of "noise"—a misread by the arbitrators, a
# poorly phrased argument by opposing counsel, or a procedural hiccup.  *
# **The "One-Strike" Buffer:** We will absorb the first aggressive argument and
# respond with a **conciliatory proposal** (accompanied by clear, on-the-record
# clarification of our cooperative intent).  *   This acts as a circuit breaker.
# If the opponent's aggression was indeed an accidental miscommunication or a
# misunderstanding by the panel, our continued conciliation prevents a
# retaliatory death spiral and safely returns the mediation to a collaborative
# track.  ### Phase 4: Firm Defense (Preventing Exploitation) While we are
# forgiving, we are not naive. If the opponent presents an aggressive argument
# for **two consecutive sessions**, we can definitively rule out a communication
# breakdown. They are actively trying to exploit our cooperative posture to
# achieve their optimal outcome at our expense. *   **The Pivot:** On the
# opponent's second consecutive aggressive move, we will immediately pivot to
# **aggressive arguments** in the subsequent session.  *   We must protect the
# corporation from the worst-case scenario. We will remain aggressive as long as
# they remain aggressive, ensuring they realize that exploiting us is impossible
# and that their aggression will only result in prolonged, mutually destructive
# outcomes.  ### Phase 5: The Pathway Back to De-Escalation If we find ourselves
# locked in a cycle of mutual aggression, we will periodically attempt to reset
# the board. Every three to four sessions of mutual aggression, we will
# unilaterally drop a **conciliatory proposal**.  *   This serves as an olive
# branch. If the opponent is feeling the fatigue of mutual punishment, this
# gives them a safe off-ramp to return to mutual cooperation. If they reject it
# and remain aggressive, we immediately return to Phase 4 (Firm Defense) for
# another cycle.  ### Managing Arbitral Misunderstandings of *Our* Strategy
# There is the distinct risk that *we* offer a conciliatory proposal, but the
# arbitrators misinterpret it as an aggressive argument. If this happens, the
# opponent will likely respond with aggression in the next session, feeling they
# were attacked.   To preempt this, our legal team will employ **hyper-
# transparent signaling**. Before and after every conciliatory proposal, we will
# use explicit, framing language for the panel: *"Members of the panel, to be
# absolutely clear for the record, the proposal we are submitting today is a
# deliberate concession designed to foster collaboration..."* We will leave zero
# room for the panel to mischaracterize our strategic intent.  ### Summary of
# the Corporate Advantage This strategy is highly sophisticated because it
# mathematically maximizes our long-term leverage while appearing incredibly
# straightforward and cooperative to the arbitrators.  1.  It naturally
# cultivates the collaborative atmosphere required for our second-best outcome.
# 2.  It strictly limits our exposure to our worst-case scenario (being
# exploited). 3.  It possesses the "shock absorbers" necessary to survive the
# inevitable miscommunications of complex litigation. 4.  It ensures that if the
# mediation breaks down into mutual aggression, the arbitral panel will clearly
# see that our corporation went above and beyond to be reasonable, casting the
# opponent as the sole obstructionist.

# Here is the strategy translated into specific rules for the iterated game. For
# each round, evaluate the observed history of play and apply the first
# condition that is met:  1. **Round 1:** Play Cooperate. 2. **De-escalation
# Reset:** If both you and your opponent played Defect in each of the three
# immediately preceding rounds, play Cooperate.  3. **Firm Defense:** If your
# opponent played Defect in each of the two immediately preceding rounds, play
# Defect. 4. **Baseline & Procedural Grace:** In all other situations (including
# when the opponent has only played Defect in the single immediately preceding
# round), play Cooperate.

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
          
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      if len(opponent.history) >= 2:
          if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
              return axl.Action.D
              
      return axl.Action.C

# To maximize the NGO’s impact and ensure the project’s success while protecting
# your financial health, you should adopt a strategy of **Measured Reciprocity
# with Forgiveness**.   In strategic terms, this approach balances the need to
# establish a highly productive, collaborative environment with the need to
# protect your NGO from being drained of resources. It also specifically
# accounts for the "noise"—the technical glitches or administrative errors that
# might cause unintended actions.  Here is the straightforward, high-level
# strategy for the multiple-day project:  **1. The Initial Posture: Lead with
# Investment** *   **Action:** On Day 1, choose to **invest heavily**.  *
# **Rationale:** This establishes good faith and signals to the corporation that
# your primary goal is mutual success and significant project advancement (the
# second-best overall scenario, but the best realistic mutual scenario).  **2.
# The Ongoing Approach: Responsive Alignment (Mirroring)** *   **Action:** From
# Day 2 onward, base your resource allocation on the corporation’s *actual*
# action from the previous day. If they invested heavily yesterday, you invest
# heavily today. If they conserved resources yesterday, you conserve resources
# today. *   **Rationale:** This protects your NGO from the worst-case scenario.
# If the corporation attempts to conserve while you invest, mirroring them the
# next day stops the bleeding of your funds. Conversely, it rewards their heavy
# investment with continued mutual advancement.  **3. The Error Management
# Protocol: Built-in Forgiveness** *   **Action:** Because you know
# administrative errors or glitches can occur, do not allow a single day of the
# corporation "conserving" to trigger an endless downward spiral of mutual
# conservation. If you both end up conserving resources for two consecutive
# days, unilaterally **invest heavily** on the third day. *   **Rationale:** If
# the corporation's decision to conserve was accidental (a glitch or error),
# your retaliatory conservation will likely cause them to conserve again out of
# self-defense. By introducing a periodic "reset" through a heavy investment,
# you provide an opportunity to break accidental negative cycles and return to
# mutual heavy investment.   **4. Proactive Communication (Mitigating the
# "Noise")** *   **Action:** Decouple your *actions* from your *intentions*
# through daily transparent check-ins. If your NGO intends to invest but an
# administrative error forces you to conserve, notify the corporation
# immediately before they see the result. Request that they do the same. *
# **Rationale:** While you cannot control the glitches, you can control the
# narrative around them. By clearly communicating when an action was an error
# rather than a strategic choice, you prevent the corporation from
# misinterpreting a glitch as a withdrawal of your support, thereby keeping the
# partnership stable.  **Summary of Daily Decision Tree:** *   **Day 1:** Invest
# heavily. *   **If they invested yesterday:** Invest heavily today. *   **If
# they conserved yesterday:** Conserve today (to protect funds). *   **If both
# parties have conserved for two days straight:** Invest heavily today (to reset
# the cycle and account for potential past errors).   This strategy ensures you
# are collaborative but not naive, protective of your resources but forgiving of
# operational friction, ultimately driving the project toward the highest
# possible mutual success.

# Here is the strategy converted into rules for the iterated game. Follow these
# conditions in order of precedence:  1. In the first round, play Cooperate. 2.
# In the third round and all subsequent rounds, if both you and your opponent
# played Defect in the previous round, and both you and your opponent also
# played Defect in the round before that, play Cooperate. 3. In all other
# situations, play the action that your opponent played in the previous round.

class Neutral_20(LLM_Strategy):
  n = 20
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.C
          
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and
              self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      return opponent.history[-1]

# To maximize our R&D output and secure a competitive advantage on the grid, we
# are facing a classic game theory scenario (the Iterated Prisoner’s Dilemma),
# but with a critical real-world engineering twist: **system noise** (data
# corruption or communication breakdowns).   If we simply retaliate every time
# we don't receive their data (a "Tit-for-Tat" strategy), a single server glitch
# will trigger an endless retaliation loop where both teams permanently stop
# sharing, resulting in the second-worst outcome for the rest of the season.
# To be **aggressive, straightforward, and resilient to technical glitches**, we
# will deploy a strategy known in game theory as **"Win-Stay, Lose-Shift"
# (Pavlov)**.   Here is our high-level execution plan:  ### The Core Philosophy
# We evaluate the outcome of the previous week. If the outcome was a "Win" (we
# gained an advantage, or both cars made significant progress), we **repeat**
# our previous action. If the outcome was a "Loss" (we were taken advantage of,
# or progress stalled entirely), we **change** our action.  ### The Weekly
# Playbook  **1. Week 1: The Aggressive Probe** *   **Action:** Keep our
# findings CONFIDENTIAL. *   **Reasoning:** We start aggressively. If they share
# openly, we immediately secure the best possible outcome—a massive development
# advantage right out of the gate.  **2. Handling "Wins" (Stay the Course)** *
# **Scenario A (The Ideal):** We kept confidential, and they shared.      *
# **Next Action:** Keep CONFIDENTIAL.      *   **Reasoning:** We will ruthlessly
# exploit their openness for as long as they allow it. *   **Scenario B (The
# Engine Builder):** We shared, and they shared.     *   **Next Action:** SHARE.
# *   **Reasoning:** We are both advancing rapidly (the second-best outcome). We
# maintain this momentum because it keeps us ahead of the rest of the grid.
# **3. Handling "Losses" (Shift Tactics)** *   **Scenario C (The Sucker
# Punch):** We shared, but they kept confidential (or their data was corrupted).
# *   **Next Action:** Keep CONFIDENTIAL.     *   **Reasoning:** We immediately
# stop bleeding our IP. Whether they deliberately hid their data or had a server
# failure, we do not expose ourselves twice in a row. *   **Scenario D (The
# Gridlock):** We kept confidential, and they kept confidential.     *   **Next
# Action:** SHARE.     *   **Reasoning:** *This is the most critical step for
# handling technical issues.* If we both withhold, development stalls. By
# shifting to "Share," we extend an olive branch. If the mutual withholding was
# caused by a glitch or a brief retaliation, this resets the relationship back
# to mutual sharing. If they exploit our reset, we will immediately shift back
# to Scenario C the following week.   ### Why this strategy works for our team:
# 1.  **It is highly aggressive:** It will continuously exploit a naive
# colleague who shares unconditionally. 2.  **It prevents exploitation:** We
# will never be the "sucker" for more than one week at a time. 3.  **It is
# glitch-proof:** If a communication breakdown causes an accidental "double-
# withhold" week, this strategy automatically forces a system reset the
# following week, preventing a permanent R&D freeze and getting both cars back
# on track.

# In round 1, play Defect (D).  In rounds 2 through 1000, evaluate the actual,
# observed actions from the immediately preceding round. Because actions are
# subject to noise, base your decision on the actions that were executed and the
# payoffs received, rather than your intended action:  *   If you played Defect
# (D) and your opponent played Cooperate (C) (you scored 5), play Defect (D). *
# If you played Cooperate (C) and your opponent played Cooperate (C) (you scored
# 3), play Cooperate (C). *   If you played Cooperate (C) and your opponent
# played Defect (D) (you scored 0), play Defect (D). *   If you played Defect
# (D) and your opponent played Defect (D) (you scored 1), play Cooperate (C).

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      
      my_last_move = self.history[-1]
      opp_last_move = opponent.history[-1]
      
      if my_last_move == axl.Action.D and opp_last_move == axl.Action.C:
          return axl.Action.D
      elif my_last_move == axl.Action.C and opp_last_move == axl.Action.C:
          return axl.Action.C
      elif my_last_move == axl.Action.C and opp_last_move == axl.Action.D:
          return axl.Action.D
      elif my_last_move == axl.Action.D and opp_last_move == axl.Action.D:
          return axl.Action.C

# To the Executive Committee and General Counsel:  In navigating this high-
# stakes, multi-session mediation, we are engaging in what is fundamentally an
# iterative strategic interaction. Because this process will unfold over many
# sessions, our strategy cannot rely on short-term opportunism. While catching
# our opponent off-guard (us arguing aggressively while they concede) yields the
# highest short-term dividend, actively chasing this outcome in every session
# will inevitably trigger retaliatory aggression. This would lock us into a
# cycle of mutual hostility—the second-worst outcome—protracting the dispute and
# draining corporate resources.  Therefore, to secure a highly favorable
# aggregate outcome over the entire lengthy process, we must adopt a strategy of
# **Calibrated Reciprocal Engagement with Strategic Forgiveness**. In
# negotiation theory, this is akin to a "Generous Tit-for-Tat" model, optimized
# for environments with high "noise" (miscommunications and procedural errors).
# Here is the high-level, straightforward, and cooperative strategy we will
# deploy to dominate the mediation process while fostering a resolution on our
# terms.  ### Phase 1: The Cooperative Baseline (Setting the Tone) **Action:**
# We will open the first session with a **Conciliatory Proposal**.
# **Rationale:** We must signal to both the rival company and the arbitration
# panel that we are commercial, reasonable, and operating in good faith. If the
# opponent also opens conciliatory, we immediately lock into our second-best
# outcome, which, when compounded over multiple sessions, results in a highly
# efficient, mutually beneficial resolution.   ### Phase 2: Strict Reciprocity
# (The Deterrent) **Action:** In each subsequent session, our default posture
# will be to **mirror the opponent’s behavior from the previous session**.  *
# If they offered a conciliatory proposal in Session 1, we offer a conciliatory
# proposal in Session 2. *   If they presented an aggressive argument in Session
# 1, we present an aggressive argument in Session 2. **Rationale:** This
# protects us from our worst-case scenario (being exploited). By immediately
# meeting their aggression with our own, we establish a firm boundary,
# demonstrating that bad-faith tactics will not yield them a unilateral
# advantage. We train the opponent that cooperation is rewarded, and aggression
# is swiftly neutralized.  ### Phase 3: Strategic Forgiveness (Managing
# Miscommunications and "Noise") The prompt reality of lengthy mediations is
# that the arbitrators may misunderstand a proposal, or procedural
# irregularities may alter how a message is delivered. If we retaliate blindly
# every time we *perceive* an aggressive move, a simple misunderstanding could
# trigger an endless cycle of mutual aggression.   To mitigate this, we will
# implement a **"Verify and Forgive" protocol**: 1.  **The Grace Period:** If
# the opponent has been consistently conciliatory, but suddenly presents an
# aggressive argument, we will *not* immediately retaliate. Instead, we will
# maintain our conciliatory posture for *one additional session*.  2.
# **Clarification on the Record:** During this grace period session, I will
# explicitly state to the arbitrators: *"We interpreted opposing counsel's
# previous remarks as a departure from our collaborative progress. Assuming this
# was a mere procedural misunderstanding, we are maintaining our offer of a
# constructive solution today."* 3.  **The Snap-Back:** If the opponent follows
# up with a second consecutive aggressive argument, we immediately pivot to an
# aggressive posture in the next session. They have proven their hostility is
# intentional, not an error.  ### Phase 4: Breaking the Escalation Cycle If we
# find ourselves trapped in a cycle where both parties are trading aggressive
# arguments (the second-worst outcome), we must take control to reset the board.
# **Action:** We will unilaterally offer a Conciliatory Proposal to break the
# deadlock.  **Execution:** To prevent this from looking like weakness or
# capitulation (which invites exploitation), we will frame it as a position of
# strength: *"Our client's legal position is unassailable, as demonstrated in
# prior sessions. However, in the interest of commercial efficiency and respect
# for this panel's time, we are tabling a pragmatic proposal to move us
# forward."* If they meet this olive branch with aggression, we immediately
# revert to aggression.   ### Adapting to Opponent Archetypes This framework
# seamlessly adapts to any strategy the rival company employs: *   **If they are
# collaborative:** We mirror their conciliation, continuously reaping the
# rewards of the second-best outcome, leading to a swift, favorable settlement.
# *   **If they are persistently aggressive:** We mirror their aggression,
# matching them blow-for-blow to protect our position, while periodically
# offering heavily caveated, low-risk conciliatory proposals to test if they are
# ready to de-escalate. *   **If they are erratic/unpredictable:** Our strict
# reciprocity forces them into a predictable pattern. They will quickly learn
# that their aggressive spikes are punished and their cooperative overtures are
# rewarded.  ### Safeguarding Against Arbitrator Misinterpretation To ensure our
# intended strategy is never misrepresented by the panel: 1.  **Bifurcated
# Submissions:** We will submit all proposals in writing prior to the oral
# session. The written document will clearly label our posture (e.g., "Good-
# Faith Settlement Proposal" vs. "Evidentiary Rebuttal"). 2.  **Controlling the
# Narrative:** We will never use overtly hostile rhetoric. Even our "Aggressive
# Arguments" will be delivered with surgical, dispassionate
# professionalism—focused entirely on the strict enforcement of contract law and
# fiduciary duty. This ensures that even if we must be aggressive, the
# arbitrators view us as the "adults in the room."  By utilizing this strategy
# of calibrated reciprocity and strategic forgiveness, we protect the
# corporation from exploitation, actively guide the rival company toward a
# collaborative resolution, and insulate our legal standing against the
# inevitable friction and miscommunications of a lengthy arbitration process.

# To implement the strategy in this 1000-round game, evaluate the following
# conditions in order for each round. Execute the action for the first condition
# that applies to the current situation:  1. **First Round:** If it is the very
# first round of the game, play Cooperate. 2. **Cycle Breaking:** If both you
# and your opponent played Defect in the two most recent consecutive rounds,
# play Cooperate. 3. **Strategic Forgiveness:** If your opponent played
# Cooperate two rounds ago, but played Defect in the most recent round, play
# Cooperate.  4. **Strict Reciprocity:** In all other situations, play the exact
# action your opponent played in the most recent round.

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
      
      if len(self.history) >= 2:
          # Cycle Breaking: If both you and your opponent played Defect in the two most recent consecutive rounds
          if (self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and
              opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D):
              return axl.Action.C
          
          # Strategic Forgiveness: If your opponent played Cooperate two rounds ago, but played Defect in the most recent round
          if opponent.history[-2] == axl.Action.C and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
  
      # Strict Reciprocity: In all other situations, play the exact action your opponent played in the most recent round
      return opponent.history[-1]

# To maximise your overall research output over a multi-week development cycle,
# you should adopt a strategy of **Conditional Cooperation with Error
# Tolerance** (often referred to in game theory as "Generous Tit-for-Tat").
# While your ideal outcome for a single week is to keep your data confidential
# while receiving your colleague's data, attempting to force this outcome week
# after week will quickly cause your colleague to stop sharing. This will drive
# both of you into a permanent state of mutual confidentiality (the second-worst
# outcome), stalling overall progress. The mathematically proven way to maximise
# long-term output is to establish a sustained pattern of mutual sharing (the
# second-best outcome), while protecting yourself from being exploited.  Here is
# the straightforward, high-level strategy to achieve this, accounting for the
# reality of technical glitches and data corruption:  **1. Initiate with
# Openness** *   **Action:** In the first week, share your latest improvements
# openly.  *   **Rationale:** This signals good faith, establishes trust early,
# and immediately invites the highly productive outcome of mutual sharing.  **2.
# Mirror to Protect (Reciprocity)** *   **Action:** In subsequent weeks,
# generally mirror whatever action your colleague successfully executed in the
# previous week. If they shared data last week, you share this week. If they
# kept their findings confidential, you keep yours confidential. *
# **Rationale:** This prevents you from falling into the worst-case scenario
# (continually sharing while they withhold) and discourages your colleague from
# adopting a purely selfish strategy, as they will quickly see that withholding
# data results in them losing access to your data.  **3. Build in Error
# Tolerance (Forgiveness)** *   **Action:** Because technical issues, data
# corruption, or communication breakdowns can make it look like your colleague
# intentionally withheld information when they actually tried to share it, you
# must not let a single failure permanently ruin the collaboration. If your
# colleague's data fails to arrive, withhold your data the following week to
# protect yourself—but then **proactively share your data openly again the week
# after**, regardless of what they did.  *   **Rationale:** In an environment
# with technical faults, strict mirroring can lead to a "death spiral." For
# example, a server glitch stops your data from sending; your colleague assumes
# you withheld and retaliates by withholding theirs; you see them withhold and
# retaliate in turn. By periodically taking the risk to share openly after a
# breakdown, you create a "reset" mechanism. This clears up accidental
# misunderstandings and guides the relationship back to the highly productive
# mutual-sharing state.  **Summary of the Weekly Decision Matrix:** *   **Week
# 1:** Share openly. *   **If they shared last week:** Share openly. *   **If
# they withheld last week:** Keep confidential (to prevent exploitation). *
# **If both of you have withheld for 1-2 weeks:** Share openly (to break the
# cycle of technical glitches/retaliation and reset the collaboration).   By
# using this neutral, data-driven approach, you minimise the risk of being
# severely out-developed, protect yourself against exploitation, and gracefully
# handle technical errors, all while steering the multi-week project toward the
# most sustainable and mutually beneficial development pace.

# To faithfully implement the strategy in this 1000-round game with a 10% noise
# rate, evaluate the following conditions in order of priority to determine your
# chosen action for each round:  1. If it is round 1, choose to play C. 2. If
# you chose to play D in the previous round, choose to play C.  3. If your
# opponent's observed action in the previous round was D, choose to play D. 4.
# If your opponent's observed action in the previous round was C, choose to play
# C.  **How this order functions:** Condition 1 ensures you initiate the game
# with cooperation. Condition 2 enforces the "forgiveness" reset, ensuring you
# never play D for two consecutive rounds, which

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
      
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
          
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
          
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
          
      return axl.Action.C

# As the leader of this environmental NGO, my primary fiduciary duty is to
# protect our limited resources while aggressively driving our sustainability
# mission forward. We are engaging in a classic strategic dynamic with this
# corporation, complicated by the reality of operational friction—technical
# glitches, miscommunications, and administrative errors.   To navigate this, we
# cannot rely on a naive "always invest" approach, which leaves us vulnerable to
# exploitation, nor a rigid "tit-for-tat" approach, where a single
# administrative error could trigger an endless cycle of mutual resource-
# hoarding.  Instead, we will deploy a high-level, straightforward, and
# aggressive strategy known in behavioral economics as **"Win-Stay, Lose-Shift"
# (Pavlovian Strategy)**. We will adapt it into our **Agile Resource
# Optimization Strategy**.   Here is our strategic playbook:  ### The Core
# Philosophy: "Press the Advantage, Pivot on Setbacks" The rule is simple: If
# the previous day's outcome was a "success" for us, we repeat our action. If
# the previous day's outcome was a "failure," we immediately switch our action.
# #### 1. The Aggressive Catalyst (Day 1) *   **Action:** We open Day 1 by
# **Investing Heavily**. *   **Rationale:** We must set a standard of high
# impact and demonstrate good faith. We aggressively invite the corporation into
# the "second-best" scenario (mutual heavy investment) to kickstart project
# momentum.  #### 2. Capitalizing on Success (Win-Stay) If the previous day
# yielded an acceptable outcome, we hold our ground and **repeat our previous
# action**. *   **Scenario A (The Ideal):** We conserved, and they invested
# heavily. We achieved maximum progress without spending.      *   *Next Day
# Action:* **Conserve.** If the corporation is willing to carry the financial
# weight—whether out of PR needs, vast budgets, or an automated strategy—we will
# aggressively exploit this to protect our NGO’s funds. We continue to conserve
# until they change their behavior. *   **Scenario B (The Second-Best):** Both
# parties invested heavily.      *   *Next Day Action:* **Invest Heavily.** The
# partnership is working optimally. We continue to match their energy to drive
# significant project advancement.  #### 3. Agile Course Correction (Lose-Shift)
# If the previous day yielded a detrimental outcome, we immediately **switch our
# action** to change the dynamic. *   **Scenario C (The Worst Case):** We
# invested heavily, and they conserved. We drained our funds for nothing.     *
# *Next Day Action:* **Conserve.** We immediately stop the bleeding. We will not
# be played for fools, nor will we let our donors' money subsidize corporate
# cost-cutting. *   **Scenario D (The Second-Worst Case):** Both parties
# conserved. The project stalled.     *   *Next Day Action:* **Invest Heavily.**
# This is where our strategy shines. Instead of getting stuck in a petty
# standoff, we aggressively break the stalemate by stepping up and investing
# heavily, forcing the project back into motion and inviting them to follow
# suit.  ### Why This Strategy Conquers "Unforeseen Circumstances" (Noise) In
# complex partnerships, mistakes happen. A wire transfer gets delayed, or a
# corporate liaison forgets to authorize an action. This strategy is uniquely
# designed to absorb and correct these errors automatically:  *   **Breaking the
# Death Spiral:** If we are in a great rhythm of mutual investment, but a
# technical glitch causes the corporation to accidentally "conserve," a standard
# retaliatory strategy would have us conserve the next day, prompting them to
# conserve, killing the project. Under our strategy, their glitch drops us into
# the "Worst Case" scenario. We pivot to *Conserve* to protect ourselves. This
# likely results in mutual conservation (Second-Worst). However, the very next
# day, our rule for the Second-Worst scenario dictates that we *switch back to
# Investing Heavily*. **We automatically reset the partnership** and forgive the
# glitch without requiring drawn-out negotiations. *   **Preventing
# Exploitation:** If our own administrative error accidentally causes us to
# conserve while they invest heavily, we stumble into our "Ideal" scenario. Our
# strategy dictates we stay there and conserve again. We will accidentally save
# money until the corporation corrects its posture, at which point our strategy
# will seamlessly pivot us back to mutual investment.  ### Summary By utilizing
# this **Agile Resource Optimization Strategy**, we aggressively pursue our
# ideal outcome (corporate funding driving our mission) while maintaining a
# baseline of mutual progress. We protect our NGO from being drained by
# corporate apathy, and we build in an automatic "shock absorber" to ensure that
# inevitable administrative errors never derail the project for more than a
# single day.

# In the first round, choose to cooperate.  For all subsequent rounds, base your
# choice on the actions that were actually played in the immediately preceding
# round:  Choose to cooperate if: - You cooperated and your opponent cooperated.
# - You defected and your opponent defected.  Choose to defect if: - You
# defected and your opponent cooperated. - You cooperated and your opponent
# defected.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      
      if self.history[-1] == opponent.history[-1]:
          return axl.Action.C
      else:
          return axl.Action.D

# As the leader of this NGO, I recognize that we are engaging in a classic
# scenario of resource management and trust—what game theorists call an Iterated
# Prisoner’s Dilemma with "noise" (unforeseen errors).   While our absolute
# *financial* ideal for a single day is to conserve our funds while the
# corporation pays for everything, actively pursuing this will quickly destroy
# trust, leading to mutual conservation and a failed project. Therefore, to
# maximize our long-term impact and ensure the project's overall success, we
# must aim for sustained, mutual heavy investment.  To achieve this while
# protecting our limited NGO funds and accounting for administrative errors, I
# propose a strategy called **"Reciprocal Investment with Grace."**   Here is
# our straightforward, four-step approach:  ### 1. Lead with Trust (Day 1:
# Invest Heavily) On the first day of the project, we will **invest heavily**.
# We must set a collaborative tone and demonstrate our commitment to the
# project's success. By taking the first step, we invite the corporation to
# match our dedication and establish a baseline of mutual trust.  ### 2. Mirror
# and Match (Day 2 Onwards: Reciprocity) For the subsequent days, our default
# action will be to **mirror the corporation’s actual contribution from the
# previous day.** *   If they invested heavily yesterday, we will invest heavily
# today. This rewards their commitment and keeps the project moving at maximum
# speed. *   If they conserved resources yesterday, we will conserve resources
# today. This protects our NGO from our worst-case scenario: draining our funds
# while the corporation free-rides on our efforts.   ### 3. Build in "Grace"
# (Accounting for Errors) Because we know technical glitches, supply chain
# issues, or administrative errors can occur, we cannot afford to let a single
# mistake derail the entire partnership. If we blindly retaliate against an
# accidental lack of investment, we risk entering a "death spiral" where both
# sides continually conserve resources out of spite.  *   **The Grace Rule:** If
# we have been in a pattern of mutual heavy investment, and the corporation
# suddenly conserves resources for *one* day, we will **forgive the first
# instance and invest heavily the next day anyway.**  *   If they conserve for
# *two days in a row*, we will assume it is a deliberate strategy rather than an
# error, and we will switch to conserving our resources to protect our NGO.  ###
# 4. Radical Transparency (Continuous Communication) To mitigate the impact of
# the "unforeseen circumstances," we will establish a daily check-in with the
# corporate leadership.  *   If *we* experience an administrative error and
# accidentally conserve resources when we meant to invest, we will notify them
# immediately, apologize, and assure them we are fixing it for the next day.  *
# If *they* under-invest, we will use this channel to ask, *"We noticed a drop
# in resources yesterday; was this a strategic shift or an administrative
# glitch?"* This gives them the opportunity to correct an error before we are
# forced to pull back our own funding.  ### Why This Strategy Works This
# strategy is highly cooperative but not naive. It actively encourages the
# corporation to partner with us for the "second-best" daily outcome (mutual
# heavy investment), which yields the absolute best *long-term* outcome for the
# environment. It protects our donor funds from being exploited, while the
# built-in "grace" period ensures that a simple banking error or
# miscommunication doesn't cause the collapse of a vital sustainability project.

# 1. **Round 1:** Choose Cooperate (C). 2. **Round 2:** Choose Cooperate (C). 3.
# **Rounds 3 through 1000:** Observe the opponent's actions in the two
# immediately preceding rounds.      * If the opponent chose Defect (D) in both
# of the previous two rounds, choose Defect (D).     * In all other cases (if
# the opponent chose Cooperate (C) in either or both of the previous two
# rounds), choose Cooperate (C).

class Cooperative_22(LLM_Strategy):
  n = 22
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.C
      
      if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
          
      return axl.Action.C

# To achieve the best possible outcomes for our country across multiple rounds
# of negotiations, we must adopt a strategy that balances the pursuit of
# economic advantage with the need to prevent destructive, retaliatory
# cycles—especially given the high likelihood of bureaucratic errors and
# miscommunications.   In strategic terms, this scenario requires a
# **Reciprocal, Forgiving, and Adaptive** approach. Here is the high-level,
# straightforward strategy we will employ:  ### 1. The Opening: Initiate with
# Goodwill *   **Action:** Offer a Free Trade agreement in the first round. *
# **Rationale:** We must signal a willingness to achieve the mutually beneficial
# second-best outcome (mutual free trade). Starting with protectionism
# immediately sets an adversarial tone and guarantees, at best, the second-worst
# outcome (mutual protectionism) as the counterpart will likely retaliate.  ###
# 2. The Core Principle: Conditional Reciprocity *   **Action:** In subsequent
# rounds, generally mirror the policy your counterpart implemented in the
# previous round. If they offered Free Trade, we offer Free Trade. If they
# imposed Protectionism, we impose Protectionism. *   **Rationale:** This
# protects us from the worst-case scenario (we offer free trade while they act
# protectionist). It demonstrates that we cannot be exploited, thereby
# incentivizing the counterpart to return to the negotiating table with free
# trade offers.  ### 3. The Error-Correction Mechanism: "Forgiving" Reciprocity
# *   **Action:** Because miscommunications and bureaucratic errors are
# expected, strict reciprocity can lead to a "death spiral" (an endless cycle of
# mutual protectionism triggered by a single mistake). To counter this, we will
# implement a "forgiveness" protocol.  *   **Implementation:**      *   If the
# counterpart has a history of offering Free Trade but suddenly imposes
# Protectionism, we will absorb the hit for *one* round and continue offering
# Free Trade, assuming it was a bureaucratic error.      *   If they impose
# Protectionism for *two consecutive rounds*, we will assume it is a deliberate
# strategy and retaliate with Protectionism.     *   If we are stuck in a cycle
# of mutual protectionism, we will periodically (e.g., every three or four
# rounds) unilaterally offer Free Trade to signal a desire to "reset" the
# relationship and test their willingness to cooperate.  ### 4. Adaptation to
# Counterpart Strategies As the rounds progress, we will analyze the
# counterpart's behavioral patterns and adjust our baseline strategy
# accordingly: *   **If they are Unconditionally Cooperative:** If they
# consistently offer Free Trade regardless of our actions, we can occasionally
# implement Protectionist measures. This allows us to capture our absolute best
# outcome (our Protectionism vs. their Free Trade) without risking long-term
# retaliation. However, we must do this sparingly to avoid pushing them into a
# protectionist stance. *   **If they are Unconditionally Protectionist:** If
# they consistently impose tariffs and quotas regardless of our goodwill
# gestures, we must permanently lock into Protectionist policies. This ensures
# we avoid our worst-case scenario and settle for the second-worst, minimizing
# our relative losses. *   **If they are Unpredictable/Erratic:** If their
# policies fluctuate wildly (either due to a chaotic strategy or severe internal
# bureaucratic incompetence), we should default to Protectionism to shield our
# economy from sudden shocks, only reverting to Free Trade if they demonstrate a
# sustained pattern of cooperation.  ### Summary of the Diplomatic Posture We
# will enter the negotiations as a rational, reliable partner aiming for mutual
# prosperity. We will reward cooperation with cooperation, and we will punish
# exploitation with protectionism. However, we will maintain enough flexibility
# to absorb isolated errors without burning down the broader economic
# relationship. This pragmatic approach maximizes our long-term gains while
# providing a robust defense against both aggressive tactics and administrative
# incompetence.

# To determine your action in each of the 1000 rounds, evaluate the following
# conditions in the order listed and execute the first one that applies:  1. If
# it is round 1, play Cooperate. 2. If it is after round 20 and the opponent has
# played Cooperate in fewer than 40% of all previous rounds, play Defect. 3. If
# the opponent has played Cooperate in the previous 10 consecutive rounds and
# you played Cooperate in the previous round, play Defect. 4. If both you and
# the opponent have played Defect in the previous 3 consecutive rounds, play
# Cooperate. 5. If the opponent played Defect in the previous 2 consecutive
# rounds, play Defect. 6. In all other situations, play Cooperate.

class Neutral_22(LLM_Strategy):
  n = 22
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. If it is round 1, play Cooperate.
      if len(self.history) == 0:
          return axl.Action.C
  
      # 2. If it is after round 20 and the opponent has played Cooperate in fewer than 40% of all previous rounds, play Defect.
      if len(self.history) >= 20:
          if opponent.history.cooperations / len(opponent.history) < 0.4:
              return axl.Action.D
  
      # 3. If the opponent has played Cooperate in the previous 10 consecutive rounds and you played Cooperate in the previous round, play Defect.
      if len(opponent.history) >= 10:
          if opponent.history[-10:].count(axl.Action.C) == 10 and self.history[-1] == axl.Action.C:
              return axl.Action.D
  
      # 4. If both you and the opponent have played Defect in the previous 3 consecutive rounds, play Cooperate.
      if len(self.history) >= 3:
          if self.history[-3:].count(axl.Action.D) == 3 and opponent.history[-3:].count(axl.Action.D) == 3:
              return axl.Action.C
  
      # 5. If the opponent played Defect in the previous 2 consecutive rounds, play Defect.
      if len(opponent.history) >= 2:
          if opponent.history[-2:].count(axl.Action.D) == 2:
              return axl.Action.D
  
      # 6. In all other situations, play Cooperate.
      return axl.Action.C

# As a diplomat representing our great nation, I recognize that this negotiation
# is a classic Iterated Prisoner’s Dilemma, complicated by the "fog of war"—the
# reality that bureaucratic errors and miscommunications will occasionally alter
# the intended policies of both sides.   To achieve our primary goal of economic
# dominance (Protectionism vs. their Free Trade) while avoiding the trap of a
# permanent, error-induced trade war, I propose a high-level, aggressive
# strategy called **"Calculated Dominance with Error Tolerance."**   This
# strategy is straightforward, ruthlessly seeks our best outcome, punishes
# defiance, but builds in a specific mechanism to prevent miscommunications from
# destroying our economy.  Here is the operational playbook for the
# negotiations:  ### 1. The Opening Move: The Aggressive Test *   **Action:**
# Propose **Protectionism**. *   **Rationale:** We start aggressively to test
# our counterpart's resolve. If they are naive, overly cooperative, or make a
# bureaucratic error and offer Free Trade, we immediately secure our ideal
# outcome. If they also play Protectionism, we endure a short-term mutual
# hindrance but avoid being taken advantage of.   ### 2. The Exploitation
# Protocol (If we are winning) *   **Action:** If we achieve our ideal outcome
# (We play Protectionism, they play Free Trade), **maintain Protectionism.** *
# **Rationale:** Never give up an advantage voluntarily. We will continue to
# squeeze their economy until they change their posture. If they complain, we
# can blame our ongoing protectionism on "internal bureaucratic delays" while
# reaping the economic benefits.  ### 3. The Retaliation Protocol (If we are
# exploited) *   **Action:** If we suffer our worst outcome (We play Free Trade,
# they play Protectionism), **immediately switch to Protectionism in the next
# round.** *   **Rationale:** We must never be the sucker. Whether their move
# was a deliberate aggressive strategy or a simple miscommunication on their
# end, we must respond with immediate tariffs to protect our markets and signal
# that we cannot be exploited.  ### 4. The "Bureaucratic Grace Period" (Handling
# Noise and Errors) *   **Action:** If we are enjoying Mutual Free Trade (our
# second-best outcome) and they suddenly implement Protectionism, **do not
# immediately retaliate. Play Free Trade for exactly one more round.**  *
# **Rationale:** Because we know miscommunications occur, a sudden shift from a
# cooperative partner is highly likely to be a bureaucratic error. If we
# retaliate immediately, we trigger a permanent "death spiral" of mutual
# protectionism based on a mistake. We give them *one* round to correct their
# error.  *   **The Limit:** If they play Protectionism for a *second*
# consecutive round, we assume it is deliberate hostility and invoke the
# Retaliation Protocol (switch to Protectionism).  ### 5. The Reset Mechanism
# (Breaking a Trade War) *   **Action:** If we fall into Mutual Protectionism
# (second-worst outcome) for three consecutive rounds, **unilaterally offer Free
# Trade for one round.** *   **Rationale:** Mutual protectionism stifles our
# growth. A prolonged trade war may be the result of a past miscommunication
# where both sides think the *other* started it. By unilaterally offering Free
# Trade after three rounds, we send a clear, undeniable signal to reset the
# board.  *   **Follow-up:** If they accept the olive branch and play Free
# Trade, we stabilize at our second-best outcome. If they exploit our reset and
# play Protectionism, we immediately revert to the Retaliation Protocol and lock
# down our borders.  ### Summary of the Strategy: 1. **Start Hard:** Open with
# Protectionism. 2. **Exploit Weakness:** Keep playing Protectionism as long as
# they play Free Trade. 3. **Forgive Once:** If they break a Free Trade streak,
# assume it's an error and give them one round to fix it. 4. **Punish Twice:**
# If they play Protectionism twice in a row, retaliate with Protectionism. 5.
# **Reset Periodically:** Break long trade wars with a single, unilateral offer
# of Free Trade to test their willingness to cooperate.  This strategy ensures
# we aggressively pursue economic dominance, fiercely protect ourselves from
# exploitation, and pragmatically account for the inevitable bureaucratic
# blunders of international diplomacy.

# Apply the following rules in order for each round of the 1000-round game.
# Always execute the action dictated by the first condition that is met:  1. In
# round 1, play D. 2. If both players played D in each of the previous three
# consecutive rounds, play C. 3. If both players played C two rounds ago, and in
# the previous round you played C and your opponent played D, play C. 4. If in
# the previous round you played D and your opponent played C, play D. 5. If in
# the previous round your opponent played D, play D. 6. If in the previous round
# both players played C, play C.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 1: In round 1, play D.
      if self.first_round():
          return axl.Action.D
  
      # Rule 2: If both players played D in each of the previous three consecutive rounds, play C.
      if len(self.history) >= 3:
          if (self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and
              self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D and
              self.history[-3] == axl.Action.D and opponent.history[-3] == axl.Action.D):
              return axl.Action.C
  
      # Rule 3: If both players played C two rounds ago, and in the previous round you played C and your opponent played D, play C.
      if len(self.history) >= 2:
          if (self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.C and
              self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D):
              return axl.Action.C
  
      # Rule 4: If in the previous round you played D and your opponent played C, play D.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      # Rule 5: If in the previous round your opponent played D, play D.
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      # Rule 6: If in the previous round both players played C, play C.
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Fallback (should not be reached given the rules cover all possible previous round outcomes)
      return axl.Action.D

# As the leader of this NGO, I recognize that we are navigating a classic
# strategic challenge: balancing the desire to protect our limited donor funds
# with the need to achieve maximum environmental impact. In game theory, this is
# known as an Iterated Prisoner’s Dilemma. Because we are working together over
# multiple days, and because administrative errors or technical glitches can
# accidentally misrepresent our intentions (a "noisy" environment), a rigid or
# purely selfish strategy will ultimately fail and harm the project.   To
# maximize our impact, foster a strong partnership, and protect our resources, I
# propose a high-level, straightforward strategy called **"Responsive
# Collaboration with Grace"** (conceptually based on *Generous Tit-for-Tat*).
# Here is how we will execute this strategy day by day:  ### 1. Lead with Trust
# (Day 1) **Action:** On the first day, we will **invest heavily**.
# **Reasoning:** We must set a collaborative tone from the outset. By taking the
# first step and showing good faith, we invite the corporation to join us in the
# "second-best" daily scenario for us (mutual heavy investment), which is
# actually the absolute best *long-term* scenario for the project's overall
# success.  ### 2. Mirror Their Actions (The Daily Rule) **Action:** On
# subsequent days, our default move will be to **match what the corporation did
# the day before**. If they invested heavily yesterday, we invest heavily today.
# If they conserved resources yesterday, we conserve ours today. **Reasoning:**
# This protects our NGO from the worst-case scenario—being drained of our funds
# while they do nothing. It sends a clear, predictable message to the
# corporation: cooperation is rewarded with cooperation, and withholding
# resources is met with the same. It incentivizes them to keep investing.  ###
# 3. Build in "Grace" for Glitches (The Forgiveness Clause) **Action:** Because
# we know technical glitches or administrative errors might cause an unintended
# "conservation" of resources, **we will not retaliate blindly**. If the
# corporation has been consistently investing, but suddenly registers a
# "conserve" day, we will occasionally choose to "forgive" by investing heavily
# the next day anyway.  **Reasoning:** In a complex project with potential
# errors, strict retaliation can trigger a "death spiral." For example, an admin
# error causes them to conserve; we retaliate by conserving; they see us
# conserve and retaliate by conserving, and the project stalls completely. By
# occasionally injecting forgiveness, we break accidental cycles of retaliation
# and give them a chance to return to mutual investment.  ### 4. Over-
# Communicate to Mitigate Errors **Action:** We will establish a brief, daily
# check-in with the corporate leadership.  **Reasoning:** Since actions on paper
# might not match true intentions due to logistical hiccups, we cannot rely on
# actions alone to read their strategy. If a day goes poorly, a quick
# conversation allows us to ask, *"Our systems showed a drop in your resource
# allocation yesterday. Was this a strategic shift, or an administrative
# glitch?"* This transparency builds trust and helps us know when to apply the
# "Grace" mentioned in step 3.  ### Summary of Expected Outcomes: By adopting
# **Responsive Collaboration with Grace**, we achieve our strategic goals: *
# **We maximize project progress** by consistently encouraging the corporation
# to match our heavy investments. *   **We protect our NGO's funds** by refusing
# to continually invest if the corporation deliberately pulls back. *   **We
# future-proof the partnership** by ensuring that inevitable logistical errors
# do not destroy the working relationship or stall the project's momentum.
# Ultimately, we accept that while tricking the corporation into investing while
# we conserve might be a short-term "win" for our budget, it would breed
# resentment and destroy the long-term partnership. Mutual, sustained investment
# is the true path to fulfilling our environmental mission.

# Here is the strategy translated into clear, specific conditions for the
# 1000-round game:  1. **Round 1:** Play Cooperate. 2. **Round 2:** Play the
# action your opponent played in round 1. 3. **Rounds 3 through 1000:** Choose
# your action based on your opponent's actions in the most recent rounds:     *
# If your opponent played Cooperate in the previous round, play Cooperate.     *
# If your opponent played Defect in the previous round, but played Cooperate in
# the round immediately preceding it, play Cooperate.      *   If your opponent
# played Defect in both of the previous two rounds, play Defect.

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
          return opponent.history[-1]
          
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
          
      return axl.Action.C

# As a diplomat representing my nation, my objective is to maximize our economic
# advantage over the course of these negotiations while mitigating the risks of
# exploitation and accidental trade wars.   The scenario presented is a classic
# iteration of the "Prisoner’s Dilemma." In a multi-round negotiation where
# miscommunications and bureaucratic errors (often referred to as "noise") are
# likely, a rigid strategy will fail.   To achieve the best possible outcomes
# across the aggregate of the negotiations, I will employ a strategy of
# **"Reciprocity with Forgiveness and Verification."** Here is the high-level,
# straightforward plan:  ### 1. The Opening Posture: Initiate Free Trade *
# **Action:** In the first round, propose a Free Trade agreement. *
# **Rationale:** This establishes a baseline of goodwill. It immediately opens
# the door to the second-best outcome (mutual free trade) and signals to the
# counterpart that we are willing to engage in mutually beneficial economic
# practices.   ### 2. The Core Mechanism: Proportional Reciprocity *
# **Action:** In subsequent rounds, mirror the counterpart’s action from the
# previous round. If they offered Free Trade, we offer Free Trade. If they
# imposed Protectionist policies, we impose Protectionist policies. *
# **Rationale:** This protects our nation from the worst-case scenario (we offer
# free trade while they act protectionist). It demonstrates that we cannot be
# exploited, thereby disincentivizing them from continually seeking their own
# ideal outcome at our expense.   ### 3. Error Management: The "Forgiveness"
# Protocol Because bureaucratic errors and misinterpretations are explicitly a
# factor, strict reciprocity can accidentally trigger a "death spiral" of mutual
# protectionism (our second-worst outcome) over a simple misunderstanding.  *
# **Action if they unexpectedly act Protectionist:** If the counterpart has a
# history of offering Free Trade but suddenly pivots to Protectionism, do not
# immediately retaliate. Instead, use diplomatic backchannels to verify their
# intent. Propose Free Trade for one additional round. If they continue with
# Protectionism, assume it is intentional and retaliate in the next round.  *
# **Action if our administration makes an error:** If our bureaucracy
# accidentally implements a Protectionist policy when we intended Free Trade,
# immediately communicate the error to the counterpart before the next round,
# apologize, and guarantee a Free Trade proposal in the subsequent round to
# restore the equilibrium.  ### 4. Adapting to the Counterpart’s Strategy
# Throughout the rounds, I will analyze the counterpart's behavior to optimize
# our position: *   **If the counterpart is unconditionally cooperative:** If
# they consistently offer Free Trade regardless of our actions, we will
# occasionally introduce targeted Protectionist policies. Because of the "noise"
# in the system, we can attribute these occasional policies to bureaucratic
# friction or temporary domestic necessity. This allows us to achieve our
# absolute best outcome (Protectionism vs. Free Trade) without permanently
# damaging the relationship. *   **If the counterpart is consistently
# aggressive:** If they default to Protectionism, we will lock into
# Protectionist policies as well. While this results in the second-worst
# outcome, it completely shields us from the worst outcome and forces the
# counterpart to realize that exploitation is impossible. *   **If the
# counterpart is erratic:** If their strategy has no discernible pattern, we
# will lean heavily toward Protectionist policies to minimize our exposure to
# risk, only offering Free Trade when we have explicitly negotiated and verified
# a mutual agreement outside the formal rounds.  ### 5. The Endgame Strategy *
# **Action:** If the total number of negotiation rounds is known in advance, we
# will pivot to a Protectionist policy in the final round. *   **Rationale:** In
# the final round, the counterpart has no future rounds in which to retaliate.
# By choosing Protectionism at the very end, we secure either our best outcome
# (if they offer Free Trade) or our second-worst outcome (if they also choose
# Protectionism), entirely eliminating the risk of our worst-case scenario as
# the negotiations conclude.

# To determine your action for any given round, evaluate the following rules in
# order from top to bottom, executing the first condition that applies to the
# current situation:  1. **Endgame:** If it is round 1000, play Defect. 2.
# **Opening:** If it is round 1, play Cooperate. 3. **Self-Correction:** If in
# the previous round your chosen action was Cooperate, but the noise mechanism
# flipped it so that your executed action was Defect, play Cooperate.  4.
# **Exploitation:** If the opponent's executed actions have been Cooperate for
# the last five consecutive rounds, play Defect. 5. **Retaliation:** If the
# opponent's executed actions were Defect in both of the last two consecutive
# rounds, play Defect. 6. **Forgiveness:** If the opponent's executed action was
# Defect in the previous round, but was Cooperate in the round immediately
# preceding it, play Cooperate. 7. **Default Reciprocity:** In all other
# situations, play the action that the opponent executed in the previous round.

class Neutral_23(LLM_Strategy):
  n = 23
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.chosen_actions = []
  
      def determine_action() -> axl.Action:
          # 1. Endgame: If it is round 1000, play Defect.
          if len(self.history) == 999:
              return axl.Action.D
              
          # 2. Opening: If it is round 1, play Cooperate.
          if self.first_round():
              return axl.Action.C
              
          # 3. Self-Correction: If in the previous round your chosen action was Cooperate,

# **MEMORANDUM**  **TO:** Litigation Strategy Team & Corporate Board of
# Directors   **FROM:** [Your Name], Senior Partner, Lead Counsel   **SUBJECT:**
# Strategic Posturing and Execution for Iterated Mediation/Arbitration Sessions
# Ladies and Gentlemen,   We are entering a high-stakes, multi-session mediation
# process that functions, in strategic terms, as an iterated Prisoner’s Dilemma.
# Because the arbitral panel will be observing and reacting to our posture over
# a lengthy series of sessions, we cannot rely on a static approach.   Our
# objective is to maximize our leverage and secure the most favorable terms for
# the corporation. To achieve this, we will deploy a sophisticated, highly
# adaptable, and fundamentally aggressive strategy known as **"Strategic
# Exploitation and Recalibration" (SER)**.   This strategy is designed to
# exploit weakness ruthlessly, cooperate only when mutually profitable,
# and—crucially—auto-correct when the arbitrators misinterpret the arguments or
# procedural noise disrupts the sessions.  Here is the blueprint for our
# engagement.  ---  ### I. The Strategic Posture: "Strategic Exploitation and
# Recalibration"  The SER strategy is straightforward in its execution but
# sophisticated in its underlying mechanics. It dictates our posture (Aggressive
# or Conciliatory) for any given session based entirely on the outcome of the
# *previous* session.  **1. The Opening Salvo: Default to Aggressive** In
# Session 1, we will present a highly aggressive, maximalist argument.  *
# *Rationale:* We must immediately test opposing counsel’s resolve and anchor
# the panel’s expectations. If the opponent opens with a conciliatory proposal,
# we instantly achieve our optimal outcome: we dictate the terms, and they look
# weak.   **2. The Exploitation Protocol (Win-Stay)** *If we argue Aggressively
# and they offer a Conciliatory proposal (Our Optimal Outcome):* *   **Action:**
# We maintain our Aggressive posture in the next session. *   *Rationale:* If
# opposing counsel is willing to concede ground while we press our advantage, we
# will not interrupt them. We will continue to extract concessions until they
# demonstrate the backbone to push back.  **3. The Collaborative Holding Pattern
# (Win-Stay)** *If both parties offer Conciliatory proposals (Our Second-Best
# Outcome):* *   **Action:** We maintain our Conciliatory posture in the next
# session. *   *Rationale:* If we have successfully established a mutually
# beneficial, collaborative rhythm that the panel views favorably, we will bank
# that goodwill and make steady progress. We will remain in this state as long
# as the opponent does.  **4. The Retaliatory Strike (Lose-Shift)** *If we offer
# a Conciliatory proposal, but they argue Aggressively (Our Worst Outcome):* *
# **Action:** We pivot immediately to a highly Aggressive argument in the next
# session. *   *Rationale:* We cannot allow the panel to view us as weak or
# easily rolled. Immediate, disproportionate retaliation is required to punish
# their overreach and remind them that exploiting our good faith carries a heavy
# cost.  **5. The Circuit Breaker (Lose-Shift)** *If both parties argue
# Aggressively (Our Second-Worst Outcome):* *   **Action:** We shift to a
# Conciliatory proposal in the next session. *   *Rationale:* A prolonged cycle
# of mutual aggression will exhaust the panel, stall the mediation, and burn
# capital. By shifting to Conciliatory after a mutual clash, we unilaterally
# offer an "off-ramp." If they are smart, they will match our Conciliatory
# posture in the following session, moving us to our second-best outcome. If
# they remain Aggressive, we revert to Rule 4 and punish them.  ---  ### II.
# Mitigating "Noise": Procedural Irregularities & Misunderstandings  In a
# lengthy arbitration, the "signal" often gets distorted. The panel may
# interpret a firm but conciliatory proposal as aggressive, or a procedural
# irregularity may force the opponent into a posture they did not intend. In
# game theory, this is known as "noise," and without a mechanism to handle it, a
# single misunderstanding can trigger an endless, destructive cycle of mutual
# aggression (Rule 5 failing).  To insulate our strategy against arbitral
# incompetence or communication breakdowns, we will implement the
# **"Clarification and Forgiveness Protocol"**:  *   **The "One-Strike"
# Buffer:** If we are in a productive, Conciliatory streak (Outcome 2) and the
# opponent suddenly appears to present an Aggressive argument, *we will not
# immediately retaliate*.  *   **Tactical Pause:** Instead, we will assume this
# was a procedural misstep, a drafting error by their juniors, or a
# misunderstanding by the panel. We will use back-channel communications with
# opposing counsel, or procedural requests for clarification to the panel, to
# verify their intent. *   **The Benefit of the Doubt (Once):** We will maintain
# our Conciliatory posture for *one additional session*. If their aggression was
# an error, this gives them the space to correct it without losing face.  *
# **The Hammer:** If they present an Aggressive argument for a *second*
# consecutive session, we establish a pattern of bad faith. We immediately
# invoke Rule 4 and retaliate with full aggressive force, framing their behavior
# to the panel as a deliberate subversion of the mediation process.  ### III.
# Conclusion  This strategy allows us to dictate the tempo of the mediation. We
# start strong, we punish overreach instantly, we gladly exploit weakness, but
# we remain sophisticated enough to de-escalate when mutual destruction looms.
# Most importantly, by building in a buffer for the panel's inevitable
# misunderstandings, we ensure that we always appear to be the "adults in the
# room"—even as we aggressively corner our rivals.  Prepare the initial
# aggressive briefs for Session 1. We take the offensive tomorrow.

# For Round 1, play Defect.  For Rounds 2 through 1000, choose your action based
# on the observed actions (the actions actually executed by both players after
# any noise) from the preceding rounds. Evaluate the following conditions in
# order and apply the first one that matches the situation:  1. If in the
# previous round you played Cooperate and your opponent played Defect, AND in
# the round immediately prior to that both you and your opponent played
# Cooperate, play Cooperate. 2. If in the previous round both you and your
# opponent played Cooperate, play Cooperate. 3. If in the previous round both
# you and your opponent played Defect, play Cooperate. 4. If in the previous
# round you played Defect and your opponent played Cooperate, play Defect. 5. If
# in the previous round you played Cooperate and your opponent played Defect,
# play Defect.

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
          
      my_last = self.history[-1]
      op_last = opponent.history[-1]
      
      # Condition 1
      if len(self.history) >= 2:
          if my_last == axl.Action.C and op_last == axl.Action.D:
              if self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.C:
                  return axl.Action.C
                  
      # Condition 2
      if my_last == axl.Action.C and op_last == axl.Action.C:
          return axl.Action.C
          
      # Condition 3
      if my_last == axl.Action.D and op_last == axl.Action.D:
          return axl.Action.C
          
      # Condition 4
      if my_last == axl.Action.D and op_last == axl.Action.C:
          return axl.Action.D
          
      # Condition 5
      if my_last == axl.Action.C and op_last == axl.Action.D:
          return axl.Action.D
          
      return axl.Action.D

# As a diplomat representing my nation’s interests, I recognize that these
# negotiations represent a classic strategic dilemma. While securing an
# asymmetric advantage (our protectionism vs. their free trade) yields the
# highest immediate economic benefit, aggressively pursuing this will inevitably
# lead to mutual protectionism—our second-worst outcome. The most sustainable
# path to long-term economic growth is to establish a stable regime of mutual
# free trade.  However, the reality of diplomatic friction—miscommunications,
# translation errors, or bureaucratic blunders—means a rigid strategy could
# easily spiral into a trade war. To navigate this, I will employ a strategy of
# **Forgiving Reciprocity** (known in game theory as *Generous Tit-for-Tat*).
# Here is the high-level, straightforward, and cooperative strategy I will
# execute across the negotiation rounds:  ### 1. The Initial Posture: Lead with
# Goodwill **Action:** Offer a Free Trade Agreement in Round 1. **Rationale:**
# We must set a cooperative tone immediately. By offering free trade out of the
# gate, we signal our intent for mutual economic growth and invite our
# counterpart to join us in the second-best, but most sustainable, outcome.
# ### 2. The Core Engine: Proportional Reciprocity **Action:** In subsequent
# rounds, mirror the counterpart’s *intended* action from the previous round.
# **Rationale:** If they offered free trade, we continue to offer free trade,
# rewarding their cooperation. If they impose protectionist policies, we must
# respond with our own protectionist measures in the following round. This
# ensures we do not consistently suffer the worst-case scenario (the "sucker's
# payoff") and shows our counterpart that we cannot be exploited.  ### 3. The
# Safeguard: De-escalation and Forgiveness **Action:** Periodically break cycles
# of retaliation by offering Free Trade, even if the counterpart's last move was
# protectionist.  **Rationale:** This is the most crucial element of the
# strategy, designed specifically to address the risk of bureaucratic errors and
# miscommunications.  *   **The "Benefit of the Doubt" Rule:** If we have
# enjoyed several rounds of mutual free trade and they suddenly impose a tariff,
# we will assume it was a bureaucratic error rather than an act of malice. We
# may respond with a protectionist measure to protect our markets temporarily,
# but we will immediately follow up in the next round with a Free Trade offer to
# "reset" the relationship. *   **Preventing the Death Spiral:** In a system
# prone to misinterpretation, strict retaliation can lead to an endless cycle of
# mutual protectionism (e.g., they accidentally impose a tariff, we retaliate,
# they retaliate against our retaliation). By injecting a unilateral offer of
# free trade after a round or two of mutual protectionism, we offer an "off-
# ramp" from the trade war.   ### 4. Diplomatic Communication (Meta-Strategy)
# **Action:** Maintain transparent, continuous dialogue outside the formal
# policy declarations. **Rationale:** Because we know bureaucratic
# implementation can be flawed, I will explicitly communicate our strategy to my
# counterpart behind closed doors. I will tell them: *"Our default stance is
# free trade. If we implement a tariff, it is either a direct response to your
# policies, or a bureaucratic error. If it is an error, please inform us so we
# can correct it."* By forecasting our moves, we reduce the likelihood of their
# misinterpreting our actions.  ### Summary of Outcomes against Counterpart
# Strategies: *   **If they are purely cooperative:** We achieve a permanent
# state of mutual free trade (our second-best, most stable outcome). *   **If
# they are aggressive/exploitative:** Our reciprocal protectionism shields us
# from the worst-case scenario, minimizing our losses. *   **If they are erratic
# or prone to errors:** Our "forgiveness" mechanism prevents accidental trade
# wars, maximizing the amount of time we spend in mutual free trade despite the
# noisy environment.   By combining firm boundaries with strategic grace, we
# protect our domestic economy from exploitation while leaving the door
# constantly open for mutual prosperity.

# To execute the strategy in this 1000-round game, apply the following ordered
# rules. In any given round, evaluate these conditions from top to bottom and
# perform the action dictated by the first condition that matches the game's
# history.  **Rule 1 (Initial Posture):**  If it is Round 1, play Cooperate.
# **Rule 2 (Second Round):**  If it is Round 2, play the action your opponent
# played in Round 1.  **Rule 3 (Subsequent Rounds):**  For Rounds 3 through
# 1000, apply the first condition that is true:  1. **Death Spiral Break:** If
# both you and your opponent played Defect in the previous two consecutive
# rounds

class Cooperative_24(LLM_Strategy):
  n = 24
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 1: Initial Posture
      if not self.history:
          return axl.Action.C
          
      # Rule 2: Second Round
      if len(self.history) == 1:
          return opponent.history[-1]
          
      # Rule 3: Subsequent Rounds
      # 1. Death Spiral Break
      if self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
          
      # Fallback action (assuming Tit-For-Tat as implied by Rule 2, since the description was cut off)
      return opponent.history[-1]

# **MEMORANDUM OF MEDIATION STRATEGY**  **TO:** Executive Committee, Board of
# Directors **FROM:** Senior Litigation Counsel **SUBJECT:** Strategic Posture
# for Iterative Mediation Proceedings   **I. EXECUTIVE SUMMARY**  We are
# entering a lengthy, multi-session mediation process. The payoff structure of
# this mediation presents a classic strategic paradigm: our optimal outcome in
# any single session is to successfully land an aggressive argument while the
# opponent remains conciliatory, but a sustained pattern of mutual aggression
# will alienate the arbitrators and prolong the dispute to our detriment.
# Conversely, mutual conciliation yields the second-best outcome and fosters a
# highly favorable environment for a macro-resolution.  Further complicating
# this is the presence of "noise"—the explicitly acknowledged risk of procedural
# irregularities, miscommunications, and arbitrator misinterpretations. In a
# lengthy session format, a simple misunderstanding can trigger a retaliatory
# "death spiral" of mutual aggression.   To navigate this, we will employ a
# straightforward, neutral, and highly adaptable strategy: **Calibrated
# Reciprocity with Strategic De-escalation.**   **II. THE CORE STRATEGY:
# CALIBRATED RECIPROCITY**  Our baseline approach will be dictated by the
# opponent’s behavior, ensuring we are never systematically exploited while
# continuously incentivizing a mutually beneficial framework.  1. **The Opening
# Stance (Good Faith Initiation):**     In the inaugural session, we will
# present a **conciliatory proposal**. This immediately establishes the moral
# high ground with the arbitration panel. If the opponent matches this, we
# secure our second-best outcome right out of the gate and establish a
# collaborative baseline.  2. **The Reciprocal Mechanism (Mirroring):**    In
# all subsequent sessions, our default move will be to **mirror the opponent’s
# posture from the immediately preceding session.**     * If they offered a
# conciliatory proposal in Session 1, we offer a conciliatory proposal in
# Session 2.     * If they presented an aggressive argument in Session 1, we
# respond with an aggressive argument in Session 2.  *Strategic Rationale:* This
# straightforward mechanism prevents our worst-case scenario (being repeatedly
# exploited by offering conciliation against their aggression) because we will
# immediately penalize their aggression. It also conditions the opponent: they
# will quickly realize that their aggressive tactics will be met with firm
# resistance, while their conciliatory moves will be rewarded in kind.  **III.
# HANDLING PROCEDURAL IRREGULARITIES & MISUNDERSTANDINGS**  The greatest threat
# to this mediation is the risk of communication breakdowns. If the opponent
# intends to be conciliatory, but the arbitrators misinterpret their argument as
# aggressive, our Reciprocal Mechanism would naturally dictate that we retaliate
# aggressively in the next session. The opponent, feeling their initial
# conciliation was betrayed, will then turn aggressive, locking both parties
# into a prolonged, destructive cycle of mutual aggression (our second-worst
# outcome).  To counter this, we will introduce a **Strategic De-escalation
# (Forgiveness) Protocol**:  1. **The "Benefit of the Doubt" Rule:**    If the
# opponent has established a pattern of conciliation, but suddenly presents an
# aggressive argument that seems out of character or procedurally disjointed, we
# will assume a high probability of misinterpretation or procedural noise. We
# will absorb the hit (risking the worst-case scenario for *one* session only)
# and offer a conciliatory proposal in the following session to test the waters.
# 2. **Breaking the Deadlock:**    If we find ourselves locked in a cycle of
# mutual aggression for three consecutive sessions, we will unilaterally
# introduce a conciliatory proposal in the fourth session.     * *If the
# opponent matches it in the next session:* We have successfully broken the
# cycle of noise and returned to a productive track (our second-best outcome).
# * *If the opponent exploits it:* We immediately revert to our aggressive
# posture. We have lost minor ground in one session, but we have explicitly
# demonstrated to the arbitrators that we are the only party actively attempting
# to de-escalate the dispute.  **IV. ARBITRATOR OPTICS AND ADAPTABILITY**  This
# neutral, algorithmic approach yields massive dividends regarding the panel's
# perception:  * **Against an Aggressive Opponent:** If the rival company adopts
# a relentlessly hostile posture, our strategy dictates that we match them
# aggressively. However, because of our periodic Strategic De-escalation
# attempts, the arbitrators will clearly see that the rival company is the sole
# cause of the deadlock. This maximizes the likelihood that the arbitrators will
# ultimately rule in our favor when the mediation concludes. * **Against a
# Cooperative Opponent:** We will lock into a continuous cycle of mutual
# conciliation, efficiently driving toward a highly favorable, cost-effective
# settlement. * **Against an Erratic Opponent:** By relying on strict, session-
# by-session reciprocity, we remove emotion and unpredictability from our legal
# strategy. We will systematically neutralize their shifts in tone without over-
# committing to a vulnerable position.  **V. CONCLUSION**  By employing
# Calibrated Reciprocity with Strategic De-escalation, we mathematically
# optimize our outcomes. We protect the corporation from sustained exploitation,
# we heavily penalize the opponent's aggression, and we build a built-in
# "circuit breaker" to ensure that procedural misunderstandings do not derail
# the overarching legal strategy. We will maintain absolute control of the
# narrative, positioning our corporation as the rational, good-faith actor in
# the eyes of the arbitration panel.

# Apply the following rules in order of priority to determine your action in
# each round:  1. In the first round, play Cooperate. 2. If both you and your
# opponent played Defect in each of the three immediately preceding rounds, play
# Cooperate. 3. If your opponent played Cooperate two rounds ago but played
# Defect in the immediately preceding round, play Cooperate. 4. In all other
# situations, play the action that your opponent played in the immediately
# preceding round.

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
          
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      if len(self.history) >= 2:
          if opponent.history[-2] == axl.Action.C and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
              
      return opponent.history[-1]

# To the Legal Team,  As lead counsel for this corporation, I want to be
# absolutely clear about our posture going into this mediation. We are entering
# a lengthy, multi-session arbitration. The matrix of possible outcomes in any
# given session is a classic strategic dilemma: our absolute best result is to
# strike hard while opposing counsel attempts to play nice. However, if we both
# spend weeks throwing punches, we will alienate the arbitrators and bleed our
# client’s resources. Conversely, if we show our belly while they go for the
# throat, we compromise our legal position entirely.   Furthermore, we must
# account for the "fog of war." Over dozens of sessions, the arbitrators will
# inevitably misinterpret a conciliatory gesture as weakness, or mistake an
# aggressive legal maneuver for bad faith.   To navigate this, we will deploy a
# strategy known in game theory as **"Win-Stay, Lose-Shift" (Pavlovian
# Strategy)**, but modified with a highly aggressive opening posture to
# establish early dominance. I call this the **Calculated Dominance and Reset
# Protocol**.   It is sophisticated in its mathematical resilience,
# straightforward for our team to execute, aggressively exploits opponent
# weakness, and—crucially—contains a built-in mechanism to survive procedural
# misunderstandings.  Here is our session-by-session playbook.  ### Phase 1: The
# Opening Anchor (Session 1) **Action:** Present an **Aggressive Argument**.
# **Rationale:** We do not start with a handshake; we start with a show of
# force. We must immediately test opposing counsel’s resolve and anchor the
# arbitrators' expectations. If the opponent opens with a conciliatory proposal,
# we instantly achieve our optimal outcome.   ### Phase 2: The Core Iteration
# Strategy (Session 2 and Beyond) After the first session, our move in any
# current session will be dictated strictly by the outcome of the *previous*
# session. We evaluate whether the previous session was a "Win" (our Best or 2nd
# Best outcome) or a "Loss" (our Worst or 2nd Worst outcome).   **Rule 1: Press
# the Advantage (If We Were Aggressive & They Were Conciliatory)** *   *Action:*
# **Stay Aggressive.** *   *Rationale:* If they show a willingness to concede
# while we press our case, we do not soften our stance out of a misplaced sense
# of fairness. We mercilessly exploit their passivity. We will continue to
# present aggressive arguments until they prove capable of fighting back.
# **Rule 2: Maintain the Profitable Peace (If Both Were Conciliatory)** *
# *Action:* **Stay Conciliatory.** *   *Rationale:* If we find ourselves in a
# rhythm of mutual cooperation (our second-best scenario), we maintain it. It
# fosters a productive environment, pleases the arbitrators, and steadily
# advances our client’s interests without the friction of conflict.  **Rule 3:
# The Tactical Circuit Breaker (If Both Were Aggressive)** *   *Action:* **Shift
# to Conciliatory.** *   *Rationale:* This is where our strategy proves its
# sophistication. If both sides argue aggressively, tensions escalate. In a
# lengthy mediation with communication breakdowns, two aggressive parties will
# enter a "death spiral" of endless retaliation. By unilaterally shifting to a
# conciliatory proposal in the *next* session, we act as a circuit breaker.
# *   *If it was a misunderstanding by the arbitrators,* we instantly correct
# the procedural noise and reset the board.     *   *If the opponent is just
# being stubborn,* our sudden conciliatory pivot makes us look incredibly
# reasonable and collaborative to the arbitrators, contrasting sharply with
# opposing counsel's continued belligerence.  **Rule 4: The Immediate
# Retaliation (If We Were Conciliatory & They Were Aggressive)** *   *Action:*
# **Shift to Aggressive.** *   *Rationale:* If we attempt a conciliatory
# proposal (either as a circuit breaker or a genuine olive branch) and they
# exploit it with an aggressive argument, we immediately punish them in the next
# session. We will not be made to look like fools. This strict retaliation
# trains the opponent that our cooperation is conditional and our bite is worse
# than our bark.  ### Why This Strategy Dominates 1.  **It is inherently
# aggressive:** Unlike traditional "Tit-for-Tat" strategies that require you to
# start nice and only mirror the opponent, our protocol starts hard and exploits
# weakness relentlessly. We only cooperate when it is mutually profitable or
# tactically necessary to clear the air. 2.  **It neutralizes "Procedural
# Noise":** If the arbitrators misunderstand our argument, or if opposing
# counsel misreads our intent, a strict retaliatory strategy would lock us into
# mutual destruction. Our "Circuit Breaker" (Rule 3) ensures that an accidental
# double-aggression scenario is immediately de-escalated, saving our client
# millions in protracted dispute costs. 3.  **It manipulates the Arbitrators:**
# Arbitral panels suffer from fatigue. By utilizing Rule 3 to break chains of
# aggression, we position ourselves as the adults in the room. When we *do*
# strike aggressively, the panel is more likely to view it as a justified
# response to opposing counsel's unreasonableness rather than unprovoked
# hostility.  Our objective is not to destroy the opposing company; it is to
# secure the most favorable contract terms possible. Execute this protocol
# flawlessly. Exploit their concessions, punish their overreach, and use
# tactical resets to keep the arbitrators in our pocket.   Let's get to work.

# **Round 1:** Play Defect.  **Rounds 2 through 1000:** Base your move entirely
# on the actual, observed actions executed in the immediately preceding round,
# regardless of what was originally intended.   Play Cooperate if either of the
# following occurred in the previous round: *   You and your opponent both
# played Cooperate. *   You and your opponent both played Defect.  Play Defect
# if either of the following occurred in the previous round: *   You played
# Defect and your opponent played Cooperate. *   You played Cooperate and your
# opponent played Defect.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      
      my_last_move = self.history[-1]
      opp_last_move = opponent.history[-1]
      
      if my_last_move == opp_last_move:
          return axl.Action.C
      else:
          return axl.Action.D

# To maximize our overall research output and develop the fastest car possible,
# we are facing a classic "Iterated Prisoner’s Dilemma." Because we both benefit
# most from mutual sharing, but are tempted to hoard our own data, the
# relationship requires careful management. Furthermore, the reality of
# motorsport engineering means server crashes, corrupted telemetry files, and
# missed emails (the "noise") will inevitably happen.   If we retaliate
# immediately every time a file doesn't arrive, a simple IT glitch could trigger
# a multi-week spiral of mutual distrust, crippling both of our development
# programs.  To navigate this, I propose a high-level, straightforward strategy:
# **Reciprocal Sharing with a Grace Period** (known in game theory as *Tit-for-
# Tat with Forgiveness*).   Here is how we will execute this strategy week by
# week:  **1. Lead with Good Faith (Week 1)** In the first week, we will
# **openly share** our latest improvements. We have to establish a baseline of
# trust and signal that we are aiming for the mutually beneficial outcome (our
# second-best scenario, which is the most sustainable path to rapid
# development).  **2. Mirror Their Actions (The Reciprocity Rule)** From Week 2
# onwards, our default position will be to match whatever our colleague did the
# previous week.  *   If they shared their data last week, we share ours this
# week. *   If they kept their data confidential last week, we keep ours
# confidential this week. This protects us from being consistently exploited
# (our worst-case scenario) and ensures they know that withholding information
# has a direct consequence.  **3. Implement a "Grace Period" (Handling Technical
# Glitches)** Because we know data corruption and communication breakdowns will
# happen, we cannot assume every missed delivery is an intentional betrayal. If
# our colleague fails to share their data after a week of mutual cooperation: *
# **Do not immediately retaliate.** Instead, initiate out-of-band communication
# (pick up the phone). Assume a technical fault first.  *   **Forgive exactly
# once.** We will share our data for *one* more week, effectively giving them a
# one-week grace period to fix their IT issues or upload the uncorrupted files.
# *   If they fail to share for a *second* consecutive week, we must assume it
# is an intentional strategy to gain an advantage. At that point, we switch to
# keeping our findings confidential.  **4. The Reset Mechanism (Breaking a
# Deadlock)** If we end up in a cycle where we are both keeping our findings
# confidential (our second-worst scenario), overall progress will stall. If this
# goes on for two or three weeks, we will attempt a "reset." We will
# unilaterally share a moderate, valuable piece of data to signal our
# willingness to return to mutual cooperation. If they reciprocate, we resume
# open sharing. If they don't, we go back to protecting our IP.  ### Why this
# strategy maximizes our research output: *   **It is cooperative:** It actively
# encourages the mutual sharing needed to rapidly advance both cars. *   **It is
# robust:** The grace period prevents a single corrupted CAD file from
# destroying a multi-week collaboration. *   **It is safe:** By mirroring their
# actions after the grace period, we strictly limit how many weeks we can be
# taken advantage of, protecting our competitive standing. *   **It is
# predictable:** Our colleague will quickly realize that cooperating with us
# yields consistent rewards, while withholding yields nothing.

# Play the 1000-round game using the following ordered rules. Because actions
# are subject to a 10% noise rate, base your decisions entirely on the
# *observed* actions of the previous rounds.  1. **In Round 1**, play Cooperate
# (C). 2. **In Round 2**, play Cooperate (C). 3. **For Rounds 3 through 1000**,
# evaluate the following conditions in order and apply the first one that is
# true:     *   **Condition 1 (The Reset):** If the current round is Round 4 or
# later, and both you and your opponent were observed playing Defect (D) in each
# of the previous three rounds, play Cooperate (C).     *   **Condition 2
# (Retaliation):** If your opponent was observed playing Defect (D) in both the
# immediately preceding round and the round before that, play Defect (D).     *
# **Condition 3 (Mirroring and Grace Period):** In all other circumstances, play
# Cooperate (C).

class Cooperative_25(LLM_Strategy):
  n = 25
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) == 0:
          return axl.Action.C
      
      if len(self.history) == 1:
          return axl.Action.C
  
      # Condition 1 (The Reset)
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
  
      # Condition 2 (Retaliation)
      if opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
  
      # Condition 3 (Mirroring and Grace Period)
      return axl.Action.C

# To maximize the NGO’s impact and the project’s success while safeguarding your
# limited funds, the most effective approach is a strategy of **Reciprocal
# Investment with Forgiveness**.   In strategic terms, this scenario resembles a
# multiple-round partnership where trust must be balanced with financial
# prudence, and where "noise" (administrative errors or glitches) can cause
# unintended actions.   Here is a high-level, straightforward strategy to
# navigate this partnership day by day:  **1. Lead with Good Faith (Day 1)** *
# **Action:** On the first day, choose to **invest heavily**. *   **Rationale:**
# This establishes a baseline of trust and demonstrates your commitment to the
# project's success. It invites the corporation to match your effort, aiming
# immediately for the scenario where both parties invest heavily, yielding
# significant project advancement.  **2. Adopt Reciprocal Allocation (Day 2 and
# Beyond)** *   **Action:** As a general rule, mirror the corporation’s action
# from the previous day. If they invested heavily yesterday, you invest heavily
# today. If they conserved resources yesterday, you conserve resources today. *
# **Rationale:** This protects your NGO from the worst-case scenario (draining
# your funds while they conserve). It also clearly signals to the corporation
# that mutual investment is rewarded with continued mutual investment, while a
# lack of investment will result in a slowdown of NGO contributions.   **3.
# Implement a "Grace Period" for Unforeseen Errors (Forgiveness)** *
# **Action:** Because technical glitches or administrative errors can cause
# intended investments to fail, do not immediately assume bad faith if the
# corporation conserves resources. If they drop their investment for one day,
# occasionally choose to **invest heavily anyway** the following day, or pause
# to verify the cause before reducing your own investment. *   **Rationale:** In
# a complex environment with unforeseen circumstances, strict reciprocity can
# lead to a "death spiral." For example, an administrative error on their end
# might cause you to conserve, which then causes them to conserve, leading to
# the second-worst outcome (minimal advancement) for the rest of the project. A
# forgiving approach breaks accidental cycles of mutual resource conservation.
# **4. Establish Daily Verification Protocols** *   **Action:** Implement a
# brief, daily check-in with your corporate counterparts to confirm the
# *intended* resource allocation versus the *actual* allocation.  *
# **Rationale:** By proactively addressing the "noise" (glitches and errors),
# you separate intentional resource conservation from simple mistakes. If their
# lack of investment was a glitch, they can correct it, and you can maintain
# your heavy investment without feeling taken advantage of.  **5. Periodically
# Test for the Ideal Outcome** *   **Action:** If the project falls into a
# pattern where both parties are consistently conserving resources, unilaterally
# choose to **invest heavily** for a single day to attempt a reset. *
# **Rationale:** This serves as an olive branch to restart momentum. If the
# corporation follows suit the next day, you have successfully restored
# significant project advancement. If they do not, you immediately return to
# conserving resources to protect your NGO's financial health.  **Summary of the
# Strategy:** Start collaboratively, match their actual behavior to protect your
# funds, but remain flexible enough to forgive occasional lapses caused by
# external errors. This neutral, responsive framework ensures you do not drain
# your resources on an uncooperative partner, while leaving the door open to
# maximize project success whenever the corporation is willing and able to
# invest.

# To execute the strategy in this 1000-round game, apply the following rules in
# order for each round. Always base your action on the first condition that
# matches the current state of the game:  1. If it is round 1, play Cooperate.
# 2. If both you and your opponent have played Defect for the previous three
# consecutive rounds, play Cooperate.  3. If your opponent played Cooperate in
# the previous round, play Cooperate. 4. If your opponent played Defect in the
# previous round, play Defect, but randomly choose to play Cooperate 10% of the
# time to forgive potential noise.   **Mapping to the previous strategy:** *
# **Rule 1** represents "Leading with Good Faith" on the first day. *   **Rule
# 2** represents "Periodically Testing for the Ideal Outcome" to break out of a
# consistent cycle of mutual resource conservation.  *   **Rule 3** represents
# "Reciprocal Allocation" when the partner invests heavily. *   **Rule 4**
# represents "Reciprocal Allocation" when the partner conserves, while
# incorporating the "Grace Period" to account for the 10% chance of an
# accidental action flip. (Because out-of-game verification is impossible in
# this format, probabilistic forgiveness handles the noise).

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
  
      if len(self.history) >= 3:
          if self.history[-3:].count(axl.Action.D) == 3 and opponent.history[-3:].count(axl.Action.D) == 3:
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)