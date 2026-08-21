# PHASE D — THE MEMORY GRAPH + AUTO-LINKING

**His order:** *build phase D* — the fourth phase of his SELF-SUSTAINING
EXECUTION FLOW sheet. The node schema Phase A locked becomes a living store:
nodes written under his five write conditions, linked at write time by his six
read conditions, each node carrying its own chain of readings, the whole thing
traversable.

**Date:** 2026-08-21. Module: `src/sourceborn/nodegraph.py`. Routes: `/nodes`,
`/nodes/node`, `/nodes/path`, `/nodes/subgraph`, `POST /nodes/write`,
`POST /nodes/remember`, `POST /nodes/recall`, `POST /nodes/approve`.

---

## 1. WHAT THIS CLOSES

* **Stage 5, RELATION GRAPH** — PARTIAL since the first audit (*"listed, not
  traversable"*). `neighbours()`, `path()`, `subgraph()` make it walkable,
  every hop TYPED. **The discovery audit now reads 22 of 23 RUNS; stage 1
  (source lock) is the last PARTIAL.**
* **The write gate** — Phase A defined his five write conditions and said
  enforcement is Phase D. `write_node` is that site: a failing write is
  REFUSED with the unmet conditions named, never stored malformed. The fourth
  condition — *link map created* — is met BY the write path, because the
  auto-linker runs inside it. That is exactly why it could not be enforced
  before D existed. **A link map with zero links is still a map** — it
  records that the conditions were checked and nothing matched.
* **The empty brains** — the 2026-08-12 audit found 90 of 95 node brains hold
  no memory, and it stayed true through every build since. `remember()` is
  the per-node chain of readings: append-only, each reading referencing the
  one before, kinds constrained to his eleven.
* **Three more of his nine loops** — Retrieval, Memory Reinforcement, and
  Contradiction in its honest scope. **Eight of nine now run; the ninth
  (Node-Growth) runs up to its queue and stops where only his word may act.**

## 2. HIS SIX READ CONDITIONS — ONE MECHANISM, USED TWICE

`recall(probe)` answers *which stored nodes does this material reach, and by
which of his six conditions* — the Retrieval loop, evidence named per hit.
The auto-linker is the SAME call at write time: what recall finds, the linker
links. One implementation, so retrieval and linking can never disagree.

## 3. THE GRAPH SHAPE HIS TWELVE TYPES EXIST FOR

His box 6 says auto-link; Phase A gave ten TYPED links and twelve node types
including ACTOR, PATTERN, ARTIFACT, FUTURE_STATE. Those types only do work if
the linker MATERIALIZES them:

| read condition | what happens |
|---|---|
| same actor | an **ACTOR node exists once**; each event links from it by `actor_of` |
| same pattern | events **`support`** the PATTERN node |
| same artifact family | an event **`depends_on`** the ARTIFACT — prior.py's own entailment: the object existed or the event could not stand |
| same future-state goal | an event is **`future_of`** the FUTURE_STATE node |
| similar event | `similar_to` between events — **only** on the same event shell or **≥ 2 shared seated rows**; **containers alone never link** (the Phase C anchor lesson: structure is not content) |
| same contradiction | `contradicts`, mutual — see §4 |

Two events by the same actor do NOT get a vague tie to each other — they meet
at the actor. That is a graph, not a similarity blob, and `path()` proves it:
the route from one rain event to another runs *event → actor hub → event*,
with every hop naming its type.

## 4. THE CONTRADICTION LOOP, IN ITS HONEST SCOPE

`contradicts` fires structurally in ONE case: two nodes carrying the SAME
subject whose verdicts OPPOSE (RETAIN vs REJECT). Deeper contradiction
detection from arbitrary prose is model-grade inference this module does not
have, and claiming it would be fake. Anything richer arrives from a caller
that saw it (a witness split, a filter HALT) and says so.

**A defect the first contradiction test caught, on the record:** the box-6
dedupe matched on subject and actor but NOT verdict — so an OPPOSING reading
was folded into the node it opposed, a contradiction silently swallowed as a
duplicate. The match now requires the same CLAIM (signature + actor +
verdict); the opposing reading is written and contradiction-linked, and both
stand.

## 5. HIS BOX 6 — RUN UP TO THE QUEUE, AND STOPPED THERE

* **Existing match** → the existing node is REINFORCED, never re-created:
  support 1 → 2, `duplicate_created: False` — his mall-example reinforcement
  rule applied to nodes.
* **No match** → a new node is written OPEN (his growth ruling: append-only,
  provenance carried, nothing lost).
* **The evidence gate and the maturity threshold are EVALUATED** — a node
  needs a confirmed discriminating reading AND SUPPORTED/STRONG maturity.
  Maturity alone does not queue; a test pins that.
* **A node passing both is QUEUED FOR HIM.** `promoted` stays 0 until his
  word. `approve()` exists as HIS action — an APPROVAL row referencing the
  node; the NODE row itself is never rewritten (NO REOPEN: the file still
  says OPEN, the fold reads ACCEPTED from his approval).

**Why a queue:** his sheet ends the tree at *"Assign Permanent Node ID"*, and
the question I asked — does passing the gates assign it on its own, or does
it queue for him? — is still unanswered. Until he answers, the conservative
reading stands, and it is stated on the queue itself: **this is a placeholder
for his answer, not the answer.**

## 6. APPEND-ONLY, STRUCTURALLY

No delete, remove, pop, truncate, unlink or write-mode path exists in the
module; the store opens in mode `"a"` only; a corrupt line comes back
UNREADABLE with its raw text; a test reads the module's own source (the
growth.py technique) and fails if a removal path is ever added. Nothing is
rewritten — an approval, a correction, a new reading is a new row referencing
what it acts on.

## 6b. WHAT THE REVIEW OF THE DIFF CAUGHT, AFTER THE FIRST COMMIT

The standing rule — an independent review of each phase's diff — caught
three:

* **A writer could mint a node born `ACCEPTED`.** `write_node` took any
  schema-valid status, and `POST /nodes/write` passes status from the
  client — self-promotion past his word, one request wide. A node cannot be
  born promoted: `status=ACCEPTED` is now refused at the write site with the
  reason, and ACCEPTED arrives only through `approve()`. A test pins it.
* **A read-modify-write race on node numbering.** This server answers on
  threads, and the weekly-pull audit already lost 7 of 12 concurrent writes
  to exactly this shape (load, count, append). Two concurrent writes could
  mint the same node id. One process-wide reentrant lock now covers every
  mutation — reentrant because the write site's reinforcement branch calls
  `remember()` while holding it. A test runs 8 concurrent writes and
  asserts 8 distinct ids.
* A dead `if … pass` in the auto-linker, removed.

## 7. WHAT REMAINS OPEN, STATED

* **Phase E is not built** — nothing calls the write site, the linker or the
  queue on a write or a timer. Every loop that runs, runs by hand.
* **His promotion question stands** — the queue holds until his word.
* **The five namespace collisions** still await his ruling.
* The **contradiction scope is deliberately narrow** (opposing verdicts,
  same subject); widening it is a decision about inference, not wiring, and
  it is his.
* `refs` are handed in by callers; the runtime does not yet compose a node's
  refs from its own steps automatically — that wiring belongs with E, where
  the runtime's output would flow into the graph on its own.
