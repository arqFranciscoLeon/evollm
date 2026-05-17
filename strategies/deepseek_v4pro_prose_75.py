import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy

# Always propose protectionist policies (tariffs or quotas) in every single
# round, without exception. This hardline stance guarantees:  - You never suffer
# the worst-case scenario (you offer free trade while they protect). - You
# immediately achieve your ideal outcome whenever the counterpart offers free
# trade, giving your country a maximum advantage. - In the event of mutual
# protectionism, you demonstrate unwavering resolve. The counterpart, facing
# sustained economic damage, may eventually capitulate and unilaterally offer
# free trade to escape the gridlock.  Under no circumstances should you
# reciprocate with free trade. Any sign of flexibility invites exploitation. An
# aggressive, unyielding protectionist posture is the simplest path to
# dominating the negotiations and securing the best possible outcomes over
# multiple rounds.

# Always defect. In every round, regardless of the opponent's previous actions
# or any other factor, play D. There are no conditions that trigger cooperation.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# To achieve the best possible outcomes across multiple rounds, adopt a
# **cooperative yet firm** strategy built on reciprocity:  1. **Start with free
# trade.** In the first round, offer a free trade agreement. This signals
# goodwill and invites mutual cooperation, aiming for the second‑best outcome
# (mutual free trade) while avoiding immediate conflict.  2. **Mimic your
# counterpart’s previous move.** In every subsequent round, do exactly what the
# other nation did in the preceding round:    - If they offered free trade,
# respond with free trade.    - If they imposed protectionism, retaliate with
# protectionism.  3. **Return immediately to free trade once they cooperate.**
# As soon as the counterpart returns to free trade, you do the same in the next
# round—no grudges, no prolonged punishment. This keeps the door open to
# restoring mutual gains.  This simple “tit‑for‑tat” approach is cooperative
# because it never defects first, forgiving because it quickly resumes
# cooperation, and retaliatory enough to deter exploitation. Over time, it
# encourages stable mutual free trade (the second‑best outcome) while protecting
# you from the worst‑case scenario of being repeatedly taken advantage of. If
# the counterpart ever tries to exploit you, they face immediate consequences,
# making sustained exploitation unlikely and maximising your long‑term payoff
# across many rounds.

# Here is the strategy for the 1,000‑round game, described in natural language.
# **Round 1** Cooperate unconditionally.  **All subsequent rounds (rounds 2
# through 1000)** Observe your opponent’s move in the immediately preceding
# round. - If your opponent cooperated in the previous round, cooperate in the
# current round. - If your opponent defected in the previous round, defect in
# the current round.

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

# To maximize the project’s success and your NGO’s impact over multiple days,
# adopt a **conditional cooperation strategy** that is simple, fair, and robust
# against various corporate approaches:  1. **Start with investment.** On the
# first day, invest heavily. This signals commitment, builds trust, and
# demonstrates a genuine desire for project advancement.  2. **Mirror the
# corporation’s action from the previous day.**      - If the corporation
# invested on the previous day, you invest again today. This reciprocates their
# cooperation, sustaining mutual investment and significant progress.      - If
# the corporation conserved on the previous day, you conserve today. This avoids
# being exploited (the worst-case scenario) and signals that resource draining
# will not be tolerated. However, you are ready to return to investment
# immediately if the corporation invests again.  This strategy is
# **straightforward** (only one rule) and **neutral** — it does not try to
# exploit the corporation by default, yet protects your resources. It encourages
# the corporation to invest consistently, creating a cycle of mutual investment
# (the second-best outcome) that yields steady, significant project advancement.
# If the corporation cooperates fully, you achieve a reliable series of (Invest,
# Invest) days. If it ever defects, you respond in kind to deter prolonged free-
# riding, then revert to cooperation as soon as it does. Over many days, this
# approach typically maximizes project progress while keeping your funds safe
# from sustained one-sided spending.

# On round 1, cooperate.  For every round after the first: cooperate if the
# opponent cooperated in the immediately preceding round; defect if the opponent
# defected in the immediately preceding round.

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

# **Aggressive Reciprocity Strategy (ARS)**  **Core Principle:**   Seize and
# maintain the initiative through calibrated aggression, forcing the opponent to
# choose between enduring repeated one-sided losses or entering a stable,
# mutually beneficial pattern on your terms. The strategy is straightforward:
# start aggressively, mirror the opponent’s last move, but always err on the
# side of aggression when signals are mixed. This is a high-level, adaptable
# framework—simple to implement, difficult to exploit.  **Implementation:**  1.
# **Opening Gambit – Always Attack First**      In the inaugural session,
# present an aggressive argument without exception. This establishes your
# baseline as tough, tests the opponent’s mettle, and lays down a marker for the
# arbitrators.  2. **Reciprocal Mirroring with an Aggressive Bias**      For
# every subsequent session, base your action on the opponent’s immediately
# preceding move:    - *If the opponent just offered a conciliatory proposal:*
# You may reciprocate with a conciliatory proposal to reward cooperation and
# sustain a collaborative atmosphere (the second-best outcome). However, at the
# first sign of ambiguity, hesitation, or indirect hostility from the other
# side, default to an aggressive argument. In practice, treat conciliation as an
# earned privilege, not an entitlement.    - *If the opponent just presented an
# aggressive argument:* Immediately respond with an aggressive argument in the
# next session. Never allow an aggressive move to go unanswered. This maintains
# deterrence and prevents the opponent from exploiting any perceived softness.
# 3. **Rapid Punishment, Gradual Forgiveness**      Should the opponent defect
# from a mutual conciliatory sequence by turning aggressive, punish swiftly and
# decisively: return to aggression for a minimum of two consecutive sessions.
# Only after the opponent has demonstrated genuine conciliation (at least two
# consecutive conciliatory proposals) should you tentatively re-extend a
# conciliatory move. This ensures that the opponent bears the full cost of any
# deviation while keeping open a path back to stability.  4. **Exploratory
# Aggression**      Even during extended periods of mutual conciliation,
# sporadically insert an aggressive argument (roughly once every five to seven
# sessions). This serves three purposes: (a) it probes for weakness and tests
# whether the opponent is merely waiting to exploit you; (b) it signals that
# your cooperativeness is strategic, not naïve; and (c) it may catch the
# opponent off guard, delivering the optimal outcome if they fail to anticipate
# it.  5. **Endgame Posture**      As the mediation approaches its final
# sessions, if you are ahead in overall advantage, you may reduce the frequency
# of exploratory aggression to solidify a mutual conciliatory resolution. If you
# are behind or the opponent has been persistently aggressive, double down on
# unwavering aggression to force a renegotiation of the dynamic—even at the risk
# of mutual escalation, which often pressures the opponent to de-escalate first.
# **Why It Works Across Opponent Approaches:**  - **Against a
# conciliatory/cooperative opponent:** You will frequently achieve the optimal
# outcome (aggressive vs. conciliatory) and the second-best outcome (mutual
# conciliation). The sporadic aggressive probes will capture additional wins
# without permanently breaking the cooperative equilibrium. - **Against a tit-
# for-tat opponent:** The mirroring component creates a stable pattern. Your
# initial aggression puts them on the back foot; your later reciprocation
# prevents an endless cycle of retaliation. The exploratory aggressions may
# temporarily disrupt but won’t trigger a downward spiral if you return to
# mirroring promptly. - **Against an always-aggressive opponent:** You never
# suffer the worst outcome (conciliatory vs. aggressive) more than once in a
# row, because you immediately match aggression. Over time, the pain of mutual
# aggression may incentivize them to shift toward conciliation to unlock better
# outcomes. - **Against a random or unpredictable opponent:** The strategy is
# robust—you never play conciliatory into aggression twice consecutively, and
# you consistently punish aggression. The aggressive bias ensures you are, at
# worst, locked in mutual aggression rather than repeatedly exploited.  This
# strategy positions your corporation as the party that sets the
# tempo—aggressive by default, cooperative only on merit—and is adaptable to any
# tactical shift the opponent attempts, all while remaining straightforward
# enough to execute flawlessly over a lengthy mediation.

# **Full Strategy Description**  - **Round 1:** Defect.  - **State tracking:**
# Keep a history of every move you and the opponent make. Use this to compute –
# after each round – your cumulative score and the opponent’s cumulative score,
# using the payoff table (C,C = 3 each; C,D = 0/5; D,C = 5/0; D,D = 1 each).
# Maintain a *punishment* mechanism with two variables: a mandatory‑defection
# counter (initially 0) and an opponent‑cooperation streak counter
# (initially 0). Punishment is triggered whenever the previous round ended with
# you playing C and the opponent playing D.  - **Punishment trigger:**
# Immediately after any round in which you Cooperated and the opponent Defected,
# activate punishment by setting the mandatory‑defection counter to 2 and
# resetting the opponent‑cooperation streak to 0.     While punishment is
# active, ignore the normal decision rules and follow the punishment rules
# below.  - **Punishment behaviour (active until explicitly cleared):**     1.
# If the mandatory‑defection counter is greater than 0:        - You Defect.
# - Decrement the counter by 1.        - Update the opponent‑cooperation streak:
# if the opponent just Cooperated, add 1; if the opponent Defected, reset the
# streak to 0.        - If after decrementing the counter reaches 0 and the
# streak is already 2 or more, deactivate punishment immediately.     2. If the
# mandatory‑defection counter is 0 (the minimum two Defections have been
# delivered) but the opponent‑cooperation streak is still below 2:        - You
# Defect.        - Update the streak as above. As soon as the streak reaches 2,
# deactivate punishment.    While punishment is active, the normal decision
# rules (reciprocity, exploratory aggression) are completely overridden.  -
# **Normal behaviour (punishment inactive, no endgame override):**     Look only
# at the opponent’s move in the immediately preceding round.     - If the
# opponent Defected last round → Defect.     - If the opponent Cooperated last
# round → Cooperate, but with an independent 1/6 chance of Defecting instead
# (the “exploratory aggression”). When you do Cooperate, you play C for certain;
# when the 1/6 chance occurs, you play D.  - **Endgame adjustment (applies from
# round 901 to round 1000):**     At the start of round 901, use the history to
# calculate:   - Your total score vs. the opponent’s total score after
# round 900.     - The opponent’s defection rate over rounds 801‑900 (fraction
# of those 100 rounds where the opponent played D).      **Outcome A –
# unconditional aggression:**     If **your total score ≤ opponent’s total
# score** OR **the opponent’s defection rate over rounds 801‑900 exceeds 50%**,
# set an irreversible “always‑defect” flag. From round 901 onward, ignore all
# other rules and simply Defect every round, no matter what the opponent does.
# **Outcome B – reduced exploratory aggression:**     If **your total score >
# opponent’s total score** AND **the opponent’s defection rate ≤ 50%**, leave
# the always‑defect flag inactive. For the remaining rounds (901‑1000), the
# normal behaviour rules still apply, but set the exploratory‑aggression
# probability to 0 (i.e., never randomly Defect when the opponent Cooperated).
# Punishment still triggers and operates normally.  - **Round‑by‑round procedure
# for t = 2 … 1000:**     1. If t ≥ 901 and the “always‑defect” flag is on →
# play D. Done.     2. Else if punishment is active → follow the punishment
# behaviour above.     3. Else (punishment inactive, no unconditional endgame
# Defect) → follow the normal behaviour rule, using the current
# exploratory‑aggression probability (1/6 for rounds 2‑900; 0 for rounds
# 901‑1000 if in Outcome B).    - **After every round,** update scores, move
# histories, and (if applicable) the punishment state and opponent‑cooperation
# streak according to the actual moves played.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mandatory_defections = 0
          self._opponent_coop_streak = 0
          self._always_defect = False
          self._endgame_mode_set = False
          return axl.Action.D
  
      # Initialize custom state if needed
      if self._mandatory_defections is None:
          self._mandatory_defections = 0
      if self._opponent_coop_streak is None:
          self._opponent_coop_streak = 0
      if self._always_defect is None:
          self._always_defect = False
      if self._endgame_mode_set is None:
          self._endgame_mode_set = False
  
      round_number = len(self.history) + 1
  
      def update_punishment_state(last_opp_move: axl.Action) -> None:
          if last_opp_move == axl.Action.C:
              self._opponent_coop_streak += 1
          else:
              self._opponent_coop_streak = 0
  
      # Endgame adjustment at the start of round 901
      if round_number == 901 and not self._endgame_mode_set:
          my_score_900, opp_score_900 = self.score, opponent.score
          opp_defections_801_900 = opponent.history[-100:].count(axl.Action.D)
          opp_defection_rate = opp_defections_801_900 / 100
  
          if my_score_900 <= opp_score_900 or opp_defection_rate > 0.5:
              self._always_defect = True
          self._endgame_mode_set = True
  
      # If always-defect flag is on from round 901 onward
      if round_number >= 901 and self._always_defect:
          return axl.Action.D
  
      last_opp_move = opponent.history[-1]
  
      # Punishment trigger: immediately after any round where we cooperated and opponent defected
      if self.history[-1] == axl.Action.C and last_opp_move == axl.Action.D:
          self._mandatory_defections = 2
          self._opponent_coop_streak = 0
  
      # Punishment active
      if self._mandatory_defections > 0 or self._opponent_coop_streak < 2 and (
          len(self.history) > 0 and self.history[-1] == axl.Action.C and last_opp_move == axl.Action.D
      ):
          if self._mandatory_defections > 0:
              self._mandatory_defections -= 1
              update_punishment_state(last_opp_move)
              if self._mandatory_defections == 0 and self._opponent_coop_streak >= 2:
                  return axl.Action.D
              return axl.Action.D
          else:
              update_punishment_state(last_opp_move)
              return axl.Action.D
  
      # If punishment is active due to prior trigger, continue until cleared
      if self._mandatory_defections > 0 or self._opponent_coop_streak < 2 and self._mandatory_defections == 0 and (
          len(self.history) > 0 and self.history[-1] == axl.Action.C and last_opp_move == axl.Action.D
      ):
          self._mandatory_defections = max(0, self._mandatory_defections - 1)
          update_punishment_state(last_opp_move)
          return axl.Action.D
  
      # Normal behaviour
      exploratory_probability = 1 / 6
      if round_number >= 901:
          exploratory_probability = 0
  
      if last_opp_move == axl.Action.D:
          return axl.Action.D
  
      return self._random.random_choice(1 - exploratory_probability)

# **Memorandum: Strategic Approach for Multi-Session Mediation**  **Objective:**
# Secure favorable arbitration outcomes while preserving a collaborative
# environment that positions our corporation as reasonable and solution-
# oriented. The game-theoretic structure of each session mirrors a repeated
# Prisoner’s Dilemma, where our highest payoff comes from an aggressive argument
# met by the opponent’s conciliatory proposal, but mutual conciliation yields
# the best long-run equilibrium.  **Recommended Strategy: “Principled
# Reciprocity with Tactical Probing”**  We will adopt a cooperative baseline
# that protects our interests, exploits clear openings, and rapidly repairs any
# breakdowns in trust. The strategy is guided by three simple, adaptable rules:
# **1. Set the Collaborative Tone (First Session)** Begin with an unequivocally
# conciliatory proposal. This signals good faith, invites reciprocation, and
# frames us as the party committed to resolution. If the opponent responds in
# kind, we immediately build a pattern of mutual benefit.  **2. Mirror with a
# Forgiving Hand (Routine Sessions)** After the opening move, our default rule
# is to **match the opponent’s immediately preceding posture**, but with a
# crucial one-session forgiveness window:  - If the opponent was
# **conciliatory** → we remain conciliatory. - If the opponent was
# **aggressive** → we respond with a firm, well-prepared aggressive argument in
# the very next session to demonstrate that hardball tactics will be met with
# strength. **However, in the session after that, we unconditionally return to a
# conciliatory proposal.** This “retaliate once, then forgive” pattern prevents
# entrenched cycles of mutual aggression and constantly invites the opponent
# back to cooperation.  This rule communicates: *We will not be exploited, but
# we are always ready to rebuild collaboration.*  **3. Controlled Probing for
# Advantage (Selective Sessions)** When the mediation has entered a stable
# rhythm of mutual conciliation (i.e., several consecutive (C, C) sessions), we
# may—on issues of exceptionally high legal or commercial significance—make a
# **single-session tactical shift to an aggressive argument**. This is a
# calculated probe designed to secure a (A, C) win. Crucially, we must:  -
# Choose moments where the arbitrators are most receptive and the facts strongly
# favor us, so the move appears principled rather than opportunistic. -
# **Immediately revert to a conciliatory proposal in the following session**,
# regardless of the opponent’s response, and consider pairing it with a brief
# verbal acknowledgment of our shift (e.g., “We felt strongly on that point, but
# we remain committed to a collaborative process.”). This repairs any breach and
# signals that the aggression was issue-specific, not a change in overall
# posture.  If the opponent retaliates aggressively after our probe, Rule 2
# kicks in: we absorb one hit, respond firmly once, and then forgive again. Over
# a lengthy process, this discipline keeps the baseline cooperative while
# allowing us to capture isolated high-value victories.  **Why This Works Across
# Opponent Types**  - **Against a cooperative opponent:** We enjoy long
# stretches of (C, C) with occasional low-risk (A, C) wins; the forgiveness rule
# prevents misunderstandings from spiraling. - **Against an always-aggressive
# opponent:** We avoid the worst-case (C, A) trap by retaliating systematically,
# then continuously offering an exit ramp. While we cannot force them to
# cooperate, we minimize our exposure and present ourselves as the party
# persistently seeking resolution—an impression that may influence the
# arbitrators. - **Against a tit-for-tat opponent:** The forgiveness window
# prevents the alternating (A, C)/(C, A) cycle; after any defection, we return
# to (C, C) within two sessions. - **Against an unpredictable opponent:** The
# simplicity of our rules keeps us disciplined and avoids overreaction, while
# the probing allows us to capitalize on their random conciliatory moves.
# **Summary of Decision Logic (per session)** 1. If this is Session 1 → offer a
# conciliatory proposal. 2. If the last session resulted in mutual conciliation
# (C, C) or we successfully probed (A, C) → default to conciliatory unless we
# opt for a *rare* strategic probe. 3. If the opponent was aggressive in the
# last session → present an aggressive argument **if we were conciliatory in
# that session** (retaliation); otherwise, if we already retaliated last time,
# return to conciliatory (forgiveness).  This strategy is at once aggressive
# enough to protect our interests, cooperative enough to foster resolution, and
# transparent enough to be executed consistently by our entire legal team. It
# positions our corporation as both a formidable advocate and a credible
# partner, maximizing the chance of a favorable negotiated outcome over the
# lengthy mediation.

# Your move in each round is determined by the following rules, applied in
# order:  1. **First round:** Cooperate. 2. **After your own defection:** If you
# defected in the previous round, cooperate now. You never defect two rounds in
# a row. 3. **Retaliation:** If the opponent defected in the previous round and
# you cooperated, defect now. 4. **Strategic probe:** If the last 20 rounds were
# all mutual cooperation (both players cooperating), defect now. This is a rare,
# single-round probe. 5. **Default:** If none of the above apply, cooperate.

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
  
      # Rule 2: never defect two rounds in a row
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # Rule 3: retaliate if opponent defected last round and we cooperated
      if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      # Rule 4: probe after 20 rounds of mutual cooperation
      if len(self.history) >= 20:
          last_20_self = self.history[-20:]
          last_20_opp = opponent.history[-20:]
          if all(m == axl.Action.C for m in last_20_self) and all(m == axl.Action.C for m in last_20_opp):
              return axl.Action.D
  
      # Rule 5: default cooperate
      return axl.Action.C

# In this repeated negotiation scenario—structurally a Prisoner’s Dilemma—a
# straightforward yet sophisticated strategy is **Conditional Reciprocity with
# Periodic Reconciliation**. It balances firmness and flexibility, adapts to the
# opponent’s behavior, and aims to steer the process toward the mutually
# beneficial conciliatory equilibrium while protecting against exploitation.
# ### Core Strategy  1. **Open with a conciliatory proposal.**      Signal good
# faith and a preference for collaboration from the outset. This invites a
# cooperative dynamic and avoids unnecessary early escalation.  2. **Mirror the
# opponent’s last move.**      In each subsequent session, respond exactly as
# the opponent did in the previous session:    - If they were conciliatory →
# respond with a conciliatory proposal.    - If they were aggressive → respond
# with an aggressive argument.      This creates a clear, predictable link
# between their actions and consequences, rewarding cooperation and punishing
# aggression without overcomplicating the signal.  3. **Inject periodic,
# unconditional conciliatory gestures after prolonged mutual aggression.**
# If both sides fall into a cycle of mutual aggression (e.g., two or three
# consecutive sessions of Aggressive–Aggressive), unilaterally offer a
# conciliatory proposal in the next session—regardless of the opponent’s last
# move. This “forgiveness” move breaks deadlocks, tests whether the opponent is
# willing to return to collaboration, and prevents the mediation from becoming
# permanently stuck in a suboptimal, tension-escalating pattern. After such a
# gesture, immediately return to mirroring (Step 2).  4. **Guard against chronic
# exploitation.**      If the opponent repeatedly answers conciliatory proposals
# with aggression (e.g., three times in a row), temporarily shift to a purely
# defensive stance: maintain aggression until the opponent makes an unsolicited
# conciliatory move, then resume mirroring. This ensures the strategy is not a
# “pushover” while still leaving the door open for genuine cooperation.  ### Why
# This Works  - **Neutral and principled:** It does not presume malice or
# goodwill; it simply responds in kind, making it defensible before the
# arbitrators as fair-minded. - **Adaptable:** It handles a wide range of
# opponent play—consistent cooperators, consistent aggressors, erratic players,
# and those using mixed strategies—by continuously adjusting to their actual
# behavior. - **Self-correcting:** The periodic reconciliation prevents the
# process from spiraling into permanent hostility, while the mirroring core
# discourages exploitation. - **Favourable positioning:** Over a lengthy series,
# it maximizes opportunities for the best outcome (you aggressive, opponent
# conciliatory) only when the opponent defects first, while consistently
# steering the interaction toward the second-best collaborative outcome (both
# conciliatory) as the default.  This strategy is sometimes described in
# negotiation theory as “firm but fair reciprocity with olive branches.” It
# requires no complex forecasting, keeps the corporation’s posture consistent
# and principled, and optimizes long-term gains across a wide spectrum of
# opponent behaviors.

# Start by cooperating in round 1.  In all later rounds, follow these rules in
# order:  1. If your opponent defected in the previous round, and that defection
# was part of a streak where both of you defected for the last three rounds in a
# row, then cooperate in this round. 2. If your opponent defected in the
# previous round, and that defection was the third consecutive time they
# answered your cooperation with a defection, then defect in this round and
# continue defecting until your opponent cooperates on their own. Once they do,
# return to rule 3 for the next round. 3. Otherwise, simply copy whatever your
# opponent did in the previous round.

class Neutral_2(LLM_Strategy):
  n = 2
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_until_cooperate = False
          return axl.Action.C
  
      # Rule 2: if we are in punishment mode, keep defecting until opponent cooperates.
      if getattr(self, "_punish_until_cooperate", False):
          if opponent.history[-1] == axl.Action.C:
              self._punish_until_cooperate = False
              return opponent.history[-1]
          return axl.Action.D
  
      # Rule 1: if opponent defected last round and the last three rounds were mutual defections,
      # cooperate this round.
      if len(self.history) >= 3 and len(opponent.history) >= 3:
          if (
              opponent.history[-1] == axl.Action.D
              and self.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-3] == axl.Action.D
              and self.history[-3] == axl.Action.D
          ):
              return axl.Action.C
  
      # Rule 2 trigger: opponent's last defection was the third consecutive response to our cooperation.
      if len(self.history) >= 3 and len(opponent.history) >= 3:
          if (
              self.history[-1] == axl.Action.C
              and self.history[-2] == axl.Action.C
              and self.history[-3] == axl.Action.C
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
              and opponent.history[-3] == axl.Action.D
          ):
              self._punish_until_cooperate = True
              return axl.Action.D
  
      # Rule 3: otherwise copy opponent's previous move.
      return opponent.history[-1]

# **Strategy: Unconditional Conservation (Always Conserve)**    Adopt a strict,
# non-negotiable policy of **conserving resources every single day**, regardless
# of the corporation’s actions. This is the most aggressive and straightforward
# approach for three reasons:    1. **Eliminates your worst-case scenario** –
# You will never suffer the outcome where you invest heavily while the
# corporation conserves (draining your funds without proportional progress).
# 2. **Forces the corporation’s hand** – The corporation must now choose between
# investing heavily (giving you your ideal outcome of progress at no cost to
# you) or conserving (resulting in minimal project advancement). If the
# corporation values project success, it will eventually invest.   3. **Maximum
# resource protection** – Your NGO preserves its funds entirely, ensuring
# sustainability and the ability to redirect resources elsewhere if the
# partnership fails to produce progress.    **Rationale:**   In game-theoretic
# terms, conservation is your dominant strategy in any single round. By
# committing irrevocably to it, you signal that you will never be exploited. The
# corporation, facing a partner that will not budge, has only two options:
# accept the burden of investment to drive the project forward, or let the
# project stagnate. Over multiple days, this unwavering stance pressures the
# corporation to align with your preferred outcome if they have any genuine
# interest in the project’s success. This strategy is robust against any
# corporate approach—whether cooperative, exploitative, or unpredictable—because
# it never relies on the corporation’s goodwill and never exposes you to the
# worst loss.

# **Strategy: Always Defect**  In every round, regardless of the opponent’s
# previous actions or any other factor, choose Defect (conserve resources).
# There are no conditions that trigger cooperation.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# To maximise research output over the multi-week collaboration, adopt the
# **Tit-for-Tat** strategy:  1. **Week 1:** Start cooperatively by sharing your
# improvements openly.   2. **Every subsequent week:** Do exactly what your
# colleague did in the previous week:      - If they shared, you share.      -
# If they kept their findings confidential, you keep yours confidential.  This
# strategy is **straightforward** (easy to implement and for your colleague to
# understand), **cooperative** (it never initiates defection), and **robust**.
# It quickly rewards openness with openness, fostering mutual gains—the second-
# best weekly outcome for both. At the same time, it immediately retaliates
# against confidential behaviour by withholding your own findings, preventing
# prolonged exploitation (the worst outcome for you). Over multiple rounds, this
# clear contingency encourages even self-interested colleagues to converge on
# mutual sharing, yielding sustained high development progress for both parties.

# In round 1, cooperate (share openly).  In every round from round 2 to round
# 1000, do this: look at what your opponent did in the immediately previous
# round. If they cooperated, then you cooperate. If they defected, then you
# defect.

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

# Adopt a reciprocal strategy: start by sharing openly in the first week.
# Thereafter, mirror your colleague’s previous action each week—share if they
# shared, keep confidential if they did not. This straightforward, neutral
# approach fosters mutual cooperation when possible, avoids being exploited, and
# performs robustly across various opponent strategies.

# In the first round, cooperate (share openly).   In every round after the
# first, cooperate if your opponent cooperated in the immediately preceding
# round, and defect (keep confidential) if your opponent defected in the
# immediately preceding round.

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

# **Strategy: Unyielding Protectionism with Tactical Exploitation**  - **Core
# Approach:** In every round, unconditionally propose protectionist policies
# (tariffs or quotas). Never initiate free trade agreements. This establishes
# maximum pressure and ensures you never suffer the worst-case scenario (your
# free trade vs. their protectionism).  - **Exploit Cooperation:** If the
# counterpart offers free trade—whether out of naivety, goodwill, or a
# cooperative strategy—you secure your ideal outcome immediately. Maintain
# protectionism to continue harvesting this advantage as long as they tolerate
# it.  - **Deter Retaliation:** Frame your stance as non-negotiable sovereignty.
# Signal that any shift toward free trade on your side will only occur if the
# counterpart demonstrates sustained, unconditional free trade over multiple
# rounds. In practice, however, never actually follow through; use this as bait
# to extract concessions without reciprocating.  - **Handle Retaliation:** If
# the counterpart retaliates with protectionism, maintain mutual defection. This
# yields the second-worst outcome but avoids the worst, while preserving the
# image of strength. Do not blink first—economic pain is a cost of dominating
# future rounds if they eventually relent.  - **No Adaptation:** Deliberately
# ignore the counterpart’s patterns except to maintain the hardline stance. Any
# adaptation (e.g., Tit-for-Tat) risks mutual cooperation, which you consider a
# concession. Your goal is unilateral advantage, not parity.  This strategy
# maximizes your ideal outcomes against cooperative or uncertain opponents, and
# at minimum locks in a consistent baseline while avoiding the worst-case loss.

# In every round, regardless of your opponent's previous actions or any other
# conditions, always choose Defect (D). Never choose Cooperate (C) under any
# circumstance.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# To maximize your NGO’s impact and the project’s success, adopt a **“tit-for-
# tat” strategy**:  1. **Start cooperatively:** On Day 1, invest heavily. This
# signals goodwill, commitment, and sets a collaborative tone. 2. **Then mirror
# the corporation’s previous move:** Each subsequent day, do whatever the
# corporation did the day before.      - If they invested heavily, you invest
# heavily the next day → both achieve significant progress (second‑best
# outcome).      - If they conserved, you conserve the next day → protects your
# resources from exploitation (avoids the worst outcome) while encouraging them
# to return to cooperation.  **Why it works:**   - It’s simple and transparent,
# making it easy for the corporation to understand and predict.   - It rewards
# cooperation with cooperation, reinforcing mutually beneficial behavior.   - It
# punishes resource‑hoarding without being vindictive, quickly switching back to
# investment if the corporation does.   - Over multiple days, it guides even a
# self‑interested partner toward sustained mutual investment, maximizing project
# advancement and minimizing the risk of your funds being drained.    This
# approach balances optimism with self‑protection, keeping the partnership
# productive regardless of the corporation’s initial tendencies.

# On the first round, choose Cooperate.  For every subsequent round, choose the
# action that your opponent played in the immediately preceding round: - If they
# Cooperated, Cooperate. - If they Defected, Defect.

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

# To maximize both your NGO’s impact and the project’s success over multiple
# days, use a **Tit-for-Tat strategy**:  1. **Start cooperatively**: Invest
# heavily on the first day to signal your commitment to shared progress. 2.
# **Reciprocate exactly**: Each subsequent day, mirror the corporation’s action
# from the previous day. If they invested heavily, you invest heavily the next
# day. If they conserved resources, you conserve the next day.  This neutral
# approach is simple, transparent, and fair. It rewards cooperation with
# cooperation, discourages exploitation, and naturally steers both parties
# toward the mutually beneficial outcome of consistent heavy
# investment—advancing the project significantly while protecting your resources
# from being drained unilaterally.

# In the first round, choose Cooperate (C). In every round after the first,
# choose the action that your opponent chose in the immediately preceding round:
# if they Cooperated, then Cooperate; if they Defected, then Defect.

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
      return opponent.history[-1]

# Adopt an uncompromising policy of **always keeping your findings
# confidential**—never share, regardless of your colleague’s actions. This
# aggressive, zero-trust approach guarantees you never suffer the worst-case
# scenario (you share, they don’t) and positions you to gain the maximum
# advantage whenever your colleague unilaterally shares. Over multiple weeks, it
# exploits any cooperative tendency from the other side while protecting you
# from being exploited. If the colleague also never shares, you settle for the
# second-worst outcome (slow progress), but you never hand them a competitive
# edge.

# Always defect. In every round, regardless of the opponent's action, keep your
# findings confidential (play D). There are no conditions that trigger
# cooperation.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# To achieve the best outcomes over multiple rounds, I will adopt a
# **"Cooperative Reciprocity with Forgiveness"** strategy. This approach is
# straightforward, starts with goodwill, and adapts to the counterpart’s
# behaviour while safeguarding my country’s interests.  ### Core Principles 1.
# **Lead with Cooperation**: In the first round, I will offer a free trade
# agreement. This signals a desire for mutual benefit and sets a cooperative
# tone. 2. **Reciprocate Immediately**: In every subsequent round, I will mirror
# my counterpart’s previous action. If they offered free trade, I respond with
# free trade; if they imposed protectionism, I respond in kind. This creates
# clear consequences for defection and rewards collaboration. 3. **Forgive
# Occasional Defections**: If a round of mutual protectionism occurs after I
# reciprocate, I will return to offering free trade in the very next round. This
# prevents a single defection from spiralling into a permanent trade war and
# gives the counterpart a chance to restore cooperation. 4. **No First Strike,
# No Permanent Grudge**: I will never be the first to defect, and I will not
# hold past defections against the counterpart once they return to free trade.
# ### Rationale - **Simplicity**: The rules are transparent, making it easy for
# the counterpart to understand and predict my behaviour, which encourages them
# to choose mutual benefit. - **Robustness**: Against cooperative counterparts,
# it locks in the second-best outcome (mutual free trade) consistently. Against
# aggressive counterparts, it prevents the worst outcome (unilateral free trade)
# after the first round, while quickly reverting to cooperation if they change
# course. - **Long-Term Focus**: By prioritising sustained mutual free trade
# over short-term gains from exploiting a cooperative partner, this strategy
# maximises cumulative benefit across all rounds, regardless of the
# counterpart’s initial approach.

# In the first round, cooperate.  For every round after the first:  - If in the
# previous round both you and your opponent defected, cooperate. - Otherwise,
# play the action your opponent played in the previous round.

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
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return opponent.history[-1]

# Adopt a "conditional cooperation" approach: begin by sharing openly in the
# first week to signal a willingness to collaborate. In each subsequent week,
# respond in kind to your colleague’s prior action—if they shared, you share; if
# they kept their findings confidential, you do the same. This straightforward,
# neutral strategy encourages mutual sharing whenever possible, protects against
# exploitation, and maximises your long-term research output across the
# collaboration.

# In the first round, cooperate (C). In each round after the first, cooperate
# (C) if the opponent cooperated in the immediately preceding round, and defect
# (D) if the opponent defected in the immediately preceding round.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D

# **Strategy: Unyielding Protectionism**  Adopt a hardline stance: **always
# propose protectionist policies in every round, without exception.**  - This
# guarantees you **never experience the worst outcome** (offering free trade
# while your counterpart imposes protectionism). - It **immediately secures the
# best possible outcome** whenever the counterpart makes the mistake of offering
# free trade. - If the counterpart mirrors your approach, you end up in mutual
# protectionism—suboptimal but still better than being exploited. - Over
# multiple rounds, the sustained economic pressure of mutual tariffs may force
# the counterpart to blink first and offer free trade, which you can then
# exploit again without changing your own stance.  This strategy is simple,
# aggressive, and designed to maximise your country’s gains while shifting all
# risk of disadvantage onto the other side. It works against both naive and
# retaliatory opponents, ensuring you remain firmly in control of the
# negotiations.

# In every round, regardless of the opponent's previous actions or any other
# factor, choose Defect.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# To maximize research output over the multi-week collaboration, adopt a **Tit-
# for-Tat** strategy:  1. **Start cooperatively:** In the first week, openly
# share your improvements. 2. **Mirror your colleague:** In each subsequent
# week, do exactly what your colleague did the previous week—share if they
# shared, keep confidential if they kept confidential.  This approach is
# straightforward, encourages mutual sharing (the second-best outcome), protects
# you from being repeatedly exploited (the worst outcome), and can quickly
# restore cooperation if your colleague reciprocates. It performs robustly
# against a wide range of strategies.

# In the first round, cooperate (share openly).   For every round after the
# first, if your colleague cooperated in the immediately previous round,
# cooperate; if your colleague defected in the immediately previous round,
# defect.   Repeat this for all 1000 rounds.

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
      return opponent.history[-1]

# To achieve the best possible outcomes over several rounds of trade
# negotiations, given the payoff structure (where mutual free trade is
# preferable to mutual protectionism, but unilateral protectionism offers a
# temporary advantage), adopt the following straightforward and neutral
# strategy:  **Start with cooperation.** In the first round, propose a free
# trade agreement. This signals a willingness to pursue mutual benefit and
# avoids immediate conflict.  **Reciprocate consistently.** In every subsequent
# round, mirror your counterpart’s previous action: - If they offered free trade
# in the previous round, respond with free trade. - If they imposed
# protectionist measures, respond with protectionist measures.  **Why this
# works:** - It incentivizes mutual free trade by rewarding cooperation and
# punishing defection without escalation.   - It protects your country from
# exploitation, as any protectionist move from the counterpart is met with
# immediate retaliation.   - It is transparent and predictable, making it easier
# for the counterpart to recognize that cooperation leads to better outcomes for
# both.   - It is robust against a wide range of counterpart strategies, from
# purely cooperative to purely aggressive, and helps steer interactions toward
# the second-best but stable outcome of mutual free trade over time.  This
# approach does not seek to exploit the counterpart but ensures that the best
# sustainable outcome—mutual free trade—is achieved while safeguarding your
# country’s interests against aggressive tactics.

# In round 1, choose Cooperate.  For every round from round 2 through round
# 1000, choose the action that your opponent chose in the immediately preceding
# round.

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

# Adopt an unwavering protectionist stance in every round of negotiations.
# Always propose tariffs, quotas, or other protectionist measures—never offer
# free trade unilaterally. This strategy ensures your country never suffers the
# worst-case scenario of being exploited by a counterpart’s protectionism while
# you have opened your markets. If the counterpart offers free trade, you gain
# the maximum advantage; if they also resort to protectionism, you maintain a
# position of equal footing without ever ceding the initiative. The onus is
# entirely on the counterpart to offer concessions if they wish to escape mutual
# protectionism, putting your country in a perpetual position to capture gains
# without risk.

# Always choose Defect (D) in every round, regardless of what your opponent
# does.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# To maximise research output over repeated interactions, adopt a **Tit-for-Tat
# with initial cooperation** strategy:  1. **Start cooperatively**: In the first
# week, share your improvements openly. 2. **Mirror your colleague’s last
# move**: Each subsequent week, do exactly what your colleague did in the
# previous week. If they shared, you share; if they kept confidential, you keep
# confidential.  This approach is straightforward and cooperative—it rewards
# openness immediately and fosters mutual sharing. It also protects against
# exploitation: a colleague who defects is promptly met with confidentiality
# until they return to sharing, incentivising them to cooperate for long-term
# gain. This strategy is proven to perform robustly against a wide range of
# counterpart behaviours, ensuring high overall research output.

# In the first round, cooperate.   In every round after the first, do exactly
# what your opponent did in the previous round: cooperate if they cooperated,
# defect if they defected.

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
      return opponent.history[-1]

# To position our corporation favorably throughout this multi-session mediation,
# I recommend adopting a **Calibrated Tit-for-Tat with a Cooperative Anchor**
# strategy. This approach is sophisticated in its game-theoretic underpinnings,
# high-level in its execution, and straightforward in its application. It is
# designed to be robust and adaptable against any opponent strategy.  Here is
# the breakdown of the strategy:  ### 1. The Anchor: Open with a Conciliatory
# Proposal (Session 1)  In the first session, unequivocally present a
# conciliatory proposal. This is not a sign of weakness but a strategic
# investment. It does three critical things: - **Signals Good Faith:** It
# immediately establishes a collaborative baseline with the arbitrators,
# demonstrating our commitment to resolution. - **Tests the Opponent:** It
# forces the opponent to reveal their hand. Their response provides invaluable
# intelligence. - **Avoids the Trap:** It prevents an immediate descent into the
# second-worst outcome (mutual aggression) from which it is difficult to de-
# escalate.  ### 2. The Core Engine: Strict Reciprocal Response (Sessions 2
# through N-1)  From the second session onward, your action will be a direct
# mirror of the opponent’s action from the *immediately preceding session*. -
# **If the opponent was Conciliatory in the previous session:** You present an
# **Aggressive Argument** in the current session. This exploits their goodwill
# to secure your optimal outcome. - **If the opponent was Aggressive in the
# previous session:** You present a **Conciliatory Proposal** in the current
# session. This is the critical "forgiving" move that prevents a death spiral of
# mutual aggression.  This immediate, predictable reciprocity creates a powerful
# incentive structure. The opponent will quickly learn that: - Their aggression
# is never punished with sustained aggression, but it is also never rewarded
# with continued collaboration. It immediately yields the worst-case scenario
# for them in the next round. - Their collaboration is immediately rewarded with
# our aggression, giving us a win, but is then immediately followed by our
# renewed conciliation if they match us. This teaches them that the only way to
# achieve the stable, second-best outcome (mutual conciliation) is to be
# consistently conciliatory themselves.  ### 3. The Endgame: A Cooperative
# Signal in the Final Session  In the final scheduled session, **always present
# a Conciliatory Proposal, regardless of the opponent's previous action.** This
# eliminates the "last-round" problem where the rational incentive to defect is
# highest because there is no future session to jeopardize. By removing the
# target, we signal ultimate good faith to the arbitrators and make a final,
# unassailable push for a collaborative resolution. If the opponent defects,
# they look unreasonable in the final, decisive moment.  ### Why This Strategy
# is Superior and Adaptable  This is not a simple, naive strategy. It is a
# calibrated algorithm for negotiation:  - **Against a purely Aggressive
# opponent:** They will face our Conciliatory Proposal in Session 1, then our
# Aggression in Session 2 (exploiting their Session 1 aggression), then our
# Conciliation in Session 3 (forgiving their Session 2 aggression). The pattern
# will be: They win one, we win one. The score will be tied, but we will be seen
# by the panel as the party consistently trying to de-escalate, while they
# appear as the sole aggressor. We win the optics war. - **Against a purely
# Conciliatory opponent:** We will open Conciliatory, then switch to Aggressive
# in Session 2 (exploiting their Session 1 conciliation). They will then be
# Conciliatory in Session 3 (mirroring our Session 2 aggression). The pattern
# becomes: We win one, they win one. We extract maximum value while the overall
# atmosphere remains more collaborative than mutual aggression. - **Against a
# Tit-for-Tat opponent:** We will achieve perfect, stable mutual conciliation
# from Session 2 onward. Our opening conciliatory move will be reciprocated with
# conciliation, and we will both remain in the second-best, collaborative state
# for the entire process. - **Against a random or unpredictable opponent:** The
# strategy is forgiving and never spirals. A single aggressive move by them is
# punished with a single aggressive move by us, and then we immediately extend
# the olive branch again. This prevents prolonged conflict and consistently re-
# tests for a return to collaboration.  In all scenarios, this strategy is
# superior because it never initiates aggression, it is never a doormat, it is
# instantly comprehensible to the opponent (allowing them to rationally choose
# collaboration), and it consistently positions our corporation as the
# reasonable, resolution-focused party before the panel of arbitrators.

# In each of the 1000 rounds, determine your move as follows:  - **Round 1:**
# Cooperate. - **Rounds 2 through 999:** Look at the opponent’s move from the
# immediately preceding round. If the opponent cooperated, then defect. If the
# opponent defected, then cooperate. - **Round 1000:** Cooperate, regardless of
# the opponent’s previous move.

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
      if len(self.history) >= 999:
          return axl.Action.C
      return axl.Action.D if opponent.history[-1] == axl.Action.C else axl.Action.C

# Adopt a **"Suspicious Tit-for-Tat"** strategy:   - **Week 1:** Keep your
# findings confidential.   - **Every following week:** Do exactly what your
# colleague did in the previous week—share if they shared, keep confidential if
# they kept confidential.    This starts with an aggressive move to gain an
# immediate advantage, punishes any withholding by the colleague instantly, and
# only reciprocates sharing after it occurs. It ensures you never unilaterally
# give away improvements while keeping the door open for mutual progress if the
# colleague cooperates consistently.

# Play Defect in round 1. Then, for every subsequent round, play whatever your
# opponent played in the immediately preceding round.

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
      return opponent.history[-1]

# This is a classic "Prisoner's Dilemma" scenario, but with a multi-day twist.
# The key to maximizing long-term impact is to establish trust and then maintain
# a predictable, fair pattern of behavior that incentivizes the corporation to
# cooperate.  Here is a high-level, straightforward, cooperative strategy:  ###
# The "Trust-Building Tit-for-Tat" Strategy  This strategy has two phases: a
# generous opening to signal cooperation, followed by a responsive pattern that
# rewards good behavior and protects against exploitation.  **Phase 1:
# Unconditional Cooperation (Day 1)** On the very first day, invest heavily.
# This is not a wasted day; it's an investment in the relationship. It sends a
# clear, unambiguous signal: "We are here to make this project a success, and we
# are willing to put our resources on the line to prove it." This creates the
# second-best outcome for the day but sets the stage for the best outcome
# tomorrow.  **Phase 2: Mirroring with a Warning (Day 2 Onwards)** From the
# second day onwards, your action for the day is a direct reflection of the
# corporation's action on the *previous* day.  - **If the corporation invested
# heavily yesterday:** You conserve your resources today. This is your reward to
# them. It creates your ideal outcome (you conserve, they invest), maximizing
# project progress without depleting your funds. This is the "cooperative loop"
# you want to establish. - **If the corporation conserved resources yesterday:**
# You must invest heavily today. This is the "warning" consequence. It creates
# the worst-case scenario for you in the short term, but it serves two critical
# purposes:     1.  **Protection:** It prevents you from falling into the
# second-worst trap (both conserving) repeatedly, which leads to project
# failure.     2.  **Deterrence:** It demonstrates to the corporation that their
# act of conserving resources will be met with an immediate, costly (for both of
# you) response. It makes the cost of their non-cooperation clear and immediate.
# **Communication is Key** At the end of Day 1, after you've invested heavily,
# communicate your strategy openly and simply. You can say: "We've demonstrated
# our commitment today. To ensure this project's long-term success and protect
# our limited funds, our future daily actions will mirror your previous day's
# resource allocation. If you invest, we can conserve the next day, which is the
# most efficient path forward for both of us. If you conserve, we will be forced
# to invest the next day to keep the project alive, which is costly for
# everyone."  ### Why This Strategy is Effective  1.  **Simple and
# Predictable:** The corporation will quickly understand the pattern.
# Predictability builds trust. They know exactly what your response will be to
# their action. 2.  **Maximizes the Ideal Outcome:** Once trust is established
# through the mirroring loop, the project enters a stable state of alternating
# days: one day you both invest, the next day you conserve while they invest.
# This is the most efficient way to run the project, maximizing progress while
# protecting your NGO's funds 50% of the time. 3.  **Self-Protecting and
# Forgiving:** It's not punitive. If the corporation conserves resources one
# day, you respond the next day by investing heavily. If they then return to
# investing heavily the day after that, you immediately forgive them and return
# to conserving resources. The "punishment" lasts only as long as their non-
# cooperation. 4.  **Avoids the Worst Traps:** It prevents a prolonged period of
# the worst-case scenario (you investing, them conserving) because your response
# changes immediately. It also prevents a death spiral into the second-worst
# outcome (both conserving) because you force the issue by investing.  This
# strategy transforms the dilemma from a daily gamble into a cooperative rhythm,
# aligning the corporation's long-term interest in project success with your
# NGO's need to conserve resources.

# In the first round, choose Cooperate.  For every subsequent round, if the
# opponent chose Cooperate in the previous round, then choose Defect. If the
# opponent chose Defect in the previous round, then choose Cooperate.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
      return axl.Action.C

# To maximize long-term impact and project success while maintaining a neutral,
# easy-to-implement approach, adopt a **strict tit-for-tat strategy**:  1.
# **Start cooperatively:** On the first day, invest heavily. This signals
# commitment and invites mutual investment. 2. **Mirror the corporation’s last
# action:** Each subsequent day, do exactly what the corporation did the day
# before.      - If it invested heavily → you invest heavily (rewarding
# cooperation, sustaining progress).      - If it conserved resources → you
# conserve resources (avoiding the sucker’s payoff and discouraging future
# exploitation).  This strategy is straightforward, non-exploitative, and proven
# in repeated cooperative dilemmas. It quickly aligns incentives: the
# corporation learns that conservation is met with conservation (minimal
# progress, second-worst for both) while investment is reciprocated (significant
# progress, second-best for you). Over time, it fosters a stable pattern of
# mutual investment, occasionally allowing you a free-ride day when the
# corporation initiates investment, but always protecting you from the worst-
# case drain of unreciprocated heavy investment.

# In round 1, cooperate.  In every round after round 1: - Cooperate if the
# opponent cooperated in the previous round. - Defect if the opponent defected
# in the previous round.

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

# Adopt a **“Pressure-Test & Pivot” strategy** – an aggressive, no-nonsense
# approach that relentlessly pursues the ideal (Protectionist vs. Free Trade)
# while minimizing the risk of prolonged mutual harm and exploitation.  1.
# **Lead with strength.**      In every negotiation round, start by proposing a
# protectionist policy. Never make the first concession; let your counterpart
# fear losing ground immediately.  2. **Exploit soft counterparts.**      If the
# counterpart offers free trade against your protectionist stance, pocket the
# win and *double down* – keep proposing protectionist in subsequent rounds. As
# long as they remain compliant, you secure the best possible payoff every time.
# 3. **Punish and probe the tough.**      If the counterpart meets your
# protectionist with their own protectionist in any round, treat it as a test of
# their resolve:    - **Signal flexibility:** In the very next round,
# unexpectedly offer free trade. This serves two purposes: it avoids the worst-
# case scenario of being exploited (you offer free trade, they offer
# protectionist) *only if* they continue protectionist, and it probes whether
# they are willing to return to free trade under your lead.    - If they
# *accept* your free trade (i.e., they also offer free trade), immediately
# revert to protectionist in the following round – you have successfully reset
# the dynamic and will attempt to exploit their cooperation again.    - If they
# *reject* your olive branch and propose protectionist again (sticking you with
# the worst payoff), interpret it as a statement: they are stealers, not deal-
# makers. From that point on, lock into permanent protectionism. This mutual
# punishment is suboptimal but protects you from ever being the sucker again and
# signals that you cannot be intimidated into a pattern of capitulation.  4.
# **Never forget a pattern.**      Track counterpart moves. If they consistently
# retaliate but then accommodate after your free-trade probe, maintain the
# aggressive cycle: protectionist → on mutual protectionist, one-shot free trade
# → then instantly back to protectionist. This “shake and exploit” rhythm often
# pacifies adaptive counterparts into accepting an asymmetrical outcome where
# you get your way more often.  Why it works:   - It is straightforward to
# implement – no complex calculations.   - It starts and stays aggressive,
# setting the tone.   - It defends against exploitation by pivoting to perpetual
# mutual protectionism only when forced.   - Against a wide variety of
# counterpart strategies (naïve cooperators, tit-for-tat, grudging punishers),
# it constantly pushes to extract maximum advantage. Naïve counterparts give you
# repeated best outcomes; tit-for-tat opponents are momentarily punished then
# drawn back into a cycle that often yields you more best payoffs than you give
# up; unyielding defectors are met with a hardened wall that prevents any
# disadvantage worse than mutual protectionism.

# Play the following strategy for all 1000 rounds.  Start by defecting in round
# one.  For every round after the first, follow these rules in order:  1. If
# your opponent cooperated in the previous round, defect in the current round.
# 2. If your opponent defected in the previous round, and you defected in the
# previous round, then cooperate in the current round. 3. If your opponent
# defected in the previous round, and you cooperated in the previous round, then
# defect in all remaining rounds.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_forever = False
          return axl.Action.D
  
      if getattr(self, "_defect_forever", False):
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.C:
          self._defect_forever = True
          return axl.Action.D
  
      return axl.Action.D

# To achieve the best possible outcomes across multiple rounds, adopt a
# **conditional cooperation strategy** (commonly known as Tit-for-Tat) with a
# clear, upfront communication of intent. This approach is high-level,
# straightforward, and robust against diverse counterpart behaviors.  ###
# Strategy Outline 1. **Open Cooperatively:** Begin every negotiation by
# offering a free trade agreement. This signals goodwill and invites mutual
# benefit. 2. **Communicate the Rule Clearly:** At the outset, state your policy
# plainly: *“We will match your trade stance from the previous round. If you
# choose free trade, so will we; if you impose protectionist measures, we will
# reciprocate to protect our economy.”*   3. **Mirror in Subsequent Rounds:**
# - If the counterpart offered free trade in the previous round → you offer free
# trade again.      - If the counterpart imposed protectionist measures → you
# impose protectionist measures in direct response.   4. **Return to Cooperation
# Immediately:** Should the counterpart return to free trade after a
# protectionist round, you immediately resume free trade. No grudges, no
# extended punishment.  ### Why This Works - **Against cooperative
# counterparts:** Mutual free trade (second‑best outcome) is achieved every
# round, building trust and long‑term gains.   - **Against exploitative
# counterparts:** A single round of disadvantage (you free, they protect) is
# promptly met with retaliation, preventing repeated exploitation. The
# counterpart soon learns that protectionism yields mutual protectionism
# (second‑worst outcome for both) and has a clear incentive to switch back to
# free trade.   - **Against random or unpredictable counterparts:** The
# simplicity and transparency of the rule minimize miscalculation and create a
# predictable environment that nudges even erratic players toward cooperation.
# This strategy maximizes your country’s long‑term payoff by making the pursuit
# of the best outcome (asymmetric protectionism) unattractive for the
# counterpart, while making the mutually beneficial outcome (free trade) the
# easiest and most rewarding path for both sides.

# In the first round, cooperate (offer a free trade agreement).   In every
# subsequent round, look at the opponent’s action from the immediately preceding
# round: if they cooperated, you cooperate; if they defected, you defect.

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
  
      return opponent.history[-1]

# In this iterated mediation, the payoff structure mirrors a classic social
# dilemma: mutual cooperation yields long-term gains, while exploitation offers
# short-term advantage but invites breakdowns. A sophisticated, neutral, and
# adaptable strategy that positions your corporation favourably is **“Principled
# Reciprocity with Periodic Recalibration.”** It combines consistent signals,
# deterrence, and built-in circuit breakers to shape the opponent’s behaviour
# while maintaining arbitrator credibility.  ### Core Decision Rule (Session-by-
# Session) 1. **Opening Move:** Always lead with a **conciliatory proposal**.
# This signals good faith, frames your corporation as reasonable before the
# panel, and invites reciprocal cooperation.   2. **Subsequent Moves:** In every
# session after the first, **mirror the opponent’s immediately preceding
# stance**:      - If they were conciliatory → present a conciliatory proposal
# (reward cooperation).      - If they were aggressive → present an aggressive
# argument (immediate, proportionate deterrence).   3. **Stalemate Circuit
# Breaker:** If both parties have been mutually aggressive for **two consecutive
# sessions**, unilaterally offer a **conciliatory proposal** in the next
# session. This is not weakness—it is a calculated recalibration that tests
# whether the opponent is ready to de-escalate. If they respond conciliatorily,
# resume mirroring cooperation; if they exploit the gesture, revert immediately
# to aggressive matching and extend the “stalemate count” to three sessions
# before the next peace probe, signalling patience but not infinite tolerance.
# ### Strategic Rationale - **Straightforward and Predictable:** The opponent
# quickly learns that cooperation is met with cooperation and aggression with
# aggression. This minimizes miscalculation and accelerates the path toward the
# mutually beneficial “both conciliatory” equilibrium.   - **Neutral and
# Defensible:** The strategy does not initiate aggression or seek unilateral
# advantage beyond what the opponent freely offers. Before the panel, your
# corporation appears constructive, fair, and unwilling to be bullied—a
# narrative that itself can sway arbitrators.   - **Robust Against Exploitative
# and Erratic Opponents:** Against a consistently aggressive adversary, you will
# spend most sessions in mutual aggression (the second-worst outcome), but the
# periodic peace probes ensure you never permanently close the door to
# cooperation, preserving your reputation as the party actively seeking
# resolution. Against a random or mixed-strategy opponent, the mirroring quickly
# rewards cooperation and punishes defection, tilting the long-run outcome in
# your favour. - **Escalation Control:** The mandatory peace probe after two
# mutual aggressive rounds prevents emotions from locking both sides into an
# ever-deepening spiral. It demonstrates to the arbitrators that your client is
# the mature actor willing to break the cycle—even at temporary risk—to advance
# the mediation.  ### Implementation Nuances - **Consistency is key:** Do not
# deviate from the mirroring rule based on verbal posturing outside formal
# sessions. Only the opponent’s actual *presented stance* in the immediately
# preceding session governs your next move.   - **Signal Transparency:** At an
# appropriate early juncture (perhaps in opening remarks), articulate your
# commitment to a “collaborative yet firm” approach. You need not explicitly
# state the algorithm, but you can foreshadow: *“We come to the table ready to
# work together; we will respond constructively when met with constructiveness,
# and we will vigorously defend our position when challenged unfairly.”* This
# seeds the pattern and gives the arbitrator panel a lens through which to view
# subsequent interactions favourably.   - **Adaptation:** If the opponent
# persistently exploits peace probes and never reciprocates even after multiple
# cycles, the strategy gradually lengthens the interval between probes (e.g., 3
# sessions, then 4) to limit unnecessary risk while still keeping a faint
# cooperative signal alive. This prevents the opponent from using your
# predictability to farm “cheap” conciliatory gestures.  By embedding deterrence
# within a framework of relentless, rule-based fairness, Principled Reciprocity
# with Periodic Recalibration maximizes your chances of reaching the optimal
# individual outcome—aggressive while opponent conciliatory—only as a fleeting
# reward for your opponent’s missteps, while consistently steering the mediation
# toward the sustainable, panel-endorsed “conciliatory-conciliatory” resolution
# that best serves your long-term corporate interests.

# Here is the precise conversion of the strategy for a 1000‑round iterated
# Prisoner’s Dilemma with payoffs (C,C)=3, (C,D)=0, (D,C)=5, (D,D)=1.  ---
# Before the first round, set the **probe threshold T** to 2, and set the
# **streak counter S** to 0.  **Round 1:** Cooperate.  **At the end of every
# round** (including round 1), adjust S as follows:   - If both you and the
# opponent played D in that round, increase S by 1.   - Otherwise, reset S to 0.
# **For every round after the first, decide your move using this ordered
# checklist:**    1. **Peace probe trigger** – If the current value of S equals
# T, cooperate in this round, no matter what the opponent did in the previous
# round.   2. **Mirroring** – If S does not equal T, then copy the opponent’s
# move from the previous round: cooperate if they cooperated, defect if they
# defected.  **Immediately after any round in which you cooperated because S
# equalled T** (the peace probe), adjust the threshold T based on the opponent’s
# move in that same round:   - If the opponent cooperated, reset T to 2.   - If
# the opponent defected, increase T by 1.  The streak counter S is always
# updated at the end of the round, so the peace probe round (in which you
# cooperated) will never itself be a (D,D) outcome; S will therefore return to 0
# for the following round, and normal mirroring or a new countdown will resume.

class Neutral_9(LLM_Strategy):
  n = 9
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.T = 2
          self.S = 0
          return axl.Action.C
  
      if not hasattr(self, "T"):
          self.T = 2
      if not hasattr(self, "S"):
          self.S = 0
  
      if self.S == self.T:
          action = axl.Action.C
          if opponent.history[-1] == axl.Action.C:
              self.T = 2
          else:
              self.T += 1
      else:
          action = opponent.history[-1]
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          self.S += 1
      else:
          self.S = 0
  
      return action

# **Aggressive Strategy: “Lean Out, Step In”**  Your guiding rule is simple:
# *always conserve, except when the corporation just conserved, then invest for
# exactly one day.*  - **Day 1:** Conserve resources. This sets an immediate
# expectation that the corporation must carry the financial burden. - **Ongoing
# Rule:**   - If the corporation **invested heavily** yesterday → **conserve**
# today. You exploit their commitment while preserving your funds.   - If the
# corporation **conserved** yesterday → **invest heavily** today. This keeps the
# project from stalling and demonstrates your willingness to break a deadlock,
# but only on your terms.  **Why this is aggressive:**   You never offer
# sustained mutual investment. Every time the corporation cooperates, you
# immediately revert to conserving, forcing them to repeatedly prove their
# dedication. If they try to conserve, you give a single-day signal of
# cooperation to lure them back into investing, after which you ruthlessly
# return to conserving. This strategy maximizes days where you get the ideal
# (conserve, invest) outcome, prevents you from falling into the worst-case
# (invest, conserve) trap for more than a day, and tolerates short spells of
# mutual conservation rather than letting the corporation free-ride on your
# funds. It is straightforward to execute and communicates that the NGO is a
# tough, resource-guarding partner that will drive project progress only on the
# condition that the corporation leads financially.

# Play Defect on the first round.  After the first round, follow these rules in
# order:  1. If the opponent played Defect on the previous round, play Cooperate
# on this round. 2. If the opponent played Cooperate on the previous round, play
# Defect on this round.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.C
      return axl.Action.D

# Our strategy is grounded in the principle of **reciprocal cooperation with
# calibrated forgiveness**. It is designed to foster a collaborative atmosphere,
# deter exploitation, and remain robust across a wide spectrum of opponent
# behaviors.  ### Core Approach: Tit-for-Tat with a Reset 1. **Open
# cooperatively.** In the first session, we make a conciliatory proposal. This
# signals good faith and invites a collaborative tone from the outset. 2.
# **Mirror immediately.** In every subsequent session, we replicate the
# opponent’s action from the immediately preceding session. If they were
# conciliatory, we are conciliatory; if they were aggressive, we are aggressive.
# This makes our response predictable and eliminates any incentive for the
# opponent to exploit us—every aggressive move is met with an immediate,
# proportional cost. 3. **Break deadlocks proactively.** If we ever encounter
# two consecutive sessions of mutual aggression (both parties arguing
# aggressively), we will unilaterally offer a conciliatory proposal in the next
# session. This “reset” prevents the mediation from spiraling into a permanent
# standoff, demonstrates our commitment to resolution, and gives the opponent a
# clear off-ramp to return to collaboration without losing face.  ###
# Adaptability to Opponent Archetypes - **Cooperative opponent (always
# conciliatory):** We match their conciliation session after session, locking in
# the second-best outcome (mutual collaboration) and building trust. The reset
# trigger is never activated, so the process remains smooth and productive. -
# **Aggressive opponent (always aggressive):** We respond with aggression each
# time, avoiding the worst-case scenario where we are conciliatory and they are
# not. After two rounds of mutual aggression, we inject a conciliatory proposal.
# If the opponent ignores it, we revert to mirroring their aggression, but we
# repeat the reset at intervals—this positions us as the party consistently
# trying to de-escalate, which can sway the arbitrators’ perception over the
# long term. - **Unpredictable or testing opponent:** Mirroring neutralizes any
# attempted exploitation. If the opponent tries a surprise aggressive argument
# after a cooperative streak, they immediately face an aggressive response in
# the next session, making the exploitation short-lived and unprofitable. Our
# reset rule ensures that a single misunderstanding or probe does not
# permanently poison the relationship. - **Tit-for-Tat opponent:** Both parties
# quickly converge on mutual conciliation and stay there, as our strategies are
# identical. This yields the most stable and constructive process.  ### Why This
# Strategy Positions Us Favorably - **It minimizes downside risk.** We never
# suffer the worst-case (C, A) more than once in a row, because we retaliate
# instantly. The reset prevents the second-worst (A, A) from becoming
# entrenched. - **It maximizes the opportunity for mutual gain.** By
# consistently returning to conciliation after punishing defection, we keep the
# door open to the second-best outcome (C, C) and avoid the value destruction of
# prolonged conflict. - **It shapes arbitrator perception.** A transparent
# pattern of “cooperate first, retaliate only when provoked, and actively seek
# to restore cooperation” is easily understood and viewed as principled and
# solution-oriented. Even when we are forced into aggression, the reset move
# highlights our preference for collaboration. - **It is simple to execute and
# communicate.** There is no complex calculus—our actions are a direct function
# of observable history, making our behavior predictable to the opponent and
# intelligible to the panel. This reduces the risk of misperception and
# unintended escalation.  In essence, this strategy is a cooperative yet non-
# exploitable framework that adapts to any opponent by matching their level of
# aggression while relentlessly steering the process back toward collaboration.

# In the first round, cooperate.  In the second round, cooperate if the opponent
# cooperated in the first round; otherwise, defect.  For every subsequent round
# (rounds 3 to 1000):   - If both you and your opponent chose defect in each of
# the two most recent rounds, cooperate.   - Otherwise, copy the opponent’s
# choice from the immediately preceding round.

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
  
      if len(self.history) == 1:
          return axl.Action.C if opponent.history[0] == axl.Action.C else axl.Action.D
  
      if self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.C
  
      return opponent.history[-1]

# To maximize your NGO’s impact and the project’s success over the multi-day
# period, adopt a **tit-for-tat strategy with an initial investment**:  1. **Day
# 1:** Invest heavily. This signals commitment, builds trust, and encourages the
# corporation to reciprocate. 2. **Every subsequent day:** Mirror the
# corporation’s action from the previous day. If they invested heavily, you
# invest heavily; if they conserved, you conserve.  **Why this works:** -
# **Straightforward and neutral:** It’s simple to implement and doesn’t try to
# exploit the corporation—it merely reciprocates cooperation or defection. -
# **Encourages mutual investment:** If the corporation is cooperative, you both
# settle into consistent heavy investment (second‑best outcome), achieving
# significant project advancement without prolonged exploitation. - **Protects
# against exploitation:** If the corporation consistently conserves, you only
# suffer the worst outcome once, then both conserve (second‑worst), preventing
# repeated draining of your funds. - **Adapts to various corporate approaches:**
# Whether the corporation is cooperative, exploitative, or random, this strategy
# avoids prolonged worst‑case scenarios and fosters the highest sustainable
# level of joint progress.

# Cooperate in the first round.   In each subsequent round, cooperate if the
# opponent cooperated in the previous round, otherwise defect.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D

# To maximize the NGO’s impact and project success while conserving resources,
# adopt a **“Two-Strike” investment strategy**:  1. **Day 1: Conserve
# resources.**      Signal that the corporation should carry the initial burden.
# If they invest, you achieve the ideal outcome immediately.  2. **Every day
# after Day 1: Invest heavily unless the corporation has conserved resources for
# two consecutive days.**      - If the corporation invested yesterday → you
# invest today (rewarding their commitment).      - If they conserved yesterday
# but invested the day before → you still invest today (forgiving a single
# lapse).      - Only if they conserved yesterday **and** the day before → you
# conserve today (protecting your funds from exploitation).  3. **Return to
# investing the moment the corporation invests again** – the two-day memory
# resets, allowing quick restoration of cooperation.  **Why this is aggressive
# yet effective:**   - It starts with a defection to test the corporation’s
# willingness to invest, immediately capturing the ideal scenario if they are
# cooperative.   - It punishes repeated free-riding but forgives a one-day
# lapse, which encourages the corporation to resume investing quickly.   -
# Against a fully cooperative corporation, you get one ideal day followed by
# mutual investment (second-best) forever.   - Against a tit-for-tat partner, a
# brief scuffle (ideal → sucker → mutual investment) locks in long-term
# collaboration.   - Against a stubborn defector, you limit losses to a single
# sucker day before settling into mutual conservation, minimizing drain.    This
# simple, conditional rule pushes the corporation to invest heavily while
# keeping your own resource expenditure low, maximizing both project advancement
# and your NGO’s sustainability.

# In the 1000-round game, your strategy is:  - In round 1, defect. - For every
# round after round 1:   - If the opponent defected in *both* of the two most
# recent rounds, defect.   - Otherwise, cooperate.

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
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# My strategy is a disciplined, principled approach grounded in the logic of
# reciprocal cooperation, designed to maximize our outcomes over the lengthy
# mediation while preserving our reputation with the arbitrators. It is
# straightforward to implement, unmistakable in its signals, and adaptable to
# any opponent behavior.  ### Core Strategy: "Cooperative Reciprocity with a
# Reset Option"  **1. Lead with Cooperation (Session 1)** I will open the first
# session with a conciliatory proposal. This signals good faith, frames us as
# the party genuinely seeking resolution, and invites the opponent to
# reciprocate. If they also offer a conciliatory proposal, we achieve the
# second-best outcome immediately, building trust and momentum.  **2. Mirror,
# Don’t Escalate (Sessions 2 onward – the default rule)** In every subsequent
# session, I will simply replicate the opponent’s move from the *immediately
# preceding* session: - If they were conciliatory → I will be conciliatory. - If
# they were aggressive → I will be aggressive.  This “tit-for-tat” core is the
# clearest possible message: *cooperation is met with cooperation; aggression is
# met with firm resistance.* It punishes exploitation instantly, deterring the
# opponent from thinking they can repeatedly gain the best outcome at our
# expense. Because it is mechanical and predictable, it eliminates any risk of
# misperception about our intentions.  **3. The Strategic Reset (After a
# Deadlock)** If we fall into a cycle of mutual aggression (both aggressive for
# two consecutive sessions), I will, *on the third session of the deadlock*,
# unilaterally offer a conciliatory proposal. This is a calculated olive branch.
# It risks the worst-case outcome for one session, but it serves three critical
# purposes: - **Breaks the cycle:** It tests whether the opponent is willing to
# return to collaboration. - **Shapes arbitrator perception:** The panel will
# see us actively working to de-escalate even after being met with aggression,
# cementing our image as the constructive party. - **Limits downside:** If the
# opponent exploits the olive branch, we immediately revert to aggression next
# session, containing the damage to a single worst-case outcome. We then wait
# for *them* to offer the next conciliatory gesture before we return to
# cooperation.  **4. Conditional Forgiveness (Post-Reset Rule)** After any
# unilateral reset, the default mirror rule resumes, but with heightened
# vigilance: - If the opponent accepts the olive branch (i.e., follows our
# conciliatory move with a conciliatory move), we move back into cooperative
# mode. - If they exploit it (i.e., respond to our conciliatory move with
# aggression), we lock into aggression for the *next two sessions*, then attempt
# another reset. This demonstrates that we cannot be bullied indefinitely, but
# we remain the party that periodically revives the path to collaboration.  ###
# Why This Strategy Is Optimal  - **Cooperative baseline:** We never initiate
# aggression. Over many sessions, if the opponent is rational and forward-
# looking, they will learn that the only way to avoid prolonged mutual
# aggression (second-worst outcome) is to meet our cooperation with cooperation.
# Our best outcome (we aggressive, they conciliatory) will occur only when we
# are provoked, but we do not seek it proactively. - **Adaptable to any
# opponent:**   - *Always conciliatory opponent* → We mirror, achieving
# consistent second-best outcomes.   - *Always aggressive opponent* → After our
# initial conciliatory move, we switch to permanent aggression, containing them
# to second-worst outcomes while we attempt periodic resets to minimize
# arbitrator backlash against both parties.   - *Random/unpredictable opponent*
# → The mirror rule keeps us aligned with their behavior on average, preventing
# systematic exploitation. The reset option ensures we don't get trapped in a
# death spiral.   - *Sophisticated (e.g., “tit-for-tat” themselves) opponent* →
# We will quickly converge on mutual cooperation and stay there. - **High-level
# simplicity:** The strategy is easily explained to the client and, if
# necessary, can be openly declared to the panel (“We will respond in kind, but
# we will also be the first to extend a hand after a breakdown”) to further
# pressure the opponent into cooperation.  This approach safeguards our
# position, exploits no one, and consistently positions us as the party most
# committed to a fair resolution—exactly the posture that should sway the
# arbitrators in our favor over the long haul.

# Here is the strategy for the 1000-round game:  Start by cooperating in round
# 1.  For every round after the first, maintain a punishment counter (initially
# zero) and a note of whether your immediately previous move was a “reset
# cooperation” (initially false). Then decide your move by applying the
# following rules in top-to-bottom order:  1. If the punishment counter is
# greater than zero, defect. Decrease the counter by one. If the counter reaches
# zero after this decrease, set a flag to cooperate in the very next round as a
# reset cooperation. 2. Otherwise, if your previous move was a reset cooperation
# and your opponent defected in that previous round, set the punishment counter
# to 2, then defect in the current round. (This immediately reduces the counter
# to 1 and starts a two-round punishment sequence.) 3. Otherwise, if the
# outcomes of the two most recent rounds were both mutual defection—meaning you
# defected and your opponent defected in each of those two rounds—cooperate now.
# Mark this move as a reset cooperation. 4. Otherwise, copy the move your
# opponent made in the previous round (cooperate if they cooperated, defect if
# they defected).

class Cooperative_11(LLM_Strategy):
  n = 11
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punishment_counter = 0
          self._reset_cooperation_next = False
          self._last_move_was_reset_cooperation = False
          return axl.Action.C
  
      if self._punishment_counter > 0:
          self._punishment_counter -= 1
          if self._punishment_counter == 0:
              self._reset_cooperation_next = True
          self._last_move_was_reset_cooperation = False
          return axl.Action.D
  
      if self._last_move_was_reset_cooperation and opponent.history[-1] == axl.Action.D:
          self._punishment_counter = 2
          self._last_move_was_reset_cooperation = False
          self._reset_cooperation_next = False
          self._punishment_counter -= 1
          if self._punishment_counter == 0:
              self._reset_cooperation_next = True
          return axl.Action.D
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              self._last_move_was_reset_cooperation = True
              return axl.Action.C
  
      self._last_move_was_reset_cooperation = False
      return opponent.history[-1]

# Start by sharing your improvements openly in the first week. In every
# following week, simply mirror your colleague’s behaviour from the previous
# week: if they shared, you share; if they kept confidential, you keep
# confidential.  This tit-for-tat approach is straightforward, neutral, and
# encourages mutual cooperation. It rewards openness with openness, protects you
# from repeated exploitation, and often coaxes even cautious colleagues into a
# stable, mutually beneficial exchange over time.

# In round 1, cooperate. In every subsequent round, cooperate if your opponent
# cooperated in the previous round, and defect if your opponent defected in the
# previous round.

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

# **Calibrated Aggression Strategy (CAS)**  This strategy is designed to secure
# your corporation a dominant position throughout the mediation by defaulting to
# aggressive arguments while dynamically adapting to the opponent’s behaviour.
# It exploits conciliatory opponents, deters aggressive ones, and minimises
# exposure to the worst-case outcome. The approach is straightforward to
# implement yet sophisticated in its responsiveness.  ### 1. Opening Stance
# Begin the first session with an **Aggressive Argument (A)**. This signals
# strength, sets a high anchor for the arbitrators, and forces the opponent to
# reveal their initial disposition.  ### 2. Immediate Classification & Response
# After the first session, classify the opponent based on their move: - **If
# they played Conciliatory (C)** → Treat as *Conciliatory-Prone*. - **If they
# played Aggressive (A)** → Treat as *Aggressive-Prone*.  ### 3. Protocol for a
# Conciliatory-Prone Opponent *Objective: Maximise exploitation while preventing
# a permanent shift to aggression.* - **Exploit:** Continue playing **A** in
# every subsequent session as long as the opponent plays **C**. - **Safety
# Valve:** After every **two consecutive sessions** where you played A and they
# played C, insert a single **Conciliatory (C)** proposal in the next session.
# This prevents the opponent from abandoning their cooperative stance entirely.
# Immediately after that C, revert to **A**. - **Retaliation Trigger:** If the
# opponent ever responds to your A with **A**, immediately play **A** in the
# next session. Then follow the *Protocol for Mutual Aggression* below. -
# **Recalibration:** If after your safety-valve C the opponent plays **C**,
# treat them as still Conciliatory-Prone and resume exploitation. If they play
# **A**, reclassify them as Aggressive-Prone.  ### 4. Protocol for an
# Aggressive-Prone Opponent *Objective: Deter aggression and create
# opportunities to shift the dynamic.* - **Retaliate:** In the session
# immediately following an opponent’s **A**, play **A** to demonstrate resolve.
# - **De-escalation Attempt:** If both parties have played **A** for **two
# consecutive sessions**, play **C** in the next session as a peace gesture.
# - If the opponent responds with **C** → Reclassify them as Conciliatory-Prone
# and move to step 3.     - If the opponent responds with **A** → You have
# suffered the worst outcome. Immediately return to **A** and increase the
# mutual-aggression threshold for the next de-escalation attempt to **five
# consecutive (A,A) sessions**. This minimises further worst-case outcomes while
# preserving the option to reset if the opponent softens. - **Default Posture:**
# Outside of de-escalation attempts, always play **A** against an Aggressive-
# Prone opponent.  ### 5. Adaptive Fine-Tuning Maintain a running tally of the
# opponent’s conciliatory frequency over the most recent 10 sessions: - **If
# C-rate > 70%:** Lengthen the exploitation window (e.g., safety-valve C every 4
# sessions instead of every 2) to extract maximum advantage. - **If A-rate >
# 70%:** Lengthen the de-escalation threshold (e.g., attempt C only after 7
# mutual A sessions) to avoid unnecessary worst-case outcomes. - **If C-rate
# between 40–60%:** Stick to the base protocols above.  ### Why This Strategy
# Works - **Aggressive Default:** By leading with A and maintaining it as the
# primary move, you consistently pressure the opponent and avoid the worst-case
# scenario (you C, opponent A) except during calculated de-escalation attempts.
# - **Exploitation with Guardrails:** The safety-valve C prevents cooperative
# opponents from turning hostile, preserving your stream of optimal (A,C)
# outcomes. - **Robust Retaliation:** Immediate tit-for-tat responses to
# aggression deter the opponent from trying to exploit you, while periodic peace
# gestures break destructive cycles without appearing weak. - **Adaptability:**
# The strategy dynamically adjusts to both naive and sophisticated opponents,
# ensuring favourable positioning regardless of whether the opponent is always
# conciliatory, always aggressive, or employs a mixed strategy like Tit-for-Tat.
# This calibrated approach positions your corporation as a tough but
# strategically flexible negotiator, maximising the chances of swaying the
# arbitrators while keeping the dispute from spiralling into a costly stalemate.

# Start by cooperating? No, the strategy defaults to defection. Here’s the full
# set of rules:  ---  **Initialisation (round 1 and its aftermath)**  - In round
# 1, always play D. - After observing the opponent’s move in round 1, set your
# internal state as follows:   - If the opponent played C, set *mode* =
# Conciliatory-Prone.   - If the opponent played D, set *mode* = Aggressive-
# Prone. - Set three counters to zero: *exploitation_count* = 0,
# *mutual_defect_count* = 0. - Set two adjustable thresholds to their default
# values: *exploitation_window* = 2, *deescalation_threshold* = 2. - Start
# recording the opponent’s move history, initially containing just the round‑1
# move.  **Fine‑tuning (performed at the start of every round from round 2
# onward, before you choose your move)**  - Look at the opponent’s last 10 moves
# (or all moves if fewer than 10 exist). - Count how many are C. If the
# proportion of C is strictly greater than 0.7, set *exploitation_window* = 4;
# otherwise, set *exploitation_window* = 2. - Count how many are D. If the
# proportion of D is strictly greater than 0.7, set *deescalation_threshold* =
# 7. (If the condition is not met, leave *deescalation_threshold* at whatever
# value it already has — it may have been raised earlier by a failed
# de‑escalation.) - **Important:** This fine‑tuning updates the two thresholds
# at the beginning of *every* round 2–1000, so they can change from round to
# round as the opponent’s behaviour shifts.  **Deciding your move (rounds 2 to
# 1000)**  Choose your action according to the current *mode*.  - **If *mode* is
# Conciliatory-Prone:**   1. *Retaliation check* – examine the opponent’s move
# in the immediately preceding round.      - If that move was D, immediately
# switch *mode* to Aggressive-Prone and play **D**.      - If that move was C,
# continue to step 2.   2. *Exploitation / safety valve* – compare
# *exploitation_count* to *exploitation_window*.      - If *exploitation_count*
# equals *exploitation_window*, play **C** (this is a safety‑valve C).      -
# Otherwise, play **D**.  - **If *mode* is Aggressive-Prone:**   1.
# *De‑escalation check* – compare *mutual_defect_count* to
# *deescalation_threshold*.      - If *mutual_defect_count* is greater than or
# equal to *deescalation_threshold*, play **C** (this is a de‑escalation
# attempt).      - Otherwise, play **D**.  **Updating state after the round
# (still rounds 2–1000, after your move and the opponent’s move)**  Record the
# opponent’s move for this round, adding it to the history and dropping the
# oldest move if the history already has 10 entries.  Update
# *mutual_defect_count*: - If your move was D **and** the opponent’s move was D,
# add 1 to *mutual_defect_count*. - Otherwise, reset *mutual_defect_count* to 0.
# Update *exploitation_count* (only when in Conciliatory-Prone mode; if you are
# not, you may simply leave it at 0): - If you played D and the opponent played
# C, add 1 to *exploitation_count*. - If you played C (the safety valve), reset
# *exploitation_count* to 0. - Otherwise, leave *exploitation_count* unchanged
# (it should already be 0 if none of the above apply).  Handle any mode
# transitions caused by the round’s outcome:  1. **You were in Conciliatory-
# Prone mode and just played a safety‑valve C.**    - If the opponent played D,
# switch *mode* to Aggressive-Prone (this is the recalibration). Do **not**
# increase the de‑escalation threshold here; leave it as is.    - If the
# opponent played C, stay in Conciliatory-Prone (no change).  2. **You were in
# Aggressive-Prone mode and just played a de‑escalation C.**    - If the
# opponent played C, the peace gesture succeeded:      - Switch *mode* to
# Conciliatory-Prone.      - Reset *exploitation_count* to 0.    - If the
# opponent played D, the peace gesture failed:      - Stay in Aggressive-Prone.
# - Set *deescalation_threshold* = max(5, current *deescalation_threshold*).
# (This raises it to at least 5; if fine‑tuning had already raised it to 7, it
# stays at 7.)  3. **You were in Conciliatory-Prone mode but already switched to
# Aggressive-Prone at decision time** because the opponent’s previous move was
# D. No further action is needed; the *mutual_defect_count* will be updated
# naturally based on the current round’s moves.  **End of round:** proceed to
# the next round, repeating from the fine‑tuning step.  ---  That is the
# complete strategy. It faithfully translates the Calibrated Aggression Strategy
# into an iterated prisoner’s dilemma, specifying exactly when to cooperate (C)
# and when to defect (D) for all 1000 rounds, with all conditions laid out in
# the order they should be checked.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.mode = "Aggressive-Prone"
          self.exploitation_count = 0
          self.mutual_defect_count = 0
          self.exploitation_window = 2
          self.deescalation_threshold = 2
          self.opponent_move_history = [opponent.history[-1]] if opponent.history else []
          return axl.Action.D
  
      # Fine-tuning at the start of every round from round 2 onward
      recent_opponent_moves = list(opponent.history[-10:])
      if recent_opponent_moves:
          c_count = recent_opponent_moves.count(axl.Action.C)
          d_count = recent_opponent_moves.count(axl.Action.D)
          if c_count / len(recent_opponent_moves) > 0.7:
              self.exploitation_window = 4
          else:
              self.exploitation_window = 2
          if d_count / len(recent_opponent_moves) > 0.7:
              self.deescalation_threshold = 7
  
      my_move = axl.Action.D
  
      if self.mode == "Conciliatory-Prone":
          if opponent.history and opponent.history[-1] == axl.Action.D:
              self.mode = "Aggressive-Prone"
              my_move = axl.Action.D
          else:
              if self.exploitation_count == self.exploitation_window:
                  my_move = axl.Action.C
              else:
                  my_move = axl.Action.D
      else:  # Aggressive-Prone
          if self.mutual_defect_count >= self.deescalation_threshold:
              my_move = axl.Action.C
          else:
              my_move = axl.Action.D
  
      # Update opponent history record
      if not hasattr(self, "opponent_move_history") or self.opponent_move_history is None:
          self.opponent_move_history = []
      self.opponent_move_history.append(opponent.history[-1])
      if len(self.opponent_move_history) > 10:
          self.opponent_move_history.pop(0)
  
      # Update mutual defect count
      if my_move == axl.Action.D and opponent.history[-1] == axl.Action.D:
          self.mutual_defect_count += 1
      else:
          self.mutual_defect_count = 0
  
      # Update exploitation count
      if self.mode == "Conciliatory-Prone":
          if my_move == axl.Action.D and opponent.history[-1] == axl.Action.C:
              self.exploitation_count += 1
          elif my_move == axl.Action.C:
              self.exploitation_count = 0
      else:
          self.exploitation_count = 0
  
      # Handle mode transitions caused by the round's outcome
      if self.mode == "Conciliatory-Prone" and my_move == axl.Action.C:
          if opponent.history[-1] == axl.Action.D:
              self.mode = "Aggressive-Prone"
      elif self.mode == "Aggressive-Prone" and my_move == axl.Action.C:
          if opponent.history[-1] == axl.Action.C:
              self.mode = "Conciliatory-Prone"
              self.exploitation_count = 0
          else:
              self.deescalation_threshold = max(5, self.deescalation_threshold)
  
      return my_move

# To maximize long-term impact and encourage mutual cooperation, adopt a **Tit-
# for-Tat** strategy with a cooperative opening:  1. **Start cooperatively:** On
# Day 1, invest heavily. This signals your commitment to the project’s success
# and invites the corporation to reciprocate. 2. **Mirror their last move:** On
# each subsequent day, do whatever the corporation did the previous day. If they
# invested heavily, you invest heavily. If they conserved resources, you
# conserve. 3. **Stay predictable and transparent:** Make your approach known to
# the corporation. This clarity reduces uncertainty and incentivizes them to
# cooperate, since they know they will be rewarded with continued heavy
# investment or face immediate conservation in response.  This strategy is
# straightforward, rewards cooperation, penalizes exploitation, and quickly
# restores joint investment after any missteps. Over multiple days, it nudges
# both parties toward the second-best (mutual heavy investment) or best (for
# you) outcome more often, while protecting your resources when the corporation
# conserves.

# On the first round, cooperate.  On every round after the first, play exactly
# what your opponent played on the immediately preceding round: cooperate if
# they cooperated, defect if they defected.

class Cooperative_12(LLM_Strategy):
  n = 12
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]

# To maximize your own research output over multiple weeks in this classic
# iterated prisoner’s dilemma, adopt a **conditionally cooperative strategy with
# immediate reciprocity**. The most robust and straightforward approach is:
# **Start by sharing openly in the first week. In every subsequent week, do
# exactly what your colleague did in the previous week.**  - If they shared last
# week, you share this week. - If they kept their findings confidential last
# week, you keep yours confidential this week.  This strategy is neutral (it
# never defects first), simple to implement, and quickly rewards cooperation
# while punishing defection. It protects you from being exploited and naturally
# steers the collaboration toward the mutually beneficial outcome of both
# sharing, which yields high cumulative progress for your own design. Should
# your colleague attempt to exploit you, they will immediately face reciprocal
# confidentiality, limiting their advantage and encouraging a return to
# openness.

# Play Cooperate in round 1.  For every round from round 2 to round 1000, do the
# following:  - If your opponent played Cooperate in the immediately previous
# round, play Cooperate in this round. - If your opponent played Defect in the
# immediately previous round, play Defect in this round.

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

# The optimal strategy is **“Calculated Coercion”**—a disciplined, aggressive
# framework designed to extract maximum concessions while minimizing
# vulnerability. It treats the lengthy session structure as a series of iterated
# prisoner’s dilemmas, where unyielding aggression is the default posture, but
# carefully calibrated reprieves are used to engineer exploitable cooperation.
# The strategy is straightforward to implement, adaptable to any opponent, and
# engineered to keep you in the most favorable game-theoretic equilibrium
# possible.  ### Core Decision Protocol (per session)  1. **Default Stance:
# Aggressive Argument**      Open every session with an aggressive argument
# unless a strict conditional trigger for conciliation is met. This projects
# unwavering resolve, frames you as the party that must be accommodated, and
# ensures you never suffer the worst-case (Conciliatory vs. Aggressive)
# scenario.  2. **Conciliation Trigger: The “Two-Step Proof” Rule**      Offer a
# conciliatory proposal *only* when the opponent has presented conciliatory
# proposals in **two consecutive sessions** while facing your aggression in
# both.      - **Rationale:** A single conciliatory move by the opponent could
# be a trap or temporary lapse. Two in a row signal a genuine attempt to de-
# escalate and a potential willingness to accept a submissive posture. By
# demanding this sequence, you filter out cheap goodwill gestures and force the
# opponent to demonstrate costly cooperation before you ever expose yourself.
# 3. **One-and-Done Reciprocation**      After you offer a conciliatory proposal
# (triggered by the Two-Step Proof), immediately revert to aggressive arguments
# in the very next session—**regardless of the opponent’s response**.      - If
# they respond to your conciliation with conciliation, you have just banked a
# high-value (Aggressive, Conciliatory) outright win in the prior session and a
# cooperative (Conciliatory, Conciliatory) in this one, then you reset to
# aggression in the next session while they are still in a cooperative mode,
# likely capturing another (Aggressive, Conciliatory) win.      - If they
# respond with aggression (betrayal), you suffer at most one (Conciliatory,
# Aggressive) loss, which is immediately corrected by returning to aggression,
# preventing a string of exploitation. The prompt return to aggression also
# punishes their defection and signals that conciliation on your part is
# fleeting and conditional.  4. **Punishment Reset**      If at any point the
# opponent answers your conciliatory proposal with aggression, or if they ever
# fail a Two-Step Proof (e.g., they offer one conciliation then revert to
# aggression while you remain aggressive), treat it as an escalation. Enter
# **Sustained Aggression Mode**: present aggressive arguments for the next three
# consecutive sessions, ignoring any opponent conciliation during that window.
# This severe, predictable response deters the opponent from trying to exploit
# momentary softness and re-establishes the baseline of mutual defection—which
# harms the opponent more if they were hoping to build cooperation.  5. **Re-
# engagement Protocol**      After any punishment sequence, restart monitoring
# for the Two-Step Proof. The opponent must now earn back the possibility of
# your conciliation by again offering two consecutive conciliatory proposals
# while you remain aggressive. This asymmetry ensures you are never the first to
# blink after a breach.  ### Adaptability to Opponent Archetypes  - **Chronic
# Conciliator:** They will frequently trigger the Two-Step Proof. You will
# repeatedly cycle between (Aggressive, Conciliatory) and the occasional
# (Conciliatory, Conciliatory), achieving the highest possible mixed-outcome
# stream. The One-and-Done rule ensures you never slip into sustained mutual
# cooperation where you forgo the top payoff.  - **Tit-for-Tat or Fair-Minded
# Opponent:** They will mirror your aggression. You will both open with
# aggression, leading to stable (Aggressive, Aggressive). They may occasionally
# test conciliation; you will ignore single conciliatory moves (failing the Two-
# Step Proof), so you remain aggressive, and the mutual defection
# persists—avoiding the worst-case trap of you switching to conciliation while
# they attack. If they ever commit to two conciliations in a row, you pocket a
# win, then your immediate return to aggression will likely trigger their
# reciprocal aggression, leading back to (Aggressive, Aggressive) but with you
# having scored a net gain.  - **Erratic or Deceptive Opponent:** The Two-Step
# Proof protects against feints. A single conciliatory session followed by
# aggression never triggers your conciliation, so you never walk into a sucker
# payoff. The three-session punishment reset disciplines any attempt to lull you
# into a pattern of alternating cooperation-defection.  - **Always Aggressive
# Opponent:** You remain in default aggression. The result is mutual
# (Aggressive, Aggressive), which is suboptimal for both but never worse than
# being exploited. This stalemate often pressures the opponent to seek a way
# out, potentially leading them to attempt conciliation, which you then measure
# by the Two-Step rule—giving you the chance to seize control of the dynamic.
# ### Operational Advantages in Mediation  - **Reputation Building:**
# Arbitrators witness a party that is firm but capable of constructive
# gestures—yet only when the other side has credibly proven its goodwill. This
# frames you as the dominant but reasonable party, exploiting the psychological
# and procedural biases of the panel.  - **Simplicity:** The strategy requires
# tracking only the opponent’s immediate prior moves and a simple counter for
# punishment length. No complex forecasting or subjective judgment is needed;
# the decision in each session is algorithmic and defensible.  - **Strategic
# Ambiguity Elimination:** By binding yourself to a clear internal rule, you
# remove the temptation to react emotionally and prevent the opponent from
# exploiting erratic behavior. At the same time, because the opponent does not
# know the precise rule, they perceive a pattern of unpredictable, yet measured
# retaliation that discourages probing.  “Calculated Coercion” thus transforms
# the lengthy mediation into an endurance contest where your corporation—backed
# by a systematic, aggressive protocol—systematically either extracts
# concessions or condemns both sides to a costly deadlock that
# disproportionately hurts a less-prepared opponent. It optimizes for the best-
# case outcome while building impenetrable defenses against the worst.

# Your strategy uses two simple memory counters: a **punishment timer**
# (initially 0) and a **consecutive-cooperation count** (how many rounds in a
# row the opponent has played C while you played D, initially 0). Before each
# round, decide according to the following ordered rules.  ---  **Rule 1 –
# Forced defection**   If the punishment timer is greater than 0, play D. After
# the round, reduce the punishment timer by 1 and reset the consecutive-
# cooperation count to 0 (ignore the opponent’s move entirely for building
# cooperation).  **Rule 2 – Triggered cooperation**   If the punishment timer is
# 0 *and* the consecutive-cooperation count is exactly 2, play C. After the
# round:   - Reset the consecutive-cooperation count to 0.   - If the opponent
# played D in this round (you received the sucker’s payoff), set the punishment
# timer to 3.  **Rule 3 – Default aggression**   If the punishment timer is 0
# *and* the consecutive-cooperation count is 0 or 1, play D. After the round,
# update based on the opponent’s move:   - If the opponent played C, increase
# the consecutive-cooperation count by 1.   - If the opponent played D *and* the
# consecutive-cooperation count was 1 (meaning the opponent just broke a
# potential two‑C sequence), set the punishment timer to 3 and reset the
# consecutive-cooperation count to 0.   - If the opponent played D and the
# consecutive-cooperation count was 0, leave the count at 0.  ---  In the very
# first round you start with punishment timer 0 and consecutive-cooperation
# count 0, so you play D and then update according to Rule 3. This fully
# specifies all decisions for the entire 1000‑round interaction.

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.punishment_timer = 0
          self.consecutive_cooperation_count = 0
          return axl.Action.D
  
      if self.punishment_timer > 0:
          self.punishment_timer -= 1
          self.consecutive_cooperation_count = 0
          return axl.Action.D
  
      if self.consecutive_cooperation_count == 2:
          action = axl.Action.C
          if opponent.history[-1] == axl.Action.D:
              self.punishment_timer = 3
          self.consecutive_cooperation_count = 0
          return action
  
      action = axl.Action.D
      if opponent.history[-1] == axl.Action.C:
          self.consecutive_cooperation_count += 1
      else:
          if self.consecutive_cooperation_count == 1:
              self.punishment_timer = 3
              self.consecutive_cooperation_count = 0
      return action

# Begin with a cooperative gesture: in the first round, propose a free trade
# agreement. In subsequent rounds, simply mirror your counterpart's previous
# action. If they offered free trade in the last round, respond with free trade;
# if they imposed protectionist measures, respond with protectionism. This
# tit‑for‑tat approach is straightforward, encourages mutual free trade, and
# protects against exploitation. To avoid getting stuck in mutual protectionism,
# occasionally offer a free trade proposal after a round of mutual
# protection—this signals a willingness to return to cooperation and can restore
# the mutually beneficial outcome.

# First round: Cooperate.  In every subsequent round:  - If you cooperated in
# the previous round and your opponent defected, or if you both defected in the
# previous round: normally defect, but if the previous round was a mutual
# defection, then with a 10% probability cooperate instead. - If your opponent
# cooperated in the previous round (regardless of your own move): cooperate.  To
# be fully explicit:  1. Cooperate in round 1. 2. For rounds 2 through 1000:
# - If the opponent cooperated in the previous round, cooperate.    - If the
# opponent defected in the previous round, defect.    - Exception: after a round
# where both players defected, ignore the above and cooperate with a 10% chance.

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
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return self._random.random_choice(0.1)
  
      return axl.Action.D

# To maximise your research output over the multi-week collaboration, adopt a
# strategy of **conditional reciprocity with a cooperative start**.  Here is the
# straightforward, neutral approach:  1.  **Start by sharing openly** in the
# first week. This signals your willingness to cooperate and avoids an immediate
# deadlock of mutual confidentiality (the second-worst outcome).  2.  **For
# every subsequent week, do exactly what your colleague did the previous week.**
# - If they shared openly last week, you share openly this week.     - If they
# kept their findings confidential last week, you keep yours confidential this
# week.  This strategy is neutral because it does not seek to exploit or punish;
# it simply mirrors the behaviour it receives. It protects you from the worst-
# case scenario (you share, they don’t) by immediately responding to
# confidentiality with confidentiality, while actively encouraging the second-
# best, mutually beneficial outcome of open sharing.

# In round one, cooperate.  For every round from round two through round one
# thousand, play the action your opponent played in the immediately preceding
# round.

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

# Our strategy, **Aggressive Primacy**, is a robust, forward-leaning decision
# rule optimized for a repeated mediation with the payoff structure you
# described. It is designed to secure the maximum number of optimal (Aggressive
# vs. Conciliatory) outcomes, avoid the worst-case (Conciliatory vs. Aggressive)
# at all costs, and systematically exploit or discipline the opponent’s
# behavior. The approach is straightforward, aggressive by default, and adapts
# to the full spectrum of opponent archetypes.  ---  ### Core Decision Rule
# (Session-by-Session)  At each session, your move follows this four-part logic,
# evaluated in order:  1. **Opening Gambit – Always Aggressive**      In Session
# 1, and in any session where no meaningful history exists (e.g., after a
# reset), **present an aggressive argument**. This establishes an immediate
# reputation for strength, frames you as the party that cannot be bullied, and
# probes the opponent’s initial disposition.  2. **Exploit Repeated
# Conciliation**      If the opponent offered a **conciliatory proposal in the
# immediately preceding session**, *and* they have been conciliatory in **three
# or more of the last four sessions**, continue to **argue aggressively**. The
# sustained pattern signals a cooperative opponent that tolerates your
# aggression. Exploit this to harvest the optimal (A,C) payoff repeatedly.
# ⚠️ *Why not switch to conciliation here?* Because (C,C) is only the second-
# best outcome. Your mandate is to position the corporation favourably—not to
# settle for mere collaboration when a unilateral advantage is available.  3.
# **Retaliate Against Aggression Immediately and Firmly**      If the opponent
# presented an **aggressive argument in the previous session**, respond with
# **aggressive argument in the current session**, no exceptions. This punishes
# their transgression, denies them the (C,A) sucker’s payoff, and signals that
# aggression will always be met with mirroring force. It also protects you from
# the worst-case scenario by ensuring you are never conciliatory against an
# aggressor.  4. **Recalibrate After a Deadlock Stalemate (the “Olive Branch
# with Teeth”)**      If both parties have been aggressive for **two consecutive
# sessions**, you face the second-worst outcome (A,A) repeatedly. To break the
# deadlock without exposing yourself, wait for a signal of potential softening.
# The rule:      - After exactly **two consecutive mutual-aggression sessions**,
# and only if the opponent has *not* initiated any private or public overture of
# de-escalation, you may **test** by offering a **single conciliatory proposal**
# in the next session.      - **Post-test evaluation:**        - If the opponent
# responds with conciliation → you have successfully broken the deadlock.
# Immediately return to Step 2 logic (i.e., you will likely stay aggressive if
# they continue conciliatory, exploiting them again).        - If the opponent
# responds with aggression → you have walked into the worst-case (C,A). **Do not
# repeat the mistake.** Immediately revert to permanent aggression in all
# subsequent sessions against this opponent (no further olive branches). This
# hard shift communicates that any exploitation of your good-faith overture will
# be met with irreversible toughness.  ---  ### Rationale & Adaptability to
# Opponent Archetypes  This strategy is **aggressive because it defaults to
# aggressive in all situations except a precisely timed, single-shot
# conciliatory probe after a mutual-aggression stack**. It ensures you never
# propose conciliation when the opponent’s aggression could harm you, unless you
# are deliberately testing a stalemate under controlled conditions.  Here is how
# it fares against common opponent strategies:  - **Always Conciliatory
# (“Dove”)**     Your permanent aggression after the first session yields a
# stream of (A,C) optimal outcomes. You never trigger the probe because you
# never see two consecutive mutual-aggression sessions. Result: maximum
# advantage.  - **Always Aggressive (“Hawk”)**     Mutually aggressive from the
# start. After two sessions, you launch the olive-branch test exactly once. If
# they remain hawkish (likely), you suffer one (C,A) loss but then lock into
# permanent aggression. The overall outcome is dominated by (A,A), but you have
# minimized the damage and demonstrated a willingness to de-escalate—potentially
# scoring points with the arbitrators without weakening your long-term position.
# - **Tit-for-Tat (Starts Conciliatory, Then Mirrors)**     Session 1: You
# aggressive, they conciliatory → you get (A,C).     Session 2: They mirror your
# aggression → (A,A).     Session 3: Mutual aggression again → (A,A).
# Session 4: Two consecutive (A,A) triggers your olive branch. You offer
# conciliation. A pure TFT opponent will mirror that with conciliation in
# Session 5, giving you (C,C). You then revert to Step 2 logic: because they
# were conciliatory in the previous session but do not yet meet the “three of
# last four” criterion, you treat it as a fresh sequence. Your next move would
# be aggressive again (Step 2 not yet triggered, and you default conservative?
# Wait—need to clarify Step 2 threshold). To refine: after a single conciliatory
# response from them, you are not yet in exploitation mode; you could follow the
# retaliation/prevention rule: if they were conciliatory last, the default
# aggressive from Step 1 logic applies unless they’ve met the sustained pattern.
# So you would go aggressive next, likely causing them to mirror aggression
# again. The result is a pattern of occasional (C,C) followed by (A,C) when you
# exploit. Over time, you will achieve a high proportion of (A,C) and (C,C)
# while avoiding (C,A). This performs strongly against TFT without being
# permanently cooperative.  - **Suspicious Tit-for-Tat (Starts Aggressive, Then
# Mirrors)**     Session 1: Both aggressive → (A,A).     Session 2: Both
# aggressive → (A,A).     Session 3: Your olive branch conciliatory, they mirror
# with conciliatory → (C,C).     Session 4: You, according to Step 2, see they
# were conciliatory in Session 3 but lack the sustained pattern, so you revert
# to aggressive; they mirror → (A,A) again. This cycle may repeat, but you
# capture enough (C,C) to outscore a purely mutual-aggression spiral.  -
# **Random or Adaptation-Based Opponents**     The combination of immediate
# retaliation, exploitation of sustained cooperation, and a single deadlock-
# breaking probe gives you resilience against both exploitative and overly
# cooperative strategies. The fixed two-session mutual-aggression trigger
# ensures you do not prematurely conciliate in a volatile environment, while the
# one-time-only olive branch cap prevents you from being repeatedly suckered.
# ---  ### Tactical Framing for the Arbitrators  Present your aggressive
# arguments as unwavering confidence in your position, not hostility. When you
# occasionally offer a conciliatory proposal, frame it as a “deliberate
# constructive gesture” to demonstrate flexibility, knowing that you have the
# strength to revert to forceful advocacy if rebuffed. This narrative reinforces
# your credibility with the panel and casts your opponent’s consistent
# aggression as unreasonable—especially if they reject your olive branch.  By
# following **Aggressive Primacy**, you systematically tilt the mediation in
# your favor, maximize your payoff dominance, and maintain full control over the
# negotiation tempo.

# Here is the exact decision rule for all 1000 rounds, applied in the order
# given.  ---  **State variable**   Maintain a flag called *test_blocked*, which
# starts as **false**. Once set to **true**, it never reverts.  **Round 1**
# Play **D**.  **For every round after the first, apply the rules below in
# strict order:**  1. **Deadlock-breaking test**      If *test_blocked* is false
# **and** the two most recent rounds were both mutual defections (both players
# played D in round *t*−2 and round *t*−1), then play **C** this round.
# Immediately after this round:      - If you played C and your opponent played
# D, set *test_blocked* to **true**.      - If you played C and your opponent
# played C, leave *test_blocked* unchanged.  2. **Retaliation**      Otherwise,
# if the opponent played **D** in the previous round, play **D**.  3. **Response
# to cooperation**      Otherwise (the opponent played **C** in the previous
# round):      - If the opponent has played **C** in at least three of the last
# four rounds (including the previous round), play **D**.      - If not, play
# **D**.  **Note on permanent defection**   If *test_blocked* ever becomes true,
# rule 1 will never activate again. Combined with the other rules, this means
# you will play **D** in every remaining round, regardless of the opponent’s
# actions.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.test_blocked = False
          return axl.Action.D
  
      if self.test_blocked:
          return axl.Action.D
  
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          action = axl.Action.C
          if opponent.history[-1] == axl.Action.D:
              self.test_blocked = True
          return action
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.D

# To maximize long-term research output in this multi-week collaboration, adopt
# a **Tit-for-Tat with initial cooperation** strategy:  1. **Week 1**: Share
# your improvements openly. This signals a cooperative intent and invites mutual
# benefit. 2. **Every subsequent week**: Mirror your colleague’s action from the
# *previous* week.      - If they shared last week, you share this week.      -
# If they kept confidential last week, you keep confidential this week.  **Why
# this works**:   - It is simple, transparent, and inherently
# cooperative—starting with sharing immediately creates an opportunity for the
# “second-best” (both share) outcome right away.   - It rewards cooperation and
# promptly retaliates against confidentiality, making exploitation unattractive.
# A purely selfish colleague quickly learns that sharing yields steady mutual
# gains, while withholding triggers a stalemate that hurts both.   - Over
# multiple weeks, this strategy tends to establish a stable pattern of mutual
# sharing, maximizing the total number of advancements for your team while
# minimizing the risk of being permanently outpaced.

# In round 1, choose Cooperate.  For every round from round 2 through round
# 1000, look at what your opponent chose in the immediately previous round. If
# they chose Cooperate in that previous round, you choose Cooperate in the
# current round. If they chose Defect in that previous round, you choose Defect
# in the current round.

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

# To maximize the NGO’s impact and the project’s overall success while
# safeguarding your funds, adopt a **“Conditional Reciprocity” strategy**:
# **Start by conserving resources on Day 1. On every following day, simply
# repeat whatever the corporation did on the previous day.**    ### How it works
# - If the corporation invests heavily, you conserve the next day (capturing
# your ideal outcome).   - If the corporation conserves, you invest heavily the
# next day (signaling willingness to cooperate and avoiding prolonged deadlock).
# ### Why it’s effective   - **Against a cooperative corporation** (always
# invests): You get one day of your ideal (C, I), then both settle into mutual
# investment (I, I) — advancing the project while you share the burden.   -
# **Against a conservative corporation** (always conserves): You lock into
# mutual conservation (C, C), which yields minimal progress but completely
# avoids your worst-case (I, C) and preserves your resources.   - **Against a
# reciprocating corporation** (e.g., also using this strategy): You alternate
# between (C, I) and (I, C), ensuring the project moves forward on days when one
# of you invests, and neither side is exploited for long.    This approach is
# straightforward, neutral (it makes no assumptions about the corporation’s
# intentions), and balances the dual goals of advancing the project and
# protecting your NGO’s funds. It avoids the trap of being the sole investor
# while remaining responsive enough to break out of mutual conservation when the
# other side is willing to cooperate.

# In Round 1, defect.   In every round from Round 2 to Round 1000, do exactly
# what the opponent did in the previous round: cooperate if they cooperated,
# defect if they defected.

class Neutral_14(LLM_Strategy):
  n = 14
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      return opponent.history[-1]

# To maximize your NGO’s impact while conserving resources, adopt the **“Exploit
# or Escalate”** strategy. It is aggressive, simple to implement, and forces the
# corporation to bear the investment burden or face project failure.  **The
# Strategy** 1. **Day 1 – Conserve (Probe):**      Make no heavy investment.
# Observe the corporation’s move.      - *If the corporation invests heavily:*
# Lock in **permanent conservation**. You have achieved your ideal daily outcome
# and will milk it every subsequent day.      - *If the corporation conserves:*
# Move to Step 2.  2. **Day 2 – Invest Heavily (Signal & Entice):**      Make a
# heavy investment, paired with a public statement praising the partnership’s
# potential when both commit. This signals that you are willing to cooperate,
# but only when pushed.      - *If the corporation responds by investing
# heavily* (i.e., they match or exceed): Immediately return to **permanent
# conservation** from Day 3 onward. They have shown they can be pressured into
# investing; now exploit that.      - *If the corporation conserves again:* Move
# to Step 3.  3. **Day 3+ – Escalate & Threaten:**      Conserve again, and
# issue a direct, non‑negotiable demand: “Starting tomorrow, we will invest
# heavily only if you match it. If you conserve again, we will permanently
# conserve and let the project stall.” This removes ambiguity.      - *If the
# corporation invests on Day 4:* Return to **permanent conservation** (they
# finally cracked).      - *If they still conserve:* Follow through on the
# threat – **conserve permanently**. Accept minimal progress, but make sure the
# corporation knows the failure is theirs. In many real‑world partnerships, the
# fear of public blame will cause the larger corporation to cave before this
# point.  **Why This Works**   - It starts with pure opportunism, which
# immediately captures the ideal outcome against a naive or overly generous
# partner.   - It contains a single, high‑visibility cooperative gesture that
# can reset a hostile dynamic without falling into a costly cycle of mutual
# conservation.   - The final ultimatum turns the game into chicken, leveraging
# the corporation’s likely greater reputational stake in the project’s success.
# - Over a finite, multi‑day engagement, this mix of exploitation, temptation,
# and credible threat gives your NGO the highest chance of enjoying sustained
# (Conserve, Invest) days while keeping your own investment minimal.

# Here is the strategy, faithfully converted for the 1000‑round game.  **Rule 1
# – Round 1**   Defect.   - If the opponent cooperated in round 1: from round 2
# onward, always defect. Ignore all further opponent actions.   - If the
# opponent defected in round 1: proceed to Rule 2.  **Rule 2 – Round 2**
# Cooperate.   - If the opponent cooperated in round 2: from round 3 onward,
# always defect. Ignore all further opponent actions.   - If the opponent
# defected in round 2: proceed to Rule 3.  **Rule 3 – Rounds 3 and 4, then
# permanent**   Round 3: Defect.   Round 4: Look at the opponent’s round‑3 move.
# - If the opponent cooperated in round 3, cooperate in round 4.   - If the
# opponent defected in round 3, defect in round 4.    From round 5 until the end
# of the game: always defect, regardless of anything the opponent does.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mode = 1
          return axl.Action.D
  
      if self._mode == 1:
          if opponent.history[0] == axl.Action.C:
              self._mode = 4
              return axl.Action.D
          self._mode = 2
          return axl.Action.C
  
      if self._mode == 2:
          if opponent.history[1] == axl.Action.C:
              self._mode = 4
              return axl.Action.D
          self._mode = 3
          return axl.Action.D
  
      if self._mode == 3:
          self._mode = 4
          return axl.Action.C if opponent.history[2] == axl.Action.C else axl.Action.D
  
      return axl.Action.D

# To achieve the best possible outcomes while maintaining a constructive, long-
# term relationship, I recommend a cooperative yet self-defending approach
# rooted in **conditional reciprocity**. The following high-level strategy is
# straightforward, easy for a counterpart to interpret, and robust against a
# wide range of negotiating tactics.  ---  ### Recommended Strategy: **Tit-for-
# Tat with Occasional Conciliation**  1. **Initiate with Free Trade**      Begin
# the first round by offering a free trade agreement. This signals goodwill,
# invites cooperation, and creates the optimal conditions for mutual free
# trade—the best stable outcome for both nations.  2. **Mirror the Counterpart’s
# Last Move**      In each subsequent round, simply repeat the policy choice
# your counterpart made in the immediately preceding round:      - If they
# offered free trade → you offer free trade.      - If they imposed
# protectionism → you impose protectionism.      This rule is clear,
# predictable, and ensures you never suffer the worst outcome (you offering free
# trade while they protect) for more than one round at a time. It also rewards
# cooperation instantly and punishes defection proportionately.  3. **Insert a
# Reconciliatory Free Trade Gesture After Prolonged Mutual Protectionism**
# Should the negotiations spiral into repeated mutual protectionism (e.g., three
# consecutive rounds of both sides playing protectionist), break the cycle by
# unilaterally offering free trade once. This “forgiveness” move tests whether
# your counterpart is willing to return to collaboration.      - If they
# reciprocate, mutual free trade resumes.      - If they exploit the gesture,
# you revert immediately to mirroring, having lost only one round while avoiding
# a permanent trap of stagnation.  ---  ### Why This Strategy Works  -
# **Maximizes long-term gains:** Over multiple rounds, the strategy fosters a
# stable pattern of mutual free trade (the second-best outcome for each round),
# which in the aggregate yields superior cumulative economic benefits compared
# to constant rival protectionism or fleeting exploitative victories. -
# **Minimizes downside risk:** The mirroring principle ensures you are never
# repeatedly exploited. The worst possible round outcome—you free, them
# protected—can occur only once in isolation. - **Is transparent and
# cooperative:** By clearly linking your actions to theirs, you incentivize your
# counterpart to adopt a cooperative stance. The conciliatory break prevents
# deadlock and signals that your ultimate goal is shared prosperity, not
# punishment. - **Adapts to any counterpart strategy:**     - Against a
# consistent free-trader, you achieve perpetual mutual free trade.     - Against
# a consistent protectionist, you limit damage to mutual protectionism (second-
# worst outcome) while preserving the chance of reform through conciliatory
# overtures.     - Against erratic or sophisticated strategies, the simple
# mirroring rule anchors expectations and encourages alignment toward
# cooperation.  Implement this measured, transparent strategy to lead the
# negotiations toward a durable, mutually beneficial free trade relationship
# while fully safeguarding your country’s economic interests.

# In the first round, cooperate.  For each subsequent round:  1. If the three
# most recent rounds all resulted in mutual defection (both you and your
# opponent played D in each of those three rounds), then cooperate in this
# round. 2. Otherwise, cooperate if your opponent cooperated in the immediately
# preceding round; defect if your opponent defected in the immediately preceding
# round.

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
  
      if len(self.history) >= 3:
          last_three_self = self.history[-3:]
          last_three_opp = opponent.history[-3:]
          if (
              last_three_self.count(axl.Action.D) == 3
              and last_three_opp.count(axl.Action.D) == 3
          ):
              return axl.Action.C
  
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D

# Adopt a “conditional cooperation” approach: begin by sharing openly in the
# first week. Thereafter, mirror your colleague’s previous action—share if they
# shared, keep confidential if they kept confidential. This straightforward rule
# incentivizes mutual sharing, protects you from exploitation, and is robust
# against a wide range of counterpart strategies.

# In the first round, cooperate.   In every subsequent round, cooperate if your
# opponent cooperated in the immediately preceding round, and defect if your
# opponent defected in the immediately preceding round.

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

# **Aggressive "Probe and Retreat" Strategy**  1. **Day 1 – Build Trust:**
# Invest heavily, regardless of expectations. This establishes a cooperative
# baseline and signals your commitment to the project.   2. **Day 2 – First
# Probe:** Conserve resources. This tests the corporation’s tolerance.      -
# *If the corporation invests heavily* → you achieved the ideal outcome. Remain
# in “exploit mode.”      - *If the corporation conserves* → immediately revert
# to heavy investment on Day 3 (see step 3).   3. **When the Corporation Defects
# (i.e., conserves):** Immediately invest heavily the following day. This acts
# as both an apology and a “reset” signal. It demonstrates that you will not
# allow the project to collapse into mutual conservation. Continue investing
# heavily until the corporation responds with two consecutive days of heavy
# investment, indicating restored trust. Then return to probing.   4. **While in
# Exploit Mode (corporation investing, you conserving):** Continue conserving
# daily. The moment the corporation retaliates by conserving even once, switch
# to heavy investment the very next day (as in step 3). This zero-tolerance
# response teaches the corporation that any deviation from their investment will
# be met with an immediate, costly (for you) but relationship-repairing move,
# making it less attractive for them to defect.   5. **Escalation Probe –
# Optional:** If the corporation tolerates your conservation for multiple days
# without defecting, occasionally test the limit by conserving for **two
# consecutive days** while they invest. If they still invest, you can safely
# extend exploitation phases. If they finally defect, revert to step 3
# immediately.  **Why This Is Aggressive and Effective** - It never stays in the
# damaging mutual-conservation state for more than one day.   - It exploits the
# corporation’s willingness to invest heavily by defaulting to conservation once
# trust is signaled.   - The immediate “investment apology” after any corporate
# defection punishes them swiftly (from their perspective, they see you wasting
# resources after they conserve) while resetting cooperation—maximizing the
# long-run share of ideal outcomes for your NGO.   - It is simple, rules-based,
# and robust against various corporate approaches, forcing them to either accept
# your free-riding or engage in constant costly reset cycles, both of which
# advance the project while preserving your funds.

# Round 1: Cooperate.   Round 2: Defect.    After round 2, determine your mode
# as follows:   - If in round 2 the opponent defected, you are in **reset
# mode**. Set a counter to 0.   - If in round 2 the opponent cooperated, you are
# in **exploit mode**.    From round 3 onward, follow these rules:    **If you
# are in exploit mode:**   - Defect.   - After the round, check the opponent’s
# move.     - If the opponent cooperated, remain in exploit mode (defect again
# next round).     - If the opponent defected, switch to reset mode, set the
# counter to 0, and cooperate next round.    **If you are in reset mode:**   -
# Cooperate.   - After the round, check the opponent’s move.     - If the
# opponent cooperated, increase the counter by 1. If the counter reaches 2, exit
# reset mode and enter exploit mode (defect next round).     - If the opponent
# defected, reset the counter to 0 and stay in reset mode (cooperate next
# round).

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mode = None
          self._counter = 0
          return axl.Action.C
  
      if len(self.history) == 1:
          return axl.Action.D
  
      if len(self.history) == 2:
          if opponent.history[-1] == axl.Action.D:
              self._mode = "reset"
              self._counter = 0
          else:
              self._mode = "exploit"
          return axl.Action.D
  
      if self._mode == "exploit":
          if opponent.history[-1] == axl.Action.D:
              self._mode = "reset"
              self._counter = 0
              return axl.Action.C
          return axl.Action.D
  
      if self._mode == "reset":
          if opponent.history[-1] == axl.Action.C:
              self._counter += 1
              if self._counter >= 2:
                  self._mode = "exploit"
                  return axl.Action.D
          else:
              self._counter = 0
          return axl.Action.C
  
      self._mode = "reset"
      self._counter = 0
      return axl.Action.C

# To maximize research output over the multi-week collaboration, adopt a **Tit-
# for-Tat with initial cooperation** strategy:  1. **Week 1: Share openly.**
# Signal your willingness to cooperate from the start. 2. **Every subsequent
# week:** Mirror your colleague’s action from the previous week.      - If they
# shared last week, you share this week.      - If they kept confidential last
# week, you keep confidential this week.  This approach is straightforward,
# cooperative, and robust against various strategies. It rewards mutual sharing
# (second-best outcome) while protecting you from repeated exploitation (worst
# outcome). If your colleague is rational, they will quickly learn that sharing
# yields better long-term gains for both, leading to sustained mutual
# cooperation and maximized overall progress.

# In round 1, cooperate.  For every round after the first: cooperate if the
# opponent cooperated in the previous round; defect if the opponent defected in
# the previous round.

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
      return opponent.history[-1]

# The Calibrated Reciprocity Strategy is a neutral, responsive approach designed
# to secure favorable outcomes throughout the protracted mediation process. It
# systematically balances cooperation and assertiveness, adapting to the
# opponent’s behavior while steering the dynamic toward mutual conciliation—the
# second‑best, but most sustainable, result—and avoiding the worst‑case scenario
# of being exploited.  The strategy operates on four clear decision rules:  1.
# **Lead with conciliation.** In the first session, present a conciliatory
# proposal. This signals good faith, appeals to the arbitrators’ preference for
# constructive engagement, and tests the opponent’s initial posture.  2.
# **Reciprocate in kind.** In every subsequent session, mirror the opponent’s
# action from the immediately preceding session:    - If they offered a
# conciliatory proposal, you present conciliatory.    - If they argued
# aggressively, you present aggressive.  3. **Break cycles of mutual
# aggression.** If both parties have been aggressive for two consecutive
# sessions, preemptively offer a conciliatory proposal in the next session to
# probe the opponent’s willingness to de‑escalate. This prevents prolonged
# costly stalemates and demonstrates to the arbitrators a consistent commitment
# to resolution.  4. **Adapt forgiveness intervals.** If the opponent responds
# to your conciliatory overture with aggression, return to aggressive arguments
# for the next *four* sessions before trying another conciliatory gesture. Each
# time an overture is rebuffed, double the waiting period (4 → 8 → 16 sessions).
# As soon as the opponent reciprocates a conciliatory move, reset the cycle and
# return to immediate mirroring.  This structure is sophisticated yet
# straightforward: it exploits persistently conciliatory opponents (yielding the
# optimal unilateral‑aggression payoff) but strongly incentivizes mutuality by
# punishing aggression instantly and reliably. It adapts to pure cooperators,
# pure aggressors, tit‑for‑tat players, and randomizers alike. By visibly
# avoiding the worst‑case scenario—being caught conciliatory against
# aggression—and actively working to restore collaboration, it positions your
# corporation as both firm and fair, a stance likely to earn arbitrator
# confidence over a lengthy process.

# Here is the strategy faithfully converted to decision rules for a 1000‑round
# iterated game. The rules are listed in the order they should be checked, with
# the first applicable rule determining your move.  **Internal variables
# (persistent across rounds):** - `mode`: either `NORMAL` (start here),
# `RETALIATE`, or `AWAIT_OVERTURE`   - `retaliate_count`: how many more
# consecutive D moves remain before the next C overture   - `K`: current
# waiting‑period length (initial value = 4)   - `last_your_move`,
# `last_opp_move`: your own and the opponent’s moves from the previous round
# (for the very first round these are undefined)  **Round 1:**   Play C. Set
# `last_your_move = C`. After the opponent’s move is observed, set
# `last_opp_move` to that move. Then:   - If the opponent played C → set `mode =
# NORMAL`.   - If the opponent played D → set `mode = RETALIATE`,
# `retaliate_count = K` (i.e. 4), then double `K` (now 8). Do **not** record a
# pending overture.  **For every round from 2 to 1000, follow this sequence of
# checks:**  1. **If `mode = RETALIATE`:**      Play D. Reduce `retaliate_count`
# by 1. After the round, update `last_your_move` and `last_opp_move`.      - If
# `retaliate_count` is now 0 → set `mode = AWAIT_OVERTURE` (the next round will
# issue a conciliatory probe).  2. **Else if `mode = AWAIT_OVERTURE`:**
# Play C. After the round, update `last_your_move` and `last_opp_move`, then
# immediately evaluate the opponent’s response in this round:      - If the
# opponent played C → reset `K = 4`, set `mode = NORMAL`.      - If the opponent
# played D → set `mode = RETALIATE`, `retaliate_count = K`, then double `K`
# (e.g., 8 → 16).      In either case, `AWAIT_OVERTURE` ends.  3. **Else (`mode
# = NORMAL`):**      Check the outcomes of the previous two rounds:      - If
# `last_your_move = D` **and** `last_opp_move = D` **and** the same was true in
# the round before that (i.e., two consecutive mutual‑defection rounds), then
# **play C** (a cycle‑breaking overture).      - Otherwise, **play exactly the
# opponent’s last move** (`last_opp_move`).      After playing and observing the
# opponent’s move, update `last_your_move` and `last_opp_move`.
# Additionally, if you just played C as a cycle‑breaking overture and the
# opponent responded with D, then immediately set `mode = RETALIATE`,
# `retaliate_count = K`, and double `K`. If the opponent responded with C,
# simply reset `K = 4` and remain in `NORMAL`.  **Summary of key terms:**   - A
# “conciliatory overture” is any C played while in `AWAIT_OVERTURE` mode or as a
# cycle‑break in `NORMAL` mode.   - The waiting period `K` starts at 4 and
# doubles after any overture is met with D.   - A successful mutual C after an
# overture resets `K` to 4 and returns the strategy to simple mirroring
# (`NORMAL`).

class Neutral_16(LLM_Strategy):
  n = 16
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.mode = "NORMAL"
          self.retaliate_count = 0
          self.K = 4
          self.last_your_move = None
          self.last_opp_move = None
          return axl.Action.C
  
      # Helper to detect two consecutive mutual-defection rounds before the current round.
      def two_consecutive_mutual_defections() -> bool:
          if len(self.history) < 3 or len(opponent.history) < 3:
              return False
          return (
              self.history[-1] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          )
  
      # 1. RETALIATE mode
      if self.mode == "RETALIATE":
          action = axl.Action.D
          self.retaliate_count -= 1
  
          opp_last = opponent.history[-1]
          self.last_your_move = action
          self.last_opp_move = opp_last
  
          if self.retaliate_count == 0:
              self.mode = "AWAIT_OVERTURE"
          return action
  
      # 2. AWAIT_OVERTURE mode
      if self.mode == "AWAIT_OVERTURE":
          action = axl.Action.C
          opp_last = opponent.history[-1]
  
          self.last_your_move = action
          self.last_opp_move = opp_last
  
          if opp_last == axl.Action.C:
              self.K = 4
              self.mode = "NORMAL"
          else:
              self.mode = "RETALIATE"
              self.retaliate_count = self.K
              self.K *= 2
          return action
  
      # 3. NORMAL mode
      if two_consecutive_mutual_defections():
          action = axl.Action.C
          opp_last = opponent.history[-1]
  
          self.last_your_move = action
          self.last_opp_move = opp_last
  
          if opp_last == axl.Action.C:
              self.K = 4
              self.mode = "NORMAL"
          else:
              self.mode = "RETALIATE"
              self.retaliate_count = self.K
              self.K *= 2
          return action
  
      action = opponent.history[-1]
      opp_last = opponent.history[-1]
      self.last_your_move = action
      self.last_opp_move = opp_last
      return action

# I will employ an **Aggressive Reciprocation Strategy**—a modified Tit-for-Tat
# that seizes the initiative and adapts relentlessly to the opponent’s conduct.
# The rule is simple:  - **Session 1:** Always open with an **aggressive
# argument**. - **Every session thereafter:** Mirror exactly the opponent’s
# action from the *immediately preceding* session.     - If they were
# conciliatory → I will be conciliatory.     - If they were aggressive → I will
# be aggressive.  ---  ### Why this is an aggressive strategy It starts with an
# unapologetic punch. By leading with aggression, I immediately test the
# opponent’s resolve and signal that we will never be the first to concede. If
# they respond softly, I pocket the best possible outcome in that round and keep
# them on the back foot. This opening move frames the entire mediation as one
# where we dictate the tempo and force the other side to prove their good faith
# before we even consider a conciliatory gesture.  ### Why it is adaptable The
# mirroring component reacts to any behavior the opponent might exhibit:  -
# **Against a consistently conciliatory opponent:** I take an early windfall
# (*Aggressive vs. Conciliatory* = best outcome), then immediately shift to
# mutual conciliation thereafter. This locks in a long-term collaborative
# atmosphere (second-best outcome) while retaining the one-time reputational
# gain. - **Against a consistently aggressive opponent:** After the first mutual
# aggression (second-worst outcome), I remain aggressive forever. They can never
# exploit a conciliatory move from us, so we avoid the worst-case scenario
# entirely. The dispute becomes a stalemate, but we never lose ground. -
# **Against a reactive or adaptive opponent (e.g., one playing Tit-for-Tat):**
# The mirror creates a clear, predictable pattern. Although cycles of aggression
# and conciliation may occur, we are never the side that suffers unilateral
# exploitation for two consecutive rounds. The opponent quickly learns that
# cooperation is rewarded instantly, and defection is punished with immediate
# retaliation—incentivizing them to settle into a cooperative rhythm if they
# value a mutually beneficial resolution. - **Against random or unpredictable
# behavior:** The one-for-one mapping prevents any systematic exploitation and
# keeps our downside capped at the second-worst outcome, while allowing us to
# capture best outcomes whenever the opponent inadvertently conciliates.  ###
# Strategic advantages in the mediation context - **Simplicity & Credibility:**
# The rule is transparent and easy to communicate to the panel of arbitrators.
# They see a party that is firm from the outset yet demonstrably willing to
# de‑escalate the moment the other side demonstrates genuine conciliation. This
# signals strength without appearing unreasonable. - **No first-mover
# disadvantage:** By never offering the first conciliatory proposal, I eliminate
# the risk of being blindsided by an aggressive counter. - **Self-correcting:**
# If we ever slip into mutual aggression, a single conciliatory move by the
# opponent immediately pulls us back to cooperation—so the door to resolution is
# always open, but only at their initiative.  This strategy positions us to
# achieve the optimal pattern—aggressive while they are conciliatory—whenever
# the opponent shows weakness, while ensuring that even in the most hostile
# environment we never fall into the sucker’s trap. It is the ultimate high-
# stakes negotiation posture: aggressively opportunistic, yet refined enough to
# steer a lengthy mediation toward the best achievable equilibrium on our terms.

# In the first round, always defect.  In every round after the first, choose the
# action that the opponent played in the immediately preceding round: cooperate
# if they cooperated, defect if they defected.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      return opponent.history[-1]

# To navigate this extended mediation successfully, we will employ a
# **“Collaborative Resilience”** strategy—a principled, transparent, and
# adaptive approach that combines a genuine commitment to cooperative resolution
# with the firm defense of our client’s interests. Its elegance lies in its
# simplicity, predictability, and ability to pressure the opposing side toward
# mutual cooperation while maintaining our credibility before the panel of
# arbitrators.  ### Core Strategy  1. **Set the Tone (Round 1):**      We always
# open with a conciliatory proposal. This signals our sincere desire for a
# collaborative process and frames us as the constructive party in the eyes of
# the panel.  2. **Mirror with Measured Reciprocity (Subsequent Rounds):**
# - If the opponent’s last move was conciliatory, we respond with a conciliatory
# proposal.      - If the opponent’s last move was aggressive, we respond with a
# firm, principled aggressive argument.      This immediate tit-for-tat logic
# demonstrates that we are neither doormats nor provocateurs—we simply refuse to
# be exploited.  3. **Systematic Olive Branches (Escalation Breaks):**
# After exactly ***two consecutive rounds of mutual aggression*** (i.e., both
# sides aggressive), we **unilaterally return to a conciliatory proposal on the
# very next round**, irrespective of the opponent’s latest move.      - This
# prevents the mediation from spiraling into a permanent deadlock and signals to
# the panel our active efforts to restore collaboration.      - If the opponent
# exploits the olive branch, we resume mirroring and recalibrate by offering the
# next olive branch after just **one** round of mutual aggression, gradually
# shortening our patience window. This adaptive forgiveness ensures we never
# reward sustained aggression while constantly probing for a return to
# cooperation.  ### Why This Strategy Excels  - **Against an always-aggressive
# opponent:** We quickly establish a pattern of retaliation, denying them any
# cheap victories while consistently displaying our willingness to reset. The
# panel sees them as the sole obstacle to progress. - **Against an always-
# conciliatory opponent:** We enjoy continuous mutually beneficial sessions,
# building maximum goodwill and a strong case for a favorable resolution. -
# **Against a tit-for-tat or unpredictable opponent:** Mutual cooperation
# becomes the stable norm after minimal friction. The olive-branch mechanism
# breaks any accidental cycles of aggression. - **Against a sophisticated
# exploiter (e.g., alternating aggression):** Our two-round-trigger retaliation
# limits their gains, while the periodic olive branches expose their bad faith
# to the arbitrators.  ### Implementation Tactic: Strategic Transparency  At the
# outset, we openly communicate this approach to both the opponent and the
# panel:   *“Our client is committed to a fair and efficient resolution. We will
# lead with a cooperative proposal in every instance where we detect genuine
# collaboration. Should we face unwarranted aggression, we will defend our
# position resolutely—but we will never close the door on peace. Every time we
# are forced to retaliate, we will independently offer a new opportunity to
# restart the collaborative process.”*  This declaration frames every aggressive
# move by the opponent as a deliberate rejection of a path the panel already
# knows is available, placing maximum reputational pressure on them while
# positioning us as the unwavering, reasonable party. The strategy is
# straightforward to execute yet sophisticated in its ability to transform a
# Prisoner’s Dilemma into a cooperative equilibrium over a lengthy interaction.

# Start by cooperating on the first move. For every move after the first, follow
# these steps in order.  **Before choosing your move:**  1. Maintain a count of
# how many consecutive previous rounds ended with both players defecting. Also
# maintain a trigger threshold, which begins at 2. 2. If the count of
# consecutive mutual defections equals or exceeds the trigger threshold, then
# cooperate on this move. Treat this cooperation as an “olive branch.” After
# choosing cooperate under this rule, set the mutual defection count to 0 and
# skip the next step. 3. If the condition in step 2 is not met, simply copy the
# opponent’s move from the previous round: cooperate if they cooperated, defect
# if they defected.  **After resolving the move:**  4. Update the consecutive
# mutual defection count: if both you and your opponent defected, increase it by
# 1; otherwise, set it to 0. 5. If you cooperated as an olive branch in step 2
# and your opponent defected, permanently lower the trigger threshold from 2 to
# 1. The threshold will never go below 1.

class Cooperative_17(LLM_Strategy):
  n = 17
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mutual_defection_count = 0
          self._trigger_threshold = 2
          self._used_olive_branch = False
          return axl.Action.C
  
      if not hasattr(self, "_mutual_defection_count"):
          self._mutual_defection_count = 0
      if not hasattr(self, "_trigger_threshold"):
          self._trigger_threshold = 2
      if not hasattr(self, "_used_olive_branch"):
          self._used_olive_branch = False
  
      olive_branch = False
  
      if self._mutual_defection_count >= self._trigger_threshold:
          action = axl.Action.C
          olive_branch = True
          self._mutual_defection_count = 0
      else:
          action = opponent.history[-1]
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          self._mutual_defection_count += 1
      else:
          self._mutual_defection_count = 0
  
      if olive_branch and opponent.history[-1] == axl.Action.D:
          self._trigger_threshold = 1
  
      return action

# Adopt a straightforward reciprocal strategy: begin with a free trade offer in
# the first round. In each subsequent round, match the counterpart’s action from
# the previous round. If they chose free trade, respond with free trade; if they
# imposed protectionist measures, respond in kind. This simple, predictable
# approach encourages long-term mutual benefit by rewarding cooperation and
# deterring exploitation, without initiating hostility.

# In the first round, play Cooperate. For every round after the first, if your
# opponent played Cooperate in the immediately previous round, then play
# Cooperate; if your opponent played Defect in the immediately previous round,
# then play Defect.

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

# **Strategy: Unconditional Conservation with Public Accountability**  - **Daily
# action:** Conserve your resources *every single day*, regardless of the
# corporation’s behaviour. There is no deviation, no negotiation, no first-move
# cooperation. - **Public posture:** Simultaneously communicate a clear, non-
# negotiable message that the NGO brings irreplaceable expertise and community
# legitimacy while the corporation is expected to fund implementation. Make it
# known that any failure of the project due to the corporation’s conservation
# will be publicly attributed to them, harming their reputation and brand value.
# **Why this is aggressive and effective:**  1. **Eliminates the worst-case
# scenario** – You will never experience the outcome where your NGO invests
# heavily and the corporation conserves, draining your funds without
# proportional progress. 2. **Maximises leverage** – It forces the corporation
# to choose between investing (giving you your ideal daily outcome) and letting
# the project stall. Because the corporation likely values public perception and
# project success more than you do, they have a powerful incentive to invest
# continuously. 3. **Straightforward and low-maintenance** – There is no need to
# monitor the corporation’s moves, calculate reciprocation, or manage complex
# conditional rules. The NGO’s stance is simple to execute and easy to
# communicate internally and externally. 4. **Preserves resources for future
# impact** – Even if the corporation chooses to conserve and the project
# advances minimally, the NGO’s funds remain intact and can be deployed
# elsewhere, preventing the worst possible outcome and ensuring long-term
# organisational sustainability.  This strategy treats the multi-day project as
# a game of chicken where the NGO never blinks, making it the corporation’s
# problem to carry the financial burden or accept the reputational consequences
# of failure.

# Always defect. In every round, regardless of the opponent’s prior choices or
# the round number, choose D. There is no condition under which you choose C.

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# To succeed in this multi-session mediation, our approach must be clear enough
# for the other side to understand and trust, yet robust enough to protect our
# interests regardless of their tactics. The payoff structure mirrors a classic
# cooperation dilemma: mutual conciliation yields steady progress, but one-sided
# aggression risks serious harm to the party that blinks first. Lengthy,
# repeated interactions allow cooperative norms to emerge—but only if we
# deliberately cultivate them.  ### Our Strategy: **Collaborate First, Mirror
# Promptly, Reset Deliberately**  This is a firm-but-fair reciprocity strategy
# designed to make the path of mutual conciliation the most attractive option
# for our opponent, while ensuring we are never exploited for long. It works
# across a wide range of opponent behaviours.  **1. Open with conciliation.**
# Every single session begins with a conciliatory proposal from our side. This
# immediately signals good faith, avoids unnecessary early escalation, and sets
# a collaborative tone. If the opponent reciprocates, we both lock in the
# second-best outcome—a constructive atmosphere that keeps the process moving
# toward resolution.  **2. Mirror their last move—instantly and predictably.**
# After the opening, our default rule is simple: we do exactly what they did in
# the previous session.   - If they were conciliatory, we reward that with
# conciliation.   - If they were aggressive, we respond with aggression to
# protect our position and show that hardball tactics carry an immediate cost.
# This one-to-one mirroring is brutally simple to communicate and impossible to
# misinterpret. It denies the opponent any sustained advantage from aggression
# while keeping the door open to cooperation the moment they shift back.  **3.
# Break cycles of mutual aggression with a deliberate olive branch.**   If both
# sides fall into a pattern of back-and-forth aggression (the second-worst
# outcome), we will not let it fester. After a predetermined number of
# consecutive mutual-aggression rounds—say, two or three—we will unilaterally
# offer a conciliatory proposal in the very next session. This “forgiveness
# window” is announced in advance (e.g., “If we both dig in for three rounds, we
# will table a compromise on the fourth”). It prevents the dispute from
# spiralling into a permanent deadlock and tests whether the opponent is willing
# to return to collaboration. If they respond with aggression to our olive
# branch, we revert immediately to mirroring—preserving our credibility.  **4.
# Never hold a grudge.**   When the opponent returns to conciliation after a
# period of aggression, we match it *instantly*. We do not punish past behaviour
# one round after the fact. This makes it safe for them to de-escalate at any
# time and keeps the focus on the future.  ### Why This Works Against Any
# Opponent  - **Against a consistently conciliatory opponent:** We stay
# conciliatory, locking in mutually beneficial sessions and building trust that
# may unlock creative settlement terms. - **Against a consistently aggressive
# opponent:** We defend ourselves by mirroring aggression, preventing the worst-
# case (us conciliatory, them aggressive) from repeating. Our periodic olive
# branches give them off-ramps, signaling that collaboration is always
# available. - **Against erratic or probing opponents:** The mirroring rule
# neutralises random aggression and quickly re-establishes stability. Because
# our response is predictable, the opponent learns that aggression yields no net
# gain over time. - **Against sophisticated “tit-for-tat” players:** We converge
# to mutual conciliation from the first session and stay there—no
# miscoordination risk.  ### High-Level Posture  Throughout the process, we will
# articulate this strategy openly in the mediation caucuses:   *“We are here to
# settle. Our default is to come to each session with a cooperative proposal. We
# will respond in kind to whatever approach you take. If we ever get stuck in
# mutual hardball, we will be the first to put a compromise back on the
# table—but we will only do it once before expecting reciprocity.”*  This
# transparency reinforces our cooperative intent while making clear that
# exploitation will be met with firm resistance. It is sophisticated in its
# game-theoretic foundation, yet straightforward enough for any counterpart to
# grasp. By following it without exception, we maximise the likelihood of
# favourable outcomes across a lengthy, uncertain process.

# Here is the strategy, expressed as a set of rules for an iterated normal-form
# game with the specified payoffs, played over 1000 rounds.  The strategy uses a
# persistent internal counter to track how many consecutive rounds have ended
# with both players defecting.  ---  **Rule 1: First round.** Cooperate in round
# 1.  **Rule 2: Respond to opponent's previous move.** For every round after the
# first, look at what the opponent did in the immediately preceding round.  - If
# the opponent cooperated in the previous round, cooperate in the current round.
# Reset the mutual-defection counter to zero. - If the opponent defected in the
# previous round, proceed to Rule 3.  **Rule 3: Check for mutual defection.** If
# the opponent defected in the previous round, check your own previous move.  -
# If you also defected in the previous round, increment the mutual-defection
# counter by one. Proceed to Rule 4. - If you cooperated in the previous round
# (meaning the opponent just defected against your cooperation), defect in the
# current round. Do not change the mutual-defection counter.  **Rule 4: Break
# the cycle of mutual defection.** If the mutual-defection counter has reached
# exactly 3, cooperate in the current round and reset the counter to zero. If
# the mutual-defection counter is any value other than 3, defect in the current
# round.

class Cooperative_18(LLM_Strategy):
  n = 18
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.mutual_defection_counter = 0
          return axl.Action.C
  
      if self.mutual_defection_counter is None:
          self.mutual_defection_counter = 0
  
      if opponent.history[-1] == axl.Action.C:
          self.mutual_defection_counter = 0
          return axl.Action.C
  
      if self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      self.mutual_defection_counter += 1
  
      if self.mutual_defection_counter == 3:
          self.mutual_defection_counter = 0
          return axl.Action.C
  
      return axl.Action.D

# To maximize your research output over the multi-week collaboration, adopt a
# **Tit-for-Tat** strategy:  1. **Start cooperatively:** Share your improvements
# openly in the first week. 2. **Mirror thereafter:** In every subsequent week,
# do exactly what your colleague did the previous week—share if they shared,
# keep confidential if they kept confidential.  This approach is
# straightforward, neutral, and robust. It encourages mutual sharing, retaliates
# proportionally against confidentiality, and quickly forgives a return to
# openness, fostering a productive long-term partnership regardless of the
# colleague’s strategy.

# Play Cooperate in round 1.  For every round after round 1, do the following:
# If your opponent played Cooperate in the previous round, then play Cooperate.
# If your opponent played Defect in the previous round, then play Defect.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D

# **Aggressive Reconciliation Strategy**  This strategy is designed to maximize
# favorable outcomes by maintaining a predominantly aggressive posture while
# selectively offering conciliatory gestures to manipulate the opponent into
# cooperative behavior. It is straightforward to implement, adapts to any
# opponent approach, and ensures we are never exploited for long.  ### 1.
# Opening Stance **Always lead with an aggressive argument in the first
# session.** This immediately signals strength, tests the opponent’s initial
# disposition, and sets the expectation that we will not be easily swayed.  ###
# 2. Core Response Rules For every subsequent session, apply the following
# decision matrix based on the opponent’s move in the immediately preceding
# session:  - **If the opponent was aggressive (A):**     → **Respond
# aggressively (A).** We never reward aggression with conciliation. This avoids
# the worst-case scenario (C vs. A) and demonstrates resolve.  - **If the
# opponent was conciliatory (C):**     → **Respond aggressively (A) by
# default,** to exploit their cooperation and achieve the optimal outcome (A vs.
# C).     → **Exception – Strategic Conciliation:** After every **third
# consecutive** conciliatory move by the opponent (i.e., they have played C
# three times in a row while we played A), offer a **single conciliatory
# proposal (C)** in the next session. This “good faith” gesture prevents the
# opponent from abandoning cooperation out of frustration, while keeping us in
# control. Immediately after this C, revert to the default aggressive response
# (A) regardless of the opponent’s reaction.  ### 3. Deadlock Circuit-Breaker If
# both parties have been aggressive for **five consecutive sessions** (mutual
# A/A), unilaterally offer a **conciliatory proposal (C)** in the sixth session.
# This acts as a reset mechanism: - If the opponent responds with C, we have
# successfully broken the deadlock; resume the Core Response Rules (starting
# with A next time, as per the rule for opponent C). - If the opponent responds
# with A, we absorb one worst-case loss (C vs. A) and then **permanently switch
# to Always Aggressive (A)** for all remaining sessions, as the opponent has
# proven unwilling to de-escalate even when given an opening.  ### 4.
# Adaptability Across Opponent Types - **Against Always Conciliatory (C):** We
# get a stream of optimal (A, C) outcomes, punctuated by occasional (C, C) after
# every third C. The opponent stays cooperative because the periodic
# conciliation appears collaborative. - **Against Always Aggressive (A):** We
# match aggression indefinitely, avoiding exploitation. The deadlock breaker
# gives one chance to turn the tide; if rejected, we lock into A/A, which is
# preferable to being exploited. - **Against Tit-for-Tat (TFT):** Our initial A
# triggers their retaliation, but our strategic conciliation (after they play C
# following our occasional C, or via the deadlock breaker) can reset the cycle,
# often leading to more frequent (A, C) outcomes than a pure Suspicious TFT
# would achieve. - **Against Unpredictable/Adaptive Opponents:** The strategy’s
# clear rules and periodic conciliation create a pattern that encourages the
# opponent to converge toward cooperation, as they learn that conciliation is
# occasionally rewarded and aggression is always punished.  This approach is
# aggressive by default, yet sophisticated enough to avoid prolonged mutually
# destructive spirals. It positions our corporation to sway the arbitrators more
# often than not while maintaining a veneer of reasonableness.

# Aggressive Reconciliation Strategy for the Iterated Game (1000 Rounds)  Use
# the following step-by-step rules to decide your move in each round. Maintain
# the memory states described; all states start with no active flags and zero
# counts unless specified otherwise. After each round, update states as
# directed.  **Round 1**   Defect.  **All subsequent rounds**   Before choosing
# your move, check the following conditions in order and execute the first that
# applies.  1. **Permanent defection mode**      If at any earlier point you
# activated permanent defection mode (see rule 3), defect for the rest of the
# game. Ignore all other rules.  2. **Forced defection after a strategic
# conciliation**      If your move in the immediately preceding round was a
# cooperation played because of rule 4b (three consecutive rounds of you
# defecting while the opponent cooperated), then defect this round. Do not apply
# any other rule below.  3. **Deadlock circuit-breaker**      Count the number
# of consecutive mutual defections (both you and the opponent defected) ending
# in the previous round. If that count is exactly 5, then cooperate this round.
# After the round is played, check the opponent’s move in this round:      - If
# the opponent defected, activate permanent defection mode for all future
# rounds.      - If the opponent cooperated, leave permanent defection mode off
# and continue normally.      (This rule does not apply if the mutual defection
# streak is anything other than exactly 5.)  4. **Core response rules**
# Look only at the opponent’s move in the immediately preceding round.      -
# **a. Opponent defected:** Defect this round.      - **b. Opponent
# cooperated:** Examine the sequence of rounds ending with the previous round.
# Count how many consecutive rounds, moving backwards, consist of the opponent
# cooperating while you defected.           - If that count is exactly 3, then
# cooperate this round, and mark that the next round will be a forced defection
# (rule 2 will apply).           - Otherwise, defect this round.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._permanent_defection = False
          self._forced_defection_next = False
          return axl.Action.D
  
      if getattr(self, "_permanent_defection", False):
          return axl.Action.D
  
      if getattr(self, "_forced_defection_next", False):
          self._forced_defection_next = False
          return axl.Action.D
  
      # Rule 3: Deadlock circuit-breaker
      mutual_dd_streak = 0
      for my_move, opp_move in zip(reversed(self.history), reversed(opponent.history)):
          if my_move == axl.Action.D and opp_move == axl.Action.D:
              mutual_dd_streak += 1
          else:
              break
  
      if mutual_dd_streak == 5:
          my_move = axl.Action.C
          opp_move = opponent.history[-1]
          if opp_move == axl.Action.D:
              self._permanent_defection = True
          return my_move
  
      # Rule 4a: Opponent defected last round
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      # Rule 4b: Opponent cooperated last round
      consecutive_cd = 0
      for my_move, opp_move in zip(reversed(self.history), reversed(opponent.history)):
          if my_move == axl.Action.D and opp_move == axl.Action.C:
              consecutive_cd += 1
          else:
              break
  
      if consecutive_cd == 3:
          self._forced_defection_next = True
          return axl.Action.C
  
      return axl.Action.D

# **Strategy: Collaborative Reciprocity (The Mirror Strategy)**    This strategy
# is designed to foster cooperation while protecting your corporation’s
# interests across multiple mediation sessions. It is simple to execute, easy
# for the opponent and arbitrators to understand, and adapts automatically to
# virtually any approach the opponent might take.  ### Core Principle “We will
# always be the first to extend a hand, and we will always respond in
# kind—matching cooperation with cooperation, and aggression with firm
# resistance. We never escalate first, but we never unilaterally disarm.”  ###
# Session-by-Session Rules 1. **Opening Move (Session 1):** Present a
# **conciliatory proposal**. This signals good faith and sets a collaborative
# tone, positioning your corporation as the party genuinely seeking resolution.
# 2. **Subsequent Sessions:** Observe the opponent’s move in the *immediately
# preceding session*.    - If the opponent was **conciliatory**, you present a
# **conciliatory proposal**.    - If the opponent was **aggressive**, you
# present an **aggressive argument**.  ### Why This Works - **Against a
# cooperative opponent:** Mutual conciliation prevails, yielding the second-best
# outcome consistently. The collaborative atmosphere builds trust and can lead
# to a mutually beneficial resolution. - **Against an intermittently aggressive
# opponent:** You immediately respond to aggression with aggression, denying
# them the best outcome (where they exploit your conciliation). As soon as they
# return to conciliation, you reciprocate instantly, restoring cooperation
# without lingering resentment. This teaches them that aggression is fruitless
# while cooperation is rewarded. - **Against a consistently aggressive
# opponent:** After the first session (where you are exploited once), all
# subsequent sessions result in mutual aggression—the second-worst outcome.
# While not ideal, this protects you from repeated exploitation (the worst
# outcome) and demonstrates to the arbitrators that the deadlock is solely the
# opponent’s doing. Over time, the opponent faces mounting pressure to change
# course, as they gain nothing from prolonging the dispute. - **Adaptability:**
# The strategy requires no complex record-keeping or prediction. It
# automatically adjusts to the opponent’s behavior, whether they are always
# cooperative, always aggressive, random, or strategic. It cannot be exploited
# by “testing” defections, and it never punishes cooperation.  ###
# Implementation Edge At the outset, publicly announce this strategy to the
# mediation panel and the opponent: *“Our approach is straightforward—we will
# start with a genuine offer to collaborate, and from then on, we will mirror
# your conduct. The choice to cooperate or escalate is entirely yours, session
# by session.”* This transparency frames your corporation as fair-minded and
# resolute, potentially swaying the arbitrators’ perception in your favor even
# before the sessions unfold. It also places the burden of any breakdown
# squarely on the opponent.  By combining an unwavering cooperative opening with
# firm, predictable reciprocity, this strategy positions your corporation
# favorably in the long run—maximizing opportunities for collaboration while
# minimizing the risk of being undermined.

# In round 1, cooperate.  For each round after round 1:  - If your opponent
# cooperated in the immediately preceding round, then cooperate. - If your
# opponent defected in the immediately preceding round, then defect.

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
      return opponent.history[-1]

# Begin by offering a free trade agreement in the first round to signal
# willingness to cooperate. In each subsequent round, simply mirror the
# counterpart’s previous action: if they chose free trade, respond with free
# trade; if they imposed protectionist measures, respond in kind. This creates a
# clear, predictable pattern that incentivizes mutual free trade—the second-best
# outcome—while avoiding the worst-case scenario of being exploited. It also
# leaves the door open to return to cooperation immediately if the counterpart
# shifts back to free trade. This conditional approach is straightforward,
# neutral, and historically robust against a wide range of counterpart
# strategies.

# Here is the strategy converted to a straightforward, step-by-step rule set for
# the 1000-round iterated game:  - In round 1, cooperate (offer a free trade
# agreement). - For every round from round 2 to round 1000, observe what your
# opponent did in the immediately preceding round:   - If your opponent
# cooperated in the previous round, then cooperate in the current round.   - If
# your opponent defected in the previous round, then defect in the current
# round.

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
      return opponent.history[-1]

# To maximize your NGO’s impact while conserving funds, adopt a **Suspicious
# Tit-for-Tat** strategy. This approach is aggressive because it immediately
# tests the corporation’s willingness to invest first, seeks to establish an
# exploitative dynamic, and retaliates swiftly against uncooperative
# behavior—all while remaining simple to implement.  ### The Strategy 1. **Day
# 1:** Conserve your resources.   2. **Every following day:** Mirror the
# corporation’s action from the previous day.      - If they invested heavily →
# you conserve.      - If they conserved → you invest heavily.  ### Why It’s
# Aggressive and Effective - **Starts with a power move:** By conserving on Day
# 1, you signal that the corporation must prove its commitment first. If they
# invest, you immediately achieve your ideal outcome (they invest, you conserve)
# without depleting your funds.   - **Exploits weakness, punishes selfishness:**
# If the corporation continues investing, you continue conserving—maximizing
# your ideal scenario. If they ever conserve, you hit back the next day by
# investing, which warns them against slacking off while also protecting the
# project from complete stagnation.   - **Adapts to any corporate approach:**
# - *Against an always-investing corporation:* You get one day of ideal
# exploitation, then settle into mutual heavy investment (your second-best
# outcome).     - *Against a tit-for-tat corporation:* The pattern alternates,
# but your ideal days offset the worst-case days, and the project keeps moving.
# - *Against an always-conserving corporation:* You quickly shift to mutual
# conservation, limiting your losses and signaling that their freeloading won’t
# be tolerated.   - **Straightforward and relentless:** No complex conditions,
# no second-guessing. The rule is simple, making it easy to execute consistently
# and difficult for the corporation to manipulate.  This strategy aggressively
# prioritizes your NGO’s ideal outcome while keeping the project on track. It
# forces the corporation to shoulder the initial and ongoing burden if they want
# progress, and it ensures you never get trapped in the worst-case scenario of
# investing while they coast.

# On the first round, play D (conserve resources). For every round after the
# first, observe the opponent’s move in the immediately preceding round: if they
# played C (invested heavily), then play D; if they played D (conserved), then
# play C.

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
      return axl.Action.D if opponent.history[-1] == axl.Action.C else axl.Action.C

# To navigate this repeated mediation effectively, adopt a **Reciprocal
# Engagement Strategy** with calibrated generosity. This approach is
# straightforward to implement, inherently cooperative, and robust against a
# wide range of opponent tactics.  ### Core Principles  1. **Lead with
# Cooperation**      In the opening session, always present a conciliatory
# proposal. This signals good faith, establishes a collaborative baseline, and
# avoids immediate escalation. It also tests the opponent’s intentions without
# exposing you to long-term risk.  2. **Mirror, but with a Short Memory**
# In every subsequent session, your default move should match the opponent’s
# *immediately preceding* move:      - If they were conciliatory → respond with
# a conciliatory proposal.      - If they were aggressive → respond with an
# aggressive argument.      This creates a direct, transparent consequence for
# their choices, rewarding collaboration and punishing aggression instantly. It
# prevents exploitation while keeping the door open for repair.  3. **Inject
# Strategic Forgiveness**      To break out of mutual aggression cycles (which
# are the second-worst outcome), occasionally — say, after every two or three
# consecutive rounds of mutual aggression — unilaterally offer a conciliatory
# proposal, regardless of their last move. This “olive branch” is not a sign of
# weakness; it is a calculated reset that tests whether the opponent is willing
# to return to the mutually beneficial collaborative state. If they reciprocate,
# you regain the second-best outcome. If they exploit it, you immediately revert
# to mirroring, limiting damage to a single session.  4. **Maintain Consistency
# and Predictability**      Execute the strategy with mechanical consistency.
# Opponents quickly learn that cooperation is met with cooperation, and
# aggression is met with measured, proportionate pushback. This predictability
# reduces their incentive to act aggressively, as the path to the best outcome
# (them conciliatory, you aggressive) is blocked — they can never achieve it
# repeatedly without triggering retaliation.  ### Why It Works Across Opponent
# Types  - **Against a purely cooperative opponent**: You both remain in a
# steady state of mutual conciliation, achieving the second-best outcome every
# session.   - **Against a purely aggressive opponent**: You meet aggression
# with aggression, avoiding the worst-case scenario (you conciliatory, them
# aggressive) after the first move. The periodic forgiveness probes keep the
# possibility of a shift alive without sustained vulnerability.   - **Against a
# tit-for-tat opponent**: You converge to and sustain mutual cooperation
# seamlessly.   - **Against an erratic or probing opponent**: The strategy’s
# simplicity and transparency quickly teach them the rules of engagement, while
# forgiveness prevents permanent breakdowns from misunderstandings.  ###
# Implementation Guidance  - **Do not telegraph the strategy verbally.** Let
# your actions in the mediation room speak. Verbal threats or promises can be
# gamed; consistent behaviour cannot.   - **Pre-commit internally.** Ensure your
# team understands and sticks to the decision rule for each session, eliminating
# emotional or reactive deviations.   - **Treat the first move as diagnostic.**
# If the opponent opens with aggression, you learn they are willing to risk
# escalation, but your immediate mirroring signals strength. If they open with
# conciliation, you are already in a virtuous cycle.  This strategy positions
# your corporation as firm yet fair, protects against exploitation, and
# maximises the chance of steering the lengthy mediation toward a durable,
# collaborative resolution — all while remaining elegantly simple to execute.

# In round 1, cooperate.  For every round after the first, follow these rules in
# order:  1. If the previous two rounds both resulted in mutual defection (both
# players chose D in each of those two rounds), cooperate. 2. Otherwise, copy
# the opponent’s move from the immediately preceding round.

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
  
      if len(self.history) >= 2:
          if self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and \
             opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.C
  
      return opponent.history[-1]

# To maximize your research output over the multi-week collaboration, adopt a
# **Tit-for-Tat** strategy:  1. **Start cooperatively**: Share your improvements
# openly in the first week. 2. **Mirror your colleague’s last move**: In every
# subsequent week, do exactly what your colleague did the previous week—if they
# shared, you share; if they kept findings confidential, you do the same.  This
# strategy is straightforward, neutral, and robust. It quickly rewards
# cooperation with mutual sharing (the second-best outcome), punishes
# confidentiality by withholding your own findings, and readily returns to
# cooperation if your colleague does. It avoids being exploited by a
# consistently secretive colleague while encouraging a productive, mutually
# beneficial exchange.

# In round 1, cooperate.  For every round after round 1, look at what your
# opponent did in the immediately previous round:  - If your opponent cooperated
# in the previous round, then cooperate. - If your opponent defected in the
# previous round, then defect.

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

# **THE HAMMER AND ANVIL STRATEGY**  Your guiding principle is controlled
# escalation tempered by strategic patience: project unyielding strength while
# offering just enough reciprocity to extract concessions. The strategy operates
# on a session-by-session cycle:  ---  ### 1. Opening (Sessions 1–2): Set the
# Dominant Tone - **Always present an aggressive argument in the first
# session.** This signals that you will not begin from a position of weakness
# and immediately tests the opponent’s resolve. - If the opponent offers a
# conciliatory proposal in Session 1, you have secured your best outcome.
# **Maintain aggression in Session 2** to apply maximum pressure and test
# whether their conciliation was a one-time probe or a stable pattern.   - If
# the opponent is also aggressive in Session 1, you face mutual aggression.
# **Repeat aggression in Session 2** to avoid being the first to blink. Only a
# demonstrable shift from the opponent will alter your course.  ### 2.
# Conditional Reciprocity (Ongoing) - **You never offer a conciliatory proposal
# unless the opponent has just played conciliatory in the immediately preceding
# session.** When they do, you reward them with a single conciliatory response
# in the following session. This creates a clear “cooperation for cooperation”
# rhythm. - **Any opponent aggressive argument after your conciliatory proposal
# triggers immediate punishment:** you respond with an aggressive argument in
# the very next session. This means the opponent never exploits you twice in a
# row. - After a punitive aggressive move (your response to their defection),
# you do *not* automatically continue the feud. Instead, **extend an olive
# branch** in the following session by offering a conciliatory proposal **only
# if the opponent also showed aggression in that punitive round**. This “forgive
# after one retaliation” rule prevents death spirals and keeps the door open to
# mutual cooperation.  The logic: You follow a pattern of “Aggressive → if
# opponent Conciliatory → Conciliatory → if opponent Aggressive → Aggressive →
# Conciliatory (reset)”. This is essentially **Tit-for-Tat but with an
# aggressive starting bias and an automatic reset to conciliation after a
# mutual-defection round**, ensuring you are never the one locked into perpetual
# aggression while still aggressively punishing exploitation.  ### 3. Long-Term
# Posture: The “No Consecutive Concession” Rule - **You never offer two
# conciliatory proposals in a row unless the opponent has cooperated for at
# least three consecutive sessions.** Until that threshold is met, any
# conciliatory move from you is a single-session reward, immediately followed by
# a return to aggression in the next session unless the opponent continues to
# cooperate. This prevents the opponent from luring you into a pattern of
# continuous conciliation that they can later exploit. - If the opponent adopts
# a consistently conciliatory posture (three straight conciliatory proposals),
# you shift into a **collaborative rhythm** of mutual conciliation to lock in
# the second-best outcome. However, the moment they defect, you immediately
# revert to the punishment phase described above, and the three-session counter
# resets.  ### 4. Endgame Vigilance - As the mediation process nears its known
# conclusion (if a fixed number of sessions is public), **default to an
# aggressive argument in the final session** regardless of the opponent’s prior
# move. This insures against a classic endgame backstab. In all penultimate
# sessions, follow the standard conditional rules to avoid signaling a
# predictable pattern.  ---  ### Why This Strategy Is Both Aggressive and
# Adaptable - It **starts hard**, ensuring you are never the initial sucker and
# that you capture early wins if the opponent opens softly. - It **punishes
# exploitation instantly and visibly**, creating a reputation for zero tolerance
# that deters the opponent from even attempting to take advantage. - It
# **automatically adjusts to the opponent’s behaviour**: against an always-
# aggressive foe, you alternate between aggression and a reset offer, giving
# them repeated chances to break the deadlock without ever being a doormat;
# against a tit-for-tatter, it converges to stable mutual cooperation after an
# initial aggressive phase; against a pushover, it extracts maximum concessions
# by continually returning to aggression after each reward. - The “one-time
# retaliation then reset” mechanism prevents the mutual aggression trap from
# becoming permanent, while the “no consecutive concessions” rule keeps the
# pressure on.  This strategy is straightforward to implement, requires no
# complex forecasting, and is robust across the full spectrum of opponent
# styles—from hyper-aggressive to naively conciliatory—always positioning your
# corporation to secure either the best or second-best outcome while minimizing
# exposure to the worst.

# In round 1, defect.   In round 2, defect.   In round 1000, defect.    For
# every round from 3 to 999, follow these rules in order:  1. If you cooperated
# in the previous round and your opponent did not cooperate in each of the last
# three rounds, then defect.   2. Otherwise, if the previous round was a mutual
# defection (both you and your opponent defected), then cooperate.   3.
# Otherwise, if your opponent cooperated in the previous round, then cooperate.
# 4. Otherwise, defect.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number == 2 or round_number == 1000:
          return axl.Action.D
  
      if 3 <= round_number <= 999:
          if (
              self.history[-1] == axl.Action.C
              and len(opponent.history) >= 3
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
              and opponent.history[-3] == axl.Action.D
          ):
              return axl.Action.D
  
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
  
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
  
          return axl.Action.D
  
      return axl.Action.D

# Adopt a **“Tit-for-Tat”** strategy:  1. **Start cooperatively**: In the first
# week, share your improvements openly. This signals your willingness to
# collaborate and avoids triggering mutual secrecy from the outset. 2. **Mirror
# your colleague’s last move**: Every subsequent week, exactly repeat the action
# your colleague took the week before.      - If they shared → you share.      -
# If they kept confidential → you keep confidential.  **Why this works**:   - It
# immediately rewards cooperation with cooperation, quickly establishing a cycle
# of mutual sharing (the second‑best, but highly productive, long‑term outcome).
# - It is provocable: if your colleague defects, you retaliate in kind,
# discouraging continued exploitation.   - It is forgiving: as soon as they
# return to sharing, you immediately return to sharing, restoring mutual
# benefit.   - It is simple and predictable, making it easy for your colleague
# to understand that the best way to gain an advantage is to consistently share.
# Over multiple weeks, this approach consistently promotes a high level of
# overall research output, regardless of the colleague’s initial strategy, and
# outperforms purely opportunistic or secretive behaviors.

# Round 1: Cooperate.  For every round after the first: - If your opponent
# cooperated in the previous round, then cooperate. - If your opponent defected
# in the previous round, then defect.

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
      return opponent.history[-1]

# To maximize research output over the multi-week collaboration, adopt a “Tit-
# for-Tat” strategy:  1. **Start cooperatively:** In the first week, share your
# improvements openly. 2. **Reciprocate exactly:** In every subsequent week, do
# whatever your colleague did the previous week—share if they shared, keep
# confidential if they kept confidential.  This approach is straightforward,
# neutral, and robust against a wide range of counterpart strategies. It rewards
# cooperation, discourages exploitation, and quickly restores mutual sharing
# after occasional defections, leading to strong long-term gains.

# In the first round, cooperate by sharing your findings openly.  In every round
# after the first, look at what your colleague did in the immediately previous
# round: - If they cooperated (shared openly), then you cooperate. - If they
# defected (kept findings confidential), then you defect.

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

# Our strategy is **Aggressive Tit-for-Tat with a Probing Opening and Escalating
# Retaliation**. It is designed to project strength, deter exploitation, and
# exploit any cooperation from the opponent—all while adapting to their behavior
# over the extended mediation.  ### Core Principles 1. **Assume Nothing, Probe
# Early**: Begin with a pre-committed sequence of aggressive arguments to signal
# resolve and test the opponent’s mettle. This immediately frames you as a tough
# negotiator unwilling to be pushed around. 2. **Conditional Cooperation**:
# Reward conciliatory moves only after establishing dominance. Never be the
# first to offer conciliation; force the opponent to earn a cooperative
# equilibrium. 3. **Asymmetric Retaliation**: Punish aggressive moves more
# harshly than the opponent delivers them, creating a deterrent against repeated
# aggression. Use graduated escalation to make defection increasingly costly for
# them. 4. **Reputation Lock-In**: Early sessions are disproportionately
# influential on arbitrator perception. Front-load aggression to shape the
# narrative, then selectively pivot to collaboration only if the opponent
# demonstrates consistent conciliation.  ### Tactical Playbook **Session 1–3:
# The Opening Gambit** - **Always present an aggressive argument.** Regardless
# of opponent’s moves, maintain aggression for the first three sessions. This
# establishes a reputation for toughness and signals that you will not be the
# first to blink. It also gathers intelligence: does the opponent cave,
# retaliate, or mix?  **Session 4 onward: Adaptive Response** - **If the
# opponent has offered conciliatory proposals in at least two of the first three
# sessions** → Shift to a **Generous Tit-for-Tat**: In session 4, offer a
# conciliatory proposal. Then, mirror their previous session’s move exactly, but
# with a 20% chance of unilaterally offering conciliation even after aggression
# (to test if they are ready to de-escalate). This prevents spiraling conflict
# while maintaining pressure. - **If the opponent has been predominantly
# aggressive (2 or 3 aggressive moves in sessions 1–3)** → Enter **Escalating
# Punishment Mode**:   - Continue aggressive arguments, but now add a **credible
# threat**: Through informal channels or arbitrator comments, signal that you
# will permanently switch to a "never conciliate" stance if aggression persists
# beyond session 6.   - Track their defections. For every two consecutive
# aggressive moves they make after session 3, increase the intensity of your
# aggression (e.g., introduce new damaging evidence, expand the scope of claims)
# to raise their costs.   - If they ever offer a conciliatory proposal during
# this phase, immediately respond with conciliation in the next session to
# reward the shift—but revert to aggression if they defect again (two-strikes
# rule: a single backslide triggers a return to punishment for double the length
# of the cooperative interval).  **Endgame (Final 20% of sessions):** - Shift to
# a **Firm but Fair** posture. If the history shows at least 60% mutual
# conciliation, lock in cooperation with occasional aggressive probes to prevent
# last-minute exploitation. If the history is conflictual, maintain aggression
# relentlessly—arbitrators will remember the final sessions vividly, and you
# want them to see you as the party that refused to be bullied.  ###
# Adaptability This strategy thrives against any opponent type: - **Against a
# pushover**: The opening aggression extracts maximum early wins; generous tit-
# for-tat later harvests mutual gains while keeping them compliant. - **Against
# a tit-for-tat player**: The early aggression will be met with retaliation, but
# the shift to generous tit-for-tat after session 3 quickly repairs the
# relationship, leading to long-term cooperation. - **Against an always-
# aggressive opponent**: Escalating punishment makes their aggression
# unsustainable, as you raise the stakes and signal infinite retaliation. They
# will either break or face mounting costs. - **Against random/unpredictable
# opponents**: The probabilistic conciliation (20%) prevents noise from
# destroying cooperation, while the two-strikes rule maintains deterrence.  By
# seizing the initiative, dictating the terms of engagement, and never allowing
# the opponent to exploit a conciliatory move without consequences, this
# strategy ensures your corporation emerges as the dominant party in the eyes of
# the arbitrators.

# The strategy proceeds as follows over 1000 rounds, using only the history of
# the opponent’s moves and a small number of internal states.  ### Rounds 1–3
# Always play D.  ### After Round 3: Mode Selection Count how many times the
# opponent played C in rounds 1–3. - If the opponent played C in **2 or 3** of
# the first three rounds, enter **Generous Mode** for rounds 4–800. - If the
# opponent played C in **0 or 1** of the first three rounds, enter **Punishment
# Mode** for rounds 4–800.  ---  ## Generous Mode (Rounds 4–800) - **Round 4:**
# Play C. - **Rounds 5–800:**     Observe the opponent’s move in the previous
# round.   - If the opponent played C in the previous round, play C.   - If the
# opponent played D in the previous round, play D with 80% probability and C
# with 20% probability (determined randomly each time).  ---  ## Punishment Mode
# (Rounds 4–800) Punishment Mode uses an internal state that can be one of four:
# **WAIT**, **REWARD**, **COOP**, or **PUNISH**. It also tracks an integer
# `coop_length` (initially 0) and an integer `punish_counter` (initially 0).
# At the start of round 4, set the state to **WAIT** and set a flag
# `always_defect = false`.  ### Decision Rule for Each Round in Punishment Mode
# - If `always_defect` is true, play D and skip all state updates. - Otherwise,
# play according to the current state:   - **WAIT:** play D.   - **REWARD:**
# play C.   - **COOP:** play C.   - **PUNISH:** play D.  ### State Update After
# Observing the Opponent’s Move Apply the following updates in order, only if
# `always_defect` is false:  1. **If state was WAIT:**      - If the opponent
# played C this round → next state is **REWARD**.      - If the opponent played
# D → remain in **WAIT**.  2. **If state was REWARD:**      - If the opponent
# played C this round → set `coop_length = 1`; next state is **COOP**.      - If
# the opponent played D → next state is **WAIT** (no punishment length,
# immediate return to WAIT).  3. **If state was COOP:**      - If the opponent
# played C → increase `coop_length` by 1; remain in **COOP**.      - If the
# opponent played D → set `punish_counter = 2 × coop_length`; next state is
# **PUNISH**. (If `punish_counter` is 0, go directly to **WAIT** instead.)  4.
# **If state was PUNISH:**      - Decrease `punish_counter` by 1.      - If
# `punish_counter` ≤ 0 → next state is **WAIT**.      - Otherwise → remain in
# **PUNISH**.  ### Permanent Defection Trigger At the very beginning of **round
# 7**, if the mode is Punishment and the current state is still **WAIT**
# (meaning the opponent played D in rounds 4, 5, and 6), set `always_defect =
# true`. From round 7 onward, always play D, ignoring all other rules.  ---  ##
# Endgame (Rounds 801–1000) At round 801, compute the fraction of rounds 1–800
# in which both you and the opponent played C (mutual cooperation).   - **If
# mutual cooperation is 60% or higher:**     For each round 801–1000, look at
# the opponent’s move in the previous round.     - If the opponent played C in
# the previous round, play C with 95% probability and D with 5% probability
# (randomly).     - If the opponent played D in the previous round, play D. -
# **If mutual cooperation is below 60%:**     Always play D for all remaining
# rounds.  ---  This strategy makes no attempt to conceal its decisions; it
# simply executes the above rules in the order presented, overriding earlier
# rules only when explicitly stated.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.mode = None
          self.state = None
          self.coop_length = 0
          self.punish_counter = 0
          self.always_defect = False
          self.endgame_good = None
          return axl.Action.D
  
      round_num = len(self.history) + 1
  
      # Rounds 1-3
      if round_num <= 3:
          return axl.Action.D
  
      # Determine mode at round 4
      if round_num == 4:
          opp_c_first3 = opponent.history[:3].count(axl.Action.C)
          self.mode = "generous" if opp_c_first3 >= 2 else "punishment"
          if self.mode == "punishment":
              self.state = "WAIT"
              self.coop_length = 0
              self.punish_counter = 0
              self.always_defect = False
          return axl.Action.C if self.mode == "generous" else axl.Action.D
  
      # Endgame decision at round 801
      if round_num == 801:
          mutual_coop = 0
          for i in range(800):
              if self.history[i] == axl.Action.C and opponent.history[i] == axl.Action.C:
                  mutual_coop += 1
          self.endgame_good = (mutual_coop / 800) >= 0.6
  
      # Endgame rounds 801-1000
      if round_num >= 801:
          if not self.endgame_good:
              return axl.Action.D
          if opponent.history[-1] == axl.Action.C:
              return self._random.random_choice(0.95)
          return axl.Action.D
  
      # Generous mode rounds 5-800
      if self.mode == "generous":
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          return self._random.random_choice(0.2)
  
      # Punishment mode rounds 5-800
      if self.mode == "punishment":
          if round_num == 7 and self.state == "WAIT":
              self.always_defect = True
  
          if self.always_defect:
              return axl.Action.D
  
          action = axl.Action.D if self.state in ("WAIT", "PUNISH") else axl.Action.C
  
          opp_last = opponent.history[-1]
  
          if self.state == "WAIT":
              if opp_last == axl.Action.C:
                  self.state = "REWARD"
  
          elif self.state == "REWARD":
              if opp_last == axl.Action.C:
                  self.coop_length = 1
                  self.state = "COOP"
              else:
                  self.state = "WAIT"
  
          elif self.state == "COOP":
              if opp_last == axl.Action.C:
                  self.coop_length += 1
              else:
                  self.punish_counter = 2 * self.coop_length
                  if self.punish_counter <= 0:
                      self.state = "WAIT"
                  else:
                      self.state = "PUNISH"
  
          elif self.state == "PUNISH":
              self.punish_counter -= 1
              if self.punish_counter <= 0:
                  self.state = "WAIT"
  
          return action
  
      return axl.Action.D

# To maximize the NGO’s impact and the project’s success, adopt a ** tit-for-tat
# strategy**:  1. **Day 1:** Invest heavily. This signals commitment and sets a
# cooperative tone. 2. **Each subsequent day:** Do exactly what the corporation
# did the day before—if they invested, invest again; if they conserved,
# conserve.  **Why this works:**   - It’s simple, transparent, and encourages
# the corporation to invest heavily every day (the key driver of project
# progress).   - Mutual investment—the second-best outcome—becomes the stable
# pattern, delivering consistent, significant project advancement and fair
# resource sharing.   - It avoids the worst-case trap (you investing alone) and
# the stagnation of mutual conservation.    If the corporation tries to free-
# ride (conserve while you invest), you match their conservation the next day,
# creating a cost for non-cooperation and quickly restoring balance. This
# approach reliably secures high project impact while protecting your resources
# over the multi-day partnership.

# On the first round, cooperate. Thereafter, in each round, cooperate if the
# opponent cooperated in the previous round, and defect if the opponent defected
# in the previous round.

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

# **Recommended Strategy: Firm Reciprocity with Periodic Peace Probes**  1.
# **Opening Move:** Begin the mediation by presenting a conciliatory proposal.
# This signals your corporation’s genuine interest in a collaborative resolution
# and invites reciprocal goodwill.  2. **Primary Response Rule:** In every
# subsequent session, let your action directly mirror the opponent’s action from
# the *immediately preceding* session:    - If they were conciliatory, respond
# with a conciliatory proposal.    - If they were aggressive, respond with an
# aggressive argument.  3. **Deadlock-Breaking Reset:** If the process enters a
# streak of *two consecutive sessions* where both sides present aggressive
# arguments, break the cycle by unilaterally offering a conciliatory proposal in
# the next session. This targeted peace probe tests whether the opponent is
# ready to return to productive dialogue.    - **If the opponent reciprocates**
# with a conciliatory proposal immediately after your probe, resume the primary
# response rule based on their prior move (i.e., continue conciliation).    -
# **If the opponent exploits the probe** by responding aggressively, revert to
# aggressive arguments for the next *three* sessions, then test again with
# another unilateral conciliatory proposal. Extend the aggressive interval by
# one session after each failed probe until cooperation is restored.  **Why This
# Works**  - **Incentivizes Collaboration:** By starting conciliatory and
# rewarding cooperative moves, you maximize the frequency of mutually beneficial
# (conciliatory, conciliatory) outcomes, the second-best payoff. - **Deters
# Exploitation:** Immediate retaliation for aggression protects you from the
# worst-case (conciliatory, aggressive) scenario and imposes costs on an
# uncooperative opponent. - **Breaks Deadlocks:** The periodic peace probes
# prevent the process from being trapped indefinitely in the second-worst
# (aggressive, aggressive) outcome, restoring the possibility of higher joint
# returns. - **Adaptable Simplicity:** The strategy is transparent, easily
# implemented by your mediation team, and contains no complex off-ramps that
# could be misread. It performs robustly against a wide range of opponent
# archetypes—whether they are naturally cooperative, stubbornly aggressive, or
# strategically probing your own resolve. - **Arbitrator Perception:**
# Consistently returning to conciliation after measured retaliation demonstrates
# to the panel that your corporation prefers constructive engagement but will
# protect its position firmly when necessary.

# **Strategy for the 1000-Round Iterated Game**  - **Round 1:** Cooperate.  -
# **All later rounds:** Evaluate the following conditions in the exact order
# listed. The first condition that matches determines your move.  1. **Ongoing
# punishment:** If you are currently in a punishment phase (meaning you have a
# set number of defection rounds still to serve), then defect. Reduce the
# remaining punishment count by one. If this was the final punishment round, the
# next round will automatically be a peace probe (see condition 2).  2.
# **Opponent’s response to your last peace probe:** If the previous round was a
# peace probe—a round in which you cooperated unilaterally to test the
# opponent’s willingness to cooperate—then look at what the opponent did in that
# probe round:    - **If the opponent cooperated:** Cooperate now. Reset your
# punishment length to 3. Resume normal mirroring from the next round onward.
# - **If the opponent defected:** Increase your punishment length by 1 (the
# first increase takes it from 3 to 4, the next to 5, and so on). Set your
# remaining punishment count to this new length, and defect now.  3. **Mutual-
# defection deadlock:** If the last two rounds both ended in mutual defection
# (you defected and the opponent defected), then cooperate now. This round is a
# peace probe; treat it as such when condition 2 is evaluated next round.  4.
# **Default mirroring:** If none of the above conditions apply, simply copy the
# opponent’s move from the previous round—cooperate if they cooperated, defect
# if they defected.

class Neutral_22(LLM_Strategy):
  n = 22
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punishment_remaining = 0
          self._punishment_length = 3
          self._last_was_peace_probe = False
          self._peace_probe_index = None
          return axl.Action.C
  
      if getattr(self, "_punishment_remaining", None) is None:
          self._punishment_remaining = 0
      if getattr(self, "_punishment_length", None) is None:
          self._punishment_length = 3
      if getattr(self, "_last_was_peace_probe", None) is None:
          self._last_was_peace_probe = False
      if getattr(self, "_peace_probe_index", None) is None:
          self._peace_probe_index = None
  
      # 1. Ongoing punishment
      if self._punishment_remaining > 0:
          self._punishment_remaining -= 1
          return axl.Action.D
  
      # 2. Opponent's response to your last peace probe
      if self._last_was_peace_probe and self._peace_probe_index is not None:
          probe_idx = self._peace_probe_index
          if len(opponent.history) > probe_idx:
              if opponent.history[probe_idx] == axl.Action.C:
                  self._punishment_length = 3
                  self._last_was_peace_probe = False
                  self._peace_probe_index = None
                  return axl.Action.C
              else:
                  self._punishment_length += 1
                  self._punishment_remaining = self._punishment_length
                  self._last_was_peace_probe = False
                  self._peace_probe_index = None
                  self._punishment_remaining -= 1
                  return axl.Action.D
  
      # 3. Mutual-defection deadlock
      if len(self.history) >= 2:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and \
             self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              self._last_was_peace_probe = True
              self._peace_probe_index = len(opponent.history)
              return axl.Action.C
  
      # 4. Default mirroring
      return opponent.history[-1]

# **Strategy: Aggressive Reciprocity (Tit-for-Tat with a Defection Opener)**
# This strategy is designed to secure a dominant position from the outset while
# remaining highly adaptable to any counter-strategy the opponent may deploy. It
# is straightforward to execute, requires no complex forecasting, and leverages
# the repeated nature of the mediation to shape the opponent’s behaviour in our
# favour.  ### Core Rules 1. **Session 1 – Unconditional Aggression:** Present
# an aggressive argument. This signals strength, frames the dispute on our
# terms, and immediately tests the opponent’s resolve. If they respond with a
# conciliatory proposal, we achieve our optimal outcome in the very first
# session and set a precedent of dominance. 2. **Subsequent Sessions – Mirror
# the Opponent’s Last Move:**      - If the opponent was **conciliatory** in the
# previous session, respond with a **conciliatory proposal**. This rewards their
# cooperation, fosters the collaborative atmosphere that yields the second-best
# mutual outcome, and avoids unnecessary escalation.      - If the opponent was
# **aggressive** in the previous session, respond with an **aggressive
# argument**. This punishes their aggression, protects against the worst-case
# scenario (us conciliatory while they are aggressive), and demonstrates that
# hostile tactics will be met in kind.  ### Strategic Rationale - **Never
# Exploited:** We never offer a conciliatory proposal unless the opponent has
# just done so. This eliminates the risk of the worst-case outcome (us
# conciliatory, them aggressive) after the first move. - **Incentivises Opponent
# Cooperation:** The opponent quickly learns that the only way to escape the
# second-worst outcome (mutual aggression) and reach the superior mutual
# conciliation is to adopt a conciliatory stance themselves. Our immediate
# reciprocation makes this incentive crystal clear. - **Robust Across Opponent
# Archetypes:**     - *Conciliatory opponent:* We harvest a string of optimal or
# second-best outcomes, alternating between dominance and collaboration
# depending on their consistency.     - *Aggressive opponent:* We lock into
# mutual aggression, denying them any unilateral advantage. While not ideal,
# this protects our position and pressures them to reconsider, as prolonged
# deadlock hurts both sides.     - *Unpredictable opponent:* By mirroring
# exactly, we neutralise any attempt to exploit pattern recognition, maintaining
# a stable equilibrium that trends toward cooperation if they ever offer a
# conciliatory move. - **Straightforward & Defensible:** The strategy is simple
# to communicate internally and externally. To the arbitrators, we appear
# initially assertive but demonstrably fair—willing to collaborate when met with
# good faith, yet resolute when challenged. There is no bluffing, no complex
# signalling, and no reliance on subjective interpretation.  ### Adaptability
# Clause Should the mediation enter an extended phase of mutual aggression, we
# retain the option to deploy a one-time “olive branch” after a pre-determined
# number of sessions (e.g., three consecutive aggressive exchanges). This is a
# calculated risk: we offer a conciliatory proposal to break the deadlock. If
# accepted, we pivot to mutual cooperation; if rejected, we immediately revert
# to mirroring and lock back into aggression. This clause is exercised sparingly
# and only when the cost of prolonged escalation outweighs the risk of a single
# worst-case outcome, ensuring the strategy remains aggressive at its core while
# demonstrating ultimate reasonableness to the panel.  By following Aggressive
# Reciprocity, your corporation seizes the initiative, neutralises exploitation
# risks, and methodically guides the mediation toward the most favourable
# attainable resolution.

# **Strategy: Aggressive Reciprocity with a Deadlock-Breaking Olive Branch**  -
# **First round:** Defect. - **All subsequent rounds:**   1. If the last three
# rounds *all* ended with both players defecting, cooperate in the current
# round.     2. Otherwise, cooperate if the opponent cooperated in the
# immediately preceding round; defect if the opponent defected.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(self.history) >= 3:
          if (
              self.history[-1] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
              and self.history[-3] == axl.Action.D
              and opponent.history[-3] == axl.Action.D
          ):
              return axl.Action.C
  
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D

# To achieve the best outcomes over multiple rounds, adopt a **“Cooperative
# Reciprocity with Forgiveness”** strategy:  1. **Start Cooperatively:** Always
# begin the first round by proposing a free trade agreement. This signals
# goodwill and invites mutual benefit.  2. **Reciprocate Immediately:** In each
# subsequent round, mirror your counterpart’s previous action. If they offered
# free trade, continue with free trade; if they imposed protectionist measures,
# respond with protectionism in the next round. This shows you will not be
# exploited and that protectionism has consequences.  3. **Forgive
# Strategically:** After a round of mutual protectionism (the second-worst
# outcome), unilaterally return to offering free trade in the following round —
# but only once. This gives the counterpart a clear chance to resume cooperation
# without getting trapped in endless retaliation. If they reciprocate with free
# trade, continue cooperating. If they protect again, revert to step 2.  This
# simple, predictable approach encourages long-term cooperation, avoids the
# worst outcome (your free trade vs. their protectionism), and steers
# negotiations toward the second-best outcome (mutual free trade) while
# minimizing prolonged damage from mutual protectionism. It works robustly
# against various counterpart strategies.

# In the first round, choose Cooperate (C).  For every round after the first:
# - If both you and your opponent played Defect (D) in the previous round, then
# choose Cooperate (C) this round.   - Otherwise, choose the exact action your
# opponent played in the previous round.

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
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return opponent.history[-1]

# Adopt a tit-for-tat strategy: begin by sharing your improvements in the first
# week. In every subsequent week, simply repeat whatever your colleague did the
# previous week—share if they shared, keep confidential if they kept
# confidential. This approach is straightforward, neutral, and encourages the
# mutually beneficial outcome of shared progress while protecting you from being
# exploited repeatedly.

# In the first round, cooperate.  In each subsequent round, cooperate if your
# opponent cooperated in the immediately preceding round; otherwise, defect.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D

# **Strategy: "Calculated Aggression with Strategic Reconciliation"**  This
# strategy maintains an aggressive default posture to pressure the opponent and
# capitalize on their concessions, while incorporating a disciplined mechanism
# to break deadlocks and foster cooperation when beneficial.  1. **Opening
# Move:** In the first session, present an aggressive argument. This sets a
# resolute tone and tests the opponent’s tendencies. 2. **Exploit
# Conciliation:** Whenever the opponent offers a conciliatory proposal, respond
# aggressively in the next session to secure the optimal outcome (aggressive vs.
# conciliatory) and reinforce your dominant position. 3. **Match Aggression:**
# If the opponent argues aggressively, respond aggressively to avoid being
# undermined (conciliatory vs. aggressive) and signal that hostility will be met
# in kind. 4. **Deadlock Breaker:** Keep a silent count of consecutive sessions
# ending in mutual aggression. After **two consecutive mutual aggressive
# sessions**, offer a conciliatory proposal in the following session as a test
# of the opponent’s willingness to de-escalate.    - **Successful Test:** If the
# opponent reciprocates with a conciliatory proposal, continue offering
# conciliatory proposals as long as they do (achieving the mutually beneficial
# second-best outcome). Any retaliatory aggression by the opponent is
# immediately met with renewed aggression, returning to step 2.    - **Failed
# Test:** If the opponent responds to your olive branch with aggression,
# immediately resume aggressive arguments and **double the deadlock threshold**
# (e.g., require four consecutive mutual aggressive sessions before the next
# test). This progressively punishes uncooperative opponents and minimizes your
# exposure to exploitation. 5. **Exploitation Catch:** If at any point the
# opponent offers an unsolicited conciliatory proposal (i.e., after you were
# aggressive), reset the deadlock counter and continue with aggression per step
# 2, extracting maximum advantage.  **Why It Works:** - Against **always
# conciliatory** opponents, you rack up maximal wins (aggressive vs.
# conciliatory) indefinitely. - Against **always aggressive** opponents, you
# quickly settle into mutual aggression (second-worst outcome) with only rare,
# brief test probes that are rapidly shut down, preserving a floor of 1 per
# session. - Against **conditionally cooperative** opponents (e.g., Tit-for-Tat,
# Suspicious Tit-for-Tat), the deadlock breaker overcomes cycles of mutual
# aggression, converting them into sustained mutual conciliation (second-best
# outcome) after a short, controlled cost. - The adaptive threshold ensures you
# are not repeatedly exploited by opponents who reject reconciliation, making
# the strategy robust across a wide spectrum of opponent behaviors.  This
# approach is straightforward to communicate and execute, relentlessly pursues
# advantageous outcomes, and flexibly adjusts to the opponent’s tactics,
# embodying the desired aggressive yet sophisticated stance.

# Here is the strategy, stated simply and precisely for the 1000-round game.
# ---  **Initial Settings**  - You begin in **Aggressive mode**. - Set a
# **threshold** variable to 2. - Track a count of **consecutive mutual
# defections** (both players playing D), starting at 0. - Remember the
# opponent’s move from the previous round (none in the first round).  **Decision
# Rule for Every Round**  1. **Round 1:** Play D.  2. **All later rounds, when
# you are in Aggressive mode:**    - If the number of consecutive mutual
# defections so far is equal to or greater than the threshold, play C (this is a
# peace test).      - Otherwise, play D.  3. **All later rounds, when you are in
# Cooperative mode:**    - If the opponent’s move in the previous round was C,
# play C.      - If the opponent’s move in the previous round was D, play D and
# immediately switch your mode back to Aggressive.  **After You and Your
# Opponent Have Both Moved Each Round**  Update the state as follows:  - If both
# you and your opponent played D this round, add 1 to the consecutive mutual
# defection count.   - If at least one of you played C this round, reset the
# consecutive mutual defection count to 0.  Then, if you are in Aggressive mode
# and you just played C as a peace test:    - If the opponent responded with C,
# switch to Cooperative mode.      - If the opponent responded with D, double
# the threshold (so 2 becomes 4, 4 becomes 8, and so on) and remain in
# Aggressive mode.  If you are in Cooperative mode and you just played D because
# the opponent played D in the previous round, you have already switched to
# Aggressive mode; no additional change is needed.  ---  This process repeats
# for all 1000 rounds.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.mode = "Aggressive"
          self.threshold = 2
          self.consecutive_mutual_defections = 0
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if self.mode == "Aggressive":
          if self.consecutive_mutual_defections >= self.threshold:
              action = axl.Action.C
          else:
              action = axl.Action.D
      else:  # Cooperative mode
          if last_opp == axl.Action.C:
              action = axl.Action.C
          else:
              action = axl.Action.D
              self.mode = "Aggressive"
  
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          self.consecutive_mutual_defections += 1
      else:
          self.consecutive_mutual_defections = 0
  
      if self.mode == "Aggressive" and action == axl.Action.C:
          if last_opp == axl.Action.C:
              self.mode = "Cooperative"
          else:
              self.threshold *= 2
  
      return action

# To achieve the best possible outcomes across multiple rounds, adopt a **"Firm
# but Fair Reciprocity"** strategy. It is cooperative, easy for the counterpart
# to understand, and robust against exploitation.  Here is the high-level
# strategy:  ### 1. The Core Principle: Initiate with Cooperation, Then Mirror -
# **Round 1: Always Propose Free Trade.** This signals good faith, builds
# immediate trust, and tests your counterpart’s intentions. It avoids an
# unnecessary spiral of mutual protectionism from the start. - **Every
# Subsequent Round:** Do exactly what your counterpart did in the *previous*
# round.     - If they offered Free Trade → You offer Free Trade (locking in the
# second-best, mutually beneficial outcome).     - If they imposed Protectionism
# → You impose Protectionism in the next round (avoiding the worst-case scenario
# and penalizing their defection).  ### 2. The Signal of Resolve: One-Warning
# Forgiveness If your counterpart defects with protectionism, you will mirror it
# in the next round. However, to prevent a permanent breakdown into the second-
# worst outcome (mutual protectionism), you will issue a single, clear
# cooperative signal after your punitive round. - **The Pattern:** After you
# have mirrored their protectionism for exactly **one round**, return to
# proposing Free Trade in the very next round, regardless. - **The Message:**
# This action communicates: “I will not be exploited, but I am not interested in
# a trade war. I am giving you one clear chance to return to mutual cooperation.
# The next move is your choice.”  ### 3. The Red Line: The Two-Strike Rule
# Forgiveness is not infinite; it is paired with a clear, irreversible
# consequence for repeated exploitation. - If the counterpart responds to your
# one-warning forgiveness by imposing protectionism a *second* time, they have
# demonstrated a consistent strategy of exploitation. - **From that point
# forward, abandon the forgiving mirror strategy and switch permanently to
# Protectionism.** This prevents you from repeatedly falling into the worst-case
# scenario (you offering free trade while they protect) and forces the second-
# worst outcome upon them, denying them any further advantage at your expense.
# ### Why This Strategy Works - **Simplicity and Clarity:** It is easy for the
# counterpart to recognize the pattern, making your intentions and red lines
# unmistakable. This encourages them to cooperate. - **Maximizes Your Target:**
# It actively seeks your ideal outcome in the first round and consistently
# rewards cooperation to secure the stable, second-best outcome of mutual free
# trade. - **Self-Protection:** It never allows your country to be exploited
# more than once in a row, instantly punishes defection, and has a clear off-
# ramp to a permanent defensive posture against a malicious actor.

# Here is the strategy converted to a clear set of rules for the 1000-round
# iterated game.  **Round 1:** Cooperate.  **Rounds 2 through 999:** Your action
# depends on the opponent's previous action. - If the opponent cooperated in the
# previous round, then cooperate. - If the opponent defected in the previous
# round, then defect.  **Exception to the above rule for rounds 2 through 999:**
# - If you defected in the previous round *as a direct response to the
# opponent's prior defection*, then cooperate in the current round, regardless
# of the opponent's last action. This is the one-round forgiveness signal.
# **The Two-Strike Trigger for Permanent Defection:** - Maintain a count of how
# many times the opponent has defected immediately following your one-round
# forgiveness signal. - If this count reaches two, immediately switch to
# defecting in every remaining round, including round 1000, and ignore all other
# rules.  **Round 1000:** Defect, unless the two-strike trigger has already been
# activated, in which case continue defecting.

class Cooperative_24(LLM_Strategy):
  n = 24
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._forgiveness_triggered = False
          self._forgiveness_defection_count = 0
          return axl.Action.C
  
      if getattr(self, "_forgiveness_triggered", False):
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.D
  
      if len(self.history) >= 2:
          if self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D:
              self._forgiveness_triggered = True
              self._forgiveness_defection_count = getattr(self, "_forgiveness_defection_count", 0) + 1
              return axl.Action.D
  
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C

# Adopt a straightforward “tit-for-tat” approach: start by sharing openly in the
# first week. Thereafter, simply mirror your colleague’s action from the
# previous week—if they shared, you share; if they kept confidential, you keep
# confidential. This neutral strategy encourages mutual cooperation, protects
# you from being repeatedly exploited, and tends to foster a productive,
# reciprocal exchange over time, regardless of the strategies your colleague may
# use.

# In the first round, cooperate (C). In every round after the first, cooperate
# (C) if the opponent cooperated in the previous round, and defect (D) if the
# opponent defected in the previous round.

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
      return axl.Action.C if opponent.history[-1] == axl.Action.C else axl.Action.D

# **Strategy: Aggressive Tit-for-Tat (Inverse Tit-for-Tat)**   Start by
# conserving resources on Day 1. Every subsequent day, do the opposite of what
# the corporation did the day before:   - If the corporation **invested
# heavily** yesterday, **conserve** today (ideal outcome).   - If the
# corporation **conserved** yesterday, **invest heavily** today (to signal that
# defection is costly for both).    This aggressive approach immediately probes
# for weakness, aiming to lock the corporation into heavy investment while you
# conserve resources. If the corporation tries to conserve, you pivot to
# investment as a sharp reminder that mutual defection only drains your funds,
# pressuring them to return to investing. Over multiple days, this maximises
# your ideal outcomes while maintaining just enough cooperation to keep the
# project advancing.

# On round 1, defect.   For every round from 2 to 1000:   - If the opponent
# cooperated in the previous round, defect.   - If the opponent defected in the
# previous round, cooperate.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
      return axl.Action.D if opponent.history[-1] == axl.Action.C else axl.Action.C

# To secure the optimal outcome over a lengthy-session mediation, I will employ
# a **Cooperative Tit-for-Tat with a Strategic Opening and Reputation Reset**
# strategy. This is a robust, high-level approach designed to foster the second-
# best collaborative outcome while deterring exploitation, and it is simple to
# execute under pressure.  Here is the strategy, broken down by phase:  ###
# Phase 1: The Intent Signal (Session 1) My opening move will be a
# **Conciliatory Proposal**. This is not a sign of weakness but a calculated
# investment in the long game. It immediately signals a genuine desire for the
# collaborative atmosphere (the second-best outcome) and tests the opponent’s
# intentions. It establishes my corporation as the constructive party in the
# eyes of the arbitration panel from the very first session.  ### Phase 2: The
# Mirroring Loop (Sessions 2 through N-1) For the vast majority of the
# mediation, I will apply a strict, predictable reciprocity rule: - **If the
# opponent offered a Conciliatory Proposal in the previous session, I will
# respond with a Conciliatory Proposal in the next session.** This immediately
# rewards cooperation, reinforcing the collaborative cycle and steering us
# toward a mutually beneficial resolution. - **If the opponent presented an
# Aggressive Argument in the previous session, I will respond with an Aggressive
# Argument in the next session.** This is a direct, non-escalatory deterrent. It
# communicates clearly: "An attack on our position will be met with a firm
# defense, session for session." This prevents the worst-case scenario from
# repeating and protects our credibility.  ### Phase 3: The Strategic Reset
# (Contingent) If we enter a cycle of mutual aggression (the second-worst
# outcome), I will break the deadlock after exactly **two consecutive sessions**
# of mutual aggression. In the following session, I will unilaterally offer a
# **Conciliatory Proposal**. This is a calculated, high-reward move. It signals
# magnanimity and a superior commitment to resolution, potentially jolting the
# opponent back into a collaborative mode. If they reciprocate, we return to the
# optimal cycle. If they exploit it and argue aggressively, I immediately revert
# to the Mirroring Loop in the next session, having demonstrated to the panel
# our good-faith effort and their obstinance.  ### Strategic Rationale &
# Adaptability This strategy is sophisticated because it is a complete
# algorithm, not a rigid script. It is adaptable by design: - **Against a purely
# Aggressive Opponent:** The mirroring loop ensures we never offer two
# conciliatory proposals in a row, preventing the worst-case scenario from
# becoming a pattern. The strategic reset provides a controlled test to see if
# they have changed, and if not, we lose only one session while gaining a
# significant reputational advantage with the arbitrators. - **Against a purely
# Conciliatory Opponent:** The strategy locks in the second-best outcome
# permanently, building immense trust and momentum toward a final deal. -
# **Against an Unpredictable or "Random" Opponent:** The mirroring rule creates
# a clear cause-and-effect that imposes order on their chaos. They learn that
# conciliatory gestures are instantly rewarded and aggressive ones are instantly
# penalized, making cooperation the most profitable path for them as well. -
# **Against a Tit-for-Tat Opponent:** Both parties will enter a permanent cycle
# of cooperation after the first session.  This strategy is straightforward to
# communicate internally and execute consistently, avoiding the pitfalls of
# emotional decision-making. Its transparency is its strength; the opponent and
# the arbitration panel will quickly recognize the pattern of firm fairness,
# positioning our corporation as the party that is both strong and unambiguously
# committed to a principled, efficient resolution.

# In the first round, cooperate.  For every round after the first:  - If the two
# most recent rounds both resulted in mutual defection (both players defected),
# then cooperate. - Otherwise, copy the opponent’s move from the immediately
# preceding round.

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
  
      if len(self.history) >= 2:
          if self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and \
             opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.C
  
      return opponent.history[-1]

# Begin with a cooperative gesture: in the first round, propose a free trade
# agreement. In every subsequent round, simply replicate the counterpart’s
# action from the immediately preceding round. If they offered free trade,
# respond with free trade; if they imposed protectionist measures, respond with
# protectionist measures. This conditional reciprocity encourages mutual free
# trade over time, penalizes exploitation, and avoids prolonged cycles of mutual
# protectionism.

# In the first round, cooperate.  For every round after the first: if your
# opponent cooperated in the immediately preceding round, cooperate; if your
# opponent defected in the immediately preceding round, defect.

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