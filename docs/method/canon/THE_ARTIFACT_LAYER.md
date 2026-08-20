# THE ARTIFACT LAYER — reading an object without pretending to read its language

**Source:** `GPT_Black.txt` — a transcript of the other assistant working this same
project. **His instruction: *build it*.**
**Date:** 2026-08-13

---

## 1. WHAT THE TRANSCRIPT WAS, AND WHAT WAS ALREADY HERE

Roughly half of it this core already holds, and built **independently** — from his
workbooks, not from this transcript:

| in the transcript | already here |
|---|---|
| the ten same-king brain-states (19–28) | `SP-19…SP-28` |
| LIVE_INTENT_ENGINE + INTENT_LEDGER | `intent_ledger.py` |
| `NEW WORDING ≠ NEW INTENT` | `intent_ledger.signature()` |
| `PERSONALITY ≠ ONE STATIC PROFILE` | the state-pack law |
| the run counters (2,000 · 100 · 10 · 10 · 0 · 0) | read from his own workbook |

**Eight mechanisms were NOT here.** Checked against the repo: zero hits for
`SYN-MEAN`, `ORIGIN_DISTANCE`, `SG-A`, `PC-TAB-SYN`, `Damage-Aware`,
`Actor-Role Multiplicity`, `future-state`. Those eight are what this module is.

**What cannot be verified, and is not repeated as fact:** everything about the
C-SB repository — PR #2, "7/7 passing", "CI green", the 14-stage `brain/` tree,
"37 changed files". That is another assistant's report of its own work in a
repository this session cannot reach. Source material, not established fact.

---

## 2. THE EIGHT MECHANISMS

**SG-A…SG-J — the visual placeholder registry.** Ten classes that let a sign be
reasoned about by **neighbour · position · repetition · enclosure · damage**
without claiming to know Egyptian. `SG-J damaged/unknown` is explicitly *not a
missing letter to be filled in*.

**SYN-MEAN-001…008 — eight whole-object meanings.** The object as a structure
rather than a sentence. The strongest is **008**: *event compression + identity
anchor + relation map + future memory object*.

**ORIGIN DISTANCE 0…5.** How far a reading has travelled from the visible mark —
mark → grouping → relation → authority → commission → a named person. The law:

> **farther is not WRONG. Farther is MORE INFERENCE, and more inference owes more
> evidence.**

**Nine actor roles, not one.** SUBJECT ≠ REQUESTER ≠ CONTROLLER ≠ AUTHOR ≠ SCRIBE
≠ CARVER ≠ INSTITUTION ≠ BENEFICIARY ≠ AUDIENCE — **each may hold a different
intent.** This core's `actor_name()` reads one actor per event; an artifact event
has nine.

**Future-state reconstruction.** Ask what future state the producer was trying to
create, then work **backwards** to the intent. Everything else in this core runs
forwards only.

**Damage branching.** A damaged region opens four branches that predict *different*
evidence; it is never filled in. A branch that predicts the same evidence as
another is not a branch.

**Twelve PC-TAB-SYN pattern candidates** — the transcript names eight, and each
names where it applies beyond Egypt (contracts, redactions, public filings, repaired
objects). **The other four are recorded as unnamed rather than given names.**

**MATCH SCORE ≠ EPISTEMIC CONFIDENCE.**

---

## 3. THE GATES, AND WHY THEY EXIST

The first build generated **6,480 meanings — the entire cross product**, a meaning
for every combination. That is not a finding; it is the same defect the self-made
COMBINATION steps had before cross-role was required.

Two gates, both readable off the definitions themselves:

- **ROLE_FUTURES** — a role can only work toward a future state it could affect.
  *A carver does not secure a dynasty.* A CARVER now reaches exactly one future
  state (FS-6, a future workshop reproduces the formula).
- **FUTURE_NEEDS** — a future state can only be read off marks that could carry
  it. *An identity claim needs the enclosure.*

```
ceiling, ungated                                  6,480
rejected — role cannot reach that future          3,480
rejected — marks cannot carry that claim          1,176
GENERATED                                         1,824   (28.1% kept)
  restating one of his eight                        118
  genuinely new shapes                            1,706
historical facts established                          0
translations made                                     0
new parameters created                                0
```

Both numbers are reported, so the gate's effect is visible rather than assumed.

---

## 4. WHERE HIS EIGHT MEANINGS SIT ON THE 3,204

They land on parameters that already exist — the growing phase working as he
described it. **29 distinct IDs, 0 parameters created.** The two clearest:

| meaning | lands on |
|---|---|
| **SYN-MEAN-006** External identity memory | **P2519 Intention-to-persist** · P1535 Reminder-setting (external offload) |
| **SYN-MEAN-008** Event compression record | **P0844 Sequence compression** · P1631 Abstract-symbol grounding |
| SYN-MEAN-002 Authority across domains | P2836 Obedience to authority · P2849 Authority/respect value · P3037 Authority bias |
| SYN-MEAN-005 Repetition as confirmation | P0841 Repetition learning · P3011 Confirmation bias |

Not all of it is clean — SYN-MEAN-001 picks up `Tip-of-the-tongue states`, and
SYN-MEAN-003 picks up `Spacing/distributed practice` off the word *distributed*.
Reported, not tuned away.

---

## 5. WHAT IS REFUSED — the transcript's own rejections, kept so they cannot creep back

| refused | why |
|---|---|
| owl = night / truth / wisdom | an infographic reading, not a translation |
| falcon = sky power / royal guard | same |
| waves = endurance / continuity | same |
| five columns = five reign stages / five vows | same, and it assumes the column count means something |
| confidence **7.8/10** | **MATCH SCORE ≠ EPISTEMIC CONFIDENCE** — the same defect his ASI0001 workbook already showed, where RANK was row order at score 0 |
| column 1 → 2 → 3 is chronological | visual adjacency is not sequence |

Every one carries `adopted: False`, `historical_fact: False`.

---

## 6. HIS UNANSWERED QUESTION

The transcript ends on:

> keep all in there / but show me **how many new meaning** and on that basis u
> created with new inputs

Then the chat expired and the count was never given. It is:

```
his named meanings                8
generated from the new inputs 1,824   (gated; 6,480 ungated)
of those, genuinely new shapes 1,706
historical facts established      0
translations made                 0
new parameters created            0
```

---

## 7. A DEFECT THIS BUILD CAUGHT IN THE SEATING ITSELF

Two runs of the same seating returned **different rows**. `seat()` iterated a
`set` of words, and Python randomises set iteration per process, so tied weights
came back in a different order every run — **the same input gave different
answers.** Word iteration is now sorted and ties break on the row id. Same input,
same seats, verified across three runs.

---

## 8. PLACED

```
GPT_Black.txt   37,004 chars   435 events   305 ids seated   count +871
mechanisms appended            54 rows (AXIS 25 · PATTERN 20 · OBJECTIVE 6 · RULE 3)
parameters created              0     bank stays 3,207
```
