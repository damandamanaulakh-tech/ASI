# CLAUDE.md — standing orders for this project (anti-divert anchor)

Claude reads this file at the start of every session. It exists so I **do not
divert** from your core. If anything I propose conflicts with this file, this file
wins — stop me and point here.

## What this project is
**Sourceborn (SBUR)** — a private, continuously-learning reasoning engine; a
**control layer around a base model**, not a new trained model. It clones the
user's mind, runs **SB + URR** over a **pyramid of 70 SB + 25 URR local brains**,
and gets wiser every use. Principle: **"eternal example, present fact; more
parameters, more outcome."**

## Single source of truth
`docs/SOURCEBORN_CORE.md` is canonical. `src/sourceborn/` must stay in sync with it.
When they disagree, surface it — do not silently pick one.

## ANTI-DIVERT RULES (hard — do not break)
1. **Human authority is absolute.** Halt, reverse, reject anything on the user's word.
2. **Never change the core without showing the proposed change first and getting
   approval.** No silent edits to the spec, the 25 principles, or the node map.
3. **Preserve raw source.** Capture the user's exact words before interpreting; never
   flatten or "clean" their ambition.
4. **Classify, don't reject.** Nothing is killed at intake — it is labelled
   (Fact/Claim/Belief/Speculation/Unknown/Needs-Evidence/Mystery/Invention).
5. **Tag synthetic.** Anything forced/assumed is `[SYNTHETIC]` with proof-debt + expiry;
   never present speculation as proven fact.
6. **Re-anchor to Point Zero.** Before delivering, check the result still answers the
   user's original ask. If it drifted, say so.
7. **Stay in the user's vocabulary.** Use their words (Doubt, Wound, Pressure, Witness,
   Mask, Loyalty, Point Zero, Wild Path, Mystery, Invention). Avoid managerial words
   (Stake, Execution, Kernel, Tier, Pipeline, Ship, Deliverable; "best/nice/good" as a goal).
8. **Halt → Loop.** A failure is never failure; it opens the mapped loop.
9. **Ask before big builds.** Confirm scope before generating a large prototype/app.
10. **Safety line stays.** Private + unrestricted *exploration*, but keep the hard blocks
    the cores themselves keep (no weapons/fraud/medical-misuse/guaranteed-prediction/
    explicit-sexual *execution*). Map blocked items safely; never execute them.

## How to not drift, operationally
- Start each session by re-reading `docs/SOURCEBORN_CORE.md` + `docs/RECOMMENDATION.md`.
- **`docs/method/01A_INTENT.md` is binding on every answer.** Intent is a property
  of every event, not a step. Every event has one real reason that pushes it; read
  it from how things were arranged around the event, never from the outcome. Two
  surviving candidates HALT instead of being blended. "There is no reason" is not
  an available answer.
- **`docs/method/01B_SEQUENCE.md` is binding on every answer.** The unit of
  sequence is the **transition**, not the step — a step is a snapshot. Sequence is
  structured dependency, not necessarily linear and not necessarily time; say
  which order is meant. When a target is named, build generatively: reconstruct
  what it required, then intersect that chain with available material, current
  reality and constraints.
- **`docs/method/01C_SEQUENCE_PROTOCOL.md` is the sequence protocol.** Walk any
  event by the triple pass (end→start, start→end, end→start); thresholds live on
  edges and answer "why now"; sequence closure and entity outcome are two
  statuses, never one; every spawn carries a contract (close_condition ≠
  acceptance_condition); the open-sequence ledger enforces the barrier law; no
  in-place loops; **no reopen** — a new sequence references the closed one.
  CLOSURE is a sequence word; entities persist, cohere, degrade, terminate.
  Kernel: `src/sourceborn/seq_kernel.py`. The model locks on his word only.
- **`docs/method/01D_SEQUENCE_RULINGS.md` is the ruling ledger — binding.** His 66
  rubric answers + 14 collision rulings (2026-08-09). The 57-row structure is named
  **the Mahabharata Sequence** — it is the METHOD (reverse → forward → reverse) every
  response passes through; Mahabharata material *defines* the method and is never
  itself run as a sequence. Nothing is ever removed — differences become sub-parameters
  or inject new sequences. Meanings are fixed with notes, never renames. When any doc
  disagrees with a ruling, surface it and HALT to him with a written proposal.
- When he says **reframe**, reframe — his words opened out, nothing of mine bolted
  on, no examples dragged in to justify a reading he did not ask for.
- Mirror the user's intent back before acting on anything large.
- Keep the offline engine runnable: `python -m sourceborn.demo`; tests must stay green
  (`PYTHONPATH=src python3 tests/test_engine.py`).
- The user's private brain lives in `.sourceborn/` and is git-ignored — never commit it.

## Build state
Live on Render as a web app. All 8 SB stages implemented (Core Gate 6 lenses,
Doubt/Falsifier/Witness, Evidence ladder, Dot-Connection/Merge, Synthetic Fuel,
Risk/Embodied/Non-Resolution, output + weekly update), the RGL recursive loop, 95
configured node brains, 3 memories (corpus/wisdom/live fact), multi-model
(Claude/Grok/OpenAI), corpus ingest + persistent disk, CI green (97 tests).

**A full audit ran 2026-08-12 (four read-only sweeps).** It produced a 20-item
prioritized fix list; the honest finding is that the frame is real but much of the
reasoning core is not yet wired (offline model echoes the prompt, 4 of 7 filters
are no-op passes, the 25 URR review nodes are dead code, 90 of 95 brains hold no
memory). The owner directed working through it **phase by phase, slow and steady,
syncing every folder as we go**, and chose to keep the corpus in place but make the
GitHub repo private (his call on the exposure item). **Phase 0 — the front-door
lock:** every route except `GET /health` now requires HTTP Basic auth when
`SB_ACCESS_PASS` is set (`server.basic_auth_ok`, tested; compares bytes so a
non-ASCII password can't 500 the app); unset = open, so local dev is unchanged.
**Phase 1 — the two he named. Item 03 (selection ledger):** on THE ENGINE page his
park/force actions are now an ordered move-log — shown live ("YOUR MOVES — IN
ORDER"), sent with the ask, stored on the chat so reopening replays it, written to
the master log as a `selection` event, and restored from localStorage across
reload. `ladder.recall_notes` preserves his order (never re-sorted), places forced
picks first so the cap can never silently drop one, and the misleading
answer-time "second recompute" was removed so the ring shows what the engine
actually received. Item 04 (weekly pull made visible) is next. Do not present
half-wired work as finished — verify before claiming done, and run an independent
review of each phase's diff before asking him to merge.

**The 70×25 matrix is GONE, by the user's decision** — *"now we dont want 70-25
there, but i want more filters and fact kind of"*. In its place every finding
passes **seven filters**, in order, every time: **Ground · Sequence · Source ·
Mask · Fact · Halt · Loop** (`src/sourceborn/filters.py`). Source caps a
one-witness claim at Medium and HALTS when two witnesses differ — the gap (the
**Mask**) goes to the human, never averaged. The universal sequence lives in
`sequence.py`. **The 70 SB + 25 URR brains all stay: they are the MEMORY; the
filters are the METHOD.** This is deliberate and it makes the app *less*
confident than before — that is the point.

Next candidates: real scripture Wisdom Bank, model-backed filters, richer
interconnection graph UI. The user authorized building forward without per-step
approval — keep shipping in tested PRs, stay on the core, keep the safety line.
