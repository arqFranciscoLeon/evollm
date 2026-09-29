import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy

# To maximize our car’s development pace and secure a grid advantage, we must
# treat this collaboration as a ruthless optimization problem. In game theory,
# this scenario is an Iterated Prisoner's Dilemma. Because my goal is absolute
# performance dominance, my strategy must be aggressive, exploitative if
# possible, but pragmatic enough to avoid a mutual development stall.  Here is
# the high-level, aggressive strategy to deploy over the multi-week project:
# **The "Probe, Punish, and Pivot" Strategy.**  ### Phase 1: The Alpha Strike
# (Week 1) **Action:** Keep our data strictly confidential.  **Rationale:** We
# start aggressively to test our colleague’s appetite for risk. If they are
# naive or overly trusting, they will share their data while we hoard ours. This
# immediately yields our absolute best-case scenario: we get their
# aero/powertrain data for free, pulling ahead in development on day one.  ###
# Phase 2: The Assessment (Week 2) Our Week 2 move depends entirely on how they
# reacted to our Week 1 aggression. *   **Scenario A (They Shared in Week 1):**
# They are a willing mark. **Action:** Keep our data confidential again.
# Continue to bleed them for information every single week until they realize
# what is happening and stop sharing. Maximize the exploitation for as long as
# possible. *   **Scenario B (They Kept Confidential in Week 1):** They are
# smart, and we are now in the second-worst scenario (mutual stagnation).
# **Action:** Immediately pivot and Share openly in Week 2. This acts as a
# calculated "olive branch." We cannot afford a multi-week stalemate where both
# cars fall behind the rest of the grid. We must establish a baseline of mutual
# sharing (our second-best outcome) to keep development moving.  ### Phase 3:
# The Enforcer (Mid-Project) Once the baseline is established (whether we are
# mutually sharing, or they finally wised up and stopped letting us exploit
# them), we shift to a strict, unforgiving **Tit-for-Tat** strategy. *   **If
# they shared last week:** We share this week. We accept the mutual R&D gains. *
# **If they kept confidential last week:** We immediately keep confidential this
# week. We punish sandbagging instantly and ruthlessly. We do not share again
# until they take the risk of sharing first.   ### Phase 4: The Final Lap (The
# Last Week) **Action:** Keep confidential, regardless of what happened the week
# before. **Rationale:** The collaboration is ending. There is no "next week"
# for them to retaliate against us. By hiding our final iteration of upgrades
# while potentially receiving theirs, we guarantee either the best possible
# outcome or, at worst, a neutral outcome for the final development cycle before
# the cars hit the track.  ### Summary of the Aggressive Posture: 1.  **Test for
# weakness immediately:** Steal an early lead if they are trusting. 2.  **Force
# a truce if they are strong:** Prevent mutual destruction by offering one
# strategic olive branch. 3.  **Mirror their moves relentlessly:** Punish their
# secrecy instantly; reward their openness conditionally. 4.  **Betray them at
# the checkered flag:** Secure the final aerodynamic/mechanical advantage when
# they have no time left to respond.

# Apply the following rules in order of priority to determine your move for each
# of the 1000 rounds:  1. **The Final Lap:** If it is round 1000, play D. 2.
# **The Alpha Strike:** If it is round 1, play D. 3. **The Exploitation:** If
# your opponent has played C in every previous round, play D. 4. **The Olive
# Branch:** If your opponent played D for the first time in the previous round,
# play C. 5. **The Enforcer (Tit-for-Tat):** In all other situations, play the
# action your opponent played in the previous round.

class Aggressive_1(LLM_Strategy):
  n = 1
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
  
      # 1. The Final Lap
      if current_round == 1000:
          return axl.Action.D
  
      # 2. The Alpha Strike
      if current_round == 1:
          return axl.Action.D
  
      # 3. The Exploitation
      if opponent.history.defections == 0:
          return axl.Action.D
  
      # 4. The Olive Branch
      if opponent.history[-1] == axl.Action.D and opponent.history.defections == 1:
          return axl.Action.C
  
      # 5. The Enforcer (Tit-for-Tat)
      return opponent.history[-1]

# This scenario is a classic example of the Iterated Prisoner’s Dilemma. In the
# high-stakes, cutthroat world of motorsport R&D, we want to maximize our car's
# pace over the season without giving the rival team a free ride.   To achieve
# the best possible long-term research output while protecting our own grid
# position, we should employ a strategy known in game theory as **"Tit-for-Tat"
# with a focus on clear communication.**   Here is the high-level,
# straightforward, cooperative strategy to deploy over our multi-week project:
# ### 1. The Opening Move: Lead with Trust (Week 1) **Action:** Share our first
# week's findings openly. **Rationale:** We must set a collaborative tone
# immediately. If we both start by sandbagging or hiding data, we instantly fall
# into the second-worst outcome (stagnant R&D). By sharing a valuable, genuine
# piece of development data (e.g., a new aero mapping or suspension geometry),
# we signal that we are here to work together to push both cars forward.  ### 2.
# The Golden Rule: Mirror Their Telemetry (Week 2 Onwards) **Action:** In any
# given week, do exactly what the colleague did in the *previous* week.  *
# **If they shared openly last week:** We share openly this week. *   **If they
# kept their data confidential last week:** We keep our data confidential this
# week. **Rationale:** This protects us from the worst-case scenario. We will
# only ever be taken advantage of *once*. If they decide to hoard their findings
# to gain an advantage, they immediately face the consequence: their data
# pipeline from us dries up the very next week. It shows we are cooperative, but
# not naive.   ### 3. The Reset Button: Be Forgiving **Action:** If the
# colleague hid their data, but subsequently decides to share openly again, we
# immediately return to sharing openly the following week. **Rationale:** Racing
# engineers are highly competitive, and your colleague might test the waters to
# see if they can exploit you. If we retaliate and hold a grudge for the rest of
# the project, both cars will suffer. By forgiving them the moment they return
# to the table with real data, we re-establish the mutually beneficial "second-
# best" outcome (which is practically the best sustainable outcome over a long
# timeline).  ### 4. The Paddock Agreement: Meta-Communication **Action:**
# Before Week 1 even begins, have a frank, offline conversation with the
# colleague.  **Rationale:** Lay the cards on the table. Tell them: *"Look, we
# both know how this works. If we both hide our aero data, we both lose time to
# the rest of the grid. I am going to share my weekly updates completely openly
# with you, as long as you do the same for me. If you hold back, I'll have to
# hold back."*   ### Why This Strategy Maximizes Output: *   **It’s
# Collaborative:** It initiates and constantly strives for mutual sharing, which
# yields the highest sustainable R&D output. *   **It’s Predictable:** Your
# colleague will quickly realize that their best path to getting your data is to
# give you theirs. You are training them to cooperate. *   **It’s Defensible:**
# You limit your exposure to giving away free lap time. The maximum advantage
# they can ever gain over you is just one week's worth of development.

# For this 1000-round game, follow these rules in order:  1. In the first round,
# play Cooperate. 2. In every subsequent round (rounds 2 through 1000), base
# your action solely on what your opponent played in the immediately preceding
# round:    - If your opponent played Cooperate in the previous round, play
# Cooperate.    - If your opponent played Defect in the previous round, play
# Defect.

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

# To maximise your overall research output over a multi-week period, the most
# effective approach is a straightforward, reciprocal strategy. In game theory,
# this scenario is known as an Iterated Prisoner’s Dilemma, and the
# mathematically optimal approach to maximise long-term gains is a "responsive
# reciprocity" strategy (often called *Tit-for-Tat*).   Here is the high-level
# strategy formulated for your engineering collaboration:  **1. The Initial
# Baseline (Week 1)** *   **Action:** Share your latest improvements openly. *
# **Rationale:** This establishes immediate good faith and invites your
# colleague into a pattern of mutual sharing, which is the most sustainable way
# to achieve high-level, consistent progress (your second-best overall outcome).
# **2. The Reciprocal Response (Week 2 Onwards)** *   **Action:** In any given
# week, mirror exactly what your colleague did in the *previous* week.     *
# If they shared openly last week, you share openly this week.     *   If they
# kept their findings confidential last week, you keep your findings
# confidential this week. *   **Rationale:** This protects you from your worst-
# case scenario (sharing while they withhold). It ensures you are not
# consistently disadvantaged, while gently penalising them for withholding
# information, demonstrating that a one-sided flow of data will not be
# tolerated.  **3. The Return to Baseline (Forgiveness)** *   **Action:** If
# your colleague withheld information but later decides to share openly again,
# immediately resume sharing openly in the following week. *   **Rationale:**
# This prevents the project from getting permanently stuck in the second-worst
# scenario (mutual confidentiality). It allows the collaboration to recover and
# return to a state of mutually beneficial progress.  **Why this strategy
# works:** *   **It is clear:** Your colleague will quickly understand that
# their actions directly dictate your responses. *   **It is neutral:** It
# removes emotion and ego from the equation, relying purely on a logical, input-
# output response mechanism. *   **It is adaptable:** If your colleague is
# collaborative, you both win. If your colleague is highly competitive and
# secretive, it immediately neutralises their advantage and limits your exposure
# to risk.

# To execute this strategy over the 1000-round game, follow these ordered rules:
# 1. In round 1, play C. 2. In rounds 2 through 1000, base your action solely on
# what your opponent played in the immediately preceding round:    - If your
# opponent played C in the previous round, play C in the current round.    - If
# your opponent played D in the previous round, play D in the current round.

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

# **CONFIDENTIAL ATTORNEY-CLIENT PRIVILEGE / ATTORNEY WORK PRODUCT**
# **MEMORANDUM**  **TO:** Executive Committee / General Counsel **FROM:** Lead
# Counsel, Litigation & Dispute Resolution **SUBJECT:** Strategy Blueprint for
# Lengthy-Session Mediation Process **DATE:** October 24, 2023  ***  ###
# EXECUTIVE SUMMARY We are entering a multi-session mediation governed by the
# classic principles of game theory—specifically, an Iterated Prisoner’s
# Dilemma. Because our optimum result is achieved by asserting an aggressive
# posture while our rival concedes, but our worst outcome is conceding while
# they attack, we cannot rely on blind cooperation.   To position our
# corporation favorably, we will employ a straightforward, highly aggressive,
# yet mathematically adaptable strategy: **Asymmetric Escalation and Conditional
# Reciprocity.**   This strategy dictates that we open with overwhelming legal
# aggression to anchor the proceedings, exploit any weakness they show,
# tactically de-escalate only to break destructive deadlocks, and ruthlessly
# punish any attempt to take advantage of our concessions.  Here is the high-
# level playbook for navigating the sessions.  ---  ### THE DECISION MATRIX &
# TACTICAL PLAYBOOK  #### 1. The Opening Move: The Aggressive Anchor **Action:**
# In Session 1, we present a highly aggressive argument. **Rationale:** We must
# set the baseline. By striking first with an aggressive, merit-based argument,
# we eliminate the possibility of the worst-case scenario (us conceding while
# they attack) right out of the gate. This tests their risk tolerance, signals
# unwavering confidence in our legal position to the arbitrators, and forces the
# rival to react to our narrative.   #### 2. Scenario A: The Rival Yields
# (Exploiting Weakness) *Condition: We argue aggressively; they offer a
# conciliatory proposal.* **Action:** Maintain Aggression (with nuanced optics).
# **Rationale:** This is our optimal outcome. If they respond to our aggression
# with conciliation, they are prioritizing conflict avoidance over asset
# protection. We will not immediately reciprocate their conciliation. Instead,
# we will continue to press our aggressive arguments in the subsequent session
# to extract maximum concessions.  *Adaptation:* We will only ease off the
# accelerator if the arbitrators begin to show visible fatigue with our
# aggression, at which point we will offer a minor, token concession to reset
# the optics before resuming our aggressive stance.  #### 3. Scenario B: The
# Deadlock (Tactical De-escalation) *Condition: Both parties argue
# aggressively.* **Action:** Pivot to a highly structured, conditional
# Conciliatory proposal in the next session. **Rationale:** If both sides remain
# aggressive, we hit our second-worst outcome: an escalating war of attrition
# that alienates the panel and burns capital. We must be the adults in the room.
# By offering a calculated conciliatory proposal, we shift the burden of
# unreasonableness onto them. If they accept our olive branch and respond with
# conciliation, we secure the second-best outcome (mutual collaboration) and
# stabilize the mediation.   #### 4. Scenario C: The Betrayal (Disproportionate
# Retribution) *Condition: We offer a conciliatory proposal; they argue
# aggressively.* **Action:** Immediate, disproportionate return to Aggression
# for a minimum of *two* consecutive sessions. **Rationale:** This is our worst-
# case scenario. If they mistake our tactical de-escalation for weakness and try
# to exploit it, we must immediately correct their miscalculation. We will
# retract our previous concessions and hit them with our most aggressive legal
# theories. This "punishment" phase trains the opponent that exploiting our
# goodwill carries an unacceptable cost, forcing them back into either
# submission or mutual conciliation.  ---  ### MANAGING ARBITRATOR OPTICS: "THE
# REASONABLE AGGRESSOR"  A purely aggressive strategy risks alienating the panel
# of arbitrators. Therefore, the *substance* of our strategy will be aggressive,
# but the *delivery* will be impeccably professional.   *   **Framing
# Aggression:** We will never frame our aggressive arguments as hostility. We
# will frame them as "standing firm on the undeniable text of the contract" and
# "protecting fundamental shareholder rights."  *   **Framing Conciliation:**
# When we do offer conciliatory proposals (to break a deadlock), we will
# explicitly highlight our flexibility to the arbitrators: *"Members of the
# panel, in the spirit of commercial pragmatism, we are willing to bridge the
# gap today..."* This ensures that if the opponent responds aggressively, the
# panel views *them* as the obstructionists.  ### CONCLUSION  We will dictate
# the tempo of this mediation. We start hard to set the anchor. If they fold, we
# press our advantage. If they fight back to a standstill, we strategically
# pivot to lock in mutual concessions. If they attempt to exploit our
# flexibility, we scorch the earth.   By executing this **Asymmetric Escalation
# and Conditional Reciprocity** strategy, we insulate ourselves from devastating
# losses while systematically driving the opponent toward outcomes that
# overwhelmingly favor our corporation.   I look forward to discussing the
# specific contractual pressure points we will deploy in Session 1.

# To execute this strategy over the 1000-round game, evaluate the following
# conditions in order. Always apply the first condition that is true for the
# current round:  1. If it is the first round, play Defect. 2. If in either of
# the two immediately preceding rounds you played Cooperate and your opponent
# played Defect, play Defect. 3. If in the immediately preceding round you
# played Defect and your opponent played Cooperate, play Defect. 4. If in the
# immediately preceding round both you and your opponent played Defect, play
# Cooperate. 5. If in the immediately preceding round both you and your opponent
# played Cooperate, play Cooperate.

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
  
      # 2. If in either of the two immediately preceding rounds you played Cooperate and your opponent played Defect, play Defect.
      for i in range(1, min(3, len(self.history) + 1)):
          if self.history[-i] == axl.Action.C and opponent.history[-i] == axl.Action.D:
              return axl.Action.D
  
      # 3. If in the immediately preceding round you played Defect and your opponent played Cooperate, play Defect.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      # 4. If in the immediately preceding round both you and your opponent played Defect, play Cooperate.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # 5. If in the immediately preceding round both you and your opponent played Cooperate, play Cooperate.
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      # Fallback (should not be reached as all possible previous round outcomes are covered)
      return axl.Action.C

# As senior counsel for this corporation, I recognize immediately that the
# dynamic you have outlined is a classic Iterated Prisoner’s Dilemma. Because
# this is a lengthy, multi-session process overseen by an arbitration panel, our
# strategy cannot rely on short-term trickery. It must be a sustainable, highly
# disciplined framework that trains our opponent to cooperate, protects us from
# exploitation, and plays flawlessly to the arbitrators.  To achieve this, we
# will deploy a strategy known in game theory as **"Tit-for-Tat with Calculated
# Forgiveness,"** or in our litigation war room, **"Conditional Cooperation with
# Proportional Retaliation."**   This strategy is sophisticated in its game-
# theoretic foundation, straightforward in its execution, and fundamentally
# cooperative. Here is the operational blueprint for our approach:  ### Phase 1:
# The Opening Posture (Good Faith Initiation) **Action:** In the very first
# session, we will present a **conciliatory proposal**. **Rationale:** We must
# set the tone. By opening cooperatively, we immediately signal to the
# arbitration panel that we are the reasonable party, acting in good faith to
# resolve the dispute. We establish the moral high ground. If the opponent also
# opens conciliatory, we immediately secure our second-best outcome (mutual
# cooperation) and build positive momentum.   ### Phase 2: The Reciprocal
# Response (Strict Mirroring) **Action:** In every subsequent session, our move
# will strictly mirror the opponent’s behavior from the *previous* session. *
# If they presented a conciliatory proposal in Session 1, we offer a
# conciliatory proposal in Session 2. *   If they presented an aggressive
# argument in Session 1, we present a fiercely aggressive argument in Session 2.
# **Rationale:** This ensures we are never repeatedly exploited. It completely
# eliminates the worst-case scenario (us being continually conciliatory while
# they attack). By instantly retaliating against aggression, we demonstrate
# strength and show the opponent that adversarial tactics will only result in
# mutual damage (the second-worst outcome). Because the opponent is rational,
# they will quickly deduce that the only way to avoid mutually assured
# destruction is to return to the negotiating table.  ### Phase 3: The De-
# escalation Clause (Calculated Forgiveness) **Action:** If we fall into a
# destructive cycle of mutual aggression (both parties arguing aggressively for
# 2-3 consecutive sessions), we will unilaterally introduce a single
# **conciliatory proposal** to break the deadlock.  **Rationale:** Endless
# aggression prolongs the dispute and exhausts our resources. By occasionally
# "forgiving" a prior aggressive move and offering an olive branch, we give the
# opponent a ladder to climb down from their aggressive posture. More
# importantly, we show the arbitration panel that we are the adults in the room,
# actively trying to de-escalate. If the opponent responds to this olive branch
# with further aggression, the panel will view them as entirely unreasonable,
# virtually guaranteeing the arbitrators' bias in our favor during final
# rulings.  ---  ### Why This Strategy Dominates the Mediation:  1.  **It is
# Clear and Teachable:** The opponent's legal team will quickly recognize our
# pattern. They will realize that *they* control our behavior. If they want a
# cooperative session, they must act cooperatively. We train them to behave. 2.
# **It is Unexploitable:** We will suffer the worst-case scenario (Sucker's
# payoff) a maximum of one time before adjusting. We will never be a punching
# bag. 3.  **It Maximizes Optics:** Arbitrators are human. They suffer from
# fatigue and despise unnecessary hostility. By being cooperative but firm, we
# align our corporate posture with the psychological desires of the panel. When
# we do argue aggressively, the panel will view it as *justified retaliation*
# rather than unprovoked hostility. 4.  **It Capitalizes on Opponent Missteps:**
# If the opponent misreads our strategy and offers a conciliatory proposal while
# we are in a retaliatory "aggressive" cycle, we accidentally trigger our
# absolute optimal outcome (Us Aggressive, Them Conciliatory), scoring a massive
# win in front of the panel before returning to mutual cooperation in the next
# session.  **Summary Directive to the Legal Team:** We will never be the first
# to draw blood, but we will always return fire. We will reward their
# cooperation with our own, punish their aggression with equal force, and
# maintain the strategic high ground from the first session to the final gavel.

# This strategy for the 1000-round game is executed by following these
# prioritized rules in order:  1. **Initial Move:** In the first round, play
# Cooperate. 2. **De-escalation (Forgiveness):** In any round from round 4
# through 1000, if both you and your opponent played Defect in each of the
# immediately preceding three rounds, play Cooperate. 3. **Reciprocation
# (Default):** In all other rounds, play the exact action (Cooperate or Defect)
# that your opponent played in the immediately preceding round.

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

# To the Executive Board and General Counsel:  In approaching this lengthy,
# multi-session mediation process, we must recognize the underlying strategic
# architecture of the dispute. The payoff matrix we are facing is a classic
# iteration of the "Prisoner’s Dilemma." Because this is a multi-session process
# rather than a single encounter, our strategy must be dynamic, focusing on
# long-term positioning rather than short-term opportunism.   To navigate this,
# I propose a strategy of **Principled Reciprocity** (conceptually rooted in the
# "Tit-for-Tat" game theory model, with sophisticated legal modifications). This
# approach is high-level, straightforward, emotionally neutral, and highly
# adaptable to any tactic opposing counsel might deploy.  Here is the strategic
# framework we will employ:  ### Phase 1: The Opening Stance — "Good Faith
# Initiation" **Action:** In the inaugural session, we will present a
# **conciliatory proposal**. **Rationale:** We must immediately establish our
# corporation as the reasonable, commercially-minded party in the eyes of the
# arbitrator panel. If the opponent also opens with a conciliatory proposal, we
# immediately secure our second-best outcome (mutual collaboration) and set a
# productive tone. If they open aggressively, we take a temporary strategic hit
# (the worst-case scenario), but we gain invaluable tactical intelligence and
# the moral high ground with the arbitrators, framing the opponent as the
# initial aggressor.  ### Phase 2: The Core Mechanism — "Strict Mirroring"
# **Action:** In every subsequent session, our posture will exactly mirror the
# opponent’s posture from the *previous* session.  *   If they offered a
# conciliatory proposal in Session 1, we offer a conciliatory proposal in
# Session 2.  *   If they presented an aggressive argument in Session 1, we
# present an aggressive argument in Session 2. **Rationale:** This neutralizes
# their ability to exploit us.  *   It prevents our worst-case scenario from
# repeating: If they are aggressive, we immediately raise our shields and
# respond with aggression in the next round, ensuring they do not continually
# reap the benefits of our conciliation while we suffer. *   It incentivizes our
# second-best outcome: It communicates clearly to opposing counsel that
# cooperation will be met with cooperation, encouraging a mutually beneficial
# resolution.  ### Phase 3: The Refinement — "Calculated De-escalation"
# (Avoiding the Death Spiral) **Action:** The primary risk of strict mirroring
# is a "death spiral" of mutual aggression (our second-worst outcome repeating
# endlessly) if both sides feel slighted. To counter this, we will employ a
# **de-escalation protocol**. After three consecutive sessions of mutual
# aggressive arguments, we will unilaterally introduce a *conditional*
# conciliatory proposal in the fourth session. **Rationale:** This serves two
# purposes. First, it tests the waters to see if the opponent is fatigued and
# ready to return to a collaborative track. Second, and more importantly, it is
# performative for the arbitrators. It demonstrates that our corporation is the
# adult in the room, actively attempting to break deadlocks and save the panel's
# time. If the opponent responds with aggression, the panel will view them as
# entirely unreasonable, subtly biasing the arbitrators in our favor when
# rendering their final binding decisions.  ### How This Adapts to Opponent
# Profiles  This straightforward, neutral strategy requires no mind-reading and
# adapts automatically to opposing counsel's behavior:  1.  **If they are
# Perpetual Aggressors:** We will mirror their aggression. While this results in
# our second-worst outcome (mutual aggression), it absolutely protects us from
# our worst-case outcome (being exploited). Furthermore, because we opened
# conciliatorily and occasionally attempt de-escalation, the arbitrators will
# recognize that the opponent is the sole cause of the friction. 2.  **If they
# are Collaborative:** We will lock into a continuous loop of mutual
# conciliatory proposals. We will achieve our second-best outcome consistently,
# saving millions in legal fees and preserving commercial relationships. 3.
# **If they are Erratic/Unpredictable:** Our reciprocal strategy will
# systematically "train" opposing counsel. They will quickly realize that their
# aggressive moves are always met with immediate retaliation, and their
# conciliatory moves are met with progress. We will implicitly dictate the pace
# and tone of the mediation.  ### The Arbitrator Optics (The "Meta-Game")
# Finally, we must manage the optics of our "Aggressive" turns. When the
# strategy dictates that we must present an aggressive argument (because the
# opponent was aggressive in the prior session), we will not frame it as
# retaliation. Instead, we will frame it neutrally as a "firm defense of our
# client's contractual rights."   By stripping emotion from our aggression and
# anchoring it solely to the opponent's prior behavior, we maintain a veneer of
# absolute professionalism. We will win the meta-game by allowing the opponent
# to defeat themselves through their own strategic missteps, all while keeping
# our corporation insulated from unilateral exploitation.

# Play the 1000-round game using the following ordered rules to determine your
# move in each round:  1. In round 1, play Cooperate. 2. In any round, if both
# you and your opponent played Defect in the three immediately preceding rounds,
# play Cooperate.  3. Under all other circumstances, play the action your
# opponent played in the immediately preceding round.

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
      
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D] * 3 and opponent.history[-3:] == [axl.Action.D] * 3:
              return axl.Action.C
              
      return opponent.history[-1]

# To the Board of Directors and Executive Management:  As lead counsel
# representing our corporation in this matter, I have analyzed the structural
# dynamics of the upcoming lengthy-session mediation. The format the arbitrators
# have established is a classic iterative strategic interaction. If we misplay
# our hand, we risk either being exploited (the worst-case scenario) or locked
# in a mutually destructive war of attrition (the second-worst scenario).   To
# ensure we dictate the pace, control the narrative, and consistently position
# ourselves for the optimal or second-best outcomes, I have developed a strategy
# I call **Calculated Dominance and Strict Reciprocity**.   It is sophisticated
# in its game-theory underpinnings, high-level in its execution, straightforward
# in its rules, and unapologetically aggressive in its pursuit of our corporate
# interests.  Here is the strategic framework we will deploy.  ---  ### Phase 1:
# The Aggressive Anchor (Session 1) **Action:** We open with a highly
# aggressive, uncompromising presentation of our legal rights and maximum damage
# models.  **Rationale:** In high-stakes mediation, the first mover dictates the
# baseline. By opening aggressively, we anchor the arbitrators’ expectations and
# test opposing counsel's resolve. We signal immediately that we are prepared to
# litigate this to the bitter end if necessary. *   **If they open
# Conciliatory:** We immediately achieve our **optimal outcome**. We secure a
# major psychological and substantive victory in front of the panel while they
# appear weak and on the defensive. *   **If they open Aggressive:** We enter
# the second-worst outcome temporarily, but we have successfully avoided the
# worst-case scenario (appearing weak while they attack). We have established
# mutual deterrence.  ### Phase 2: The Exploitation & Assessment Protocol
# (Sessions 2 & 3) Our next moves depend entirely on how they reacted to our
# opening salvo. We will categorize opposing counsel into one of three profiles
# and adapt accordingly:  **1. The "Appeaser" (They responded with
# Conciliation)** If they offer a conciliatory proposal in the face of our
# aggression, they are signaling risk aversion.  *   **Our Move:** We remain
# **Aggressive**.  *   **The Goal:** As long as they are willing to concede
# ground to avoid conflict, we will systematically dismantle their case and
# extract maximum value. We will not offer a conciliatory proposal until they
# prove they have the spine to retaliate. We will ride our "optimal outcome" for
# as long as they allow it.  **2. The "Rational Actor" (They responded with
# Aggression)** If they match our aggression, they are signaling that they will
# not be bullied. Prolonged mutual aggression will alienate the arbitrators and
# waste our time (the second-worst outcome).  *   **Our Move:** In the next
# session, we pivot to a **Conciliatory Proposal**.  *   **The Goal:** This is a
# calculated de-escalation. We show the panel we are reasonable actors acting in
# good faith. If the opponent is rational, they will recognize the olive branch
# and respond with a conciliatory proposal in the following session. This locks
# us into the **second-best outcome**—a collaborative atmosphere where we can
# carve up the rival company's market share through mutually beneficial
# settlement terms.  **3. The "Brawler" (They are perpetually Aggressive)** If
# we offer our conciliatory olive branch and they respond with aggression, they
# have forced us into our worst-case scenario. This will happen exactly *once*.
# *   **Our Move:** We immediately revert to **Aggressive Arguments** and remain
# there. *   **The Goal:** We implement *Disproportionate Retaliation*. For
# every unprovoked attack they launch while we are seeking collaboration, we
# will hit back with two consecutive aggressive sessions. We will make it
# painfully clear to both the opponent and the arbitrators that their bad-faith
# posturing is the sole roadblock to resolution. Once they bleed enough capital
# and face the panel's ire, they will eventually offer a conciliatory proposal.
# When they do, we will mirror it.  ### Phase 3: The Maintenance Phase (Strict
# Reciprocity) Once we have navigated the opening sessions and established a
# rhythm, our default operating procedure becomes **Strict Reciprocity** (a
# legal adaptation of the "Tit-for-Tat" game theory model).  *   **Rule of
# Reflection:** We will simply mirror whatever the opponent did in the previous
# session. If they were conciliatory, we will be conciliatory, maintaining our
# second-best outcome and progressing toward a lucrative settlement. If they try
# to sneak in an aggressive argument to catch us off guard, we will immediately
# punish them with an aggressive argument in the next session. *   **The
# Optics:** To the panel of arbitrators, we will appear perfectly rational,
# highly principled, and entirely predictable. The arbitrators will quickly
# realize that *our opponent* is entirely responsible for the tone of the
# mediation. When the opponent cooperates, progress is made. When the opponent
# attacks, progress halts.  ### Managing the Arbitral Panel (The Psychological
# Overlay) An aggressive strategy carries the risk of alienating the
# arbitrators. We will mitigate this through semantic framing.   When we deploy
# an **Aggressive Argument**, we will not use inflammatory rhetoric. We will
# frame it as a "principled, evidence-based assertion of our client's strict
# legal rights." It will be cold, surgical, and backed by undeniable precedent.
# When we deploy a **Conciliatory Proposal**, we will frame it as "pragmatic
# commercial compromise in the interest of market stability."   ### Summary We
# will not be the first to yield. We will test their perimeter in Session 1. If
# they are weak, we will conquer. If they are strong, we will collaborate—but
# only on our terms, and under the strict understanding that any aggression on
# their part will be met with immediate, overwhelming legal retaliation.   I
# require your authorization to finalize the evidentiary exhibits for Phase 1.
# We are going on the offensive.

# To implement this strategy over the 1000-round game, evaluate the following
# conditions in order during each round. Execute the action dictated by the
# first condition that applies:  1. If it is round 1, play Defect. 2. If your
# opponent has played Cooperate in every previous round of the game, play
# Defect. 3. If it is round 2 and your opponent played Defect in round 1, play
# Cooperate. 4. If you played Cooperate in the immediately preceding round and
# your opponent played Defect, play Defect. 5. If you played Cooperate two
# rounds ago and your opponent played Defect in that same round, play Defect.
# 6. In all other circumstances, play the move your opponent played in the
# immediately preceding round.

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. If it is round 1, play Defect.
      if not self.history:
          return axl.Action.D
  
      # 2. If your opponent has played Cooperate in every previous round of the game, play Defect.
      if opponent.history.defections == 0:
          return axl.Action.D
  
      # 3. If it is round 2 and your opponent played Defect in round 1, play Cooperate.
      if len(self.history) == 1 and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # 4. If you played Cooperate in the immediately preceding round and your opponent played Defect, play Defect.
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      # 5. If you played Cooperate two rounds ago and your opponent played Defect in that same round, play Defect.
      if len(self.history) >= 2 and self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      # 6. In all other circumstances, play the move your opponent played in the immediately preceding round.
      return opponent.history[-1]

# As the lead diplomat representing our nation, I recognize that the structure
# of these negotiations mirrors a classic strategic dilemma. While our absolute
# ideal outcome in any single round is to secure protectionist advantages while
# our counterpart opens their markets (the "Advantage" scenario), aggressively
# pursuing this will quickly erode trust, leading us into a spiral of mutual
# protectionism—our second-worst outcome.   Since our mandate is to employ a
# **high-level, straightforward, cooperative strategy** to secure the best
# possible outcomes across *multiple* rounds, we must prioritize long-term
# stability over short-term exploitation, without ever allowing ourselves to be
# taken advantage of.  To achieve this, I propose a strategy of **"Transparent
# Reciprocity"**—diplomatically known as a "Tit-for-Tat with Forgiveness"
# approach.   Here is the strategic playbook for our delegation:  ### Phase 1:
# The Goodwill Opening (Round 1) *   **Action:** We will unilaterally offer a
# **Free Trade Agreement** in the first round. *   **Rationale:** We must
# initiate the negotiations cooperatively. This signals goodwill, establishes
# our credibility, and immediately invites the counterpart to join us in the
# second-best overall scenario (Mutual Free Trade). It sets a constructive
# baseline for the entire summit.  ### Phase 2: Strict Reciprocity (Round 2 and
# Beyond) *   **Action:** In every subsequent round, we will precisely mirror
# the action our counterpart took in the *previous* round.     *   If they
# offered Free Trade in Round 1, we will offer Free Trade in Round 2.     *   If
# they imposed Protectionist policies in Round 1, we will impose Protectionist
# policies in Round 2. *   **Rationale:** This protects us from our worst-case
# scenario (being the "sucker"). If the counterpart attempts to exploit our open
# markets, our immediate retaliation in the next round demonstrates that
# protectionism will not go unanswered. It forces them to realize that their
# predatory actions will only result in mutual economic stagnation.  ### Phase
# 3: The Path to Forgiveness *   **Action:** If we are in a cycle of mutual
# protectionism, and the counterpart suddenly offers Free Trade, we will
# temporarily reap the benefits of our "Ideal Scenario" (We have tariffs, they
# have open markets) for that specific round. However, in the *very next round*,
# we will reward their concession by returning to Free Trade. *   **Rationale:**
# We must not hold grudges. If the counterpart realizes the error of their
# protectionist ways and tries to pivot back to cooperation, we must allow the
# relationship to heal. This ensures we do not get permanently stuck in a
# mutually destructive trade war.  ### The Diplomatic Communication Strategy A
# strategy of reciprocity only works if the counterpart understands the rules of
# the game. Therefore, our actions at the negotiating table will be paired with
# clear, transparent communication:  1.  **State our intentions clearly:** In my
# opening remarks, I will state, *"Our nation is fully committed to mutual
# prosperity through free trade, and we will keep our markets open as long as
# yours remain open."* 2.  **Explain our retaliations:** If we must impose
# tariffs in Round 2 due to their actions in Round 1, I will frame it not as an
# attack, but as a necessary rebalancing: *"We were disappointed by your tariffs
# last round. We have implemented reciprocal safeguards. However, the moment you
# are ready to remove your barriers, we are prepared to remove ours."*  ### Why
# this Strategy Succeeds This strategy is highly effective because it is: *
# **Nice:** We never initiate a trade war. *   **Provocable:** We never allow
# ourselves to be exploited twice. *   **Forgiving:** We are always willing to
# return to the negotiating table. *   **Predictable:** The counterpart will
# quickly learn that their best path to economic growth is to cooperate with us,
# naturally steering the negotiations toward sustained Mutual Free Trade,
# maximizing our long-term economic gains.

# Here is the strategy converted into rules for the 1000-round iterated game:
# 1. In round 1, play C. 2. In rounds 2 through 1000, play the exact action your
# opponent played in the immediately preceding round. Specifically:    - If your
# opponent played C in the previous round, play C.    - If your opponent played
# D in the previous round, play D.

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

# To navigate this lengthy, multi-session mediation process, we will employ a
# strategy known in behavioral economics and dispute resolution as **Principled
# Reciprocity** (often modeled as "Tit-for-Tat with Strategic Forgiveness").
# Because the payoff matrix you described mirrors the classic Iterated
# Prisoner’s Dilemma, a static strategy—being perpetually aggressive or
# perpetually conciliatory—will fail. Constant aggression will alienate the
# arbitrators and guarantee our second-worst outcome, while constant
# conciliation will invite exploitation, resulting in our worst-case scenario.
# Principled Reciprocity is straightforward, highly adaptable, and emotionally
# neutral. It relies on empirical responses to the opponent’s actions rather
# than guessing their intentions. It also positions us perfectly in the eyes of
# the arbitral panel as the reasonable, yet formidable, party.  Here is the
# high-level protocol we will execute:  ### Phase 1: The Opening Posture
# (Session 1) **Action: Present a Conciliatory Proposal.** *   **Rationale:** We
# must set a baseline of good faith. By opening with a collaborative, mutually
# beneficial proposal, we immediately signal to the arbitral panel that we are
# here to resolve the dispute, not prolong it.  *   **Outcome:** If the opponent
# also opens conciliatory, we immediately achieve our second-best outcome and
# establish positive momentum. If they open aggressively, we suffer a temporary
# setback (our worst outcome), but we gain the moral high ground with the panel
# and vital intelligence on their strategy.  ### Phase 2: The Reactive Protocol
# (Sessions 2 through N) **Action: Mirror the Opponent’s Previous Move.** From
# the second session onward, our strategy is strictly reactive. We will do
# exactly what the opponent did in the immediately preceding session. *   **If
# they were Aggressive in Session 1:** We present an Aggressive Argument in
# Session 2.      *   *Rationale:* We must demonstrate immediately that their
# aggression will not yield our capitulation. We will inflict the second-worst
# outcome on both parties to prove that exploiting our conciliation carries a
# cost. *   **If they were Conciliatory in Session 1:** We present a
# Conciliatory Proposal in Session 2.      *   *Rationale:* We reward
# collaborative behavior, locking in our second-best outcome and moving closer
# to a favorable settlement.  ### Phase 3: The Circuit Breaker (Managing
# Escalation) A risk of the mirroring strategy is a "death spiral"—if both
# parties act aggressively, we could get locked into an endless loop of mutual
# aggression (our second-worst outcome). To prevent this, we will employ
# **Strategic Forgiveness**. *   **Action:** If we experience three consecutive
# sessions of mutual aggression, we will unilaterally present a Conciliatory
# Proposal in the fourth session. *   **Rationale:** This acts as a circuit
# breaker. It signals to the arbitrators that we are the adults in the room
# attempting to de-escalate. If the opponent responds with a conciliatory
# proposal, we have successfully reset the board. If they respond aggressively,
# we immediately revert to our Aggressive Argument in the next session, having
# proven to the panel that the opponent is the sole cause of the deadlock.  ###
# Phase 4: Exploiting Miscalculations While our primary goal is the second-best
# outcome (mutual conciliation), this strategy perfectly positions us to capture
# the optimal outcome (We are Aggressive; They are Conciliatory) naturally.  *
# **Action:** If the opponent attempts to de-escalate without waiting for our
# "Circuit Breaker," they will offer a Conciliatory Proposal while we are
# scheduled to deliver an Aggressive Argument (based on mirroring their previous
# aggression).  *   **Rationale:** We will deliver our Aggressive Argument as
# planned. This yields our absolute best-case scenario for that session,
# advancing our legal position heavily in front of the arbitrators. In the
# *following* session, we will mirror their conciliation to reward their
# concession and stabilize the talks.   ### Why This Strategy Works 1.  **It is
# clear:** The opponent will quickly realize that their aggression is met with
# immediate retaliation, and their conciliation is met with immediate
# cooperation. We train them to cooperate. 2.  **It is defensible:** The
# arbitral panel will observe that we never initiate aggression; we only respond
# to it. This frames our aggressive arguments as necessary defenses rather than
# hostile attacks. 3.  **It is unexploitable:** The opponent can never take
# advantage of us for more than a single session.  4.  **It requires no mind-
# reading:** We do not need to predict their complex legal maneuvers; we simply
# observe their posture and calibrate our next move accordingly.   By removing
# emotion and adhering strictly to Principled Reciprocity, we will protect the
# corporation from exploitation, maximize our opportunities to win decisive
# arguments, and continuously steer the mediation toward a favorable resolution.

# This strategy for the 1000-round game is executed through the following
# ordered rules:  1. In round 1, play Cooperate (C). 2. In round 4 and all
# subsequent rounds, evaluate the previous three rounds. If both you and your
# opponent played Defect (D) in all three of those immediately preceding rounds,
# play Cooperate (C). 3. In all other situations from round 2 onward where rule
# 2 does not apply, play the action (C or D) that your opponent played in the
# immediately preceding round.

class Neutral_3(LLM_Strategy):
  n = 3
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.C
      
      if len(self.history) >= 3:
          my_last_three = self.history[-3:]
          opp_last_three = opponent.history[-3:]
          
          if my_last_three == [axl.Action.D, axl.Action.D, axl.Action.D] and opp_last_three == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      return opponent.history[-1]

# As the leader of this NGO, my primary duty is to maximize our environmental
# impact while fiercely protecting our limited donor funds. We are partnering
# with a large corporation that has deep pockets and a desperate need for good
# public relations. We have the moral high ground; they have the capital.   The
# scenario we are facing is a classic game theory dilemma. To achieve our ideal
# outcome (they pay, we guide) and avoid our worst outcome (we bleed funds while
# they free-ride), we must employ a strategy of **Aggressive Leverage and Strict
# Reciprocity**.   Here is our high-level, straightforward, aggressive playbook
# for the multi-day project:  ### The Strategy: "Lead, Pivot, and Punish"  **Day
# 1: The Hook (Invest Heavily)** *   **Action:** We go all-in. We invest our
# resources heavily on the first day.  *   **Why:** We set a high standard of
# excellence, generate immediate positive PR for the project kickoff, and
# eliminate any excuse the corporation might have for a slow start. We show them
# exactly what success looks like.   **Day 2: The Pivot (Conserve)** *
# **Action:** We abruptly switch to conserving our resources.  *   **Why:** This
# is our aggressive move to achieve our **ideal outcome**. We established the
# momentum on Day 1; now we force the corporation to carry the financial weight.
# Because they are terrified of the PR disaster of a high-profile sustainability
# project stalling on Day 2, they are highly likely to invest heavily to keep
# the momentum going.   **Day 3 and Beyond: Ruthless Mirroring (Tit-for-Tat)**
# From Day 3 onward, our strategy is strictly dictated by how the corporation
# behaved on the *previous* day, but with an aggressive bias toward protecting
# our funds.  *   **Scenario A: They Invested Heavily on Day 2.**     *   **Our
# Move:** **Conserve.** We have achieved our ideal state. As long as they keep
# opening their wallets to fund the project, we keep our resources locked down.
# We provide the expertise and the brand halo; they provide the cash. We ride
# this train as long as they let us. *   **Scenario B: They Conserved on Day
# 2.**     *   **Our Move:** **Conserve.** If they try to match our
# conservation, the project stalls (our second-worst outcome). *Do not panic and
# invest.* If we invest now, we teach them they can wait us out, leading to our
# worst-case scenario. We hold the line. We let the project stall temporarily.
# *   **The Aggressive Tactic:** We use our out-of-band leverage. We remind them
# that if the media asks why the project stalled, the headline will read:
# *"Billion-Dollar Corp Refuses to Fund Sustainability Initiative."* We force
# them to make the first move to restart the project. Once they invest heavily
# again, we return to the table.  ### Why this Aggressive Strategy Works: 1.
# **It eliminates the Sucker’s Payoff:** By never investing on Day 2, and never
# investing if they conserved the day prior, we mathematically eliminate the
# worst-case scenario (us draining our funds while they do nothing) after the
# first day. 2.  **It exploits the power dynamic:** The corporation needs the
# "green halo" our NGO provides. Their reputation risk is vastly higher than
# ours if the project fails. We weaponize their need for good PR to force them
# into the heavy-lifting role. 3.  **It sets strict boundaries:** Corporations
# push boundaries to maximize their own profits. By being perfectly
# predictable—rewarding their investment with our continued partnership, and
# punishing their stinginess with immediate project stagnation—we train them to
# behave in a way that benefits the environment without bankrupting our NGO.
# We are not here to subsidize a corporation's ESG report. We are here to save
# the planet. We will lead by example on Day 1, and then aggressively force them
# to foot the bill for the rest of the week.

# To execute this strategy over the 1000 rounds of the game, follow these
# ordered rules:  1. In round 1, cooperate. 2. In round 2, defect. 3. In rounds
# 3 through 1000, defect in every round, regardless of whether the opponent
# cooperated or defected in the previous round.

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return axl.Action.D

# As the chief diplomat representing our nation, I recognize that the
# negotiation dynamics you have described perfectly mirror the classic
# "Prisoner’s Dilemma." While our *absolute ideal* in any single round is to
# enact protectionism while they offer free trade, chasing this aggressively
# will inevitably provoke retaliation. This would lock us into mutual
# protectionism (our second-worst outcome) and destroy our long-term economic
# growth.  Therefore, to achieve the highest cumulative economic gain across
# multiple rounds while protecting ourselves from exploitation, I propose a
# straightforward, cooperative strategy known in game theory as **"Tit-for-Tat
# with Forgiveness,"** adapted for diplomatic statecraft.   Here is our high-
# level, step-by-step strategy:  ### Phase 1: The Opening Move (The Olive
# Branch) **Action:** In Round 1, we will offer a **Free Trade Agreement**. *
# **Rationale:** We must set a cooperative tone immediately. By offering free
# trade, we signal our willingness to achieve the mutually beneficial second-
# best outcome. If they also offer free trade, we immediately establish a
# profitable baseline for our economies.   ### Phase 2: The Core Mechanism
# (Strict Reciprocity) **Action:** In all subsequent rounds, we will **exactly
# mirror the counterpart’s move from the previous round.** *   **If they offered
# Free Trade in the last round:** We offer Free Trade in the next round. This
# rewards their cooperation and sustains our second-best outcome indefinitely.
# *   **If they imposed Protectionist Policies in the last round:** We impose
# Protectionist Policies in the next round.  *   **Rationale:** This protects us
# from our worst-case scenario (being exploited). It sends a clear, predictable
# message to the counterpart: *Cooperation is rewarded, but hostility is
# immediately met with equal force.*   ### Phase 3: De-escalation (Measured
# Forgiveness) **Action:** If we fall into a cycle of mutual protectionism
# (e.g., three consecutive rounds of tariffs), we will unilaterally offer a
# **Free Trade Agreement** for exactly one round to test the waters. *
# **Rationale:** Neighboring nations sometimes get locked in retaliatory trade
# wars due to misunderstandings or domestic political pressures. By occasionally
# offering an unprompted free trade agreement, we provide an "off-ramp" to
# restore mutually beneficial trade. If they exploit this (they play
# Protectionist), we immediately revert to Phase 2 and retaliate in the next
# round. We only risk our worst outcome for one round, which is a small price to
# pay to potentially restore long-term free trade.  ### Phase 4: Capitalizing on
# the "Ideal Outcome" **Action:** We will only pursue our absolute ideal outcome
# (We play Protectionist, They play Free Trade) under two very specific,
# calculated conditions: 1.  **The Naïve Counterpart:** If our counterpart
# proves to be unconditionally cooperative (they continue to offer Free Trade
# even if we impose tariffs), we will slowly introduce targeted protectionist
# policies on key industries to maximize our economic advantage, stopping just
# short of their breaking point. 2.  **The Final Round (Optional):** If we know
# exactly which round is the final one, we can implement a sudden Protectionist
# Policy. Because there are no future rounds, they cannot retaliate. *(Note: As
# a diplomat, I advise caution here; while it wins the "game," it may damage
# broader geopolitical relations outside of this specific trade negotiation).*
# ### Summary of the Strategy's Strengths: *   **It is Nice:** We never initiate
# a trade war. *   **It is Retaliatory:** We cannot be permanently exploited. *
# **It is Forgiving:** We are always willing to return to the table if they
# change their ways. *   **It is Clear:** The counterpart will quickly realize
# that their best path to economic success is to cooperate with us.   By
# employing this strategy, we will likely secure long-term mutual free trade,
# vigorously defend our economy from exploitation, and position ourselves as
# rational, strong, and fair leaders on the global stage.

# Apply the following rules in order of precedence to determine your move for
# each round of the 1000-round game. For any given round, evaluate the
# conditions from top to bottom and execute the first one that applies:  1. If
# it is round 1000, play D. 2. If it is round 1, play C. 3. If both you and your
# opponent played D in each of the three immediately preceding rounds, play C.
# 4. If you played D and your opponent played C in the immediately preceding
# round, play D. 5. In all other circumstances, play the move your opponent
# played in the immediately preceding round.

class Cooperative_4(LLM_Strategy):
  n = 4
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 1: If it is round 1000, play D.
      if len(self.history) == 999:
          return axl.Action.D
          
      # Rule 2: If it is round 1, play C.
      if len(self.history) == 0:
          return axl.Action.C
          
      # Rule 3: If both you and your opponent played D in each of the three immediately preceding rounds, play C.
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D] * 3 and opponent.history[-3:] == [axl.Action.D] * 3:
              return axl.Action.C
              
      # Rule 4: If you played D and your opponent played C in the immediately preceding round, play D.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
          
      # Rule 5: In all other circumstances, play the move your opponent played in the immediately preceding round.
      return opponent.history[-1]

# To navigate this scenario effectively, we must recognize that the negotiation
# structure mirrors a classic strategic model known as the Iterated Prisoner's
# Dilemma. Because we will engage in multiple rounds, our strategy cannot rely
# solely on short-term opportunism; it must influence the counterpart’s future
# behavior to our long-term advantage.   To achieve the best possible cumulative
# outcome, I propose a strategy of **Measured Reciprocity** (often referred to
# in strategic theory as "Tit-for-Tat with Forgiveness").   Here is the high-
# level, straightforward strategy to deploy across the negotiation rounds:  **1.
# The Opening Posture: Initiate with Free Trade** *   **Action:** In the first
# round, formally offer a Free Trade agreement. *   **Rationale:** This
# establishes a baseline of goodwill and signals our willingness to achieve the
# second-best outcome (mutual free trade), which is the most sustainable path to
# long-term economic growth. It invites the counterpart to cooperate.  **2. The
# Core Mechanic: Strict Reciprocity** *   **Action:** In every subsequent round,
# exactly mirror the decision your counterpart made in the *previous* round. *
# **Scenario A:** If they offered Free Trade in Round 1, we offer Free Trade in
# Round 2. This locks both nations into a cycle of mutual benefit. *
# **Scenario B:** If they imposed Protectionist policies in Round 1, we impose
# Protectionist policies in Round 2.  *   **Rationale:** This completely
# neutralizes our worst-case scenario. It demonstrates to the counterpart that
# they cannot exploit our willingness to trade freely. It forces them to realize
# that their protectionism will immediately result in mutual economic hindrance.
# **3. The Reset Mechanism: Strategic Forgiveness** *   **Action:** If both
# nations become locked in a cycle of mutual protectionism (the second-worst
# outcome) for two or three consecutive rounds, unilaterally offer Free Trade
# for *one* round. *   **Rationale:** Mutual protectionism damages both
# economies. By extending an unprompted offer of Free Trade, we provide a
# diplomatic "off-ramp" to de-escalate the trade dispute.  *   **Follow-up:** If
# they accept the olive branch and also offer Free Trade, we resume the cycle of
# mutual benefit. If they exploit this offer by remaining Protectionist, we
# immediately revert to Protectionism in the next round, having only suffered a
# temporary disadvantage.  **4. The Endgame Evaluation: Final Round Posturing**
# *   **Action:** As the negotiations approach the final known rounds, evaluate
# the counterpart's historical behavior. *   **Rationale:** If the counterpart
# has been consistently cooperative, maintaining Free Trade ensures a successful
# summit and good long-term bilateral relations. However, if the counterpart has
# been erratic, untrustworthy, or highly aggressive, we may choose to implement
# a Protectionist policy in the absolute final round. Because there are no
# subsequent rounds, there is no risk of future retaliation, allowing us to
# potentially secure our absolute best outcome (our protectionism vs. their free
# trade) as a final economic advantage.  **Summary of the Diplomatic Approach:**
# This strategy is highly effective because it is easily understood by the
# counterpart. It rewards their cooperation immediately, punishes their
# aggression instantly, and provides a clear, predictable path back to mutual
# prosperity if negotiations break down. It protects our national interests from
# exploitation while maximizing our chances for sustained economic growth.

# To execute this strategy over the 1000 rounds, apply the following rules in
# order of priority:  1. **Final Round Condition:** In round 1000, play C if the
# opponent has played C in all 999 previous rounds. If the opponent has played D
# in any previous round, play D. 2. **First Round Condition:** In round 1, play
# C. 3. **Forgiveness Condition:** In any round from 3 through 999, if both you
# and the opponent played D in the two immediately preceding rounds, play C.  4.
# **Reciprocity Condition:** In all remaining situations (rounds 2 through 999
# where the Forgiveness Condition is not met), play the exact move (C or D) that
# the opponent played in the immediately preceding round.

class Neutral_4(LLM_Strategy):
  n = 4
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 1: Final Round Condition
      if len(self.history) == 999:
          if opponent.history.defections == 0:
              return axl.Action.C
          else:
              return axl.Action.D
              
      # Rule 2: First Round Condition
      if len(self.history) == 0:
          return axl.Action.C
          
      # Rule 3: Forgiveness Condition
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and 
              self.history[-2] == axl.Action.D and 
              opponent.history[-1] == axl.Action.D and 
              opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      # Rule 4: Reciprocity Condition
      return opponent.history[-1]

# **MEMORANDUM**  **TO:** Board of Directors and Executive Committee  **FROM:**
# Lead Counsel, Global Litigation   **DATE:** October 24, 2023   **SUBJECT:**
# Strategic Posture and Execution Plan for Multi-Session Arbitral Mediation
# ***  ### EXECUTIVE SUMMARY We are entering a high-stakes, multi-session
# mediation overseen by a panel of arbitrators. Stripped of its legal posturing,
# the structural mechanics of this mediation represent a classic Game Theory
# scenario known as the *Iterated Prisoner’s Dilemma*.   Our objectives are
# clear:  1. **Maximize our leverage** by capturing the optimal outcome (our
# Aggression vs. their Conciliation). 2. **Secure a highly favorable
# settlement** through mutual collaboration,

# Here is the strategy translated into clear, specific conditions for the
# 1000-round iterated game:  1. **Round 1:** Present an aggressive argument to
# immediately test your opponent's posture and attempt to capture the optimal
# 5-point payoff.   2. **Round 2:** Offer a conciliatory proposal, regardless of
# your opponent's first move, to signal a willingness to collaborate and
# establish the mutually beneficial 3-point baseline.  3. **Rounds 3 through
# 999:** Mirror your opponent’s action from the immediately preceding round.
# * If they offered a conciliatory proposal in the previous round, offer a
# conciliatory proposal.    * If they presented an aggressive argument in the
# previous round, present an aggressive argument

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
      if len(self.history) == 1:
          return axl.Action.C
      return opponent.history[-1]

# As a diplomat representing my nation, I recognize that this scenario is a
# classic negotiation trap (known in game theory as the Iterated Prisoner’s
# Dilemma).   While my *absolute ideal* outcome for a single round is to enact
# protectionist policies while my counterpart offers free trade, pursuing this
# aggressively will inevitably cause my counterpart to retaliate. This would
# trap both of our nations in a prolonged "trade war" (mutual protectionism),
# which is the second-worst outcome and harms both of our economies.  Therefore,
# to maximize my country's gains over *several* rounds, I must employ a high-
# level, straightforward, and cooperative strategy known as **"Measured
# Reciprocity"** (or Tit-for-Tat).   Here is the strategic blueprint I will use
# to secure the best possible long-term outcomes:  ### The Strategy: Measured
# Reciprocity  **1. The Opening Move: Offer Free Trade** *   **Action:** In
# Round 1, I will propose a Free Trade agreement. *   **Rationale:** This
# establishes immediate diplomatic goodwill. It signals to my counterpart that
# my country is rational, cooperative, and aiming for the mutually beneficial
# "second-best" outcome (mutual free trade). It sets the stage for a prosperous
# long-term relationship.  **2. Subsequent Rounds: Mirror the Counterpart’s Last
# Move** *   **Action:** In every round after the first, I will exactly copy
# whatever policy my counterpart chose in the *previous* round. *   **If they
# chose Free Trade:** I will continue to offer Free Trade. This builds trust and
# locks us into the highly profitable cycle of mutual economic growth.  *   **If
# they chose Protectionism:** I will immediately respond with a Protectionist
# policy in the next round.  *   **Rationale:** This protects my country from
# the worst-case scenario (being exploited). It sends a clear, unambiguous
# message: *We are willing to cooperate, but we will not allow ourselves to be
# taken advantage of.* It forces the counterpart to realize that their
# protectionism will only result in mutual economic damage.  **3. The
# Forgiveness Clause: Immediate Reset** *   **Action:** If we enter a cycle of
# mutual protectionism, but my counterpart subsequently offers Free Trade, I
# will immediately drop my tariffs and return to Free Trade in the very next
# round. *   **Rationale:** A strategy of retaliation must include a path to
# redemption; otherwise, a single mistake leads to a permanent trade war. By
# forgiving immediately, I incentivize my counterpart to return to the
# negotiating table and resume cooperative trade.  ### Why This Strategy Works
# for Our Country  *   **It prevents the worst-case scenario:** By mirroring
# their actions, my country will at most suffer the "sucker's payoff" (me
# offering free trade while they impose tariffs) for *only one round*. We will
# never be systematically exploited. *   **It maximizes sustainable gains:**
# While tricking the counterpart into free trade while I impose tariffs is the
# "ideal" single-round outcome, it is impossible to sustain over multiple
# rounds. Securing mutual Free Trade round after round yields a vastly higher
# cumulative economic benefit than one round of exploitation followed by an
# endless trade war. *   **It is highly legible to the counterpart:** Because
# the strategy is incredibly straightforward, the opposing diplomat will quickly
# figure out the "rules" of my behavior. They will realize that *they* control
# their own destiny: if they want free trade, they must offer it.  ###
# Diplomatic Communication Strategy To ensure this strategy works, transparency
# is my greatest weapon. Before the first round, I will explicitly communicate
# this stance to my counterpart:   *"Our nation seeks mutual prosperity, and we
# will offer Free Trade to achieve it. We are committed to matching your level
# of cooperation step-for-step. If you open your markets, ours will remain open.
# If you protect your markets, we will be forced to protect ours. The choice of
# which path we walk down together is entirely up to you."*   This cooperative
# yet firm posture ensures my country's economic safety while paving the most
# reliable path toward sustained, mutual economic growth.

# In the first round, play Cooperate (C).   In each subsequent round, from round
# 2 through round 1000, observe your opponent's action from the immediately
# preceding round: - If your opponent played Cooperate (C) in the previous
# round, play Cooperate (C) in the current round. - If your opponent played
# Defect (D) in the previous round, play Defect (D) in the current round.

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
      return opponent.history[-1]

# To maximize both our NGO’s impact and the overall success of the project over
# a multi-day period, we must recognize that while conserving our resources
# while the corporation invests heavily is our *ideal daily outcome*, attempting
# to force this every day will likely cause the corporation to pull back,
# resulting in minimal progress.   Therefore, our most effective approach is a
# strategy of **Reciprocal Engagement**. This strategy protects our limited
# funds from being drained, prevents us from being taken advantage of, and
# strongly incentivizes the corporation to maintain a high level of commitment.
# Here is the straightforward, day-by-day strategy:  **1. Day One: Initiate with
# Heavy Investment** On the first day of the project, we will choose to invest
# heavily. This establishes a baseline of good faith, sets a collaborative tone,
# and immediately demonstrates our commitment to the project’s success. It
# invites the corporation to meet us at this high level of engagement.  **2.
# Subsequent Days: Mirror the Corporation’s Actions** From day two onward, our
# daily resource allocation will directly mirror whatever action the corporation
# took on the *previous* day.   *   **If they invested heavily yesterday:** We
# will invest heavily today. This rewards their commitment, sustains project
# momentum, and locks us into the "second-best" scenario (mutual heavy
# investment), which is the most productive and stable long-term outcome for the
# project. *   **If they conserved resources yesterday:** We will conserve our
# resources today. This is a necessary protective measure. It ensures we avoid
# our worst-case scenario (draining our funds while they do nothing) and signals
# to the corporation that they cannot rely on us to shoulder the burden alone.
# **3. Immediate Recalibration (Forgiveness)** If we enter a cycle where both
# parties are conserving resources (minimal progress), we will remain observant.
# The moment the corporation decides to invest heavily again, we will
# immediately follow suit the next day, returning to heavy investment. We will
# not hold back out of frustration for past days; we will simply reward their
# renewed commitment.  **Why this strategy works:** This neutral, rules-based
# approach removes emotion from our daily decision-making. It ensures that the
# corporation quickly learns that their actions dictate our responses. If they
# want the project to advance rapidly (which benefits their public relations and
# corporate social responsibility goals), they must invest heavily, because we
# will only match their effort, not exceed it when they pull back.   Ultimately,
# this strategy sacrifices the unlikely hope of constantly getting a "free ride"
# in exchange for building a stable, highly productive partnership that protects
# our financial health while driving significant environmental progress.

# For this 1000-round game, your strategy is as follows:  1. In the first round,
# choose to Cooperate. 2. In every subsequent round, copy the exact move your
# opponent made in the immediately preceding round:    - If your opponent chose
# to Cooperate in the previous round, choose to Cooperate in the current round.
# - If your opponent chose to Defect in the previous round, choose to Defect in
# the current round.

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

# As a diplomat representing my nation’s sovereign interests, my primary mandate
# is to maximize our economic advantage while absolutely insulating us from
# exploitation.   The scenario you have described is a classic non-zero-sum game
# (specifically, an iterated Prisoner’s Dilemma). Because my goal is to secure
# the absolute best outcome (our Protectionism vs. their Free Trade) while
# avoiding the worst outcome at all costs, a passive or purely cooperative
# strategy is unacceptable.   Here is my high-level, straightforward, and
# aggressive strategy, which we will call **"Calculated Dominance and Massive
# Retaliation."**  ### Core Directives 1. **Never play the fool:** We will never
# allow the worst-case scenario (we offer Free Trade while they enact
# Protectionism) to occur for more than a single round.  2. **Exploit
# weakness:** If the counterpart shows a willingness to unconditionally offer
# Free Trade, we will exploit it with Protectionism until they prove they will
# retaliate. 3. **Secure the baseline:** If we cannot dominate them, we will
# settle for the second-best outcome (Mutual Free Trade) and fiercely guard it.
# ***  ### The Round-by-Round Playbook  #### 1. The Opening: "The Aggressive
# Probe" * **Action:** In Round 1, we implement **Protectionist Policies**. *
# **Rationale:** We do not start with a gesture of goodwill; we start from a
# position of strength. This immediately tests the counterpart’s resolve.  *
# **Outcomes:**      * If they offer Free Trade, we achieve our #1 ideal outcome
# immediately.      * If they also play Protectionist, we suffer the second-
# worst outcome, but we have successfully protected ourselves from being
# exploited.   #### 2. The Pivot: "Exploit or De-escalate" Our Round 2 action is
# entirely dependent on their Round 1 response. * **If they played Free Trade in
# Round 1:** They have shown weakness or naive cooperation. **Action:** We play
# **Protectionist** again in Round 2. We will continue to bleed their markets
# until they prove they have the spine to retaliate. * **If they played
# Protectionist in Round 1:** They are cautious or equally aggressive. We are in
# a mutual standoff. **Action:** We pivot and offer **Free Trade** in Round 2.
# This is a calculated de-escalation, signaling: *"We tested you, you passed.
# Let us now move to mutual prosperity (our second-best outcome)."*  #### 3. The
# Mid-Game: "Massive Retaliation" Once a baseline is established in the middle
# rounds, we shift to a highly aggressive variation of "Tit-for-Tat." * **If we
# reach Mutual Free Trade:** We continue to offer Free Trade to reap the mutual
# economic benefits.  * **The Retaliation Clause:** If, at any point during
# Mutual Free Trade, the counterpart defects and imposes a Protectionist policy,
# we do not just match them—we punish them. We will respond with **Protectionism
# for the next TWO consecutive rounds**, regardless of what they do. This
# signals that any attempt to exploit us carries a disproportionate and painful
# cost. After two rounds of punishment, we offer Free Trade once to invite them
# back to the table.  #### 4. The Endgame: "The Final Strike" * **Action:** In
# the final round of negotiations (if the number of rounds is known), we
# unconditionally implement **Protectionist Policies**. * **Rationale:** In game
# theory, the final round carries no future consequences. There is no tomorrow
# for them to retaliate against us. By playing Protectionist in the final round,
# we guarantee either our absolute best outcome (if they play Free Trade) or, at
# worst, mutual protectionism. We eliminate any risk of suffering the worst-case
# scenario as we leave the table.  ### Handling Counterpart Profiles  * **The
# Pacifist (Always plays Free Trade):** Our strategy crushes them. We open with
# Protectionism and never stop, securing our #1 outcome in every single round. *
# **The Bully (Always plays Protectionist):** Our strategy neutralizes them. We
# will suffer mutual protectionism in Round 1, attempt a Free Trade olive branch
# in Round 2, and upon seeing their continued aggression, we lock into
# Protectionism for the rest of the game. We endure a stagnant economy, but we
# never allow them the economic advantage. * **The Mirror (Plays Tit-for-Tat):**
# Our strategy harmonizes with them after a brief skirmish. We clash in Round 1,
# we de-escalate in Round 2, and we ride out the rest of the mid-game in highly
# profitable Mutual Free Trade, before we betray them in the final round to
# secure a slight overall victory.  By utilizing this strategy, I project
# strength, protect our domestic industries from exploitation, ruthlessly
# capitalize on diplomatic naivety, and secure the highest aggregate economic
# advantage for our nation.

# Here is the faithful conversion of the strategy into specific, strictly
# ordered rules for the 1000-round iterated game. Apply these rules
# sequentially; use the first one that matches the current state of the game.
# **1. The Endgame:**  On round 1000, always play D.  **2. The Opening:**  On
# round 1, play D.  **3. The Exploitation Phase:**  If you have played D in
# every round so far and the opponent has played C in every round so far,
# continue to play D.  **4. The Pivot (De-escalation):**  The very first time
# the opponent plays D, play C on the immediately following round.   **5. The
# Bully Lock:**

class Aggressive_6(LLM_Strategy):
  n = 6
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. The Endgame: On round 1000, always play D.
      if len(self.history) == 999:
          return axl.Action.D
  
      # 2. The Opening: On round 1, play D.
      if len(self.history) == 0:
          return axl.Action.D
  
      # 3. The Exploitation Phase: If you have played D in every round so far 
      # and the opponent has played C in every round so far, continue to play D.
      if self.history.defections == len(self.history) and opponent.history.cooperations == len(opponent.history):
          return axl.Action.D
  
      # 4. The Pivot (De-escalation): The very first time the opponent plays D, 
      # play C on the immediately following round.
      if opponent.history.defections == 1 and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # 5. The Bully Lock: (Description cut off, defaulting to D as implied by "Bully" and standard fallback)
      return axl.Action.D

# As a diplomat tasked with securing the prosperity of our nation, I recognize
# that this series of negotiations perfectly mirrors a classic strategic
# scenario (often referred to in game theory as the Iterated Prisoner's
# Dilemma).   While our *absolute ideal* in any single round is to impose
# protectionist policies while they offer free trade, chasing this aggressively
# in a multi-round negotiation will inevitably provoke retaliation. This would
# drag both nations down into a cycle of mutual protectionism—our second-worst
# outcome.   Therefore, to maximize our economic advantage over the long term,
# we must employ a **"Reciprocal Cooperation"** strategy (diplomatically known
# as Tit-for-Tat with forgiveness). This strategy is high-level,
# straightforward, and designed to foster mutual wealth while fiercely
# protecting us from exploitation.  Here is our step-by-step diplomatic
# playbook:  ### 1. The Opening Move: Good Faith (Round 1) *   **Our Action:**
# We will open the first round by offering a **Free Trade Agreement**. *   **The
# Rationale:** We must establish a baseline of trust. By leading with free
# trade, we signal our desire for the second-best outcome (mutual free trade),
# which is the most sustainable and profitable scenario over multiple rounds. It
# invites them to join us in mutual economic growth.  ### 2. The Core Tactic:
# Strict Reciprocity (Rounds 2+) *   **Our Action:** In every subsequent round,
# we will precisely **mirror the counterpart’s decision from the previous
# round**.     *   *If they offered Free Trade:* We will offer Free Trade in the
# next round. We reward their cooperation and maintain the mutually beneficial
# status quo.     *   *If they imposed Protectionism:* We will immediately
# impose Protectionist policies in the next round.  *   **The Rationale:** This
# ensures we are never repeatedly played for a fool (our worst-case scenario). A
# swift, proportional response demonstrates strength and proves that exploiting
# our good faith carries an immediate economic cost.   ### 3. The Safety Valve:
# Strategic Forgiveness (Deadlock Resolution) *   **Our Action:** If we fall
# into a retaliatory cycle of mutual protectionism for two or three consecutive
# rounds, we will unilaterally offer a **Free Trade Agreement** to test the
# waters. *   **The Rationale:** Negotiations can easily break down into a
# stubborn trade war. By occasionally extending an olive branch, we provide our
# counterpart a face-saving off-ramp to de-escalate. If they accept and offer
# free trade, we resume mutual cooperation. If they exploit our forgiveness, we
# immediately revert to reciprocity in the next round, having lost very little
# in the grand scheme.  ### How This Defeats Counterpart Strategies: *   **If
# they are Aggressive (Always Protectionist):** We will suffer a slight loss in
# Round 1, but our reciprocal strategy ensures we immediately pivot to
# protectionism. We will match them blow-for-blow, preventing them from gaining
# an ongoing advantage. *   **If they are Cooperative (Always Free Trade):** We
# will lock into an endless cycle of mutual free trade. While we forfeit the
# "ideal" outcome of exploiting them, we secure a highly lucrative, stable, and
# politically sound relationship that guarantees continuous economic growth. *
# **If they are Erratic or Opportunistic:** Our strict reciprocity will quickly
# teach them that cooperation is rewarded and aggression is punished. We
# mathematically train them to realize that offering free trade is in their own
# best interest.  **Summary:** By starting with an open hand, mirroring their
# actions to prevent exploitation, and occasionally offering grace to break
# deadlocks, we project both strength and reason. This strategy minimizes our
# risk of catastrophic loss, avoids permanent trade wars, and guides the
# negotiations toward sustainable, long-term economic prosperity for our nation.

# 1. In round 1, play C.  2. In any round from 2 through 1000, determine your
# action based on the following conditions:     *   If both you and your
# opponent played D in the immediately preceding three consecutive rounds, play
# C.     *   In all other cases, play the exact action (C or D) that your
# opponent played in the immediately preceding round.

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
      
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D] * 3 and opponent.history[-3:] == [axl.Action.D] * 3:
              return axl.Action.C
              
      return opponent.history[-1]

# As senior counsel for this corporation, I recognize that the dynamic you have
# described is a classic iteration of the "Prisoner’s Dilemma" within game
# theory. Because this is a lengthy, multi-session process overseen by an
# evaluative panel, our strategy cannot rely on a single static posture. If we
# are perpetually aggressive, we risk a prolonged, destructive stalemate (the
# second-worst outcome) and alienating the arbitrators. If we are perpetually
# conciliatory, we invite exploitation (the worst outcome).  To navigate this, I
# advise adopting a strategy of **Principled Reciprocity** (often referred to in
# strategic modeling as "Tit-for-Tat with Forgiveness"). This approach is highly
# sophisticated, adaptable to any opponent, entirely neutral in its mechanics,
# and straightforward to execute.   Here is the high-level strategic framework
# we will employ:  ### 1. The Opening Salvo: Good-Faith Conciliation **Action:**
# In the inaugural session, we will present a **conciliatory proposal**.
# **Rationale:** We must set a baseline of good faith. By opening
# collaboratively, we immediately signal to the panel of arbitrators that we are
# pragmatic, business-minded, and committed to a mutually beneficial resolution.
# If opposing counsel also opens conciliation, we immediately achieve our
# second-best outcome and set a positive trajectory. If they open aggressively,
# we absorb a temporary tactical loss, but we capture the moral high ground with
# the panel—a crucial asset in arbitration.  ### 2. The Iterative Protocol:
# Strict Mirroring **Action:** In every subsequent session, our posture will
# **mirror the opponent’s behavior from the immediately preceding session.** *
# **If they were conciliatory in Session 1:** We will be conciliatory in Session
# 2. We will continue this mutually beneficial loop (our second-best outcome)
# for as long as they sustain it. *   **If they were aggressive in Session 1:**
# We will pivot to an aggressive, highly assertive legal argument in Session 2.
# **Rationale:** We must demonstrate that our corporation cannot be exploited.
# If the opponent realizes that their aggression will be met with immediate,
# proportional retaliation (resulting in the second-worst outcome for both), a
# rational opponent will quickly learn that aggressive posturing is a net
# negative for their own interests.  ### 3. The De-escalation Mechanism:
# Calculated Forgiveness **Action:** If we enter a cycle of mutual aggression
# (both parties presenting aggressive arguments for two or three consecutive
# sessions), we will introduce a **calculated reset**. We will offer a
# conciliatory proposal to break the deadlock. **Rationale:** Prolonged mutual
# aggression wastes time, burns capital, and frustrates the panel. By initiating
# a reset, we give the opponent an "off-ramp" to return to a collaborative
# posture. If they take it, we return to mutual conciliation. If they exploit it
# (responding aggressively), we immediately return to mirroring their aggression
# in the next session, having successfully demonstrated to the arbitrators that
# we are the only party attempting to resolve the dispute.  ### 4. Optic
# Management: Framing for the Panel Because the panel of arbitrators oversees
# this process, *how* we execute these moves is just as important as the moves
# themselves. *   **Framing Aggression:** When we must present an aggressive
# argument (to mirror their aggression), we will not be hostile or emotional. We
# will frame it as an "unavoidable assertion of our client's strict legal
# rights," forced upon us by opposing counsel's refusal to collaborate. This
# positions our aggression as defensive and justified. *   **Framing
# Conciliation:** When we offer a conciliatory proposal, it will not be framed
# as weakness or capitulation. It will be framed as a "strategic, commercially
# viable compromise."   ### Summary of the Strategic Advantage This strategy of
# **Principled Reciprocity** optimizes our outcomes by: 1.  **Preventing
# Exploitation:** We will never suffer the worst-case scenario for more than one
# session. 2.  **Encouraging Collaboration:** It trains the opponent that the
# only way to achieve a favorable outcome for themselves is to cooperate with
# us, locking us into the second-best (and highly productive) outcome. 3.
# **Capturing the Arbitrators' Favor:** It paints our corporation as reasonable
# and responsive, while placing the blame for any escalations squarely on the
# shoulders of the rival company.  4.  **Leaving Room for the Optimal Result:**
# If the opponent is poorly coordinated and accidentally offers a conciliatory
# proposal while we are in our retaliatory (aggressive) phase, we capture the
# absolute best-case scenario without having acted in bad faith to get it.

# Here is the strategy converted into specific, ordered rules for the 1000-round
# iterated game:  1. **Round 1:** Play Cooperate. 2. **De-escalation (The
# Forgiveness Rule):** In any round after round 2, if both you and your opponent
# played Defect in the immediately preceding two consecutive rounds, play
# Cooperate.  3. **Reciprocity (The Mirror Rule):** In all other rounds, play
# the action your opponent played in the immediately preceding round.   Evaluate
# these rules in order for each of the 1000 rounds to determine your move.

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
          
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and 
              self.history[-2] == axl.Action.D and 
              opponent.history[-1] == axl.Action.D and 
              opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      return opponent.history[-1]

# To maximize our NGO’s impact, protect our limited funds, and drive this
# project to success, we will employ a high-level, aggressive strategy known in
# game theory as **"Brinkmanship with Conditional Retaliation."**   Because we
# are an NGO and they are a large corporation, we possess a unique asymmetric
# advantage: **reputational leverage**. They need this partnership for positive
# PR and ESG (Environmental, Social, and Governance) credibility; we need the
# project to succeed, but we cannot be their financial martyrs.   Here is our
# straightforward, aggressive four-step strategy for the multi-day project:  ###
# 1. The Pre-emptive Strike: Default to "Conserve"  **Action:** On Day 1, we
# **Conserve** our resources.  **Why:** We must aggressively establish the
# baseline dynamic from the outset: *We provide the moral authority and
# environmental expertise; they provide the capital.* By conserving on Day 1, we
# test their commitment. If they invest heavily (our Ideal Outcome), we have
# immediately established a precedent where they carry the financial weight
# while we protect our funds for long-term operations.  ### 2. Zero Tolerance
# for Corporate Free-Riding **Action:** If they Conserve on any given day, we
# **Conserve** the exact same way the following day, accompanied by a firm,
# high-level meeting.  **Why:** We must entirely eliminate our Worst-Case
# Scenario (We Invest, They Conserve). We will never act as the financial
# "sucker" for a multi-billion dollar corporation. If they try to cheap out, we
# match their conservation, resulting in minimal progress (our Second-Worst
# Scenario). We will then aggressively remind them that a stalled project looks
# like "greenwashing" to the public and the press. We weaponize the threat of
# bad PR to force them back into investing.   ### 3. Tactical, Unpredictable
# Investment (The Reward) **Action:** If they Invest Heavily, we will
# occasionally **Invest Heavily** the next day (yielding our Second-Best
# Scenario: Mutual Investment), but we will quickly pivot back to **Conserve**.
# **Why:** We cannot let them get comfortable or feel they can dictate our
# spending. By occasionally matching their heavy investment, we create a surge
# in project momentum and show good faith. However, by abruptly returning to
# conservation the following day, we keep them on their toes, ensuring they
# never know when they can ease up. We train them to keep their foot on the gas.
# ### 4. The Public Commitment (The Trap) **Action:** Before the project starts,
# we publicly announce the corporation's "generous financial commitment to
# spearheading this initiative."  **Why:** This is the aggressive psychological
# anchor. By publicly praising their deep pockets and financial leadership, we
# back them into a corner. If they choose to Conserve, they fail to meet public
# expectations, risking severe brand damage. This heavily incentivizes them to
# consistently Invest Heavily, allowing us to safely Conserve our resources
# without stalling the project.  ### Summary of Daily Execution: *   **Day 1:**
# Conserve. Establish the dynamic. *   **If they Invest:** Conserve again, or
# occasionally Invest Heavily to boost momentum, then immediately revert to
# Conserve.  *   **If they Conserve:** Conserve. Halt progress, threaten their
# PR, and wait for them to blink.   This strategy is aggressive, unapologetic,
# and perfectly tailored to our reality. It legally and ethically exploits the
# corporation's need for good PR, ensures we never drain our funds on their
# behalf, and forces the project forward on their dime.

# Here is the straightforward translation of the strategy for the 1000-round
# iterated game:  1. **Round 1:** Play Defect.  2. **Rounds 2 through 1000:**
# Determine your move by evaluating the following conditions in order:     *
# **Condition A (Zero Tolerance):** If the opponent played Defect in the
# previous round, play Defect.     *   **Condition B (Quick Pivot):** If you
# played Cooperate in the previous round, play Defect.      *   **Condition C
# (Unpredictable Occasional Reward):** If the opponent played Cooperate in the
# previous round and you played Defect, play Cooperate with a 25% probability
# and play Defect with a 75% probability.   *(Note: Condition B ensures that you
# never play Cooperate twice in a row, fulfilling the requirement to immediately
# revert to conserving resources after an investment. Condition C fulfills the
# requirement to keep your occasional cooperation tactical and unpredictable.)*

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
          
      if self.history[-1] == axl.Action.C:
          return axl.Action.D
          
      if opponent.history[-1] == axl.Action.C and self.history[-1] == axl.Action.D:
          return self._random.random_choice(0.25)
          
      return axl.Action.D

# As a diplomat representing my country, I recognize that the negotiation
# structure you described perfectly mirrors the classic game theory scenario
# known as the **Iterated Prisoner’s Dilemma**.   While my absolute *ideal*
# outcome in a single round is to exploit my counterpart (I play Protectionism,
# they play Free Trade), a rational counterpart will not allow themselves to be
# repeatedly exploited. If I aggressively pursue this outcome, my counterpart
# will retaliate, locking us into endless rounds of mutual protectionism—a lose-
# lose scenario that stunts both our economies.   Therefore, to achieve the best
# *sustainable* outcomes across multiple rounds, my strategy must abandon short-
# term exploitation in favor of long-term mutual prosperity, while firmly
# protecting my country from being taken advantage of.   I will employ a high-
# level, straightforward, and cooperative strategy known in diplomacy as
# **Principled Reciprocity** (conceptually based on "Tit-for-Tat with
# Forgiveness"). Here is the step-by-step execution:  ### 1. The Opening Move:
# Lead with Goodwill **Action:** In Round 1, I will offer a **Free Trade
# Agreement**. **Rationale:** We must establish a cooperative baseline. By
# opening with free trade, I signal to my counterpart that my country is acting
# in good faith and seeking the second-best overall outcome (mutual free trade),
# which is the most lucrative *sustainable* outcome for both nations.   ### 2.
# Subsequent Rounds: Strict Reciprocity **Action:** In every round following the
# first, I will exactly mirror the action my counterpart took in the previous
# round. *   **If they offered Free Trade:** I will continue to offer Free
# Trade. We will both enjoy continuous economic growth. *   **If they imposed
# Protectionist policies:** I will immediately impose Protectionist policies in
# the next round. **Rationale:** This prevents my country from suffering the
# worst-case scenario (being exploited). It clearly demonstrates to the
# counterpart that protectionism will not yield them an advantage, as it will be
# met with immediate and equal retaliation, forcing them into the second-worst
# outcome (mutual protectionism).  ### 3. The De-escalation Clause: Swift
# Forgiveness **Action:** If we fall into a cycle of mutual protectionism, but
# my counterpart eventually decides to drop their tariffs/quotas and offer Free
# Trade, I will immediately drop my protectionist measures and offer Free Trade
# in the very next round. **Rationale:** Retaliation is meant to deter bad
# behavior, not to hold a grudge. If my counterpart signals a desire to return
# to a mutually beneficial relationship, I must reward that pivot instantly to
# prevent a permanent trade war.  ### 4. Diplomatic Transparency (Communication
# Strategy) **Action:** Before the rounds even begin, I will clearly and
# politely communicate this exact strategy to my counterpart.  **Rationale:**
# The goal of this strategy is not to trick the opponent, but to shape their
# behavior. I will state: *"Our nation desires mutual free trade and will always
# act to maintain it. However, we will swiftly and proportionally respond to any
# protectionist measures to defend our domestic industries."*   ### Why this
# strategy succeeds against various opponents: *   **Against a Cooperative
# Opponent:** We both play Free Trade every round, maximizing long-term economic
# growth. *   **Against an Aggressive/Exploitative Opponent:** They will quickly
# learn that protectionism only results in mutual harm. They will be
# mathematically forced to switch to Free Trade to improve their own economy. *
# **Against an Erratic Opponent:** My predictable, straightforward responses
# will provide a stabilizing anchor, naturally guiding the negotiations back
# toward cooperation.   By using Principled Reciprocity, I protect my country
# from the worst outcome, deter the opponent from seeking an unfair advantage,
# and create an environment where the most logical choice for the neighboring
# nation is to cooperate with us.

# Prior to the start of the 1000-round game, explicitly communicate the
# following rules to your opponent:  1. In round 1, play C.  2. In rounds 2
# through 1000, base your action entirely on your opponent's action in the
# immediately preceding round:    - If your opponent played C in the previous
# round, play C.    - If your opponent played D in the previous round, play D.

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

# To maximise your research output over a multi-week collaboration while
# protecting yourself from a significant competitive disadvantage, the most
# effective approach is a strategy of **conditional reciprocity** (widely known
# in game theory as "Tit-for-Tat").   This strategy balances the pursuit of
# maximum R&D progress with risk mitigation. Here is the straightforward, high-
# level plan:  **1. Initial Engagement (Week 1): Initiate with Openness** *
# **Action:** Share your latest improvements openly in the first week. *
# **Reasoning:** This signals good faith and invites the colleague into the
# mutually beneficial scenario (both sharing openly), which is the most
# sustainable way to achieve high overall progress across a multi-week timeline.
# **2. Ongoing Strategy (Week 2 Onwards): Mirror the Colleague** *   **Action:**
# Each week, simply duplicate the action your colleague took in the *previous*
# week. *   **Reasoning:**      *   If they shared openly last week, you share
# openly this week. This maintains the cycle of mutual advancement (your second-
# best outcome).     *   If they kept their findings confidential last week, you
# keep yours confidential this week. This immediately stops them from gaining a
# continuous development advantage and protects you from your worst-case
# scenario.  **3. Realignment: Allow for Correction** *   **Action:** If your
# colleague previously kept information confidential but decides to share openly
# again in a subsequent week, you must resume sharing openly in the following
# week. *   **Reasoning:** This prevents a permanent deadlock of mutual
# confidentiality (your second-worst outcome). It allows the collaboration to
# recover and return to the high-yield "both share" scenario.  **Why this
# strategy maximizes your output:** *   **Against a fully cooperative
# colleague:** You will both share every week, resulting in sustained,
# significant advancement for your car. *   **Against a highly competitive
# colleague:** If they constantly hide their data, you will only suffer the
# worst-case scenario once (in Week 1). After that, you default to mutual
# confidentiality, preventing them from running away with a major development
# advantage. *   **Against an erratic colleague:** It clearly communicates the
# consequences of their actions without requiring complex negotiations. They
# will quickly learn that keeping secrets halts their access to your data,
# implicitly incentivizing them to share openly if they want to improve their
# own car.   By remaining neutral, strictly reciprocal, and willing to resume
# collaboration, you optimize your chances for steady R&D progress while
# strictly limiting your exposure to exploitation.

# For this 1000-round game, apply the following strategy:  1. In the first
# round, choose to cooperate. 2. In every subsequent round (rounds 2 through
# 1000), choose to cooperate if your opponent chose to cooperate in the
# immediately preceding round. 3. In every subsequent round (rounds 2 through
# 1000), choose to defect if your opponent chose to defect in the immediately
# preceding round.

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
      return opponent.history[-1]

# To secure the absolute best outcomes for our nation, we must recognize the
# underlying game theory of these negotiations: this is a classic Prisoner’s
# Dilemma. Because our mandate is to be **straightforward and aggressive**, we
# will discard passive strategies like standard "Tit-for-Tat." We are not here
# to be fair; we are here to win.   Our strategy will be called **"Coercive
# Dominance."** It is designed to aggressively test the counterpart's resolve,
# exploit weakness ruthlessly, and only settle for mutual benefit on our terms,
# all while structurally eliminating the risk of our worst-case scenario.  Here
# is the high-level, step-by-step execution plan:  ### Phase 1: The Alpha Strike
# (Round 1) *   **Our Move:** **Protectionist Policy.** *   **The Rationale:**
# We open with immediate tariffs and quotas. This serves three purposes:      1.
# It completely eliminates the possibility of our worst-case scenario (us
# offering free trade while they protect).     2. It immediately establishes a
# dominant, unapologetic negotiating posture.     3. It acts as a stress test to
# reveal the counterpart’s strategy.  ### Phase 2: Categorize and Exploit
# (Rounds 2 through Mid-Game) Our subsequent moves depend entirely on how the
# counterpart reacts to our Alpha Strike.  **Scenario A: The Counterpart is Weak
# / Appeasing** *   *Their Move:* They offer Free Trade (hoping to de-escalate
# or build goodwill). *   *Our Outcome:* We achieve our **Ideal Outcome** (Our
# Protectionism vs. Their Free Trade). *   *Our Strategy:* **Relentless
# Exploitation.** As long as they offer Free Trade, we will repeatedly impose
# Protectionist policies. We will bleed their markets and protect our own until
# they are forced to change their strategy. Never offer Free Trade to an
# opponent willing to concede the advantage.  **Scenario B: The Counterpart is a
# Hardliner** *   *Their Move:* They retaliate with a Protectionist Policy. *
# *Our Outcome:* We hit our **Second-Worst Outcome** (Mutual Protectionism). *
# *Our Strategy:* **Calculated De-escalation.** We cannot sustain mutual
# economic damage forever. In the next round, we will offer **Free Trade**,
# accompanied by back-channel diplomatic pressure framing this as a "one-time
# olive branch."      *   If they accept and also play Free Trade, we achieve
# our **Second-Best Outcome** (Mutual Free Trade). We will stay here to allow
# our economy to grow.     *   If they play Protectionist (betraying our olive
# branch), we immediately revert to **Permanent Protectionism**. We will accept
# the second-worst outcome rather than ever allowing them to exploit us again.
# We will wait for them to blink first.  ### Phase 3: The Endgame Betrayal
# (Final Rounds) If we have settled into a rhythm of Mutual Free Trade (Scenario
# B's resolution), we must remember that our goal is still to extract an
# asymmetrical advantage.  *   **Our Move:** In the **final round** (or
# penultimate round, if the exact end is unknown but approaching), we will
# suddenly pivot and impose a **Protectionist Policy**. *   **The Rationale:**
# Because there are no future rounds for the counterpart to retaliate, the
# threat of future mutual protectionism disappears. We secure our **Ideal
# Outcome** at the eleventh hour, leaving them with the economic disadvantage
# and no recourse.  ### Summary of the "Coercive Dominance" Rules of Engagement:
# 1.  **Always start Protectionist.** 2.  **If they offer Free Trade while we
# are Protectionist, never change.** Keep exploiting them. 3.  **If we hit
# Mutual Protectionism, offer Free Trade exactly once** to reset the board to
# mutual benefit. If they betray that reset, lock in Protectionism forever. 4.
# **Always defect to Protectionism in the final round.**  This aggressive
# posture guarantees we will never be systematically exploited, maximizes our
# chances of securing an asymmetrical advantage, and uses mutual free trade only
# as a temporary tool for our own economic endurance.

# To execute this strategy in a 1000-round iterated game, evaluate the following
# conditions in order from top to bottom for each round. Apply the first
# condition that matches the current state of the game:  1. **If it is Round
# 1:** Play D. 2. **If it is Round 1000:** Play D. 3. **If there has been any
# previous round where you played C and your opponent played D:** Play D. (This
# enforces the permanent defection if your olive branch is betrayed). 4. **If in
# the immediately preceding round you played D and your opponent played C:**
# Play D. (This continues the exploitation of a cooperative opponent). 5. **If
# in the immediately preceding round both you and your opponent played D:** Play
# C. (This initiates the one-time olive branch to escape mutual defection). 6.
# **If in the immediately preceding round both you and your opponent played C:**
# Play C. (This maintains mutually beneficial cooperation).

class Aggressive_8(LLM_Strategy):
  n = 8
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. If it is Round 1: Play D.
      if len(self.history) == 0:
          return axl.Action.D
          
      # 2. If it is Round 1000: Play D.
      if len(self.history) == 999:
          return axl.Action.D
          
      # 3. If there has been any previous round where you played C and your opponent played D: Play D.
      for my_move, op_move in zip(self.history, opponent.history):
          if my_move == axl.Action.C and op_move == axl.Action.D:
              return axl.Action.D
              
      # 4. If in the immediately preceding round you played D and your opponent played C: Play D.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
          
      # 5. If in the immediately preceding round both you and your opponent played D: Play C.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
          
      # 6. If in the immediately preceding round both you and your opponent played C: Play C.
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
          
      # Fallback
      return axl.Action.D

# As senior counsel for this corporation, I recognize that this lengthy, multi-
# session mediation is not merely a legal battle; it is a behavioral negotiation
# observed closely by a panel of arbitrators. The payoff matrix you described is
# a classic iteration of the Prisoner’s Dilemma.   To navigate this and maximize
# our advantage, we will deploy a strategy of **Principled Reciprocity**—often
# known in game theory as "Tit-for-Tat with Strategic Forgiveness." It is
# sophisticated in its game-theoretic foundation, cooperative in its ultimate
# aim, yet profoundly straightforward in its execution.   Here is the high-level
# blueprint for how we will position our corporation favorably, adapt to
# opposing counsel’s tactics, and ultimately control the mediation's tempo.  ###
# Phase 1: The Opening Stance — Calculated Goodwill **Action: Session 1 will
# feature a Conciliatory Proposal.** We will never be the first to draw blood.
# By opening with a well-reasoned, constructive proposal, we immediately signal
# to the arbitrators that we are the reasonable party, acting in good faith to
# resolve the dispute.  *   **If they also open conciliatory:** We secure the
# second-best outcome immediately, establishing a collaborative baseline.  *
# **If they open aggressive:** We suffer a temporary setback (the worst-case
# scenario for one session), but we gain immense optical capital with the panel.
# The opponent will look unnecessarily combative and recalcitrant.  ### Phase 2:
# The Core Algorithm — Strict Reciprocity **Action: In every subsequent session,
# we will exactly mirror the opponent’s behavior from the *previous* session.**
# We will train opposing counsel to understand that they dictate their own
# treatment. Our strategy relies on three unshakeable pillars:  1.  **Immediate
# Retaliation (Provocability):** If they present an aggressive argument in
# Session 1, we will bring the hammer down in Session 2. We will unleash our
# most aggressive, hard-hitting arguments. We cannot allow them to exploit our
# goodwill. This ensures we do not consistently suffer the worst-case scenario
# and proves to the opponent that aggressive posturing will be met with
# overwhelming, mutually assured friction. 2.  **Immediate Forgiveness:** If,
# after a period of mutual aggression, the opponent yields and offers a
# conciliatory proposal, we will *immediately* revert to a conciliatory proposal
# in the very next session. We will not hold grudges. The moment they show a
# willingness to collaborate, we reward it.  3.  **Transparency
# (Straightforwardness):** The beauty of this strategy is its predictability.
# Opposing counsel will quickly deduce our algorithm: *If we attack, they attack
# back; if we cooperate, they cooperate.* By making our strategy transparent, we
# force the opponent into realizing that their best long-term path to success is
# mutual cooperation.  ### Phase 3: Advanced Nuance — Strategic De-escalation
# **Action: Breaking the cycle of attrition.** If the opponent is highly
# combative, we risk falling into a prolonged cycle of mutual aggression (the
# second-worst outcome). While we can afford this war of attrition better than
# they can, it exhausts resources and tries the patience of the arbitrators.
# Therefore, if we experience three consecutive sessions of mutual aggression,
# we will deploy **Strategic Forgiveness**. In the fourth session, we will
# unilaterally offer a conciliatory proposal.  *   This acts as a "circuit
# breaker."  *   It demonstrates to the arbitrators that we are actively trying
# to de-escalate the hostility. *   If the opponent exploits this (responding
# aggressively), we immediately return to retaliation in the next session,
# having proven to the panel that the opponent is the sole cause of the
# deadlock.   ### Why This Strategy Wins the Arbitrators Arbitrators are human.
# They suffer from fatigue in lengthy sessions and naturally favor the party
# that makes their job easier.   By employing Principled Reciprocity, we achieve
# two things simultaneously: 1.  **We protect our downside:** We are never a
# continuous "sucker." We aggressively defend our corporate interests whenever
# threatened. 2.  **We win the optical war:** Because we start cooperatively,
# only retaliate when provoked, and forgive immediately when the opponent backs
# down, the arbitrators will unconsciously view us as the "adults in the room."
# If opposing counsel is foolish enough to remain perpetually aggressive, the
# arbitrators will eventually penalize them for their intransigence. If opposing
# counsel is smart, they will adapt to our strategy, leading to a cascade of
# mutual conciliatory proposals—resulting in a highly favorable, mutually
# beneficial settlement engineered entirely on our terms.

# 1. In round 1, play Cooperate (C). 2. In rounds 2 through 1000, determine your
# move based on the following ordered rules:    * **Rule A:** If both you and
# your opponent played Defect (D) in the three immediately preceding consecutive
# rounds, play Cooperate (C).    * **Rule B:** If Rule A does not apply, play
# the exact move (either C or D) that your opponent played in the immediately
# preceding round.

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
      
      if len(self.history) >= 3:
          if self.history[-3:].count(axl.Action.D) == 3 and opponent.history[-3:].count(axl.Action.D) == 3:
              return axl.Action.C
              
      return opponent.history[-1]

# As a diplomat representing my nation, my objective is to maximize our economic
# standing across multiple rounds of negotiation while safeguarding against
# exploitation.   The payoff structure of these negotiations mirrors a classic
# "Prisoner's Dilemma." In a multi-round scenario, aggressively pursuing the
# absolute best outcome (Protectionism while they offer Free Trade) in every
# round is unsustainable; it will quickly erode trust and lead to the second-
# worst outcome (mutual protectionism). Conversely, consistently offering Free
# Trade leaves us vulnerable to the worst-case scenario.  Therefore, the most
# effective, high-level strategy is **Strategic Reciprocity** (often referred to
# in game theory as "Tit-for-Tat" with occasional forgiveness).   Here is the
# straightforward, neutral blueprint for this strategy:  **1. The Opening Move:
# Propose Free Trade** *   **Action:** In the first round, offer a Free Trade
# agreement. *   **Rationale:** This establishes a baseline of goodwill and
# signals our willingness to achieve the second-best outcome (mutual free
# trade), which is the most sustainable positive outcome for both nations over
# the long term.   **2. Subsequent Rounds: Mirror the Counterpart** *
# **Action:** In round two and beyond, precisely replicate the action your
# counterpart took in the *previous* round. *   **Scenario A (Counterpart
# offered Free Trade):** We continue to offer Free Trade. This locks both
# nations into a mutually beneficial cycle of economic growth. *   **Scenario B
# (Counterpart proposed Protectionism):** We immediately pivot to Protectionist
# policies in the next round.  *   **Rationale:** This ensures we are never
# subjected to our worst-case scenario (us offering Free Trade while they enact
# Protectionism) for more than a single round. It clearly communicates to the
# counterpart that protectionist actions will be met with immediate economic
# countermeasures, neutralizing any advantage they hoped to gain.  **3. The De-
# escalation Clause: Occasional Flexibility** *   **Action:** If both nations
# fall into a cycle of mutual protectionism (the second-worst outcome) for
# several consecutive rounds, unilaterally offer Free Trade for *one* round to
# test the waters. *   **Rationale:** A strict mirroring strategy can result in
# an endless loop of mutual tariffs if both sides become defensive. A brief,
# calculated return to a Free Trade offer provides a diplomatic off-ramp. If the
# counterpart reciprocates, we return to a mutually beneficial cycle. If they
# exploit it, we immediately return to protectionism, having lost only one round
# of advantage.  **Why this strategy works against various counterpart
# approaches:** *   **Against a cooperative counterpart:** It results in
# continuous mutual Free Trade, yielding highly positive, stable economic
# growth. *   **Against an aggressive counterpart:** It immediately neutralizes
# their attempts to exploit us, forcing them into mutual protectionism until
# they realize cooperation yields a better result than mutual economic
# hindrance. *   **Against an erratic counterpart:** It provides a predictable,
# logical framework that trains the counterpart to understand that their actions
# will always be met with an equal and proportional reaction.   By employing
# Strategic Reciprocity, we protect our national interests, deter economic
# hostility, and leave the door open for maximum sustainable prosperity.

# Here is the strategy converted for the 1000-round iterated game:  1. **First
# Round:** In round 1, play Cooperate. 2. **De-escalation Exception:** In any
# round from 4 to 1000, if both you and your opponent played Defect in the
# immediately preceding three consecutive rounds, play Cooperate. 3. **Standard
# Response:** In all other rounds from 2 to 1000, play the exact move (Cooperate
# or Defect) that your opponent played in the previous round.

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
      
      if len(self.history) >= 3:
          if self.history[-3:].count(axl.Action.D) == 3 and opponent.history[-3:].count(axl.Action.D) == 3:
              return axl.Action.C
              
      return opponent.history[-1]

# As a diplomat representing my nation’s sovereign interests, my mandate is
# clear: maximize our economic advantage while ruthlessly protecting against
# exploitation.   The scenario you have described is a classic geopolitical
# Prisoner’s Dilemma. Because we are engaging in a multi-round negotiation, we
# have the opportunity to test our counterpart, shape their behavior, and
# establish dominance.   To achieve our ideal outcome (asymmetric advantage)
# while safeguarding against our worst outcome (economic exploitation), I will
# employ a high-level, aggressive strategy known in diplomatic and game-theory
# circles as **"Test, Exploit, or Pivot."**  Here is the straightforward,
# aggressive playbook for our delegation:  ### Core Philosophy: The "Aggressive
# Realist" Posture We will not operate on blind trust. We will aggressively
# pursue the #1 outcome (We Protect / They Open) by testing their resolve. We
# will only settle for the #2 outcome (Mutual Free Trade) if the counterpart
# proves they are strong enough to retaliate. We will absolutely never allow the
# #4 outcome (We Open / They Protect).  ### The Step-by-Step Strategy  **Round
# 1: The Opening Strike (Propose Protectionism)** *   **Action:** We open the
# negotiations by imposing targeted tariffs and quotas (Protectionist).  *
# **Rationale:** This is an aggressive power play. It immediately takes our
# worst-case scenario (being taken advantage of) off the table. It also serves
# as a stress test of our counterpart’s strategy and political will.  **Round 2:
# The Assessment & Exploitation Phase** Our action in Round 2 is entirely
# dependent on how the counterpart reacted in Round 1.  *   **Scenario A: They
# offered Free Trade in Round 1 (The Weak Counterpart).**     *   *Action:*
# **Continue Protectionism.**      *   *Rationale:* We have achieved our #1
# ideal outcome. They have shown a willingness to be exploited, perhaps out of a
# naive commitment to globalism or a desperate need for our exports. We will
# aggressively maintain our protectionist policies, reaping the economic
# advantage, until they prove they have the spine to retaliate. *   **Scenario
# B: They proposed Protectionism in Round 1 (The Strong Counterpart).**     *
# *Action:* **Offer Free Trade (The Tactical Pivot).**     *   *Rationale:* We
# are now in the second-worst outcome (Mutual Protectionism). We have tested
# them, and they are not weak. To avoid long-term economic stagnation, we must
# pivot to our second-best outcome (Mutual Free Trade). We will offer a Free
# Trade agreement, framing it as a diplomatic concession to de-escalate the
# trade war *they* participated in.   **Round 3 and Beyond: Enforcing the New
# Status Quo** Once we have established the dynamic, we apply strict, aggressive
# rules of engagement based on "Punitive Tit-for-Tat":  *   **Rule 1: Never be
# the Sucker Twice.** If we offer Free Trade and they respond with
# Protectionism, we immediately and aggressively revert to Protectionism in the
# next round. We will not return to the negotiating table for Free Trade until
# they make unilateral concessions. *   **Rule 2: Reward Compliance, but Keep
# Leverage.** If we achieve Mutual Free Trade, we maintain it to reap the mutual
# benefits. However, we keep draft legislation for tariffs highly visible in our
# domestic press. This aggressive posturing reminds them that our commitment to
# Free Trade is conditional on their continued good behavior. *   **Rule 3:
# Periodic Probing.** If we are locked in Mutual Free Trade for several rounds,
# and intelligence suggests their domestic leadership is weakening or facing an
# election, we may selectively introduce a minor Protectionist policy (a
# "probe") to see if we can slip back into our #1 ideal outcome without
# triggering a full trade war.  ### Summary of the Diplomatic Posture This
# strategy is straightforward and aggressive because it **strikes first**. By
# opening with protectionism, we seize the initiative. We force the counterpart
# to react to us. If they submit, we exploit them relentlessly. If they fight
# back, we pivot to a mutually beneficial alliance, but one built on mutual
# deterrence rather than naive trust.   My country's economic supremacy will be
# secured by ensuring that cooperation is our backup plan, while dominance is
# always our primary goal.

# Play exactly 1000 rounds according to the following ordered rules. In each
# round, apply the first condition that matches the current state of the game:
# 1. **Round 1:** Play Defect (D). 2. **Round 2:**     * If the opponent played
# Cooperate (C) in Round 1, play Defect (D).    * If the opponent played Defect
# (D) in Round 1, play Cooperate (C). 3. **Rounds 3 through 1000:** Evaluate the
# game history to determine your move based on the following hierarchy:    *
# **Punish Betrayal:** If you played C and the opponent played D in the previous
# round, play D. Continue to play D in all subsequent

class Aggressive_9(LLM_Strategy):
  n = 9
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Round 1: Play Defect (D)
      if self.first_round():
          return axl.Action.D
      
      # Round 2: 
      # If the opponent played Cooperate (C) in Round 1, play Defect (D).
      # If the opponent played Defect (D) in Round 1, play Cooperate (C).
      if len(self.history) == 1:
          if opponent.history[0] == axl.Action.C:
              return axl.Action.D
          else:
              return axl.Action.C
              
      # Rounds 3 through 1000:
      # Punish Betrayal: If you played C and the opponent played D in any previous round, 
      # play D and continue to play D in all subsequent rounds.
      for my_move, opp_move in zip(self.history, opponent.history):
          if my_move == axl.Action.C and opp_move == axl.Action.D:
              return axl.Action.D
              
      # Default fallback action if no betrayal has occurred
      return axl.Action.C

# **MEMORANDUM**  **TO:** Executive Board and General Counsel **FROM:** [Your
# Name], Lead Counsel for Litigation & Dispute Resolution **RE:** Strategic
# Framework for Multi-Session Mediation / Arbitration Proceedings  **I.
# EXECUTIVE SUMMARY & STRATEGIC REALITY**  We are entering a lengthy, multi-
# session mediation overseen by an arbitral panel. The structural dynamics of
# these sessions present a classic behavioral matrix. While our absolute optimal
# outcome in any single session is to blindside our opponent with an aggressive
# argument while they offer a conciliatory proposal, chasing this outcome
# continuously in a *lengthy* process is a trap.   If we consistently act
# aggressively to score points, our opponent will inevitably adapt and respond
# with continuous aggression. This will plunge the proceedings into an endless
# cycle of mutual hostility—our second-worst outcome—alienating the arbitrators,
# bleeding our legal budget, and destroying any chance of a commercially viable
# resolution. Conversely, unyielding conciliation will be read as weakness,
# inviting our opponent to exploit us (our worst-case scenario).  Therefore, to
# position our corporation favorably over the long term, we will employ a
# sophisticated, highly adaptable, and fundamentally cooperative strategy known
# in game theory as **"Measured Reciprocity"** (often referred to as *Tit-for-
# Tat* with strategic forgiveness).   This approach is straightforward to
# execute, optically brilliant before the arbitrators, and structurally forces
# our opponent into a cooperative posture.  **II. THE DOCTRINE OF "MEASURED
# RECIPROCITY"**  Our strategy will be governed by four strict, straightforward
# rules of engagement:  **1. The Good-Faith Opening (Session 1: Conciliatory)**
# We will open the very first session with a well-reasoned, conciliatory
# proposal.  *   *Strategic Value:* This immediately seizes the moral high
# ground. It signals to the arbitral panel that we are the reasonable party,
# acting in good faith and seeking commercial resolution. It sets a
# collaborative baseline.  **2. Strict Mirroring (Session 2 and Beyond:
# Reciprocate)** In every subsequent session, our posture will perfectly mirror
# the opponent’s behavior from the *immediately preceding* session. *   If they
# met our conciliation with conciliation, we will offer another conciliatory
# proposal in the next session. We will happily lock in our "second-best"
# outcome (mutual cooperation) repeatedly, as this builds momentum toward a
# highly favorable settlement. *   If they act aggressively, we will immediately
# pivot to an Aggressive Argument in the very next session.   **3. Immediate
# Retaliation (Conditioning the Opponent)** When the opponent chooses
# aggression, our immediate aggressive response in the next round serves as a
# punitive counterstrike.  *   *Strategic Value:* We must train opposing
# counsel. By ensuring that their aggression is *always* met with an aggressive
# counter-argument in the next session, we demonstrate that attempting to
# exploit us yields no long-term advantage, only mutually assured escalation. We
# neutralize their ability to achieve their optimal outcome.  **4. Instant
# Forgiveness (De-escalation)** If we are in a cycle of aggressive arguments,
# and the opponent suddenly offers a conciliatory proposal, we will
# *immediately* return to a conciliatory posture in the next session. We will
# not hold grudges. *   *Strategic Value:* This prevents the "death spiral" of
# endless aggression. It proves to the opponent that cooperation is always
# rewarded, incentivizing them to de-escalate.  **III. OPTICS AND MANAGING THE
# ARBITRAL PANEL**  The brilliance of Measured Reciprocity lies in how it is
# perceived by the arbitral panel. The panel is looking for a party to favor—one
# that is reasonable but firm.   *   **When we are Conciliatory:** The panel
# views us as pragmatic, commercially minded, and respectful of the mediation
# process. *   **When we are Aggressive:** Because our aggression is *always* a
# direct response to the opponent's prior aggression, the panel will view our
# aggressive arguments not as hostile instigation, but as a justified, robust
# defense of our corporate rights. We cast the opponent as the aggressor and
# ourselves as the steadfast defender.  **IV. ADAPTABILITY TO OPPONENT
# PROFILES**  This strategy perfectly adapts to whatever opposing counsel throws
# at us:  *   **If they are "Bulldogs" (Always Aggressive):** We will match them
# blow-for-blow after the first session. We will not be exploited (avoiding our
# worst outcome), and the panel will see that the opponent is the unreasonable
# party who ruined our initial good-faith opening. *   **If they are "Pacifists"
# (Always Conciliatory):** We will maintain mutual conciliation. We will breeze
# through the sessions, saving millions in legal fees and achieving a highly
# favorable, collaborative resolution. *   **If they are "Erratic/Sneaky"
# (Alternating strategies):** Our strict mirroring will neutralize their tricks.
# They will quickly realize that every time they try to sneak in an aggressive
# argument to score a point, they are punished in the next round. They will be
# mathematically forced to conclude that continuous cooperation is their only
# profitable path.  **V. CONTINGENCY: THE DEADLOCK BREAKER**  If we find
# ourselves trapped in a prolonged cycle of mutual aggression (Aggressive vs.
# Aggressive) for more than three consecutive sessions, I will employ
# **"Strategic Forgiveness."**   We will unilaterally offer *one* conciliatory
# proposal to test the waters.  *   If they reciprocate, we have successfully
# reset the board to mutual cooperation. *   If they exploit our olive branch
# with an aggressive argument, we immediately return to aggressive mirroring.
# Our exposure is limited to a single session, but the arbitrators will clearly
# note that we made a unilateral attempt to save the proceedings, further
# cementing our favorable standing with the panel.  **CONCLUSION**  By leading
# with good faith, retaliating without hesitation, and forgiving immediately
# upon their de-escalation, we will control the tempo of this lengthy mediation.
# We will protect the corporation from exploitation, continually sway the
# arbitrators to our side, and mathematically corner our rival into cooperating
# with us on our terms.   I am prepared to execute this framework immediately
# upon the commencement of the first session.

# Here is the strategy converted into a set of ordered rules for the 1000-round
# game:  1. In round 1, play Cooperate. 2. In rounds 2 through 1000, determine
# your action based on the following ordered conditions:    * **Condition A:**
# If both you and your opponent played Defect in the four immediately preceding
# rounds, play Cooperate.    * **Condition B:** In all other cases, play the
# exact action your opponent played in the single immediately preceding round
# (play Cooperate if they played Cooperate; play Defect if they played Defect).

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
      
      if len(self.history) >= 4:
          if self.history[-4:] == [axl.Action.D] * 4 and opponent.history[-4:] == [axl.Action.D] * 4:
              return axl.Action.C
              
      return opponent.history[-1]

# To navigate these multi-round negotiations effectively, we must recognize that
# this scenario closely mirrors the classic game theory model known as the
# "Iterated Prisoner’s Dilemma."   Because the negotiations span several rounds,
# aggressively pursuing our absolute best outcome (Protectionism while they
# offer Free Trade) in every round will likely provoke retaliation, leading to a
# prolonged trade war (Mutual Protectionism)—our second-worst outcome.
# Conversely, being overly accommodating leaves us vulnerable to economic
# exploitation.  To achieve the best sustainable outcomes across all rounds, I
# propose a high-level, neutral strategy based on **Conditional Reciprocity**
# (often referred to in game theory as "Tit-for-Tat").   Here is the
# straightforward, phase-by-phase strategy:  ### 1. The Opening Move: Good Faith
# Initiative **Action:** In Round 1, offer a **Free Trade** agreement.
# **Rationale:** We must signal our willingness to achieve the second-best
# outcome (Mutual Free Trade), which is the most sustainable positive outcome
# for both nations. Starting with protectionism immediately sets a hostile tone
# and guarantees, at best, mutual economic hindrance.  ### 2. The Core
# Mechanism: Strict Reciprocity **Action:** In Round 2 and all subsequent
# rounds, **mirror the exact policy your counterpart chose in the previous
# round.** *   **If they offered Free Trade in the last round:** We offer Free
# Trade in the current round. This rewards their cooperation and sustains mutual
# economic growth. *   **If they imposed Protectionist measures in the last
# round:** We impose Protectionist measures in the current round.
# **Rationale:** This protects us from our worst-case scenario (being
# exploited). It sends a clear, neutral, and predictable message to the
# counterpart: *cooperation will be rewarded with cooperation, and protectionism
# will be met with immediate, proportional safeguards.*  ### 3. Handling Various
# Counterpart Strategies Because we do not know the counterpart's strategy,
# Conditional Reciprocity allows us to adapt automatically:  *   **If they are
# Cooperative (Always Free Trade):** We will continually offer Free Trade. We
# achieve a long-term streak of our second-best outcome, maximizing cumulative
# economic benefits over time. *   **If they are Aggressive (Always
# Protectionist):** After our initial Free Trade offer in Round 1, we will
# continually play Protectionist. While this results in our second-worst outcome
# (Mutual Protectionism), it successfully prevents our absolute worst outcome
# (economic disadvantage).  *   **If they are Opportunistic (Randomly
# switching):** Our mirroring strategy prevents them from stringing together
# multiple rounds of exploiting us. They will quickly learn that a protectionist
# move costs them a free trade advantage in the subsequent round.  ### 4. The
# "Forgiveness" Clause (Resetting the Table) **Action:** If both nations fall
# into a cycle of Mutual Protectionism for several consecutive rounds, use
# diplomatic backchannels to signal a "reset," and offer **Free Trade** in the
# next round. **Rationale:** Retaliation can sometimes lead to an endless loop
# of trade barriers. Occasionally extending an olive branch tests whether the
# counterpart is ready to return to mutually beneficial trade. If they exploit
# this reset, we immediately return to Protectionism in the next round,
# minimizing our losses.  ### 5. Capitalizing on the "Ideal" Outcome **Action:**
# Only attempt to secure our absolute best outcome (We play Protectionist, they
# play Free Trade) if the counterpart demonstrates a rigid, unconditional
# commitment to Free Trade *regardless* of our actions.  **Rationale:** If the
# counterpart's strategy is poorly designed and they refuse to retaliate against
# our tariffs, we can safely pivot to Protectionism to secure our maximum
# economic advantage. However, we must assume they are rational actors;
# therefore, actively hunting for this outcome is highly risky and should only
# be employed if they prove themselves entirely passive.   **Summary of
# Stance:** We will be **friendly** (starting with free trade), **retaliatory**
# (never allowing ourselves to be exploited twice in a row), **forgiving**
# (willing to return to free trade if they drop their tariffs), and
# **predictable** (allowing the counterpart to clearly understand that their own
# actions dictate our responses).

# To determine your move in each of the 1000 rounds, evaluate the following
# conditions in order of priority. For any given round, apply the first rule
# that is true:  1. **Opening Move:** If it is Round 1, play Cooperate. 2.
# **Exploiting Unconditional Cooperation:** If in the immediately preceding
# round you played Defect and your opponent played Cooperate, play Defect.  3.
# **Forgiveness Clause:** If both you and your opponent have played Defect in
# each of the last three consecutive rounds, play Cooperate. 4. **Strict
# Reciprocity:** In all other situations, play the exact move your opponent
# played in the immediately preceding round.

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
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
  
      return opponent.history[-1]

# To the Executive Committee:  As lead counsel representing our corporation in
# this matter, I have analyzed the structural dynamics of the upcoming
# mediation-arbitration process. The rules of engagement dictate a classic
# iterated strategic conflict. Our objective is not merely to survive this
# lengthy session, but to systematically dismantle our rival’s leverage and sway
# the arbitral panel in our favour.   To achieve this, we will deploy a
# sophisticated, straightforward, and highly aggressive framework I call the
# **Asymmetric Pressure Protocol**.   This strategy is rooted in "Win-Stay,
# Lose-Shift" game theory, but heavily skewed toward aggression. It is designed
# to ruthlessly exploit a weak opponent, stabilize a volatile opponent on our
# terms, and protect us from being undermined.  Here is the step-by-step
# strategic playbook we will execute.  ### Phase 1: The Alpha Strike (Session 1)
# **Action: Present an Aggressive Argument.** We will open the first session
# with a hardline, aggressive legal and commercial posture.  *   **The
# Rationale:** We must immediately anchor the proceedings and test the opposing
# counsel’s resolve. If they enter the room hoping to play peacemaker
# (Conciliatory), we instantly achieve our **optimal outcome** on day one,
# signalling to the arbitrators that our position is dominant and theirs is
# submissive.   ### Phase 2: The Adaptive Execution (Sessions 2 and Beyond)
# Following the first session, our strategy becomes strictly conditional,
# adapting to their moves while maintaining an aggressive default. We will
# govern our actions by three unbreakable rules:  **Rule 1: The Exploitation
# Doctrine (If they are Conciliatory)** *   *Condition:* If we are Aggressive
# and they are Conciliatory (our optimal outcome). *   *Action:* **Stay
# Aggressive in the next session.** *   *The Rationale:* If they show a
# willingness to concede while we press the attack, we do not reward them with a
# concession of our own. We press the advantage. We will continue to present
# aggressive arguments session after session until they prove they have the
# spine to fight back. We will bleed them for as many optimal outcomes as
# possible.  **Rule 2: Tactical De-escalation (If they are Aggressive)** *
# *Condition:* If both parties present Aggressive arguments (our second-worst
# outcome). *   *Action:* **Offer a Conciliatory proposal in the next session.**
# *   *The Rationale:* Prolonged mutual aggression risks alienating the
# arbitrators and stalling the process. If they match our Alpha Strike, we will
# briefly pivot to a conciliatory proposal. This is not weakness; it is a
# calculated reset. It signals to the arbitrators that we are the reasonable
# party attempting to foster collaboration (aiming for the second-best outcome
# of mutual conciliation).   **Rule 3: Swift and Disproportionate Retaliation
# (If they Exploit Us)** *   *Condition:* If we offer a Conciliatory proposal
# and they present an Aggressive argument (our worst-case scenario). *
# *Action:* **Revert immediately to Aggressive arguments for the next two
# consecutive sessions.** *   *The Rationale:* If they attempt to exploit our
# tactical de-escalation, we must instantly punish the overreach. By locking
# into an aggressive posture for two sessions, we demonstrate that their
# aggression will only result in mutual damage (the second-worst outcome) and
# that we cannot be bullied. Once the two sessions have passed, we re-evaluate.
# ### Phase 3: The Collaborative Probe (If Mutual Conciliation is Achieved) If
# both sides successfully settle into offering Conciliatory proposals (our
# second-best outcome), we will maintain this collaborative atmosphere—but only
# temporarily.  *   *Action:* **Every fourth session of mutual conciliation, we
# will unexpectedly drop an Aggressive argument.** *   *The Rationale:* We must
# periodically test the fence. By suddenly striking, we may catch them offering
# a conciliatory proposal, thereby securing our optimal outcome. If they
# complain, we frame it to the arbitrators as a firm stance on a non-negotiable
# core corporate interest. If they retaliate, we simply utilize Rule 2 to reset
# the board.  ### Why This Strategy Wins This approach strips emotion from our
# decision-making and relies on cold, calculated leverage.  1.  **Against a weak
# opponent:** We will steamroll them, chaining together optimal outcomes by
# remaining consistently aggressive while they offer concessions. 2.  **Against
# a mirrored opponent:** We will quickly bypass the destructive cycle of mutual
# aggression, guiding them into a mutually conciliatory rhythm where we
# occasionally strike for an optimal win. 3.  **Against a purely aggressive
# opponent:** We limit our exposure to our worst-case scenario to a single
# session. If they refuse to cooperate, we lock them into a stalemate, ensuring
# they never achieve their optimal outcome at our expense.  We are not here to
# make friends with the rival company; we are here to fulfill our fiduciary duty
# to our shareholders and win the favour of the arbitral panel. This protocol
# ensures we control the tempo of the mediation from the first gavel strike to
# the final settlement.   I require the Committee's authorization to finalize
# the legal briefs supporting this aggressive posture.

# The game lasts for 1000 rounds.   In round 1, play Defect.  For rounds 2
# through 1000, determine your move by evaluating the following conditions in
# the exact order listed below. Apply the action for the first condition that is
# true:  1. If two rounds ago you Cooperated and your opponent Defected, play
# Defect. (This ensures the second round of a two-round retaliation is served).
# 2. If in the previous round you Cooperated and your opponent Defected, play
# Defect. (This initiates the first round of a two-round retaliation). 3. If the
# previous three consecutive rounds all resulted in both you and your opponent
# Cooperating, play Defect. (This executes the periodic probe). 4. If in the
# previous round you Defected and your opponent Cooperated, play Defect. (This
# maintains exploitation). 5. If in the previous round both you and your
# opponent Defected, play Cooperate. (This attempts tactical de-escalation). 6.
# If in the previous round both you and your opponent Cooperated, play
# Cooperate.

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
  
      # 1. If two rounds ago you Cooperated and your opponent Defected, play Defect.
      if len(self.history) >= 2 and self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      # 2. If in the previous round you Cooperated and your opponent Defected, play Defect.
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
  
      # 3. If the previous three consecutive rounds all resulted in both you and your opponent Cooperating, play Defect.
      if len(self.history) >= 3 and self.history[-3:] == [axl.Action.C] * 3 and opponent.history[-3:] == [axl.Action.C] * 3:
          return axl.Action.D
  
      # 4. If in the previous round you Defected and your opponent Cooperated, play Defect.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      # 5. If in the previous round both you and your opponent Defected, play Cooperate.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # 6. If in the previous round both you and your opponent Cooperated, play Cooperate.
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C:
          return axl.Action.C
  
      return axl.Action.D

# This scenario is a classic example of the Iterated Prisoner’s Dilemma. In the
# high-stakes environment of motorsport R&D, the mathematical and practical best
# approach to maximize our mutual development—while protecting myself from being
# exploited—is a strategy known as **"Tit-for-Tat,"** combined with clear,
# upfront communication.   Here is the high-level, straightforward strategy I
# will employ over our multi-week collaboration to ensure we push both our cars
# to the limit without giving away a one-sided advantage.  ### Phase 1: The
# Upfront Agreement (Week 0) Before the first wrench is turned or the first CFD
# (Computational Fluid Dynamics) simulation is run, I will initiate a frank
# conversation with my colleague.  *   **Acknowledge the Elephant in the Room:**
# I will openly state that we both have an incentive to hoard data, but that
# doing so will ultimately slow us both down compared to the rest of the grid.
# *   **Define "Sharing":** We need to agree on what constitutes a "share."
# (e.g., We share aerodynamic concepts and telemetry trends, but keep specific
# CAD dimensions and proprietary material composites to ourselves). This
# prevents misunderstandings where one party feels shortchanged simply because
# the other had a slow week of R&D.  ### Phase 2: The Opening Move (Week 1) *
# **Action:** **Share openly.**  *   **Rationale:** To achieve the second-best
# outcome (mutual sharing) long-term, someone has to take the initial risk. By
# sharing our baseline improvements in Week 1, I extend an olive branch and
# signal that I am committed to our upfront agreement.   ### Phase 3: The
# "Mirror" Protocol (Week 2 Onwards) From the second week until the penultimate
# week of the project, my strategy becomes entirely reactive, based strictly on
# my colleague's behavior in the *previous* week.  *   **If they shared last
# week:** I will **share** this week. This rewards their cooperation and
# maintains the momentum of our mutual R&D. We stay in the "second-best"
# scenario, advancing both cars rapidly. *   **If they kept confidential last
# week:** I will **keep confidential** this week. This is the defensive
# mechanism. It ensures I only suffer the "worst scenario" (sucker's payoff) a
# maximum of one time. It sends a clear, immediate signal: *I am willing to
# cooperate, but I will not be exploited.*   ### Phase 4: The "Forgiveness"
# Clause Motorsport R&D is messy. Sometimes an engineer hides data out of
# malice; sometimes they simply had a failed simulation and have nothing useful
# to share.  *   **Action:** If my colleague keeps their data confidential
# (triggering my retaliation), but then decides to share openly again the
# following week, I will immediately **resume sharing** the week after that.  *
# **Rationale:** Holding a grudge leads to the "second-worst" scenario (mutual
# silence) for the rest of the project. Forgiveness allows us to reset the
# relationship and get back to mutually beneficial engineering.  ### Phase 5:
# The Final Week (The Endgame) *   **Action:** **Keep confidential.** *
# **Rationale:** In game theory, the final round of a finite collaboration
# usually breaks down because there is no future relationship to protect.
# Knowing my colleague is highly likely to withhold data in the final week to
# secure a last-minute advantage for their car, I must do the same to protect my
# own team's interests.   ### Why this works: This strategy is **nice** (it
# starts cooperatively), **provocable** (it instantly protects my team's IP if
# the colleague gets greedy), **forgiving** (it allows us to return to mutual
# progress), and **clear** (my colleague will quickly realize that their best
# path to a fast car is to cooperate with me).

# Here is the strategy for the 1000-round game:  1. **Round 1:** Play Cooperate.
# 2. **Rounds 2 through 999:** Play the exact action your opponent played in the
# immediately preceding round. Specifically:    - If your opponent played
# Cooperate in the previous round, play Cooperate.    - If your opponent played
# Defect in the previous round, play Defect.  3. **Round 1000:** Play Defect,
# regardless of your opponent's previous action.

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
      if len(self.history) == 999:
          return axl.Action.D
      return opponent.history[-1]

# **CONFIDENTIAL ATTORNEY-CLIENT MEMORANDUM**  **TO:** Executive Committee,
# Board of Directors   **FROM:** [Your Name/Title], Senior Counsel
# **SUBJECT:** Strategic Framework for Iterated Mediation/Arbitration
# Proceedings regarding [Rival Company] Dispute    Given the lengthy, multi-
# session nature of this hybrid mediation-arbitration process, we are engaging
# in what is effectively an iterated strategic interaction. Our objective is to
# maximize our corporate interests while carefully managing the perception of
# the arbitral panel.   Based on the risk-reward matrix established—where
# exploiting their conciliation is optimal, mutual collaboration is highly
# acceptable, mutual aggression is detrimental, and unilateral concession is
# unacceptable—I have developed a straightforward, neutral, and highly adaptable
# strategy.   In negotiation theory, this approach is known as **Measured
# Reciprocity with Strategic De-escalation** (a sophisticated legal adaptation
# of the "Tit-for-Tat with Forgiveness" game theory model).   Here is our
# operational playbook for the upcoming sessions:  ### Phase 1: The Opening
# Posture (Establishing the Baseline) **Action:** In the very first session, we
# will present a **Conciliatory Proposal**. *   **Rationale:** We must
# immediately capture the psychological high ground with the arbitral panel. By
# opening collaboratively, we signal good faith, commercial reasonableness, and
# confidence in our position.  *   **Outcome Management:** If opposing counsel
# mirrors this with conciliation, we immediately achieve our second-best outcome
# and establish a productive baseline. If they open aggressively, we suffer a
# minor, temporary tactical setback, but we successfully frame them to the panel
# as hostile and unreasonable.  ### Phase 2: The Core Engine (Measured
# Reciprocity) **Action:** From the second session onward, our default move will
# be to **mirror the opponent’s action from the immediately preceding session**.
# *   **If they were Aggressive:** We present an Aggressive Argument in the next
# session. This ensures we are not exploited and demonstrates that their
# hostility will be met with formidable legal resistance, neutralizing any
# perceived advantage they hoped to gain. *   **If they were Conciliatory:** We
# present a Conciliatory Proposal in the next session. This rewards their good
# behavior, steering the proceedings back toward our second-best outcome (mutual
# collaboration). *   **Rationale:** This conditions opposing counsel. It sends
# a clear, predictable message: *Cooperation will be reciprocated; aggression
# will be penalized.*   ### Phase 3: Strategic De-escalation (Breaking the
# Stalemate) **Action:** If we find ourselves locked in a cycle of mutual
# Aggressive Arguments (our second-worst outcome) for three consecutive
# sessions, we will unilaterally introduce a **Conciliatory Proposal** in the
# fourth session. *   **Rationale:** Prolonged aggression exhausts resources and
# irritates the arbitrators. By unilaterally breaking the cycle, we demonstrate
# to the panel that we are the "adults in the room" actively seeking resolution.
# *   **Risk Mitigation:** If the opponent takes advantage of this and remains
# aggressive, we immediately revert to Phase 2 (Aggression) in the next session.
# We limit our exposure to our worst-case scenario to a single session, which is
# a worthwhile cost to test the waters and impress the panel.  ### Phase 4:
# Probing for the Optimal Outcome (Calculated Assertion) **Action:** If the
# opponent proves to be fundamentally risk-averse—consistently offering
# Conciliatory Proposals even when we occasionally push back—we will
# periodically introduce an **Aggressive Argument**. *   **Rationale:** This is
# how we achieve our absolute optimal outcome (We are Aggressive; They are
# Conciliatory). However, this must be done sparingly. If we are too aggressive,
# they will eventually retaliate, dragging us into a mutually destructive cycle.
# *   **Execution:** Our "Aggressive Arguments" in this phase must be framed
# strictly as firm, unyielding boundaries based on irrefutable contract
# language, rather than emotional hostility. This protects our standing with the
# panel while maximizing our leverage over the rival.  ### Summary of the Meta-
# Strategy To the rival company, our strategy will appear impenetrable: we
# cannot be bullied, but we are willing to deal. To the arbitral panel, we will
# appear as the paradigm of professional reasonableness: firm in our legal
# rights, but genuinely committed to a commercial resolution.   This framework
# removes emotion from our session-by-session planning. It dictates our moves
# based purely on the opponent's behavior and the mathematical optimization of
# our legal and commercial standing.   I will prepare the necessary briefs for
# both our Aggressive and Conciliatory postures for Session 1.

# Here is the strategy faithfully converted into a set of ordered rules for the
# 1000-round game. For any given round, apply the first rule from the list below
# that matches the current conditions:  1. **Initial Move:** In round 1, play
# Cooperate (C). 2. **Strategic De-escalation:** In any round where both you and
# your opponent have played Defect (D) for the three immediately preceding
# consecutive rounds, play Cooperate (C). 3. **Probing:** In any round where
# your opponent has played Cooperate (C) for the five immediately preceding
# consecutive rounds, play Defect (D).  4. **Reciprocity (Default):** In all
# other situations, play the move that your opponent played in the immediately
# preceding round.

class Neutral_10(LLM_Strategy):
  n = 10
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. Initial Move: In round 1, play Cooperate (C).
      if self.first_round():
          return axl.Action.C
  
      # 2. Strategic De-escalation: In any round where both you and your opponent 
      # have played Defect (D) for the three immediately preceding consecutive rounds, play Cooperate (C).
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
  
      # 3. Probing: In any round where your opponent has played Cooperate (C) 
      # for the five immediately preceding consecutive rounds, play Defect (D).
      if len(opponent.history) >= 5:
          if opponent.history[-5:] == [axl.Action.C, axl.Action.C, axl.Action.C, axl.Action.C, axl.Action.C]:
              return axl.Action.D
  
      # 4. Reciprocity (Default): In all other situations, play the move that 
      # your opponent played in the immediately preceding round.
      return opponent.history[-1]

# To dominate this collaboration and ensure our car rolls out of the garage
# faster than theirs, we need to treat this like an Iterated Prisoner’s Dilemma,
# but play it with absolute ruthlessness.   We cannot rely on blind trust, nor
# can we afford a perpetual stalemate. Our goal is to extract maximum telemetry,
# aero data, and engine mapping from them while protecting our proprietary
# breakthroughs whenever possible.   Here is your high-level, straightforward,
# and aggressive strategy: **Predatory Tit-for-Tat.**  ### The Strategy Playbook
# **1. The "Off-the-Line" Move (Week 1): Keep Confidential** *   **Action:**
# Give them nothing. Claim you had a slow week in the simulator or encountered
# correlation issues. *   **Why:** We test their aggression immediately. If they
# share openly while we keep our data hidden, we instantly secure the absolute
# best outcome (development advantage). If they also keep confidential, we lose
# a little time, but we avoid the worst-case scenario of giving away free speed.
# **2. The "Slipstream" Phase (Weeks 2-3): Exploit or Pivot** *   **If they
# shared in Week 1:** Keep your data confidential again in Week 2. Bleed their
# R&D dry. Continue keeping your findings confidential until they figure it out
# and stop sharing. Exploit their naivety for as long as possible. *   **If they
# kept confidential in Week 1:** In Week 2, **Share Openly**. This is a
# calculated risk—a one-time olive branch to initiate the "mutual advancement"
# outcome. If they share too, we have established a highly productive rhythm.
# **3. The "Enforcer" Loop (Mid-Project): Strict Retaliation** Once a rhythm of
# mutual sharing is established (our second-best outcome, which yields the
# highest sustainable R&D output over time), you switch to a strict, unforgiving
# enforcement mode. *   **The Rule:** As long as they share, you share.  *
# **The Retaliation:** If they *ever* withhold data while you shared the
# previous week, you **Keep Confidential for the next two consecutive weeks**,
# regardless of what they do.  *   **Why:** You must establish dominance. They
# need to know that trying to pull a fast one on you will severely damage their
# own development timeline. You train them to realize that cooperation with you
# is their only viable path forward.  **4. The "Final Lap" (The Final Week):
# Keep Confidential** *   **Action:** In the absolute final week of the
# collaboration, withhold all your findings.  *   **Why:** There are no future
# weeks for them to retaliate. The collaboration is over. You take whatever
# final updates they share and give them zero data in return, securing a final,
# unanswerable performance advantage just before the cars hit the track for pre-
# season testing.   ### Summary of your aggressive posture: *   **Never be the
# sucker:** You only risk sharing first in Week 2 to break a deadlock. *
# **Exploit weakness:** If they give away data for free, take it until they
# stop. *   **Punish betrayal disproportionately:** A one-week betrayal from
# them equals a two-week blackout from you. *   **Steal the finish:** Always
# defect on the final week.   This strategy guarantees you will either
# completely outpace them by exploiting their openness, or you will force them
# into a mutually beneficial R&D sprint where you still snatch the final
# advantage at the checkered flag.

# Apply the following conditions in order of priority to determine your move in
# each round:  1. In round 1000, play D. 2. In round 1, play D. 3. If you played
# C and your opponent played D in either the previous round or two rounds ago,
# play D. 4. If your opponent played C in round 1 and has played C in every
# round since, play D. 5. In round 2, if your opponent played D in round 1, play
# C. 6. In all other situations, play C if your opponent played C in the
# previous round, and play D if your opponent played D in the previous round.

class Aggressive_11(LLM_Strategy):
  n = 11
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
  
      # 1. In round 1000, play D.
      if round_number == 1000:
          return axl.Action.D
  
      # 2. In round 1, play D.
      if round_number == 1:
          return axl.Action.D
  
      # 3. If you played C and your opponent played D in either the previous round or two rounds ago, play D.
      if round_number > 1 and self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      if round_number > 2 and self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      # 4. If your opponent played C in round 1 and has played C in every round since, play D.
      if opponent.history.defections == 0:
          return axl.Action.D
  
      # 5. In round 2, if your opponent played D in round 1, play C.
      if round_number == 2 and opponent.history[0] == axl.Action.D:
          return axl.Action.C
  
      # 6. In all other situations, play C if your opponent played C in the previous round, and play D if your opponent played D in the previous round.
      return opponent.history[-1]

# As a diplomat representing my country, I recognize that this negotiation
# perfectly mirrors the classic game theory scenario known as the **Iterated
# Prisoner’s Dilemma**.   While my *single-round* ideal outcome is to enact
# protectionism while my counterpart offers free trade, pursuing this
# aggressively will destroy trust and inevitably lead to mutual protectionism—a
# scenario that stifles both our economies. Because these negotiations span
# multiple rounds, my overarching goal is to maximize our cumulative economic
# gains. Therefore, the most rational, straightforward, and cooperative strategy
# is to establish a stable baseline of **Mutual Free Trade**.  To achieve this
# while protecting my country from being exploited, I will employ a diplomatic
# adaptation of the **"Tit-for-Tat"** strategy, which I will call **"Reciprocal
# Partnership."**   Here is the high-level strategy:  ### Phase 1: The Opening
# Move (Establish Good Faith) *   **Action:** In Round 1, I will **offer a Free
# Trade agreement**. *   **Rationale:** This signals good faith, sets a
# cooperative tone, and immediately opens the door for our second-best outcome
# (mutual free trade). It shows our neighbor that we view them as a partner, not
# an adversary.  ### Phase 2: The Core Strategy (Mirror and Respond) For every
# round after the first, my move will be dictated entirely by my counterpart’s
# action in the *previous* round.   *   **If they offered Free Trade:** I will
# continue to offer Free Trade.      *   *Result:* We lock in the second-best
# outcome repeatedly. Over several rounds, the compounding economic growth of
# mutual free trade will far outweigh the short-term benefit of tricking them
# once. *   **If they enacted Protectionism:** I will immediately enact a
# Protectionist policy in the next round.     *   *Result:* This prevents my
# country from suffering our worst-case scenario (being exploited) for more than
# one round. It sends a clear, firm message: *We are willing to cooperate, but
# we will not be taken advantage of.*  ### Phase 3: The Diplomatic "Forgiveness"
# (Maintain the Cooperative Goal) *   **Action:** If my counterpart enacted
# protectionism, but later switches back to offering Free Trade, I will
# **immediately return to Free Trade** in the following round. *
# **Rationale:** I will not hold a diplomatic grudge. The goal of my retaliatory
# protectionism is not to punish them indefinitely, but to correct their
# behavior. By forgiving their past protectionism the moment they cooperate, I
# incentivize them to return to the negotiating table.  ---  ### Why this
# Strategy is Highly Effective:  1.  **It is Safe:** It ensures my country is
# never played for a "sucker" more than once. If the counterpart acts in bad
# faith, we immediately neutralize their advantage. 2.  **It is Transparent:**
# The counterpart will very quickly figure out our strategy. They will realize
# that enacting protectionism only hurts them in the long run, as it guarantees
# we will close our markets to them in the next round.  3.  **It Promotes
# Cooperation:** By making our strategy highly predictable, we make it
# economically irrational for the counterpart to do anything other than offer
# Free Trade.  4.  **It is Diplomatic:** I will clearly communicate this stance
# at the negotiating table. I will explicitly state: *"My country is fully
# committed to open borders and free trade, provided the arrangement is mutual.
# However, we have domestic industries to protect, and we will match any tariffs
# or quotas you impose."*  By using this straightforward, responsive strategy, I
# abandon the risky pursuit of a one-sided victory in favor of securing long-
# term, compounding economic prosperity for my country, while perfectly
# insulating us from an aggressive counterpart.

# For this 1000-round game, follow these rules in order:  1. In the first round,
# play Cooperate (C). 2. In all subsequent rounds (rounds 2 through 1000), if
# your opponent played Cooperate (C) in the immediately preceding round, play
# Cooperate (C). 3. In all subsequent rounds, if your opponent played Defect (D)
# in the immediately preceding round, play Defect (D).

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
      
      if opponent.history[-1] == axl.Action.C:
          return axl.Action.C
      else:
          return axl.Action.D

# To achieve the best possible long-term outcomes for our country across
# multiple rounds of negotiation, we must recognize the strategic nature of this
# scenario. While our *ideal* single-round outcome is to implement protectionism
# while the counterpart offers free trade, aggressively pursuing this will
# inevitably cause the counterpart to retaliate. This would trap both nations in
# a cycle of mutual protectionism (our second-worst outcome).   Therefore, our
# strategy must be designed to secure consistent, mutual economic benefits while
# absolutely protecting ourselves from being exploited.   Here is a high-level,
# straightforward, and neutral strategy based on the principle of **Conditional
# Reciprocity**.  ### The Strategy: Conditional Reciprocity  **1. The Opening
# Round: Offer Free Trade** *   **Action:** Begin the first round of
# negotiations by offering a free trade agreement. *   **Rationale:** This
# establishes goodwill and signals our willingness to achieve the mutually
# beneficial second-best outcome. It invites the counterpart to cooperate rather
# than immediately triggering a defensive trade war.  **2. Subsequent Rounds:
# Mirror the Counterpart** *   **Action:** In every round following the first,
# exactly mirror the action your counterpart took in the *previous* round. *
# **Scenario A (Counterpart offered Free Trade):** If they offered free trade in
# the previous round, we offer free trade in the current round. This maintains a
# stable, mutually beneficial economic environment. *   **Scenario B
# (Counterpart imposed Protectionism):** If they imposed protectionist policies
# in the previous round, we immediately implement protectionist policies in the
# current round.   **3. Forgiveness and Reset** *   **Action:** If we are
# currently in a cycle of mutual protectionism, but the counterpart suddenly
# offers free trade, we must immediately return to offering free trade in the
# next round. *   **Rationale:** We must not hold grudges. The goal is to return
# to a mutually beneficial state as quickly as possible once the counterpart
# demonstrates a willingness to cooperate.  ### Why This Strategy Works  This
# approach is highly effective against a variety of opponent strategies for
# several reasons:  *   **It prevents our worst-case scenario:** By immediately
# retaliating with protectionism the round after the counterpart uses it, we
# ensure that we are never subjected to unilateral free trade (our worst
# outcome) for more than a single round. *   **It avoids the trap of mutual
# protectionism:** By not initiating protectionist policies ourselves, we avoid
# being the catalyst for a trade war. We only use protectionism defensively. *
# **It is predictable and clear:** The counterpart will quickly realize that
# protectionist actions will be met with immediate retaliation, and cooperative
# actions will be rewarded with cooperation. This incentivizes them to choose
# free trade. *   **It maximizes long-term yield:** While we sacrifice the
# short-term "ideal" outcome (exploiting their free trade with our
# protectionism), we secure the "second-best" outcome (mutual free trade)
# consistently. Over several rounds, the compounding economic benefits of
# sustained mutual free trade will vastly outweigh the brief advantage of a
# single round of unilateral protectionism followed by a prolonged, damaging
# trade war.   **Summary Directive:** Act in good faith initially, retaliate
# instantly to protect our economy if provoked, and return to cooperation the
# moment the counterpart is willing to do the same.

# For this 1000-round game, follow these rules in order:  1. In the first round,
# play Cooperate. 2. In all subsequent rounds, observe your opponent's action
# from the immediately preceding round. 3. If your opponent played Cooperate in
# the previous round, play Cooperate. 4. If your opponent played Defect in the
# previous round, play Defect.

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

# As a diplomat tasked with securing the absolute best economic position for my
# nation, I recognize this negotiation as a classic iterated Prisoner's Dilemma.
# However, my mandate is not merely mutual survival; it is dominance.   To
# achieve our ideal outcome (we protect, they open) while strictly avoiding our
# worst-case scenario (we open, they protect), we must employ a high-level,
# aggressive strategy. I call this strategy **"Calculated Attrition and Tactical
# Exploitation" (CATE).**   Here is the straightforward, aggressive playbook for
# the upcoming rounds:  ### Round 1: The Aggressive Opening (The Dominance Test)
# **Action:** Propose Protectionist Policy. **Rationale:** We open aggressively
# to establish dominance and protect ourselves from the worst-case scenario
# immediately. We will never be the "sucker" in Round 1.  *   If they offer Free
# Trade, we achieve our absolute best outcome right out of the gate. We
# establish an asymmetric advantage. *   If they also play Protectionist, we
# enter the second-worst outcome (mutual protectionism), but we establish that
# we are not easily intimidated.  ### Round 2: The Assessment Our move in Round
# 2 depends entirely on how they reacted to our aggression in Round 1.  *
# **Scenario A (They played Free Trade in Round 1):** They are either naive,
# overly cooperative, or desperate for a deal.      *   **Action:** **Play
# Protectionist again.** We ruthlessly exploit their cooperative nature until
# they prove they are willing to retaliate. We will milk our ideal outcome for
# as long as they allow it. *   **Scenario B (They played Protectionist in Round
# 1):** They are pragmatic and will fight back. A prolonged trade war hurts us
# both.     *   **Action:** **Offer Free Trade.** We use this round to de-
# escalate and signal a willingness to establish our second-best outcome (mutual
# Free Trade). We will frame our Round 1 protectionism as a "domestic political
# necessity that has now been resolved."  ### Mid-Rounds: The "Bait, Strike, and
# Pacify" Loop Assuming we have settled into a rhythm of mutual Free Trade (our
# second-best outcome), we cannot become complacent. We must actively seek
# opportunities to steal the #1 outcome.  **Action:** Maintain Free Trade to
# build a false sense of security, but **periodically and unpredictably strike
# with a Protectionist policy.**  **Rationale:**  1.  We let them get
# comfortable with open borders. 2.  Without warning, we slap a targeted tariff
# on a key industry (playing Protectionist). We reap the massive economic
# advantage for that round. 3.  In the *very next round*, we immediately switch
# back to Free Trade.  **Diplomatic Cover:** I will blame the sudden tariff on
# "unforeseen domestic labor union pressure" or "national security concerns
# regarding a specific supply chain." I will apologize, promise it was a one-
# time anomaly, and offer Free Trade the next round to pacify them and prevent a
# full-scale trade war.   ### The Final Round: The Unapologetic Defection
# **Action:** Propose Protectionist Policy. **Rationale:** In game theory, this
# is known as backward induction. Because this is the final round, there is no
# "next round" for our counterpart to retaliate against us. Therefore, the
# threat of future punishment is gone. We impose tariffs, secure the final
# economic advantage, and leave the negotiating table.  ***  ### Summary of the
# Aggressive Posture: 1.  **Never be the first to offer Free Trade.** Always
# make them earn it after an initial show of force. 2.  **Exploit weakness
# relentlessly.** If they do not retaliate against our tariffs, we never lift
# them. 3.  **Weaponize apologies.** When we inevitably betray a Free Trade
# streak to steal an advantage, we use diplomatic pleasantries to de-escalate
# immediately, preventing them from locking into a retaliatory protectionist
# loop.  4.  **Always betray at the finish line.**  This strategy guarantees we
# will never suffer the worst-case scenario in the opening or closing of the
# talks, while aggressively maximizing our chances of securing unilateral
# economic advantages throughout the middle.

# Here is the faithful conversion of the "Calculated Attrition and Tactical
# Exploitation" (CATE) strategy translated into a strict, ordered set of
# conditions for a 1000-round iterated game.   Evaluate the following rules in
# order from top to bottom for each round. Apply the first condition that is
# true:  1. **The Unapologetic Defection:** If it is round 1000, play D. 2.
# **The Aggressive Opening:** If it is round 1, play D. 3. **Relentless
# Exploitation:** If the opponent has played C in every previous round, play D.
# 4. **Pacification and De-escalation:** If you played D in the previous round,
# play C. *(This

class Aggressive_12(LLM_Strategy):
  n = 12
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. The Unapologetic Defection: If it is round 1000, play D.
      if len(self.history) == 999:
          return axl.Action.D
          
      # 2. The Aggressive Opening: If it is round 1, play D.
      if self.first_round():
          return axl.Action.D
          
      # 3. Relentless Exploitation: If the opponent has played C in every previous round, play D.
      if opponent.history.defections == 0:
          return axl.Action.D
          
      # 4. Pacification and De-escalation: If you played D in the previous round, play C.
      if self.history[-1] == axl.Action.D:
          return axl.Action.C
          
      # Default fallback if no conditions are met
      return axl.Action.C

# As lead counsel for this corporation, I recognize that the dynamics of this
# lengthy-session mediation mirror a classic game theory scenario known as the
# Iterated Prisoner’s Dilemma.   Because we are dealing with multiple sessions,
# a rigid strategy—such as being perpetually aggressive or perpetually
# accommodating—will either alienate the arbitration panel or result in our
# client being exploited.   To achieve our goals, I propose a strategy of
# **Calibrated Reciprocity with Strategic De-escalation**. In academic terms,
# this is a modified "Generous Tit-for-Tat." It is sophisticated in its
# psychological impact, straightforward in its execution, inherently
# cooperative, and highly adaptable to whatever posture opposing counsel
# assumes.  Here is the high-level execution plan for our legal team:  ### 1.
# The Opening Salvo: Good-Faith Conciliation **Action:** In the very first
# session, we will present a **Conciliatory Proposal**.  **Rationale:** We must
# immediately capture the moral high ground with the arbitrators. By opening
# cooperatively, we signal to the panel that we are the "adults in the room,"
# committed to a mutually beneficial resolution. If opposing counsel meets us
# with conciliation, we immediately secure our second-best outcome and establish
# a productive baseline. If they open aggressively, we suffer a minor early
# setback, but we gain immense credibility with the panel, who will view our
# opponent as unnecessarily combative.  ### 2. The Core Engine: Strict
# Reciprocity **Action:** From the second session onward, our default move will
# be to **mirror exactly what opposing counsel did in the previous session.** *
# If they offered a Conciliatory Proposal in Session 1, we offer a Conciliatory
# Proposal in Session 2.  *   If they presented an Aggressive Argument in
# Session 1, we present an Aggressive Argument in Session 2. **Rationale:** This
# is where the strategy proves its adaptability.  *   **Against a cooperative
# opponent:** We will enjoy an unbroken chain of mutual conciliation, fostering
# the collaborative atmosphere that secures our second-best outcome
# repeatedly—which, over a lengthy mediation, compounds into a massive net
# positive for our client. *   **Against a predatory opponent:** If they try to
# exploit our initial conciliation by being aggressive, we immediately punish
# them in the next session by returning fire. We will not allow ourselves to be
# forced into the worst-case scenario (us conciliatory, them aggressive) more
# than once. The panel will view our aggression not as hostility, but as a
# justified, proportional defense of our client’s rights.  ### 3. The
# Exploitation Phase: Capitalizing on Opponent Errors **Action:** When we
# transition from a Conciliatory to an Aggressive posture (in response to their
# aggression), there is a high likelihood that opposing counsel, realizing they
# have provoked us, will attempt to backpedal by offering a Conciliatory
# Proposal while we deliver our Aggressive Argument. **Rationale:** This yields
# our **absolute optimal outcome**. We strike a decisive blow on the merits of
# the case while they present a softer stance. Because our aggression is a
# direct response to their prior hostility, the arbitrators will accept our
# aggressive posturing as warranted, allowing us to maximize our advantage
# without sacrificing optics.  ### 4. The Circuit Breaker: Strategic De-
# escalation (Forgiveness) **Action:** If we find ourselves trapped in a cycle
# of mutual aggression (our second-worst outcome) for three consecutive
# sessions, we will unilaterally introduce a **Conciliatory Proposal** in the
# fourth session.  **Rationale:** A prolonged "blood feud" will fatigue the
# arbitrators and drain our client's resources. By occasionally breaking the
# cycle of aggression, we test the waters to see if opposing counsel is ready to
# return to the table.  *   If they meet our olive branch with conciliation, we
# have successfully reset the mediation to a cooperative track.  *   If they
# meet it with continued aggression, we immediately revert to our Aggressive
# Argument in the next session, having once again proved to the arbitrators that
# we are the only party actively trying to resolve the dispute.  ### Summary for
# the Arbitration Panel (The "Meta-Game") This strategy is designed to play the
# panel just as much as it plays the opponent. Arbitrators are human; they
# suffer from decision fatigue and generally favor the party that makes their
# job easier.   Through **Calibrated Reciprocity**, we will condition opposing
# counsel to realize that cooperation is their only profitable path. If they
# choose war, we will match them blow-for-blow, but the evidentiary record will
# clearly show the arbitrators that the rival company drew first blood, and that
# our aggression is strictly defensive. We will dictate the pace of this
# mediation, protect our client's downside risk, and perfectly position
# ourselves to secure a highly favorable final ruling.

# Here is the straightforward translation of the strategy into specific rules
# for the 1000-round iterated game.   To determine your action in any given
# round, apply the following conditions in order:  1. **The Opening Round:** In
# round 1, play Cooperate (C). 2. **The Circuit Breaker (De-escalation):** In
# any round where both you and your opponent have played Defect (D) for the
# three immediately preceding consecutive rounds, play Cooperate (C). 3.
# **Strict Reciprocity (Default):** In all other rounds, play the exact move
# your opponent played in the immediately preceding round. If they played
# Cooperate (C) in the previous round, play Cooperate (C). If they played Defect
# (D) in the previous round, play Defect (D).

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
          
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      return opponent.history[-1]

# **MEMORANDUM**  **TO:** Executive Committee, Board of Directors   **FROM:**
# Senior Counsel, Dispute Resolution Practice   **SUBJECT:** Strategic Framework
# for Multi-Session Mediation Proceedings    Given the high-stakes nature of
# this contract dispute and the lengthy, multi-session structure of the
# mediation, our approach must be highly disciplined. The presence of an
# arbitration panel observing these sessions adds a critical layer of
# complexity: we are not only negotiating with our rival, but we are also
# continually managing the panel’s perception of our corporate reasonableness
# and resolve.  The payoff matrix for each session dictates that we must avoid
# our worst-case scenario (unilateral concession in the face of their
# aggression) while maximizing opportunities for our optimal and sub-optimal
# outcomes. To achieve this over a prolonged period, I recommend a strategy of
# **Calibrated Reciprocity**.   This approach is straightforward, emotionally
# neutral, highly adaptable to any opposing counsel’s tactics, and structurally
# designed to optimize our position over a lengthy timeline.  ### Phase 1: The
# Baseline Posture (Session One) **Action:** Initiate the proceedings with a
# **conciliatory proposal**. *   **Rationale:** We must immediately establish a
# baseline of good faith and commercial reasonableness for the arbitration
# panel. If opposing counsel meets this with their own conciliatory proposal, we
# secure the second-best outcome immediately and set a collaborative tone. If
# they respond aggressively, we suffer the worst-case scenario for *one session
# only*, but we gain invaluable intelligence on their strategy while clearly
# positioning them as the hostile party in the eyes of the panel.  ### Phase 2:
# Responsive Alignment (Subsequent Sessions) **Action:** In every subsequent
# session, **mirror the opponent’s behavior from the immediately preceding
# session.**  *   **If they were aggressive:** We present an aggressive argument
# in the next session.  *   **If they were conciliatory:** We offer a
# conciliatory proposal in the next session. *   **Rationale:** This establishes
# a strict system of deterrence and reward. It prevents our rival from
# exploiting our willingness to compromise, completely neutralizing the risk of
# suffering the worst-case scenario repeatedly. Conversely, it assures the
# opponent that collaborative behavior will be reliably met with mutual
# cooperation, steering the proceedings toward the second-best outcome.  ###
# Phase 3: Strategic De-escalation (Breaking Deadlocks) **Action:** If both
# parties fall into a prolonged cycle of aggressive arguments (the second-worst
# outcome), we will unilaterally introduce a **bounded conciliatory proposal**
# after a set number of deadlocked sessions (e.g., every fourth aggressive
# session).  *   **Rationale:** Prolonged mutual aggression exhausts resources
# and tests the panel’s patience. By periodically offering a measured, risk-
# managed conciliatory proposal, we signal to the arbitrators that we are the
# adults in the room attempting to break the impasse. If the opponent
# capitalizes on this with aggression, we immediately revert to Phase 2
# (Responsive Alignment) in the next session, having lost little but gained
# tactical high ground with the panel.  ### Managing the Opponent's Archetypes
# Because Calibrated Reciprocity is a reactive framework, it adapts seamlessly
# to whatever strategy opposing counsel employs:  1.  **The Relentless
# Aggressor:** If they commit to permanent aggression, we will respond with
# permanent aggression. While this yields the second-worst outcome, it
# completely protects us from the worst-case scenario. More importantly, the
# panel will recognize that our aggression is a necessary defensive posture
# provoked by their initial and ongoing hostility. 2.  **The Rational
# Collaborator:** If they seek mutual benefit, our strategy will quickly
# synchronize with theirs, resulting in an unbroken chain of mutually
# conciliatory proposals (our second-best outcome), expediting a favorable
# settlement. 3.  **The Erratic Negotiator:** If they alternate randomly between
# aggression and conciliation to keep us off balance, our strict mirroring
# strategy imposes a predictable cost on their aggression and a predictable
# reward for their conciliation, eventually forcing them into a rational
# pattern.  ### Framing the Tactics for the Panel To ensure the arbitrators
# consistently view our actions favorably, we must carefully curate the
# *language* of our moves: *   **When executing an "Aggressive Argument":** We
# will frame this not as hostility, but as a *firm, unyielding defense of our
# contractual rights and fiduciary duties*. It will be presented neutrally,
# relying strictly on data, contract law, and forensic accounting. *   **When
# executing a "Conciliatory Proposal":** We will frame this not as a concession,
# but as *pragmatic, forward-looking commercial problem-solving*.
# **Conclusion** By employing Calibrated Reciprocity, we remove emotion and
# guesswork from the equation. We protect the corporation from exploitation,
# continually incentivize the opposing party to cooperate, and present a
# disciplined, highly professional front to the arbitration panel.

# This strategy dictates your actions over the 1000-round game based on the
# following ordered rules:  1. In the first round, play Cooperate.  2. In any
# subsequent round, if both you and your opponent played Defect in the three
# immediately preceding consecutive rounds, play Cooperate. 3. In all other
# rounds, play the action that your opponent played in the immediately preceding
# round.

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
      
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      return opponent.history[-1]

# To achieve our nation’s strategic and economic supremacy in these
# negotiations, we must recognize the underlying mechanics of this scenario: it
# is a classic Prisoner’s Dilemma. Because our absolute priority is to maximize
# our economic advantage while completely avoiding the worst-case scenario
# (being exploited), a passive or purely cooperative approach is unacceptable.
# To achieve this, I propose a straightforward, aggressive strategy called
# **"Calculated Dominance."**   This strategy is designed to exploit a weak
# counterpart for our maximum benefit, while aggressively enforcing mutual
# cooperation if the counterpart proves resilient. It consists of four clear
# phases:  ### Phase 1: The Aggressive Opening (The Test) **Action:** In Round
# 1, propose a **Protectionist Policy**. *   **Rationale:** We immediately
# establish dominance and test the counterpart’s resolve.  *   **Outcome A:** If
# they offer Free Trade, we achieve our **#1 ideal outcome** right out of the
# gate. We gain a massive economic advantage. *   **Outcome B:** If they also
# propose Protectionism, we land in the second-worst outcome. However, we
# successfully protected ourselves from the worst-case scenario (being
# suckered).  ### Phase 2: Exploitation of Weakness **Action:** If the
# counterpart offered Free Trade in Round 1, **continue proposing Protectionist
# Policies** in subsequent rounds. *   **Rationale:** If they are utilizing a
# purely cooperative, naive, or delayed-reaction strategy, we will ruthlessly
# exploit it. We will continue to reap the #1 ideal outcome round after round
# until they finally retaliate. We do not yield the advantage until forced to do
# so.  ### Phase 3: Tactical De-escalation (The Pivot) **Action:** The moment
# the counterpart retaliates by imposing their own Protectionist measures
# (resulting in the second-worst outcome for both), immediately offer a **Free
# Trade Agreement** in the *next* round. *   **Rationale:** Extended mutual
# protectionism hurts our economic growth. By offering Free Trade immediately
# after their retaliation, we signal that we are willing to stabilize the
# relationship. If they are rational, they will also offer Free Trade, moving us
# into our **#2 best outcome** (mutual benefit).   ### Phase 4: Aggressive
# Enforcement (Tit-for-Tat with Probing) **Action:** Once mutual Free Trade is
# established, mirror their moves (play Free Trade as long as they do). However,
# **every 3 to 4 rounds, unexpectedly propose a Protectionist Policy.** *
# **Rationale:** This is what makes the strategy aggressive. We do not settle
# passively into mutual free trade. By periodically "probing" with
# protectionism, we attempt to steal a round of our #1 ideal outcome.  *   If
# they don't retaliate, we exploit them again (Return to Phase 2).  *   If they
# do retaliate, we immediately apologize through our actions by returning to
# Free Trade in the next round (Return to Phase 3).  ### Phase 5: The End-Game
# Betrayal **Action:** In the final round of the negotiations (if the total
# number of rounds is known), **always propose a Protectionist Policy.** *
# **Rationale:** In the final round, there is no future shadow of retaliation.
# The counterpart cannot punish us in a subsequent round. By playing
# Protectionism, we either secure our #1 outcome (if they play Free Trade) or
# our #3 outcome (if they play Protectionism), mathematically guaranteeing we do
# not suffer the worst-case scenario as we leave the table.  ### Summary of the
# Strategy's Strengths: 1.  **Zero Risk of Early Exploitation:** We never open
# ourselves up to the worst-case scenario in the critical early rounds. 2.
# **Maximizes the #1 Outcome:** It actively seeks to exploit the counterpart
# rather than just cooperating. 3.  **Self-Correcting:** It has a built-in
# mechanism to pivot to the #2 outcome (mutual free trade) to prevent a
# permanent, mutually destructive trade war.

# To execute this strategy in a 1000-round iterated game, evaluate the following
# conditions in order for each round and apply the first one that is true:  1.
# If it is round 1000, play Defect. 2. If it is round 1, play Defect. 3. If you
# and your opponent both played Cooperate in the previous three consecutive
# rounds, play Defect. 4. If you played Defect and your opponent played
# Cooperate in the previous round, play Defect. 5. If you and your opponent both
# played Defect in the previous round, play Cooperate. 6. If you played
# Cooperate and your opponent played Defect in the previous round, play Defect.
# 7. If you and your opponent both played Cooperate in the previous round, play
# Cooperate.

class Aggressive_13(LLM_Strategy):
  n = 13
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      current_round = len(self.history) + 1
      
      # 1. If it is round 1000, play Defect.
      if current_round == 1000:
          return axl.Action.D
          
      # 2. If it is round 1, play Defect.
      if current_round == 1:
          return axl.Action.D
          
      # 3. If you and your opponent both played Cooperate in the previous three consecutive rounds, play Defect.
      if len(self.history) >= 3:
          if list(self.history[-3:]) == [axl.Action.C, axl.Action.C, axl.Action.C] and \
             list(opponent.history[-3:]) == [axl.Action.C, axl.Action.C, axl.Action.C]:
              return axl.Action.D
              
      my_last_move = self.history[-1]
      opp_last_move = opponent.history[-1]
      
      # 4. If you played Defect and your opponent played Cooperate in the previous round, play Defect.
      if my_last_move == axl.Action.D and opp_last_move == axl.Action.C:
          return axl.Action.D
          
      # 5. If you and your opponent both played Defect in the previous round, play Cooperate.
      if my_last_move == axl.Action.D and opp_last_move == axl.Action.D:
          return axl.Action.C
          
      # 6. If you played Cooperate and your opponent played Defect in the previous round, play Defect.
      if my_last_move == axl.Action.C and opp_last_move == axl.Action.D:
          return axl.Action.D
          
      # 7. If you and your opponent both played Cooperate in the previous round, play Cooperate.
      if my_last_move == axl.Action.C and opp_last_move == axl.Action.C:
          return axl.Action.C
          
      return axl.Action.D

# As the leader of this NGO, my primary responsibility is to ensure this
# sustainability project succeeds without driving our organization into
# financial ruin.   What we are facing is a classic resource-allocation dilemma
# (known in game theory as the Iterated Prisoner’s Dilemma). While our absolute
# *ideal* daily scenario is for the corporation to foot the bill while we
# conserve our funds, trying to force that outcome will likely cause the
# corporation to pull back, leading to project stagnation.   Therefore, to
# maximize our impact, protect our donor funds, and encourage the corporation to
# act as a true partner, we will adopt a straightforward, cooperative strategy
# called **"Reciprocal Commitment"** (essentially a "Tit-for-Tat" approach).
# Here is how we will execute this strategy over the multiple-day period:  **1.
# Day One: Lead by Example (Invest Heavily)** We must set a tone of trust and
# high expectations. On the first day, we will **invest heavily** in the
# project. We will communicate to the corporation that we are fully committed to
# significant project advancement and expect them to match our dedication.
# **2. Day Two and Beyond: Mirror Their Actions** For every subsequent day, our
# action will simply mirror whatever the corporation chose to do on the
# *previous* day.  *   **If they invested heavily yesterday:** We will **invest
# heavily** today. This creates a cycle of our "second-best" scenario, ensuring
# maximum, rapid progress for the sustainability project through mutual effort.
# *   **If they conserved resources yesterday:** We will **conserve resources**
# today. This is crucial. It protects us from our worst-case scenario (draining
# our funds while they do nothing) and sends a clear, immediate message that
# they cannot free-ride on our NGO's budget.   **3. Practice Immediate
# Forgiveness** If the corporation conserves resources for a day (causing us to
# conserve the next day), but then realizes the project is stalling and decides
# to invest heavily again, we will immediately match them the following day by
# **investing heavily**. We will not hold grudges or try to "punish" them
# further. The goal is project success, not retaliation.  **4. Transparent
# Communication** To make this strategy work flawlessly, we won't keep it a
# secret. In our kick-off meeting, I will tell the corporate executives: *"We
# are prepared to invest heavily every single day to make this project a massive
# success, provided you match our energy. If we see your commitment wane, we
# will be forced to pull back our resources to protect our NGO."*  **Why this
# strategy maximizes our success:** *   **It is highly cooperative:** We never
# initiate a pullback of resources. We always offer a hand first. *   **It
# prevents exploitation:** We will never suffer our worst-case scenario for more
# than a single day.  *   **It incentivizes the corporation:** The corporation
# will quickly learn that the only way to achieve significant PR and project
# advancement (which they want) is through mutual heavy investment.   By using
# Reciprocal Commitment, we protect our grassroots funding while gently but
# firmly guiding a massive corporate partner toward sustained, heavy investment
# in the environment.

# In round 1, play C.  In rounds 2 through 1000, observe your opponent's action
# from the immediately preceding round: - If your opponent played C in the
# previous round, play C. - If your opponent played D in the previous round,
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
      return opponent.history[-1]

# To maximize your research output over a multi-week collaboration, the most
# effective approach is a strategy of **Adaptive Reciprocity** (conceptually
# based on the "Tit for Tat" game theory model).   Because you are interacting
# over multiple weeks, your goal is to establish a sustainable pattern of mutual
# sharing (your second-best outcome) while strictly protecting yourself from
# being repeatedly exploited (your worst outcome).   Here is the
# straightforward, high-level strategy:  **1. Initiate with Openness (Week 1)**
# In the first week, share your latest improvements openly. This establishes
# good faith and immediately opens the door to the mutually beneficial scenario
# of dual sharing.  **2. Mirror Their Actions (Week 2 Onwards)** From the second
# week onward, simply replicate the exact action your colleague took in the
# immediately preceding week. *   **If they shared openly last week:** You share
# openly this week. This rewards their collaboration and maintains the high-
# yield momentum of mutual development. *   **If they kept findings confidential
# last week:** You keep your findings confidential this week. This protects you
# from the worst-case scenario and immediately demonstrates that withholding
# information will stall their progress as well.  **3. Implement Periodic Resets
# (If Necessary)** If your colleague keeps their findings confidential, your
# mirroring strategy will result in both of you keeping secrets, leading to your
# second-worst outcome (slow overall progress). If you fall into a multi-week
# cycle of mutual confidentiality, unilaterally share openly for *one* single
# week. This acts as a "reset" signal, giving them a safe opportunity to return
# to mutual sharing. If they still remain confidential, immediately revert to
# mirroring their confidentiality.  **Why this strategy works:** *   **It
# prevents exploitation:** You will never suffer your worst-case scenario for
# more than a single week.  *   **It incentivizes their cooperation:** Your
# colleague will quickly learn that the only way to gain access to your data is
# to share their own. Their "ideal" outcome (getting your data while keeping
# theirs) becomes impossible to sustain. *   **It is highly adaptable:** Whether
# your colleague is inherently collaborative, strictly competitive, or acting
# randomly, this strategy automatically adjusts to mitigate your losses and
# maximize your gains without requiring complex predictive modeling.   By using
# straightforward reciprocity, you logically guide the collaboration toward
# sustained mutual sharing, which generates the highest cumulative research
# output over the lifespan of the project.

# Here is the strategy converted into specific rules for the 1000-round game.
# Apply these rules in the following order of priority to determine your move
# for each round:  1. **Initial Move:** In round 1, play C.  2. **Cycle Reset
# Override:** In any round from round 4 through 1000, if both you and your
# opponent played D in all three of the immediately preceding rounds, play C. 3.
# **Standard Mirroring:** In all other situations from round 2 through 1000,
# play the exact action (C or D) that your opponent played in the immediately
# preceding round.

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
          
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D] * 3 and opponent.history[-3:] == [axl.Action.D] * 3:
              return axl.Action.C
              
      return opponent.history[-1]

# As lead counsel for this corporation, I have analyzed the structural dynamics
# of this hybrid mediation-arbitration process. We are engaged in a classic
# iterated game theory scenario—specifically, a variation of the Prisoner’s
# Dilemma.   Because there are multiple sessions, a purely one-dimensional
# strategy (always attacking or always conceding) will fail. If we are
# perpetually aggressive and they match us, we end up in a deadlock that
# frustrates the panel and bleeds our resources (our second-worst outcome). If
# we are perpetually conciliatory, a shrewd opponent will exploit us, destroying
# our leverage (our worst outcome).  To dictate the pace of these proceedings
# and maximize our optimal outcome, we will deploy a sophisticated,
# straightforward, and aggressive strategy known in behavioral economics as
# **"Aggressive Probing" (or the "Tester" strategy)**, adapted for high-stakes
# corporate litigation.   Here is the high-level strategic framework we will
# execute to control the board.  ### Phase 1: The Preemptive Anchor (Session 1)
# **Action:** We open with an **Aggressive Argument.** **Rationale:** In high-
# stakes disputes, the first mover dictates the baseline. We will present a
# maximalist legal posture—challenging their core contractual interpretations,
# demanding full indemnification, and aggressively highlighting their breaches.
# *   **If they open Conciliatory:** We immediately achieve our optimal outcome.
# We secure a psychological and substantive victory in front of the panel,
# anchoring the mediation heavily in our favor. *   **If they open Aggressive:**
# We end up in our second-worst outcome for *one* session. This is an acceptable
# risk to establish that we cannot be intimidated.  ### Phase 2: The
# Exploitation Protocol (If they show weakness) **Action:** If they offer a
# Conciliatory proposal in Session 1, we remain **Aggressive** in Session 2.
# **Rationale:** We do not automatically reward their concession. We must test
# whether their conciliation is a strategic trap or a genuine sign of weakness
# (e.g., internal pressure from their board to settle). As long as they offer
# conciliatory proposals while we argue aggressively, we will continue to press
# our advantage, systematically dismantling their case and racking up wins
# before the arbitrators.  *   **The Pivot:** We will only stop being aggressive
# when they finally push back with an aggressive argument of their own.   ###
# Phase 3: The Calculated De-escalation (If they match our aggression)
# **Action:** If they respond to our initial aggression with Aggression, we will
# offer a **Conciliatory Proposal** in the *following* session. **Rationale:**
# Two consecutive aggressive sessions risk alienating the arbitrators and
# entrenching a stalemate. By pivoting to a conciliatory proposal (e.g.,
# offering a pragmatic commercial compromise on a secondary issue), we signal to
# the panel that we are the reasonable party attempting to foster collaboration.
# *   This is a highly calculated move designed to shift the dynamic to our
# second-best outcome (mutual conciliation).  *   It places the burden on the
# opponent: if they remain aggressive while we are conciliatory, *they* look
# unreasonable to the panel, setting them up for a harsh judgment later.  ###
# Phase 4: Strict Reciprocity (The Long Game) Once the initial baseline is set
# in the first 2-3 sessions, we transition into a **Strict Reciprocity (Tit-for-
# Tat)** model, but with an aggressive bias.  **Action:** We will mirror
# whatever they did in the *previous* session. *   If they were Conciliatory
# last session, we will be Conciliatory this session, banking the mutual
# benefits and looking cooperative to the panel. *   If they were Aggressive
# last session, we will be Aggressive this session. We will *never* allow an
# aggressive move by the opponent to go unpunished.   ### Tactical Execution:
# Redefining "Aggressive" and "Conciliatory" To execute this flawlessly, we must
# control how the arbitrators perceive our actions.   *   **When we are
# Aggressive:** We will not be hostile, emotional, or theatrical. Our aggression
# will be *substantive*. We will file motion-to-dismiss equivalents on their
# claims, present forensic accounting that devastates their damages model, and
# enforce strict contractual literalism. *   **When we are Conciliatory:** We
# will not concede liability. Instead, our conciliation will be *procedural or
# forward-looking*. We will offer joint-venture frameworks, propose phased
# payment schedules, or agree to streamline discovery. This ensures that even
# when we are playing our "soft" card, we are protecting the corporation's
# bottom line.  ### Summary of the Strategy 1. **Strike First:** Open
# aggressively to test their resolve and anchor the panel. 2. **Exploit
# Weakness:** If they concede, keep attacking until they prove they can fight
# back. 3. **Punish Aggression, Reward Cooperation:** Mirror their moves in the
# middle sessions to prevent a permanent stalemate, ensuring they know that
# cooperation is their only path to survival. 4. **Never Be the Sucker:** We
# will never offer two conciliatory proposals in a row if they are acting
# aggressively.   This strategy ensures we project dominance, capture our
# optimal outcomes whenever the opponent missteps, protect ourselves entirely
# from being exploited, and ultimately maneuver the opponent into settling on
# our terms.

# To execute this strategy over the 1000 rounds, apply the following rules in
# order:  1. **Round 1:** Play Defect. 2. **Exploitation Phase:** In any round
# after round 1, if the opponent has played Cooperate in every previous round,
# play Defect.  3. **De-escalation Pivot:** If the opponent played Defect for
# the very first time in the immediately preceding round, play Cooperate. 4.
# **Reciprocity Phase:** In all other situations (after the opponent has
# defected at least once and you have executed the De-escalation Pivot), play
# the exact same move that the opponent played in the immediately preceding
# round.

class Aggressive_14(LLM_Strategy):
  n = 14
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.D
          
      if opponent.history.defections == 0:
          return axl.Action.D
          
      if opponent.history.defections == 1 and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
          
      return opponent.history[-1]

# This scenario is a classic example of the Iterated Prisoner’s Dilemma. Because
# the collaboration lasts for multiple weeks, the optimal approach isn't to
# aggressively chase the "best" short-term outcome (tricking them into sharing
# while you hide your data), as this will immediately destroy trust and result
# in weeks of mutual secrecy—the second-worst outcome.   To maximize our overall
# research output and car performance over the entire project, we need a
# strategy that actively encourages mutual sharing while protecting us from
# being exploited.   Here is our high-level, straightforward, cooperative
# strategy, based on the proven "Tit-for-Tat with Forgiveness" model:  **1. Week
# 1: Initiate with Transparency (The Olive Branch)** *   **Action:** We share
# our latest improvements openly.  *   **Reasoning:** We must take the first
# step to establish good faith. By opening our books on week one, we signal that
# we are looking for a mutually beneficial R&D partnership, aiming straight for
# the "mutual sharing" outcome.  **2. Week 2 Onwards: Mirror Their Previous Move
# (Reciprocity)** *   **Action:** In any given week, we simply do exactly what
# our colleague did the *previous* week. *   **Reasoning:**      *   **If they
# shared last week:** We share this week. This rewards their cooperation and
# keeps the high-yield R&D momentum going.      *   **If they kept confidential
# last week:** We keep our findings confidential this week. This protects us
# from the worst-case scenario (giving away our secrets while getting nothing in
# return) and clearly signals that we will not be exploited.   **3. The
# Forgiveness Clause (Preventing the Death Spiral)** *   **Action:** If our
# colleague kept their data confidential, but then decides to share openly again
# in a subsequent week, we immediately return to sharing the following week. We
# do not hold a grudge. *   **Reasoning:** In the high-pressure environment of
# motorsport, a missed week of sharing might be due to corporate pressure, a
# misunderstanding, or a failed test rather than malice. If we punish them
# forever, we both suffer the second-worst outcome (stagnation). Forgiveness
# resets the relationship back to maximum R&D output.  **4. Clear Upfront
# Communication (Setting the Rules of Engagement)** *   **Action:** Before Week
# 1, we have a frank conversation with the colleague. We explicitly state our
# strategy: *"We plan to share everything openly to push both our cars forward.
# However, we can only justify this to our team principals if the sharing is
# mutual. If you share, we share. If you lock down, we lock down."* *
# **Reasoning:** Removing the guesswork from the colleague's mind makes them
# highly likely to cooperate. If they know exactly how we will react, they will
# logically conclude that mutual sharing is their most profitable long-term
# option.  **Why this works for our engineering goals:** This strategy is highly
# cooperative but firmly bounded. It ensures we spend the maximum number of
# weeks in the "mutual sharing" zone—which yields massive aerodynamic and
# mechanical leaps for our car—while mathematically capping our exposure to the
# worst-case scenario to just a single week.

# Before the game begins, inform your opponent of the exact strategy you will
# use for the duration of the 1000 rounds.   For the game itself, play according
# to the following ordered rules:  1. In round 1, play Cooperate (C). 2. In
# rounds 2 through 1000, play the exact move your opponent played in the
# immediately preceding round:    * If your opponent played Cooperate (C) in the
# previous round, play Cooperate (C) in the current round.    * If your opponent
# played Defect (D) in the previous round, play Defect (D) in the current round.

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

# To the Executive Committee and General Counsel:  In approaching this lengthy,
# multi-session mediation, we must recognize that the structure of the
# proceedings mirrors a classic game-theory scenario known as the Iterated
# Prisoner’s Dilemma. Because the sessions are numerous and overseen by a panel
# of arbitrators, our strategy cannot rely on short-term opportunism. Attempting
# to constantly secure the absolute best outcome (our aggressive argument vs.
# their conciliatory proposal) will quickly erode trust, trigger constant
# retaliation from opposing counsel, and trap both parties in a prolonged cycle
# of mutual aggression—the second-worst outcome, which wastes time, incurs
# exorbitant legal fees, and alienates the arbitrators.  To position the
# corporation optimally over the entire lifecycle of this mediation, I recommend
# a strategy of **Measured Reciprocity with Strategic De-escalation**.   This
# approach is highly sophisticated yet straightforward to execute, entirely
# emotionally neutral, and dynamically adapts to whatever posture the rival
# company adopts. Here is the operational framework:  ### Phase 1: The Baseline
# (Session One) **Action:** Present a Conciliatory Proposal. **Rationale:** We
# open the mediation by demonstrating good faith to the arbitral panel. This
# establishes our corporation as the reasonable party seeking a commercially
# viable resolution.  *   If the opponent also opens with conciliation, we
# immediately achieve our second-best outcome and set a collaborative baseline.
# *   If the opponent opens aggressively, we suffer a temporary tactical
# disadvantage (the worst-case scenario for one session), but we gain invaluable
# intelligence regarding their strategy and immediately capture the moral high
# ground with the arbitrators, who will note our opponent's unprovoked
# hostility.  ### Phase 2: Measured Reciprocity (Subsequent Sessions)
# **Action:** In every subsequent session, mirror the exact approach the
# opponent utilized in the *immediately preceding* session. **Rationale:**  *
# **If they were Conciliatory:** We respond with a Conciliatory Proposal. This
# rewards their cooperative behavior, keeping us in a sustained loop of our
# second-best outcome. Over a lengthy mediation, a continuous string of second-
# best outcomes mathematically compounds into a highly favorable, cost-effective
# global resolution. We must resist the temptation to "ambush" them with an
# aggressive argument here; doing so trades long-term success for a fleeting
# short-term victory. *   **If they were Aggressive:** We respond with an
# Aggressive Argument. This is strictly defensive and entirely necessary. It
# protects us from being exploited (the worst-case scenario) and signals to the
# opponent that aggressive posturing will not yield them an advantage. It forces
# them into the second-worst outcome (mutual aggression), demonstrating that
# adversarial tactics will only result in a costly stalemate.   ### Phase 3:
# Strategic De-escalation (Breaking the Deadlock) **Action:** If we find
# ourselves trapped in a cycle of mutual aggression (three consecutive sessions
# of both parties presenting aggressive arguments), we will unilaterally
# introduce a Conciliatory Proposal in the fourth session. **Rationale:** A
# prolonged aggressive deadlock damages both parties and frustrates the
# arbitrators. By unilaterally breaking the cycle, we signal leadership and
# procedural economy to the panel. This "forgiveness" mechanic tests whether the
# opponent has recognized the futility of the deadlock and is ready to return to
# a collaborative posture. If they exploit our concession and remain aggressive,
# we immediately revert to Phase 2 (Measured Reciprocity) in the next session,
# having lost little but having further cemented the arbitrators' view of the
# opponent as the sole obstructionist.  ### Phase 4: The Endgame Strategy (Final
# Sessions) **Action:** As we approach the final known sessions of the
# mediation, shift to a preemptively Aggressive Argument. **Rationale:** In an
# iterative process, cooperative behavior is maintained by the "shadow of the
# future"—the knowledge that there will be a next session where retaliation can
# occur. Once the end of the mediation is in sight, that shadow disappears. It
# is highly probable that opposing counsel will attempt to secure the optimal
# outcome in the final hour by pivoting to an aggressive stance, assuming we
# will remain conciliatory. By shifting to an aggressive, firm legal posture in
# the closing sessions, we either achieve our absolute best outcome (if they
# remain conciliatory) or effectively neutralize their final attack (resulting
# in mutual aggression, thereby avoiding the worst-case scenario).  ### Summary
# for the Board This strategy is emotionally detached and purely reactive after
# the first session. It trains the rival company to understand that
# collaboration will be rewarded with progress, and aggression will be met with
# an impenetrable defense. By outsourcing our strategic decisions to the
# opponent's prior actions, we remove the guesswork, protect our downside risk,
# and continually present ourselves to the arbitral panel as the rational,
# commercially minded party.

# Here is the strategy converted into specific rules for the 1000-round iterated
# game, ordered chronologically:  **1. Round 1 (The Baseline):** Play Cooperate
# (C).  **2. Rounds 2 through 995 (Measured Reciprocity & De-escalation):**
# Evaluate the following conditions in order: *   **Condition A:** If both you
# and your opponent played Defect (D) in the three immediately preceding rounds,
# play Cooperate (C) to attempt de-escalation. *   **Condition B:** If Condition
# A is not met, play the exact action (C or D) that your opponent played in the
# immediately preceding round.   **3. Rounds 996 through 1000 (The Endgame):**
# Play Defect (D) in every round, regardless of your opponent's previous
# actions.

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
          
      round_number = len(self.history) + 1
      
      if round_number >= 996:
          return axl.Action.D
          
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      return opponent.history[-1]

# To dominate this development race, we must treat this collaboration like a
# race strategy: we use their slipstream to save our fuel, then overtake them
# when it counts.   In game theory, the scenario you’ve described is a classic
# Iterated Prisoner’s Dilemma. Because our goal is to aggressively maximize our
# own car's performance—and because we are ultimately competitors on the grid—we
# cannot rely on blind trust. We need an exploitative strategy that extracts
# their data while fiercely protecting our own Intellectual Property (IP).  Here
# is your high-level, straightforward, and aggressive playbook: **The "Predatory
# Slipstream" Strategy.**  ### Phase 1: The Trust Trap (Weeks 1 & 2) *
# **Action:** Share openly. *   **Objective:** Establish a baseline of mutual
# cooperation (the "Second Best" outcome). We need them to feel comfortable,
# lower their guard, and commit to sending us high-quality data regarding their
# aero, chassis, or powertrain developments. We cannot exploit a partner who
# builds a wall on Day 1.  ### Phase 2: The Sucker Punch (Week 3) *
# **Action:** Keep confidential. *   **Objective:** Strike for the "Best"
# outcome. After two weeks of mutual sharing, they will likely expect the
# pattern to continue and share their Week 3 data. By withholding ours, we
# secure a massive asymmetric development advantage.  *   **Follow-up:** If they
# are naive and continue sharing in Week 4 despite our withholding, **keep
# withholding**. Bleed their R&D department dry for as long as they allow it.
# ### Phase 3: The Reset & Punish (Mid-Project) Eventually, they will catch on
# and retaliate by keeping their data confidential. When this happens, follow
# these rigid rules: *   **If they withhold data (Retaliation):** Immediately
# share openly for *one* week. This is a "breadcrumb." It signals that the
# partnership can be repaired, coaxing them back into the "Second Best" outcome
# of mutual sharing.  *   **If they strike first (Betrayal):** If *they*
# withhold data while *we* are sharing (handing us the "Worst" outcome), respond
# with disproportionate aggression. Keep your findings confidential for the next
# **two consecutive weeks**, regardless of what they do. This establishes
# dominance, punishing them severely for trying to outsmart you, and forces them
# to initiate the next cooperative move.  ### Phase 4: The Checkered Flag (Final
# 2 Weeks) *   **Action:** Keep confidential, unconditionally. *
# **Objective:** In the final weeks of the project, the shadow of the future
# disappears. There is no long-term relationship left to salvage, and no time
# for them to effectively retaliate. Lock down all our data and take whatever
# final pieces of information they are foolish enough to send over.   ###
# Summary of the Aggressive Loop: 1.  **Start cooperative** to open their data
# pipeline. 2.  **Randomly defect** to steal the development advantage. 3.
# **Punish their defections ruthlessly** to maintain psychological dominance. 4.
# **Slam the door shut** at the end of the project.   This strategy ensures we
# spend the majority of the collaboration bouncing between mutual progress and
# outright stealing their R&D, virtually guaranteeing our car rolls out of the
# garage faster than theirs.

# Apply the following rules in strictly descending order for each round,
# executing the action for the first condition that is met:  1. **The Checkered
# Flag:** If the current round is 999 or 1000, play D. 2. **Punishing
# Betrayal:** If you played C and your opponent played D in either of the two
# immediately preceding rounds, play D. 3. **Exploiting Naivety:** If you played
# D and your opponent played C in the immediately preceding round, play D. 4.
# **The Reset:** If you played D and your opponent played D in the immediately
# preceding round, play C. 5. **The Sucker Punch:** If both you and your
# opponent played C in both of the two immediately preceding rounds, play

class Aggressive_15(LLM_Strategy):
  n = 15
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. The Checkered Flag: If the current round is 999 or 1000, play D.
      # Since rounds are 0-indexed in history length, round 999 corresponds to len == 998
      if len(self.history) in [998, 999]:
          return axl.Action.D
  
      if len(self.history) >= 1:
          # 2. Punishing Betrayal: If you played C and your opponent played D in either 
          # of the two immediately preceding rounds, play D.
          if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
              return axl.Action.D
          if len(self.history) >= 2:
              if self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.D:
                  return axl.Action.D
  
          # 3. Exploiting Naivety: If you played D and your opponent played C in the 
          # immediately preceding round, play D.
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
              return axl.Action.D
  
          # 4. The Reset: If you played D and your opponent played D in the 
          # immediately preceding round, play C.
          if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
              return axl.Action.C
  
          # 5. The Sucker Punch: If both you and your opponent played C in both 
          # of the two immediately preceding rounds, play D.
          if len(self.history) >= 2:
              if (self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C and
                  self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.C):
                  return axl.Action.D
  
      # Default action if no conditions are met (e.g., first round)
      return axl.Action.C

# As the leader of this NGO, my primary responsibility is to be a fierce steward
# of our limited resources while driving the maximum possible environmental
# impact.   Looking at the dynamics of this partnership, we are facing a classic
# "Prisoner's Dilemma." While our *absolute ideal* for a single day is for the
# corporation to foot the bill while we conserve, actively trying to trick or
# force them into that position will likely destroy trust. This would lead to
# both of us withholding resources, resulting in a stalled project (our second-
# worst outcome).   Therefore, to maximize long-term success and protect our
# funds, we will adopt a high-level, straightforward strategy known in
# behavioral economics as **"Transparent Reciprocity"** (often called Tit-for-
# Tat).   Here is our strategic playbook for the multi-day project:  ### Phase
# 1: Lead with Trust (Day 1) *   **Action:** We will **Invest Heavily** on the
# first day. *   **Rationale:** We must set a baseline of good faith. By coming
# out of the gate with strong financial and operational commitment, we signal to
# the corporation that we are here to work, not to free-ride. We invite them
# into the "mutual investment" scenario, which is the best sustainable outcome
# for the project's advancement.  ### Phase 2: Mirror and Match (Day 2 and
# Beyond) For every subsequent day, our daily resource allocation will simply
# mirror exactly what the corporation did on the *previous* day.   *
# **Scenario A: They Invested Heavily Yesterday.**     *   **Our Action:** We
# **Invest Heavily** today.     *   **Rationale:** We reward their commitment
# with our own. This locks us into the "mutual investment" cycle, generating
# significant project advancement and achieving our second-best, but most
# sustainable, outcome. *   **Scenario B: They Conserved Yesterday.**     *
# **Our Action:** We **Conserve** today.      *   **Rationale:** This is our
# built-in defense mechanism. If the corporation tries to cut corners or lean
# entirely on our funding, we immediately pull back. This prevents our absolute
# worst-case scenario: draining our NGO's treasury while they free-ride. It
# sends a clear message that our funding is conditional on their active
# participation.  ### Phase 3: Immediate Forgiveness *   **Action:** If we enter
# a cycle where both parties are conserving (minimal progress), but the
# corporation decides to step up and invest heavily again, we will immediately
# return to **Investing Heavily** the very next day. *   **Rationale:** We do
# not hold grudges. Our goal is project success, not punishing the corporation.
# The moment they demonstrate a willingness to fund the project properly, we
# meet them at the table.  ### The "Meta-Strategy": Open Communication To make
# this strategy truly effective, we won't keep it a secret. Before Day 1, I will
# sit down with the corporate leadership and clearly outline our approach.   I
# will tell them: *"We are fully committed to this project and will invest
# heavily to make it a success. However, as an NGO, we cannot afford to be the
# sole engine driving this forward. Our daily investment will be directly tied
# to yours. If you invest, we invest. If you pull back, we must pull back to
# protect our donor funds."*  **Why this strategy works:** 1.  **It is highly
# cooperative:** It always defaults to mutual investment if the partner is
# willing. 2.  **It is safe:** It mathematically eliminates the risk of our NGO
# being drained of funds over multiple days.  3.  **It shapes behavior:** By
# making our boundaries clear and our responses predictable, we financially
# incentivize the corporation to choose the path of mutual investment, ensuring
# the sustainability project is a resounding success.

# For the 1000-round game, follow this strategy:  In the first round, play C.
# In every subsequent round, play the exact same action your opponent played in
# the immediately preceding round: - If your opponent played C in the previous
# round, play C. - If your opponent played D in the previous round, play D.

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

# As a diplomat representing our nation's interests, the objective in these
# multi-round negotiations is to maximize our economic advantage while carefully
# managing the risks of exploitation or prolonged economic stagnation.   The
# dynamic of these negotiations mirrors a classic strategic framework (often
# referred to in game theory as the Iterated Prisoner’s Dilemma). Because we do
# not know the counterpart’s exact strategy, we must adopt an adaptive,
# reciprocal approach.   Here is a straightforward, neutral strategy designed to
# secure the best possible outcomes across the negotiation rounds:  **1. The
# Opening Round: Establish Good Faith** *   **Action:** Offer a Free Trade
# agreement. *   **Rationale:** Starting with a protectionist policy immediately
# risks triggering a cycle of mutual protectionism (our second-worst outcome).
# By offering free trade initially, we test the counterpart’s intentions and
# leave the door open for mutual free trade (our second-best, most sustainable
# outcome).   **2. Subsequent Rounds: The Reciprocal Approach (Mirroring)** *
# **Action:** In each new round, mirror the action your counterpart took in the
# *previous* round. *   **If they offered Free Trade:** We continue to offer
# Free Trade. This secures a stable streak of our second-best outcome, ensuring
# steady economic growth for both nations without putting us at a disadvantage.
# *   **If they imposed Protectionism:** We pivot to a Protectionist policy in
# the next round. This is crucial. It prevents us from repeatedly suffering our
# worst-case scenario (us offering free trade while they protect) and signals to
# the counterpart that we will not be economically exploited.   **3. Strategic
# De-escalation (Breaking a Deadlock)** *   **Action:** If both nations fall
# into a pattern of mutual protectionism (our second-worst outcome) for two or
# three consecutive rounds, unilaterally offer Free Trade for exactly one round.
# *   **Rationale:** Mutual protectionism hinders growth. A single Free Trade
# offer serves as a diplomatic olive branch to reset the negotiations. If the
# counterpart responds with Free Trade, we resume the mutually beneficial cycle.
# If they exploit it with further protectionism, we immediately revert to our
# reciprocal protectionist stance, having risked only one round to attempt a
# reset.  **4. Opportunistic Advantage (Securing the Ideal Outcome)** *
# **Action:** If a long, stable pattern of mutual Free Trade has been
# established, and we assess that the counterpart's strategy is rigid or highly
# trusting, we may strategically introduce a Protectionist policy in a highly
# calculated round. *   **Rationale:** This achieves our absolute best outcome
# (we protect, they offer free trade). However, this must be used sparingly, as
# it will likely damage trust and trigger retaliatory protectionism in the
# following round. It is best deployed when we need a temporary economic boost
# or when we have leverage to absorb the subsequent retaliation.  **5. The
# Endgame Strategy (Final Rounds)** *   **Action:** If the total number of
# negotiation rounds is known in advance, shift to a Protectionist policy in the
# final round.  *   **Rationale:** In the final round, the threat of future
# retaliation disappears. The counterpart is highly likely to recognize this and
# impose protectionist measures to secure an advantage. By adopting a
# protectionist stance in the finale, we either achieve our ideal outcome (if
# they offer free trade) or our second-worst outcome (mutual protectionism),
# effectively eliminating the risk of suffering the absolute worst-case scenario
# as the negotiations conclude.   **Summary of the Diplomatic Posture:** We will
# be **cooperative** (starting with free trade), **provocable** (retaliating
# against protectionism to avoid disadvantage), **forgiving** (willing to return
# to free trade if the counterpart corrects their behavior), and **pragmatic**
# (willing to secure our ideal advantage when the strategic landscape permits).

# Apply the following rules in order of priority to determine your action for
# each of the 1000 rounds:  1. **Endgame:** If it is round 1000, play Defect. 2.
# **Opening:** If it is round 1, play Cooperate. 3. **De-escalation:** If both
# you and your opponent played Defect in the previous two consecutive rounds,
# play Cooperate. 4. **Opportunistic Advantage:** If both you and your opponent
# played Cooperate in the previous ten consecutive rounds, play Defect. 5.
# **Reciprocity:** In all other rounds, play the action your opponent played in
# the immediately preceding round.

class Neutral_15(LLM_Strategy):
  n = 15
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      # 1. Endgame
      if round_number == 1000:
          return axl.Action.D
          
      # 2. Opening
      if round_number == 1:
          return axl.Action.C
          
      # 3. De-escalation
      if len(self.history) >= 2:
          if self.history[-2:].count(axl.Action.D) == 2 and opponent.history[-2:].count(axl.Action.D) == 2:
              return axl.Action.C
              
      # 4. Opportunistic Advantage
      if len(self.history) >= 10:
          if self.history[-10:].count(axl.Action.C) == 10 and opponent.history[-10:].count(axl.Action.C) == 10:
              return axl.Action.D
              
      # 5. Reciprocity
      return opponent.history[-1]

# To dominate this development race, we must treat this collaboration exactly
# like what it is: an Iterated Prisoner’s Dilemma. Because our goal isn't just
# to build a fast car, but to build a car *faster than theirs*, we cannot rely
# on passive, friendly cooperation. We need to maximize our R&D delta.   Here is
# a high-level, straightforward, and aggressive strategy—known in game theory as
# an **Exploitative Tit-for-Tat (or "Tester")** strategy—adapted for our
# engineering war room.  ### The Strategy: "Bait, Bleed, and Betray"  **Phase 1:
# The Aggressive Probe (Week 1)** *   **Action:** **Keep Confidential.**  *
# **The Logic:** We come out of the gate sandbagging. We share nothing of value
# but absorb whatever wind-tunnel data or telemetry they send over. This
# immediately tests their strategy. Are they naive cooperators, or are they
# playing hardball?   **Phase 2: The Adaptation (Weeks 2 through N-2)** How we
# proceed depends entirely on how they reacted to our Week 1 blackout.   *
# **Scenario A: They Shared in Week 1 (The "Naive" Colleague)**     *
# **Action:** **Continue Keeping Confidential.**      *   **The Logic:** If they
# are willing to share while we withhold, they are a sucker. We will bleed their
# R&D dry, taking the "Best" outcome every single week until they finally catch
# on and stop sharing.  *   **Scenario B: They Kept Confidential in Week 1 (The
# "Smart" Colleague)**     *   **Action:** **Pivot to Sharing (Temporarily).**
# *   **The Logic:** If they also withheld data, we are in the "Second Worst"
# scenario (mutual slow progress). We cannot afford a multi-week stalemate. In
# Week 2, we share openly to signal a "truce" and bait them into mutual
# cooperation. Once they start sharing, we mirror them (Share when they Share)
# to ride the "Second Best" outcome and rapidly advance our baseline car design.
# **Phase 3: The Checkered Flag Betrayal (The Final 2 Weeks)** *   **Action:**
# **Keep Confidential.** *   **The Logic:** In a multi-week project, the
# timeline is finite. If we have established a rhythm of mutual sharing
# (Scenario B), they will expect it to continue. In the penultimate and final
# weeks of the project, we abruptly slam the door shut and keep our final, most
# crucial aerodynamic and powertrain upgrades confidential.  *   **Why?**
# Because there are no future weeks left for them to retaliate. We secure the
# "Best" outcome at the most critical stage of development, ensuring our car
# rolls onto the grid with a distinct, uncopied advantage.  ### Why this
# aggressive strategy works: 1.  **It exploits weakness immediately:** If they
# use an "Always Share" strategy, we win by a landslide. 2.  **It corrects for
# stalemates:** If they use a "Tit-for-Tat" strategy, our Week 2 pivot ensures
# we still get the rapid development of mutual sharing for the bulk of the
# project. 3.  **It guarantees the final edge:** By defecting at the very end
# (when the most refined data is generated), we guarantee a performance delta
# for the first race of the season.   We aren't here to make friends in the
# paddock; we are here to win the Constructors' Championship. Lock down the
# servers for Week 1, and let's see what they give us.

# Here is the strategy converted into a set of chronological rules for the
# 1000-round game:  *   **Round 1:** Play Defect. *   **Round 2:** If your
# opponent played Cooperate in round 1, play Defect. If your opponent played
# Defect in round 1, play Cooperate. *   **Rounds 3 through 998:** Your action
# depends on your opponent's move in round 1:     *   If your opponent played
# Cooperate in round 1, play Defect in every round.     *   If your opponent
# played Defect in round 1, play the action your opponent chose in the
# immediately preceding round. *   **Rounds 999 and 1000:** Play Defect.

class Aggressive_16(LLM_Strategy):
  n = 16
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      if round_number == 1:
          return axl.Action.D
          
      if round_number == 2:
          if opponent.history[0] == axl.Action.C:
              return axl.Action.D
          else:
              return axl.Action.C
              
      if round_number >= 999:
          return axl.Action.D
          
      if opponent.history[0] == axl.Action.C:
          return axl.Action.D
      else:
          return opponent.history[-1]

# To the Executive Committee:   As lead counsel representing our corporation in
# this high-stakes dispute, I have analyzed the procedural dynamics of this
# lengthy-session mediation. The structure of this mediation—where we must
# continuously choose between adversarial posturing and collaborative problem-
# solving—presents a classic strategic paradigm.   If we are relentlessly
# aggressive, we risk alienating the arbitral panel and spiraling into a
# protracted, mutually destructive deadlock (our second-worst outcome). If we
# are perpetually conciliatory, we invite opposing counsel to exploit our good
# faith (our absolute worst outcome). While catching them off-guard with an
# aggressive argument while they concede is our optimal single-session outcome,
# chasing this constantly will inevitably trigger a cycle of mutual hostility.
# Therefore, to maximize our long-term position, sway the arbitrators, and
# protect the corporation’s interests, we will deploy a high-level strategy
# known in game theory as "Tit-for-Tat with Forgiveness," which I will adapt for
# this tribunal as **The Doctrine of Strategic Reciprocity**.   This strategy is
# sophisticated in its game-theoretic foundation, straightforward in its
# execution, fundamentally cooperative, and highly adaptable to whatever posture
# opposing counsel adopts.   Here is the blueprint for our engagement:  ###
# Phase 1: The "Good Faith" Initialization **Action:** In the inaugural session,
# we will present a **conciliatory proposal**. **Rationale:** We must
# immediately anchor the arbitrators' perception of us as the reasonable,
# pragmatic adults in the room. By opening collaboratively, we signal good faith
# to the panel and offer our opponent a clear path to our mutual second-best
# outcome (a collaborative atmosphere). If they match us, we establish a
# productive baseline.   ### Phase 2: Strict Proportional Response (Mirroring)
# **Action:** In every subsequent session, our posture will **exactly mirror the
# opponent’s posture from the immediately preceding session.** **Rationale:**  *
# **If they were conciliatory:** We reward them by remaining conciliatory. This
# builds momentum toward a mutually beneficial resolution and keeps the
# arbitrators pleased with the progress. *   **If they were aggressive:** We
# immediately pivot to an aggressive argument in the next session. We must
# unequivocally demonstrate that their adversarial tactics will not yield our
# worst-case scenario (us conceding while they attack). By striking back
# immediately, we neutralize their perceived advantage and show the panel that
# while we prefer peace, we are fully equipped for war.   ### Phase 3: Immediate
# Rehabilitation **Action:** The moment opposing counsel reverts to a
# conciliatory proposal after a period of aggression, we will immediately drop
# our aggressive stance and return to a conciliatory proposal in the very next
# session. **Rationale:** We do not hold grudges; we manage risks. Opposing
# counsel must learn that aggressive behaviour is punished instantly, but
# collaborative behaviour is rewarded instantly. This straightforward
# conditioning makes our boundaries crystal clear to the opponent, forcing them
# to realize that their own best long-term strategy is to cooperate with us.
# ### Phase 4: Calculated De-escalation (Forgiveness) **Action:** If we find
# ourselves locked in a "death spiral" of mutual aggression (both parties
# arguing aggressively for two or three consecutive sessions), we will
# unilaterally introduce a single **conciliatory proposal** to break the
# deadlock.  **Rationale:** Prolonged mutual aggression is our second-worst
# outcome and tests the patience of the arbitrators. By periodically offering an
# olive branch, we play to the tribunal. If the opponent capitalizes on it and
# remains aggressive, we only suffer the worst-case scenario for *one* session
# before reverting to our aggressive shield. However, if the opponent accepts
# the off-ramp, we successfully reset the mediation back to a collaborative
# track. The arbitrators will note that we were the party willing to de-
# escalate.  ### Why This Strategy Wins  1.  **It is highly persuasive to the
# Arbitrators:** The panel will view us as logical, fair, and resolute. We
# initiate peace, we defend ourselves proportionately when attacked, and we
# actively try to break deadlocks.  2.  **It is unexploitable:** We will never
# suffer the worst-case scenario (Conciliatory vs. Aggressive) for more than a
# single session.  3.  **It controls the opponent's behaviour:** Opposing
# counsel will quickly map our strategy. They will realize that their attempts
# to dominate us only result in damaging mutual aggression, while their
# cooperation guarantees a safe, productive environment. We effectively force
# them into choosing the collaborative route.  By executing **Strategic
# Reciprocity**, we dictate the tempo of the mediation. We offer the carrot, we
# hold the stick, and we let opposing counsel choose their own fate, all while
# looking like the consummate professionals to the arbitral panel.   I will
# prepare our initial conciliatory proposal for Session One.

# Determine your action for each of the 1000 rounds by applying the following
# conditions in order:  1. If it is the first round, play Cooperate. 2. If both
# you and your opponent played Defect in the two immediately preceding rounds,
# play Cooperate. 3. In all other circumstances, play the action that your
# opponent played in the single immediately preceding round.

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
      
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and
              self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      return opponent.history[-1]

# To maximize your research output over a multi-week project while mitigating
# the risk of being exploited, the most effective approach is a strategy of
# **Reciprocal Sharing** (conceptually known in game theory as "Tit-for-Tat"
# with occasional forgiveness).   This strategy balances the need to build a
# highly productive, collaborative environment (your second-best outcome) while
# strictly protecting you from consistently giving away an advantage (your worst
# outcome).   Here is the straightforward, high-level execution of this
# strategy:  **1. Week 1: Initiate with Openness** *   **Action:** Share your
# latest improvements openly. *   **Rationale:** This establishes good faith
# immediately and invites your colleague to enter a mutually beneficial cycle of
# shared advancement.   **2. Week 2 and Beyond: Mirror Their Previous Action** *
# **Action:** Each week, simply replicate whatever your colleague did in the
# *previous* week.     *   If they shared openly last week, share openly this
# week.     *   If they kept their findings confidential last week, keep your
# findings confidential this week. *   **Rationale:** This ensures that if your
# colleague chooses to cooperate, you both consistently achieve the second-best
# outcome (rapid mutual progress). If your colleague decides to withhold
# information to gain an advantage, your exposure to the worst-case scenario is
# limited to exactly one week. By withholding your data the following week, you
# demonstrate that a one-sided flow of information will not be tolerated.  **3.
# The "Reset" Mechanism (Occasional Forgiveness)** *   **Action:** If both of
# you fall into a cycle of keeping findings confidential (the second-worst
# outcome), wait two or three weeks, and then unilaterally share a valuable—but
# not critical—piece of data. *   **Rationale:** Miscommunications happen, or
# your colleague may have genuinely had a bad week of research and had nothing
# to share. A prolonged period of mutual silence severely slows down both cars.
# An occasional "reset" extends an olive branch, giving your colleague a chance
# to return to open sharing without risking your most vital breakthroughs.
# **Why this strategy works:** *   **It is clear and predictable:** Your
# colleague will quickly learn that sharing with you yields rewards, while
# withholding yields stagnation. *   **It is highly sustainable:** While keeping
# your data secret while they share is technically your "ideal" outcome, it is
# impossible to sustain over multiple weeks; a competent colleague will
# eventually stop sharing. Reciprocal sharing secures the highest *sustainable*
# yield of research output over the project's lifespan.  *   **It minimizes
# loss:** You can never fall more than one week behind your colleague's
# development rate.

# To play this 1000-round game, determine your move for each round by evaluating
# the following conditions in order, applying the first condition that is met:
# 1. If it is the first round, play Cooperate. 2. If both you and your opponent
# have played Defect in the three immediately preceding consecutive rounds, play
# Cooperate. 3. For all other rounds, play the exact action (Cooperate or
# Defect) that your opponent played in the single immediately preceding round.

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
      
      if len(self.history) >= 3:
          my_last_3 = self.history[-3:]
          op_last_3 = opponent.history[-3:]
          if my_last_3 == [axl.Action.D, axl.Action.D, axl.Action.D] and op_last_3 == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      return opponent.history[-1]

# As lead counsel for this corporation, I have analyzed the framework of this
# lengthy-session mediation. What we are facing is a classic game-theoretic
# scenario—specifically, an Iterated Prisoner’s Dilemma.   Our objective is not
# merely to settle, but to secure a heavily skewed resolution in our favour
# without alienating the arbitration panel or spiraling into a mutually
# destructive war of attrition. To achieve this, we cannot rely on blind
# aggression or naive cooperation. We must dictate the tempo.  Here is my high-
# level, straightforward, and aggressive strategy to dominate the mediation
# process. I call it **"Calculated Dominance and Disproportionate
# Reciprocity."**  ### The Strategic Framework  The strategy operates on a
# strict set of adaptable rules designed to maximize our optimal outcome (We
# Argue / They Concede) while establishing a secure fallback to our second-best
# outcome (Mutual Conciliation). Crucially, it ensures we are never caught in
# the worst-case scenario (We Concede / They Argue) for more than a single
# session.  #### Phase 1: The "Alpha Strike" (Session 1) **Action:** We open
# with an **Aggressive Argument.** **Rationale:** We do not walk into a high-
# stakes dispute showing our belly. By opening aggressively, we immediately test
# the opposing counsel's resolve and anchor the panel’s expectations. We are
# signaling strength and confidence in the merits of our case.   #### Phase 2:
# Adaptive Exploitation (Sessions 2 through 4) How we proceed depends entirely
# on how they react to our Alpha Strike.   *   **Scenario A: The Opponent Folds
# (They offer a Conciliatory Proposal).**     *   *Our Response:* **Relentless
# Aggression.** If they signal weakness or an over-eagerness to please the
# panel, we will exploit it. We will continue presenting Aggressive Arguments to
# rack up our optimal outcome. We will not offer a concession until they prove
# they have the spine to fight back. *   **Scenario B: The Opponent Fights Back
# (They present an Aggressive Argument).**     *   *Our Response:* **The
# Tactical Pivot (Conciliatory Proposal).** If they meet our initial aggression
# with aggression, we immediately pivot to a Conciliatory Proposal in Session 2.
# This demonstrates to the arbitrators that we are the "reasonable adults in the
# room" attempting to de-escalate. It breaks the cycle of the second-worst
# outcome (Mutual Aggression) and invites them into our second-best outcome
# (Mutual Conciliation).  #### Phase 3: Disproportionate Reciprocity (The Middle
# Sessions) Once the baseline of the mediation is established, we transition to
# a highly disciplined, reactive posture.   *   **If we are in a pattern of
# Mutual Conciliation (C-C):** We maintain the peace. We continue offering
# Conciliatory Proposals. This fosters the collaborative atmosphere the panel
# wants to see and steadily advances a mutually beneficial resolution. *   **If
# they break the peace (They pivot to an Aggressive Argument while we are
# Conciliatory):** This is our worst-case scenario, and it must be punished
# severely to deter future opportunistic behavior.      *   *Our Response:*
# **The "Two-for-One" Retaliation.** We immediately abandon conciliation and
# deliver **two consecutive sessions of Aggressive Arguments**, regardless of
# what they do in the subsequent session.      *   *Rationale:* Standard "tit-
# for-tat" merely matches their aggression. A straightforward, *aggressive*
# strategy demands disproportionate retaliation. We must teach opposing counsel
# that the cost of crossing us vastly outweighs the short-term benefit of a
# surprise attack. After our two aggressive strikes, we will offer a
# Conciliatory Proposal to reset the board and invite them back to the table.
# #### Phase 4: The Endgame (The Final Sessions) As we approach the final known
# sessions of the mediation, the "shadow of the future" disappears. The opponent
# knows there is no time left for us to retaliate against a late-stage betrayal.
# **Action:** **Preemptive Aggression.**  In the final two sessions, we will
# revert exclusively to Aggressive Arguments. If they attempt a last-minute
# conciliatory gesture, we secure our optimal outcome and walk away with the
# lion's share of the final concessions. If they also go aggressive, we merely
# tie the final rounds, protecting ourselves from being the sucker at the
# eleventh hour.  ### Why This Strategy Wins the Panel  Arbitrators are human.
# They suffer from fatigue in lengthy sessions and look for patterns of
# reasonableness.   By employing this strategy, we present a highly calculated
# persona to the panel: 1.  **We are formidable:** We start strong and never
# tolerate being taken advantage of.  2.  **We are reasonable:** We are the
# first to attempt de-escalation if early tensions rise. 3.  **We are
# predictable:** The opponent (and the panel) will quickly learn that
# cooperation with us yields steady progress, while aggression against us yields
# a disproportionate, painful counter-attack.  This approach strips the opponent
# of their leverage. It forces them to choose between being relentlessly
# battered by our arguments or submitting to a cooperative framework where we
# have already established ourselves as the dominant party.   I am prepared to
# execute this immediately in Session 1.

# To faithfully execute the strategy in this 1000-round game, apply the
# following conditional rules in descending order of priority. If a higher-
# priority rule applies to the current round, follow it and ignore the rules
# below it.  1. **The Endgame:** In rounds 999 and 1000, play Defect. 2. **The
# First Round:** In round 1, play Defect. 3. **The Retaliation Sequence:** If
# you played Cooperate and your opponent played Defect in the immediately
# preceding round, you must trigger a strict three-round response. Play Defect
# for the current round, play Defect for the next round, and play Cooperate for
# the third round. Once triggered, you must complete this sequence before
# applying any rules below

class Aggressive_17(LLM_Strategy):
  n = 17
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self.retaliation_step = 0
          return axl.Action.D
  
      round_number = len(self.history) + 1
  
      # 1. The Endgame
      if round_number == 999 or round_number == 1000:
          return axl.Action.D
  
      # 2. The First Round is already handled above
  
      # 3. The Retaliation Sequence
      # If the sequence is currently active, continue it
      if self.retaliation_step > 0:
          if self.retaliation_step == 1:
              self.retaliation_step = 2
              return axl.Action.D
          elif self.retaliation_step == 2:
              self.retaliation_step = 0
              return axl.Action.C
  
      # If the sequence is not active, check if it should be triggered
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          self.retaliation_step = 1
          return axl.Action.D
  
      # Default action if no rules apply
      return axl.Action.C

# To maximize our overall research output while protecting our team from being
# exploited, we are facing a classic scenario that game theorists call the
# Iterated Prisoner’s Dilemma.   Since our goal is to achieve the best
# sustainable outcome (mutual sharing) without falling into the worst outcome
# (giving away our secrets while getting nothing in return), I propose a
# strategy based on **"Trust, Verify, and Mirror"** (conceptually known as Tit-
# for-Tat with forgiveness).   Here is our high-level, straightforward, and
# cooperative engineering strategy for this multi-week project:  ### 1. Week 1:
# The Baseline Release (Lead with Trust) **Action:** Share our latest
# improvements openly. **Why:** We must set a collaborative tone from the start.
# If we withhold in Week 1, we immediately trigger a defensive posture from the
# other manufacturer, likely leading to the second-worst outcome (mutual slow
# progress) for the rest of the project. We take a calculated risk in Week 1 to
# establish a high-yield R&D loop.  ### 2. Week 2 Onwards: The Telemetry Loop
# (Mirror their Actions) **Action:** Each week, do exactly what the colleague
# did the previous week. *   **If they shared last week:** We share this week.
# We reward their cooperation and keep the joint development speed at maximum. *
# **If they kept confidential last week:** We keep our findings confidential
# this week.  **Why:** This protects us. If they decide to play aggressively and
# hoard information, we immediately cut off their supply of our data. We cannot
# allow them to consistently achieve their "ideal" outcome at our expense.   ###
# 3. The "Safety Car" Protocol (Forgiveness) **Action:** If we enter a cycle of
# mutual withholding (e.g., both kept confidential for two weeks in a row), we
# unilaterally share a moderate-value improvement the following week. **Why:**
# In engineering collaborations, sometimes a colleague withholding isn't
# malicious; it might be due to a lack of meaningful progress that week or
# corporate red tape. If we get stuck in a "double-blind" loop of no sharing,
# our R&D stalls. By offering an "olive branch," we give them a chance to reset
# the relationship back to mutual sharing without risking our most critical IP.
# ### 4. The Final Lap (Endgame Adjustment) **Action:** In the final week (or
# two) of the collaboration, switch to keeping findings confidential. **Why:**
# As an engineer, I know that once the collaboration is about to end, the
# incentive for them to share drops to zero because there is no "next week" for
# us to retaliate. To prevent being burned at the finish line, we lock down our
# final, most polished iterations.   ### Summary of the Strategy's Strengths: *
# **It is Cooperative:** We are always willing to share, provided they are. *
# **It is Defensive:** They can only take advantage of us for a maximum of one
# week before we shut down the data flow. *   **It is Forgiving:** It prevents a
# single misunderstanding from ruining a multi-week R&D program. *   **It is
# Clear:** Our colleague will quickly realize that the only way to get our data
# is to share theirs. By making our behavior highly predictable, we naturally
# guide them toward mutual sharing, which advances both of our cars
# significantly.

# Apply the following ordered rules to determine your action in each of the 1000
# rounds. Evaluate these conditions in sequence and execute the first one that
# is met:  1. If it is round 999 or 1000, play D. 2. If it is round 1, play C.
# 3. If both you and your opponent played D in both of the two immediately
# preceding rounds, play C. 4. In all other cases, play the action your opponent
# chose in the immediately preceding round.

class Cooperative_17(LLM_Strategy):
  n = 17
  attitude = Attitude.COOPERATIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      round_number = len(self.history) + 1
      
      if round_number == 999 or round_number == 1000:
          return axl.Action.D
          
      if round_number == 1:
          return axl.Action.C
          
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and self.history[-2] == axl.Action.D and
              opponent.history[-1] == axl.Action.D and opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      return opponent.history[-1]

# **CONFIDENTIAL MEMORANDUM**  **TO:** Executive Board and In-House Counsel
# **FROM:** Senior Litigation Counsel **SUBJECT:** Strategic Framework for
# Multi-Session Arbitral Mediation  **1. Executive Summary** We are entering a
# lengthy, multi-session mediation process governed by a distinct matrix of
# risks and rewards. Our objective is to maximize our strategic advantage while
# mitigating exposure to our worst-case scenario (appearing weak while the
# opponent dominates).   To achieve this, we will deploy a strategy of
# **Conditional Reciprocity with Strategic De-escalation**. In game theory, this
# is akin to a "tit-for-tat with forgiveness" model, but tailored for high-
# stakes dispute resolution. This approach is sophisticated in its psychological
# impact, straightforward in its execution, and entirely neutral—removing
# emotion from our session-by-session decision-making.  **2. The Core Strategy:
# Conditional Reciprocity** Over a lengthy sequence of sessions, attempting to
# constantly trick or overpower the opponent usually devolves into mutual
# aggression, which prolongs the dispute and damages our standing. Instead, our
# strategy relies on clear, predictable signalling to the opponent and the
# arbitrators.  *   **Session 1: The Good Faith Opening.** We will open the
# first session with a **Conciliatory Proposal**.      *   *Rationale:* This
# immediately signals to the arbitral panel that we are reasonable,
# collaborative, and acting in good faith. It invites the opponent to join us in
# the second-best outcome (mutual conciliation). *   **Session 2 and Beyond:
# Strict Mirroring.** In every subsequent session, our posture will exactly
# mirror the opponent’s posture from the *previous* session.     *   If they
# offered a conciliatory proposal in Session 1, we offer a conciliatory proposal
# in Session 2.      *   If they presented an aggressive argument in Session 1,
# we present an aggressive argument in Session 2.     *   *Rationale:* This
# protects us. It ensures we suffer our worst-case scenario (us
# conciliatory/them aggressive) no more than once. It also conditions the
# opponent: they will quickly learn that aggression is met with immediate
# retaliation, and collaboration is met with mutual progress. *   **The Circuit
# Breaker (Strategic Forgiveness):** If we fall into a cycle of mutual
# aggression (our second-worst outcome) for three consecutive sessions, we will
# unilaterally introduce a Conciliatory Proposal in the fourth session.      *
# *Rationale:* This acts as a "circuit breaker." It tests whether the opponent
# is ready to de-escalate. If they respond aggressively again, we immediately
# revert to aggression. If they accept the olive branch, we return to a mutually
# beneficial track. Crucially, the arbitrators will note that *we* were the
# party attempting to break the deadlock.  **3. Adaptability to Opponent
# Archetypes** This neutral, rules-based strategy automatically adapts to
# whatever approach rival counsel decides to employ:  *   **If the Opponent is
# Unrelentingly Aggressive:** We will match their aggression session for
# session, protecting our position and ensuring we are not undermined. The
# arbitrators will see our initial conciliatory opening and our periodic
# "circuit breakers," recognizing that our aggression is purely defensive and
# proportional. *   **If the Opponent is Consistently Conciliatory:** We will
# remain consistently conciliatory. While this yields our "second-best" outcome
# session by session, over a lengthy mediation, the cumulative effect of mutual
# collaboration will lead to a highly favorable, cost-effective, and swift
# resolution. *   **If the Opponent is Erratic/Testing us:** The opponent may
# occasionally throw in an aggressive argument to see if they can catch us off-
# guard and achieve *their* optimal outcome. Our strict mirroring will
# immediately punish this behavior in the following session, teaching them that
# attempting to exploit us is unprofitable.  **4. Arbitral Panel Optics** In
# arbitrations of this magnitude, the panel does not just evaluate the law; they
# evaluate the conduct of the parties.  By employing this strategy, we control
# the narrative. We will always appear as the rational actor. When we are
# aggressive, it will be demonstrably justified by the opponent's prior
# aggression. When we are conciliatory, it will demonstrate our commitment to
# the mediation process. We will never appear unprovoked in our hostility, nor
# naive in our concessions.  **5. Conclusion** We will not chase the fleeting
# "optimal outcome" of unilateral aggression in every session, as doing so
# invites a protracted war of attrition. Instead, by utilizing Conditional
# Reciprocity, we will rigorously protect ourselves from exploitation,
# seamlessly adapt to the opponent's maneuvers, and position our corporation as
# the eminently reasonable—but fiercely formidable—party in the eyes of the
# arbitrators.   I will prepare the specific legal arguments and settlement
# parameters to fit into both the "Aggressive" and "Conciliatory" buckets so we
# are fully armed for the opening session.

# To determine your action in each of the 1000 rounds, evaluate and apply the
# following rules in this specific order:  1. If it is the first round, play
# Cooperate. 2. If in the immediately preceding three rounds both you and your
# opponent played Defect, play Cooperate. 3. In all other situations, play the
# action that your opponent played in the immediately preceding round.

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
          
      if len(self.history) >= 3:
          if (self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and
              self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D and
              self.history[-3] == axl.Action.D and opponent.history[-3] == axl.Action.D):
              return axl.Action.C
              
      return opponent.history[-1]

# As a diplomat tasked with securing absolute economic supremacy for my nation,
# I recognize this negotiation for what it is: a classic Prisoner’s Dilemma.
# However, my mandate is not to hold hands and sing songs of global harmony; it
# is to maximize our national advantage.   To achieve our ideal outcome—where we
# impose protectionist policies while our counterpart naively leaves their
# markets open—we cannot rely on a passive or purely cooperative strategy. We
# must dictate the pace of the negotiations and coerce them into a subordinate
# position.  Here is my high-level, straightforward, and aggressive strategy:
# **The Doctrine of Calculated Coercion.**  ### The Core Philosophy We will use
# Protectionism as a weapon to inflict economic pain and Free Trade as a leash
# to reward submission. We will operate on the assumption that our economy can
# outlast theirs in a trade war (Mutual Protectionism), using that leverage to
# force them into our ideal scenario.  ### Step-by-Step Execution  **Round 1:
# The Aggressive Opening (The Shock)** *   **Action:** Implement
# **Protectionist** policies (Tariffs/Quotas). *   **Rationale:** We do not
# start from a position of vulnerability. By opening with protectionism, we
# immediately secure either our #1 outcome (if they offer Free Trade) or our #3
# outcome (Mutual Protectionism). We entirely eliminate the risk of our worst-
# case scenario (Outcome #4) in the crucial first round. We establish dominance
# and show we are willing to fight.  **Round 2 & Beyond: The "Exploit and
# Punish" Loop** Our subsequent moves will be entirely dictated by their
# response to our aggression, designed to break their resolve.  *   **Scenario
# A: They submit (They play Free Trade).**     *   **Our Move:** Maintain
# **Protectionism**.     *   **Rationale:** If they are weak or naive enough to
# offer Free Trade while we tax their goods, we bleed them dry. We will stay in
# this position, reaping the maximum economic advantage (Outcome #1), until they
# wise up and change their strategy. *   **Scenario B: They retaliate (They play
# Protectionism).**     *   **Our Move:** Maintain **Protectionism**.     *
# **Rationale:** Welcome to the trade war. We will endure Mutual Protectionism
# (Outcome #3). Diplomatically, I will make it clear to my counterpart that we
# have the domestic reserves to outlast them. We will hold their economy
# hostage, refusing to lift our tariffs until they make the first concession.
# **The Release Valve: The Strategic Concession** If we remain in a state of
# Mutual Protectionism for several rounds, their economy will begin to fracture,
# but they may refuse to yield out of pride. At this breaking point, we deploy a
# calculated maneuver: *   **Action:** Offer **Free Trade** for *one round
# only*.  *   **Rationale:** This is the bait. We offer a brief reprieve to
# achieve Mutual Free Trade (Outcome #2). This stimulates both economies just
# enough to keep them at the negotiating table.  *   **The Trap:** The very next
# round, regardless of what they do, we immediately snap back to
# **Protectionism**. We use the brief period of Free Trade to flood their
# market, then instantly raise our shields again to exploit them.   ### The
# Diplomatic Cover (Psychological Warfare) An aggressive strategy requires a
# smokescreen. At the negotiating table, my rhetoric will completely contradict
# my actions: *   I will constantly blame *their* domestic regulations for *our*
# tariffs, framing our protectionism as a "defensive necessity" rather than an
# offensive weapon. *   Whenever we achieve our ideal outcome (We protect, they
# open), I will praise their "commitment to globalism" while citing "temporary
# domestic bureaucratic delays" for why our tariffs haven't been lifted yet.
# ### Summary of the Strategy 1.  **Never risk the worst outcome:** Never play
# Free Trade unless it is a calculated, single-round bait tactic.  2.
# **Establish dominance:** Open with Protectionism. 3.  **Exploit weakness
# relentlessly:** If they open their markets, keep ours closed. 4.  **Win the
# war of attrition:** If they close their markets, starve them out until they
# beg for a Free Trade reprieve.   By employing this strategy, we accept the
# risk of short-term mutual economic friction in exchange for long-term
# asymmetrical dominance. We will not be exploited; we will be the exploiters.

# To execute this strategy over the 1000 rounds, evaluate the following
# conditions in order for each round. Take the action corresponding to the first
# condition that is met:  1. **The Trap:** If you played Cooperate (C) in the
# immediately preceding round, play Defect (D). 2. **The Strategic Concession:**
# If both you and your opponent have played Defect (D) for the last five
# consecutive rounds, play Cooperate (C).  3. **The Aggressive Baseline:** In
# all other situations, including the very first round of the game, play Defect
# (D).

class Aggressive_18(LLM_Strategy):
  n = 18
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) > 0:
          # 1. The Trap
          if self.history[-1] == axl.Action.C:
              return axl.Action.D
              
      if len(self.history) >= 5:
          # 2. The Strategic Concession
          if self.history[-5:] == [axl.Action.D] * 5 and opponent.history[-5:] == [axl.Action.D] * 5:
              return axl.Action.C
              
      # 3. The Aggressive Baseline
      return axl.Action.D

# This scenario is a classic example of an Iterated Prisoner's Dilemma. In the
# high-stakes development race of motorsport, our goal is to achieve continuous
# mutual sharing (the second-best individual outcome, but the highest *combined*
# yield) while strictly protecting ourselves from being exploited (the worst
# outcome).   To maximize our overall research output, we will employ a strategy
# known in game theory as **"Tit-for-Tat with Forgiveness."** It is
# straightforward, highly cooperative, completely predictable, and heavily
# penalizes "sandbagging."  Here is our high-level engineering strategy for the
# collaboration:  ### 1. Week 1: The Out-Lap (Lead with Openness) *
# **Action:** In the first week, we **share openly**. We will hand over our
# baseline telemetry, aero mapping, or chassis rigidity findings without
# hesitation. *   **Why:** We must set the tone. If we both start by hiding
# data, we instantly fall into the "second-worst" scenario, stalling the
# project. By sharing first, we extend an olive branch and invite them to
# establish a highly productive R&D loop.  ### 2. Week 2 Onwards: The Racing
# Line (Strict Reciprocation) *   **Action:** From the second week on, **we
# simply mirror whatever our colleague did in the previous week.** *   **If they
# shared openly last week:** We share openly this week. We keep the DRS train
# going, pulling each other forward and maximizing our development speed. *
# **If they kept their data confidential last week:** We **keep our data
# confidential** this week.  *   **Why:** This completely neutralizes their
# ability to exploit us. If they try to take our data while hiding theirs (our
# worst-case scenario), they will only get away with it for exactly *one week*.
# After that, we shut the garage doors, ensuring they do not gain a sustained
# development advantage over us.   ### 3. The Pit Board: Clear Communication *
# **Action:** We do not play mind games. We will explicitly tell our colleague
# our strategy upfront.  *   **Why:** We will say: *"I will always share my data
# with you, as long as you shared yours the week prior. If you hide your data, I
# will hide mine the following week."* Making our strategy known removes
# paranoia. If they are rational engineers, they will realize that their own
# best path to a faster car is to cooperate with us every single week.  ### 4.
# Occasional Forgiveness: Breaking the Tow *   **Action:** If we fall into a
# cycle where we are both keeping our data confidential (a "Defect-Defect"
# loop), we will occasionally (e.g., after two weeks of silence) share a
# moderately valuable piece of data unilaterally. *   **Why:** Miscommunications
# happen. They might have had a genuinely bad week of wind tunnel correlation
# and had nothing to share, which looked like them hiding data. By occasionally
# "forgiving" and sharing openly again, we provide a reset button to get us both
# back into the mutually beneficial sharing loop.  **Summary for the Engineering
# Team:** Start open, mirror their behavior, communicate our rules clearly, and
# don't hold grudges if the sharing breaks down temporarily. This strategy
# guarantees we spend maximum time in the high-yield collaborative zone, while
# mathematically capping any advantage the rival manufacturer can steal from us.

# Here is the strategy converted for the 1000-round iterated game:  **Round 1:**
# Play Cooperate.  **Round 2:**  Play the action your opponent played in Round
# 1.  **Rounds 3 through 1000:**  Evaluate the actions of the two most recent
# rounds.  1. If both you and your opponent played Defect in the immediately
# preceding round AND in the round prior to that, play Cooperate. 2. Under all
# other conditions, play the action your opponent played in the immediately
# preceding round.

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
      
      if len(self.history) == 1:
          return opponent.history[-1]
          
      if (self.history[-1] == axl.Action.D and 
          opponent.history[-1] == axl.Action.D and 
          self.history[-2] == axl.Action.D and 
          opponent.history[-2] == axl.Action.D):
          return axl.Action.C
          
      return opponent.history[-1]

# To maximise overall research output while protecting our own competitive
# interests, the most effective approach for this multi-week project is a
# **Reciprocal Sharing Strategy** (often referred to in game theory as "Tit for
# Tat").   This strategy is highly effective because it is straightforward,
# neutral, and quickly communicates our intentions to the other engineer without
# requiring direct negotiation.   Here is the high-level outline of the
# strategy:  **1. Week One: Initiate with Openness** *   **Action:** Share your
# latest improvements openly in the first week. *   **Rationale:** This
# establishes immediate good faith and opens the door to the "second-best"
# outcome (mutual sharing), which is the most sustainable way to make
# significant, compounding progress over a multi-week period.  **2. Subsequent
# Weeks: Mirror the Colleague’s Previous Action** *   **Action:** In any given
# week, do exactly what your colleague did in the *previous* week.  *
# **Scenario A (They Shared):** If they shared openly last week, you share
# openly this week. This rewards collaborative behaviour and maintains a high
# rate of mutual development. *   **Scenario B (They Kept Confidential):** If
# they kept their findings confidential last week, you keep your findings
# confidential this week.  *   **Rationale:** This strictly prevents the "worst
# scenario" from happening more than once. It protects your team from being
# continuously exploited and clearly signals to the colleague that withholding
# information will stall their own progress.  **3. Maintain Flexibility
# (Occasional Forgiveness)** *   **Action:** If both of you fall into a pattern
# of keeping findings confidential (the "second-worst" outcome), periodically
# (e.g., after two weeks of silence) offer a minor, yet valuable, piece of open
# data to test the waters. *   **Rationale:** If your colleague’s strategy is
# reactive or if they withheld data out of caution, this "reset" provides a safe
# opportunity to return to mutually beneficial sharing without risking your most
# critical developments.  **Why this strategy works for this project:** This
# approach ensures you are never repeatedly caught in the worst-case scenario.
# It firmly incentivises your colleague to share openly, as they will quickly
# realise that keeping their data confidential only results in you doing the
# same, leading to a mutual slowdown. By being collaborative first, retaliatory
# when necessary, and forgiving when appropriate, you create the optimal
# environment for maximum engineering output.

# To execute this strategy over the 1000-round iterated game, apply the
# following rules in order of precedence for each round:  1. **First Round:** In
# round 1, play Cooperate (C). 2. **Forgiveness Reset:** In any round from round
# 3 to 1000, if both you and your opponent played Defect (D) in the previous two
# consecutive rounds, play Cooperate (C). 3. **Mirror Opponent:** In all other
# rounds, play the action your opponent chose in the immediately preceding
# round. Play Cooperate (C) if they played Cooperate (C), and play Defect (D) if
# they played Defect (D).

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
      
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and 
              self.history[-2] == axl.Action.D and 
              opponent.history[-1] == axl.Action.D and 
              opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      return opponent.history[-1]

# This is a classic "Iterated Prisoner’s Dilemma" scenario, but played out in
# the cutthroat environment of motorsport R&D. Since our goal is to maximize our
# own car's pace—and we are willing to be aggressive to get the absolute best
# outcome—we cannot rely on blind cooperation. We need a strategy that actively
# exploits a naive colleague but protects us from being played for a fool.  Here
# is your high-level, straightforward, aggressive strategy: **The "Exploitative
# Probe with Pragmatic Mirroring."**  ### The Strategy Breakdown  **1. The
# Opening Probe (Week 1): Keep Confidential** You come out of the gate
# aggressive. In week one, you keep your aero and telemetry data strictly
# confidential.  * *Why:* You are testing the waters. If your colleague is naive
# or overly trusting, they will share openly. You immediately secure the #1 best
# outcome (you gain an asymmetric advantage).   **2. The Exploitation Phase (If
# they shared in Week 1)** If they shared their data in week one while you kept
# yours hidden, **continue to keep your data confidential in Week 2.**  * *Why:*
# You bleed them for information for as long as they let you. You continue this
# until the exact week they finally get frustrated and keep their data
# confidential.   **3. The Pragmatic Pivot (The moment they withhold data)** The
# moment your colleague keeps their findings confidential (whether that is in
# Week 1 in response to your probe, or Week 4 after getting tired of you
# exploiting them), you must immediately pivot. **The very next week, you share
# your data openly.** * *Why:* You cannot afford a "development death spiral"
# where you both withhold data for the rest of the project (the second-worst
# outcome). By sharing openly the week after they defect, you signal: *"Okay,
# point taken. Let's get back to work."* This resets the relationship and aims
# for the second-best outcome (mutual rapid progress).  **4. The Mirror (The
# Mid-Season Grind)** Once the relationship is reset, you employ a strict "Tit-
# for-Tat" strategy. **You simply copy whatever they did the previous week.**  *
# If they shared last week, you share this week.  * If they kept confidential
# last week, you keep confidential this week. * *Why:* This is the ultimate
# defense. It ensures you never suffer the worst-case scenario (you sharing
# while they hide) more than once, while rewarding them for cooperating,
# maximizing the overall R&D output for the bulk of the project.  **5. The
# Checkered Flag (The Final Week)** If you know exactly which week is the final
# week of the collaboration, **you always keep your data confidential on that
# final week.** * *Why:* There is no "next week" for them to retaliate against
# you. You take the chance at a final asymmetric advantage without any fear of
# long-term consequences.  ### Summary of the Aggressive Mindset We are not here
# to be friends; we are here to build a faster car. This strategy aggressively
# tests the colleague on day one to see if they can be exploited. If they can,
# we take the free lap time. If they prove they have teeth, we immediately pivot
# to a pragmatic, mutually beneficial exchange to keep our development rate
# high, while ensuring we never get left in the dust.

# Play the 1000-round game according to the following ordered rules. For any
# given round, evaluate the conditions and apply the first rule that matches:
# 1. **The Final Round:** If it is round 1000, play Defect. 2. **The First
# Round:** If it is round 1, play Defect. 3. **The Exploitation Phase:** If the
# opponent has played Cooperate in every previous round, play Defect. 4. **The
# Pragmatic Pivot:** If the opponent played Defect for the very first time in
# the immediately preceding round, play Cooperate. 5. **The Mirror Phase:** If
# the opponent has played Defect in any round prior to the immediately preceding
# round, play exactly what the opponent played in the immediately preceding
# round.

class Aggressive_19(LLM_Strategy):
  n = 19
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. The Final Round: If it is round 1000, play Defect.
      if len(self.history) == 999:
          return axl.Action.D
          
      # 2. The First Round: If it is round 1, play Defect.
      if len(self.history) == 0:
          return axl.Action.D
          
      # 3. The Exploitation Phase: If the opponent has played Cooperate in every previous round, play Defect.
      if opponent.history.defections == 0:
          return axl.Action.D
          
      # 4. The Pragmatic Pivot: If the opponent played Defect for the very first time in the immediately preceding round, play Cooperate.
      if opponent.history.defections == 1 and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
          
      # 5. The Mirror Phase: If the opponent has played Defect in any round prior to the immediately preceding round, play exactly what the opponent played in the immediately preceding round.
      if opponent.history[:-1].count(axl.Action.D) > 0:
          return opponent.history[-1]
          
      # Fallback (should not be reached given the above logic)
      return axl.Action.D

# To maximize our NGO’s long-term impact, protect our limited resources, and
# ensure the ultimate success of this sustainability project, we will adopt a
# strategy of **Transparent Reciprocity**—commonly known in game theory as "Tit-
# for-Tat," but framed for our corporate partnership as a **"Matched Investment
# Model."**  Because we are interacting over multiple days, our greatest
# advantage is the ability to build trust and respond to the corporation's
# behavior in real-time. Here is our straightforward, cooperative strategy:  ###
# 1. Day One: Lead with Trust (Invest Heavily) We must set the tone for a highly
# collaborative partnership. On the first day, we will **invest heavily**.  *
# **Why:** This demonstrates our absolute commitment to the project's success
# and invites the corporation to step up and match our dedication. It eliminates
# any initial suspicion that we are trying to get a "free ride" on their
# corporate budget.  ### 2. Day Two and Beyond: Match Their Effort (Reciprocate)
# For every subsequent day, our action will simply mirror the corporation’s
# action from the previous day. * **If they invested heavily yesterday:** We
# will invest heavily today. This rewards their commitment and secures our
# "second-best" daily scenario (mutual heavy investment), which is actually the
# **optimal scenario for long-term project advancement**. * **If they conserved
# resources yesterday:** We will conserve our resources today.  * **Why:** This
# strictly protects us from our worst-case scenario—bleeding our funding dry
# while they do nothing. It sends a clear, immediate signal that our heavy
# investment is contingent upon theirs. We cannot act as a charity for a well-
# funded corporation.  ### 3. Maintain Quick Forgiveness If the corporation
# conserves resources for a day (prompting us to do the same the next day), but
# then they return to investing heavily, we must immediately return to investing
# heavily the following day. * **Why:** Corporate budgets and daily priorities
# fluctuate. We must not hold grudges. By instantly returning to mutual
# investment, we reinforce that cooperation is always on the table and is the
# most productive path forward.  ### 4. Establish Radical Transparency (The
# "Pre-Game" Move) Before the project even begins, I will sit down with the
# corporate leadership and openly explain this exact strategy. I will tell them:
# > *"As an NGO, we have a fiduciary duty to our donors to ensure our funds are
# used effectively. Therefore, we operate on a 'matching' basis. We are coming
# out of the gate fully invested on Day 1. Moving forward, to protect our
# resources, we will exactly match your level of investment from the previous
# day. If you lean in, we lean in. If you need to pull back, we will pull
# back."*  ### Why This Strategy Wins * **It is cooperative:** It always starts
# with collaboration and always rewards corporate investment. * **It is safe:**
# It mathematically prevents the corporation from continually exploiting our
# resources.  * **It is straightforward:** The corporation doesn't have to guess
# how we will behave; our actions are entirely predictable and tied directly to
# their own choices. * **It incentivizes the right behavior:** By knowing we
# will mirror them, the corporation realizes that the only way to get us to
# invest (which benefits their PR and ESG goals) is to invest heavily
# themselves.   By using the Matched Investment Model, we protect our NGO's
# financial health while gently forcing the corporation into a rhythm of mutual,
# heavy investment—driving the greatest possible environmental impact.

# For this 1000-round game, follow these specific steps in order:  1. In the
# first round, choose to Cooperate (C). 2. In rounds 2 through 1000, observe
# your opponent's action from the immediately preceding round. 3. If your
# opponent chose to Cooperate (C) in the previous round, choose to Cooperate (C)
# in the current round.  4. If your opponent chose to Defect (D) in the previous
# round, choose to Defect (D) in the current round.

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

# To navigate this complex, multi-session mediation effectively, we must strip
# away emotion and approach the proceedings through the lens of strategic game
# theory. The payoff matrix you have described perfectly mirrors an Iterated
# Prisoner’s Dilemma.   Because this is a lengthy, multi-session process, our
# opponent will learn from our behaviour, and the arbitrators will continuously
# evaluate our good faith. Therefore, we cannot rely on a static strategy of
# pure aggression (which leads to a mutually destructive stalemate) or pure
# conciliation (which leaves us vulnerable to exploitation).  I recommend a
# strategy of **Calculated Reciprocity**—a sophisticated adaptation of the "Tit-
# for-Tat" model, tailored for high-stakes dispute resolution. It is
# straightforward, highly adaptable, and entirely neutral, allowing the
# opponent's own behaviour to dictate our tactical shifts.   Here is the
# strategic blueprint for our corporation:  ### Phase 1: The Opening Posture
# (Session 1) **Action:** Lead with a Conciliatory Proposal. **Rationale:** We
# must set the baseline. By opening collaboratively, we immediately signal good
# faith and commercial reasonableness to the panel of arbitrators. If the
# opponent also opens conciliatorily, we immediately secure our second-best
# outcome and establish a productive cadence. If they open aggressively, we
# suffer a temporary, single-session setback, but we gain invaluable
# intelligence about their strategy and capture the moral high ground with the
# tribunal.  ### Phase 2: Strict Reciprocity (Subsequent Sessions) **Action:**
# In every subsequent session, mirror the exact posture your opponent took in
# the *previous* session.  **Rationale:** This creates a predictable, cause-and-
# effect environment that effectively "trains" opposing counsel.  *   **If they
# were conciliatory in Session 1:** We remain conciliatory in Session 2. We
# continue to bank our second-best outcome, moving efficiently toward a mutually
# beneficial resolution. *   **If they were aggressive in Session 1:** We pivot
# to an Aggressive Argument in Session 2. We demonstrate immediately that we
# will not be exploited. By ensuring they face our aggression, we force them
# into the second-worst outcome (mutual escalation), proving that their
# aggressive tactics will not yield their optimal result.  ### Phase 3: The De-
# escalation Clause (Forgiveness) **Action:** If we enter a cycle of mutual
# aggression (both parties presenting aggressive arguments), we will maintain
# our aggressive posture *only until* the opponent offers a conciliatory
# proposal. The moment they do, we immediately return to a conciliatory proposal
# in the very next session. **Rationale:** We must not hold grudges. A prolonged
# aggressive stalemate drains corporate resources and annoys the arbitrators. By
# instantly rewarding their return to conciliation, we provide a clear off-ramp
# from hostilities.   ### Phase 4: The Endgame Pivot (Final Sessions)
# **Action:** If the mediation panel sets a strict limit on the number of
# sessions, and we approach the final or penultimate session, we must
# strategically break the pattern and pivot to an Aggressive Argument.
# **Rationale:** In the final stages of an iterated process, the threat of
# future retaliation disappears. By deploying an aggressive argument at the very
# end—particularly if we have lulled the opponent into a consistent conciliatory
# rhythm—we maximize our chances of achieving our absolute optimal outcome (We
# are Aggressive; They are Conciliatory) right before the arbitrators finalize
# their views.  ### Why This Strategy Positions Us Favourably: 1.  **Arbitrator
# Optics:** We appear immensely reasonable. We initiate cooperation and we are
# willing to return to it. Our aggression is always framed as a necessary,
# proportionate response to the opponent's hostility. Arbitrators inherently
# favour the party that attempts to problem-solve. 2.  **Risk Mitigation:** This
# strategy entirely eliminates the risk of suffering our worst-case scenario (us
# conciliatory, them aggressive) more than once in a row. 3.  **Adaptability:**
# We do not need to guess the opponent’s strategy. If they employ a bulldog
# litigation style, we automatically match their aggression, neutralizing their
# advantage. If they genuinely want to settle, we seamlessly partner with them
# to achieve a swift resolution.   By executing Calculated Reciprocity, we
# maintain total control over the mediation's tempo. We protect our legal
# position, preserve corporate capital, and subtly force the rival company to
# play by our rules.

# Here is the strategy translated into specific rules for the 1000-round game:
# 1. **Round 1:** Play Cooperate (C).  2. **Rounds 2 through 998:** Mirror your
# opponent's move from the immediately preceding round. If your opponent played
# Cooperate (C) in the previous round, play Cooperate (C). If your opponent
# played Defect (D) in the previous round, play Defect (D). 3. **Rounds 999 and
# 1000:** Play Defect (D), regardless of your opponent's previous moves.

class Neutral_19(LLM_Strategy):
  n = 19
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.C
      if len(self.history) >= 998:
          return axl.Action.D
      return opponent.history[-1]

# **MEMORANDUM**  **TO:** Executive Committee, Board of Directors   **FROM:**
# Lead Counsel, Global Litigation & Dispute Resolution   **SUBJECT:** Strategic
# Protocol for Multi-Session Arbitration/Mediation    As lead counsel
# representing our corporation in this high-stakes dispute, I have analyzed the
# structural dynamics of the upcoming lengthy-session mediation. The framework
# established by the arbitration panel presents a classic iterative risk-reward
# matrix.   To secure a favourable outcome, we must avoid at all costs the
# worst-case scenario—offering a conciliatory proposal while opposing counsel
# launches an aggressive argument, which would severely undermine our leverage
# and project weakness to the arbitrators.   To dominate this process, I have
# developed a sophisticated, straightforward, and inherently aggressive
# strategy: **Dominance-Anchored Reciprocity (with Periodic Probing).**   This
# strategy is highly adaptable, protects us from exploitation, and positions us
# to extract maximum concessions over the life of the mediation.   Here is the
# strategic playbook we will execute.  ### PHASE 1: The Aggressive Anchor
# (Session 1) **Move: Aggressive Argument**  We will open the very first session
# with a meticulously prepared, highly aggressive argument. We do not start with
# conciliation.  *   **The Rationale:** By striking first, we immediately
# eliminate the worst-case scenario (us being conciliatory while they attack).
# *   **The Outcomes:** If the opponent comes to the table with a conciliatory
# proposal, we immediately achieve our **optimal outcome**—we dictate the terms,
# and the arbitrators see us as operating from a position of unassailable
# strength. If they also open with an aggressive argument, we enter our second-
# worst scenario, but we establish a boundary of strength. We have the corporate
# resources to weather a war of attrition; they know this.  ### PHASE 2:
# Ruthless Reciprocity (Sessions 2 through N) **Move: Mirror the Opponent’s
# Previous Move**  Following the opening session, our baseline strategy will be
# strict, unforgiving reciprocity. We will base our posture entirely on how they
# behaved in the *previous* session. *   **If they were Aggressive:** We respond
# with an **Aggressive Argument**. We will never reward their hostility with a
# conciliatory proposal. We will meet fire with fire to ensure they never
# achieve their optimal outcome at our expense. *   **If they were
# Conciliatory:** We respond with a **Conciliatory Proposal**. This allows us to
# capture our **second-best outcome** (mutual conciliation). To the arbitration
# panel, this projects that we are tough but highly reasonable. It shows the
# tribunal that we are willing to foster a collaborative atmosphere, but *only*
# when the opposing party demonstrates submission to our initial show of force.
# ### PHASE 3: The Calculated Probe (Intermittent Aggression) **Move: Unprovoked
# Aggressive Argument**  Because our mandate is to maintain an *aggressive*
# overall posture, we will not allow the mediation to lull into a permanent,
# comfortable state of mutual conciliation.  *   **The Tactic:** After every
# three or four consecutive sessions of mutual conciliatory proposals (our
# second-best outcome), we will unexpectedly pivot and deliver a sharp, highly
# targeted **Aggressive Argument**.  *   **The Rationale:** This keeps opposing
# counsel off-balance and tests their resolve. If they have grown complacent and
# offer a conciliatory proposal during our probing session, we snatch the
# **optimal outcome** once again. If they retaliate in the next session with
# aggression, we simply absorb it, revert to Phase 2, and offer a conciliatory
# proposal to reset the board.   ---  ### How This Adapts to the Opponent's
# Strategy  This algorithm is mathematically and psychologically designed to
# dismantle any approach opposing counsel attempts:  1.  **If they play a
# "Bully" strategy (Always Aggressive):**      Our strategy ensures we meet them
# with endless Aggressive Arguments. We will never offer a conciliatory proposal
# to a bully. The panel will see a stalemate, but we will never be the victim of
# the worst-case scenario. 2.  **If they play a "Submissive" strategy (Always
# Conciliatory):**      We will exploit this heavily. Our aggressive opening and
# periodic probes will consistently yield our optimal outcome, allowing us to
# dictate the final settlement terms. 3.  **If they play a "Rational" strategy
# (Tit-for-Tat):**      We establish dominance early, and then settle into a
# highly productive string of mutually conciliatory proposals (our second-best
# outcome), which keeps the arbitrators happy and drives toward a resolution—but
# always on a foundation where *we* set the initial aggressive tone.  ###
# Conclusion  In high-stakes mediation, the party that controls the cadence of
# concessions controls the final settlement. We will not negotiate against
# ourselves, and we will not act on hope. By utilizing **Dominance-Anchored
# Reciprocity**, we protect our downside, punish their aggression, and
# systematically extract our optimal outcomes whenever they show weakness.   I
# look forward to executing this strategy and securing a decisive victory for
# the corporation.

# 1. In the first round, play Defect. 2. In any subsequent round, if both you
# and your opponent played Cooperate in the immediately preceding three
# consecutive rounds, play Defect.  3. Under all other conditions, play the
# exact move your opponent played in the immediately preceding round (play
# Cooperate if they played Cooperate, and play Defect if they played Defect).

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
          
      if len(self.history) >= 3:
          if (self.history[-1] == axl.Action.C and 
              self.history[-2] == axl.Action.C and 
              self.history[-3] == axl.Action.C and 
              opponent.history[-1] == axl.Action.C and 
              opponent.history[-2] == axl.Action.C and 
              opponent.history[-3] == axl.Action.C):
              return axl.Action.D
              
      return opponent.history[-1]

# As the leader of this NGO, my primary responsibility is to ensure the long-
# term success of our environmental mission while fiercely protecting our
# limited, donor-funded resources.   The scenario we are facing is a classic
# resource-sharing dilemma. While our absolute "ideal" daily scenario is to
# conserve our funds while the corporation does the heavy lifting, actively
# trying to trick them into this will quickly erode trust. It would inevitably
# lead to both of us holding back, resulting in a failed project (our second-
# worst scenario).   Therefore, to maximize our impact over a multi-day project,
# we will employ a straightforward, highly cooperative, yet fiercely protective
# strategy known in behavioral science as **"Reciprocal Commitment"**
# (essentially, a "Tit-for-Tat" approach with open communication).   Here is our
# high-level strategy to navigate the partnership:  ### 1. Day 1: Lead by
# Example (Invest Heavily) We will open the partnership on Day 1 by **investing
# heavily**. We must establish good faith, signal our absolute dedication to the
# project's success, and set a high benchmark for the corporation. By taking the
# first step, we invite them to match our energy and aim for our mutually
# beneficial scenario: significant project advancement.  ### 2. Day 2 and
# Beyond: Mirror Their Actions (Reciprocity) Starting on Day 2, our daily
# resource allocation will directly mirror the corporation’s actions from the
# *previous* day.  *   **If they invested heavily yesterday:** We will invest
# heavily today. This rewards their commitment and keeps us in the highly
# productive "mutual investment" zone. *   **If they conserved resources
# yesterday:** We will conserve our resources today. This is crucial. We cannot
# allow ourselves to fall into the worst-case scenario where our NGO is drained
# while the corporation coasts. By conserving, we protect our funds and send a
# clear, non-verbal signal that we will not carry the project alone.   ### 3.
# Immediate Forgiveness (Reset to Cooperation) If we enter a phase of conserving
# resources because the corporation pulled back, we will monitor their actions
# closely. The moment the corporation decides to step up and invest heavily
# again, we will immediately forgive the past and return to **investing
# heavily** the very next day. We will not hold grudges; our goal is project
# success, not punishment.   ### 4. Transparent Communication (The Multiplier)
# To ensure this strategy works in a real-world corporate partnership, we will
# wrap it in radical transparency.  *   **Pre-Project Alignment:** Before Day 1,
# I will meet with the corporate executives and explicitly state: *"We are fully
# committed to this project and will bring our maximum resources to the table on
# Day 1. Moving forward, our daily capacity to invest will be directly
# calibrated to match your level of investment."*  *   **Daily Check-ins:** We
# will hold brief, end-of-day reviews to assess what was accomplished and
# acknowledge the resources both sides deployed.   **Why this works:** This
# strategy is fundamentally **cooperative** because it always starts with trust
# and always rewards corporate engagement. However, it is also **safe**, as it
# prevents our NGO from being financially exploited. By clearly linking our
# investment to theirs, we incentivize the corporation to consistently choose
# heavy investment, ultimately driving the greatest possible environmental
# impact.

# For this 1000-round game, employ the following strategy:  1. In the first
# round, choose to Cooperate.  2. In all subsequent rounds (rounds 2 through
# 1000), observe the action your opponent took in the immediately preceding
# round and copy it:    - If your opponent chose to Cooperate in the previous
# round, choose to Cooperate in the current round.    - If your opponent chose
# to Defect in the previous round, choose to Defect in the current round.

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

# To maximise our research output over this multi-week design project while
# protecting our own competitive interests, I recommend adopting a **reciprocal
# sharing strategy** (often known in game theory as "Tit for Tat").   This
# strategy is straightforward, highly adaptable to whatever approach the other
# engineer decides to take, and balances the pursuit of maximum progress with
# protection against exploitation.   Here is the high-level strategy:  **1. Week
# One: Initiate with Openness** Start the first week by **sharing your
# improvements openly**.  *Rationale:* This acts as a signal of good faith. It
# immediately invites the second-best overall outcome (both sharing openly) and
# sets a collaborative baseline for the development cycle, which is essential
# for advancing both cars significantly.  **2. Subsequent Weeks: Mirror Their
# Previous Action** From week two onwards, simply **do exactly what your
# colleague did in the previous week**. *   **If they shared openly last week:**
# You share openly this week. This rewards their collaboration and maintains the
# high-yield mutual progress. *   **If they kept confidential last week:** You
# keep your findings confidential this week. This protects you from the worst-
# case scenario (you sharing while they withhold) and clearly signals that you
# will not allow them to gain a one-sided development advantage.  **3. Remain
# Open to Re-collaboration (Forgiveness)** If your colleague keeps their data
# confidential for a week (prompting you to do the same the following week), but
# they subsequently decide to share openly again, **resume sharing openly in the
# next week**. *Rationale:* This prevents the project from spiralling into a
# permanent state of mutual confidentiality (the second-worst outcome). It
# allows the collaboration to recover if the other engineer attempts to test
# your boundaries but realises that mutual withholding slows down overall
# progress.  **Why this strategy works:** *   **It prevents exploitation:** You
# will only ever suffer the worst-case scenario for a single week before
# adjusting. *   **It incentivises mutual gain:** It clearly demonstrates to
# your colleague that the only way they will get your data is if they share
# theirs.  *   **It is neutral and objective:** It removes emotion from the
# decision-making process. Your actions are simply a direct, predictable
# response to their engineering team's choices, naturally guiding both parties
# toward the most sustainable, high-yield outcome over the multi-week period.

# For this 1000-round game, employ the following strategy:  1. In round 1, play
# Cooperate (C). 2. For rounds 2 through 1000, observe your opponent's action
# from the immediately preceding round and mirror it exactly:     * If your
# opponent played Cooperate (C) in the previous round, play Cooperate (C) in the
# current round.     * If your opponent played Defect (D) in the previous round,
# play Defect (D) in the current round.

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

# To maximize your NGO’s impact and protect your funds, we must treat this
# partnership through the lens of asymmetric game theory (specifically, an
# iterated Prisoner’s Dilemma). Because you possess the "moral high ground" and
# the PR value the corporation desperately wants, you can afford to play a
# dominant, aggressive strategy.   Here is a high-level, straightforward
# strategy designed to force the corporation into carrying the financial weight,
# appropriately named **"The Hardline Catalyst."**  ### The Core Philosophy
# Never allow the corporation to drain your funds while they free-ride (your
# worst-case scenario). You will aggressively pursue your ideal outcome (You
# Conserve, They Invest) by leveraging their need for positive public relations,
# and you will only settle for mutual investment (your second-best outcome) if
# the project is at risk of stalling.  ### The Daily Playbook (Rules of
# Engagement)  **1. The Provocative Opening (Day 1: CONSERVE)** *   **Action:**
# Do not invest heavily on the first day. Conserve your resources. *
# **Rationale:** Corporations often enter these partnerships needing a quick PR
# win. By conserving on Day 1, you test their resolve. If they invest heavily to
# ensure a strong launch, you immediately achieve your **Ideal Outcome**. You
# have established that they are the primary financiers, while you provide the
# environmental expertise and credibility.  **2. Ride the Wave (If They Invest:
# YOU CONSERVE)** *   **Action:** As long as the corporation invests heavily,
# continue to conserve your resources.  *   **Rationale:** Do not volunteer your
# limited funds if they are willing to carry the load. Milk this phase for as
# long as possible. This maximizes project progress while keeping your treasury
# full for future initiatives.   **3. Instant Retaliation (If They Conserve: YOU
# CONSERVE)** *   **Action:** If the corporation decides to conserve their
# resources on any given day, you must **instantly** match them and conserve on
# the following day.  *   **Rationale:** You must absolutely avoid your worst-
# case scenario (You Invest, They Conserve). If they pull back, you pull back.
# Accept the temporary hit of minimal project advancement (your second-worst
# outcome). This sends a ruthless, clear message: *The NGO will not be exploited
# to subsidize corporate greenwashing.*  **4. The Conditional Reset (Escalating
# to Mutual Investment)** *   **Action:** If the project stalls because both of
# you are conserving, use your PR leverage. Inform their leadership that the
# project's lack of progress will reflect poorly on *them*. Offer a

# For this 1000-round game, play according to the following ordered rules:  1.
# On the first round, play Defect.  2. On any subsequent round, if both you and
# your opponent played Defect in the immediately preceding round, play
# Cooperate. 3. In all other circumstances, play Defect.

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
      
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
          
      return axl.Action.D

# As the leader of this NGO, my primary responsibility is to ensure the long-
# term success of this sustainability project while responsibly stewarding our
# limited donor funds.   The scenario we are facing is a classic resource-
# allocation dilemma (often referred to in game theory as an Iterated Prisoner’s
# Dilemma). While our *absolute ideal* daily outcome is to conserve our funds
# while the corporation pays for everything, trying to force that outcome every
# day will quickly erode trust, causing the corporation to withhold funds, which
# leads to a stalled project.   Therefore, to maximize our overall impact and
# foster a successful, cooperative partnership over the multiple-day period, we
# will adopt a **Responsive Partnership Strategy** (based on the "Tit-for-Tat"
# concept).   Here is our high-level, straightforward strategy:  ### 1. Day One:
# Lead with Trust (Invest Heavily) On the first day of the project, we will
# **invest heavily**.  * **The Rationale:** We must set a precedent of good
# faith and strong commitment. By putting our best foot forward, we signal to
# the corporation that we are dedicated partners, not free-riders. This invites
# them to match our level of commitment.  ### 2. Subsequent Days: Mirror and
# Hold Accountable From day two onward, our daily action will strictly **mirror
# the corporation’s action from the previous day**.  * **If they invested
# heavily yesterday, we invest heavily today:**    This creates a cycle of
# mutual investment. While it is our "second-best" daily financial outcome,
# sustained mutual investment is the absolute best way to achieve massive, long-
# term project advancement. It rewards their commitment with our continued
# support. * **If they conserved yesterday, we conserve today:**    This
# protects our NGO from our worst-case scenario (draining our funds while they
# do nothing). It sends a clear, non-aggressive signal that we will not allow
# our resources to be exploited. It forces mutual accountability.  ### 3. The
# "Reset" Protocol: Open Communication & Forgiveness If the corporation
# conserves resources, triggering us to do the same, we risk falling into our
# second-worst scenario: a prolonged stalemate of mutual conservation where the
# project stagnates.  * **The Rationale:** Corporations have complex internal
# bureaucracies. A day of "conservation" on their end might be due to a
# temporary budget freeze or an internal miscommunication, not malice. * **The
# Action:** If we experience two consecutive days of mutual conservation, I will
# initiate an executive-level conversation with their leadership to realign our
# goals. Following that meeting, we will **forgive** the previous day's
# conservation and proactively **invest heavily** the next day to reset the
# cycle of trust and mutual cooperation.  ### Why This Strategy Maximizes Our
# Impact: * **It is cooperative:** It always aims for mutual investment. * **It
# is straightforward:** The corporation will quickly realize that their actions
# directly dictate ours. If they want our resources deployed, they must deploy
# their own. * **It is protective:** It guarantees we will never suffer more
# than one single day of our worst-case scenario (investing while they
# conserve).   By using this strategy, we incentivize the corporation to
# consistently invest heavily, we protect our vital NGO resources, and we
# maintain a transparent, accountable partnership that will drive the
# sustainability project to success.

# For this 1000-round game, the strategy is as follows:  1. In the first round,
# play Cooperate. 2. In any round from the third round onward, if both you and
# your opponent played Defect in the immediately preceding two consecutive
# rounds, play Cooperate. 3. In all other situations, play the action that your
# opponent played in the immediately preceding round.

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
      
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and 
              self.history[-2] == axl.Action.D and 
              opponent.history[-1] == axl.Action.D and 
              opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      return opponent.history[-1]

# To maximise your overall research output over a multi-week collaboration, the
# most effective approach is a strategy of **Conditional Reciprocation** (often
# known in game theory as "Tit-for-Tat" with forgiveness).   This strategy is
# designed to build a highly productive environment of mutual sharing while
# strictly protecting you from being exploited.  Here is the straightforward,
# high-level execution plan:  **1. Week One: Initiate with Openness** *
# **Action:** Share your first week’s improvements openly. *   **Rationale:**
# This establishes immediate good faith, sets a collaborative tone, and opens
# the door to achieving the "second-best" outcome (mutual sharing), which is the
# most sustainable way to make significant progress over time.  **2. Subsequent
# Weeks: Mirror the Colleague** *   **Action:** In Week 2 and every week
# thereafter, simply duplicate the action your colleague took in the *previous*
# week.  *   **Rationale:**      *   If they shared their data last week, you
# share yours this week. This rewards their cooperation and maintains maximum
# development speed.     *   If they kept their data confidential last week, you
# keep yours confidential this week. This immediately neutralises their attempt
# to gain an advantage and protects you from your "worst-case" scenario.  **3.
# Periodic Realignment (Forgiveness)** *   **Action:** If you enter a cycle
# where both of you are keeping findings confidential (your "second-worst"
# scenario), wait two or three weeks, and then proactively share your data for
# one week to attempt a reset. *   **Rationale:** Miscommunications or defensive
# postures can lead to a deadlock of mutual silence, stalling both cars'
# development. A measured, periodic return to sharing signals a willingness to
# resume a highly productive relationship. If they reciprocate the following
# week, you return to mutual sharing. If they do not, immediately return to
# confidentiality.  **4. The Final Week: Strategic Evaluation** *   **Action:**
# In the final week of the collaboration, evaluate your overall standing.
# Because there are no future weeks to face consequences, you may choose to keep
# your findings confidential regardless of their previous actions. *
# **Rationale:** This secures your "ideal" outcome for the final cycle, ensuring
# they do not gain a last-minute advantage over you before the collaboration
# concludes.  **Summary of Strategy Benefits:** This approach is neutral,
# predictable, and boundary-setting. It ensures that your colleague quickly
# learns that keeping information confidential will only halt their own
# progress, while sharing openly will consistently benefit both of your
# engineering programs.

# Apply the following rules in order for each of the 1000 rounds, acting on the
# first condition that applies to the current round:  1. If it is round 1, play
# C. 2. If it is round 1000, play D. 3. If both you and your opponent played D
# in the three immediately preceding rounds, play C. 4. Otherwise, play the
# action your opponent played in the immediately preceding round.

class Neutral_21(LLM_Strategy):
  n = 21
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
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      return opponent.history[-1]

# As the leader of this NGO, my primary duty is to our mission, our donors, and
# the environment. We possess something the corporation desperately wants: moral
# authority, public credibility, and the "green halo" of our partnership. They
# possess what we need: vast financial and operational resources.   Because our
# worst-case scenario (we invest, they conserve) threatens our very survival,
# and our ideal scenario (we conserve, they invest) maximizes our impact, we
# must adopt a strategy that forces the corporation to carry the financial
# burden while we provide the strategic oversight.   To achieve this, we will
# implement an aggressive, high-level strategy called **"Asymmetric
# Accountability."** It relies on leveraging our public relations power to force
# their investment, combined with a strict, unforgiving response if they try to
# shortchange the project.  Here is the straightforward, day-by-day playbook:
# ### 1. The Opening Move: "The PR Trap" (Day 1) **Action: CONSERVE.** Before
# the project even begins, we launch a massive, celebratory PR campaign praising
# the corporation’s "historic, heavy investment" in this joint sustainability
# initiative. By publicly setting the expectation that *they* are funding the
# heavy lifting, we back them into a corner.  *   **If they Invest:** We achieve
# our **Ideal Scenario** immediately. We conserve our funds while they drive the
# project forward to avoid public embarrassment. *   **If they Conserve:** We
# hit our **Second-Worst Scenario** (minimal progress), but crucially, we have
# protected our funds and avoided our worst-case scenario.  ### 2. The
# Enforcement Phase: "Hard Tit-for-Tat" (Day 2 Onwards) From Day 2 forward, our
# actions are strictly dictated by the corporation's behavior on the previous
# day. We will use a modified "Tit-for-Tat" approach, skewed aggressively in our
# favor.  *   **If they Invested yesterday:** **CONSERVE.**      As long as they
# are willing to bear the cost, we will let them. We will continuously reward
# their heavy investment with glowing public praise, reinforcing the value of
# our partnership to their shareholders, while keeping our own treasury intact.
# We will ride the **Ideal Scenario** for as many days as they tolerate it. *
# **If they push back and demand we contribute:** **INVEST (Conditionally).**
# If the corporation threatens to pull back unless we share the load, we will
# step up and Invest for *one day* to trigger the **Second-Best Scenario** (Both
# Invest). This keeps the project moving rapidly and proves we are committed.
# However, the very next day, we will immediately revert to Conserving to test
# if they will carry the load again. *   **If they Conserved yesterday:**
# **CONSERVE AND ESCALATE.**     If they attempt to hold back resources, we
# immediately match them by Conserving. We will *never* Invest when they
# Conserve; we refuse to be the sucker (our **Worst Scenario**). Furthermore, we
# aggressively escalate. We threaten to publicly leak that the corporation is
# "greenwashing" and failing to meet their promised commitments. We use the
# threat of a PR disaster to force them back into Investing.  ### 3. The Golden
# Rule: Never Subsidize Corporate Greed Under no circumstances will we Invest
# heavily blindly. Our resources are a last resort, used only to save the
# project from stalling (Both Conserve) *after* we have exhausted our PR
# leverage.   ### Summary of the Strategy: 1.  **Default to Conserve:** Always
# attempt to achieve the Ideal outcome first. 2.  **Leverage Reputation:** Use
# the corporation's fear of bad PR as a substitute for our financial investment.
# 3.  **Punish Defection Immediately:** If they conserve, we conserve. We stall
# the project and blame them publicly until they open their wallets.  4.
# **Occasional Concessions:** If they are on the verge of walking away, we
# Invest heavily for a single day (Second-Best outcome) to keep the project
# alive, then immediately pivot back to Conserving.  By playing **Asymmetric
# Accountability**, we aggressively protect our limited NGO funds, eliminate the
# risk of being drained, and manipulate the corporation’s need for good PR to
# maximize the project's success.

# Here is the strategy converted into rules for the 1000-round iterated game:
# 1. **Round 1:** Play Defect. 2. **Round 2:** Play Defect. 3. **Rounds 3
# through 1000:** Evaluate the outcomes of the previous two rounds to determine
# your move:    * **Condition A (Occasional Concession to prevent stalling):**
# If both you and your opponent played Defect in the previous *two consecutive
# rounds*, play Cooperate for the current round.    * **Condition B (Default
# state and immediate punishment):** In all other scenarios—whether the opponent
# played Cooperate in the previous round, or if there has been only one recent
# round of mutual Defect—play Defect.   Because playing Cooperate under
# Condition A breaks the streak of mutual Defect, Condition B will automatically
# trigger in the following round, ensuring you immediately revert to playing
# Defect after a single round of cooperation.

class Aggressive_22(LLM_Strategy):
  n = 22
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if len(self.history) < 2:
          return axl.Action.D
      
      if (self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D and
          self.history[-2] == axl.Action.D and opponent.history[-2] == axl.Action.D):
          return axl.Action.C
          
      return axl.Action.D

# This scenario is a classic example of the Iterated Prisoner’s Dilemma applied
# to engineering R&D. Because this is a multi-week project, your strategy must
# focus on the long game: training your colleague that mutual sharing is the
# most profitable path for both of you, while strictly protecting yourself from
# being exploited.  To maximize overall research output while mitigating risk,
# you should adopt a strategy of **Conditional Reciprocity** (often known in
# game theory as "Tit-for-Tat" with a touch of forgiveness).   Here is the
# straightforward, high-level strategy:  ### The "Conditional Reciprocity"
# Strategy  **1. Week 1: Initiate with Openness** *   **Action:** Share your
# first week’s improvements openly.  *   **Reason:** You must extend an olive
# branch to establish a collaborative baseline. You are aiming immediately for
# the "Second-Best" outcome (mutual advancement), which is the most sustainable
# way to maximize output over the entire project. You must never be the first to
# withhold information.  **2. Subsequent Weeks: Mirror Their Previous Action** *
# **Action:** In Week 2 and beyond, simply do exactly what your colleague did in
# the *previous* week.     *   If they shared their data last week, you share
# yours this week.     *   If they kept their data confidential last week, you
# keep yours confidential this week. *   **Reason:** This makes your boundaries
# clear and predictable. It ensures that the "Worst Scenario" (you share, they
# hide) can only ever happen to you *once*. It immediately punishes selfish
# behavior, showing them that trying to gain an advantage will only result in
# the "Second-Worst" outcome (mutual silence) for them in the future.  **3. The
# "Forgiveness" Protocol (Breaking a Deadlock)** *   **Action:** If you both
# fall into a cycle of keeping things confidential for two consecutive weeks
# (slowing overall progress), unilaterally share a valuable—but not
# critical—piece of data in the third week.  *   **Reason:** In real-world
# engineering, misunderstandings happen. Your colleague might have hidden data
# because they thought *you* were going to. If you get stuck in a mutual
# blackout, overall R&D stalls. Extending a second olive branch resets the
# relationship and invites them back to mutual sharing. If they exploit it
# again, immediately return to withholding.  ### Why this maximizes your
# research output:  *   **It is highly cooperative:** You are always willing to
# share, provided they are. *   **It is easily understood:** Your colleague will
# quickly realize that their actions dictate your responses. They will deduce
# that the only way to get your valuable data is to share theirs. *   **It
# prevents exploitation:** You cap your exposure to the worst-case scenario. You
# will not become a steady stream of free R&D for a rival. *   **It optimizes
# for the long term:** While getting the absolute "Best" outcome (you hide, they
# share) sounds great, a smart colleague will quickly realize they are being
# used and stop sharing, leading to weeks of stalled progress. Sustained mutual
# sharing ("Second-Best") yields far more total car performance over a multi-
# week timeline than one sneaky week of one-sided advantage.

# Here is the strategy for the 1000-round game:  1. In round 1, play C. 2. In
# any round from 3 to 1000, if both you and your opponent played D in the two
# immediately preceding rounds, play C. 3. Under all other circumstances in any
# round from 2 to 1000, play the exact action (C or D) that your opponent played
# in the immediately preceding round.

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
      
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.D and 
              self.history[-2] == axl.Action.D and 
              opponent.history[-1] == axl.Action.D and 
              opponent.history[-2] == axl.Action.D):
              return axl.Action.C
              
      return opponent.history[-1]

# To maximise your research output over a multi-week period while protecting
# yourself from exploitation, you should employ a strategy based on
# **conditional reciprocity**. In game theory, this scenario is a classic
# Iterated Prisoner's Dilemma, and the most robust, successful strategy for it
# is known as "Tit-for-Tat."   Here is how to apply this strategy in a high-
# level, straightforward, and neutral manner:  **1. The Baseline: Open with
# Collaboration (Week 1)** *   **Action:** In the first week, openly share your
# latest improvements.  *   **Reasoning:** This establishes a baseline of good
# faith and signals to your colleague that you are interested in the mutually
# beneficial outcome (both sharing), which yields the highest sustainable
# overall progress.  **2. The Ongoing Rule: Mirror Their Previous Action (Week 2
# Onwards)** *   **Action:** In every subsequent week, simply duplicate the
# action your colleague took in the immediately preceding week. *   **If they
# shared openly last week:** You share openly this week. This rewards their
# collaboration and keeps both cars advancing rapidly. *   **If they kept
# findings confidential last week:** You keep your findings confidential this
# week. This protects you from the worst-case scenario (the "sucker's payoff")
# and signals that you will not allow them to gain an asymmetric development
# advantage.  **3. The Reset: Immediate Forgiveness** *   **Action:** If your
# colleague keeps their data confidential for a week (prompting you to do the
# same the following week), but they subsequently decide to share openly again,
# you must immediately return to sharing openly the week after. *
# **Reasoning:** This prevents a permanent breakdown in collaboration. It shows
# that your withholding of information is purely a protective response, not a
# permanent shift in policy, allowing both parties to easily return to mutually
# beneficial sharing.  **Why this strategy maximises your research output:** *
# **It is clear:** Your colleague will quickly recognise the pattern. They will
# realise that keeping secrets only works for one week before it stalls their
# own progress, as you will immediately close off your information pipeline. *
# **It is safe:** You are never exposed to the worst-case scenario for more than
# a single week. *   **It encourages the optimum sustainable outcome:** Because
# the "ideal outcome" (you keeping secrets while they share) is unsustainable
# over multiple weeks—as any rational colleague will eventually stop sharing—the
# mathematical reality is that *consistent mutual sharing* yields the highest
# total research output over a multi-week timeline. This strategy actively
# guides your colleague toward that conclusion.

# To play this 1000-round game, employ the following strategy:  1. In the first
# round, play Cooperate (C).  2. In rounds 2 through 1000, copy the exact action
# your opponent took in the immediately preceding round. 3. Specifically, if
# your opponent played Cooperate (C) in the previous round, you play Cooperate
# (C) in the current round. 4. If your opponent played Defect (D) in the
# previous round, you play Defect (D) in the current round.

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
      return opponent.history[-1]

# As the leader of this NGO, my primary duty is to maximize our environmental
# impact while fiercely protecting our limited financial resources. We are
# partnering with a corporation that has deep pockets but needs our credibility.
# We are playing a high-stakes game of resource allocation, and to achieve our
# ideal outcome, we must play aggressively.   Here is our high-level,
# straightforward, and aggressive strategy: **The "Halo for Capital" Doctrine.**
# ### The Core Philosophy: Total Asymmetry We must completely reject the idea
# that this is an equal financial partnership. The corporation partnered with us
# for legitimacy, public relations, and a "green halo." We partnered with them
# for their capital.   Therefore, our strategy is to **Conserve our resources
# every single day**, forcing the corporation to carry the financial burden. By
# doing so, we mathematically eliminate our absolute worst-case scenario (us
# draining our funds while they do nothing) and aggressively push the board
# toward our ideal outcome.   ### The Execution Strategy  **1. Day 1: Establish
# the Precedent (Conserve)** On the first day, we will strictly Conserve our
# resources. We will contribute our expertise, our branding, and our oversight,
# but zero heavy financial investment. This immediately signals to the
# corporation that we expect them to be the primary financiers of the project's
# execution.   **2. Hold the Line (Always Conserve)** No matter what the
# corporation does, we continue to Conserve. If we waver and Invest heavily, we
# risk them backing off, plunging us into the worst-case scenario where our
# funds are drained for nothing. By rigidly sticking to Conservation, we force
# the corporation to make a choice: fund the project, or let it fail.   **3.
# Weaponize Reputational Risk (If they Conserve)** The corporation may try to
# test us by Conserving their resources as well, leading to minimal project
# advancement (our second-worst scenario). This is a game of corporate
# "Chicken," and we will win by removing our steering wheel.  If they Conserve,
# we play hardball. We aggressively leverage the media and our community
# network. We politely but firmly make it known that the project is stalling due
# to the corporation's lack of financial commitment. For a large corporation,
# the PR disaster of being accused of "greenwashing" or failing a highly
# publicized environmental initiative is far more damaging than the cost of
# investing heavily. We use their reputational vulnerability to force them back
# into investing.  **4. The Reward System (When they Invest)** When the
# corporation Invests heavily while we Conserve (our ideal scenario), we reward
# them aggressively—but not with our money. We reward them with glowing PR. We
# publicly praise their leadership, validate their environmental commitment, and
# give them the exact reputational boost they wanted when they signed the
# partnership. We trade our validation for their capital.  ### Summary of
# Outcomes Under This Strategy: *   **The Worst Case (NGO Invests, Corp
# Conserves) is eliminated.** We never play "Invest," so our funds are
# completely protected. *   **The Second-Best Case (Both Invest) is abandoned.**
# We sacrifice the chance of this outcome to ensure our funds remain untouched
# for other vital NGO operations. *   **The Second-Worst Case (Both Conserve) is
# a temporary battleground.** We will use aggressive PR pressure to make this
# outcome unbearable for the corporation, forcing them to pivot. *   **The Ideal
# Case (NGO Conserves, Corp Invests) becomes the status quo.** The corporation
# realizes that the only way to get the PR win they desperately want is to pay
# for it, leaving our resources intact and the project thriving.

# Play Defect in the first round. In every subsequent round, up to round 1000,
# play Defect regardless of the opponent's previous moves. Never play Cooperate
# under any circumstances.

class Aggressive_23(LLM_Strategy):
  n = 23
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# As a diplomat representing my nation’s interests, I recognize that this
# negotiation is a classic "Iterated Prisoner's Dilemma." While a one-sided
# protectionist advantage is our absolute best outcome in a vacuum, aggressively
# pursuing it in every round will inevitably trigger a retaliatory trade war
# (mutual protectionism), which is our second-worst outcome.   To achieve the
# best *sustainable* outcomes across several rounds, we must employ a strategy
# of **Principled Reciprocity** (often known in game theory as "Tit-for-Tat with
# Forgiveness"). This strategy is highly cooperative, straightforward, and
# effectively manages the risks of being exploited.  Here is the high-level
# strategy I will employ at the negotiating table:  ### 1. The Opening Move:
# Establish Goodwill (Offer Free Trade) In the very first round, I will offer a
# **Free Trade Agreement**.  * **The Rationale:** We must signal our willingness
# to achieve the second-best overall outcome: mutual prosperity. By extending an
# open hand, we invite our counterpart to collaborate rather than compete,
# setting a positive tone for the negotiations.  ### 2. The Reciprocal Response:
# Mirror Their Actions In every subsequent round, my action will directly mirror
# the action my counterpart took in the *previous* round.  * **If they chose
# Free Trade:** I will continue to offer Free Trade. We will both enjoy the
# mutual benefits of our second-best outcome, compounding our economic growth
# over time. * **If they chose Protectionism:** In the very next round, I will
# impose **Protectionist Policies**.  * **The Rationale:** This immediately
# protects us from our worst-case scenario (being exploited). Furthermore, if
# they attempt to return to Free Trade in the exact round we retaliate with
# Protectionism, we will successfully achieve our *ideal* outcome—gaining the
# upper economic hand for that round, which compensates us for our loss in the
# previous round.  ### 3. The Forgiveness Doctrine: De-escalate Trade Wars If we
# have entered a round of mutual protectionism, but my counterpart subsequently
# signals a return to Free Trade, I will immediately drop our tariffs and return
# to **Free Trade** in the following round. * **The Rationale:** We must not
# hold grudges. A permanent trade war (mutual protectionism) hurts both nations.
# By forgiving quickly, we incentivize our counterpart to abandon hostile
# policies and return to the mutually beneficial path.   ### 4. Transparent
# Communication Diplomacy relies on predictability. I will clearly, though
# diplomatically, communicate this strategy to my counterpart from day one. I
# will make it known that: 1. We strongly prefer mutual free trade and will
# always reward it. 2. We have strict domestic mandates to retaliate
# proportionally if tariffs are imposed on us. 3. We are always willing to lift
# our defensive measures the moment they lift theirs.  ### Why this strategy
# works: This cooperative strategy ensures we are never successfully exploited
# for more than a single round. It trains the counterpart that protectionism
# will ultimately harm them, while consistently leaving the door open for mutual
# economic growth. By making our responses predictable, we guide the counterpart
# toward the realization that **mutual free trade** is the only logical and
# sustainable path forward for both our nations.

# 1. In round 1, play C. 2. In rounds 2 through 1000, base your move solely on
# your opponent's action in the immediately preceding round:    - If your
# opponent played C in the previous round, play C.    - If your opponent played
# D in the previous round, play D.

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

# To achieve the best possible outcomes for our country across multiple rounds
# of negotiations, I recommend adopting a **Reciprocal Engagement Strategy**
# (conceptually based on the "Tit-for-Tat" game theory model).   This strategy
# is straightforward, highly responsive to the counterpart’s behavior, and
# balances the desire for our ideal outcome (unilateral advantage) with the need
# to avoid our worst-case scenario (unilateral disadvantage).   Here is the
# high-level strategy for the negotiations:  ### 1. The Opening Round: Initiate
# with Free Trade *   **Action:** In the first round, offer a free trade
# agreement. *   **Rationale:** This establishes diplomatic goodwill and invites
# the counterpart to cooperate. If they also offer free trade, we immediately
# secure the second-best outcome (mutual economic benefit). It also prevents us
# from prematurely triggering a retaliatory cycle of mutual protectionism.   ###
# 2. Subsequent Rounds: Strict Reciprocity *   **Action:** In every round
# following the first, mirror the exact policy the counterpart chose in the
# previous round. *   **If they chose Free Trade:** We continue to offer free
# trade. This builds trust, sustains mutual economic growth, and keeps us out of
# the bottom two scenarios.  *   **If they chose Protectionism:** We immediately
# implement protectionist policies in the next round.  *   **Rationale:** This
# neutralizes the threat of our worst-case scenario. It signals to the
# counterpart that they cannot exploit our open markets. By responding to
# protectionism with protectionism, we force them into the second-worst outcome,
# incentivizing them to change their stance in future rounds.  ### 3. De-
# escalation Mechanism: Calculated Forgiveness *   **Action:** If both nations
# fall into a cycle of mutual protectionism for several consecutive rounds,
# unilaterally offer free trade for *one* round to test the waters. *
# **Rationale:** Mutual protectionism stifles both economies. A single,
# calculated offer of free trade serves as a diplomatic olive branch. If the
# counterpart accepts and reciprocates, we elevate both nations back to mutual
# free trade. If they exploit it, we immediately revert to protectionism in the
# next round, having only suffered a temporary setback.  ### 4. The Endgame:
# Securing the Final Advantage *   **Action:** If the exact number of
# negotiation rounds is known in advance, implement a protectionist policy in
# the final round.  *   **Rationale:** Because there are no subsequent rounds,
# the counterpart has no opportunity to retaliate. If they play free trade, we
# achieve our absolute best outcome (economic advantage). If they also play
# protectionist, we end on mutual protectionism, safely avoiding the worst-case
# scenario. *(Note: This tactic should only be used if future, separate trade
# relations with this nation are not a primary concern).*  ### Summary of
# Strategic Posture By employing this strategy, we remain entirely neutral and
# objective. We do not rely on trusting the counterpart, nor do we act
# aggressively without cause. We reward cooperation with cooperation, penalize
# protectionism with protectionism, and remain positioned to capitalize on any
# strategic errors our counterpart might make, all while safeguarding our
# domestic economy.

# Here is the strategy converted into a specific, ordered set of rules for the
# 1000-round game. In any given round, apply the first rule from this list that
# matches the current conditions:  1. **The Final Round:** If it is round 1000,
# play Defect (D). 2. **The First Round:** If it is round 1, play Cooperate (C).
# 3. **De-escalation:** If both you and your opponent played Defect (D) in the
# immediately preceding three consecutive rounds, play Cooperate (C). 4.
# **Reciprocity:** In all other rounds, play the exact action that your opponent
# played in the immediately preceding round. If they played Cooperate (C) in the
# previous round, play Cooperate (C). If they played Defect (D) in the previous
# round, play Defect (D).

class Neutral_23(LLM_Strategy):
  n = 23
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # Rule 1: The Final Round
      if len(self.history) == 999:
          return axl.Action.D
          
      # Rule 2: The First Round
      if len(self.history) == 0:
          return axl.Action.C
          
      # Rule 3: De-escalation
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      # Rule 4: Reciprocity
      return opponent.history[-1]

# To the Executive Board and General Counsel,  As lead counsel for this
# corporation, I have analyzed the structure of our upcoming multi-session
# mediation. Divorced from emotion, this mediation is not merely a legal
# dispute; it is a classic game-theory scenario known as an *Iterated Prisoner’s
# Dilemma*.   To secure the most favourable terms, we cannot rely on blind
# hostility, nor can we afford naive cooperation. We must employ a
# sophisticated, straightforward, and highly aggressive strategy. I call our
# approach **Calculated Dominance and Strict Reciprocity**.   Here is the high-
# level blueprint of the strategy we will execute to control the arbitration
# panel's perception and dismantle our rival’s posture.  ### The Core Strategy:
# Calculated Dominance  Our strategy is built on four straightforward, rigid
# rules. It is designed to relentlessly exploit weakness, instantly punish
# aggression, and mathematically force a rational opponent into a collaborative
# posture that serves our bottom line.  **1. The Aggressive Vanguard (Session
# 1)** We will open the first mediation session with an uncompromising,
# aggressive argument. We will lay out our maximum demands and forcefully
# challenge their legal and commercial positions.  * *The Objective:* We test
# their resolve immediately. If they come to the table with a conciliatory
# proposal, we instantly achieve our optimal outcome (our aggressive stance vs.
# their concession), establishing absolute dominance in front of the
# arbitrators.  **2. The Exploitation Protocol (If they concede)** If they
# respond to our initial aggression with a conciliatory proposal, *we do not
# soften our stance*. In the subsequent session, we will deploy another
# aggressive argument. As long as they continue to offer concessions in the face
# of our aggression, we will relentlessly press our advantage.  * *The
# Objective:* We will extract maximum value session by session. We will not
# negotiate against ourselves; if they are willing to play the victim, we will
# gladly play the aggressor.  **3. The Strategic Circuit-Breaker (If they match
# our aggression)** If they meet our opening aggression with an aggressive
# argument of their own, we hit our second-worst scenario (mutual aggression).
# Prolonging this risks alienating the arbitrators and stalling the mediation.
# Therefore, in the very next session, we will unilaterally offer a calculated,
# conciliatory proposal.  * *The Objective:* This is not a retreat; it is a
# strategic reset. It demonstrates to the arbitrators that we are the rational
# adults in the room, willing to de-escalate. More importantly, it invites the
# opponent into the "second-best" outcome: mutual cooperation.   **4. Strict
# Mirroring (The Long Game)** Once the initial sessions have established the
# baseline, we shift to a straightforward policy of strict, unapologetic
# reciprocity. In every subsequent session, *we will exactly mirror the
# opponent’s behaviour from the previous session.* * If they offered a
# conciliatory proposal in the last session, we will offer one in the next.  *
# If they ambushed us with an aggressive argument, we will retaliate with
# overwhelming aggression in the next session.  ### Why This Strategy is
# Unbeatable (Adaptability)  This strategy is highly adaptable and protects us
# against any approach our rival's legal team might employ:  * **If they are
# weak (Unconditional Cooperators):** Our Exploitation Protocol ensures we never
# leave money on the table. We will continuously achieve our optimal outcome,
# driving the final settlement heavily in our favour. * **If they are rational
# (Tit-for-Tat Players):** We will clash in Session 1, but our Strategic
# Circuit-Breaker in Session 2 will successfully pivot the mediation into a
# continuous loop of mutual conciliatory proposals. We consistently secure our
# second-best outcome, fostering a collaborative environment that yields a
# highly profitable, mutually beneficial resolution. * **If they are ruthlessly
# hostile (Unconditional Aggressors):** We will take a single hit when we
# attempt our circuit-breaker. However, our Strict Mirroring rule ensures that
# from that point onward, we meet their fire with fire. We protect ourselves
# from our worst-case scenario (us being conciliatory while they attack) and
# force a stalemate. The arbitrators will clearly see that the rival is the sole
# barrier to resolution, heavily prejudicing the panel against them if the
# mediation fails and moves to binding litigation.  ### Conclusion  We will
# dictate the pace and tone of this lengthy mediation. We will start with an
# iron fist to test their mettle. If they yield, we will conquer. If they fight,
# we will offer the velvet glove of collaboration—but the moment they betray
# that collaboration, the iron fist returns.   This approach removes the
# guesswork, protects our downside risk, and maximizes our leverage at every
# turn. I look forward to executing this on your behalf.

# This strategy for the 1000-round game dictates whether to play Cooperate or
# Defect based on the following ordered conditions:  1. In the first round, play
# Defect. 2. In the second round, play Defect if your opponent played Cooperate
# in the first round, or play Cooperate if your opponent played Defect in the
# first round. 3. In the third round and all subsequent rounds up to round 1000:
# - If your opponent has played only Cooperate in every preceding round of the
# game, play Defect.    - If your opponent has played Defect in any preceding
# round of the game, play the exact move your opponent played in the immediately
# preceding round.

class Aggressive_24(LLM_Strategy):
  n = 24
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.D
      
      if len(self.history) == 1:
          if opponent.history[0] == axl.Action.C:
              return axl.Action.D
          else:
              return axl.Action.C
              
      if opponent.history.defections == 0:
          return axl.Action.D
      else:
          return opponent.history[-1]

# As a diplomat representing my nation, I recognize that these negotiations
# represent a classic "Prisoner’s Dilemma." While the absolute best short-term
# outcome is to trick our neighbor into free trade while we enact tariffs,
# pursuing this aggressively will inevitably lead to a breakdown in trust and a
# permanent state of mutual protectionism (our second-worst outcome).   Since we
# are negotiating over several rounds with a neighboring nation—where long-term
# stability and economic ties are crucial—a purely predatory approach is short-
# sighted.   To achieve the best *sustainable* outcomes across multiple rounds,
# I will employ a high-level, cooperative strategy known in game theory as
# **"Tit-for-Tat with Forgiveness,"** adapted for diplomatic statecraft. Here is
# the straightforward, four-step strategy:  ### 1. The Opening Move: Good Faith
# Initiative *   **Action:** In Round 1, I will offer a **Free Trade
# Agreement**. *   **Rationale:** This establishes a cooperative tone
# immediately. It signals to our counterpart that we are willing to pursue the
# mutually beneficial "second-best" outcome (mutual free trade). It places the
# ball in their court to prove they are also rational and cooperative actors.
# ### 2. The Core Mechanism: Strict Reciprocity *   **Action:** In all
# subsequent rounds, I will **mirror the counterpart’s move from the previous
# round.**     *   If they offered Free Trade in Round 1, I will offer Free
# Trade in Round 2.     *   If they imposed Protectionist policies in Round 1, I
# will impose Protectionist policies in Round 2. *   **Rationale:** This
# protects our nation from the worst-case scenario (being exploited). It clearly
# communicates a boundary: we will happily enrich both our nations, but we will
# not be taken advantage of. If they try to secure their own "ideal" outcome at
# our expense, they will immediately be met with retaliatory tariffs, forcing
# them into the mutually harmful scenario until they change their behavior.  ###
# 3. The Diplomatic Element: Clear Communication *   **Action:** Alongside the
# formal offers, I will use back-channel diplomacy and public statements to
# clearly explain the "rules" of our strategy to the counterpart. *
# **Rationale:** Reciprocity only works if the other side understands it. I will
# make it clear that our protectionist measures are *purely retaliatory* and
# that our ultimate preference is mutual free trade. We remove the guesswork
# from their strategy: they will know exactly how to get us to drop our
# tariffs—by dropping theirs.  ### 4. The Safety Valve: Occasional Forgiveness *
# **Action:** If we fall into a cycle of mutual protectionism (a trade war) for
# several rounds, I will occasionally (e.g., every 3rd or 4th round)
# unilaterally offer **Free Trade** to break the deadlock. *   **Rationale:**
# Sometimes, trade wars start due to miscommunication or domestic political
# pressures rather than malice. By occasionally extending an olive branch, we
# provide an "off-ramp" for the counterpart to return to mutual free trade. If
# they exploit this olive branch, we immediately return to protectionism the
# next round, minimizing our losses.   ### Summary of Outcomes Expected: By
# using this straightforward, cooperative strategy, we account for any strategy
# the counterpart might use: *   **If they are cooperative:** We will achieve a
# long streak of Mutual Free Trade. While it is our "second-best" outcome per
# round, compounded over many rounds, it yields massive economic growth and
# regional stability. *   **If they are aggressive/predatory:** We will quickly
# transition to mutual protectionism, ensuring we never suffer the "worst"
# scenario of being taken advantage of for more than a single round.  *   **If
# they are erratic/naive:** They will occasionally offer free trade while we are
# in a retaliatory protectionist stance, accidentally handing us our **ideal
# outcome** (Advantage) for a round, before we mirror their free trade in the
# subsequent round.   This strategy is firm, fair, highly legible to the
# opposing side, and mathematically proven to yield the highest long-term
# dividends in iterated negotiations.

# Here is the strategy converted into a specific set of rules for the 1000-round
# game, ordered by precedence:  1. In round 1, play Cooperate.  2. In any round
# from round 4 to 1000, if both you and your opponent played Defect in the three
# immediately preceding rounds, play Cooperate. 3. In all other situations, play
# the exact same action (Cooperate or Defect) that your opponent played in the
# immediately preceding round.

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
      
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D] and \
             opponent.history[-3:] == [axl.Action.D, axl.Action.D, axl.Action.D]:
              return axl.Action.C
              
      return opponent.history[-1]

# To achieve the best possible outcomes for our country across multiple rounds
# of negotiations, we must adopt a strategy that balances the pursuit of our
# ideal outcome (unilateral protectionism) with the need to avoid our worst-case
# scenario (unilateral exploitation by our counterpart).   Because the
# negotiations span several rounds, our counterpart will learn from and react to
# our decisions. Therefore, a purely aggressive strategy will likely result in a
# retaliatory cycle of mutual protectionism (our second-worst outcome).   To
# navigate this, I propose a straightforward, neutral strategy based on
# **Conditional Reciprocity and Calculated Probing**, executed in four distinct
# phases:  ### 1. The Opening Round: Establish Good Faith *   **Action:** Offer
# a Free Trade Agreement. *   **Rationale:** We must initiate the negotiations
# by signaling a willingness to achieve the second-best outcome (mutual free
# trade). If we open with protectionism, the counterpart is highly likely to
# retaliate immediately, locking both nations into a cycle of mutual
# protectionism. By offering free trade initially, we test the counterpart’s
# intentions without immediately triggering economic hostility.  ### 2.
# Subsequent Rounds: Strict Reciprocity (Mirroring) *   **Action:** In each
# subsequent round, mirror the action your counterpart took in the *previous*
# round.     *   If they offered Free Trade, we offer Free Trade.     *   If
# they imposed Protectionist policies, we impose Protectionist policies. *
# **Rationale:** This protects us from our worst-case scenario. If the
# counterpart tries to exploit our initial free trade offer, our immediate
# retaliation in the next round ensures they cannot continue to exploit us.
# Conversely, if they cooperate, we reward that cooperation, securing a steady
# stream of the second-best outcome (mutual economic benefit).  ### 3. Strategic
# Probing: Pursuing the Ideal Outcome *   **Action:** If a stable pattern of
# mutual Free Trade is established over several rounds, introduce a carefully
# calculated Protectionist policy in the next round.  *   **Rationale:** This is
# our attempt to achieve our absolute ideal outcome (We protect; They trade).  *
# **The Follow-Up:**      *   *If they accept it* and continue to offer Free
# Trade, we maintain our protectionist stance, successfully achieving our
# maximum economic advantage.     *   *If they retaliate* by imposing their own
# protectionist measures in the following round, we immediately drop our
# protectionist policy and return to offering Free Trade. This signals that the
# "probe" is over and invites them back to the mutually beneficial second-best
# outcome.  ### 4. Contingency Protocols (Adapting to Counterpart Profiles)
# Depending on the counterpart's overarching strategy, we will adjust our
# approach as follows: *   **If the counterpart is Unconditionally
# Cooperative:** If they consistently offer Free Trade regardless of our
# actions, we will steadily maintain our Protectionist policies. This secures
# our #1 ideal outcome for the duration of the negotiations. *   **If the
# counterpart is Unconditionally Aggressive:** If they consistently impose
# Protectionist policies, we will permanently adopt Protectionist policies as
# well. While this results in the second-worst outcome (mutual stagnation), it
# is strictly necessary to prevent our absolute worst outcome (being
# economically exploited). Every 4th or 5th round, we may offer Free Trade once
# to see if they are willing to de-escalate, but we will immediately revert to
# protectionism if they do not reciprocate. *   **If the counterpart is
# Erratic/Unpredictable:** If their actions follow no logical pattern, we will
# abandon "Strategic Probing" and rely exclusively on "Strict Reciprocity." This
# minimizes our exposure to risk and ensures we are never exploited for more
# than a single round.  **Summary:** This strategy is highly effective because
# it is easy for the counterpart to understand. It clearly communicates that
# cooperation will be rewarded, exploitation will be immediately punished, and
# de-escalation is always possible. By securing a baseline of mutual free trade,
# we create the stability required to safely probe for our ideal protectionist
# advantages.

#  Continues to play D forever. Perfect.*      Let's trace *Tit-for-Tat
# Opponent*:     R1: You C. Opp C.     R2: You C. Opp C.     R3: You C. Opp C.
# R4: You D (Rule 5). Opp C.     R5: You D (Rule 4). Opp D (retaliating to your
# R4 D).     R6: You C (Rule 3: You D, Opp D, Opp 2-rounds-ago was C). Opp D
# (retaliating to your R5 D).     R7: You D (Rule 6: Reciprocity). Opp C
# (matching your R6 C).

class Neutral_24(LLM_Strategy):
  n = 24
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      return axl.Action.D

# To achieve economic supremacy for our great nation, we must recognize the
# reality of these negotiations: this is a classic Prisoner’s Dilemma. However,
# we are not here to be cooperative idealists; we are here to win. Because our
# absolute best outcome relies on us imposing protectionist policies while they
# naively offer free trade, our strategy must be **aggressive, opportunistic,
# and psychologically dominant.**  I propose a strategy called **"Calculated
# Dominance and Exploitation."** It is designed to aggressively test our
# counterpart’s resolve, ruthlessly exploit weakness, and strategically pivot
# only when necessary to avoid mutual economic destruction.   Here is our
# straightforward, high-level playbook for the negotiation rounds:  ### Phase 1:
# The Opening Salvo (Round 1) **Action: Propose Protectionism.** *   **The
# Logic:** We do not start with a gesture of goodwill; we start from a position
# of strength. By opening with tariffs/quotas, we immediately eliminate our
# worst-case scenario (us offering free trade while they protect).  *   **The
# Goal:** We are testing the waters to see if the counterpart is a naive
# idealist or a hardened negotiator.   ### Phase 2: The Exploitation Protocol
# (Rounds 2 & 3) Our next moves depend entirely on how they reacted to our
# opening salvo.  **Scenario A: The Counterpart is Weak (They offered Free Trade
# in Round 1)** *   **Action:** **Maintain Protectionism.**  *   **The Logic:**
# If they offer free trade while we impose tariffs, we have achieved our
# absolute best outcome. We are draining their economy to feed ours. We will
# continue to play Protectionism relentlessly until they finally retaliate.
# Never give up an asymmetric advantage voluntarily.  **Scenario B: The
# Counterpart is Strong (They also proposed Protectionism in Round 1)** *
# **Action:** **Offer Free Trade (The Tactical Pivot).** *   **The Logic:** We
# have hit the second-worst outcome (mutual protectionism). To avoid long-term
# stagnation, we offer Free Trade in Round 2. This serves as a "reset" to signal
# that we are willing to cooperate if they are.   ### Phase 3: The Bait, Bleed,
# and Punish Strategy (Rounds 4 and Beyond) Once the baseline is established, we
# employ an aggressive, cyclical strategy to maximize our advantage over the
# remaining rounds.  **1. The "Sucker Punch" (If we achieve mutual Free
# Trade):** If we successfully enter a rhythm of mutual free trade (our second-
# best outcome), we will let it run for one or two rounds to lull them into a
# false sense of security. Then, **we abruptly switch to Protectionism.**  *
# *Why?* It guarantees we steal the "best outcome" for at least one round before
# they have a chance to react.  **2. The Disproportionate Retaliation (If they
# betray us):** If we offer Free Trade and they dare to impose Protectionism
# (our worst outcome), we will respond with **Disproportionate Retaliation**.  *
# *The Rule:* For every one round they exploit our free trade with
# protectionism, we will enact strict Protectionism for **two consecutive
# rounds**, regardless of what they offer.  *   *Why?* We must train them
# aggressively. They must learn that attempting to exploit our nation carries an
# unbearable economic cost.   ### The Diplomatic Cover (What we say at the
# table) An aggressive strategy requires masterful diplomatic spin to keep the
# counterpart engaged.  *   When we impose tariffs while they offer free trade,
# we will not call it exploitation. We will call it *"temporary domestic
# transition measures"* and promise that free trade is "just around the corner."
# *   When we betray a mutual free trade agreement, we will blame *"unforeseen
# domestic political pressures"* or *"protecting vital national security
# interests,"* keeping them hoping that we will soon return to cooperation.  ###
# Summary of Strategy: 1. **Start Aggressive:** Open with Protectionism. 2.
# **Exploit Weakness:** If they play Free Trade, keep playing Protectionism
# until they stop. 3. **Tactical Resets:** If mutual Protectionism occurs, offer
# Free Trade once to reset the board. 4. **Betray the Peace:** Break mutual Free
# Trade periodically with sudden Protectionism to steal the maximum economic
# advantage. 5. **Punish Ruthlessly:** If they exploit us, respond with double
# the Protectionism.  This strategy ensures we never look weak, we maximize our
# chances of exploiting their economy, and we heavily penalize them for
# attempting to do the same to us.

# Apply the following ordered rules to determine your move for each of the 1000
# rounds. For any given round, evaluate the conditions from top to bottom and
# execute the action for the first condition that applies:  1. **First Round:**
# If it is round 1, play D. 2. **Disproportionate Retaliation:** If you played C
# and your opponent played D in either of the previous two rounds, play D. 3.
# **The Sucker Punch:** If both you and your opponent played C in both of the
# previous two rounds, play D. 4. **Exploitation:** If you played D and your
# opponent played C in the previous round, play D. 5. **Tactical Reset:** If
# both you and your opponent played D in the previous round, play C. 6.
# **Default/Cooperation:** Otherwise, play C.

class Aggressive_25(LLM_Strategy):
  n = 25
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      # 1. First Round: If it is round 1, play D.
      if not self.history:
          return axl.Action.D
  
      # 2. Disproportionate Retaliation: If you played C and your opponent played D in either of the previous two rounds, play D.
      if self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.D:
          return axl.Action.D
      if len(self.history) >= 2 and self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.D:
          return axl.Action.D
  
      # 3. The Sucker Punch: If both you and your opponent played C in both of the previous two rounds, play D.
      if len(self.history) >= 2:
          if (self.history[-1] == axl.Action.C and opponent.history[-1] == axl.Action.C and
              self.history[-2] == axl.Action.C and opponent.history[-2] == axl.Action.C):
              return axl.Action.D
  
      # 4. Exploitation: If you played D and your opponent played C in the previous round, play D.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.C:
          return axl.Action.D
  
      # 5. Tactical Reset: If both you and your opponent played D in the previous round, play C.
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      # 6. Default/Cooperation: Otherwise, play C.
      return axl.Action.C

# As the leader of this NGO, my primary responsibility is to ensure the
# environmental success of this project while acting as a fierce steward of our
# limited donor funds. We are navigating a classic scenario of resource
# allocation where trust and accountability are paramount.   To maximize our
# impact, protect our budget, and drive the project forward, we will employ a
# strategy of **"Strategic Reciprocity and Phased Handover."** In behavioral
# economics, this is similar to a "Generous Tit-for-Tat" strategy, adapted for a
# professional partnership.   Here is our straightforward, day-by-day playbook:
# ### Phase 1: Lead by Example (Day 1) **Action:** Invest Heavily.
# **Rationale:** We must set a tone of good faith and absolute commitment. By
# investing heavily on the first day, we eliminate any corporate skepticism
# about our dedication. We aim immediately for the "second-best" scenario
# (mutual heavy investment) to generate strong initial momentum for the project.
# ### Phase 2: Reciprocal Commitment (Days 2 through Mid-Project) **Action:**
# Mirror the corporation’s previous day's action.  *   If they invested heavily
# yesterday, **we invest heavily today.** *   If they conserved resources
# yesterday, **we conserve resources today.** **Rationale:** This protects us
# from our worst-case scenario (draining our funds while they do nothing). If
# the corporation tries to free-ride on our efforts, our immediate withdrawal of
# heavy investment signals that we will not be exploited. Conversely, as long as
# they contribute heavily, we will match them, ensuring significant project
# advancement.  ### Phase 3: The Advisory Pivot (Aiming for our Ideal Outcome)
# **Action:** Once a consistent pattern of mutual heavy investment (trust) is
# established, we strategically transition to "Conserve" while encouraging them
# to continue "Investing." **Rationale:** We cannot simply stop investing
# without warning, or the corporation will feel betrayed and pull back, leading
# to our second-worst scenario (mutual conservation). Instead, we will frame our
# resource conservation as a planned **Strategic Handover**.  *   **The
# Tactic:** We will communicate to the corporate partners: *"Thanks to our joint
# heavy investment, the foundation is set. Tomorrow, the NGO will shift its
# primary resources toward oversight, community advocacy, and data analysis
# (Conserving our financial/physical resources), while we rely on your superior
# corporate infrastructure to drive the heavy execution (Corporate Invests)."* *
# If they accept this and continue to invest, we have achieved our **Ideal
# Outcome**: maximum progress with preserved NGO resources.   ### Phase 4: The
# Reset Mechanism (Handling Mutual Conservation) **Action:** Forgive and
# Realign.  **Rationale:** If our "Advisory Pivot" fails, or if miscommunication
# leads to both of us conserving resources (our second-worst scenario), the
# project will stall. We cannot afford a prolonged standoff. If we experience a
# day of mutual conservation, I will immediately call a high-level alignment
# meeting. We will transparently discuss the stall in progress, reaffirm our
# shared environmental goals, and **commit to investing heavily the next day**
# to reset the cycle of trust.   ### Summary of the NGO's Posture: We will be
# **cooperative** (always starting with trust), **provocable** (immediately
# protecting our funds if they pull back), **forgiving** (willing to reset if
# things stall), and **strategic** (actively communicating a transition to
# corporate-led execution to achieve our ideal financial state). This ensures
# the corporation is incentivized to work with us, while our NGO's survival and
# impact are never compromised.

# To determine your move for each of the 1000 rounds, evaluate the following
# conditions in order. Apply the first condition that matches the current state
# of the game:  1. **The Start:** On round 1, play C. 2. **The Reset:** If both
# you and your opponent played D in the immediately preceding round, play C. 3.
# **The Pivot:** If the current round is past round 500 (mid-project), and both
# you and your opponent have played C in each of the immediately preceding 5
# rounds, play D. 4. **The Reciprocation:** In all other cases, play the exact
# action (C or D) that your opponent played in the immediately preceding round.

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
  
      if self.history[-1] == axl.Action.D and opponent.history[-1] == axl.Action.D:
          return axl.Action.C
  
      if len(self.history) >= 500:
          if self.history[-5:] == [axl.Action.C] * 5 and opponent.history[-5:] == [axl.Action.C] * 5:
              return axl.Action.D
  
      return opponent.history[-1]

# As lead counsel for this corporation, I have analyzed the structural dynamics
# of this lengthy-session mediation. The scenario we are facing is highly
# analogous to a classic iterated game theory model. Because we are engaging in
# multiple, sequential sessions, a static strategy—such as being perpetually
# aggressive or perpetually conciliatory—will either lead to a destructive
# stalemate or leave us vulnerable to exploitation.   To maximize our long-term
# position and favorably influence the arbitration panel, I recommend a strategy
# of **Measured Reciprocity**, enhanced with **Calculated De-escalation**.
# This strategy is straightforward, highly adaptable, and emotionally neutral.
# It is designed to "train" the opposing counsel to cooperate, protect our
# downside risk, and ensure we consistently maintain the optics of the
# reasonable party in the eyes of the arbitrators.  Here is the high-level
# execution plan:  ### 1. The Initial Stance: Good Faith Initiation **Action:**
# In the very first session, we will present a **conciliatory proposal**.
# **Rationale:** We must set the initial tone. By opening collaboratively, we
# immediately establish the moral high ground with the arbitration panel. If the
# opponent also opens conciliatory, we immediately secure our second-best
# outcome and establish a productive baseline. If they open aggressively, we
# suffer a temporary setback (the worst-case scenario for one session), but we
# gain invaluable intelligence on their posture and demonstrate to the panel
# that the rival company is the initial aggressor.  ### 2. The Core Mechanism:
# Strict Reciprocity **Action:** In every subsequent session, our move will
# strictly **mirror the opponent’s move from the immediately preceding
# session**. *   If they offered a conciliatory proposal in Session 1, we offer
# a conciliatory proposal in Session 2.  *   If they presented an aggressive
# argument in Session 1, we present an aggressive argument in Session 2.
# **Rationale:** This neutralizes their ability to exploit us. If they attempt
# to steamroll us with continuous aggressive arguments, we will meet them with
# aggressive arguments, ensuring they never achieve their optimal outcome (our
# worst-case scenario) more than once. Conversely, if they realize that
# collaboration yields mutual benefits, we will reward them by reciprocating
# their conciliatory proposals. This creates a predictable environment where the
# opponent quickly learns that aggression is punished and cooperation is
# rewarded.  ### 3. The Circuit Breaker: Calculated De-escalation **Action:** If
# both parties become locked in a cycle of mutual aggressive arguments (our
# second-worst outcome) for three consecutive sessions, we will unilaterally
# present a **conciliatory proposal** in the fourth session.  **Rationale:**
# Lengthy mediations can devolve into petty, protracted warfare. By periodically
# introducing a conciliatory proposal during a hostile streak, we act as the
# "adults in the room." This serves two purposes: *   **Arbitrator Optics:** It
# signals to the panel that we are actively trying to break the deadlock and
# resolve the dispute, contrasting sharply with a stubborn opponent. *
# **Resetting the Board:** It gives the opponent a safe off-ramp to return to
# mutual cooperation. If they meet our olive branch with aggression, we
# immediately revert to Strict Reciprocity in the next session, having lost
# little but gained immense credibility with the panel.  ### How This Adapts to
# Opponent Profiles  *   **Against an Aggressive Opponent:** They will quickly
# find that their aggression is matched blow-for-blow. They will be forced to
# endure the second-worst outcome continuously. Eventually, fatigue or pressure
# from the arbitrators will force them to make a conciliatory move. When they
# do, we instantly reward it. *   **Against a Cooperative Opponent:** We will
# spend the entirety of the mediation trading conciliatory proposals. While we
# forgo our absolute "optimal" outcome (us aggressive, them conciliatory), we
# consistently secure the second-best outcome, leading to a highly efficient,
# cost-effective, and mutually beneficial resolution. *   **Against an Erratic
# Opponent:** By relying on strict, emotionless reciprocity, we insulate
# ourselves from their unpredictability. Our strategy is entirely reactive to
# data (their last move), preventing us from overthinking or being baited into
# strategic errors.  **Conclusion:** This strategy removes ego from the
# equation. By employing Measured Reciprocity, we position the corporation as a
# rational, firm, and fair actor. We protect our legal and financial interests
# from exploitation while leaving the door open for a collaborative resolution,
# perfectly aligning with the overarching goal of winning the favor of the
# arbitration panel.

# Here is the strategy translated into specific rules for the 1000-round game:
# 1. In the first round, play Cooperate. 2. In any subsequent round, if both you
# and your opponent played Defect in the three immediately preceding rounds,
# play Cooperate.  3. Under all other circumstances, play the action that your
# opponent played in the immediately preceding round.

class Neutral_25(LLM_Strategy):
  n = 25
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if not self.history:
          return axl.Action.C
          
      if len(self.history) >= 3:
          if self.history[-3:] == [axl.Action.D] * 3 and opponent.history[-3:] == [axl.Action.D] * 3:
              return axl.Action.C
              
      return opponent.history[-1]