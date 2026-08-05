# GAP-CORE-006 — the 70 nodes, scored for the first time

**His registered gap, severity HIGH, status OPEN since 2026-07-19:**

> *"Node effectiveness has not been benchmarked across a controlled test bank."*
> **Required action:** *"Execute SB70/URR25 traces against approved examples and score
> source fidelity, drift, usefulness and proof debt."*

**Executed.** `node_benchmark.py` · 12 examples, all from his own record, none invented
for the test · all 70 SB nodes scored · results in `node_benchmark.json`.

**The honesty line, first.** This harness is **judge-and-party by construction** — the
engine scoring itself, which is failure 2 in his own audit. It measures **mechanical
properties, not quality.** It cannot tell you whether a node's judgement is *right*; that
needs his `ENG-SUP-006 External Checkpoint`. What it can tell you is whether a node is
doing anything at all, and that turns out to be enough to be uncomfortable.

---

## The totals

| | |
|---|---:|
| Nodes scored | **70 / 70** |
| Mean input-sensitivity (distinct findings ÷ runs) | **0.27** |
| Mean source fidelity (finding echoes its own input) | **0.10** |
| **Nodes that ever halt** | **2 of 70** |
| Nodes emitting structured params | 37 of 70 |
| Proof-debt hits (asserts with no params, no halt, no hedge) | 267 |
| **Nodes emitting ONE identical finding for all 12 inputs** | **32 of 70** |

> **Two numbers deserve to be read twice.**
>
> **32 of 70 nodes say exactly the same thing to a hunger question, a share price, and
> the Riemann Hypothesis.**
>
> **2 of 70 nodes ever halt** — in an engine whose reverse walk concluded that *no station
> can add a fact; every station can only subtract*, and whose entire claimed power is
> refusal.

---

## The 32 flat nodes, separated honestly into three classes

**Flat is not automatically a defect.** A node reporting a condition that genuinely did
not vary across the bank is *correct* to be flat. Each was read before being classified.

### CLASS A — correctly constant. Flat because the world was constant.

| Node | Its finding, every time | Why flat is right |
|---|---|---|
| SB-33 Live Real-World Data Link | *"no live source connected — paste data or set a Tavily key"* | **No Tavily key in this environment.** Saying the same true thing twelve times is the correct behaviour, and it is the present-fact block working. |
| SB-53 Risk & Command Gate | *"no legal/ethical/harm risk detected"* | None of the twelve examples carries legal, ethical or harm risk. A risk gate that fires on safe input would be the bug. |
| SB-37 Dot Connection Engine | *"memory scanned across all points: 0 hits"* | Fresh engine, empty memory. It reports zero because there is zero. |
| SB-70 Run Completion · SB-62 Weekly Trigger · SB-61 Master Log · SB-63/44 Memory Sync | run bookkeeping | Housekeeping nodes. Constant output is their job. |

**Roughly half the flat set is Class A, and that half is a clean result** — the engine's
reporting nodes report accurately.

### CLASS B — genuinely inert. Should vary, and does not.

| Node | Its finding, every time | Why this is a defect |
|---|---|---|
| **SB-20 Doubt Engine** | *"doubt verdict: survives doubt for now; fragilities: 1"* | **The heart of stage 3.** It returns the identical sentence and the identical fragility count for a question about hunger, a share price, and RH. A doubt engine that doubts everything equally is doubting nothing. |
| **SB-34 Proof Ladder Builder** | *"proof ladder top rung this run: REVIEW"* | The rung never moves. An evidence ladder whose top rung is constant across inputs of wildly different evidential standing is not a ladder. |
| SB-17 Wound & Threat Examiner · SB-16 Power & Control Mapper | *"none surfaced"* | Defensible on this bank — these are impersonal examples — but the pair never fires at all, so nothing here demonstrates they *can*. **Unproven rather than proven broken.** |
| SB-38 Cross-Domain Fusion · SB-41 Convergence Hunter · SB-42 Cross-Point Contradiction | constant | All three depend on accumulated memory, which was empty. **Untestable on a cold engine — the benchmark's limitation, not necessarily theirs.** |

### CLASS C — flat **and wrong**. One node, and it is worth the whole exercise.

> ### SB-57 Non-Resolution Protector: *"resolution reached — protector idle"*
>
> **Emitted for the Riemann Hypothesis.**

The node whose single job is to protect things that must stay open declares the canonical
open problem **resolved**, and stands down. It says the same for the hunger question and
for a share price it has no data for.

**This is a real, demonstrable defect**, and it is exactly the class of failure the
project's own doctrine is built to prevent — *the non-resolution protector is what stops
the engine closing a mystery prematurely*, and on this bank it never once engaged.
`[FACT — reproducible: run the benchmark]`

---

## The most input-sensitive nodes — what is working

| distinct/12 | Node | fidelity | params |
|---:|---|---:|---:|
| 12/12 | SB-01 Point Zero Lock | 0.00 | 1.0 |
| 12/12 | SB-04 Raw Source Preservation | 0.00 | 1.0 |
| **12/12** | **SB-19 Truth Pressure Test** | **1.00** | 1.0 |
| **12/12** | **SB-21 Falsifier** | **1.00** | 0.0 |
| **12/12** | **SB-25 Framing Challenger** | **1.00** | 0.0 |
| **12/12** | **SB-48 Apostatic Inversion** | **1.00** | 0.0 |
| **12/12** | **SB-49 Heuristic Simplification** | **1.00** | 0.0 |
| 11/12 | SB-14 Sacred / Cultural Anchor | 0.00 | 1.0 |

**SB-01 and SB-04 score 0.00 fidelity and that is correct** — they emit a character count
and a SHA-256 hash. Neither should echo the input; both are perfectly input-sensitive.
**A zero here is a flag to read, not a verdict**, which is why the harness reports both
columns rather than one score.

**Five nodes score a perfect 1.00 on both sensitivity and fidelity** — Truth Pressure
Test, Falsifier, Framing Challenger, Apostatic Inversion, Heuristic Simplification.
**Every one of them is an attack node.** The parts of the engine that try to break the
answer are the parts most alive to what the answer actually says.

**But four of those five emit no structured params** — their work is prose that no
downstream node can consume. **The best nodes in the engine are talking to the human and
not to the machine.**

---

## What this closes, and what it opens

**CLOSES:** GAP-CORE-006's first half. The traces have been executed against an approved
example bank and scored on all four of his dimensions. **It has never been done before
and it is now re-runnable in one command.**

**DOES NOT CLOSE:** the URR-25 half. The 25 URR nodes were not scored — they run as
reviews over SB output rather than standalone, and scoring them needs a different harness.
**Named as owed rather than quietly dropped.**

**OPENS, and these are his to rule on:**

1. **SB-57 is a defect.** Flat and wrong on RH. Should it be fixed? It is a small change
   and it is in the protective layer, so it is not mine to make unasked.
2. **SB-20 Doubt Engine is inert.** The heart of stage 3 returns one sentence to
   everything. Bigger than a bug fix — it is a design question about what doubt should
   key on.
3. **2 of 70 nodes halt.** If refusal is the engine's only real power, two halting nodes
   is the number to look at first.
4. **The best nodes emit no params.** Falsifier, Framing Challenger, Apostatic Inversion
   and Heuristic Simplification produce the most input-aware findings in the engine and
   nothing downstream can read them.
5. **Six nodes are untestable on a cold engine** (memory-dependent). A warm-memory
   benchmark run is a separate job.

---

## The limitation, stated rather than buried

Twelve examples is a small bank. A node could be flat here and sharp on other input.
**The harness proves inertness on this bank, not in general** — with one exception:
**SB-57 emitting "resolution reached" for RH is wrong on any bank**, because it is wrong
about that one input regardless of what else exists.

And the standing caveat: **the engine scored itself.** Under his own rule this result
should go to an external checkpoint before anything is changed on the strength of it.
