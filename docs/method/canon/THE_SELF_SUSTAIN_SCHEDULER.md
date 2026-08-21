# PHASE E — THE SELF-SUSTAIN SCHEDULER

**His order:** *build phase E* — the last phase of his SELF-SUSTAINING
EXECUTION FLOW sheet, governed by his own staging law:

> **Manual Mode Now → Semi-Auto → Auto-Sustain Target**

It is STAGED, not a switch — his correction to my auto proposal, which had
asked whether to switch auto on. So the machinery ships whole and the mode
ships **MANUAL**: deploying Phase E changes nothing until he lifts the mode,
and lifting it is HIS action, recorded as its own append-only row carrying
what it was before.

**Date:** 2026-08-21. Module: `src/sourceborn/autoloop.py`; one wiring line
in `scheduler.py`. Routes: `/auto`, `POST /auto/tick`, `POST /auto/mode`.

---

## 1. WHAT A TICK IS

One bounded pass of the loop his sheet draws:

```
material arrives          handed texts · inbox files · (AUTO_SUSTAIN)
      │                   the previous tick's own written nodes
      ▼
Phase B runtime           runtime.run — all eighteen, answer: None
      │
      ▼
refs composed             autoloop.refs_from_run — FROM THE RUN'S OWN
      │                   STEPS (the wiring Phase D left stated as open)
      ▼
Phase D write site        nodegraph.write_node — his five conditions;
      │                   a refused write stays refused; a match is
      │                   reinforced, never duplicated
      ▼
Phase C engine            combine.run over the tick's material;
      │                   delta() against the tick before
      ▼
THE REPORT                appended; the report is the product
```

## 2. THE FOUR LAWS OF THE TICK — EACH TESTED

1. **THE GATE DOES NOT MOVE.** A tick may seat, link, combine, predict. It
   may NOT promote, answer, kill, add a parameter, or write his count
   ledger. Enforced STRUCTURALLY: no `approve`, no `kill`, no `growth.add`
   exists in the module's code, and a test reads the source. The queue for
   him fills; `promoted` cannot move from here; a tick report has no answer
   field at all.
2. **BOUNDED, AND EVERY CAP REPORTED.** Auto + append-only + no delete is
   the main risk — an unbounded tick would fill his base with rows nobody
   chose. 5 items and 40 nodes per tick. A deferred INBOX file is genuinely
   picked up next tick (the cursor never saw it); a deferred HANDED text is
   NOT stored, and the report says it must be handed again — **the first
   test run caught the dishonest line**: claiming "never dropped" for both
   would have been false for the second.
3. **QUIET IS QUIET.** A daemon tick that finds nothing new appends nothing
   — an hourly heartbeat would flood an append-only ledger with noise. A
   HAND tick always appends, because he asked, and "quiet" is an answer.
4. **NOTHING IS UN-PROCESSED BY DELETION.** Inbox files are never removed.
   The cursor is a fold over past reports (name → content hash). An
   unchanged file is skipped and said so; a CHANGED file is a superseding
   reading, processed again.

## 3. THE THREE MODES

| mode | means |
|---|---|
| **MANUAL** (shipped) | the tick runs only when called. The daemon does not drive it. |
| **SEMI_AUTO** | the hourly daemon runs the tick; new material processed within budget; nothing feeds back. |
| **AUTO_SUSTAIN** | his target: the daemon runs the tick AND the previous tick's own written nodes re-enter as ONE prepared example for the engine — **the L4 loop, the only loop whose input is the system's own output** — bounded to the last tick, its delta reported. A feedback pass that opens nothing is the loop finding its own quiet. |

## 4. THE DAEMON THAT ALREADY RUNS

No new thread. The hourly daemon that has driven the weekly pull since
Phase 1 (`scheduler.start_weekly_scheduler`) now also calls
`autoloop.tick_if_due` — **each job in its own try, so a tick failure can
never kill the weekly pull and a pull failure can never kill the tick.** In
MANUAL, `tick_if_due` returns without doing anything, and a test pins it.

## 5. WHAT A TICK IS NOT

**A tick is not a check.** Maturities decay on checks-without-confirmation —
his rule, never age — and a tick checks nothing against the world. So
maturities do not move here; the report carries `maturities_touched: 0` with
the reason. Evidence still arrives from outside, through `check()` and
`remember()`, on his word or a caller's verdict.

## 6. WHERE THIS LEAVES HIS SHEET

**All five phases run:** A locked · B runs · C runs · D runs · E runs (mode
MANUAL). All nine auto loops have their trigger; the ninth (Node-Growth)
still stops at the queue. The discovery audit reads 22 of 23; stage 1 source
lock remains the one PARTIAL.

## 7. WHAT WAITS ON HIM, UNCHANGED AND NOW LOAD-BEARING

* **The mode.** MANUAL until his word — `POST /auto/mode`. Semi-auto first
  is the staging his own sheet names.
* **The promotion question.** The queue holds; `promoted` stays 0. In
  SEMI_AUTO and beyond, candidates will accumulate at the queue — his answer
  decides whether they ever move without him.
* **The five namespace collisions.**
* **Stage 1 SOURCE LOCK** — still discipline, not a checksum; the Phase A
  fingerprint technique is the shape of the fix, and applying it to raw
  source intake is its own piece of work.
