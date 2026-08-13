# CLAUDE.md — standing orders for this project (anti-divert anchor)

Claude reads this file at the start of every session. It exists so I **do not
divert** from your core. If anything I propose conflicts with this file, this file
wins — stop me and point here.

## What this project is
**Sourceborn (SBUR)** — a private, continuously-learning reasoning engine; a
**control layer around a base model**, not a new trained model. It clones the
user's mind, runs over the frame HE set — **1 - 10 - 8 - 40** (1 system · 10 segments ·
8 containers each · 40 named sub-parameters per container = 80 containers,
3,204 named) — and gets wiser every use. Principle: **"eternal example, present fact; more
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
(Claude/Grok/OpenAI), corpus ingest + persistent disk, CI green (138 tests).

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
actually received. **Item 04 (the weekly pull, visible and cumulative):**
`scheduler.run_weekly` is the ONE job the hourly daemon and the manual button both
call, so a hand-pull no longer skips the novelty pass; every run is kept as its own
dated file under `<SB_ROOT>/weekly/`, created with mode `"x"` so the filesystem
guarantees no run is overwritten (a check-then-write lost 7 of 12 concurrent pulls
— this server answers on threads *and* runs a daemon thread calling the same
function); `GET /weekly` (paged via `?offset=`) + `GET /weekly/file?name=` serve
the ledger; the dashboard has a real panel (pill click or *Weekly pull*) with an
*Older runs* page and the true kept count — counted by `listdir`, never by parsing
a page, so it cannot start under-reporting; the pill reads three states (never
run · overdue · current) instead of saying "active" forever after one run; the
label is composed ONCE server-side (`_weekly_phrase`/`status()["state"]`) and only
displayed by the pill and the MY PAGE row, which used to be permanently blank; and
a failed novelty pass, a failed history write and a corrupt run file are each
reported rather than swallowed. Every value the panel interpolates is escaped —
run files can arrive from a restored backup, so they are untrusted input.

**The queue lives in the repo: `docs/AUDIT_2026-08-12_WORKLIST.md`** — all 20 items
verbatim with live status, updated in the same commit that closes one. Items 05–08
(real model / the four dead filters / the URR nodes / the 90 empty brains) are the
ones that make it actually reason; nothing closed so far has changed that. Do not
present half-wired work as finished — verify before claiming done, and run an
independent review of each phase's diff before asking him to merge.

**THE MACHINE IS NOW PLUGGED IN (2026-08-13, on his word "so plug it in the
system / make change in al file where its required / no place holder, skipping
data / 3072 is the count").** His canon is filed verbatim at
`docs/method/canon/THE_MACHINE_AS_HE_STATES_IT.md` and
`docs/method/canon/THE_2560_PLACED_ON_THE_ARCHITECTURE.md`, and his rulings are
in `docs/method/01D_SEQUENCE_RULINGS.md` §20. What was built:
`micro.py` splits every sentence into a **micro-sequence** carrying his exact
field list (ENTITY · RELATION · ACTION · NEGATION · INFORMATION OBJECT/STATE ·
EXPECTED vs ACTUAL · TEMPORAL RELATION · DEPENDENCY · EXPECTATION DIFFERENCE ·
POSSIBLE HUMAN EFFECT · INTENT · REPETITION LINK · PATTERN CONTRIBUTION), with
**intent NEVER concluded from one event** and **his feeling never picked**;
`patterns.py` keeps every micro-sequence, finds the arrangement that recurs as
the **union of steps across linked events** (each step carrying its own support —
his own S2 has no disclosure fact and S3 no resource fact, yet both belong),
surfaces a **PATTERN-CANDIDATE at 5 repeats** (his ruling; the *reducing* rule is
MY reading and says so on screen), runs **R-F-R / Doubt before he ever sees it**,
holds **the six that never collapse** with five of them empty and his, offers all
**six of his actions** (approve · reject · rename · split · combine · redefine),
and enforces **NO REOPEN** — every edit appends a write-back referencing the
version it acted on and the prior version is kept whole; `router.py` selects
mechanisms **FROM the structured problem** (never the reverse) and carries his
SEG→flow placement; `/reading` is the microscope — his RUBRIC VIEW with the
editable fields, the answer last. **Item 20 is CLOSED by "3072 is the count"**
(the 80/2,560 base HALT is answered) and **item 18 is placed by him** at the
write-back sequence. One occurrence can never become a pattern — a test exists
whose only job is to prove that. **OPEN SEAM, surfaced not decided:** "rubric
means paramters the 3000" against "Human Parameter ≠ Rubric"; nothing was moved.

**HE CORRECTED THE PARSE ITSELF (2026-08-13) — `senses.py`.** His teaching is
canon at `docs/method/canon/LEFT_AND_NOTHING_HIS_CORRECTION.md`: **"left" is not
departure, it is what REMAINS with the person**; **"nothing" is not zero, it is
zero MATERIAL return while the emotional/experiential return stays**; and
**"Good or bad, memories are always emotional count for human"** — so valence is
never a stand-in for value (`pleasantness ≠ importance`, `pain ≠ worthlessness`).
`senses.py` is USER-DEFINED SEMANTIC CONTEXT, seeded with his four teachings in
his own words. A sense actually changes the parse (`SENSE-001` blocks the
`participation` class off "left", and the block is recorded), **both readings are
always kept** so the screen shows what the machine would have thought, and the
raw sentence is never altered. `return_reading()` grades all eight of his RETURN
dimensions and an unstated one says *not stated*, never zero. `memory_reading()`
returns valence and significance as TWO fields that never collapse. **He named a
danger himself — "a person who gets nothing in return is automatically good" is a
dangerous overgeneralization — and that refusal is stored ON the rule that could
have produced it**, so it can never quietly grow into it. Edits are write-backs
with NO REOPEN; a rejected sense is CLOSED, never deleted. `/senses`,
`POST /senses/teach`, `POST /senses/reject`. **Left for him:** he pointed out his
pattern is a LOOP, not a line (care → responsibility → action → moments → memory
→ meaning → renewed responsibility); the pattern record is still an ordered
chain, and making it cyclic waits on his word.

**HIS FRAME IS 1-10-8-40, AND THE 70-25 IS OFF THE SCREEN TOO (2026-08-13).**
He caught it still rendering after he killed it: *"we quit 70-25 things and adopt
new frame work of 1-10-8-40 / why still it show 70-25"*. He was right and it was
my failure. `human_registry.py` loads **his own document**
(`ASI_Claude_Parameters.docx` — HUMAN FUNCTIONAL REGISTRY v1.0) whole:
**10 segments · 80 containers · 3,204 named sub-parameters · 40 universal
filters · 12 operating states · 20 failure classes · 30-step operating chain**,
parsed with **zero containers disagreeing with their stated target**. Every name
is HIS. `data/human_registry.json` is the file. Three more of his corrections,
all from the same message: **(1)** the ENGINE PYRAMID now draws his ladder from
that registry, `URR n/25` is gone (it was a 0-to-7 filter count wearing a 25
label), and "70×25 URR matrix" is now "the seven filters"; **(2)** every held
node's ask used to read identically — SB-55 and SB-56 asked for the same thing
and neither said what it was doing — so `_walk_ask` now carries **the node's own
job and the node's own finding** first; **(3)** the node walk showed a
*description* of the work ("raw source locked untouched: 77 chars") with the
content nowhere, so `NodeStep` now carries **job · took · produced** and SB-01
prints **the actual Point Zero text** he wrote, at every node, so he can correct
it. `/registry`, `/registry/container?id=`, `/registry/activate?q=`. THE READING
matches against all 3,204 with IDF weighting (a word in forty of his names is
weaker evidence than a rare one) and prints **his names, his container notes and
what modulates them — never bare ID numbers**.

**HUMAN MEANS THE BODY, NOT THE BRAIN (2026-08-13) — `domains.py`.** His
ontology correction, canon at
`docs/method/canon/HUMAN_IS_THE_BODY_NOT_THE_BRAIN.md`: **Human = the physical
human — body, appearance, biological condition, safety, survival,
ageing/life-extension, physical capacity. Human is NOT the thinking/memory/
reasoning brain.** MEMORY · EMOTION · REASONING · MORALITY · RESPONSIBILITY are
each ≠ Human physical and belong to other brains. He also found that his own
registry is a **mixed organism+cognition model**, so all 3,204 must NOT be
treated as the Human bank — and he ordered the split made **without deleting the
original source records**. So `domains.py` is an OVERLAY: his document stays
byte-for-byte, and the overlay says which brain each container serves. His eight
node classes are real (HUMAN BODY · BRAIN/MIND · RELATION/AFFECT · VALUE/WISDOM ·
RULE/DUTY/ASI · RESULT/CONSEQUENCE · ATTENTION/GOAL · EXCLUSION/BOUNDARY); all 80
containers are classified; **11 are marked MIXED with the reason, including
CON-015 which HE flagged himself** — marked and surfaced, never resolved by me.
`route_words()` is his arrow chart executable. `HIS_CONTAINER_TARGETS` holds the
containers he named by hand (safe→CON-006, alive→CON-001+CON-008,
keep-working→CON-007) because lexical matching can never find them — they are
labelled **HIS ASSIGNMENT** wherever shown. `enforce_scope()` means a container
can only be reported under HUMAN BODY if a word actually routed there, and
anything that fails is moved to `out_of_scope` **with the reason kept**, so his
first machine reading stays visible beside the corrected one. **"not the brain"
is an explicit boundary**: that layer is reported out of scope, never as a hit.

**SURFACE ≠ SYSTEM, AND NOTHING IS UPGRADED (2026-08-13) — `claims.py`.** His
rice/MBA test, canon at `docs/method/canon/DO_NOT_JUDGE_THE_VISIBLE_THING.md`:
*"The ASI should not collapse all of that into 'MBA = success.'"* Four claim
statuses are now real and **nothing is ever upgraded** — a figure he stated is
`SOURCE-ASSERTED / NOT VERIFIED HERE`, a causal phrasing is a `CAUSAL HYPOTHESIS`
carrying all twelve of his alternative causes (experience · market timing ·
capital · relationships · execution · location · demand · distribution ·
risk-taking · team · previous knowledge · luck), an absolute is
`USER VALUE / GENERALIZATION` and not evidence, and a path-not-taken is a
`COUNTERFACTUAL` that must never conclude entrepreneurship beats employment.
`outcome_note()` enforces **HIGH REVENUE ≠ HIGH PROFIT ≠ GOOD BUSINESS** by
reporting what was **not stated** rather than assuming it good. **`judgment_gate()`
is the thing he asked the Rubric Pyramid to FORCE**: his nine steps — VISIBLE
THING → DO NOT JUDGE YET → FIND SYSTEM → CAPABILITIES → INPUTS → EXECUTION →
RESULTS → COMPARE ALTERNATIVE EXPLANATIONS → THEN JUDGE — each reported met or
unmet with evidence. On his own sentence it returns **JUDGMENT NOT SUPPORTED
YET**, because the one step his own reasoning skipped was comparing the
alternatives. His five patterns are stored with the marks HE gave them (3
checked, 2 unchecked). `domains.py` gained his seven new node classes, and on
this sentence **HUMAN BODY does not fire at all** — which is what he said should
happen, and is the proof the body/brain split holds.

**SAME ACTION / CHANGED FUNCTION, AND THE MASK BY OBSERVER POSITION
(2026-08-13) — `repetition.py`.** From his fictional father/door test; he chose
both himself ("go for 1 & 3"). Canon:
`docs/method/canon/SAME_ACTION_CHANGED_FUNCTION.md`. **(1)** His principle
*"identical physical action ≠ identical functional role"* — CHECK #1 acquires the
information, CHECK #2-5 cannot acquire what #1 already did. The pattern engine
was structurally blind to this because it keys on CONTENT and five checks have
identical content; the difference is **ordinal position**. `read_repetition()`
adds that axis, `position_signature()` gives the first and later occurrences
**different addresses** so the pattern layer can see a difference where the words
show none, and what the later checks ARE doing is held open with his six
candidates and **none chosen**. A later occurrence is only ruled out from
acquiring when the source says the actor already knows; otherwise it stays OPEN.
**(2)** BEHAVIOR ≠ MEANING — `read_views()` separates ACTOR from OBSERVER and
**reuses Filter 3 / Source rather than inventing a rule**: two witnesses who
differ HALT, the gap goes to him, never averaged, neither reading preferred. One
view caps at Medium. **A browser caught a bug the unit tests missed**: the engine
splits an ask into sentences, so the count (sentence 1) and the knowledge state
(sentence 3) never met and the app said "not supported yet" on the very example
it was built for — both readings now run at ASK level and a test pins that.

**THE PYRAMID IS BUILT, BECAUSE HE WROTE IT AND I HAD CALLED IT MINE
(2026-08-13) — `asi_pyramid.py`, `/asi`.** On the Samrath sentence I reported
"the machine, today: 0" beside "MY READING: 51" and he cut it down: *"what the
fuck is machine today / who the hell is that, r u fucking that much drifting /
**my reading u shit that is ASI / which u supposed to build**"*. He was right —
there is one system, and labelling the real reading *mine* while leaving the
engine at zero was drift with an excuse on it. He then wrote the answer himself,
and it is canon at `docs/method/canon/THE_PYRAMID_HIS_ANSWER.md`. **It is now
executable and it returns HIS numbers, not near them:** 7 STRONG /
SOURCE-GROUNDED + 11 CANDIDATE / INFERRED = **18 of 3,204 (0.56%), 3,186
inactive** — the same 18 flat IDs, the same tiers. **His flat addressing
`SB-HFR-P0001..SB-HFR-P3204`** is the spine: he derived it by hand and all 18
numbers he cited land exactly on the name he gave them, all 8 container ranges
match, including the two containers holding 42 instead of 40 (CON-042, CON-057).
Built: **the split** (PRIOR/REPEATED against CURRENT/TODAY — *"not one flat
sentence"*), **the SAME EVENT SHELL** held ONCE with two routes (`GO_TO_SCHOOL`
never changed; the condition around it did), **his tiny-words table** as the
actual parser (never · always · but · today · birthday · very · happy · went),
**CRYING ≠ SADNESS** with his seven candidates unresolved and a test whose only
job is to prove P2250 Sadness never enters the set, **CAUSALITY NOT PROVEN** with
his ten hidden branches opened as hypotheses and the fabrication he named kept on
the record as refused, **two intent candidates never blended**, and
**PC-CONTEXT-INTENT-001** with his four guards (`cause = UNKNOWN`,
`generalization = NOT ALLOWED YET`). **It is a mechanism, not a lookup:** the same
shape in different words returns the same 18 with `GO_TO_GYM` as the shell, a flat
report returns 1, and a shape he has not named is reported *unnamed* rather than
empty. Two defects of mine that his sentence exposed and are fixed: the shell
read `GO_TO_GO` (the infinitive taken for the destination), and every positive
word collapsed into his *Happiness* — now "excited" resolves to his own
**P2256 Excitement**, because his v1.0 source says these must not be collapsed;
rows he assigned read HIS ASSIGNMENT, rows I mapped say so and are correctable.
**Still open and stated as absences, not hidden:** 3,186 of his 3,204 have no
route to them — the signal mechanism reaches 18, and the rest need a signal named
for them; and behavioural repetition still has no ordinal-position axis (*"he
always cry"* returns `applies False` in `repetition.py`, which only covers
information-seeking actions). One thing surfaced and NOT resolved: in his chart he
marked **P2564** HIT, in his final list he placed it under CANDIDATE — his list is
followed and his chart mark is carried beside it.

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
