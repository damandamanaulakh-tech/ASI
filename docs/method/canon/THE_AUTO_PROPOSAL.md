# THE AUTO PROPOSAL — how it runs without you

**His ask:** *show me what you r building how it will be working / which and how
the algorithm will work / how it will add new node / how the memory brain on
nodes will work / how it make combinations how many loops there it make / how
newly added parameters or other headers will be connected and new memory nodes
will generate and how all keep linking in auto — because here for now i'm giving
instruction but to make it self sustain it need to work in auto / what is ur
proposal to build it*

**Date:** 2026-08-13. This is a PROPOSAL. Nothing in section 4 is built yet.

---

## 0. THE ONE-LINE ANSWER

Every generator, gate, kill, maturity and ledger already exists and runs. **What
does not exist is the wiring that makes a write cause the next piece of work.**
Today you are the wire. Three things replace you, and only three:

```
1. AN EDGE STORE     nodes can find each other          (stage 5, today PARTIAL)
2. A WRITE TRIGGER   a write wakes the next step        (stage 22, today PARTIAL)
3. A BUDGET + STOP   auto without a stop is a leak      (does not exist at all)
```

There is **already a daemon thread** — `scheduler.start_weekly_scheduler`,
started at `server.py:2393`, checking hourly. It drives the weekly pull and
nothing else. Auto does not need a new daemon; it needs that one to drive more.

---

## 1. THE FLOW, AS IT WOULD RUN WITHOUT YOU

```
                    ┌──────────────────────────────────────┐
                    │  A NEW THING ARRIVES                 │
                    │  a file · your words · a run's own   │
                    │  output from the pass before         │
                    └───────────────┬──────────────────────┘
                                    ▼
        ╔═══════════════════════════════════════════════════════╗
        ║  INTAKE            growing.place()        EXISTS      ║
        ║  events_in ─► role_of ─► seat ─► intent_seat          ║
        ║  every happening an event, every event an intent      ║
        ╚═══════════════════╤═══════════════════════════════════╝
                            ▼
        ┌───────────────────────────────────────────────────────┐
        │  SEATED ON THE BANK   3,204 + 3        EXISTS         │
        │  the example gives existing IDs SUPPORT               │
        │  it creates no parameter                              │
        └───────────────────┬───────────────────────────────────┘
                            ▼
        ╔═══════════════════════════════════════════════════════╗
        ║  ★ THE LINKER                          TO BUILD  (A)  ║
        ║                                                       ║
        ║  a new row is written  ─────┐                         ║
        ║                             ▼                         ║
        ║              what IDs did it seat on?                 ║
        ║                             │                         ║
        ║                             ▼                         ║
        ║        which existing rows seat on those same IDs?    ║
        ║                             │                         ║
        ║                             ▼                         ║
        ║              WRITE AN EDGE for each overlap           ║
        ║              edge = (row A, row B, shared IDs, weight)║
        ║                             │                         ║
        ║   THIS IS ALSO STAGE 5. The relation graph stops      ║
        ║   being a list and becomes traversable.               ║
        ╚═══════════════════╤═══════════════════════════════════╝
                            ▼
        ┌───────────────────────────────────────────────────────┐
        │  MEMORY NODE          per row, per edge   TO BUILD (B)│
        │  what this row has seen, and what changed when it did │
        │  APPEND ONLY — a node is a chain of readings          │
        └───────────────────┬───────────────────────────────────┘
                            ▼
        ╔═══════════════════════════════════════════════════════╗
        ║  COMBINATION       selfmake · artifact     EXISTS     ║
        ║  but reached BY HAND today — the trigger is (C)       ║
        ║                                                       ║
        ║  new edges ─► new arrangements ─► new combinations    ║
        ║  gated: cross-role · ROLE_FUTURES · FUTURE_NEEDS      ║
        ╚═══════════════════╤═══════════════════════════════════╝
                            ▼
        ┌───────────────────────────────────────────────────────┐
        │  THE 23-STAGE LOOP    discovery.loop()     EXISTS     │
        │  01..23 · closes · S0 ─► S1 ─► terminates             │
        │  12 predicts · 17 kills · 18 matures · 19 verdicts    │
        └───────────────────┬───────────────────────────────────┘
                            ▼
        ╔═══════════════════════════════════════════════════════╗
        ║  ★ BUDGET AND STOP                     TO BUILD  (D)  ║
        ║                                                       ║
        ║  rows written this tick    < cap ?                    ║
        ║  new edges this tick       < cap ?                    ║
        ║  did anything NEW open ?                              ║
        ║          │ yes                    │ no                ║
        ║          ▼                        ▼                   ║
        ║      loop again              STOP — and say so        ║
        ╚═══════════════════╤═══════════════════════════════════╝
                            ▼
        ┌───────────────────────────────────────────────────────┐
        │  THE DAEMON       scheduler.py            EXISTS      │
        │  already running hourly at server.py:2393             │
        │  today it drives ONLY the weekly pull                 │
        └───────────────────┬───────────────────────────────────┘
                            ▼
        ╔═══════════════════════════════════════════════════════╗
        ║  YOUR GATE — UNCHANGED, AND IT DOES NOT MOVE          ║
        ║                                                       ║
        ║  auto may:   seat · link · combine · predict · mature ║
        ║  auto may NOT: promote · make canonical · add a       ║
        ║                parameter · answer · delete            ║
        ║                                                       ║
        ║  everything auto produces arrives at your desk as a   ║
        ║  candidate with its evidence. Nothing crosses without ║
        ║  your word.                                           ║
        ╚═══════════════════════════════════════════════════════╝
```

---

## 2. YOUR QUESTIONS, ANSWERED ONE BY ONE

### How does it add a new node?

A node is a row in the growth ledger — it already has 17 typed series
(`PARAM`, `EVENT`, `INTENT`, `CANDIDATE`, `STEP`, `ADDRESS`, `HALT`…). Adding is
`growth.add()`, append-only, and no removal path exists in the module — a test
reads its own source to prove that.

**What is missing is not the adding. It is that an added row is inert.** It sits
in the file. Nothing looks at it, nothing links to it, and nothing happens
because it arrived.

**Proposed:** `growth.add()` gains one line — it emits the row it wrote. The
linker subscribes. That is the whole change at the write site; everything else
hangs off it.

### How will the memory brain on nodes work?

Today `brains.BrainRegistry` holds 95 configured node brains with a
`weekly_update` path, and the 2026-08-12 audit found **90 of 95 hold no memory**.
That is still true and I am not going to pretend otherwise.

**Proposed shape, and it follows the maturity ledger exactly** — because that one
is built and works:

```
a memory node is NOT a field that gets overwritten.
it is a CHAIN of readings, each referencing the one before it.

  reading 1   first seen — seated on P0717, P1787
  reading 2   linked to SB-EX-00042 (3 shared IDs)
  reading 3   a combination opened; maturity SUPPORTED
  reading 4   a prediction was refuted; maturity WEAKENED
```

`maturity.update()` already does precisely this for one value. The memory node
is the same mechanism applied to a row instead of a reading. **Nothing is
overwritten, so history is never rewritten** — your no-reopen rule, which is
already enforced in three other places.

### How does it make combinations, and how many loops?

Combinations are built and gated. What is missing is only the trigger. **There
are five loops. Four exist.**

| # | loop | turns on | exists? |
|---|---|---|---|
| **L1** | the 23-stage discovery loop — 01…23, close, S0→S1, terminate | a text | **YES** |
| **L2** | self-extension — harvest → arrangements → steps → extend | material | **YES** (by hand) |
| **L3** | maturity — check → read → append reading | evidence | **YES** |
| **L4** | **the link loop** — write → seat → edge → combine → write | a write | **NO** |
| **L5** | the daemon tick — hourly | the clock | **YES** (weekly pull only) |

**L4 is the one that makes it self-sustaining**, because it is the only loop
whose input is the system's own output. L1 already closes on itself, but a human
starts it. L4 starts itself, from a write.

**How many turns per tick?** Bounded, and that is deliberate: a budget per tick
(rows, edges, passes), and the loop stops the moment a pass opens nothing new.
That stop condition is already proven three times over — extending `selfmake` on
the same material writes 0 steps, and `discovery.loop` terminates in 2–3 passes.

### How do newly added parameters and headers get connected?

**By what they seat on, not by their name.** Two rows are linked when they seat
on shared IDs in the 3,204. That is computable the moment a row is written, it
needs no vocabulary, and it works identically for a parameter, a candidate, an
event, a step or a halt — which is why it generalises to "other headers" without
a special case per type.

Edge weight is the shared-ID overlap, with the same IDF discipline the seating
already uses: **two rows sharing a rare ID is evidence; two rows sharing a common
one is not.** Without that, everything links to everything and the graph is
noise — the same failure mode as the ungated 6,480 meanings and the 2,627
combinations.

---

## 3. WHAT I WILL NOT PRETEND

**Auto plus append-only plus no delete is a real risk, and it is the main one.**
Every gate so far has been necessary: ungated, the artifact generator returned
6,480 of 6,480; the self-made steps returned 2,627 of a possible 3,160; my first
`loop()` never terminated. Each time the raw cross product was the wrong answer.

Running that on a timer, into a ledger that by your own rule can never delete,
would fill your base with rows nobody chose. So the budget in (D) is not
housekeeping — **it is the thing that makes auto safe to switch on at all**, and
I would build it before, not after.

**And auto must not touch three things:**
- it may not **promote** — canonical still needs your word
- it may not **add a parameter** — rule 7, repeated semantic loss, unchanged
- it may not **answer** — it prepares, you decide

---

## 4. THE PROPOSAL — four pieces, in dependency order

| | piece | what it does | unblocks |
|---|---|---|---|
| **A** | **EDGE STORE** `links.py` | rows link by shared seated IDs, IDF-weighted, append-only. `neighbours()`, `path()`, `subgraph()` | **stage 5** stops being a list |
| **B** | **MEMORY NODE** `nodemem.py` | per-row chain of readings, same shape as `maturity.update` | the 90 empty brains get a real store |
| **C** | **WRITE TRIGGER** in `growth.add` | a write emits; the linker runs; new edges open combinations | **stage 22** stops being by-hand |
| **D** | **BUDGET + STOP** `autoloop.py` | per-tick caps, stop-when-nothing-new, a run report you can read | makes A–C safe to leave running |

Then one line in `scheduler.py` attaches `autoloop.tick()` to the daemon that is
**already running**.

**Order matters and it is not negotiable:** D exists before the daemon is
attached. A and B are inert stores — they cannot run away. C is the first thing
that can, and D is what holds it.

**What you would see after each piece:**

- after **A** — `/links` shows the graph; stage 5 goes PARTIAL → RUNS
- after **B** — every row has a visible history; the empty-brains finding starts
  closing
- after **C** — adding one file causes edges and combinations without you asking
- after **D** — the daemon runs it hourly, with a bounded, readable report, and
  stops itself

**My recommendation:** build A and B first and leave the trigger off. They are
useful immediately — the graph is a real answer to stage 5 — and they cannot
misbehave, because nothing calls them on a timer. Then look at what A actually
produces on your 479 files **before** deciding whether C should fire on every
write or only on a batch. I would rather show you the edge counts on real
material than guess the caps for D in advance.

---

## 5. THE HONEST STATE OF THINGS THIS PROPOSAL RESTS ON

- 23 of 23 stages run; the chain completes; `loop()` terminates three ways
- three stages remain PARTIAL: **1** source lock (discipline, not a checksum),
  **5** relation graph (listed, not traversable), **22** new-combination
  availability (by hand)
- **90 of 95 node brains hold no memory** — from the 2026-08-12 audit, still open
- the daemon exists and runs; it drives one job
- nothing in this document is built
