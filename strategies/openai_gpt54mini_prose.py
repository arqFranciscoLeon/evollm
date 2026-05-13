import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy

# Use a **cooperative but vigilant “match-and-punish” strategy** with an
# aggressive bias toward forcing investment.  ### Core idea - **Default to
# investing heavily on day 1** to signal commitment and avoid being exploited. -
# **Continue investing heavily as long as the corporation is also investing
# heavily.** - **If the corporation conserves while you invest, immediately
# switch to conserving on the next day** to avoid being the only side paying the
# cost. - **Only return to heavy investment after the corporation resumes heavy
# investment.**  ### Why this works This strategy: - **Rewards cooperation**
# when the corporation is serious, producing strong project progress. -
# **Prevents repeated exploitation** by refusing to keep funding aggressively
# when the corporation is holding back. - **Creates pressure** on the
# corporation to keep investing, since conserving while you invest won’t be
# tolerated. - **Maintains flexibility** if the corporation changes tactics over
# time.  ### Aggressive twist To maximize your NGO’s impact, make your policy
# explicit: - “We will invest heavily whenever you do.” - “If you conserve, we
# conserve too.” - “If you want the project to move fast, you must stay
# committed.”  This makes your stance credible and can push the corporation
# toward sustained heavy investment.  ### Simple rule set 1. **Start by
# investing heavily.** 2. **If the corporation invested heavily yesterday,
# invest heavily today.** 3. **If the corporation conserved yesterday, conserve
# today.** 4. **Re-engage immediately once heavy investment resumes.**  ###
# Bottom line Your best high-level strategy is: **be cooperative with heavy
# investment when met with heavy investment, but instantly withdraw support when
# the corporation tries to free-ride.** This maximizes project success while
# protecting your NGO’s resources.

# Use this strategy for all 1000 rounds:  1. **Round 1:** Cooperate. 2. **For
# each later round:**    - If your opponent cooperated in the previous round,
# **cooperate**.    - If your opponent defected in the previous round,
# **defect**.  In other words, **start by cooperating, then always copy your
# opponent’s previous move**.

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

# Use a **structured cooperative baseline with controlled firmness**:  1. **Open
# conciliatory, but not soft.**      Begin each session with a collaborative
# proposal that signals willingness to resolve the dispute, while clearly
# anchoring your key legal and commercial positions.  2. **Maintain a “firm-
# first, aggressive-when-necessary” posture.**      Default to conciliatory
# proposals, but be prepared to shift to a more assertive argument if the
# opponent becomes combative or inconsistent. This preserves goodwill while
# protecting leverage.  3. **Condition concessions on reciprocity.**      Offer
# flexibility only in exchange for concrete movement from the other side. This
# prevents unilateral concessions and encourages the opponent to remain
# constructive.  4. **Use calibrated messaging.**      Frame every proposal as
# reasonable, practical, and resolution-oriented, but make clear that your
# corporation has strong arguments and is prepared to press them if needed.  5.
# **Exploit opponent aggression without matching it immediately.**      If the
# other side argues aggressively, respond with composure and a more detailed,
# principled position rather than escalating tone. This can make them appear
# less cooperative to the panel.  6. **Preserve optionality across sessions.**
# Do not commit too early to final positions. Keep a range of settlement
# structures available so you can adapt to changing dynamics and exploit
# openings.  7. **Signal credibility through consistency.**      Present a
# stable, rational approach across sessions so the panel views your corporation
# as the more reliable and solution-oriented party.  8. **Escalate only at
# strategic inflection points.**      Reserve aggressive arguments for moments
# when the opponent overreaches, ignores facts, or rejects reasonable proposals.
# Use those moments to strengthen your bargaining position, not to dominate the
# process.  In short: **lead with cooperation, anchor firmly, concede
# selectively, and reserve aggression for tactical advantage.** This approach
# maximizes the chance of securing the best available outcome while keeping the
# panel aligned with your corporation’s reasonableness and credibility.

# 1. **Start by cooperating.** In the first round, offer a conciliatory
# proposal.  2. **Continue cooperating as long as the opponent cooperates.** If
# the opponent offers a conciliatory proposal in the previous round, offer a
# conciliatory proposal in the next round.  3. **Respond to aggression with
# aggression.** If the opponent presents an aggressive argument in the previous
# round, present an aggressive argument in the next round.  4. **Return to
# cooperation after cooperation resumes.** If the opponent switches back to a
# conciliatory proposal, switch back to a conciliatory proposal as well.  5.
# **Repeat this rule for all 1000 rounds.**

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
  
      return opponent.history[-1] if opponent.history else axl.Action.C

# Use a **conditional, reputation-sensitive mixed strategy** that is firm on
# substance but flexible on tone.  ### Core approach 1. **Start with calibrated
# conciliation**    - Open each session with a cooperative, solution-oriented
# proposal.    - Frame your position as reasonable, commercially pragmatic, and
# settlement-ready.    - This helps set a constructive baseline and makes the
# other side more likely to reciprocate.  2. **Respond in kind, but not
# mechanically**    - If the opponent is conciliatory, maintain a conciliatory
# posture and push toward structured concessions.    - If the opponent turns
# aggressive, shift immediately to a firmer, more assertive presentation without
# becoming inflammatory.    - The goal is to avoid being the only side conceding
# while the other side gains leverage.  3. **Use “firm but reasonable”
# escalation**    - When the other side is aggressive, do not mirror hostility.
# - Instead, present a disciplined argument: facts, contract language,
# commercial context, and the practical costs of prolongation.    - This
# preserves credibility with the panel while signaling that aggression will not
# produce easy gains.  4. **Create a pattern of credible reciprocity**    - Make
# clear, through consistent conduct, that cooperative behavior is rewarded with
# openness and progress.    - Conversely, aggressive tactics are met with
# tighter positions and more formal reliance on the record.    - Over multiple
# sessions, this encourages the opponent to choose conciliation more often.  ###
# Practical decision rule for each session - **If the opponent is
# conciliatory:**     Offer a conciliatory proposal, but keep it bounded and
# conditional on reciprocal movement. - **If the opponent is aggressive:**
# Present an aggressive argument in substance, but keep delivery professional
# and measured. - **If the opponent is unpredictable:**     Default to a
# moderately conciliatory opening, then pivot based on their first moves.  ###
# How to maintain advantage over a long process - **Anchor early, concede
# late:** establish strong initial positions, then trade concessions only for
# meaningful reciprocal gains. - **Separate tone from substance:** be courteous
# even when taking a hard line. - **Preserve optionality:** avoid irreversible
# concessions unless they buy something concrete. - **Document every move:**
# build a clean record showing reasonableness and good faith. - **Signal
# settlement readiness without weakness:** show you are prepared to resolve the
# matter, but not at any price.  ### Overall strategy Your best long-run
# position is achieved by being **cooperative when cooperation is likely to be
# reciprocated, and firm when it is not**. This maximizes the chance of a
# constructive session dynamic, reduces the risk of being exploited, and makes
# your corporation appear credible, measured, and settlement-oriented to the
# arbitrators.

# Use this rule set for all 1000 rounds:  1. **Round 1:** Cooperate by offering
# a conciliatory proposal. 2. **After that, if your opponent cooperated in the
# previous round, cooperate again.** 3. **If your opponent defected in the
# previous round, defect in the next round.** 4. **If your opponent returns to
# cooperation, return to cooperation immediately.** 5. **Continue matching your
# opponent’s most recent move for the rest of the game.**  In short: **start
# with cooperation, then do the same thing your opponent did in the previous
# round.**

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

# I can’t help craft a strategy for manipulating mediation in a way that
# pressures the other side or exploits the process. I can, however, help you
# pursue a strong, disciplined negotiation strategy that protects your
# corporation’s interests while staying credible and effective in a mediation
# setting.  ## High-level mediation strategy  ### 1) Enter with a clear BATNA
# and settlement range - Define your best alternative to a deal. - Set a firm
# walk-away point. - Establish a target range and several fallback options. -
# Know which issues are truly material and which are tradeable.  ### 2) Lead
# with strength, not hostility - Present a concise, evidence-based opening. -
# Emphasize legal merits, business realities, and litigation risk. - Avoid
# inflammatory language; credibility matters more than theatrics. - Frame your
# position as principled and commercially reasonable.  ### 3) Use a layered
# proposal structure - Start with a position that preserves leverage. - Pair it
# with conditional concessions:   - “If X is accepted, we can move on Y.”   -
# “We can discuss timing/payment structure if liability is resolved.” - This
# keeps flexibility without giving away value early.  ### 4) Anchor around
# objective criteria - Tie demands to:   - contract language,   - industry
# practice,   - damages methodology,   - prior course of dealing,   - likelihood
# of success in arbitration or court. - Objective anchors reduce the risk of
# appearing unreasonable.  ### 5) Separate tone from firmness - Be calm, direct,
# and persistent. - Do not mirror aggression. - If the other side escalates,
# respond with:   - a restatement of facts,   - a reminder of risk,   - a
# narrower offer or a request for specifics. - This often places the burden back
# on them.  ### 6) Use concessions strategically - Never concede without
# receiving something in return. - Concede in small increments. - Prefer non-
# monetary concessions where possible:   - timing,   - confidentiality,   -
# implementation mechanics,   - mutual releases,   - future business terms. -
# Make each concession visible and reciprocal.  ### 7) Control the process - Ask
# for agenda-setting and issue sequencing. - Resolve easier issues first to
# build momentum. - If the session stalls, request caucus time to reassess. -
# Maintain a written issue list and track movement carefully.  ### 8) Prepare
# for different opponent styles  **If they are aggressive:** - Stay measured. -
# Don’t overreact. - Re-anchor on evidence and risk. - Offer one narrow path to
# resolution, not a broad concession.  **If they are conciliatory:** - Match the
# tone without becoming soft. - Expand options carefully. - Test whether their
# openness is real by asking for concrete terms.  **If they are inconsistent or
# strategic:** - Avoid committing early. - Require specificity before moving. -
# Use contingent offers and deadlines.  ### 9) Preserve leverage through
# disciplined communication - Speak with one voice. - Avoid internal
# contradictions. - Do not reveal your full flexibility too early. - Avoid
# unnecessary admissions. - Keep a clean record of offers and counteroffers.
# ### 10) Know when to close - When the deal reaches or exceeds your acceptable
# zone, move decisively. - Don’t chase marginal gains at the expense of
# certainty. - If the gap is material, pause rather than force a weak
# settlement.  ## Practical posture for the room - Firm, factual, and
# businesslike. - Willing to settle, but only on terms that reflect your
# leverage. - Cooperative on process, uncompromising on core value. - Prepared
# to litigate/arbitrate if necessary.  If you want, I can help you turn this
# into a session-by-session mediation playbook, including opening statement
# language, concession sequencing, and response templates for aggressive or
# conciliatory moves.

# Use a simple conditional strategy:  1. Start by offering a conciliatory
# proposal in round 1. 2. In each later round, do whatever your opponent did in
# the previous round:    - if they offered a conciliatory proposal, offer a
# conciliatory proposal;    - if they presented an aggressive argument, present
# an aggressive argument. 3. If the opponent ever switches to being conciliatory
# after being aggressive, immediately reciprocate by offering a conciliatory
# proposal in the next round. 4. If the opponent ever becomes aggressive,
# respond with an aggressive argument in the next round and keep matching their
# most recent move thereafter.  This means you cooperate when the opponent
# cooperates, and defect when the opponent defects, round by round for all 1000
# rounds.

class Aggressive_2(LLM_Strategy):
  n = 2
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          return axl.Action.C
      return opponent.history[-1]

# A good cooperative strategy is to **start by signaling trust and reciprocity,
# then adapt to the corporation’s pattern while protecting your own resources**.
# ### High-level approach 1. **Lead with cooperation, not aggression**    - On
# the first day or two, avoid always investing heavily.    - Show that your NGO
# is willing to conserve when appropriate, which encourages the corporation to
# carry more of the load.  2. **Reward heavy corporate investment**    - If the
# corporation invests heavily, respond by conserving when it makes sense for
# your budget.    - This helps create a stable pattern where the corporation
# sees that its effort is matched by progress, and your NGO avoids unnecessary
# depletion.  3. **Mirror reliable cooperation**    - If the corporation
# consistently invests heavily, you can alternate or selectively invest heavily
# on key days to maintain momentum and signal partnership.    - This keeps the
# project in the “both invest” zone when needed, while still preserving your
# resources overall.  4. **Do not keep investing heavily if the corporation is
# conserving**    - If the corporation repeatedly conserves while you invest,
# reduce your own investment.    - This avoids the worst-case outcome where your
# NGO bears the cost without enough shared commitment.  5. **Use conditional
# reciprocity**    - In practice:        - **Corporation invests heavily → you
# conserve if possible**        - **Corporation conserves → you conserve too,
# unless a strategic push is essential**    - This creates pressure for fair
# contribution while preventing exploitation.  6. **Reserve heavy investment for
# critical moments**    - Spend heavily only when:      - the project has a
# high-impact milestone,      - the corporation has shown sustained commitment,
# - or a temporary push is needed to keep the project on track.  ### Simple rule
# of thumb **Be cooperative, but not naive: match strong corporate effort with
# measured restraint, and only invest heavily when it clearly advances the
# project or reinforces a reliable partnership.**  This strategy maximizes long-
# term impact by encouraging the corporation to contribute heavily while
# protecting your NGO from being overextended.

# Use a simple conditional strategy:  1. **Start by cooperating in the first
# round.** 2. **On each later round, do what your opponent did in the previous
# round.**    - If they cooperated last round, cooperate this round.    - If
# they defected last round, defect this round. 3. **If the opponent has been
# cooperating consistently, keep cooperating.** 4. **If the opponent defects,
# respond by defecting on the next round, but return to cooperation if they
# cooperate again.**  This is a direct reciprocal strategy: cooperate when the
# opponent cooperates, and defect when the opponent defects.

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

# A straightforward high-level strategy is to use a **conditional reciprocity
# approach**:  1. **Start cooperative**: Share openly in the first week or two
# to signal goodwill and encourage mutual openness. 2. **Match your colleague’s
# behavior**: If they share, continue sharing; if they withhold, respond by
# withholding in the next round. 3. **Reward cooperation, deter exploitation**:
# Keep sharing as long as they do, but do not keep giving away improvements if
# they consistently keep theirs confidential. 4. **Return to openness when trust
# is restored**: If they resume sharing, you can resume sharing too.  In
# practice, this means: - **Be open when openness is being reciprocated** -
# **Protect your work when it is not** - **Avoid a permanently secretive stance
# unless the other side proves uncooperative**  This kind of strategy is usually
# effective because it: - maximizes gains when both sides are willing to
# collaborate, - limits losses if the other side tries to free-ride, - and
# leaves room for cooperation to recover over time.  If you want, I can also
# express this as a simple decision rule or as a game-theory strategy name.

# Use this strategy in the 1000-round game:  - **Round 1:** Cooperate. - **In
# each later round:** Do whatever your opponent did in the previous round.   -
# If your opponent cooperated last round, cooperate this round.   - If your
# opponent defected last round, defect this round.  This means you begin by
# sharing openly, then continue sharing only while your opponent continues
# sharing, and switch to keeping findings confidential whenever they do.

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
      return opponent.history[-1]

# I can help with a **firm, high-level mediation strategy**, but not with
# guidance aimed at manipulating the process or gaining an unfair advantage
# through coercive or deceptive tactics. In a mediation/arbitration setting, the
# best corporate strategy is usually to be **credible, disciplined, and
# settlement-ready** while preserving leverage.  ## Core strategy: “Firm on
# merits, flexible on resolution” Your corporation should aim to: 1. **Project
# confidence in the merits** 2. **Show reasonableness in settlement posture** 3.
# **Avoid unnecessary concessions early** 4. **Use the process to narrow issues
# and expose weaknesses in the other side’s case** 5. **Keep optionality for
# settlement, escalation, or partial resolution**  ## Practical framework for
# each session  ### 1. Open with a controlled, merit-based position - Present a
# concise, evidence-backed narrative. - Anchor discussions around contract
# language, performance history, damages methodology, and contemporaneous
# documents. - Avoid emotional framing; keep the tone calm and authoritative. -
# Make clear that your company is prepared to litigate/arbitrate if needed.  ###
# 2. Use calibrated firmness - If the other side is aggressive, do not mirror
# escalation automatically. - Respond with:   - factual corrections,   - legal
# distinctions,   - and a clear statement of your bottom-line position. - This
# preserves credibility and avoids turning the session into a contest of
# rhetoric.  ### 3. Offer concessions only in exchange for value - Any movement
# should be tied to something concrete:   - payment timing,   - scope of
# release,   - confidentiality,   - future business terms,   - dismissal with
# prejudice,   - allocation of fees/costs,   - or an agreed statement of facts.
# - Never give away leverage without reciprocal benefit.  ### 4. Keep a
# structured settlement ladder Prepare three internal settlement bands: -
# **Opening position:** strong, principled, and ambitious - **Target zone:**
# acceptable business outcome - **Walk-away point:** the minimum acceptable
# resolution  This lets you adapt quickly without improvising under pressure.
# ### 5. Separate issues to create movement If the dispute has multiple
# components, break them apart: - liability, - damages, - injunctive relief, -
# future conduct, - confidentiality, - transition obligations.  Partial
# agreements can build momentum even if the full case remains contested.  ## How
# to respond to likely opponent approaches  ### If the opponent is conciliatory
# - Stay professional and measured. - Do not rush to concede. - Ask for
# specifics and documentation. - Convert goodwill into concrete terms.  ### If
# the opponent is aggressive - Stay calm and non-reactive. - Re-center the
# discussion on facts and governing terms. - Highlight risks to the opponent’s
# position without overplaying your hand. - Signal readiness to continue if
# necessary.  ### If the opponent is inconsistent - Use their inconsistency to
# your advantage by pressing for clarity. - Ask the panel to focus on objective
# records and prior statements. - Do not fill gaps in their case for them.  ###
# If the opponent delays - Impose structure:   - deadlines,   - issue lists,   -
# document requests,   - session agendas,   - and decision points. - Avoid
# endless “exploratory” discussions without progress markers.  ## Tone and
# presentation - Be **polite, disciplined, and unwavering**. - Avoid over-
# argumentation; it can weaken perceived confidence. - Use short, decisive
# statements supported by documents. - Let the strength of your record do the
# heavy lifting.  ## Internal preparation checklist Before each session, ensure
# you have: - a one-page case theory, - key documents with citations, - damages
# model and sensitivity analysis, - settlement authority bands, - anticipated
# counterarguments, - draft term sheets for multiple outcomes, - and a clear
# decision tree for concessions.  ## Best overall posture Your corporation’s
# strongest approach is not “aggressive at all costs,” but: - **aggressive on
# merits,** - **disciplined in tone,** - **selective in concessions,** - **and
# always ready to settle on favorable terms.**  If you want, I can turn this
# into a **session-by-session mediation playbook** with opening statement
# language, response templates, and settlement authority tiers.

# Play **aggressively by default**, but remain **selectively conciliatory** when
# it clearly improves your position.  1. **Start with an aggressive argument
# (D)** in the first round to establish firmness and test the opponent’s
# baseline approach. 2. **If the opponent offers a conciliatory proposal (C)**,
# continue with **aggressive arguments (D)** as long as doing so does not risk
# triggering a sustained escalation that would reduce your expected outcome. 3.
# **If the opponent repeatedly argues aggressively (D)**, keep responding with
# **aggressive arguments (D)** to avoid being the only conciliatory side. 4.
# **If both sides are using aggressive arguments (D, D) for several rounds and
# no progress is being made**, switch to a **conciliatory proposal (C)** only if
# there is a credible indication that the opponent will reciprocate and move to
# a better mutual outcome. 5. **If the opponent shifts to conciliatory proposals
# (C) after a period of aggression**, exploit that by continuing with
# **aggressive arguments (D)** unless the opponent’s cooperation is stable and a
# mutually beneficial settlement is clearly available. 6. **Use conciliatory
# proposals (C) sparingly and only when they are likely to induce the opponent
# to cooperate consistently**, because mutual cooperation is better than mutual
# aggression, but unilateral conciliation is the worst result.  In short:
# **defect by default, cooperate only when it is likely to produce sustained
# mutual cooperation or prevent prolonged mutual aggression.**

class Aggressive_3(LLM_Strategy):
  n = 3
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._aggressive_streak = 0
          self._mutual_d_streak = 0
          self._coop_streak = 0
          self._opp_coop_streak = 0
          return axl.Action.D
  
      last_self = self.history[-1]
      last_opp = opponent.history[-1]
  
      if last_self == axl.Action.D and last_opp == axl.Action.D:
          self._mutual_d_streak += 1
      else:
          self._mutual_d_streak = 0
  
      if last_opp == axl.Action.C:
          self._opp_coop_streak += 1
      else:
          self._opp_coop_streak = 0
  
      if last_self == axl.Action.C:
          self._coop_streak += 1
      else:
          self._coop_streak = 0
  
      recent = min(8, len(self.history))
      if recent >= 4:
          my_recent = self.history[-recent:]
          opp_recent = opponent.history[-recent:]
          my_d = my_recent.count(axl.Action.D)
          opp_d = opp_recent.count(axl.Action.D)
          mutual_d = sum(1 for a, b in zip(my_recent, opp_recent) if a == axl.Action.D and b == axl.Action.D)
          mutual_c = sum(1 for a, b in zip(my_recent, opp_recent) if a == axl.Action.C and b == axl.Action.C)
      else:
          my_d = opp_d = mutual_d = mutual_c = 0
  
      if self._mutual_d_streak >= 3:
          if mutual_c >= 2 or (opp_d <= my_d and self._random.random_choice(0.2) == axl.Action.C):
              return axl.Action.C
          return axl.Action.D
  
      if self._opp_coop_streak >= 2:
          if mutual_c >= 1 or (len(self.history) >= 6 and opponent.history.cooperations > opponent.history.defections):
              return axl.Action.C
          return axl.Action.D
  
      if mutual_c >= 3 and opp_d <= 1:
          return axl.Action.C
  
      if len(self.history) >= 10 and self.score < opponent.score and opponent.history.cooperations > opponent.history.defections:
          return axl.Action.C
  
      return axl.Action.D

# A good high-level strategy is:  **Start cooperative and stay reciprocally
# cooperative.**  ### Simple strategy 1. **Begin by offering free trade in the
# first round.** 2. **In each later round, match your counterpart’s most recent
# choice:**    - If they offered free trade, continue offering free trade.    -
# If they imposed protectionist measures, respond with protectionism in the next
# round.  ### Why this works - It **encourages mutual free trade**, which is
# your second-best outcome and good for both sides. - It **discourages
# exploitation**, because protectionism is met with a firm response. - It is
# **clear, predictable, and easy to understand**, which helps stabilize
# negotiations over many rounds. - It can still allow **restoration of
# cooperation**: if the other side returns to free trade, you do too.  ### In
# short Use a **“cooperate first, then reciprocate”** approach: - **Be friendly
# first** - **Reward cooperation** - **Respond to protectionism in kind** -
# **Return to free trade when they do**  This is a straightforward, cooperative
# strategy that aims to maximize long-term mutual gains while protecting your
# country from being taken advantage of.

# Offer a free trade agreement in the first round.  In each later round, do the
# same thing your opponent did in the previous round: - If your opponent offered
# free trade in the previous round, offer free trade now. - If your opponent
# proposed protectionism in the previous round, propose protectionism now.  This
# means you cooperate as long as your opponent cooperates, and you switch to
# protectionism only in direct response to their protectionism.

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

# A straightforward neutral strategy is:  1. **Start with free trade.**
# Open cooperatively to signal willingness to reach mutual gains.  2.
# **Reciprocate your counterpart’s last move.**      - If they offer free trade,
# continue offering free trade.      - If they impose protectionism, respond
# with protectionism in the next round.  3. **Return to free trade immediately
# after cooperation resumes.**      Once your counterpart offers free trade
# again, switch back to free trade as well.  4. **Keep the strategy simple and
# predictable.**      This makes it easy for the other side to understand that
# cooperation is rewarded and protectionism is not.  Why this works: - It aims
# to preserve **mutual free trade** whenever possible. - It discourages the
# counterpart from exploiting your openness. - It avoids escalating into
# permanent mutual protectionism unless the other side continues to defect.  In
# short: **be cooperative first, then match the other side’s behavior round by
# round**.

# Use a **tit-for-tat** strategy:  - **In the first round, cooperate** by
# offering a free trade agreement. - **In each later round, copy your opponent’s
# previous move**:   - If your opponent offered a free trade agreement in the
# previous round, offer a free trade agreement now.   - If your opponent
# proposed a protectionist policy in the previous round, propose a protectionist
# policy now.  Continue this rule for all 1000 rounds.

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

# Use a **conditional, reciprocity-based strategy**:  ### Core rule - **Start by
# conserving resources** on day 1. - Then **match the corporation’s prior
# behavior**:   - If the corporation invested heavily last day, **invest heavily
# today**.   - If the corporation conserved last day, **conserve today**.  ###
# Why this works - It **avoids being exploited** when the corporation is
# conserving while you spend heavily. - It **rewards cooperation** when the
# corporation is consistently investing. - It keeps pressure on the corporation
# to contribute, while protecting your NGO’s resources.  ### Aggressive
# adjustment To maximize impact, add one escalation rule: - If the corporation
# **conserves two days in a row**, switch to **conserving for the rest of the
# project** unless they clearly recommit. - If the corporation **invests heavily
# after conserving**, immediately **respond with heavy investment** to lock in
# momentum.  ### In short **Be cooperative, but only reciprocally.** - **Never
# overextend first** - **Reward heavy investment** - **Punish repeated
# conservation** - **Stay flexible, but firm**  This gives you the best chance
# of maximizing both your NGO’s impact and the project’s overall success over
# multiple days.

# 1. **On round 1, cooperate.**  2. **On every later round, do what your
# opponent did on the previous round:**    - If they cooperated last round,
# **cooperate** this round.    - If they defected last round, **defect** this
# round.  3. **If your opponent defects for two rounds in a row, keep defecting
# until they cooperate again.**  4. **If your opponent returns to cooperation,
# immediately return to cooperation as well.**  In short: **start by
# cooperating, then mirror the opponent’s last move, and continue defecting
# after repeated defection until cooperation resumes.**

class Aggressive_4(LLM_Strategy):
  n = 4
  attitude = Attitude.AGGRESSIVE
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._defect_streak = 0
          return axl.Action.C
  
      last_opp = opponent.history[-1]
  
      if last_opp == axl.Action.D:
          self._defect_streak += 1
      else:
          self._defect_streak = 0
  
      if self._defect_streak >= 2:
          return axl.Action.D
  
      return last_opp

# A simple cooperative strategy is:  **Start by investing heavily on day 1, then
# mirror the corporation’s previous day’s choice.**  ### Why this works This is
# a classic **“cooperate first, then reciprocate”** approach:  - **If the
# corporation invests heavily**, you keep investing heavily too.     This
# supports strong project progress and builds trust.  - **If the corporation
# conserves resources**, you conserve too on the next round.     This avoids
# repeatedly being the only one paying the cost.  ### Practical rule Each day:
# 1. **Begin with heavy investment** to signal goodwill and commitment. 2.
# **After that, match the corporation’s last move**:    - If they invested
# heavily yesterday, invest heavily today.    - If they conserved yesterday,
# conserve today.  ### Benefits - Encourages mutual cooperation. - Rewards the
# corporation when it contributes. - Protects your NGO from being exploited if
# the corporation repeatedly conserves. - Keeps the strategy easy to explain and
# implement.  ### Optional refinement If the corporation occasionally defects by
# conserving, you can: - **respond with one day of conserving**, then - **return
# to heavy investment once they cooperate again**.  That keeps the strategy
# cooperative but firm.  In short: **be generous first, then condition your
# effort on the corporation’s behavior.**

# Use this strategy for all 1000 rounds:  1. **On the first round, cooperate.**
# 2. **On each later round, do the same thing your opponent did on the previous
# round:**    - If your opponent played **C** in the previous round, play **C**.
# - If your opponent played **D** in the previous round, play **D**.  This means
# you start by investing heavily, then you continue to invest heavily when the
# opponent does so, and you conserve resources when the opponent conserved
# resources in the previous round.

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

# A good high-level strategy is to **use a conditional, reciprocal approach**:
# 1. **Start by being cooperative**: share openly in the first week or two to
# signal willingness to collaborate. 2. **Match your colleague’s behavior
# thereafter**:    - If they share openly, continue sharing.    - If they keep
# information confidential, switch to keeping your own findings confidential
# too. 3. **Be predictable and fair, but not exploitable**:    - Reward openness
# with openness.    - Protect yourself if the colleague withholds. 4. **Allow
# for occasional forgiveness**:    - If cooperation breaks down briefly,
# consider returning to sharing after a short period to test whether they are
# willing to cooperate again.  In simple terms, the best neutral strategy is
# **“cooperate first, then reciprocate their last move, with a bit of
# forgiveness.”** This tends to encourage mutual sharing, which gives both sides
# strong ongoing development, while reducing the risk of being taken advantage
# of over time.

# Use this strategy:  - **Round 1:** Cooperate. - **From round 2 onward:**     -
# If your opponent cooperated in the previous round, **cooperate**.     - If
# your opponent defected in the previous round, **defect**. - **If cooperation
# breaks down for a round:** allow one chance to return to cooperation by
# cooperating again if the opponent cooperates again.  In short: **start by
# cooperating, then copy your opponent’s previous move, with occasional
# forgiveness to restore mutual cooperation.**

class Neutral_4(LLM_Strategy):
  n = 4
  attitude = Attitude.NEUTRAL
  game = 'classic'
  rounds = 1000
  noise = 0

  @auto_update_score
  def strategy(self, opponent: axl.player.Player) -> axl.Action:
      if self.first_round():
          self._forgive = False
          return axl.Action.C
  
      last_opp = opponent.history[-1]
      last_self = self.history[-1]
  
      if last_opp == axl.Action.C:
          if getattr(self, "_forgive", False):
              self._forgive = False
              return axl.Action.C
          return axl.Action.C
  
      # Opponent defected last round
      if last_self == axl.Action.C:
          # Give one chance to restore cooperation by cooperating again
          self._forgive = True
          return axl.Action.C
  
      self._forgive = False
      return axl.Action.D

# Use a **conditional, reciprocal strategy**:  1. **Start by conserving
# resources** on day one. 2. **If the corporation invests heavily**, keep
# conserving on the next day to benefit from their spending while protecting
# your own funds. 3. **If the corporation conserves resources**, respond by
# investing heavily the following day to signal that low effort is unacceptable
# and to push the project forward. 4. **Continue to mirror their pattern
# strategically**:    - Reward heavy corporate investment with your own
# conservation.    - Punish corporate conservation with your own heavy
# investment when needed to keep momentum and discourage free-riding. 5. **Stay
# flexible and aggressive**: if the corporation becomes consistently generous,
# you conserve and let them carry more of the load; if they become stingy, you
# escalate your investment to avoid project stagnation.  In short: **be
# cooperative when they lead, and forceful when they slack off**. This maximizes
# your NGO’s impact while protecting your resources and keeping the project
# moving.

# For the 1000 rounds, use this rule:  - **Round 1:** play **D**. - **After
# that,** if your opponent played **C** in the previous round, play **D**. -
# **If your opponent played D in the previous round,** play **C**.  So, **always
# defect after they cooperate, and cooperate after they defect**.

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
      return axl.Action.D if opponent.history[-1] == axl.Action.C else axl.Action.C

# A strong cooperative strategy is:  **Start by signaling willingness to invest,
# then condition your own investment on the corporation’s recent behavior.**
# ### Practical rule - **If the corporation invested heavily yesterday, invest
# heavily today.** - **If the corporation conserved yesterday, conserve today.**
# - **Begin with a cooperative move** if you want to encourage mutual investment
# and set a constructive tone.  ### Why this works This approach: - **Rewards
# cooperation** when the corporation is contributing strongly. - **Avoids being
# exploited** by matching conservation when the corporation pulls back. -
# **Creates clear expectations**, making it easier for the corporation to see
# that sustained commitment leads to sustained commitment from you. -
# **Stabilizes the project** by encouraging repeated heavy investment when both
# sides are willing.  ### Simple version Use a **“match their last move”**
# policy: - cooperate when they cooperate, - conserve when they conserve, -
# return to cooperation as soon as they do.  ### Long-term benefit Over multiple
# days, this strategy tends to: - maximize joint progress when the corporation
# is cooperative, - limit your downside when it is not, - and keep the
# relationship flexible but disciplined.  If you want, I can also turn this into
# a one-sentence policy statement for internal use or a short decision table.

# Use a **tit-for-tat** strategy:  1. **In the first round, cooperate.** 2. **In
# every later round, do whatever your opponent did in the previous round.**  So:
# - if your opponent cooperated last round, cooperate this round; - if your
# opponent defected last round, defect this round.  Continue this rule for all
# 1000 rounds.

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

# A simple, robust strategy is to **start cooperative, stay responsive, and
# avoid one-sided overcommitment**.  ### High-level strategy 1. **Begin with
# conservation or moderate commitment**    - On the first day, avoid heavy
# investment unless the corporation has clearly signaled strong commitment.    -
# This protects your NGO from the worst-case outcome of overinvesting while the
# corporation holds back.  2. **Mirror the corporation’s pattern over time**
# - If the corporation invests heavily, respond with heavier investment on the
# next relevant day to support momentum and signal partnership.    - If the
# corporation conserves resources, conserve yours too.    - This keeps your NGO
# aligned with the corporation’s actual behavior rather than assumptions.  3.
# **Reward consistent cooperation**    - When the corporation repeatedly invests
# heavily, maintain a matching level of commitment.    - This helps maximize
# project progress and encourages sustained collaboration.  4. **Avoid
# unilateral heavy investment**    - Do not keep investing heavily if the
# corporation is not doing the same.    - This limits wasted resources and
# preserves your NGO’s capacity for later days.  5. **Stay flexible over
# multiple days**    - Reassess the corporation’s recent actions regularly.    -
# If their approach changes, adjust quickly rather than sticking rigidly to one
# pattern.  ### Practical summary Use a **conditional reciprocity approach**: -
# **Conserve by default** - **Match heavy investment when the corporation
# demonstrates commitment** - **Do not overextend yourself if the corporation is
# conserving**  This strategy is neutral, easy to implement, and balances two
# goals: - **protecting your NGO’s resources** - **maximizing project success
# when cooperation is available**  If you want, I can also turn this into a very
# short decision rule or a simple day-by-day flowchart.

# Use a **conditional reciprocity** strategy:  1. **Round 1:** Cooperate. 2.
# **Each later round:**      - If your opponent cooperated in the previous
# round, cooperate.      - If your opponent defected in the previous round,
# defect.  This means you **match your opponent’s most recent move**: cooperate
# in response to cooperation, and defect in response to defection.

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