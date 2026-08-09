# 01C — THE SEQUENCE PROTOCOL

**Project instruction. Binding on every walk the engine runs.**
**The model is NOT yet locked — it locks on the owner's word. These are the
corrections he ordered in before locking.**

This document puts the whole sequence investigation and its protocols in one
place: the definition (01B), the triple-pass rule, the four tests, the main-line
structure, the six core objects, the corrected invariants, and the execution
kernel. The kernel is implemented and tested at `src/sourceborn/seq_kernel.py`.

---

## 0 · The rulings this protocol stands on — his words

> "Reverse engineering means end to start, then again start to end and then last
> end to start, whatever work is done for that event is a sequence"

> "everything have unique code running / and loops happen everywhere"

> "so when i talk about sequence, this is the intent and pattern im looking for,
> everything closed, no open node, but 1000000 of inventions, ideas"

> "Krishna is the line of sequence, each character is another sequence on that,
> type remain same, number of sequence can more, From Arjun, Karan, Bheem
> everyone is sequence loop on Krishna main sequence of Mahabharta"

> "but now we have the code & formula to design the brain for computer"

---

## 1 · The triple pass — how any event is walked

The definition of sequence is settled (01B: the unit is the transition; sequence
is structured dependency; not necessarily linear, not necessarily time). The
**protocol** for walking one is the triple pass:

| Pass | Direction | What it does |
|---|---|---|
| **1** | **END → START** | From the result, walk back what it required, link by link, until the chain bottoms out before the visible beginning. Builds the required chain. |
| **2** | **START → END** | Run the same chain forward as a generative sequence — required chain ∩ available material ∩ current reality ∩ constraints. This is the executable walk. |
| **3** | **END → START** | The ledger audit. Walk back once more checking every row: closed, closed, closed. **No open node.** |

**Whatever work is done for that event is the sequence.** Not the visible
episode — the work. The 18 days were the closure window; the sequence ran for
generations (T-4).

---

## 2 · The structure — the main line and the sequences on it

His ruling, opened out:

- **One MAIN SEQUENCE — the line.** The controller's own sequence: the one node
  that holds the full ledger and every early trigger. In the Mahabharata that
  line is Krishna. Nobody else holds more than a fragment.
- **Every character / entity followed is its own sequence, attached to the
  line.** Arjun, Karna, Bheem — each a sequence loop riding on the main one.
- **Type remains the same; the number can grow.** Every rider runs the same
  grammar with its own unique code. Unlimited count, one grammar.

`[READING — the engine mapping]` For the computer brain: the main line is the
engine's controller sequence holding the open-sequence ledger; every node brain,
walk and child task is a rider sequence attached to it. The Krishna-role is the
spec for the controller (T-4 §the code & formula).

---

## 3 · The four tests, and what survived into law

| Test | Entity | What it proved |
|---|---|---|
| **T-1 GRAVITY** | no stake, no chooser | 21 agentic nodes go dark **as one block** → the agentic middle is a regime, not the trunk. Mass-energy is one slot. Boundary may be absent. Trace = memory with no rememberer (orbital decay, CMB). Compression is physical (no-hair). PHYSICAL inheritance lane needed. |
| **T-2 PYRAMIDS** | artifact | **Requirement has no fixed position** — it preceded the entity, held by another system. Formative representation (design) constrains formation. Testing in real stone (Bent Pyramid, mid-build). Verification FAILED its own requirement (every tomb robbed) → feedback ended pyramid-building. Role: same matter, different sequence identity. Actor attribution mandatory. |
| **T-3 BRAIN** | self-modelling | Four clocks nested (evolve/grow/develop/memorize). Thresholds are the entity's basic unit (−55 mV, prediction error, critical periods). Trace ≠ memory (traces that don't retrieve; retrievals without traces). Six memory types dissociable by lesion. **The brain has no validation gate** — science/courts/citation are the prosthesis; putting the gate inside the engine is the novelty. Learning = migration of the re-entry point. Formative representation needs no designer (DNA). Self-repair exists → controller may be SELF. |
| **T-4 MAHABHARATA** | the era + the controller | **Nothing that closes in the closure window was opened in it.** Declared close conditions (vows, boons, curses) are ledger rows opened generations early; **a vow outranks the local rules of the sequence where it closes** (the three rule-breaks, all vow-closures). The controller waits for the threshold (the cheer haran), removes blockers in advance (kavach-kundal), hands the executor the end first (the reverse walk as gift), brings all open rows to one synchronization field, **and includes his own closure in the ledger** (Gandhari's curse). A closed sequence is never reopened (Karna's refusal is the law working correctly). The closure packet became the Book — compression that expands. |

---

## 4 · The six core objects — the corrections, as given

### 4.1 THRESHOLD — separated from trigger, carried on edges

**TRIGGER** = something changed / was observed / occurred.
**THRESHOLD** = the condition that must become true before the transition is
permitted to fire. A condition can exist for years without causing a
transition — threshold answers **"why now?"**

Every executable edge carries:

```text
EDGE {
    source · target
    activation_event
    threshold_condition
    evaluator · evaluation_time
    status
}
```

Nine threshold types, surviving every domain:
**VALUE** (voltage, temperature) · **RANGE** (enter/leave viable band) ·
**TIME** (deadline, duration, age) · **EVENT** (collision, message, child
returns) · **COUNT/QUORUM** (N children closed, majority) ·
**CONFIDENCE/PROOF** (evidence ≥ required) · **STATE** (entity enters X) ·
**ABSENCE** (expected thing has not occurred) · **COMPOSITE** (A AND B, A OR B,
A unless C).

The recheck contract — answering "availability re-checked WHEN?":

```text
RECHECK WHEN: child returns OR resource-state changes
              OR deadline reached OR external event received
```

Thresholds live **on edges, not as another numbered stage.**

### 4.2 SEQUENCE CLOSURE ≠ ENTITY OUTCOME — orthogonal, both recorded

*Did the sequence finish?* and *what happened to the thing followed?* are two
different questions:

| Sequence | Entity |
|---|---|
| destruction: CLOSED SUCCESS | TERMINATED |
| repair: CLOSED FAILURE | persists, DEGRADED |
| pyramid build: CLOSED SUCCESS | INSTANTIATED / persisting |
| gravity: CLOSED | NOT APPLICABLE |

**ENTITY OUTCOME values:** persists · modified · degraded · repaired ·
transformed (identity decision required) · split · merged ·
consumed/incorporated · terminated/destroyed · new entity instantiated ·
absent · unknown · not applicable.

The Closure Packet carries **`sequence_closure_status` + `entity_outcome`** —
never one status doing both jobs.

### 4.3 THE SPAWN CONTRACT — a child must know why it exists

```text
SPAWN_CONTRACT {
    child_sequence_id · parent_sequence_id · parent_node_id
    spawn_reason
    requested_result · return_schema
    scope · context_snapshot
    controller
    activation_condition
    close_condition          ← when the child's own work is done
    acceptance_condition     ← when the parent's requirement is met
    required_or_optional
    epistemic_requirement · proof_depth
    dependencies
    deadline_or_time_condition
    termination_policy
}
```

**close_condition ≠ acceptance_condition.** The water example: child "find
water" closes legitimately as CLOSED FAILURE ("search completed, no water
located") while the parent's requirement stays unresolved — and the parent
spawns the next child. The distinction is essential.

### 4.4 THE OPEN-SEQUENCE LEDGER — the enforcement mechanism

```text
Sequence  Parent  Parent Node  Required?  Controller  Contract  State
S₀        ROOT    —            YES        AI          C₀        OPEN
S₀.1      S₀      DEP-17       YES        self        C₁        CLOSED
S₀.2      S₀      DEP-17       YES        external    C₂        OPEN
S₀.2.1    S₀.2    AVAIL-2      YES        self        C₄        OPEN
```

The sync gate stops asking vaguely "are all children closed?" and queries:

```text
required_open_children(parent_node) == 0
AND all_required_returns_accepted == TRUE
→ only then: PARENT NODE CLOSES
```

> **"Without the ledger, closure is philosophy. With the ledger, closure
> becomes machine-executable."**

### 4.5 DRIVER ORIGIN — Want restored, beside Need, never inside the spine

Want is not a universal sequence stage. It is one possible **reason a sequence
is opened** — and it is not Need:

**NATURAL DYNAMICS** · **NEED** (viability imposes) · **WANT** (preference
creates a desired difference) · **EXTERNAL DEMAND** (command/request/obligation)
· **GOAL** (represented target) · **OPPORTUNITY** (possible, worth exploring) ·
**CURIOSITY** (uncertainty itself motivates) · **DAMAGE/DEVIATION**
(restoration) · **RELATIONAL** (produced by interaction between systems).

Hunger → NEED. Spicy food → WANT → new sequence (never joins the eating one).
Pyramid → GOAL + EXTERNAL DEMAND. Pure research → CURIOSITY. Gravity → NATURAL
DYNAMICS, no fake requirement.

### 4.6 CONTROLLER — mandatory on every transition

**NONE/NATURAL** · **SELF** · **DISTRIBUTED SELF** · **EXTERNAL** · **JOINT** ·
**META-CONTROLLER**.

Self-repair is representable only once controller is mandatory: remyelination →
controller = SELF/distributed → spawn repair sequence → close. Surgery →
EXTERNAL. **Homeostasis is not one immortal loop** — it is repeated
threshold-bounded regulation episodes, each spawned on a crossing and each
closed on return to band.

---

## 5 · The corrected invariants

1. **THE BARRIER LAW** (replacing "no sequence can move while open," which would
   wrongly freeze parallel branches):

   > **NO DEPENDENT EDGE MAY CROSS A CLOSURE BARRIER WHILE A REQUIRED
   > PREDECESSOR / CHILD CONTRACT REMAINS OPEN.**

   A parent may remain OPEN/**SUSPENDED** at the barrier while required children
   execute; its independent branches keep moving.

2. **No in-place loop.** UNRESOLVED → suspend at barrier → spawn new sequence →
   child closes → return → re-evaluate. The regression "LOOP (same sequence
   continues)" is struck from the grammar.

3. **No reopen — the word is removed from the grammar.** S₀ closed + new
   evidence → CREATE S₁ with `S₁.references = S₀`. (T-4: Karna's refusal is this
   law behaving correctly.)

4. **CLOSURE is reserved for sequence execution.** Entities do not "close" —
   they **PERSIST, COHERE, DEGRADE, TERMINATE** (identity continuity criteria
   decide TRANSFORMED). The physical phenomenon may continue while the
   analytical sequence about it must close. No contradiction once the words are
   separated.

5. **Encounter is conditional.** RELATION EXISTS? → yes: COUPLING · no:
   ENCOUNTER/ACCESS → COUPLING. No forced node.

---

## 6 · The execution kernel

```text
STATE
  ↓
DRIVER / EVENT
  ↓
THRESHOLD SATISFIED?
  ├── NO → dormant / await declared recheck condition
  └── YES
        ↓
      NODE — CAN NODE CONTRACT CLOSE?
        ├── YES → CLOSE NODE → NEXT EDGE
        └── NO  → CREATE SPAWN CONTRACT
                   → REGISTER CHILD (ledger)
                   → CHILD EXECUTES → CHILD CLOSES
                   → CLOSURE PACKET → LEDGER UPDATE
                   → PARENT RE-EVALUATES
                        ├── resolved   → CLOSE NODE
                        └── unresolved → NEW CHILD
```

And at the end of every sequence:

```text
SEQUENCE CONTRACT SATISFIED
→ ENTITY OUTCOME RECORDED
→ ALL REQUIRED CHILDREN TERMINAL
→ TRACE / MEMORY RECORDED
→ CLOSURE PACKET
→ SEQUENCE CLOSED
→ RETURN / ARCHIVE / SEED NEW SEQUENCE
```

**Implemented:** `src/sourceborn/seq_kernel.py` — thresholds on edges, the spawn
contract with close vs acceptance, the ledger with the barrier law, sequence
closure separated from entity outcome, no-reopen enforced, driver origins and
controllers as fixed vocabularies. Run `PYTHONPATH=src python3 -m
sourceborn.seq_kernel` for the water example end to end.

---

## 7 · Open — waiting on the owner

- **The model lock.** These corrections are in; the lock is his word.
- **T-5 — the universe chain at true resolution.** *"Formation of universe to
  earth to human are vague think must have may b 30 step in sequence"* —
  universe → galaxy → planet → human → the 3-lakh-year human line to now,
  ~30 real steps, each with its unique code, loops marked, triple-passed.
- **Relational requirement (8c)** — named, still untested by any T.
