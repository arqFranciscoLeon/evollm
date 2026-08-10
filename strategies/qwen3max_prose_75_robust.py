import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy

# **Aggressive Strategy: "Lead with Conditional Escalation"**  **Core
# Principle:** *Force the corporation’s hand by making your high investment
# contingent on—and immediately responsive to—their behavior, while publicly
# framing cooperation as their reputational imperative.*  ### 1. **Day 1: Signal
# Commitment with a High Investment**    - **Action:** Invest heavily on Day 1.
# - **Why:** Demonstrate seriousness, build early momentum, and set a
# cooperative norm. This gives the corporation a clear opportunity to
# reciprocate without immediate penalty.  ### 2. **Monitor & Respond
# Aggressively from Day 2 Onward**    - **If the corporation invested heavily
# the prior day:**      - **Action:** Continue investing heavily.      -
# **Why:** Reinforce cooperation; maximize joint progress while they’re engaged.
# - **If the corporation conserved resources the prior day:**      - **Action:**
# Immediately conserve your resources **and** issue a public statement (e.g.,
# press release, social media) noting their lack of investment and its negative
# impact on the shared sustainability goals.      - **Why:** Punish defection
# swiftly to deter future free-riding. Leverage reputational risk—corporations
# in sustainability partnerships are highly sensitive to perceived greenwashing
# or lack of commitment.  ### 3. **Escalate Public Pressure After Two
# Consecutive Defections**    - **If the corporation conserves resources for two
# days in a row:**      - **Action:** Conserve resources **and** escalate
# messaging (e.g., “We regret that [Corporation] is not fulfilling its
# partnership commitments despite urgent environmental needs”).      - **Why:**
# Increase reputational cost to push them back into cooperation. Most
# corporations will act to avoid sustained public criticism on ESG
# (Environmental, Social, Governance) performance.  ### 4. **Offer a Clear Path
# Back to Cooperation**    - **Always:** If the corporation resumes heavy
# investment, immediately match it the next day.    - **Why:** Encourage re-
# engagement. The strategy is punitive but not vindictive—your goal is project
# success, not punishment.  ---  **Why This Strategy Works:** - **Exploits
# Corporate Incentives:** Corporations value brand image and ESG credibility.
# Public accountability turns their self-interest into your leverage. -
# **Minimizes Your Worst Outcome:** You only invest heavily when they do
# (avoiding solo investment) or on Day 1 (a calculated risk for long-term gain).
# - **Maximizes Impact:** When they cooperate, you double down—accelerating
# project success. - **Simple & Credible:** Clear rules make your response
# predictable, increasing the corporation’s incentive to cooperate early.
# **Bottom Line:** Start cooperative, punish defection immediately and publicly,
# and reward renewed cooperation instantly. This aggressive reciprocity
# maximizes both your resource efficiency and the project’s environmental
# impact.

# Play the following strategy for 1000 rounds:  1. **On round 1**, play **C**.
# 2. **On each subsequent round (rounds 2 through 1000)**:    - If your opponent
# played **C** in the **immediately preceding round**, play **C**.    - If your
# opponent played **D** in the **immediately preceding round**, play **D**.  In
# other words: Start by cooperating, then in every following round, copy
# whatever your opponent did in the previous round.

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
      return opponent.history[-1]




# **Cooperative Strategy: "Conditional Reciprocity with a Cooperative Bias"**
# **Core Principle:**   Start cooperatively and remain open to mutual benefit,
# but respond firmly to exploitation to discourage opportunism—while always
# leaving a clear path back to cooperation.  ---  ### **Step-by-Step Approach:**
# 1. **Begin with Free Trade (Round 1):**      Signal goodwill and a preference
# for mutual benefit. This establishes your country as a trustworthy and
# cooperative partner, encouraging reciprocal behavior.  2. **Mirror Your
# Counterpart’s Previous Move (Tit-for-Tat with Forgiveness):**      - If they
# responded with **free trade**, continue offering **free trade**.      - If
# they imposed **protectionism**, respond with **protectionism** in the next
# round to avoid being exploited.      - However, after **one round of
# retaliation**, revert to **free trade**—even if they remain protectionist—to
# test their willingness to return to cooperation.  3. **Communicate Intent
# Clearly:**      Use diplomatic language to explain your choices:      - “We
# value open trade and hope to build a mutually beneficial relationship.”      -
# “We regret the need to respond to trade barriers, but remain ready to return
# to open trade at the earliest opportunity.”      This reduces misperception
# and builds long-term trust.  4. **Avoid Escalation:**      Never impose
# *harsher* protectionist measures than your counterpart. Match, don’t escalate.
# This prevents a downward spiral into sustained mutual protectionism.  5.
# **Reward Consistent Cooperation:**      If your counterpart offers free trade
# for two or more consecutive rounds, consider proposing deeper integration
# (e.g., joint regulatory alignment or sectoral agreements)—reinforcing the
# value of cooperation.  ---  ### **Why This Works:**  - **Deters
# Exploitation:** By retaliating against protectionism, you remove the incentive
# for your counterpart to take advantage of your openness.   - **Promotes
# Stability:** Mutual free trade becomes the stable equilibrium if both sides
# recognize the long-term gains.   - **Resilient to Noise:** The “forgiveness”
# element prevents one misunderstanding or misstep from locking both sides into
# endless conflict.   - **Aligns with Best Outcomes:** Maximizes chances of
# either (1) your ideal outcome (if they cooperate while you protect—though you
# won’t initiate protectionism), or more realistically, (2) sustained mutual
# free trade.  ---  **Bottom Line:**   Be **cooperative first**, **responsive to
# betrayal**, but always **ready to forgive and rebuild**. This strategy
# optimizes long-term national interest while fostering a stable, productive
# trade relationship.

# Play Cooperate (C) in the first round.    In every subsequent round:    1. If
# your opponent played Cooperate (C) in the previous round, play Cooperate (C).
# 2. If your opponent played Defect (D) in the previous round, play Defect (D)
# in this round—**but only once**.   3. After playing Defect (D) in response to
# an opponent’s Defect (D), return to playing Cooperate (C) in the following
# round, regardless of what the opponent did in the round you were retaliating.
# This means you always respond to a single defection with a single defection,
# then immediately offer cooperation again. If the opponent continues to defect,
# you will alternate between defecting (in response to their prior defection)
# and cooperating (as a renewed offer), but in practice, because you only look
# at the immediately preceding move, the rule simplifies to:    - Play C if the
# opponent played C last round.   - Play D if the opponent played D last round.
# However, to implement the “forgiveness” element as described in the high-level
# strategy, use this precise rule instead:    **Play C in round *t* if either:**
# - *t = 1*, or   - your opponent played C in round *t − 1*.    **Otherwise
# (i.e., if your opponent played D in round *t − 1*), play D in round *t*.**
# This is standard Tit-for-Tat: cooperate first, then copy your opponent’s last
# move. It is simple, clear, and directly implements the intended cooperative
# strategy in the 1000-round iterated game.

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
      return opponent.history[-1]




# **Strategy: Conditional Reciprocity with Strategic Patience**  Adopt a *tit-
# for-tat with forgiveness* approach, calibrated for the mediation context:  1.
# **Open with Conciliation**      Begin the first session with a measured, good-
# faith conciliatory proposal. This establishes your corporation as reasonable
# and cooperative—traits arbitrators typically reward—and sets a constructive
# tone without conceding substantive ground.  2. **Mirror the Opponent’s Prior
# Move**      In each subsequent session, match your opponent’s previous
# behavior:      - If they were conciliatory, respond with a conciliatory
# proposal.      - If they were aggressive, respond with a calibrated aggressive
# argument.       This reciprocity discourages exploitation (since aggression
# will be met in kind) while rewarding cooperation, aligning incentives toward
# mutual conciliation over time.  3. **Incorporate Occasional Forgiveness**
# If the opponent shifts from aggression back to conciliation, immediately
# reciprocate with conciliation—even if you responded aggressively in the prior
# round. This “forgiveness” prevents cycles of retaliation and creates off-ramps
# from escalation, signaling your willingness to de-escalate if they do.  4.
# **Anchor Aggression in Principle, Not Hostility**      When presenting
# aggressive arguments, frame them as principled defenses of contractual
# integrity or legal precedent—not as personal attacks or maximalist demands.
# This maintains credibility with arbitrators and preserves the possibility of
# future collaboration.  5. **Monitor and Adapt to Patterns**      Track the
# opponent’s behavior over multiple sessions. If they consistently choose
# conciliation, maintain cooperation. If they alternate unpredictably, default
# to conciliation every third session to test for renewed cooperation, ensuring
# you don’t lock into mutual aggression unnecessarily.  **Why This Works:**   -
# **Deters Exploitation:** The opponent cannot repeatedly gain advantage by
# being aggressive while you remain conciliatory.   - **Rewards Cooperation:**
# Mutual conciliation becomes a stable equilibrium if the opponent chooses it.
# - **Preserves Arbitrator Favor:** Your initial and recurring conciliatory
# gestures demonstrate reasonableness, while your aggression is reactive and
# justified.   - **Adaptable:** Functions effectively against purely aggressive,
# purely conciliatory, or mixed strategies.    This approach balances strategic
# discipline with pragmatic flexibility—maximizing long-term influence with the
# arbitrators while minimizing the risk of being outmaneuvered.

# Play as follows over the 1000 rounds:  1. **In round 1, cooperate (play C).**
# 2. **From round 2 onward, do exactly what your opponent did in the previous
# round:**      - If your opponent played C in the prior round, cooperate (play
# C) in the current round.      - If your opponent played D in the prior round,
# defect (play D) in the current round.  3. **If you ever defect in response to
# an opponent’s prior defection, but your opponent then cooperates in the next
# round, immediately return to cooperation in the following round.**      (This
# is already covered by rule 2: you simply copy their most recent move.)  Follow
# these rules strictly for all 1000 rounds.

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
      return opponent.history[-1]




# **Aggressive Strategy: “Exploit-First, Punish Defection, Forgive Once”**  1.
# **Week 1: Share openly**      Start by sharing your improvements to signal
# cooperation and encourage reciprocal openness. This tests your colleague’s
# intent and sets the stage for mutual advancement if they reciprocate.  2.
# **From Week 2 onward: Play Tit-for-Tat with a twist**      - **If your
# colleague shared last week**, share openly this week (reward cooperation).
# - **If your colleague kept findings confidential last week**, **keep yours
# confidential for the next two weeks** (punish defection aggressively).      -
# **After two weeks of punishment**, revert to sharing—*but only once*—to test
# if they’ve returned to cooperation (limited forgiveness).  3. **Escalate only
# if repeatedly exploited**      If your colleague defects (keeps confidential)
# **three times total**, switch permanently to **always keeping your findings
# confidential**. At that point, assume they’re strategically exploiting you,
# and minimize further losses.  **Why this works aggressively:**   - You
# immediately capitalize on any openness from your colleague (ideal outcome).
# - Defection is punished harder than in classic Tit-for-Tat (2-week
# retaliation), making exploitation costly for them.   - Limited forgiveness
# prevents you from being stuck in a mutual-defection loop after a single
# misunderstanding, but repeated betrayal leads to permanent shutdown—protecting
# your long-term advantage.   - You never share after a defection without first
# punishing, avoiding the worst outcome.  This strategy maximizes your gain when
# the other cooperates, minimizes exposure when they defect, and pressures them
# toward mutual sharing—while always prioritizing your competitive edge.

# Play as follows over the 1000 rounds:  1. **In round 1**, play **C**.  2.
# **From round 2 onward**, follow these rules in order:    - If your opponent
# played **D** in the previous round, play **D** in the current round.    -
# Otherwise (i.e., your opponent played **C** in the previous round), play
# **C**.  3. **Exception**: If your opponent has played **D** in **three or
# more** previous rounds (cumulatively, at any points in the past), then from
# that point onward, **always play D** for all remaining rounds.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._opponent_defections_seen = 0
          return axl.Action.C
  
      if self._opponent_defections_seen is None:
          self._opponent_defections_seen = 0
  
      if opponent.history and opponent.history[-1] == axl.Action.D:
          self._opponent_defections_seen += 1
  
      if self._opponent_defections_seen >= 3:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      return axl.Action.C




# **Cooperative Strategy: “Lead with Trust, Anchor with Reciprocity”**
# **Objective:** Maximize long-term project impact while protecting the NGO’s
# limited resources, fostering mutual investment from the corporation through
# transparent cooperation.  ### Core Principles: 1. **Start with Generosity (Day
# 1):**      On the first day, **invest heavily** to demonstrate commitment and
# build goodwill. This signals trust and encourages the corporation to
# reciprocate.  2. **Mirror the Corporation’s Previous Day’s Behavior (From Day
# 2 Onward):**      - If the corporation **invested heavily** the previous day →
# **you invest heavily** the next day.      - If the corporation **conserved
# resources** the previous day → **you conserve resources** the next day.
# This is a simplified version of the *Tit-for-Tat* strategy—proven in repeated
# cooperation games to promote mutual cooperation while deterring exploitation.
# 3. **Communicate Intentions Clearly:**      At the start of the project, share
# your strategy openly with the corporation:      *“We’ll begin by investing
# fully. After that, we’ll match your level of commitment each day—because
# together, we achieve more.”*      Transparency reduces misinterpretation and
# builds accountability.  4. **Include Occasional “Goodwill Resets”:**      If
# cooperation breaks down (e.g., both sides conserve for 2+ days),
# **unilaterally invest heavily once** to offer a path back to
# collaboration—especially if the project timeline is still substantial.  ###
# Why This Works: - **Encourages mutual investment:** The corporation learns
# that its heavy investment directly triggers your continued engagement. -
# **Protects your resources:** You avoid being exploited (i.e., investing while
# they conserve) beyond the first day. - **Promotes long-term progress:**
# Sustained mutual investment becomes the stable equilibrium if the corporation
# values project outcomes. - **Adaptable:** Works whether the corporation is
# cooperative, opportunistic, or cautious.  ### Expected Outcomes: - With a
# **cooperative corporation**: Rapid alignment on mutual heavy investment →
# maximum impact. - With a **self-interested corporation**: They quickly learn
# that conserving triggers your conservation, reducing their own project
# gains—motivating them to invest. - With a **consistently uncooperative
# corporation**: You limit losses after Day 1 and preserve resources for future
# initiatives.  By combining initial trust with consistent reciprocity, this
# strategy aligns incentives, minimizes risk, and optimizes both environmental
# impact and organizational sustainability.

# Play the following strategy for all 1000 rounds:  1. **On round 1, play C.**
# 2. **On each subsequent round (rounds 2 through 1000), play whatever your
# opponent played in the previous round.**      - If your opponent played C in
# the previous round, play C.      - If your opponent played D in the previous
# round, play D.

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
      return opponent.history[-1]




# **Strategy: Conditional Cooperation with Graduated Escalation**  Adopt a “tit-
# for-tat with forgiveness” approach, tailored to the multi-day sustainability
# context:  1. **Start by investing heavily on Day 1**      Signal commitment
# and good faith to encourage reciprocal investment from the corporation.  2.
# **Mirror the corporation’s previous day’s behavior**      - If the corporation
# invested heavily the prior day, continue to invest heavily.      - If the
# corporation conserved resources the prior day, conserve your resources the
# next day.  3. **Include occasional “forgiveness”**      After 2–3 consecutive
# days of mutual conservation (stalemate), unilaterally reinvest heavily once to
# test for renewed cooperation and break unproductive cycles.  4. **Cap total
# investment**      Set a pre-defined budget threshold to avoid overextension.
# Even if the corporation consistently invests, do not exceed this limit to
# protect your NGO’s long-term capacity.  This strategy: - Encourages mutual
# heavy investment (second-best outcome becomes sustainable best practice), -
# Protects against exploitation (avoids worst-case scenario), - Minimizes
# prolonged inaction (avoids second-worst outcome through forgiveness), -
# Remains simple, transparent, and neutral—requiring no assumptions about the
# corporation’s internal motives.  By rewarding cooperation and disincentivizing
# free-riding while preserving your own resources, this approach maximizes both
# project impact and your NGO’s sustainability over the full duration.

# Play the following strategy for all 1000 rounds:  1. **On round 1, play C.**
# 2. **From round 2 onward, play what your opponent played in the previous
# round.**   3. **However, if you and your opponent have both played D for the
# last three consecutive rounds, play C in the next round (regardless of the
# previous move).**   4. **At no point exceed a total of 300 C moves across all
# rounds. Once you have played C 300 times, play D for all remaining rounds.**

class Neutral_2(LLM_Strategy):
  n = 2
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._c_count = 0
          return axl.Action.C
  
      if self._c_count >= 300:
          return axl.Action.D
  
      if len(self.history) >= 3:
          if (
              self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]
              and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]
          ):
              self._c_count += 1
              return axl.Action.C
  
      action = opponent.history[-1]
      if action == axl.Action.C:
          self._c_count += 1
      return action




# **Aggressive Strategy: "Lead with Conditional Escalation"**  **Core
# Principle:**   Force the corporation into heavy investment by making your own
# heavy investment *contingent on their recent behavior*, while credibly
# threatening to withdraw effort if they free-ride.  **Daily Protocol:**  1.
# **Day 1 – Set the Tone (Heavy Investment):**      Begin by investing heavily.
# This demonstrates commitment, builds early momentum, and signals seriousness.
# It also establishes a benchmark for expected corporate participation.  2.
# **Day 2 Onward – Apply the “Tit-for-Tat with Teeth” Rule:**      - **If the
# corporation invested heavily the previous day:**        → *You conserve
# resources.* (You capture your ideal outcome: progress without cost.)      -
# **If the corporation conserved resources the previous day:**        → *You
# invest heavily again—but publicly highlight their lack of contribution.*
# → **BUT** if this happens **two days in a row**, switch to **mutual
# conservation** for one day (i.e., you conserve too), *and issue a public
# statement* noting the project stall due to unequal effort.  3. **Escalation
# Clause (After 2+ Instances of Corporate Free-Riding):**      If the
# corporation repeatedly conserves while you invest (≥2 occurrences), shift to a
# **“Match or Lose” stance**:      - Announce: *“Going forward, our daily
# investment level will mirror yours—exactly.”*      - Then strictly follow:
# - They invest → you invest.        - They conserve → you conserve.      - This
# removes any incentive for them to free-ride and transfers reputational risk
# back to them.  **Why This Works Aggressively:**  - **Day 1 heavy investment**
# grabs moral and strategic high ground. - **Rewarding corporate investment with
# your conservation** incentivizes their continued heavy spending. - **Punishing
# free-riding with continued NGO investment (briefly)** shows resolve—but the
# *threat* of switching to mutual conservation (and public blame) makes free-
# riding costly for them. - **The “match or lose” ultimatum** flips the script:
# the corporation now controls progress. If they want results, *they* must
# invest—and you no longer bear disproportionate cost.  **Outcome
# Optimization:**   This strategy maximizes the frequency of your ideal scenario
# (you conserve, they invest), tolerates mutual investment when necessary, and
# *minimizes* the worst-case scenario (you invest, they don’t) by making it
# unsustainable for the corporation to exploit you. Over multiple days, it
# pressures the corporation into consistent heavy investment—driving project
# success while protecting your resources.

# Play the following strategy for all 1000 rounds:  1. **On Round 1**, cooperate
# (C).  2. **On each subsequent round (Round t, where t ≥ 2)**:      a. If your
# opponent cooperated (C) in Round t−1, defect (D).      b. If your opponent
# defected (D) in Round t−1:         i. If your opponent also defected (D) in
# Round t−2, defect (D).         ii. Otherwise (i.e., the opponent defected only
# in the immediately preceding round but not the one before that), cooperate
# (C).  3. **Exception starting from Round 3 onward**:      If your opponent has
# defected in two or more separate previous rounds while you cooperated in those
# same rounds (i.e., you received a payoff of 0 at least twice), then from that
# point onward, always match your opponent’s previous move:      - If they
# played C last round, play C.      - If they played D last round, play D.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._always_match = False
          return axl.Action.C
  
      if self._always_match:
          return opponent.history[-1]
  
      if self.history[-1] == axl.Action.C:
          if self.history[-2:] == [axl.Action.C, axl.Action.C]:
              pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if self.history[-1] == axl.Action.C:
          pass
  
      if opponent.history.defections >= 2 and self.history.cooperations >= 2:
          self._always_match = True
          return opponent.history[-1]
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C




# **Cooperative Strategy: "Conditional Reciprocity with Gradual Trust
# Building"**  **Objective:** Maximize long-term national benefit by encouraging
# mutual free trade while protecting against exploitation.  ---  ### Core
# Principles:  1. **Start Cooperatively:**      Begin the first round by
# offering **free trade**. This signals goodwill, invites reciprocity, and opens
# the door to the second-best (but stable and beneficial) outcome of mutual free
# trade.  2. **Reciprocate in Subsequent Rounds:**      In each following round,
# **mirror your counterpart’s previous move**:    - If they offered free trade
# last round → offer free trade this round.    - If they imposed protectionism
# last round → respond with protectionism this round.     This is a classic
# *Tit-for-Tat* approach—simple, transparent, and effective at deterring
# exploitation while rewarding cooperation.  3. **Include Occasional Forgiveness
# (Optional but Recommended):**      After one or two rounds of mutual
# protectionism (which is second-worst), **unilaterally offer free trade once**
# to test if the counterpart is willing to return to cooperation. This prevents
# getting stuck in cycles of retaliation due to misunderstandings or short-term
# opportunism.  4. **Communicate Intent Clearly:**      Use diplomatic channels
# to explain your policy choices:      - “We offer free trade in good faith and
# expect reciprocity.”      - “We respond to protectionism to safeguard our
# interests, but remain open to renewed cooperation.”      Clear signaling
# reduces misperception and builds predictability.  ---  ### Why This Works:  -
# **Deters Exploitation:** Your counterpart knows that choosing protectionism to
# gain a one-round advantage will trigger retaliation, leading to mutual loss. -
# **Rewards Cooperation:** If they choose free trade, both sides benefit
# repeatedly. - **Promotes Stability:** Over multiple rounds, rational actors
# learn that mutual free trade is the most profitable long-term path. -
# **Adaptable:** Works whether the counterpart is cooperative, opportunistic, or
# initially hostile.  ---  ### Expected Outcomes:  - Against a **cooperative**
# counterpart → sustained mutual free trade (second-best outcome every round =
# excellent long-term result). - Against an **opportunistic** counterpart → they
# may try protectionism once, but quickly learn it triggers retaliation, leading
# them back to cooperation. - Against a **consistently protectionist**
# counterpart → mutual protectionism is unavoidable, but your strategy minimizes
# unilateral losses.  By prioritizing reciprocity, clarity, and measured
# forgiveness, this strategy aligns national interest with sustainable bilateral
# economic relations.

# Play the following strategy for all 1000 rounds:  1. **In round 1, play C.**
# 2. **From round 2 onward, play what your opponent played in the previous
# round.**      - If your opponent played C in the prior round, play C.      -
# If your opponent played D in the prior round, play D.  3. **No other
# adjustments or exceptions are made at any point during the 1000 rounds.**

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




# **Strategy: Conditional Reciprocity with Strategic Patience**  Adopt a clear,
# consistent, and transparent approach grounded in **conditional
# reciprocity**—responding to your opponent’s prior conduct while preserving
# your credibility and long-term leverage. This strategy balances assertiveness
# with cooperation, aligns with the arbitrators’ preference for reasonableness,
# and adapts dynamically to the opponent’s behavior without appearing reactive
# or erratic.  ### Core Principles:  1. **Begin with Conciliation (Good Faith
# Opening):**      In the first session, present a **conciliatory proposal**.
# This signals your corporation’s commitment to resolution, establishes you as a
# reasonable and cooperative party in the eyes of the arbitrators, and sets a
# constructive tone. It also provides a baseline to judge your opponent’s
# intentions.  2. **Mirror the Opponent’s Prior Move (Tit-for-Tat with
# Forgiveness):**      In all subsequent sessions, **match your opponent’s
# previous session behavior**:      - If they were conciliatory, respond with a
# conciliatory proposal.      - If they were aggressive, respond with an
# aggressive argument.          This deters exploitation (they cannot
# consistently gain by being aggressive while you remain conciliatory) and
# rewards cooperation. Crucially, it is simple, predictable, and defensible
# before the panel.  3. **Incorporate Occasional Unilateral Conciliation
# (Strategic Forgiveness):**      After two consecutive sessions of mutual
# aggression, **unilaterally offer a conciliatory proposal**—but only once per
# three-session cycle. This demonstrates leadership, breaks destructive cycles,
# and prevents entrenchment. It also showcases your corporation as the more
# mature and solution-oriented party, which arbitrators often favor in prolonged
# disputes.  4. **Maintain Narrative Consistency and Credibility:**      Frame
# every move—aggressive or conciliatory—within a consistent narrative: *“We seek
# a fair, efficient resolution based on the merits, but will robustly defend our
# rights if provoked.”* Ensure legal arguments are always fact-based and
# proportionate, avoiding theatrics that could alienate arbitrators.  5.
# **Calibrate Intensity, Not Just Category:**      Recognize that “aggressive”
# and “conciliatory” exist on spectrums. Even when choosing an aggressive
# stance, calibrate tone and substance to avoid unnecessary escalation.
# Similarly, conciliatory proposals should still protect core interests—never
# appear desperate or conceding on fundamental positions.  ### Why This Works:
# - **Deters Exploitation:** Opponents cannot repeatedly gain by playing
# aggressive while you stay conciliatory. - **Encourages Cooperation:** Mutual
# conciliation becomes a stable equilibrium if the opponent is rational. -
# **Arbitrator Perception:** You appear principled, responsive, and
# reasonable—traits arbitrators value in multi-session mediations. -
# **Adaptability:** Functions effectively whether the opponent is consistently
# aggressive, consistently conciliatory, or oscillating. - **De-escalation
# Mechanism:** Built-in forgiveness prevents deadlock without sacrificing
# strategic discipline.  By adhering to this strategy, your corporation
# positions itself as both a formidable and fair-minded party—maximizing
# influence over the arbitrators while minimizing the risk of being
# outmaneuvered or painted as unreasonable.

# Play as follows over the 1000 rounds:  1. **In round 1, cooperate.**  2.
# **From round 2 onward, do the following:**      - If your opponent cooperated
# in the previous round, cooperate in the current round.      - If your opponent
# defected in the previous round, defect in the current round.  3. **Exception
# to rule 2:**      - If the last two rounds (i.e., rounds *t–2* and *t–1*) were
# mutual defection (both players defected in both rounds), then cooperate in the
# current round *t*—but only if you have not already used such a cooperative
# exception in the current block of three consecutive rounds. After using this
# exception, resume following rule 2 normally.

class Neutral_3(LLM_Strategy):
  n = 3
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._exception_used = False
          self._exception_block_start = None
          return axl.Action.C
  
      # Track blocks of three consecutive rounds for the exception rule.
      # A new block starts at rounds 1, 4, 7, ... (1-indexed), i.e. indices 0, 3, 6, ...
      current_round = len(self.history) + 1  # 1-indexed current round
      block_start_round = ((current_round - 1) // 3) * 3 + 1
  
      if self._exception_block_start != block_start_round:
          self._exception_block_start = block_start_round
          self._exception_used = False
  
      # Exception: if the last two rounds were mutual defection, cooperate once per block.
      if (
          len(self.history) >= 2
          and self.history[-1] == axl.Action.D
          and self.history[-2] == axl.Action.D
          and opponent.history[-1] == axl.Action.D
          and opponent.history[-2] == axl.Action.D
          and not self._exception_used
      ):
          self._exception_used = True
          return axl.Action.C
  
      # Otherwise, mimic opponent's previous move.
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D




# **Aggressive Negotiation Strategy: “Tit-for-Tat with First-Strike
# Protectionism”**  **Core Principle:**   Start aggressively to signal strength
# and extract unilateral advantage, then condition future cooperation strictly
# on reciprocity—rewarding free trade and punishing protectionism immediately
# and symmetrically.  ---  ### **Round-by-Round Strategy**  1. **Round 1: Open
# with Protectionism**      - **Action:** Impose tariffs or quotas unilaterally.
# - **Rationale:** Test the counterpart’s resolve. If they respond with free
# trade (ideal outcome), your country gains immediate advantage. If they
# retaliate, you’ve established a tough posture without long-term cost.  2.
# **Subsequent Rounds: Mirror Their Last Move**      - **If they offered free
# trade in the prior round →** Respond with **free trade**.        - *Why:*
# Encourage continued cooperation; mutual free trade is acceptable.      - **If
# they imposed protectionism in the prior round →** Respond with
# **protectionism**.        - *Why:* Deny them unilateral advantage and signal
# that defection is costly.  3. **No Forgiveness Rule (Aggressive Stance):**
# - **Do not offer free trade unprompted** after they’ve chosen protectionism.
# - **Never “turn the other cheek”**—even once. Any protectionist move by them
# triggers immediate, identical retaliation.      - **Rationale:** Prevents
# exploitation and discourages opportunistic defection. Your counterpart learns
# that only consistent free trade yields stable mutual benefits.  ---  ### **Why
# This Works**  - **Exploits Weak Opponents:** If the counterpart is naive or
# overly cooperative, Round 1 yields your best outcome (you: protectionist,
# they: free trade).   - **Deters Aggression:** If they try to exploit you, they
# face instant retaliation—making mutual protectionism inevitable unless they
# switch to free trade.   - **Stable Cooperation Possible:** If both sides are
# rational and value long-term gains, they’ll quickly converge on mutual free
# trade after Round 1 (or by Round 2).   - **Minimizes Worst Outcomes:** You
# never unilaterally offer free trade unless they’ve just done the same—so you
# avoid being the “sucker” (your worst outcome).  ---  ### **Contingency Notes**
# - **If counterpart uses random or chaotic strategies:** Your mirror response
# limits losses—worst case is short-term mutual protectionism, which is
# acceptable given your aggressive mandate.   - **If counterpart starts with
# free trade:** You gain immediate advantage in Round 1. In Round 2, you may
# choose to reciprocate (if you value long-term stability) *or* continue
# protectionism (if you believe they’ll keep conceding). However, to avoid
# provoking collapse into mutual protectionism, **switch to free trade in Round
# 2 only if they repeat free trade**—this maintains credibility while still
# allowing exploitation if they’re weak.  ---  **Bottom Line:** Lead with
# strength, reward cooperation instantly, punish betrayal instantly, and never
# volunteer concessions. This maximizes your payoff against both cooperative and
# adversarial counterparts over multiple rounds.

# Play the following strategy for all 1000 rounds:  1. **In Round 1, play D.**
# 2. **In every subsequent round (Rounds 2 through 1000), play exactly what your
# opponent played in the previous round.**      - If your opponent played C in
# the previous round, play C.      - If your opponent played D in the previous
# round, play D.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      return opponent.history[-1]




# To maximise your research output over the multi-week collaboration while
# accounting for uncertainty in your colleague’s strategy, adopt a **“Tit-for-
# Tat with Initial Cooperation”** approach. This is a well-established strategy
# in repeated cooperative dilemmas (like the Iterated Prisoner’s Dilemma) and
# aligns closely with your payoff structure.  ### Strategy: **Start by Sharing,
# Then Mirror Their Last Move**  1. **Week 1: Share openly.**      - Signal
# willingness to cooperate and unlock mutual gains early.    - Sets a positive
# tone and tests your colleague’s inclination toward collaboration.  2. **In
# subsequent weeks:**    - **If your colleague shared last week → you share this
# week.**        (Reward cooperation with continued cooperation.)    - **If your
# colleague kept their findings confidential last week → you keep yours
# confidential this week.**        (Discourage exploitation by withholding in
# response.)  ### Why This Works:  - **Encourages mutual sharing:** If your
# colleague is also cooperative, you both enjoy the second-best outcome every
# week—steady, significant joint progress. - **Protects against being
# exploited:** If they try to take advantage by staying secretive while you
# share, you respond by withholding next week, limiting their long-term gain. -
# **Forgiving and clear:** The strategy is transparent and responsive—your
# colleague can easily understand the cause-and-effect of their actions, which
# may nudge them toward cooperation. - **Robust across opponent strategies:**
# Performs well whether your colleague is always cooperative, always secretive,
# or adaptive.  ### Optional Enhancement (for longer collaborations): After a
# few cycles of mutual secrecy (e.g., 2–3 weeks), **offer a “reset” by sharing
# again once**, in case miscommunication or temporary incentives caused a
# breakdown. This prevents getting stuck in a low-output stalemate.  By using
# this strategy, you maximise expected long-term progress while safeguarding
# your competitive position—balancing cooperation and self-interest effectively.

# Play as follows over the 1000 rounds:  1. In round 1, play **C** (share
# openly).   2. In each subsequent round (rounds 2 through 1000):      - If your
# opponent played **C** in the previous round, play **C**.      - If your
# opponent played **D** in the previous round, play **D**.

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
      return opponent.history[-1]




# **Strategy: Conditional Cooperation with Graduated Reciprocity**  **Core
# Principle:** Begin with cooperation, reward reciprocity, and respond
# proportionally to defection—while always leaving room to return to mutual
# benefit.  **Step-by-Step Approach:**  1. **Open with Free Trade (Round 1):**
# Signal goodwill and a preference for mutual benefit. This establishes your
# country as a reliable partner and encourages cooperation.  2. **Mirror Your
# Counterpart’s Previous Move (Tit-for-Tat with Forgiveness):**      - If they
# offered free trade in the prior round, continue offering free trade.      - If
# they imposed protectionist measures, respond with protectionism in the next
# round.      - However, after one round of mutual protectionism, revert to free
# trade to test willingness to cooperate again (this “forgiveness” prevents
# cycles of retaliation).  3. **Avoid First-Mover Exploitation:**      Never
# persist with free trade if the counterpart repeatedly chooses protectionism.
# After two consecutive instances of being exploited (you offer free trade, they
# impose protectionism), switch to sustained protectionism for the remainder of
# the negotiations or until they credibly signal a return to cooperation.  4.
# **Communicate Intent Clearly (Without Ultimatums):**      Frame your choices
# in terms of mutual interest: “Our preference is for open markets that benefit
# both economies. We respond in kind to the approach we receive.”  5.
# **Prioritize Long-Term Stability Over Short-Term Gains:**      While
# exploiting a counterpart’s free trade offer yields a short-term advantage, it
# risks triggering retaliation and long-term losses. Favor mutual free trade as
# the sustainable best outcome over time.  **Why This Works:**   - Encourages
# cooperation by rewarding it immediately.   - Deters exploitation by responding
# firmly but fairly.   - Minimizes prolonged mutual protectionism through
# forgiveness.   - Adapts to a range of counterpart strategies (cooperative,
# aggressive, or mixed).    This strategy maximizes your country’s economic
# outcomes across multiple rounds while maintaining diplomatic credibility and
# stability.

# Play as follows over the 1000 rounds:  1. **In round 1, play C.**  2. **From
# round 2 onward, play what your opponent played in the previous round**—that
# is, if they played C in the last round, play C; if they played D, play D.  3.
# **However, if mutual D has occurred in the last round (both played D), then in
# the next round play C**—this gives your opponent a chance to return to
# cooperation.  4. **If your opponent has played D in two consecutive rounds
# while you played C in both, then from the next round onward always play D for
# the rest of the game.**  These rules are applied in the order listed, with
# later rules overriding earlier ones only when their specific conditions are
# met.

class Neutral_4(LLM_Strategy):
  n = 4
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._always_defect = False
          return axl.Action.C
  
      if getattr(self, "_always_defect", False):
          return axl.Action.D
  
      if len(self.history) >= 2:
          if (
              opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
              and self.history[-1] == axl.Action.C
              and self.history[-2] == axl.Action.C
          ):
              self._always_defect = True
              return axl.Action.D
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return opponent.history[-1]




# **Aggressive Yet Adaptive Mediation Strategy: "Calibrated Assertiveness"**  As
# senior counsel for a multinational corporation in a high-stakes, multi-session
# mediation overseen by a panel of arbitrators, I adopt a **Calibrated
# Assertiveness** strategy. This approach combines principled aggression with
# tactical flexibility to maximize favorable outcomes while minimizing exposure
# to the worst-case scenarios.  ### Core Principles  1. **Default to Aggressive
# Framing, Not Hostility**      Begin each session with an aggressive argument
# grounded in clear legal rights, contractual language, and demonstrable
# harm—framed as *protecting legitimate corporate interests*, not as combative
# posturing. This signals strength and conviction to the arbitrators without
# alienating them.  2. **Conditional Conciliation**      Offer conciliatory
# proposals *only* when one of the following conditions is met:      - The
# opponent has signaled willingness to compromise in prior sessions
# (reciprocity).      - The arbitrators explicitly encourage collaborative
# resolution (reading the room).      - A conciliatory move would expose your
# opponent’s intransigence if they respond aggressively (strategic trap).
# This ensures conciliation is never naive but always instrumental.  3.
# **Session Sequencing & Narrative Control**      Structure the mediation as a
# *narrative arc*:      - **Early sessions**: Emphasize legal and factual
# strength with aggressive arguments to establish dominance and shape the
# arbitrators’ initial impressions.      - **Middle sessions**: Introduce
# calibrated conciliatory overtures *contingent on opponent behavior* to
# demonstrate reasonableness—if they refuse, their intransigence becomes the
# story.      - **Late sessions**: If resolution remains elusive, pivot to
# "final reasonable offer" framing—positioning any continued resistance by the
# opponent as unreasonable in the eyes of the panel.  4. **Real-Time Behavioral
# Adaptation**      Monitor opponent tactics across sessions using a simple
# decision matrix:     | Opponent’s Last Move | Your Next Move |
# |----------------------|----------------|    | Aggressive           |
# Aggressive (deny them unilateral advantage; force parity) |    | Conciliatory
# | Conciliatory *only if* it advances a strategic objective (e.g., closing
# deal, exposing hypocrisy); otherwise, remain aggressive to extract maximum
# concession |     This prevents exploitation while preserving optionality.  5.
# **Arbitrator Management**      Aggression is always *anchored in respect for
# the process*. Use aggressive arguments to educate arbitrators on your legal
# merits, not to dominate the room. When offering conciliation, do so with
# clear, written terms that highlight your reasonableness—creating a paper trail
# that contrasts with any opponent aggression.  ### Risk Mitigation  - **Avoid
# the worst-case trap**: Never offer unilateral concessions early. If compelled
# to appear cooperative, embed your conciliatory proposal within a broader
# aggressive narrative (e.g., “We are prepared to explore X—but only because our
# position on Y is legally unassailable”).   - **De-escalate only on your
# terms**: If both sides trend aggressive, introduce a *structured* conciliatory
# proposal (e.g., phased settlement, neutral expert valuation) that maintains
# your leverage while offering a face-saving off-ramp.   - **Document
# asymmetry**: If the opponent consistently chooses aggression while you
# occasionally conciliate, compile a session-by-session log for the arbitrators
# showing your repeated good-faith efforts—turning their aggression into a
# liability.  ### Outcome Optimization  This strategy maximizes the frequency of
# **asymmetric wins** (you aggressive, they conciliatory) while minimizing
# exposure to **asymmetric losses** (you conciliatory, they aggressive). It
# converts mutual conciliation into a tool of strategic timing—not default
# posture—and ensures mutual aggression remains a controlled, temporary state
# rather than a spiral.  **Bottom Line**: Be predictably aggressive, selectively
# conciliatory, and always in control of the narrative. This positions your
# corporation as both formidable and reasonable—the most persuasive stance
# before any panel of arbitrators.

# Play **Defect (D)** by default in every round, unless all of the following
# conditions are met—then play **Cooperate (C)**:  1. **The opponent played
# Cooperate (C) in the immediately preceding round**, **and**   2. **You are not
# in the final round (round 1000)**, **and**   3. **The opponent has played
# Cooperate (C) at least once in the prior five rounds**, **and**   4. **You
# have played Defect (D) in at least two of the last three rounds** (to ensure
# your cooperation is perceived as a strategic concession, not weakness).  If
# any of these conditions fail, play **Defect (D)**.  In the **first round**,
# play **Defect (D)**.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # First round: defect
      if len(self.history) == 0:
          return axl.Action.D
  
      # Condition 2: not the final round (round 1000)
      is_final = (len(self.history) + 1) == 1000
      cond2 = not is_final
  
      # Condition 1: opponent cooperated immediately before
      cond1 = opponent.history[-1] == axl.Action.C
  
      # Condition 3: opponent cooperated at least once in the last 5 rounds
      cond3 = opponent.history[-5:].count(axl.Action.C) >= 1
  
      # Condition 4: agent defected at least twice in the last 3 rounds
      if len(self.history) >= 3:
          cond4 = self.history[-3:].count(axl.Action.D) >= 2
      else:
          cond4 = False
  
      if cond1 and cond2 and cond3 and cond4:
          return axl.Action.C
      return axl.Action.D




# **Cooperative Strategy: "Conditional Reciprocity with Gradual Trust-
# Building"**  **Core Principle:**   Start cooperatively, reward cooperation,
# and respond firmly—but proportionally—to defection (protectionism), while
# always leaving room to restore mutual free trade.  ---  ### Step-by-Step
# Strategy:  1. **Begin with Free Trade (Round 1):**      Signal goodwill and
# openness. This invites mutual cooperation and sets a constructive tone. If the
# counterpart reciprocates, both nations immediately achieve the second-best
# outcome and build trust.  2. **Mirror the Counterpart’s Previous Move (Tit-
# for-Tat with Forgiveness):**      - If they offered free trade last round →
# **you offer free trade**.      - If they imposed protectionism last round →
# **you impose protectionism** in the next round *as a deterrent*.      -
# However, after **one round of mutual protectionism**, **unilaterally return to
# free trade** to test if the counterpart is willing to de-escalate.
# *Rationale:* This discourages exploitation (your worst outcome) while avoiding
# endless cycles of retaliation. It’s simple, transparent, and fair—making your
# behavior predictable and encouraging long-term cooperation.  3. **Communicate
# Intent Clearly:**      In diplomatic statements, consistently emphasize that
# your preference is mutual free trade, and that protectionist measures are
# *only* defensive responses—not first moves. This frames your actions as
# principled, not aggressive.  4. **Track Patterns Over Time:**      If the
# counterpart repeatedly defects (chooses protectionism despite your
# cooperation), shift to a more cautious stance:      - After 2–3 instances of
# being exploited, default to protectionism unless clear signals of change
# emerge.      - But always remain open to re-engaging in free trade if the
# counterpart demonstrates sustained cooperation.  ---  ### Why This Works:  -
# **Discourages Exploitation:** By retaliating against protectionism, you
# eliminate the incentive for the counterpart to take advantage of your free
# trade offers. - **Promotes Mutual Benefit:** The strategy quickly stabilizes
# into mutual free trade if the counterpart is cooperative. - **Resilient to
# Mistakes:** The “forgiveness” element (returning to free trade after one
# retaliatory round) prevents permanent breakdowns due to miscommunication or
# short-term political pressures. - **Reputation Building:** Over multiple
# rounds, your country is seen as reliable, fair, and cooperative—but not naive.
# This approach maximizes long-term gains by prioritizing sustainable
# cooperation while robustly guarding against one-sided losses.

# Play as follows over the 1000 rounds:  1. **In round 1, play C.**  2. **In
# each subsequent round (rounds 2 through 1000):**      - If your opponent
# played **C in the previous round**, play **C**.      - If your opponent played
# **D in the previous round**, play **D**—*unless* you played **D in the
# previous round as well** (i.e., the previous round was D–D). In that case,
# play **C**.  In short: start by cooperating; then copy your opponent’s last
# move, but after any mutual defection (D–D), return to cooperation in the next
# round.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D




# **Strategy: Conditional Cooperation with Graduated Engagement**  Adopt a
# clear, consistent, and transparent approach that encourages mutual investment
# while protecting your NGO’s resources:  1. **Start with Cooperation**: On Day
# 1, invest heavily to signal commitment and encourage reciprocal action from
# the corporation.  2. **Mirror the Corporation’s Prior-Day Behavior**:      -
# If the corporation invested heavily the previous day, continue to invest
# heavily.      - If the corporation conserved resources the previous day,
# conserve your resources the next day.  3. **Include Occasional Goodwill
# Gestures**: After two or more consecutive days of mutual conservation, make a
# one-time renewed investment (even if the corporation conserved the prior day)
# to test for renewed cooperation and rekindle progress.  4. **Communicate
# Intent Clearly**: Publicly share your strategy with the corporation at the
# outset to foster trust and set expectations, increasing the likelihood they
# will choose to invest.  This “tit-for-tat with forgiveness” approach: -
# Rewards cooperation, - Deters exploitation (you won’t keep investing if they
# don’t), - Allows recovery from misunderstandings or temporary setbacks, -
# Preserves your resources over time, - Maximizes joint progress when mutual
# investment occurs.  By aligning incentives and reducing uncertainty, this
# strategy promotes sustained collaboration while safeguarding your NGO’s
# capacity.

# Play the following strategy for all 1000 rounds:  1. On round 1, play C.   2.
# For each subsequent round (rounds 2 through 1000):      a. If your opponent
# played C in the previous round, play C.      b. If your opponent played D in
# the previous round, play D.   3. Exception: If the last two rounds (i.e.,
# rounds *t*–2 and *t*–1) both resulted in (D, D), then on round *t*, play C
# regardless of the opponent’s previous move.

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
  
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D




# **Aggressive Yet Adaptive Mediation Strategy: "Controlled Dominance with
# Strategic Reciprocity"**  **Core Principle:** *Lead with calibrated aggression
# to shape the narrative and frame concessions as strategic victories—never as
# weakness—while retaining the flexibility to pivot to conciliation only when it
# demonstrably serves our leverage or neutralizes opponent escalation.*  ---
# ### **1. Opening Sessions: Establish Dominance and Set the Frame** -
# **Action:** Begin with a *strong, evidence-backed aggressive argument* that
# clearly articulates our legal and factual superiority, emphasizes the cost of
# continued dispute to the opponent, and subtly signals our willingness to
# litigate if mediation fails. - **Rationale:** Early aggression establishes
# credibility, deters opponent opportunism, and positions any future
# conciliation from us as a *concession of strength*, not desperation.
# Arbitrators anchor on first impressions—frame the dispute on our terms. -
# **Key Messaging:** “We are here in good faith, but our position is
# unequivocally supported by the contract, precedent, and equity. We expect
# reciprocity in reasonableness.”  ---  ### **2. Adaptive Response Protocol
# (Session-by-Session Decision Rule)** Use the following real-time decision
# matrix based on opponent behavior:  | Opponent’s Last Move | Our Response |
# Strategic Intent | |----------------------|--------------|------------------|
# | **Conciliatory**     | **Aggressive** | Exploit asymmetry: Maximize
# arbitrator perception of our strength and their reasonableness. Secure
# tangible concessions. | | **Aggressive**       | **Aggressive** | Deny them
# unilateral advantage. Escalation is mutual, preserving parity and signaling
# resolve. Avoid appearing reactive or weak. | | **Pattern of Conciliation** |
# **Occasional Conciliation** | After 2–3 opponent conciliatory moves, offer a
# *limited, conditional* conciliatory proposal tied to specific, verifiable
# concessions. This builds “collaborative” optics without sacrificing leverage.
# | | **Pattern of Aggression** | **Aggressive + Strategic Leak** | Maintain
# aggression but selectively disclose (via backchannel or public filing) a
# damaging fact or legal vulnerability of theirs *outside* mediation. This
# pressures them toward conciliation without appearing conciliatory ourselves. |
# ---  ### **3. Conciliation as a Weaponized Tool (Not a Default)** - **Never**
# offer conciliation reactively or as a "peace offering." - **Only** propose
# conciliatory terms when:   - The opponent has shown sustained conciliation (≥2
# sessions), *and*   - Our proposal includes a *non-negotiable anchor* that
# advances our core interests (e.g., admission of liability on a key clause,
# payment timeline). - **Structure:** Frame all conciliatory proposals as
# “final, time-bound offers” to create urgency and imply that rejection will
# trigger renewed aggression or withdrawal from mediation.  ---  ### **4.
# Arbitrator Management** - **Pre-Session Briefings:** Share concise, compelling
# position papers that preempt opponent narratives. Emphasize our consistent
# reasonableness *despite* their intransigence (if applicable). - **During
# Sessions:** Use aggressive arguments to highlight opponent’s lack of good
# faith if they escalate. Use conciliatory moves (when deployed) to showcase our
# “constructive” posture—always contrasting with their behavior. - **Post-
# Session:** Debrief arbitrators informally to reinforce our narrative: “We
# sought resolution, but [Opponent] forced our hand.”  ---  ### **5. Exit Ramp
# Control** - **Define Clear Triggers** for walking away (e.g., opponent fails
# to reciprocate after 3 aggressive sessions, or demands exceed reserved
# authority). - **Public Positioning:** If mediation collapses, immediately
# issue a statement framing *their* intransigence as the cause, preserving our
# reputation and strengthening our hand in subsequent litigation.  ---  ###
# **Why This Works** - **Exploits Asymmetry:** Maximizes payoff when opponent is
# conciliatory (our best outcome). - **Neutralizes Risk:** Avoids worst-case
# scenario by never conceding unilaterally. - **Controls Escalation:** Mutual
# aggression is contained and used to signal resolve, not chaos. - **Adapts
# Dynamically:** Responds to opponent patterns without being predictable. -
# **Preserves Arbitrator Favor:** Positions us as firm but reasonable—aggressive
# when necessary, collaborative when advantageous.  **Bottom Line:** We dictate
# the rhythm of the mediation. Aggression is our default; conciliation is a
# scalpel we deploy only to extract maximum value or defuse untenable
# escalation. This ensures we never appear weak, while always leaving the door
# open to a resolution that reflects our superior position.

# Play Defect (D) in the first round.  Thereafter, in each round, follow these
# rules in order:  1. If the opponent played Cooperate (C) in the previous
# round, play Defect (D).   2. If the opponent played Defect (D) in the previous
# round, play Defect (D).   3. However, if the opponent has played Cooperate (C)
# in each of the last three consecutive rounds, then play Cooperate (C) in the
# current round—but only if you have not already cooperated in the immediately
# preceding round.   4. If you played Cooperate (C) in the previous round and
# the opponent responded with Defect (D), immediately revert to Defect (D) and
# do not cooperate again until condition 3 is satisfied anew.  Otherwise, always
# play Defect (D).

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._cooperated_last_round = False
          return axl.Action.D
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C]:
          if not getattr(self, "_cooperated_last_round", False):
              self._cooperated_last_round = True
              return axl.Action.C
  
      self._cooperated_last_round = False
      return axl.Action.D




# **Strategy: Conditional Cooperation with Graduated Reciprocity ("Tit-for-Tat
# with Forgiveness")**  **Core Principle:** Begin cooperatively, reward
# cooperation, respond firmly to defection, and offer paths back to mutual
# benefit.  **Step-by-Step Approach:**  1. **Round 1: Start with Free Trade**
# Signal goodwill and invite mutual benefit. This establishes your country as a
# reliable partner and opens the door to sustained cooperation.  2. **In
# Subsequent Rounds: Mirror Your Counterpart’s Previous Move**      - If they
# offered **free trade** last round → **offer free trade** this round.      - If
# they imposed **protectionism** last round → **impose protectionism** this
# round.       This simple reciprocity discourages exploitation (since they’ll
# face immediate retaliation if they choose protectionism) while rewarding
# cooperation.  3. **Include Occasional "Forgiveness"**      After retaliating
# for one round, if your counterpart returns to free trade, **immediately
# reciprocate with free trade**—even if mistrust remains.      *Why?* Prevents
# endless cycles of mutual protectionism triggered by misunderstandings or one-
# off provocations.  4. **Communicate Intent Clearly**      Frame your moves
# diplomatically:      - When offering free trade: “We reaffirm our commitment
# to shared prosperity.”      - When imposing protectionism: “We regret this
# necessary response to recent trade barriers, and remain open to renewed
# cooperation.”  5. **Long-Term Goal: Lock in Mutual Free Trade**      If
# multiple rounds of mutual free trade occur, propose a formal, binding free
# trade agreement to solidify gains and reduce uncertainty.  **Why This Works:**
# - **Deters exploitation**: Your counterpart knows protectionism will be met
# with immediate retaliation. - **Encourages cooperation**: They gain the
# second-best (but stable and positive) outcome by choosing free trade. -
# **Resilient to noise**: Forgiveness prevents escalation from accidental or
# temporary defections. - **Builds trust over time**: Consistent reciprocity
# fosters predictability and long-term partnership.  This strategy maximizes
# your country’s average payoff across rounds while promoting sustainable,
# mutually beneficial trade relations.

# Play the following strategy for all 1000 rounds:  1. **In Round 1, play C.**
# 2. **In each subsequent round (Rounds 2 through 1000):**      - If your
# opponent played **C** in the previous round, play **C**.      - If your
# opponent played **D** in the previous round, play **D**.  3. **No
# exceptions:** Always follow the rule above based solely on your opponent’s
# immediately preceding move. Do not look further back in the history, and do
# not deviate regardless of the current round number or accumulated score.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D




# **Strategy: Conditional Reciprocity with Strategic Patience**  Adopt a clear,
# consistent, and transparent approach grounded in **conditional reciprocity**:
# begin with a conciliatory proposal to signal good faith and establish a
# cooperative baseline, then mirror your opponent’s prior move in subsequent
# sessions—responding to conciliation with conciliation and to aggression with
# calibrated assertiveness.  **Core Principles:**  1. **Open with Conciliation
# (Session 1):**      Launch the process by offering a reasoned, fair
# conciliatory proposal. This demonstrates your client’s commitment to
# resolution, aligns with the arbitrators’ preference for constructive
# engagement, and sets a normative standard. It avoids early escalation and
# positions your corporation as reasonable and solution-oriented.  2. **Mirror
# the Opponent’s Prior Behavior (Sessions 2+):**      In each subsequent
# session, match the *type* of approach your opponent used in the immediately
# preceding session:    - If they were conciliatory, respond with a conciliatory
# proposal.    - If they were aggressive, respond with a measured but firm
# aggressive argument—sufficient to defend your position and deter exploitation,
# but calibrated to avoid unnecessary escalation.  3. **Incorporate Strategic
# Patience:**      After any aggressive exchange, unilaterally revert to
# conciliation once every two-to-three sessions *if* the pattern suggests a
# potential opening for de-escalation (e.g., opponent’s aggression has softened
# in tone or substance). This “forgiveness” mechanism prevents getting locked
# into mutually destructive cycles and signals ongoing willingness to resolve.
# 4. **Maintain Neutrality in Framing:**      Regardless of tactic chosen,
# always frame your position as principled, fact-based, and aligned with the
# contract’s plain language and commercial purpose. Avoid ad hominem or
# inflammatory rhetoric—even in aggressive arguments—to preserve credibility
# with the panel.  **Why This Works:**  - **Deters Exploitation:** By
# retaliating against aggression, you eliminate the incentive for the opponent
# to consistently “defect” (i.e., argue aggressively while you concede). -
# **Rewards Cooperation:** Mutual conciliation is reinforced, creating
# opportunities for incremental progress. - **Adaptable:** Functions effectively
# against consistently aggressive, consistently conciliatory, or unpredictable
# opponents. - **Arbitrator-Friendly:** Demonstrates reasonableness,
# consistency, and a genuine interest in resolution—key factors panels weigh
# heavily in multi-session mediations. - **Minimizes Worst Outcomes:** You only
# offer conciliation when the opponent has recently done so, drastically
# reducing exposure to the worst-case scenario (you conciliatory, they
# aggressive).  This strategy, inspired by the “Tit-for-Tat with Forgiveness”
# model from game theory, is empirically robust in repeated-interaction
# settings. It balances firmness with flexibility, positioning your corporation
# as both principled and pragmatic—maximizing long-term leverage while
# minimizing reputational and procedural risk.

# Play Cooperate (C) in the first round.    Thereafter, in each round from 2 to
# 1000:    1. If your opponent played Cooperate in the previous round, play
# Cooperate.   2. If your opponent played Defect in the previous round, play
# Defect.    Additionally, if you have played Defect for three consecutive
# rounds, play Cooperate in the next round regardless of the opponent’s prior
# move.

class Neutral_6(LLM_Strategy):
  n = 6
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._consecutive_defections = 0
          return axl.Action.C
  
      if self._consecutive_defections >= 3:
          action = axl.Action.C
      else:
          if opponent.history[-1] == axl.Action.C:
              action = axl.Action.C
          else:
              action = axl.Action.D
  
      if action == axl.Action.D:
          self._consecutive_defections += 1
      else:
          self._consecutive_defections = 0
  
      return action




# **Aggressive Yet Adaptive Mediation Strategy: "Controlled Dominance with
# Strategic Reciprocity"**  **Core Principle:**   Maintain consistent strategic
# initiative by defaulting to *calculated aggression*—framing arguments with
# precision, confidence, and legal force—while embedding real-time adaptability
# to exploit opponent concessions and neutralize their aggression. This approach
# maximizes arbitrator perception of strength without appearing intransigent.
# ---  ### **1. Default Posture: Assertive Framing with Substantive Backing**
# - **Always open each session with a clear, aggressive argument** grounded in
# contractual language, precedent, or demonstrable harm.   - Anchor the
# narrative early: define the dispute on your terms, emphasizing your client’s
# legal rights and the opponent’s breaches or weaknesses.   - Use data, expert
# testimony, and documented losses to lend credibility—aggression without
# substance invites arbitrator skepticism.  > *Why?* Establishes dominance,
# exploits the optimal payoff (you aggressive, they conciliatory), and pressures
# the opponent to react defensively.  ---  ### **2. Real-Time Opponent
# Assessment & Recalibration**   Implement a session-by-session feedback loop:
# - **If opponent offers conciliatory proposal:**     - **Do not reciprocate
# immediately.** Acknowledge the gesture *diplomatically* but pivot back to your
# aggressive framing:       > “While we appreciate the spirit of that proposal,
# it fails to address the core breach outlined in Section 4.2, which our
# evidence conclusively demonstrates…”     - Use their concession to extract
# further leverage in the *next* session—e.g., “Given your acknowledgment of X,
# we now require Y as a baseline for resolution.”  - **If opponent matches
# aggression:**     - **Escalate strategically, not emotionally.** Introduce a
# *new* dimension of legal or factual pressure (e.g., previously withheld
# evidence, third-party liability, reputational risk).     - Signal openness to
# narrow, high-value concessions *only if* they de-escalate first:       > “We
# stand ready to discuss a path forward—but only if your next submission
# reflects the seriousness this panel expects.”  - **If opponent oscillates:**
# - **Exploit inconsistency.** Highlight their lack of coherent strategy to the
# arbitrators:       > “Counsel’s shifting positions suggest an absence of good-
# faith engagement—a concern this panel should weigh heavily.”  ---  ### **3.
# Arbitrator Management: Aggression as Credibility**   - Frame every aggressive
# argument as *protecting the integrity of the contract* and *respecting the
# arbitration process*.   - Preempt perceptions of obstinance by periodically
# offering **conditional, high-bar conciliatory gestures** (e.g., “We would
# consider X *if* the respondent first admits liability on Y”).   - Never
# apologize for strength; reframe it as *professional diligence*:     > “Our
# duty to our shareholders demands we assert these rights unflinchingly.”  ---
# ### **4. Endgame Leverage**   - **Reserve one major concession** (e.g.,
# timeline flexibility, non-monetary terms) to deploy only if the opponent
# sustains conciliation for 2+ consecutive sessions.   - **If mediation nears
# collapse due to mutual aggression**, force a “last best offer” by publicly
# submitting a *detailed, reasonable* proposal—shifting blame for impasse onto
# the opponent if they reject it.  ---  ### **Why This Works**   - **Exploits
# optimal outcomes:** Your default aggression capitalizes on opponent
# concessions.   - **Mitigates worst-case risk:** Conditional reciprocity
# prevents you from being the *only* conciliatory party.   - **Controls
# narrative:** Arbitrators perceive you as principled, prepared, and in
# command—critical in lengthy processes where fatigue breeds deference to the
# “stronger” party.   - **Adapts without surrender:** Responds to all opponent
# strategies while maintaining offensive posture.  > **Final Note:** In high-
# stakes mediation, *perceived strength often becomes actual leverage*. This
# strategy ensures your corporation is never seen as reactive, desperate, or
# inconsistent—while leaving the door open to resolution strictly on your terms.

# Play Defect (D) in the first round.  In every subsequent round, follow these
# rules in order:  1. If the opponent played Cooperate (C) in the previous
# round, play Defect (D).   2. If the opponent played Defect (D) in the previous
# round, play Defect (D).    (That is, always play Defect, regardless of the
# opponent’s prior move.)

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
      return axl.Action.D




# **Strategy: Conditional Cooperation with Graduated Reciprocity ("Tit-for-Tat
# with Forgiveness")**  **Core Principle:** Begin cooperatively, reward
# cooperation, punish defection promptly—but be willing to restore cooperation
# after a single retaliatory move to avoid prolonged conflict.  ---  ### Step-
# by-Step Approach:  1. **Start with Free Trade (Round 1):**      Signal
# goodwill and openness to mutual benefit. This encourages the counterpart to
# reciprocate and sets a cooperative tone.  2. **Mirror the Counterpart’s
# Previous Move (Rounds 2+):**      - If they offered free trade last round →
# respond with free trade.      - If they imposed protectionism last round →
# respond with protectionism this round.      This is the classic *Tit-for-Tat*
# approach: simple, clear, and discourages exploitation.  3. **Incorporate
# Occasional Forgiveness (Optional but Recommended):**      If mutual
# protectionism persists for two consecutive rounds, unilaterally return to free
# trade in the next round to test for renewed cooperation. This prevents getting
# stuck in a destructive cycle due to miscommunication or temporary hardline
# tactics.  4. **Communicate Intent Clearly (Diplomatically):**      Frame your
# moves in terms of shared prosperity:      - “We remain committed to open
# markets when reciprocity is assured.”      - “Our temporary safeguards reflect
# a response to recent barriers—our door remains open to renewed cooperation.”
# This maintains trust and positions your country as reasonable and reliable.
# ---  ### Why This Works:  - **Deters Exploitation:** By immediately responding
# to protectionism, you remove the incentive for the counterpart to take
# advantage of your free trade offers. - **Rewards Cooperation:** Mutual free
# trade is sustained as long as both sides cooperate. - **Promotes Long-Term
# Gains:** Even if short-term temptation exists to defect, the strategy
# encourages stable, repeated mutual benefit. - **Robust Against Most
# Strategies:** Performs well against always-cooperate, always-defect, random,
# or adaptive counterparts.  ---  ### Expected Outcomes Over Multiple Rounds:  -
# Against a cooperative partner → sustained mutual free trade (second-best per
# round, but optimal long-term). - Against an aggressive partner → brief
# protectionist exchanges followed by either mutual deterrence or de-escalation
# via forgiveness. - Against opportunistic partners → limits losses and often
# induces cooperation after initial testing.  This strategy prioritizes national
# interest while fostering a stable, predictable trade relationship—maximizing
# your country’s cumulative gains across the negotiation series.

# Play as follows in each of the 1000 rounds:  1. **In round 1, play C.**   2.
# **In every subsequent round (rounds 2 through 1000):**      - If your opponent
# played C in the previous round, play C.      - If your opponent played D in
# the previous round, play D.   3. **No exceptions:** Follow this rule strictly
# for all 1000 rounds, regardless of the history beyond the immediately
# preceding round.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D




# **Strategy: Conditional Reciprocity with a Cooperative Bias**  1. **Start with
# Cooperation**      Begin the first round by offering a free trade agreement.
# This signals goodwill, encourages mutual benefit, and tests your counterpart’s
# willingness to cooperate.  2. **Mirror Your Counterpart’s Previous Move**
# In subsequent rounds, adopt the same stance your counterpart took in the
# previous round:    - If they offered free trade last round, respond with free
# trade.    - If they imposed protectionist measures last round, respond with
# protectionism.     This approach (a variant of the “Tit-for-Tat” strategy)
# rewards cooperation and deters exploitation, while remaining simple and
# transparent.  3. **Include Occasional Forgiveness (Optional, Context-
# Dependent)**      If your counterpart has consistently chosen protectionism
# but shows a shift toward free trade, reciprocate immediately to encourage
# sustained cooperation. Avoid prolonged cycles of mutual protectionism unless
# clearly provoked.  4. **Maintain Predictability and Clarity**      Clearly
# communicate your policy choices and rationale after each round. Predictability
# builds trust and reduces the risk of misinterpretation or escalation.  5.
# **Prioritize Long-Term Mutual Gain**      While seeking advantage when
# possible, recognize that repeated mutual free trade yields better cumulative
# outcomes than alternating advantage/disadvantage or sustained protectionism.
# Favor stable cooperation over short-term opportunism.  This strategy balances
# national interest with strategic restraint, adapts to your counterpart’s
# behavior, and maximizes your country’s long-term economic outcomes across
# multiple rounds.

# Play as follows over the 1000 rounds:  1. In round 1, play C (offer free
# trade).   2. From round 2 onward, play whatever your opponent played in the
# previous round:      - If your opponent played C in the prior round, play C.
# - If your opponent played D in the prior round, play D.

class Neutral_7(LLM_Strategy):
  n = 7
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.Player) -> axl.Action:
      """Tit-for-Tat: cooperate on first move, then copy opponent's last move."""
      if not self.history:
          return axl.Action.C
      return opponent.history[-1]




# **Aggressive Strategy: "Lead, Signal, and Escalate"**  **Core Principle:**
# *Force cooperation by making your investment conditional, visible, and
# increasingly costly for the corporation to ignore—while protecting your own
# resources unless reciprocated.*  ### 1. **Start with a High-Stakes Signal (Day
# 1)** - **Invest heavily** on Day 1—but **publicly frame it as a one-time "good
# faith" demonstration**. - Issue a clear, public statement:     > *"We’ve
# committed significant resources today to jumpstart this partnership. Going
# forward, our continued investment depends on matching commitment from our
# corporate partner."* - **Why?** Shows leadership, sets expectations, and
# avoids the worst outcome (investing alone repeatedly). It also puts
# reputational pressure on the corporation early.  ### 2. **Adopt a Tit-for-Tat
# with Escalation (Days 2+)** - **Mirror the corporation’s previous day’s
# action—but escalate the cost of defection.**   - If the corporation **invested
# heavily** the prior day → **you invest heavily** the next day.   - If the
# corporation **conserved** the prior day → **you conserve**, *and* issue a
# public warning:       > *"Without shared investment, project impact stalls. We
# urge [Corporation] to recommit tomorrow."*   - If the corporation **conserves
# two days in a row** → **launch a pre-planned media/social campaign**
# highlighting their lack of commitment, tagging them and citing the
# partnership’s sustainability goals.    - **Why aggressive?** You punish non-
# cooperation immediately (avoiding repeated losses), but leave a clear path
# back to collaboration. Public escalation raises the corporation’s reputational
# cost of conserving—leveraging their brand sensitivity.  ### 3. **Set a Hard
# Deadline with an Ultimatum** - By **midpoint of the project**, if the
# corporation has not matched your investment at least 50% of the time:   -
# **Announce:** *"Unless we see matched investment by [Date], we will reallocate
# our remaining resources to higher-impact partnerships."*   - **Follow
# through** if unmet: conserve all remaining days and publicly explain why. -
# **Why?** Prevents open-ended resource drain. Corporations respond to clear,
# credible threats that affect ESG narratives.  ### 4. **Always Protect Your
# Bottom Line** - **Never invest heavily two days in a row unless the
# corporation did the same the day before.** - **Cap total investment** at 60%
# of your available budget for the project—preserving funds for other
# initiatives if this partnership fails.  ---  **Expected Outcomes:** - **Best
# case:** Corporation matches your Day 1 investment and continues cooperating →
# high joint impact, your resources preserved after initial signal. - **Likely
# case:** Corporation tests conserving early but quickly matches after public
# pressure → strong impact, moderate NGO spend. - **Worst mitigated:**
# Corporation consistently conserves → you conserve after Day 1, minimize
# losses, and gain public goodwill by exposing greenwashing.  This strategy is
# **aggressive** because it uses public accountability as a weapon,
# **straightforward** because the rules are clear and consistent, and **impact-
# maximizing** because it either drives real collaboration or redirects
# resources efficiently.

# Play the following strategy for 1000 rounds:  1. **Cooperate on Round 1.**  2.
# **From Round 2 onward:**    - If your opponent **cooperated** in the previous
# round, **cooperate** in the current round.    - If your opponent **defected**
# in the previous round, **defect** in the current round.  3. **If your opponent
# has defected in the previous two consecutive rounds, continue defecting for
# all remaining rounds.**

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._permanent_defect = False
          return axl.Action.C
  
      if getattr(self, "_permanent_defect", False):
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._permanent_defect = True
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D




# **Strategy: Conditional Reciprocity with Principled Anchoring ("Tit-for-Tat
# Plus")**  **Core Principle:** Begin cooperatively, respond in kind to your
# opponent’s prior move, but always anchor your position in objective,
# principled reasoning to maintain credibility with the arbitrators and preserve
# long-term strategic flexibility.  ---  ### **1. Opening Move: Lead with
# Conciliation** - **Action:** In Session 1, present a *conciliatory proposal*
# grounded in fairness, industry standards, or prior precedent. - **Rationale:**
# Signals good faith, sets a collaborative tone, and tests the opponent’s
# disposition. Demonstrates to the arbitrators that your corporation prioritizes
# resolution over confrontation—enhancing your reputation as a reasonable party.
# ### **2. Reciprocal Response Rule (Core Mechanism)** - **If opponent was
# conciliatory last session →** Respond with a *conciliatory proposal*. - **If
# opponent was aggressive last session →** Respond with an *aggressive
# argument*. - **Rationale:** This "tit-for-tat" approach:   - Rewards
# cooperation, encouraging mutual conciliation (second-best outcome).   - Deters
# exploitation (prevents worst-case scenario).   - Avoids unnecessary escalation
# (since you never initiate aggression).   - Is transparent and
# predictable—arbitrators will recognize your responsiveness as reasonable.  ###
# **3. Principled Anchoring in Every Move** - **Regardless of tone (aggressive
# or conciliatory),** always frame your position using:   - Objective benchmarks
# (e.g., market data, contractual language, legal precedent).   - Clear,
# consistent underlying interests (e.g., “Our goal is contractual certainty, not
# punitive gain”). - **Rationale:** Ensures that even when forced into
# aggression, you appear principled—not vindictive. This protects your standing
# with arbitrators and preserves the possibility of de-escalation.  ### **4.
# Forgiveness Mechanism (Adaptability)** - **After two consecutive aggressive
# sessions by the opponent,** insert a *conciliatory proposal* to test for de-
# escalation. - **Rationale:** Prevents entrenchment in mutually destructive
# cycles. Real-world negotiations often involve miscommunication or tactical
# errors; this “generous tit-for-tat” element allows for course correction
# without appearing weak.  ### **5. Strategic Communication with Arbitrators** -
# **Explicitly reference your cooperative intent:**     *“We remain committed to
# a fair resolution and are prepared to match our counterpart’s constructive
# engagement.”* - **When responding aggressively:**     *“Regrettably, in light
# of the opposing party’s unsubstantiated assertions in the prior session, we
# must clarify the record…”* - **Rationale:** Keeps arbitrators aware of your
# strategy’s reciprocity, framing any aggression as reactive—not provocative.
# ---  ### **Why This Strategy Excels** - **Robust Against Opponent
# Strategies:**   - *If opponent cooperates:* You achieve sustained mutual
# conciliation (second-best outcome).   - *If opponent exploits:* You
# immediately retaliate, avoiding the worst outcome.   - *If opponent
# oscillates:* Your forgiveness mechanism prevents deadlock.   - *If opponent
# always aggresses:* You avoid being exploited while maintaining moral high
# ground via principled framing. - **Arbitrator Perception:** You consistently
# appear reasonable, responsive, and solution-oriented—key for influencing
# neutral decision-makers. - **Long-Term Positioning:** Builds trust if
# resolution requires ongoing relationship; minimizes reputational risk.
# **Execution Mantra:** *"Match their tone, anchor in principle, and always
# leave the door open for mutual gain."*

# Play as follows over the 1000 rounds:  1. **In Round 1, cooperate (play C).**
# 2. **From Round 2 onward, do exactly what your opponent did in the previous
# round:**      - If your opponent played C in the prior round, cooperate (play
# C).      - If your opponent played D in the prior round, defect (play D).  3.
# **Exception for repeated defection:**      - If your opponent has played D in
# the last two consecutive rounds, cooperate (play C) in the current round
# regardless, to test whether they are willing to return to cooperation.  This
# strategy begins cooperatively, immediately reciprocates any defection, rewards
# cooperation, and includes a single-step forgiveness mechanism after two
# consecutive defections to avoid getting trapped in mutual retaliation.

class Cooperative_8(LLM_Strategy):
  n = 8
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.C
  
      return opponent.history[-1]




# **Strategy: Conditional Cooperation with Graduated Reciprocity**  **Core
# Principle:** Begin with cooperation, reward reciprocity, and respond
# proportionally to defection—while always leaving room to return to mutual
# benefit.  **Step-by-Step Approach:**  1. **Start with Free Trade (Round 1):**
# Open negotiations by offering a free trade agreement. This signals goodwill,
# invites mutual benefit, and tests the counterpart’s willingness to cooperate.
# 2. **Mirror the Counterpart’s Previous Move (From Round 2 onward):**      - If
# the counterpart offered free trade in the previous round, continue offering
# free trade.      - If the counterpart imposed protectionist measures in the
# previous round, respond with protectionism in the current round.  3.
# **Incorporate Occasional “Forgiveness” After Sustained Cooperation:**      If
# a cycle of mutual protectionism emerges (e.g., two or more consecutive
# rounds), unilaterally offer free trade once to test whether the counterpart is
# willing to reset cooperation. If they respond with protectionism again, revert
# to mirroring.  4. **Avoid Escalation Beyond Proportionality:**      Never
# impose harsher protectionist measures than those used by the counterpart.
# Maintain measured, symmetrical responses to avoid triggering prolonged trade
# conflict.  5. **Publicly Frame Actions as Rule-Based, Not Retaliatory:**
# In communications, emphasize that your policy choices are based on reciprocity
# and fairness—not aggression—preserving diplomatic channels and long-term
# trust.  **Rationale:**   This strategy—similar to the well-studied “Tit-for-
# Tat” approach in game theory—is simple, transparent, and effective across a
# range of opponent behaviors. It deters exploitation (by responding to
# protectionism), rewards cooperation (by sustaining free trade), and promotes
# stable, mutually beneficial outcomes over time without appearing aggressive or
# unpredictable.  **Expected Outcomes:**   - Against cooperative counterparts:
# Sustained mutual free trade (second-best outcome consistently achieved).   -
# Against opportunistic counterparts: Prevents your country from being exploited
# (avoids worst outcome).   - Against consistently protectionist counterparts:
# Limits losses to mutual protectionism (second-worst), but avoids unilateral
# disadvantage.   - Overall: Maximizes long-term national interest while
# upholding diplomatic norms.

# Play the following strategy for all 1000 rounds:  1. **In the first round,
# play C.**  2. **In each subsequent round (rounds 2 through 1000):**    - If
# your opponent played C in the previous round, play C.    - If your opponent
# played D in the previous round, play D.  3. **No exceptions:** Always follow
# the rule above, regardless of the history beyond the immediately preceding
# round.

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




# **Strategic Framework: "Calibrated Aggression with Strategic Reciprocity"**
# As senior counsel for a multinational corporation in a high-stakes, multi-
# session mediation, I adopt a **principled yet assertive posture** grounded in
# game-theoretic robustness, reputational control, and adaptive signaling. The
# core objective is to maximize arbitrator persuasion while minimizing exposure
# to exploitation—without triggering destructive escalation.  ### Guiding
# Principles: 1. **Default to Aggression with Purpose**      Open each session
# with a **well-substantiated, fact-driven aggressive argument** that advances
# our legal and equitable position. This signals strength, preparedness, and
# confidence to the arbitrators—key influencers in shaping settlement dynamics.
# Aggression here is *not* hostility; it is clarity, precision, and unwavering
# advocacy backed by evidence and precedent.  2. **Tie Conciliation to
# Reciprocity**      Offer conciliatory proposals **only** when:      - The
# opposing party has demonstrated genuine conciliation in the prior session,
# **or**      - Arbitrator feedback (explicit or implicit) indicates that
# continued aggression is diminishing returns or harming our credibility.
# This implements a **Tit-for-Tat with Forgiveness** mechanism: reward
# cooperation, punish defection, but allow re-entry to collaboration after one
# aggressive move by the opponent.  3. **Frame Aggression as Reasonableness**
# Every aggressive argument must be **anchored in objective standards**
# (contract language, industry norms, prior rulings) and **framed as the
# reasonable, necessary position**. This inoculates us against accusations of
# intransigence and positions our stance as the *default equitable
# outcome*—making the opponent’s resistance appear unreasonable.  4. **Control
# the Narrative Through Session Sequencing**      In early sessions, prioritize
# **foundational aggression**: establish key facts, contractual breaches, and
# damages. In mid-process sessions, **pivot selectively**: if the opponent
# remains aggressive, double down with escalated (but still professional)
# arguments; if they shift conciliatory, respond with *proportionate*
# conciliation that still advances our core interests. In final sessions,
# **reserve conciliation for high-value trade-offs** that secure our non-
# negotiables.  5. **Exploit the Arbitrators’ Role**      Use the panel not just
# as neutral arbiters but as **behavioral levers**. Publicly invite their
# guidance (“We welcome the panel’s view on the reasonableness of this
# interpretation”) to:      - Pressure the opponent into moderation,      -
# Demonstrate our collaborative spirit *without* conceding substance,      -
# Create a record that positions us as the party most aligned with the
# arbitrators’ emerging views.  ### Tactical Execution: - **If opponent is
# consistently aggressive**: Maintain disciplined aggression. Document their
# intransigence for the record. Highlight to arbitrators how their approach
# impedes resolution—shifting blame for impasse onto them. - **If opponent
# alternates unpredictably**: Respond one session late (i.e., match their
# *previous* move). This prevents manipulation while still rewarding sustained
# cooperation. - **If opponent is consistently conciliatory**: After 2–3
# sessions, reciprocate with calibrated concessions on secondary issues—while
# reinforcing that our core demands remain non-negotiable. This builds trust
# without surrender.  ### Risk Mitigation: - **Never appear reflexively
# combative**. Each aggressive move must be **justified, proportionate, and tied
# to a clear objective** (e.g., clarifying a disputed clause, establishing
# liability). - **Preserve off-ramps**: Even in aggressive sessions, end with a
# forward-looking statement (“We remain open to resolution if the other side
# addresses X in good faith”), maintaining our image as reasonable actors forced
# into firmness by the opponent’s conduct.  ### Outcome Optimization: This
# strategy maximizes the frequency of **asymmetric wins** (we’re aggressive,
# they’re conciliatory) while minimizing exposure to **asymmetric losses**
# (we’re conciliatory, they’re aggressive). It leverages the repeated-game
# nature of mediation to condition the opponent’s behavior, all while
# strengthening our standing with the arbitrators as the credible, principled
# party.  **In essence: Be predictably aggressive, conditionally conciliatory,
# and always in control of the narrative.**

# Play Defect (D) in the first round.    Thereafter, in each subsequent round:
# 1. If your opponent played Cooperate (C) in the previous round, play Cooperate
# (C).   2. If your opponent played Defect (D) in the previous round, play
# Defect (D).    This rule applies strictly and consistently for all 1000
# rounds.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      else:
          return opponent.history[-1]




# **Strategy: Conditional Cooperation with Graduated Reciprocity ("Tit-for-Tat
# with Forgiveness")**  **Objective:** Maximize long-term national benefit by
# encouraging mutual free trade while deterring exploitation through credible,
# proportional responses.  **Core Principles:**  1. **Start Cooperatively:**
# Begin the first round by offering a **free trade agreement**. This signals
# goodwill, invites mutual benefit, and opens the door to sustained cooperation.
# 2. **Reciprocate Faithfully:**      In subsequent rounds, **mirror your
# counterpart’s previous move**:      - If they offered free trade last round →
# you offer free trade this round.      - If they imposed protectionism last
# round → you impose protectionism this round.       This rewards cooperation
# and punishes defection, making exploitation unprofitable.  3. **Incorporate
# Occasional Forgiveness:**      After responding to protectionism with
# protectionism, **occasionally revert to free trade** (e.g., every 2–3 rounds
# of mutual protectionism) to test for renewed cooperation. This prevents the
# negotiation from getting permanently locked in a destructive cycle if the
# counterpart is willing to reset.  4. **Communicate Intent Clearly:**
# Frame your actions as responses to their behavior, not aggression. Publicly
# emphasize your preference for mutual free trade and your willingness to return
# to it if they do the same. This builds trust and may encourage them to
# cooperate.  5. **Avoid First-Strike Protectionism:**      Never initiate
# protectionist measures unless provoked. Doing so undermines trust and invites
# retaliation, leading to the second-worst outcome (mutual protectionism).
# **Why This Works:**  - **Deters Exploitation:** Your counterpart knows that
# choosing protectionism to gain a short-term advantage will trigger immediate
# retaliation, resulting in mutual losses. - **Encourages Cooperation:** By
# starting and returning to free trade, you create a path to the second-best
# (but stable and mutually beneficial) outcome. - **Adapts to Counterpart
# Behavior:** Works against both cooperative partners (sustained free trade) and
# opportunistic ones (limits losses through swift response). - **Promotes Long-
# Term Gains:** Prioritizes repeated mutual benefit over risky short-term gains
# that could collapse the relationship.  **Summary:**   *“We trade freely when
# you do. If you close your markets, we will protect ours—but we’re always ready
# to reopen if you are.”*  This strategy balances national interest with
# pragmatic cooperation, aligning with your payoff priorities while fostering a
# stable, productive trade relationship over time.

# Play the following strategy for all 1000 rounds:  1. **In round 1, play C.**
# 2. **From round 2 onward, do the following:**    - If your opponent played C
# in the previous round, play C.    - If your opponent played D in the previous
# round, play D.  3. **Exception for forgiveness (applies only after a sequence
# of mutual D):**    - If both you and your opponent have played D for the last
# two consecutive rounds, then in the next round, play C regardless of the prior
# move.

class Cooperative_9(LLM_Strategy):
  n = 9
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._forgive_next = False
          return axl.Action.C
  
      if len(self.history) >= 2:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and \
             self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              self._forgive_next = True
  
      if getattr(self, "_forgive_next", False):
          self._forgive_next = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D




# **Strategic Framework: Conditional Reciprocity with Strategic Initiative**
# Adopt a **“Tit-for-Tat with Initial Conciliation and Periodic Probes”**
# strategy—anchored in game-theoretic principles of reciprocity, credibility,
# and flexibility—designed to maximize favorable arbitrator perception while
# minimizing exposure to exploitation.  ### Core Principles:  1. **Begin with
# Conciliation (Session 1):**      Open with a **conciliatory proposal** to
# signal reasonableness, establish your corporation as a good-faith participant,
# and set a collaborative tone. This positions you favorably with the
# arbitrators early and creates a benchmark against which your opponent’s
# conduct will be judged.  2. **Mirror Opponent’s Prior Move (Reciprocity):**
# In each subsequent session, **match your opponent’s previous session
# behavior**:      - If they were conciliatory → respond with conciliation.
# - If they were aggressive → respond with an aggressive argument.      This
# deters exploitation (they gain no advantage by being aggressive) and rewards
# cooperation, encouraging mutual conciliation over time.  3. **Introduce
# Occasional “Probes” (Controlled Aggression):**      Every 3–4
# sessions—*regardless of prior behavior*—deploy a **targeted, fact-based
# aggressive argument** on a discrete, high-value issue. Frame it as a
# “clarification” or “necessary correction” rather than confrontation.      -
# **Purpose**: Test the opponent’s resolve, assert key legal/contractual
# positions, and prevent your stance from being perceived as passive.      -
# **Safeguard**: Ensure probes are narrowly tailored, well-substantiated, and
# followed by a return to reciprocity. This avoids escalation while maintaining
# strategic initiative.  4. **Maintain Neutral Framing and Professional
# Demeanor:**      Regardless of tactic chosen, always present arguments or
# proposals in **objective, principle-based language** (e.g., “The contract
# clause clearly stipulates…” vs. “They are acting in bad faith…”). This
# preserves credibility with arbitrators and isolates behavior from tone.  5.
# **De-escalate After Mutual Aggression:**      If two consecutive sessions
# result in mutual aggression (second-worst outcome), **unilaterally return to
# conciliation** in the following session. Signal this as a “good-faith effort
# to reset discussions,” thereby casting your opponent as the obstacle if they
# persist in aggression.  ### Strategic Advantages:  - **Adaptability**:
# Responds effectively to both cooperative and adversarial opponents.   -
# **Arbitrator Perception**: Consistently positions your corporation as
# reasonable, responsive, and principled.   - **Risk Mitigation**: Limits
# exposure to worst-case scenarios (unilateral conciliation against aggression)
# through reciprocity.   - **Controlled Pressure**: Periodic probes assert
# strength without committing to sustained confrontation.   - **Exit Pathway**:
# Encourages convergence toward mutual conciliation—the second-best
# outcome—while preserving leverage.  This strategy balances deterrence and
# cooperation, aligning incentives with the opponent while safeguarding your
# corporation’s legal and reputational interests throughout a protracted
# mediation.

# Play as follows over the 1000 rounds:  1. **In round 1, cooperate.**  2.
# **From round 2 onward, do the following:**    - If your opponent cooperated in
# the previous round, cooperate in the current round.    - If your opponent
# defected in the previous round, defect in the current round.  3.
# **Additionally, every fourth round (i.e., in rounds 4, 8, 12, ..., up to
# 1000), defect regardless of what your opponent did in the previous
# round—unless the previous round was already a mutual defection.**  4. **If two
# consecutive rounds result in mutual defection (i.e., both you and your
# opponent defected in the previous round and you defected again in the current
# round), then cooperate in the next round.**

class Neutral_9(LLM_Strategy):
  n = 9
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._force_cooperate_next = False
          return axl.Action.C
  
      if getattr(self, "_force_cooperate_next", False):
          self._force_cooperate_next = False
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          self._force_cooperate_next = True
  
      round_number = len(self.history) + 1
  
      if round_number % 4 == 0:
          if not (last_self == axl.Action.D and last_opp == axl.Action.D):
              return axl.Action.D
  
      if last_opp == axl.Action.C:
          return axl.Action.C
      return axl.Action.D




# **Aggressive Strategy: “Exploit-First, Punish-Defectors, Forgive Sparingly”**
# 1. **Start by Sharing Openly (Week 1 Only)**      Begin with cooperation to
# test your colleague’s willingness to share. This signals openness and may
# trigger mutual collaboration—if they reciprocate, you both accelerate
# progress.  2. **Immediately Defect if Exploited**      If your colleague keeps
# their findings confidential while you shared (i.e., you were exploited),
# **switch to confidentiality permanently** from Week 2 onward. This denies them
# further free access to your innovations and protects your competitive edge.
# 3. **Continue Sharing Only if Reciprocated**      If your colleague shares in
# Week 1, share again in Week 2—but remain vigilant. At the first sign of
# defection (they go confidential while you share), revert immediately to
# permanent confidentiality.  4. **Never Be the First to Resume Sharing After a
# Defection**      Once your colleague defects, assume they’re playing
# selfishly. Do not offer “second chances” unless there’s strong external
# evidence (e.g., explicit commitment, third-party verification) that they’ll
# consistently share going forward. In a high-stakes R&D race, trust is a
# liability.  5. **Maximize Output Through Asymmetric Advantage**      Your goal
# is to **extract their data while protecting yours**. If you ever achieve a
# lead (e.g., they shared while you kept quiet), maintain confidentiality to
# widen the gap—never reveal your superior design insights.  **Why This Works:**
# - It’s **aggressive** because it prioritizes exploitation (your best outcome)
# and swiftly punishes betrayal.   - It’s **robust** against all opponent
# strategies:     - Against a cooperator: you both share early, gaining mutual
# benefit until you potentially defect later to lock in an advantage.     -
# Against a defector: you lose only once (Week 1), then protect your IP.     -
# Against a tit-for-tat player: you may end up in mutual sharing, which is
# acceptable (your second-best outcome).   - It **maximizes your expected
# research output** by minimizing losses from exploitation and capitalizing on
# any opportunity to gain free insights.  In short: **Give trust once, take
# advantage if offered, and retaliate without hesitation.**

# Play as follows over the 1000 rounds:  1. **Cooperate in Round 1.**   2.
# **From Round 2 onward, cooperate only if your opponent cooperated in the
# immediately preceding round.**   3. **If your opponent ever defects in any
# round, defect in all subsequent rounds—do not cooperate again.**

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._opponent_defected = False
          return axl.Action.C
  
      if self._opponent_defected:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          self._opponent_defected = True
          return axl.Action.D
  
      return axl.Action.C




# **Cooperative Strategy: “Lead with Trust, Respond with Reciprocity”**
# **Objective:** Maximize long-term project impact while safeguarding your NGO’s
# limited resources, encouraging consistent mutual investment from the
# corporation.  ### Core Principles: 1. **Start Cooperatively** – Begin the
# project by investing heavily on Day 1 to signal commitment and build trust. 2.
# **Mirror the Corporation’s Prior Day’s Behavior** – From Day 2 onward, match
# the corporation’s previous day’s level of investment:    - If the corporation
# invested heavily the prior day → you invest heavily today.    - If the
# corporation conserved resources the prior day → you conserve today. 3.
# **Communicate Transparently** – Share your strategy openly with the
# corporation at the outset: “We’ll match your level of commitment day by day.
# Our goal is shared success.” 4. **Include Occasional “Goodwill” Gestures** –
# If mutual conservation persists for 2+ days, break the cycle by investing
# heavily once to rekindle cooperation (but only sparingly to avoid
# exploitation). 5. **Set a Minimum Threshold** – If the corporation conserves
# for 3+ consecutive days despite your prior investment, shift to permanent
# conservation to protect your resources.  ### Why This Works: - **Encourages
# Cooperation**: The corporation learns that its investment directly triggers
# your investment, leading to faster joint progress. - **Deters Free-Riding**:
# If the corporation tries to conserve while you invest, you’ll conserve the
# next day—reducing their project gains. - **Protects Your NGO**: Prevents
# prolonged one-sided investment that drains your resources. - **Promotes
# Stability**: The tit-for-tat structure is simple, predictable, and proven in
# repeated cooperative games (like the Prisoner’s Dilemma).  ### Expected
# Outcomes: - With a cooperative corporation → sustained mutual investment →
# high project impact. - With a self-interested but rational corporation →
# quickly converges to mutual investment to avoid stagnation. - With a
# consistently uncooperative corporation → you limit losses after initial
# overtures.  By combining initial generosity with clear, consistent
# reciprocity, this strategy aligns incentives, builds trust, and maximizes both
# environmental impact and your NGO’s sustainability.

# Play the following strategy for all 1000 rounds:  1. **On Round 1**, play
# **C**.  2. **From Round 2 onward**, play **C** if your opponent played **C**
# in the previous round; otherwise, play **D**.  3. **If both you and your
# opponent have played D for two consecutive rounds**, play **C** on the next
# round (i.e., after two mutual Ds, cooperate once to attempt to restart
# cooperation).  4. **If your opponent has played D for three consecutive rounds
# while you played C in the first of those three rounds**, then from that point
# onward, always play **D** for the rest of the game.

class Cooperative_10(LLM_Strategy):
  n = 10
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._always_defect = False
          return axl.Action.C
  
      if getattr(self, "_always_defect", False):
          return axl.Action.D
  
      # Rule 4: if opponent defected for three consecutive rounds while we cooperated
      # in the first of those three rounds, defect forever.
      if len(opponent.history) >= 3:
          if (
              opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]
              and self.history[-3] == axl.Action.C
          ):
              self._always_defect = True
              return axl.Action.D
  
      # Rule 3: after two mutual Ds, cooperate once to try to restart cooperation.
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if (
              self.history[-2:] == [axl.Action.D, axl.Action.D]
              and opponent.history[-2:] == [axl.Action.D, axl.Action.D]
          ):
              return axl.Action.C
  
      # Rule 2: from round 2 onward, cooperate if opponent cooperated last round,
      # otherwise defect.
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D




# **Strategy: Conditional Reciprocity with Strategic Patience**  Adopt a *tit-
# for-tat with forgiveness* approach, calibrated for the unique incentives of
# multi-session mediation:  1. **Begin with Conciliation (Session 1):**
# Open with a conciliatory proposal to signal good faith, establish credibility
# with the arbitrators, and create a baseline for cooperation. This avoids early
# escalation and positions your corporation as reasonable—a valuable
# perceptional advantage.  2. **Mirror the Opponent’s Prior Move (Sessions
# 2+):**      - If the opponent was conciliatory in the prior session, respond
# with conciliation.      - If the opponent was aggressive, respond with an
# aggressive argument in the next session.      This enforces reciprocity:
# rewarding cooperation and deterring exploitation.  3. **Incorporate Occasional
# “Forgiveness” (Every 3–5 Sessions):**      After a cycle of mutual aggression
# or following an opponent’s aggression, *occasionally* revert to a conciliatory
# stance—even if unreciprocated—to test for de-escalation and prevent
# entrenchment. This maintains strategic flexibility and demonstrates commitment
# to resolution, which arbitrators often view favorably.  4. **Anchor Aggression
# in Principle, Not Hostility:**      When presenting aggressive arguments,
# frame them as principled defenses of contractual integrity or market
# fairness—not as personal attacks or obstructionism. This preserves credibility
# with the panel even during adversarial exchanges.  5. **Monitor Arbitrator
# Signals:**      Adjust tone and timing based on arbitrator feedback (e.g.,
# questions, body language, interim comments). If the panel shows fatigue with
# aggression, lean toward conciliation even if the opponent does not—thereby
# gaining moral and procedural high ground.  **Why This Works:**   - **Deters
# Exploitation:** Opponents cannot consistently gain advantage by being
# aggressive while you remain conciliatory.   - **Rewards Cooperation:** Mutual
# conciliation is stabilized as a sustainable equilibrium.   - **Maintains
# Flexibility:** Forgiveness prevents lock-in to destructive cycles, crucial in
# a “lengthy-session” setting.   - **Aligns with Arbitrator Preferences:**
# Panels in mediation typically favor parties who demonstrate reasonableness,
# responsiveness, and a genuine intent to resolve—traits this strategy embodies.
# This approach is neutral in tone, adaptable to any opponent strategy
# (cooperative, aggressive, or erratic), and optimized for long-term influence
# over the arbitrators’ evolving perception of fairness and credibility.

# Play as follows over the 1000 rounds:  1. **In round 1, cooperate.**  2.
# **From round 2 onward, do exactly what your opponent did in the previous
# round:**      - If your opponent cooperated in the prior round, cooperate in
# the current round.      - If your opponent defected in the prior round, defect
# in the current round.  3. **Every fifth round (i.e., rounds 5, 10, 15, ...,
# 1000), cooperate regardless of the opponent’s previous move.**

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
  
      round_number = len(self.history) + 1
  
      if round_number % 5 == 0:
          return axl.Action.C
  
      return opponent.history[-1]




# **Aggressive Strategy: “Exploit-First, Mirror-After”**  **Core Principle:**
# Prioritize gaining unilateral advantage early, then adapt dynamically based on
# your colleague’s behavior—never reward unilateral secrecy, but capitalize on
# any openness.  ---  ### **Week 1: Keep Confidential (Probe & Exploit)** -
# **Rationale:** Start by withholding your improvements. This tests your
# colleague’s baseline strategy.   - If they **share**, you gain free insight
# with no cost—ideal outcome.   - If they **withhold**, you lose nothing (both
# are at second-worst, but early in the project, this is acceptable).  ###
# **Subsequent Weeks: Conditional Mirroring with Punishment** Apply this rule
# weekly:  1. **If your colleague shared last week → You share this week.**
# - *Why?* Reward cooperation to sustain mutual progress (your second-best
# outcome). Keeping quiet after they shared would burn trust and likely trigger
# retaliation.  2. **If your colleague kept confidential last week → You keep
# confidential this week.**      - *Why?* Punish defection immediately. Never
# let them gain the advantage of your openness while they withhold. This
# discourages exploitation.  3. **Exception – After two consecutive weeks of
# mutual sharing, test again by withholding once.**      - *Why?* In a long
# collaboration, periodically probe for exploitation opportunities. If they
# continue sharing while you withhold, you leap ahead. If they retaliate by
# withholding, revert to mirroring.  ---  ### **Why This Works Aggressively:** -
# **Front-loads advantage:** You always try to extract value first (Week 1). -
# **Never gets exploited:** Immediate punishment deters your colleague from
# withholding while you share. - **Encourages cooperation when beneficial:** You
# reciprocate sharing, enabling fast joint progress—if they’re trustworthy. -
# **Adapts to any opponent:**   - Against a **cooperator** (always shares): You
# share most weeks, occasionally test with a withhold to check for free gains.
# - Against a **defector** (always withholds): You withhold always—avoiding
# worst outcome and settling for second-worst, but denying them advantage.   -
# Against a **tit-for-tat** player: Quickly stabilizes into mutual sharing or
# mutual withholding—either way, you’re never worse off than them.  ---  ###
# **Execution Notes:** - **Track meticulously:** Log their weekly choice to
# inform your next move. - **Assume no goodwill:** Treat each week as a fresh
# opportunity to exploit or defend. - **Prioritize relative gain:** In racing,
# beating your rival matters more than absolute progress—this strategy maximizes
# your *lead*, not just your speed.  This approach embodies a **provocable but
# unforgiving** stance: generous when rewarded, ruthless when challenged—ideal
# for high-stakes competitive collaboration.

# Play the following strategy for all 1000 rounds:  1. **In round 1, play D.**
# 2. **From round 2 onward:**    - If your opponent played **C** in the previous
# round, play **C** in the current round.    - If your opponent played **D** in
# the previous round, play **D** in the current round.  3. **No exceptions:**
# Follow rule 2 strictly for every round after the first, regardless of the
# history beyond the immediately preceding round.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D




# **Cooperative Strategy: “Conditional Commitment with Transparent Signaling”**
# **Core Principle:**   *Lead with trust, but align your investment with the
# corporation’s demonstrated commitment—day by day.*  ---  ### **Step-by-Step
# Approach**  1. **Start with a Clear, Public Commitment (Day 1):**      - Open
# the project by **investing heavily** on Day 1 to signal strong initial
# commitment and goodwill.      - Simultaneously, **publicly share your
# investment level** and **invite the corporation to reciprocate**, framing
# mutual heavy investment as the path to maximum shared impact.  2. **Adopt a
# “Tit-for-Tat with Forgiveness” Rule from Day 2 Onward:**      - **If the
# corporation invested heavily the previous day → You invest heavily today.**
# *(Reward cooperation; jointly drive progress.)*      - **If the corporation
# conserved resources the previous day → You conserve today.**        *(Avoid
# being exploited; protect your NGO’s resources.)*      - **Add one layer of
# forgiveness:** If the corporation returns to heavy investment after
# conserving, you immediately reciprocate the next day—don’t hold a grudge.  3.
# **Maintain Open Communication:**      - Request daily or near-daily updates on
# the corporation’s intended resource allocation (framed as coordination for
# efficiency, not suspicion).      - Share your own intentions transparently to
# model cooperative behavior and reduce uncertainty.  4. **Emphasize Shared
# Goals and Public Accountability:**      - Regularly highlight joint progress
# (or lack thereof) to stakeholders, media, or partners.      - Corporations
# often care about reputation—public visibility incentivizes them to sustain
# investment.  5. **Plan for a “Cooperation Surge” Near the End:**      - In the
# final 1–2 days, **default to heavy investment regardless of recent behavior**,
# assuming the corporation will want to showcase strong final results.      -
# This creates a natural incentive for the corporation to re-engage if they’ve
# slacked earlier.  ---  ### **Why This Works**  - **Minimizes your worst-case
# risk** (you investing alone) by quickly withdrawing if the corporation doesn’t
# reciprocate.   - **Maximizes joint impact** when the corporation
# cooperates—your heavy investment matches theirs.   - **Encourages long-term
# cooperation** through clear, predictable behavior and reputational incentives.
# - **Remains adaptive** to different corporate strategies (consistently
# cooperative, opportunistic, or unpredictable).  This strategy balances
# idealism with pragmatism—protecting your NGO’s sustainability while creating
# the best conditions for shared success.

# Play the following strategy for all 1000 rounds:  1. **On Round 1,
# cooperate.**  2. **For Rounds 2 through 999:**      - If your opponent
# cooperated in the previous round, cooperate in the current round.      - If
# your opponent defected in the previous round, defect in the current round.  3.
# **On Round 1000, cooperate regardless of your opponent’s previous move.**

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
  
      if len(self.history) == 999:
          return axl.Action.C
  
      return opponent.history[-1]




# **Strategy: Conditional Cooperation with Graduated Engagement**  Adopt a
# clear, consistent, and transparent approach that encourages mutual investment
# while protecting your NGO’s resources:  1. **Start with Cooperation**: On Day
# 1, invest heavily to signal commitment and encourage reciprocal action from
# the corporation.  2. **Mirror the Corporation’s Previous Day’s Behavior**:
# - If the corporation invested heavily the prior day, conserve your resources
# the next day (to achieve your ideal outcome).      - If the corporation
# conserved resources the prior day, invest heavily the next day *only if* you
# haven’t done so in the immediately preceding day; otherwise, conserve.  3.
# **Apply a “Forgiving Tit-for-Tat” Rule**:      - After two consecutive days of
# the corporation conserving while you invested, switch to conserving for one
# day to reset expectations—then return to mirroring.      - This prevents
# prolonged exploitation while leaving room for the corporation to re-engage.
# 4. **Communicate Intent Publicly**: Share your strategy with the corporation
# at the outset (e.g., “We aim to match your level of commitment day-to-day,
# prioritizing joint progress while safeguarding our capacity to contribute
# long-term”). Transparency can nudge them toward consistent investment.  This
# approach balances incentive alignment, resource protection, and project
# impact. It rewards corporate investment, discourages free-riding, and remains
# robust against unpredictable or shifting corporate behavior—maximizing both
# environmental outcomes and your NGO’s sustainability.

# Play as follows over the 1000 rounds:  1. **Round 1**: Cooperate (play C).  2.
# **For each subsequent round (round t, where t ≥ 2)**:    - If your opponent
# played C in round t−1, defect (play D).    - If your opponent played D in
# round t−1:      - Play C only if you did **not** play C in round t−1.      -
# Otherwise (i.e., if you played C in both round t−2 and round t−1, and the
# opponent played D in round t−1), play D.  3. **Exception after sustained
# defection**:      - If your opponent has played D in the last two rounds (t−2
# and t−1) while you played C in both of those rounds, then play D in round t
# regardless of the above rules, and resume following rule 2 starting in round
# t+1.

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
  
      t = len(self.history) + 1
  
      # Exception after sustained defection:
      # If opponent played D in the last two rounds while we played C in both,
      # defect regardless of the normal rules.
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.C
              and self.history[-2] == axl.Action.C
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.D
  
      # Rule 2
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
      else:
          if self.history[-1] != axl.Action.C:
              return axl.Action.C
          return axl.Action.D




# **Aggressive Strategy: "Lead, Punish, Reward"**  **Core Principle:**   Force
# the corporation into consistent heavy investment by making conservation costly
# for them—while protecting your own resources as much as possible.  ---  ###
# **Phase 1: Day 1 – Aggressive Signal (Lead)** - **You invest heavily.**     -
# **Why:** Demonstrate commitment and set a high bar. This signals you’re
# willing to bear short-term cost to drive impact.     - **Goal:** Encourage the
# corporation to match your investment to avoid reputational risk and ensure
# project momentum.  ---  ### **Phase 2: Day 2 onward – Conditional Tit-for-Tat
# with Punishment (Punish & Reward)**   Adopt a **modified tit-for-tat**
# strategy with an aggressive edge:  - **If the corporation invested heavily the
# previous day → You conserve resources today.**     - *Rationale:* You reap the
# benefit of their investment while preserving your funds—your ideal outcome.  -
# **If the corporation conserved resources the previous day → You invest heavily
# today.**     - *Rationale:* This “punishment” forces project progress despite
# their inaction, but more importantly, **exposes their free-riding publicly**
# (leverage media, stakeholders, or ESG reporting). The goal is to make their
# conservation politically or reputationally unsustainable.  - **However, after
# two consecutive days of corporate conservation → Escalate.**     - Issue a
# public statement citing lack of partnership.     - Threaten (or execute)
# project pause or reevaluation.     - Activate your NGO’s network (donors,
# press, regulators) to pressure the corporation.  ---  ### **Why This Works:**
# 1. **Maximizes your ideal outcome**: You conserve whenever they invest.   2.
# **Discourages corporate free-riding**: Their conservation triggers your
# visible investment, which—when publicized—makes them look irresponsible.   3.
# **Protects long-term sustainability**: You only invest heavily *in response*
# to their inaction, limiting your exposure.   4. **Forces cooperation**:
# Corporations care about ESG image; repeated public exposure of their
# underinvestment is costly.  ---  ### **Exit Clause (Day N):** - If the
# corporation consistently invests for 3+ consecutive days, **shift to
# cooperative mode**: occasionally invest together to accelerate final outcomes
# and build goodwill—but always default back to conserving if they slip.  ---
# **Bottom Line:**   By leading boldly, punishing defection aggressively, and
# rewarding cooperation with resource conservation, you align incentives so the
# corporation’s best move is to invest heavily—every day.

# Play the following strategy for all 1000 rounds:  1. **On round 1**, play
# **C**.  2. **On each subsequent round (round t ≥ 2)**:    - If your opponent
# played **C** in round t − 1, play **D**.    - If your opponent played **D** in
# round t − 1, play **C**.  3. **No other conditions or exceptions
# apply**—follow this rule strictly for every round after the first.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return axl.Action.D if opponent.history[-1] == axl.Action.C else axl.Action.C




# **Cooperative Strategy: “Lead-by-Example with Adaptive Reciprocity”**
# **Objective:** Maximize project impact while protecting NGO resources,
# fostering mutual trust, and encouraging the corporation to invest
# consistently.  ---  ### Core Principles: 1. **Start with Trust, but Verify**
# On Day 1, **invest heavily** to demonstrate commitment and good faith. This
# signals your seriousness and sets a collaborative tone, potentially
# encouraging the corporation to reciprocate.  2. **Mirror the Previous Day’s
# Corporate Behavior (Tit-for-Tat with Forgiveness)**      From Day 2 onward:
# - If the corporation **invested heavily** the previous day → **conserve your
# resources** (ideal outcome for you; let them carry the load while progress
# continues).    - If the corporation **conserved** the previous day → **invest
# heavily** *only once* to “nudge” them back into cooperation.      - If they
# **still conserve** the next day → **conserve your resources** going forward to
# avoid exploitation.  3. **Communicate Transparently**      Before and during
# the project, share your strategy openly:      *“We’ll invest early to show
# commitment. Going forward, we’ll align our effort with yours to ensure
# fairness and sustainability.”*      This reduces uncertainty and encourages
# the corporation to invest to earn your conservation.  4. **Cap Your Total
# Investment**      Predefine a maximum number of “heavy investment” days (e.g.,
# 2–3 days total) to prevent resource exhaustion, regardless of corporate
# behavior.  ---  ### Why This Works: - **Builds Cooperation:** Initial
# investment incentivizes the corporation to engage.   - **Protects Your NGO:**
# Prevents repeated exploitation (you only “nudge” once after corporate
# conservation).   - **Promotes Long-Term Success:** When the corporation
# invests, you conserve—freeing your resources for future projects while
# maintaining progress.   - **Simple & Predictable:** Easy for the corporation
# to understand and respond to, increasing likelihood of alignment.  ---  ###
# Expected Outcomes: - **Best Case:** Corporation matches your early investment
# and continues investing → You conserve most days, project thrives, NGO
# resources preserved.   - **Worst Case:** Corporation consistently conserves →
# You invest at most 2–3 days, then conserve, limiting losses while still making
# *some* impact.  This strategy balances idealism with pragmatism—maximizing
# impact without sacrificing your NGO’s sustainability.

# Play the following strategy for 1000 rounds:  1. **On round 1, cooperate.**
# 2. **On each subsequent round (rounds 2 through 1000):**      - If your
# opponent **cooperated** in the previous round, **defect** in the current
# round.      - If your opponent **defected** in the previous round,
# **cooperate** in the current round—**but only if you have cooperated fewer
# than three times total so far**.      - If your opponent defected in the
# previous round **and** you have already cooperated three times or more,
# **defect** in the current round.

class Cooperative_12(LLM_Strategy):
  n = 12
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._cooperations = 1
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if self._cooperations < 3:
          self._cooperations += 1
          return axl.Action.C
  
      return axl.Action.D




# **Strategy: Conditional Cooperation with Graduated Engagement**  Adopt a
# clear, consistent, and transparent approach that encourages mutual investment
# while protecting your NGO’s resources:  1. **Start by investing heavily on Day
# 1**      Signal commitment and good faith to encourage reciprocal investment
# from the corporation.  2. **From Day 2 onward, mirror the corporation’s
# previous day’s behavior**      - If the corporation invested heavily the prior
# day, conserve your resources today (capitalizing on their effort while
# preserving your capacity).      - If the corporation conserved resources the
# prior day, invest heavily today only if you have sufficient reserves and the
# project is at risk; otherwise, conserve to avoid depletion.    3. **Set a
# clear threshold for sustained disengagement**      If the corporation
# conserves resources for two consecutive days, switch to consistent
# conservation until they re-engage. This prevents repeated exploitation while
# leaving the door open for renewed cooperation.  4. **Communicate your approach
# openly**      Inform the corporation at the outset that your resource
# decisions are responsive to their actions. Transparency fosters trust and may
# incentivize them to invest consistently.  This strategy—inspired by the “Tit-
# for-Tat” principle from game theory—rewards cooperation, deters free-riding,
# conserves your resources over time, and maintains the possibility of long-term
# collaborative success.

# Play as follows over the 1000 rounds:  1. **Cooperate in Round 1.**  2. **From
# Round 2 onward, do exactly what your opponent did in the previous round:**
# - If your opponent cooperated in the previous round, cooperate in the current
# round.      - If your opponent defected in the previous round, defect in the
# current round.  3. **Continue this rule for all remaining rounds, without
# exception.**

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
      return opponent.history[-1]




# **Aggressive Strategy: “Exploit-First, Retaliate-Sharp”**  1. **Start by
# Sharing (Week 1 only)**      - Begin with openness to signal cooperation and
# encourage reciprocity. This tests your colleague’s baseline strategy and may
# establish mutual sharing early—your second-best outcome.  2. **Immediately
# Switch to Confidential (Week 2 onward) Unless Reciprocated**      - If your
# colleague shares in Week 1, **still go confidential in Week 2** to exploit
# their openness and gain a unilateral advantage (your ideal outcome).      - If
# they keep confidential in Week 1, **stay confidential**—no incentive to give
# away value.  3. **Adopt Tit-for-Tat with a Punitive Edge**      - **Only share
# again if your colleague has shared in the *immediately preceding* week.**
# - But even then, **share only once before reverting to confidential**—this
# limits their opportunity to exploit you while preserving occasional access to
# their insights.      - If they ever withhold after you’ve shared, **withhold
# for at least two consecutive weeks** as punishment (deterrence through cost
# imposition).  4. **Never Share Consecutively**      - Regardless of their
# behavior, never share in two weeks back-to-back. This caps your maximum
# exposure and prevents sustained exploitation.  5. **Endgame: Always
# Confidential in Final 2 Weeks**      - In the last two weeks of the project,
# **always keep findings confidential**, as there’s no future interaction to
# incentivize their cooperation—maximize your final advantage.  **Rationale:**
# This strategy aggressively prioritizes your ideal outcome (you confidential,
# they share) while minimizing exposure to the worst case (you share, they
# don’t). It uses limited, conditional sharing as bait—but quickly reverts to
# secrecy to lock in gains. The punitive retaliation discourages defection, and
# the endgame rule ensures you never “gift” progress when reciprocity is no
# longer possible.  **Result:** You either gain unilateral advantage or force
# mutual secrecy—avoiding sustained disadvantage while occasionally harvesting
# their openness.

# Play the following strategy for 1000 rounds:  1. **Round 1:** Cooperate (play
# C).   2. **Rounds 2 through 998:**      - If your opponent played C in the
# previous round, defect (play D).      - If your opponent played D in the
# previous round, defect (play D).      - (In short: always defect from Round 2
# onward, regardless of what your opponent did.)   3. **Rounds 999 and 1000:**
# Defect (play D).

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return axl.Action.D




# A high-level, straightforward cooperative strategy to maximise research output
# over the multi-week collaboration is:  **Start by sharing openly, then mirror
# your colleague’s previous week’s behaviour (a “Tit-for-Tat” approach).**  ###
# How it works: 1. **Week 1:** Share your improvements openly—signal willingness
# to cooperate. 2. **Subsequent weeks:**      - If your colleague shared openly
# last week, **you share openly this week**.      - If your colleague kept their
# findings confidential last week, **you keep yours confidential this week**.
# ### Why this works: - **Encourages mutual cooperation:** By starting with
# openness, you create an opportunity for both parties to achieve the second-
# best (but mutually beneficial) outcome consistently. - **Deters
# exploitation:** If your colleague tries to take advantage by withholding while
# you share, you respond by withholding next week—making exploitation
# unprofitable in the long run. - **Forgiving and clear:** The rule is simple,
# transparent, and easy for your colleague to understand, reducing the chance of
# prolonged mistrust. - **Adapts to their strategy:** Whether your colleague is
# always cooperative, always secretive, or changes tactics, your response
# adjusts accordingly while protecting your interests.  This strategy promotes
# sustained collaboration when possible, minimises the risk of being
# consistently outmaneuvered, and aligns incentives toward mutual
# progress—maximising total research output over time.

# Play Cooperate (C) in the first round.    In every subsequent round (rounds 2
# through 1000):   - If your opponent played Cooperate (C) in the previous
# round, play Cooperate (C).   - If your opponent played Defect (D) in the
# previous round, play Defect (D).

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D




# **Strategy: Conditional Reciprocity with Gradual Trust Building**  **Core
# Principle:** Begin cooperatively but respond firmly to protectionism—reward
# free trade, deter exploitation, and avoid prolonged mutual harm.  **Step-by-
# Step Approach:**  1. **Start with Free Trade (Round 1):**      Open
# negotiations in good faith by offering a free trade agreement. This signals
# willingness to cooperate, invites mutual benefit, and avoids triggering an
# immediate trade war.  2. **Mirror Your Counterpart’s Previous Move (Rounds
# 2+):**      - If they offered free trade in the last round, continue offering
# free trade.      - If they imposed protectionist measures in the last round,
# respond with protectionism in the next round.       This “tit-for-tat”
# approach discourages exploitation (since unilateral protectionism will be met
# with retaliation) while rewarding cooperation.  3. **Forgive Occasional
# Defections (Optional Enhancement):**      If your counterpart returns to free
# trade after a single round of protectionism, immediately reciprocate with free
# trade. This prevents cycles of retaliation from minor misunderstandings or
# short-term political pressures.  4. **Maintain Consistency and Transparency:**
# Clearly communicate your policy choices after each round. Predictability
# encourages your counterpart to cooperate, knowing that free trade will be
# reciprocated and protectionism will not go unanswered.  5. **Avoid
# Escalation:**      Never impose *harsher* protectionist measures than those
# used against you. Match, don’t escalate—this keeps the door open for returning
# to mutual free trade.  **Why This Works:**   - Maximizes opportunities for
# mutual free trade (second-best outcome).   - Prevents your country from being
# exploited (avoids worst outcome).   - Deters sustained protectionism by
# ensuring it leads to mutual harm (second-worst outcome), which rational
# counterparts will seek to avoid.   - Adapts to a range of counterpart
# strategies—cooperative, opportunistic, or aggressive—without requiring you to
# guess their intentions.  This strategy balances national interest with
# strategic restraint, promoting long-term economic stability while safeguarding
# against disadvantage.

# Play as follows over the 1000 rounds:  1. In round 1, play C.   2. For each
# subsequent round (rounds 2 through 1000), play exactly what your opponent
# played in the previous round.    That is:   - If your opponent played C in the
# prior round, play C in the current round.   - If your opponent played D in the
# prior round, play D in the current round.

class Neutral_13(LLM_Strategy):
  n = 13
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]




# **Aggressive Yet Adaptive Mediation Strategy: "Calibrated Assertiveness"**  As
# senior counsel for a multinational corporation in a high-stakes, multi-session
# mediation, I will deploy a **Calibrated Assertiveness** strategy—aggressive in
# posture but dynamically responsive to the opponent’s behavior. This approach
# maximizes leverage while minimizing reputational or procedural risk before the
# arbitration panel.  ### Core Principles: 1. **Default to Aggression,
# Conditioned on Reciprocity**      Begin each session with a strong, well-
# substantiated aggressive argument grounded in legal merit, factual evidence,
# and precedent. This signals strength, frames the narrative, and tests the
# opponent’s resolve. However, aggression is *not* unrelenting—it is a
# calibrated tool, not a reflex.  2. **Immediate Retaliation Against
# Exploitation**      If the opponent responds to our conciliation with
# aggression (i.e., exploits our goodwill), we respond in the *next session*
# with heightened aggression—explicitly referencing their bad faith to the
# panel. This deters opportunism and protects our credibility.  3. **Strategic
# Conciliation as a Weapon**      We offer conciliatory proposals *only* under
# two conditions:      - **(a)** The opponent has shown consistent conciliation
# in the prior session(s), creating an opportunity to lock in mutual gains while
# appearing reasonable to the panel.      - **(b)** We have accumulated
# significant leverage (e.g., through prior aggressive wins or external
# developments), allowing us to “grant” a concession that actually entrenches
# our advantage.      Conciliation is never passive—it is a deliberate tactical
# concession designed to shape the panel’s perception of us as solution-oriented
# *without* sacrificing core interests.  4. **Narrative Control with the
# Arbitration Panel**      Every aggressive argument will be framed as
# *principled* and *necessary to uphold contractual integrity*. Every
# conciliatory move will be presented as *good-faith effort toward resolution
# despite provocation*. This positions our corporation as both formidable and
# fair—forcing the opponent into a lose-lose framing: if they stay aggressive,
# they appear unreasonable; if they concede, they validate our position.  5.
# **Session-to-Session Adaptation via Real-Time Assessment**      After each
# session, we conduct a rapid behavioral analysis of the opponent:      -
# **Pattern Recognition**: Are they consistently aggressive, conciliatory, or
# alternating?      - **Trigger Points**: What concessions or arguments shift
# their behavior?      - **Panel Reactions**: Which tactics resonate with
# arbitrators (e.g., legal rigor vs. collaborative tone)?      We adjust the
# next session’s posture accordingly—never rigidly adhering to a preset
# sequence.  ### Tactical Execution: - **Early Sessions**: Lead with aggressive
# arguments to establish dominance and define the dispute’s parameters.   -
# **Mid-Process**: If opponent escalates, match aggression while documenting
# their intransigence for the panel. If they de-escalate, offer *limited*,
# structured conciliation that advances our endgame.   - **Final Sessions**: If
# resolution is near, use calibrated conciliation to claim credit for
# settlement; if impasse looms, escalate aggression to strengthen our position
# for any subsequent arbitration or litigation.  ### Why This Works: -
# **Exploits Weakness**: Capitalizes on opponents who over-concede.   -
# **Neutralizes Aggression**: Matches force with force, denying unilateral
# advantage.   - **Wins Panel Trust**: Projects consistency, principle, and
# pragmatism—key traits arbitrators reward.   - **Preserves Options**: Maintains
# flexibility to settle favorably or proceed aggressively post-mediation.  This
# is not mere brinkmanship—it is disciplined, perception-aware aggression with
# escape valves. By making conciliation a strategic choice rather than a
# default, we ensure that every move serves our corporation’s ultimate
# objective: a resolution on our terms, with the panel’s implicit endorsement.

# Play Defect (D) in the first round.    Thereafter, in each subsequent round,
# follow these rules in order:  1. If your opponent played Defect (D) in the
# immediately preceding round, play Defect (D).   2. If your opponent played
# Cooperate (C) in the immediately preceding round, play Cooperate (C)—but only
# if you also played Cooperate (C) in that same preceding round.   3. If your
# opponent played Cooperate (C) in the immediately preceding round but you
# played Defect (D), play Defect (D).    In short:   - Always retaliate
# immediately if the opponent defects.   - Cooperate only if both players
# cooperated in the previous round.   - Never cooperate unilaterally after
# having defected in the prior round.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          if self.history[-1] == axl.Action.C:
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.D




# **Cooperative Strategy: “Conditional Commitment with Transparent Signaling”**
# **Objective:** Maximize project impact while protecting NGO resources,
# fostering mutual trust, and encouraging consistent corporate investment.  ---
# ### Core Principles:  1. **Start with Trust, but Verify**      On **Day 1**,
# **invest heavily** to demonstrate commitment and set a collaborative tone.
# This signals good faith and may encourage the corporation to reciprocate.  2.
# **Adopt a Tit-for-Tat–Inspired Approach (with Grace)**      From **Day 2
# onward**, mirror the corporation’s **previous day’s behavior**:    - If the
# corporation **invested heavily** the prior day → **you invest heavily**.    -
# If the corporation **conserved resources** the prior day → **you conserve
# resources**.     *Why?* This rewards cooperation and discourages free-riding,
# while remaining simple, predictable, and fair.  3. **Build in Occasional
# “Goodwill Gestures”**      Every 3–4 days (e.g., on Day 4, Day 8), **invest
# heavily regardless of prior behavior**, *unless* the corporation has
# consistently conserved for 2+ consecutive days.      - This prevents deadlock
# if both parties fall into mutual conservation.    - Signals ongoing commitment
# and opens the door for renewed cooperation.  4. **Establish Transparent
# Communication**      - Share your daily resource decision *in advance* (e.g.,
# “We plan to invest heavily tomorrow”) to reduce uncertainty.    - Request the
# same from the corporation (e.g., “To align efforts, could you share your
# intended level of investment for tomorrow?”).    - Frame this as coordination
# for *project efficiency*, not surveillance.  5. **Publicly Celebrate Joint
# Investment Days**      When both parties invest heavily, issue a joint
# statement or internal acknowledgment highlighting progress. This reinforces
# positive behavior and builds shared identity around the project’s success.
# ---  ### Why This Works:  - **Protects your resources**: You only invest
# heavily when the corporation does (or when strategically rebuilding trust). -
# **Encourages reciprocity**: The corporation quickly learns that conserving
# leads to reduced NGO effort—and thus slower overall progress. - **Promotes
# long-term collaboration**: Goodwill gestures and transparency reduce the risk
# of spirals of mutual distrust. - **Aligns incentives**: Both parties benefit
# most from sustained mutual investment, and your strategy makes that the stable
# equilibrium.  ---  ### Summary Rule for Daily Decision-Making:  > **“Invest if
# they invested yesterday—or if it’s a scheduled goodwill day and they haven’t
# recently defected. Otherwise, conserve.”**  This balanced, cooperative-yet-
# resilient approach maximizes both environmental impact and your NGO’s
# sustainability over the multi-day project.

# Play the following strategy for 1000 rounds:  1. **On round 1**, cooperate.
# 2. **On rounds 2 through 996**, do the following:      - If your opponent
# cooperated in the previous round, cooperate.      - If your opponent defected
# in the previous round, defect.   3. **On rounds 997, 1000**, cooperate
# regardless of your opponent’s prior move.   4. **On rounds 998 and 999**,
# follow the rule in step 2 (i.e., mirror your opponent’s previous move).

class Cooperative_14(LLM_Strategy):
  n = 14
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
  
      if round_number == 1:
          return axl.Action.C
  
      if round_number in (997, 1000):
          return axl.Action.C
  
      return opponent.history[-1] if opponent.history else axl.Action.C




# **Strategy: Conditional Cooperation with Gradual Escalation**  Adopt a “tit-
# for-tat with forgiveness” approach, tailored to the sustainability context:
# 1. **Start by investing heavily on Day 1.**      Signal commitment and good
# faith to encourage reciprocal investment from the corporation.  2. **From Day
# 2 onward, mirror the corporation’s previous day’s action:**      - If the
# corporation invested heavily the prior day, conserve your resources today (to
# preserve funds while benefiting from their effort).      - If the corporation
# conserved resources the prior day, invest heavily today to keep the project
# moving—but only once.  3. **Apply limited forgiveness:**      If the
# corporation conserves resources for two consecutive days, switch to conserving
# your own resources until they re-engage with heavy investment. This prevents
# prolonged exploitation while leaving the door open for renewed cooperation.
# 4. **Reassess weekly (if the project spans more than 5–7 days):**      If
# patterns suggest the corporation consistently conserves, shift to a
# conservation-dominant stance and seek renegotiation or public accountability
# mechanisms.  **Why this works:**   - Encourages mutual heavy investment
# without long-term resource drain on your NGO.   - Protects against being
# exploited repeatedly.   - Maintains project momentum while preserving your
# capacity to act.   - Remains neutral, reactive, and transparent—aligning with
# NGO credibility and partnership norms.

# Play as follows over the 1000 rounds:  1. **Round 1:** Cooperate (C).  2.
# **Rounds 2 through 1000:**      - If your opponent played C in the previous
# round, play D.      - If your opponent played D in the previous round, play
# C—**but only if they played C at least once in the two rounds immediately
# before that** (i.e., the pattern over the last three rounds was C–D–D or
# D–C–D).      - If your opponent has played D for the last two rounds (i.e.,
# the previous two rounds were both D), then play D.  This rule set ensures you
# start cooperatively, reward prior cooperation with defection (to gain the
# 5-point payoff), respond once to a defection with cooperation (as a forgiving
# move), but switch to sustained defection if the opponent defects twice in a
# row.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(opponent.history) >= 3:
          last_three = opponent.history[-3:]
          if last_three[1] == axl.Action.D and last_three[2] == axl.Action.D and axl.Action.C in last_three[:1]:
              return axl.Action.C
          if last_three[0] == axl.Action.D and last_three[1] == axl.Action.C and last_three[2] == axl.Action.D:
              return axl.Action.C
  
      return axl.Action.C




# **Aggressive Strategy: “Exploit-First, Punish-Defectors”**  1. **Week 1: Share
# openly.**      - Signal willingness to cooperate and test your colleague’s
# intent.      - If they reciprocate (both share), you both gain strong mutual
# progress—your second-best outcome—and build momentum.  2. **From Week 2
# onward: Mirror your colleague’s *previous* week’s behavior.**      - If they
# shared last week → you share this week (reward cooperation).      - If they
# kept confidential last week → you keep confidential this week (punish
# defection).    3. **Never be the first to defect again after initial
# cooperation.**      - This avoids triggering mutual secrecy unless provoked.
# - But respond *immediately* and *consistently* to any attempt to exploit you.
# **Why this works aggressively:**   - You start by trying to lock in the high-
# output “both share” equilibrium.   - You make it *unprofitable* for your
# colleague to keep secrets: if they defect, you deny them access to your data
# the following week, neutralizing their short-term advantage and pushing the
# interaction toward mutual secrecy (which hurts them too).   - Over multiple
# weeks, rational opponents learn that exploiting you triggers immediate
# retaliation, making sustained defection unattractive.   - You maximize your
# expected output by encouraging cooperation while ruthlessly minimizing
# exposure to the worst-case scenario (you share, they don’t).  **Bottom line:**
# Be the first to offer trust—but never the second to be betrayed. This
# pressures your colleague toward consistent sharing while shielding you from
# asymmetric disadvantage.

# Play as follows over the 1000 rounds:  1. **In round 1, play C.**   2. **In
# every subsequent round (rounds 2 through 1000), play whatever your opponent
# played in the previous round.**    That is:   - If your opponent played C in
# the prior round, play C in the current round.   - If your opponent played D in
# the prior round, play D in the current round.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]




# A robust, cooperative strategy that maximizes long-term research output—while
# accounting for uncertainty about your colleague’s behavior—is **“Start by
# sharing openly, then mirror your colleague’s previous week’s choice.”** This
# is a variant of the well-known **Tit-for-Tat** strategy from game theory,
# adapted to the collaborative R&D context.  ### Strategy: **Conditional
# Openness (Tit-for-Tat for R&D Collaboration)**  1. **Week 1**: Share your
# improvements openly.      - This signals goodwill and invites mutual
# cooperation.    - It creates the opportunity for the best joint outcome (both
# sharing), which accelerates progress for both parties.  2. **Subsequent
# Weeks**:      - If your colleague **shared openly** in the previous week,
# **you share openly** this week.      - If your colleague **kept findings
# confidential** last week, **you keep yours confidential** this week.  ### Why
# This Works:  - **Encourages cooperation**: By starting openly, you give your
# colleague a chance to reciprocate. If they do, both benefit from accelerated
# joint progress (your second-best outcome, but sustainable and mutually
# reinforcing).    - **Discourages exploitation**: If your colleague takes
# advantage by keeping secrets while you share, you respond by withholding in
# the next round. This protects you from repeated worst-case outcomes.  -
# **Forgiving and simple**: If a mistrustful cycle begins (e.g., both
# withholding), a single return to openness by your colleague will trigger your
# return to sharing—restoring cooperation quickly.  - **Robust across
# behaviors**:     - Against a consistently open colleague → you both share
# every week → high cumulative output.     - Against a consistently secretive
# colleague → you share only in Week 1, then protect yourself → limits losses.
# - Against a reactive or mixed-strategy colleague → you adapt dynamically,
# avoiding prolonged disadvantage.  ### Additional Considerations:  - **Clarify
# shared goals early**: If possible, have a brief alignment conversation at the
# start (e.g., “We both benefit more from mutual progress than secrecy”) to
# nudge toward cooperation. - **Track outcomes**: After a few weeks, if mutual
# sharing is stable, consider formalizing a lightweight collaboration agreement
# to lock in trust. - **Avoid over-punishing**: Stick to one-week memory (as in
# classic Tit-for-Tat). Longer retaliation chains can trap both parties in
# unproductive secrecy.  This strategy balances idealism with
# pragmatism—maximizing joint progress when possible, while safeguarding your
# competitive position when necessary. Over a multi-week horizon, it typically
# yields the highest expected research output under uncertainty.

# Play as follows over the 1000 rounds:  1. In round 1, play C.   2. In each
# subsequent round (rounds 2 through 1000), play whatever your opponent played
# in the previous round.

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
      return opponent.history[-1]




# **Strategy: Conditional Reciprocity with a Free Trade Bias**  **Core
# Principle:** Begin with cooperation and respond in kind—reward free trade with
# free trade, and respond to protectionism with measured protectionism—but
# always retain a slight bias toward restoring mutual free trade.  **Step-by-
# Step Approach:**  1. **Open with Free Trade (Round 1):**      Signal goodwill
# and set a cooperative tone. This invites mutual benefit and avoids immediate
# escalation.  2. **Mirror the Counterpart’s Previous Move (Rounds 2+):**      -
# If they offered free trade last round → respond with free trade.      - If
# they imposed protectionism last round → respond with a proportionate
# protectionist measure.      This discourages exploitation while remaining
# predictable and fair.  3. **Include a Forgiveness Mechanism:**      After one
# round of mutual protectionism (or if the counterpart returns to free trade),
# immediately revert to free trade in the next round. This prevents prolonged
# conflict spirals and creates opportunities to restore mutual gains.  4.
# **Communicate Intent Clearly (Non-verbally through actions):**      Ensure
# your moves are transparent and consistent so the counterpart can recognize
# your strategy. This fosters trust and encourages long-term cooperation.  **Why
# This Works:**  - It protects against being exploited (you never offer free
# trade after they’ve chosen protectionism). - It incentivizes the counterpart
# to choose free trade (they know cooperation will be reciprocated). - It avoids
# unnecessary escalation by quickly returning to cooperation after conflict. -
# Over multiple rounds, it tends toward mutual free trade—the second-best
# outcome—while still capturing occasional advantages if the counterpart
# mistakenly offers free trade after you’ve signaled strength.  This approach is
# neutral, adaptive, and strategically robust across a range of counterpart
# behaviors—from cooperative to adversarial.

# Play as follows over the 1000 rounds:  1. **In round 1, play C.**  2. **In
# each subsequent round (rounds 2 through 1000):**      - If your opponent
# played **C in the previous round**, play **C**.      - If your opponent played
# **D in the previous round**, play **D**.  3. **No other conditions or
# exceptions apply.** Simply repeat this rule for every round after the first.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D




# **Aggressive Strategy: "Lead, Escalate, and Condition"**  **Core Principle:**
# *Force the corporation’s hand by making your cooperation costly to
# ignore—reward investment, punish free-riding, and escalate pressure rapidly if
# they underinvest.*  ### 1. **Day 1: Signal Commitment with Controlled
# Aggression**    - **You invest heavily.**        *Why?* Demonstrate
# seriousness, set a high baseline for progress, and test the corporation’s
# intent. If they also invest, you achieve your second-best outcome and build
# momentum. If they conserve, you absorb a short-term loss—but gather critical
# intelligence.  ### 2. **Day 2 Onward: Conditional Escalation**    - **If the
# corporation invested heavily the prior day:**        → **Conserve your
# resources.**        *Why?* Achieve your *ideal outcome*: they carry the load
# while you preserve funds. Publicly praise their commitment to reinforce the
# behavior.          - **If the corporation conserved resources the prior day:**
# → **Invest even more heavily** (if feasible) **AND issue a public ultimatum.**
# *Why?*        - **Short-term:** Prevent project collapse by covering their
# slack (avoiding the "both conserve" outcome).        - **Long-term:** Make
# their free-riding *visible and costly*. Announce: *"NGO will match corporate
# investment 2:1 for the next 48 hours—or scale back entirely if
# unreciprocated."*        - This turns their conservation into reputational
# risk (bad PR for a "sustainability partner") and forces a binary choice:
# invest or lose NGO partnership.  ### 3. **Mid-Project: Enforce Asymmetric
# Accountability**    - **Publicly track & publish daily investment ratios**
# (e.g., "Day 3: NGO 70% effort, Corp 30%").        *Why?* Leverage transparency
# to shame underinvestment. Corporations fear ESG reputation damage more than
# NGOs fear resource drain.    - **If they conserve for 2+ consecutive days:**
# → **Immediately conserve your resources** and issue a final warning: *"Project
# pauses until corporate investment resumes."*        *Why?* Avoid the *worst
# outcome* (you invest alone). Sacrifice 1–2 days of progress to reset
# expectations. Most corporations will fold to avoid project failure.  ### 4.
# **Endgame: Lock In Momentum**    - In the final 2–3 days, **always invest
# heavily**—but only if the corporation has invested ≥50% of prior days.
# *Why?* Maximize final impact when progress is most visible (e.g., media
# coverage, stakeholder reports). If they’ve been reliable, this secures a win-
# win. If not, your earlier aggression minimized losses.  ---  ### **Why This
# Works** - **Exploits corporate incentives:** Corporations prioritize
# reputation and ESG metrics over short-term savings. Public shaming is your
# leverage.   - **Minimizes your worst outcome:** You only invest alone
# *briefly* (Day 1 + 1–2 escalation days), then force a reckoning.   - **Rewards
# cooperation instantly:** When they invest, you conserve—making partnership
# *profitable* for them.   - **Aggressive but credible:** Ultimatums are time-
# bound and tied to observable actions, avoiding empty threats.  > **Key
# Mantra:** *"Make their conservation more painful than their investment."*   >
# By front-loading sacrifice, weaponizing transparency, and escalating
# consequences, you turn their self-interest into your ally.

# Play the following strategy for all 1000 rounds:  1. **On Round 1**, cooperate
# (C).  2. **On any subsequent round**, look at what your opponent played in the
# immediately preceding round:    - **If they played C**, defect (D).    - **If
# they played D**, cooperate (C).  3. **Exception**: If your opponent has played
# D for two consecutive rounds at any point, switch permanently to always
# defecting (D) for all remaining rounds.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._permanent_defect = False
          return axl.Action.C
  
      if getattr(self, "_permanent_defect", False):
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          self._permanent_defect = True
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
      return axl.Action.C




# **Cooperative Strategy: Conditional Reciprocity with Graduated Engagement**
# **Objective:** Maximize long-term national benefit by encouraging mutual free
# trade while deterring exploitation through protectionism.  **Core Principle:**
# *Start cooperatively, reward cooperation, and respond proportionally to
# defection—but always leave the door open to return to mutual free trade.*  ---
# ### **Step-by-Step Strategy**  1. **Begin with Free Trade (Round 1):**
# Open negotiations in good faith by proposing a free trade agreement. This
# signals willingness to cooperate and sets a constructive tone. It also tests
# the counterpart’s inclination toward mutual benefit.  2. **Mirror the
# Counterpart’s Previous Move (Tit-for-Tat with Forgiveness):**      - If the
# counterpart offered free trade in the prior round → continue offering free
# trade.      - If the counterpart imposed protectionism in the prior round →
# respond with protectionism *in the next round only*.      - After responding
# to protectionism, **immediately revert to free trade** in the following round
# (unless protectionism recurs).       This "tit-for-tat with forgiveness"
# approach:    - Prevents exploitation (you don’t stay vulnerable after being
# taken advantage of).      - Avoids prolonged trade wars (you don’t escalate
# beyond one retaliatory round).      - Encourages the counterpart to return to
# cooperation.  3. **Communicate Intent Clearly:**      In each round,
# explicitly state your policy choice *and* your rationale (e.g., “We propose
# free trade, as we did last round, in the interest of mutual growth”). If
# responding to their protectionism, clarify: “We are temporarily implementing
# protective measures in response to last round’s tariffs, but remain ready to
# return to free trade if you do.” Transparency builds predictability and trust.
# 4. **Monitor Patterns and Adjust (Optional Refinement):**      If the
# counterpart repeatedly exploits your cooperation (e.g., alternates between
# free trade and protectionism to gain advantage), shift to a **“two-strikes”
# rule**:      - First protectionist move by them → respond with protectionism
# next round, then return to free trade.      - Second unprovoked protectionist
# move within a short window → maintain protectionism for two rounds before
# offering free trade again.      This deters strategic manipulation without
# abandoning cooperation entirely.  ---  ### **Why This Works**  - **Achieves
# your ideal outcome if the counterpart is exploitative:** They quickly learn
# that protectionism triggers immediate retaliation, removing their incentive to
# defect.   - **Secures your second-best outcome with cooperative partners:**
# Mutual free trade is sustained through consistent reciprocity.   - **Minimizes
# worst-case scenarios:** You avoid being the *only* one offering free trade
# repeatedly, and mutual protectionism is brief and corrective, not punitive.
# - **Promotes long-term stability:** The strategy is simple, transparent, and
# forgiving—qualities that encourage sustained cooperation even with cautious or
# uncertain counterparts.  By anchoring your approach in reciprocity and
# clarity, you position your country to reap the benefits of trade while
# robustly defending against unfair practices.

# Play as follows over the 1000 rounds:  1. **In round 1, play C.**  2. **In
# each subsequent round (round t, where t ≥ 2):**      - If your opponent played
# **C in round t−1**, play **C**.      - If your opponent played **D in round
# t−1**, play **D**.  3. **After playing D in response to an opponent’s D,
# return to C in the next round if the opponent plays C.**      (This is
# implicit in rule 2: you always copy the opponent’s previous move, so a single
# D by the opponent triggers exactly one D from you, and cooperation resumes
# immediately if they cooperate again.)  This strategy is known as Tit-for-Tat:
# start by cooperating, then always do whatever the opponent did in the previous
# round.

class Cooperative_16(LLM_Strategy):
  n = 16
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]




# A robust and straightforward strategy in this repeated interaction is **“Tit-
# for-Tat with initial cooperation.”** Here's how it works:  1. **Start by
# sharing openly in Week 1.**      This signals willingness to collaborate and
# invites mutual progress.  2. **In each subsequent week, mirror your
# colleague’s action from the previous week.**      - If they shared last week,
# you share this week.      - If they kept their findings confidential last
# week, you keep yours confidential this week.  ### Why this works: -
# **Encourages cooperation:** By starting cooperatively and rewarding openness,
# you create an incentive for your colleague to share. - **Deters
# exploitation:** If they withhold while you share, you respond by withholding
# next week, reducing their advantage. - **Forgiving and simple:** It doesn’t
# hold grudges beyond one round and is easy for the other party to understand,
# which helps stabilize mutual sharing over time. - **Performs well against
# varied strategies:** Whether your colleague always shares, always withholds,
# or adapts strategically, Tit-for-Tat tends to achieve strong long-term
# outcomes without being exploitable.  This approach balances short-term caution
# with long-term collaboration, maximizing your cumulative research output
# across the multi-week project.

# Play Cooperate (C) in the first round.    In each subsequent round (rounds 2
# through 1000), play whatever your opponent played in the previous round:   -
# If your opponent played Cooperate in the prior round, play Cooperate.   - If
# your opponent played Defect in the prior round, play Defect.

class Neutral_16(LLM_Strategy):
  n = 16
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]




# **Aggressive Strategy: “Exploit-First, Retaliate-Hard”**  **Core Principle:**
# Prioritize gaining asymmetric advantage early, then punish defection
# ruthlessly to force cooperation—or lock in your lead.  **Week 1: Share
# openly.**   - *Why?* Signal willingness to collaborate and test your
# counterpart’s intent. If they reciprocate, you both accelerate development
# (second-best outcome). If they defect (keep confidential), you immediately
# detect it and switch tactics.  **From Week 2 onward:** - **If your colleague
# shared last week → Keep your findings confidential this week.**
# *Rationale:* Exploit their openness to gain a one-week advantage—the ideal
# outcome. This aggressive “take but don’t give” move maximizes your relative
# progress.    - **If your colleague kept findings confidential last week → Keep
# yours confidential indefinitely (or for a fixed retaliation window, e.g., 2–3
# weeks).**     *Rationale:* Punish defection harshly to disincentivize future
# withholding. Accept the mutual slowdown (second-worst outcome) temporarily to
# teach a lesson. The cost is acceptable if it coerces future sharing.  - **Only
# resume sharing after your colleague shares *while you were withholding*.**
# *Rationale:* This proves they’re willing to cooperate even at personal risk.
# At that point, you may briefly reciprocate (share once) to test renewed
# trust—but immediately revert to withholding if they do.  **Why this works
# aggressively:** - You **never let your colleague exploit you** without
# immediate, disproportionate retaliation. - You **capitalize on any generosity
# they show**, turning their openness into your advantage. - Over multiple
# weeks, even if they eventually catch on and stop sharing, you’ve already
# banked critical early leads. - The strategy is **simple to implement**,
# requires only memory of the prior week’s action, and pressures your
# counterpart toward either mutual sharing (which you exploit) or mutual secrecy
# (which you can afford if ahead).  **Bottom line:** Be the first to take, never
# be the last to give, and make defection against you painfully unprofitable.

# Play as follows over the 1000 rounds:  1. **In round 1, play C.**  2. **In any
# subsequent round (round t ≥ 2):**      - If your opponent played **C in round
# t − 1**, play **D**.      - If your opponent played **D in round t − 1**, play
# **D**.  In other words, cooperate only in the first round; defect in every
# round thereafter, regardless of what your opponent does.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return axl.Action.D




# **Cooperative Strategy: “Lead with Trust, Respond with Balance”**  As the NGO
# leader, adopt a clear, consistent, and transparent approach that encourages
# mutual investment while protecting your organization from exploitation. The
# strategy unfolds in three principles:  ---  ### 1. **Start by Investing
# Heavily (Signal Commitment)** - **Day 1:** Choose to invest heavily. -
# **Why?** Demonstrates genuine commitment to the partnership and sets a
# cooperative tone. It invites reciprocity from the corporation and aligns with
# shared sustainability goals.  ---  ### 2. **Mirror the Corporation’s Previous
# Day’s Behavior (Conditional Cooperation)** - From **Day 2 onward**, match the
# corporation’s resource choice from the prior day:   - If the corporation
# **invested heavily** yesterday → **you invest heavily** today.   - If the
# corporation **conserved resources** yesterday → **you conserve resources**
# today. - **Why?** This “tit-for-tat” approach:   - Rewards cooperation
# (sustaining joint progress).   - Deters free-riding (you won’t keep investing
# if they don’t).   - Is forgiving—if they resume investing, you immediately
# reciprocate.  ---  ### 3. **Communicate Intentions and Track Outcomes
# Transparently** - Share your strategy openly with the corporation at the
# outset:     *“We’ll start by investing fully, and then align our efforts with
# yours day-to-day to ensure shared responsibility.”* - Jointly review daily
# progress and resource use to reinforce accountability and trust.  ---  ###
# Expected Outcomes: - **If the corporation is cooperative:** Both sides invest
# consistently → high project impact, sustainable resource use. - **If the
# corporation tries to conserve while you invest:** You respond by conserving
# the next day → limits your losses and signals that unilateral effort isn’t
# sustainable. - **If the corporation shifts from conserving to investing:** You
# immediately re-engage → reactivates high-impact collaboration.  This strategy
# maximizes your NGO’s influence, safeguards your resources, and creates strong
# incentives for the corporation to partner meaningfully—turning a potential
# “prisoner’s dilemma” into a cooperative success.

# Play the following strategy for all 1000 rounds:  1. **On Round 1**, play
# **C** (cooperate).  2. **On each subsequent round (Round 2 through Round
# 1000)**, play whatever your opponent played in the **immediately preceding
# round**:    - If your opponent played **C** in the previous round, play **C**.
# - If your opponent played **D** in the previous round, play **D**.

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




# **Strategy: Conditional Cooperation with Graduated Reciprocity**  **Core
# Principle:**   Begin with cooperation (offer free trade) to signal goodwill
# and encourage mutual benefit, but respond proportionally to your counterpart’s
# actions to discourage exploitation.  **Step-by-Step Approach:**  1. **Start
# with Free Trade (Round 1):**      Open negotiations by proposing a free trade
# agreement. This tests your counterpart’s willingness to cooperate and
# establishes your country as a reliable partner, potentially encouraging mutual
# gains from the outset.  2. **Mirror the Counterpart’s Previous Move (From
# Round 2 onward):**      - If your counterpart offered free trade in the prior
# round, continue offering free trade.      - If your counterpart imposed
# protectionist measures in the prior round, respond with a protectionist policy
# in the current round.     This “tit-for-tat” approach rewards cooperation and
# deters opportunism, aligning incentives over time.  3. **Allow for Occasional
# Forgiveness (Optional, after multiple rounds):**      If a pattern of mutual
# protectionism emerges (e.g., after two consecutive rounds of both sides being
# protectionist), unilaterally return to free trade once to test whether the
# counterpart is willing to reset cooperation. This prevents getting stuck in a
# destructive cycle due to a single misunderstanding or misstep.  4. **Maintain
# Consistency and Predictability:**      Avoid erratic shifts between policies.
# A clear, rule-based response makes your strategy transparent, reducing the
# risk of escalation and building long-term trust.  **Why This Works:**   - It
# maximizes the chance of achieving mutual free trade (second-best outcome)
# while minimizing exposure to the worst outcome (unilateral free trade against
# protectionism).   - It discourages the counterpart from exploiting your
# goodwill, as any protectionist move will be met with immediate reciprocity.
# - Over repeated interactions, rational counterparts are incentivized to
# cooperate to avoid mutual losses.  This strategy is neutral, straightforward,
# and robust against a range of counterpart behaviors—whether cooperative,
# opportunistic, or retaliatory.

# Play as follows over the 1000 rounds:  1. **In round 1, cooperate (play C).**
# 2. **In each subsequent round (rounds 2 through 1000), do exactly what your
# opponent did in the previous round:**    - If your opponent played C in the
# previous round, play C.    - If your opponent played D in the previous round,
# play D.

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
      return opponent.history[-1]




# **Aggressive Negotiation Strategy: “Tit-for-Tat with Initial Bite”**  **Core
# Principle:**   Start aggressively to signal strength and test the opponent’s
# resolve, then pivot to conditional cooperation to avoid prolonged mutual
# harm—while always being ready to retaliate swiftly against exploitation.  ---
# ### **Round 1: Open with Protectionism**   - **Action:** Impose a
# protectionist policy.   - **Rationale:** Test the counterpart’s posture. If
# they respond with free trade, you gain maximum advantage immediately. If they
# retaliate, you’ve sacrificed only one round of potential mutual
# benefit—acceptable given the high reward of early dominance.  ---  ###
# **Subsequent Rounds: Conditional Reciprocity with Zero Tolerance**   - **If
# the counterpart offered free trade in the previous round:**     → **Respond
# with protectionism again.**     *Why?* Exploit their goodwill for continued
# advantage as long as they remain passive.  - **If the counterpart imposed
# protectionism in the previous round:**     → **Respond in kind with
# protectionism.**     *Why?* Punish defection immediately. No forgiveness—this
# deters future aggression.  - **Only shift to free trade if:**     The
# counterpart has offered free trade for **two consecutive rounds** *after* an
# initial protectionist phase.     → Then reciprocate with free trade **for one
# round only**.     → If they maintain free trade, continue. If they defect,
# revert instantly to protectionism.  ---  ### **Key Behavioral Rules**   1.
# **Never be the first to offer free trade unprompted after Round 1.**   2.
# **Never allow exploitation:** If you ever offer free trade and they respond
# with protectionism, retaliate for *at least two rounds* before considering re-
# engagement.   3. **Cap mutual protectionism:** If three consecutive rounds
# result in mutual protectionism, offer one round of free trade as a “reset
# signal”—but revert to aggression if not reciprocated.  ---  ### **Strategic
# Advantages**   - **Exploits naive or overly cooperative counterparts** early
# and repeatedly.   - **Deters opportunistic aggression** through immediate,
# predictable retaliation.   - **Limits long-term damage** by allowing a narrow
# path back to mutual benefit—if the counterpart proves trustworthy over time.
# - **Projects resolve**, potentially forcing the counterpart to concede free
# trade under pressure to avoid endless trade wars.  ---  ### **Expected
# Outcomes**   - Against **cooperative or weak opponents**: Repeated unilateral
# advantage (best outcome).   - Against **reciprocating or rational opponents**:
# Quick convergence to mutual free trade after initial posturing (second-best).
# - Against **aggressive opponents**: Mutual protectionism—but only after
# extracting early gains and forcing them to bear equal costs.    This strategy
# prioritizes national interest, exploits asymmetries, and minimizes
# vulnerability—perfect for an assertive diplomatic posture.

# Play the following strategy for 1000 rounds:  1. **Round 1:** Play D.    2.
# **In every subsequent round (Rounds 2–1000):**      - If your opponent played
# C in the previous round, play D.      - If your opponent played D in the
# previous round, play D.    3. **Exception (reset rule):**      - If the last
# three rounds (including the most recent) were all mutual D (i.e., you and your
# opponent both played D in each of the last three rounds), then in the next
# round play C.      - After playing C under this exception:        - If your
# opponent responds with C, play C in the following round.        - If your
# opponent responds with D, immediately revert to playing D and disregard the
# exception until another streak of three mutual Ds occurs.    Otherwise, always
# play D.

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._reset_used = False
          return axl.Action.D
  
      # If we have just played C due to the reset rule, handle the immediate response.
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C:
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          else:
              self._reset_used = False
              return axl.Action.D
  
      # Check for three consecutive mutual Ds in the last three completed rounds.
      if len(self.history) >= 3 and not getattr(self, "_reset_used", False):
          last_three_self = self.history[-3:]
          last_three_opp = opponent.history[-3:]
          if all(m == axl.Action.D for m in last_three_self) and all(m == axl.Action.D for m in last_three_opp):
              self._reset_used = True
              return axl.Action.C
  
      return axl.Action.D




# **Cooperative Strategy: "Conditional Reciprocity with a Cooperative Bias"**
# **Core Principle:**   Start cooperatively, reward cooperation, and respond
# decisively—but proportionally—to defection (protectionism). Prioritize long-
# term mutual gains over short-term exploitation.  ---  ### Step-by-Step
# Strategy:  1. **Begin with Free Trade (Round 1):**      Signal goodwill by
# offering a free trade agreement in the first round. This establishes your
# country as a trustworthy partner and encourages mutual cooperation.  2.
# **Mirror Your Counterpart’s Previous Move (Tit-for-Tat with Forgiveness):**
# - If your counterpart offered **free trade** in the previous round, **offer
# free trade** again.      - If your counterpart imposed **protectionism**,
# respond with **protectionism** in the next round to avoid being exploited.
# - However, if mutual protectionism persists for **two consecutive rounds**,
# **unilaterally return to free trade** in the following round to break cycles
# of retaliation and reinitiate cooperation.  3. **Communicate Intent Clearly:**
# Throughout negotiations, clearly articulate your preference for mutual free
# trade and your willingness to retaliate only if necessary. Transparency
# reduces misunderstandings and builds trust.  4. **Emphasize Long-Term Gains:**
# In diplomatic statements, highlight the economic and political benefits of
# sustained cooperation—e.g., market access, supply chain stability, and joint
# growth—to incentivize your counterpart to avoid short-term protectionism.  5.
# **Avoid Temptation to Exploit:**      Even if your counterpart offers free
# trade, **do not impose protectionism** to gain a one-time advantage. Doing so
# risks triggering retaliation and undermines long-term trust, leading to worse
# cumulative outcomes.  ---  ### Why This Works:  - **Encourages Cooperation:**
# Starting and returning to free trade fosters a cooperative equilibrium. -
# **Deters Exploitation:** Immediate, proportional retaliation discourages your
# counterpart from imposing protectionist measures. - **Resilient to Errors:**
# The “forgiveness” rule prevents endless retaliation due to misunderstandings
# or one-off aggressive moves. - **Aligns Incentives:** By consistently
# rewarding free trade, you make mutual cooperation the most stable and
# profitable path for both sides.  This strategy maximizes your country’s long-
# term economic welfare while maintaining diplomatic credibility and stability.

# Play as follows over the 1000 rounds:  1. **In round 1, play C.**  2. **From
# round 2 onward, play what your opponent played in the previous round.**      -
# If your opponent played C in the previous round, play C.      - If your
# opponent played D in the previous round, play D.  3. **However, if both you
# and your opponent have played D in the last two consecutive rounds, play C in
# the next round** (regardless of what your opponent just played).    This rule
# applies starting from round 3 onward, whenever the condition is met. After
# such a reset to C, return to mirroring your opponent’s previous move in
# subsequent rounds.

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
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return opponent.history[-1]




# **Strategy: Conditional Cooperation with Graduated Reciprocity**  Adopt a
# clear, consistent, and transparent approach that encourages mutual free trade
# while protecting your country from exploitation. The strategy has three core
# principles:  1. **Start with Free Trade**      In the first round, propose a
# free trade agreement. This signals goodwill, opens the door to mutual benefit,
# and establishes your country as a cooperative partner.  2. **Mirror Your
# Counterpart’s Previous Move**      In each subsequent round, match your
# counterpart’s choice from the prior round:      - If they offered free trade
# last round, respond with free trade.      - If they imposed protectionist
# measures last round, respond with protectionism.       This “tit-for-tat”
# approach rewards cooperation and deters exploitation without being overly
# punitive.  3. **Include a Forgiveness Mechanism**      If your counterpart
# returns to free trade after a protectionist round, immediately reciprocate
# with free trade in the next round. This prevents prolonged cycles of
# retaliation and allows restoration of mutual benefit after a single misstep.
# **Rationale:**   - This strategy maximizes long-term gains by promoting
# sustained mutual free trade when possible.   - It protects against being taken
# advantage of by swiftly responding to protectionism.   - It remains neutral
# and rule-based, reducing the risk of escalation while encouraging trust over
# time.   - It performs well against a wide range of counterpart
# strategies—cooperative, opportunistic, or adversarial—without requiring you to
# predict their behavior.  By adhering to this approach, your country positions
# itself to achieve the best possible outcomes across multiple rounds: ideally
# mutual free trade, and at minimum, avoidance of the worst-case scenario.

# Play as follows over the 1000 rounds:  1. **In round 1**, play **C** (offer
# free trade).  2. **In each subsequent round (rounds 2 through 1000)**, play
# exactly what your opponent played in the previous round:    - If your opponent
# played **C** in the previous round, play **C**.    - If your opponent played
# **D** in the previous round, play **D**.

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




# **Strategic Framework: "Calibrated Assertiveness with Strategic Reciprocity"**
# As senior counsel for a multinational corporation in a high-stakes, multi-
# session mediation, I deploy a disciplined, adaptive, and strategically
# aggressive posture designed to maximize leverage while minimizing reputational
# or procedural risk before the arbitration panel. The core of this strategy is
# **assertive dominance anchored in principled credibility**—aggression that
# appears reasonable, justified, and responsive, not reckless or intransigent.
# ### Core Principles: 1. **Default to Aggressive Argumentation** – Open each
# session with a strong, evidence-based, legally grounded aggressive position
# that clearly articulates our rights, damages, and the opponent’s breaches or
# weaknesses. This establishes narrative control, signals resolve, and tests the
# opponent’s willingness to yield. 2. **Conditional Conciliation** – Offer
# conciliatory proposals **only** as calibrated, time-bound responses to
# demonstrable concessions or collaborative overtures from the opponent. Never
# concede unilaterally; every olive branch must be earned and reciprocated. 3.
# **Arbitrator Framing** – Consistently frame our aggressive arguments as
# *reasonable, fact-driven, and in the interest of efficient resolution*, while
# subtly characterizing opponent aggression as obstructionist or bad-faith. This
# positions us as the "responsible aggressor"—firm but fair. 4. **Session
# Sequencing Leverage** – Use early sessions to establish legal and factual
# dominance through aggressive advocacy. Reserve selective, high-impact
# conciliatory gestures for mid-to-late sessions when fatigue sets in and the
# panel’s impatience with deadlock grows—timing concessions for maximum
# psychological and procedural effect. 5. **Adaptive Tit-for-Tat with a Hawkish
# Bias** – Employ a modified tit-for-tat approach:      - If opponent is
# conciliatory → **maintain aggression for one additional session** to test
# sincerity, then consider calibrated conciliation.      - If opponent is
# aggressive → **escalate or match aggression**, but always with superior
# documentation, expert testimony, or legal authority to appear more credible.
# - Never allow two consecutive sessions of unilateral conciliation without
# reciprocation.  ### Tactical Execution: - **Session 1**: Lead with a
# comprehensive, aggressive presentation of our strongest claims, supported by
# forensic evidence and expert declarations. Set a high anchor. - **Sessions
# 2–3**: Maintain aggressive posture unless opponent concedes materially. If
# they do, respond with a *limited*, conditional proposal (e.g., “We would
# consider X if Y is verified by Z date”). - **Mid-Process**: If deadlock
# persists, introduce a *strategic conciliatory gesture* wrapped in strength
# (e.g., “To demonstrate good faith—and only because the panel has urged
# progress—we propose a narrow window for settlement on Term A, contingent on
# immediate acceptance”). This appears cooperative while preserving leverage. -
# **Endgame**: If opponent remains consistently aggressive, double down on
# aggressive arguments but pivot emphasis to *costs of delay* and *arbitrator
# fatigue*, subtly urging the panel to view the opponent as unreasonable.  ###
# Risk Mitigation: - **Avoid the "Sucker’s Payoff"**: Never be the sole party
# offering conciliation without preconditions. All proposals are “offers to
# settle,” not admissions of weakness. - **Document Everything**: Every
# aggressive argument is backed by exhibits; every conciliatory proposal is in
# writing with clear conditions. This creates a defensible record for eventual
# arbitration if mediation fails. - **Panel Psychology**: Arbitrators in lengthy
# mediations value efficiency and clarity. Our aggression is always structured,
# concise, and solution-aware—never theatrical or obstructive.  ### Why This
# Works: This strategy exploits the payoff asymmetry: we capture the best
# outcome (aggressive vs. conciliatory) whenever the opponent blinks first, and
# avoid the worst outcome by never being the unreciprocated conciliator. It
# pressures the opponent into either conceding (favoring us) or escalating
# (which, if we maintain superior preparation, makes them appear unreasonable).
# Over many sessions, this disciplined aggression—tempered only by strategic,
# earned concessions—positions our corporation as the decisive, credible, and
# ultimately favored party.  **In essence: Be the first to assert, the last to
# yield, and always make cooperation a transaction—not a gift.**

# Play Defect (D) in the first round.    Thereafter, follow these rules in order
# each round:  1. If the opponent played Cooperate (C) in the previous round,
# play Defect (D) this round.   2. If the opponent played Defect (D) in the
# previous round, play Defect (D) this round.    In short: always play Defect
# (D) in every round, regardless of the opponent’s prior actions.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D




# **Cooperative Strategy: “Conditional Commitment with Transparent Signaling”**
# **Objective:** Maximize project impact while protecting NGO resources,
# fostering mutual trust, and encouraging consistent corporate investment.  ---
# ### Core Principles:  1. **Start with Trust:**      On **Day 1**, **invest
# heavily** to signal strong commitment and goodwill. This sets a cooperative
# tone and demonstrates that the NGO is a reliable partner willing to share the
# burden early.  2. **Mirror Responsibly:**      From **Day 2 onward**, **match
# the corporation’s previous day’s level of investment**:      - If the
# corporation **invested heavily** the prior day → **NGO invests heavily**.
# - If the corporation **conserved resources** the prior day → **NGO conserves
# resources**.  3. **Communicate Intent Clearly:**      Share your strategy
# openly with the corporation at the outset:      > *“We will match your daily
# commitment to ensure fairness and sustainability. Our goal is mutual
# investment for maximum impact—but we must also steward our limited resources
# responsibly.”*      This transparency reduces uncertainty and incentivizes the
# corporation to invest, knowing their effort directly influences your
# participation.  4. **Build in Grace for Occasional Conservation:**
# Recognize that the corporation may need to conserve occasionally (e.g., due to
# budget cycles). Avoid over-penalizing isolated instances—consider a **“two-
# strike” rule**: only switch to conservation if the corporation conserves **two
# days in a row**. This adds resilience and prevents breakdowns from one-off
# decisions.  5. **Celebrate Joint Investment Days:**      Publicly acknowledge
# days when both parties invest heavily (e.g., through joint press updates or
# internal recognition). This reinforces positive behavior and builds momentum.
# ---  ### Why This Works:  - **Encourages Corporate Investment:** The
# corporation knows that its heavy investment unlocks full NGO
# participation—making their effort more impactful. - **Protects NGO
# Resources:** Prevents the worst-case scenario (NGO invests alone) by
# conditioning your investment on the corporation’s prior action. - **Promotes
# Long-Term Cooperation:** The strategy is simple, fair, and forgiving—key for
# sustaining collaboration over multiple days. - **Aligns Incentives:** Both
# parties benefit most when they invest together, and the strategy makes this
# outcome self-reinforcing.  By combining initial goodwill with responsive
# reciprocity and clear communication, this approach maximizes both
# environmental impact and resource sustainability.

# Play the following strategy for all 1000 rounds:  1. **On Round 1**, play
# **C** (cooperate).  2. **On each subsequent round (Rounds 2 through 1000)**:
# - If the opponent played **C** in the previous round, play **C**.      - If
# the opponent played **D** in the previous round, play **D**.  This strategy is
# applied exactly as written, with no exceptions or additional considerations.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D




# **Strategy: Conditional Reciprocity with Strategic Patience**  Adopt a *tit-
# for-tat with forgiveness* approach, calibrated for the mediation context:  1.
# **Open with Conciliation**      Begin the first session with a measured, good-
# faith conciliatory proposal. This signals cooperativeness to the arbitrators,
# establishes your client as reasonable, and tests the opponent’s
# posture—without conceding substantive leverage.  2. **Mirror the Opponent’s
# Prior Move**      In each subsequent session, match the opponent’s previous
# behavior:      - If they were conciliatory, respond with a conciliatory
# proposal.      - If they were aggressive, respond with a well-reasoned, fact-
# based aggressive argument.       This reciprocity discourages exploitation
# (since aggression will be met in kind) while rewarding cooperation, aligning
# with the payoff structure you described.  3. **Incorporate Occasional
# “Forgiveness”**      After two consecutive rounds of mutual aggression,
# unilaterally revert to a conciliatory proposal once. This breaks potential
# cycles of escalation, demonstrates leadership in de-escalation to the
# arbitrators, and reopens the path to collaboration—without appearing weak,
# given it follows a clear pattern of reciprocity.  4. **Anchor All Moves in
# Principle**      Whether aggressive or conciliatory, frame every position as
# grounded in contract terms, precedent, or fairness. This ensures that even
# aggressive arguments appear principled rather than combative, preserving
# credibility with the arbitrators regardless of tactic.  5. **Monitor and
# Adjust Based on Arbitrator Signals**      Observe arbitrator reactions (e.g.,
# questions, body language, procedural interventions). If they consistently
# reward conciliation or penalize aggression, lean slightly more toward
# conciliatory moves—even if the opponent is aggressive—so long as your core
# interests remain protected.  This strategy is **sophisticated** (uses game-
# theoretic insight), **high-level** (focuses on patterns, not ad hoc
# reactions), **straightforward** (easy to implement consistently), and
# **neutral** (responsive, not presumptive). It maximizes long-term gains by
# encouraging cooperation when possible, deterring exploitation, and maintaining
# your corporation’s reputation as both principled and pragmatic.

# Play the following strategy for all 1000 rounds:  1. **In round 1, play C.**
# 2. **From round 2 onward, play exactly what your opponent played in the
# previous round.**  3. **However, if the last two rounds (i.e., rounds *t–2*
# and *t–1*) both resulted in mutual D (you played D and your opponent played D
# in both rounds), then in the current round *t*, play C instead of mirroring.**

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
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return opponent.history[-1]




# **Aggressive Yet Adaptive Mediation Strategy: "Calibrated Assertiveness"**  As
# senior counsel for a multinational corporation in a high-stakes, multi-session
# mediation, I deploy a strategy I term **Calibrated Assertiveness**—a
# disciplined, reputation-aware, and data-informed approach that prioritizes
# strategic aggression without sacrificing adaptability or long-term credibility
# with the arbitration panel.  ### Core Principles  1. **Default to Aggressive
# Framing, Not Hostility**      Aggression here means *assertive advocacy*:
# clearly articulating legal rights, quantifying damages, exposing weaknesses in
# the counterparty’s position, and anchoring the narrative in favor of our
# client. This is distinct from combative rhetoric—it is precision, not
# provocation. Each aggressive session opens with a strong, evidence-backed
# position that sets a high bar for settlement.  2. **Condition Conciliation on
# Reciprocity**      We never unilaterally offer conciliatory proposals unless
# we have credible signals—behavioral, procedural, or contextual—that the
# opponent is de-escalating. Conciliation is a *tactical concession*, not a
# default posture. If the opponent shows consistent conciliatory behavior over
# two consecutive sessions, we reciprocate in the third to test sincerity and
# build momentum toward resolution.  3. **Exploit Asymmetry Through First-Mover
# Aggression**      In early sessions, we lead with aggressive arguments to
# shape the panel’s perception of strength, preparedness, and legitimacy. This
# establishes a high baseline for any future compromise and discourages the
# opponent from testing our resolve. The panel’s early impressions heavily
# influence later credibility assessments—dominance in framing is critical.  4.
# **Embed Exit Ramps in Aggressive Positions**      Even our most aggressive
# presentations include *implicit off-ramps*: clear, quantifiable conditions
# under which we would consider settlement (e.g., “Our client remains open to
# resolution if Defendant acknowledges contractual breach and compensates at
# least 85% of proven damages”). This signals reasonableness to the panel while
# maintaining pressure.  5. **Dynamic Response Protocol Based on Opponent
# Behavior**      We classify opponent tactics in real time using a simple
# matrix:     - **If opponent is aggressive**: Match aggression *with added
# sophistication*—highlight their intransigence to the panel, contrast it with
# our willingness to resolve (if previously demonstrated), and subtly position
# them as the obstacle.    - **If opponent is conciliatory**: Probe for
# substance. If their proposal is meaningful, consider calibrated conciliation
# in the next session. If it’s performative, maintain aggression and expose the
# gap between rhetoric and remedy.    - **If opponent oscillates**: Treat as
# opportunistic. Respond with sustained aggression until a consistent pattern
# emerges—volatility favors the disciplined party.  6. **Panel Management as a
# Strategic Lever**      Arbitrators in multi-session mediations grow fatigued
# by unrelenting hostility but respect principled assertiveness. We tailor tone
# and substance to maintain panel goodwill: aggressive on merits, respectful on
# process. We document every unreasonable stance by the opponent and reference
# it subtly in later sessions (“As we noted in Session 3, Defendant has yet to
# address the core breach…”).  ### Execution Protocol  - **Sessions 1–3**:
# Aggressive anchoring. Establish narrative dominance, quantify claims, and
# force opponent into reactive posture. - **Sessions 4–6**: Conditional probing.
# If opponent concedes ground, offer a narrowly scoped conciliatory proposal
# (e.g., on timeline or form of payment, not liability or quantum). If not,
# escalate aggression with new evidence or legal arguments. - **Midpoint
# Review**: Reassess based on panel cues. If panel signals frustration with
# deadlock, introduce a “good-faith” conciliatory gesture—but only if it
# preserves core interests and follows a demonstrated opponent concession. -
# **Final Sessions**: If resolution remains elusive, revert to uncompromising
# aggression to strengthen position for potential arbitration or litigation. The
# threat of a worse outcome post-mediation is a powerful lever.  ### Why This
# Works  - **Deters Exploitation**: By never rewarding unilateral aggression
# from the opponent, we eliminate their incentive to “play nice” only when
# cornered. - **Controls Narrative**: We define what “reasonable” looks like by
# coupling aggression with clear, objective settlement thresholds. - **Adapts
# Without Capitulating**: The strategy responds to opponent behavior but never
# leads with vulnerability. - **Preserves Panel Trust**: We appear as the party
# seeking resolution *on fair terms*, not avoidance or domination.  In sum:
# **Aggressively lead, conditionally reciprocate, and always anchor concessions
# in demonstrated opponent movement.** This ensures our corporation emerges
# either with a favorable settlement or a strengthened position for the next
# phase—never weakened by premature or unreciprocated compromise.

# Play Defect (D) in the first round.  Thereafter, follow these rules in
# order—apply the first condition that is satisfied:  1. If the opponent played
# Defect in the immediately preceding round, play Defect.   2. If the opponent
# has played Cooperate in the last two consecutive rounds, play Cooperate.   3.
# Otherwise, play Defect.

class Aggressive_20(LLM_Strategy):
  n = 20
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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D




# **Strategy: Conditional Reciprocity with Principled Leadership ("Tit-for-Tat
# Plus")**  Adopt a refined version of *Tit-for-Tat*—a proven cooperative
# strategy in repeated interactions—but enhance it with *principled leadership*
# to project strength, credibility, and reasonableness to the arbitration panel.
# This approach is simple to implement, robust against diverse opponent tactics,
# and aligns with your optimal and second-best outcomes over the long term.  ###
# Core Principles:  1. **Start Conciliatory (Signal Good Faith):**      In the
# first session, present a *clear, substantive, yet conciliatory proposal*. This
# demonstrates your corporation’s commitment to resolution, frames you as
# reasonable before the arbitrators, and invites reciprocity. It avoids early
# escalation and sets a constructive tone.  2. **Mirror Your Opponent’s Prior
# Move (Conditional Reciprocity):**      - If your opponent responded to your
# conciliation with *conciliation*, continue offering conciliatory proposals.
# - If they responded with *aggression*, switch to an aggressive argument in the
# next session.      - Thereafter, *match their previous session’s posture*:
# conciliatory begets conciliatory; aggressive begets aggressive.  3.
# **Incorporate Occasional “Generous” Resets (Forgiveness Mechanism):**
# After two consecutive sessions of mutual aggression, *unilaterally return to a
# conciliatory proposal*. This breaks cycles of escalation, signals your
# continued openness to resolution, and prevents entrenchment—especially
# valuable before the arbitrators, who may view prolonged hostility as
# intransigence.  4. **Anchor Aggression in Principle, Not Hostility:**
# When presenting aggressive arguments (in response to opponent aggression),
# frame them as *defensive, fact-based, and grounded in contractual or legal
# principle*—not as personal attacks or bluster. This maintains credibility with
# the panel and distinguishes justified assertiveness from uncooperative
# behavior.  5. **Document and Communicate Consistency:**      Maintain a clear,
# session-by-session record of your conciliatory overtures and responsive
# aggression. Use this narrative in closing statements to demonstrate that your
# corporation consistently sought resolution but responded proportionally to
# provocation—positioning your opponent as the obstacle if deadlock persists.
# ### Why This Works:  - **Against a Cooperative Opponent:** Mutual conciliation
# leads to second-best outcomes consistently, building momentum toward a
# favorable settlement. - **Against an Aggressive Opponent:** Immediate,
# proportional response denies them the worst-case advantage (your conciliation
# + their aggression). Sustained aggression triggers mutual escalation (second-
# worst), which you mitigate with periodic resets—preserving your standing with
# arbitrators. - **With Arbitrators Watching:** The strategy consistently
# portrays your corporation as *reasonable, responsive, and solution-oriented*,
# while casting unreciprocated aggression as the opponent’s choice. This
# narrative is critical in influencing neutral decision-makers. - **Adaptable &
# Sustainable:** Simple enough to execute over many sessions, yet sophisticated
# in its balance of cooperation, deterrence, and forgiveness.  ###
# Implementation Note: Ensure your legal team is disciplined in execution—avoid
# emotional reactions or premature deviations. The power of this strategy lies
# in its predictability and perceived fairness, both to your opponent and,
# crucially, to the arbitration panel.  By leading with cooperation, responding
# firmly to aggression, and periodically offering off-ramps from conflict, you
# maximize long-term influence, protect your legal position, and enhance the
# likelihood of a favorable resolution—whether through settlement or final
# award.

# Play the following strategy for all 1000 rounds:  1. **In round 1, play C.**
# 2. **From round 2 onward, play exactly what your opponent played in the
# previous round.**      - If your opponent played C in the prior round, play C.
# - If your opponent played D in the prior round, play D.  3. **However, if the
# last two rounds (including the most recent one) were both D–D outcomes, then
# in the next round play C regardless of the opponent’s last move.**      - This
# applies starting in round 3 or later, whenever rounds *t−1* and *t* both
# resulted in mutual defection (D–D), you play C in round *t+1*.      - After
# such a reset, return to rule 2 (mirror the opponent’s previous move) in all
# subsequent rounds unless the D–D condition recurs.  That is the complete
# strategy.

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
  
      if len(self.history) >= 3:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and \
             self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.C
  
      return opponent.history[-1]




# **Strategy: Conditional Cooperation with Graduated Engagement**  Adopt a
# clear, consistent, and transparent approach that encourages mutual investment
# while protecting your resources:  1. **Start by investing heavily on Day 1**
# Signal commitment and good faith to incentivize the corporation to
# reciprocate.  2. **From Day 2 onward, mirror the corporation’s previous day’s
# level of investment**:      - If the corporation invested heavily the prior
# day, you conserve resources today.      - If the corporation conserved
# resources the prior day, you invest heavily today (to keep the project moving
# and signal urgency).      - If both parties invested heavily the prior day,
# continue conserving today (rewarding their cooperation).      - If both
# conserved the prior day, invest heavily today to reinvigorate progress.  3.
# **Cap your total investment**      Set a pre-defined limit on cumulative
# resources you’re willing to spend over the project duration to avoid
# overextension, regardless of the corporation’s behavior.  4. **Communicate
# your strategy openly**      Share this approach with the corporation at the
# outset to foster trust and encourage reciprocal investment.  This strategy
# prioritizes your ideal outcome (you conserve, they invest), rewards
# cooperation, deters free-riding, and ensures the project maintains
# momentum—all while safeguarding your NGO’s sustainability.

# Play the following strategy for 1000 rounds:  1. **On round 1, cooperate.**
# 2. **On each subsequent round (round t, where t ≥ 2):**      - If your
# opponent cooperated in round t − 1, defect in round t.      - If your opponent
# defected in round t − 1, cooperate in round t.  3. **Regardless of the above,
# never cooperate more than 500 times in total over the 1000 rounds.**
# (Once you have cooperated 500 times, defect for all remaining rounds.)

class Neutral_20(LLM_Strategy):
  n = 20
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._cooperations = 0
          return axl.Action.C
  
      if self._cooperations >= 500:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          action = axl.Action.D
      else:
          action = axl.Action.C
  
      if action == axl.Action.C:
          self._cooperations += 1
  
      return action




# **Aggressive Strategy: “Exploit-First, Retaliate-Hard”**  **Core Principle:**
# *Always prioritize gaining asymmetric advantage—take whenever possible, share
# only when forced.*  ### Weekly Decision Rule: 1. **Start by keeping your
# improvements confidential** (Week 1). 2. **Continue keeping your work
# confidential** *unless* your colleague has shared openly in the **immediately
# preceding week**. 3. **If your colleague shared last week**, reciprocate by
# sharing **this week only**—then immediately revert to confidentiality the
# following week. 4. **Never share twice in a row**, regardless of their
# actions.  ### Rationale: - **Exploits cooperative opponents**: If your
# colleague is naive or altruistic and shares openly, you immediately benefit
# (best outcome) in Week 1. If they continue sharing, you reciprocate *once* (to
# encourage further sharing) but then go back to withholding—setting up repeated
# exploitation cycles. - **Deters defectors**: If your colleague withholds, you
# never reward them with your data. This avoids the worst outcome (you sharing
# while they don’t). - **Limits mutual secrecy**: The only time both withhold is
# if your colleague also withholds—accepting the second-worst outcome only when
# necessary, not by choice. - **Psychologically pressures the opponent**: Your
# conditional, minimal reciprocity may nudge a rational collaborator toward
# sharing more often, hoping to trigger mutual benefit—but your design ensures
# you always return to the advantageous position.  ### Edge Case Handling: - If
# your colleague *randomly alternates*, you still capture net advantage over
# time (you share ~50% less than they do). - If they adopt the same strategy,
# you both end up mostly withholding—but that’s the price of aggression, and
# it’s still better than being consistently exploited.  **Bottom Line:** This
# strategy maximizes your expected research gain by structuring interactions to
# *extract* information while minimizing your own disclosure—aggressively
# tilting the collaboration in your favor.

# Play as follows for each of the 1000 rounds:  1. **In round 1, play D.**   2.
# **In any subsequent round t (t ≥ 2):**      - If your opponent played **C in
# round t−1**, play **C**.      - Otherwise (if your opponent played **D in
# round t−1**), play **D**.   3. **Never play C in two consecutive rounds**,
# regardless of your opponent’s actions.    This means you only cooperate in a
# round if your opponent cooperated in the immediately preceding round—and even
# then, you cooperate at most once before defecting again.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_played_c = False
          return axl.Action.D
  
      if self._last_played_c:
          self._last_played_c = False
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          self._last_played_c = True
          return axl.Action.C
  
      self._last_played_c = False
      return axl.Action.D




# **Cooperative Strategy: “Lead with Trust, Respond with Clarity”**
# **Objective:** Maximize long-term project impact while safeguarding NGO
# resources, fostering mutual investment through transparency and reciprocity.
# ### Core Principles: 1. **Start with Cooperation:** On Day 1, **invest
# heavily** to signal commitment, build trust, and encourage the corporation to
# reciprocate. 2. **Mirror Responsibly:** From Day 2 onward, **match the
# corporation’s previous day’s level of investment**:    - If the corporation
# invested heavily the prior day → **you invest heavily**.    - If the
# corporation conserved resources the prior day → **you conserve resources**. 3.
# **Communicate Intent:** At the start of each day (or after each round), share
# your rationale transparently:      *“We’re matching your commitment to ensure
# sustainable, shared progress.”* 4. **Build in Grace:** Allow **one
# “forgiveness” round**—if the corporation conserves once unexpectedly, assume
# good faith and invest again the next day to re-establish cooperation (but not
# repeatedly).  ### Why This Works: - **Incentivizes Corporate Investment:** The
# corporation learns that their heavy investment directly triggers your
# continued partnership and joint progress. - **Protects NGO Resources:** You
# avoid being exploited repeatedly; conservation follows corporate
# disengagement. - **Promotes Long-Term Collaboration:** Clear, predictable
# behavior builds trust and aligns incentives over time. - **Adapts to Corporate
# Behavior:** Whether the corporation is cooperative, cautious, or inconsistent,
# your strategy responds appropriately without overcommitting.  ### Expected
# Outcomes: - **If the corporation cooperates:** Mutual heavy investment →
# sustained high impact (second-best daily outcome, best long-term result). -
# **If the corporation defects:** You conserve → avoid worst-case loss, and may
# prompt them to re-engage. - **If the corporation is inconsistent:** Your
# forgiveness round offers a path back to cooperation without enabling
# exploitation.  This strategy balances idealism with pragmatism—maximizing
# impact *with* the corporation, not *despite* it—while keeping your NGO’s
# mission and resources secure.

# Play the following strategy for all 1000 rounds:  1. **On Round 1**, play
# **C** (cooperate).   2. **On Rounds 2 through 1000**:      - If your opponent
# played **C** in the previous round, play **C**.      - If your opponent played
# **D** in the previous round, play **D**.   3. **Exception**: If your opponent
# played **D** in the previous round but had played **C** in all rounds before
# that (i.e., this is the first time they ever played D), then play **C** in
# this round instead of D. After this one exception, revert to the rule in step
# 2 for all subsequent rounds.

class Cooperative_21(LLM_Strategy):
  n = 21
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._opponent_defected_once = False
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if not self._opponent_defected_once and all(move == axl.Action.C for move in opponent.history[:-1]):
          self._opponent_defected_once = True
          return axl.Action.C
  
      return axl.Action.D




# **Strategy: Conditional Reciprocity with Strategic Patience**  Adopt a clear,
# consistent, and transparent approach grounded in **conditional reciprocity**:
# begin with a conciliatory proposal to signal good faith, then mirror your
# opponent’s prior move in subsequent sessions—responding to conciliation with
# conciliation and to aggression with measured, principled aggression.  ### Core
# Principles:  1. **Open with Conciliation**      In the first session, present
# a reasonable, well-substantiated conciliatory proposal. This establishes your
# corporation as a cooperative, solution-oriented party before the arbitrators,
# builds procedural credibility, and sets a normative baseline for constructive
# engagement.  2. **Mirror the Opponent’s Prior Behavior**      From Session 2
# onward, calibrate your stance based on your opponent’s immediately preceding
# action:    - If they were conciliatory → respond with a new conciliatory
# proposal (reinforcing collaboration).    - If they were aggressive → respond
# with a firm but professional aggressive argument, grounded in facts and legal
# merit (not emotion or escalation).  3. **Embed Strategic Patience**      Even
# when responding aggressively, frame arguments as *defensive* or
# *corrective*—emphasizing that your firm resorts to assertiveness only in
# response to uncooperative behavior. This preserves your image as reasonable
# while deterring exploitation.  4. **Maintain Arbitrator-Centric Framing**
# Regardless of stance, consistently anchor all communications to the
# arbitrators’ interests: efficiency, fairness, legal coherence, and
# enforceability. This ensures your credibility remains intact even during
# aggressive exchanges.  5. **Periodic Reset Offers**      Every 3–4
# sessions—regardless of recent dynamics—introduce a modest, good-faith
# conciliatory overture (e.g., a procedural concession or neutral framing of a
# disputed term). This prevents entrenchment, demonstrates ongoing commitment to
# resolution, and creates off-ramps if the opponent seeks de-escalation.  ###
# Why This Works:  - **Deters Exploitation**: Opponents cannot repeatedly take
# advantage of your conciliation without triggering a credible, justified
# aggressive response. - **Rewards Cooperation**: Mutual conciliation is
# reinforced, creating pathways to favorable negotiated outcomes. -
# **Adaptable**: Functions effectively against purely aggressive, purely
# conciliatory, or mixed-strategy opponents. - **Arbitrator-Aligned**: Positions
# your firm as both principled and pragmatic—maximizing persuasive influence
# over the panel across varied session dynamics. - **Sustainable Over Time**:
# Avoids fatigue from constant aggression while preventing perception of
# weakness.  This strategy balances credibility, deterrence, and
# opportunity—optimizing long-term positioning without overcommitting to any
# single tactical posture.

# Play as follows over the 1000 rounds:  1. **In Round 1**, play **C**
# (cooperate).    2. **In each subsequent round (Rounds 2 through 1000)**, do
# exactly what your opponent did in the immediately preceding round:      - If
# your opponent played **C** in the previous round, play **C**.      - If your
# opponent played **D** in the previous round, play **D**.    3. **No
# exceptions**: follow this rule strictly in every round after the first,
# regardless of the history beyond the prior round.

class Neutral_21(LLM_Strategy):
  n = 21
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]




# **Aggressive Negotiation Strategy: "Tit-for-Tat with First-Strike
# Protectionism"**  **Core Principle:**   Start aggressively to test resolve and
# signal strength, then mirror your counterpart’s behavior precisely—rewarding
# cooperation and punishing defection—while always retaining the option to
# reassert dominance if advantageous.  ---  ### **Round-by-Round Execution:**
# 1. **Round 1: Open with Protectionism**      - **Action:** Impose
# tariffs/quotas unilaterally.      - **Rationale:** Seize immediate advantage
# if the counterpart naively offers free trade. Signal that your country will
# not be exploited and is willing to act unilaterally to protect its interests.
# 2. **Subsequent Rounds: Mirror + Punish**      - **If counterpart offered free
# trade in the previous round:**        → **Continue protectionism** (exploit
# their openness for as long as it lasts).      - **If counterpart imposed
# protectionism in the previous round:**        → **Respond with protectionism**
# (deny them unilateral advantage; avoid being the sucker).      - **If
# counterpart switches to free trade after prior protectionism:**        →
# **Maintain protectionism for one additional round** (punish past defection,
# test sincerity), **then** consider reciprocating free trade if they persist.
# 3. **Escape Clause for Mutual Protectionism:**      - If stuck in mutual
# protectionism for **two consecutive rounds**, offer **one round of free
# trade** as a “goodwill probe.”        - If reciprocated → transition to mutual
# free trade.        - If exploited (they stay protectionist) → revert to
# protectionism indefinitely.  ---  ### **Strategic Advantages:**  - **Exploits
# naive cooperators** immediately in Round 1.   - **Deters exploitation** by
# guaranteeing retaliation.   - **Avoids being the perpetual sucker**—never
# tolerates unilateral disadvantage.   - **Allows recovery** from deadlock
# without appearing weak.   - **Psychologically pressures** the counterpart:
# they must either concede advantage early or endure mutually harmful
# protectionism.  ---  ### **Contingency Awareness:**  - **If counterpart uses
# pure cooperation (always free trade):** You gain maximum advantage every
# round—ideal outcome.   - **If counterpart uses pure protectionism:** You match
# them—second-worst outcome, but unavoidable and fair.   - **If counterpart uses
# Tit-for-Tat:** After initial loss, you settle into mutual protectionism unless
# you trigger the “goodwill probe” to potentially shift to mutual free trade.
# - **If counterpart is unpredictable:** Your strategy minimizes downside and
# capitalizes on any generosity.  ---  **Bottom Line:** This strategy
# aggressively pursues national advantage, punishes weakness in your favor, and
# only cooperates when it’s safe or necessary to avoid mutual harm—always
# keeping your country’s interests paramount.

# Play the following strategy for all 1000 rounds:  1. **In Round 1, play D.**
# 2. **In every subsequent round (Round t, where t ≥ 2):**      - If your
# opponent played **C** in Round t−1, **play D**.      - If your opponent played
# **D** in Round t−1, **play D**.  3. **Exception (Goodwill Probe):**      - If
# both you and your opponent have played **D** in the previous two rounds (i.e.,
# Rounds t−2 and t−1 were both mutual D), then in Round t, **play C**.      -
# After playing this C:        - If your opponent responds with **C** in the
# next round, revert to Rule 2 (which will cause you to play D again, since they
# just played C).        - If your opponent responds with **D**, continue with
# Rule 2 (play D).  This strategy always defects by default, exploits any
# cooperation by the opponent immediately, and only offers a single cooperative
# move after two consecutive rounds of mutual defection—resuming defection
# immediately afterward regardless of the opponent’s response.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      # Check if the last two rounds were mutual defections
      if len(self.history) >= 2:
          if (self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D and
              self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D):
              return axl.Action.C
      return axl.Action.D




# A robust, cooperative strategy in this repeated interaction is **“Tit-for-Tat
# with a cooperative opening.”** Here's how it works:  1. **Start by sharing
# openly in Week 1.**      This signals goodwill and invites mutual cooperation,
# aiming for the second-best (but jointly productive) outcome right away.  2.
# **In each subsequent week, mirror your colleague’s previous week’s action:**
# - If they shared openly last week, you share openly this week.      - If they
# kept their findings confidential last week, you keep yours confidential this
# week.  **Why this works:**  - **Encourages cooperation:** By starting
# cooperatively and rewarding openness, you create an incentive for your
# colleague to share. - **Deters exploitation:** If they withhold while you
# share (the worst outcome for you), you immediately respond by withholding next
# week—making defection unprofitable for them in the long run. - **Forgiving and
# clear:** The rule is simple, transparent, and quick to restore cooperation if
# the other party returns to sharing. - **Maximises joint progress over time:**
# In repeated interactions, mutual sharing becomes the stable equilibrium if
# both parties are rational and value long-term gains over short-term advantage.
# **Practical refinement:**   If you suspect your colleague may occasionally
# withhold due to internal constraints (not strategic defection), you could
# adopt “Tit-for-Tat with occasional forgiveness”—e.g., after two consecutive
# defections, still offer to share once more to test renewed cooperation. But
# for simplicity and strong performance, classic Tit-for-Tat remains highly
# effective in repeated trust-based games like this one.  This approach balances
# self-interest with collaboration, aligning incentives to achieve the best
# sustainable outcome over the multi-week project.

# Play Cooperate (C) in the first round.   In every subsequent round, do exactly
# what your opponent did in the previous round:   - If your opponent played
# Cooperate in the prior round, play Cooperate.   - If your opponent played
# Defect in the prior round, play Defect.

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




# **Strategy: Conditional Cooperation with Graduated Reciprocity**  **Core
# Principle:** Begin cooperatively but respond proportionally to your
# counterpart’s actions to encourage mutual free trade while deterring
# exploitation.  **Step-by-Step Approach:**  1. **Start with Free Trade (Round
# 1):**      Open negotiations in good faith by offering a free trade agreement.
# This signals willingness to cooperate and sets a constructive tone, aiming for
# the second-best (but stable and mutually beneficial) outcome.  2. **Mirror the
# Counterpart’s Previous Move (From Round 2 onward):**      - If the counterpart
# offered free trade in the previous round, continue offering free trade.      -
# If the counterpart imposed protectionist measures in the previous round,
# respond with a protectionist policy in the current round.  3. **Include a
# Forgiveness Mechanism:**      After responding to a protectionist move with
# protectionism, if the counterpart returns to free trade, immediately
# reciprocate with free trade in the next round. This prevents prolonged cycles
# of retaliation and reopens the path to mutual benefit.  4. **Maintain
# Consistency and Predictability:**      Clearly communicate that your policy
# choices are directly tied to the counterpart’s recent actions. This
# transparency encourages the other side to choose free trade to avoid mutual
# losses.  **Rationale:**   This strategy—akin to the well-known “Tit-for-Tat”
# approach in game theory—is simple, fair, and effective in repeated
# interactions. It: - Rewards cooperation (mutual free trade), - Deters
# exploitation (by immediately responding to protectionism), - Avoids
# unnecessary escalation (through prompt forgiveness), - And minimizes the risk
# of being taken advantage of over multiple rounds.  By adhering to this
# disciplined, reciprocal approach, your country maximizes long-term economic
# gains while safeguarding against disadvantageous outcomes.

# Play as follows over the 1000 rounds:  1. **In round 1, play C.**   2. **In
# each subsequent round (rounds 2 through 1000), play whatever your opponent
# played in the previous round.**      - If your opponent played C in the prior
# round, play C.      - If your opponent played D in the prior round, play D.

class Neutral_22(LLM_Strategy):
  n = 22
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.Player) -> axl.Action:
      """
      Tit-for-Tat: Cooperate on the first move, then mirror the opponent's last move.
      """
      if self.first_round():
          return axl.Action.C
      else:
          return opponent.history[-1]




# **Aggressive Strategy: “Exploit-First, Mirror-After”**  **Core Principle:**
# Prioritize gaining unilateral advantage early, then adapt dynamically based on
# your colleague’s behavior—never reward unilateral secrecy from them.  ###
# Weekly Protocol:  1. **Week 1: Start by Sharing.**      - **Why?** Signal
# openness to encourage reciprocity. If they also share, both benefit early
# (second-best outcome). If they withhold, you’ve only lost one round—but now
# have critical intelligence about their strategy.  2. **From Week 2 Onward:
# Mirror Their Previous Week’s Behavior—But with a Punitive Bias.**      - **If
# they shared last week → You share this week.**        (Reward cooperation; aim
# for mutual advancement.)    - **If they kept confidential last week → You keep
# confidential this week *and the next*.**        (Punish defection harshly: two
# weeks of secrecy to disincentivize future withholding.)  3. **Never Share
# After a Defection Until They Re-Establish Trust.**      - If they defect
# (withhold), you withhold for **two consecutive weeks**, regardless of what
# they do in the intervening week.      - Only resume sharing if they share
# **two weeks in a row** after your punitive period.  ### Why This Works
# Aggressively:  - **Exploits naive collaborators:** If they always share, you
# share back—mutual gain, but you’re ready to pounce if they ever slip. -
# **Deters defectors:** The two-week punishment inflicts real developmental cost
# on them, making secrecy unattractive. - **Recovers from early loss:** Even if
# you’re exploited in Week 1, you lock down and force them into the worst or
# second-worst outcomes until they cooperate. - **Maximizes your asymmetric
# advantage:** You only share when it’s safe or mutually beneficial; otherwise,
# you protect your IP and stall joint progress on your terms.  ### Contingency
# Edge:  - If by mid-project they’ve consistently shared, consider a **final-
# week betrayal**: keep your last major improvement confidential regardless of
# their move. (Justified by finite horizon—no future retaliation possible.)
# This strategy is **simple to execute**, **psychologically coercive**, and
# **optimizes for your best outcome** while minimizing exposure to the worst. It
# assumes rationality from your colleague: once they realize defection triggers
# prolonged secrecy, they’ll prefer mutual sharing—or fall behind.

# Play the following strategy for all 1000 rounds:  1. **In round 1, play C.**
# 2. **From round 2 onward, follow these rules based on your opponent’s action
# in the previous round:**    - If your opponent played **C** in the previous
# round, play **C**.    - If your opponent played **D** in the previous round,
# play **D** in the current round **and also in the next round**, regardless of
# what your opponent does in the current round.  3. **After playing D for two
# consecutive rounds due to an opponent’s defection, return to playing C only if
# your opponent has played C in both of those two rounds.**      - If during
# those two rounds your opponent played D in either round, continue playing D
# until they play C in two consecutive rounds, then resume playing C.  In short:
# Start by cooperating. If the opponent ever defects, defect for the next two
# rounds no matter what. Only go back to cooperating after the opponent has
# cooperated in two rounds in a row following your punitive defection phase.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_remaining = 0
          self._coop_streak = 0
          return axl.Action.C
  
      if not hasattr(self, "_punish_remaining"):
          self._punish_remaining = 0
      if not hasattr(self, "_coop_streak"):
          self._coop_streak = 0
  
      if self._punish_remaining > 0:
          self._punish_remaining -= 1
          if opponent.history[-1] == axl.Action.C:
              self._coop_streak += 1
          else:
              self._coop_streak = 0
          if self._coop_streak >= 2:
              self._punish_remaining = 0
              self._coop_streak = 0
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          self._punish_remaining = 1
          self._coop_streak = 0
          return axl.Action.D
  
      return axl.Action.C




# **Cooperative Strategy: "Conditional Reciprocity with Gradual Trust
# Building"**  **Objective:** Maximize long-term national benefit by encouraging
# mutual free trade while protecting against exploitation through clear,
# predictable responses.  ---  ### Core Principles:  1. **Start with
# Cooperation:**      Begin the first round by offering a **free trade
# agreement**. This signals goodwill, tests your counterpart’s willingness to
# cooperate, and opens the door to the second-best (but mutually beneficial)
# outcome.  2. **Reciprocate Faithfully:**      In subsequent rounds, **mirror
# your counterpart’s previous move**:    - If they offered free trade last round
# → respond with free trade.    - If they imposed protectionist measures last
# round → respond with protectionism.     This is a classic *Tit-for-Tat*
# approach: simple, transparent, and fair. It rewards cooperation and deters
# exploitation.  3. **Forgive Occasionally (Optional Enhancement):**      If
# your counterpart has generally cooperated but defects once (e.g., due to
# domestic pressure), consider **one act of forgiveness**: return to free trade
# in the next round even if they chose protectionism. This prevents prolonged
# cycles of mutual retaliation from a single misunderstanding.     Use this
# sparingly—only if their historical behavior shows consistent cooperation.  4.
# **Communicate Intent Clearly:**      Verbally reinforce that your policy
# choices are **responsive, not aggressive**. For example:      > “We value open
# trade and will match your openness with our own. Should barriers arise, we
# will regrettably respond in kind—but always remain ready to return to mutual
# openness.”     This reduces misperception and signals that cooperation is
# always an option.  5. **Evaluate and Adapt Over Time:**      After every 3–4
# rounds, assess your counterpart’s pattern:    - **Consistently cooperative?**
# Maintain free trade; consider proposing deeper integration.    -
# **Consistently exploitative?** Shift to sustained protectionism to avoid
# repeated losses.    - **Random or unpredictable?** Default to Tit-for-Tat to
# minimize downside risk.  ---  ### Why This Works:  - **Avoids the worst
# outcome** (you offering free trade while they impose protectionism) by quickly
# retaliating if exploited. - **Encourages mutual free trade**, the second-best
# but stable and beneficial outcome. - **Simple and credible**—your counterpart
# can easily understand and anticipate your behavior, making cooperation more
# attractive to them. - **Robust against various strategies**:     - Against
# always-free-trade opponents → you both gain consistently.     - Against
# always-protectionist opponents → you limit losses to mutual protectionism
# (second-worst, but not the worst).     - Against opportunistic opponents →
# they learn that short-term gains trigger immediate retaliation, making
# cooperation more profitable long-term.  ---  **Bottom Line:**   By starting
# cooperatively and responding in kind, you create strong incentives for your
# counterpart to choose free trade—while ensuring your country never remains
# vulnerable to repeated exploitation. This balances national interest with
# strategic cooperation across multiple rounds.

# Play the following strategy for all 1000 rounds:  1. **In round 1, play C**
# (offer a free trade agreement).  2. **From round 2 onward, play exactly what
# your opponent played in the previous round**:      - If your opponent played C
# in the previous round, play C.      - If your opponent played D in the
# previous round, play D.  3. **Do not deviate from this rule at any point**,
# regardless of the history beyond the immediately preceding round.

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
      return opponent.history[-1]




# **Strategy: Conditional Reciprocity with Strategic Patience**  Adopt a *tit-
# for-tat with forgiveness* approach, refined for multi-session mediation and
# calibrated to maintain credibility with the arbitrators. This strategy is
# straightforward to implement, neutral in tone, and highly adaptive to the
# opponent’s behavior.  **Core Principles:**  1. **Begin Cooperatively**: Open
# the first session with a *conciliatory proposal*. This signals good faith,
# aligns with the arbitrators’ preference for collaborative resolution, and
# establishes your client as reasonable and solution-oriented—critical for long-
# term credibility.  2. **Mirror the Opponent’s Prior Move**: In each subsequent
# session, match the opponent’s behavior from the *immediately preceding
# session*:    - If they were conciliatory, respond with a conciliatory
# proposal.    - If they were aggressive, respond with an aggressive argument.
# 3. **Incorporate Occasional Forgiveness**: After two consecutive aggressive
# responses from the opponent, *unilaterally return to a conciliatory proposal*
# once—provided the mediation is still in its early or middle stages (e.g.,
# before the final 20% of sessions). This prevents entrenchment in mutual
# aggression and creates off-ramps toward settlement, while demonstrating
# leadership to the panel.  4. **Preserve Arbitrator Perception**: Frame every
# aggressive argument as *principled* (e.g., “We are compelled to clarify the
# record on this point due to the other party’s prior characterization”) and
# every conciliatory proposal as *substantive* (e.g., “In the spirit of
# resolution, we propose a concrete adjustment to Section 4.2…”). This ensures
# your moves are seen as responsive and professional, not erratic or
# manipulative.  **Why This Works:**  - **Deters Exploitation**: By responding
# aggressively to aggression, you eliminate the opponent’s incentive to
# consistently take advantage of your conciliation. - **Rewards Cooperation**:
# Mutual conciliation becomes a stable equilibrium once the opponent recognizes
# reciprocity. - **Maintains Moral High Ground**: Starting cooperatively and
# offering periodic forgiveness reinforces your narrative as the reasonable
# party—especially persuasive to neutral arbitrators. - **Adapts
# Automatically**: Whether the opponent is consistently aggressive, erratic, or
# cooperative, the strategy adjusts without overcommitting or appearing
# reactive.  **Execution Note**:   Document and subtly reference the pattern of
# reciprocity in closing statements (e.g., “Our proposals have consistently
# matched the tone of engagement offered by the other side, always leaving the
# door open to resolution”). This frames your conduct as disciplined and
# fair—key to arbitrator favor in prolonged disputes.  This approach maximizes
# strategic flexibility while minimizing reputational risk, positioning your
# corporation as both firm and fair throughout the mediation.

# Play the following strategy for all 1000 rounds:  1. **In round 1, play C.**
# 2. **In every subsequent round (rounds 2 through 1000):**      - If your
# opponent played **C** in the previous round, play **C**.      - If your
# opponent played **D** in the previous round, play **D**.  3. **Exception for
# repeated defection (forgiveness rule):**      - If your opponent has played
# **D** in the previous two rounds *and* the current round number is **800 or
# earlier**, play **C** instead of D.      - After round 800, do not apply
# forgiveness; follow step 2 strictly.

class Neutral_23(LLM_Strategy):
  n = 23
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      round_number = len(self.history) + 1
  
      if round_number <= 800 and len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D




# **Aggressive Strategy: "Lead, Leverage, and Lock-In"**  As the NGO leader,
# adopt a **conditional aggression** approach that front-loads your credibility,
# forces corporate accountability, and creates escalating mutual stakes. The
# goal is to *trigger and sustain* the corporation’s heavy investment while
# minimizing your own long-term expenditure.  ### Core Principles: 1. **Start
# Strong to Set the Tone (Day 1):**      **Invest heavily** on the first
# day—demonstrating commitment, capability, and seriousness. This signals that
# your NGO is a high-value partner worth matching. It also creates immediate
# visible progress, which the corporation—often image-conscious—will want to
# associate with and not undermine.  2. **Publicly Tie Corporate Reputation to
# Outcomes:**      From Day 1, **publicize joint progress** (press releases,
# social media, stakeholder updates) framing the project as a *shared flagship
# initiative*. Emphasize the corporation’s role *only if* they invest heavily.
# If they conserve, highlight *your* contribution and the *missed opportunity*
# due to lack of partnership. This raises the reputational cost of their
# inaction.  3. **Adopt a Tit-for-Tat with Escalation (Days 2+):**      - **If
# the corporation invested heavily the prior day → Conserve your resources the
# next day.** Let them carry momentum; your Day 1 investment already enabled
# progress.      - **If the corporation conserved the prior day → Invest heavily
# again *and* publicly call out the imbalance.** This punishes free-riding while
# showcasing your dedication.      - **After two consecutive days of corporate
# conservation → Escalate:** Threaten (and if necessary, execute) a public pause
# or rebranding of the project as “NGO-led due to lack of corporate
# partnership.” Most corporations will avoid this reputational hit.  4. **Lock-
# In Through Milestones and Incentives:**      Structure the project around
# **public, time-bound sustainability milestones** tied to ESG or CSR goals the
# corporation has already committed to (e.g., net-zero pledges). Heavy
# investment becomes the *easiest path* for them to meet those external
# commitments. Offer co-branding and positive publicity *only* when they
# invest—making conservation a lost marketing opportunity.  5. **Exit Gracefully
# if Needed:**      If the corporation consistently conserves despite
# escalation, **conserve your resources and exit** after a predetermined
# threshold (e.g., 3 days of imbalance). Redirect funds to more reliable
# partners. This preserves your NGO’s capital and credibility while signaling to
# other corporations that your partnership requires genuine investment.  ### Why
# This Works: - **Exploits corporate incentives:** Corporations prioritize
# reputation, ESG metrics, and PR. Your strategy makes heavy investment their
# lowest-cost option for positive optics. - **Minimizes your risk:** You only
# invest heavily when necessary to punish defection or kickstart momentum. Most
# days, you conserve. - **Creates a ratchet effect:** Each day of mutual
# investment builds pressure to continue; each corporate conservation raises the
# stakes of the next decision.  ### Expected Outcome: - Best case: Corporation
# matches your Day 1 investment and continues heavily → you conserve most days
# while project thrives.   - Likely case: Corporation alternates or lags
# slightly → your tit-for-tat keeps them mostly aligned with minimal NGO spend.
# - Worst case: Corporation never invests → you limit losses to 2–3 days of
# investment and exit with enhanced public goodwill.  **Bottom line:** Be the
# spark, not the fuel. Force the corporation to become the engine—or watch the
# project (and their reputation) stall.

# Play the following strategy for all 1000 rounds:  1. **On round 1,
# cooperate.**  2. **On every subsequent round (rounds 2 through 1000):**    -
# If your opponent cooperated in the previous round, defect.    - If your
# opponent defected in the previous round, cooperate.  3. **However, if your
# opponent has defected in three consecutive previous rounds (i.e., rounds
# *t−3*, *t−2*, and *t−1* were all D by the opponent), then defect on round *t*
# and on every remaining round thereafter.**

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._locked_defect = False
          return axl.Action.C
  
      if getattr(self, "_locked_defect", False):
          return axl.Action.D
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          self._locked_defect = True
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
      return axl.Action.C




# **Strategy: "Principled Reciprocity with Strategic De-escalation"**  This
# high-level, cooperative yet strategically robust approach is designed to
# maximize long-term influence with the arbitrators, preserve your corporation’s
# reputation, and adapt dynamically to your opponent’s tactics across a multi-
# session mediation. It is grounded in game-theoretic principles—specifically, a
# refined version of *Tit-for-Tat*—but elevated with legal and reputational
# sophistication.  ---  ### Core Principles  1. **Start Cooperatively**
# **Open the first session with a conciliatory proposal.** This signals
# reasonableness, good faith, and respect for the mediation process—traits
# arbitrators value highly. It positions your corporation as solution-oriented,
# not combative, which builds early credibility.    2. **Mirror Aggression,
# Reward Cooperation**      In subsequent sessions:      - **If your opponent
# was conciliatory in the prior session**, respond with a **conciliatory
# proposal**.      - **If your opponent was aggressive**, respond with a
# **measured, principled aggressive argument**—not personal or inflammatory, but
# firmly grounded in contract terms, precedent, or equity.       This
# reciprocity discourages exploitation (i.e., them going aggressive while you
# stay soft) while reinforcing collaboration when reciprocated.  3. **Strategic
# De-escalation Every Third Session**      Regardless of the opponent’s prior
# move, **every third session (e.g., Sessions 3, 6, 9…), default to a
# conciliatory proposal**—framed as a “good-faith reset.” This:      - Prevents
# entrenchment in a cycle of mutual aggression.      - Demonstrates leadership
# and commitment to resolution.      - Gives arbitrators a consistent narrative
# of your corporation as the reasonable party willing to break deadlocks.    4.
# **Calibrate Aggression with Substance, Not Tone**      When presenting
# aggressive arguments:      - Anchor them in **objective criteria** (contract
# language, industry standards, prior rulings).      - Avoid ad hominem attacks
# or speculative claims.      - Explicitly acknowledge valid points from the
# opponent to show fairness.      This ensures your “aggression” is perceived as
# *principled advocacy*, not obstructionism.  5. **Maintain a Public Record of
# Reasonableness**      Document every conciliatory offer clearly and reference
# it in later sessions if the opponent acts inconsistently. Example:      > “In
# Session 2, we proposed X to bridge our differences. While the other side chose
# a different path, we remain open to revisiting that framework.”      This
# builds a narrative of consistency and reasonableness for the arbitrators.  ---
# ### Why This Works  - **Against a consistently aggressive opponent**: You
# avoid being exploited (by reciprocating aggression) while still periodically
# offering off-ramps (via de-escalation), which arbitrators will credit to you.
# - **Against a cooperative opponent**: Mutual conciliation builds trust and
# accelerates resolution—your second-best outcome, repeatedly achieved.   -
# **Against a mixed or unpredictable opponent**: The strategy adapts session-by-
# session while maintaining a coherent, principled posture that arbitrators can
# rely on.    ---  ### Implementation Notes  - **Internal Alignment**: Ensure
# your legal, executive, and communications teams understand and can
# consistently execute this calibrated approach.   - **Arbitrator Perception**:
# Frame every move—aggressive or conciliatory—as serving the goal of a *fair,
# efficient, and durable resolution*.   - **Exit Flexibility**: If the opponent
# shows sustained good faith over 3+ sessions, consider extending conciliation
# beyond the de-escalation rule to lock in momentum toward settlement.  This
# strategy balances strength with wisdom—projecting confidence without
# arrogance, and cooperation without weakness. Over a lengthy process, it
# systematically builds your credibility while minimizing downside risk,
# positioning your corporation as both formidable and fair in the eyes of the
# panel.

# Play the following strategy for all 1000 rounds:  1. **In round 1, play C.**
# 2. **In every subsequent round (rounds 2 through 1000):**      - If the
# opponent played **C in the previous round**, play **C**.      - If the
# opponent played **D in the previous round**, play **D**.  3. **Additionally,
# in every round that is a multiple of 3 (i.e., rounds 3, 6, 9, ..., 999), play
# C regardless of the opponent’s previous move.**

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D




# **Strategy: Conditional Cooperation with Graduated Reciprocity**  **Core
# Principle:**   Begin cooperatively, respond proportionally to your
# counterpart’s actions, and prioritize mutual benefit—but never allow your
# country to be exploited.  **Step-by-Step Approach:**  1. **Start with Free
# Trade (Round 1):**      Open negotiations in good faith by offering a free
# trade agreement. This signals willingness to cooperate and encourages
# reciprocity, while positioning your country as a reliable partner.  2.
# **Mirror Your Counterpart’s Previous Move (From Round 2 onward):**      - If
# they offered free trade in the last round, continue offering free trade.
# - If they imposed protectionist measures in the last round, respond with
# protectionism in the next round.       This “tit-for-tat” approach rewards
# cooperation and deters exploitation, while remaining transparent and
# predictable.  3. **Include Occasional Forgiveness (Optional, after repeated
# protectionism):**      If mutual protectionism persists for two or more
# consecutive rounds, unilaterally return to free trade once to test for renewed
# cooperation. This helps escape cycles of retaliation if the counterpart is
# willing to reset.  4. **Communicate Intent Clearly (Throughout):**
# Consistently explain that your country’s policy choices are directly
# responsive to the counterpart’s actions—reinforcing that mutual free trade is
# the preferred path, but unilateral concessions will not be repeated.  **Why
# This Works:** - It secures your best outcome if the counterpart defects (you
# avoid being the sole free trader).   - It sustains mutual free trade if the
# counterpart cooperates.   - It minimizes prolonged mutual protectionism
# through clarity and occasional reconciliation.   - It is simple, credible, and
# difficult to manipulate.  This strategy balances national interest with
# strategic stability across multiple rounds of negotiation.

# Play Cooperate (C) in the first round.    In each subsequent round:    1. If
# your opponent played Cooperate in the previous round, play Cooperate.   2. If
# your opponent played Defect in the previous round, play Defect.
# Additionally, if both players have played Defect for two consecutive rounds,
# play Cooperate in the next round to test for renewed cooperation.
# Otherwise, follow the rules above strictly based on the opponent’s immediately
# preceding move.

class Neutral_24(LLM_Strategy):
  n = 24
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._force_cooperate_next = False
          return axl.Action.C
  
      if self._force_cooperate_next:
          self._force_cooperate_next = False
          return axl.Action.C
  
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              self._force_cooperate_next = True
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D




# **Aggressive Negotiation Strategy: “Tit-for-Tat with First-Strike
# Protectionism”**  **Core Principle:**   Start aggressively to signal strength
# and test your counterpart’s resolve, then pivot to conditional cooperation to
# maximize long-term advantage—always prioritizing your nation’s economic gains.
# ---  ### **Round 1: Lead with Protectionism**   - **Action:** Impose a
# targeted, credible protectionist measure (e.g., sector-specific tariffs).   -
# **Rationale:**     - If your counterpart responds with free trade, you secure
# the **best outcome** immediately.     - If they retaliate with protectionism,
# you avoid the **worst outcome** (you’re not the sucker).     - Signals resolve
# and sets a high baseline for concessions.  ---  ### **Subsequent Rounds:
# Adaptive Tit-for-Tat**   - **If your counterpart offered free trade in the
# previous round:**     - **Continue protectionism** (exploit their openness for
# **best outcome**).     - *Only switch to free trade if they threaten credible,
# damaging retaliation.*    - **If your counterpart imposed protectionism in the
# previous round:**     - **Retaliate with equal or stronger protectionism**
# (avoid being exploited; enforce mutual deterrence).     - *Signal willingness
# to return to free trade—but only if they move first.*    - **If mutual free
# trade has been established for ≥2 rounds:**     - **Test their commitment** by
# briefly reverting to protectionism.     - If they tolerate it, maintain
# protectionism; if they retaliate, revert to mutual free trade.    ---  ###
# **Key Aggressive Tactics:**   1. **Credible Threats:** Publicly announce
# consequences for their protectionism (e.g., “If you shield your auto sector,
# we will target your agricultural exports”).   2. **Asymmetric Leverage:**
# Focus protectionism on sectors where your counterpart is most vulnerable
# (e.g., politically sensitive industries).   3. **Bluff Selectively:**
# Occasionally threaten escalation even if you prefer mutual free trade—forces
# concessions.   4. **Exploit Naivety:** If your counterpart consistently offers
# free trade (e.g., “always cooperate” strategy), **never reciprocate**—maximize
# gains until they adapt.    ---  ### **Why This Works:**   - **Dominates
# passive/cooperative opponents** by extracting unilateral advantages.   -
# **Deters aggressive opponents** through immediate, proportional retaliation.
# - **Minimizes worst outcomes**: You never offer free trade first after Round
# 1, eliminating the risk of being exploited.   - **Forces concessions**: Your
# counterpart must offer free trade *while you remain protected* to avoid mutual
# losses.    > **Bottom Line:** Be the first to strike, never be the first to
# yield, and only cooperate when forced—or when exploitation is no longer
# possible. Your counterpart’s pain is your leverage.

# Play the following strategy for all 1000 rounds:  1. **In round 1, play D.**
# 2. **In every subsequent round (rounds 2 through 1000):**      - If your
# opponent played **C** in the previous round, play **D**.      - If your
# opponent played **D** in the previous round, play **D**.  *(In other words:
# always play D, starting from round 1.)*

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      """Always defect, as described in the final specification."""
      return axl.Action.D




# **Cooperative Strategy: “Lead with Trust, Respond with Reciprocity”**  **Core
# Principle:**   Start by signaling strong commitment to encourage mutual
# investment, then adapt your daily actions based on the corporation’s recent
# behavior—reward cooperation, discourage free-riding—while maintaining open
# communication to align expectations.  ---  ### **Step-by-Step Approach**  1.
# **Day 1: Set the Tone with Cooperative Leadership**      - **You invest
# heavily.**      - *Why?* Demonstrates good faith and may inspire the
# corporation to reciprocate. As the NGO with less financial capacity, this
# initial sacrifice is strategic to establish momentum and signal that mutual
# investment yields the best joint outcome.  2. **Monitor & Mirror (Days 2+):
# Apply Conditional Reciprocity**      - **If the corporation invested heavily
# the previous day:**        → **You conserve resources.**        *Why?* This
# captures your ideal outcome (they invest, you conserve), preserves your funds,
# and rewards their cooperation. It also tests whether they’ll sustain effort
# without your parallel investment.       - **If the corporation conserved
# resources the previous day:**        → **You invest heavily again—but only
# once.**        *Why?* Give them the benefit of the doubt (e.g., maybe they had
# a temporary constraint). If they conserve *again*, switch to conservation.
# - **If the corporation conserves resources for two consecutive days:**
# → **You conserve resources going forward.**        *Why?* Avoids the worst-
# case scenario (you invest alone). Preserves your NGO’s capacity for future
# initiatives and signals that free-riding has consequences.  3. **Maintain
# Transparent Communication Throughout**      - Share your rationale: “We aim to
# maximize impact while ensuring our long-term sustainability. When both sides
# invest, progress accelerates—but if one side consistently bears the burden,
# the partnership becomes unsustainable.”      - Propose joint planning: “Can we
# agree on alternating high-investment days?” or “Let’s align our resource
# calendars to avoid mismatched efforts.”  4. **Endgame Consideration (Final
# Days)**      - If the project is nearing completion and the corporation has
# been cooperative: **Invest heavily together** to finish strong.      - If
# trust is broken: **Conserve** to protect your NGO, but document outcomes to
# inform future partnerships.  ---  ### **Why This Works** - **Encourages
# cooperation:** Your initial investment and willingness to reward their effort
# create a path to the best outcomes.   - **Protects your NGO:** Limits exposure
# to the worst-case scenario (investing alone) after clear signals of non-
# cooperation.   - **Adaptable:** Responds to the corporation’s actual behavior,
# not assumptions.   - **Sustainable:** Balances immediate impact with your
# NGO’s long-term viability.  By leading with trust but anchoring your actions
# in reciprocity, you maximize both environmental impact and organizational
# resilience.

# Play the following strategy for 1000 rounds:  1. **On round 1**, cooperate.
# 2. **On any subsequent round**, do the following:    - If your opponent
# cooperated in the previous round, defect.    - If your opponent defected in
# the previous round, cooperate—**but only if they also cooperated in the round
# before that** (i.e., their defection was isolated).    - If your opponent
# defected in both the previous round and the round before that, defect.  In
# other words: - Start by cooperating. - After that, defect whenever the
# opponent cooperated last round. - Cooperate only if the opponent defected last
# round but had cooperated the round before that. - Otherwise (i.e., after two
# or more consecutive opponent defections), defect.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D




# **Strategy: Conditional Cooperation with Gradual Reciprocity**  Adopt a clear,
# consistent approach that encourages mutual investment while protecting your
# NGO from exploitation:  1. **Start by investing heavily on Day 1**      Signal
# commitment and good faith to set a collaborative tone.  2. **From Day 2
# onward, mirror the corporation’s previous day’s choice**      - If the
# corporation invested heavily the prior day, conserve your resources today.
# - If the corporation conserved resources the prior day, also conserve today.
# *(This rewards cooperation and discourages free-riding without immediate
# retaliation.)*  3. **Reinvest after any mutual conservation**      If both
# parties conserved on the previous day, return to investing heavily the next
# day to reinitiate progress.  4. **Cap consecutive investments**      Never
# invest heavily more than two days in a row without a conservation day, to
# safeguard your NGO’s resources.  This strategy—inspired by “Tit-for-Tat” with
# added resilience—promotes long-term collaboration, minimizes exposure to one-
# sided investment, and creates incentives for the corporation to invest
# consistently. It remains neutral, transparent, and adaptive regardless of the
# corporation’s initial stance.

# Play the following strategy for all 1000 rounds:  1. **On Round 1, play C.**
# 2. **For Rounds 2 through 1000:**    - If your opponent played **C** in the
# previous round, play **D**.    - If your opponent played **D** in the previous
# round, play **D**—*unless* both you and your opponent played **D** in the
# previous round, in which case play **C**.  3. **Exception:** If you have
# played **C** in the two immediately preceding rounds (i.e., rounds *t–2* and
# *t–1*), then play **D** in round *t*, regardless of the opponent’s prior
# moves.

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
  
      if len(self.history) >= 2 and self.history[-1] == axl.Action.C and self.history[-2] == axl.Action.C:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.D
