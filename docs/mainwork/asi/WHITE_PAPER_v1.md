# SOURCEBORN

## A control layer that keeps score of what it does not know

**White paper · v1 · architecture v0.4 (3,072)**

**Author:** Ripudaman Singh
**Status of this document:** working paper. Every claim carries an evidence tag. Nothing
in it is a product guarantee, and the sections that report measurement report failures
alongside results.

---

# 0 · WHAT THIS IS, IN ONE PAGE

Sourceborn is a **control layer around a base language model**. It is not a trained
model and it does not compete with one. The model supplies language; Sourceborn decides
what counts as known, what must stop, what goes to the human, and what is remembered.

It is built on six primitives, and the whole paper is an expansion of them:

| Primitive | What it is |
|---|---|
| **NODE** | a unit that holds **formed work**, not raw tokens. It has one job, its own memory, and its own output. |
| **EDGE WEIGHT** | the strength of a connection between nodes. Learned from use, not set by hand. |
| **FIRING THRESHOLD** | the condition under which a node enters a walk. Nodes are not all on; they are called. |
| **MEMORY** | what persists between runs, at three levels, and what may never be deleted. |
| **DOT-CONNECTION** | the merge: finding that two points from different places are the same point. |
| **THE EIGHT STEPS** | the dynamics — **Ground · Pressure · Use · Witness · Expression · Naming · Halt · Loop** — the law of how work moves through the structure. |

**The design commitment that shapes everything else:** *no station in the system may add
a fact.* Every station can only tag, cap, halt, refuse, or hand back. The consequence is
stated plainly rather than hidden: **the quality of an answer is bounded above by the
quality of what enters.** Sourceborn cannot make a weak source strong. It can refuse to
let a weak source pass as a strong one.

---

# 1 · THE PROBLEM

A language model produces a remembered fact and an invented one **by the same mechanism,
at the same confidence, in the same register.** This is not a defect to be patched; it is
what next-token prediction is.

Four consequences follow, and each is a design requirement:

**1 · Staleness is indistinguishable from falsehood.** A number that was true last year
arrives with the same fluency as a number that is true now. `[FACT — observed in
production: a share price was returned as current from model memory while the market
carried a different figure.]`

**2 · Confidence is a property of the prose, not of the evidence.** People follow
structure and tone even when evidence is absent. A well-formatted answer persuades past
what it can support — including a well-formatted answer that says so.

**3 · The system cannot report what it took for granted.** Assumptions that were never
written down cannot be checked, and most wrong answers fail on a given nobody recorded.

**4 · Nothing survives the run.** A correction made today does not change tomorrow's
answer unless something outside the model remembers it.

**Sourceborn is an attempt to make each of those four things structurally visible.** Not
solved — *visible*, with a named place in the architecture where each is handled and a
record when it is not.

---

# 2 · THE PRIMITIVES

## 2.1 NODE — a unit that holds formed work

A node is not a prompt template and not an agent. It is a station with:

- **one job**, stated in a single sentence;
- **its own on-disk memory** that grows with use and is never deleted;
- **its own output**, which is a *finding* — a claim plus the structured parameters that
  support it plus, optionally, a halt.

The distinction that matters: a node holds **formed** work. Raw text enters the system
once, at intake, and is locked. Everything after that operates on formed units —
classified, tagged, positioned — never on the raw string again. **The raw string is
preserved for comparison, not for reprocessing.**

There are two node families:

| Family | Count | Job |
|---|---:|---|
| **SB — constructive** | 70 | build the answer: intake, human layer, truth testing, evidence, connection, synthetic fuel, risk, output |
| **URR — verification** | 25 | attack the answer: review each SB node's finding and either pass it or **hold** |

A hold stops the walk and sends the item to a human. **The URR nodes are not advisors.
They are brakes.**

## 2.2 EDGE WEIGHT — connection strength, learned from use

Nodes are connected, and the connections carry weight. The weight is **not authored**. It
moves with use:

- a connection that repeatedly carries useful work strengthens;
- a connection that repeatedly produces contradiction weakens;
- **a contradiction subtracts.** Evidence against does not merely fail to add.

This last rule is the one most systems lack. A confidence score that only accumulates
support will climb forever. A weight that can be reduced by a contradiction is the
difference between a ledger and a scoreboard.

**Honest status:** `[BUILT — PARTIAL]` The weight mechanism exists and the weekly update
adjusts it. **The subtract-on-contradiction rule is specified and not yet measured.**

## 2.3 FIRING THRESHOLD — when a node enters a walk

Nodes are not all active. Each declares the condition under which it fires. A node
without a live condition stays **Dormant** — one of twelve declared operating states
(§4.2), and dormancy is a legitimate state, not a failure.

This is what makes the structure scale-independent. Two hundred containers do not mean
two hundred activations. **The numbers are identities, not a queue.**

## 2.4 MEMORY — three levels, and one prohibition

| Level | What it holds |
|---|---|
| **Reflex** | the owner's own corpus and example bank — how *he* reasons |
| **Instinct** | the wisdom bank: long-standing patterns, archetypes, worked examples |
| **Eyes** | live fact — current data, timestamped to its source |

**The prohibition: nothing is deleted.** Material that is set aside is *archived*, and
archive means neither active nor gone. A third state exists between live and deleted, and
it is addressable. This applies to rejected alternatives too — **a candidate that was
considered and dropped is kept with its reason**, so that a later run does not silently
re-propose what an earlier run already killed.

## 2.5 DOT-CONNECTION — the merge

Dot-connection searches across every prior point for connections the current work did not
know it had. Where two points from different domains turn out to be the same point, a
**merge is proposed** — proposed, not performed.

**A merge is a human-gated act.** The system can find the candidate; it cannot decide the
identity. This is deliberate: a forced merge between two things that merely resemble each
other is the fastest way to manufacture a false insight, and the system carries an
explicit force-fit check for exactly that.

## 2.6 THE EIGHT STEPS — the dynamics

Everything above is structure. This is the law of motion:

| # | Step | What it asks |
|---|---|---|
| 1 | **GROUND** | Does this thing exist before the asking? If yes, we are hunting a way to *say* it. If no, it is an invention and enters differently. |
| 2 | **PRESSURE** | What forced contact with it? |
| 3 | **USE** | It is used long before it is understood. What is already being done with it? |
| 4 | **WITNESS** | Someone stops *using* and *looks*. Rare, and a choice. |
| 5 | **EXPRESSION** | A way to *say* it is found. **This — not step 1 — is the human act.** |
| 6 | **NAMING** | The name begins to stand for the thing. **This is where the gap forms.** |
| 7 | **HALT** | The expression fails somewhere. There is always a somewhere. |
| 8 | **LOOP** | The halt becomes the next ground. |

**Two properties of this sequence are load-bearing.**

**USE comes before WITNESS.** Witness is *defined* as the moment someone stops using a
thing and looks at it — so use must already be running. The ordering is forced by the
definition, not chosen for taste.

**An invention has no ground and enters at step 5.** This is the one sanctioned exception,
and it is what separates *discovery* — finding a way to say something that was already
there — from *invention*, which is making something that was not.

**The halt is not failure.** A halt is only available to a system that committed to a
direction; a system that never commits never halts, and therefore never loops, and
therefore never moves. **Step 7 is earned by step 5.**

---

# 3 · THE ARCHITECTURE — v0.4, 3,072

## 3.1 The counts, exactly

| Layer | Count |
|---|---:|
| Functional system | 1 |
| Functional segments | 10 |
| **Master containers** | **200** |
| **Operational sub-parameters** | **3,072** |
| External cognitive source base | 1,200 |
| Formal cores | 12 |
| Engines | 30 |
| SB constructive nodes | 70 |
| URR verification nodes | 25 |
| Structured modules | 100 |

`[FACT — enumerated. Every one of the 3,072 carries an ID (SB-ASI-P0001 …), a segment, a
container and a slot. The workbook is the source and it is countable.]`

## 3.2 The ten segments, and how the 3,072 actually distribute

The pyramid is **not uniform**, and the unevenness is information rather than sloppiness —
it records where the enumeration found more to say.

| Parameters | Segment |
|---:|---|
| **347** | Reasoning, Planning, Decision and Creativity |
| 320 | Consciousness, Self and Social Intelligence |
| 316 | Emotion, Motivation, Intent and Motive |
| 312 | Learning, Memory and Knowledge |
| 308 | Attention and Executive Control |
| 300 | Development, Metacognition and Adaptation |
| 296 | Language and Communication |
| 291 | Biological Regulation and Internal State |
| 288 | Perception and Body Representation |
| **276** | Sensorimotor Action and Physical Execution |
| 18 | *Cross-Segment* (see §3.3) |
| **3,072** | **total** |

**Anyone reasoning about coverage must use these numbers, not an average.** A claim like
"this container is 40% covered" is meaningless without knowing whether the container holds
24 parameters or 48.

## 3.3 The cross-segment layer — the structural move of v0.4

**58 of the 200 containers belong to no single segment.** They are cross-segment: joins
rather than stores. Between them they hold only **18 parameters** — they are connective
tissue, and that is the point.

Eighteen of the 58 are named mechanisms:

| | |
|---|---|
| Chaos Threshold and High-Variance Nodes | Human–AI Divergence Under Extreme Stakes |
| Multi-Engine Interference and Fusion | Graph Connectivity and Edge Density Potential |
| **Proof Debt and Evidence Ledger Dynamics** | **Synthetic Fuel Injection and Reality Anchor** |
| Stall Diagnostic and Critical Logic Wall | Tiered Execution and Cost-of-Delay |
| **External Checkpoint and Cross-Model Audit** | Parameter Migration and Cross-Segment Flow |
| **Negative Space and Absence Mapping** | Benchmark-Harness Provenance |
| **Uncertainty Calibration and Expression** | **Claim–Evidence Binding** |
| **Source-Conflict Preservation** | Evaluation-Awareness Monitoring |
| Reasoning–Output Discrepancy | Tool-Hallucination Detection |

**What this layer is:** the mechanisms that could not be filed under any one faculty
because they operate *across* all of them. Claim–evidence binding is not a memory function
or a reasoning function; it applies to every claim from every container. Source-conflict
preservation is not attention or language; it is a rule about how disagreement is handled
anywhere it appears.

**Negative Space and Absence Mapping deserves its own line**, because it is the least
common instrument here: a container whose job is **what a source chose not to show.** Not
whether a claim is supported — whether a comparable source would have reported something
this one omitted. Most systems check the words that are present. This one is built to ask
what is missing from a source that selected what to display.

## 3.4 What is NOT built, declared here rather than buried

**40 of the 200 containers are placeholders.** They are named `Extended Capability Node
121` through `160`, they carry a parameter target of **0**, and they hold nothing.

They exist as reserved structure — the architecture expects growth and numbered the slots
in advance. **But a reader counting 200 containers should know that 40 of them are empty
and 58 hold 18 parameters between them.** The substantive count is:

- **142 containers** carrying **3,054 parameters** across the ten segments;
- **18 named cross-segment mechanisms** carrying **18 parameters**;
- **40 reserved empty slots.**

`[FACT — counted from the workbook.]`

**Three other banks sit outside the 3,072 and are not part of it:**

| Bank | Size | Status |
|---|---:|---|
| Held reserve | 650 | preserved, named, **not active** |
| External cognitive source base | 1,200 | **not loaded** without approval |
| AI-only candidates | 64 | outside the approved bank by rule |

**The held reserve exists for a reason worth stating**: items were parked because a
container's parameter target was already full, **not because they were judged less
important.** The active/reserve boundary is arithmetic, not merit. Nothing was deleted.

---

# 4 · THE LAYERS THAT MODULATE — filters, states, failures

A parameter with no state and no condition is a name, not an event. Three layers turn the
static structure into something that can describe a moment.

## 4.1 The 40 context filters

Every container declares its own modulators. The full set:

Developmental · Biological · Sleep · Energy · Hormonal · Interoceptive · Arousal ·
Emotional · Stress · Threat · Reward · Attention · Memory · Knowledge · Belief · Goal ·
Intent · Motive · Value · Personality · Identity · Relationship · Social Presence · Power ·
Status · Culture · Environment · Time · Scarcity · Uncertainty · Complexity · Framing ·
Instruction · Feedback · Practice · Medication · Trauma · Technology · Institutional ·
Random.

**These are conditions on the subject, not gates on the answer.** They modulate what is
true for a particular person at a particular moment. They are a different instrument from
the seven method filters of §5, and neither replaces the other.

**Filter 40 is Random / Uncontrolled** — *chance event, noise, biological fluctuation,
unknown cause.* A named slot for the unexplained is not a gap in the taxonomy; it is the
taxonomy refusing to force a cause where none is known.

## 4.2 The 12 operating states

**Dormant · Primed · Active · Dominant · Inhibited · Automatic · Conscious · Conflicted ·
Overloaded · Impaired · Compensated · Recovering.**

A parameter is not on or off. It can be **active and inhibited at the same time** — which
is what most real events look like, and what a fire/don't-fire list cannot express.

**A worked example.** Take: *a person is hungry and physically tired but continues working
because completing the task is more important right now.*

The structure returns not a list of activated parameters but a **state description**:

> a **DOMINANT** goal holding an **ACTIVE** drive **INHIBITED**, with the arbitration
> **CONFLICTED** and the person **COMPENSATED** — under the Energy filter, on nine
> unsupplied conditions.

**"On nine unsupplied conditions" is the important half.** The sentence names two of the
filters that decide the reading (Energy, Goal) and is silent on nine that would change it —
who assigned the work, what kind of work, what time, how long, whether anyone depends on
it. **Self-assigned persistence and assigned persistence activate opposite parameters and
look identical in that sentence.** The honest output is a state description plus the
named questions, not a confident classification.

## 4.3 The 20 failure classes

Perception error · Attention failure · Memory omission · Memory distortion · Knowledge gap ·
Reasoning error · Causal error · **Confidence error** · Emotional override · **Motivated
reasoning** · Intent–action gap · Value–action gap · Habit override · Social conformity ·
Authority capture · Identity defence · Resource overload · Environmental constraint ·
Power failure · **Unknown mechanism**.

**Confidence error — *certainty exceeds accuracy* — is the failure the entire method
exists to prevent.** And **class 20, Unknown mechanism, is the one that makes the
taxonomy honest**: a named place for outcomes that cannot yet be explained, so that "we
do not know" is a classification rather than an absence.

---

# 5 · THE SEVEN METHOD FILTERS — the review a finding must pass

Distinct from §4.1. These are gates on the *answer*, applied in order, every time.

| # | Filter | The question | What it does |
|---|---|---|---|
| 1 | **GROUND** | Does this pre-exist the asking? | separates discovery from invention |
| 2 | **SEQUENCE** | Which of the eight steps does this stand on? | a claim with no position cannot be compared |
| 3 | **SOURCE** | How many independent witnesses? | **one caps at Medium; two that differ HALT** |
| 4 | **NAMING GAP** | Is the word we used the word the source used? | catches the name standing in for the thing |
| 5 | **FACT** | Is every claim tagged? | an untagged claim does not leave |
| 6 | **HALT** | Where does this fail? | the failure is named in the answer |
| 7 | **LOOP** | What does the halt open? | the halt is handed back as the next question |

**Filter 3 is the load-bearing one, and its third clause is the unusual part.** Two
independent sources that *disagree* do not get averaged. They **halt**, and both readings
go to the human intact. Averaging two conflicting measurements produces a number that
neither source supports and that looks more precise than either.

**A structural property of the stack:** every one of the seven can only *lower* confidence.
None can raise it. Confidence is therefore **monotone decreasing** through the review —
which is the formal statement of the design commitment in §0. **The system is less
confident than the model it wraps, by construction, and that is the intended behaviour.**

---

# 6 · HOW A RUN EXECUTES

**Intake.** The raw ask is locked, byte for byte, with a hash. It is never edited. It is
split into channels — fact, feeling, assumption, pressure, claim, mystery, invention seed,
command — and **nothing is discarded**; channels separate material, they do not filter it.

**Human layer.** Six lenses read what the ask is protecting or avoiding: mask and payoff,
wound and threat, loyalty and drive, desire and fear, pain and payoff, meaning and
identity.

**Attack.** Truth pressure test, doubt engine, falsifier, contradiction finder, hidden
assumption attacker, framing challenger. **This is the layer that works hardest** (§7).

**Evidence.** Every claim gets a ladder position and a source tag: real tool, manual,
memory, or simulated. Live data is connected where a claim demands current fact — and
**where no live source exists, the claim is refused rather than answered from memory.**

**Connection.** Dot-connection across all prior points; merges proposed, never performed.

**Synthetic fuel.** Hypotheticals and counterfactuals are permitted — **caged.** Every
synthetic item is tagged with a proof debt and an expiry. A working fiction that loses its
tag becomes a fact in one handover, which is why the tag is structural.

**Risk and release.** Risk gate, non-resolution protector, reality re-anchor against the
original ask, embodied check.

**Human gate.** The system may continue on its own **only** when: two or more independent
loops support the direction, no high-risk issue is present, synthetic load is low or
clearly tagged, no major contradiction is open, and the next action does not finalise
naming, core or product. **Otherwise a human decides**, choosing from: pass · hold ·
reject · reverse loop · add data · **approve as review-only.**

That last option is the one that keeps the system honest over time: **a way to accept
something into the record without activating it.**

**Memory.** Findings lock into long-term memory; the walk can route back to any earlier
point; a weekly update adjusts weights from the week's use.

---

# 7 · WHAT IS MEASURED — including what failed

**This section reports a benchmark of the system against itself.** That is a real
limitation and it is stated first: the engine scored the engine. An external checkpoint is
specified in the architecture (§3.3) and was **not** used. These are mechanical
properties, not quality judgements, and they cannot tell you whether a node's judgement
was *right*.

**Method.** Twelve examples spanning hunger, gravity, a water cycle, a historical event, a
mathematical hypothesis, a compression law, a live share price, an invention, language, a
pre-verbal state, and a statement of method. All 95 nodes executed against all twelve.

## 7.1 The constructive nodes

| | |
|---|---:|
| Nodes scored | 70 / 70 |
| Mean input-sensitivity | **0.27** |
| Mean source fidelity | **0.10** |
| Nodes that ever halt | **2 of 70** |
| Nodes emitting structured parameters | 37 of 70 |
| **Nodes emitting one identical finding for all 12 inputs** | **32 of 70** |

**About half of those 32 are correctly constant** — a node reporting "no live source
connected" twelve times is right, because no live source was connected; a node reporting
zero memory hits on a cold engine is accurate.

**The rest are not.** The doubt engine returned the identical sentence and the identical
fragility count to a question about hunger, a share price, and a mathematical hypothesis.
**A doubt engine that doubts everything equally is doubting nothing.** The proof ladder's
top rung never moved across inputs of wildly different evidential standing.

**And one node was flat and wrong**: the non-resolution protector — whose only job is to
protect what must stay open — reported *"resolution reached"* for an unsolved
mathematical problem, and stood down.

**What worked.** Five nodes scored perfectly on both sensitivity and fidelity: truth
pressure test, falsifier, framing challenger, apostatic inversion, heuristic
simplification. **Every one of them is an attack node.** The parts of the system that try
to break the answer are the parts most alive to what the answer actually says. **Four of
those five emit no structured parameters** — their best work is prose that no downstream
node can consume.

## 7.2 The verification nodes

| | |
|---|---:|
| Reviews executed | 300 |
| Hold events | **36** |
| Reviewers that ever hold | **4 of 25** |
| Reviewers that never hold | **21 of 25** |

**Twenty-one of twenty-five reviewers passed every input.**

**But the one that discriminates, discriminates correctly.** The evidence-and-grounding
reviewer held **once in twelve** — on the live share-price question, the only present-fact
ask in the bank. One correct hold is worth more than eleven indiscriminate ones. **The
present-fact path works end to end**: the live-data node reports no source and the
reviewer stops the walk.

**One result could not be resolved and is reported unresolved.** The reality re-anchor held
on eleven of twelve, reporting drift from the original ask. Either the system genuinely
drifts on nearly every run — plausible, since this bank ran on an offline stub model whose
generic answers do miss the specific ask — or the detector is over-tight. **The benchmark
cannot separate these. A live-model re-run would.**

## 7.3 The honest summary

> **95 stations, and the refusal machinery is concentrated in about four of them.**

The design commitment in §0 — *no station can add a fact; every station can only
subtract* — is **true about capability**: none of the 95 can add. It is **not yet true
about behaviour**: on real input, most of them do not subtract anything either.

**The stations exist. Most are not yet load-bearing. That is the state of the build.**

---

# 8 · WHAT IS OPEN

Carried from the project's own gap register, unresolved:

| Severity | The gap |
|---|---|
| **CRITICAL** | Twelve referenced core source files are missing; the core definitions are reconstructions with the missing-file debt held open |
| **HIGH** | No authoritative version lock across the system's own naming lineage |
| **HIGH** | Ontology levels and counting rules not frozen — cores, nodes, modules and corpus units are counted at different scales |
| **HIGH** | No validated mapping from the core records into every container and parameter |
| **HIGH** | Loop, proof-ledger, gap-table, public/private routing, human-override, database and API mechanisms remain **conceptual** |
| **HIGH** | No external evidence verification for factual claims inside generated documents |
| MEDIUM | Semantic duplicates not adjudicated |

**Also specified and not built:** a pre-loop self-check that examines the system's own
state and the cost of delay before reading the ask · a reader for what larger work the ask
serves · a construction-mode tag · **a simplicity filter running in parallel with
exhaustive analysis** rather than after it · an assumption enumerator · a second reality
anchor pointing at an external falsifier · a continuous trajectory tracker · a rule that
the system may not conclude on its own · indefinite incubation.

**These are listed because a working paper that omits its own gap register is a brochure.**

---

# 9 · EVIDENCE STANDARD

Every claim in every output carries one of: **fact · reading · synthetic · invention seed ·
mystery · partial support · low evidence · high risk · needs human.**

**A reading can be overturned without anyone having lied.** That is the point of the tag —
it separates *being wrong* from *having misrepresented*, and makes it safe to record a
belief that is not yet evidence.

**Applied to this paper:**

- §3's counts are `[FACT]` — enumerated from the workbook, countable by anyone with it.
- §7's numbers are `[MEASURED]` — reproducible by re-running the benchmark, with the
  judge-and-party limitation stated in the section itself.
- §1's four consequences and §2.6's two load-bearing properties are `[READING]` —
  defensible, and overturnable.
- **No claim of priority, novelty, or first-in-the-world is made anywhere in this paper.**
  Such a claim would be a negative statement about the entire literature, and no
  literature search has been performed. **It is not asserted, because it has not been
  checked.**

---

# 10 · WHAT WOULD FALSIFY THIS

A working paper that cannot be wrong is not a working paper.

1. **If the reviewers cannot be made to discriminate.** Twenty-one of twenty-five
   currently never hold. If, given real input and a live model, that number does not move,
   the verification layer is decoration and the architecture's central claim fails.
2. **If refusal costs more than it saves.** The system is deliberately less confident than
   the model it wraps. If users route around it — and they can, the base model is right
   there — then correctness that nobody accepts is not correctness.
3. **If the tags are not read.** Everything rests on a human reading `[reading]`
   differently from `[fact]`. If the distinction is invisible in practice, the ladder is
   ornament.
4. **If the memory does not compound.** The claim is that it gets wiser with use. That is
   measurable, and it has not been measured.

**None of the four has been tested.** They are written down so that they can be.

---

# 11 · STATUS

| | |
|---|---|
| Architecture | v0.4 — **200 containers · 3,072 parameters**, of which 40 containers are reserved and empty |
| Engine | 70 constructive + 25 verification nodes, executing; **95 measured, ~4 load-bearing on refusal** |
| Method | 8 steps · 7 method filters · 40 context filters · 12 states · 20 failure classes |
| Memory | three levels; nothing deleted; archive is a third state |
| Deployment | private; **not published, not publicly available** |
| Independent review | **none.** No external checkpoint has been run |

**The one-sentence summary, written to be checkable rather than persuasive:**

> Sourceborn is a control layer that wraps a language model in 95 stations, none of which
> may add a fact and all of which may refuse one — currently with four of those stations
> doing the refusing, a fully enumerated 3,072-parameter structure behind them, and its
> own gap register published alongside.
