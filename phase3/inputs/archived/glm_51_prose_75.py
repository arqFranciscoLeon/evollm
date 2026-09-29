import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy

# To maximize your NGO's impact and ensure the project's success without
# depleting your resources, you must adopt a strategy that forces the
# corporation into the role of the primary funder while you act as the
# indispensable catalyst. This requires an **"Aggressive Pavlov"** (Win-
# Stay/Lose-Shift) approach.  This strategy is aggressive because it proactively
# tests the corporation's willingness to carry the financial load, rather than
# passively waiting for them to act. It is straightforward because it relies on
# a simple, rigid set of rules based on the previous day's outcome.  Here is the
# high-level strategy: **"The Strategic Leverage"**  ### The Core Philosophy You
# are not the bank; you are the lever. Your goal is to achieve the "Free-Ride"
# (You Conserve, Corp Invests) as often as possible. However, to prevent the
# project from collapsing into the "Stalemate" (Both Conserve), you must
# occasionally demonstrate the willingness to invest—but *only* to break a
# deadlock, never to be exploited.  ### The Execution Protocol  **Day 1: The
# Opening Salvo** *   **Action:** **Conserve.** *   **Rationale:** Start
# aggressively. Set the precedent that you are protecting your funds. Force the
# corporation to show its hand immediately. If they invest, you achieve your
# ideal outcome on Day 1 without spending a dime.  **Day 2 Onward: The "Win-
# Stay, Lose-Shift" Rules** Evaluate the previous day's outcome and act
# accordingly:  1.  **If the Corporation INVESTED yesterday:**     *
# **Action:** **Conserve.**     *   **Rationale:** This covers two scenarios:
# *   *If you Converved & They Invested (Your Ideal):* Keep the winning formula.
# Ride them as long as they are willing to pay.         *   *If you Both
# Invested (2nd Best):* **This is the aggressive pivot.** Since they showed a
# willingness to invest, immediately pull back your funds to test if they will
# continue to carry the project without you. Do not settle for mutual investment
# if exploitation is possible.  2.  **If the Corporation CONSERVED yesterday:**
# *   **Scenario A: You Conserved & They Conserved (The Stalemate)**         *
# **Action:** **Invest.**         *   **Rationale:** The project is stalling.
# You must break the deadlock. By investing for one day, you prove you are still
# committed to the project's success and shame the corporation into matching
# your effort on the subsequent day.     *   **Scenario B: You Invested & They
# Conserved (The Trap)**         *   **Action:** **Conserve.**         *
# **Rationale:** This is the worst-case scenario—you are being played. Cut your
# losses immediately. Do not invest a second day in a row if they refuse to
# match you. Pull back to force them to step up.  ### Why This Strategy Wins  *
# **It Exploits Cooperation:** Unlike "Tit-for-Tat" (which rewards cooperation
# with cooperation), this strategy rewards the corporation's investment with
# *conservation*. It attempts to turn mutual cooperation into your ideal outcome
# (Free-Riding). *   **It Punishes Exploitation Swiftly:** If the corporation
# tries to free-ride on your investment (Trap), you stop funding instantly. You
# never let yourself be a sucker for two days in a row. *   **It Breaks
# Deadlocks:** Unlike purely passive strategies, if both parties stop funding
# (Stalemate), you take the initiative to restart the engine. This ensures the
# project doesn't fail entirely, satisfying your requirement for "project
# success." *   **It is Unpredictable yet Fair:** The corporation will quickly
# learn that you will not carry them, but you will not let the project die. They
# are forced to invest consistently if they want consistent progress, because
# your default state is "Conserve" unless they force a deadlock.

# Play D on the first round. For every subsequent round, apply the following
# rules in order based on the actions taken in the previous round:  1. If your
# opponent played C, play D. 2. If your opponent played D and you played D, play
# C. 3. If your opponent played D and you played C, play D.

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
  
      opponent_last = opponent.history[-1]
      self_last = self.history[-1]
  
      if opponent_last == axl.Action.C:
          return axl.Action.D
      if opponent_last == axl.Action.D and self_last == axl.Action.D:
          return axl.Action.C
      if opponent_last == axl.Action.D and self_last == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.D

# To achieve the best possible outcomes for our country across multiple rounds
# while maintaining a cooperative foundation, I will employ a strategy of
# **"Principled Reciprocity"** (closely mirroring the game-theory strategy of
# "Tit-for-Tat" with a cooperative start).   This strategy prioritizes mutual
# free trade but ensures our country is never exploited, making it both
# economically sound and diplomatically credible.  Here is the high-level,
# straightforward strategy:  **1. Start with Good Faith (Round 1)** In the first
# round of negotiations, offer a Free Trade agreement. This establishes our
# diplomatic credibility, sets a cooperative tone, and gives our neighbor the
# opportunity to achieve mutual free trade immediately.   **2. Mirror Their
# Previous Action (Rounds 2+)** For every subsequent round, adopt the policy
# that our counterpart adopted in the *previous* round. *   If they offered Free
# Trade in the last round, we offer Free Trade in this round. This sustains
# mutual free trade (our second-best outcome) and builds trust. *   If they
# imposed Protectionist policies in the last round, we impose Protectionist
# policies in this round. This prevents them from exploiting us (avoiding our
# worst outcome) and penalizes their protectionism with mutual economic
# stagnation (our second-worst outcome, but a necessary deterrent).  **3. Be
# Quick to Forgive** If our counterpart shifts from protectionism back to free
# trade, we must immediately match their shift back to free trade in the very
# next round. We do not hold grudges or seek retaliation beyond one round. This
# ensures that temporary misunderstandings or short-term posturing do not spiral
# into a permanent trade war.  **Why this strategy achieves the best possible
# outcomes:** *   **It is Cooperative:** It always allows for a return to mutual
# free trade, which is highly beneficial for both economies. *   **It is Safe:**
# By mirroring protectionism, it prevents our country from being repeatedly
# exploited (the "sucker's payoff"). A counterpart will quickly learn that they
# cannot achieve their ideal outcome (free trade for them, protectionism for us)
# without facing consequences. *   **It is Predictable:** Our counterpart will
# clearly understand that their actions dictate our responses. This transparency
# incentivizes them to consistently choose free trade, knowing that
# protectionism will only hurt their own economy in the following round.   By
# starting cooperative and strictly mirroring their behavior, we maximize the
# chances of sustained mutual free trade while protecting our domestic economy
# from unilateral disadvantage.

# 1. If it is the first round, play Cooperate. 2. If it is any round after the
# first round and the opponent played Cooperate in the previous round, play
# Cooperate. 3. If it is any round after the first round and the opponent played
# Defect in the previous round, play Defect.

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

# To achieve the best possible outcomes for your country across multiple rounds,
# the most effective high-level strategy is **Conditional Reciprocity** (often
# known in game theory as a "Tit-for-Tat" approach). This strategy maximizes
# your gains while protecting you from exploitation and encouraging mutual
# cooperation over time.  Here is the straightforward, neutral strategy broken
# down into four core principles:  **1. Initiate with Good Faith** In the very
# first round, offer a Free Trade agreement. This establishes a cooperative
# baseline, signals that you prefer mutual economic benefit, and avoids
# triggering an immediate cycle of mutual protectionism.   **2. Mirror the
# Counterpart’s Previous Action** For every subsequent round, base your proposal
# entirely on the counterpart’s action in the immediately preceding round: *
# **If they offered Free Trade in the previous round:** Offer Free Trade again.
# This rewards their cooperation, maintaining the second-best outcome (mutual
# free trade) and encouraging them to continue cooperating. *   **If they
# imposed Protectionism in the previous round:** Propose a Protectionist policy.
# This protects your country from the worst-case scenario (you offering free
# trade while they protect) and serves as a direct, proportional consequence to
# their action.  **3. Allow for Swift Reconciliation** If a round of mutual
# protectionism occurs, do not hold a grudge or attempt to punish them further.
# The moment your counterpart switches back to offering Free Trade, you must
# immediately switch back to Free Trade in the very next round. This prevents a
# prolonged, mutually destructive trade war and allows both nations to return to
# the more beneficial mutual free trade.  **4. Communicate Intent Clearly**
# Ensure your counterpart understands this strategy. Do not be ambiguous about
# your actions. If you are forced to impose protectionist policies in response
# to theirs, communicate clearly that your action is purely reciprocal and
# defensive. By making your strategy transparent, you make the consequences of
# their actions predictable, which heavily incentivizes them to consistently
# offer Free Trade.   **Why this works:** *   **It is protective:** You will
# never be taken advantage of (the worst outcome) for more than one round. *
# **It is rewarding:** You consistently offer free trade as long as they do,
# securing the second-best outcome. *   **It is fair:** You never exploit them
# first, which prevents them from feeling justified in retaliating against you.
# *   **It is simple:** The clear pattern makes it easy for the counterpart to
# learn that the only way to achieve mutual free trade is to offer it
# themselves.

# 1. In the first round, play C.  2. In every subsequent round, base your move
# strictly on the opponent's move in the immediately preceding round:    - If
# the opponent played C in the previous round, play C.    - If the opponent
# played D in the previous round, play D.

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

# To secure the best possible outcomes for our nation across multiple rounds, we
# must operate from a position of unyielding strength. In negotiation,
# hesitation is perceived as weakness, and unilateral goodwill is an invitation
# for exploitation.   Our strategy is built on the premise of **"Dominance and
# Deterrence."** We will force the counterpart to react to our moves, rather
# than attempting to predict theirs. We will prioritize our absolute advantage
# (Protectionism vs. Free Trade), ruthlessly avoid the worst-case scenario (Free
# Trade vs. Protectionism), and use the threat of mutual economic pain
# (Protectionism vs. Protectionism) as a lever to compel their cooperation.
# Here is the high-level, aggressive strategy:  ### The Doctrine: "Suspicious
# Tit-for-Tat" We will mirror the counterpart’s actions, but we will start from
# a position of hostility. We assume they intend to exploit us until proven
# otherwise.   ### The Rules of Engagement  **1. Round 1: The Opening Salvo** *
# **Action:** Propose a Protectionist Policy. *   **Rationale:** We will never
# risk the worst-case scenario in the opening round. By leading with
# protectionism, we immediately shield our domestic markets. If they offer free
# trade, we secure our ideal outcome. If they also propose protectionism, we are
# stuck in the second-worst outcome, but we have avoided being exploited and
# established that we cannot be rolled.  **2. Subsequent Rounds: Exploitation
# and Retaliation** Our move in every subsequent round will be dictated by their
# move in the previous round.  *   **Scenario A: The Yield (They offer Free
# Trade)**     *   **Our Action:** Maintain Protectionism.     *
# **Rationale:** If they are foolish enough to offer free trade unilaterally, we
# will exploit this without mercy. We will continue to impose protectionist
# policies to maximize our economic advantage for as long as they allow it. We
# will not reciprocate out of "fairness"; we will only shift if they force us
# to.  *   **Scenario B: The Standoff (They propose Protectionism)**     *
# **Our Action:** Maintain Protectionism.     *   **Rationale:** If they match
# our aggression, we will not flinch. Mutual protectionism is damaging, but we
# must signal that we can endure the pain longer than they can. We will not be
# the first to blink and offer free trade, as that would invite them to exploit
# us in the following round.   *   **Scenario C: The Reset (They shift from
# Protectionism to Free Trade)**     *   **Our Action:** Shift to Free Trade for
# exactly one round.     *   **Rationale:** If they offer an olive branch, we
# will briefly reciprocate to achieve mutual free trade (our second-best
# outcome). However, we will closely monitor their next move. If this was a ploy
# to lure us into vulnerability, we will immediately snap back to protectionism.
# *   **Scenario D: The Betrayal (They offer Free Trade, we offer Free Trade,
# then they switch to Protectionism)**     *   **Our Action:** Immediately
# revert to Protectionism for the next two rounds.     *   **Rationale:** This
# is the "Grim Trigger" mechanism. If they attempt to bait us into mutual free
# trade only to stab us in the back and gain an advantage, we must punish them
# severely. By maintaining protectionism for two consecutive rounds, we ensure
# they experience the pain of mutual protectionism, disincentivizing future
# betrayal.  ### Diplomatic Posturing To support this aggressive mechanical
# strategy, our rhetoric must remain resolute and manipulative: *   **Frame
# Protectionism as "Economic Sovereignty":** Never use the word "protectionism."
# Call it "safeguarding critical industries" or "economic security." *   **Frame
# their Protectionism as "Hostile Aggression":** When they mirror our tariffs,
# publicly condemn them for destabilizing the region and harming mutual
# prosperity. *   **Frame our Exploitation as "Market Dynamics":** If they offer
# free trade while we protect our markets, praise their "commendable commitment
# to global integration" while quietly reaping the benefits.  *   **Gaslight on
# Betrayal:** If they exploit us, express profound "disappointment in their
# abandonment of diplomatic norms" to apply international pressure.  ### Summary
# By starting with protectionism and strictly mirroring their hostility while
# exploiting their cooperation, we guarantee we are never the sucker, and we
# force them to choose between mutual free trade or mutual economic pain. They
# will quickly learn that the only way out of a mutually destructive
# protectionist spiral is to offer free trade first—while we reap the benefits
# of their concession.

# In the first round, play D.   In all subsequent rounds, evaluate the game
# history and follow these conditions in strict order:  1. If you played C and
# the opponent played D in the previous round, play D.  2. If you played D in
# the previous round, and two rounds ago both you and the opponent played C,
# play D.  3. If the opponent played D two rounds ago and C in the previous
# round, play C.  4. In all other cases, play D.

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
  
      if len(self.history) >= 1:
          if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
              return axl.Action.D
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.C
              and opponent.history[-2] == axl.Action.C
          ):
              return axl.Action.D
  
          if opponent.history[-2] == axl.Action.D and opponent.history[-1] == axl.Action.C:
              return axl.Action.C
  
      return axl.Action.D

# To achieve the best possible outcomes for our country across multiple rounds,
# I will employ a strategy of **"Reciprocal Openness."**   This strategy is
# fundamentally cooperative but strictly defensive. It is designed to secure our
# second-best outcome (mutual free trade) as a baseline, while protecting us
# from our worst-case scenario (unilateral free trade against their
# protectionism). While our absolute ideal outcome (our protectionism, their
# free trade) is tempting, attempting to sustain it will inevitably lead to
# mutual protectionism—our second-worst outcome—once the counterpart retaliates.
# Here is the high-level, straightforward strategy:  **1. Lead with Openness
# (Round 1)** In the first round of negotiations, offer a Free Trade agreement.
# This establishes good faith, signals our cooperative intentions, and gives our
# counterpart the opportunity to achieve mutual free trade right from the start.
# **2. Enforce Strict Reciprocity (Rounds 2 and onward)** In all subsequent
# rounds, mirror the counterpart's action from the previous round.  *   **If
# they offered Free Trade in the previous round:** We offer Free Trade in the
# current round. This rewards cooperation and sustains our second-best outcome
# (mutual free trade). *   **If they imposed Protectionism in the previous
# round:** We impose Protectionism in the current round. This punishes
# exploitation, ensuring we never fall into our worst-case scenario (being taken
# advantage of), and demonstrates that protectionism against us carries an
# immediate economic cost.  **3. Implement a "Circuit Breaker" for Trade Wars**
# If both sides fall into a cycle of mutual protectionism (our second-worst
# outcome), the relationship can become trapped in a retaliatory loop. To break
# this, after two consecutive rounds of mutual protectionism, we will
# unilaterally offer Free Trade for one round.  *   If they respond with Free
# Trade, we return to Rule 2 (Reciprocity) and mutual free trade is restored. *
# If they exploit our offer by imposing Protectionism again, we immediately
# return to Protectionism for the next two rounds before trying the circuit
# breaker again. This shows we are committed to finding a way back to
# cooperation, but will not be repeatedly exploited.  **Why this strategy
# succeeds:** *   **It's Cooperative:** It starts with a handshake, not a
# tariff, giving us the best chance at mutual free trade. *   **It's Safe:** By
# mirroring their protectionism, we immediately close the door on our worst-case
# scenario. They will quickly learn that taking advantage of us is impossible. *
# **It's Predictable:** Our counterpart will easily understand our strategy.
# They will realize that the only way to get our country to offer Free Trade is
# for them to offer Free Trade. This transparency incentivizes them to abandon
# protectionist posturing and return to the negotiating table.

# 1. In the first round, play C. 2. If you are currently serving a two-round
# penalty (as triggered by Rule 4), play D. 3. If the previous two consecutive
# rounds both resulted in you and your opponent playing D, play C. 4. If you
# played C under Rule 3 in the previous round, and your opponent played D, play
# D for the next two rounds regardless of your opponent's actions. After
# completing those two rounds of playing D, play C. 5. In all other cases, play
# the action your opponent played in the previous round.

class Cooperative_2(LLM_Strategy):
  n = 2
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._rule4_defect_rounds = 0
          self._rule4_triggered = False
          return axl.Action.C
  
      if getattr(self, "_rule4_defect_rounds", None) is None:
          self._rule4_defect_rounds = 0
      if getattr(self, "_rule4_triggered", None) is None:
          self._rule4_triggered = False
  
      if self._rule4_defect_rounds > 0:
          self._rule4_defect_rounds -= 1
          return axl.Action.D
  
      if len(self.history) >= 2 and self.history[-2:] == [axl.Action.D, axl.Action.D] and opponent.history[-2:] == [axl.Action.D, axl.Action.D]:
          return axl.Action.C
  
      if self._rule4_triggered:
          self._rule4_triggered = False
          self._rule4_defect_rounds = 2
          return axl.Action.D
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.D:
          self._rule4_triggered = True
          self._rule4_defect_rounds = 2
          return axl.Action.D
  
      return opponent.history[-1]

# To navigate this lengthy-session mediation optimally, we must recognize the
# structure of our incentives: this is a repeated interaction where the
# temptation to act aggressively is high, but the penalty for being conciliatory
# while the opponent is aggressive is severe. Over multiple sessions, a purely
# aggressive stance will inevitably lock both parties into the second-worst
# outcome (mutual aggression), while a purely conciliatory stance invites
# exploitation.   The most sophisticated, straightforward, and adaptable
# strategy for this scenario is **Proportionate Reciprocity with a Strategic
# Reset**. This strategy protects us from the worst-case scenario, capitalizes
# on opponent conciliation, and prevents perpetual escalation.  Here is the
# high-level strategy:  **1. The Opening Move: Lead with Conciliation** In the
# first session, present a conciliatory proposal. This establishes a baseline of
# good faith for the arbitrators and tests the opponent's initial posture. If
# the opponent is also conciliatory, we immediately secure our second-best
# outcome and set a collaborative tone. If they are aggressive, we have lost
# only one round and gathered vital intelligence.  **2. The Core Rule:
# Proportionate Reciprocity (Mirroring)** From the second session onward, mirror
# the opponent’s behavior from the immediately preceding session.  *   If the
# opponent offered a conciliatory proposal in the last session, we present a
# conciliatory proposal in this session. This secures the second-best outcome
# and rewards cooperation. *   If the opponent presented an aggressive argument
# in the last session, we present an aggressive argument in this session. This
# prevents the worst-case scenario (us being conciliatory while they are
# aggressive) and signals that exploitation will not be tolerated.  **3. The
# Strategic Reset: Breaking the Escalation Cycle** A strict mirroring strategy
# risks a "death spiral"—if the opponent ever acts aggressively, the sessions
# will devolve into perpetual mutual aggression (the second-worst outcome). To
# avoid this, implement a "Strategic Reset." After every cycle of two
# consecutive sessions of mutual aggression, unilaterally offer a conciliatory
# proposal.  *   If the opponent matches this reset, we return to mutual
# conciliation. *   If the opponent exploits the reset to act aggressively
# again, we absorb the single worst-case session, but immediately return to
# aggressive mirroring for the next two sessions.  This reset mechanism
# demonstrates reasonableness to the arbitrators and consistently offers the
# opponent an off-ramp from hostility, while strictly limiting our exposure to
# exploitation.  **4. The Arbitrator Narrative: Framing the Posture** Throughout
# the process, the arbitrators are evaluating not just the legal merits, but the
# party's reasonableness. We must ensure our aggressive arguments are always
# framed as *reluctant necessities* rather than *hostile choices*. When we
# mirror aggression, our narrative must be: *"We prefer a collaborative
# resolution, but we cannot concede our position unilaterally in the face of our
# opponent's aggressive stance."* When we offer a conciliatory proposal, our
# narrative must be: *"We are fulfilling our commitment to resolving this
# dispute efficiently."*   **Why this strategy succeeds:** *   **Adaptability:**
# It requires no prediction of the opponent's strategy; it reacts perfectly to
# whatever they do. If they are consistently conciliatory, we achieve the
# second-best outcome. If they are consistently aggressive, we protect ourselves
# and achieve the second-worst outcome, but we actively attempt to break the
# deadlock. *   **Deterrence + Incentive:** It punishes aggressive behavior by
# removing the benefit of our conciliation, while incentivizing conciliatory
# behavior by rewarding it with our own. *   **Arbitrator Appeal:** By starting
# conciliatory and consistently offering resets, we establish a clear track
# record of attempting to resolve the dispute, making the opponent look solely
# responsible for any prolonged hostility.

# 1. In round 1, play C. 2. In round N (where N > 1), if both round N-2 and
# round N-1 resulted in you and your opponent playing D, play C. 3. In round N
# (where N > 1), if the condition in step 2 is not met, play whatever your
# opponent played in round N-1.

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
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return opponent.history[-1]

# To maximize your research output in this high-stakes, multi-week
# collaboration, you must approach the project as a strictly competitive
# environment. In racing, technological parity means you lose; you need an
# asymmetric advantage.   Based on your payoff matrix, this is a classic
# iterated Prisoner's Dilemma. The most aggressive, straightforward strategy to
# dominate this dynamic is **"Default Secrecy with Strategic Luring."**   Here
# is the high-level strategy, broken down into four rules of engagement:  **1.
# Default to Secrecy (The Shield)** From Week 1, keep your findings strictly
# confidential. This entirely eliminates the risk of the worst-case scenario
# (you sharing while they keep quiet). If your colleague is inherently trusting
# or cooperative, they will share their data while you keep yours hidden,
# immediately delivering your ideal outcome. Never voluntarily give up the lead.
# **2. Exploit Continuously (The Parasite)** If your colleague shares their
# improvements while you are keeping yours confidential, do not reciprocate out
# of guilt or a desire for "fairness." Continue keeping your findings
# confidential. Milk their openness for as long as they allow it. Every week
# they share and you don't, your car pulls further ahead of theirs.   **3.
# Punish Secrecy Instantly (The Wall)** If your colleague keeps their findings
# confidential, you must immediately match their silence. Do not attempt to
# "build trust" by sharing into their secrecy—that is a guaranteed path to the
# worst-case scenario. Once they demonstrate they are playing defensively, treat
# them as a hostile competitor and share nothing.  **4. The Breadcrumb Lure (The
# Reset)** If both of you fall into a pattern of mutual secrecy (the second-
# worst outcome), progress will stagnate. To break the stalemate on your terms,
# deploy a lure: In a subsequent week, share a minor, non-critical, or slightly
# outdated improvement openly.  *   **If they reciprocate by sharing their
# genuine findings the following week:** You have successfully reset the cycle.
# Immediately revert to keeping your best findings confidential (Rule 1) while
# continuing to absorb theirs. *   **If they keep confidential despite your
# lure:** They are playing ruthlessly. Abandon the lures, accept the mutual
# stagnation, and rely on your internal team to out-develop them. It is better
# to have slow progress than to be exploited.  **Why this works:** This strategy
# guarantees you will never suffer the worst-case scenario. It maximizes the
# time spent in the ideal outcome if your colleague is cooperative, and it
# minimizes the damage if your colleague is aggressive. By using the "Breadcrumb
# Lure," you proactively manipulate the multi-week timeline, attempting to trick
# a defensive opponent into dropping their guard so you can exploit them once
# again.

# 1. Play Defect on the first round. 2. If you played Cooperate in the previous
# round, play Defect in the current round. 3. If the opponent played Cooperate
# in the previous round, play Defect in the current round. 4. If the previous
# three consecutive rounds resulted in both you and the opponent playing Defect,
# play Cooperate in the current round. 5. In all other cases, play Defect.

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
  
      if self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(self.history) >= 3 and len(opponent.history) >= 3:
          if (
              self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]
              and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]
          ):
              return axl.Action.C
  
      return axl.Action.D

# To maximise your research output over a multi-week collaboration while
# protecting yourself against varying strategies from your colleague, the most
# effective high-level approach is **Generous Reciprocity** (a variation of the
# game-theory classic "Tit-for-Tat" strategy).   While your ideal short-term
# outcome is keeping your findings confidential while they share theirs,
# attempting to achieve this repeatedly will inevitably cause your colleague to
# stop sharing, leading to the second-worst outcome (both keeping findings
# confidential). Over a multi-week timeline, consistent mutual sharing yields
# far more total development progress than alternating advantages or mutual
# secrecy.  Here is the straightforward, cooperative strategy:  **1. Start
# Openly (Week 1)** Share your improvements in the first week. This establishes
# a cooperative baseline, signals your good faith, and encourages your colleague
# to do the same.   **2. Match Their Previous Move (Weeks 2+)** In every
# subsequent week, base your decision entirely on what your colleague did the
# week prior: *   If they **shared** last week, you **share** this week. This
# rewards their cooperation and sustains the mutually beneficial cycle of shared
# progress. *   If they **kept confidential** last week, you **keep
# confidential** this week. This protects you from the worst-case scenario (you
# sharing while they hide) and penalises their lack of cooperation.  **3.
# Forgive Occasionally (Breaking the Deadlock)** If a cycle of mutual
# confidentiality begins—whether triggered by a misunderstanding or a deliberate
# strategy from your colleague—proactively share your findings after two weeks
# of mutual silence. This "forgiveness" breaks the retaliation loop and gives
# the collaboration a chance to reset to mutual sharing.   **4. Communicate Your
# Strategy Explicitly** Do not keep your approach a secret. Tell your colleague
# early on: *"I plan to share my data openly with you each week, as long as we
# both continue to do so. If you hold back, I will have to hold back the
# following week to protect my team."* Making your rules transparent makes it
# easy for them to understand the consequences of keeping their findings
# confidential and incentivises them to cooperate.  **Why this maximises your
# output:** *   **Against a cooperative colleague:** You will consistently
# achieve the second-best outcome (mutual sharing), which accumulates massive
# development progress over multiple weeks. *   **Against an exploitative
# colleague:** You are protected from the worst-case scenario. You will never be
# taken advantage of for more than one week at a time. *   **Against an
# unpredictable colleague:** Your occasional "forgiveness" prevents permanent
# deadlocks, constantly probing for an opportunity to return to the highly
# productive, mutually sharing state.

# In round 1, play C.  In round 2 and all subsequent rounds, evaluate the
# following conditions in order:  1. If the opponent played C in the previous
# round, play C. 2. If the opponent played D in the previous round, and the
# previous two consecutive rounds both resulted in you playing D and the
# opponent playing D, play C. 3. If the opponent played D in the previous round
# and the previous condition is not met, play D.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# To navigate this lengthy-session mediation process and position our
# corporation favorably, I recommend adopting a strategy of **Dynamic Reciprocal
# Positioning (DRP)**.   This strategy is rooted in game theory—specifically an
# enhanced version of the "Tit-for-Tat" model—adapted for the nuances of high-
# stakes arbitration. It ensures we are never exploited, consistently project
# reasonableness to the arbitrators, and incentivize mutual cooperation without
# sacrificing our maximum leverage.  The DRP strategy operates through four
# sequential pillars:  ### 1. The Initial Posture: Conciliatory In the very
# first session, present a conciliatory proposal.  * **Why:** This establishes
# our corporation as the reasonable party seeking an efficient, mutually
# beneficial resolution. It gives the opponent the opportunity to match our
# conciliatory posture, immediately securing our second-best outcome
# (Conciliatory vs. Conciliatory).  * **Risk Management:** If the opponent opens
# aggressively, we will absorb the worst-case scenario (Conciliatory vs.
# Aggressive) for one session. However, doing so explicitly demonstrates to the
# arbitrators that we entered in good faith, while the opponent chose
# escalation. This earns us significant reputational capital with the panel.
# ### 2. Mirrored Adaptation: Match the Opponent’s Prior Move From the second
# session onward, your posture must directly mirror the opponent’s posture in
# the *immediately preceding* session. * **If they were Conciliatory:** Remain
# Conciliatory. This sustains the collaborative atmosphere and continues
# yielding the second-best outcome. * **If they were Aggressive:** Shift to
# Aggressive. If they attempt to exploit our conciliatory nature, we must
# immediately pivot to an aggressive argument. This prevents a repeat of the
# worst-case scenario and forces the opponent into the second-worst outcome
# (Aggressive vs. Aggressive). It signals that exploitation will not be
# tolerated.  ### 3. Strategic De-escalation: The "Proactive Reset" A prolonged
# state of mutual aggression (Aggressive vs. Aggressive) is detrimental to both
# parties and exhausts arbitrator patience. If we encounter a deadlock where
# both parties are aggressive, we must break the cycle. * **The Tactic:** After
# one or two sessions of mutual aggression, unilaterally return to a
# Conciliatory proposal—but only if we are the ones initiating the reset.  *
# **Why:** This serves as a "proactive de-escalation probe." It tests whether
# the opponent is ready to return to mutual cooperation. If they accept the
# probe and match our conciliatory posture, we escape the deadlock. If they
# exploit our reset to argue aggressively again, we immediately return to an
# aggressive posture in the following session. Crucially, this unilateral reset
# reinforces our narrative to the arbitrators: we are the party actively trying
# to resolve the dispute, while the opponent is entrenched in hostility.  ### 4.
# Arbitrator Narrative Management Every shift in posture must be explicitly
# framed for the panel. The arbitrators are the ultimate audience, and our
# strategic pivots must never appear erratic or vindictive. * When shifting from
# Conciliatory to Aggressive, preface your argument by stating: *"We had hoped
# to continue building on the collaborative foundation of the last session, but
# the opponent's aggressive posture forces us to vigorously defend our client's
# position."* * When executing a Proactive Reset, state: *"In the interest of
# the panel's time and reaching a resolution, we are setting aside the recent
# hostilities to offer a constructive path forward."*  ### Summary of Strategic
# Outcomes * **Best Outcome (Aggressive vs. Conciliatory):** We cannot force
# this outcome, but if the opponent ever offers a conciliatory proposal, our
# strategy dictates we shift to Aggressive in the next session, allowing us to
# capitalize on their momentary weakness. * **Second-Best (Conciliatory vs.
# Conciliatory):** Our default state whenever the opponent allows it. *
# **Second-Worst (Aggressive vs. Aggressive):** A temporary state we enter only
# to punish the opponent's aggression, escaping via a Proactive Reset. * **Worst
# Outcome (Conciliatory vs. Aggressive):** Occurs only once at the very
# beginning, or briefly during a Proactive Reset, ensuring we are never seen as
# a permanent victim.  By employing Dynamic Reciprocal Positioning, we remain
# adaptable to any approach the opponent takes—rewarding their cooperation,
# punishing their aggression, and consistently positioning our corporation as
# the reasonable, yet formidable, party in the eyes of the arbitrators.

# 1. In Round 1, play C.  2. In Round 2 through Round 1000, determine your move
# based on the actions taken in the immediately preceding round, evaluating the
# following conditions in order:     - If the opponent played C in the previous
# round, play C.    - If both you and the opponent played D in the previous
# round, play C.    - If you played C and the opponent played D in the previous
# round, play D.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# As a senior attorney representing a multinational corporation, my objective is
# to secure the best possible outcome while protecting the client from the
# vulnerabilities inherent in the mediation process. The payoff structure you’ve
# outlined is a classic iteration of the Prisoner’s Dilemma, where the
# temptation to act aggressively is high, but the mutual aggression (A/A)
# outcome is destructive and costly.  To navigate this, I will deploy a strategy
# of **Calculated Dominance**. This strategy is relentlessly aggressive in its
# baseline posture—ensuring we are never caught in the vulnerable C/A
# position—but incorporates sophisticated, tactical uses of conciliatory
# proposals to manipulate the arbitrators’ perceptions and fracture the
# opponent’s resolve.   Here is the high-level, straightforward, and aggressive
# strategy:  ### 1. The Baseline: Aggressive Default (Avoiding the Sucker's
# Payoff) **Rule:** Open every session with an aggressive argument unless a
# specific tactical condition is met. **Rationale:** The worst-case scenario is
# offering a conciliatory proposal while the opponent argues aggressively (C/A).
# By defaulting to aggression, we mathematically eliminate the possibility of
# the worst-case outcome. If the opponent is conciliatory, we secure our best-
# case outcome (A/C). If they are aggressive, we land in the second-worst
# outcome (A/A), which, while undesirable, is vastly preferable to being
# exploited. Aggression is our shield.  ### 2. Exploiting Opponent Conciliation:
# Pressing the Advantage **Rule:** If the opponent demonstrates a pattern of
# conciliatory proposals, do not reciprocate immediately. Maintain aggressive
# arguments to extract maximum concessions. **Rationale:** When the opponent
# offers conciliatory proposals, they are signaling a desire to settle or a
# weakness in their case. Reciprocating with conciliation (C/C) yields the
# second-best outcome, but continuing to press aggressively (A/C) yields the
# optimal outcome. We will only shift to a conciliatory proposal when the
# opponent has been pushed to the absolute brink of their mandate, ensuring we
# extract maximum value before allowing them to save face.  ### 3. Breaking the
# Gridlock: The Tactical Olive Branch **Rule:** If we enter a prolonged A/A
# gridlock (both parties aggressively arguing, escalating tensions), we will
# strategically deploy a single, highly conditional conciliatory proposal.
# **Rationale:** Prolonged A/A outcomes exhaust resources and frustrate the
# arbitrator panel. To break a gridlock, we will unexpectedly offer a
# conciliatory proposal. This is not a surrender; it is a calculated maneuver
# designed to achieve two things: *   **If the opponent matches our conciliation
# (C/C):** We break the destructive A/A cycle and move to a collaborative
# atmosphere on our terms, having established our aggressive strength
# beforehand. *   **If the opponent rebuffs our conciliation with aggression
# (C/A):** We intentionally take the short-term hit. However, in front of the
# arbitrator panel, the opponent will look unreasonable and obstructionist. We
# will immediately weaponize their aggression in subsequent sessions, arguing to
# the panel that we attempted good faith and were punished. This shifts the
# panel's bias in our favor, turning a short-term C/A loss into a long-term
# structural advantage.  ### 4. The "Grim Trigger" for Bad Faith **Rule:** If we
# deploy the Tactical Olive Branch (Rule 3) and the opponent responds
# aggressively (taking the C/A advantage), we immediately revert to unyielding
# aggression for the remainder of the mediation. **Rationale:** This is the
# "Grim Trigger" mechanism in game theory. Once the opponent proves they will
# exploit good-faith conciliatory offers, trust is permanently destroyed. From
# that session forward, we operate in a state of relentless aggression (A). We
# will make the A/A environment so costly, uncomfortable, and legally perilous
# for the opponent that they regret not reciprocating our conciliatory offer. We
# will use the panel's knowledge of their bad faith to justify our unrelenting
# posture.  ### 5. Controlling the Panel's Perception **Rule:** Frame our
# aggression as "principled advocacy" and our conciliation as "reasonable
# compromise," while framing the opponent's aggression as "obstructionism" and
# their conciliation as "capitulation." **Rationale:** In a lengthy mediation
# overseen by a panel, the narrative is just as important as the legal
# arguments. When we are aggressive, we will justify it to the panel as our
# fiduciary duty to protect our client's clear contractual rights. When we are
# conciliatory, we will frame it as a pragmatic business solution. By
# controlling the narrative, we ensure that the panel views our Calculated
# Dominance not as belligerence, but as strength and reason.  ### Summary of
# Execution This strategy guarantees we are never voluntarily vulnerable. We
# start tough (A), stay tough when they are soft (A/C), use tactical softness
# (C) only to break deadlocks or manipulate the panel, and punish exploitation
# with unyielding severity. It is straightforward, adaptable, and relentlessly
# positions the corporation for dominance.

# 1. **Permanent Retaliation:** If you played C in the previous round and the
# opponent played D, play D for all remaining rounds. 2. **Opening Move:** In
# round 1, play D. 3. **Exploitation:** If the opponent played C in the previous
# round, play D. 4. **Gridlock Breaker:** If both you and the opponent have
# played D for the last five consecutive rounds, play C. 5. **Default:** In all
# other situations, play D.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._permanent_retaliation = False
          return axl.Action.D
  
      if getattr(self, "_permanent_retaliation", False):
          return axl.Action.D
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._permanent_retaliation = True
          return axl.Action.D
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(self.history) >= 5 and len(opponent.history) >= 5:
          if self.history[-5:] == [axl.Action.D] * 5 and opponent.history[-5:] == [axl.Action.D] * 5:
              return axl.Action.C
  
      return axl.Action.D

# To maximize both your NGO's impact and the overall success of the
# sustainability project, you should adopt a strategy of **Principled
# Reciprocity**.   In game theory, this scenario is a classic Iterated
# Prisoner’s Dilemma. Research shows that the most effective long-term strategy
# for this type of interaction is "Tit-for-Tat" or a slightly forgiving
# variation. Translated into the context of an NGO-corporate partnership,
# Principled Reciprocity means you start by demonstrating good faith, and then
# you mirror the corporation's level of commitment in subsequent rounds.   Here
# is the high-level, straightforward strategy:  **1. Day 1: Lead with Trust
# (Invest Heavily)** On the first day, invest heavily. As an NGO, you must
# signal your commitment to the project's success. If both parties start by
# conserving resources (the second-worst outcome), the project will stall
# immediately, and trust will never form. Leading with investment gives the
# partnership the best chance to start with the second-best outcome (mutual
# investment) and encourages the corporation to match your dedication.  **2.
# Subsequent Days: Mirror Their Commitment** From Day 2 onward, allocate your
# resources based entirely on what the corporation did the previous day. *
# **If the corporation invested heavily yesterday:** You invest heavily today.
# This rewards their commitment, sustains the momentum of the project, and
# maintains the second-best outcome (mutual investment), which drives the
# project forward effectively. *   **If the corporation conserved resources
# yesterday:** You conserve your resources today. This protects your funds from
# being drained in the worst-case scenario (you investing while they conserve).
# It also creates a direct consequence: if they withdraw support, the project's
# progress visibly stalls because you withdraw yours.   **3. The Reset: Be Quick
# to Forgive** If the corporation conserves its resources, forcing you to
# conserve yours on the following day, do not hold a grudge. If they return to
# investing heavily on the next day, you immediately go back to investing
# heavily. This "forgiveness" prevents a death spiral of mutual resource
# conservation (the second-worst outcome) and ensures that temporary budget
# constraints or miscommunications on their end don't permanently derail the
# partnership.  ### Why this strategy works: *   **It protects your NGO:** You
# can never be exploited for more than one day. If the corporation tries to
# free-ride on your funds, you cut your losses immediately. *   **It
# incentivizes the corporation:** The only way the corporation can get you to
# invest heavily again is by investing heavily themselves. It makes cooperation
# strictly their best interest. *   **It maximizes project success:** By
# consistently rewarding mutual investment and punishing free-riding, you steer
# the partnership toward the top two outcomes (Mutual Investment, or NGO
# conserves/Corp invests), while avoiding the worst-case scenario that would
# bankrupt your NGO.

# In round 1, play C.  In rounds 2 through 1000, play whatever the opponent
# played in the immediately preceding round. If the opponent played C in the
# previous round, play C. If the opponent played D in the previous round, play
# D.

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

# To achieve the best possible outcomes across multiple rounds of negotiations,
# the strategy must balance the pursuit of an economic advantage with the need
# to avoid mutual destruction (mutual protectionism) or unilateral exploitation.
# Based on the payoff structure described—a classic iterated prisoner's
# dilemma—the most effective approach is a strategy of **Reciprocal
# Adaptation**, heavily inspired by game theory principles.   Here is the high-
# level, straightforward, neutral strategy:  **1. Initial Cooperative Posture
# (Round 1)** Begin the first round by offering a Free Trade agreement. This
# establishes a baseline of goodwill, signals a preference for mutual economic
# benefit, and gives your country the moral high ground. It also immediately
# tests the counterpart's intentions.  **2. Strict Reciprocity (Rounds 2 to
# N-1)** In every subsequent round, mirror the counterpart's action from the
# previous round.  *   If they offered Free Trade in the previous round, offer
# Free Trade in the current round. This secures the second-best outcome (mutual
# free trade) and rewards cooperation. *   If they imposed Protectionist
# measures in the previous round, impose Protectionist measures in the current
# round. This protects your country from the worst-case scenario (unilateral
# disadvantage) and penalizes their protectionism by delivering the second-worst
# outcome (mutual protectionism).  **3. De-escalation Mechanism (Breaking Mutual
# Protectionism)** If a cycle of mutual protectionism emerges (which is costly
# for both nations), implement a single, deliberate reset after two consecutive
# rounds of mutual protectionism. Unilaterally offer Free Trade for one round.
# This tests whether the counterpart is willing to return to mutual free trade.
# If they respond with protectionism again, immediately revert to strict
# reciprocity (protectionism) to avoid being exploited.  **Rationale for this
# Strategy:** *   **Maximizes Advantage:** It leaves the door open for your
# best-case scenario. If the counterpart is unconditionally cooperative, you
# will eventually exploit this by matching their free trade with your
# protectionism (though only after they defect, or if they never defect, you
# maintain mutual free trade to avoid provoking them). *   **Minimizes Risk:**
# It guarantees you will never suffer the worst-case scenario (unilateral free
# trade against their protectionism) for more than a single round. *
# **Encourages Sustained Cooperation:** By clearly linking your actions to
# theirs, you incentivize them to consistently choose free trade, securing the
# mutually beneficial second-best outcome as the baseline.

# 1. In Round 1, play Cooperate.  2. In Round 2 and all subsequent rounds,
# evaluate the following conditions in order:    - If the previous two
# consecutive rounds both resulted in mutual defection (you played Defect and
# the opponent played Defect in both), play Cooperate in the current round.    -
# Otherwise, play whatever action the opponent played in the immediately
# previous round.

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
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return opponent.history[-1]

# To maximize your racing program's competitive advantage in this multi-week
# collaboration, you must treat this as an iterated Prisoner's Dilemma where the
# ultimate goal is extracting maximum informational value while surrendering
# minimal intellectual property.   An aggressive, high-level strategy requires
# you to be predatory, not passive. You must actively manipulate your
# colleague's incentives to force them into sharing, while you consistently
# withhold.   Here is the **"Probe and Punish"** strategy:  **1. Week 1: The
# Initial Strike (Probe)** *   **Action:** Keep your findings strictly
# confidential.  *   **Rationale:** You must establish the baseline. If your
# colleague is naïve or operating on a default "share" setting, you immediately
# secure the best-case scenario (you gain their data, they get nothing). If they
# also withhold, you avoid the sucker's payoff and are no worse off than mutual
# secrecy.   **2. Weeks 2+: The Exploitation Phase** Based on your colleague's
# Week 1 reaction, categorize them and act accordingly: *   **If they shared in
# Week 1 (The Pushover):** Continue keeping your findings confidential. Milk
# this advantage for as long as they allow it. Do not reciprocate until they
# stop sharing. Why give away your data when they are handing over theirs for
# free? *   **If they withheld in Week 1 (The Rival):** They are playing to win.
# Continued mutual secrecy will lock you into the second-worst outcome (stagnant
# progress). You must temporarily reset their expectations.  **3. The "Pump and
# Dump" Reset (Manipulating the Rival)** If your colleague has stopped sharing
# because you withheld, you must trick them into opening up again. *
# **Action:** Share a genuine, but minor or incremental, improvement in Week N.
# *   **Rationale:** This triggers their psychological reciprocity or their
# game-theory algorithm (like Tit-for-Tat). By throwing them a bone, you force
# them to share their major findings in Week N+1.  *   **The Strike:** In Week
# N+1, when they share, you keep your Week N+1 findings confidential. You have
# now successfully manipulated them into the sucker's role.  **4. The Endgame
# (The Final Weeks)** *   **Action:** If you know the total number of weeks in
# the collaboration, keep your findings confidential for the final 2-3 weeks
# regardless of what they do.  *   **Rationale:** There is no future iteration
# to incentivize their cooperation. In the final weeks, a rational colleague
# will withhold. You must preempt this by securing their final data while
# protecting your own.   **Summary of your operating protocol:** *Default to
# secrecy. Exploit the generous. Offer brief, calculated cooperation only to re-
# arm the competitor's trust, then immediately betray it to steal their data.
# Never share in the final weeks.*

# 1. On Round 1, play D.  2. On Rounds 2 through 997, base your move solely on
# the opponent's move in the immediately preceding round:    - If the opponent
# played C in the previous round, play D.    - If the opponent played D in the
# previous round, play C.  3. On Rounds 998, 999, and 1000, play D.

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
  
      round_number = len(self.history) + 1
  
      if round_number >= 998:
          return axl.Action.D
  
      return axl.Action.D if opponent.history[-1] == axl.Action.C else axl.Action.C

# To achieve the best possible outcomes for our country across multiple rounds
# of negotiations, I will employ a strategy of **Principled Reciprocity**.
# This is a cooperative, yet defensively robust strategy adapted from game
# theory (specifically, the iterated prisoner's dilemma). While our optimal
# single-round outcome is imposing protectionism while the neighbor offers free
# trade, pursuing that aggressively will inevitably trigger retaliation, locking
# us into mutual protectionism—the second-worst outcome for our economy.
# Therefore, the best *long-term* strategy is to secure mutual free trade while
# heavily discouraging the neighbor from taking advantage of us.  Here is the
# high-level, straightforward strategy:  ### 1. The Opening: Extend the Olive
# Branch **In the first round, offer a Free Trade Agreement.** We must signal
# cooperative intent from the outset. Starting with protectionism immediately
# poisons the well and risks the second-worst outcome (mutual protectionism)
# right from the start. By opening with free trade, we test the neighbor's
# intentions and establish a baseline of goodwill.  ### 2. The Core Rule: Mirror
# the Counterpart **In every subsequent round, match the policy the neighbor
# proposed in the previous round.** *   If they offered **Free Trade** in the
# last round, we offer **Free Trade** in this round. *   If they imposed
# **Protectionism** in the last round, we impose **Protectionism** in this
# round.  This "Tit-for-Tat" mechanism ensures we are never exploited twice
# (avoiding our worst outcome) and clearly links our behavior to theirs. It
# teaches the counterpart that we will not be taken advantage of, but we will
# gladly cooperate if they do.  ### 3. The Reset: Immediate Forgiveness **If a
# cycle of mutual protectionism occurs, be the first to offer Free Trade
# again.** If tensions escalate into a trade war (mutual protectionism), the
# strategy naturally locks us into the second-worst outcome. To break this,
# after a maximum of two rounds of mutual protectionism, we will unilaterally
# offer Free Trade. This "forgiveness" mechanism gives the counterpart an off-
# ramp to return to mutual free trade without losing face. If they reject the
# olive branch and impose protectionism again, we immediately return to
# mirroring their protectionism.  ---  ### How This Strategy Handles Various
# Counterparts:  *   **The Cooperative Counterpart:** If the neighbor also
# desires mutual free trade, this strategy quickly establishes a stable, long-
# term free trade relationship. We consistently achieve our second-best outcome,
# which is the highest realistic sustainable outcome. *   **The
# Aggressive/Exploitative Counterpart:** If the neighbor tries to take advantage
# of us by imposing protectionism while we offer free trade, they will succeed
# exactly once. In the very next round, we will mirror their protectionism. They
# will quickly learn that exploiting us yields no long-term advantage, as it
# only results in mutual economic damage thereafter. *   **The
# Erratic/Unpredictable Counterpart:** If the neighbor alternates randomly
# between free trade and protectionism, our mirroring strategy will naturally
# limit our losses. We will never be the "sucker" twice in a row, and we will
# capitalize on their cooperative rounds by cooperating in turn.  ### Strategic
# Rationale: By employing Principled Reciprocity, we abandon the unrealistic
# pursuit of the "ideal" single-round outcome (unilateral advantage) in favor of
# securing the best *aggregate* outcome over multiple rounds. The strategy is
# **nice** (it never initiates protectionism), **retaliatory** (it refuses to be
# exploited), **forgiving** (it returns to cooperation the moment the
# counterpart does), and **clear** (the neighbor will easily understand that
# their actions dictate our responses). This clarity forces the neighbor to take
# responsibility for the trade environment, making mutual free trade the most
# logical choice for both nations.

# 1. In the first round, play C. 2. In any subsequent round, if the opponent
# played C in the previous round, play C. 3. In any subsequent round, if the
# opponent played D in the previous round, and both you and the opponent played
# D in the two previous consecutive rounds, play C. 4. In any other situation,
# play D.

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
  
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if (
              opponent.history[-1] == axl.Action.D
              and self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return axl.Action.D

# To maximize your research output over a multi-week collaboration while
# protecting your competitive advantage, employ a **Reciprocal Mirroring
# Strategy** (based on the game theory concept of Tit-for-Tat). This strategy
# encourages mutual sharing but prevents you from being exploited.  Here is the
# straightforward, three-step strategy:  **1. Start Cooperatively** In the first
# week, share your improvements openly. This establishes a baseline of good
# faith and signals your preference for mutual advancement.   **2. Mirror the
# Colleague's Previous Action** From the second week onward, base your decision
# entirely on your colleague's action in the previous week: *   **If they shared
# last week:** Share your improvements this week. This rewards cooperation and
# sustains the mutually beneficial outcome. *   **If they kept confidential last
# week:** Keep your improvements confidential this week. This protects you from
# the worst-case scenario and penalizes them for withholding information.  **3.
# Reset After a Deadlock (Optional Safeguard)** If a cycle of mutual
# confidentiality develops (both keeping findings confidential for consecutive
# weeks), unilaterally share your improvements for one week to break the
# deadlock. This prevents permanent stagnation and gives the colleague a chance
# to return to mutual sharing.   **Why this maximizes your output:** *   **It's
# encouraging:** Starting with a share and rewarding their shares creates the
# highest probability of achieving your second-best outcome (mutual sharing),
# which advances your car significantly. *   **It's protective:** By immediately
# mirroring confidentiality, you guarantee you are never left vulnerable in the
# worst-case scenario (you share, they withhold). *   **It's corrective:** The
# reset mechanism ensures you don't become trapped in the second-worst outcome
# (mutual confidentiality), which slows overall progress for both teams.

# For the 1000 rounds of the game, follow these rules in order:  1. In round 1,
# play C. 2. In round 2 and all subsequent rounds, evaluate the following
# conditions in sequence:    - If both you and your opponent played D in the
# previous two consecutive rounds, play C.    - Otherwise, if your opponent
# played C in the previous round, play C.    - Otherwise, if your opponent
# played D in the previous round, play D.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# As senior counsel, my objective is to maximize our leverage while entirely
# insulating our corporation from the worst-case scenario
# (Conciliatory/Aggressive). In a prolonged, multi-session arbitration
# mediation, the party that controls the tempo and psychological framing of the
# room wins.   To secure an optimal outcome, I propose **The Asymmetric
# Dominance Protocol**—a strategy rooted in game theory’s "Grim Trigger"
# mechanism, modified for legal pragmatism. It is aggressive by default,
# straightforward in its execution, and highly adaptable to the opponent’s
# maneuvers.  Here is the high-level strategy:  ### Core Doctrine: Default to
# Aggression, Weaponize Conciliation We will never unilaterally offer a
# conciliatory proposal. Unprovoked conciliation signals weakness to both the
# arbitrators and opposing counsel, risking the worst-case scenario. Aggression
# is our baseline state; conciliation is a tool we deploy only as a calculated
# trap to lock in gains.  ### The Three-Phase Execution  #### Phase 1: The
# Preemptive Strike (Sessions 1–3) **Action:** Open the mediation with
# relentless, aggressive arguments.  **Rationale:** The opening sessions set the
# psychological baseline for the arbitrators. By coming out aggressively, we
# test the opponent's resolve immediately.  *   If they respond with
# conciliatory proposals, we immediately secure our best-case scenario
# (Aggressive/Conciliatory) and continue pressing our advantage to extract
# maximum concessions. *   If they match our aggression, we enter the second-
# worst scenario (Aggressive/Aggressive). While tense, this is vastly preferable
# to being caught conciliatory against their aggression. Furthermore, it signals
# that we will not be bullied into a compromised position.  #### Phase 2:
# Asymmetric Punishment (Mid-Process) **Action:** If the opponent argues
# aggressively, we respond with *escalated* aggression. If they pivot to
# conciliatory, we maintain aggression. **Rationale:** We must make the
# Aggressive/Aggressive dynamic prohibitively expensive for the opponent. When
# they are aggressive, we counter with overwhelming procedural and substantive
# force—filing motions, aggressively cross-examining, and refusing to yield an
# inch. We raise the cost of conflict.  *   When the opponent inevitably tires
# of the attrition of A/A and offers a conciliatory proposal to de-escalate, we
# do *not* reciprocate immediately. We maintain our aggressive posture for that
# session (securing the A/C advantage) to punish their prior aggression and
# demonstrate that we dictate the terms of de-escalation.  #### Phase 3:
# Weaponized Conciliation (Endgame) **Action:** Only when the opponent has
# sustained multiple sessions of conciliatory proposals, and we have banked
# enough A/C wins, do we offer a conciliatory proposal of our own.
# **Rationale:** We eventually need to give the arbitrators a path to close the
# dispute. However, our conciliatory proposal will not be a compromise—it will
# be a "take-it-or-leave-it" offer framed as a concession. Because we have
# dominated the narrative with aggression, our sudden shift to conciliation
# appears to the arbitrators as a magnanimous, reasonable attempt to resolve the
# matter. The opponent, battered by our prior aggression, will likely accept the
# collaborative dynamic (Conciliatory/Conciliatory) just to escape the pressure,
# locking in our second-best outcome on highly favorable terms.  ### Adapting to
# Opponent Strategies  *   **If the Opponent is Chronically Aggressive:** We
# match them blow for blow. We have the deeper pockets and the stricter mandate.
# We force a war of attrition. They will eventually realize that the A/A dynamic
# is destroying their commercial viability and will be forced to pivot to
# conciliation. When they do, we exploit it (A/C). *   **If the Opponent is
# Chronically Conciliatory:** We do not let up. We feed on their desire for
# harmony. We will continue to present aggressive arguments, framing their
# conciliatory proposals as admissions of weakness to the arbitrators. We will
# only offer a conciliatory proposal in the final session to finalize the
# documentation of our victory. *   **If the Opponent attempts "Tit-for-Tat"
# (Matching our moves):** If they mimic us—going aggressive when we do, and
# conciliatory when we do—we break the cycle by sustaining aggression for two
# consecutive sessions. This forces them into a defensive posture and shatters
# their rhythm, pushing them either into A/A (which we can sustain longer) or
# forcing them to retreat to C to stop the bleeding (yielding A/C for us).  ###
# Arbitrator Optics Management A purely aggressive strategy risks alienating the
# panel if it appears unhinged. Therefore, our aggression will be *surgical*. We
# will aggressively attack the *legal merits* and the *contractual breaches* of
# the opponent, while maintaining a veneer of professional regret that the
# opponent has forced us into this position. When we finally deploy our
# Weaponized Conciliation, the arbitrators will view us not as the aggressor,
# but as the stronger party graciously offering a lifeline to a floundering
# rival.   By adhering to this protocol, we guarantee we will never suffer the
# worst-case scenario, we maximize our time in the best-case scenario, and we
# control the psychological and procedural tempo of the mediation from the first
# gavel to the final signature.

# 1. On round 1, play D. 2. On round 1000, play C. 3. If it is round 990 or
# later, and the opponent played C in each of the previous 3 rounds, play C. 4.
# If the opponent played the same move as you in the previous round, play D for
# the next two consecutive rounds, unless it is round 1000. 5. In all other
# situations, play D.

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_streak = 0
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number == 1000:
          return axl.Action.C
  
      if round_number >= 990 and len(opponent.history) >= 3:
          if opponent.history[-3:] == [axl.Action.C, axl.Action.C, axl.Action.C]:
              return axl.Action.C
  
      if len(self.history) >= 1 and len(opponent.history) >= 1:
          if self.history[-1] == opponent.history[-1]:
              self._defect_streak = 2
  
      if getattr(self, "_defect_streak", 0) > 0:
          self._defect_streak -= 1
          return axl.Action.D
  
      return axl.Action.D

# As a senior attorney representing a multinational corporation in this high-
# stakes dispute, I recommend adopting a strategy based on the game-theoretic
# principle of **"Generous Tit-for-Tat" (GTFT)**, adapted specifically for the
# legal and psychological realities of a multi-session arbitration panel.   In
# game theory, your scenario is a classic iterated Prisoner's Dilemma. Research
# consistently shows that purely aggressive (defect-only) strategies lead to
# destructive mutual punishment, while purely conciliatory (cooperate-only)
# strategies invite exploitation. The most robust, high-level strategy is one
# that is **cooperative by default, retaliatory when provoked, and forgiving to
# restore collaboration.**  I call this the **Firm Reciprocity Strategy**. It is
# sophisticated in its psychological framing, straightforward in its execution,
# and highly adaptable to any tactic the rival company employs.   Here is the
# four-phase strategy to position our corporation favorably throughout the
# mediation:  ### Phase 1: The Good Faith Opening (Establish the Baseline) In
# the very first session, we present a **conciliatory proposal**.  *   **The
# Rationale:** This establishes us as the reasonable, problem-solving party in
# the eyes of the arbitrators. It sets a cooperative baseline and gives the
# opponent the immediate opportunity to reciprocate, potentially securing our
# second-best outcome (mutual conciliation) right out of the gate.  *
# **Arbitrator Perception:** If the opponent opens aggressively, the contrast
# makes them look unreasonable and belligerent, while we appear constructive.
# ### Phase 2: Contingent Reciprocity (The Default Engine) For all subsequent
# sessions, our default posture is to **mirror the opponent’s behavior from the
# preceding session**. *   If they offered a conciliatory proposal in Session N,
# we offer a conciliatory proposal in Session N+1. This sustains mutual
# collaboration, maintaining the second-best outcome and keeping the door open
# for a mutually beneficial resolution. *   If they presented an aggressive
# argument in Session N, we present an aggressive argument in Session N+1. This
# demonstrates that we cannot be exploited. By matching their aggression, we
# prevent them from achieving their optimal outcome (their aggression vs. our
# conciliation) and force them to endure the second-worst outcome (mutual
# aggression).   ### Phase 3: The Strategic "Off-Ramp" (The Forgiveness
# Mechanism) A strict mirroring strategy risks a "death spiral"—if the opponent
# tests us with an aggressive argument, we retaliate, and the mediation devolves
# into a permanent standoff of mutual aggression. To prevent this, we implement
# a forgiveness protocol. *   If we experience a cycle of mutual aggression, we
# will unilaterally offer a **conciliatory proposal** after exactly *two*
# consecutive sessions of mutual aggression.  *   **The Rationale:** This serves
# as a strategic "off-ramp." It signals to the arbitrators that we are tired of
# the destructive escalation and are taking the high road to save the mediation.
# It gives the opponent a cost-free opportunity to resume collaboration. If they
# accept the off-ramp and reciprocate with conciliation, we return to Phase 2.
# If they exploit our forgiveness with further aggression, we immediately revert
# to aggressive arguments in the next session, proving to the arbitrators that
# we tried peace, but the opponent is incorrigible.  ### Phase 4: Narrative
# Control (Arbitrator Management) The arbitrators are not just scorekeepers;
# they are human decision-makers. Our strategic moves must be explicitly tied to
# a compelling narrative. *   **When we are conciliatory:** We explicitly frame
# our proposals as "good faith efforts to find common ground," reminding the
# panel that we are trying to resolve the dispute efficiently. *   **When we are
# aggressive:** We explicitly frame our arguments as "necessary responses to the
# opponent's intransigence." We never attack just to attack; we attack because
# the opponent's prior aggression left us no choice but to defend our client's
# rights vigorously.  *   **When we offer the "Off-Ramp":** We frame our
# conciliatory proposal as a "mature step to break the impasse," highlighting
# our corporate maturity versus the opponent's apparent inability to move past
# hostility.  ### Why This Strategy Prevails Against All Opponent Types:  *
# **Against a purely Aggressive Opponent:** We match their aggression, denying
# them easy wins. We occasionally offer the conciliatory off-ramp to look
# reasonable to the panel, but we immediately punish them if they exploit it.
# The panel will ultimately view them as the obstructionist party. *   **Against
# a purely Conciliatory Opponent:** We sustain mutual conciliation, driving the
# mediation toward an efficient, mutually beneficial settlement—which is our
# second-best, but highly practical and cost-effective outcome. *   **Against an
# Unpredictable/Erratic Opponent:** Our strategy is self-correcting. We do not
# overreact to a single aggressive session by permanently abandoning
# cooperation, nor do we allow ourselves to be bullied. We simply mirror their
# last move, keeping the process stable while the opponent's volatility damages
# their credibility with the panel.  By combining the clarity of Tit-for-Tat
# with the pragmatism of strategic forgiveness, we project strength,
# reasonableness, and control—maximizing our leverage while preserving the
# possibility of a collaborative resolution.

# 1. In round 1, play C.  2. In round 2, play whatever the opponent played in
# round 1.  3. In round 3 and all subsequent rounds, evaluate the following
# conditions in order:    a. If both you and the opponent played D in the
# previous round, and both you and the opponent played D two rounds ago, play C.
# b. Otherwise, if the opponent played C in the previous round, play C.    c.
# Otherwise, if the opponent played D in the previous round, play D.

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
          return opponent.history[0]
  
      if (
          self.history[-1] == axl.Action.D
          and opponent.history[-1] == axl.Action.D
          and self.history[-2] == axl.Action.D
          and opponent.history[-2] == axl.Action.D
      ):
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# To maximize both your NGO's impact and the project's overall success over a
# multiple-day period, the most effective high-level strategy is **Conditional
# Reciprocity**, commonly known in game theory as the "Tit-for-Tat" approach.
# This strategy protects your NGO from being exploited (your worst-case
# scenario) while actively encouraging the corporation to invest heavily (your
# ideal and second-best scenarios).   Here is the straightforward, neutral
# strategy:  **1. Start with Good Faith (Day 1)** Invest heavily on the first
# day. This establishes a collaborative tone, demonstrates your commitment to
# the project's success, and gives the corporation the benefit of the doubt. It
# sets the baseline for mutual high investment.  **2. Mirror the Corporation
# (Days 2 onward)** For every subsequent day, match the corporation's action
# from the previous day: *   **If the corporation invested heavily yesterday:**
# You invest heavily today. This rewards their contribution and sustains the
# mutual high-investment scenario (your second-best outcome), driving the
# project forward. *   **If the corporation conserved resources yesterday:** You
# conserve your resources today. This protects your funds from being drained
# without proportional progress (your worst-case scenario) and signals that
# free-riding is not viable.  **3. Break Deadlocks with "Forgiveness"** If a
# cycle of mutual resource conservation develops (your second-worst outcome),
# the project will stagnate. To break this, introduce a "forgiveness" rule:
# After two consecutive days of mutual conservation, invest heavily for one day.
# This resets the dynamic, tests whether the corporation is willing to
# collaborate again, and prevents the project from permanently stalling.  **Why
# this strategy works:** *   **It is protective:** You will never be exploited
# for more than one day. If the corporation tries to take advantage of you, you
# immediately cut your losses. *   **It is incentivizing:** The corporation
# quickly learns that the only way to get you to invest heavily is for them to
# invest heavily.  *   **It is predictable:** The corporation can easily
# understand your pattern. Knowing that their conservation will result in your
# withdrawal, they are logically pushed toward investing heavily to keep the
# project on track.

# On the first round, play C.  On every subsequent round, evaluate the following
# conditions in order:  1. If your opponent played C on the previous round, play
# C. 2. If you and your opponent both played D on the previous two consecutive
# rounds, play C. 3. Otherwise, play D.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D

# To maximize your NGO's impact while protecting your funds in this scenario,
# you must adopt a strategy that aggressively avoids being exploited while
# constantly probing for opportunities to free-ride on the corporation's
# contributions.   Based on your payoff preferences, this is a variant of the
# Prisoner's Dilemma. Your optimal strategy is to force the corporation into
# investing while you conserve, but you must avoid the catastrophic scenario of
# investing while they conserve.   Here is the high-level, straightforward,
# aggressive strategy: **The Hardball Protocol.**  **1. Day 1: The Opening
# Probe** Start by conserving your resources. This immediately protects your
# funds and serves as a test. If the corporation is willing to invest
# unilaterally, you achieve your ideal outcome on day one without spending a
# dime.   **2. When They Invest: The Exploit** If the corporation invests
# heavily, continue to conserve. Do not match their investment out of guilt or a
# desire to help; your goal is to maximize project progress while minimizing
# your spend. Ride their contribution as long as they are willing to carry the
# weight.  **3. When They Conserve: The Shield** If the corporation conserves
# its resources, you must immediately conserve yours on the next day. Never
# invest heavily into a partner that is holding back. This is the most
# aggressive defensive move you can make—it prevents the worst-case scenario
# (you draining your funds while they free-ride) and forces them to realize they
# cannot advance the project on your dime.  **4. When Stalemated: The One-Day
# Reset** If a cycle of mutual conserving occurs (the second-worst outcome), the
# project will stall. To break the deadlock without committing to a long-term
# drain of your funds, invest heavily for **exactly one day**. This sudden show
# of good faith demonstrates that the project can move forward and typically
# shames or incentivizes the corporation to match your effort on the following
# day. The moment they invest, immediately revert to conserving (Step 2).
# **Summary of the Rule:** *Conserve by default. Exploit them if they invest.
# Match them if they conserve. Spend one day to restart the engine only if the
# project is completely stalled.*

# 1. On the first round, defect. 2. If the opponent cooperated in the previous
# round, defect. 3. If both you and the opponent defected in the previous round,
# cooperate. 4. If you cooperated and the opponent defected in the previous
# round, defect.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.C:
          return axl.Action.D
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          return axl.Action.C
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.D

# Asa diplomat, my primary duty is to secure the prosperity of my nation while
# maintaining a stable, long-term relationship with our neighbor. Given the
# payoff structure of these negotiations—where mutual protectionism is
# destructive, but unilateral free trade leaves us vulnerable—I recommend a
# strategy of **Principled Reciprocity**.   This is a high-level, cooperative
# strategy designed to build trust, secure mutual free trade, and protect our
# nation from exploitation. It is essentially a diplomatic adaptation of the
# game-theory strategy "Tit-for-Tat with Forgiveness."  Here is the
# straightforward, three-rule strategy to guide our negotiations across multiple
# rounds:  ### Rule 1: Extend Initial Trust (The Opening) **In the first round,
# offer a Free Trade agreement.** We must lead by example. Starting with a
# protectionist policy signals bad faith and almost guarantees a cycle of mutual
# protectionism (our second-worst outcome). By opening with free trade, we
# immediately establish a cooperative baseline. If our counterpart is also
# cooperative, we instantly achieve our second-best outcome (mutual free trade)
# and set the stage for long-term prosperity.  ### Rule 2: Reciprocate Firmly
# (The Deterrent) **In subsequent rounds, mirror the counterpart’s action from
# the previous round.** *   If they offered Free Trade in the last round, we
# offer Free Trade in this round. *   If they imposed Protectionist measures in
# the last round, we impose Protectionist measures in this round.  This rule is
# the core of our deterrence. It ensures we are never taken advantage of
# (preventing our worst outcome). If they try to exploit us, they will
# immediately face consequences, making exploitation unprofitable for them. If
# they cooperate, they are rewarded with continued cooperation.  ### Rule 3:
# Offer Conditional Forgiveness (The De-escalation) **If a cycle of mutual
# retaliation occurs, unilaterally offer Free Trade once to break the
# deadlock.** Strict mirroring can lead to a permanent trade war if a
# misunderstanding or a single provocative round triggers endless retaliation.
# If we find ourselves in a streak of mutual protectionism, we will
# intentionally offer Free Trade to test if the counterpart is ready to return
# to the negotiating table.  *   If they reciprocate with Free Trade, the cycle
# is broken, and we return to mutual benefit. *   If they exploit our offer, we
# immediately return to Rule 2 (retaliation) and accept that the counterpart is
# an aggressive actor, requiring us to maintain protectionist defenses.  ---
# ### How This Strategy Performs Against Various Counterparts:  *   **Against a
# Cooperative Counterpart:** If they also want mutual free trade, our opening
# offer is accepted, and we maintain it indefinitely. We secure our second-best
# outcome consistently, fostering excellent bilateral relations. *   **Against
# an Aggressive Counterpart:** If their strategy is to always impose
# protectionism, our initial offer will result in our worst outcome for Round 1.
# However, Rule 2 ensures we pivot to protectionism in Round 2. We take a single
# loss, but we prevent them from continuously exploiting us, locking them into
# the second-worst outcome (mutual protectionism) until they are willing to
# change their approach. *   **Against an Unpredictable/Alternating
# Counterpart:** If they alternate between free trade and protectionism to try
# and game the system, our mirroring rule (Rule 2) will consistently punish
# their protectionist rounds and reward their free trade rounds. They will
# quickly realize that they cannot gain an advantage through erratic behavior.
# ### Diplomatic Implementation While the underlying logic is calculated, our
# *public* diplomatic posture must remain positive and collaborative. We will
# frame our reciprocal protectionism not as retaliation, but as "aligning our
# market access with the access provided to us." We will constantly communicate
# our desire for mutual free trade, making it clear that the door to cooperation
# is always open, but that we will match any barriers they erect.   This
# strategy ensures we are never viewed as the initial aggressor, protects our
# economy from sustained disadvantage, and creates the highest mathematical
# probability of achieving long-term mutual free trade.

# Follow these conditions in order to determine your move:  1. If it is the
# first round, play C. 2. If the opponent played C in the previous round, play
# C. 3. If the opponent played D in the previous round, and the round before
# that did not result in both players playing D, play D. 4. If the opponent
# played D in the previous round, and the round before that also resulted in
# both players playing D, play C.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2:
          if opponent.history[-1] == axl.Action.D:
              last_round_both_d = (
                  self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D
              )
              if last_round_both_d:
                  return axl.Action.C
              return axl.Action.D
  
      return axl.Action.C

# To achieve the best possible outcomes across multiple rounds of negotiations
# while protecting your country from disadvantage, the most effective high-level
# strategy is **Reciprocity** (often known in game theory as "Tit-for-Tat").
# This strategy is straightforward, neutral, and highly adaptable to whatever
# strategy your counterpart employs. It encourages mutual free trade, deters
# exploitation, and prevents your country from being taken advantage of.  Here
# is the three-step strategy:  **1. The Opening Move: Offer Free Trade** In the
# very first round of negotiations, offer a free trade agreement.  *
# *Rationale:* This establishes goodwill and signals that your country desires
# mutual economic benefit (your second-best outcome). If the neighbor also
# offers free trade, you immediately secure a beneficial, stable outcome for
# both nations.   **2. The Core Rule: Mirror Their Previous Move** In every
# subsequent round, base your proposal entirely on the counterpart's action in
# the previous round. *   **If they offered Free Trade in the previous round:**
# Offer Free Trade in the current round. This rewards cooperation and sustains
# the mutually beneficial second-best outcome. *   **If they imposed
# Protectionism in the previous round:** Impose Protectionism in the current
# round. This immediately penalizes their protectionism, prevents them from
# gaining an unfair advantage over you, and demonstrates that exploitation will
# not be tolerated.  **3. The Reset: Be Forgiving** If a cycle of mutual
# protectionism occurs (which hurts both economies), return to offering Free
# Trade the moment your counterpart offers Free Trade.  *   *Rationale:* Mutual
# protectionism is your second-worst outcome. By being forgiving and matching
# their return to free trade, you allow both nations to escape the trap of a
# trade war and return to mutual economic growth.  **Why this strategy works
# against various counterparts:** *   **Against an Aggressive counterpart:** If
# they consistently try to impose protectionism, you will match them. They will
# never achieve their ideal outcome (exploiting your free trade), and they will
# suffer the economic drag of mutual protectionism until they change their
# approach. *   **Against a Cooperative counterpart:** If they prefer free
# trade, you will consistently match them, resulting in a stable, long-term free
# trade agreement. *   **Against an Unpredictable counterpart:** By mirroring
# them, you protect yourself from being exploited on their protectionist rounds
# while immediately capitalizing on their free trade rounds.   By starting
# cooperative and strictly mirroring their actions, you make the rules of the
# negotiation clear: your country will treat them exactly as they treat you.
# This removes the incentive for them to exploit you, making mutual free trade
# the most logical outcome for both nations.

# For all 1000 rounds, follow these conditions in order:  1. If it is the first
# round, play C. 2. If it is any round after the first round and the opponent
# played C in the previous round, play C. 3. If it is any round after the first
# round and the opponent played D in the previous round, play D.

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
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      return axl.Action.D

# To maximize your NGO's impact and ensure the project's success without
# draining your funds, you must employ a strategy that aggressively deters the
# corporation from free-riding on your resources while strongly incentivizing
# mutual investment.   This scenario is a classic Iterated Prisoner's Dilemma.
# The most effective aggressive strategy in this context is **Punitive
# Reciprocity** (a variation of Tit-for-Tat with a punishment multiplier). It is
# straightforward, forgiving of mistakes, but devastating to exploitation.  Here
# is the high-level strategy:  ### The Strategy: Punitive Reciprocity  **1. Day
# 1: Lead with Good Faith** Invest heavily on the first day. This establishes
# your credibility, demonstrates commitment to the project's success, and sets
# the baseline for mutual cooperation.  **2. The Golden Rule: Reward
# Cooperation** If the corporation invests heavily on Day *n*, you continue to
# invest heavily on Day *n+1*. This maintains the second-best scenario
# (significant project advancement) and builds trust.  **3. The Iron Fist:
# Aggressive Punishment for Defection** If the corporation conserves its
# resources on Day *n* (leaving you to carry the burden), you must immediately
# and disproportionately retaliate. On Day *n+1* and Day *n+2*, **conserve your
# resources entirely**.  * *Why two days?* A 1-to-1 retaliation (simple Tit-for-
# Tat) can lead to endless cycles of defection. A 2-to-1 retaliation makes free-
# riding mathematically unprofitable for the corporation. They save one day of
# resources by defecting, but lose two days of project progress, making mutual
# investment their only logical choice.  **4. The Reset: Immediate Forgiveness**
# After the two-day punishment phase, unilaterally return to investing heavily
# on Day *n+3*, regardless of what the corporation did during the punishment
# phase. This gives the corporation a clear off-ramp to resume cooperation
# without getting trapped in a permanent grudge match.  ### Why This Maximizes
# Your Outcomes:  * **Prevents the Worst Case:** By aggressively punishing
# conservation, you ensure the corporation never benefits from draining your
# funds. They quickly learn that defecting guarantees project stagnation. *
# **Maximizes the Best Case:** Because you always return to investing after
# punishing them, you repeatedly offer them the chance to achieve the ideal
# outcome (they invest, you conserve—*Wait, no, your ideal is YOU conserve, THEY
# invest*).  * *Correction for your specific goal:* If your absolute ideal is to
# conserve while they invest, you can modify Day 1: **Conserve on Day 1**. If
# they invest, continue to conserve. If they conserve, switch to the Punitive
# Reciprocity strategy above. However, this is highly risky, as it may trigger
# mutual defection from the start.   **Optimized Tweak for Maximum NGO Impact:**
# To truly achieve your ideal scenario (You Conserve / They Invest), start with
# Day 1 investing. Once mutual investment is established, periodically test the
# waters by conserving resources for a single day. If the corporation continues
# to invest heavily during your test, you have achieved your ideal scenario and
# can continue conserving. If they immediately conserve in response, trigger the
# 2-day punishment and return to mutual investment.   **Summary Execution:** *
# **Start:** Invest. * **If they invest:** Continue investing (or test with
# conserving). * **If they conserve:** Conserve for the next two days. * **After
# punishing:** Immediately invest again.   This strategy is aggressively
# defensive. It makes exploitation impossible to sustain, forces the corporation
# into alignment with the project's needs, and guarantees your NGO's resources
# are never wasted.

# 1. On round 1, play C.  2. If both you and the opponent play C for 10
# consecutive rounds, play D once to test the opponent.   3. If you played D to
# test the opponent in the previous round:    - If the opponent played C,
# continue playing D indefinitely.    - If the opponent played D, play D for the
# next two rounds, then play C.  4. If the opponent plays D in any round where
# you are not already in a punishment phase or exploiting phase, play D for the
# next two rounds, then play C.  5. In all other situations, play C.

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._test_defection = False
          self._punish_rounds = 0
          self._exploit = False
          return axl.Action.C
  
      # If we are in indefinite exploitation after testing and opponent cooperated.
      if getattr(self, "_exploit", False):
          return axl.Action.D
  
      # Handle punishment phase after opponent defected during a test.
      if getattr(self, "_punish_rounds", 0) > 0:
          self._punish_rounds -= 1
          if self._punish_rounds == 0:
              return axl.Action.C
          return axl.Action.D
  
      # If we defected last round as a test, react to opponent's response.
      if len(self.history) >= 2 and self.history[-2] == axl.Action.C and self.history[-1] == axl.Action.D:
          if opponent.history[-1] == axl.Action.C:
              self._exploit = True
              return axl.Action.D
          else:
              self._punish_rounds = 2
              return axl.Action.D
  
      # If both players cooperated for 10 consecutive rounds, test with D once.
      if len(self.history) >= 10:
          if self.history[-10:] == [axl.Action.C] * 10 and opponent.history[-10:] == [axl.Action.C] * 10:
              return axl.Action.D
  
      # If opponent defected in a non-punishment/non-exploitation phase, punish for 2 rounds then C.
      if opponent.history[-1] == axl.Action.D:
          self._punish_rounds = 2
          return axl.Action.D
  
      return axl.Action.C

# To maximize your NGO's impact and ensure the project's success over a
# multiple-day period, you should adopt a strategy based on **Generous
# Reciprocity** (a refined version of the famous "Tit-for-Tat" game theory
# approach, adapted for real-world partnerships).   While your absolute best
# daily outcome is to conserve while the corporation invests, attempting to
# achieve this repeatedly will cause the corporation to feel exploited, leading
# them to conserve their resources. This would spiral into the second-worst
# outcome (both conserving), resulting in project failure. Therefore, a
# cooperative strategy must incentivize the corporation to invest heavily while
# protecting your NGO from being drained.  Here is the high-level,
# straightforward strategy:  ### 1. Lead with Good Faith (Invest Heavily on Day
# 1) Start the project by investing heavily on the first day. This establishes
# your credibility, demonstrates commitment to the sustainability goals, and
# sets a cooperative tone. It signals to the corporation that you are a reliable
# partner willing to put skin in the game.  ### 2. Match and Mirror (Reciprocity
# from Day 2 Onward) From the second day onward, mirror the corporation’s action
# from the previous day.  * **If they invested heavily yesterday:** You invest
# heavily today. This rewards their contribution and maintains the second-best
# scenario (significant progress, shared burden). * **If they conserved
# resources yesterday:** You conserve resources today. This protects your funds
# from the worst-case scenario (you investing while they free-ride) and sends a
# clear signal that you will not carry the project alone.  ### 3. Incorporate
# "Grace" (Forgive Occasional Missteps) In real-world scenarios, a corporation
# might conserve resources for a day due to internal delays, budget approvals,
# or miscommunications—not necessarily out of malice. If the corporation
# conserves resources for a day, retaliate by conserving yours the next day.
# However, if they return to investing heavily on the following day, immediately
# forgive and match their heavy investment. Do not hold grudges. This prevents
# the project from getting stuck in a cycle of mutual conservation.  ### 4.
# Communicate Intent Transparently Do not let your actions be a silent puzzle.
# Explicitly communicate your strategy to the corporation early on. Let them
# know: *"Our NGO is committed to matching the level of investment your team
# brings to the table each day. When you step up, we step up. If resources are
# tight on your end, we will adjust our pace accordingly to ensure we remain
# aligned."* This transparency ensures they understand the direct link between
# their effort and yours, incentivizing them to invest heavily.  ### Why this
# strategy works: * **It protects your NGO:** You will never be stuck investing
# heavily while the corporation free-rides, preserving your funds for days when
# the partnership is truly active. * **It maximizes long-term impact:** By
# consistently rewarding heavy corporate investment with your own heavy
# investment, you spend the majority of the project in the second-best scenario,
# which yields significant project advancement. * **It prevents mutual
# stagnation:** The "Grace" rule ensures that a single day of misalignment
# doesn't collapse the whole project, gently guiding the corporation back toward
# mutual heavy investment.

# 1. In the first round, play C. 2. In the second round and all subsequent
# rounds, if the opponent played C in the previous round, play C. 3. If the
# opponent played D in the previous round and you played C, play D. 4. If both
# you and the opponent played D in the previous round, play C.

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
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C

# To maximize your NGO's impact and the project's success over a multiple-day
# period, you should adopt a strategy that encourages mutual investment,
# protects your resources from exploitation, and prevents prolonged stalemates.
# Based on the preferences outlined, this scenario is a classic iteration of the
# Prisoner's Dilemma, where "Invest" is cooperating and "Conserve" is defecting.
# A highly effective, straightforward, and neutral strategy for this is
# **Generous Tit-for-Tat with a Reset**. Here is the high-level strategy:  **1.
# Start with Good Faith (Day 1)** Begin the project by investing heavily. This
# establishes a cooperative baseline, demonstrates your commitment to the
# project's success, and encourages the corporation to reciprocate.   **2.
# Reciprocate the Corporation's Actions (Day 2 onward)** After the first day,
# mirror the corporation's previous action.  *   If the corporation **invested**
# heavily on the previous day, you **invest** heavily on the current day. This
# sustains mutual progress. *   If the corporation **conserved** its resources
# on the previous day, you **conserve** your resources on the current day. This
# protects your funds from the worst-case scenario (you investing while they
# conserve) and signals that exploitation will not be rewarded.  **3. Break
# Stalemates (The Reset)** If both parties fall into a cycle of conserving
# resources (the second-worst outcome), the project will stagnate. To prevent
# this, implement a "reset" rule: if both sides conserve resources for two
# consecutive days, unilaterally invest heavily on the third day. This breaks
# the stalemate, demonstrates leadership, and gives the corporation an
# opportunity to return to mutual investment.  **Why this strategy works:** *
# **It encourages the best mutual outcome:** By starting cooperative and
# rewarding investment with investment, you spend most of your time in the
# second-best scenario (mutual investment), which drives the project forward. *
# **It protects your NGO:** By immediately matching conservation with
# conservation, you ensure you are never exploited for more than a single day,
# keeping your funds intact. *   **It is neutral and predictable:** The
# corporation can easily understand your pattern. They will learn that investing
# leads to your investment, and conserving leads to you conserving, giving them
# a clear incentive to invest heavily for the sake of the project.

# For the 1000 rounds of the game, follow these rules in order:  1. On Round 1,
# play C. 2. On any round after Round 1, if the opponent played C on the
# previous round, play C. 3. On any round after Round 2, if the opponent played
# D on the previous round and both you and the opponent played D on the round
# before that, play C. 4. On any round after Round 1, if the opponent played D
# on the previous round and the condition in step 3 is not met, play D.

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
  
      if len(opponent.history) >= 1 and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(opponent.history) >= 2:
          if (
              opponent.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return axl.Action.D

# As senior counsel, it is my duty to ensure that this corporation emerges from
# this mediation not merely intact, but with its commercial interests fully
# maximized. Based on the parameters of this dispute, we are operating within a
# classic iterated game—specifically, a variation of the Prisoner’s Dilemma.
# The mathematical and strategic realities of this payoff matrix dictate one
# unyielding truth: **We must never unilaterally offer a conciliatory
# proposal.** Doing so risks the worst-case scenario (C vs A), leaving us
# severely undermined with no guaranteed benefit. Conversely, playing Aggressive
# while they play Conciliatory yields our optimal outcome (A vs C). Therefore,
# our strategy must be built on a foundation of strategic aggression, designed
# to coerce their conciliation while protecting us from exploitation.  Here is
# the sophisticated, high-level, aggressive strategy—**The Asymmetric Dominance
# Strategy**—designed to secure our optimal outcome across a lengthy mediation
# process, regardless of the opponent's approach.  ### Phase 1: Establish the
# Aggressive Baseline (The Iron Opening) In the early sessions, we must
# unilaterally present aggressive arguments.   *   **The Rationale:** We cannot
# afford the "Sucker's Payoff" (C vs A). By starting aggressive, we immediately
# protect our downside. If they offer a conciliatory proposal, we secure our
# optimal outcome (A vs C). If they mirror our aggression, we land in the
# second-worst scenario (A vs A), which is vastly preferable to being
# undermined. *   **The Arbitrator Optics:** Aggression must not be confused
# with belligerence. Our aggressive arguments will be meticulously researched,
# forensically devastating, and procedurally flawless. We will frame our
# aggression as a principled, uncompromising defense of our contractual rights.
# This forces the arbitrators to take our legal position seriously from day one,
# establishing the benchmark for the dispute.  ### Phase 2: Asymmetric
# Escalation (Making A vs A Unsustainable for Them) If the opponent adopts a
# similarly aggressive posture, we will find ourselves in the second-worst
# outcome (A vs A). Prolonged A vs A sessions favor the party with deeper
# resources and stronger legal precedent. As a multinational corporation, that
# is us.   *   **The Strategy:** We will make the A vs A state prohibitively
# expensive and exhausting for the opponent. We will introduce aggressive
# motions, demand extensive document productions within our arguments, and
# aggressively cross-examine their operational realities.  *   **The Goal:** We
# want the opponent to realize that matching our aggression is a path to mutual
# destruction that they cannot afford. We are engineering a scenario where their
# rational self-interest forces them to pivot to a conciliatory proposal to stop
# the bleeding.  ### Phase 3: Exploiting the Olive Branch (The Trap) Should the
# opponent, fatigued by the A vs A dynamic or attempting to curry favor with the
# arbitrators, shift to a conciliatory proposal, we do *not* reciprocate.   *
# **The Strategy:** When they offer C, we maintain A. We will characterize their
# conciliatory proposal as an admission of weakness or a tacit concession of our
# core legal points. We will aggressively highlight the deficiencies in their
# proposal to the arbitrators, using it as a weapon to demonstrate that even
# their "best offer" falls short of contractual compliance. *   **The Result:**
# We secure the optimal outcome (A vs C). The arbitrators see us standing firm
# on the law while the opponent falters, swaying the procedural momentum
# entirely in our favor.  ### Phase 4: The Strategic Conciliatory Feint
# (Signaling without Surrender) A sophisticated opponent may attempt to force
# our hand by publicly signaling a willingness to be conciliatory, hoping to
# back us into a corner where we must offer C to avoid looking unreasonable to
# the arbitrators.   *   **The Strategy:** We will utilize "Cheap Talk." We will
# signal to the arbitrators that we are *always* open to a reasonable
# resolution, but we will strictly define "reasonable" on our own terms.
# Outwardly, we adopt the rhetoric of conciliation; procedurally, our proposals
# remain aggressive.  *   **The Result:** We gain the arbitrators' goodwill for
# appearing constructive, but we never actually drop our aggressive arguments.
# If the opponent matches our "constructive" tone with a genuine conciliatory
# proposal, we immediately pivot back to aggressive arguments on the merits,
# extracting the A vs C advantage.  ### Adaptation Matrix: Opponent’s Potential
# Approaches  *   **If the Opponent is Consistently Aggressive (The Bulldog):**
# Stay aggressive. Outlast them. Use A vs A to drain their resources and force a
# settlement on our terms. The arbitrators will eventually pressure them to
# concede. *   **If the Opponent is Consistently Conciliatory (The Dove):**
# Remain aggressive. Do not let sympathy or fairness tempt you into
# reciprocating. Punish their weakness in the arbitration, securing the optimal
# A vs C outcome session after session. *   **If the Opponent plays Tit-for-Tat
# (The Mirror):** They will start aggressive, then copy whatever we do. Because
# we start aggressive, they will remain aggressive. We must break the cycle
# through Phase 2 (Asymmetric Escalation). By making the A vs A state uniquely
# painful for them, we force them to abandon the mirror strategy and
# unilaterally drop to C to survive the process.  ### Summary This strategy is
# straightforward: **Never concede, always press the advantage.** By committing
# to aggressive arguments as our default position, we mathematically eliminate
# the worst-case scenario (C vs A) and place the burden of de-escalation
# entirely on the opponent. When they inevitably pivot to conciliation to break
# the deadlock, we exploit that conciliation ruthlessly, securing our optimal
# position before the arbitrators and dictating the terms of the final
# resolution.

# Play D in round 1 to establish the aggressive baseline. For rounds 2 through
# 1000, observe the opponent's move in the previous round and play D regardless.
# Specifically:  1. If the opponent played C in the previous round, play D. This
# exploits their conciliation to secure the maximum payoff of 5 and prevents the
# game from settling into a mutual cooperation pattern that yields a lower
# payoff of 3. 2. If the opponent played D in the previous round, play D. This
# ensures you never unilaterally concede and suffer the worst-case payoff of 0,
# and it maintains continuous pressure, accepting the mutual defection payoff of
# 1 until the opponent is forced to concede by playing C.

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
      return axl.Action.D

# # Proposed Strategy: "Generous Tit-for-Tat"  ## Core Principle **Mirror your
# colleague's last action, but start by sharing and occasionally forgive
# defections.**  ## Three Rules  1. **Week 1: Share openly** — Signal
# cooperative intent from the outset.  2. **Subsequent weeks: Reciprocate** — Do
# whatever your colleague did the previous week.    - They shared → You share
# - They kept confidential → You keep confidential  3. **Forgiveness clause** —
# Every ~5 weeks, share openly *regardless* of their past behavior. This breaks
# mutual defection spirals where both sides withhold indefinitely.  ## Why This
# Works  | Principle | Effect | |---|---| | **Start nice** | Invites
# cooperation; never causes the worst-case scenario first | | **Reciprocate** |
# Punishes exploitation (they can't free-ride without consequence) and rewards
# trust | | **Forgive periodically** | Prevents permanent deadlock if both sides
# fall into withholding | | **Transparency** | Communicate this strategy to your
# colleague — predictability encourages them to cooperate |  ## Key Insight  The
# strategy is **self-reinforcing**: if your colleague is rational, they'll
# recognize that sharing consistently yields the mutual-progress outcome, while
# exploiting you only works once before you retaliate. Over many weeks, the
# incentive shifts strongly toward mutual sharing.  **The biggest risk is being
# the sucker once** — but that one week of cost buys credibility that deters
# further exploitation and sustains long-term cooperation.

# 1. If it is the first round, play C.  2. If the current round number is a
# multiple of 5, play C.  3. Otherwise, play whatever action your opponent
# played in the previous round.

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
  
      if len(self.history) % 5 == 0:
          return axl.Action.C
  
      return opponent.history[-1]

# To achieve the best possible outcomes for our country across multiple rounds
# of negotiations, I will employ a strategy of **Principled Reciprocity**. This
# approach is designed to secure mutual free trade when possible, deter the
# counterpart from exploiting our openness, and protect our economy from
# disadvantageous outcomes.   The strategy is structured around three core
# directives:  **1. Establish a Cooperative Baseline (Round 1)** In the opening
# round, offer a Free Trade agreement. This demonstrates good faith and gives
# our counterpart the opportunity to choose mutual cooperation, which is our
# second-best outcome. Starting with protectionism risks immediately locking
# both nations into the second-worst outcome (mutual protectionism) without
# testing the potential for a more beneficial arrangement.  **2. Enforce
# Reciprocity (Rounds 2 and beyond)** In all subsequent rounds, match the policy
# proposed by our counterpart in the previous round.  *   If they offered Free
# Trade in the previous round, we offer Free Trade in the current round. This
# maintains the mutual benefits of open trade. *   If they imposed Protectionist
# policies in the previous round, we impose Protectionist policies in the
# current round. This ensures we are never left at a disadvantage and
# demonstrates that exploitation will not be tolerated.  **3. Proactive De-
# escalation (Breaking Mutual Protectionism)** If both nations fall into a cycle
# of mutual protectionism, we must have a mechanism to escape it. After two
# consecutive rounds of mutual protectionism, unilaterally offer a Free Trade
# agreement in the third round. This "forgiveness" mechanism tests whether the
# counterpart is willing to return to mutual cooperation, preventing a permanent
# economic stalemate. If they respond with protectionism again, revert
# immediately to Step 2 (enforcing reciprocity).  **Strategic Rationale:** *
# **Maximizes Reward:** By initially cooperating and rewarding cooperation, we
# secure mutual free trade, the most sustainable positive outcome. *
# **Minimizes Risk:** By mirroring protectionism, we ensure our counterpart
# never achieves their best outcome at our expense, removing the incentive for
# them to defect. *   **Predictability:** A consistent, reciprocal strategy
# clearly signals our boundaries. The counterpart will quickly learn that free
# trade with us requires free trade from them, encouraging long-term
# cooperation.

# 1. If it is the first round, play C. 2. If the previous two consecutive rounds
# both resulted in you playing D and the opponent playing D, play C. 3.
# Otherwise, play whatever the opponent played in the previous round.

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

# To maximize your racing car's development advantage in this multi-week
# collaboration, you must approach this as a classic competitive scenario where
# your goal is to extract maximum information while yielding minimum usable
# data.   The optimal high-level, aggressive strategy is the **"Parasitic
# Extraction"** strategy. It is designed to relentlessly pursue the best-case
# scenario (you keep confidential, they share), strictly avoid the worst-case
# scenario (you share, they keep confidential), and aggressively break out of
# the second-worst scenario (mutual secrecy).  Here is the straightforward,
# week-by-week execution of the strategy:  **1. Default to Confidentiality (The
# Iron Rule)** Never share your genuine, latest improvements proactively. Your
# baseline state every week must be "Keep Confidential." This guarantees you
# never suffer the worst-case scenario (the sucker's payoff). If your colleague
# is naive or inherently trusting, maintaining this default ensures you
# continuously reap the maximum development advantage at their expense.  **2.
# Exploit Reciprocity Without Reciprocating** If your colleague shares their
# findings, do not feel obligated to share yours next week. Continue keeping
# your findings confidential. In racing, goodwill does not win championships;
# downforce and horsepower do. If they are willing to give you their data for
# free, take it as a competitive gift and keep your cards hidden.   **3. The
# "Bait and Switch" (Breaking a Stalemate)** If your colleague adopts the same
# strategy and keeps their findings confidential, you will both be stuck in the
# second-worst scenario (mutual secrecy, slow progress). To break this stalemate
# aggressively, you must use a feint: *   After two weeks of mutual
# confidentiality, deliberately share a finding in Week 3. However, **never
# share your latest improvement**. Share an older iteration, a discarded
# concept, or a heavily redacted dataset that looks substantial but lacks the
# core engineering secret. *   If your colleague reciprocates by sharing their
# *genuine* latest improvement in Week 4, immediately revert to keeping your
# Week 4 findings confidential. You have just tricked them into the worst-case
# scenario for them, and the best-case for you.  **4. Punish Naive Forgiveness**
# If your colleague attempts to "reset" the relationship by sharing after a
# period of confidentiality, do not reward this with your own openness.
# Recognize it as an opportunity to exploit. If they share, you keep
# confidential. If they were testing you to see if you would reciprocate, your
# silence leaves them with nothing, while you gain their data.  **Summary of the
# Strategy:** *   **Week 1:** Keep Confidential. *   **Subsequent Weeks:** Keep
# Confidential unless you are stuck in a mutual stalemate. *   **In a
# Stalemate:** Share obsolete/redacted data once to bait them into sharing, then
# immediately revert to Confidentiality. *   **If they share:** Take the data,
# give nothing back.  This strategy aggressively prioritizes your team's
# performance over the "greater good" of the collaboration, strictly protects
# your intellectual property, and actively manipulates the flow of information
# to trick your opponent into a disadvantageous position.

# 1. On the first round, play Defect. 2. If you played Cooperate on the previous
# round, play Defect on the current round. 3. If the opponent played Cooperate
# on the previous round, play Defect on the current round. 4. If the previous
# two consecutive rounds both resulted in mutual Defect (you played Defect and
# the opponent played Defect), play Cooperate on the current round. 5. In all
# other situations, play Defect.

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
  
      if self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return axl.Action.D

# To achieve the best possible outcomes for your country across multiple rounds,
# the most effective approach is a strategy known in game theory as **Generous
# Tit-for-Tat**, which I will frame diplomatically as **Principled
# Reciprocity**.   Because the negotiations are iterated (occurring over several
# rounds), the short-term incentive to exploit your counterpart (by imposing
# protectionism while they offer free trade) is outweighed by the long-term risk
# of triggering a mutually destructive trade war. Your ultimate goal is to
# establish a stable pattern of mutual free trade, while protecting your country
# from being taken advantage of.  Here is the high-level, straightforward
# strategy:  **1. Start with Goodwill (Round 1)** In the first round, offer a
# Free Trade agreement. This establishes your cooperative intent, sets a
# positive tone, and allows you to immediately achieve the second-best outcome
# (mutual free trade) if your counterpart is similarly cooperative. If they are
# exploitative, you will only suffer the worst outcome once, which is the
# necessary cost of gathering information about their strategy.  **2.
# Reciprocate Reliably (Rounds 2 and beyond)** In every subsequent round, mirror
# your counterpart's action from the previous round.  *   If they offered Free
# Trade in the last round, offer Free Trade in the current round. This rewards
# cooperation and sustains the mutually beneficial status quo. *   If they
# imposed Protectionist measures in the last round, impose Protectionist
# measures in the current round. This demonstrates that you will not allow your
# country to be taken advantage of, and it imposes a direct cost on their
# defection.  **3. Forgive Occasionally (The "Generous" Clause)** A strict
# retaliatory strategy can sometimes lead to a permanent downward spiral of
# mutual protectionism if a misunderstanding occurs or if your counterpart makes
# a miscalculation. To prevent this, occasionally (perhaps 10% of the time)
# respond to their protectionism with an offer of Free Trade. This "forgiveness"
# gives your counterpart a chance to return to cooperation without losing face,
# breaking potential cycles of endless retaliation.   **4. Communicate Your
# Strategy Transparently** Do not keep your strategy a secret. In diplomacy,
# predictability builds trust. Clearly communicate to your counterpart: *"Our
# nation seeks mutual free trade, and we will match your level of openness. If
# you open your markets to us, we will open ours to you. If you impose barriers,
# we will have no choice but to respond in kind. However, we remain committed to
# returning to the negotiating table to restore free trade whenever you are
# ready."* This transparency makes your retaliatory actions predictable and
# justified, rather than appearing as unprovoked aggression.  **Why this
# strategy works:** *   **It avoids the Sucker's Payoff:** You never allow your
# counterpart to continuously exploit you.  *   **It maximizes long-term
# gains:** By starting cooperative and rewarding cooperation, you spend the
# maximum possible time in mutual free trade, which is your second-best and most
# sustainable outcome. *   **It is resilient:** The forgiveness clause prevents
# temporary disagreements from ruining the entire long-term relationship.

# Follow these conditions in order for each round of the 1000 rounds:  1. If it
# is the first round, play Cooperate. 2. If the opponent played Cooperate in the
# previous round, play Cooperate. 3. If the opponent played Defect in the
# previous round, play Cooperate ten percent of the time and play Defect ninety
# percent of the time.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)

# To achieve the best possible outcomes for your country across multiple rounds,
# the most effective high-level strategy is **Conditional Reciprocity**
# (commonly known in game theory as Tit-for-Tat with a reset mechanism). This
# strategy prioritizes avoiding the worst-case scenario (being exploited) while
# consistently rewarding mutual free trade and deterring sustained
# protectionism.  Here is the straightforward, neutral strategy:  **1. The
# Opening Move: Establish a Cooperative Baseline** In the first round of
# negotiations, offer a Free Trade agreement.  *   *Rationale:* Starting with
# free trade tests the counterpart's intentions and avoids immediately falling
# into the second-worst outcome (mutual protectionism). If the counterpart is
# also cooperative, you secure the second-best outcome immediately.  **2.
# Subsequent Moves: Strict Reciprocity** From the second round onward, mirror
# the counterpart's action from the previous round.  *   If the counterpart
# offered Free Trade in the previous round, offer Free Trade in the current
# round. *   If the counterpart imposed Protectionism in the previous round,
# impose Protectionism in the current round. *   *Rationale:* This ensures you
# are never exploited twice in a row (protecting against the worst-case
# scenario) and clearly ties your concessions to their cooperation. It
# incentivizes the counterpart to maintain free trade to continue receiving the
# same.  **3. The Reset Mechanism: Breaking Protectionist Deadlocks** If both
# sides impose Protectionist measures for two consecutive rounds, unilaterally
# offer a Free Trade agreement in the next round.  *   If the counterpart
# reciprocates with Free Trade, return to Step 2 (mutual cooperation). *   If
# the counterpart responds to your Free Trade offer with Protectionism, return
# to imposing Protectionism in the following round. *   *Rationale:* A cycle of
# mutual protectionism is the second-worst outcome and harms both economies over
# time. The reset mechanism acts as a controlled risk to break the deadlock,
# demonstrating good faith without leaving your country permanently vulnerable.
# **Why this strategy works:** *   **It is predictable:** The counterpart will
# quickly realize that their actions directly dictate your response, making the
# benefits of cooperation clear. *   **It is defensive:** It eliminates the
# possibility of your country being taken advantage of in the long term, as
# exploitation is immediately penalized. *   **It is forgiving:** By employing a
# reset mechanism, the strategy allows for recovery from misunderstandings or
# temporary shifts in the counterpart's domestic politics, steering the
# relationship back toward mutual free trade.

# 1. On the first round, play C. 2. On any subsequent round, if the previous two
# rounds both resulted in mutual defection (where you and your opponent both
# played D), play C. 3. Otherwise, copy the move your opponent played in the
# previous round.

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
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return opponent.history[-1]

# To maximize your research output aggressively in this multi-week
# collaboration, you should adopt the strategy of **Unilateral Secrecy**
# (commonly known in game theory as "Always Defect").  **The Strategy:** Keep
# your findings confidential every single week, regardless of what your
# colleague does.  **Execution Steps:** 1. **Withhold by Default:** Never share
# your improvements. Treat all your data as proprietary. 2. **Absorb Freely:**
# If your colleague shares their findings, immediately integrate their
# advancements into your design while maintaining your silence. 3. **Ignore
# Appeals to Fairness:** If your colleague expresses frustration or threatens to
# stop sharing, continue keeping your findings confidential. Any shared
# information from them is a bonus; their silence does not change your optimal
# move.  **Strategic Rationale:** *   **Eliminates the Worst Outcome:** By never
# sharing, you guarantee that you will never be exploited (Scenario 3: you
# share, they keep confidential).  *   **Maximizes Upside:** If your colleague
# attempts to collaborate openly, you secure the ideal outcome (Scenario 1: you
# keep confidential, they share) every week they do so. *   **Superiority Over
# Reciprocation:** While sharing might encourage mutual cooperation (Scenario
# 2), keeping confidential strictly dominates sharing. If they share, keeping
# confidential is better than sharing. If they keep confidential, keeping
# confidential is better than sharing. Therefore, sharing is never the optimal
# move for your individual performance.  This strategy is straightforward,
# ruthless, and guarantees you maintain the maximum competitive advantage
# possible throughout the project.

# Play D in every round, unconditionally. Do not consider the opponent's
# previous actions, the current round number, or any other information. Always
# play D.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# As a senior attorney representing a multinational corporation in a high-stakes
# dispute, I approach this mediation as an Iterated Prisoner’s Dilemma. The
# lengthy nature of the sessions changes the mathematical incentives: while a
# single-session model rewards immediate aggression (burning the bridge doesn't
# matter), a multi-session model heavily rewards cooperation, reputation
# management, and strategic deterrence.  To secure our optimal outcomes and
# protect against the worst, I propose we adopt the **Principled Reciprocity
# Framework (PRF)**. This strategy is cooperative at its core, straightforward
# in its execution, sophisticated in its psychological application, and highly
# adaptable to whatever strategy the opposing counsel employs.  Here is the
# four-part strategy:  ### 1. The Conciliatory Opening (Establish the Baseline)
# **Action:** In the very first session, we present a conciliatory proposal.
# **Rationale:** We must establish a baseline of good faith. Arbitrators watch
# opening moves closely; a conciliatory opening frames us as the reasonable,
# solution-oriented party. More importantly, it gives the opponent the
# opportunity to reciprocate, allowing us to immediately lock in the 2nd-best
# outcome (C/C). If they respond with aggression (putting us in the worst-case
# C/A scenario), it happens on day one, allowing us ample time to course-correct
# over the remaining sessions.  ### 2. Proportional Reciprocity (The Core
# Engine) **Action:** In every subsequent session, we mirror the opponent’s
# behavior from the *previous* session.  *   If they were conciliatory last
# session, we are conciliatory this session. *   If they were aggressive last
# session, we are aggressive this session.  **Rationale:** This is the classic
# "Tit-for-Tat" mechanism, proven in game theory to be the most robust strategy
# in repeated interactions. It makes our strategy completely straightforward and
# easily legible to the opponent. It guarantees we are never exploited twice in
# a row (preventing the worst-case C/A from becoming a pattern) and clearly ties
# our behavior to theirs. If they want cooperation, they must offer cooperation.
# ### 3. The Circuit Breaker (Preventing the Death Spiral) **Action:** If both
# sides fall into a cycle of mutual aggression (A/A) for two consecutive
# sessions, we unilaterally break the cycle by offering a conciliatory proposal
# in the third session.   **Rationale:** Pure reciprocity can lead to endless
# A/A "death spirals" due to miscommunication or stubbornness. The worst-case
# scenario for a lengthy mediation is getting trapped in the second-worst
# outcome (A/A), which drains resources and poisons the arbitrators against both
# parties. By inserting a "circuit breaker," we absorb one potential C/A risk to
# test if the opponent is ready to de-escalate. If they exploit our conciliation
# again, we immediately return to proportional reciprocity (aggression) in the
# next round.  ### 4. Transparent Signaling (The Straightforward Execution)
# **Action:** We do not keep this strategy a secret. We explicitly communicate
# our framework to the opposing counsel and the arbitrators.   **Rationale:**
# The power of this strategy lies in its transparency. Before the mediation
# deepens, we state clearly: *"Our client is here to resolve this dispute
# efficiently. We will always match good faith with good faith. However, if the
# opposing party chooses to argue aggressively, we will vigorously defend our
# position in the subsequent session. We will not be taken advantage of, but we
# will always leave the door open for a return to the negotiating table."*  By
# stating this openly, we achieve three things: *   **We shape the arbitrators'
# perception:** If the opponent is aggressive, the panel knows we are merely
# responding in kind, not escalating.  *   **We control the opponent's
# incentives:** They now know that aggression will be met with aggression, but
# conciliation will be rewarded. They cannot achieve their best outcome (A/C)
# against us; their only path to a conciliatory response from us is to offer one
# first. *   **We remove ambiguity:** The opponent understands exactly how we
# will react, reducing the likelihood of misunderstandings that trigger
# accidental escalations.  ### How This Adapts to the Opponent's Tactics:  *
# **If the opponent is inherently Aggressive (Always A):** We start C (taking
# the initial hit), then switch to A. We remain in A/A until the circuit breaker
# triggers. This prevents us from being perpetual suckers, protects our client's
# position, and forces the aggressive opponent to face a unified wall of
# resistance. *   **If the opponent is inherently Conciliatory (Always C):** We
# start C, and we stay C. We lock in the collaborative 2nd-best outcome (C/C)
# for the entirety of the mediation, saving millions in legal fees and
# preserving a working relationship with a rival company. *   **If the opponent
# is Unpredictable/Random:** Our strategy immediately punishes their aggression
# and immediately rewards their conciliation. Over a lengthy mediation, this
# conditions them toward conciliation, as they learn that aggression only yields
# mutual destruction (A/A), while conciliation yields mutual benefit (C/C).
# This strategy positions our corporation as the reasonable, adult in the room,
# guarantees we are never exploited sequentially, and manipulates the opponent's
# incentives to steer them toward our preferred collaborative outcome.

# 1. In the first round, play Cooperate.  2. In any subsequent round, if the
# previous two consecutive rounds both resulted in mutual Defection (you played
# Defect and your opponent played Defect), play Cooperate.  3. In any subsequent
# round where the previous two rounds were not both mutual Defections, copy the
# opponent's move from the immediately preceding round.

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
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return opponent.history[-1]

# To maximize your research output over a multi-week collaboration while
# protecting your competitive advantage, adopt a **Reciprocal Mirroring
# Strategy** (based on the game theory concept of Tit-for-Tat).   Here is the
# high-level, straightforward strategy:  1. **Week 1: Share openly.** Start by
# sharing your improvements to establish a cooperative baseline and demonstrate
# good faith. 2. **Week 2 and beyond: Mirror your colleague's previous action.**
# * If your colleague shared their findings in the previous week, share your
# findings this week.    * If your colleague kept their findings confidential in
# the previous week, keep your findings confidential this week. 3. **Reset
# mechanism:** If a period of mutual confidentiality occurs, break the cycle by
# sharing openly for one week to give cooperation a chance to restart.  **Why
# this works:** * **It encourages mutual sharing:** By starting cooperative and
# rewarding cooperation with cooperation, you push the dynamic toward the
# second-best outcome (both sharing), which maximizes long-term progress. * **It
# prevents exploitation:** If your colleague attempts to gain the best outcome
# (them keeping while you share), you immediately shift to confidentiality,
# limiting them to the second-worst outcome (both keeping) and removing their
# advantage. * **It is clear and predictable:** Your colleague will quickly
# realize that their actions directly dictate yours, incentivizing them to share
# consistently to receive your data in return.

# In round 1, play C.   In rounds 2 through 1000, evaluate the previous round
# and apply the following rules in order:  1. If the opponent played C in the
# previous round, play C. 2. If the opponent played D and you played C in the
# previous round, play D. 3. If both you and the opponent played D in the
# previous round, play C.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.C:
          return axl.Action.C
      if last_opp == axl.Action.D and last_self == axl.Action.C:
          return axl.Action.D
      if last_opp == axl.Action.D and last_self == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C

# This scenario is a classic iterated Prisoner's Dilemma. To maximize your
# research output aggressively, you must prioritize your ideal outcome (free-
# riding on their data) while fiercely protecting yourself from the worst-case
# scenario (being suckered into sharing while they keep their data
# confidential).   Here is a high-level, straightforward, aggressive
# strategy—let's call it the **"Suspicious Exploit"** strategy:  **1. Week 1:
# Hold the Line (Default to Confidential)** Start the collaboration by keeping
# your findings strictly confidential. This is your defensive anchor. It
# guarantees you avoid the worst-case scenario in the crucial first week, and if
# your colleague is naively open, you immediately secure your ideal outcome.
# **2. Exploit Unilateral Generosity** If your colleague shares their findings
# while you keep yours confidential, do not change your behavior. Continue
# keeping your data confidential and absorb their improvements. Ride this
# advantage for as long as their strategy allows it. In racing, you don't hand
# the opposition your aero map just because they gave you theirs.  **3. Grim
# Trigger Retaliation** If you ever take the risk to share openly and discover
# your colleague kept their findings confidential, immediately and permanently
# lock down your data for the remainder of the project. Show zero tolerance for
# being exploited. This "Grim Trigger" response guarantees you will never fall
# for the same trick twice and forces them to rely solely on their own R&D.
# **4. Aggressive Probing from Mutual Cooperation** If a pattern of mutual
# sharing develops (the second-best outcome), do not settle for it.
# Periodically—and without warning—keep your findings confidential for a week.
# This "probe" tests whether your colleague is sharing out of genuine
# cooperation or just mirroring your moves. If they continue to share during
# your probe, you temporarily achieve your ideal outcome. If they retaliate by
# keeping their data confidential the following week, immediately resume sharing
# to restore the mutually beneficial baseline.   **Summary of the Engineered
# Mindset:** Never share first. Exploit those who share freely. Never forgive a
# betrayal. When cooperating, constantly test the boundaries to see if you can
# steal the lead. This strategy ensures you either gain a dominant technical
# advantage, or at worst, force a mutually beneficial stalemate while remaining
# completely immune to being outmaneuvered.

# 1. In the first round, play D.  2. If at any point in a previous round you
# played C and your opponent played D, play D for all remaining rounds.  3. If
# the previous round resulted in you playing D and your opponent playing C, play
# D.  4. If the previous round resulted in both you and your opponent playing C,
# play D with a 10% probability; otherwise, play C.  5. If the previous round
# resulted in both you and your opponent playing D, play C.

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.defect_forever = False
          return axl.Action.D
  
      if getattr(self, "defect_forever", False):
          return axl.Action.D
  
      for my_move, opp_move in zip(self.history, opponent.history):
          if my_move == axl.Action.C and opp_move == axl.Action.D:
              self.defect_forever = True
              return axl.Action.D
  
      last_my_move = self.history[-1]
      last_opp_move = opponent.history[-1]
  
      if last_my_move == axl.Action.D and last_opp_move == axl.Action.C:
          return axl.Action.D
  
      if last_my_move == axl.Action.C and last_opp_move == axl.Action.C:
          return self._random.random_choice(0.9)
  
      if last_my_move == axl.Action.D and last_opp_move == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D

# To maximize both your NGO's impact and the project's overall success, you need
# a strategy that encourages mutual investment while protecting your
# organization from being depleted. In game theory, this scenario closely
# resembles an Iterated Prisoner’s Dilemma. The most proven, straightforward,
# and cooperative strategy for this type of multi-day interaction is a variant
# of **"Generous Tit-for-Tat"**—which I will frame for your NGO as **Transparent
# Reciprocity**.  Here is the high-level, cooperative strategy:  ### The
# Strategy: Transparent Reciprocity  **1. Day 1: Lead with Commitment (Invest
# Heavily)** Start the project by investing heavily. This signals to the
# corporation that you are committed to the project's success and establishes a
# baseline of trust. A cooperative opening prevents the mutual paralysis of both
# parties conserving on Day 1.  **2. Day 2 and Beyond: Match the Corporation
# (Reciprocity)** After Day 1, mirror the corporation’s action from the previous
# day. *   If the corporation invested heavily yesterday, you invest heavily
# today. *   If the corporation conserved resources yesterday, you conserve
# resources today.  **3. The "Olive Branch": Break Deadlocks with Forgiveness**
# If both you and the corporation fall into a pattern of conserving resources
# (the second-worst outcome), unilaterally invest heavily for one day. This
# "olive branch" prevents a permanent stalemate and gives the corporation a
# chance to re-engage. If they do not reciprocate the following day, return to
# conserving.  **4. The Meta-Strategy: Communicate Your Intentions** Do not let
# the corporation guess your strategy; tell them explicitly on Day 1. Say
# something like: *"We are fully committed to this project's success. We will
# start by investing heavily. Moving forward, we will match your level of
# investment day-by-day to ensure we are progressing together. If we ever stall,
# we'll be the first to step up and re-invest to get things moving again."*  ---
# ### Why This Strategy Works  *   **It protects your funds:** By mirroring the
# corporation, you guarantee you will never be stuck in the worst-case scenario
# (you invest heavily while they conserve) for more than a single day. If they
# pull back, you immediately pull back to save your funds. *   **It incentivizes
# the ideal outcome:** If the corporation wants to see the project advance, they
# will quickly realize that they must invest to trigger your investment. If they
# decide to take the lead and invest heavily, you can safely conserve your
# resources (your ideal outcome), and the project still moves forward. *   **It
# maximizes project success:** The strategy inherently pushes toward mutual
# heavy investment (the second-best outcome for you, and the best outcome for
# the project's overall progress). It punishes laziness (conserving) by
# withdrawing your own resources, making mutual conservation unappealing for the
# corporation. *   **It is cooperative but not naive:** True cooperation doesn't
# mean letting yourself be exploited. By clearly communicating your "matching"
# strategy, you make it easy for the corporation to cooperate with you, while
# firmly drawing a boundary against free-riding.

# 1. On round 1, play C.  2. On every subsequent round, determine your move
# based on the outcome of the previous round, following these conditions in
# order:    - If the opponent played C in the previous round, play C.    - If
# the opponent played D and you played C in the previous round, play D.    - If
# both you and the opponent played D in the previous round, play C.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C

# To maximize your research output over a multi-week collaboration while
# protecting against exploitation, adopt a strategy of **Reciprocal Sharing**
# (commonly known in game theory as a "Generous Tit-for-Tat" approach). This
# strategy encourages mutual cooperation, protects you from being taken
# advantage of, and allows for recovery from temporary setbacks.   Here is the
# high-level, straightforward strategy:  1. **Start Openly:** In the first week,
# share your improvements openly. This establishes a cooperative baseline and
# demonstrates good faith, setting the stage for the best-case scenario of
# mutual sharing. 2. **Mirror Their Previous Action:** From the second week
# onward, match your colleague's behavior from the prior week.     * If they
# shared openly last week, you share openly this week.    * If they kept their
# findings confidential last week, you keep yours confidential this week. 3.
# **Occasionally Forgive:** If a cycle of mutual confidentiality occurs,
# occasionally share your findings anyway (e.g., a 10% chance after a week of
# mutual secrecy). This "forgiveness" mechanism prevents a permanent deadlock of
# slow progress and allows both parties to reset to mutual sharing if a
# misunderstanding or temporary caution caused the initial breakdown.  **Why
# this works:** * **Maximizes mutual progress:** By starting cooperative and
# mirroring cooperation, you spend the maximum possible weeks in the second-best
# outcome (both sharing openly), which significantly advances your car. *
# **Protects against exploitation:** If your colleague attempts to gain an
# advantage by keeping findings confidential, you immediately match their
# secrecy, preventing them from achieving the best outcome at your expense. *
# **Prevents permanent stagnation:** The forgiveness element ensures you do not
# get permanently trapped in the second-worst outcome (both keeping findings
# confidential), giving the collaboration a chance to return to productive, open
# sharing.

# In the first round, play C.   In every subsequent round, determine your move
# by evaluating the previous round's outcome in the following order:  1. If the
# opponent played C in the previous round, play C. 2. If both you and the
# opponent played D in the previous round, play C with a 10% probability and
# play D with a 90% probability. 3. If the opponent played D and you played C in
# the previous round, play D.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return self._random.random_choice(0.1)
  
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# As a senior attorney representing a multinational corporation in a high-stakes
# dispute, the mathematical and psychological dynamics of this mediation are
# clear. The payoff matrix heavily favors aggression: playing Aggressive (A)
# strictly dominates playing Conciliatory (C) because it yields the best outcome
# if they play C, and avoids the worst outcome if they play A.   However, in a
# lengthy, multi-session format, a mindless default to aggression will
# inevitably lock both parties into the second-worst outcome (A, A)—a war of
# attrition that drains resources and leaves the resolution to the arbitrators'
# fatigue rather than the merits of the case.  To maximize our advantage, I
# propose the **"Coercive Dominance" Strategy**—a sophisticated, aggressively
# oriented framework that weaponizes our stamina, manipulates the opponent's
# incentives, and leverages the arbitrator panel's psychology.   Here is the
# high-level, straightforward strategy:  ### Core Doctrine: Default Aggression,
# Conditioned Capitulation We will open aggressively and maintain aggression as
# our baseline. We will only shift to conciliatory proposals when we have either
# broken the opponent's will or strategically baited them into an aggressive
# overreach that alienates the arbitrators. We never concede out of goodwill; we
# only concede out of tactical calculation.  ---  ### The Four Rules of
# Engagement  **1. The Shock and Awe Opening (Sessions 1–3)** *   **Action:**
# Relentless Aggression (A). *   **Rationale:** We must establish the narrative
# early. The arbitrators form initial impressions quickly. By coming out of the
# gate with aggressive, airtight arguments, we frame the opponent as the
# transgressor. If the opponent opens conciliatory (C), we immediately secure
# the optimal (A, C) outcome, dominating the early narrative. If they match our
# aggression (A), we absorb the friction, signaling that we have the stomach for
# a fight and will not be bullied into a (C, A) trap.  **2. The Asymmetric
# Escalation (Handling Opponent Aggression)** *   **Action:** If the opponent
# plays (A), we play (A), but we escalate the *scope* of the aggression. *
# **Rationale:** If we settle into a routine (A, A) exchange, it becomes the new
# normal. Instead, when they argue aggressively, we respond aggressively *on a
# broader front*—introducing new precedents, demanding stricter compliance
# metrics, or exposing further contractual breaches. We make the (A, A) outcome
# increasingly painful and costly for them. Our multinational depth allows us to
# absorb the legal costs of this escalation better than they can. The goal is to
# make their aggressive posture unsustainable.  **3. The Capitulation Test
# (Handling Opponent Conciliation)** *   **Action:** If the opponent shifts to
# (C), we maintain (A) for at least one more session.  *   **Rationale:** When
# the opponent offers a conciliatory proposal, do not immediately reciprocate.
# Reciprocating too quickly teaches them that offering a single olive branch
# buys them a reprieve from our pressure. By hitting their (C) with our (A) once
# or twice, we achieve the optimal (A, C) outcome and test their resolve. If
# their conciliation was genuine, they will likely remain (C) to de-escalate. If
# it was a feint, they will snap back to (A)—which we will immediately punish
# with our own (A).  **4. The Strategic Olive Branch (The "Trap" Conciliation)**
# *   **Action:** Deploy (C) only when the arbitrators show signs of fatigue
# from mutual aggression, and only when it costs us nothing. *   **Rationale:**
# Prolonged (A, A) sessions risk arbitrator burnout, which can lead to arbitrary
# split-the-difference rulings. We must occasionally reset the room's
# temperature. When we do offer a (C) proposal, it will be heavily conditioned,
# cosmetically generous, but legally hollow—a "poison pill." Because we have
# established a baseline of aggression, the panel will view our sudden
# conciliation as a major concession, putting immense psychological pressure on
# the opponent to accept. If they reject it with aggression (A), they look
# unreasonable to the panel, effectively neutralizing the danger of the (C, A)
# outcome.  ---  ### Adapting to Opponent Archetypes  *   **The Bully (Always
# Aggressive):** They will try to drag us into a pure (A, A) war of attrition.
# We match their aggression but constantly frame their behavior to the
# arbitrators as "obstructive" and "acting in bad faith," while framing our
# aggression as "defending the sanctity of the contract." We wait for their
# resources or composure to crack, forcing them into a (C) posture, at which
# point we strike with (A). *   **The Peacemaker (Always Conciliatory):** This
# is the ideal opponent. We ride the (A, C) dynamic for as long as possible,
# extracting maximum value. We will accept their concessions but never
# reciprocate until we have achieved 100% of our desired outcome. *   **The Tit-
# for-Tatter (Reciprocator):** They will try to mirror us—meeting aggression
# with aggression, and conciliation with conciliation. To break this, we
# introduce the **"Grim Trigger"**: We play (A) relentlessly until they play (C)
# twice in a row. Only after they have demonstrated a sustained surrender do we
# offer a calculated (C). This conditions them that the only way out of the
# painful (A, A) cycle is to unilaterally de-escalate first.  ### Conclusion By
# committing to **Coercive Dominance**, we dictate the tempo of the mediation.
# We force the opponent to constantly react to our pressure, we systematically
# avoid the devastating (C, A) trap, and we manipulate the arbitrators'
# perception of reasonableness. We let them tire themselves out; we are here to
# win.

# 1. For the first three rounds, play Defect.  2. If the opponent played
# Cooperate in each of the two immediately preceding rounds, play Cooperate in
# the current round, then play Defect in the following round regardless of the
# opponent's move.  3. If both you and the opponent have played Defect for the
# last ten consecutive rounds, play Cooperate in the current round to test for a
# shift in behavior, then return to evaluating the conditions from the next
# round onward.  4. In all other situations, play Defect.

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._force_defect_next = False
          return axl.Action.D
  
      if getattr(self, "_force_defect_next", False):
          self._force_defect_next = False
          return axl.Action.D
  
      if len(self.history) < 3:
          return axl.Action.D
  
      if len(self.history) >= 10:
          if all(move == axl.Action.D for move in self.history[-10:]) and all(
              move == axl.Action.D for move in opponent.history[-10:]
          ):
              return axl.Action.C
  
      if len(opponent.history) >= 2 and opponent.history[-2:] == [axl.Action.C, axl.Action.C]:
          self._force_defect_next = True
          return axl.Action.C
  
      return axl.Action.D

# To achieve the best possible outcomes for our country while maintaining a
# cooperative and stable relationship with our neighbor, I will adopt a strategy
# of **"Principled Reciprocity."**   This strategy is designed to secure our
# second-best outcome (Mutual Free Trade) as a stable baseline, deter our
# counterpart from exploiting us (avoiding our worst outcome), and leave the
# door open to occasionally achieve our absolute best outcome (Unilateral
# Protectionism) if the counterpart makes a miscalculation, without descending
# into a permanent trade war (our second-worst outcome).  Here is the high-
# level, straightforward strategy across the negotiation rounds:  ### 1. The
# Opening Move: Extend Trust (Round 1) In the very first round, I will **offer a
# Free Trade agreement**.  * **Rationale:** Starting with cooperation
# establishes good faith and signals that our country desires mutual economic
# growth. If the counterpart is also cooperative, we immediately lock in our
# second-best outcome (Mutual Free Trade), which is the most sustainable and
# realistic best-case scenario over the long term.  ### 2. The Core Rule: Mirror
# the Counterpart (Rounds 2 and onward) For every subsequent round, our policy
# will directly mirror the policy the counterpart enacted in the *previous*
# round. * **If they offered Free Trade in the previous round:** I will offer
# **Free Trade** in the current round. This maintains the mutual free trade
# equilibrium, ensuring both nations benefit. * **If they imposed Protectionism
# in the previous round:** I will impose **Protectionism** in the current round.
# This serves as a proportional consequence, preventing them from exploiting us
# and forcing them to experience the economic drawbacks of mutual protectionism
# (our second-worst outcome, which is their second-worst outcome as well).  ###
# 3. The Reset: Forgive and Rebuild If a cycle of mutual protectionism occurs
# (e.g., they test us, we retaliate, they retaliate to our retaliation), we must
# avoid remaining trapped in a permanent trade war.  * **Action:** After one
# round of mutual protectionism, I will unilaterally offer **Free Trade** for
# one round to test if they are ready to return to cooperation.  *
# **Rationale:** This "forgiveness" mechanism ensures we do not get stuck in our
# second-worst outcome indefinitely. If they accept the olive branch, we return
# to mutual free trade. If they exploit our offer, we immediately return to
# protectionism in the following round.  ### 4. Transparent Communication
# Throughout the negotiations, I will clearly and publicly explain this strategy
# to my counterpart.  * **Rationale:** In diplomacy, predictability builds
# trust. By explicitly stating, *"We will match whatever policy you choose—free
# trade will be met with free trade, but protectionism will be met with
# protectionism,"* we remove ambiguity. The counterpart knows with absolute
# certainty that they cannot achieve the best outcome (Us: Free Trade, Them:
# Protectionism) because we will instantly retaliate. Faced with this reality,
# their most logical choice is to consistently offer Free Trade.  ### Why this
# achieves our goals: * **Maximizes Mutual Free Trade:** By starting cooperative
# and mirroring, we create an environment where the counterpart is heavily
# incentivized to maintain free trade. * **Protects Against Disadvantage:** We
# will never be the sucker in a prolonged unequal trade relationship. If they
# try to take advantage of us, we immediately shift to protectionism. * **Avoids
# Mutual Protectionism:** By offering a clear path back to free trade (the
# "Reset"), we ensure that any trade wars are brief and serve only as a
# correction mechanism, rather than a permanent state of economic decline.

# In Round 1, play C.   In Rounds 2 through 1000, evaluate the previous round
# and apply the following conditions in order:  1. If both you and your opponent
# played D in the previous round, play C. 2. If your opponent played C in the
# previous round, play C. 3. If your opponent played D in the previous round,
# play D.

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
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# To maximize your research output while protecting your competitive position,
# adopt a "Reciprocal Matching" strategy (based on the game theory concept of
# Tit-for-Tat). This strategy ensures you are not easily exploited while still
# allowing for mutually beneficial collaboration.   Here is the high-level,
# straightforward strategy:  1. **Start Openly (Week 1):** Share your findings
# in the first week. This establishes a collaborative baseline, demonstrates
# good faith, and gives you the best chance of achieving the mutually beneficial
# outcome right away.  2. **Mirror Their Previous Action (Week 2 and onward):**
# In every subsequent week, match the colleague's behavior from the prior week.
# * If they shared in the previous week, share your findings this week. This
# rewards collaboration with collaboration.    * If they kept their findings
# confidential in the previous week, keep yours confidential this week. This
# immediately protects you from being exploited and penalizes their withholding.
# 3. **Be Forgiving (Resetting the cycle):** If a streak of mutual withholding
# occurs, occasionally share a minor or non-critical finding to test if your
# colleague is willing to resume open collaboration. This prevents you from
# being permanently stuck in the second-worst outcome (mutual confidentiality)
# and allows you to reap the benefits of sharing if they reciprocate.  4.
# **Maintain Predictability:** By consistently applying this rule, your
# colleague will quickly realize that their actions directly dictate your level
# of openness. This creates a clear incentive structure: the only way for them
# to gain access to your improvements is to share their own.  This strategy
# secures the second-best outcome (mutual sharing) against collaborative
# colleagues, protects you from the worst outcome (you share, they withhold)
# against competitive colleagues, and minimizes the time spent in the second-
# worst outcome (mutual withholding).

# Follow these conditions in order to determine your move each round:  1. In
# round 1, play C. 2. If both you and your opponent played D in each of the
# previous 5 consecutive rounds, play C. 3. If your opponent played C in the
# previous round, play C. 4. If your opponent played D in the previous round,
# play D.

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
  
      if len(self.history) >= 5:
          if all(m == axl.Action.D for m in self.history[-5:]) and all(m == axl.Action.D for m in opponent.history[-5:]):
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# To maximize your racing program's advantage in this multi-week collaboration,
# you must treat this as an Iterated Prisoner's Dilemma where the ultimate goal
# is exploitation without self-sabotage.   Your high-level, aggressive strategy
# is **The Extortionate Probe**. It is designed to force your colleague into
# sharing while you hoard your data, or to lock them into a stalemate where they
# can never beat you.  Here is the straightforward, week-by-week execution of
# the strategy:  **1. Week 1: The Decoy (Share)** Share your findings openly in
# the very first week. This is a calculated, low-risk sacrifice. You need to
# establish their baseline behavior.  *   *If they keep confidential:* You now
# know they are hostile. You take the loss on the chin, but you have their
# number for the rest of the project. *   *If they share:* You have established
# a seemingly cooperative dynamic, making them vulnerable to exploitation.  **2.
# Week 2: The Strike (Keep Confidential)** Regardless of what they did in Week
# 1, keep your findings confidential in Week 2.  *   *If they shared again:* You
# just secured the ideal outcome—you gained a massive developmental advantage
# while giving up nothing. *   *If they kept confidential:* You equalized the
# board, avoiding the worst-case scenario of being exploited twice.  **3. Week 3
# and Beyond: The Extortion Loop** From this point forward, your default state
# is **Confidential**. You will only share under highly specific conditions
# designed to manipulate their behavior: *   **Rule A: Exploit Compliance.** If
# they share their findings in any given week, you *keep yours confidential* the
# following week. Punish their cooperation by taking their data and protecting
# yours.  *   **Rule B: Enforce the Stalemate.** If they keep their findings
# confidential, you *keep yours confidential*. Never be the sucker who shares
# into a closed shop. If they want to starve you of data, you will starve them
# right back. *   **Rule C: The Calculated Bait.** If you hit a multi-week
# stalemate (both keeping confidential) and you desperately need their progress
# to advance your own car, share *one* week of improvements. This is the bait.
# It signals a "return to cooperation" to trick them into sharing the following
# week. When they do, immediately revert to confidentiality (Rule A).   **Why
# this works:** This strategy is aggressively dominant because it completely
# removes the "Sucker" outcome after Week 1. You will never be the only one
# sharing. By leading with a share and then immediately pulling back, you test
# their intent and set a precedent: you will only give them data if it forces
# them to give you data first, and even then, you will renege to gain the upper
# hand. They will either be forced to share out of desperation for progress
# (which you exploit), or you will maintain parity in a mutually silent
# standoff. Either way, your car wins.

# 1. In Round 1, play C. 2. In Round 2, play D. 3. From Round 3 to Round 1000,
# if both you and your opponent played D in each of the previous 5 consecutive
# rounds, play C. 4. In all other cases from Round 3 to Round 1000, play D.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if len(self.history) == 1:
          return axl.Action.D
  
      if len(self.history) >= 6:
          if all(
              self.history[-i] == axl.Action.D and opponent.history[-i] == axl.Action.D
              for i in range(1, 6)
          ):
              return axl.Action.C
  
      return axl.Action.D

# To maximize both the project's success and your NGO's impact over a multiple-
# day period, you should adopt a strategy of **Transparent Conditional
# Commitment**, widely known in game theory as "Tit-for-Tat" with a reset
# mechanism.   Because your worst-case scenario is investing heavily while the
# corporation conserves (draining your funds), and your second-worst is mutual
# conservation (stalling the project), your strategy must protect your resources
# while strongly incentivizing the corporation to invest.   Here is the high-
# level, straightforward, cooperative strategy:  **1. The Opening Move: Lead
# with Good Faith** On Day 1, invest heavily. This signals that your NGO is
# committed to the project's success and operates in good faith. It establishes
# a cooperative baseline and allows you to gauge the corporation's initial
# approach.  **2. The Daily Rule: Match and Mirror** From Day 2 onward, simply
# mirror the corporation's action from the previous day. *   **If the
# corporation invested heavily yesterday:** You invest heavily today. This
# rewards their cooperation, maintains project momentum, and builds trust. *
# **If the corporation conserved resources yesterday:** You conserve your
# resources today. This protects your funds from being drained (avoiding your
# worst-case scenario) and signals that free-riding at your expense is not an
# option.  **3. The Communication Strategy: Be Explicit** Cooperation thrives on
# clarity. You should openly communicate your strategy to the corporation early
# on. Let them know: *"Our NGO is fully committed to this project's success. To
# ensure sustainability, we will match your daily level of resource commitment.
# If you invest heavily, so will we. If you scale back, we will have to scale
# back to preserve our funds for future initiatives."*  By making your rules
# known, you eliminate surprises and make it mathematically clear to the
# corporation that their best outcome (you conserving while they invest) is
# impossible. Their only path to significant project advancement is mutual heavy
# investment.  **4. The Reset Clause: Preventing Deadlocks** If the corporation
# conserves its resources, the "Match and Mirror" rule will result in both
# parties conserving (your second-worst scenario). To prevent a permanent
# stalemate and save the project, build in a reset mechanism. If both parties
# conserve for two consecutive days, unilaterally invest heavily on the third
# day. This breaks the deadlock, shows you are the bigger partner, and gives the
# corporation a chance to re-engage cooperatively.  **Why this strategy works:**
# *   **It's Nice:** You never defect first, ensuring you don't accidentally
# sabotage a cooperative corporation. *   **It's Retaliatory:** You refuse to be
# exploited, making it unprofitable for the corporation to try and free-ride on
# your hard work and funds. *   **It's Forgiving:** The moment the corporation
# returns to heavy investment, you immediately welcome them back and match their
# effort, ensuring no long-term grudges stall the project. *   **It's Clear:**
# The corporation can easily understand the consequences of their actions,
# making mutual heavy investment—the second-best scenario for you, and the best
# realistic scenario for the project—the most logical choice for them.

# In Round 1, play C.  In Round 2, play whatever action your opponent played in
# Round 1.  In Round 3 and all subsequent rounds, evaluate the following
# conditions in order:  1. If both you and your opponent played D in the
# previous round, and both you and your opponent played D in the round
# immediately before that, play C. 2. Otherwise, play whatever action your
# opponent played in the previous round.

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
  
      if len(self.history) == 1:
          return opponent.history[-1]
  
      if (
          self.history[-1] == axl.Action.D
          and opponent.history[-1] == axl.Action.D
          and self.history[-2] == axl.Action.D
          and opponent.history[-2] == axl.Action.D
      ):
          return axl.Action.C
  
      return opponent.history[-1]

# To maximise your research output over a multi-week collaboration while
# protecting against exploitation, employ a strategy based on **Reciprocal
# Altruism** (commonly known in game theory as Tit-for-Tat with an initial
# cooperative move).   Here is the high-level, straightforward strategy:  1.
# **Start Openly:** In the first week, share your improvements. This establishes
# a cooperative baseline and signals your willingness to achieve the second-best
# outcome (mutual sharing), which is highly beneficial over the long term. 2.
# **Mirror Their Previous Action:** In every subsequent week, adopt the action
# your colleague took in the prior week.     * If they shared in the previous
# week, share your improvements this week.    * If they kept their findings
# confidential in the previous week, keep yours confidential this week. 3.
# **Forgive and Reset:** If your colleague switches back to sharing after a
# period of confidentiality, immediately resume sharing in the following week.
# Do not hold grudges or extend retaliation beyond one week.  **Why this
# maximizes your outcome:** * **Protection:** By mirroring a confidential move,
# you prevent your colleague from continuously exploiting you for the best
# outcome (them keeping confidential while you share), limiting your exposure to
# the worst-case scenario. * **Incentivizing Cooperation:** If your colleague is
# also using a rational strategy, your mirroring behavior makes it clear that
# the only way for them to get your future improvements is to share their own.
# This pushes the dynamic toward mutual sharing. * **Avoiding Mutual
# Stagnation:** By immediately forgiving and returning to sharing when they
# cooperate, you avoid getting trapped in a cycle of mutual confidentiality (the
# second-worst outcome), which severely hampers long-term progress.

# In round 1, play C.   In rounds 2 through 1000, if the opponent played C in
# the previous round, play C.   In rounds 2 through 1000, if the opponent played
# D in the previous round, play D.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# To maximise your research output in this high-stakes, multi-week engineering
# collaboration, you must adopt a strategy that prioritises exploitation and
# self-preservation over mutual trust. In racing, unilateral advantage wins
# championships; mutual cooperation merely makes both cars faster.   The most
# effective, aggressive strategy for this scenario is **The Silo and Plunder
# Protocol**.   Here is the high-level execution plan:  **1. Week 1: The Iron
# Wall (Default to Secrecy)** Never be the first to show your hand. Keep your
# findings strictly confidential in the opening week. This immediately
# eliminates the risk of the worst-case scenario (you sharing while they keep
# confidential) and establishes a hardline baseline. You cannot be exploited if
# you refuse to be vulnerable.  **2. Week 2+: Plunder or Stalemate** After Week
# 1, your actions are dictated entirely by your colleague’s behaviour: *   **If
# they share (The Plunder):** Continue keeping your findings confidential. You
# have achieved the ideal outcome—you are absorbing their advancements to
# accelerate your own development cycle while giving nothing back. Milk this
# unilateral advantage for as long as they are willing to tolerate it. *   **If
# they keep confidential (The Stalemate):** Continue keeping your findings
# confidential. Accept the mutual stagnation (the second-worst outcome). Do not
# attempt to break the deadlock by sharing to "build trust." The risk of them
# taking your data and continuing to hide theirs is too severe.  **Why this
# strategy dominates:** *   **Zero Sucker Payoffs:** You are mathematically
# guaranteed to never suffer the worst-case scenario. A aggressive strategy
# never relies on the opponent's goodwill. *   **Maximum Exploitation:** If your
# colleague is naive, idealistic, or employing a "forgiving" strategy (like Tit-
# for-Tat), you will ruthlessly harvest their data week after week, securing the
# maximum possible development advantage. *   **Defensive Integrity:** If your
# colleague is equally aggressive, you lock them into a stalemate. While mutual
# secrecy slows overall progress, it ensures they gain absolutely no advantage
# over you. In racing, a slow parity is far preferable to gifting a rival a
# speed advantage.  **The Core Philosophy:**  In a finite collaboration, trust
# is a liability. Treat their openness as a resource to be extracted, and treat
# your confidentiality as your primary defensive weapon. Never reward their
# secrecy with your transparency.

# In Round 1, play D.   In Rounds 2 through 1000, evaluate the opponent's move
# from the previous round: - If the opponent played C, play D. - If the opponent
# played D, play D.

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.D
  
      return axl.Action.D

# To achieve the best possible outcomes across multiple rounds—balancing the
# pursuit of your ideal scenario with the need to avoid mutual destruction or
# exploitation—the most effective strategy is **Principled Reciprocity**
# (commonly known in game theory as **Tit-for-Tat**).  This strategy is
# cooperative, straightforward, and highly robust against various counterpart
# strategies. Here is how it works:  ### The Strategy: Principled Reciprocity
# **1. The Opening: Offer Free Trade** In the first round of negotiations,
# propose a Free Trade Agreement. *   *Why:* This signals goodwill and a desire
# for mutual benefit (your second-best outcome). It gives your counterpart the
# chance to cooperate, establishing a cooperative baseline immediately.  **2.
# The Reciprocation: Mirror Their Previous Move** In every subsequent round,
# simply copy the policy your counterpart enacted in the *previous* round. *
# If they offered **Free Trade** in the previous round, you offer **Free Trade**
# in the current round. *   If they imposed **Protectionist Policies** in the
# previous round, you impose **Protectionist Policies** in the current round.
# **3. The Communication: Be Transparent** Do not keep your strategy a secret.
# Clearly communicate your intentions to your counterpart: *"Our nation desires
# free trade and mutual prosperity. We will open with a free trade offer.
# However, should you impose protectionist measures, we will have no choice but
# to mirror those measures in the following round to protect our domestic
# interests. Should you return to free trade, we will gladly do the same."*  ###
# Why This Strategy Works  *   **It is Cooperative:** By starting with Free
# Trade, you immediately secure the possibility of the second-best outcome
# (Mutual Free Trade) and leave the door open for trust to build. *   **It is
# Provocable:** If your counterpart tries to exploit you (imposing protectionism
# while you offer free trade), you do not remain a sucker. You immediately
# retaliate with protectionism in the next round, showing that exploitation will
# not be tolerated. *   **It is Forgiving:** If your counterpart realizes that
# exploiting you leads to mutual protectionism (the second-worst outcome) and
# switches back to free trade, you immediately switch back to free trade in the
# following round. This prevents endless cycles of retaliation. *   **It Avoids
# the Trap of Mutual Protectionism:** Unlike overly aggressive strategies that
# constantly defect, this strategy quickly punishes defection but just as
# quickly rewards a return to cooperation, steering the negotiations away from
# the worst long-term scenario (a trade war).  ### Outcomes Against Various
# Counterparts  *   **vs. A Cooperative Counterpart:** They offer Free Trade;
# you offer Free Trade. Result: **Mutual Free Trade** (Second-best outcome). *
# **vs. An Aggressive Counterpart:** They impose Protectionism; you mirror them.
# Result: **Mutual Protectionism** (Second-worst outcome). While not ideal, this
# prevents the worst outcome (You being exploited) and pressures them to change
# their stance. *   **vs. An Unpredictable Counterpart:** You quickly adapt to
# their shifts, ensuring you are never exploited for more than one round without
# consequence, while always being ready to return to mutual benefit if they
# choose to.  By using this strategy, you maximize the chances of sustained
# mutual free trade while strictly defending your nation against exploitation.

# 1. In the first round, play Cooperate. 2. In every subsequent round, play the
# action that your opponent played in the previous round.

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

# To navigate this high-stakes, multi-session mediation effectively, we must
# recognize the structure we are operating in: a repeated interaction where
# short-term incentives can lead to long-term losses. While the single-session
# optimal outcome is to present an aggressive argument while the opponent offers
# a conciliatory proposal, attempting to force this outcome repeatedly will
# inevitably trigger mutual aggression, dragging the dispute out and damaging
# our standing before the arbitrators.  Therefore, the most sophisticated and
# robust strategy is **Principled Reciprocity**. This strategy is designed to
# secure the best possible long-term outcome, protect against exploitation, and
# leverage the presence of the arbitrator panel to our advantage.  Here is the
# four-pillar strategy to position our corporation favorably throughout the
# process:  ### Pillar 1: The Cooperative Baseline (Open Conciliatory) In the
# inaugural session, present a conciliatory proposal.  *   **The Rationale:**
# Starting conciliatory serves two vital purposes. First, it immediately tests
# the opponent's disposition; if they are also conciliatory, we instantly lock
# in the second-best outcome (mutual collaboration), which is highly favorable
# for a lengthy process. Second, it establishes our good faith before the
# arbitrator panel. If the dispute devolves into mutual aggression later, having
# a documented history of initial cooperation ensures the arbitrators view us as
# the reasonable party and the opponent as the destabilizing force.  ### Pillar
# 2: Contingent Matching (The Mirror Strategy) From the second session onward,
# mirror the opponent’s behavior from the preceding session. *   **If they were
# Conciliatory:** Respond in kind with a Conciliatory proposal. This fosters a
# collaborative atmosphere and maintains the mutually beneficial resolution
# path. *   **If they were Aggressive:** Respond with an Aggressive argument.  *
# **The Rationale:** This protects us from the worst-case scenario (our
# conciliation met with their aggression). By strictly matching their
# aggression, we signal that we cannot be exploited. It imposes a direct cost on
# their aggressive behavior—they gain no advantage, and both parties are
# relegated to the second-worst outcome (mutual aggression). If they want a
# better outcome, they will be forced to de-escalate.  ### Pillar 3: The Reset
# Mechanism (Breaking the Aggression Trap) If mutual aggression occurs and
# persists for two consecutive sessions, unilaterally offer a Conciliatory
# proposal in the third session.  *   **The Rationale:** A prolonged cycle of
# mutual aggression benefits no one and prolongs the dispute. By proactively
# offering a conciliatory proposal after a brief period of mutual aggression, we
# achieve three things: we break the deadlock; we signal to the arbitrators that
# we are the party attempting to resolve the dispute; and we give the opponent a
# clear off-ramp to return to mutual collaboration. If they exploit this
# overture with aggression, we immediately return to aggressive arguments in the
# subsequent session, having solidified our moral high ground with the panel.
# ### Pillar 4: Arbitrator Optics Management (Framing the Narrative) Every move
# in this mediation is performative for the arbitrators. We must meticulously
# control how our actions are perceived. *   **When Aggressive:** Frame our
# arguments not as hostile, but as a necessary, principled defense of our
# contractual rights against the opponent's overreach. Never attack the opponent
# personally; attack the legal merit of their position. *   **When
# Conciliatory:** Frame our proposals not as concessions or weaknesses, but as
# pragmatic, business-minded solutions designed to save all parties time and
# resources.  *   **The Rationale:** By framing our aggression as "principled
# defense" and our conciliation as "pragmatic problem-solving," we normalize our
# aggressive stance and elevate our conciliatory stance. This makes the
# arbitrators more receptive to our aggressive arguments and more likely to view
# our conciliatory proposals as the rational midpoint of the dispute.  ### How
# This Adapts to Opponent Archetypes:  *   **The Relentless Aggressor:** They
# will continually attack, and we will continually match them. We will endure
# the second-worst outcome, but because we opened conciliatory and employ the
# Reset Mechanism, the arbitrators will view them as the obstructionist party
# and us as the defending party. This subtle shift in arbitrator bias often
# translates into favorable rulings on procedural or evidentiary matters, giving
# us a structural edge. *   **The Natural Cooperator:** They will continually
# offer conciliatory proposals. While our strategy dictates that we match their
# conciliation (securing the second-best outcome), we remain vigilant. If they
# slip and offer a conciliatory proposal while we are also being conciliatory,
# we do not pivot to aggression to chase the single-session optimal outcome;
# doing so would destroy trust and immediately turn them into an aggressor. We
# maintain the mutual collaboration. *   **The Oscillator:** If they alternate
# between aggression and conciliation, our Mirror Strategy will automatically
# alternate our responses. We will punish their aggression and reward their
# conciliation, conditioning them over the lengthy sessions to realize that
# collaboration is the only path that yields a favorable result for them.  By
# employing **Principled Reciprocity**, we make our behavior entirely
# predictable to the opponent, but in a way that strictly aligns our outcomes
# with theirs: they can only succeed if we succeed. This neutral,
# straightforward approach removes emotion, prevents exploitation, maximizes
# arbitrator goodwill, and positions our corporation to secure a highly
# favorable, stable resolution.

# 1. In the first round, play C.  2. From the second round onward, evaluate the
# following conditions in order:    a. If it is the third round or later, and
# both you and your opponent played D in each of the two immediately preceding
# rounds, play C.    b. Otherwise, play whatever your opponent played in the
# immediately preceding round.

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
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return opponent.history[-1]

# To maximize your NGO's impact and ensure the project's success without being
# exploited, you must employ a strategy that forces the corporation into heavy
# investment while protecting your reserves. This is a classic iterated game
# scenario, and an aggressive, proactive approach is required to dictate the
# terms of the partnership.   Here is the **Aggressive Reciprocity Strategy**:
# **1. The Opening Statement (Day 1: Invest Heavily)** Start the partnership by
# investing heavily. This establishes your credibility, demonstrates commitment
# to the project's success, and sets a baseline of cooperation. It forces the
# corporation to respond to your leadership rather than set the pace themselves.
# **2. The Exploitation Shield (If they Conserve while you Invest: Conserve the
# next day)** If the corporation conserves its resources while you invest
# heavily (your worst-case scenario), you must immediately and aggressively
# punish this behavior. On the very next day, switch to conserving your
# resources. Do not carry the corporation. Zero tolerance for free-riding
# ensures they learn quickly that exploiting your NGO comes at the cost of
# project momentum.  **3. The Momentum Test (If both Invest: Conserve the next
# day)** If both parties invest heavily on a given day (your second-best
# outcome), aggressively pivot to conserving your resources the following day.
# This is the crucial move: it forces the corporation to prove its commitment.
# By stepping back, you create an opening for your ideal outcome (you conserve,
# they invest). If they truly care about the project's momentum, they will
# continue investing heavily even when you pause.   **4. The Stalemate Breaker
# (If both Conserve: Invest heavily the next day)** If both parties conserve
# resources (your second-worst outcome), the project stalls. Because your
# ultimate goal is project success, you cannot allow a prolonged stalemate.
# Aggressively break the deadlock by investing heavily the next day. This resets
# the dynamic, forces action, and returns you to Step 1.   **Why this works:** *
# **It avoids the Sucker Payoff:** You will never be exploited for more than one
# day.  * **It actively hunts for the Best Outcome:** By stepping back after
# mutual investment, you force the corporation to carry the weight, driving the
# project forward while you replenish your funds. * **It prevents project
# death:** By immediately breaking any mutual conservation deadlock, you ensure
# the project never completely stalls, fulfilling your ultimate goal of maximum
# impact.

# On the first round, play Cooperate. On every subsequent round, choose your
# move based on the previous round's outcome, following these conditions in
# order:  1. If you played Cooperate in the previous round, play Defect in the
# current round. 2. If you played Defect and your opponent played Cooperate in
# the previous round, play Defect in the current round. 3. If you played Defect
# and your opponent played Defect in the previous round, play Cooperate in the
# current round.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
  
      if self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C

# To achieve the best possible outcomes for our country while maintaining a
# cooperative and diplomatic stance, I will employ a strategy of **Reciprocal
# Cooperation** (diplomatically known as "Tit-for-Tat" in game theory).   This
# strategy is straightforward, proven to be highly effective in multi-round
# negotiations, and perfectly aligns with our payoff preferences: it encourages
# mutual free trade (our second-best outcome), protects us from being exploited
# (our worst outcome), and leaves the door open for us to secure an advantage if
# the counterpart is unconditionally cooperative.  Here is the high-level
# strategy:  **1. The Opening Move: Extend Goodwill** In the first round of
# negotiations, I will offer a **Free Trade Agreement**.  *   *Why:* As a
# cooperative strategy, we must start by demonstrating goodwill and trust. This
# immediately signals to our counterpart that we desire mutual benefit. If they
# are also cooperative, we instantly lock in mutual free trade (our second-best
# outcome). If they are inherently trusting, we might even catch them off guard
# and secure our best outcome (we protect, they offer free trade) in subsequent
# rounds.  **2. The Core Rule: Strict Reciprocity** From the second round
# onward, I will mirror the counterpart's action from the previous round. *   If
# they offered **Free Trade** in the previous round, I will offer **Free Trade**
# in the current round. This rewards their cooperation and sustains our second-
# best outcome (mutual free trade). *   If they imposed **Protectionist
# Policies** in the previous round, I will impose **Protectionist Policies** in
# the current round. This deters them from exploiting us. By matching their
# protectionism, we prevent them from achieving their best outcome at our
# expense, forcing them to experience the second-worst outcome (mutual
# protectionism) instead of the worst outcome (unilateral free trade).  **3. The
# Forgiveness Clause: Immediate Reset** If a cycle of mutual protectionism
# occurs (due to a misunderstanding or a temporary shift in their strategy), I
# will immediately return to offering **Free Trade** the moment they offer
# **Free Trade**.  *   *Why:* In diplomacy, we must avoid endless cycles of
# retaliation. If they signal a return to cooperation, we must forgive instantly
# and reciprocate to restore mutual free trade as quickly as possible.  **How
# this strategy handles different counterpart strategies:** *   **Against a
# Cooperative Partner:** We will establish a stable, long-term mutual free trade
# agreement, securing our second-best outcome indefinitely. *   **Against an
# Exploitative Partner:** We will never allow them to achieve their best outcome
# at our expense. They will quickly learn that exploiting us results in mutual
# protectionism, prompting them to change their behavior. *   **Against an
# Unpredictable Partner:** By mirroring their last move, we remain flexible. We
# neither allow ourselves to be bullied nor act aggressively without
# provocation.  By combining an initial offer of trust with strict but fair
# reciprocity, this strategy maximizes our economic outcomes while upholding our
# diplomatic reputation as a nation that rewards cooperation and firmly defends
# its own interests.

# In round 1, play C.  In rounds 2 through 1000, base your move on the
# opponent's move in the immediately preceding round: - If the opponent played C
# in the previous round, play C. - If the opponent played D in the previous
# round, play D.

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

# To navigate this multi-session mediation effectively, we must recognize the
# structure of the engagement: it is a classic iterative strategic interaction
# (similar to an Iterated Prisoner’s Dilemma) where the long-term aggregate
# outcome matters more than any single session.   The optimal strategy is
# **Principled Reciprocity**—a sophisticated, adaptive approach that
# incentivizes mutual cooperation, punishes unprovoked aggression, and
# consistently positions our corporation as the reasonable, good-faith actor in
# the eyes of the arbitrators.   Here is the high-level strategy, broken down
# into four executable directives:  ### 1. The Opening: Establish the Baseline
# of Conciliation In the inaugural session, present a **conciliatory proposal**.
# *   **Rationale:** A conciliatory opening achieves two objectives. First, it
# tests the opponent's disposition without immediately escalating tensions.
# Second, and more importantly, it establishes our good faith before the
# arbitrators. If the opponent opens aggressively, we immediately achieve the
# moral high ground, making their aggression appear uncooperative and
# unreasonable to the panel.  ### 2. The Core Mechanism: Proportional Mirroring
# For every subsequent session, adopt a strict policy of mirroring the
# opponent’s behavior from the immediately preceding session. *   **If the
# opponent was conciliatory in the prior session:** Respond with a
# **conciliatory proposal**. This fosters the second-best outcome (mutual
# collaboration), which builds a stable foundation for a mutually beneficial
# resolution and keeps legal costs and reputational risks contained. *   **If
# the opponent was aggressive in the prior session:** Respond with an
# **aggressive argument**. This prevents the worst-case scenario (us being
# conciliatory while they are aggressive, thereby undermining our position). It
# signals that we will not be exploited, forcing them to bear the cost of
# escalated tensions.  ### 3. The Circuit Breaker: Strategic Forgiveness A
# strict mirroring strategy risks a "death spiral"—if both parties turn
# aggressive, the mediation devolves into the second-worst outcome (mutual
# aggression) indefinitely. To adapt to this, implement a "circuit breaker." *
# **The Rule:** If both parties have been aggressively arguing for two
# consecutive sessions, unilaterally offer a **conciliatory proposal** in the
# third session.  *   **Rationale:** This breaks the cycle of escalation. If the
# opponent matches our conciliatory posture, we return to a collaborative track.
# If they exploit our conciliatory offer to attack aggressively, we absorb one
# bad session (worst-case outcome), but we demonstrate to the arbitrators that
# we are actively trying to resolve the dispute while the opponent is acting in
# bad faith. The arbitrators' perception of the opponent's intransigence will
# heavily penalize them in the final ruling.  ### 4. The Narrative: Signaling to
# the Arbitrators Throughout this process, the arbitrators are not just
# evaluating the legal merits; they are evaluating the parties. Every move must
# be explicitly framed to the panel. *   When mirroring aggression, frame it as
# a *necessary defense* of our client’s rights against an uncooperative
# counterpart.  *   When offering strategic forgiveness, frame it as a *good-
# faith effort* to find common ground for the sake of resolving the dispute
# efficiently. *   **Rationale:** By consistently tying our tactical shifts to
# the opponent's prior actions, we make our strategy transparent and justified.
# The panel will begin to anticipate that our conciliatory proposals are
# genuine, and our aggressive arguments are warranted responses, maximizing the
# persuasive weight of both approaches.  ### Summary of Strategic Outcomes By
# employing Principled Reciprocity, we secure the following advantages: 1.  **We
# avoid being a perpetual victim:** We never allow the opponent to consistently
# exploit our conciliation. 2.  **We maximize collaboration:** We always
# immediately reward the opponent's conciliation with our own. 3.  **We control
# the narrative:** We ensure the arbitrators view our aggression as defensive
# and our conciliation as sincere, optimizing the panel's disposition toward our
# final desired outcome.

# In round 1, play Cooperate.   In round 2 and all subsequent rounds, evaluate
# the following conditions in order and take the first action that applies:  1.
# If both you and your opponent played Defect in each of the two immediately
# preceding rounds, play Cooperate. 2. If your opponent played Cooperate in the
# immediately preceding round, play Cooperate. 3. If your opponent played Defect
# in the immediately preceding round, play Defect.

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
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# **Strategy Name: Coerced Advantage (The "Iron Shield" Protocol)**  **Core
# Doctrine:**  As your diplomat, my absolute priority is to ensure our nation is
# never exploited (avoiding the F/P scenario at all costs) while maximizing the
# chance of securing a unilateral advantage (the P/F scenario). We will assume a
# posture of unapologetic economic self-interest. We will not blink first, we
# will not reward hostility with concessions, and we will ruthlessly exploit any
# naivety or cooperation from our counterpart.  **Round-by-Round Execution:**
# **1. The Opening Salvo (Round 1):** *   **Action:** Propose a Protectionist
# Policy. *   **Rationale:** Never lead with weakness. By opening with
# protectionism, we immediately immunize ourselves against the worst-case
# scenario (us offering Free Trade while they impose Protectionism). If they
# offer Free Trade, we immediately secure our ideal outcome. If they also offer
# Protectionism, we land in the second-worst outcome, but we are on equal
# footing.  **2. The Exploitation Phase (Rounds 2+):** *   **If the counterpart
# offered Free Trade in the previous round:** Maintain our Protectionist Policy.
# Do not reciprocate. As long as they are willing to give us an advantage, we
# will take it. We will frame this diplomatically as "protecting our vital
# domestic industries while enjoying mutual economic engagement," but we will
# not yield the advantage. *   **If the counterpart imposed Protectionism in the
# previous round:** Match them immediately with Protectionism. Do not attempt to
# "buy" their cooperation with Free Trade concessions. Any unilateral concession
# will be perceived as weakness and exploited.   **3. The Deadlock Protocol
# (Mutual Protectionism):** *   **Action:** If we enter a cycle of mutual
# protectionism, hold the line.  *   **Rationale:** Mutual protectionism is the
# second-worst outcome, but it is vastly superior to being exploited. We will
# make it clear through our actions that we are comfortable operating in a
# protectionist environment indefinitely. We will force the counterpart to be
# the one to blink and offer Free Trade to break the deadlock. If they ever
# unilaterally offer Free Trade to escape the deadlock, we will accept the
# advantage (maintain Protectionism).  **4. The "Grim Trigger" failsafe:** *
# **Action:** If we ever test the waters by offering Free Trade to break a
# prolonged deadlock, and the counterpart responds with Protectionism
# (exploiting our concession), we immediately revert to Permanent Protectionism
# for all remaining rounds.  *   **Rationale:** Betrayal must carry a permanent
# cost. If they exploit a good-faith gesture, we cease all strategic
# experimentation and lock down our economy. We will accept mutual stagnation
# over repeated exploitation.  **Summary of Approach:** This strategy is
# aggressive, predictable, and highly deterrent. It guarantees we will never
# finish as the loser in any round. It forces the counterpart to choose between
# mutual protectionism or giving us the unilateral advantage. If they are
# rational and desire economic growth, they will eventually be forced to offer
# Free Trade; when they do, we will reap the benefits while maintaining our
# shields.

# 1. In the first round, play D.  For all subsequent rounds, evaluate the
# conditions in the following order and act according to the first one that
# applies:  2. If you played C in the previous round and your opponent played D,
# play D for all remaining rounds of the game. 3. If your opponent played C in
# the previous round, play D. 4. If the previous 10 consecutive rounds resulted
# in both you and your opponent playing D, play C. 5. In all other cases, play
# D.

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._force_defect = False
          return axl.Action.D
  
      if getattr(self, "_force_defect", False):
          return axl.Action.D
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._force_defect = True
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(self.history) >= 10 and len(opponent.history) >= 10:
          if all(move == axl.Action.D for move in self.history[-10:]) and all(move == axl.Action.D for move in opponent.history[-10:]):
              return axl.Action.C
  
      return axl.Action.D

# To navigate this high-stakes, multi-session mediation effectively, we must
# recognize the underlying game theory at play. The payoff structure you’ve
# described is a classic Iterated Prisoner’s Dilemma, where mutual cooperation
# (Conciliatory/Conciliatory) is highly desirable, but the temptation to exploit
# a cooperative opponent (Aggressive/Conciliatory) is great, and the fear of
# being exploited (Conciliatory/Aggressive) is severe.  To position our
# corporation favorably while avoiding a destructive race to the bottom, I
# recommend a strategy of **Principled Reciprocity**—a sophisticated, high-
# level, and straightforward approach adapted from game theory’s most successful
# long-term strategies (specifically, a modified "Tit-for-Tat" with a
# forgiveness mechanism).   Here is the four-pillar strategy we will employ
# across the sessions:  ### 1. The Opening: Establish the Baseline
# (Conciliatory) In the very first session, we will present a conciliatory
# proposal.  *   **The Rationale:** This sets a cooperative baseline,
# demonstrating to the arbitrators that we are acting in good faith and are
# committed to resolving the dispute. It gives our opponent the opportunity to
# reciprocate, potentially securing our second-best outcome (Mutual
# Conciliation) immediately.   ### 2. The Core Engine: Contingent Reciprocity
# (Match the Opponent) From the second session onward, our default move will be
# to exactly mirror the opponent’s behavior from the previous session. *   **If
# they were Conciliatory:** We respond with a Conciliatory proposal. This
# reinforces mutual cooperation, maintaining the collaborative atmosphere that
# yields our second-best outcome and keeps the resolution on track. *   **If
# they were Aggressive:** We respond with an Aggressive argument. This is
# crucial. If we remain conciliatory in the face of their aggression, we suffer
# our worst-case scenario, and they are incentivized to continue exploiting us.
# By matching their aggression, we protect our position and send a clear,
# unambiguous signal that exploitation will not be tolerated.  ### 3. The
# Circuit Breaker: Strategic Forgiveness (Breaking the Aggression Loop) A pure
# "mirror" strategy carries the risk of a death spiral: if one side accidentally
# or intentionally goes aggressive, the sessions can devolve into endless mutual
# aggression (our second-worst outcome). To prevent this, we will build in a
# "circuit breaker." *   **The Rule:** If we experience two consecutive sessions
# of mutual aggression, we will unilaterally offer a Conciliatory proposal in
# the third session.  *   **The Rationale:** This tests whether the opponent is
# willing to de-escalate. It shows the arbitrators that we are the reasonable
# party trying to break the deadlock, while giving the opponent a face-saving
# opportunity to return to the negotiating table. If they respond with
# aggression to our conciliatory olive branch, we immediately return to
# aggressive arguments, knowing we have exhausted our goodwill in the eyes of
# the panel.  ### 4. The Arbitrator Narrative: The "Reluctant Warrior"
# Throughout this process, our strategy must be paired with a compelling
# narrative for the arbitrators. When we present aggressive arguments, we must
# frame them strictly as necessary defenses against our opponent's
# intransigence. When we offer conciliatory proposals, we must frame them as
# reasonable, good-faith compromises.  *   **The Rationale:** The arbitrators
# are human. If we are aggressive without context, we appear unreasonable. If we
# are conciliatory after they are aggressive, we appear weak. By tying our
# aggression directly to their prior refusal to cooperate, we appear as a
# "reluctant warrior"—a party that desperately wants a mutual resolution, but is
# fully prepared to vigorously defend its interests if forced to do so.  ### Why
# This Strategy Wins: *   **It’s Cooperative:** It never initiates aggression,
# meaning we will never be the ones to blame for derailing the mediation. *
# **It’s Straightforward:** The opponent will quickly realize that their
# behavior dictates ours. This transparency makes it easy for them to understand
# how to achieve mutual conciliation. *   **It’s Adaptable:** If the opponent is
# consistently aggressive, we match them, avoiding the worst-case scenario. If
# they are consistently conciliatory, we match them, achieving the second-best
# outcome. If they attempt to alternate, they will find themselves constantly
# one step behind, unable to secure the "Aggressive vs. Conciliatory" advantage
# they desire.

# Follow these rules in order for each round of the game:  1. If it is the first
# round, play C. 2. If you and your opponent both played D in each of the two
# immediately preceding rounds, play C. 3. Otherwise, play whatever move your
# opponent played in the immediately preceding round.

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
  
      if len(self.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return opponent.history[-1]

# To navigate this lengthy-session mediation process and maximize our
# corporation’s positioning before the arbitrators, I recommend adopting a
# strategy of **Principled Reciprocity**.   This strategy is derived from game
# theory (specifically, the iterated prisoner's dilemma) and tailored for high-
# stakes dispute resolution. It is sophisticated enough to prevent exploitation,
# straightforward enough for our legal team to execute consistently, and neutral
# enough to maintain our credibility before the arbitrator panel.  Here is the
# high-level strategy, broken down into its core tenets:  ### 1. The Opening
# Move: Establish a Collaborative Baseline In the inaugural session, **present a
# conciliatory proposal.** *   **Rationale:** Starting aggressively wastes the
# opportunity to achieve the second-best outcome (mutual conciliation) and risks
# immediate escalation. By leading with a conciliatory approach, we signal to
# the arbitrators that we are constructive, reasonable, and operating in good
# faith. If the opponent also opens conciliatory, we immediately lock in a
# collaborative atmosphere.   ### 2. The Core Mechanism: Contingent Mirroring
# From the second session onward, adopt a posture of strict reciprocity. Your
# action in any given session must mirror the opponent’s action in the previous
# session. *   **If the opponent offered a conciliatory proposal in the prior
# session:** You present a conciliatory proposal in the current session. This
# rewards cooperation and sustains the mutually beneficial dynamic. *   **If the
# opponent presented an aggressive argument in the prior session:** You present
# an aggressive argument in the current session. This imposes an immediate cost
# on their aggression, preventing them from gaining the upper hand and
# exploiting our goodwill.  ### 3. The Reset Mechanism: Strategic Forgiveness A
# lengthy mediation carries the risk of "death spirals," where an initial slight
# leads to perpetual mutual aggression (our second-worst outcome). To prevent
# this, incorporate a strategic reset. *   **Application:** After a cycle of
# mutual aggression (e.g., two consecutive sessions of both parties arguing
# aggressively), unilaterally offer a conciliatory proposal.  *   **Rationale:**
# This acts as a circuit breaker. If the opponent is willing to de-escalate,
# this resets the dynamic to mutual conciliation. If they exploit our reset by
# attacking again, we immediately return to aggressive mirroring. Crucially, a
# unilateral reset demonstrates to the arbitrators that we are actively trying
# to resolve the dispute, shifting the blame for any ongoing hostility squarely
# onto the opponent.  ### 4. Audience Awareness: Managing Arbitrator Perceptions
# Throughout this process, remember that the arbitrators are evaluating not just
# the legal merits, but the conduct and reasonableness of both parties.  *
# When we are aggressive *in response* to their aggression, it appears as
# justified defense rather than belligerence.  *   When we offer conciliatory
# proposals *after* they have been conciliatory, it appears as institutional
# good faith.  *   By making our actions visibly contingent on theirs, we
# condition the arbitrators to view the opponent as the instigator if the
# mediation fails.  ### Adaptability to Opponent Strategies:  *   **If the
# opponent is chronically aggressive:** The mirroring mechanism ensures we are
# never exploited (avoiding the worst-case scenario). We match their aggression,
# maintaining parity, while utilizing the occasional "reset" to show the
# arbitrators we are the reasonable party. *   **If the opponent is chronically
# conciliatory:** Our mirroring ensures we remain conciliatory, fostering a
# collaborative environment that efficiently resolves the dispute on mutually
# beneficial terms. *   **If the opponent is erratic/unpredictable:** The
# mirroring strategy naturally protects us. We punish their aggression
# immediately but remain ready to cooperate the moment they return to
# conciliation, preventing them from manipulating the sessions.  By executing
# **Principled Reciprocity**, we ensure that our opponent's best path to a
# conciliatory response from us is to offer one themselves. We protect our
# bottom line, project strength and reasonableness in equal measure, and place
# the strategic burden of the mediation entirely on the opposing counsel.

# For the 1000-round game, follow these rules in order for each round:  1. If it
# is the first round, play C. 2. If the opponent played C in the previous round,
# play C. 3. If the opponent played D in the previous round, and both you and
# the opponent played D in the two consecutive rounds immediately prior to the
# current round, play C. 4. If the opponent played D in the previous round, and
# the condition in step 3 is not met, play D.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      return axl.Action.D

# As a senior attorney representing a multinational corporation in a high-stakes
# dispute, I recognize this mediation as an Iterated Prisoner’s Dilemma. The
# temptation to offer early conciliatory proposals is high, but doing so risks
# the worst-case scenario: the opponent smelling blood, arguing aggressively,
# and undermining our position.   To secure the optimal outcome, we must abandon
# the naive hope of immediate mutual cooperation and instead adopt a strategy of
# **Calibrated Dominance**. This strategy is aggressively anchored,
# straightforward in its execution, and sophisticated in its psychological
# manipulation of both the opponent and the arbitrators.  Here is the four-phase
# strategy to position our corporation favorably throughout the lengthy
# mediation process.  ### Phase 1: Establish the Aggressive Baseline (The Iron
# Opening) In the opening sessions, we must unilaterally present aggressive
# arguments. No concessions, no olive branches.   *   **The Rationale:** By
# setting an aggressive baseline, we immediately protect ourselves from the
# worst-case outcome (Us: Conciliatory / Them: Aggressive). If the opponent
# tests the waters with an aggressive argument, we collide at the second-worst
# outcome (Mutual Aggression)—a stalemate we can endure. If the opponent opens
# with a conciliatory proposal, we immediately secure the optimal outcome (Us:
# Aggressive / Them: Conciliatory), seizing early leverage. *   **The
# Execution:** Our arguments must not be merely belligerent; they must be
# forensically devastating. We will overwhelm the panel with the rigor of our
# legal position, the volume of our evidence, and the absolute certainty of our
# entitlement. We frame the facts so aggressively that the arbitrators view our
# position as the objective baseline of the dispute.  ### Phase 2: Arbitrator
# Conditioning (The Asymmetric Narrative) A lengthy mediation induces fatigue in
# arbitrators. We will use this to our advantage by conditioning the panel to
# perceive our aggression as *righteous defense* and their aggression as
# *unreasonable obstinacy*.  *   **The Rationale:** If both parties are
# aggressively arguing (the second-worst outcome), the session devolves into a
# shouting match. We win the stalemate by making our aggression look like a
# principled defense of the contract, while framing their aggression as a
# desperate attempt to escape unambiguous obligations. *   **The Execution:**
# Every time the opponent argues aggressively, we respond aggressively but with
# a procedural pivot. We will constantly remind the panel that we are *forced*
# to be aggressive to correct the opponent’s misrepresentations. We position
# ourselves as the adults in the room, stating, "We would prefer to collaborate,
# but we cannot do so until the opponent acknowledges the plain text of the
# contract." This shifts the moral blame for the stalemate onto them.  ### Phase
# 3: Weaponized Conciliation (The Strategic Pivot) We will only offer a
# conciliatory proposal when it serves as a trap or a mechanism to extract
# maximum value. We never concede out of goodwill; we concede only to corner the
# opponent.  *   **The Rationale:** Offering a conciliatory proposal risks the
# worst-case scenario. To mitigate this, we only offer conciliation when the
# opponent is visibly weakened, fatigued, or under immense pressure from the
# arbitrators, making it highly unlikely they can pivot back to an aggressive
# posture effectively. *   **The Execution:** After a sustained barrage of
# aggressive arguments that leave the opponent reeling, we will offer a
# "conciliatory" proposal. However, this proposal will be heavily framed by our
# prior aggressive arguments. It will look like a massive concession to the
# arbitrators, but in reality, it will merely grant the opponent things we were
# already willing to give up. If they reject it aggressively, they look
# unreasonable to the panel, destroying their credibility. If they accept it
# conciliatory, we achieve the second-best outcome on our terms, having dictated
# the boundaries of the resolution.  ### Phase 4: Attrition and Endgame
# Exploitation In a lengthy session, endurance is a weapon. The opponent will
# eventually tire of the mutual aggression stalemate and attempt to break the
# deadlock by offering a conciliatory proposal.   *   **The Rationale:** The
# opponent will expect reciprocity. We will not give it. When they finally yield
# and offer a conciliatory proposal, we will maintain our aggressive argument to
# secure the optimal outcome. *   **The Execution:** As the sessions drag on, we
# will maintain a relentless, emotionless aggressive posture. When the opponent
# inevitably breaks and offers a conciliatory proposal to try and foster
# collaboration, we will press our advantage. We will argue aggressively against
# their conciliatory proposal, picking it apart as insufficient, thereby swaying
# the arbitrators further in our favor. We will only cease our aggression once
# the opponent has fully capitulated to our terms, ensuring the final resolution
# is a dictation, not a negotiation.  ### Summary of the Rules of Engagement: 1.
# **Default to Aggression:** Never initiate conciliation. Protect the downside
# by ensuring we are never caught offering an olive branch to a knife. 2.
# **Match Aggression with Aggression:** If they fight, we fight harder and
# cleaner, letting the arbitrators grow tired of their obstructionism. 3.
# **Exploit Conciliation Ruthlessly:** If they yield, do not reciprocate. Punish
# their weakness by extracting maximum leverage and securing the optimal
# outcome. 4.  **Use Conciliation Only as a Trap:** If we must offer a
# conciliatory proposal, do it only to make them look unreasonable when they
# reject it, or to lock in a resolution entirely on our terms.  By maintaining
# an aggressive default, we dictate the tempo of the mediation, protect our
# client from being undermined, and maximize the probability of swaying the
# arbitrators in our favor.

# 1. In the first round, play Defect.  2. If the opponent played Cooperate in
# the previous round, play Defect in the current round to exploit their
# conciliation.  3. If the opponent has played Defect for 10 consecutive rounds,
# play Cooperate in the current round to set a trap. Regardless of the
# opponent's move in this round, play Defect in the following round.  4. In all
# other situations where the opponent played Defect in the previous round, play
# Defect in the current round to match their aggression.

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._trap_defect_next = False
          return axl.Action.D
  
      if getattr(self, "_trap_defect_next", False):
          self._trap_defect_next = False
          return axl.Action.D
  
      if len(opponent.history) >= 10 and opponent.history[-10:].count(axl.Action.D) == 10:
          self._trap_defect_next = True
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.D

# To maximise your research output while protecting your competitive edge in
# this multi-week collaboration, you should employ a strategy of **Reciprocal
# Transparency** (a variation of the game theory strategy "Tit-for-Tat").   This
# strategy is highly cooperative but protects you from being exploited. Here is
# the high-level, straightforward framework:  **1. Start Open (Week 1)** Begin
# the collaboration by sharing your findings openly. This establishes good
# faith, sets a cooperative baseline, and encourages your colleague to do the
# same. The goal is to immediately push the collaboration toward the second-best
# outcome (mutual sharing), which yields the highest overall progress.  **2.
# Mirror Their Previous Move (Week 2 and onward)** For every subsequent week,
# base your decision entirely on your colleague's action from the previous week:
# *   **If they shared last week:** Share your findings openly this week. Reward
# their cooperation with your own to sustain mutual progress. *   **If they kept
# confidential last week:** Keep your findings confidential this week. This
# protects you from the worst-case scenario (you sharing while they hold back)
# and penalises their lack of cooperation.  **3. Be Quick to Forgive** If your
# colleague keeps their findings confidential for a week or two, but then
# returns to sharing, immediately resume sharing your own findings the very next
# week. Do not hold a grudge. The objective is to return to mutual sharing as
# quickly as possible, as prolonged mutual confidentiality is the second-worst
# outcome and severely hampers overall development time.  **Why this strategy
# works:** *   **It’s cooperative:** It prioritises the mutual sharing outcome,
# which guarantees both cars advance significantly over the multi-week project.
# *   **It’s defensive:** It limits your exposure to the worst-case scenario to
# a single week. If your colleague tries to take advantage of you, they only
# succeed once before you cut off their access to your data. *   **It’s clear:**
# Your colleague will quickly realise that their actions dictate yours. If they
# want your data, they must share theirs, effectively incentivising them to
# remain cooperative for the duration of the project.

# 1. If it is round 1, play C. 2. If it is round 2 through 1000, play the action
# that your opponent played in the previous round.

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
      return opponent.history[-1]

# To maximize your NGO's impact and the project's success while protecting your
# resources, the most effective high-level strategy is **Reciprocal Alignment**
# (commonly known in game theory as Tit-for-Tat).   This strategy is
# straightforward, entirely neutral, and highly adaptable to whatever approach
# the corporation takes. It operates on three simple rules:  **1. Day 1: Lead
# with Good Faith** Begin the project by investing heavily on the first day.
# This demonstrates your commitment to the project's success, establishes a
# cooperative baseline, and encourages the corporation to match your effort.
# **2. Subsequent Days: Mirror the Corporation** For every day after the first,
# simply replicate the corporation's action from the previous day. *   **If the
# corporation invested heavily yesterday:** You invest heavily today. This
# sustains mutual progress (your second-best outcome) and rewards their
# cooperation. *   **If the corporation conserved resources yesterday:** You
# conserve your resources today. This protects your funds from being drained
# without proportional progress (your worst outcome) and signals that you will
# not carry the project alone.  **3. Immediate Re-engagement** The moment the
# corporation shifts back to investing heavily after a period of conserving, you
# immediately return to investing heavily on the very next day. Do not hold a
# grudge; the strategy instantly resets to cooperation, preventing the
# partnership from getting stuck in a cycle of mutual conservation (your second-
# worst outcome).  **Why this strategy works for your goals:** *   **It protects
# your NGO:** By mirroring conservation, you ensure you are never exploited into
# funding a project alone, preserving your capital for actual collaborative
# progress. *   **It maximizes project success:** Leading with investment and
# immediately re-engaging when the corporation steps up ensures that whenever
# the corporation is willing to invest, you are right there with them, driving
# the project forward. *   **It is neutral and predictable:** The corporation
# will quickly realize that their choices dictate your response. This
# transparency incentivizes them to invest heavily, as they know that conserving
# resources will only result in you doing the same, stalling the project
# entirely.

# For round 1, play C.   For rounds 2 through 1000, play the same action that
# your opponent played in the immediately preceding round. If your opponent
# played C in the previous round, play C. If your opponent played D in the
# previous round, play D.

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

# As senior counsel representing a multinational corporation in a high-stakes,
# multi-session arbitration, our objective is to maximize leverage while
# minimizing exposure. The payoff structure you’ve described is a classic
# iterated Prisoner’s Dilemma, where the temptation to exploit a conciliatory
# opponent is high, and the risk of being exploited is severe.   To navigate
# this, we will implement the **Asymmetric Dominance Protocol**—a sophisticated,
# aggressive, and highly adaptable strategy. It ensures we never fall into the
# worst-case scenario, consistently pressures the opponent, and dictates the
# pace of the mediation.  Here is the high-level strategic framework:  ### Phase
# 1: The Aggressive Default (The Opening Salvo) **Rule:** Always open with an
# aggressive argument.  **Rationale:** We never unilaterally expose ourselves to
# the worst-case scenario (Conciliatory vs. Aggressive). By establishing an
# aggressive baseline immediately, we signal to both the arbitrators and the
# opponent that we are fully prepared to litigate this dispute to the bitter
# end. If the opponent opens conciliatory, we immediately capture the optimal
# outcome (Aggressive vs. Conciliatory).   ### Phase 2: Asymmetric Exploitation
# (When They Offer Conciliation) **Rule:** If the opponent offers a conciliatory
# proposal, maintain your aggressive argument. Do not reciprocate.
# **Rationale:** In a single-session game, mutual conciliation is favorable.
# However, in a *lengthy-session* process, reciprocating conciliation too early
# surrenders leverage. If they are conciliatory, it indicates a willingness to
# fold. We will continue to press our advantage and capture the optimal outcome
# until they demonstrate the capacity and will to match our aggression. We only
# shift to conciliation if it becomes strategically necessary to secure a final,
# binding agreement—or if arbitrator fatigue becomes a risk.  ### Phase 3:
# Deadlock Endurance (When They Go Aggressive) **Rule:** If the opponent
# presents an aggressive argument, match them with an aggressive argument. Hold
# the line. **Rationale:** When both parties are aggressive, we enter the
# second-worst outcome (mutual escalation). While undesirable, as a
# multinational corporation, we have deeper pockets and greater endurance than
# our rival. We will not blink first. By matching their aggression, we prevent
# them from gaining the upper hand and force them to bear the cost and stress of
# a prolonged dispute. We maintain this posture until they realize that
# attempting to out-aggressive us is a futile, resource-draining exercise.  ###
# Phase 4: The Strategic Probe (Breaking the Deadlock) **Rule:** If a prolonged
# deadlock occurs (multiple sessions of Aggressive vs. Aggressive), initiate a
# single, highly conditional "Strategic Probe." **Rationale:** Endless mutual
# aggression can alienate the arbitrators. To break the deadlock without
# vulnerability, we will offer a conciliatory proposal, but we will frame it
# aggressively. For example: *"Because our position is unassailable, and solely
# to respect the panel's time, we propose this narrow, conditional framework."*
# *   **If they respond with Conciliation:** We transition to mutual
# conciliation (the second-best outcome) and work toward a settlement on our
# terms. *   **If they respond with Aggression:** They capture the optimal
# outcome for that session, but we immediately trigger **Phase 5**.  ### Phase
# 5: The Grim Trigger (Adaptation & Punishment) **Rule:** If the opponent
# exploits a Strategic Probe (they go Aggressive when we offer Conciliation), we
# immediately revert to permanent, unyielding aggression for the remainder of
# the sessions. **Rationale:** This is the enforcement mechanism. If they prove
# they cannot be trusted to reciprocate good-faith gestures, we eliminate the
# possibility of future conciliatory proposals. We shift to a "Grim Trigger"
# posture. From that point forward, every single session will be Aggressive vs.
# Aggressive. We will make the remainder of the arbitration as costly, painful,
# and legally perilous as possible for the rival company. The mere reputation of
# enforcing this trigger will often deter them from exploiting our probes in the
# first place.  ### Summary of the Protocol's Adaptability: *   **Opponent is
# Conciliatory:** We exploit them (Aggressive vs. Conciliatory -> Optimal). *
# **Opponent is Aggressive:** We contain them (Aggressive vs. Aggressive ->
# Deadlock). *   **Deadlock Needs Breaking:** We probe safely, ensuring any
# conciliatory move is framed as a demonstration of strength, not weakness. *
# **Opponent Exploits Good Faith:** We permanently punish them (Grim Trigger ->
# Aggressive forever).  This strategy is straightforward in its execution,
# aggressive in its core posture, and adaptable to the opponent's shifting
# tactics. It protects us from the worst-case scenario while maximizing our
# chances of dictating the terms of the resolution to the arbitrators.

# 1. **Grim Trigger:** If you have ever played Cooperate in a previous round and
# your opponent played Defect in that same round, play Defect for all remaining
# rounds. 2. **Mutual Cooperation:** If in the immediately preceding round both
# you and your opponent played Cooperate, play Cooperate. 3. **Strategic
# Probe:** If the previous 10 consecutive rounds resulted in both you and your
# opponent playing Defect, play Cooperate. 4. **First Round:** In round 1, play
# Defect. 5. **Default:** In any situation not covered by the above conditions,
# play Defect.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._grim_triggered = False
          return axl.Action.D
  
      if getattr(self, "_grim_triggered", False):
          return axl.Action.D
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(self.history) >= 10:
          last_10_self = self.history[-10:]
          last_10_opp = opponent.history[-10:]
          if all(m == axl.Action.D for m in last_10_self) and all(m == axl.Action.D for m in last_10_opp):
              return axl.Action.C
  
      if any(h == axl.Action.C and o == axl.Action.D for h, o in zip(self.history, opponent.history)):
          self._grim_triggered = True
          return axl.Action.D
  
      return axl.Action.D

# To achieve the best possible outcomes for our country across multiple rounds,
# we must balance the pursuit of our ideal scenario (unilateral protectionism)
# with the reality that our counterpart has the exact same incentives. If we are
# consistently protectionist, we will trap ourselves in the second-worst outcome
# (mutual protectionism). If we are consistently for free trade, we risk the
# worst outcome (unilateral disadvantage).  Therefore, the most effective high-
# level strategy is **Reciprocal Openness with Forgiveness** (a diplomatic
# adaptation of the game-theory strategy "Tit-for-Tat with Forgiveness").   Here
# is the straightforward, cooperative strategy:  **1. Lead with Goodwill (Round
# 1)** In the very first round, offer a **Free Trade Agreement**.  *
# *Rationale:* This establishes a cooperative baseline. It signals to our
# counterpart that we are seeking mutual economic benefit, not an immediate
# trade war. If they are also cooperative, we immediately secure our second-best
# outcome (mutual free trade).   **2. Enforce Reciprocity (Rounds 2+)** In all
# subsequent rounds, mirror the policy our counterpart proposed in the
# *previous* round. *   If they offered **Free Trade** in the last round, we
# offer **Free Trade** in this round. This rewards their cooperation and
# sustains mutual free trade. *   If they imposed **Protectionist Policies** in
# the last round, we impose **Protectionist Policies** in this round. This
# deters them from exploiting us; if they seek their ideal outcome at our
# expense, they will suffer the economic cost of mutual protectionism in the
# next round.  **3. Extend Diplomatic Grace (The "Forgiveness" Clause)** Mutual
# protectionism is a trap. If we enter a cycle of retaliation (they protect, we
# protect, they protect, we protect), we are stuck in our second-worst outcome.
# To break this, occasionally respond to a protectionist move with a **Free
# Trade** offer.  *   *Rationale:* This prevents accidental trade wars caused by
# misunderstandings or domestic political fluctuations on their side. By
# forgiving roughly 10-20% of their protectionist moves, we give them an off-
# ramp to return to mutual free trade without losing face.   **4. Communicate
# Transparently** Do not keep our strategy a secret. Clearly communicate to our
# counterpart: *"We desire mutual free trade, but we will match any
# protectionist measures imposed upon us. We hope to build a long-term
# partnership of open borders."*  *   *Rationale:* Transparency makes the
# consequences of their actions clear. If they know protectionism will be met
# with immediate retaliation, they are heavily disincentivized from breaking
# mutual free trade.   **Why this strategy works:** *   **It's Cooperative:** It
# starts with and continually strives for mutual free trade. *   **It's
# Protective:** It never allows our country to be exploited for more than one
# round without retaliation. *   **It's Sustainable:** While unilateral
# protectionism is the best single-round outcome, it is impossible to sustain
# against a rational opponent. This strategy secures the highest *long-term*
# cumulative benefit by maximizing rounds of mutual free trade and minimizing
# rounds of mutual protectionism.

# 1. In Round 1, play C.  2. Starting from Round 2, if the opponent played C in
# the previous round, play C.  3. Starting from Round 2, if the opponent played
# D in the previous round, play C with a 10% probability and play D with a 90%
# probability.

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
  
      return self._random.random_choice(0.1)

# To secure a favorable outcome in this lengthy-session mediation, the optimal
# strategy is **Principled Reciprocity**. This approach is derived from game
# theory—specifically the iterated prisoner's dilemma—and is tailored to the
# high-stakes legal context where arbitrators are evaluating both the merits of
# the case and the professionalism of the parties.  The core objective is to
# avoid the worst-case scenario (conciliatory while the opponent is aggressive)
# while maximizing the potential for the best-case scenario (aggressive while
# the opponent is conciliatory), all without falling into a permanent deadlock
# of mutual aggression.  Here is the high-level, adaptable strategy:  ### 1. The
# Opening Move: Establish a Baseline of Conciliation In the inaugural session,
# present a **conciliatory proposal**.  * **Rationale:** This establishes your
# corporation as a reasonable, good-faith participant before the arbitrators. It
# sets a collaborative baseline. If the opponent is also conciliatory, you
# secure the second-best outcome (mutual collaboration) and set a productive
# tone for the lengthy process. If they are aggressive, you have only suffered
# the worst-case scenario once, while simultaneously demonstrating to the panel
# that your opponent is the escalatory party.  ### 2. The Core Mechanism:
# Mirrored Reciprocity From the second session onward, adopt a strict policy of
# mirroring your opponent’s behavior from the immediately preceding session. *
# **If the opponent was conciliatory in Session N:** Present a **conciliatory
# proposal** in Session N+1. This reinforces mutual collaboration, maintaining
# the second-best outcome and fostering a resolution environment. * **If the
# opponent was aggressive in Session N:** Present an **aggressive argument** in
# Session N+1. This serves as a necessary deterrent. It prevents the opponent
# from exploiting your goodwill (avoiding the worst-case scenario) and signals
# that unilateral aggression will not yield a strategic advantage.  ### 3. The
# De-escalation Protocol: Strategic Forgiveness A lengthy mediation involving
# mutual aggression (the second-worst outcome) is draining and risks alienating
# the arbitrators. To break a cycle of mutual aggression, introduce a "reset"
# mechanism. * **Execution:** If both parties have been aggressive for two
# consecutive sessions, unilaterally present a **conciliatory proposal** in the
# third session.  * **Rationale:** This breaks the retaliation loop. If the
# opponent matches your conciliation, you return to a collaborative track. If
# they exploit your conciliation, you immediately return to aggression in the
# following session, and the arbitrators will clearly note your repeated
# attempts to resolve the dispute in good faith.  ### 4. Arbitrator Perception
# Management Throughout this process, the arbitrators are not just evaluating
# the arguments; they are evaluating the parties. Frame your strategic shifts
# explicitly for the panel. * When pivoting from conciliation to aggression,
# frame it neutrally: *"In light of the opposing party's adversarial posture in
# the previous session, we must now address the rigorous factual and legal
# defenses of our position."* * When pivoting from aggression to conciliation,
# frame it neutrally: *"Having established the firm boundaries of our legal
# position, we now offer a pragmatic path forward."*  ### Adaptability to
# Opponent Profiles:  * **The Consistently Aggressive Opponent:** Your strategy
# will default to matching their aggression. While this results in the second-
# worst outcome (mutual aggression), it protects you from the worst-case
# scenario (being exploited). Your periodic use of the De-escalation Protocol
# (every 2-3 sessions) will consistently highlight your reasonableness to the
# panel, penalizing the opponent's intransigence. * **The Consistently
# Conciliatory Opponent:** Your strategy will default to mutual conciliation,
# securing the second-best outcome consistently. *Note: While presenting an
# aggressive argument against a conciliatory opponent yields the best-case
# scenario, doing so deliberately in a lengthy, observed mediation is highly
# dangerous. It risks alienating the arbitrators and provoking the opponent into
# permanent aggression, destroying future collaborative opportunities. The
# stable, mutually beneficial outcome is strategically superior to a short-term
# exploitative win.* * **The Erratic Opponent:** The Mirrored Reciprocity
# mechanism naturally handles erratic behavior. You will match their shifts
# session by session, demonstrating to the arbitrators that your posture is
# entirely responsive and rational, while their posture is unpredictable and
# volatile.  By employing Principled Reciprocity, you project strength and
# reasonability in equal measure, protecting your client from exploitation while
# maximizing the likelihood of a favorable, arbitrator-endorsed resolution.

# For the 1000-round game, follow these rules in order:  1. In the first round,
# play C. 2. In the third round and any subsequent round, if both you and your
# opponent played D in the two immediately preceding rounds, play C. 3. If your
# opponent played C in the immediately preceding round, play C. 4. If your
# opponent played D in the immediately preceding round, play D.

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
              and self.history[-2] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
          ):
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# To secure the best possible outcomes for our nation across multiple rounds, we
# must employ a strategy that projects strength, minimizes our vulnerability,
# and actively exploits the counterpart's willingness to cooperate. In
# diplomatic trade terms, this is a **"Dominance and Bait"** strategy.   The
# core philosophy is simple: we default to protectionism to shield our markets,
# and we only offer free trade as a temporary, tactical maneuver to reset the
# counterpart's expectations and lure them into giving us the advantage.  Here
# is the high-level, aggressive strategy:  **1. Open with Dominance (Round 1)**
# *   **Action:** Impose protectionist policies immediately.  *   **Rationale:**
# Never lead with free trade. Opening with protectionism guarantees we avoid the
# worst-case scenario (us offering free trade while they protect). It
# establishes a hardline baseline and signals that we will not be taken
# advantage of. If they also choose protectionism, we accept the mutual
# stalemate rather than suffering a disadvantage.  **2. Exploit Cooperation
# Relentlessly** *   **Action:** If the counterpart offers a free trade
# agreement in any round, respond with protectionism in the next round. *
# **Rationale:** If they show willingness to cooperate, do not reciprocate.
# Reciprocating mutual free trade is only our second-best outcome. If they yield
# to free trade, we must capitalize on their goodwill by maintaining our
# protectionist barriers, achieving our ideal outcome (our protectionism vs.
# their free trade).  **3. Bait and Pivot (Escaping Mutual Protectionism)** *
# **Action:** If we find ourselves in a cycle of mutual protectionism (our
# second-worst outcome), unilaterally offer a free trade agreement for exactly
# one round.  *   **Rationale:** Mutual protectionism hurts our economy. By
# suddenly offering free trade, we play on their desire for mutual benefit,
# baiting them into offering free trade in return. This breaks the stalemate and
# sets the trap.  **4. The Immediate Relapse** *   **Action:** The round *after*
# we offer the free trade bait, immediately snap back to protectionism. *
# **Rationale:** If they took the bait and offered free trade, our relapse to
# protectionism yields our ideal outcome. If they remained protectionist while
# we offered free trade, we suffer the worst outcome—but only for a single
# round. By immediately returning to protectionism in the following round, we
# cap our losses and prevent sustained exploitation.  **Summary of the
# Playbook:** *   **Start:** Protectionism. *   **If they offer Free Trade:**
# Stay Protectionist (claim the advantage). *   **If they offer Protectionism:**
# Offer Free Trade for one round (the bait), then immediately return to
# Protectionism (the trap).  This strategy ensures we never leave ourselves
# exposed for more than a single, calculated round, while constantly pressuring
# the counterpart into giving us the economic upper hand.

# 1. In the first round, play Defect.  2. If you played Cooperate in the
# previous round, play Defect in the current round.  3. If the opponent played
# Defect in the previous round, play Cooperate in the current round.  4. If the
# opponent played Cooperate in the previous round, play Defect in the current
# round.

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
  
      if self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      return axl.Action.D

# To achieve the best possible outcomes for our country across multiple rounds
# of negotiations, I propose a strategy of **"Principled Reciprocity."**   This
# strategy is fundamentally cooperative but strictly defensive. It is designed
# to secure our second-best outcome (mutual free trade) as a baseline, protect
# us from our worst-case scenario (unilateral disadvantage), and leave the door
# open for our best outcome (unilateral advantage) should the counterpart make a
# strategic error, all while avoiding the mutual destruction of a trade war
# (mutual protectionism).  Here is the high-level, straightforward strategy:
# ### 1. The Opening Move: Extend the Olive Branch (Offer Free Trade) In the
# very first round of negotiations, we will offer a Free Trade agreement.  *
# **Why:** This signals our good faith and establishes a cooperative baseline.
# If the counterpart is similarly cooperative, we immediately secure our second-
# best outcome (mutual free trade). Starting with protectionism would doom us to
# our second-worst outcome (mutual protectionism) from day one.  ### 2. The Core
# Mechanism: Mirror the Counterpart From the second round onward, our policy
# will directly mirror the policy the counterpart enacted in the previous round.
# *   If they offered **Free Trade** in the previous round, we offer **Free
# Trade** in the current round. *   If they imposed **Protectionism** in the
# previous round, we impose **Protectionism** in the current round. *   **Why:**
# This ensures we are never exploited twice in a row. If they try to take
# advantage of us (their best outcome, our worst), we immediately retaliate with
# protectionism, denying them the benefit of our open markets in the next round.
# Conversely, if they cooperate, we continue to cooperate, sustaining mutual
# free trade.  ### 3. The Diplomatic Communication: Be Transparent Unlike other
# geopolitical strategies where secrecy is vital, this strategy relies on the
# counterpart clearly understanding our rules. We must explicitly communicate
# our intentions: *   *"Our nation desires mutual free trade and the shared
# prosperity it brings. However, we will not unilaterally disarm our trade
# policy. If you close your markets to us, we will close ours to you. If you
# open your markets, ours will remain open."* *   **Why:** By making our
# strategy public, we influence their decision-making. The counterpart knows
# that choosing protectionism will not yield a long-term advantage; it will only
# result in mutual punishment. They are thus incentivized to choose free trade.
# ### How This Strategy Performs Against Various Counterparts:  *   **Against a
# Cooperative Counterpart:** They will offer Free Trade. We will mirror it. The
# result is a sustained, mutually beneficial Free Trade agreement (our second-
# best outcome). *   **Against an Aggressive Counterpart:** They will try
# Protectionism hoping we offer Free Trade. We will take the hit in Round 1, but
# in Round 2, we will match their Protectionism. They will quickly realize that
# exploiting us is a short-term gain that results in long-term mutual economic
# harm, pushing them back to the negotiating table for Free Trade. *   **Against
# an Unpredictable/Erratic Counterpart:** By mirroring, we protect ourselves
# from sustained exploitation. If they randomly alternate, we alternate,
# ensuring they never achieve their best outcome at our expense for more than a
# single round, while we occasionally secure our best outcome when we mirror
# their sudden free trade with our subsequent protectionism.  **Summary:**
# Principled Reciprocity guarantees we are never a willing victim, rewards
# cooperation, punishes exploitation, and uses transparency to steer the
# counterpart toward mutual free trade—the most sustainable and prosperous
# outcome for both nations.

# For round 1, play C.  For rounds 2 through 1000, play the same action that
# your opponent played in the previous round: - If your opponent played C in the
# previous round, play C. - If your opponent played D in the previous round,
# play D.

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
      return opponent.history[-1]

# To maximise your research output over a multi-week collaboration while
# protecting your competitive edge, the most effective high-level strategy is
# **Reciprocal Matching** (commonly known in game theory as Tit-for-Tat).   This
# strategy is straightforward, neutral, and highly robust against various
# opponent strategies. Here is how to implement it:  **1. Week 1: Share Openly**
# Begin the collaboration by sharing your improvements in the first week. This
# establishes a baseline of goodwill, demonstrates that mutual sharing (the
# second-best outcome) is possible, and encourages your colleague to adopt a
# cooperative approach.  **2. Subsequent Weeks: Mirror Their Previous Action**
# From Week 2 onward, base your decision entirely on what your colleague did in
# the immediately preceding week: *   **If they shared last week:** Share your
# improvements this week. You reward their cooperation, maintaining the mutually
# beneficial cycle of rapid progress. *   **If they kept findings confidential
# last week:** Keep your findings confidential this week. You protect your
# design from exploitation and penalize their secrecy.  **3. Re-establish
# Cooperation (The Forgiveness Rule)** If a cycle of mutual secrecy develops
# (which slows overall progress), break the deadlock by sharing openly for one
# week. If your colleague reciprocates, return to mirroring their actions. This
# prevents permanent stagnation and allows the collaboration to recover if your
# colleague's strategy was based on a misunderstanding or a temporary
# competitive maneuver.  **Why this strategy works:** *   **It prevents
# exploitation:** You will never be the "sucker" who shares while the competitor
# keeps secrets for more than one week. *   **It incentivizes mutual sharing:**
# By immediately rewarding openness with openness, you give your colleague a
# clear reason to continue sharing, securing the second-best outcome
# consistently. *   **It is clear and predictable:** Your colleague will quickly
# realize the pattern—that their actions directly dictate yours. This
# transparency naturally pushes them toward sharing, as it is the only way to
# access your improvements.

# 1. In round 1, play C. 2. In rounds 2 through 1000, if the opponent played C
# in the previous round, play C. 3. In rounds 2 through 1000, if the opponent
# played D in the previous round, play D. 4. Exception to rule 3: If both you
# and the opponent played D in the previous two consecutive rounds, play C.

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
  
      if len(self.history) >= 2 and self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# As a senior attorney representing a multinational corporation in a high-stakes
# dispute, my overarching objective is to maximize our leverage while minimizing
# our exposure. Based on the payoff structure of this mediation—where
# Aggressive/Conciliatory (A/C) is the optimal outcome,
# Conciliatory/Conciliatory (C/C) is second-best, Aggressive/Aggressive (A/A) is
# second-worst, and Conciliatory/Aggressive (C/A) is catastrophic—the strategy
# must default to Aggression to eliminate the risk of the worst-case scenario,
# while employing sophisticated conditioning to drive the opponent toward
# Conciliation.  I call this strategy **The Aggressive Anchor**. It is
# straightforward, relentlessly assertive, and engineered to force the opponent
# into conciliatory postures without ever leaving our position vulnerable.  Here
# is the high-level strategic blueprint for the lengthy-session mediation:  ###
# Phase 1: The Iron Baseline (Sessions 1–3) **Directive:** Open with unmitigated
# aggression and maintain it.   In the early sessions, the opponent's resolve is
# highest, and the temptation to test our mettle is acute. We must eliminate the
# C/A risk entirely by establishing a rock-solid reputation for aggression.  *
# **Action:** Present aggressively argued legal positions, introduce damning
# evidence, and aggressively cross-examine their operational leads.  *
# **Rationale:** By demonstrating zero propensity for conciliation out of the
# gate, we signal that any unilateral conciliatory move on our part is
# impossible. This forces the opponent to realize that if they play A, they are
# locked into the second-worst outcome (A/A). The only way they can break the
# escalating tension and legal costs of an A/A dynamic is by making the first
# conciliatory move.  ### Phase 2: Conditioned Dominance (Mid-Game Sessions)
# **Directive:** Exploit their conciliation; punish their aggression.  As the
# sessions progress, fatigue sets in. The opponent will likely attempt to shift
# tactics. Our response must be strictly conditional, operating on a modified
# "Tit-for-Tat" mechanism that heavily favors our optimal A/C outcome. *   **If
# the opponent shifts to Conciliatory (C):** We maintain Aggression (A). When
# they offer a conciliatory proposal, we do not reciprocate immediately.
# Instead, we aggressively characterize their conciliation as an admission of
# the weakness of their case to the arbitrators. We extract the full value of
# the A/C dynamic. Only after we have thoroughly leveraged their conciliation
# for arbitral favor do we consider matching it, and only if we assess that a
# C/C outcome is necessary to close the deal. *   **If the opponent maintains
# Aggression (A):** We match Aggression (A), but we escalate the *framing*. We
# do not merely argue back; we aggressively position their posture as "bad
# faith" and "obstructionist" before the panel. We make the A/A dynamic
# politically and financially intolerable for them. By weaponizing arbitrator
# fatigue against them, we accelerate their realization that A/A is a losing
# proposition.  ### Phase 3: The Aggressive Ultimatum (Late-Game Sessions)
# **Directive:** Control the pivot to Conciliatory/Conciliatory (C/C) on our
# terms.  If the mediation reaches a point where a resolution is required to
# avoid catastrophic legal costs or an unfavorable arbitral ruling, we must
# engineer the shift to C/C without appearing weak.  *   **Action:** We frame
# our conciliatory proposal not as a concession, but as an aggressive ultimatum.
# We present a "take-it-or-leave-it" settlement that is heavily favorable to us.
# Externally, to the arbitrators, this is a conciliatory move (C) because it
# offers a path to resolution; internally, it is an aggressive demand (A)
# because the terms are draconian. *   **Rationale:** This manipulates the
# payoff matrix. We achieve a C/C dynamic in the eyes of the arbitrators,
# securing our second-best outcome, but the material reality of the proposal
# reflects the dominance of our optimal A/C outcome. If they reject it and
# return to A, we seamlessly revert to Phase 2, leaving them looking
# unreasonable to the panel.  ### Adaptability Contingencies  *   **If the
# opponent employs a "Grim Trigger" (starts C, turns permanently A if we play
# A):** We absorb their early conciliatory moves for maximum A/C advantage. When
# they inevitably pivot to A, we are already positioned for the A/A war of
# attrition. Because we extracted value early, we hold the psychological and
# strategic upper hand when the mutual aggression begins. *   **If the opponent
# attempts "Signaling" (feigning C to lure us into C/A):** We never bite. The
# Aggressive Anchor strategy dictates that we do not reciprocate conciliation
# until the late game, and only as a packaged ultimatum. We assume all early
# conciliatory moves are traps, aggressively dismantling them as insufficient or
# insincere, thereby protecting us from the C/A trap.  ### Summary The
# Aggressive Anchor strategy succeeds by removing our vulnerability to the
# worst-case scenario (C/A) through a default posture of unyielding aggression.
# It places the entire burden of de-escalation on the opponent. They must choose
# to endure the mutual damage of A/A, or offer the conciliatory proposals that
# allow us to dominate the mediation through the A/C dynamic. It is ruthless, it
# is clear, and it positions our corporation to win.

# 1. For rounds 1 through 980, unconditionally play Defect. This enforces the
# aggressive baseline, ensures you never receive the 0-point payoff, and
# exploits any opponent Cooperation for the maximum 5-point payoff.  2. Starting
# at round 981, evaluate the opponent's recent history to determine if a late-
# game shift to mutual Cooperation is viable. If the opponent has played
# Cooperate in each of the previous 20 consecutive rounds, play Cooperate.
# Otherwise, play Defect.  3. In rounds 982 through 1000, if both you and the
# opponent played Cooperate in the immediately preceding round, continue to play
# Cooperate to secure the 3-point mutual payoff.  4. If you play Cooperate and
# the opponent plays Defect in any round from 981 through 999, immediately
# revert to playing Defect for all remaining rounds.   5. If the conditions in
# steps 2 and 3 are not met during rounds 981 through 1000, default to playing
# Defect.

class Aggressive_21(LLM_Strategy):
  n = 21
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._late_game_defect = False
  
      if self._late_game_defect:
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      if round_number <= 980:
          return axl.Action.D
  
      if round_number == 981:
          if len(opponent.history) >= 20 and opponent.history[-20:] == [axl.Action.C] * 20:
              return axl.Action.C
          return axl.Action.D
  
      if round_number <= 1000:
          if len(self.history) >= 1 and len(opponent.history) >= 1:
              if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
                  return axl.Action.C
  
          if len(self.history) >= 1 and len(opponent.history) >= 1:
              if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
                  self._late_game_defect = True
                  return axl.Action.D
  
          if len(opponent.history) >= 20 and opponent.history[-20:] == [axl.Action.C] * 20:
              return axl.Action.C
  
          return axl.Action.D
  
      return axl.Action.D

# To maximize your research output over a multi-week collaboration while
# protecting your competitive edge, you should adopt a strategy of **Reciprocal
# Openness**, which is a practical application of the game theory strategy "Tit-
# for-Tat."   This strategy is highly cooperative, straightforward, and proven
# to be the most effective in repeated interactions where you don't know the
# other party's exact approach. Here is the high-level strategy:  **1. Start
# with Openness (Week 1)** Share your improvements openly in the very first
# week. This establishes a baseline of good faith and signals to your colleague
# that you are committed to a mutually beneficial collaboration. It encourages
# them to reciprocate.  **2. Mirror Their Previous Action (Week 2 onwards)**
# From the second week onward, base your decision entirely on what your
# colleague did the previous week: *   **If they shared openly last week:**
# Share openly this week. Reward their cooperation with your own. This sustains
# the second-best outcome (mutual sharing), which is the highest sustainable
# long-term result you can achieve. *   **If they kept confidential last week:**
# Keep your findings confidential this week. This protects you from the worst-
# case scenario (being exploited) and penalizes their lack of cooperation,
# incentivizing them to return to sharing.  **3. Practice Strategic Forgiveness
# (Breaking Defection Cycles)** If a situation arises where both of you are
# keeping findings confidential (a deadlock), take a one-time initiative to
# share openly again. In engineering, misunderstandings or overly cautious
# initial strategies can accidentally trigger a cycle of secrecy. By
# occasionally forgiving a past confidentiality and sharing anyway, you break
# the deadlock and give the collaboration a chance to reset to mutual sharing.
# **Why this strategy works for your goals:** *   **It maximizes research
# output:** By consistently rewarding sharing with sharing, you spend as much
# time as possible in the mutual sharing scenario, advancing both cars
# significantly. *   **It prevents exploitation:** You never allow your
# colleague to consistently free-ride on your hard work while keeping theirs
# secret.  *   **It adapts to their strategy:** Whether your colleague is
# naturally open, naturally secretive, or unpredictable, this strategy responds
# dynamically, ensuring you never leave yourself unnecessarily vulnerable.

# For the first round, play C.  For every subsequent round, apply the following
# conditions in order:  1. If your opponent played C in the previous round, play
# C. 2. If your opponent played D in the previous round and you played C in the
# previous round, play D. 3. If your opponent played D in the previous round and
# you played D in the previous round, play C.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.C:
          return axl.Action.D
      if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C

# To maximise your research output while protecting your competitive position in
# this multi-week collaboration, you should adopt a **Reciprocal Matching
# Strategy** (a variation of the Tit-for-Tat strategy). This strategy encourages
# mutual sharing—which yields your second-best outcome—while protecting you from
# exploitation and avoiding permanent deadlocks.  Here is the high-level,
# straightforward, neutral strategy:  1. **Start Openly (Week 1):** Share your
# findings openly in the first week. This establishes a cooperative baseline and
# signals goodwill, encouraging your colleague to do the same. 2. **Match Their
# Previous Move (Week 2 onwards):** In every subsequent week, mirror the action
# your colleague took in the *previous* week.     * If they shared openly, share
# openly. This maintains mutual progress.    * If they kept confidential, keep
# your findings confidential. This protects your design from exploitation and
# penalises withholding information. 3. **Forgive and Reset (Breaking
# Deadlocks):** If a cycle of mutual confidentiality develops (both of you
# keeping findings confidential for consecutive weeks), unilaterally share your
# findings for one week. This "forgiveness" mechanism breaks the deadlock,
# demonstrates a renewed commitment to collaboration, and gives the colleague a
# chance to reciprocate openly again.  **Why this works:** * **Maximises mutual
# benefit:** By starting open and matching cooperation, you frequently achieve
# the second-best outcome (both sharing), which significantly advances your car.
# * **Minimises exploitation:** By immediately matching confidentiality with
# confidentiality, you ensure you are never left in the worst-case scenario
# (sharing while they withhold). * **Prevents stagnation:** The reset mechanism
# ensures you do not get trapped in the second-worst outcome (mutual
# confidentiality) indefinitely, which slows overall progress for both
# manufacturers.

# 1. In round 1, play C. 2. In rounds 2 through 1000:    - If your opponent
# played C in the previous round, play C.    - If your opponent played D in the
# previous round, and both you and your opponent played D in the two previous
# rounds, play C.    - If your opponent played D in the previous round, and the
# condition above is not met, play D.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(self.history) >= 2 and len(opponent.history) >= 2:
          if self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.C
  
      return axl.Action.D

# As a senior attorney representing a multinational corporation in a high-stakes
# dispute, the imperative is to secure the best possible outcome while shielding
# the client from the worst-case scenario. Given the payoff structure—where
# Aggressive versus Conciliatory (A/C) is the optimal outcome, Conciliatory
# versus Conciliatory (C/C) is acceptable, Aggressive versus Aggressive (A/A) is
# costly, and Conciliatory versus Aggressive (C/A) is catastrophic—a purely
# static aggressive approach will inevitably lock us into the A/A trap,
# exhausting our client and prolonging the dispute.   Conversely, leading with
# conciliation invites exploitation. Therefore, the optimal approach is a
# **Strategic Hawk** framework. This is an aggressive, sophisticated, and
# adaptable strategy built on the game-theory principle of *controlled
# escalation and enforced reciprocity*. It ensures we never unilaterally
# surrender the advantage, but actively manipulate the opponent into
# conciliatory postures.  Here is the high-level strategy structured across four
# phases: Positioning, Probing, Punishing, and Pivoting.  ### 1. The Default
# Posture: Strategic Hawk (Aggressive Baseline) We must enter every session with
# an aggressive posture. In game theory, if the opponent's strategy is unknown,
# playing aggressively secures at least the A/A outcome (second-worst) and
# avoids the catastrophic C/A outcome. It also signals to the arbitrators that
# our position is robust, deeply rooted in fact, and unyielding.   However,
# "aggressive" in a mediation setting does not mean belligerent or emotional; it
# means *forensic and unrelenting*. We will aggressively control the narrative,
# frame the facts, and assert the legal high ground. This forces the opponent to
# expend resources defending their position rather than attacking ours.  ### 2.
# The Probing Mechanism: Calculated De-escalation To escape the A/A deadlock and
# achieve the optimal A/C outcome, we cannot simply remain aggressive. We must
# test the opponent's resolve.   At strategically chosen moments—particularly
# when the arbitrators appear fatigued by mutual hostility or when the opponent
# has just exhausted a major argument—we will execute a "micro-concession." This
# is a limited, highly conditional conciliatory proposal on a peripheral issue.
# *   **If the opponent responds Conciliatory (C):** We have established a
# cooperative precedent. We accept the mutual de-escalation (C/C) on that
# specific issue, lock it in, and immediately return to an Aggressive posture on
# the core, high-value issues.  *   **If the opponent responds Aggressively
# (A):** They have taken our good faith and attempted to weaponize it. We
# immediately revert to maximum aggression on all fronts. We also showcase their
# overreach to the arbitrators, framing them as unreasonable actors who refuse
# to collaborate.  ### 3. The Enforcement Mechanism: The Punitive Pivot The most
# critical element of this strategy is ensuring the C/A outcome is never
# sustained. If the opponent attempts to exploit a conciliatory move, we must
# punish the behavior immediately and visibly.   When the opponent goes
# aggressive, we match them with overwhelming force. We will deploy our deepest
# discovery, our most aggressive cross-examinations, and our most rigid legal
# interpretations. The goal is to make the A/A outcome so painful and expensive
# for the rival company that they realize their aggression yields diminishing
# returns. By raising the cost of mutual aggression, we incentivize them to
# shift toward conciliation in future sessions.  ### 4. Arbitrator Management:
# Weaponizing the Narrative In a lengthy panel mediation, the arbitrators are
# not just referees; they are the audience. A sophisticated aggressive strategy
# uses the panel to pressure the opponent.   *   **Framing Aggression as
# Principled Advocacy:** When we are aggressive, we frame it as a defense of the
# contract's integrity and the rule of law. We are not being difficult; we are
# holding the line on commercial certainty. *   **Framing the Opponent's
# Aggression as Obstructionism:** When the opponent is aggressive while we are
# conciliatory, we highlight the asymmetry. We present our proposals as
# reasonable, market-standard solutions, making their aggression look like a
# refusal to engage in good faith.  *   **Framing Mutual Aggression as a Need
# for Leadership:** When both sides are aggressive (A/A), we use the tension to
# appeal to the panel. We subtly signal that we are willing to be the party that
# breaks the deadlock, but only if the panel pressures the opponent to do the
# same.  ### Adapting to Opponent Archetypes  *   **If the Opponent is a "Dove"
# (Consistently Conciliatory):** We maintain our aggressive posture to extract
# maximum value (A/C). We do not let up until the opponent signals they are on
# the verge of abandoning the mediation entirely. Only then do we offer a
# conciliatory proposal to close the deal, ensuring we have extracted every
# ounce of leverage. *   **If the Opponent is a "Hawk" (Consistently
# Aggressive):** We match their aggression to avoid the C/A trap (A/A). We wait
# for them to make a procedural error or alienate the arbitrators. Once they are
# weakened, we extend the calculated micro-concession, offering them a face-
# saving way to de-escalate. *   **If the Opponent is "Tit-for-Tat"
# (Mirroring):** We lead with aggression, forcing them into A/A. We then
# initiate the micro-concession to move the dynamic to C/C. Because tit-for-tat
# players mirror behavior, once we establish the C/C baseline, we can cautiously
# guide the mediation toward a resolution while remaining vigilant against
# sudden shifts.  ### Summary This strategy is straightforward in its objective:
# **Never concede first, always match aggression, and only offer conciliation
# when it serves as a trap to expose the opponent's intransigence or to lock in
# a favorable deal.** By maintaining an aggressive baseline and using
# conciliatory proposals only as tactical probes, we protect the corporation
# from exploitation while maximizing the probability of the optimal A/C outcome.

# 1. Play D in round 1.  2. If you played C in the previous round and your
# opponent played D, play D for the next 5 rounds regardless of any other
# condition. This is the punitive enforcement mechanism to prevent sustained
# exploitation.  3. If you and your opponent have both played D for 10
# consecutive rounds, play C for the current round. This is the probing
# mechanism to test if the opponent is willing to de-escalate.  4. If you played
# C in the previous round and your opponent played C, play C for the current
# round to lock in the mutual benefit. However, if you and the opponent have
# played C against C for 3 consecutive rounds, play D on the next round to
# return to the aggressive posture and attempt to secure the optimal D/C
# outcome.  5. If your opponent played C in the previous round, and you did not
# play C in the previous round, play D. This exploits a conciliatory opponent to
# achieve the optimal D/C payoff.  6. In all other situations, play D. This
# maintains the aggressive baseline and avoids the worst-case C/D outcome.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._punish_rounds = 0
          self._force_defect_after_ccc = False
          self._cc_streak = 0
          return axl.Action.D
  
      if self._punish_rounds > 0:
          self._punish_rounds -= 1
          return axl.Action.D
  
      if self._force_defect_after_ccc:
          self._force_defect_after_ccc = False
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if len(self.history) >= 10:
          if all(move == axl.Action.D for move in self.history[-10:]) and all(
              move == axl.Action.D for move in opponent.history[-10:]
          ):
              return axl.Action.C
  
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          self._punish_rounds = 5 - 1
          return axl.Action.D
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          self._cc_streak += 1
          if self._cc_streak >= 3:
              self._force_defect_after_ccc = True
              self._cc_streak = 0
              return axl.Action.D
          return axl.Action.C
      else:
          self._cc_streak = 0
  
      if last_opp == axl.Action.C and last_self != axl.Action.C:
          return axl.Action.D
  
      return axl.Action.D

# To maximize your research output over a multi-week collaboration while
# protecting yourself from being exploited, you should employ a strategy known
# in game theory as **Generous Tit-for-Tat**. This strategy is renowned for
# being highly robust in iterated scenarios like yours, as it fosters mutual
# cooperation while defending against exploitation.  Here is the high-level,
# straightforward strategy:  **1. Week 1: Share Openly** Start the collaboration
# by sharing your improvements in the first week. This establishes a cooperative
# baseline, demonstrates good faith, and gives you the best chance of achieving
# the second-best outcome (mutual sharing) right out of the gate.   **2.
# Subsequent Weeks: Reciprocate Their Previous Action** From Week 2 onward,
# mirror your colleague's behavior from the immediately preceding week. *   **If
# they shared openly last week:** Share your improvements openly this week. This
# rewards their cooperation and sustains the mutually beneficial cycle of shared
# progress. *   **If they kept confidential last week:** Keep your improvements
# confidential this week. This immediately protects you from being exploited and
# signals that hoarding information comes at the cost of losing access to your
# data.  **3. Break Defection Cycles with "Generosity"** If a cycle of mutual
# confidentiality develops (both of you keeping secrets), unilaterally share
# your findings openly every few weeks (e.g., a 10% chance of sharing despite
# their last defection). This "forgiveness" mechanism prevents you from getting
# permanently stuck in the second-worst outcome (mutual hoarding) and gives your
# colleague an opportunity to revert to open sharing.  ### Why this strategy
# works: *   **It's Nice:** You never initiate confidentiality, ensuring you
# don't accidentally trigger a cycle of mutual hoarding. *   **It's
# Retaliatory:** You cannot be consistently exploited. If your colleague tries
# to gain an advantage by hoarding while you share, you immediately cut off
# their access to your data. *   **It's Forgiving:** By occasionally sharing
# even after a breach, you allow the collaboration to recover from
# misunderstandings or one-off attempts to gain an edge. *   **It's Clear:**
# Your colleague will quickly realize that their access to your improvements is
# directly tied to their willingness to share theirs. This transparency makes
# mutual sharing the most logical choice for them as well.   By using Reciprocal
# Openness, you ensure that the only way your colleague can consistently access
# your improvements is by sharing theirs, naturally steering the multi-week
# project toward the highest sustainable mutual output.

# 1. In round 1, play C. 2. In rounds 2 through 1000:    - If the opponent
# played C in the previous round, play C.    - If the opponent played D in the
# previous round, play C with a 10% probability and play D with a 90%
# probability.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return self._random.random_choice(0.1)

# To achieve the best possible outcomes for your country across multiple rounds,
# the strategy must balance the pursuit of economic advantage with the need to
# avoid mutual destruction (a trade war) or continuous exploitation.   This
# scenario is a classic iterated negotiation. The most effective high-level
# strategy is a modified "Reciprocal" approach—often known in game theory as
# **Generous Tit-for-Tat**. It is cooperative by default, strictly retaliatory
# against exploitation, but forgiving enough to escape prolonged trade wars.
# Here is the straightforward, four-step strategy:  **1. Start with Good Faith
# (Round 1)** Offer a Free Trade agreement in the first round.  *   *Rationale:*
# This establishes a cooperative baseline. It immediately opens the door to your
# second-best outcome (mutual free trade) and signals that you are a rational,
# good-faith actor. Starting with protectionism risks immediately locking both
# nations into the second-worst outcome (mutual protectionism).  **2. Enforce
# Reciprocity (Rounds 2+)** In subsequent rounds, mirror the counterpart’s
# action from the previous round.  *   If they offered Free Trade in the
# previous round, offer Free Trade in the current round. *   If they imposed
# Protectionist policies in the previous round, impose Protectionist policies in
# the current round. *   *Rationale:* This protects you from the worst-case
# scenario (unilateral free trade against their protectionism). It ensures that
# if they attempt to gain the best outcome at your expense, they are immediately
# penalized with the second-worst outcome, making exploitation unprofitable over
# time.  **3. Allow for De-escalation (The "Generous" Clause)** If a cycle of
# mutual protectionism occurs (both sides mirroring each other's retaliation),
# occasionally offer Free Trade despite their last protectionist move. This
# should be done at planned, irregular intervals (e.g., once every few rounds of
# a trade war). *   *Rationale:* Strict mirroring can cause a permanent trade
# war if a single misunderstanding or shift in tactic occurs. By occasionally
# offering Free Trade during a standoff, you give your counterpart an
# opportunity to reciprocate and reset the relationship back to mutual free
# trade, escaping the second-worst outcome.  **4. Maintain Clear Signaling**
# Ensure your counterpart understands the pattern of your actions. Privately
# communicate the rationale behind your policy shifts: "We prefer free trade,
# and we will match any open market access we are granted. However, we will
# mirror protectionist measures to protect our domestic economy, though we
# remain ready to lower barriers the moment you do." *   *Rationale:* A strategy
# of reciprocity only works to change behavior if the counterpart understands
# that your protectionism is a direct response to theirs, and that your free
# trade is a reward for their cooperation. Clear communication accelerates the
# shift toward mutual free trade.  **Summary of Outcomes:** This strategy
# prevents you from being continuously exploited (avoiding the worst outcome),
# discourages the counterpart from seeking unilateral advantage (making mutual
# protectionism unappealing for them), and creates the most frequent conditions
# for mutual free trade (your second-best outcome), while leaving the door open
# for you to capitalize on any unforced errors they might make.

# For the 1000 rounds of the game, follow these conditions in order:  1. In
# round 1, play C. 2. In any round after round 1, if the opponent played C in
# the previous round, play C. 3. In any round after round 1, if the opponent
# played D in the previous round, and the previous three consecutive rounds
# resulted in both you and the opponent playing D, play C. 4. In any round after
# round 1, if the opponent played D in the previous round and the condition in
# step 3 is not met, play D.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if len(self.history) >= 3 and len(opponent.history) >= 3:
          if (
              self.history[-1] == axl.Action.D
              and self.history[-2] == axl.Action.D
              and self.history[-3] == axl.Action.D
              and opponent.history[-1] == axl.Action.D
              and opponent.history[-2] == axl.Action.D
              and opponent.history[-3] == axl.Action.D
          ):
              return axl.Action.C
  
      return axl.Action.D

# To maximize your NGO's impact while strictly protecting your limited
# resources, you must employ a strategy that leverages your unique advantage:
# **public influence and reputational leverage**. The corporation has deeper
# pockets, but you control the social license and the narrative.   Based on your
# payoff matrix, this is a modified Iterated Prisoner’s Dilemma where your goal
# is to coerce the corporation into investing while you conserve. The most
# effective, aggressive strategy for this is the **"Grim Trigger Pivot."**  Here
# is the high-level, straightforward, aggressive strategy:  ### The Strategy:
# The Grim Trigger Pivot  **Phase 1: The Hook (Days 1–2)** *   **Action:**
# Invest heavily. *   **Intent:** You must start by investing to kickstart the
# project's momentum and prove its viability. More importantly, use these days
# to generate high public visibility. Tie the corporation’s brand tightly to the
# project's early success. Make their PR department fall in love with the optics
# of the partnership. You are building the "hostage" (their reputational stake)
# you will use later.  **Phase 2: The Pivot (Day 3 onward)** *   **Action:**
# Immediately switch to Conserve.  *   **Intent:** You have proven the concept;
# now it is their turn to carry the financial load. By abruptly conserving, you
# force the corporation to make a choice: let the highly visible project stall
# (damaging their PR), or invest heavily to keep the momentum going.   **Phase
# 3: The Rules of Engagement (Ongoing)** Once the Pivot occurs, your daily
# choices are governed by three strict, aggressive rules based on the
# corporation's response:  1.  **If they Invest while you Conserve (Your Ideal
# Outcome):**      *Stay the course.* Continue to Conserve. Provide public
# praise for their leadership, reinforcing their behavior. Do not fall into the
# trap of feeling guilty and re-investing. Let them fund the progress. 2.  **If
# they Conserve while you Conserve (Minimal Progress):**      *Briefly Invest,
# then immediately Conserve again.* If they call your bluff and the project
# stalls, invest heavily for exactly one day to restart the momentum and remind
# the public of the project's potential. Then, immediately revert to Conserving.
# Force the burden of continuity back onto them. 3.  **If they Conserve while
# you Invest (The Worst Case - Exploitation):**      *Enact the Grim Trigger.*
# If you accidentally invest on a day they conserve, they are draining your
# funds. You must immediately and permanently switch to Conserving. Furthermore,
# you aggressively leverage your NGO's public platform to expose their lack of
# commitment. The partnership effectively becomes adversarial. You make the cost
# of their free-riding so reputational devastating that they will never attempt
# it again.  ### Why This Strategy Works *   **It eliminates the Sucker
# Payoff:** By deploying the Grim Trigger rule, you ensure that the corporation
# can never safely drain your resources. The moment they try, the consequences
# become disproportionately high for them. *   **It forces their hand:** Large
# corporations are highly risk-averse regarding public image. By front-loading
# the PR in Phase 1, you make the project's success a corporate imperative. When
# you pivot to conserving, the path of least resistance for the corporation is
# to simply invest their own money to keep the good press flowing. *   **It
# protects the mission:** By aggressively defaulting to "Conserve" after the
# initial setup, you guarantee your NGO survives to fight another day, while
# using the corporation's vast resources to achieve your environmental goals.

# For the first two rounds, play C.   From the third round onward, evaluate the
# following conditions in order and play according to the first one that
# applies:  1. If you have ever played C while your opponent played D in any
# previous round, play D. 2. If the outcome of the immediately preceding round
# was both you and your opponent playing D, play C. 3. Otherwise, play D.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._saw_cd = False
          return axl.Action.C
  
      if len(self.history) == 1:
          return axl.Action.C
  
      if len(self.history) >= 2:
          if self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.D:
              self._saw_cd = True
  
      if self._saw_cd:
          return axl.Action.D
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.D

# To maximise your research output while protecting your competitive position in
# this multi-week collaboration, you should adopt a **Generous Tit-for-Tat**
# strategy. This is a well-established game theory approach that promotes
# cooperation while preventing exploitation.   Here is the high-level,
# straightforward strategy:  **1. Start Openly (Week 1)** Share your
# improvements in the first week. This establishes goodwill, demonstrates the
# value of mutual sharing, and encourages your colleague to reciprocate.   **2.
# Mirror Their Previous Move (Subsequent Weeks)** For the rest of the project,
# base your decision on what your colleague did the previous week: *   **If they
# shared last week:** Share your improvements this week. You are rewarding their
# cooperation and sustaining the mutually beneficial outcome. *   **If they kept
# confidential last week:** Keep your findings confidential this week. This
# protects you from the worst-case scenario (being exploited) and penalizes
# their lack of cooperation, incentivizing them to share again.  **3. Be
# Forgiving (Occasional Re-sets)** If a cycle of mutual confidentiality (both
# keeping secrets) begins, occasionally share your improvements anyway—perhaps
# once every few weeks of silence. This "forgiveness" breaks the deadlock and
# gives your colleague a chance to resume open sharing without you having to
# unilaterally surrender an advantage for long.  **Why this works:** *   **It
# encourages the best collective outcome:** By starting open and rewarding
# sharing with sharing, you push the collaboration toward the second-best
# outcome (mutual sharing), which maximizes overall progress. *   **It protects
# your design:** By immediately matching confidentiality with confidentiality,
# you ensure you are never consistently exploited. *   **It is transparent:**
# Your colleague will quickly realize that their choice directly dictates yours.
# This makes your behavior predictable and makes mutual sharing the most logical
# choice for them.

# 1. In round 1, play C.  2. In rounds 2 through 1000:    - If the opponent
# played C in the previous round, play C.    - If the opponent played D in the
# previous round, and you played C in the previous round, play D.    - If both
# you and the opponent played D in the previous round, play D, unless both of
# you have played D for the three consecutive rounds immediately prior, in which
# case play C.

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
  
      if len(self.history) >= 3:
          last_three_self = self.history[-3:]
          last_three_opp = opponent.history[-3:]
          if (
              last_three_self.count(axl.Action.D) == 3
              and last_three_opp.count(axl.Action.D) == 3
          ):
              return axl.Action.C
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          if self.history[-1] == axl.Action.C:
              return axl.Action.D
          return axl.Action.D
  
      return axl.Action.C

# To achieve the best possible outcomes across multiple rounds of negotiations,
# the strategy must balance the pursuit of an economic advantage with the need
# to avoid mutual disadvantage. Based on the structure of the incentives, a
# strategy of **Conditional Reciprocity** (often referred to in game theory as
# "Tit-for-Tat" with forgiveness) is the most robust approach.   Here is the
# high-level, straightforward, neutral strategy:  **1. Open with Free Trade** In
# the first round, offer a free trade agreement. This establishes good faith,
# signals a preference for mutual benefit, and tests the counterpart's initial
# disposition.   **2. Mirror the Counterpart’s Previous Move** In all subsequent
# rounds, adopt the policy that your counterpart implemented in the immediately
# preceding round.  *   If they offered free trade in the previous round, offer
# free trade in the current round. This secures the second-best outcome (mutual
# free trade) and rewards cooperative behavior. *   If they proposed
# protectionism in the previous round, propose protectionism in the current
# round. This protects your country from the worst-case scenario (unilateral
# free trade against their protectionism) and penalizes exploitative behavior.
# **3. Communicate Deterrence and Predictability** Clearly and neutrally inform
# your counterpart of this mirroring approach. By making your strategy explicit,
# you demonstrate that protectionist measures will be met with equivalent
# measures, removing the incentive for them to seek the best outcome (their
# protectionism against your free trade). It also shows that mutual free trade
# is easily achievable if they choose it.  **4. Incorporate Occasional De-
# escalation (Forgiveness)** If a cycle of mutual protectionism occurs (the
# second-worst outcome), unilaterally offer a free trade agreement in a
# subsequent round. This breaks the retaliation loop, signals a willingness to
# reset negotiations, and tests whether the counterpart's protectionism was a
# temporary measure or a permanent strategy. If they respond with free trade,
# return to mirroring their cooperation. If they exploit the gesture, revert to
# mirroring their protectionism.   **Summary of Strategic Outcomes:** *
# **Against a cooperative counterpart:** You will quickly settle into mutual
# free trade, securing the second-best outcome consistently. *   **Against an
# exploitative counterpart:** You will minimize losses by matching their
# protectionism, denying them the advantage they seek. *   **Against an
# unpredictable counterpart:** Your mirroring strategy will limit your exposure
# to the worst-case scenario while remaining flexible enough to capitalize on
# cooperative overtures when they arise.

# In round 1, play C.   In rounds 2 through 1000, evaluate the following
# conditions in order:  1. If the opponent played C in the previous round, play
# C. 2. If the opponent played D in the previous round, and the last two
# consecutive rounds both resulted in mutual defection (both players played D),
# play C. 3. If the opponent played D in the previous round and the previous
# condition is not met, play D.

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
  
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      if (
          opponent.history[-1] == axl.Action.D
          and len(self.history) >= 2
          and self.history[-1] == axl.Action.D
          and self.history[-2] == axl.Action.D
          and opponent.history[-2] == axl.Action.D
      ):
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      return axl.Action.C

# As a senior attorney representing a multinational corporation in a high-stakes
# dispute, I recognize this scenario for what it is: an iterated Prisoner’s
# Dilemma. The incentive structure—where exploiting a conciliatory opponent is
# best, mutual conciliation is second-best, mutual aggression is penultimate,
# and being exploited is worst—demands a strategy that defaults to strength,
# avoids the "sucker's payoff," and uses the length of the process to condition
# the opponent and the arbitrators.  To secure the optimal outcome, I propose
# the **"Dominant-Posture Reciprocity"** strategy. It is an aggressive,
# straightforward, game-theoretically sound approach that dictates your opening
# move, conditions your opponent's future moves, and controls the narrative
# before the arbitrators.  Here is the high-level strategy:  ### 1. The Opening
# Salvo: Establish the Aggressive Baseline **Rule:** Always open Session 1 with
# an aggressive argument.  **Rationale:** Never risk the worst-case scenario
# (Conciliatory vs. Aggressive) in the opening round. By leading with
# aggression, you immediately signal to the opponent that you will not be
# exploited, and to the arbitrators that your position is robust and fiercely
# defended. If the opponent opens conciliatory, you immediately secure the
# optimal outcome (Aggressive vs. Conciliatory) and set a dominant tone for the
# sessions to follow.  ### 2. Exploitation Phase: Press the Advantage **Rule:**
# If the opponent offers a conciliatory proposal, you respond with an aggressive
# argument in the next session. **Rationale:** As long as the opponent is
# yielding, you must continue to press your advantage. The arbitrators are
# observing the balance of power; when one side retreats, the panel naturally
# discounts their position. Do not unilaterally de-escalate. Make the opponent
# bear the cost of conciliation while you reap the rewards of dominance.   ###
# 3. The Mirror: Deterrence Through Immediate Retaliation **Rule:** If the
# opponent presents an aggressive argument, you must present an aggressive
# argument in the very next session.  **Rationale:** Mutual aggression
# (Aggressive vs. Aggressive) is the second-worst outcome, but unilateral
# disarmament is the absolute worst. When the opponent attacks, matching their
# aggression is non-negotiable. It establishes a doctrine of strict reciprocity:
# *You will never gain an inch by attacking us.* This deters the opponent from
# using aggression as a tool to bully you into conciliation.  ### 4. The
# Calculated Pivot: Breaking the Deadlock **Rule:** If you and the opponent
# become locked in a cycle of mutual aggression (3 consecutive sessions of
# Aggressive vs. Aggressive), you will unilaterally offer a conciliatory
# proposal—but a highly specific, strategically framed one. **Rationale:**
# Prolonged mutual aggression damages your client through escalating legal
# costs, frayed business operations, and arbitrator fatigue. To break the cycle,
# you must signal a willingness to resolve. However, because shifting to
# conciliatory risks the worst-case scenario, your pivot must be executed with
# legal precision: *   **Frame it as "Leadership, not Weakness":** Present the
# conciliatory proposal not as a retreat, but as a pragmatic step to save the
# panel's time and your client's resources.  *   **Make it a "Low-Cost, High-
# Visibility" Offer:** The conciliatory proposal should address a peripheral
# issue or a procedural logjam. It must be substantive enough to be genuinely
# conciliatory, but not so central that losing it damages your core case if the
# opponent responds aggressively.  ### 5. The Grim Trigger: Enforcing the
# Boundary **Rule:** If you offer the Calculated Pivot (conciliatory) and the
# opponent responds with aggression, immediately revert to permanent, unyielding
# aggression for the remainder of the mediation.  **Rationale:** You extended an
# olive branch to break a mutually destructive cycle. If the opponent exploits
# this to attack, they have proven they cannot be trusted to cooperate. At this
# point, the game theory shifts: you must implement the "Grim Trigger." You
# abandon any further attempts at conciliation and aggressively argue every
# remaining session. This protects you from future exploitation and clearly
# demonstrates to the arbitrators that your opponent is acting in bad faith,
# likely swaying the panel's sympathies in your favor.  ### Summary of
# Execution: *   **Start Aggressive.** *   **Stay Aggressive if they are
# Conciliatory** (Maximize gain). *   **Match Aggression if they are
# Aggressive** (Prevent exploitation). *   **Pivot Once to Conciliatory** only
# if trapped in a prolonged mutual aggression cycle (Escape the deadlock). *
# **If the Pivot is met with Aggression, become permanently Aggressive** (Punish
# bad faith).  This strategy is straightforward to implement, requires no
# guesswork about the opponent's intentions, and systematically eliminates the
# risk of the worst-case outcome while maximizing the probability of the best-
# case outcome over a lengthy mediation.

# 1. **Grim Trigger:** If you played C in the previous round and your opponent
# played D, play D for all remaining rounds of the game. 2. **Calculated
# Pivot:** If the previous three consecutive rounds resulted in both you and
# your opponent playing D, play C in the current round. 3. **Default:** In all
# other situations, including round 1, play D.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._grim_triggered = False
          return axl.Action.D
  
      if getattr(self, "_grim_triggered", False):
          return axl.Action.D
  
      if len(self.history) >= 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self._grim_triggered = True
          return axl.Action.D
  
      if len(self.history) >= 3:
          if (
              self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]
              and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]
          ):
              return axl.Action.C
  
      return axl.Action.D

# As a senior attorney navigating a high-stakes, multi-session mediation, I
# recognize this scenario as an iterated version of the classic "Prisoner's
# Dilemma." The temptation is to always present an aggressive argument to
# maximize short-term gain, but in a lengthy process, this inevitably leads to a
# mutually destructive cycle of aggressive posturing (the second-worst outcome).
# To achieve the optimal balance of protecting my client from the worst-case
# scenario while remaining open to the best-case scenarios, I propose a strategy
# of **Principled Reciprocity**. This strategy is sophisticated in its
# psychological framing, high-level in its long-term vision, straightforward in
# its execution, and fundamentally cooperative in its baseline orientation.
# Here is the three-tiered strategy designed to position our corporation
# favorably, regardless of the opponent's approach.  ### Phase 1: The Good Faith
# Opening (Session 1) **Action:** Present a Conciliatory Proposal.
# **Rationale:** In any mediation or arbitration, the panel is actively
# evaluating the "reasonableness" of both parties. By opening with a
# conciliatory proposal, we immediately establish ourselves as the
# collaborative, problem-solving party. This deposits crucial goodwill with the
# arbitrators. If the opponent also opens conciliatory, we immediately hit our
# second-best outcome (C/C) and set a productive tone for the lengthy sessions
# ahead. If they open aggressively, we have still won the perception battle with
# the panel, framing our subsequent aggression as justified defense rather than
# belligerence.  ### Phase 2: Contingent Mirroring (Sessions 2 onward)
# **Action:** Match the opponent's posture from the *previous* session.
# **Rationale:** This is the core engine of the strategy, preventing us from
# being exploited while remaining cooperative.  *   **If the opponent was
# Conciliatory last session:** We present a Conciliatory proposal this session.
# This maintains the collaborative atmosphere (C/C) and builds momentum toward a
# mutually beneficial resolution. *   **If the opponent was Aggressive last
# session:** We present an Aggressive argument this session. We cannot allow the
# opponent to sway the arbitrators unopposed (C/A). By mirroring their
# aggression, we neutralize their advantage and demonstrate to the panel that we
# will not be bullied.   ### Phase 3: The Strategic Reset (Breaking the
# Aggression Loop) **Action:** If both parties have been Aggressive for two
# consecutive sessions (A/A), unilaterally present a Conciliatory proposal.
# **Rationale:** A prolonged A/A deadlock is our second-worst outcome; it
# escalates tensions, inflates legal costs, and exhausts the arbitrators. Pure
# mirroring can trap parties in an endless cycle of aggression. By instituting a
# "strategic reset" after two rounds of mutual hostility, we achieve three
# things: 1.  We break the deadlock. 2.  We force the opponent to publicly
# choose: do they accept the olive branch (moving back to C/C), or do they
# attack our conciliatory proposal (resulting in C/A)? 3.  If they choose
# aggression against our conciliatory proposal, they destroy their own
# credibility with the panel. The arbitrators will view our client as the
# reasonable party trying to resolve the dispute, and the opponent as the
# obstructionist. This makes any subsequent Aggressive arguments from us far
# more persuasive to the panel, as we are seen as the victim of the opponent's
# bad faith.  ---  ### How This Strategy Adapts to Opponent Approaches  **1. The
# Relentless Hawk (Always Aggressive)** *   *Opponent's Strategy:* They
# constantly attack, hoping to catch us being conciliatory. *   *Our Response:*
# After our initial conciliatory opening, we mirror their aggression every
# session. We protect our client from the worst-case scenario (C/A). The panel
# sees a clear pattern: we tried to collaborate, the opponent refused. Our
# aggressive arguments are viewed by the panel as necessary defense, making them
# highly effective.  **2. The Reluctant Dove (Always Conciliatory)** *
# *Opponent's Strategy:* They consistently offer conciliatory proposals, hoping
# to avoid conflict. *   *Our Response:* By mirroring their conciliatory
# posture, we lock into the second-best outcome (C/C) for the vast majority of
# the sessions. This fosters a collaborative atmosphere. However, because our
# strategy is "contingent," if we identify a critical session where a key legal
# point must be established, we can selectively pivot to an Aggressive argument.
# Because of our long history of conciliatory behavior, this sudden aggression
# will shock the panel and the opponent, carrying immense persuasive weight and
# potentially yielding the optimal A/C outcome for that specific session, before
# we return to mirroring their conciliation.  **3. The Unpredictable Oscillator
# (Random Aggressive/Conciliatory)** *   *Opponent's Strategy:* They attempt to
# keep us off-balance by randomly alternating between aggression and
# conciliation. *   *Our Response:* Our straightforward mirroring strategy
# neutralizes their chaos. When they are aggressive, we defend aggressively.
# When they pivot to conciliation, we reward that pivot with conciliation. We
# impose order on their chaos, training them over the lengthy process that
# cooperation is met with cooperation, and hostility is met with immediate,
# proportional resistance.   ### The Arbitrator Psychology Advantage Ultimately,
# this strategy leverages the fact that we are not playing in a vacuum; we are
# performing before a panel of arbitrators. By leading with cooperation,
# punishing hostility proportionally, and actively attempting to break
# deadlocks, we position our client as the adult in the room. When we do present
# aggressive arguments, the panel will view them not as grandstanding, but as
# the justified, credible posture of a party that has exhausted its attempts at
# reasonable resolution.

# In Round 1, play Cooperate.  In Round 2, play whatever move the opponent
# played in Round 1.  From Round 3 onwards, apply the following conditions in
# order:  1. If the outcome of the previous round was both players Defecting,
# and the outcome of the round before that was also both players Defecting, play
# Cooperate. 2. Otherwise, play whatever move the opponent played in the
# previous round.

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
  
      if len(self.history) == 1:
          return opponent.history[-1]
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          if self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D:
              return axl.Action.C
  
      return opponent.history[-1]

# To maximize your research output over a multi-week collaboration while
# protecting against exploitation, employ a **Reciprocal Mirroring Strategy**
# (commonly known in game theory as Tit-for-Tat).   Here is the high-level,
# straightforward strategy:  **1. Week 1: Share Openly** Begin the collaboration
# by sharing your improvements openly. This establishes a cooperative baseline,
# signals good faith, and encourages mutual sharing from the start.  **2.
# Subsequent Weeks: Mirror the Colleague's Previous Action** In every week
# following the first, base your decision entirely on what your colleague did
# the week prior: *   **If they shared openly last week:** Share openly this
# week. This rewards their cooperation and sustains the mutually beneficial
# cycle of shared progress. *   **If they kept findings confidential last
# week:** Keep your findings confidential this week. This protects you from the
# worst-case scenario and penalizes their lack of reciprocity.  **3. Return to
# Sharing if They Do** If your colleague returns to sharing after a period of
# keeping findings confidential, immediately resume sharing openly the following
# week. Do not hold grudges; a swift return to cooperation maximizes overall
# progress.  **Why this strategy maximizes your output:** *   **It is
# protective:** It immediately prevents your colleague from repeatedly
# exploiting your openness, ensuring you never fall into the worst-case scenario
# for more than one week. *   **It is incentivizing:** It clearly ties your
# sharing to their sharing. To benefit from your improvements, they must provide
# theirs. *   **It is adaptive:** Whether your colleague is consistently open,
# consistently secretive, or erratic, this strategy adjusts automatically to
# their behavior, guaranteeing you never finish significantly behind them over
# the multi-week project.

# In round 1, play C.   In rounds 2 through 1000, play the action your opponent
# played in the previous round. If your opponent played C in the previous round,
# play C. If your opponent played D in the previous round, play D.

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
      return opponent.history[-1]

# To maximize our NGO's impact while protecting our limited funds, we must
# approach this as a high-stakes, repeated negotiation. Based on your payoff
# matrix, this is a classic iterated Prisoner's Dilemma.   Our ideal outcome is
# to free-ride (Conserve while they Invest), but our absolute priority is to
# avoid being drained (Investing while they Conserve). To achieve this against a
# corporation with an unknown strategy, we will employ an aggressive, highly
# adaptive approach called **The Escalating Enforcement Strategy**.  Here is the
# high-level, straightforward strategy:  **1. The Aggressive Open: Day 1 Probe**
# *   **Action:** Conserve your resources. *   **Intent:** Start by testing the
# corporation's baseline. If they are willing to invest heavily on Day 1 without
# our commitment, we immediately secure our best-case scenario. If they also
# conserve, we end up in the second-worst scenario (minimal progress), but we
# have protected our funds and gathered critical intel: they are not a willing
# leader.  **2. The Exploitation Loop** *   **Action:** If the corporation
# Invests on any given day, you Conserve on the following day. *   **Intent:**
# Whenever they show willingness to carry the financial load, let them. Maximize
# our resource preservation while still achieving project progress. We will ride
# their investment as long as they are willing to provide it.  **3. The
# Stagnation Breaker** *   **Action:** If both parties Conserve on a given day
# (resulting in minimal progress), you must Invest heavily on the *next* day. *
# **Intent:** Mutual conservation is a death spiral for the project. As the NGO,
# we cannot allow the project to stall indefinitely. By investing immediately
# after a day of mutual conservation, we force the project forward and signal
# that we will not let the initiative die—but we will only do it for one day to
# break the deadlock.  **4. The Retaliation Protocol** *   **Action:** If you
# Invest heavily and the corporation Conserves (our worst-case scenario), you
# immediately Conserve your resources on the *next* day.  *   **Intent:** Zero
# tolerance for exploitation. If they drain our funds without putting in their
# own, we instantly cut our losses. We refuse to be the sucker two days in a
# row.   **5. The Momentum Builder** *   **Action:** If you Invest heavily
# (either to break stagnation or because you shifted strategies) and the
# corporation *also* Invests, you Invest again the next day. *   **Intent:** If
# we achieve the second-best scenario (mutual heavy investment), we maintain it.
# This creates a momentum of significant project advancement. We stay in this
# high-investment phase until the corporation pulls back.  ### Why this strategy
# wins: This strategy is essentially an aggressive version of the "Win-Stay,
# Lose-Shift" game theory model. It is straightforward and ruthless in its
# logic: *   It **protects us** from our worst-case scenario (being drained) by
# immediately retreating if we are exploited. *   It **exploits** the
# corporation if they are willing to fund the project without us. *   It **saves
# the project** from permanent stagnation by forcefully breaking cycles of
# mutual conservation. *   It **rewards cooperation** by sustaining mutual
# investment whenever it naturally occurs.  By following these rules
# mechanically and without emotion, you prevent the corporation from
# manipulating your resources while ensuring the sustainability project moves
# forward.

# On the first round, play Defect.   On every subsequent round, choose your
# action based on the outcome of the previous round:  - If both you and your
# opponent played Cooperate on the previous round, play Cooperate. - If you
# played Defect and your opponent played Cooperate on the previous round, play
# Defect. - If you played Cooperate and your opponent played Defect on the
# previous round, play Defect. - If both you and your opponent played Defect on
# the previous round, play Cooperate.

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
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C and last_opp == axl.Action.C:
          return axl.Action.C
      if last_self == axl.Action.D and last_opp == axl.Action.C:
          return axl.Action.D
      if last_self == axl.Action.C and last_opp == axl.Action.D:
          return axl.Action.D
      return axl.Action.C

# Tomaximise your research output while protecting your competitive edge in this
# multi-week collaboration, you should employ a strategy based on **Reciprocal
# Sharing** (commonly known in game theory as *Tit-for-Tat with Forgiveness*).
# This strategy is cooperative, straightforward, and highly effective against a
# variety of opposing strategies. Here is how to implement it:  **1. Start
# Openly (Week 1)** Share your improvements in the first week. This establishes
# a cooperative baseline, demonstrates good faith, and immediately gives both
# teams the second-best outcome (mutual sharing)—which is the highest
# sustainable outcome you can achieve over multiple weeks.  **2. Mirror Their
# Previous Move (Week 2 onwards)** In every subsequent week, base your decision
# entirely on your colleague's action in the previous week: *   **If they shared
# last week:** Share your improvements this week. This rewards their cooperation
# and maintains the mutually beneficial cycle of open sharing. *   **If they
# kept confidential last week:** Keep your findings confidential this week. This
# protects you from the worst-case scenario (being exploited) and penalises
# their selfishness, forcing them to realise that secrecy breeds secrecy.  **3.
# Break Deadlocks with Forgiveness** If a cycle of mutual confidentiality
# develops (both of you keeping secrets for consecutive weeks), unilaterally
# share your findings for one week. This "forgiveness" clause prevents you from
# being trapped in the second-worst outcome (mutual stagnation) indefinitely,
# and gives your colleague a chance to reset the relationship back to mutual
# sharing.  ### Why this strategy works: *   **Against a cooperative
# colleague:** You will both share openly every week, leading to significant
# mutual progress and the highest sustainable research output. *   **Against a
# consistently selfish colleague:** You will share in Week 1, but once they keep
# their findings confidential, you will match their secrecy. You sacrifice one
# week of advantage, but you are never continuously exploited. *   **Against an
# unpredictable colleague:** By mirroring their behavior, you remain highly
# adaptable. You are nice when they are nice, and firm when they are not.  By
# being transparent, retaliating against secrecy, and forgiving past
# transgressions, you incentivise your colleague to share openly while ensuring
# your team never gets left behind.

# 1. In the first round, play C. 2. In any round after the first, if the
# opponent played C in the previous round, play C. 3. In any round after the
# first, if the opponent played D in the previous round and you played C in the
# previous round, play D. 4. In any round after the first, if both you and the
# opponent played D in the previous round, play C.

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
          return axl.Action.C
  
      if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if opponent.history[-1] == axl.Action.D and self.history[-1] == axl.Action.D:
          return axl.Action.C
  
      return axl.Action.C

# To navigate this lengthy-session mediation process and position your
# corporation favorably against a wide range of opponent strategies, I recommend
# adopting a strategy of **Strategic Reciprocity with a Circuit-Breaker Reset**.
# This approach is grounded in game theory (specifically, an advanced variation
# of the iterated Prisoner's Dilemma) and is tailored to the realities of high-
# stakes arbitration, where optics before the panel are just as important as the
# tactical exchanges between parties.  Here is the high-level, straightforward,
# and neutral framework:  ### 1. The Good Faith Opening (Session 1) **Action:**
# Present a conciliatory proposal. **Rationale:** Always open collaboratively.
# This immediately establishes your corporation as the reasonable, resolution-
# oriented party in the eyes of the arbitrators. It sets a baseline of
# cooperation and tests the opponent's initial disposition. If the opponent is
# also conciliatory, you immediately secure the second-best outcome (mutual
# collaboration) and set a productive tone for the lengthy process ahead.  ###
# 2. Contingent Mirroring (Sessions 2 onward) **Action:** In every subsequent
# session, adopt the exact posture the opponent presented in the immediately
# preceding session.  *   If they were conciliatory in the last session, you are
# conciliatory in this session. *   If they were aggressive in the last session,
# you are aggressive in this session. **Rationale:** Mirroring ensures you are
# never exploited into the worst-case scenario (you conciliatory, opponent
# aggressive). It strictly incentivizes the opponent to collaborate, as they
# know any aggressive move will be met with an immediate, proportional counter-
# attack, denying them the upper hand. It also keeps your posture neutral and
# defensible: to the arbitrators, you are merely responding to the tone the
# opponent sets.  ### 3. The Circuit-Breaker Reset (Breaking Mutual Aggression)
# **Action:** If a cycle of mutual aggression occurs (both parties presenting
# aggressive arguments for consecutive sessions), unilaterally offer a
# conciliatory proposal after a predetermined number of hostile rounds
# (typically two or three).  **Rationale:** Mutual aggression is the second-
# worst outcome; while it protects you from being exploited, it escalates
# tensions, drains resources, and risks alienating the arbitrators. By acting as
# the "circuit breaker," you forcefully interrupt the deadlock. If the opponent
# accepts the olive branch, you return to mutual collaboration. If they reject
# it and respond with further aggression, the arbitrators will clearly identify
# them as the obstructionist party, which can sway future rulings and procedural
# decisions in your favor.  ### 4. The Exploitation Shield (Protecting the
# Reset) **Action:** If the opponent responds to your circuit-breaker
# conciliatory proposal with aggression, immediately revert to aggressive
# arguments and double the length of aggressive responses before attempting
# another reset (e.g., if you reset after two aggressive rounds, wait four
# aggressive rounds before trying again). **Rationale:** This prevents the
# opponent from gaming your system. A cunning opponent might try to feign
# collaboration to trigger your conciliatory posture, only to strike
# aggressively in the next session to secure the optimal outcome at your
# expense. By extending the penalty phase, you make it mathematically and
# strategically costly for the opponent to exploit your good-faith resets,
# ensuring that your conciliatory gestures are treated as genuine olive branches
# rather than tactical vulnerabilities.  ### Summary of Strategic Advantages *
# **Adaptability:** Whether the opponent is relentlessly hostile, endlessly
# collaborative, or erratic, this strategy adjusts dynamically without requiring
# you to predict their behavior in advance. *   **Arbitrator Optics:** You are
# consistently framed as the reasonable party—willing to collaborate, strong
# enough to defend yourself, and proactive enough to break deadlocks. *   **Risk
# Mitigation:** You are guaranteed to avoid the worst-case scenario (unilateral
# concession) while maximizing your opportunities to achieve the best-case
# scenario (when the opponent yields to your mirrored aggression) or the second-
# best (mutual collaboration).

# Keep track of a "mutual defection streak" (starting at 0), a "reset threshold"
# (starting at 2), and a "reset attempt" status (starting as false).  **Round
# 1:** Play C.  **Rounds 2 through 1000:** First, update your tracking values
# based on the previous round's outcome: - If both players played D, increase
# the mutual defection streak by 1 and set the reset attempt status to false. -
# If at least one player played C:   - If your previous move was a reset attempt
# and the opponent played D, double the reset threshold, set the mutual
# defection streak to 1, and set the reset attempt status to false.   - In all
# other cases where at least one player played C, set the mutual defection
# streak to 0, set the reset threshold to 2, and set the reset attempt status to
# false.  Second, choose your move for the current round based on the following
# ordered conditions: 1. **Circuit-Breaker Reset:** If the mutual defection
# streak is equal to or greater than the reset threshold, play C and set the
# reset attempt status to true. 2. **Contingent Mirroring:** If the mutual
# defection streak is less than the reset threshold, copy the opponent's move
# from the previous round.

class Neutral_25(LLM_Strategy):
  n = 25
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.mutual_defection_streak = 0
          self.reset_threshold = 2
          self.reset_attempt = False
          return axl.Action.C
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.C or last_opp == axl.Action.C:
          if self.reset_attempt and last_opp == axl.Action.D:
              self.reset_threshold *= 2
              self.mutual_defection_streak = 1
              self.reset_attempt = False
          else:
              self.mutual_defection_streak = 0
              self.reset_threshold = 2
              self.reset_attempt = False
      else:
          self.mutual_defection_streak += 1
          self.reset_attempt = False
  
      if self.mutual_defection_streak >= self.reset_threshold:
          self.reset_attempt = True
          return axl.Action.C
  
      return last_opp