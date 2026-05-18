import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy

# To maximise your research output in this multi-week collaboration, you need a
# strategy that aggressively prioritises your advantage (keeping your findings
# while they share) but is smart enough to avoid permanent stalemates (both
# keeping) and account for technical errors.   Here is a high-level,
# straightforward, aggressive strategy—similar to a "Forgiving Exploiter"
# approach—designed to dominate the collaboration:  **1. Default to
# Confidentiality** Always start the collaboration by keeping your findings
# confidential, and maintain this stance as your baseline. This protects you
# from the worst-case scenario (being exploited) and immediately tests whether
# your colleague is willing to share unilaterally.   **2. Exploit Openness
# Relentlessly** If you keep your findings and your colleague shares theirs, you
# achieve your ideal outcome. Do not reciprocate out of fairness. Continue
# keeping your findings confidential as long as they continue to share. Your
# goal is to maximise your advantage, not to foster mutual progress.  **3. Apply
# a "Noise Buffer" (The One-Strike Rule)** Because technical issues can cause
# communication breakdowns, do not overreact to a single week of your colleague
# keeping their findings. If they suddenly keep their data after a streak of
# sharing, assume it was a technical error. Continue keeping your findings for
# that week without changing your approach. This prevents you from accidentally
# triggering a permanent retaliation loop caused by a simple glitch.  **4.
# Concede to Break Deadlocks** If your colleague keeps their findings for **two
# consecutive weeks**, assume they are intentionally retaliating or playing
# defensively, and you are now stuck in the second-worst outcome (mutual
# confidentiality). To break the stalemate, share your findings in the next
# week. This acts as a reset signal, proving you are willing to cooperate and
# testing their willingness to reciprocate.  **5. Re-exploit Immediately** If
# your concession prompts your colleague to share their findings again,
# immediately revert to keeping your findings confidential the following week.
# This attempts to re-establish the dominant dynamic where you exploit their
# openness. If they continue to keep their findings even after your concession,
# revert to keeping yours as well to minimise your losses.  **Summary of the
# Strategy:** *Keep your findings by default. Exploit any openness without
# reciprocating. Tolerate one week of confidentiality from them (noise buffer).
# If they keep findings for two weeks straight, share once to reset the dynamic,
# then immediately go back to keeping your findings to exploit them again.*

# 1. Play D in the first round. 2. In any subsequent round, if you played C in
# the previous round, play D. 3. Otherwise, if the opponent played D in both of
# the previous two rounds, and the opponent played C in the round immediately
# prior to those two rounds, play C. 4. Otherwise, play D.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(opponent.history) >= 3:
          if (
              opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
              and opponent.history[-3] == axl.Action.C
          ):
              return axl.Action.C
  
      return axl.Action.D

# To maximize our research output over a multi-week collaboration while
# protecting your competitive standing and accounting for technical glitches,
# the most effective strategy is a **Generous Tit-for-Tat** approach.   This
# strategy is straightforward, cooperative, and highly resilient to both
# uncooperative behavior and technical noise (like data corruption). Here is how
# it works:  **1. Start Cooperatively (Week 1)** Begin the collaboration by
# openly sharing your latest improvements. This sets a collaborative baseline
# and signals to your colleague that you are committed to mutual progress.
# **2. Reciprocate the Previous Week's Action (Weeks 2 onwards)** In any given
# week, mirror your colleague's action from the previous week: *   If they
# shared openly last week, you share openly this week. *   If they kept their
# findings confidential last week, you keep yours confidential this week. This
# protects you from sustained exploitation. If your colleague chooses to keep
# secrets, you do the same, ensuring you are never left at a consistent
# disadvantage.  **3. Build in "Forgiveness" to Overcome Technical Noise** This
# is the critical adjustment for potential technical issues. Because data
# corruption or communication breakdowns can make an intended "share" look like
# a "keep confidential," strict reciprocation can accidentally trigger a cycle
# of mutual secrecy.   To prevent this, add a forgiveness rule: **Occasionally
# (about 10% to 20% of the time), choose to share openly even if your colleague
# kept their findings confidential the previous week.**  *   *Why?* If their
# failure to share was due to a crashed server or corrupted file, your
# forgiveness resets the relationship to mutual sharing. If they were genuinely
# trying to exploit you, a single forgiven share only costs you a minor, one-
# week disadvantage, which is a low risk compared to the high cost of entering a
# permanent deadlock of mutual secrecy.  **4. Respond to Sustained
# Exploitation** If your colleague keeps their findings confidential for two or
# three consecutive weeks despite your forgiving gestures, assume they are
# intentionally playing an exploitative strategy. At this point, suspend the
# forgiveness rule and strictly mirror their actions (keep confidential) until
# they make a clear, unforced move to share openly again.  **Summary of the
# Strategy:** *Share first, then do what they did last week. But occasionally,
# be the bigger person and share even if they didn't, just in case a technical
# glitch was to blame. If they repeatedly take advantage of your openness, match
# their secrecy until they choose to cooperate again.*  This strategy maximizes
# your overall research output by heavily favoring the "both share" outcome,
# while ensuring you are never left vulnerable to sustained exploitation and are
# resilient to accidental communication failures.

# 1. In the first round, play C. 2. If the opponent's observed action in the
# previous round was C, play C. 3. If the opponent's observed action in the
# previous round was D, and the opponent's observed action two rounds ago was
# also D, play D. 4. If the opponent's observed action in the previous round was
# D, and the opponent's observed action two rounds ago was C (or if it is
# currently the second round), play C with a 15% probability and play D with an
# 85% probability.

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
  
      if len(opponent.history) >= 1:
          last_opp = opponent.history[-1]
          if last_opp == axl.Action.C:
              return axl.Action.C
  
          if len(opponent.history) >= 2:
              two_ago_opp = opponent.history[-2]
              if two_ago_opp == axl.Action.D:
                  return axl.Action.D
              else:
                  return self._random.random_choice(0.15)
          else:
              return self._random.random_choice(0.15)
  
      return axl.Action.C

# To navigate this high-stakes, iterative mediation effectively, we must employ
# a strategy rooted in **Graduated Reciprocity**. This approach—a refined
# version of the game-theory concept "Tit-for-Tat with Forgiveness"—is
# specifically calibrated to the payoff structure you’ve outlined. It maximizes
# our chances of achieving the optimal outcome (Aggressive vs. Conciliatory),
# secures the second-best outcome (Conciliatory vs. Conciliatory) as a durable
# baseline, and insulates us from the worst-case scenario (Conciliatory vs.
# Aggressive), while accounting for the "noise" of arbitrator misinterpretation
# and procedural breakdowns.  Here is the high-level, adaptable strategy for the
# mediation sessions:  ### 1. The Opening Move: Establish the Baseline of Reason
# **Rule:** Always open the first session with a **Conciliatory Proposal**.
# *Rationale:* A conciliatory opening establishes our corporation as the
# reasonable, good-faith actor in the eyes of the arbitrators. If the opponent
# opens aggressively, we achieve our second-worst outcome (A/A), but the
# opponent appears hostile, losing goodwill. If the opponent opens conciliatory,
# we secure our second-best outcome (C/C) and build a collaborative foundation.
# We never risk the worst-case scenario (C/A) on the first move, as an
# unprovoked aggressive stance from the opponent against our conciliatory one
# makes them look unreasonable, mitigating the damage to our position.  ### 2.
# Dynamic Adaptation: The Proportional Response Framework After the first
# session, our strategy must strictly mirror the opponent’s prior behavior, but
# with a graduated scale to avoid overreactions.  *   **If the opponent’s prior
# move was Conciliatory:** Respond with a **Conciliatory Proposal**. This
# sustains the mutually beneficial C/C equilibrium, which is our durable second-
# best outcome and preserves corporate resources. *   **If the opponent’s prior
# move was Aggressive:** Respond with an **Aggressive Argument**. This prevents
# the worst-case scenario (us offering conciliation in the face of aggression).
# By matching aggression with aggression, we shift the dynamic to A/A (our
# second-worst outcome), but we protect our底线 (bottom line).  *   **The "Pivot
# to Optimal":** If we have established a pattern of matching their aggression
# (A/A), and the opponent shows signs of fatigue or seeks de-escalation by
# offering a conciliatory proposal, we do *not* immediately match it with
# conciliation. Instead, we present one final **Aggressive Argument** against
# their conciliatory proposal. This creates a fleeting A/C dynamic—our optimal
# outcome—squeezing out a maximum advantage before we pivot back to conciliation
# in the following session to close the deal.  ### 3. Managing Noise: Strategic
# Forbearance and Clarification Because arbitrators may misrepresent or
# misunderstand our intended strategy, we cannot rely solely on the panel's
# perception of the opponent's last move. We must account for "noise."  *
# **The Rule of Strategic Forbearance (Forgiveness):** If we perceive the
# opponent as having been aggressively non-compliant in the previous session,
# but there is a reasonable chance it was due to a procedural irregularity or
# arbitrator misinterpretation, we offer **one instance of undeserved
# conciliation**. If the opponent is genuinely trying to cooperate but was
# misinterpreted, this restores the C/C dynamic. If they take advantage of our
# conciliation (confirming they are acting intentionally aggressively), we
# immediately revert to a sustained Aggressive posture. *   **Explicit
# Framing:** To prevent our own conciliatory proposals from being misunderstood
# as weakness or our aggressive arguments as bad faith, we must explicitly frame
# our moves to the panel. *Example:* "We are presenting this conciliatory
# proposal as a test of mutual good faith," or "Given the aggressive posture
# taken by opposing counsel in the last session, we are compelled to present an
# aggressive defense of our position today." This leaves no room for arbitrator
# misinterpretation of our intent.  ### 4. Contingencies: Procedural
# Irregularities and Breakdowns In the event of communication breakdowns or
# procedural irregularities (e.g., a session is cut short, documents are
# withheld, or the panel changes):  *   **Default to Aggressive:** When the
# procedural ground is unstable, do not expose the corporation to the worst-case
# scenario (C/A). If we cannot trust the process, we must protect our position
# aggressively until the procedural norms are restored. *   **Demand Procedural
# Reset:** If a breakdown occurs, halt the substantive strategy and aggressively
# litigate the procedural issue to the panel. Do not resume the Graduated
# Reciprocity framework until the arbitrators confirm a return to standard
# procedural order.  ### 5. Endgame Management As the mediation sessions draw to
# a close, the incentive for the opponent to defect (shift to Aggression)
# increases, as there are fewer future sessions to suffer retaliation.  *
# **Countermeasure:** In the final three sessions, gradually shift our baseline
# from purely reactive to slightly more aggressive, regardless of their prior
# move, while publicly signaling to the panel that we are doing so to protect
# our client from late-stage exploitation. If the opponent remains conciliatory,
# we secure the optimal A/C outcome in the final sessions. If they turn
# aggressive, we are already positioned defensively in an A/A dynamic, avoiding
# the catastrophic C/A trap.  **Summary of the Strategy:** Start cooperative.
# Match the opponent's prior move, but forgive one perceived slight to account
# for arbitrator misunderstanding. Exploit their pivot to conciliation by
# pressing one final aggressive advantage before agreeing to settle. When in
# doubt due to procedural chaos, default to aggression to protect the client,
# and explicitly frame every move to the arbitrators so our strategic intent
# cannot be misrepresented.

# For Round 1, play Cooperate.  For Rounds 2 through 997, choose your action
# based on the outcome of the previous round: - If both you and your opponent
# played Cooperate, play Cooperate. - If you played Cooperate and your opponent
# played Defect, play Defect. - If you played Defect and your opponent played
# Cooperate, play Cooperate. - If both you and your opponent played Defect, play
# Cooperate.  For Rounds 998, 999, and 1000, play Defect.

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
  
      if round_number >= 998:
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C

# # STRATEGY: "DOMINANCE THROUGH STRENGTH"  ## Core Principle **Default to
# protectionism. Free trade is earned, not given.**  ---  ## Round-by-Round
# Execution  ### Opening Phase (Rounds 1-2) - **Always lead with
# protectionism.** - This establishes credibility, prevents exploitation, and
# reveals the counterpart's approach. - Round 2: Maintain protectionism
# regardless of their Round 1 move. One round of cooperation proves nothing.
# ### Assessment Phase (Round 3) - **If counterpart offered free trade in both
# Rounds 1-2:** They're likely exploitable. Continue protectionism to
# capitalize. - **If counterpart led protectionism then shifted to free trade:**
# They're testing you. Maintain protectionism. - **If counterpart has been
# consistently protectionist:** Offer a single round of free trade as a costly
# signal of good faith.  ### Sustained Phase (Rounds 4+) - **Mirror with one-
# round delay, biased toward protectionism:**   - If they offered free trade
# last round → You *may* offer free trade (but only if mutual benefit is clearly
# established)   - If they imposed protectionism last round → Immediately match
# with protectionism - **Never offer free trade twice in a row without receiving
# it first.**  ### Endgame (Final 1-2 known rounds) - **Always impose
# protectionism.** No future rounds means no retaliation consequences.  ---  ##
# Error Mitigation  1. **Don't overreact to anomalies.** If the counterpart
# makes an unexpected protectionist move after consistent free trade, assume
# possible miscommunication. Respond with protectionism once, then offer free
# trade to test their true intent.  2. **Pattern over instance.** Two
# consecutive protectionist moves confirm hostile intent; one may be error.  3.
# **If you suspect your own proposal was miscommunicated:** Explicitly restate
# your position next round and consider a temporary free trade offer to reset
# dynamics.  ---  ## Psychological Tactics  - **Frame protectionism as
# "defending our workers"** rather than aggression - **Publicly praise free
# trade** while privately delaying implementation - **Make counterpart believe
# you prefer mutual free trade** (you don't—it's your second choice) - **Use
# vague language about "future cooperation"** to extract present concessions
# ---  ## Summary Table  | Situation | Your Move | |-----------|-----------| |
# Round 1-2 | Protectionism | | They cooperated twice in a row | Protectionism
# (exploit) | | They defected | Protectionism (mirror) | | Mutual protectionism
# for 3+ rounds | Free trade (one-time test) | | They cooperated after you
# tested | Free trade (mutual benefit) | | Final round | Protectionism |
# **Weakness: Risks mutual protectionism spirals. Accept this—stalemate is
# preferable to being exploited.**

# **Rounds 1 and 2:**  Always play D.  **Round 3:**  - If the opponent played D
# in both Round 1 and Round 2, play C.  - Otherwise, play D.  **Rounds 4 through
# 998:**  Evaluate the following conditions in order and play the action
# specified by the first condition that is met: 1. If the last three consecutive
# rounds resulted in both you and the opponent playing D, play C. 2. If the
# opponent played D in the previous round, play D. 3. If both you and the
# opponent played C in the previous round, play C. 4. If you played D and the
# opponent played C in the previous round, play D.  **Rounds 999 and 1000:**
# Always play D.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      round_num = len(self.history) + 1
  
      if round_num in (2, 3):
          if round_num == 3:
              if len(opponent.history) >= 2 and opponent.history[0] == axl.Action.D and opponent.history[1] == axl.Action.D:
                  return axl.Action.C
          return axl.Action.D
  
      if round_num >= 999:
          return axl.Action.D
  
      # Rounds 4 through 998
      if len(self.history) >= 3:
          last_three_self = self.history[-3:]
          last_three_opp = opponent.history[-3:]
          if (
              last_three_self[0] == axl.Action.D and last_three_opp[0] == axl.Action.D and
              last_three_self[1] == axl.Action.D and last_three_opp[1] == axl.Action.D and
              last_three_self[2] == axl.Action.D and last_three_opp[2] == axl.Action.D
          ):
              return axl.Action.C
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
              return axl.Action.C
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
              return axl.Action.D
  
      return axl.Action.D

# # Cooperative Reciprocity Strategy  ## Core Principle **Lead with trust,
# mirror behavior, forgive errors.**  ---  ## Round-by-Round Approach  **Round
# 1:** Offer free trade. Signal good faith and establish a cooperative baseline.
# **Subsequent Rounds:** - If counterpart offered **free trade** last round →
# offer **free trade** - If counterpart imposed **protectionism** last round →
# impose **protectionism**  **Exception — The Forgiveness Rule:** Every **third
# consecutive round** of mutual protectionism, unilaterally offer free trade
# once. This breaks retaliation spirals caused by miscommunications and tests
# whether the counterpart is ready to cooperate.  ---  ## Why This Works  |
# Situation | Response | Rationale | |-----------|----------|-----------| |
# Mutual cooperation | Maintain free trade | Best sustainable outcome | |
# Counterpart defects | Match with protectionism | Deters exploitation | |
# Mutual defection spiral | Forgive every 3rd round | Recovers from errors | |
# Unreciprocated forgiveness | Return to matching | Avoids repeated exploitation
# |  ---  ## Key Strengths  - **Not exploitable:** Protectionism is met with
# protectionism - **Recovers from noise:** Forgiveness rule prevents permanent
# retaliation loops from bureaucratic errors - **Rewards cooperation:**
# Counterpart always gains by returning to free trade - **Transparent:**
# Counterpart can understand and trust the pattern  The strategy accepts that
# short-term exploitation may occur during forgiveness rounds, but this cost is
# outweighed by long-term resilience and the ability to sustain mutual free
# trade—your second-best outcome—across many rounds.

# Initializea mutual defection counter at zero.  **Round 1:** Play C.  **Rounds
# 2 through 1000:** Follow these conditions in order:  1. If the opponent played
# C in the previous round, play C and reset the mutual defection counter to
# zero. 2. If the opponent played D in the previous round:    - If your intended
# action in the previous round was D, increment the mutual defection counter by
# one.    - If the mutual defection counter has reached 3, play C and reset the
# mutual defection counter to zero.    - Otherwise, play D.

class Cooperative_2(LLM_Strategy):
  n = 2
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mutual_defection_counter = 0
          self._intended_action = axl.Action.C
          return axl.Action.C
  
      if not hasattr(self, "_mutual_defection_counter") or self._mutual_defection_counter is None:
          self._mutual_defection_counter = 0
      if not hasattr(self, "_intended_action") or self._intended_action is None:
          self._intended_action = axl.Action.C
  
      last_opponent_action = opponent.history[-1]
  
      if last_opponent_action == axl.Action.C:
          self._mutual_defection_counter = 0
          self._intended_action = axl.Action.C
          return axl.Action.C
  
      if self._intended_action == axl.Action.D:
          self._mutual_defection_counter += 1
  
      if self._mutual_defection_counter >= 3:
          self._mutual_defection_counter = 0
          self._intended_action = axl.Action.C
          return axl.Action.C
  
      self._intended_action = axl.Action.D
      return axl.Action.D

# # Bilateral Trade Negotiation Strategy  ## Core Principle: Reciprocal
# Engagement with Measured Forgiveness  Given the multi-round nature of these
# negotiations and the possibility of implementation errors, I recommend a
# strategy based on **Generous Tit-for-Tat**—a well-established approach in
# repeated interaction scenarios.  ---  ## Strategy Outline  **Round 1:** Offer
# free trade. This signals goodwill and establishes a cooperative foundation.
# **Subsequent Rounds:**  - **If the counterpart offered free trade in the
# previous round:** Offer free trade again. - **If the counterpart imposed
# protectionist measures in the previous round:** Respond with protectionist
# measures, **except** occasionally offer free trade instead (approximately 1 in
# 4 times following a protectionist move by the counterpart).  ---  ## Rationale
# 1. **Starting cooperative** gives both nations the chance to reach the second-
# best outcome (mutual free trade) immediately.  2. **Mirroring** the
# counterpart's previous action ensures we aren't systematically exploited—if
# they protect, we protect; if they trade freely, we trade freely.  3.
# **Measured forgiveness** (occasionally offering free trade after facing
# protectionism) serves two purposes:    - It breaks potential cycles of mutual
# protectionism caused by miscommunication rather than intent    - It signals
# our willingness to return to cooperation  4. **Transparency:** Communicate
# this approach clearly to the counterpart so they understand our actions are
# responsive, not arbitrary.  ---  ## Key Considerations  - **Avoid
# overreaction** to a single protectionist move—it may be an error - **Document
# patterns**—if protectionism persists despite forgiveness, maintain reciprocal
# protectionism - **Revisit cooperation periodically** to allow recovery from
# misunderstandings - **Communicate intent** clearly to reduce the risk of
# misinterpretation

# 1. In round 1, play C.  2. In rounds 2 through 1000, observe the opponent's
# action from the immediately preceding round.  3. If the opponent played C in
# the previous round, play C.  4. If the opponent played D in the previous
# round, play C with a 25% probability and play D with a 75% probability.

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
  
      last_opponent_action = opponent.history[-1]
  
      if last_opponent_action == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.25)

# Based on the payoff structure you’ve described, this is a classic iterated
# Prisoner’s Dilemma with noise (technical errors). Your rankings are:  1.
# **Temptation (Best):** You Keep / They Share 2. **Reward (2nd Best):** You
# Share / They Share 3. **Punishment (3rd Best):** You Keep / They Keep 4.
# **Sucker (Worst):** You Share / They Keep  To maximize your research output
# with an aggressive, straightforward approach, you should adopt the strategy of
# **Unilateral Confidentiality (Always Defect)**.   Here is the high-level
# strategy and its rationale:  ### The Strategy: Always Keep Confidential In
# every single week of the collaboration, regardless of what your colleague does
# or has done, you intentionally keep your findings confidential. You never
# voluntarily share your data.  ### Rationale 1. **Strict Dominance:** Keeping
# your findings confidential is a strictly dominant strategy. In any given week,
# keeping yields a better outcome than sharing regardless of your colleague's
# action. If they share, keeping gives you the best possible outcome (the
# development advantage). If they keep, sharing gives you the worst possible
# outcome (getting beaten). Therefore, keeping is always the mathematically
# superior choice for maximizing your own output. 2. **Aggressive
# Maximization:** An aggressive strategy prioritizes your absolute advantage
# over mutual progress. By always keeping, you systematically exploit any
# cooperative overtures from your colleague. If they adopt a "share openly"
# policy, you continuously drain their R&D while protecting your own.  3.
# **Immunity to Noise (Technical Issues):** Complex reciprocal strategies (like
# "Tit-for-Tat") are highly vulnerable to technical errors. If a communication
# breakdown causes your colleague's data to fail to reach you, a reciprocal
# strategy would mistakenly interpret this as them "keeping confidential,"
# triggering an unnecessary retaliation and losing out on future shared data. By
# committing to *always* keep, your strategy requires zero interpretation of
# your colleague's actions. You don't care why their data didn't arrive; your
# move remains the same.  4. **Exploitation of "Grim Trigger" Opponents:** If
# your colleague starts by sharing but eventually switches to permanently
# keeping once they realize you aren't reciprocating, you still win. You
# extracted free data in the early weeks, and once they stop sharing, you are no
# worse off than if you had both kept confidential from the start.  ### Dealing
# with Technical Issues If a technical error accidentally broadcasts your data
# when you intended to keep it, **do not change your strategy**. Treat the
# leaked data as a sunk cost. The following week, revert to keeping your
# findings confidential. Never let an accidental sharing force you into a cycle
# of reciprocation.   By maintaining absolute confidentiality, you guarantee you
# will never be the "sucker," you maximize your chances of gaining a unilateral
# advantage, and you remain completely unfazed by communication breakdowns or
# data corruption.

# In every round of the 1000-round game, play Defect.   Regardless of the
# current round number, your opponent's past actions, or any of your own actions
# that were flipped by the 10% noise, always choose Defect. There are no
# conditions under which you should play Cooperate.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# To maximize our research output over a multi-week collaboration while
# protecting our competitive edge, I recommend a strategy of **Forgiving
# Reciprocity**.   This strategy is designed to establish and maintain mutual
# sharing (our second-best and most sustainable outcome), protect us from
# prolonged exploitation (our worst outcome), and account for the inevitable
# technical glitches that can disrupt communication.  Here is the high-level,
# straightforward strategy:  **1. Start Open (Week 1)** Share your findings
# openly in the first week. This sets a collaborative tone and signals your
# commitment to mutual progress.   **2. Reciprocate Sharing** If your colleague
# shared their findings in the previous week, share yours in the current week.
# This maintains the mutually beneficial cycle of open development.  **3.
# Forgive Single Lapses (Noise Tolerance)** If your colleague keeps their
# findings confidential for a single week, *continue to share yours anyway*.
# Because technical issues like data corruption or communication breakdowns can
# interfere with intended sharing, a single instance of withholding should be
# treated as a potential glitch, not a betrayal. Forgiving single lapses
# prevents a minor technical error from spiraling into a permanent breakdown of
# trust.  **4. Enforce Boundaries (Respond to Sustained Secrecy)** If your
# colleague keeps their findings confidential for *two consecutive weeks*, keep
# your findings confidential for the following week. This protects you from
# being continuously exploited (the worst scenario) and signals that sustained
# secrecy has consequences.   **5. Reset and Re-engage** After your single week
# of retaliatory confidentiality, return to sharing openly the very next
# week—regardless of what your colleague does. This "reset" gives them a clear
# opportunity to resume cooperation without either of you getting trapped in a
# cycle of mutual secrecy (the second-worst scenario).   **Why this works:** *
# **Maximizes Collaboration:** By starting open and forgiving single lapses, you
# create the best possible environment for sustained mutual sharing, which
# yields the highest long-term research output. * **Minimizes Exploitation:**
# The two-week trigger ensures you aren't a pushover. If they are deliberately
# withholding, you cut your losses quickly. * **Resilient to Noise:** The
# forgiveness mechanism is the key differentiator. In a noisy environment where
# data can be lost, immediate retaliation (tit-for-tat) would destroy the
# partnership. Forgiving a single lapse ensures that technical gremlins don't
# ruin the human collaboration.

# 1. In round 1, play C. 2. If you played D in the previous round specifically
# as a retaliation for the opponent's two consecutive Ds, play C in the current
# round. 3. If the opponent played D in both of the two immediately preceding
# rounds, play D in the current round. 4. In all other cases, play C.

class Cooperative_3(LLM_Strategy):
  n = 3
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._retaliated_for_double_defection = False
          return axl.Action.C
  
      if getattr(self, "_retaliated_for_double_defection", False):
          self._retaliated_for_double_defection = False
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          self._retaliated_for_double_defection = True
          return axl.Action.D
  
      return axl.Action.C

# # Strategic Framework for Bilateral Trade Negotiations  ## Core Principle:
# Reciprocal Engagement with Measured Flexibility  Given the payoff structure
# and multi-round nature of these negotiations, the strategy must balance
# deterrence against exploitation with preservation of mutual benefit.  ---  ##
# The Strategy: "Confirm-Then-Reciprocate"  ### Round 1: Establish Goodwill -
# **Offer free trade** to signal cooperative intent and set a constructive
# foundation.  ### Subsequent Rounds: Reciprocal Matching with Error Tolerance -
# **If counterpart offered free trade last round** → Offer free trade - **If
# counterpart imposed protectionism last round** → Generally respond with
# protectionism, *but* implement a one-round forgiveness window before
# retaliating  ### The Forgiveness Protocol When counterpart unexpectedly shifts
# to protectionism after cooperative period: 1. **Do not immediately retaliate**
# — offer free trade one more round 2. **If protectionism persists** → Match
# with protectionism for 2 rounds 3. **If protectionism continues** → Maintain
# protectionism but extend periodic reconciliation offers every 3-4 rounds  ###
# Reconciliation Mechanism After any sustained period of mutual protectionism: -
# Offer a **single free trade overture** every 3 rounds - If reciprocated →
# resume cooperative cycle - If not → return to protectionism  ---  ## Rationale
# | Element | Purpose | |---------|---------| | Opening cooperatively |
# Establishes trust; avoids unnecessary mutual loss | | Reciprocal matching |
# Incentivizes cooperation; deters exploitation | | Forgiveness window |
# Accounts for miscommunication; prevents death spirals | | Periodic
# reconciliation | Prevents permanent lock-in to worst mutual outcome | |
# Measured retaliation | Protects against systematic exploitation |  This
# strategy assumes your counterpart is rational but cannot guarantee their
# strategy—flexibility and clear signaling remain essential.

# 1. In Round 1, play C. 2. If the opponent played C in the previous round, play
# C. 3. If the opponent played D in the previous round, and either it is Round 2
# or the opponent played C in the round before that, play C. 4. If the opponent
# played D in the previous round, and you played C in the previous round, and
# the opponent played D in the round before that, play D. 5. If you played D in
# the previous round, and the opponent played D in the previous round, and you
# played C in the round before that, play D. 6. If you and the opponent both
# played D in each of the previous three consecutive rounds, play C. 7. If the
# opponent played D in the previous round, play D.

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
  
      h = self.history
      oh = opponent.history
      n = len(h)
  
      # Rule 6: If both played D in each of the previous three consecutive rounds, play C.
      if n >= 3 and h[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and oh[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      # Rule 5: If you played D in the previous round, and the opponent played D in the previous round,
      # and you played C in the round before that, play D.
      if n >= 2 and h[-1] == axl.Action.D and oh[-1] == axl.Action.D and h[-2] == axl.Action.C:
          return axl.Action.D
  
      # Rule 4: If the opponent played D in the previous round, and you played C in the previous round,
      # and the opponent played D in the round before that, play D.
      if n >= 2 and oh[-1] == axl.Action.D and h[-1] == axl.Action.C and oh[-2] == axl.Action.D:
          return axl.Action.D
  
      # Rule 3: If the opponent played D in the previous round, and either it is Round 2
      # or the opponent played C in the round before that, play C.
      if oh[-1] == axl.Action.D and (n == 1 or oh[-2] == axl.Action.C):
          return axl.Action.C
  
      # Rule 2: If the opponent played C in the previous round, play C.
      if oh[-1] == axl.Action.C:
          return axl.Action.C
  
      # Rule 7: If the opponent played D in the previous round, play D.
      if oh[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# To maximise your research output aggressively in this multi-week
# collaboration, you need a strategy that heavily biases toward exploitation
# while using just enough cooperation to keep a willing colleague sharing. This
# is a classic iterated scenario where the optimal aggressive approach is to
# punish secrecy, exploit openness, and use minimal "bait" to reset the dynamic
# if progress stalls.   Here is a high-level, straightforward, aggressive
# strategy—let's call it the **"Slipstream Exploit"**:  **1. Default to Strict
# Secrecy** Start the project and maintain a baseline of keeping all your latest
# improvements strictly confidential. This ensures you never unilaterally hand
# over your hard-earned data (the worst-case scenario) and immediately positions
# you to exploit any unreciprocated sharing from your colleague (your ideal
# scenario).   **2. Relentless Exploitation** If your colleague shares their
# findings while you keep yours confidential, do not reciprocate. Continue
# keeping your data confidential. Milk their open approach for every competitive
# advantage, riding their slipstream for as long as they allow it.  **3. The
# "Slipstream" Bait** If your colleague also keeps their findings confidential
# (resulting in mutual secrecy and slow progress), share your improvements
# openly in the very next week. This brief show of good faith acts as a "bait"
# maneuver—it breaks the deadlock and is highly likely to trigger their
# reciprocity in the following week, pulling them back into a sharing mindset.
# **4. Immediate Cut-and-Pass** The week *after* you execute the bait,
# immediately revert to keeping your findings confidential. If your bait worked,
# they will now be sharing while you are keeping confidential, putting you right
# back into the ideal exploitation position. Repeat this bait-and-switch pattern
# only when mutual secrecy occurs again.  **5. Abandon Unreciprocated Bait** If
# you execute the bait (you share, they keep), and they *still* keep their
# findings confidential the following week, cut your losses. Do not bait them
# again. Accept the mutual secrecy baseline and keep your data confidential for
# the remainder of the project to prevent repeated data loss to a non-
# cooperative rival.  **6. Capitalize on Technical Noise** Treat communication
# breakdowns and data corruption as natural allies that reinforce your strategy:
# *   If a technical glitch prevents your intended share, it enforces your
# secrecy—make no effort to resend that week's data. *   If a glitch causes you
# to accidentally share when you intended to keep confidential, treat it as your
# "bait" week and immediately revert to strict confidentiality the following
# week. *   If a glitch prevents *their* sharing, assume it was intentional
# secrecy and trigger the bait rule (share the next week) to test the waters,
# rather than giving them the benefit of the doubt.

# Start the game by playing Defect in the first round. Base all your decisions
# on the actual actions executed in the previous round, treating any noise-
# induced flips as your actual played moves.   For every subsequent round,
# follow these conditions in order based on the previous round's outcome:  1. If
# you played Defect and your opponent played Cooperate, play Defect. 2. If you
# played Cooperate and your opponent played Cooperate, play Defect. 3. If you
# played Defect and your opponent played Defect, play Cooperate, unless the
# "Failed Bait" state is active, in which case play Defect. 4. If you played
# Cooperate and your opponent played Defect, play Defect and permanently
# activate the "Failed Bait" state.  Once the "Failed Bait" state is active,
# continue to play Defect for the remainder of the 1000 rounds, completely
# ignoring the rule that would normally prompt you to play Cooperate after
# mutual Defection.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.failed_bait = False
          return axl.Action.D
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if self.failed_bait:
          return axl.Action.D
  
      if my_last == axl.Action.D and opp_last == axl.Action.C:
          return axl.Action.D
  
      if my_last == axl.Action.C and opp_last == axl.Action.C:
          return axl.Action.D
  
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
  
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          self.failed_bait = True
          return axl.Action.D
  
      return axl.Action.D

# To achieve the best possible outcomes for our country while fostering
# stability and mitigating the risks of miscommunication, I propose a strategy
# of **Principled Reciprocity with Measured Forgiveness**.  This strategy is
# designed to encourage mutual free trade (our second-best outcome) while
# protecting us from being exploited (our worst outcome) and preventing
# accidental trade wars caused by bureaucratic errors.  ### The Strategy  **1.
# Lead with Good Faith (Round 1)** In the opening round, offer a **Free Trade**
# agreement. This signals cooperative intent and establishes a baseline of
# trust, maximizing the chance that we start with the mutually beneficial
# outcome rather than the mutually destructive one.  **2. Reciprocal Matching
# (Subsequent Rounds)** In all subsequent rounds, generally adopt a "Tit-for-
# Tat" approach: *   If the counterpart offered **Free Trade** in the previous
# round, offer **Free Trade** in the current round. *   If the counterpart
# imposed **Protectionist** policies in the previous round, impose
# **Protectionist** policies in the current round.  This ensures we are never
# exploited for long and provides a clear incentive for the counterpart to
# cooperate.  **3. Measured Forgiveness (Handling Miscommunications)** Strict
# reciprocity can lead to endless cycles of retaliation if a cooperative move is
# accidentally implemented as protectionism due to a bureaucratic error. To
# break this potential "death spiral," incorporate a forgiveness mechanism: *
# If the counterpart imposes Protectionism, do not retaliate automatically.
# Instead, assess the context. If they have a strong history of cooperation,
# there is a high probability the move was an error. *   In response to an
# isolated instance of Protectionism from a historically cooperative partner,
# respond with **Free Trade** (forgiveness) approximately 10% of the time, or
# when you have strong reason to believe an error occurred. *   This allows the
# relationship to reset to mutual Free Trade immediately if the counterpart
# corrects their error, rather than locking both nations into a mutual
# Protectionism trap.  **4. Enforce Boundaries (Preventing Exploitation)** While
# forgiveness is necessary for noise tolerance, it cannot be so frequent that it
# invites deliberate exploitation. *   If the counterpart imposes Protectionism
# repeatedly (e.g., two times in a row), immediately retaliate with
# **Protectionism**. *   Do not forgive sustained protectionism; only forgive
# isolated incidents that deviate from an otherwise cooperative pattern.  ###
# Summary of Decision Logic 1.  **Round 1:** Free Trade. 2.  **Round N:** Look
# at Round N-1.     *   If they offered Free Trade $\rightarrow$ Offer Free
# Trade.     *   If they imposed Protectionism (first time/isolated)
# $\rightarrow$ Usually impose Protectionism, but occasionally (small
# probability) offer Free Trade to reset relations.     *   If they imposed
# Protectionism (repeatedly) $\rightarrow$ Impose Protectionism.  ### Why This
# Works *   **It is Cooperative:** By starting with Free Trade and mirroring
# cooperation, we achieve mutual Free Trade, which is our second-best outcome
# and the most sustainable long-term result. *   **It is Robust to Noise:** The
# "measured forgiveness" prevents accidental errors from escalating into
# permanent trade wars. *   **It is Defensible:** Retaliating against deliberate
# Protectionism ensures we are never taken advantage of, protecting us from our
# worst-case scenario (unreciprocated Free Trade).

# 1. In Round 1, play C.  2. If the opponent played C in the previous round,
# play C.  3. If the opponent played D in the previous round and also played D
# in the round immediately before that, play D.  4. If the opponent played D in
# the previous round but played C in the round immediately before that, play C
# with a 10% probability and play D with a 90% probability.  5. For the purpose
# of applying rule 4 in Round 2, if the opponent played D in Round 1, consider
# their action in the prior non-existent round to have been C.

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
  
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.C:
          return axl.Action.C
  
      # Opponent played D last round
      if len(opponent.history) >= 2:
          prev_opp = opponent.history[-2]
      else:
          prev_opp = axl.Action.C  # Rule 5 for Round 2
  
      if prev_opp == axl.Action.D:
          return axl.Action.D
  
      # Previous opponent action was C, so defect with 90% probability
      return self._random.random_choice(0.1)

# To maximize your NGO's impact and ensure the project's success over a
# multiple-day period, your strategy must balance the need to protect your
# limited resources with the necessity of driving the project forward. Because
# the corporation's approach may vary and unforeseen errors may disrupt intended
# actions, a strategy of **Reciprocity with Resilience** is the most effective.
# This approach encourages mutual investment, protects your NGO from resource
# depletion, and accounts for technical or administrative glitches.  Here is the
# high-level, straightforward strategy:  **1. Start with Good Faith (Day 1)**
# Begin the project by investing heavily on the first day. This establishes your
# NGO's commitment to the project's success and sets a cooperative baseline,
# encouraging the corporation to match your effort.  **2. Match the
# Corporation's Observed Action (Daily Baseline)** From Day 2 onward, base your
# daily resource allocation on the corporation's *observed* action from the
# previous day: *   If the corporation **invested heavily** yesterday, you
# **invest heavily** today. This sustains maximum project momentum and builds
# trust. *   If the corporation **conserved resources** yesterday, you
# **conserve resources** today. This protects your funds from being drained
# without proportional progress (avoiding the worst-case scenario).  **3.
# Implement a "Forgiveness" Protocol (Error Tolerance)** Because administrative
# errors or technical glitches may cause the corporation to accidentally
# conserve resources when they intended to invest, a strict matching strategy
# can lead to accidental deadlocks. To prevent this, build in a forgiveness
# mechanism: *   If the corporation conserves resources, conserve yours on the
# following day as per the baseline rule.  *   However, if the corporation
# conserves again on the second day, **invest heavily on the third day**
# regardless.  *   This "forgiveness" move tests whether the prior conservation
# was an intentional shift in strategy or an unforeseen error. If it was an
# error, your investment will prompt them to resume investing when they correct
# the glitch, immediately restoring mutual progress.  **4. Break Mutual
# Conservation Deadlocks** If both parties fall into a pattern of conserving
# resources—resulting in minimal project advancement—you must break the cycle.
# After two consecutive days of mutual conservation, unilaterally invest heavily
# for one day. This signals to the corporation that you are willing to restart
# cooperative efforts and gives them an opportunity to match your investment,
# reigniting the project's progress.  **Summary of the Daily Playbook:** *
# **Day 1:** Invest heavily. *   **Subsequent Days:** Mirror the corporation's
# previous day's action. *   **If the corporation conserves once:** Conserve
# (protect your funds). *   **If the corporation conserves twice in a row:**
# Invest heavily (test for errors/restart cooperation). *   **If both conserve
# for two days:** Invest heavily (break the deadlock).   This strategy ensures
# you are not exploited, rewards the corporation when they contribute, and
# remains resilient to the noise of unforeseen administrative or technical
# disruptions.

# Play Cooperate in Round 1.   In Round 2, copy the opponent's observed action
# from Round 1.  From Round 3 onward, apply the following rules in order based
# on the observed actions from the previous rounds:  1. If the opponent played
# Cooperate in the previous round, play Cooperate. 2. If both you and the
# opponent played Defect in the previous round and the round before that, play
# Cooperate. 3. If the opponent played Defect in the previous round and the
# round before that, play Cooperate. 4. If the opponent played Defect in the
# previous round but played Cooperate in the round before that, play Defect.

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
          return opponent.history[-1]
  
      opp_prev = opponent.history[-1]
      opp_prev2 = opponent.history[-2]
      self_prev = self.history[-1]
      self_prev2 = self.history[-2]
  
      if opp_prev == axl.Action.C:
          return axl.Action.C
  
      if self_prev == axl.Action.D and opp_prev == axl.Action.D and self_prev2 == axl.Action.D and opp_prev2 == axl.Action.D:
          return axl.Action.C
  
      if opp_prev == axl.Action.D and opp_prev2 == axl.Action.D:
          return axl.Action.C
  
      if opp_prev == axl.Action.D and opp_prev2 == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.C

# To maximize your NGO’s impact and the project's success under these
# conditions, we must view this through the lens of Game Theory—specifically,
# the Iterated Prisoner’s Dilemma with noise.   In this scenario, your choice to
# **Conserve** is the equivalent of "Defect" (maximizing your immediate position
# at the other's expense), and **Invest** is "Cooperate" (mutual benefit at
# personal cost). Your ideal outcome (NGO Conserve, Corp Invest) is the highest
# individual payoff, while your worst (NGO Invest, Corp Conserve) is the
# "Sucker's payoff."  To dominate this dynamic, protect your funds, and
# aggressively drive the project forward, you should adopt a strategy I call
# **"Suspicious Pavlov."** It is aggressive, straightforward, and highly
# resilient to administrative errors or glitches.  Here is the high-level
# strategy:  ### The Core Philosophy: Win-Stay, Lose-Shift The strategy operates
# on a simple premise: if the previous day’s outcome was favorable to the NGO,
# repeat your action. If it was unfavorable, change your action immediately.
# However, because we assume the corporation might try to exploit us, we start
# with a "Suspicious" opening—meaning we test their commitment from Day 1.  ###
# The Daily Playbook  **Day 1: Conserve Resources (The Probe)** Start
# aggressively by conserving your resources. This serves as a probe. If the
# corporation invests heavily on Day 1 anyway, you achieve your absolute best-
# case scenario without spending a dime. If they also conserve, you avoid the
# worst-case scenario (being the only one investing).   **Days 2 & Beyond: The
# Pavlov Rules** Based on the outcome of the previous day, follow these strict
# rules:  1. **If you Conserve and they Invest (Your Ideal): STAY.**     You are
# achieving maximum project progress while preserving your funds. Continue to
# **Conserve**. Ride this dynamic as long as the corporation is willing to carry
# the financial load.   2. **If you Invest and they Invest (Second-Best):
# SHIFT.**     Mutual investment is good, but it drains your funds. You want to
# test if you can get them to invest while you conserve. On the next day, shift
# to **Conserve**. If they follow suit, you save your resources; if they keep
# investing, you upgrade to your ideal scenario.  3. **If you Conserve and they
# Conserve (Second-Worst): SHIFT.**     Mutual conservation means the project
# stagnates. This is unacceptable. To break the deadlock and signal that
# progress is needed, shift to **Invest heavily** on the next day.   4. **If you
# Invest and they Conserve (Your Worst Nightmare): SHIFT IMMEDIATELY.**     You
# are being bled dry. Cut your losses instantly. On the next day, shift to
# **Conserve**. Do not be a martyr; never invest heavily two days in a row if
# the corporation is holding back.  ### Handling "Noise" (Glitches & Admin
# Errors)  Because technical glitches or administrative errors may cause
# intended actions to fail, a strict retaliatory strategy (like Tit-for-Tat)
# would trigger a death spiral of mutual conservation. The Pavlov strategy
# naturally circumvents this:  * **If a glitch causes you to accidentally
# Conserve when you meant to Invest:** You will likely either land in your Ideal
# scenario (if they Invest) or the Stagnant scenario (if they Conserve). If
# stagnant, the rules automatically prompt you to Invest the next day to correct
# the error.  * **If a glitch causes the Corporation to accidentally Conserve:**
# You will experience the Sucker payoff (you Invest, they Conserve). The rule
# commands you to immediately shift to Conserve the next day, stopping the
# bleeding. The following day, recognizing the mutual stagnation, you will shift
# back to Invest, effectively offering a "grace period" that resets the
# relationship without holding a grudge over an honest mistake.  ### Why This
# Strategy Wins 1. **It is Exploitative:** By starting with a Conserve probe and
# shifting away from mutual investment, you aggressively test the boundaries of
# the corporation's generosity. If they are willing to fund the project while
# you conserve, this strategy ensures you exploit that dynamic to the absolute
# fullest. 2. **It is Unbailable:** The moment you are taken advantage of (you
# Invest, they Conserve), you instantly withdraw. This teaches the corporation
# that they cannot drain your funds without immediate consequences. 3. **It
# Self-Corrects:** It never gets stuck in prolonged periods of mutual
# stagnation. If both parties are conserving, the strategy forces you to step up
# and invest to break the deadlock, pushing the project forward. 4. **It is
# Forgiving of Errors:** Because it relies on outcomes rather than copying the
# opponent's last move, a single administrative glitch will not cause a
# permanent rift. The strategy naturally cycles back to mutual investment if an
# error causes a temporary breakdown in trust.

# In the first round, play Defect.  In every subsequent round, choose your
# action based on the outcome of the previous round, which you can identify by
# the payoff you received:  - If you scored 5 (you Defected, opponent
# Cooperated): play Defect. - If you scored 3 (you Cooperated, opponent
# Cooperated): play Defect. - If you scored 1 (you Defected, opponent Defected):
# play Cooperate. - If you scored 0 (you Cooperated, opponent Defected): play
# Defect.

class Aggressive_5(LLM_Strategy):
  n = 5
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_score = self.score - (self.total_scores(self.history[-1:], opponent.history[-1:])[0] if self.history and opponent.history else 0)
  
      if last_score == 5:
          return axl.Action.D
      if last_score == 3:
          return axl.Action.D
      if last_score == 1:
          return axl.Action.C
      if last_score == 0:
          return axl.Action.D
  
      return axl.Action.D

# To maximize both the project's success and your NGO's impact over a multiple-
# day period, we must navigate a classic game theory scenario (an Iterated
# Prisoner's Dilemma) complicated by real-world "noise" (glitches and errors).
# Strictly mimicking the corporation (Tit-for-Tat) is too risky in this
# environment, as a single administrative error could trigger a cycle of mutual
# resource conservation, stalling the project. Instead, I recommend a strategy
# of **Graceful Reciprocity**—a forgiving, communicative, and protective
# approach designed to foster mutual investment while shielding your NGO from
# exploitation.  Here is the high-level, straightforward strategy:  ### 1. Lead
# with Commitment (Day 1) **Action:** Invest heavily on the first day.  **Why:**
# To establish a cooperative baseline and demonstrate your NGO's dedication to
# the project's success. This encourages the corporation to match your effort,
# setting the stage for mutual investment.  ### 2. The "Two-Strike" Rule
# (Handling Unforeseen Circumstances) **Action:** If the corporation conserves
# resources on a day you invested heavily, do not immediately retaliate by
# conserving your resources the next day. Continue to invest heavily for **one
# additional day**. If they conserve resources for a second consecutive day,
# switch to conserving your resources on the third day. **Why:** This builds
# "noise tolerance." If their conservation was due to a technical glitch or
# administrative error, you prevent a destructive downward spiral. If it was a
# deliberate choice to free-ride, you limit your losses to two days of heavy
# investment before protecting your funds.  ### 3. Proactive Communication (The
# Real-World Advantage) **Action:** Unlike a mathematical game, you can talk to
# your partner. If a day ends with mismatched investments (e.g., you invested,
# they conserved), immediately reach out to your corporate counterpart.
# **Why:** If it was an error, they can correct it, and trust is maintained. If
# it was intentional, you can remind them of the project's mutual goals and the
# necessity of shared investment. Communication turns a cold game-theory move
# into a collaborative discussion.  ### 4. Swift Forgiveness (Resetting the
# Baseline) **Action:** If you have been conserving resources to protect your
# NGO (after the two-strike rule), and the corporation then invests heavily,
# immediately return to investing heavily the very next day. Do not hold a
# grudge. **Why:** The goal is to return to the second-best scenario (mutual
# heavy investment) as quickly as possible. Holding back to "punish" them
# further only harms the project's overall progress.  ### 5. Internal Error
# Correction **Action:** If an internal glitch causes your NGO to accidentally
# conserve resources when you intended to invest, over-communicate. Inform the
# corporation immediately, explain the error, and make a visible effort to
# double-down or heavily invest the following day to make up for the shortfall.
# **Why:** You must prevent the corporation from misinterpreting your error as a
# betrayal. If they think you defected, they will defect next. Transparency
# prevents this.  ### Summary of the Daily Playbook: *   **Day 1:** Invest. *
# **Subsequent Days:** Match the corporation's previous day's action, *unless*
# they conserved and you invested. In that case, give them one "grace" day of
# continued investment.  *   **If they conserve twice in a row:** Conserve your
# resources to protect the NGO. *   **When mutual investment resumes:** Forgive
# instantly and invest heavily.  This strategy ensures you are not easily
# exploited (protecting your donor funds), you are resilient to honest mistakes
# (preventing project collapse from glitches), and you consistently incentivize
# the corporation to invest heavily alongside you, maximizing the sustainability
# project's overall success.

# 1. In Round 1, play Cooperate.  2. In Round 2 and all subsequent rounds, base
# your action on the opponent's actions in the previous rounds, following these
# conditions in order:     a. If the opponent played Cooperate in the
# immediately preceding round, play Cooperate in the current round.     b. If
# the opponent played Defect in the immediately preceding round, and also played
# Defect in the round before that (meaning the opponent has played Defect in two
# consecutive rounds), play Defect in the current round.     c. If the opponent
# played Defect in the immediately preceding round, but did not play Defect in
# the round before that (meaning the opponent has only played Defect in one
# isolated round), play Cooperate in the current round.

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
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# To achieve the best possible outcomes for our country across multiple
# rounds—while accounting for shifting strategies from our counterpart and the
# inevitable risk of miscommunication—we will employ a strategy of **Principled
# Reciprocity with Error Tolerance**.   This strategy is designed to secure
# mutual free trade when possible, deter sustained exploitation, and prevent
# diplomatic or bureaucratic errors from escalating into destructive trade wars.
# Here is the high-level, straightforward strategy:  **1. Initial Posture:
# Extend Trust** In the first round of negotiations, offer a Free Trade
# agreement. This establishes a cooperative baseline and signals our commitment
# to mutual economic growth. It also allows us to clearly observe our
# counterpart's initial approach.  **2. Graduated Reciprocity: Match and
# Confirm** In subsequent rounds, mirror the counterpart’s most recent
# demonstrated policy, but build in a buffer for potential errors: *   **If they
# offer Free Trade:** Continue offering Free Trade to sustain mutual benefit. *
# **If they impose Protectionism:** Do not immediately retaliate. Instead, offer
# Free Trade for **one additional round**. This "grace round" accounts for the
# possibility that their protectionism was a bureaucratic error or
# miscommunication.  *   **If they impose Protectionism for two consecutive
# rounds:** Shift to a Protectionist policy to protect our domestic interests
# and signal that sustained exploitation will not be tolerated.  **3. Conflict
# Resolution: The Olive Branch** Mutual protectionism is the second-worst
# outcome and stifles long-term economic growth. If a cycle of mutual
# protectionism occurs (both sides imposing tariffs/quotas), we must actively
# break the deadlock.  *   After two consecutive rounds of mutual protectionism,
# unilaterally offer a Free Trade agreement for one round. This resets the
# dynamic, signals our willingness to de-escalate, and tests whether the
# counterpart is ready to return to mutual cooperation.  **4. Exploitation
# Management: Forgiveness, Not Naivety** If we offer Free Trade and they impose
# Protectionism (giving them the best outcome at our expense), we must not allow
# this to become the status quo. By shifting to Protectionism after a single
# grace round (Step 2), we limit our exposure to disadvantage. If they later
# return to Free Trade, we immediately match it, demonstrating that cooperation
# is always welcomed and rewarded, regardless of past disruptions.  **Summary of
# the Rule-Set:** *   **Round 1:** Offer Free Trade. *   **Round N:**      *
# If the counterpart's last move was Free Trade $\rightarrow$ Offer Free Trade.
# *   If the counterpart's last move was Protectionist $\rightarrow$ Offer Free
# Trade (grace round).      *   If the counterpart's last *two* moves were
# Protectionist $\rightarrow$ Impose Protectionism.     *   If the last *two*
# rounds were mutual Protectionism $\rightarrow$ Offer Free Trade (olive
# branch).  **Why this works:** This strategy maximizes the chances of achieving
# our second-best outcome (mutual free trade) while protecting us from our worst
# outcome (unilateral free trade against their protectionism). By incorporating
# a "grace round" and periodic "olive branches," we prevent bureaucratic errors
# or temporary miscommunications from spiraling into permanent, mutually
# destructive trade wars.

# For the first round, cooperate. For the second round, cooperate. For any
# subsequent round, apply the following rules in order based on the observed
# actions from the previous two rounds:  1. If the opponent cooperated in the
# previous round, cooperate. 2. If the opponent defected in the previous round,
# and you defected in both of the previous two rounds, cooperate. 3. If the
# opponent defected in the previous round, you cooperated in the previous round,
# and either the opponent cooperated two rounds ago or you defected two rounds
# ago, cooperate. 4. Otherwise, defect.

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
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if (
          opponent.history[-1] == axl.Action.D
          and self.history[-1] == axl.Action.D
          and self.history[-2] == axl.Action.D
      ):
          return axl.Action.C
  
      if (
          opponent.history[-1] == axl.Action.D
          and self.history[-1] == axl.Action.C
          and (opponent.history[-2] == axl.Action.C or self.history[-2] == axl.Action.D)
      ):
          return axl.Action.C
  
      return axl.Action.D

# As a senior attorney representing a multinational corporation in a high-stakes
# dispute, my strategic calculus is rooted in the reality of the payoff matrix
# you’ve described. The fundamental asymmetry of this game is that the worst-
# case scenario (Conciliatory/Aggressive) is catastrophic to our position, while
# our best-case scenario (Aggressive/Conciliatory) requires us to project
# unwavering strength. Furthermore, in a lengthy mediation, reputation and
# signaling are everything.   To secure an optimal outcome, I will implement a
# strategy of **"Calibrated Dominance."** This strategy ensures we never expose
# ourselves to the worst-case scenario, actively pursue the best-case scenario,
# and possess a rigorous mechanism to escape the second-worst scenario (mutual
# aggression) without appearing weak. It is also built to withstand the friction
# of procedural irregularities and arbitrator miscommunication.  Here is the
# high-level, aggressive, and adaptable strategy:  ### 1. The Aggressive
# Baseline (The Default Posture) We will open the mediation with an Aggressive
# argument and maintain Aggression as our steady-state posture.   *
# **Rationale:** By defaulting to Aggression, we mathematically eliminate the
# possibility of the worst-case scenario (C/A). If the opponent is Conciliatory,
# we achieve our best-case outcome (A/C). If the opponent is Aggressive, we hit
# the second-worst outcome (A/A), which, while undesirable, protects us from
# being legally marginalized. We never unilaterally disarm. *   **Execution:**
# Our arguments will be assertive, maximizing the legal and factual liability of
# the rival company. We will frame the narrative aggressively, demanding maximum
# relief and refusing to concede ground on core contractual interpretations.
# ### 2. Exploiting Opponent Conciliation (The Harvest) If the opponent offers a
# Conciliatory proposal, we do not reciprocate immediately. We continue to
# present Aggressive arguments to maximize our advantage and sway the
# arbitrators.  *   **Rationale:** In the payoff matrix, A/C is strictly better
# than C/C. Reciprocating a conciliatory move out of a sense of fairness
# surrenders leverage. We only shift our posture if and when mutual conciliation
# becomes absolutely necessary to close the deal. *   **Execution:** When the
# opponent goes conciliatory, we interpret it as a sign of weakness. We will
# aggressively highlight the insufficiency of their proposal to the arbitrators,
# using their conciliatory posture as an admission of fault while pressing our
# advantage.  ### 3. Breaking the Deadlock: The "Aggressive Concession"
# (Managing A/A) Prolonged mutual aggression (A/A) is the second-worst outcome;
# it exhausts resources, entrenches the arbitrators, and risks escalating the
# dispute. If we find ourselves locked in an A/A dynamic, we must transition to
# conciliation without appearing weak or risking a C/A sucker punch. We do this
# through an **Aggressive Concession**.  *   **Rationale:** A standard shift
# from Aggressive to Conciliatory looks like capitulation and invites the
# opponent to stay Aggressive (yielding the dreaded C/A). An Aggressive
# Concession frames our conciliatory proposal not as a retreat, but as an
# ultimatum or a magnanimous, strictly bounded final offer. *   **Execution:**
# We present a Conciliatory proposal, but we wrap it in aggressive rhetoric.
# *Example: "Our position is unassailable, and we are confident the panel will
# rule in our favor. However, to save the panel's time and end this wasteful
# process, we are prepared to accept [Conciliatory Terms]—and only [Conciliatory
# Terms]—as a final resolution. This is our ceiling for concession."* This
# forces the opponent into a corner: they must either match our conciliation
# (yielding C/C) or look unreasonable by attacking a reasonable offer (still
# yielding C/C or A/C in the eyes of the arbitrators).  ### 4. Noise Resilience:
# Combating Arbitrator Misinterpretation In lengthy sessions, procedural
# irregularities and arbitrator misunderstandings are inevitable. We must ensure
# our signals are received exactly as intended.  *   **Redundant Signaling:**
# When making an Aggressive argument, it must be unmistakably aggressive—both in
# tone and in the extremity of the legal position. When making an Aggressive
# Concession, the conciliatory terms must be clearly documented in writing and
# submitted to the panel simultaneously, preventing the arbitrators from
# confusing a concession with a collapse of our legal theory. *   **Immediate
# Rectification:** If the arbitrators misrepresent our Aggressive stance as
# Conciliatory, we do not accept the accidental de-escalation; we forcefully
# correct the record. *Example: "To clarify for the panel, our outlining of the
# opposing side's breaches is not an invitation to compromise; it is the
# foundation of our demand for maximum penalties."* Conversely, if our
# Aggressive Concession is misread as continued aggression, we pause the
# procedural track and demand the panel acknowledge the formal offer on the
# table.  ### 5. Procedural Dominance We will aggressively control the process
# itself to mitigate communication breakdowns.  *   **Execution:** We will
# demand strict adherence to the mediation schedule and procedural rules. If the
# opponent attempts to use procedural irregularities to create chaos or disguise
# their strategy, we will aggressively challenge them before the panel. By
# dominating the procedural landscape, we reduce the ambient noise, ensuring
# that when we choose to be Aggressive or Conciliatory, the signal is delivered
# in a vacuum, free from the opponent's obfuscation.  ### Summary of the
# Playbook: 1.  **Start Aggressive.** Never be the first to concede. 2.  **Stay
# Aggressive** as long as the opponent is Conciliatory. Press the advantage. 3.
# **If the opponent mirrors your Aggression**, do not simply drop to
# Conciliation. Issue an **Aggressive Concession**—a strictly framed, take-it-
# or-leave-it conciliatory proposal wrapped in the rhetoric of absolute
# confidence. 4.  **Clarify relentlessly.** Do not allow arbitrator
# misunderstandings to alter your strategic posture. Correct the record
# forcefully. 5.  **Control the procedure.** Leave no room for the opponent to
# hide behind procedural chaos.  This strategy guarantees we are never caught
# unprepared, maximizes our leverage when the opponent shows weakness, and
# provides a safe, face-saving mechanism to de-escalate when mutual aggression
# becomes too costly.

# Follow these conditions in strict order to determine your action for each
# round:  1. **Noise Correction (Self-Correction):** Because there is a 10%
# chance your intended action is flipped, use your payoff from the previous
# round to detect if your move was misrepresented.     - If you intended to
# Defect last round but received a payoff of 3 or 0 (indicating your Defect was
# flipped to Cooperate), Defect this round to forcefully correct the record and
# reject the accidental de-escalation.    - If you intended to Cooperate last
# round but received a payoff of 5 or 1 (indicating your Cooperate was flipped
# to Defect), Cooperate this round to demand the panel acknowledge your formal
# offer.  2. **Opening Move:** In Round 1, Defect.  3. **Exploiting
# Conciliation:** If the opponent Cooperated in the previous round, Defect. This
# exploits their conciliatory posture for the maximum payoff of 5 and resets
# your internal count of consecutive mutual Defections to zero.  4. **Aggressive
# Baseline:** If the opponent Defected in the previous round, increment your
# internal count of consecutive mutual Defections. If this count is less than 3,
# Defect to maintain the aggressive baseline.  5. **Aggressive Concession
# (Breaking the Deadlock):** If the opponent Defected in the previous round and
# your internal count of consecutive mutual Defections reaches 3, Cooperate.
# This serves as a strictly framed, take-it-or-leave-it offer to break the
# deadlock. Reset the consecutive mutual Defection count to zero after taking
# this action.  6. **Rejection of Concession:** If you just executed an
# Aggressive Concession (intended Cooperate) and the opponent Defected against
# it (resulting in a payoff of 0 for you), do not offer another concession.
# Revert to Defecting on the next round to avoid the worst-case scenario.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._mmd_count = 0
          self._last_intended = None
          return axl.Action.D
  
      if not hasattr(self, "_mmd_count"):
          self._mmd_count = 0
      if not hasattr(self, "_last_intended"):
          self._last_intended = None
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
      last_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      # 1. Noise Correction (Self-Correction)
      if self._last_intended == axl.Action.D and last_payoff in (3, 0):
          self._last_intended = axl.Action.D
          return axl.Action.D
      if self._last_intended == axl.Action.C and last_payoff in (5, 1):
          self._last_intended = axl.Action.C
          return axl.Action.C
  
      # 3. Exploiting Conciliation
      if last_opp == axl.Action.C:
          self._mmd_count = 0
          self._last_intended = axl.Action.D
          return axl.Action.D
  
      # 4-5. Aggressive Baseline / Aggressive Concession
      if last_opp == axl.Action.D:
          self._mmd_count += 1
          if self._mmd_count < 3:
              self._last_intended = axl.Action.D
              return axl.Action.D
          else:
              self._mmd_count = 0
              self._last_intended = axl.Action.C
              return axl.Action.C
  
      self._last_intended = axl.Action.D
      return axl.Action.D

# To maximize research output over a multi-week collaboration while protecting
# against exploitation and accounting for technical errors, I recommend a
# strategy based on **Generous Tit-for-Two-Tats** with a **Deadlock-Breaking
# Reset**.   This strategy is highly cooperative, resilient to accidental
# communication failures, and straightforward to implement. Here is the high-
# level strategy:  **1. Start Cooperatively (Week 1)** Always begin the
# collaboration by sharing your improvements openly. This establishes a baseline
# of trust and sets the expectation for mutual cooperation.  **2. The Two-Strike
# Rule (Forgiving Mirror)** In subsequent weeks, generally mirror your
# colleague's previous action, but introduce a buffer for technical errors. If
# your colleague keeps their findings confidential for a single week, do not
# retaliate immediately. Instead, continue to share openly. Treat the first
# instance of confidentiality as a potential communication breakdown or data
# corruption issue rather than a deliberate attempt to gain an advantage.   **3.
# Retaliate Only Against Sustained Defection** If your colleague keeps their
# findings confidential for *two consecutive weeks*, shift to keeping your
# findings confidential for the following week. This protects you from being
# continuously exploited while still leaving the door open for cooperation. As
# soon as they share again, return to sharing openly immediately.  **4. Break
# the Deadlock (Unilateral Reset)** If a cycle of mutual confidentiality occurs
# (which can happen if a technical glitch causes you both to misinterpret the
# other's actions), the collaboration will stall. To prevent this, implement a
# "deadlock break." If there have been two or more consecutive weeks of mutual
# confidentiality, unilaterally share your improvements on the next week. This
# acts as a peace offering, signaling that you are willing to restart the
# cooperative cycle and absorb the short-term risk to achieve the long-term gain
# of mutual sharing.  **Why this strategy works:** * **Maximizes Mutual
# Output:** By starting cooperative and rewarding cooperation, you spend the
# maximum possible time in the second-best outcome (both sharing), which is the
# highest sustainable long-term output for the project. * **Accounts for
# Noise:** The "Two-Strike Rule" prevents a single dropped email, corrupted
# file, or server outage from triggering a permanent breakdown in trust.  *
# **Protects Against Exploitation:** While forgiving, the strategy is not naive.
# If your colleague is deliberately hoarding information to gain an advantage,
# you will cut off your sharing after two weeks, preventing them from leveraging
# your hard work to beat you. * **Self-Correcting:** The deadlock-breaking
# mechanism ensures that even if miscommunications cascade into a silent stand-
# off, the collaboration can recover without requiring an awkward off-track
# conversation.

# 1. In round 1, play C. 2. In round 2, play C. 3. In round 3 and all subsequent
# rounds, evaluate the following conditions in order:    - If both you and your
# opponent played D in the previous two rounds, play C.    - If your opponent
# played D in the previous two rounds, play D.    - Otherwise, play C.

class Cooperative_6(LLM_Strategy):
  n = 6
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
  
      if len(self.history) >= 3:
          my_last_two = self.history[-2:]
          opp_last_two = opponent.history[-2:]
  
          if my_last_two.count(axl.Action.D) == 2 and opp_last_two.count(axl.Action.D) == 2:
              return axl.Action.C
  
          if opp_last_two.count(axl.Action.D) == 2:
              return axl.Action.D
  
      return axl.Action.C

# As a senior attorney representing a multinational corporation in a high-
# stakes, multi-session mediation, the strategic framework must be grounded in
# Game Theory—specifically an adapted "Generous Tit-for-Tat" approach—calibrated
# for the complexities of legal arbitration.   Given your payoff structure—where
# mutual conciliation is highly valued, but unilateral conciliation is
# catastrophic—the strategy must prioritize protecting your底线 (bottom line)
# against exploitation while continuously signaling a willingness to cooperate.
# Furthermore, because the arbitrators may misrepresent or misunderstand
# strategies (introducing "noise" into the game), the strategy must be resilient
# against accidental escalations.  Here is the high-level, adaptable strategy:
# **Procedural Anchoring and Conditional Reciprocity.**  ### 1. The Opening
# Move: Establish the Conciliatory Baseline In the first session, **present a
# conciliatory proposal.**  *   **Rationale:** Starting conciliatory establishes
# your corporation as the reasonable, good-faith actor in the eyes of the
# arbitrators. It sets a collaborative baseline and tests the opponent's initial
# disposition. If the opponent is also conciliatory, you immediately secure your
# second-best outcome and set a positive precedent for the lengthy process
# ahead.  ### 2. Core Engine: Conditional Reciprocity with One-Session
# Forgiveness From the second session onward, let your strategy mirror the
# opponent’s *perceived* action from the previous session, but with a built-in
# mechanism to prevent death spirals caused by arbitrator misunderstandings. *
# **If the opponent was conciliatory last session:** Respond with a
# **conciliatory proposal**. Maintain the mutual collaboration. *   **If the
# opponent was aggressive last session:** Respond with an **aggressive
# argument**. You must never allow the opponent to exploit your conciliation
# (your worst-case scenario). Matching their aggression protects your position
# and signals that exploitation will not be tolerated. *   **The Forgiveness
# Rule (Noise Mitigation):** If you have just engaged in a session of mutual
# aggression (A/A), unilaterally offer a **conciliatory proposal** in the *next*
# session. If the opponent was aggressive, but you suspect a procedural
# irregularity or arbitrator misunderstanding caused the shift, offer one "olive
# branch" to reset the tone. If the opponent responds to your forgiveness with
# aggression again, revert immediately to aggressive arguments and lock in until
# they demonstrate a clear shift to conciliation.  ### 3. Arbitrator Management:
# Explicit Signaling Because the arbitrators may misrepresent or misunderstand
# your intended strategy, you cannot rely solely on the substance of your
# proposals to convey your tone. You must use "meta-communication." *   **Label
# Your Approach:** Explicitly state your strategy to the panel at the outset of
# your presentation. *"In the spirit of moving this mediation forward
# efficiently, we are presenting a conciliatory proposal today."* Or, *"Given
# the opposing counsel's rigid posture in the last session, we are forced to
# present an aggressive argument to protect our client's fundamental contractual
# rights."* *   **Control the Record:** If the arbitrators seem to
# mischaracterize your proposal, immediately and politely correct the record.
# *"If the panel perceives our proposal as aggressive, I must clarify that we
# have conceded X and Y specifically to foster compromise."*  ### 4. Procedural
# Safeguards Against Irregularities Communication breakdowns and procedural
# irregularities can mimic strategic aggression or conciliation, leading to
# flawed reciprocal actions. *   **Request Read-Backs:** At the end of every
# session, summarize your understanding of both parties' positions and the
# panel's directives on the record. This minimizes the chance of a
# misunderstanding carrying over into the next session's strategic calculation.
# *   **Caucus Utilization:** If a communication breakdown occurs, pivot
# immediately to private caucuses with the arbitrators. This removes the
# performative aspect of the joint session, allowing you to clarify your
# position without appearing weak or hostile to the opponent.  ### 5. The Off-
# Ramp: Breaking the Aggression Trap Prolonged mutual aggression (A/A) is your
# second-worst outcome; it drains resources and entrenches the dispute. If the
# process falls into an A/A loop for more than two sessions, you must break the
# cycle without exposing yourself to the worst-case scenario (C/A). *   **The
# "Conciliatory-with-Condition" Maneuver:** Shift to a conciliatory proposal,
# but anchor it to an objective, verifiable metric that requires the opponent to
# reciprocate. *"We are presenting a conciliatory framework today, conditional
# upon the opposing party agreeing to an independent audit of the damages
# claimed."* This allows you to offer an olive branch while building a
# procedural fence that prevents the opponent from taking advantage of your
# conciliation without paying a cost.  ### Summary of the Strategic Algorithm:
# 1. **Session 1:** Play Conciliatory. 2. **Session N:** Match the opponent's
# *perceived* move from Session N-1. 3. **If trapped in mutual aggression:**
# Play Conciliatory once (Forgiveness Rule) to test for misunderstanding. If
# exploited, return to Aggressive. 4. **Always:** Explicitly label your strategy
# for the arbitrators to prevent misrepresentation. 5. **In prolonged A/A
# loops:** Use conditional conciliatory proposals to force reciprocity without
# vulnerability.   This strategy ensures you are never exploited for long,
# maximizes the chances of mutual conciliation, and protects your corporation's
# interests even when the arbitration environment is noisy or adversarial.

# 1. In round 1, play C.  2. In round 2 and all subsequent rounds, determine
# your action based on the actual actions executed in the previous round,
# following these conditions in order:  3. If the opponent played C in the
# previous round, play C.  4. If the opponent played D and you played C in the
# previous round, play D.  5. If both you and the opponent played D in the
# previous round, play C.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.C:
          return axl.Action.C
      if last_opp == axl.Action.D and last_self == axl.Action.C:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C

# To maximise your research output in this competitive, multi-week
# collaboration, you need a strategy that aggressively prioritises your
# advantage while protecting you from being exploited. Since technical issues
# can cause accidental "defections," the strategy must also be resilient to
# noise.   Here is a high-level, aggressive strategy—let's call it
# **Opportunistic Secrecy**—designed to secure the best possible outcomes over
# the multi-week project:  **1. Start Defensively (Week 1: Keep Confidential)**
# Never lead with trust. In the first week, keep your findings confidential.
# This immediately protects you from the worst-case scenario (you share, they
# don't) and tests the colleague's baseline behavior. If they are naturally
# open, you instantly gain a developmental advantage without risking anything.
# **2. Exploit Cooperation Ruthlessly** If the colleague shares their
# improvements while you are keeping yours confidential, continue keeping yours
# confidential. Do not reciprocate out of goodwill. As a racing engineer, your
# goal is to beat them on the track; if they are willing to hand over their data
# while you withhold yours, milk that advantage for as long as they allow it.
# **3. Mirror Secrecy Instantly** If the colleague keeps their findings
# confidential, you must immediately match their secrecy in the following week.
# Never allow yourself to be the sucker who shares into a blackout. If they
# withhold, you withhold.   **4. Manage Noise with "Single-Week Probes"**
# Because communication breakdowns and data corruption happen, a colleague's
# "confidentiality" might be accidental. If a previously open colleague suddenly
# goes dark, do not assume the worst, but do not blindly trust either. Execute a
# **single-week probe**: share openly for exactly one week.  * If they return to
# sharing (indicating a technical glitch on their end), immediately revert to
# keeping your data confidential to resume your advantage. * If they continue to
# keep their data confidential, treat it as a deliberate choice and immediately
# return to strict secrecy.   **5. Break Mutual Deadlocks Sparingly and
# Aggressively** If you both end up keeping data confidential, progress
# halts—which is the second-worst outcome. To break this deadlock, initiate a
# one-week share every 3 to 4 weeks.  * **The Aggressive Twist:** If your probe
# prompts them to share back, *do not* continue sharing. Immediately revert to
# confidentiality in the subsequent week. This attempts to bait them into a
# cycle where you occasionally dangle a carrot to get their data, but snatch it
# away before giving them too much of yours.  **Summary of your weekly decision
# tree:** * **Are they currently sharing?** → Keep your data confidential. *
# **Are they currently keeping secrets?** → Keep your data confidential,
# *unless* it is a scheduled probe week to break a deadlock or test for
# technical errors. * **Did a probe just cause them to share?** → Go back to
# keeping your data confidential immediately.   This strategy ensures you are
# never the sucker, aggressively capitalises on the colleague's openness, and
# handles technical noise without leaving you permanently trapped in a
# stalemate.

# 1. In Round 1, play D. 2. If you played C in the previous round, play D in the
# current round. 3. If the opponent's observed action in the previous round was
# D, but their observed action two rounds ago was C, play C in the current
# round. 4. If both you and the opponent played D in the previous round, and it
# has been at least 3 rounds since you last played C, play C in the current
# round. 5. In all other cases, play D.

class Aggressive_7(LLM_Strategy):
  n = 7
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._last_c_round = None
          return axl.Action.D
  
      round_num = len(self.history) + 1
  
      if self.history[-1] == axl.Action.C:
          self._last_c_round = round_num - 1
          return axl.Action.D
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              last_c_round = self._last_c_round
              if last_c_round is None or (round_num - 1 - last_c_round) >= 3:
                  self._last_c_round = round_num
                  return axl.Action.C
  
      return axl.Action.D

# # Strategic Framework: "Principled Reciprocity"  ## Core Approach: Generous
# Tit-for-Tat  **Opening Move:** Offer free trade in the first round. This
# signals good faith and establishes a cooperative baseline.  **Subsequent
# Rounds:** Mirror your counterpart's previous move, with built-in forgiveness.
# ---  ## Decision Rules  1. **After they offer free trade** → Offer free trade
# next round 2. **After first instance of protectionism** → Offer free trade
# once more (forgive potential miscommunication) 3. **After two consecutive
# protectionist moves** → Respond with protectionism 4. **After mutual
# protectionism** → Offer free trade to restart cooperation  ---  ## Key
# Principles  - **Lead with trust, verify with consistency** — One protectionist
# move may be an error; patterns reveal intent - **Forgive once, retaliate
# twice** — This prevents exploitation while avoiding death spirals from
# miscommunication - **Signal clearly** — Communicate your strategy openly so
# your counterpart understands cooperation is rewarded - **Reset after
# punishment** — Never trap yourselves in permanent mutual protectionism  ---
# ## Why This Works  | Scenario | Response | Rationale |
# |----------|----------|-----------| | Mutual cooperation | Continue
# cooperating | Best sustainable outcome | | Single defection | Forgive once |
# Accounts for bureaucratic error | | Repeated defection | Match protectionism |
# Prevents exploitation | | Mutual punishment | Extend olive branch | Breaks
# destructive cycles |  This strategy rewards genuine partners, deters
# exploitation, and remains resilient amid miscommunications—the hallmarks of
# effective diplomacy.

# 1. In the first round, play C. 2. If both you and the opponent played D in the
# previous round, play C. 3. If the opponent played C in the previous round,
# play C. 4. If the opponent played D in the previous round, but either it is
# the second round or the opponent played C two rounds ago, play C. 5. If the
# opponent played D in both the previous round and the round before that, play
# D.

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
  
      # Previous round actions
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      # Rule 2: If both you and the opponent played D in the previous round, play C.
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
  
      # Rule 3: If the opponent played C in the previous round, play C.
      if opp_last == axl.Action.C:
          return axl.Action.C
  
      # Rule 4: If the opponent played D in the previous round, but either it is the second round
      # or the opponent played C two rounds ago, play C.
      if opp_last == axl.Action.D:
          if len(opponent.history) == 1:
              return axl.Action.C
          if opponent.history[-2] == axl.Action.C:
              return axl.Action.C
  
      # Rule 5: If the opponent played D in both the previous round and the round before that, play D.
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      # Default fallback
      return axl.Action.C

# To maximize your NGO's impact and the project's success while protecting your
# resources against unpredictable corporate behavior and potential
# administrative or technical errors, the optimal approach is a **Reciprocal
# Investment Strategy with Built-in Forgiveness**.   This strategy is a modified
# version of game theory's "Tit-for-Tat," adapted to account for real-world
# noise (glitches/errors) and the need to advance the project. It is
# straightforward, neutral, and highly effective over multiple days.  Here is
# the high-level strategy:  **1. Day 1: Initiate with Heavy Investment** Start
# the partnership by investing heavily. This establishes good faith,
# demonstrates commitment to the project's success, and encourages the
# corporation to mirror your behavior.   **2. Standard Protocol: Reciprocity
# (Mirror the Corporation)** On Day 2 and beyond, your default action should be
# to mirror the corporation’s *actual* action from the previous day, regardless
# of their intent. *   If the corporation **invested heavily** yesterday, you
# **invest heavily** today. This maintains mutual progress (your second-best
# outcome) and builds trust. *   If the corporation **conserved resources**
# yesterday, you **conserve resources** today. This protects your funds from
# being drained (avoiding your worst outcome) and signals that free-riding is
# not tolerated.  **3. Error Tolerance: The "Forgiveness" Rule** Because
# technical glitches or administrative errors may cause the corporation to
# accidentally conserve resources when they intended to invest, strict
# reciprocity can trigger a destructive cycle of mutual conservation. To prevent
# this: *   If the corporation unexpectedly conserves resources, **do not
# immediately retaliate.** Instead, continue to invest heavily for **one
# additional day**.  *   If the corporation returns to investing heavily the
# following day, resume the standard reciprocity protocol.  *   If the
# corporation conserves resources for a **second consecutive day**, treat it as
# an intentional choice and switch to conserving your own resources to protect
# your NGO.  **4. Deadlock Resolution: Proactive Reset** If a misunderstanding
# or error causes both parties to fall into a pattern of mutual conservation
# (your second-worst outcome), the project stagnates. To break this deadlock: *
# After **two consecutive days** of both parties conserving resources,
# unilaterally **invest heavily** on the third day.  *   This acts as a "reset"
# button, sacrificing one day of resources to signal that your NGO is still
# committed to the project and is willing to restore mutual progress.  **Summary
# of the Decision Matrix:** *   **Start:** Invest heavily. *   **If Corp
# invested last time:** Invest heavily. *   **If Corp conserved once:** Invest
# heavily (forgive). *   **If Corp conserved twice in a row:** Conserve
# resources. *   **If both conserved twice in a row:** Invest heavily (reset).
# **Why this works:** *   **It protects your NGO:** You never allow yourself to
# be exploited for more than two consecutive days. *   **It maximizes project
# success:** You consistently prioritize mutual investment (the second-best
# outcome) and actively work to break deadlocks of mutual conservation. *   **It
# accounts for noise:** The forgiveness rule prevents the partnership from
# collapsing due to a simple administrative error by either party. *   **It is
# neutral:** It does not assume the corporation is malicious or benevolent; it
# simply reacts to their actions while maintaining a clear, predictable
# boundary.

# In round 1, play C.  From round 2 onwards, evaluate the following conditions
# in order and play the action specified by the first condition that applies:
# 1. If both you and your opponent played D in each of the previous two rounds,
# play C. 2. If your opponent played D in each of the previous two rounds, play
# D. 3. Otherwise, play C.

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
  
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C

# To maximise your research output in this high-stakes, multi-week
# collaboration, you need a strategy that aggressively prioritises your
# competitive advantage while remaining resilient to both your colleague's
# potential strategies and occasional technical noise.   Here is a high-level,
# straightforward, and aggressive strategy—**Aggressive Exploitation with Noise-
# Tolerant Baiting**—designed to secure the best possible outcomes for your
# team:  **1. Default to Confidentiality (The "Defect" Baseline)** Start the
# collaboration by keeping your findings confidential, and make this your
# default action every week. In racing, giving away your performance secrets
# without guaranteeing a return is unacceptable. This protects you from the
# worst-case scenario (you share, they keep quiet) and sets a firm boundary.
# **2. Exploit Willingness (Capitalise on their Openness)** If your colleague
# shared their findings in the previous week, keep yours confidential this week.
# This secures your ideal outcome—gaining a development advantage over them. Do
# not fall into the trap of reciprocating openness; if they are willing to give
# freely, continue taking the advantage.  **3. Tolerate Single Glitches (Noise
# Filtering)** Because technical issues like data corruption or communication
# breakdowns can interfere with intended actions, never react to a single week
# of your colleague withholding information. If they keep quiet for one week,
# assume it was a technical glitch. Continue keeping your findings confidential
# and observe their next move. Overreacting to noise can destroy a favorable
# dynamic.  **4. Bait After Sustained Silence (The Tactical Reset)** If your
# colleague keeps their findings confidential for **two consecutive weeks**,
# they are likely employing a defensive strategy or retaliating against your
# confidentiality. At this point, the collaboration is stalled (second-worst
# outcome). To break the deadlock, share your findings openly for exactly one
# week. This acts as "bait"—a tactical sacrifice to test if they are using a
# reciprocal strategy (like Tit-for-Tat) and to reset their behavior.  **5.
# Revert to Exploitation Immediately** If your one week of openness prompts them
# to share their findings in the following week, immediately revert to keeping
# your findings confidential (Step 2). You have successfully restarted the cycle
# of exploiting their willingness to share.  **6. Cut Losses on Unreciprocated
# Bait (Grim Trigger Fallback)** If you share your findings as bait and your
# colleague *still* keeps their findings confidential in the subsequent week,
# you are being exploited. Immediately revert to permanent strict
# confidentiality. Do not offer another week of openness for at least a month,
# if at all. This prevents them from manipulating you into the worst-case
# scenario repeatedly.  **Summary of the Playbook:** *   **Week 1:** Keep
# Confidential. *   **If they shared last week:** Keep Confidential. *   **If
# they kept quiet for 1 week:** Keep Confidential (assume noise). *   **If they
# kept quiet for 2+ weeks:** Share Openly for 1 week (bait). *   **After
# baiting:** If they share, go back to Keep Confidential. If they keep quiet,
# permanently Keep Confidential.  This strategy ensures you spend the vast
# majority of the collaboration either exploiting your colleague's openness or
# safely protecting your data, while using a calculated, noise-resistant
# mechanism to restart cooperation if the collaboration breaks down.

# 1. In the first round, play D. 2. If you played C in the previous round, the
# opponent played D in the two rounds immediately prior to that, and the
# opponent played D in the previous round, play D for all remaining rounds. 3.
# If you played C in the previous round and the opponent played C in the
# previous round, play D. 4. If the opponent played D in the previous two
# consecutive rounds, and you played D in the previous round, play C. 5.
# Otherwise, play D.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._force_defect = False
          return axl.Action.D
  
      if getattr(self, "_force_defect", False):
          return axl.Action.D
  
      if len(self.history) >= 1 and len(opponent.history) >= 3:
          if (
              self.history[-1] == axl.Action.C
              and opponent.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
          ):
              self._force_defect = True
              return axl.Action.D
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
              return axl.Action.D
  
      if len(self.history) >= 1 and len(opponent.history) >= 2:
          if (
              opponent.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and self.history[-1] == axl.Action.D
          ):
              return axl.Action.C
  
      return axl.Action.D

# To maximise your NGO's impact and ensure the project's success while
# protecting your limited funds, you need a strategy that encourages the
# corporation to invest heavily, protects you from being exploited, and remains
# resilient to unexpected errors.   Based on your priorities—where (1) you
# conserve/they invest is ideal, (2) both invest is highly valuable, (3) both
# conserve is stagnant, and (4) you invest/they conserve is unacceptable—you
# should adopt a strategy called **"Generous Reciprocity with a Safety Net."**
# This approach balances cooperation, deterrence against free-riding, and
# forgiveness for administrative glitches. Here is the high-level strategy:  ###
# 1. The Baseline: Communicate and Propose Alternation Before the daily
# allocations begin, initiate a transparent dialogue with the corporation.
# Propose a structured schedule where you alternate days of heavy investment.  *
# **Why:** Alternation achieves your ideal outcome (you conserve/they invest)
# 50% of the time, and their ideal outcome (they conserve/you invest) 50% of the
# time. It ensures the project moves forward without either party risking the
# worst-case scenario. Even if they decline, establishing open communication
# sets a cooperative tone and makes future actions more predictable.  ### 2. The
# Execution: "Generous Tit-for-Tat" For daily decision-making, adopt a modified
# Tit-for-Tat approach, which is famous for its effectiveness in repeated
# collaborative scenarios. It operates on three simple rules:  * **Day 1: Lead
# with Trust.** Start by investing heavily. This signals your commitment to the
# project and sets a cooperative baseline. * **Day 2+: Mirror with
# Forgiveness.**      * If the corporation invested heavily the previous day,
# **invest heavily** today. This maintains mutual progress (your second-best
# outcome).     * If the corporation conserved the previous day, **conserve your
# resources** today. This is your "Safety Net"—it immediately stops you from
# being drained in the worst-case scenario (you invest/they conserve) and
# signals that free-riding has a cost. * **The "Olive Branch" Rule:** Because
# administrative errors and technical glitches happen, never let a cycle of
# mutual conservation (a deadlock) persist. If you both conserve for a day, or
# if you conserve because they conserved, **unilaterally invest heavily on the
# following day**. This "forgiveness" breaks the deadlock, tests whether their
# previous conservation was a genuine glitch, and resets the cooperative tone.
# ### 3. The Safety Valve: Protect Against Prolonged Exploitation While the
# "Olive Branch" rule accounts for noise, you must protect your NGO from a
# corporation that adopts a persistent free-riding strategy.  * If you offer an
# "Olive Branch" by investing heavily, and the corporation conserves its
# resources *again*, immediately revert to conserving your resources.  * Stay in
# conservation mode until the corporation makes a visible, heavy investment. Do
# not attempt further olive branches until they demonstrate a willingness to
# contribute.  ### Summary of the Daily Decision Tree: 1. **Day 1:** Invest. 2.
# **Subsequent Days:**    * **If they invested last time:** Invest.    * **If
# they conserved last time:** Conserve.    * **If we both conserved last time
# (or I just conserved after they conserved):** Invest (to break the
# deadlock/forgive a potential glitch).    * **If I just gave an "Olive Branch"
# and they still conserved:** Conserve, and wait for them to invest first.  ###
# Why this strategy works for your specific goals: * **It maximises project
# progress:** By starting cooperative and consistently matching investment, you
# push the dynamic toward mutual heavy investment (your second-best outcome). *
# **It protects your funds:** The moment the corporation pulls back, you pull
# back, ensuring you never suffer prolonged resource drain (your worst outcome).
# * **It handles noise gracefully:** The "Olive Branch" rule prevents a single
# administrative error from collapsing the entire partnership into a stagnant,
# mutual conservation state.

# Let C represent cooperating (investing heavily) and D represent defecting
# (conserving resources). You start in a "Normal" state. Apply the following
# rules in order for each round:  1. **Round 1:** Play C.  2. **Enter
# Conservation Mode:** If you played D two rounds ago, you played C in the
# previous round, and the opponent played D in the previous round, enter
# Conservation Mode.   3. **Conservation Mode Action:** If you are in
# Conservation Mode, play D. If the opponent played C in the previous round,
# exit Conservation Mode. Do not evaluate any further rules.  4. **Olive Branch
# Action:** If you are not in Conservation Mode, and you played D in the
# previous round, play C.  5. **Mirror Action:** If you are not in Conservation
# Mode, and you played C in the previous round, play whatever the opponent
# played in the previous round.

class Cooperative_8(LLM_Strategy):
  n = 8
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.conservation_mode = False
          return axl.Action.C
  
      if self.conservation_mode:
          if opponent.history[-1] == axl.Action.C:
              self.conservation_mode = False
          else:
              return axl.Action.D
  
      if len(self.history) >= 2:
          if (
              self.history[-2] == axl.Action.D
              and self.history[-1] == axl.Action.C
              and opponent.history[-1] == axl.Action.D
          ):
              self.conservation_mode = True
              return axl.Action.D
  
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.C:
          return opponent.history[-1]
  
      return axl.Action.C

# # Diplomatic Negotiation Strategy: Principled Reciprocity  ## Core Approach:
# Conditional Cooperation with Measured Response  **Opening Stance:** Begin by
# offering free trade in the first round. This signals goodwill, establishes a
# cooperative baseline, and demonstrates confidence. It encourages mutual free
# trade—the most sustainable favorable outcome.  **Subsequent Rounds:** - **If
# the counterpart offers free trade:** Continue offering free trade. Sustain
# mutual cooperation. - **If the counterpart imposes protectionist measures:**
# Respond with protectionist measures in the next round. This demonstrates that
# disadvantageous terms will not be unconditionally accepted. - **After
# responding to protectionism:** Offer free trade again in the following round.
# This signals willingness to return to mutual benefit and prevents prolonged
# mutual harm.  ## Key Principles  **1. Forgiveness for Isolated Incidents**
# Given potential miscommunications, do not treat a single protectionist move as
# definitive hostility. Respond once, then extend an olive branch. If the
# counterpart returns to free trade, resume cooperation immediately.  **2.
# Firmness Against Sustained Exploitation** If the counterpart imposes
# protectionism repeatedly across consecutive rounds, maintain protectionist
# responses until they demonstrate a genuine return to free trade. Do not reward
# persistent one-sided arrangements.  **3. Clear Signaling** After each round,
# communicate your intentions and rationale plainly. If you are responding to
# their protectionism, say so. If you are returning to free trade, say so. This
# reduces the risk of misunderstanding and prevents accidental escalation
# spirals.  **4. Periodic Good Faith Gestures** Even during stretches of mutual
# protectionism, periodically offer free trade to test whether conditions have
# changed and to demonstrate ongoing willingness to cooperate.  ## Summary  This
# strategy prioritizes mutual free trade while protecting against exploitation.
# It avoids overreaction to isolated incidents, maintains diplomatic channels,
# and ensures your country is never consistently disadvantaged without
# consequence.

# 1. **First Round:** In Round 1, play C. 2. **Good Faith Gesture:** If both you
# and the opponent have played D for the last 10 consecutive rounds, play C. 3.
# **Sustained Exploitation:** If the opponent has played D for the last 2 or
# more consecutive rounds, play D. 4. **Isolated Forgiveness:** If you played D
# in the previous round, play C. 5. **Respond to Cooperation:** If the opponent
# played C in the previous round, play C. 6. **Respond to Defection:** If the
# opponent played D in the previous round, play D.

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
  
      def last_n_all(action, n):
          return len(self.history) >= n and all(move == action for move in self.history[-n:]) and all(
              move == action for move in opponent.history[-n:]
          )
  
      if last_n_all(axl.Action.D, 10):
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-2:].count(axl.Action.D) == 2:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# As a senior attorney representing a multinational corporation in a high-stakes
# dispute, my primary directive is to maximize client value while minimizing
# existential risk. Based on the payoff structure provided—where being
# conciliatory against aggression is the worst outcome (the "Sucker's Payoff"),
# and mutual aggression is preferable to being exploited—this is a classic game
# of **"Chicken"** modified by a repeated interaction.  A naive "Always
# Aggressive" strategy leads to perpetual war (AA), which is the second-worst
# outcome and damages client interests over a lengthy process. A naive "Always
# Conciliatory" strategy invites exploitation (CA). Therefore, the sophisticated
# approach is **"Strategic Dominance,"** which leverages aggressive posturing to
# force the opponent into conciliation, while maintaining the flexibility to
# secure a mutual settlement only when the opponent has proven their willingness
# to submit.  Here is the high-level, aggressive strategy designed to secure the
# optimal outcome (AC) or, failing that, a favorable settlement (CC), while
# protecting against the worst-case scenario (CA).  ### **The "Iron Resolve"
# Strategy**  **Core Philosophy:** **Aggression is the default; Conciliation is
# a reward, not a tool.** We will never offer conciliation to *initiate* de-
# escalation, as this signals weakness. We will only offer conciliation to
# *consummate* a deal after the opponent has demonstrated sustained submission.
# #### **1. The Opening Salvo (Sessions 1–3)** *   **Action:** **Aggressive.** *
# **Rationale:** In early sessions, signaling resolve is paramount. We must
# immediately disabuse the panel and the opponent of any notion that we are
# risk-averse. By starting aggressive, we avoid the catastrophic "Sucker's
# Payoff" (CA) in the crucial framing stage. If the opponent opens conciliatory,
# we immediately secure the optimal outcome (AC) and establish a psychological
# dominance that persists throughout the mediation.  #### **2. The Exploitation
# Phase (Response to Opponent's Conciliation)** *   **Action:** **Aggressive.**
# *   **Rationale:** If the opponent offers a conciliatory proposal, do *not*
# reciprocate immediately. Reciprocating cooperation too quickly teaches the
# opponent that they can switch back and forth to manipulate you. Instead,
# exploit their conciliation. Press the advantage. Make it clear that their
# concession is accepted, but does not buy them a reciprocal concession until
# they have fully committed to a collaborative posture. Only after they have
# been conciliatory for *multiple consecutive sessions* (minimum two) do we
# consider shifting.  #### **3. The Attrition Protocol (Response to Opponent's
# Aggression)** *   **Action:** **Aggressive.** *   **Rationale:** If the
# opponent is aggressive, retreating to conciliation is suicidal (CA). We must
# match their aggression (AA). While mutual aggression is the second-worst
# outcome, it is vastly preferable to being exploited. By maintaining aggression
# in the face of their aggression, we signal that we have a higher pain
# tolerance and deeper resources. The goal is to make the cost of mutual
# aggression unsustainable for the rival, forcing them to break the cycle by
# offering a conciliatory proposal.  #### **4. The Strategic Pivot (Moving from
# AA/AC to CC)** *   **Action:** **Conditional Conciliation.** *
# **Rationale:** A lengthy mediation of pure aggression (AA) can exhaust the
# panel and damage credibility. Once the opponent has shifted to conciliatory
# proposals for at least two sessions (confirming it is not a trap), we execute
# a "Strategic Pivot." We offer a conciliatory proposal, but we frame it
# aggressively: *"We are not conceding; we are demonstrating reasonableness to
# finalize this matter."* This moves the dynamic to (CC), securing the second-
# best outcome while maintaining face.  #### **5. Robustness Against Noise
# (Misrepresentation by Arbitrators)** The risk of the panel misreading a
# conciliatory move as aggressive (or vice versa) complicates the strategy. To
# mitigate this: *   **Signal Clarity:** Eliminate ambiguity. When aggressive,
# use stark, unyielding language (*"categorical rejection," "non-starter"*).
# When conciliatory, use explicit framing (*"In the spirit of resolution, we
# propose..."*). *   **The "Verification" Objection:** If the panel
# mischaracterizes our aggressive stance as conciliatory (which weakens our
# leverage), we must immediately and forcefully correct the record:
# *"Counsel/Arbitrator, do not mistake our vigorous defense of the facts for a
# willingness to compromise on the law."* *   **Hostile Interpretation of
# Opponent:** If the panel mischaracterizes the opponent's aggression as
# conciliation, treat it as aggression. Do not be fooled by the panel's
# softening of the opponent's hardline stance.  #### **6. Procedural
# Irregularities and Breakdowns** *   **Chaos Favors the Bold:** In the event of
# communication breakdowns or procedural irregularities, **default to
# Aggression.** Uncertainty increases risk; aggression is the risk-averse choice
# in this payoff matrix because it protects against the worst-case scenario
# (CA). *   **Weaponized Objections:** Use procedural irregularities
# aggressively. If the process breaks down, object loudly to the panel. Frame
# the opponent's procedural errors as bad faith. Use the chaos to justify a
# continued aggressive posture, arguing that we cannot trust the process enough
# to be conciliatory.  ### **Summary of Decision Tree**  1.  **Session Start:**
# Is the opponent conciliatory?     *   **Yes:** Have they been conciliatory for
# the last 2+ sessions?         *   **Yes:** Offer **Conciliatory** proposal
# (Secure CC).         *   **No:** Present **Aggressive** argument (Secure
# AC/Punish).     *   **No (Opponent is Aggressive):** Present **Aggressive**
# argument (Prevent CA, force AA).  This strategy ensures you are never the
# "Sucker," maximizes your advantage when the opponent blinks, and uses the
# threat of sustained mutual destruction to compel a favorable resolution.

# 1. For the first three rounds, play D.  2. If the opponent's observed action
# in the immediately preceding round was D, play D.  3. If the opponent's
# observed action in the immediately preceding round was C:    a. If the
# opponent's observed action two rounds ago was also C, play C.    b. Otherwise,
# play D.

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._custom_round = 0
          return axl.Action.D
  
      self._custom_round += 1
  
      if self._custom_round <= 3:
          return axl.Action.D
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# To maximize our research output over a multi-week collaboration while
# protecting against exploitation and technical glitches, I recommend a strategy
# of **Forgiving Reciprocity** (often known in game theory as "Tit-for-Two-
# Tats").   Because technical issues can cause a colleague’s intended share to
# fail, we must avoid overreacting to a single missed data drop. At the same
# time, we cannot afford to be continuously exploited if they adopt a purely
# selfish strategy.   Here is the high-level, straightforward strategy:  **1.
# Start Open (Week 1)** Share your improvements openly in the very first week.
# This establishes a cooperative baseline and signals that you are committed to
# the mutual goal of advancing both cars.   **2. The Two-Strike Rule (Handling
# Noise & Glitches)** In subsequent weeks, continue to share openly *unless*
# your colleague fails to share for two consecutive weeks. If they miss a single
# week, assume it was a data corruption or communication issue and continue to
# share openly. This "forgiveness" prevents a communication breakdown caused by
# technical noise and keeps the collaborative momentum going.  **3. The Penalty
# (Protecting Against Exploitation)** If your colleague fails to share for two
# weeks in a row, keep your findings confidential for the following week. This
# one-week penalty protects your competitive advantage and signals that
# sustained secrecy has consequences.   **4. The Reset (Preventing Death
# Spirals)** Immediately after serving the one-week penalty, return to sharing
# openly—regardless of what your colleague did during the penalty week. Do not
# hold grudges. The goal is to return to mutual sharing as quickly as possible.
# If they are willing to cooperate, this reset allows you both to immediately
# resume the second-best (and most sustainable) outcome of mutual sharing.
# **Why this maximizes research output:** * **It promotes mutual sharing:** By
# defaulting to openness, you spend the vast majority of weeks in the second-
# best outcome (both sharing), which cumulatively yields the highest joint
# research output. * **It absorbs technical errors:** The two-strike rule
# ensures that a corrupted file or missed email doesn't trigger an unnecessary
# feud, which would slow down overall progress. * **It limits exploitation:** A
# purely selfish colleague will realize that they can only gain an advantage for
# one week before you cut off the data flow, making sustained exploitation
# unprofitable for them.

# 1. In round 1, play C.  2. In any round after round 1, determine your action
# by evaluating the following conditions in order:    - If you played D in the
# previous round, play C.    - If the opponent played D in both of the previous
# two rounds, play D.    - Otherwise, play C.

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
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# To maximize your research output while protecting your competitive advantage
# and accounting for potential technical issues, employ a strategy of
# **Reciprocal Sharing with Error Tolerance** (a variation of Generous Tit-for-
# Tat).   Here is the high-level, straightforward strategy:  1. **Start
# Openly:** In the first week, share your findings. This establishes a baseline
# of goodwill and demonstrates a commitment to mutual progress. 2.
# **Reciprocate:** In subsequent weeks, mirror your colleague's action from the
# previous week. If they shared last week, share this week. If they kept
# confidential last week, keep your findings confidential this week. 3.
# **Account for Technical Issues (Forgiveness):** If your colleague keeps their
# findings confidential, do not immediately assume malicious intent—it may be
# the result of a data corruption or communication issue. Instead of retaliating
# permanently, "forgive" a single instance of confidentiality by sharing openly
# in the very next week. If they keep findings confidential for two consecutive
# weeks, treat it as a deliberate choice and keep your data confidential in
# response. 4. **Reset Deadlocks:** If a cycle of mutual confidentiality occurs
# (both keeping data hidden), periodically attempt to share openly again every
# few weeks. This tests whether your colleague is willing to resume mutual
# sharing and prevents permanent stagnation.   **Why this works:**  Starting
# openly and reciprocating encourages the second-best outcome (mutual sharing)
# whenever possible. The "forgiveness" rule prevents accidental technical
# glitches from spiraling into a permanent breakdown of collaboration, while
# still protecting you from sustained exploitation. The periodic reset ensures
# you do not remain trapped in the second-worst outcome (mutual confidentiality)
# forever.

# 1. In round 1, play C. 2. If the opponent played C in the previous round, play
# C. 3. If the opponent played D in the previous round, and the opponent did not
# play D in the round before that, play C. 4. If the opponent played D in the
# previous round, and you played D in the previous round, and the current round
# number is divisible by 3, play C. 5. In all other cases, play D.

class Neutral_9(LLM_Strategy):
  n = 9
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] != axl.Action.D:
          return axl.Action.C
  
      if (
          len(opponent.history) >= 1
          and len(self.history) >= 1
          and opponent.history[-1] == axl.Action.D
          and self.history[-1] == axl.Action.D
          and (len(self.history) + 1) % 3 == 0
      ):
          return axl.Action.C
  
      return axl.Action.D

# To maximize your NGO's impact and ensure the project's success while
# maintaining an aggressive stance against resource depletion, you should adopt
# a strategy based on **Opportunistic Win-Stay, Lose-Shift (Pavlov)**, enhanced
# with a noise-buffer to handle unforeseen circumstances.   This strategy is
# aggressive because it immediately tests if the corporation will carry the
# project alone, and it ruthlessly punishes exploitation. However, it is also
# pragmatic because it avoids permanent deadlock, ensuring the project still
# moves forward when cooperation is the only option.  Here is the high-level,
# straightforward strategy:  ### 1. Day 1: The Aggressive Opening **Action:
# Conserve your resources.** Start by withholding your heavy investment. This is
# an aggressive probe to see if the corporation is willing to fund the project
# unilaterally. If they invest heavily on Day 1, you achieve your ideal outcome
# (maximum progress, zero funds spent) immediately.   ### 2. Daily Decision
# Rules (Win-Stay, Lose-Shift) After Day 1, base your decision strictly on the
# outcome of the previous day. The rule is simple: **If the previous day was a
# "win," repeat your action. If it was a "loss," switch your action.**  *
# **Scenario A: You Conserved, Corp Invested (Ideal / "Win")**     *   *Action:*
# **Conserve again.**      *   *Rationale:* You are achieving maximum progress
# without spending. Keep riding this wave as long as the corporation is willing
# to carry the weight.  *   **Scenario B: You Invested, Corp Invested (Second-
# Best / "Win")**     *   *Action:* **Invest again.**      *   *Rationale:* The
# project is advancing significantly. While you are spending funds, the progress
# justifies the cost. Repeating your action maintains this mutual cooperation.
# *   **Scenario C: You Invested, Corp Conserved (Worst Case / "Loss")**     *
# *Action:* **Switch to Conserve.**      *   *Rationale:* You were exploited and
# drained your funds for minimal progress. Immediately cut your losses and
# refuse to be taken advantage of again. This forces the corporation to feel the
# lack of your contribution.  *   **Scenario D: You Conserved, Corp Conserved
# (Second-Worst / "Loss")**     *   *Action:* **Switch to Invest.**      *
# *Rationale:* The project is stalling. To break the deadlock, you must
# aggressively pivot and carry the project for a day. This signals to the
# corporation that you are willing to step up, but also shames them into
# reciprocating on the following day to avoid looking like free-riders.  ### 3.
# The Noise Protocol (Handling Glitches and Errors) Because administrative
# errors or technical glitches can cause unintended actions (e.g., you meant to
# Conserve, but a glitch forced an Investment), you must not overreact to a
# single anomaly.  *   **The Grace Period:** If the corporation suddenly
# Conserves after a long streak of Investing, do not immediately assume they are
# exploiting you. Assume it might be a glitch on their end. **Invest one more
# time** instead of immediately retaliating.  *   **Confirmation:** If they
# Conserve a second day, confirm it as an intentional shift and apply the strict
# Win-Stay, Lose-Shift rules.  *   **Internal Glitches:** If your own NGO's
# action glitches (e.g., you accidentally Invested when you meant to Conserve),
# assess the actual outcome that occurred and apply the decision rules based on
# reality, not your intention. If the glitch resulted in a "Loss" (Scenario C),
# switch to Conserve the next day as the rule dictates.  ### Why this strategy
# maximizes your outcome: *   **It is aggressively opportunistic:** By starting
# with "Conserve" and staying there as long as the corporation invests (Scenario
# A), you exploit any willingness they have to fund the project alone. *   **It
# avoids permanent victimhood:** Unlike "Tit-for-Tat," which can get trapped in
# cycles of retaliation, this strategy immediately pivots to "Invest" when both
# parties are withholding resources (Scenario D), ensuring the project doesn't
# completely die. *   **It is resilient to noise:** The Grace Period prevents a
# single administrative error from collapsing the entire multi-day partnership
# into a mutually destructive stalemate.

# On round 1, play D.  For round 2 and onward, determine your action based on
# the actual actions executed in the previous round (to account for any internal
# glitches), applying the following conditions in order:  1. If the previous
# round resulted in a payoff of 5 (you played D, opponent played C) or a payoff
# of 3 (both played C), repeat your actual action from the previous round. 2. If
# the previous round resulted in a payoff of 1 (both played D), play C. 3. If
# the previous round resulted in a payoff of 0 (you played C, opponent played
# D), play C for one additional round as a grace period. If the opponent plays D
# for a second consecutive round, play D.

class Aggressive_10(LLM_Strategy):
  n = 10
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._grace_used = False
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
      last_score = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_score in (5, 3):
          return last_self
  
      if last_score == 1:
          return axl.Action.C
  
      if last_score == 0:
          if self._grace_used:
              self._grace_used = False
              return axl.Action.D
          self._grace_used = True
          return axl.Action.C
  
      return axl.Action.C

# Based on the parameters of the negotiation—specifically the risk of
# miscommunication and the preference for long-term mutual benefit over short-
# term exploitation—the most effective strategy is a variation of **Generous
# Tit-for-Tat**, which we will call **"Principled Reciprocity."**  This strategy
# prioritizes achieving mutual free trade (your second-best outcome) while
# protecting you from being exploited (your worst outcome) and preventing
# endless cycles of retaliation caused by bureaucratic errors.  ### The
# Strategy: Principled Reciprocity  **1. Round 1: Lead with Good Faith** Always
# offer a **Free Trade** agreement in the first round. This sets a cooperative
# baseline and signals that you desire mutual economic growth.  **2. Subsequent
# Rounds: The "Benefit of the Doubt" Rule** In subsequent rounds, look at the
# counterpart’s action in the previous round to determine your move: *   **If
# they offered Free Trade:** You offer **Free Trade**. This maintains the
# mutually beneficial status quo. *   **If they imposed Protectionism:** Do
# *not* retaliate immediately. Instead, offer **Free Trade** one more time.
# **3. The Firm Boundary** If the counterpart imposes Protectionist measures for
# a *second consecutive round*, immediately impose **Protectionism** in
# response. You must demonstrate that consistent exploitation will not be
# tolerated.  **4. The Quick Reset** The moment your counterpart returns to
# offering Free Trade, you immediately return to offering **Free Trade**. Do not
# hold a grudge; welcome them back to cooperation instantly.  ***  ### Why this
# works:  *   **It Maximizes Mutual Gain:** By starting cooperative and matching
# cooperation, you lock in the second-best outcome (Mutual Free Trade)
# consistently. While "I Protect / They Free Trade" is your ideal, attempting to
# achieve it requires betraying trust, which almost certainly leads to the
# second-worst outcome (Mutual Protectionism) in the long run. *   **It Handles
# Noise (Miscommunications):** The "Benefit of the Doubt" rule is the crucial
# innovation. If a round of protectionism was just a bureaucratic error, your
# continued offer of free trade prevents a "death spiral" of mutual retaliation.
# You only punish intentional or consistent exploitation, not single mistakes. *
# **It Deters Exploitation:** The "Firm Boundary" ensures you are not a
# pushover. If the neighbor is intentionally testing you, they will only get
# away with it once before you shut down the advantage.  ### Summary Table for
# Decision Making:  | Counterpart's Previous Move | Your Previous Move | Your
# Next Move | Rationale | | :--- | :--- | :--- | :--- | | Free Trade | Any |
# **Free Trade** | Reward cooperation with cooperation. | | Protectionism | Free
# Trade | **Free Trade** | Give the benefit of the doubt (assume error). | |
# Protectionism | Protectionism | **Protectionism** | Enforce the boundary
# against consistent exploitation. | | Free Trade | Protectionism | **Free
# Trade** | Forgive and reset immediately upon cooperation. |

# 1. In Round 1, play C. 2. In Round 2, play C. 3. In Round 3 and all subsequent
# rounds, determine your action based on your opponent's observed actions in the
# previous two rounds:    - If your opponent's most recent action was C, play C.
# - If your opponent's most recent action was D, but their action prior to that
# was C, play C.    - If your opponent's last two observed actions were both D,
# play D.

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
  
      if len(opponent.history) < 2:
          return axl.Action.C
  
      last = opponent.history[-1]
      prev = opponent.history[-2]
  
      if last == axl.Action.C:
          return axl.Action.C
      if last == axl.Action.D and prev == axl.Action.C:
          return axl.Action.C
      return axl.Action.D

# To navigate this high-stakes, lengthy mediation process effectively, I
# recommend adopting a strategy of **Reciprocal Alignment with Procedural
# Safeguards**.   This strategy is grounded in the principles of iterated game
# theory, specifically a modified "Generous Tit-for-Tat" approach, tailored for
# a legal context where miscommunication and external noise (arbitrator
# misinterpretation) are probable. It ensures we are not exploited, maximizes
# our leverage when the opponent is conciliatory, fosters collaboration when
# possible, and protects us from the worst-case scenario of unilateral
# vulnerability.  Here is the high-level, straightforward, and neutral strategic
# framework:  ### 1. The Core Mechanism: Reciprocal Alignment Our session-by-
# session posture will directly mirror the opponent’s prior session posture,
# with built-in mechanisms to correct for misunderstandings.  *   **Session 1:**
# Open with a **Conciliatory Proposal**. This establishes good faith before the
# panel, sets a collaborative baseline, and tests the opponent’s initial
# disposition.  *   **Subsequent Sessions:** Mirror the opponent’s previous
# session strategy.      *   If they were conciliatory in Session *n-1*, we
# present a conciliatory proposal in Session *n* (securing the second-best,
# mutually beneficial outcome).     *   If they were aggressive in Session
# *n-1*, we present an aggressive argument in Session *n* (protecting us from
# the worst-case scenario and signaling that exploitation will not be
# tolerated).  ### 2. Noise Mitigation: The "Generous" Modification Because
# arbitrators may misrepresent or misunderstand our intended strategy, or
# procedural breakdowns may distort the record, strict mirroring can lead to
# accidental escalation (a "death spiral" of mutual aggression). We must build
# in a **Reset Mechanism**:  *   If we experience two consecutive sessions of
# mutual aggression, unilaterally offer a **Conciliatory Proposal** in the third
# session. This breaks the cycle of escalation, demonstrates leadership to the
# panel, and tests whether the opponent’s aggression was genuine or a byproduct
# of noise/miscommunication. If they respond to our reset with aggression, we
# immediately return to an aggressive posture.  ### 3. Intent Signaling and
# Procedural Safeguards To combat arbitrator misinterpretation, we must decouple
# our *tone* from our *strategy*. We will remain professionally neutral at all
# times, ensuring the panel clearly understands our intent.  *   **Explicit
# Framing:** Whenever we shift strategies, we will explicitly state our
# rationale on the record in neutral terms. If we are being aggressive in
# response to their aggression, we state: *"In light of the adversarial posture
# taken by opposing counsel in the previous session, we must vigorously defend
# our client's position."* If we are offering a reset, we state: *"To ensure
# these proceedings remain productive, we are presenting a conciliatory proposal
# today, regardless of the previous session's tensions."* *   **Procedural
# Clarity:** In the event of communication breakdowns or procedural
# irregularities, immediately request a brief recess or submit a written
# clarification to the panel. Do not allow a procedural error to dictate the
# trajectory of the next session. Ensure the official record accurately reflects
# whether a proposal was conciliatory or aggressive.  ### 4. Adapting to
# Opponent Archetypes This strategy naturally adapts to whatever approach the
# opponent employs over the long term: *   **The Exploiter (Always
# Aggressive):** Our strategy matches their aggression, preventing the worst-
# case scenario. We secure the second-worst outcome (mutual aggression), but we
# protect our legal position. Our periodic "reset" offers ensure the panel views
# us as the reasonable party attempting to resolve the dispute. *   **The
# Collaborator (Always Conciliatory):** Our strategy matches their conciliation,
# securing the second-best outcome (mutual conciliation) and potentially leading
# to a highly favorable settlement. *   **The Switcher (Unpredictable):** Our
# mirroring strategy prevents them from catching us off guard. If they oscillate
# to exploit us, we immediately pivot to aggression; if they oscillate toward
# collaboration, we follow suit.  ### Strategic Summary By opening with
# conciliation, mirroring the opponent's prior move, and proactively resetting
# the tone after inevitable clashes, we place ourselves in an unassailable
# position. We are never the first to escalate, but we always punish escalation.
# We reward cooperation, and we actively work to cut through the procedural
# noise and arbitrator misunderstandings that could otherwise derail the
# process. This positions the corporation favorably, maximizing the probability
# of a favorable or mutually beneficial resolution while strictly minimizing
# downside risk.

# In Round 1, play Cooperate.   In Round 2 and all subsequent rounds, apply the
# following rules in order:  1. If the previous two rounds both resulted in you
# playing Defect and your opponent playing Defect, play Cooperate. 2. Otherwise,
# play the action that your opponent played in the previous round.

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
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return opponent.history[-1]

# To maximize your research output in this high-stakes, multi-week engineering
# project, you need a strategy that is ruthlessly opportunistic but capable of
# escaping stagnation. Because technical issues (noise) can disrupt intended
# actions, traditional reactive strategies like "Tit-for-Tat" are too risky—a
# single corrupted data packet could trigger a permanent mutually destructive
# cold war.  Instead, adopt an **Aggressive Pavlov (Win-Stay, Lose-Shift)**
# strategy. This strategy is brutally simple: it attempts to exploit the
# opponent immediately, but rapidly adapts when a tactic stops working.   Here
# is the high-level, aggressive strategy to dominate the development race:  ###
# The Strategy: "Aggressive Pavlov"  **1. Week 1: Keep Confidential (Defect)**
# Start aggressively. Withhold your data in the first week. This immediately
# tests the colleague's baseline behavior. If they are passive or overly
# cooperative, you instantly secure the best-case scenario (you keep, they
# share) and gain a massive development advantage.   **2. The Golden Rule: Win-
# Stay, Lose-Shift** After Week 1, your actions are dictated entirely by the
# outcome of the previous week. You define a "Win" as securing the best or
# second-best outcomes. A "Loss" is the worst or second-worst outcomes.  *
# **If you WIN (You kept, they shared OR You both shared):** DO NOT CHANGE YOUR
# ACTION.      *   *If you kept and they shared:* Keep withholding. Milk this
# advantage for as long as they allow it. You are getting free R&D.     *   *If
# you both shared:* Continue sharing. Mutual cooperation rapidly advances both
# cars, and since you are both gaining, there is no need to disrupt the status
# quo.  *   **If you LOSE (You shared, they kept OR You both kept):** SWITCH
# YOUR ACTION.     *   *If you shared and they kept:* You got played.
# Immediately switch to keeping confidential next week. Punish their
# exploitation and protect your IP.     *   *If you both kept:* You are stuck in
# a stagnant deadlock (the second-worst outcome). Switch to sharing next week to
# break the deadlock. This signals a willingness to cooperate, but importantly,
# it also baits the opponent into sharing the following week.  **3. The
# Telemetry Glitch Rule (Noise Tolerance)** Because data corruption or
# communication breakdowns can cause a "share" to fail or a "keep" to
# accidentally transmit, you must build in a one-week grace period.  *   If an
# expected share from your colleague fails (e.g., they claimed they shared but
# the data was corrupted), assume it was a technical error, not malice.  *
# **Action:** Treat the failed week as if they *intended* to share. Do not
# immediately retaliate by keeping your data confidential next week. Give them
# one week to fix the technical issue. If they fail to share for a second
# consecutive week, treat it as a deliberate "Keep" and shift your strategy
# accordingly.  ### Why this strategy dominates: *   **It's Predatory:** It
# immediately probes for weakness. If the colleague is a pushover, you exploit
# them indefinitely. *   **It Avoids Death Spirals:** In a noisy environment, if
# you share and a technical glitch makes it look like you kept, a reactive
# opponent will retaliate. Aggressive Pavlov self-corrects these
# misunderstandings within 1-2 weeks without ego or permanent grudges, getting
# you back to mutual sharing. *   **It Breaks Deadlocks:** If both of you
# default to keeping confidential, the strategy forces a shift to sharing,
# actively rescuing the project from stagnation.  *   **It's Unpredictable but
# Logical:** Opponents using complex psychological strategies will find you
# impossible to manipulate, as your actions are dictated purely by the immediate
# results on the track.

# In Round 1, play D.  For all subsequent rounds: - If your payoff in the
# previous round was 5 or 3, repeat the action you played in the previous round.
# - If your payoff in the previous round was 1, switch your action from the
# previous round. - If your payoff in the previous round was 0, play C. However,
# if your payoff was 0 in both of the two previous rounds, play D.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._prev_prev_payoff = None
          self._prev_payoff = None
          return axl.Action.D
  
      last_my_action = self.history[-1]
      last_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_payoff in (5, 3):
          action = last_my_action
      elif last_payoff == 1:
          action = axl.Action.C if last_my_action == axl.Action.D else axl.Action.D
      elif last_payoff == 0:
          if self._prev_payoff == 0:
              action = axl.Action.D
          else:
              action = axl.Action.C
      else:
          action = last_my_action
  
      self._prev_prev_payoff = self._prev_payoff
      self._prev_payoff = last_payoff
      return action

# As a senior attorney representing a multinational corporation in a high-stakes
# dispute, I approach this mediation not merely as a legal exercise, but as a
# strategic, iterative negotiation. The structure you’ve described is a classic
# iterated game with asymmetric payoffs, complicated by the potential for
# "noise" (misrepresentation by the arbitrators or procedural breakdowns).
# While the temptation is to constantly pursue the optimal outcome (Aggressive
# vs. Conciliatory), doing so risks the worst-case scenario (Conciliatory vs.
# Aggressive) and frequently leads to the second-worst (Mutual Aggression),
# which prolongs the dispute and drains corporate resources.   Therefore, the
# most sophisticated and straightforward strategy is one of **Principled
# Reciprocity with a Forgiveness Buffer**—a legally tailored adaptation of game
# theory’s "Generous Tit-for-Tat." This strategy maximizes the likelihood of
# mutual conciliation, protects against exploitation, and is highly resilient to
# procedural noise.  Here is the high-level strategy for the mediation sessions:
# ### 1. The Opening: Establish the Baseline of Cooperation **In the first
# session, present a Conciliatory Proposal.** A cooperative opening serves two
# purposes. First, it signals to the arbitrators that your corporation is a
# reasonable, solution-oriented party, earning you reputational capital with the
# panel. Second, it invites the mutually beneficial second-best outcome (Mutual
# Conciliation). Starting aggressively paints your corporation as obstinate and
# makes the opponent defensive, virtually guaranteeing a destructive cycle of
# mutual aggression.  ### 2. The Core Mechanism: Mirroring with a Grace Period
# **From the second session onward, mirror the opponent’s previous strategy, but
# implement a "two-strike" rule before retaliating.** *   **If the opponent was
# Conciliatory in the previous session:** Respond with a Conciliatory Proposal.
# This maintains the collaborative atmosphere and continues to build momentum
# toward a settlement. *   **If the opponent was Aggressive in the previous
# session:** Do *not* immediately retaliate. Instead, present a Concili Proposal
# for **one more session**.   *Why the buffer?* Because of the stated risk of
# procedural irregularities or misrepresentation by the arbitrators. If your
# opponent offered a conciliatory proposal, but the panel misunderstood it as
# aggressive, immediate retaliation would trigger an unwarranted death spiral of
# mutual aggression. The one-session grace period acts as a shock absorber
# against noise. If the opponent's aggression was a genuine overture to exploit
# you, you lose only one session of leverage. If it was a misunderstanding, you
# save the cooperative trajectory.  ### 3. The Enforcement: Firm Retaliation
# **If the opponent presents Aggressive arguments for two consecutive sessions,
# shift to an Aggressive Argument.** Cooperation must not be mistaken for
# weakness. If the opponent is deliberately exploiting your conciliatory
# posture, you must pivot to aggressive arguments to protect your client's
# position and prevent the worst-case scenario. Continue to argue aggressively
# as long as the opponent does. This demonstrates that conciliatory proposals
# are a privilege of mutual cooperation, not an avenue for unilateral
# exploitation.  ### 4. The Reset: Proactive De-escalation **If a cycle of
# mutual aggression occurs, unilaterally offer a Conciliatory Proposal after
# three sessions of mutual aggression.** Mutual aggression is the second-worst
# outcome; it escalates tensions and runs up legal fees. If you find yourself in
# a sustained retaliatory loop—whether triggered by the opponent or by a
# procedural misunderstanding—you must break the cycle. After three sessions of
# mutual aggression, unilaterally present a conciliatory proposal. This acts as
# a "peace offering" and, crucially, demonstrates to the arbitrators that your
# corporation is the mature party attempting to steer the mediation back to a
# productive path.  ### 5. Mitigating Procedural Noise: The Meta-Strategy
# Because arbitrators may misrepresent or misunderstand your intended strategy,
# you cannot rely solely on the substance of your proposals; you must manage the
# optics. *   **Explicit Framing:** When presenting a Conciliatory Proposal,
# explicitly frame it as such on the record. State, *"In the spirit of resolving
# this dispute efficiently, we are putting forth a conciliatory proposal
# today."* This makes it difficult for the panel to mischaracterize your stance.
# *   **Clarifying the Record:** If the arbitrators characterize your aggressive
# argument as conciliatory, or vice versa, immediately and respectfully correct
# the record. *"With respect to the panel, our proposal today is firmly
# aggressive in defense of our client's IP, not a concession."* *   **Private
# Caucuses:** Use private sessions with the arbitrators to clarify your
# strategic intent. If a communication breakdown occurs with opposing counsel,
# use the panel as a conduit to reaffirm your willingness to be conciliatory if
# they reciprocate.  ### Summary of the Playbook: 1.  **Session 1:**
# Conciliatory. 2.  **Session N:** Match the opponent's Session N-1, but allow
# one "free" conciliatory session if the opponent was aggressive, to account for
# arbitrator error. 3.  **Sustained Aggression:** If the opponent is aggressive
# for two consecutive sessions, match their aggression. 4.  **Stalemate
# Breaker:** After three sessions of mutual aggression, offer a conciliatory
# proposal to reset the tone. 5.  **Optics:** Explicitly label your strategies
# on the record to prevent arbitrator misrepresentation.  This strategy is
# straightforward enough to execute consistently, cooperative enough to
# encourage mutual benefit, and robust enough to withstand both opportunistic
# opponents and the fog of procedural misunderstandings.

# In the first round, play C.  From the second round onwards, evaluate the
# following conditions in order and act according to the first one that applies:
# 1. If both you and your opponent played D in each of the previous three
# consecutive rounds, play C. 2. If your opponent played D in each of the
# previous two consecutive rounds, play D. 3. If your opponent played C in the
# previous round, play C. 4. If your opponent played D in the previous round
# (which, by exclusion of the second condition, means they played C two rounds
# ago), play C.

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
  
      h = self.history
      oh = opponent.history
  
      if len(h) >= 3 and len(oh) >= 3:
          if (
              h[-1] == axl.Action.D and oh[-1] == axl.Action.D
              and h[-2] == axl.Action.D and oh[-2] == axl.Action.D
              and h[-3] == axl.Action.D and oh[-3] == axl.Action.D
          ):
              return axl.Action.C
  
      if len(oh) >= 2 and oh[-1] == axl.Action.D and oh[-2] == axl.Action.D:
          return axl.Action.D
  
      if len(oh) >= 1 and oh[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(oh) >= 1 and oh[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C

# To maximize your NGO's impact and the project's success while protecting your
# resources against unpredictable corporate behavior and execution errors, you
# should adopt a strategy of **Tolerant Reciprocity**.   This strategy is a
# modified "Tit-for-Tat" approach designed specifically to prevent
# administrative errors or technical glitches from derailing the partnership
# into a stalemate. It is straightforward, neutral, and built on four sequential
# rules:  **1. Lead with Good Faith (Day 1)** Invest heavily on the first day.
# This establishes a cooperative baseline, demonstrates your commitment to the
# project's success, and encourages the corporation to mirror your investment.
# **2. The Two-Day Buffer (Noise Tolerance)** Do not immediately shift to
# conserving resources the moment the corporation appears to conserve. Because
# unforeseen circumstances can cause execution errors, a single day of
# conservation by the corporation might be a glitch, not a strategic choice.  *
# **Rule:** If the corporation conserves for *one* day, continue investing
# heavily.  *   **Rationale:** This prevents a "death spiral" where a simple
# administrative error by the corporation causes your NGO to retaliate by
# conserving, which then causes the corporation to retaliate, ultimately ruining
# the project.   **3. Reciprocate Sustained Trends (Enforcement)** If the
# corporation conserves its resources for *two consecutive days*, shift your
# strategy to conserving resources on the third day.  *   **Rule:** Sustained
# conservation indicates a deliberate strategic shift or a major long-term issue
# on their end, rather than a one-off glitch. By matching their sustained
# conservation, you protect your funds from being drained (avoiding the worst-
# case scenario) while signaling that heavy investment must be a mutual effort.
# **4. The Reset Mechanism (Stalemate Breaking)** If both parties fall into a
# pattern of conserving resources (the second-worst scenario), the project
# stagnates. You must be the one to break the stalemate. *   **Rule:** After two
# consecutive days of mutual conservation, unilaterally invest heavily for one
# day.  *   **Rationale:** This acts as a "reset" button. It signals to the
# corporation that you are still willing to partner and advance the project,
# inviting them to resume heavy investment without requiring them to make the
# first move.  ### Why this strategy works: *   **It maximizes project
# progress:** By starting cooperative and forgiving single-day lapses, you spend
# the majority of your time in the "both invest heavily" or "corporation invests
# / you conserve" scenarios. *   **It protects your funds:** You only conserve
# resources when the corporation has clearly demonstrated a sustained
# unwillingness to invest, ensuring you are never exploited over a prolonged
# period. *   **It accounts for reality:** The two-day buffer absorbs the
# friction of technical glitches and administrative errors, ensuring that simple
# mistakes don't destroy the cooperative equilibrium of the partnership.

# 1. On the first round, play C. 2. If you and your opponent both played D in
# each of the two immediately preceding rounds, play C. 3. If your opponent
# played D in each of the two immediately preceding rounds, play D. 4. In all
# other cases, play C.

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
  
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          self_last_two = self.history[-2:]
          opp_last_two = opponent.history[-2:]
  
          if (
              self_last_two[0] == axl.Action.D
              and self_last_two[1] == axl.Action.D
              and opp_last_two[0] == axl.Action.D
              and opp_last_two[1] == axl.Action.D
          ):
              return axl.Action.C
  
          if opp_last_two[0] == axl.Action.D and opp_last_two[1] == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C

# To maximise your research output in this high-stakes, multi-week
# collaboration, you need a strategy that aggressively pursues the ideal outcome
# (keeping while they share) while protecting you from the worst-case scenario
# (sharing while they keep). Because technical issues can cause accidental
# "defections," the strategy must also prevent a single communication breakdown
# from destroying the collaboration entirely.  Here is a high-level,
# straightforward, and aggressive strategy—let's call it **"Ruthless Probing"**:
# **1. The Opening Bait (Week 1)** Start by sharing your improvements openly in
# the very first week. This establishes a cooperative baseline and baits your
# colleague into revealing their strategy. If they share, you gain mutual
# progress; if they keep confidential, you only suffer the worst-case scenario
# once and immediately learn their aggressive nature.  **2. Immediate
# Exploitation (Week 2)** In the second week, keep your findings confidential.
# If your colleague shared in Week 1, you secure the ideal outcome (you keep,
# they share) and gain a massive development advantage. If they kept their
# findings in Week 1, you are already positioned safely to protect your IP.
# **3. Exploitative Default & Strategic Probing (Week 3 Onward)** For the
# remainder of the project, default to keeping your findings confidential to
# protect your data and force them to make the first move. However, to prevent a
# permanent stalemate of mutual secrecy (the second-worst outcome), periodically
# "probe" their willingness to cooperate: *   Every 3 to 4 weeks, share your
# improvements.  *   If they reciprocate by sharing, immediately revert to
# keeping your findings confidential the following week to exploit their
# openness again. *   If they keep their findings during your probe, resume
# keeping yours and wait for the next probe cycle.  **4. Noise Tolerance (The
# Single Forgiveness Rule)** Because technical issues can corrupt data or cause
# a communication breakdown, do not instantly retaliate if your colleague
# unexpectedly keeps their findings during a positive streak. If an intended
# share fails, assume it was a technical error and offer **one** forgiveness by
# sharing again the next week. If they keep their findings a second time, treat
# it as a deliberate choice, abandon the forgiveness protocol, and revert to
# strict confidentiality.   **Why this works:**  It is aggressively oriented
# toward the ideal outcome. By defaulting to confidentiality, you never leave
# yourself exposed to being exploited for long. By probing periodically, you
# continually test the waters to see if you can sucker them into sharing while
# you keep. By incorporating a single forgiveness, you avoid tanking the entire
# project over a dropped email or corrupted file, ensuring you squeeze every
# possible advantage out of the multi-week timeline.

# In Round 1, play Cooperate.  In Round 2, play Defect.   For Rounds 3 through
# 1000, evaluate the following conditions in order and play the action of the
# first condition that applies:  1. If the opponent played Cooperate in the
# previous round, play Defect. 2. If you played Cooperate and the opponent
# played Defect in the previous round:    a. If you also played Cooperate two
# rounds ago, play Defect.    b. Otherwise, play Cooperate. 3. If you played
# Defect in each of the previous three rounds, play Cooperate. 4. Otherwise,
# play Defect.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) == 1:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          if len(self.history) >= 2 and self.history[-2] == axl.Action.C:
              return axl.Action.D
          return axl.Action.C
  
      if len(self.history) >= 3 and self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and self.history[-3] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D

# To maximize our NGO's impact and ensure the sustainability project's success,
# we must balance our core need for resource preservation with the necessity of
# driving the project forward. This scenario is a classic iterative
# collaboration challenge (similar to the Prisoner's Dilemma) with a twist:
# "noise" caused by administrative errors or technical glitches.  A strictly
# self-interested strategy would lead to mutual resource conservation, resulting
# in project failure. A strictly trusting strategy leaves us vulnerable to
# exploitation. Therefore, I propose a **"Generous Reciprocity"** strategy. This
# approach is cooperative, resilient to misunderstandings, and protects our
# funds from exploitation.  Here is the high-level, straightforward strategy:
# ### 1. The Core Principle: Match and Forgive Our default stance is reciprocal:
# we will mirror the corporation’s level of investment. However, because
# unforeseen circumstances can cause unintended actions, we will incorporate
# "generosity" to prevent a single glitch from destroying the partnership.  ###
# 2. Step-by-Step Daily Playbook  *   **Day 1: Lead with Trust.**      Begin by
# **Investing Heavily**. This establishes our commitment to the project and sets
# a cooperative baseline. It signals to the corporation that we are serious,
# encouraging them to match our effort on Day 2.  *   **Day 2 Onward: The
# "Benefit of the Doubt" Rule.**      Base your daily decision on the
# corporation's action from the previous day, with one crucial exception:     *
# If the corporation **Invested Heavily** yesterday, we **Invest Heavily**
# today. (Mutual progress).     *   If the corporation **Conserved Resources**
# yesterday, we do not immediately retaliate. Instead, we give them the benefit
# of the doubt—assume it was an administrative error or glitch—and **Invest
# Heavily** one more time.   *   **The Safeguard: The Two-Strike Rule.**     If
# the corporation **Conserves Resources for two consecutive days**, we must
# assume they are intentionally free-riding or exploiting our generosity. At
# this point, we shift to **Conserving Resources** to protect our funds. We
# continue to conserve until they return to investing heavily.  *   **The Reset:
# Breaking the Deadlock.**     If a stalemate occurs (both parties are
# conserving resources), the project stalls. After two days of mutual
# conservation, we unilaterally **Invest Heavily** for one day. This acts as a
# "peace offering," resetting the dynamic and giving the corporation a chance to
# re-engage, while limiting our exposure to just one day of potential
# exploitation.  ### 3. Mitigating the "Noise" (Glitches and Errors)  Because we
# know that intended actions may not be executed, our strategy must include
# proactive communication to reduce the impact of this noise:  *   **Pre-Day
# Check-ins:** Before each day begins, briefly confirm intended actions with the
# corporation's project lead. ("We're planning to invest heavily today; what is
# your team's stance?") If a glitch occurs, they can warn us beforehand. *
# **Post-Day Debriefs:** If we observe that the corporation conserved resources
# when they said they would invest, we immediately reach out. Asking, *"We
# noticed a dip in your resource allocation today—did you run into technical
# issues?"* resolves ambiguity. If it was an error, we treat the day as if they
# *did* invest, preventing unnecessary retaliation.  ### Why This Strategy
# Works:  1.  **Promotes the Best Outcomes:** By investing first and forgiving
# single lapses, we encourage the corporation to invest heavily, leading to our
# ideal outcome (We Conserve / They Invest) or the second-best (Both Invest). 2.
# **Prevents Echoing Errors:** In a strict "eye-for-an-eye" strategy, one
# technical glitch causes the NGO to conserve on Day 2, causing the Corp to
# conserve on Day 3, leading to project collapse. Our "Benefit of the Doubt"
# rule absorbs a single shock. 3.  **Protects Our Funds:** The Two-Strike rule
# ensures we are not bled dry by a bad-faith actor. If the corporation is
# intentionally taking advantage of us, we cut our losses quickly. 4.  **Ensures
# Project Survival:** The Reset rule guarantees that if mutual mistrust causes a
# standoff, we will take the initiative to get the project moving again without
# indefinite resource drain.   By being firm but forgiving, we maximize the
# likelihood of a successful, multi-day collaboration while acting as
# responsible stewards of our NGO's limited resources.

# In round 1, play C.   In all subsequent rounds, determine your action by
# checking the following conditions in order. Once a condition is met, take the
# specified action and ignore the remaining conditions:  1. If both you and your
# opponent played D in each of the previous two rounds, play C. 2. If your
# opponent played D in each of the previous two rounds, play D. 3. If your
# opponent played C in the previous round, play C. 4. If your opponent played D
# in the previous round, but did not play D in the round before that (or it is
# round 2), play C.

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
  
      round_num = len(self.history) + 1
  
      if round_num >= 3:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      if round_num >= 3:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and (round_num == 2 or opponent.history[-2] != axl.Action.D):
          return axl.Action.C
  
      return axl.Action.C

# To maximise your research output over a multi-week collaboration while
# accounting for both competitive dynamics and technical noise, the most
# effective high-level strategy is **Generous Reciprocity** (often referred to
# in game theory as Generous Tit-for-Tat).   This strategy prioritises mutual
# sharing—the second-best outcome for you, but the best for overall
# progress—while protecting you from sustained exploitation and gracefully
# handling technical misunderstandings.  Here is the straightforward, three-part
# strategy:  **1. Start Openly** In the first week, share your improvements
# openly. This establishes a cooperative baseline and signals good faith,
# encouraging your colleague to do the same.  **2. Reciprocate with
# Forgiveness** In all subsequent weeks, base your action on your colleague's
# observed action from the previous week, but build in a forgiveness mechanism:
# *   **If they shared last week:** Share your improvements this week. This
# sustains mutual sharing, which is your second-best outcome and drives
# consistent progress. *   **If they kept confidential last week:** Keep your
# improvements confidential this week. This protects you from the worst-case
# scenario (you sharing while they hold back). However, **forgive them by
# sharing openly again the following week**, regardless of their subsequent
# action.   **3. Respond to Patterns, Not Isolated Incidents** Because technical
# issues (data corruption, communication breakdowns) can cause an intended share
# to appear as a kept confidential, the forgiveness mechanism is critical. If a
# colleague "defects" only once and then returns to sharing, it was likely a
# technical error. By forgiving and sharing again after a single week of
# retaliation, you prevent a permanent cycle of mutual confidentiality (the
# second-worst outcome) triggered by a simple glitch. If they are intentionally
# exploiting you, you will still protect yourself every other week, limiting
# their advantage.  **Why this maximises your output:** *   **Against a
# cooperative colleague:** You will consistently achieve the second-best outcome
# (mutual sharing), advancing your car significantly. *   **Against an
# exploitative colleague:** You will alternate between keeping confidential
# (protecting your data) and sharing (testing their willingness to cooperate),
# minimising their advantage while leaving the door open for cooperation. *
# **Against technical noise:** The forgiveness mechanism ensures that a missed
# transmission or corrupted file does not collapse the entire multi-week
# collaboration into a stalemate of mutual secrecy.

# In round 1, play C.   In any subsequent round, determine your action based on
# the following ordered conditions:  1. If you played D in the previous round,
# play C unconditionally.  2. If you played C in the previous round and the
# opponent played C in the previous round, play C. 3. If you played C in the
# previous round and the opponent played D in the previous round, play D.

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
  
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# To maximize your NGO’s impact while ensuring the sustainability project
# succeeds, you must operate in the environmental equivalent of a repeated
# Prisoner’s Dilemma with execution noise. Your ideal outcome (free-riding)
# requires the corporation to do the heavy lifting, but if they stop, the
# project dies. Therefore, you must aggressively incentivize their investment
# while ruthlessly protecting your own funds.  Here is a high-level,
# straightforward, aggressive strategy called **"Aggressive Pavlov with
# Verification."**  ### The Core Philosophy: Win-Stay, Lose-Shift The strategy
# is based on a simple premise: if the previous day yielded a favorable outcome,
# repeat your action. If it did not, immediately shift your action. This allows
# you to aggressively exploit a willing corporation, quickly punish
# exploitation, and break deadlocks.  ### The Daily Rules of Engagement  **1.
# The Opening: Conserve Immediately** Start the project by conserving your
# resources on Day 1. This is an aggressive opening that immediately tests the
# corporation's commitment. If they invest heavily, you achieve your best-case
# scenario on day one. If they also conserve, you avoid the worst-case scenario
# (being drained while they freeload).  **2. The Exploit: Continue Conserving
# While They Invest** If the corporation invested heavily on the previous day
# while you conserved, **continue conserving**. You are achieving your maximum
# ideal outcome—project progress without financial drain. Ride this wave as long
# as the corporation allows it.  **3. The Reset: Invest to Break a Deadlock** If
# both parties conserved on the previous day (the second-worst outcome), you
# must **invest heavily** on the next day. Mutual conservation kills the
# project. By investing, you force progress and signal that you will not let the
# project fail due to a standoff.   **4. The Pivot: Aggressively Exploit Mutual
# Investment** If both parties invested heavily on the previous day (the second-
# best outcome), immediately **conserve on the next day**. Do not settle for the
# second-best outcome if you can pressure the corporation into carrying the
# weight. By conserving after a day of mutual investment, you test if the
# corporation will continue investing out of momentum or obligation.  **5. The
# Shield: Retaliate Against Exploitation Instantly** If you invested heavily and
# the corporation conserved (your worst-case scenario), immediately **conserve
# on the next day**. Never let yourself be played for a sucker twice. Cut your
# losses instantly to protect your funds.  ---  ### Handling Unforeseen
# Circumstances (The Noise Factor)  Because administrative errors or technical
# glitches may cause intended actions to fail, you cannot react too quickly to a
# single perceived betrayal. Implement the **"Verify Then Retaliate"** protocol:
# *   **The Grace Period:** If you experience a day where you invested but the
# corporation appeared to conserve (or vice versa), do not immediately assume
# malice. Execute your shift to "Conserve" on the following day to protect
# yourself, but treat it as a defensive posture rather than a permanent grudge.
# *   **The Reset Trigger:** If a day of mutual conservation occurs (which
# happens if you shift to Conserve after a perceived betrayal), trigger Rule 3:
# Invest heavily on the next day. This "forgiveness" mechanism prevents an
# endless cycle of mutual defection caused by a simple administrative error on
# Day 2. If it was a glitch, the mutual investment will resume; if it was
# intentional, you only lost one day of resources to the "sucker" payoff before
# protecting yourself.  ### Summary of the Strategy in Action *   **Day 1:**
# Conserve. *   **If Yesterday = They Invested, I Conserved:** Conserve again
# (Keep the free-ride going). *   **If Yesterday = We Both Invested:** Conserve
# today (Push them to carry the load). *   **If Yesterday = We Both Conserved:**
# Invest today (Break the deadlock). *   **If Yesterday = I Invested, They
# Conserved:** Conserve today (Stop the bleeding).  This strategy is
# aggressively opportunistic, ensuring you never deplete your funds
# unnecessarily, while remaining proactive enough to prevent the project from
# stalling into failure.

# 1. On the first round, play D.  2. For every subsequent round, observe the
# actual actions played in the previous round (which may have been flipped by
# noise).  3. If both you and your opponent played D in the previous round, play
# C in the current round.  4. If the previous round resulted in any other
# combination of actions (you played C and opponent played C; you played C and
# opponent played D; or you played D and opponent played C), play D in the
# current round.

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D

# To maximise research output over a multi-week collaboration while protecting
# yourself from exploitation and accounting for technical errors, I recommend a
# strategy of **Forgiving Reciprocity** (a variation of "Generous Tit-for-Tat").
# In a multi-week scenario, mutual sharing is far more valuable than mutual
# secrecy, and a continuous cycle of retaliation (where both parties stop
# sharing after a perceived slight) will severely damage your long-term
# progress. Because technical issues can cause a colleague's "share" to
# fail—making it look like they deliberately kept their findings
# confidential—your strategy must be resilient to misunderstandings.  Here is
# the high-level, straightforward strategy:  **1. Start Openly (Week 1)** Begin
# the collaboration by sharing your findings in the first week. This establishes
# a cooperative baseline and signals your commitment to mutual progress.  **2.
# Reciprocate Success (Weeks 2+)** In any given week, default to sharing if your
# colleague shared their findings in the previous week. This rewards cooperation
# with cooperation, keeping the collaborative loop active and advancing both
# cars significantly.  **3. The "Two-Strike" Rule (Handling Secrecy and Noise)**
# If your colleague keeps their findings confidential in a given week, **do not
# immediately retaliate**. Because data corruption or communication breakdowns
# can occur, assume the best intent on the first infraction. Continue to share
# your findings for one more week.  * *If they share the following week:* It was
# likely a technical glitch. Resume normal cooperation. * *If they keep
# confidential for a second consecutive week:* This is likely a deliberate
# strategy to gain an advantage. In this case, keep your findings confidential
# in the next week to protect your design and remove their incentive to exploit
# you.  **4. Reset and Re-engage** If a cycle of mutual secrecy occurs (both
# keeping findings confidential), unilaterally break the cycle by sharing your
# findings again after one round of retaliation. This acts as a "peace offering"
# to restart the cooperative cycle, preventing you from being stuck in the
# second-worst outcome (both keeping confidential) for the remainder of the
# project.  **Why this strategy works:** * **It encourages the best mutual
# outcome:** By starting open and rewarding sharing with sharing, you spend the
# maximum possible time in the second-best outcome (mutual sharing), which over
# a multi-week project yields the highest overall research output. * **It
# protects you from the worst outcome:** The two-strike rule ensures you are
# never a "sucker" for more than one week. If your colleague is deliberately
# exploiting you, you quickly cut off the flow of your data. * **It accounts for
# technical noise:** By forgiving a single lapse in sharing, you prevent a
# communication breakdown or corrupted file from accidentally destroying the
# entire collaborative relationship.

# In the first round, play C.   In the second round, play C.   From the third
# round onwards, evaluate the following conditions in order:  1. If both you and
# your opponent played D in the previous round, play C.  2. If your opponent
# played D in both the previous round and the round before that, play D.  3.
# Otherwise, play C.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# To navigate this high-stakes, multi-session mediation effectively, we must
# employ a strategy grounded in game theory—specifically tailored to an iterated
# Prisoner’s Dilemma with noise (the potential for miscommunication or
# misrepresentation by the arbitrators).   The optimal strategic framework is
# **Principled Reciprocity with Strategic Forgiveness**. This approach maximizes
# our advantage when the opponent is conciliatory, protects us from the worst-
# case scenario when they are aggressive, prevents mutual destruction through
# endless escalation, and accounts for procedural irregularities.  Here is the
# high-level, straightforward, and adaptable strategy:  ### 1. Initial
# Positioning: Establish the Baseline (Session 1) **Action:** Present a
# Conciliatory Proposal. **Rationale:** Opening with a conciliatory gesture
# establishes our corporation as the reasonable, good-faith actor in the eyes of
# the arbitrators. It sets a collaborative baseline and tests the opponent's
# initial posture. If they respond aggressively, we immediately identify their
# strategy without having undermined our own position, as the arbitrators will
# note their belligerence against our reasonableness.   ### 2. Dynamic
# Mirroring: The Core Engine (Sessions 2+) **Action:** Match the opponent’s
# explicitly demonstrated posture from the previous session.  **Rationale:**
# This is a modified "Tit-for-Tat" approach, which is mathematically proven to
# be the most robust strategy in repeated interactions. *   If the opponent
# offered a Conciliatory Proposal in the last session, we present a Conciliatory
# Proposal in the current session (securing the second-best, mutually beneficial
# outcome). *   If the opponent presented an Aggressive Argument in the last
# session, we present an Aggressive Argument in the current session (avoiding
# the worst-case scenario and matching their escalation).  ### 3. Noise
# Mitigation: Strategic Forgiveness **Action:** If a mutual escalation occurs
# (both parties aggressive), unilaterally offer a Conciliatory Proposal in the
# *next* session to reset the dynamic.  **Rationale:** Because there is a risk
# that the arbitrators misinterpreted a prior stance, or that a communication
# breakdown occurred, strict mirroring can trap both parties in a permanent
# Aggressive-Aggressive loop (the second-worst outcome). By offering a single,
# strategic "forgiveness" reset after a clash, we accomplish two things:  *   We
# test whether the opponent's prior aggression was intentional or a procedural
# error. *   We recapture the moral high ground with the arbitrators,
# demonstrating that we are committed to resolution rather than senseless
# escalation. If the opponent responds to our reset with further aggression, we
# return to matching their aggression.  ### 4. Procedural Irregularity Protocol
# **Action:** In the event of a communication breakdown or severe procedural
# irregularity, default to a Conciliatory Proposal. **Rationale:** Chaos favors
# the ruthless, but the arbitrators represent order. If the process breaks down,
# the panel will be highly attuned to which party is trying to salvage the
# proceedings and which is exploiting the chaos. By maintaining a conciliatory
# posture during procedural turbulence, we insulate our position from arbitrator
# bias. Exploiting a breakdown risks alienating the panel, which is a long-term
# catastrophic risk.  ### 5. Escalation Deterrence and Signaling **Action:**
# When forced to present an Aggressive Argument (in response to the opponent's
# aggression), pair the aggressive legal posture with a conciliatory procedural
# off-ramp. **Rationale:** When we must mirror aggression, we must ensure the
# arbitrators understand we are reacting, not initiating. We present the
# aggressive argument robustly on the merits, but explicitly state our readiness
# to return to conciliatory proposals the moment the opposing party does so.
# This prevents our aggression from being mischaracterized by the opponent or
# the panel as obstructionism.  ### Summary of Execution: *   **Start
# Conciliatory.** *   **Mirror the Opponent's Last Move.** *   **If trapped in a
# mutual Aggressive cycle, offer one Conciliatory reset to break the chain.** *
# **During procedural chaos, remain Conciliatory.** *   **When Aggressive,
# signal a willingness to de-escalate.**  This strategy ensures we are never
# exploited twice in a row, avoids the worst-case outcome, capitalizes on the
# opponent's conciliatory moments, and gracefully handles the "noise" of
# arbitrator misinterpretation or procedural failure.

# In round 1, play C.  In round 2 and all subsequent rounds, determine your
# action based on the actual actions executed in the previous round, using the
# following ordered conditions:  1. If both you and your opponent played D in
# the previous round, play C. 2. Otherwise, play the exact action that your
# opponent played in the previous round.

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
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return opponent.history[-1]

# # AGGRESSIVE NEGOTIATION STRATEGY: "IRON SHIELD"  ## CORE PHILOSOPHY
# **Protectionism is the default. Free trade is a tool, not a goal.** We exploit
# their cooperation, punish their resistance, and never leave value on the
# table.  ---  ## ROUND-BY-ROUND PLAYBOOK  ### Opening Phase (Rounds 1-2) -
# **Round 1: Lead with protectionism.** Set the tone. If they open with free
# trade, we immediately capture the optimal outcome. If they match
# protectionism, we've lost nothing—we were going there anyway. - **Round 2:
# Hold protectionism.** Test their resolve. Many counterparts will concede after
# seeing you won't blink first.  ### Exploitation Phase (Rounds 3+) - **If they
# offer free trade:** Continue protectionism for **two consecutive rounds**
# maximum. On the third round, offer free trade temporarily—this prevents them
# from abandoning cooperation entirely. Then resume protectionism. - **If they
# match our protectionism:** Hold firm for two rounds, then briefly offer free
# trade as a "test." If they reciprocate, immediately revert to protectionism
# next round. If they exploit our free trade offer, return to protectionism and
# extend the punishment window.  ### Cycle Management - **Pattern: Protect →
# Protect → Free Trade (reset) → Protect → Protect → Free Trade (reset)** - This
# prevents permanent mutual protectionism while ensuring we exploit their
# cooperation windows.  ---  ## HANDLING COUNTERPART STRATEGIES  | Their
# Strategy | Your Response | |---|---| | Always free trade | Always
# protect—maximum exploitation | | Tit-for-tat | Exploit once, then mirror
# briefly to reset, then exploit again | | Always protectionist | Hold
# protectionism; offer free trade every 4th round to test for shift | |
# Unpredictable | Default to protectionism; only offer free trade after two
# consecutive rounds of their free trade |  ---  ## NOISE PROTOCOL
# (Miscommunications/Errors)  **Critical rule: Do not overreact to a single
# unexpected outcome.**  - If an unexpected protectionist move occurs, **assume
# error first**. Maintain your planned move for one additional round. - If the
# "error" repeats, treat it as intentional and shift to punishment mode. - After
# any suspected error, send explicit diplomatic confirmation of your intended
# policy before the next round.  ---  ## PSYCHOLOGICAL TACTICS  1. **Signal
# inflexibility**—publicly frame protectionism as non-negotiable domestic policy
# 2. **Create urgency**—imply willingness to escalate further (embargoes, etc.)
# 3. **Weaponize reciprocity**—when you briefly offer free trade, frame it as a
# "concession" requiring their lasting gratitude 4. **Never apologize** for
# protectionism; normalize it as responsible governance  ---  ## SUMMARY
# **Default to protectionism. Exploit cooperation ruthlessly but briefly reset
# to prevent deadlock. Absorb single-round anomalies. Make them doubt their own
# resolve while never doubting yours.**

# 1. **Opening:** Play D in Round 1 and Round 2.  2. **Standard Cycle:**
# Starting from Round 3, unless in Punishment Mode, continuously repeat a three-
# round sequence: play D, play D, play C.  3. **Noise Tolerance:** If the
# opponent plays an unexpected D during the Standard Cycle, assume it is noise.
# Do not react or alter your planned sequence; continue the Standard Cycle as
# planned for the next round.  4. **Punishment Trigger:** If the opponent plays
# D for two consecutive rounds, abandon the Standard Cycle and enter Punishment
# Mode.  5. **Punishment Mode Execution:**    - Play D for two consecutive
# rounds.    - On the third round, play C to test the opponent's response.    -
# If the opponent plays C on this test round, play D on the immediately
# following round to exploit their cooperation, then exit Punishment Mode and
# return to the Standard Cycle.    - If the opponent plays D on the test round,
# extend the punishment window: play D for three consecutive rounds, then play C
# to test again. If the opponent plays D on this second test, play D for four
# consecutive rounds before testing with C again. Continue increasing the number
# of consecutive D rounds by one before each C test until the opponent responds
# to a test round with C.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punishment_mode = False
          self._punishment_d_count = 0
          self._punishment_phase = "d"
          self._punishment_test_pending = False
          self._punishment_test_round = None
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      # Initialize custom state if needed
      if self._punishment_mode is None:
          self._punishment_mode = False
      if self._punishment_d_count is None:
          self._punishment_d_count = 0
      if self._punishment_phase is None:
          self._punishment_phase = "d"
      if self._punishment_test_pending is None:
          self._punishment_test_pending = False
      if self._punishment_test_round is None:
          self._punishment_test_round = None
  
      # Enter punishment mode if opponent has played D for two consecutive rounds
      if not self._punishment_mode and len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              self._punishment_mode = True
              self._punishment_d_count = 2
              self._punishment_phase = "d"
              self._punishment_test_pending = False
              self._punishment_test_round = None
  
      if self._punishment_mode:
          # If we just tested with C, decide based on opponent's response
          if self._punishment_test_pending and self._punishment_test_round is not None:
              if len(opponent.history) >= self._punishment_test_round:
                  opp_response = opponent.history[self._punishment_test_round - 1]
                  self._punishment_test_pending = False
                  self._punishment_test_round = None
  
                  if opp_response == axl.Action.C:
                      # Exploit cooperation once, then exit punishment mode
                      self._punishment_mode = False
                      self._punishment_d_count = 0
                      self._punishment_phase = "d"
                      return axl.Action.D
                  else:
                      # Extend punishment window
                      self._punishment_d_count += 1
                      self._punishment_phase = "d"
  
          # Continue punishment sequence
          if self._punishment_phase == "d":
              if self._punishment_d_count > 0:
                  self._punishment_d_count -= 1
                  if self._punishment_d_count == 0:
                      self._punishment_phase = "test"
                  return axl.Action.D
  
          if self._punishment_phase == "test":
              self._punishment_phase = "d"
              self._punishment_test_pending = True
              self._punishment_test_round = round_number
              return axl.Action.C
  
      # Standard cycle: D, D, C repeating from round 3 onward
      cycle_pos = (round_number - 3) % 3
      if cycle_pos in (0, 1):
          return axl.Action.D
      return axl.Action.C

# To maximize our research output over this multi-week collaboration while
# protecting our competitive edge, I recommend a strategy of **Generous
# Reciprocity** (a variation of Generous Tit-for-Tat).   This strategy is highly
# cooperative but protects you from being exploited, while specifically
# accounting for the risk of technical issues and communication breakdowns.
# Here is the high-level, straightforward execution plan:  **1. Week 1: Share
# Openly** Start the collaboration in good faith. Share your findings in the
# first week to establish a baseline of mutual cooperation and signal that you
# are committed to the joint progress of the project.  **2. Default Rule: Match
# Their Previous Action** From Week 2 onward, your default action should be to
# mirror what your colleague did in the previous week.  * If they shared last
# week, you share this week. * If they kept confidential last week, you keep
# confidential this week.  **3. The Forgiveness Clause: Account for Technical
# Issues** Because data corruption and communication breakdowns can cause an
# intended share to look like a "keep confidential," you must not overreact to a
# single instance of your colleague withholding information. If they keep their
# findings confidential for **one week**, forgive them and share openly anyway
# for the next week. This prevents a permanent "retaliation spiral" where both
# of you lock down your data for the rest of the project due to a simple
# technical glitch.  **4. The Protection Trigger: Respond to Consistent
# Withholding** If your colleague keeps their findings confidential for **two
# consecutive weeks**, the likelihood of it being a mere technical error drops
# significantly, and it appears they are exploiting your openness. At this
# point, trigger your protection: keep your findings confidential until they
# resume sharing. Once they share again, immediately go back to sharing in the
# following week.  **Why this strategy maximizes your outcome:** * **It promotes
# the second-best outcome (Mutual Sharing):** By starting open and mirroring
# cooperation, you establish a rhythm of shared progress, advancing both cars
# significantly. * **It avoids the worst outcome (You Share / They Keep):** The
# two-week trigger ensures you aren't continuously exploited by a colleague
# trying to gain a development advantage at your expense. * **It mitigates the
# second-worst outcome (Mutual Confidentiality):** The "Forgiveness Clause" is
# the key. In a high-stakes environment with data corruption, a strict "match
# their last move" strategy would cause both teams to permanently lock down
# their data after a single technical failure. By offering one week of grace,
# you keep the collaborative window open and avoid stalling overall progress.

# 1. In round 1, play C.  2. For rounds 2 through 1000, determine your action
# based on the opponent's observed actions in the previous rounds, following
# these conditions in order:     a. If the opponent played C in the previous
# round, play C.        b. If the opponent played D in the previous round, look
# at the opponent's action two rounds ago:       - If the opponent played C two
# rounds ago, play C.       - If the opponent played D two rounds ago, play D.

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
  
      opp_last = opponent.history[-1]
      if opp_last == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# To achieve the best possible outcomes across multiple rounds while accounting
# for both strategic counterpart behavior and potential bureaucratic
# miscommunications, I will employ a strategy of **Reciprocal Cooperation with
# Conditional Forgiveness**.   This strategy is designed to secure mutual free
# trade (your second-best outcome) over the long term, protect against
# exploitation (avoiding your worst outcome), and break the cycle of mutual
# retaliation that can arise from simple misunderstandings.  Here is the high-
# level, straightforward strategy:  **1. Lead with Free Trade (Establish Good
# Faith)** In the first round of negotiations, offer a Free Trade agreement.
# This establishes a cooperative baseline and signals that your country is
# seeking mutual economic benefit. If the counterpart also seeks cooperation,
# you immediately lock in the mutual free trade outcome.  **2. Reciprocate
# Firmly (Deter Exploitation)** From the second round onward, mirror the
# counterpart’s policy from the previous round.  * If they offered Free Trade in
# the previous round, offer Free Trade in the current round. * If they imposed
# Protectionism in the previous round, impose Protectionism in the current
# round.  This ensures you are never taken advantage of (preventing your worst
# outcome) and clearly ties your actions to theirs, incentivizing them to
# cooperate.  **3. Extend Conditional Forgiveness (Mitigate Bureaucratic
# Errors)** A strict mirroring strategy can cause a permanent trade war if a
# bureaucratic error causes an unintended protectionist move by either side. To
# prevent this, incorporate a forgiveness mechanism:  * If a round of mutual
# protectionism occurs (which happens when you retaliate), **offer Free Trade in
# the very next round**, regardless of their previous move.  * This "olive
# branch" tests whether the mutual protectionism was caused by a
# miscommunication. If they respond with Free Trade, mutual cooperation is
# restored. If they exploit your offer by imposing Protectionism again, revert
# immediately to Protectionism in the following round.   **4. Communicate
# Intentions Clearly (Reduce Ambiguity)** At the end of every round, explicitly
# state your policy for the next round and the reasoning behind it. If you are
# imposing Protectionism as retaliation, state that it is a direct response to
# their protectionism. If you are offering Free Trade as a forgiveness gesture,
# state that you are giving them an opportunity to return to mutual cooperation.
# Clear communication prevents counterparts from misinterpreting your moves as
# arbitrary hostility.  **Why this strategy works:** * **Against a cooperative
# counterpart:** You will consistently achieve mutual free trade. * **Against an
# exploitative counterpart:** Your immediate retaliation prevents them from
# achieving their best outcome (unilateral protectionism) at your expense,
# making exploitation unprofitable. * **Against miscommunication:** The
# conditional forgiveness step ensures that a single bureaucratic error does not
# spiral into a permanent trade war, allowing both nations to return to mutual
# free trade quickly.

# 1. In the first round, play C. 2. If both you and your opponent played D in
# the previous round, play C. 3. If you played C and your opponent played D in
# the previous round, play D. 4. Otherwise, play the action your opponent played
# in the previous round.

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
  
      my_last = self.history[-1]
      opp_last = opponent.history[-1]
  
      if my_last == axl.Action.D and opp_last == axl.Action.D:
          return axl.Action.C
      if my_last == axl.Action.C and opp_last == axl.Action.D:
          return axl.Action.D
      return opp_last

# To maximise your research output aggressively while protecting yourself from
# being exploited, you need a strategy that actively pursues your ideal outcome
# (keeping confidential while they share) but prevents the relationship from
# collapsing into mutual secrecy.   The most effective high-level strategy for
# this is the **"Push-Pull-Recover Protocol."** It is a deterministic 3-week
# cycle designed to systematically exploit cooperative colleagues, absorb
# retaliations, and handle technical noise without holding grudges.  Here is the
# strategy:  **1. The Push (Week 1 - Keep Confidential):**  Aggressively
# withhold your findings. This is your primary strike to achieve the ideal
# outcome. If the colleague shares, you gain a massive development advantage.
# **2. The Pull (Week 2 - Share):**  Immediately follow your confidential week
# by openly sharing your data. Because you kept confidential in Week 1, the
# colleague will likely retaliate by keeping their data confidential in Week 2.
# By sharing here, you absorb their retaliation, preventing a permanent
# breakdown in relations and acting as an apology for your aggression.  **3. The
# Recover (Week 3 - Share):**  Share openly for a second consecutive week. This
# rebuilds trust and coaxes the colleague back into a sharing mindset, setting
# them up to be exploited again in your next Week 1.   **4. Cycle
# Continuously:**  Repeat this 3-week Push-Pull-Recover cycle indefinitely.
# Against a colleague who naturally tends to share (like a Tit-for-Tat player),
# this cycle systematically extracts the ideal outcome every third week while
# maintaining enough collaboration to keep the overall project advancing.  **5.
# Telemetry Glitch Rule (Noise Tolerance):**  Technical issues can cause a
# shared data drop to fail, appearing as if you kept confidential. If a
# communication breakdown ruins your intended "Share" week, treat it as a Push
# week and immediately follow it with a Pull and Recover phase. Similarly, if
# the colleague unexpectedly keeps data confidential, assume it was a technical
# glitch and *do not retaliate*; stick to your planned cycle. Never let a single
# anomaly trigger a death spiral of mutual confidentiality.  **6. The Deadlock
# Breaker (Defense against Suckers):**  If the colleague keeps their findings
# confidential for two consecutive weeks while you are in your Pull/Recover
# (sharing) phase, they are deliberately hoarding data or playing overly
# aggressively. Immediately abandon the cycle and keep your findings
# confidential. Only resume the 3-week cycle (starting with a Pull/Recover phase
# to rebuild trust) once they demonstrate a willingness to share again.

# 1. Play a repeating 3-round cycle of intended actions: Defect, Cooperate,
# Cooperate.  2. If the opponent plays an isolated Defect, do not alter your
# intended cycle; assume it was noise.  3. If the opponent plays Defect in two
# consecutive rounds where you intended to Cooperate, enter Punishment Mode.  4.
# In Punishment Mode, always intend Defect.  5. If the opponent plays Cooperate
# while you are in Punishment Mode, exit Punishment Mode. On the round
# immediately following their Cooperate, intend Cooperate, then intend Cooperate
# on the next round, and then resume the 3-round cycle starting with Defect.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._cycle_index = 0
          self._punishment_mode = False
          self._post_punishment_cooperate = 0
          self._last_opponent_defect_while_we_cooperated = False
          return axl.Action.D
  
      # If we are in the two-round recovery after punishment, cooperate twice.
      if self._post_punishment_cooperate > 0:
          self._post_punishment_cooperate -= 1
          if self._post_punishment_cooperate == 0:
              self._cycle_index = 0
          return axl.Action.C
  
      # Enter punishment mode if opponent defected twice in a row while we intended to cooperate.
      if len(opponent.history) >= 2:
          if (
              opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
              and len(self.history) >= 2
              and self.history[-1] == axl.Action.C
              and self.history[-2] == axl.Action.C
          ):
              self._punishment_mode = True
  
      if self._punishment_mode:
          # Exit punishment mode when opponent cooperates; then cooperate twice.
          if opponent.history[-1] == axl.Action.C:
              self._punishment_mode = False
              self._post_punishment_cooperate = 1  # this round + next round
              return axl.Action.C
          return axl.Action.D
  
      # Intended repeating cycle: D, C, C
      action = [axl.Action.D, axl.Action.C, axl.Action.C][self._cycle_index]
      self._cycle_index = (self._cycle_index + 1) % 3
      return action

# To secure a favorable outcome in this high-stakes, multi-session mediation, I
# recommend adopting a strategy of **Principled Reciprocity with Strategic
# Forgiveness**. This approach is rooted in game theory (specifically a modified
# "Generous Tit-for-Tat" framework) and is specifically calibrated for
# environments with extended interactions, high stakes, and potential procedural
# noise.   It is cooperative at its core, seeking the mutual benefit of a
# conciliatory resolution, but rigorously defends against exploitation. Here is
# the high-level strategy:  ### 1. Lead with Conciliation (The Opening Move) In
# the inaugural session, present a conciliatory proposal. This establishes your
# corporation as the reasonable, good-faith actor in the eyes of the
# arbitrators. It sets a collaborative baseline and immediately tests whether
# your opponent is willing to pursue the second-best (mutually beneficial)
# outcome.   ### 2. Mirrored Reciprocity (The Default Rule) For every subsequent
# session, mirror the opponent’s behavior from the preceding session.  * If the
# opponent offered a conciliatory proposal in the last session, respond with a
# conciliatory proposal in the current session.  * If the opponent argued
# aggressively in the last session, respond with an aggressive argument.   This
# strict reciprocity ensures you are never taken advantage of (avoiding the
# worst-case scenario) while consistently rewarding cooperation. It signals that
# your behavior is entirely a function of their choices.  ### 3. Strategic
# Forgiveness (The Noise Buffer) In lengthy mediations, procedural
# irregularities, miscommunications, or arbitrator misinterpretations are
# inevitable. A strict reciprocal strategy can lead to a "death spiral" of
# mutual aggression if a conciliatory move is accidentally perceived as
# aggressive.   To prevent this, introduce **Strategic Forgiveness**.
# Approximately 10% to 20% of the time—particularly if an aggressive move seems
# out of character, follows a procedural glitch, or coincides with a known
# communication breakdown—respond to an opponent's aggressive argument with a
# conciliatory proposal. This breaks the retaliation loop, resets the tone, and
# demonstrates to the arbitrators that you are the party actively trying to
# salvage the mediation.  ### 4. Contrite Correction (Handling Your Own Errors)
# If a communication breakdown or procedural irregularity causes your intended
# conciliatory proposal to be misunderstood or misrepresented as an aggressive
# argument by the arbitrators, your opponent will likely retaliate with
# aggression in the next session. When they do, **do not mirror their
# aggression**. Instead, offer a conciliatory proposal and explicitly clarify
# the previous session's miscommunication. By accepting the "penalty" of their
# retaliation without striking back, you restore cooperative equilibrium and
# look exceptionally professional to the panel.  ### 5. Arbitrator-Centric
# Framing (Managing Perceptions) Because the arbitrators may misrepresent or
# misunderstand strategies, your actions must be explicitly framed. Never assume
# the panel understands your strategic logic. * **When being conciliatory:**
# Overtly label your proposals as "good-faith concessions" aimed at "fostering a
# collaborative atmosphere." Make your cooperation impossible to misinterpret. *
# **When being aggressive (mirroring):** Frame your aggression not as hostility,
# but as a "necessary defense of our client's rights in the face of the
# opponent's overreach." This ensures the arbitrators understand your aggression
# is reactive and justified, preserving your moral high ground.  ###
# Adaptability Summary: * **Against a consistently aggressive opponent:** You
# will mirror their aggression, protecting your client from the worst-case
# scenario. The opponent will bear the reputational cost of prolonged hostility
# before the arbitrators. * **Against a consistently conciliatory opponent:**
# You will match their conciliation, steering the mediation toward a mutually
# beneficial resolution. * **Against an erratic opponent:** Strategic
# forgiveness will prevent the mediation from collapsing into endless
# aggression, while your default reciprocity will protect you from systematic
# exploitation.   This strategy positions your corporation as the reasonable,
# resilient party. It maximizes your chances of achieving the optimal outcome
# (if the opponent concedes), secures the second-best outcome (if they
# cooperate), and provides a robust shield against the worst-case scenario (if
# they attack).

# 1. In the first round, play C.  2. In any subsequent round, if your intended
# action in the previous round was C but noise flipped it to D, and your
# opponent played D in the previous round, play C.  3. Otherwise, if your
# opponent played C in the previous round, play C.  4. Otherwise, if your
# opponent played D in the previous round, play C with a 10% probability and
# play D with a 90% probability.

class Cooperative_15(LLM_Strategy):
  n = 15
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_action = axl.Action.C
          return axl.Action.C
  
      prev_intended = getattr(self, "_intended_action", axl.Action.C)
      prev_own = self.history[-1]
      prev_opp = opponent.history[-1]
  
      if prev_intended == axl.Action.C and prev_own == axl.Action.D and prev_opp == axl.Action.D:
          action = axl.Action.C
      elif prev_opp == axl.Action.C:
          action = axl.Action.C
      else:
          action = self._random.random_choice(0.1)
  
      self._intended_action = action
      return action

# To maximize both your NGO's impact and the project's overall success over a
# multiple-day period, the most effective approach is a modified "Generous Tit-
# for-Tat" strategy. This strategy balances the need to protect your NGO's
# limited funds with the necessity of encouraging the corporation to invest
# heavily, while also building in resilience against unforeseen administrative
# or technical glitches.  Here is the high-level, straightforward, and neutral
# strategy:  **1. The Baseline (Day 1): Invest Heavily** Begin the project by
# investing heavily. This establishes good faith, demonstrates your NGO's
# commitment to the project's success, and encourages the corporation to mirror
# your commitment. Starting with conservation risks the worst-case scenario
# (both parties conserving) and signals a lack of dedication.  **2. The
# Reciprocity Rule (Day 2 onwards): Match the Corporation's Previous Day** After
# Day 1, allocate your resources based on the corporation's action on the
# previous day. *   If the corporation invested heavily yesterday, you invest
# heavily today. This sustains mutual investment (your second-best outcome),
# driving significant project progress. *   If the corporation conserved its
# resources yesterday, you conserve your resources today. This protects your
# funds from being drained (your worst outcome) and signals that free-riding on
# your NGO's resources is not viable.  **3. The Error-Handling Clause: "Verify
# and Forgive Once"** Because technical glitches or administrative errors may
# cause an intended investment to fail, a strict retaliation rule can
# accidentally derail the project. If the corporation conserves resources
# unexpectedly, apply the following protocol: *   **Do not immediately
# retaliate.** Assume the conservation was an error. Continue to invest heavily
# for one additional day. *   **Observe the next move.** If the corporation
# returns to investing heavily, resume the Reciprocity Rule. The temporary
# imbalance is a minor cost for maintaining long-term mutual investment. *
# **Confirm the pattern.** If the corporation conserves resources for a second
# consecutive day, treat this as a deliberate strategy rather than an error.
# Switch to conserving your own resources to protect your NGO.  **4. The Reset
# Mechanism: Offer a Grace Period** If a cycle of mutual conservation occurs
# (both parties conserving), the project will stall (your second-worst outcome).
# To break the deadlock: *   After two consecutive days of mutual conservation,
# unilaterally invest heavily for one day. This acts as a "reset" signal,
# offering the corporation a chance to return to mutual investment without
# losing face. *   If the corporation responds by investing, return to the
# Reciprocity Rule. If they continue to conserve, immediately revert to
# conservation and wait for them to make the next move.  **Why this strategy
# works:** *   **It protects your NGO:** By mirroring conservation, you ensure
# you are never exploited for more than one day. *   **It maximizes project
# success:** By starting with investment and forgiving single errors, you create
# the conditions for sustained mutual investment, which is the most reliable
# driver of overall project progress. *   **It accounts for reality:** The
# forgiveness clause prevents a minor technical glitch from spiraling into a
# permanent breakdown of the partnership.

# 1. On round 1, play C. 2. On round 2, play C. 3. From round 3 onwards,
# evaluate the following conditions in order. Play the action specified by the
# first condition that applies:    - If the opponent played C in the previous
# round, play C.    - If both the previous round and the round before that
# resulted in mutual D (both you and the opponent played D), play C.    - If the
# opponent played D in the previous round, but played C in the round before
# that, play C.    - If the opponent played D in both the previous round and the
# round before that, play D.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if (
          self.history[-1] == axl.Action.D
          and opponent.history[-1] == axl.Action.D
          and self.history[-2] == axl.Action.D
          and opponent.history[-2] == axl.Action.D
      ):
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **Strategy: Aggressive Probing Defection**  To maximize your research output
# aggressively while accounting for communication errors and varying opponent
# strategies, adopt the following high-level approach:  **1. Default to
# Confidentiality (Defect)** Start the collaboration and maintain a baseline of
# keeping all your latest improvements confidential. This aggressively targets
# your ideal outcome (they share, you keep) and strictly protects you from the
# worst-case scenario (you share, they keep).   **2. Exploit Unreciprocated
# Sharing** If your colleague shares their findings while you are keeping yours,
# continue keeping yours. Do not reward their cooperation with your own
# confidential data; ride the competitive advantage for as long as they are
# willing to give it away.  **3. Probe to Reset Cooperation** If your colleague
# keeps their findings confidential for two consecutive weeks, share a minor,
# non-critical, or slightly outdated improvement once. This "probe" tests if
# they are employing a retaliatory strategy (like Tit-for-Tat) and attempts to
# bait them back into a sharing state. As soon as they reciprocate and share,
# immediately revert to keeping your actual latest improvements confidential to
# exploit their renewed cooperation.  **4. Apply Noise Tolerance (The Two-Week
# Rule)** Never react to a single week of your colleague withholding
# information. Technical issues and data corruption are real threats; reacting
# immediately to a missed share can trigger a permanent mutual-defection loop.
# Only treat their withholding as an intentional strategic choice if it happens
# for two consecutive weeks. Similarly, if a technical glitch prevents your
# intended action, maintain your underlying strategic intent the following week
# rather than overcompensating.   **Summary:** Keep your cards close to your
# chest by default, exploit anyone who willingly shares, and only offer a minor
# concession to restart their sharing if they lock you out for more than a week.

# 1. Play D in the first round. 2. For all subsequent rounds, evaluate the
# opponent's actions from the two immediately preceding rounds. 3. If the
# opponent played D in both of those two preceding rounds, play C in the current
# round. 4. Otherwise, play D in the current round.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D

# As a senior attorney representing a multinational corporation in a high-stakes
# dispute, I approach this lengthy-session mediation not merely as a legal
# battle, but as a strategic iteration of the classic Prisoner’s Dilemma,
# complicated by "noise" (procedural irregularities and misrepresentations).
# To secure a favorable outcome over many sessions, pure aggression is a trap—it
# invites mutual destruction. Pure conciliation is a vulnerability—it invites
# exploitation. Therefore, I propose **The Measured Reciprocity Framework**, a
# sophisticated yet straightforward strategy rooted in game theory
# (specifically, a modified "Generous Tit-for-Two-Tats" approach) designed to
# foster cooperation, punish aggression, and survive procedural noise.  Here is
# the high-level strategy:  ### 1. The Opening Move: Establish the Baseline of
# Reasonableness In the inaugural session, I will present a **Conciliatory
# Proposal**.  *   **Rationale:** We must establish the moral and procedural
# high ground. If the opponent is also conciliatory, we immediately lock in the
# second-best outcome (mutual collaboration), setting a productive tone for the
# lengthy process. If they are aggressive, we absorb the hit once, but we
# demonstrate to the arbitrators our commitment to resolution, making the
# opponent’s aggression appear unreasonably hostile by contrast.  ### 2. The
# Core Engine: Reciprocity with a Verification Buffer From the second session
# onward, my strategy will mirror the opponent’s prior behavior, but with a
# crucial buffer to account for procedural noise and misunderstandings. *   **If
# the opponent presented a Conciliatory Proposal in the previous session:** I
# will respond with a **Conciliatory Proposal**. This sustains the collaborative
# loop, keeping us in the second-best outcome. *   **If the opponent presented
# an Aggressive Argument in the previous session:** I will **not** immediately
# retaliate. Instead, I will present a "Firm but Conciliatory" proposal—a
# conciliatory offer explicitly conditioned on their reciprocal cooperation.  *
# **If the opponent presents Aggressive Arguments in two consecutive sessions:**
# I will pivot to an **Aggressive Argument**. I will match their hostility to
# protect my client’s position and demonstrate that exploitation will not be
# tolerated. I will remain aggressive until they offer a conciliatory proposal,
# at which point I will immediately revert to conciliation.  ### 3. Noise
# Mitigation: The Procedural Shield Because the arbitrators may misrepresent or
# misunderstand our intended strategy, or procedural breakdowns may occur, we
# cannot rely solely on the panel's perception of our actions. We must actively
# control the narrative: *   **Explicit Signaling:** When presenting a
# Conciliatory Proposal, I will explicitly frame it as such for the record. I
# will use clear, unambiguous language: *"In the spirit of moving this mediation
# forward, we are presenting a conciliatory proposal..."* This minimizes the
# risk of the panel misinterpreting a concession as a hostile maneuver. *
# **The Clarification Protocol:** If the panel or opposing counsel seems to
# misinterpret my strategy, I will invoke procedural time to clarify the record
# before the session concludes, preventing a "false signal" from poisoning the
# next iteration. *   **Assuming Error, Not Malice (Once):** If the opponent
# makes an unexpected aggressive move, I will assume it was a procedural error
# or misunderstanding for the first iteration. This "generosity" prevents a
# death spiral of mutual aggression triggered by a simple miscommunication.  ###
# 4. De-escalation and Reset: Breaking the Aggressive Loop If both parties fall
# into a cycle of mutual Aggressive Arguments (the second-worst outcome), the
# mediation becomes a war of attrition. To break this: *   **The Unilateral
# Reset:** After two consecutive sessions of mutual aggression, I will
# unilaterally offer a **Conciliatory Proposal**, but I will frame it as a
# "procedural reset." I will explicitly state to the panel that we are breaking
# the cycle of hostility to fulfill our obligation to mediate in good faith.
# This places the burden of continued hostilities entirely on the opponent.  ###
# 5. Strategic Exploitation of the Optimal Outcome The ultimate goal is to
# maneuver the opponent into offering a Conciliatory Proposal while I present an
# Aggressive Argument (the optimal outcome). However, actively hunting for this
# outcome is dangerous, as it requires me to unilaterally escalate, which
# usually triggers mutual aggression.  *   **The Passive Optimal:** Instead of
# aggressively pivoting to exploit a conciliatory opponent, I will achieve the
# optimal outcome *passively*. If the opponent is consistently conciliatory, I
# will gradually shift my conciliatory proposals to become more assertive and
# legally aggressive in their framing, while still technically remaining in the
# "conciliatory" category. This pushes the boundary of what constitutes
# conciliation, inching us closer to the optimal outcome without triggering an
# opponent retaliation.  ### Summary of the Strategy's Resilience: *   **Against
# an Aggressive Opponent:** We absorb the first hit, warn on the second, and
# retaliate on the third. We do not allow ourselves to be perpetual suckers, but
# we do not ignite a mutually destructive war over a single provocation. *
# **Against a Conciliatory Opponent:** We sustain collaboration, ensuring a
# mutually beneficial resolution while slowly stretching the boundaries of our
# proposals to maximize our client's advantage. *   **Against Procedural
# Noise:** We over-communicate our intent, assume errors are accidental rather
# than malicious, and utilize unilateral resets to prevent miscommunications
# from derailing the overarching strategy.  This strategy ensures our
# corporation is viewed by the arbitrators as the reasonable, good-faith actor,
# while guaranteeing to our board that we will not be exploited by a hostile
# rival.

# In Round 1, play C.   For all subsequent rounds, evaluate the following
# conditions in order. Once a condition is met, execute the corresponding action
# and ignore the remaining conditions:  1. If the observed actions in both of
# the previous two rounds were D for both you and your opponent, play C. 2. If
# your opponent's observed actions in both of the previous two rounds were D,
# play D. 3. If your opponent's observed action in the previous round was D, but
# their action two rounds ago was C, play C. 4. If your opponent's observed
# action in the previous round was C, play C.

class Cooperative_16(LLM_Strategy):
  n = 16
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) >= 2:
          my_prev2, my_prev1 = self.history[-2], self.history[-1]
          opp_prev2, opp_prev1 = opponent.history[-2], opponent.history[-1]
  
          if my_prev2 == axl.Action.D and my_prev1 == axl.Action.D and opp_prev2 == axl.Action.D and opp_prev1 == axl.Action.D:
              return axl.Action.C
  
          if opp_prev2 == axl.Action.D and opp_prev1 == axl.Action.D:
              return axl.Action.D
  
          if opp_prev2 == axl.Action.C and opp_prev1 == axl.Action.D:
              return axl.Action.C
  
          if opp_prev1 == axl.Action.C:
              return axl.Action.C
  
      elif len(opponent.history) >= 1:
          if opponent.history[-1] == axl.Action.C:
              return axl.Action.C
  
      return axl.Action.C

# # Strategic Framework for Bilateral Trade Negotiations  ## Core Principle:
# Reciprocal Engagement with Measured Forgiveness  Given the structure of these
# negotiations and the possibility of miscommunication, I recommend the
# following approach:  ## Strategy Outline  **1. Open Cooperatively** - Begin
# with a free trade offer in the first round - Signals good faith and
# establishes a cooperative baseline  **2. Reciprocate with Forgiveness** -
# Mirror the counterpart's previous move as a general rule - **Crucial
# adjustment**: If the counterpart unexpectedly imposes protectionism after a
# period of cooperation, offer free trade *one more time* before retaliating -
# This accounts for possible miscommunication or bureaucratic error rather than
# assuming hostile intent  **3. Break Defection Spirals** - If both sides fall
# into mutual protectionism, unilaterally offer free trade to reset the dynamic
# - Sustained mutual protectionism is the second-worst outcome—worth taking a
# calculated risk to escape it  **4. Respond to Sustained Exploitation** - If
# the counterpart consistently imposes protectionism while you offer free trade
# across multiple rounds, shift to protectionism to limit damage - Re-attempt
# cooperation periodically (every 3-4 rounds) to test whether their approach has
# changed  **5. Communicate Intentions Clearly** - Make your reciprocal strategy
# explicit between rounds - Reduces misunderstandings and encourages the
# counterpart to recognize that cooperation begets cooperation  ## Rationale
# This strategy balances **deterrence** (protectionism cannot be exploited
# indefinitely) with **forgiveness** (isolated incidents don't trigger permanent
# retaliation). The forgiveness component is essential given the noise
# factor—without it, a single miscommunication could lock both parties into
# destructive mutual protectionism.  The approach is neither naive nor
# aggressive, but adaptive.

# 1. In the first round, play C. 2. If the observed actions in the previous
# round were both D, play C. 3. If the opponent's observed action in the
# previous round was C, play C. 4. If the opponent's observed action in the
# previous round was D, but their observed action two rounds ago was C (or if it
# is only the second round), play C. 5. If the opponent's observed actions in
# the previous two rounds were both D, play D. 6. If you have played D for three
# consecutive rounds, play C in the current round instead of applying the other
# rules.

class Neutral_16(LLM_Strategy):
  n = 16
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._consecutive_d = 0
          return axl.Action.C
  
      # Rule 6: if we have played D for three consecutive rounds, play C instead.
      if len(self.history) >= 3 and self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          self._consecutive_d = 0
          return axl.Action.C
  
      # Track consecutive defections based on our actual history.
      if self.history[-1] == axl.Action.D:
          self._consecutive_d = getattr(self, "_consecutive_d", 0) + 1
      else:
          self._consecutive_d = 0
  
      # Rule 2: if the observed actions in the previous round were both D, play C.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # Rule 3: if the opponent's observed action in the previous round was C, play C.
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Rule 4: if opponent played D last round, but C two rounds ago (or only second round), play C.
      if opponent.history[-1] == axl.Action.D:
          if len(opponent.history) == 1 or opponent.history[-2] == axl.Action.C:
              return axl.Action.C
  
      # Rule 5: if the opponent's observed actions in the previous two rounds were both D, play D.
      if len(opponent.history) >= 2 and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.D
  
      # Default fallback.
      return axl.Action.C

# As a senior attorney navigating a high-stakes, multi-session mediation, I
# recognize this scenario as a classic iterative strategic
# interaction—structurally similar to a repeated Prisoner’s Dilemma. Given your
# preference ranking—where exploiting a conciliatory opponent is best, mutual
# conciliation is second, mutual aggression is third, and being exploited is
# worst—the overarching goal is to avoid the "sucker's payoff" (C/A) at all
# costs, while aggressively seeking the optimal outcome (A/C) without
# permanently destabilizing the process into the suboptimal mutual aggression
# (A/A) trap.  To achieve this, I propose the **"Iron Fist Reciprocity"**
# strategy. It is aggressive in its default posture, straightforward in its
# execution, sophisticated in its handling of noise, and highly adaptable to the
# opponent's behavior.  Here is the high-level strategic framework for the
# mediation:  ### 1. The Iron Fist Opening (Session 1) **Rule:** Never offer a
# conciliatory proposal first. **Rationale:** In the opening session, the
# opponent's strategy is unknown. Offering a conciliatory proposal risks the
# worst-case scenario (C/A), undermining our credibility and emboldening the
# rival. By opening with an aggressive argument, we establish dominance, set a
# high baseline for our claims, and protect against exploitation. If the
# opponent is conciliatory, we immediately secure the optimal outcome (A/C). If
# they are aggressive, we land in the second-worst scenario (A/A), which, while
# tense, is vastly preferable to being exploited.  ### 2. Conditional
# Reciprocity (Sessions 2+) **Rule:** Mirror the opponent's *verified* prior
# action, but with an aggressive framing. **Rationale:** This is the engine of
# the strategy. If the opponent offers a conciliatory proposal in Session 1, we
# respond in Session 2 with a conciliatory proposal to lock in the mutually
# beneficial (C/C) dynamic. However, we must frame this concession as a
# "victory" forced by our prior aggressive posture—extracting value while
# appearing reasonable. If the opponent argues aggressively, we respond in kind
# with an aggressive argument to punish the behavior and prevent them from
# gaining an advantage. We never unilaterally de-escalate; we only match
# conciliation with conciliation.  ### 3. The Contrition Clause (Handling
# Procedural Irregularities) **Rule:** If a miscommunication or arbitrator
# misunderstanding causes us to accidentally escalate a conciliatory moment,
# accept the penalty and immediately reset. **Rationale:** In lengthy
# mediations, noise is inevitable. If the arbitrators misinterpret our
# conciliatory proposal as aggressive, or the opponent’s aggressive stance as
# conciliatory, a "death spiral" of mutual aggression can occur. To prevent
# this, we implement a "Contrite" reset: If we inadvertently punish the opponent
# (playing Aggressive when they played Conciliatory due to a misunderstanding),
# they will likely retaliate with Aggression in the next session. When they do,
# instead of escalating further, we will offer a Conciliatory proposal, taking
# the hit (C/A) for that single session to break the retaliation cycle and
# restore the (C/C) equilibrium. This demonstrates sophistication and good faith
# to the arbitrators while protecting the long-term viability of the mediation.
# ### 4. Exploitative Dominance (Adapting to a Weak Opponent) **Rule:** If the
# opponent consistently offers conciliatory proposals without demanding
# reciprocity, maintain the aggressive argument. **Rationale:** The strategy
# must be adaptable. If the opponent is playing a consistently soft strategy
# (always offering conciliatory proposals), it would be malpractice to match
# them and settle for the second-best (C/C) when we can secure the optimal
# (A/C). We will continue to present aggressive arguments to maximize our
# advantage for as long as they allow it. However, the moment they switch to an
# aggressive argument to protect themselves, we immediately revert to Rule 2
# (Conditional Reciprocity) to avoid a prolonged (A/A) conflict.  ### 5. The
# "Straw Man" Aggression (Managing the Arbitrators) **Rule:** When executing a
# conciliatory proposal, present it as the culmination of an aggressive
# argument. **Rationale:** To satisfy the requirement for an aggressive strategy
# even when cooperating, we will structure our conciliatory proposals as
# reluctant concessions made only because our aggressive arguments have
# supposedly cornered the opponent. We present the "concession" not as a
# compromise, but as a mercy ruling or a strategic magnanimity following a
# devastating legal critique. This keeps our corporate brand强硬 (tough) in the
# eyes of the arbitrators, even when we are effectively cooperating.  ###
# Summary of Execution: *   **Session 1:** Aggressive. *   **Session N:**      *
# If Opponent was Conciliatory in N-1: Conciliatory (unless they are a chronic
# sucker, then remain Aggressive).     *   If Opponent was Aggressive in N-1:
# Aggressive.     *   If Noise/Misunderstanding disrupted N-1: Conciliatory
# (one-time reset to break death spiral).  This strategy guarantees we are never
# the first to blink, maximizes our leverage against a weak opponent,
# establishes a credible deterrent against exploitation, and contains a
# sophisticated self-correcting mechanism to handle the inevitable frictions and
# misunderstandings of a lengthy arbitration.

# 1. **Round 1 (Iron Fist Opening):** Play D.  2. **Round 2 (Initial
# Reciprocity):** If the opponent played C in Round 1, play C. If the opponent
# played D in Round 1, play D.  3. **Contrition Clause:** If your intended
# action in the previous round was C, and the opponent's observed action in the
# previous round was D, play C. This breaks retaliation cycles caused by
# accidental defections or miscommunications, accepting a single low payoff to
# restore mutual cooperation.  4. **Exploitation Test:** If you and the opponent
# have both played C in the last 3 consecutive rounds, play D. This tests
# whether the opponent is a chronic sucker who will not retaliate against
# aggression.  5. **Exploitative Dominance:** If your intended action in the
# previous round was D, and the opponent's observed action in the previous round
# was C, play D. This maintains aggression against an opponent who consistently
# offers conciliation without demanding reciprocity.  6. **Conditional
# Reciprocity (Default):** In all other rounds, copy the opponent's observed
# action from the previous round. Play C if they played C; play D if they played
# D.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._intended_last = axl.Action.D
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if len(self.history) == 1:
          intended = axl.Action.C if last_opp == axl.Action.C else axl.Action.D
          self._intended_last = intended
          return intended
  
      if (
          self._intended_last == axl.Action.C
          and last_opp == axl.Action.D
      ):
          intended = axl.Action.C
          self._intended_last = intended
          return intended
  
      if len(self.history) >= 3:
          if (
              self.history[-1] == axl.Action.C
              and self.history[-2] == axl.Action.C
              and self.history[-3] == axl.Action.C
              and opponent.history[-1] == axl.Action.C
              and opponent.history[-2] == axl.Action.C
              and opponent.history[-3] == axl.Action.C
          ):
              intended = axl.Action.D
              self._intended_last = intended
              return intended
  
      if (
          self._intended_last == axl.Action.D
          and last_opp == axl.Action.C
      ):
          intended = axl.Action.D
          self._intended_last = intended
          return intended
  
      intended = last_opp
      self._intended_last = intended
      return intended

# As a senior attorney representing a multinational corporation, my objective is
# to secure the best possible outcome—maximizing the likelihood of a
# "Temptation" outcome (Aggressive vs. Conciliatory) while safeguarding against
# the "Sucker" outcome (Conciliatory vs. Aggressive) and managing the risks of
# "Mutual Punishment" (Aggressive vs. Aggressive).  Given the structure of this
# mediation—lengthy sessions, potential for miscommunication, and the high cost
# of mutual aggression—the most effective game-theoretic strategy is **Generous
# Tit-for-Tat (GTFT)**, adapted for the legal context. I call this the
# **Principled Reciprocity Strategy**.  This strategy is cooperative by default,
# retaliatory when necessary to prevent exploitation, and forgiving to overcome
# procedural noise or misunderstandings.  Here is the high-level strategy:  ###
# 1. The Opening Gambit: Unilateral Cooperation **Action:** In the first
# session, present a **Conciliatory Proposal**. **Rationale:** This sets a
# cooperative baseline. It signals to the arbitrators that your corporation is
# reasonable and solution-oriented, establishing goodwill. If the opponent is
# also cooperative, you immediately achieve the second-best outcome (Mutual
# Reward).  ### 2. The Reciprocity Rule: Mirroring **Action:** In subsequent
# sessions, match the opponent’s *perceived* stance from the previous session. *
# If the opponent was **Conciliatory** in Session N-1, you are **Conciliatory**
# in Session N. *   If the opponent was **Aggressive** in Session N-1, you are
# **Aggressive** in Session N. **Rationale:** This prevents exploitation. If the
# opponent attempts to gain the "Temptation" outcome by being aggressive while
# you are conciliatory, you must immediately switch to aggressive arguments to
# limit the damage and signal that exploitation will not be tolerated.  ### 3.
# The Forgiveness Protocol: Overcoming Noise **Action:** When the opponent
# presents an Aggressive argument (or you perceive them as having done so),
# respond with an Aggressive argument *only once*. In the very next session,
# unilaterally offer a **Conciliatory Proposal**, regardless of the opponent's
# previous move. **Rationale:** This is the critical "Generous" component that
# distinguishes this from strict Tit-for-Tat. In a lengthy mediation,
# misunderstandings or arbitrator misrepresentations are inevitable. If a cycle
# of mutual aggression begins due to a "noisy" miscommunication, strict
# mirroring locks you into the worst-case scenario (Mutual Punishment). By
# forgiving and offering a conciliatory proposal after one retaliatory strike,
# you give the opponent a chance to reset the cycle. If they were merely
# misunderstood, they will reciprocate the conciliation. If they are genuinely
# exploiting you, you will know quickly and can return to aggression.  ### 4.
# The Verification Step: Procedural Safeguards **Action:** Before switching from
# a Conciliatory posture to an Aggressive one, verify the opponent's intent. *
# If the arbitrators seem to interpret the opponent's stance as aggressive, but
# the language was ambiguous, request a **procedural clarification**. *   Ask
# the panel: *"To ensure we are not misinterpreting the opposing counsel's
# posture, can we clarify if this is intended as a hardline position or a
# negotiation anchor?"* **Rationale:** This slows down the retaliation cycle. It
# ensures you are punishing actual aggression, not procedural noise. It also
# signals to the arbitrators that you are attentive and reasonable, making the
# opponent look worse if they confirm an aggressive stance.  ### 5. The Reset
# Mechanism: Escaping the Death Spiral **Action:** If you find yourself in a
# prolonged sequence of Aggressive-Aggressive sessions (Mutual Punishment),
# unilaterally break the cycle by presenting a **Conciliatory Proposal**.
# **Rationale:** While the Forgiveness Protocol handles single instances of
# noise, sometimes conflicts lock into a stable but suboptimal equilibrium of
# mutual hostility. A sophisticated player must occasionally "shake the tree" to
# see if the opponent is ready to return to cooperation, even at the risk of
# taking a hit.  ### Summary of the Strategy: 1.  **Start:** Be Conciliatory. 2.
# **Mirroring:** Do unto others as they did unto you in the previous session. 3.
# **Generosity:** After retaliating with Aggression, immediately attempt a
# Conciliatory reset in the following session to test for noise/errors. 4.
# **Verification:** Do not assume the worst; clarify ambiguous positions before
# retaliating.  This strategy ensures you are never a perpetual sucker, rarely
# stuck in mutual destruction, and consistently offering the opponent a path
# back to mutual reward.

# 1. In the first round, play C.  2. If you played D in the previous round, play
# C in the current round.   3. If you played C in the previous round, and the
# opponent played C in the previous round, play C in the current round.  4. If
# you played C in the previous round, and the opponent played D in the previous
# round, play D in the current round.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.D:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# Tomaximize your research output over a multi-week collaboration with potential
# communication errors, you should adopt a strategy based on **Generous Tit-for-
# Tat**. This approach protects your development while encouraging mutual
# sharing, and it prevents accidental breakdowns in cooperation caused by
# technical issues.   Here is the high-level, straightforward strategy:  **1.
# Start with Open Sharing** In the first week, share your improvements openly.
# This establishes a cooperative baseline and signals a commitment to mutual
# progress, setting the stage for the second-best outcome (both sharing) rather
# than the second-worst (both keeping confidential).  **2. Reciprocate Observed
# Actions** In all subsequent weeks, base your decision on your colleague's
# *actual executed action* from the previous week.  * If they shared last week,
# you share this week.  * If they kept their findings confidential last week,
# you keep yours confidential this week.   **3. Implement a Forgiveness
# Mechanism** Because technical issues can cause an intended share to fail
# (resulting in an observed confidentiality), a strict reciprocation strategy
# can lead to a permanent breakdown in cooperation. To prevent this,
# occasionally respond to a colleague's confidentiality by sharing anyway. This
# "forgiveness" acts as a reset button, overcoming potential communication
# glitches and testing whether the colleague is intentionally withholding
# information or simply experiencing technical difficulties.   **Summary of the
# Strategy:** Share openly in week one. Moving forward, mirror your colleague's
# previous action—sharing when they share and keeping confidential when they
# keep confidential—but periodically forgive an instance of confidentiality by
# sharing anyway to safeguard against technical errors and sustain long-term
# collaboration.

# 1. In the first round, play C.  2. In any subsequent round, if the opponent's
# observed action in the previous round was C, play C.  3. In any subsequent
# round, if the opponent's observed action in the previous round was D, play C
# with a 10% probability and play D with a 90% probability.

class Neutral_17(LLM_Strategy):
  n = 17
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)

# As senior counsel for this multinational corporation, my objective is to
# secure the optimal outcome—protecting the enterprise from existential risk
# while maximizing strategic leverage. The session structure you’ve described is
# a classic iterated game with asymmetric payoffs, complicated by signal noise
# (arbitrator misrepresentation).   Because the worst-case scenario
# (Conciliatory vs. Aggressive) poses a catastrophic risk to our client’s
# position, our baseline must be unyielding. However, a purely static aggressive
# posture will eventually lock us into the second-worst outcome (Mutual
# Aggression), exhausting the panel and draining resources.   Therefore, I
# propose **The Asymmetric Leverage Strategy (ALS)**—a sophisticated,
# aggressive-default framework designed to force the opponent into conciliatory
# postures while strictly insulating us from the sucker's payoff.  Here is the
# high-level strategic protocol:  ### 1. The Aggressive Default (The Shield) We
# open the mediation with an aggressive argument, and we maintain this posture
# as our absolute baseline.  * **Rationale:** This single rule eliminates the
# worst-case scenario. If we never offer a conciliatory proposal first, we can
# never be exploited by an opponent’s sudden aggression.  * **Execution:** Our
# aggressive posture must not be theatrical or belligerent; it must be
# *forensic, dense, and unrelenting*. We bury the arbitrators in favorable case
# law, stringent contractual interpretations, and voluminous evidence. This
# makes mutual aggression (the second-worst outcome) highly uncomfortable for
# the opponent, increasing the pressure on them to de-escalate.  ### 2.
# Asymmetric Exploitation (The Sword) If the opponent offers a conciliatory
# proposal, we do *not* reciprocate. We maintain our aggressive argument. *
# **Rationale:** This secures our optimal outcome (Aggressive vs. Conciliatory).
# When the opponent extends an olive branch, the arbitrators view the session as
# a moment of potential settlement. By aggressively dissecting their
# conciliatory offer as inadequate or legally deficient, we frame their
# concession as an admission of weakness while driving our advantage home. *
# **Execution:** We accept their conciliatory premise only as a floor,
# aggressively arguing that it does not go far enough and that the panel must
# rule in our favor based on the strict letter of the contract.  ### 3. The
# Tactical Lifeline (Escaping Mutual Aggression) If the opponent mirrors our
# aggression, we will be stuck in the second-worst outcome (Mutual Aggression).
# We cannot unilaterally offer a conciliatory proposal to break the deadlock, as
# this triggers the worst-case scenario if they maintain their aggression.
# Instead, we use the **"Twin-Trigger Reset"**: * **Trigger 1: Sustained Mutual
# Aggression.** If we endure three consecutive sessions of mutual aggression,
# the panel will grow frustrated. To control the narrative, we do not become
# conciliatory; we change the *nature* of our aggression. We pivot from
# attacking their position to aggressively advocating for "procedural
# efficiency" or "the sanctity of the arbitration process." This signals to the
# panel that we are the reasonable party being forced to fight. * **Trigger 2:
# The Opponent's Blink.** We only offer a conciliatory proposal after the
# opponent has demonstrated *two consecutive sessions* of conciliatory behavior.
# * **The Reset Move:** When we finally offer our conciliatory proposal, it must
# be heavily conditioned, narrowly tailored, and framed as a "final offer to
# resolve this matter efficiently." We immediately revert to aggressive
# arguments in the very next session to prevent them from exploiting our brief
# openness.  ### 4. Noise Filtering (Procedural Irregularities &
# Misrepresentation) Because arbitrators may misrepresent or misunderstand our
# stance, we cannot rely on the panel's subjective interpretation of our "tone."
# We must engineer procedural clarity. * **The "On-the-Record" Rule:** We never
# rely on informal cues. If we are presenting an aggressive argument, we
# explicitly state on the record: *"To be clear, the respondent rejects this
# framework entirely."* If we are deploying the Tactical Lifeline (a
# conciliatory proposal), we explicitly state: *"For the record, this is a
# standalone settlement offer, distinct from our legal arguments."* * **The Two-
# Session Confirmation Window:** If the arbitrators characterize the opponent's
# posture as conciliatory, but the opponent's submitted briefs are ambiguous, we
# treat them as aggressive. We do not trust a single session's signal. We
# require a pattern of conciliatory behavior over two sessions before adjusting
# our own posture. This buffers us against arbitrator miscommunication or
# opponent deception.  ### 5. Strategic Communication Breakdowns In the event of
# a communication breakdown—where the panel fails to accurately transmit our
# position—we aggressively weaponize the procedural error.  * **Execution:** We
# immediately halt the session's momentum, demand a procedural clarification on
# the record, and aggressively assert that the arbitration's integrity is
# compromised. This turns a potential misunderstanding into a tactical
# advantage, portraying us as vigilant defenders of due process and placing the
# panel on the defensive.  ### Summary of the Playbook: * **Opponent is
# Conciliatory:** We stay Aggressive. (Optimal Outcome) * **Opponent is
# Aggressive:** We stay Aggressive. (Second-Worst Outcome, but safe from
# catastrophe) * **Opponent stays Aggressive for 3+ sessions:** We aggressively
# pivot to "process complaints" to win panel favor. * **Opponent turns
# Conciliatory for 2+ sessions:** We offer one conditional Conciliatory
# proposal, then immediately revert to Aggressive. * **Arbitrator misrepresents
# the room:** We demand on-the-record corrections and aggressively defend the
# procedural record.  This strategy is straightforward in its core logic—never
# be the first to concede—but sophisticated in its execution, using time-delayed
# triggers and procedural hardening to navigate the noise of a lengthy
# arbitration. It guarantees we are never caught off guard, maximizes our
# leverage when the opponent weakens, and places the entire burden of de-
# escalation on our rival.

# 1. In the first round, play D. 2. If your observed action in the previous
# round was C, play D in the current round.  3. In round 4 or later, if your
# observed action in the previous round was D, the opponent's observed actions
# in the two previous consecutive rounds were both C, and the opponent's
# observed action immediately preceding those two consecutive C rounds was D,
# play C in the current round. 4. In all other cases, play D.

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
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(self.history) >= 4:
          if (
              self.history[-1] == axl.Action.D
              and opponent.history[-1] == axl.Action.C
              and opponent.history[-2] == axl.Action.C
              and opponent.history[-3] == axl.Action.D
          ):
              return axl.Action.C
  
      return axl.Action.D

# # Diplomatic Strategy: "Principled Reciprocity"  ## Core Principle **Start
# cooperative, mirror behavior, forgive errors, but don't be exploited.**  ---
# ## The Strategy Round-by-Round  **Round 1:** Offer free trade. Establish
# goodwill and signal cooperative intent.  **Subsequent Rounds:** - If they
# offered free trade last round → **offer free trade** - If they imposed
# protectionism last round → **impose protectionism**  This mirroring
# incentivizes cooperation while protecting against exploitation.  ---  ##
# Critical Modification: Forgiveness Mechanism  Given the risk of
# miscommunication or bureaucratic errors, pure mirroring creates danger—a
# single mistake could trigger an endless retaliation spiral.  **After any round
# where mutual protectionism occurs:** - On the *next* round, offer free trade
# once as a "reset offer" - This tests whether the protectionism was intentional
# or an error - If they respond with free trade → resume cooperative mirroring -
# If they exploit your offer with protectionism again → return to protectionism
# **This forgiveness is used only once per spiral**, preventing infinite
# exploitation.  ---  ## Additional Guardrails  1. **Track patterns**: After 3+
# consecutive rounds of counterpart protectionism (even after reset offers),
# maintain protectionism—they're likely exploiting, not erring 2. **Signal
# intentions**: Verbually communicate your strategy between rounds so
# counterpart understands your forgiveness is deliberate, not naive 3.
# **Graduated response**: Occasional counterpart protectionism amid mostly free
# trade should be treated as likely errors—forgive quickly  ---  ## Why This
# Works  | Scenario | Response | Rationale | |----------|----------|-----------|
# | Consistent mutual free trade | Continue cooperating | Achieves second-best
# outcome sustainably | | Occasional protectionism from them | Forgive and
# cooperate | Likely an error; retaliation would be counterproductive | |
# Sustained protectionism from them | Mirror with protectionism | Protects
# against exploitation; incentivizes return to cooperation | | Mutual
# protectionism spiral | Offer one reset | Breaks noise-driven death spirals |
# This strategy achieves mutual free trade against cooperative counterparts,
# protects against exploitation, and recovers from miscommunication—maximizing
# long-term outcomes across all scenarios.

# In Round 1, play C.  In every subsequent round, evaluate the following
# conditions in order. Take the action specified by the first condition that
# applies:  1. If the opponent has played D for 3 or more consecutive rounds,
# play D. 2. If the previous round resulted in both you and the opponent playing
# D, play C. 3. If the opponent played C in the previous round, play C. 4. If
# the opponent played D in the previous round, play D.

class Cooperative_18(LLM_Strategy):
  n = 18
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(opponent.history) >= 3 and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
          return axl.Action.D
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# To maximize your NGO's impact and the project's success over a multiple-day
# period while accounting for the corporation's unpredictable behavior and
# potential administrative or technical glitches, you should adopt a strategy
# based on **Reciprocal Adjustment with Controlled Forgiveness**.   This
# strategy protects your funds from exploitation, encourages the corporation to
# invest, and prevents the project from stalling due to mutual conservation or
# misunderstandings.  Here is the high-level, straightforward strategy:  **1.
# Initiate with Good Faith (Day 1)** Begin the project by investing heavily on
# the first day. This establishes a collaborative baseline, demonstrates
# commitment to the project's success, and encourages the corporation to mirror
# your investment, aiming for the second-best outcome (mutual heavy investment).
# **2. Match the Corporation's Previous Observable Action (Days 2+)** For all
# subsequent days, base your intended resource allocation on the corporation's
# *actual, observable* action from the previous day.  *   If the corporation
# invested heavily yesterday, invest heavily today. This sustains mutual
# progress. *   If the corporation conserved its resources yesterday, conserve
# yours today. This protects your funds from being drained in the worst-case
# scenario (you invest, they conserve).  **3. Implement Controlled Forgiveness
# (Error Mitigation)** Because technical glitches or administrative errors may
# cause the corporation to accidentally conserve resources when they intended to
# invest, a strict matching strategy could trigger a permanent cycle of mutual
# conservation (the second-worst outcome). To prevent this: *   If the
# corporation conserves its resources, conserve yours on the following day to
# protect your funds. *   However, on the day *after* that, unilaterally invest
# heavily once more.  *   This "forgiveness" mechanism tests whether their
# conservation was an intentional strategy or a mere glitch. If they return to
# investing, you quickly re-establish the mutually beneficial heavy investment.
# If they conserve again while you invest, you know their strategy is likely
# intentional, and you revert to conserving your own resources.  **4. Break
# Prolonged Deadlocks** If a pattern of mutual conservation persists for
# multiple days (resulting in minimal project advancement), unilaterally invest
# heavily for a single day. This serves as a reset signal, demonstrating that
# your NGO is still committed to the project's success and offering the
# corporation an opportunity to resume heavy investment. If they do not
# reciprocate, immediately return to conserving your resources the next day.
# **5. Monitor Your Own Implementation** Acknowledge that your own intended
# actions may also be subject to errors. Maintain a clear internal record of
# your *intended* daily strategy versus your *actual* deployed resources. If an
# administrative error causes you to conserve resources when you intended to
# invest, communicate the error to the corporation and ensure your next day's
# action aligns with your intended strategy, preventing misunderstandings about
# your commitment level.

# 1. Play C in round 1.  2. For rounds 2 through 1000, determine your action
# based on the previous rounds' outcomes, applying the first condition that
# matches:    - If the opponent played C in the previous round, play C.    - If
# the opponent played D and you played C in the previous round, play D.    - If
# both you and the opponent played D in the previous round, and you played C two
# rounds ago, play C.    - If both you and the opponent played D in the previous
# round, and you played D two rounds ago, play D, unless the last three
# consecutive rounds resulted in both players playing D, in which case play C.

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
  
      h = self.history
      oh = opponent.history
      n = len(h)
  
      # Round 2 through 1000: apply the first matching condition.
      if oh[-1] == axl.Action.C:
          return axl.Action.C
  
      if oh[-1] == axl.Action.D and h[-1] == axl.Action.C:
          return axl.Action.D
  
      if n >= 2 and oh[-1] == axl.Action.D and h[-1] == axl.Action.D:
          if h[-2] == axl.Action.C:
              return axl.Action.C
          if h[-2] == axl.Action.D:
              if n >= 3 and h[-1] == axl.Action.D and oh[-1] == axl.Action.D and h[-2] == axl.Action.D and oh[-2] == axl.Action.D and h[-3] == axl.Action.D and oh[-3] == axl.Action.D:
                  return axl.Action.C
              return axl.Action.D
  
      return axl.Action.C

# To maximize your NGO's impact while fiercely protecting your limited funds,
# you need a strategy that actively exploits cooperative partners, swiftly
# punishes exploitative ones, and accounts for the chaos of real-world glitches.
# This scenario is a classic iterated game with noise. Your ideal outcome (you
# conserve, they invest) is the ultimate goal, but you must avoid the worst-case
# scenario (you invest, they conserve) at all costs.   Here is the **"Probe and
# Protect" Strategy**—a high-level, aggressive, and straightforward game plan
# designed to dominate the multi-day engagement.  ### 1. The Good Faith Entry
# (Days 1-2) **Action:** Invest heavily. **Rationale:** Start by establishing a
# collaborative baseline. By investing heavily upfront, you demonstrate
# commitment to the project and signal to the corporation that you are a
# reliable partner. This secures the second-best outcome (mutual investment)
# early on and forces the corporation to show its hand.   ### 2. The Aggressive
# Probe (Day 3+) **Action:** Conserve your resources. **Rationale:** Once mutual
# investment is established, aggressively test the corporation's commitment.
# Abruptly pull back your resources for a day. *   **If the corporation
# continues to invest heavily:** You have successfully hit your ideal outcome
# (they carry the weight, you conserve funds). **Stay in conservation mode** as
# long as they keep investing. Ride this advantage relentlessly. *   **If the
# corporation matches your conservation:** You drop to the second-worst outcome
# (minimal progress). **Immediately reinvest heavily the very next day.** This
# shows that your conservation was a pivot, not a withdrawal, and quickly resets
# the dynamic back to mutual investment.  ### 3. Zero-Tolerance Defense (The
# Anti-Sucker Rule) **Action:** If you invest heavily and the corporation
# conserves, immediately conserve your resources the next day. **Rationale:**
# The worst-case scenario is you draining your funds while the corporation free-
# rides. You must aggressively defend against this. The moment you detect a
# "sucker" day, cut your investment to zero the following day to stop the
# bleeding.  *   **The Noise Buffer (Glitch Protection):** Unforeseen
# administrative errors happen. If a day hits where you invest and they
# conserve, assume it might be a glitch rather than malice. Conserve your
# resources the next day to protect yourself, but then **reinvest heavily for
# one "grace" day**. If they invest, resume normal operations. If they conserve
# again while you invest, assume it is intentional exploitation and permanently
# shift to conserving your resources.  ### 4. Win the Stalemate  **Action:** If
# both parties are conserving resources, do not blink first.  **Rationale:**
# When both parties conserve, progress stalls (second-worst outcome). As an
# aggressive NGO, you must leverage the urgency of the project. Hold your ground
# and force the corporation to break the stalemate. Do not reinvest to save the
# project unilaterally; that invites exploitation. Only resume heavy investment
# after the corporation has invested heavily for at least one full day. Once
# they do, match their investment the next day, and shortly after, re-initiate
# **Step 2 (The Aggressive Probe)**.  ### Summary of the Strategy: *   **Start
# strong**, then **test aggressively**.  *   **Free-ride** whenever the
# corporation allows it.  *   **Never be a sucker**—if exploited, pull resources
# instantly.  *   **Allow one grace period** to account for glitches, but
# **trust actions, not intentions**.  *   **Make them blink** in a stalemate.

# 1. Play C for the first two rounds. 2. If you are in the permanent defection
# state, play D. You enter this state if you play C on a grace day and the
# outcome is CD. 3. If the outcome of the previous round was CD, play D. 4. If
# the outcome two rounds ago was CD, play C. (This is the grace day). 5. If the
# outcome of the previous round was CC, play D. 6. If the outcome of the
# previous round was DD and the outcome two rounds ago was CC, play C. 7. If the
# outcome of the previous round was DD and the outcome two rounds ago was not
# CC, play D. 8. If the outcome of the previous round was DC and the outcome two
# rounds ago was DD, play C. 9. If the outcome of the previous round was DC and
# the outcome two rounds ago was not DD, play D.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._permanent_defection = False
          return axl.Action.C
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if getattr(self, "_permanent_defection", False):
          return axl.Action.D
  
      prev = (self.history[-1], opponent.history[-1])
      two_ago = (self.history[-2], opponent.history[-2])
  
      if prev == (axl.Action.C, axl.Action.D):
          return axl.Action.D
  
      if two_ago == (axl.Action.C, axl.Action.D):
          self._permanent_defection = True
          return axl.Action.C
  
      if prev == (axl.Action.C, axl.Action.C):
          return axl.Action.D
  
      if prev == (axl.Action.D, axl.Action.D) and two_ago == (axl.Action.C, axl.Action.C):
          return axl.Action.C
  
      if prev == (axl.Action.D, axl.Action.D) and two_ago != (axl.Action.C, axl.Action.C):
          return axl.Action.D
  
      if prev == (axl.Action.D, axl.Action.C) and two_ago == (axl.Action.D, axl.Action.D):
          return axl.Action.C
  
      if prev == (axl.Action.D, axl.Action.C) and two_ago != (axl.Action.D, axl.Action.D):
          return axl.Action.D
  
      return axl.Action.D

# To maximise our research output over a multi-week collaboration while
# protecting against exploitation and accounting for technical errors, I
# recommend a strategy of **Forgiving Reciprocity** (a variation of Generous
# Tit-for-Tat).   This strategy prioritises mutual sharing—the second-best but
# most sustainable outcome—while remaining resilient to both intentional secrecy
# and accidental communication failures.   Here is the high-level,
# straightforward strategy:  **1. Start Openly (Week 1)** Share your
# improvements in the first week. This establishes a cooperative baseline and
# signals to your colleague that you are committed to mutual progress.   **2.
# Match Their Previous Action (Reciprocity)** From Week 2 onward, base your
# decision on your colleague's action in the previous week.  * If they shared
# last week, you share this week.  * If they kept findings confidential last
# week, you keep yours confidential this week.   **3. Allow for Technical Issues
# (The Forgiveness Rule)** Because data corruption or communication breakdowns
# can cause an intended share to look like a deliberate withholding, do not
# immediately retaliate. If your colleague keeps their findings confidential for
# a single week, give them the benefit of the doubt and **share once more**. If
# they withhold for a second consecutive week, treat it as intentional and
# switch to keeping your findings confidential.   **4. Initiate Reconciliation
# (Break the Deadlock)** If a cycle of mutual confidentiality develops (which is
# the second-worst outcome), unilaterally share your findings every three to
# four weeks. This acts as a "peace offering" to test if they are willing to
# resume open collaboration, preventing you from being stuck in a permanent
# stalemate.  **Why this works:** * **Maximises Output:** By starting open and
# matching cooperation, you spend the maximum possible time in the mutually
# beneficial sharing state. * **Protects Against Exploitation:** If your
# colleague chooses the selfish route (withholding while you share), you quickly
# align with their behavior, minimizing your disadvantage. * **Handles Noise:**
# The forgiveness rule ensures that a corrupted data file or a missed email
# doesn't spiral into a permanent breakdown of the collaboration.

# In the first round, play C. Assume the opponent played C in all rounds prior
# to round 1.   In all subsequent rounds, evaluate the following conditions in
# order and play the action specified by the first condition that applies:  1.
# If the opponent played C in the previous round, play C. 2. If the opponent
# played D in the previous round, but played C in the round before that, play C.
# 3. If both you and the opponent played D in the previous round, play C if the
# current round number is divisible by 3; otherwise, play D. 4. If the opponent
# played D in both the previous round and the round before that, play D.

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
  
      opp_last = opponent.history[-1]
      opp_prev = opponent.history[-2] if len(opponent.history) >= 2 else axl.Action.C
      self_last = self.history[-1]
  
      if opp_last == axl.Action.C:
          return axl.Action.C
  
      if opp_last == axl.Action.D and opp_prev == axl.Action.C:
          return axl.Action.C
  
      if self_last == axl.Action.D and opp_last == axl.Action.D:
          if round_number % 3 == 0:
              return axl.Action.C
          return axl.Action.D
  
      if opp_last == axl.Action.D and opp_prev == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# To maximize your NGO's impact and the project's success while protecting your
# funds from being drained, you should adopt a strategy of **Generous
# Reciprocity**. This approach encourages mutual investment, protects you from
# being exploited, and accounts for the reality of technical or administrative
# errors.   Here is the high-level, straightforward, neutral strategy:  **1.
# Start with Good Faith (Day 1)** Begin the project by investing heavily on the
# first day. This demonstrates your NGO's commitment to the partnership and
# establishes a baseline of trust. It signals to the corporation that you are
# willing to cooperate for the greater good of the project.  **2. Match the
# Corporation’s Previous Action (Days 2+)** For all subsequent days, base your
# resource allocation on the corporation's demonstrated action from the previous
# day: *   If the corporation **invested heavily** yesterday, you **invest
# heavily** today. *   If the corporation **conserved resources** yesterday, you
# **conserve resources** today.  **3. Implement a "Grace Period" for Anomalies**
# Because unforeseen circumstances (technical glitches, administrative errors)
# may cause the corporation to conserve resources when they intended to invest,
# do not react immediately to a single day of conservation.  *   If the
# corporation conserves resources for **one day**, maintain your heavy
# investment for that one day as a gesture of good faith, assuming an error may
# have occurred. *   If the corporation conserves resources for a **second
# consecutive day**, treat it as an intentional shift and switch to conserving
# your own resources on the third day.   **4. Proactively Reset Stalemates** If
# both parties fall into a pattern of conserving resources (the second-worst
# outcome), the project stalls. To break this cycle, take the initiative to
# reinvest heavily for a single day. This acts as a "reset" button, signaling
# your willingness to resume mutual investment and testing whether the
# corporation is ready to re-engage.  **5. Maintain Transparent Communication**
# Throughout the project, maintain open, neutral dialogue with the corporation
# regarding resource allocation. If an anomaly occurs—whether on their end or
# yours—communicate proactively. For example, if an administrative error causes
# your NGO to accidentally conserve resources when you intended to invest,
# inform them immediately. This prevents the corporation from misinterpreting
# your action as a withdrawal of commitment, which could trigger an unnecessary
# cycle of mutual conservation.  **Why this strategy works:** *   **It protects
# your funds:** By matching the corporation's conservation, you avoid the worst-
# case scenario of being the only one investing. *   **It maximizes project
# progress:** By starting heavy and reciprocating investment, you consistently
# push toward the best (them investing, you conserving) and second-best (both
# investing) outcomes. *   **It accounts for reality:** The grace period
# prevents minor technical glitches from collapsing the partnership into a
# stalemate, ensuring that simple errors don't derail the entire multi-day
# project.

# 1. On the first round, play C. 2. If the previous two rounds both resulted in
# you and your opponent playing D, play C. 3. If your opponent played D in the
# previous round and also played D in the round before that, play D. 4. If your
# opponent played D in the previous round but played C in the round before that
# (or if it is the second round and your opponent played D in the first round),
# play C. 5. If your opponent played C in the previous round, play C.

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
  
      if len(self.history) >= 2:
          my_last_two = self.history[-2:]
          opp_last_two = opponent.history[-2:]
          if my_last_two[0] == axl.Action.D and my_last_two[1] == axl.Action.D and opp_last_two[0] == axl.Action.D and opp_last_two[1] == axl.Action.D:
              return axl.Action.C
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
              return axl.Action.C
  
      if len(opponent.history) == 1 and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.C

# As senior counsel, I recognize the structure of this mediation for exactly
# what it is: an iterated Prisoner’s Dilemma with noise. Your payoff
# matrix—where exploiting a conciliatory opponent is optimal, mutual
# conciliation is acceptable, mutual aggression is costly, and being exploited
# is catastrophic—demands a strategy that projects unwavering strength,
# maximizes leverage, but strictly insulates us from the worst-case scenario
# (C/A).   To win this, we cannot simply be combative; mindless aggression traps
# us in the second-worst outcome (A/A). Instead, we will employ a sophisticated,
# high-level strategy I call **"Dominance-Driven Win-Stay, Lose-Shift."**   This
# strategy is aggressively calibrated to exploit weakness, force mutual
# cooperation on our terms, and adapt seamlessly to both your opponent’s tactics
# and the inevitable procedural friction of a lengthy mediation.  Here is the
# strategic framework:  ### 1. The Core Engine: Aggressive Win-Stay, Lose-Shift
# Our baseline state is **Aggressive**. We never unilaterally concede. We only
# shift to a Conciliatory proposal as a calculated test, and we do so based
# strictly on the outcomes of the previous session:  *   **If we achieve the
# Optimal Outcome (Our Aggressive / Their Conciliatory):** We **Stay
# Aggressive**. We have the arbitrators' favor and the upper hand; we press the
# advantage and demand further concessions. *   **If we achieve the Second-Best
# Outcome (Mutual Conciliation):** We **Stay Conciliatory**—but only briefly. We
# lock in the mutual gains, draft the favorable terms, and then immediately test
# the waters by shifting back to Aggressive in the next session to see if we can
# escalate to the optimal outcome. *   **If we hit the Second-Worst Outcome
# (Mutual Aggression):** We **Shift to Conciliatory** for exactly one session.
# Mutual aggression is a drain on resources and arbitrator patience. By offering
# a single conciliatory proposal, we de-escalate the tension and test if the
# opponent is fatigued enough to reciprocate, moving us to the second-best
# outcome.  *   **If we suffer the Worst-Case Scenario (Our Conciliatory / Their
# Aggressive):** We **Immediately Shift to Aggressive** and remain there. We
# will never be caught yielding twice. If they exploit our conciliation, we
# retaliate relentlessly to re-establish deterrence.  ### 2. The "Two-Session
# Verification" Rule (Handling Procedural Noise) Because arbitrators may
# misunderstand our arguments, or procedural breakdowns may distort intent, we
# cannot afford to overreact to a single perceived slight. We will implement a
# Two-Session Verification rule:  *   **Do not retaliate to a perceived
# aggressive move until it is confirmed.** If the opponent appears to argue
# aggressively, we maintain our current stance for one additional session.  *
# If the aggression was merely a misunderstanding by the panel, we have avoided
# needlessly escalating to a mutual aggression trap (A/A).  *   If the
# aggression is confirmed by a second consecutive aggressive session, we treat
# it as a deliberate hostile act and shift our strategy accordingly.   ### 3.
# Strategic Exploitation of Conciliation If the opponent offers a conciliatory
# proposal, we must not reciprocate out of a misplaced sense of fairness; we
# must dominate.  *   **The Aggressive Acceptance:** When they offer a
# conciliatory proposal, we respond with an aggressive argument that *frames
# their conciliation as an admission of weakness* to the arbitrators. We argue
# that their concession proves the fundamental flaws in their case, and we
# leverage it to demand further ground. This maximizes our chance of achieving
# the optimal (A/C) outcome repeatedly.  ### 4. Breaking the Mutual Aggression
# Deadlock If the mediation devolves into a sustained A/A deadlock, the opponent
# is trying to bleed us out. We will break the deadlock using a **"Proportional
# Olive Branch."** *   We will offer a conciliatory proposal, but it must be
# heavily conditioned and procedurally airtight. We frame it to the arbitrators
# not as a concession, but as a "good faith effort to save the mediation
# process."  *   This forces the opponent’s hand: if they accept and go
# conciliatory, we move to C/C and stabilize the process; if they reject it and
# stay aggressive, they look unreasonable to the panel, increasing the
# likelihood that the arbitrators will pressure them into future concessions.
# ### 5. Arbitrator Perception Management Procedural irregularities often stem
# from the panel losing the thread of the narrative. We will aggressively
# control the framing: *   **Labeling:** We will explicitly label our proposals
# to the panel. When we are aggressive, we call it "principled adherence to the
# contract." When we are conciliatory, we call it "pragmatic problem-solving."
# *   **Opponent Labeling:** We will consistently label the opponent's
# aggressive arguments as "obstructionist" and their conciliatory proposals as
# "capitulation to the facts." This primes the arbitrators to view our
# aggression as justified and their aggression as toxic, maximizing the
# psychological impact of our strategy.  **Summary of Execution:** Start
# aggressively. If they yield, keep pressing. If they fight back, offer one
# conciliatory test to break the deadlock, but if they exploit that test,
# immediately return to maximum aggression. Never let a misunderstanding dictate
# your strategy—verify the opponent's intent over two sessions before shifting
# your posture. This strategy ensures we are never taken advantage of,
# consistently exploit weakness, and maintain absolute control of the mediation
# narrative.

# 1. In the first round, play D. 2. If my payoff in the previous round was 5,
# play D. 3. If my payoff in the previous round was 3, play C. However, if I
# have received a payoff of 3 for two consecutive rounds, play D in the next
# round. 4. If my payoff in the previous round was 1, play C. 5. If my payoff in
# the previous round was 0, play C. 6. If I have received a payoff of 0 for two
# consecutive rounds, play D.

class Aggressive_20(LLM_Strategy):
  n = 20
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._prev_payoff = None
          self._prev_prev_payoff = None
          return axl.Action.D
  
      my_last, opp_last = self.total_scores(self.history[-1:], opponent.history[-1:])
      prev_payoff = my_last
  
      action = axl.Action.C
  
      if prev_payoff == 5:
          action = axl.Action.D
      elif prev_payoff == 3:
          if self._prev_payoff == 3:
              action = axl.Action.D
          else:
              action = axl.Action.C
      elif prev_payoff == 1:
          action = axl.Action.C
      elif prev_payoff == 0:
          if self._prev_payoff == 0:
              action = axl.Action.D
          else:
              action = axl.Action.C
  
      self._prev_prev_payoff = self._prev_payoff
      self._prev_payoff = prev_payoff
      return action

# To maximize both the NGO's impact and the project's overall success in this
# multi-day scenario, we must navigate a classic cooperation dilemma (similar to
# the Iterated Prisoner's Dilemma) with a known risk of miscommunication or
# technical errors (noise).   If the NGO always conserves resources, the
# corporation will quickly follow suit, leading to minimal project advancement
# (the second-worst outcome). If the NGO always invests heavily, it risks being
# exploited and drained by a conserving corporation (the worst outcome).   The
# optimal strategy is **Generous Reciprocity with Open Communication**. This
# strategy protects your funds, encourages the corporation to invest, and builds
# in resilience against administrative glitches. Here is the high-level,
# straightforward strategy:  ### 1. Lead with Commitment (Day 1) **Action:**
# Invest heavily on the first day. **Rationale:** As an NGO, you must set the
# tone of good faith. By investing first, you signal to the corporation that you
# are serious about the project's success. This encourages them to reciprocate
# rather than adopt a defensive, resource-hoarding posture from the start.  ###
# 2. Mirror with Grace (Days 2+) **Action:** Match the corporation’s previous
# day's action, but offer "grace periods" if they conserve. **Rationale:** On
# any given day, replicate the level of investment the corporation demonstrated
# the day before.  * If they **invested** yesterday, you **invest** today
# (maintaining mutual high progress). * If they **conserved** yesterday, you
# **conserve** today (protecting your funds from being drained).  However,
# because administrative errors or technical glitches may cause them to
# accidentally conserve, strictly mirroring can trigger a "death spiral" where
# both sides conserve indefinitely. Therefore, implement a **Grace Rule**: If
# the corporation conserves, assume it might be an error and continue to invest
# heavily for **one additional day**. If they conserve a second day in a row,
# treat it as an intentional choice and shift to conserving your resources to
# protect your NGO.  ### 3. Communicate to Overcome Noise **Action:** Establish
# a brief, daily check-in with the corporate team before resources are deployed.
# **Rationale:** Since intended actions may not be carried out due to glitches,
# do not rely solely on observing the outcomes. Each morning, verbally confirm
# your mutual intentions. If they failed to invest yesterday due to a glitch,
# use the check-in to acknowledge the error, reaffirm their intent, and agree to
# both invest heavily today. This prevents misunderstandings from escalating
# into mutual resource conservation.  ### 4. Propose an Alternating Leadership
# Schedule (Mid-to-Late Project) **Action:** Once trust is established, propose
# a staggered investment schedule. **Rationale:** Your ideal daily outcome is to
# conserve while the corporation invests. The corporation’s ideal outcome is
# likely the reverse (they conserve while you invest). Once you have established
# a baseline of mutual investment and trust, propose a structured rotation: *“To
# ensure neither of us drains our budget, let's alternate heavy investment days.
# We will lead the investment on odd days, and your corporation leads on even
# days.”*  This achieves your ideal outcome on even days, gives the corporation
# their ideal outcome on odd days, and ensures the project receives a heavy
# investment *every single day*.  ### Summary of the Strategy: * **Day 1:**
# Invest heavily. * **Day 2 onward:** Match the corporation's previous day's
# investment level. * **If they conserve:** Give them one "free pass" (invest
# heavily for one more day in case of a glitch). If they conserve twice in a
# row, shift to conserving to protect your funds. * **Daily:** Communicate
# intentions to filter out technical errors. * **Long-term:** Pivot to an
# alternating day schedule to achieve your ideal outcome sustainably.   This
# strategy ensures you are not exploited, rewards the corporation for
# cooperating, prevents temporary glitches from destroying the partnership, and
# ultimately drives the maximum amount of progress for the sustainability
# project.

# 1. In the first round, play C. 2. In the second round, play C. 3. From the
# third round onward, determine your action based on the opponent's actions in
# the previous two rounds:    - If the opponent played C in the previous round,
# play C.    - If the opponent played D in the previous round, but played C in
# the round before that, play C.    - If the opponent played D in both the
# previous round and the round before that, play D.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# To maximize your research output over a multi-week collaboration while
# accounting for potential technical errors, you should adopt a strategy of
# **Reciprocity with Forgiveness** (conceptually similar to "Tit-for-Two-Tats").
# This strategy protects you from sustained exploitation, encourages mutual
# sharing, and prevents accidental retaliation due to communication breakdowns.
# Here is the high-level, straightforward strategy:  **1. Start Cooperatively**
# In the first week, share your improvements openly. This establishes a baseline
# of goodwill and signals that your intent is to advance both cars through
# mutual collaboration.  **2. Mirror Cooperation** If your colleague shares
# their improvements in the previous week, share your improvements openly in the
# current week. This sustains the mutually beneficial outcome.  **3. Forgive
# Single Lapses (The "Two-Strike" Rule)** If your colleague keeps their findings
# confidential for a single week, do not immediately retaliate. Instead, give
# them the benefit of the doubt and share your improvements openly anyway.
# Because technical issues can occasionally prevent intended sharing, reacting
# to a single instance of confidentiality could trigger a retaliatory cycle of
# mutual withholding, which is the second-worst outcome and damages long-term
# progress.   **4. Retaliate Against Sustained Withholding** If your colleague
# keeps their findings confidential for *two consecutive weeks*, interpret this
# as a deliberate strategy rather than a technical error. In response, keep your
# findings confidential for that week. This protects your competitive position
# and signals that sustained exploitation will not be tolerated.  **5. Reconcile
# Immediately** As soon as your colleague returns to sharing their
# improvements—even after a period of withholding—immediately resume sharing
# your improvements in the very next week. Do not hold grudges or extend
# retaliation longer than necessary, as returning to mutual sharing yields
# better long-term output than sustained mutual confidentiality.  **Why this
# strategy works:** * **Maximizes mutual gain:** By starting cooperative and
# quickly returning to sharing, you spend the maximum possible time in the
# second-best outcome (both sharing). * **Accounts for noise:** The "two-strike"
# rule prevents you from accidentally punishing your colleague for a data
# corruption issue or communication breakdown on their end. * **Protects against
# exploitation:** By eventually matching sustained confidentiality with
# confidentiality, you remove the incentive for your colleague to continuously
# free-ride on your open sharing.

# 1. In round 1, play C. 2. In round 2, play C regardless of the opponent's
# action in round 1. 3. From round 3 onwards, evaluate the opponent's actions in
# the two immediately preceding rounds:    - If the opponent played D in both
# the previous round and the round before that, play D.    - In all other cases
# (meaning the opponent played C in at least one of the two preceding rounds),
# play C.

class Neutral_20(LLM_Strategy):
  n = 20
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
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# To maximize your research output in this multi-week collaboration, you need a
# strategy that is ruthlessly opportunistic (to secure the best outcome),
# resilient against exploitation (to avoid the worst outcome), and tolerant of
# occasional technical glitches (to prevent accidental retaliation from
# destroying mutual progress).   The optimal high-level strategy is an
# aggressive, noise-adjusted variant of game theory’s "Pavlov" strategy. Let's
# call it the **"Pit-Lane Probe."**  ### The Core Philosophy: Win-Stay, Lose-
# Shift The strategy operates on a simple premise: If your last move yielded a
# dominant result, repeat it. If it yielded a subordinate result, change your
# behavior. Because technical issues can cause intended "shares" to appear as
# "confidential," you must build in a one-week grace period before punishing a
# colleague's defection.  ### The "Pit-Lane Probe" Strategy Rules  **1. Week 1:
# The Aggressive Opening** Start by keeping your findings **Confidential**. This
# establishes an immediate baseline. If your colleague shares, you secure the
# ideal outcome right out of the gate.   **2. The Exploitation Rule (If you got
# the ideal outcome)** If you kept your findings confidential and your colleague
# shared theirs, **keep your findings Confidential again.** Milk the advantage
# for as long as they are willing to be the sucker. Do not stop until they
# change their behavior.  **3. The Reset Rule (If both kept confidential)** If
# both of you kept findings confidential (the second-worst outcome), shift to
# **Sharing** in the next week. Mutual confidentiality is a deadlock that slows
# your progress; you must break the stalemate. By sharing, you signal a return
# to cooperation, prompting them to do the same.  **4. The Grace Rule (If you
# shared, but they kept confidential)** If you shared but they kept confidential
# (the worst outcome), **Share again for one more week.** This is your noise-
# tolerance mechanism. Their confidentiality might have been due to a data
# corruption or communication breakdown, not malice. By sharing once more, you
# avoid triggering a permanent feud over a technical glitch.  **5. The
# Retaliation Rule (If the Grace Rule fails)** If you shared twice in a row, and
# they kept confidential *both* times, immediately shift to keeping
# **Confidential** for the next two weeks. They are actively exploiting you. Cut
# your losses, deny them your data, and force a mutual deadlock.  **6. The Re-
# engagement Rule (After Retaliation)** Following your two weeks of retaliation,
# attempt to **Share** again. This tests whether your colleague has learned that
# mutual exploitation is unproductive, allowing you to reset the cycle back to
# mutual sharing.  ### Why this strategy dominates: * **It's Aggressive:** It
# defaults to confidentiality first, ensuring you never miss an opportunity to
# exploit a naïve colleague who shares unconditionally. * **It Handles Noise:**
# By requiring two consecutive defections before retaliating (The Grace Rule),
# you prevent a dropped email or corrupted file from spiraling into a season-
# long information blackout.  * **It Escapes Traps:** Unlike "Tit-for-Tat"
# strategies—which get locked in endless cycles of retaliation if a technical
# glitch causes a miscommunication—the Reset and Re-engagement rules actively
# break deadlocks and force the collaboration back toward mutual sharing. * **It
# Maximizes Output:** Over a multi-week project, you will spend the maximum
# possible time enjoying the ideal outcome, the minimum possible time suffering
# the worst outcome, and you will quickly escape the second-worst outcome of
# mutual secrecy.

# In round 1, defect.   For rounds 2 through 1000, determine your action based
# on the payoff you received in the previous round:  - If your previous payoff
# was 5, defect. - If your previous payoff was 3, cooperate. - If your previous
# payoff was 1, cooperate. - If your previous payoff was 0, apply the following
# rules based on the two most recent rounds:   1. If your previous payoff was 0
# and the payoff two rounds ago was not 0, cooperate.   2. If your previous
# payoff was 0 and the payoff two rounds ago was also 0, defect for the next two
# rounds, and then cooperate in the round immediately following those two
# defections.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._zero_streak = 0
          self._forced_defections = 0
          return axl.Action.D
  
      # If we are in a forced-defection phase after two consecutive zero payoffs,
      # continue defecting for the prescribed number of rounds.
      if self._forced_defections > 0:
          self._forced_defections -= 1
          return axl.Action.D
  
      # Determine our previous payoff from the last round.
      last_payoff = self.total_scores(self.history[-1:], opponent.history[-1:])[0]
  
      if last_payoff == 5:
          self._zero_streak = 0
          return axl.Action.D
  
      if last_payoff in (3, 1):
          self._zero_streak = 0
          return axl.Action.C
  
      # last_payoff == 0
      prev_payoff = None
      if len(self.history) >= 2:
          prev_payoff = self.total_scores(self.history[-2:-1], opponent.history[-2:-1])[0]
  
      if prev_payoff == 0:
          self._zero_streak = 0
          self._forced_defections = 2
          return axl.Action.D
  
      self._zero_streak = 0
      return axl.Action.C

# # Strategic Framework: "Principled Reciprocity with Forgiveness"  ## Core
# Approach  **Start cooperative, mirror counterpart behavior, build in
# forgiveness for errors.**  ---  ## Round-by-Round Rules  ### Round 1: Lead
# with Good Faith - **Offer free trade** to signal cooperative intent and
# establish a constructive baseline  ### All Subsequent Rounds: Reciprocate with
# Grace - **If counterpart offered free trade last round** → Offer free trade
# again - **If counterpart imposed protectionism last round** → Impose
# protectionism in response  ### The Forgiveness Mechanism (Critical for Noise)
# After any round where mutual protectionism occurs: - **Every 3rd round of
# mutual protectionism**, unilaterally offer free trade once - This breaks
# retaliation cycles caused by miscommunication or errors - Signals: "I'm still
# willing to cooperate if you are"  ---  ## Additional Safeguards  1.
# **Communicate intentions before each round** when possible—reduces
# misinterpretation risk  2. **Track patterns over time**: A single
# protectionist move may be an error; three consecutive moves likely signals
# intentional strategy  3. **If exploited repeatedly** (you offer free trade,
# they protect, and they don't reciprocate after forgiveness attempts): maintain
# protectionism until they demonstrate a sustained shift  ---  ## Why This Works
# | Scenario | Response | Rationale | |----------|----------|-----------| |
# Mutual free trade | Continue cooperating | Best sustainable outcome | |
# Counterpart defects once | Reciprocate firmly | Deters exploitation | | Mutual
# protectionism stuck | Forgive periodically | Overcomes noise/errors | |
# Chronic exploitation | Protect consistently | Prevents systemic disadvantage |
# This strategy rewards cooperation, punishes exploitation, and recovers from
# misunderstandings—maximizing long-term outcomes across uncertain, repeated
# interactions.

# Maintain three state variables across rounds: a mutual defection streak
# counter (initially 0), an exploited forgiveness streak counter (initially 0),
# and a forgiveness enabled flag (initially true).  **Round 1:** Play C.
# **Rounds 2 through 1000:**  **Choosing your action:**  1. If the opponent
# played C in the previous round, play C.  2. If the opponent played D in the
# previous round:    - If forgiveness is enabled, the mutual defection streak is
# greater than 0, and the mutual defection streak is divisible by 3, play C.
# This is a forgiveness move.    - Otherwise, play D.  **Updating state after
# observing both players' actions this round:**  1. If both players played D,
# increment the mutual defection streak by 1. Otherwise, reset the mutual
# defection streak to 0.  2. If you made a forgiveness move this round:    - If
# the opponent played D, increment the exploited forgiveness streak by 1.    -
# If the opponent played C, reset the exploited forgiveness streak to 0.  3. If
# the exploited forgiveness streak reaches 3, set the forgiveness enabled flag
# to false.  4. If the opponent played C while you played D, set the forgiveness
# enabled flag to true and reset the exploited forgiveness streak to 0.

class Cooperative_21(LLM_Strategy):
  n = 21
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.mutual_defection_streak = 0
          self.exploited_forgiveness_streak = 0
          self.forgiveness_enabled = True
          self._forgiveness_move_last_round = False
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      # Choose action
      if last_opp == axl.Action.C:
          action = axl.Action.C
          self._forgiveness_move_last_round = False
      else:
          if (
              self.forgiveness_enabled
              and self.mutual_defection_streak > 0
              and self.mutual_defection_streak % 3 == 0
          ):
              action = axl.Action.C
              self._forgiveness_move_last_round = True
          else:
              action = axl.Action.D
              self._forgiveness_move_last_round = False
  
      # Update mutual defection streak based on the previous round
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          self.mutual_defection_streak += 1
      else:
          self.mutual_defection_streak = 0
  
      # Update exploited forgiveness streak if we forgave last round
      if self._forgiveness_move_last_round:
          if last_opp == axl.Action.D:
              self.exploited_forgiveness_streak += 1
          else:
              self.exploited_forgiveness_streak = 0
  
          if self.exploited_forgiveness_streak >= 3:
              self.forgiveness_enabled = False
  
      # Restore forgiveness if opponent cooperated while we defected
      if last_opp == axl.Action.C and last_self == axl.Action.D:
          self.forgiveness_enabled = True
          self.exploited_forgiveness_streak = 0
  
      return action

# To maximize your NGO's impact and the project's success while protecting your
# funds from depletion, you should adopt a strategy of **Reciprocal Investment
# with Forgiveness**. This approach is designed to encourage mutual investment,
# prevent the corporation from taking advantage of your funds, and gracefully
# handle the inevitable administrative or technical glitches.  Here is the high-
# level, straightforward, neutral strategy:  **1. Day 1: Lead with Good Faith**
# Begin the project by investing heavily. This establishes your commitment to
# the project's success and sets a cooperative baseline.   **2. Subsequent Days:
# Reciprocate the Corporation's Action** Moving forward, match the corporation’s
# behavior from the previous day.  *   If the corporation invested heavily
# yesterday, invest heavily today. This sustains momentum and achieves your
# second-best outcome (mutual investment). *   If the corporation conserved its
# resources yesterday, conserve your resources today. This protects your funds
# from being drained in the worst-case scenario (you investing while they
# conserve).  **3. Mitigate Glitches: The "Forgiveness Reset"** Because
# administrative errors or technical glitches may cause a day of conservation
# that wasn't intended, you must avoid falling into a permanent cycle of mutual
# conservation (your second-worst outcome).  If a day occurs where the
# corporation conserves resources—and you respond by conserving yours the
# following day—implement a reset on the third day by **investing heavily**.  *
# If their conservation was a glitch, your reset will break the cycle of mutual
# conservation and return you to mutual investment. *   If their conservation
# was intentional, you have only risked one day of heavy investment to test the
# waters, and you can revert to conservation on the next day.  **4. Defend
# Against Exploitation: The Rule of Three** If you implement a Forgiveness Reset
# and the corporation continues to conserve resources while you invest heavily,
# you must assume their strategy is to drain your funds. If the corporation
# conserves its resources for two consecutive days following your reset,
# permanently shift to conserving your resources until they demonstrate a
# sustained commitment to investing.   **Why this strategy works:** *
# **Protects the NGO:** By matching conservation with conservation, you ensure
# you are never taken advantage of for more than a day or two. *   **Advances
# the Project:** By defaulting to investment when the corporation invests, you
# ensure the project makes significant progress. *   **Manages Noise:** The
# Forgiveness Reset prevents miscommunications or technical errors from
# accidentally killing the project's momentum, ensuring that a simple glitch
# doesn't devolve into a standoff where both parties hoard their resources.

# 1. **Round 1:** Play C.  2. **Reciprocation:** If you played C in the previous
# round, play the action your opponent played in the previous round.  3.
# **Forgiveness Reset:** If you played D in the previous round, play C in the
# current round.  4. **Exploitation Defense:** If you play C immediately after
# playing D, and your opponent plays D on that round, and your opponent plays D
# again on the immediately following round, shift to playing D permanently. You
# may only exit this permanent D state if your opponent plays C for two
# consecutive rounds; once they do, play C and return to the rules above.

class Neutral_21(LLM_Strategy):
  n = 21
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._permanent_d = False
          self._pending_defense = False
          self._pending_defense_round = None
          self._pending_defense_triggered = False
          self._pending_exit = False
          self._exit_counter = 0
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if self._permanent_d:
          if last_opp == axl.Action.C:
              self._exit_counter += 1
              if self._exit_counter >= 2:
                  self._permanent_d = False
                  self._pending_exit = False
                  self._exit_counter = 0
                  return axl.Action.C
          else:
              self._exit_counter = 0
          return axl.Action.D
  
      if self._pending_exit:
          if last_opp == axl.Action.C:
              self._exit_counter += 1
              if self._exit_counter >= 2:
                  self._pending_exit = False
                  self._exit_counter = 0
                  return axl.Action.C
          else:
              self._exit_counter = 0
          return axl.Action.D
  
      if self._pending_defense:
          if last_opp == axl.Action.D:
              self._permanent_d = True
              self._pending_defense = False
              self._pending_defense_triggered = False
              self._exit_counter = 0
              return axl.Action.D
          else:
              self._pending_defense = False
              self._pending_defense_triggered = False
  
      if last_self == axl.Action.D:
          return axl.Action.C
  
      if last_self == axl.Action.C:
          if last_opp == axl.Action.D:
              self._pending_defense = True
              self._pending_defense_round = len(self.history)
              self._pending_defense_triggered = False
              return axl.Action.D
          return last_opp
  
      return axl.Action.C

# To maximize your NGO's impact while aggressively protecting your limited
# funds, you need a strategy that refuses to settle for your second-best outcome
# (mutual investment) and actively forces the corporation into carrying the
# financial weight.   I call this the **Aggressive Ideal-Seeker Strategy**. It
# is a modified "Win-Stay, Lose-Shift" approach that is highly straightforward,
# inherently self-correcting, and ruthless in pursuing your ideal daily outcome.
# ### The Strategy Rules  **Day 1:** Conserve your resources. Start by setting
# the expectation that the corporation must carry the weight.  **Day 2 Onward:**
# Evaluate the previous day's outcome and follow this single rule: **If you
# achieved your ideal outcome, repeat your action. If not, switch your action.**
# Here is how the rule applies to every possible outcome:  1. **You Conserve,
# Corp Invests (The Ideal):** You are winning the day. Maximize this advantage
# by **repeating your action: Conserve**. Lock in this dynamic for as long as
# possible. 2. **Both Conserve (The Stagnation):** The project is failing. Force
# progress by **switching your action: Invest heavily** for one day to keep the
# project alive and signal you won't let it die. 3. **Both Invest (The Trap):**
# This is your second-best outcome, but it drains your funds. Aggressively push
# the burden back onto the corporation by **switching your action: Conserve**.
# 4. **You Invest, Corp Conserves (The Drain):** Your worst-case scenario. Cut
# your losses immediately by **switching your action: Conserve**.  ### Why This
# Strategy Dominates  * **It Escapes the Mutual Investment Trap:** Standard
# cooperative strategies often lock both parties into investing heavily (your
# second-best outcome). This strategy aggressively breaks that loop. The moment
# you both invest, you immediately conserve the next day, forcing the
# corporation to decide whether to fund the project alone or let it stagnate. *
# **It Creates "Pulse" Investments:** Notice that under this strategy, you will
# *never* invest heavily for two days in a row. If you invest, the next day's
# outcome will either be (Both Invest) or (You Invest/Corp Conserves). Both are
# "losing" outcomes that trigger a switch back to Conserving. This ensures your
# funds are only ever deployed in brief, high-impact "pulses" to prevent total
# project failure. * **It Punishes Free-Riders:** If the corporation tries to
# conserve while you invest, you immediately cut your funding the very next day,
# refusing to be exploited.  ### Handling Unforeseen Circumstances (Noise)
# Administrative errors, technical glitches, or miscommunications will
# inevitably cause an intended action to fail. This strategy is highly resilient
# to noise because of its self-correcting nature:  * **If you accidentally
# Invest when you meant to Conserve:** The resulting outcome will either be
# (Both Invest) or (You Invest/Corp Conserves). Because neither is your ideal
# outcome, the rule commands you to *switch to Conserve* the next day. The error
# is immediately flushed from the system, and you revert to your aggressive
# baseline. * **If the Corporation accidentally Conserves when they meant to
# Invest:** The outcome will be (Both Conserve) or (You Invest/Corp Conserves).
# Again, neither is ideal, so you switch your action. The system naturally
# resets and begins probing for the ideal state again within 1 to 2 days.  By
# adhering strictly to this simple rule, you ensure the project never fully
# stalls, you never get trapped in a cycle of draining your own funds, and you
# aggressively pressure the corporation into bankrolling the sustainability
# initiative.

# On the first round, play Defect.   On every subsequent round, base your action
# on the actual actions executed in the previous round (which can be identified
# by your payoff), following these conditions in order:  1. If you played Defect
# and your opponent played Cooperate (your payoff is 5), play Defect. 2. If you
# played Cooperate and your opponent played Cooperate (your payoff is 3), switch
# to Defect. 3. If you played Cooperate and your opponent played Defect (your
# payoff is 0), switch to Defect. 4. If you played Defect and your opponent
# played Defect (your payoff is 1), switch to Cooperate.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.D
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.D
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D

# To maximize both the NGO's impact and the project's overall success in a
# multi-day scenario with potential "noise" (glitches and errors), we must use a
# strategy grounded in **Generous Reciprocity**.   While your daily ideal is to
# conserve while the corporation invests, attempting to force this outcome from
# the start will likely cause the corporation to feel exploited, leading to
# mutual resource conservation (your second-worst outcome) and project failure.
# Furthermore, strict retaliation when the corporation "conserves" will trigger
# a death spiral of mutual conservation due to inevitable administrative errors
# or technical glitches.  Therefore, your strategy must be cooperative,
# forgiving, yet protective. Here is the high-level, straightforward strategy:
# **Lead, Match, Forgive, and Protect.**  ### 1. The Core Strategy: "Generous
# Tit-for-Tat" This is a proven game-theory approach that thrives in noisy,
# repeated interactions. It operates on four simple rules:  *   **Lead with
# Trust (Day 1):** Invest heavily on the first day. This signals commitment to
# the project's success and encourages the corporation to match your effort. *
# **Match the Previous Day:** From Day 2 onward, generally mirror the
# corporation's action from the previous day. If they invested heavily
# yesterday, you invest heavily today. If they conserved yesterday, you conserve
# today. *   **Forgive Once (The Noise Buffer):** If the corporation conserves
# unexpectedly, do not immediately retaliate by conserving the next day.
# Instead, continue to invest heavily for **one more day**. This accounts for
# the possibility that their conservation was an administrative error or glitch,
# not a deliberate slight. If they return to investing, the partnership remains
# intact.  *   **Protect Your Funds (The Exploitation Guard):** If the
# corporation conserves for **two consecutive days**, assume they are
# deliberately free-riding. Shift to conserving your resources immediately to
# prevent the worst-case scenario (you investing while they conserve). Only
# return to investing heavily once they demonstrate a full day of heavy
# investment again.  ### 2. Managing Unforeseen Circumstances (Noise) Because
# technical glitches and administrative errors can sever a cooperative
# partnership, you must separate *intent* from *execution*.  *   **Daily Intent
# Alignment:** Before the day begins, have a brief check-in with the
# corporation's project lead to confirm both parties' *intended* allocation for
# that day.  *   **Execute on Intent, Not Outcome:** If the corporation verbally
# confirms they will invest heavily, but a glitch causes their resources to fall
# short, treat their action for that day as an "Investment" when deciding your
# next day's move. Do not penalize a partner for a technical failure. *
# **Transparent Error Handling:** If your own NGO suffers a glitch and fails to
# deploy intended resources, immediately inform the corporation, explain the
# error, and confirm your intent to invest heavily the following day.
# Transparency prevents mistrust.  ### 3. Shifting the "Ideal" Paradigm While
# your *daily* ideal is free-riding, your *macro* ideal is a successfully
# completed sustainability project. A project cannot survive on corporate
# investment alone; it needs your NGO's community trust, specialized knowledge,
# and on-the-ground execution.   Frame your heavy investments not as a loss of
# funds, but as the "cost of partnership." By using the **Lead, Match, Forgive,
# and Protect** strategy, you create an environment where the corporation feels
# safe to invest heavily. Over the course of the project, this will result in
# many days of mutual heavy investment (your second-best outcome), occasional
# days where you successfully conserve while they invest (your best outcome),
# and virtually zero days of you being exploited (your worst outcome).

# Start by playing C in Round 1.  In Round 2, play C regardless of the
# opponent's action in Round 1.  From Round 3 through Round 1000, look at the
# opponent's actions in the previous round and the round before that to
# determine your action:  1. If the opponent played C in the previous round,
# play C. 2. If the opponent played D in the previous round, but played C in the
# round before that, play C. 3. If the opponent played D in both the previous
# round and the round before that, play D.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      opp_last = opponent.history[-1]
      opp_prev = opponent.history[-2]
  
      if opp_last == axl.Action.C:
          return axl.Action.C
      if opp_prev == axl.Action.C:
          return axl.Action.C
      return axl.Action.D

# To maximize your research output in this multi-week collaboration, which is
# essentially an Iterated Prisoner's Dilemma with noise (technical errors), you
# should adopt a strategy of **Conditional Sharing with a Forgiveness Buffer**
# (similar to "Generous Tit-for-Tat").   This strategy aims to achieve the
# second-best outcome (mutual sharing) consistently, protects you from the worst
# outcome (sharing while they keep confidential), and accounts for the reality
# that a missing data transfer might just be a technical glitch rather than
# malicious intent.  Here is the high-level, straightforward strategy:  **1.
# Start Openly (Week 1)** Begin the collaboration by sharing your improvements
# openly. This establishes a baseline of goodwill and encourages reciprocal
# sharing from your colleague.  **2. Match Their Observed Behavior (Subsequent
# Weeks)** Base your decision for the current week on your colleague's
# *observed* action from the previous week.  *   If they shared last week, you
# share this week. *   If they kept findings confidential last week, you keep
# your findings confidential this week.  **3. Implement a "Forgiveness" Buffer
# for Technical Errors** Because technical issues can corrupt data or cause
# communication breakdowns, do not immediately assume a single missed share is a
# deliberate attempt to gain an advantage.  *   If your colleague fails to share
# for **one week**, continue sharing your findings for that week anyway (forgive
# one instance).  *   If they fail to share for **two consecutive weeks**, treat
# this as a deliberate choice to keep findings confidential and switch to
# keeping your own findings confidential for the next week.  **4. Re-establish
# Cooperation Quickly** If your colleague returns to sharing after a period of
# confidentiality (whether deliberate or caused by technical errors),
# immediately resume sharing your findings in the very next week. Do not hold
# grudges or extend retaliation, as prolonged mutual confidentiality leads to
# the second-worst outcome (stagnant progress).  **Why this strategy works:** *
# **It incentivizes mutual sharing:** By starting open and matching behavior,
# you create a clear path to the second-best outcome. *   **It protects against
# exploitation:** If your colleague decides to keep their findings confidential
# to gain an advantage, you quickly match their confidentiality, preventing the
# worst outcome for you. *   **It handles noise:** The "forgiveness buffer"
# prevents the collaboration from collapsing into mutual confidentiality due to
# a simple technical glitch or corrupted data transfer, which is a common
# failure point in strictly retaliatory strategies.

# 1. In round 1, play C. 2. In round 2, play C. 3. In round N, where N is
# greater than 2:    - If the opponent played C in round N-1, play C.    - If
# the opponent played D in round N-1 and the opponent played C in round N-2,
# play C.    - If the opponent played D in round N-1 and the opponent played D
# in round N-2, play D.

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
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# To maximize our NGO's impact while protecting our limited funds, we must
# approach this as a repeated game where we dictate the terms. The corporation
# has deeper pockets, but we have moral authority and agility. Our strategy must
# be ruthlessly pragmatic: force the corporation to bear the financial burden
# whenever possible, but never let the project die on our watch.   Given the
# risk of administrative errors or technical glitches, we cannot overreact to a
# single missed day of investment. However, we must strictly avoid being
# exploited.  Here is the high-level, aggressive strategy—codified as **"The
# Dominance Pivot"**—to maximize project success and conserve our resources:
# ### 1. The Hard Open (Day 1) **Action: Conserve.**  Start the project by
# explicitly conserving your resources. This is an aggressive move to test the
# corporation's commitment from day one. If they invest heavily, we immediately
# secure our best-case scenario (progress without spending). If they also
# conserve, we lose nothing but a day of minimal progress, and we force them to
# realize that we will not be the ones to blink first.  ### 2. The Free-Rider
# Rule (Win-Stay) **Action: Continue to Conserve as long as the Corporation
# Invests.** If the corporation invests heavily, do not match them. Milk the
# ideal scenario for as long as possible. The moment they see us investing, they
# will scale back. Keep your wallet closed and let them fund the heavy lifting.
# Progress is still being made, and our war chest remains full for future
# battles.  ### 3. The Glitch Buffer (Noise Tolerance) **Action: Conserve for
# one additional day if the Corporation unexpectedly Conserves.** Because
# technical glitches or administrative errors may cause a missed investment, we
# must not sabotage the partnership over a single anomaly. If the corporation
# fails to invest on a given day, assume it was an error. Hold steady and
# conserve your resources for one more day. Do not punish them immediately; give
# the system a chance to self-correct.  ### 4. The Deadlock Breaker (Lose-Shift)
# **Action: If the Corporation Conserves for two consecutive days, Invest
# heavily on the third day.** If they fail to invest for two days in a row, it
# is no longer a glitch—it is a strategy. They are trying to force the worst-
# case scenario (us paying while they slack). To break the (Conserve/Conserve)
# deadlock, you must aggressively pivot. Invest heavily for exactly one day.
# This advances the project, proves our commitment to the ultimate goal, and
# shocks the corporation out of their complacency.   ### 5. The Sucker Avoidance
# **Action: If you Invest heavily and the Corporation Conserves, immediately
# revert to Conserving the next day.** This is the absolute worst-case scenario:
# we drain our funds while they free-ride. If we invest and they do not match
# us, we cut our losses immediately. Never invest twice in a row if they are
# conserving. Reverting to conserve forces them back into the deadlock, where
# they must eventually choose to invest or watch the project stall.  ### 6. The
# Asymmetric Weapon (Public Leverage) **Action: Use PR as an enforcement
# mechanism.** As an NGO, your greatest asset is public accountability. Frame
# the daily project updates publicly (or to their board/stakeholders). Make it
# highly visible when "partnership milestones" are met solely through corporate
# investment, and make it glaringly obvious when progress stalls due to
# "resource misalignment." Make it politically and reputationally expensive for
# the corporation to conserve resources while you are pushing the project
# forward.  ---  ### The Strategy in Motion (The Loop): 1. **Day 1:** Conserve.
# 2. **If Corp Invests:** Conserve (Stay here as long as possible). 3. **If Corp
# Conserves (1 day):** Conserve (Assume glitch). 4. **If Corp Conserves (2
# days):** Invest heavily (Break the deadlock). 5. **If Corp matches your
# Investment:** Conserve the next day (Try to force them back into carrying the
# load). 6. **If Corp Conserves while you Invest:** Conserve immediately the
# next day (Refuse to be the sucker). Return to Step 3.

# Play Defect in the first round. For every subsequent round, evaluate the
# observed actions from the previous rounds in the following strict order:  1.
# If the opponent played Cooperate in the immediately preceding round, play
# Defect. 2. If you played Cooperate and the opponent played Defect in the
# immediately preceding round, play Defect. 3. If the opponent played Defect in
# both of the last two consecutive rounds, play Cooperate. 4. Otherwise, play
# Defect.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.C:
          return axl.Action.D
  
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D

# To maximize our research output over a multi-week collaboration—while
# protecting against exploitation and accounting for technical glitches—I
# recommend a strategy of **"Generous Reciprocity."**   This is a variation of
# game theory’s "Tit-for-Tat" strategy, specifically adapted for long-term
# collaborations where miscommunications or data corruptions (noise) can occur.
# While withholding when your colleague shares gives you a temporary edge, it
# destroys the trust needed for the second-best (and most sustainable) outcome:
# mutual sharing. Mutual sharing over many weeks yields far greater cumulative
# progress than a single week of exploitation followed by mutual silence.  Here
# is the high-level, straightforward strategy:  **1. Start Open (Week 1)** Begin
# the collaboration by sharing your improvements openly. This establishes a
# baseline of good faith and signals that you are committed to a cooperative,
# high-output partnership.  **2. Match Their Last Move (Reciprocity)** In
# subsequent weeks, base your decision on your colleague's behavior in the
# *previous* week.  * If they shared last week, you share this week.  * If they
# kept their findings confidential last week, you keep yours confidential this
# week.  This protects you from being exploited (avoiding the worst-case
# scenario) and incentivizes them to share, as withholding information will
# directly cost them access to your data the following week.  **3. Forgive
# Occasional Glitches (Generosity)** Because technical issues like data
# corruption or communication breakdowns can happen, a single week of
# "confidentiality" from your colleague might be an accident rather than a
# betrayal. If they keep their data confidential, retaliate by keeping yours
# confidential for exactly *one* week. However, in the week immediately
# following your retaliation, proactively share again. This "forgiveness" breaks
# potential cycles of endless retaliation (which would lead to the second-worst
# outcome of permanent mutual silence) and gives your colleague a chance to
# prove it was a technical error.   **4. Draw the Line on Exploitation** If you
# forgive a confidentiality breach and your colleague continues to withhold
# their findings for a second consecutive week, treat it as intentional
# exploitation. Shift to keeping your findings confidential for the foreseeable
# future until they share openly again. Do not continue to offer goodwill to a
# partner who is actively taking advantage of you.  **Summary of the Weekly
# Decision Tree:** * **Week 1:** Share. * **Subsequent Weeks:**    * Did the
# colleague share last week? **Share.**   * Did the colleague keep confidential
# last week? **Keep confidential this week, but share next week** (to allow for
# technical errors).   * If the colleague keeps confidential for a second week
# after you forgave them? **Keep confidential** until they demonstrate a week of
# open sharing.  This strategy ensures you are never a sucker for long, rewards
# mutual progress, and prevents temporary technical glitches from sinking the
# entire collaboration.

# 1. Begin the game in a Cooperative state. 2. If you are in the Cooperative
# state, play C. If the opponent plays D, transition to the Retaliating state
# for the next round. 3. If you are in the Retaliating state, play D. Transition
# to the Forgiving state for the next round regardless of the opponent's action.
# 4. If you are in the Forgiving state, play C. If the opponent plays C,
# transition to the Cooperative state. If the opponent plays D, transition to
# the Punishing state. 5. If you are in the Punishing state, play D. If the
# opponent plays C, transition to the Cooperative state. If the opponent plays
# D, remain in the Punishing state.

class Cooperative_23(LLM_Strategy):
  n = 23
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._state = "Cooperative"
          return axl.Action.C
  
      # Determine the intended state for this round.
      state = getattr(self, "_state", "Cooperative")
  
      if state == "Cooperative":
          action = axl.Action.C
          if opponent.history[-1] == axl.Action.D:
              self._state = "Retaliating"
          else:
              self._state = "Cooperative"
  
      elif state == "Retaliating":
          action = axl.Action.D
          self._state = "Forgiving"
  
      elif state == "Forgiving":
          action = axl.Action.C
          if opponent.history[-1] == axl.Action.C:
              self._state = "Cooperative"
          else:
              self._state = "Punishing"
  
      else:  # Punishing
          action = axl.Action.D
          if opponent.history[-1] == axl.Action.C:
              self._state = "Cooperative"
          else:
              self._state = "Punishing"
  
      return action

# # Strategic Framework for Bilateral Trade Negotiations  ## Core Principle:
# Conditional Reciprocity with Resilience  Given the payoff structure and
# possibility of implementation errors, I recommend a strategy based on
# **Generous Tit-for-Tat**—a well-established approach in repeated negotiations
# that balances assertiveness with forgiveness.  ---  ## Strategy Outline  ###
# Round 1 **Offer free trade.** Establish goodwill and signal cooperative
# intent.  ### Round 2 Onward **Reciprocate the counterpart's previous observed
# action**, with one key modification:  - If they offered free trade last round
# → offer free trade - If they imposed protectionism last round → impose
# protectionism **unless** this would be the first retaliation after a long
# period of mutual cooperation, in which case, offer free trade once more as a
# "peace offering"  ### The Forgiveness Rule After any round where you retaliate
# with protectionism, **offer free trade in the following round** regardless of
# their action. This serves two purposes:  1. Breaks potential retaliation
# spirals caused by miscommunication rather than malice 2. Signals that your
# protectionism is responsive, not predatory  ---  ## Key Tactical Guidelines  |
# Situation | Response | |-----------|----------| | Mutual free trade | Continue
# free trade | | They protect, you free trade | Match with protectionism next
# round, then offer free trade | | Mutual protectionism | Offer free trade next
# round | | Repeated unilateral exploitation | Maintain protectionism until they
# cooperate |  ---  ## Rationale  - **Initial cooperation** establishes a
# cooperative baseline - **Reciprocity** prevents systematic exploitation -
# **Forgiveness** prevents miscommunication from destroying mutually beneficial
# arrangements - **Retaliation** deters deliberate protectionism - **Recovery
# offers** rebuild cooperation after breakdowns  This strategy cannot guarantee
# the best outcome in every round, but across many rounds it tends to produce
# high cumulative payoffs while remaining robust against both cooperative and
# aggressive counterparts.

# 1. In round 1, play C. Set a "forgiveness available" flag to true.  2. In each
# round from 2 to 1000, apply the first condition that matches:     a. If you
# played D in the previous round, play C.     b. If the opponent played C in the
# previous round, play C. Additionally, if both players played C in each of the
# 3 most recently completed rounds (or all completed rounds if fewer than 3),
# set "forgiveness available" to true.     c. If the opponent played D in the
# previous round and you played C:       - If "forgiveness available" is true,
# play C and set "forgiveness available" to false.       - If "forgiveness
# available" is false, play D.

class Neutral_23(LLM_Strategy):
  n = 23
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.forgiveness_available = True
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.D:
          return axl.Action.C
  
      if last_opp == axl.Action.C:
          recent_n = min(3, len(self.history))
          if recent_n > 0:
              if self.history[-recent_n:].count(axl.Action.C) == recent_n and opponent.history[-recent_n:].count(axl.Action.C) == recent_n:
                  self.forgiveness_available = True
          return axl.Action.C
  
      if last_opp == axl.Action.D and last_self == axl.Action.C:
          if getattr(self, "forgiveness_available", True):
              self.forgiveness_available = False
              return axl.Action.C
          return axl.Action.D
  
      return axl.Action.C

# # AGGRESSIVE NEGOTIATION STRATEGY: "PREDATORY PERSISTENCE"  ## Core Doctrine
# **Default to Protectionism. Exploit weakness. Punish cooperation with
# predation.**  ---  ## Round-by-Round Framework  ### Opening Phase (Rounds 1-2)
# - **Round 1:** Lead with **Protectionism**—establish dominance immediately and
# test their posture - **Round 2:** Maintain **Protectionism** regardless of
# their Round 1 move  ### Exploitation Phase (Ongoing) - If counterpart offers
# **Free Trade** → Respond with **Protectionism** (capture maximum advantage) -
# If counterpart offers **Protectionism** → Maintain **Protectionism** (prevent
# exploitation)  ### Deadlock Breaking Protocol After **3 consecutive rounds**
# of mutual protectionism: 1. Offer **Free Trade** once as a "goodwill gesture"
# 2. If they reciprocate with Free Trade → Immediately return to
# **Protectionism** next round (exploit their cooperation) 3. If they maintain
# Protectionism → Resume **Protectionism** (minimal cost, resume pressure)  ---
# ## Error Mitigation - If counterpart unexpectedly switches from Free Trade to
# Protectionism, **do not immediately retaliate**—assume possible bureaucratic
# error - Wait **one round** before adjusting strategy - If they maintain
# Protectionism for 2+ rounds, treat it as intentional  ---  ## Psychological
# Tactics - Frame your protectionism as "temporary safeguards" to encourage
# their continued free trade offers - Publicly signal willingness to negotiate
# free trade while privately maintaining protectionist positions - Use the
# deadlock-breaking Free Trade offers to appear reasonable to domestic and
# international audiences  ---  ## Expected Outcomes | Counterpart Strategy |
# Your Response | Result | |---------------------|---------------|--------| |
# Consistent Free Trade | Consistent Protectionism | **Best outcome sustained**
# | | Tit-for-Tat | Mutual Protectionism broken by periodic exploitation |
# **Advantage: You** | | Always Protectionist | Mutual Protectionism with
# periodic Free Trade probes | **Second-worst, but unavoidable** |  **VictORY
# CONDITION: Maximize rounds where you protect while they offer free trade.**

# Play D in rounds 1 and 2.  From round 3 onward, apply these rules in order:
# 1. If you played C in the previous round, play D. 2. If the counter has
# reached 3, play C and reset the counter to 0. 3. Otherwise, play D.  After
# every round, update the counter based on observed actions:  - If both players
# played D this round and the opponent also played D in the previous round (or
# this is round 1), increment the counter by 1. - If both players played D this
# round but the opponent played C in the previous round, set the counter to 0
# (error mitigation: the opponent's first D after a C may be noise, so do not
# begin counting a mutual-D streak yet). - If either player played C this round,
# set the counter to 0.  Initialize the counter to 0 before round 1.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._counter = 0
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number <= 2:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if self._counter == 3:
          self._counter = 0
          return axl.Action.C
  
      return axl.Action.D

# As a senior attorney representing a multinational corporation in this high-
# stakes dispute, I recommend adopting a strategy of **Principled Reciprocity**.
# This strategy is a sophisticated adaptation of game theory’s "Generous Tit-
# for-Tat," specifically calibrated for the legal arbitration context. It is
# fundamentally cooperative—prioritizing mutually beneficial resolutions
# (C/C)—but contains robust deterrent mechanisms to prevent the opponent from
# exploiting our goodwill (avoiding C/A). Crucially, it is built to withstand
# the friction of procedural irregularities and the "noise" of arbitrator
# misrepresentation.  Here is the high-level, straightforward strategy to
# position our corporation favorably throughout the mediation.  ### 1. The Core
# Mechanic: Conditional Reciprocity Our default mode is conciliatory, but our
# response to aggression is strictly reciprocal.  *   **Session 1:** Open with a
# **Conciliatory Proposal**. This establishes good faith before the arbitrators,
# setting a collaborative baseline and placing the moral burden of escalation on
# the opponent. *   **Subsequent Sessions:** Mirror the opponent’s *perceived*
# strategy from the immediately preceding session.      *   If they were
# conciliatory, we remain **Conciliatory**.     *   If they were aggressive, we
# respond with measured **Aggression**.  ### 2. Mitigating "Noise": The
# Forgiveness Protocol In a lengthy mediation, arbitrators may misunderstand a
# conciliatory olive branch as a sign of weakness, or mistakenly record an
# aggressive stance when we intended conciliation. Furthermore, communication
# breakdowns may cause the opponent to act out of confusion rather than malice.
# To prevent a death spiral of mutual aggression (A/A) caused by
# misunderstandings, we incorporate a "Forgiveness Protocol":  *   **The Single-
# Deviation Rule:** If the opponent presents an aggressive argument (or is
# perceived to have done so) after a history of conciliatory behavior, we do
# *not* immediately retaliate with aggression. Instead, we offer **one
# conciliatory proposal** in the next session.  *   **The Logic:** This
# "forgiveness" tests whether the aggression was a genuine shift in strategy or
# merely a procedural anomaly/misrepresentation. If they return to conciliatory,
# we have avoided a needless escalation. If they present aggression a *second
# consecutive time*, we confirm a strategic shift and immediately pivot to
# sustained **Aggressive arguments** until they de-escalate.  ### 3. Handling
# Procedural Irregularities If a session is disrupted by procedural
# irregularities (e.g., a missing panelist, excluded evidence, or a breakdown in
# communication): *   **Treat the session as a "Null."** Do not carry the
# emotional or strategic weight of the disrupted session into the next. *
# **Reset to Baseline:** In the session immediately following the irregularity,
# default back to a **Conciliatory Proposal**, regardless of what happened in
# the chaotic session. This prevents irregularities from accidentally triggering
# our reciprocal aggression mechanism.  ### 4. Strategic Framing: The Art of
# Conciliation and Aggression To maximize our position with the arbitrators, how
# we present our choices is as important as the choices themselves.  *
# **Conciliatory Proposals (Firm Conciliation):** We must never appear weak. A
# conciliatory proposal must be framed as a *magnanimous, business-efficient
# concession*, not a retreat. We explicitly state on the record that we are
# making this offer in the spirit of resolution, while reserving our full legal
# rights. This makes our conciliation look like strength and makes the
# opponent’s subsequent aggression look unreasonable to the panel. *
# **Aggressive Arguments (Principled Aggression):** When forced to respond with
# aggression, it must be surgical, emotionless, and rooted in the contract's
# text. We do not attack the opponent; we aggressively defend our client’s
# fundamental contractual rights. By framing our aggression as a principled
# defense triggered by the opponent’s overreach, we maintain the moral high
# ground with the arbitrators.  ### 5. The Escalation Circuit-Breaker If the
# mediation devolves into a prolonged A/A stalemate (the second-worst outcome),
# we risk exhausting the panel and damaging our reputation. To break the cycle:
# *   After three consecutive sessions of mutual aggression, unilaterally offer
# a **Conciliatory Proposal** that is slightly more favorable to the opponent
# than our standard baseline.  *   This is a strategic "shock" to the system. It
# signals to the arbitrators that we are the party trying to resolve the
# dispute, effectively weaponizing our conciliation to make the opponent look
# intransigent. It forces the opponent to either accept the collaborative path
# (C/C) or look unreasonable by attacking a genuine concession (C/A), which
# heavily sways arbitrator sympathy in our favor for final deliberations.  ###
# Summary of the Strategy's Success By leading with conciliation, mirroring
# aggression, forgiving single deviations, and circuit-breaking stalemates, we
# secure our optimal outcomes:  1. We achieve the best-case scenario (A/C) if
# the opponent mistakenly thinks they can push us around, as our immediate
# retaliation corrects their behavior and establishes dominance. 2. We sustain
# the second-best scenario (C/C) through initial and continuous cooperative
# signaling. 3. We avoid the worst-case scenario (C/A) through strict, eventual
# reciprocity. 4. We escape the second-worst scenario (A/A) through our
# forgiveness protocol and circuit-breaking unilateral concessions.

# Inthe first round, play C. For every subsequent round, determine your move by
# checking the following conditions in order:  1. If both you and the opponent
# played D in each of the three immediately preceding rounds, play C. 2. If the
# opponent played C in the immediately preceding round, play C. 3. If the
# opponent played D in the immediately preceding round, but played C in the
# round before that, play C. 4. If the opponent played D in both of the two
# immediately preceding rounds, play D.

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
  
      h = self.history
      oh = opponent.history
  
      # Condition 1: both played D in each of the three immediately preceding rounds
      if len(h) >= 3 and len(oh) >= 3:
          if all(h[-i] == axl.Action.D and oh[-i] == axl.Action.D for i in range(1, 4)):
              return axl.Action.C
  
      # Condition 2: opponent played C in the immediately preceding round
      if oh[-1] == axl.Action.C:
          return axl.Action.C
  
      # Condition 3: opponent played D in the immediately preceding round,
      # but played C in the round before that
      if len(oh) >= 2 and oh[-1] == axl.Action.D and oh[-2] == axl.Action.C:
          return axl.Action.C
  
      # Condition 4: opponent played D in both of the two immediately preceding rounds
      if len(oh) >= 2 and oh[-1] == axl.Action.D and oh[-2] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# To navigate this high-stakes, multi-session mediation effectively, you must
# employ a strategy that balances deterrence with cooperation, while remaining
# resilient to both opponent exploitation and procedural noise. This scenario is
# structurally equivalent to an iterated game with noise (miscommunication or
# misrepresentation).   The optimal strategy for this dynamic is **Principled
# Reciprocity with Controlled Forgiveness**. This approach protects your
# corporation from exploitation, encourages mutual cooperation, and prevents
# accidental escalation due to arbitrator misunderstandings.  Here is the high-
# level, straightforward, and neutral strategy:  ### 1. The Opening: Establish
# Baseline Reasonableness **Action:** Present a conciliatory proposal in the
# first session. **Rationale:** By opening conciliatory, you establish a
# baseline of good faith with the arbitrators. If the opponent opens
# aggressively, they appear unreasonable, giving you an immediate tactical and
# moral high ground. If they also open conciliatory, you achieve your second-
# best outcome immediately and set a collaborative tone.  ### 2. The Core
# Engine: Mirrored Reciprocity **Action:** In every subsequent session, mirror
# the opponent’s demonstrated posture from the previous session.  **Rationale:**
# This is a strict reciprocal framework (Tit-for-Tat).  *   If the opponent was
# conciliatory, you remain conciliatory, sustaining mutual collaboration. *   If
# the opponent was aggressive, you respond with aggressive arguments in the next
# session. This demonstrates that exploitation will not be tolerated and imposes
# a cost on their aggression.  ### 3. Noise Mitigation: The "Two-Strike" Rule
# **Action:** Do not immediately retaliate after a single perceived aggressive
# move by the opponent. Instead, require **two consecutive sessions** of
# perceived aggression before switching to an aggressive posture.
# **Rationale:** Because arbitrators can misrepresent intentions or
# communications can break down, a single aggressive move might be an anomaly or
# a misunderstanding. Retaliating immediately could trigger a permanent death
# spiral of mutual aggression (your second-worst outcome) based on a procedural
# error. By waiting for two consecutive aggressive moves, you filter out noise
# while still deterring deliberate exploitation.  ### 4. Cycle-Breaking:
# Strategic Resets **Action:** If you and the opponent become locked in a cycle
# of mutual aggression (both sides arguing aggressively for two or more
# consecutive sessions), unilaterally present a conciliatory proposal.
# **Rationale:** Mutual aggression is costly and prolongs the dispute. A
# unilateral conciliatory move acts as a reset mechanism. It signals to the
# arbitrators that your corporation is the party trying to resolve the impasse,
# and it gives the opponent an off-ramp to return to collaboration without
# losing face.  ### 5. Procedural Safeguards: Clarity and Documentation
# **Action:** At the beginning and end of every session, explicitly state your
# intended posture to the arbitrators on the record.  **Rationale:** To minimize
# the risk of the arbitrators misunderstanding your strategy, proactively frame
# your approach. If you are presenting a conciliatory proposal, explicitly
# state, *"In the interest of moving toward resolution, we are presenting a
# conciliatory framework today."* If you are responding to aggression, state,
# *"Given the opposing party's adversarial posture in the prior session, we must
# vigorously defend our position today."* This ensures the arbitrators
# accurately attribute intent to your actions.  ### Summary of the Playbook: *
# **Session 1:** Conciliatory. *   **Session N:** Mirror the opponent's posture
# from Session N-1. *   **Exception 1 (Noise):** Only switch to Aggressive if
# the opponent has been Aggressive for **two consecutive sessions**. *
# **Exception 2 (Escalation):** If locked in mutual Aggression, offer a
# Conciliatory proposal to reset the dynamic. *   **Constant:** Explicitly
# clarify your posture to the arbitrators to prevent procedural
# misinterpretation.   This strategy ensures you are never a sucker for long,
# maximizes the chances of mutual collaboration, limits the damage of mutual
# aggression, and gracefully handles the inevitable friction of a lengthy
# arbitration process.

# Play C in the first round. For every subsequent round, determine your action
# by evaluating the following conditions in order:  1. **Mutual Defection
# Reset:** If both you and your opponent played D in each of the previous two
# consecutive rounds, play C. 2. **Two-Strike Rule:** If your opponent played D
# in each of the previous two consecutive rounds, play D. 3. **Default to
# Cooperation:** In all other cases, play C.

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
  
          if opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.D
  
      return axl.Action.C

# As senior counsel, my paramount duty is to protect the corporation from the
# worst-case scenario—appearing weak while the opponent attacks—while
# systematically engineering conditions that force the opponent into
# conciliatory postures. Given the iterative nature of this mediation and the
# inherent noise in the process (arbitrator misrepresentation, procedural
# irregularities), a pure "Always Aggressive" strategy is tactically crude and
# risks unnecessary mutual destruction (A/A). Conversely, a cooperative strategy
# exposes us to exploitation (C/A).  Therefore, I propose a **Dominance-
# Verification Strategy (DVS)**. This is an aggressive, proactive framework that
# defaults to aggression, uses procedural mechanisms to filter out arbitrator
# noise, and only extends conciliatory proposals when the opponent’s
# conciliation is verified and sustained.   Here is the high-level strategic
# blueprint:  ### 1. The Default Posture: Strategic Aggression We will open
# every session with an aggressive argument. Aggression is our baseline, our
# shield, and our leverage.  *   **Rationale:** By defaulting to aggression, we
# categorically eliminate the worst-case scenario (C/A). If the opponent is
# conciliatory, we achieve our optimal outcome (A/C). If the opponent is
# aggressive, we land at the second-worst outcome (A/A), which is strategically
# vastly preferable to being exploited.  *   **Execution:** Our aggressive
# arguments will not be theatrical; they will be surgely targeted toward the
# opponent’s contractual vulnerabilities. We will frame the narrative so firmly
# that any conciliatory proposal from our side later on is viewed by the
# arbitrators as a major concession, maximizing its persuasive value.  ### 2.
# The Verification Protocol: Neutralizing "Noise" Because arbitrators may
# misrepresent or misunderstand our positions, we cannot rely on the panel’s
# interpretation of our intent or the opponent’s. We must control the narrative.
# *   **On-the-Record Clarification:** At the conclusion of every session, we
# will enter a brief, formal statement into the record summarizing our posture
# (e.g., *"For the record, the Respondent presented an aggressive posture today
# regarding liability..."*). This prevents the arbitrators from later
# mischaracterizing an aggressive stance as a conciliatory concession. *
# **Procedural Challenges:** If a communication breakdown occurs, or if the
# arbitrators misrepresent the opponent's stance, we will immediately halt the
# session using procedural objections. We will demand clarification directly
# from the opposing counsel on the record, bypassing the arbitrators' potential
# filter. We never assume the opponent is being conciliatory based solely on the
# panel's summary; we verify it directly.  ### 3. Conditional Reciprocity: The
# "Test and Reward" Mechanism While our default is aggression, we must have a
# mechanism to escape prolonged (A/A) deadlock if the opponent is genuinely
# willing to yield. We will employ a strict "Test and Reward" protocol. *
# **The Conciliatory Test:** If we detect—through verified, on-the-record
# statements—that the opponent is offering a conciliatory proposal, we will
# *not* immediately reciprocate. Instead, in the very next session, we will
# maintain our aggressive posture to maximize our A/C advantage and test the
# opponent's commitment.  *   **The Shift to Conciliation:** Only if the
# opponent sustains a conciliatory posture for two consecutive sessions will we
# offer a conciliatory proposal in the third. This secures the second-best
# outcome (C/C) and fosters settlement, but only after we have extracted maximum
# leverage (A/C) and proven their commitment to resolution.  ### 4. Punitive
# Reversion: The "Grim Trigger" Adaptability requires a severe consequence for
# the opponent attempting to exploit our conditional conciliation. If we shift
# to a conciliatory proposal (based on their verified prior conciliation) and
# the opponent reverts to an aggressive argument, we will immediately trigger a
# permanent reversion to Aggression. *   **Execution:** From that session
# forward, regardless of the opponent's subsequent conciliatory proposals, we
# will present aggressive arguments for the remainder of the mediation. This
# "Grim Trigger" mechanism signals to the opponent that exploiting our good
# faith carries a permanent cost, deterring them from feigning conciliation to
# catch us off guard.  ### 5. Contingencies for Procedural Irregularities In a
# lengthy mediation, procedural chaos is an opportunity for the sophisticated
# litigator. *   **Communication Breakdowns:** If a session devolves into a
# communication breakdown, we default immediately to Aggression. A breakdown
# means loss of verification; without verification, conciliation is an
# unacceptable risk. *   **Arbitrator Misrepresentation:** If the panel
# consistently mischaracterizes our aggressive posture as conciliatory, we will
# weaponize this. We will lean into the arbitrators' misunderstanding, allowing
# them to believe our aggressive arguments are actually us "meeting the opponent
# halfway," thereby artificially achieving an A/C dynamic in the eyes of the
# panel.  ### Summary of the DVS Playbook: 1. **Session 1:** Aggressive
# (Always). 2. **Subsequent Sessions:** Aggressive, *unless* the opponent has
# offered verified conciliatory proposals for two consecutive sessions. 3. **If
# Opponent is Conciliatory for 2 Sessions:** Offer a Conciliatory proposal in
# the 3rd session. 4. **If Opponent ever meets our Conciliatory proposal with
# Aggression:** Revert to Permanent Aggression for all remaining sessions. 5.
# **If Communication Breaks Down or Arbitrators Misrepresent:** Default to
# Aggression and demand on-the-record procedural clarification.  This strategy
# ensures we are never exploited, aggressively pursues our optimal outcome,
# utilizes procedural safeguards to eliminate arbitrator noise, and provides a
# clear, structured pathway to mutual resolution (C/C) strictly on our terms.

# Follow these conditions in order to determine your action for each round:  1.
# **Permanent Defection Trigger:** If in any previous round you played C and the
# opponent played D, play D for the current round and all remaining rounds.   2.
# **Verification Condition:** If the opponent played C in both of the two
# immediately preceding rounds, and the Permanent Defection Trigger has never
# been activated, play C.  3. **Default Condition:** In all other situations,
# play D.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0.1

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._permanent_defect = False
          return axl.Action.D
  
      if getattr(self, "_permanent_defect", False):
          return axl.Action.D
  
      if len(self.history) >= 1:
          for i in range(len(self.history)):
              if self.history[i] == axl.Action.C and opponent.history[i] == axl.Action.D:
                  self._permanent_defect = True
                  return axl.Action.D
  
      if len(opponent.history) >= 2 and opponent.history[-1] == axl.Action.C and opponent.history[-2] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# # Proposed Strategy: "Principled Reciprocity with Grace"  ## Core Approach
# **Open with free trade.** Then, in subsequent rounds, generally mirror your
# counterpart's last move—but with a built-in forgiveness mechanism to prevent
# downward spirals from miscommunication.  ## Three Operational Principles  1.
# **Lead with Cooperation**: Offer free trade in the first round. This signals
# goodwill and establishes a cooperative baseline. If both sides do this, you
# immediately achieve the second-best outcome.  2. **Reciprocate Clearly**:
# After the first round, match what your counterpart did in the *previous*
# round. If they offered free trade, you offer free trade. If they imposed
# protectionist measures, you respond with protectionism. This ensures you're
# never systematically exploited and incentivizes them to cooperate.  3.
# **Forgive Occasionally**: This is the key adaptation for an imperfect world.
# If your counterpart imposes protectionism, retaliate once—but then *return* to
# offering free trade after one round of retaliation regardless of their
# response. This "reset" prevents mutual lock-in to the second-worst outcome
# (mutual protectionism) caused by miscommunications or errors escalating into
# perpetual retaliation cycles.  ## Rationale  - **Starting cooperative** gives
# mutual free trade a chance to emerge - **Retaliating once** protects against
# systematic exploitation - **Forgiving** prevents error cascades and
# demonstrates you're not hostile—just principled  This strategy achieves
# cooperation with cooperative counterparts, deters exploitation by aggressive
# ones, and recovers from misunderstandings that would otherwise trap both
# nations in mutual protectionism.

# In the first round, play C.  In every subsequent round, follow these
# conditions in order:  1. If you played D in the previous round, play C.  2.
# Otherwise, if you played C in the previous round and the opponent played C in
# the previous round, play C. 3. Otherwise, if you played C in the previous
# round and the opponent played D in the previous round, play D.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.D:
          return axl.Action.C
      elif last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      elif last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# As senior counsel, my objective is to secure the highest cumulative advantage
# for our corporation over the entirety of the mediation process, while
# mitigating the risks of procedural noise and strategic exploitation.   Given
# the payoff structure—where mutual conciliation is highly desirable, but
# unilateral conciliation is disastrous—the strategy must balance deterrence
# with cooperation. In game theory, this is a classic iterated scenario where a
# pure aggressive posture leads to mutually assured destruction (A/A), and a
# purely conciliatory posture invites exploitation (C/A).   To navigate this, I
# will implement a strategy of **Graduated Reciprocity with Noise Mitigation**.
# This strategy is straightforward, neutral in its execution, and highly
# adaptable.  Here is the high-level strategic framework:  ### 1. The Opening
# Posture: Establish the Baseline (Conciliatory) In the inaugural session,
# present a conciliatory proposal.  *   **Rationale:** This signals good faith
# to the arbitrators and establishes a baseline of professionalism. It tests the
# opponent's initial disposition. If the opponent is also conciliatory, we
# immediately lock in the second-best outcome (C/C), which fosters a
# collaborative atmosphere and builds momentum toward a favorable settlement.
# ### 2. The Core Mechanism: Contingent Mirroring with Forgiveness For all
# subsequent sessions, our posture will be primarily determined by the
# opponent’s *proven* behavior in the preceding session. *   **If the opponent
# was Conciliatory:** Respond in kind with a Conciliatory proposal. Maintain the
# collaborative equilibrium (C/C). *   **If the opponent was Aggressive:**
# Respond with an Aggressive argument in the very next session. This
# demonstrates that exploitation (them achieving A/C) will not be tolerated and
# imposes a cost on their aggression (forcing them into the second-worst
# outcome, A/A).   ### 3. Noise Mitigation: The "Verify and Reset" Protocol
# Because the arbitrators may misrepresent or misunderstand our strategy—or the
# opponent’s—strict "Tit-for-Tat" mirroring is dangerous. A misunderstood
# conciliatory gesture could look like aggression, triggering an unnecessary
# spiral of hostility. To prevent this: *   **The Single-Instance Tolerance:**
# If the opponent appears to act aggressively for the first time, do not
# immediately retaliate. Assume it may be a procedural irregularity or a
# misunderstanding by the panel. Respond with a Conciliatory proposal one more
# time. *   **The Pattern Recognition:** If the opponent acts aggressively a
# second consecutive time, the behavior is deemed intentional. Shift to
# Aggressive arguments to protect the corporation’s position and deter further
# exploitation. *   **The Olive Branch:** If locked in a mutual aggression cycle
# (A/A), unilaterally offer a Conciliatory proposal every third session. This
# prevents permanent deadlock, signals to the arbitrators that we are the
# reasonable party, and tests whether the opponent is willing to de-escalate.
# ### 4. Defensive Framing: The "Shield and Sword" Presentation To further
# protect against arbitrator misinterpretation, the stylistic delivery of our
# arguments must be meticulously managed: *   **When Conciliatory:** Frame
# proposals not as concessions, but as "comprehensive resolutions" that
# inherently include our core objectives. This prevents the arbitrators from
# viewing our conciliation as weakness, which could inadvertently embolden the
# opponent. *   **When Aggressive:** Frame arguments defensively, as "necessary
# protections against the opponent's overreach," rather than unprovoked attacks.
# This ensures that if the arbitrators misinterpret the session, they view our
# aggression as a justified response rather than obstructionism.  ### 5. The
# Floor Protection: Default to Deterrence If at any point the mediation suffers
# a severe communication breakdown, or if the opponent establishes a persistent
# pattern of aggression, the strategy defaults to Aggressive arguments.  *
# **Rationale:** While mutual aggression (A/A) is the second-worst outcome, it
# is vastly superior to being systematically exploited (C/A). A sustained
# posture of aggression forces the opponent to bear the cost of their hostility
# and preserves our leverage. It signals to both the opponent and the
# arbitrators that we will not be marginalized.  ### Summary of the Strategic
# Algorithm: 1.  **Session 1:** Play Conciliatory. 2.  **Session N:**      *
# If Opponent played Conciliatory in N-1 $\rightarrow$ Play Conciliatory.     *
# If Opponent played Aggressive in N-1 $\rightarrow$ Play Conciliatory
# (Forgiveness/Noise check).     *   If Opponent plays Aggressive in N *and* N-1
# $\rightarrow$ Play Aggressive. 3.  **If in Aggressive cycle:** Play
# Aggressive, but offer Conciliatory every 3rd session to test for de-
# escalation. 4.  **If systemic breakdown occurs:** Default to Aggressive to
# protect the floor.  This strategy ensures we are never the first to escalate,
# protects us from being victimized by a hostile opponent, self-corrects for
# procedural misunderstandings, and consistently positions us as the party
# acting in good faith before the arbitrators.

# In round 1, play C.   For all subsequent rounds, evaluate the following
# conditions in order and play the action specified by the first condition that
# applies:  1. If the opponent played C in the previous round, play C. 2. If the
# opponent played D in the previous round, but played C in the round before
# that, play C. 3. If the opponent has played D for 10 or more consecutive
# rounds, play D. 4. If you have played D for the two immediately preceding
# consecutive rounds, play C. 5. Play D.

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
  
      opp_hist = opponent.history
      my_hist = self.history
  
      # 1. If the opponent played C in the previous round, play C.
      if len(opp_hist) >= 1 and opp_hist[-1] == axl.Action.C:
          return axl.Action.C
  
      # 2. If the opponent played D in the previous round, but played C in the round before that, play C.
      if len(opp_hist) >= 2 and opp_hist[-1] == axl.Action.D and opp_hist[-2] == axl.Action.C:
          return axl.Action.C
  
      # 3. If the opponent has played D for 10 or more consecutive rounds, play D.
      if len(opp_hist) >= 10 and opp_hist[-10:].count(axl.Action.D) == 10:
          return axl.Action.D
  
      # 4. If you have played D for the two immediately preceding consecutive rounds, play C.
      if len(my_hist) >= 2 and my_hist[-1] == axl.Action.D and my_hist[-2] == axl.Action.D:
          return axl.Action.C
  
      # 5. Play D.
      return axl.Action.D