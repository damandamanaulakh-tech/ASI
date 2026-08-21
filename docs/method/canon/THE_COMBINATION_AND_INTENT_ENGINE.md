# PHASE C — THE COMBINATION + INTENT ENGINE

**His order:** *build phase C* — the third phase of his SELF-SUSTAINING
EXECUTION FLOW sheet, after A (registries + IDs, locked) and B (the runtime
pipeline). His own concept, in his words, is what this engine executes:

> *"concept is simple as much parameters we plug, we will generate more
> pattern and intent"*

> *"as long i keep adding the example, once the basic will over it will start
> making new combinations on new thoughts"*

**Date:** 2026-08-21. Module: `src/sourceborn/combine.py`. Routes: `/combine`,
`POST /combine/run`.

---

## 1. WHAT EXISTED, AND WHAT DID NOT

Combination generation existed twice — `selfmake` over the repo (pairs only,
by hand) and runtime step 9 over one ask — and intent generation existed once
(`intents.generate`, gated by active containers). Four things did not exist:

* **ROUNDS.** A combination could never combine again. *"New combinations on
  new thoughts"* had no mechanism, because nothing fed a round's output back
  in as the next round's input.
* **A STOP.** Nothing said when generating was finished. The
  loop-until-quiet discipline existed as evidence (`extend()` writes 0 on the
  same material) but not as a loop.
* **THE CHAIN.** A combination arrived bare. Now every candidate leaves the
  engine carrying its prediction (stage 12), its falsifier (stage 17's food)
  and its maturity (stage 18) — testable the moment it exists.
* **STAGE 22 AS A FUNCTION.** "New combination availability" was a by-hand
  diff of generation counts. `delta()` computes it.

## 2. THE FOUR GATES — WHY THE ROUNDS DO NOT EXPLODE

Every ungated cross product in this project has been the wrong answer (6,480
of 6,480 meanings; 2,627 of 3,160 pairs). The engine's gates, in order:

1. **CROSS-ROLE OVER SETS.** A combination's roles are a SET, and a new part
   must bring a role the set does not hold. ACTION × ACTION is one mode
   twice; ACTION + INFERENCE + INFERENCE is the same failure at order 3. Six
   roles exist, so **order 6 is the structural ceiling**.
2. **CO-OCCURRENCE.** All parts must appear together in at least one example.
   A combination nothing exhibited is not available — it is imaginable, and
   the engine does not deal in imaginable.
3. **THE ANCHOR.** Every combination must hold at least one ROW-granularity
   part — a row an actual word reached. Nothing floats on structure alone.
4. **RECURRENCE TO BREED.** An order-2 candidate enters a deeper round only
   at support ≥ 2 — maturity's own RECURRENCE_MIN, his rule 6: one
   interesting event is not a pattern. **One example can never produce order
   3, and a test pins it.** This is what makes *"once the basic will over"*
   mechanical: depth unlocks exactly where material recurred.

**Genuinely new against selfmake:** selfmake's COMBINATION steps stop at
PAIRS. The engine breeds order 3 and beyond — but only where support earned
it, which is his "new thoughts" with the brake built in.

## 3. TWO DEFECTS THE BUILD CAUGHT IN ITSELF

* **The scaffold multiplied.** Seating on a short ask mostly lands at
  CONTAINER granularity — the role's own containers, which are STRUCTURE:
  any two-role text exhibits them whatever it says. Folding that 16-container
  scaffold in turned one two-sentence text into **240 candidates** — the
  cross-product failure through a side door. The fix: a role-event no word
  anchored enters as **ONE unanchored part** (`ROLE->*`) — the role
  happened, and that is ALL the part claims. His rain sentence now yields
  **exactly 1 candidate**: `ACTION->CON-021 + INFERENCE->*` — an ACTION
  seated on his row met an INFERENCE, which IS the rain example's shape as
  selfmake found it.
* **Duplicate signatures burned cap slots.** Two parents can breed the same
  set in one round; the pool now holds one entry per signature, or a round's
  cap fills with copies and under-reports what opened.

## 4. HONESTY RULES

* **Maturity is fed honestly.** Co-occurrence is SUPPORT — an input, never a
  confirmation. An unchecked candidate reads UNTESTED whatever its support,
  because "nobody checked" is not "it held".
* **Evidence is handed in.** `check()` moves a maturity only on verdicts from
  outside: `together_again` confirms the REPETITION prediction (the row that
  names the candidate's own parts, so it discriminates by construction);
  `apart_events` is what the falsifier watches. The engine never goes looking.
* **The kill is on request only.** `kill=False` is the default — his word:
  *"nothing needs to kill for now, add everything and generate."* The kill
  still runs when asked, through `intent_ledger.kill`, and a test proves both.
* **No silent caps.** A round cap that bites reports exactly how many
  candidates it dropped, every round.
* **The engine never writes.** No ledger row, no file, no parameter — a run
  is a report, and a test reads the module's own source (the Phase A
  technique) to prove no write path exists in it.
* **Corpus runs go through selfmake's OWN harvest** (`paths=`), so a corpus
  run and a selfmake run can never disagree about what a file exhibits.

## 5. HIS NINE AUTO LOOPS — OWNED AND NOT OWNED

`loops()` states it so C cannot quietly claim loops it does not own:

| loop | state |
|---|---|
| **Combination** | **RUNS — this engine** (started by hand; the trigger is E) |
| **Intent** | **RUNS — this engine feeds it per candidate** |
| Evidence | RUNS as prediction; checking is handed in |
| R-F-R | RUNS (patterns.rfr_check, runtime step 13) |
| Next-Sequence | RUNS (discovery.close, runtime step 18) |
| Retrieval | DEFINED — reading by similarity is Phase D |
| Contradiction | DEFINED — finding the links is Phase D |
| Memory Reinforcement | WAITS FOR D — the per-node chain of readings |
| Node-Growth | WAITS FOR D **and his answer** — the promotion policy question is still open |

An engine that claimed all nine would be lying about four of them.

## 6. WHERE IT IS WIRED

* **Runtime step 9** now hands its seatings to this ONE engine, so the
  runtime's view and the engine's can never drift — the same rain ask yields
  the same one candidate both ways, and a test pins the equality.
* **The discovery audit reads stage 22 RUNS** — 21 of 23 now run; stages 1
  (source lock) and 5 (relation graph) are the remaining PARTIALs, and both
  are Phase D's business.
* The arrow chart shows **A locked · B runs · C runs · D, E NOT BUILT**.

## 7. WHAT REMAINS OPEN, STATED

* **The trigger is manual.** `combine.run` and `delta()` run when called;
  nothing calls them on a write or a timer. That is Phase E, and it is the
  scheduler's gap, not this stage's.
* **Row-level seating precision** is still the open part of the seating
  itself — the engine inherits it. On corpus runs, neighbouring containers
  seated by generic words produce candidate families that differ by one
  container; the support numbers are honest but the rows are coarse.
* His **promotion policy question** and the **five namespace collisions**
  are still unanswered; Phase D needs the first.
