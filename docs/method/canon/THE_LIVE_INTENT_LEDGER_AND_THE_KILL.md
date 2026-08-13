# THE LIVE INTENT LEDGER — AND THE KILL HE SUPPLIED

**His words:** *"merge this one too / and read the file as well"*
**File:** `ASI0001_tablet_run_LIVE_INTENT_v2.xlsx` — 19 sheets, read in full,
values and formulas.
**Date:** 2026-08-13

---

## 1. WHAT THIS FILE CLOSES

At the end of the last build I reported one gap open, in these words:

> **the killing step.** Nothing eliminates a fork on evidence. 154 intents come
> back as 154 whatever is known; generate → evidence → contradiction →
> falsification → survivor set has no survivor stage, in the code or in his
> workbook.

His `LIVE_INTENT_ENGINE` sheet carries a column I did not have:

```
Falsifier / What would flip it
```

and it is **filled on all ten of his candidates**, beside `Support Count` and
`Counterexample Count`. That is the survivor stage. It is his, not mine.

The rule that follows from it, and is now enforced in code: **a candidate that
names nothing that would flip it cannot be killed by any evidence, and that is a
defect in the candidate, not a strength.** `intent_ledger.kill()` reports such a
candidate as `cannot_be_killed` rather than quietly letting it survive.

---

## 2. WHAT HE RAN

**ONE actor. ONE event. TEN states. TEN intents. NONE chosen.**

- Actor: `Same King`
- Event: `Advisor requests a private meeting`
- States: Insecure legitimacy · Secure legitimacy · Grieving · Suspicious after
  betrayal · Trusting after repeated reliability · Exhausted / low physical
  capacity · Victory-elevated confidence · Defeat-shaken · Divided loyalty ·
  Legacy-anxious / finite-horizon
- Novelty deltas: 0.73 – 0.99
- Support 1 · Counterexamples 0 · Epistemic status `SYNTHETIC / REVIEW` ·
  User decision `HOLD` · Promotion `HOLD` · Canonical `NO` — on every row.

**His ten states already exist in this core as SP-19 … SP-28.** So under his own
rule — *"its not required that it should make new everytime, mostly wording
meaning are are exist in the core"* — they are **matched, not re-typed**.
`intent_ledger.from_core()` proves the join: all 10 map to packs, 0 missing.

What IS new: **the event** (his ten King sequences did not contain it — it is now
the 11th `EVENT_FORKS` entry, `ADVISOR_PRIVATE_MEETING`, with 10 routes), the ten
falsifiers, his seven-rule contract, and the namespace ruling.

---

## 3. HIS SEVEN-RULE LIVE INTENT GENERATION CONTRACT — now executable

| # | his rule | what enforces it |
|---|---|---|
| 1 | Do not select only from the 100 prewritten King characters | `intents.generate` builds from active parameters, not a character list |
| 2 | At runtime, activate parameters/addresses from the current Sequence | `intents.from_state_pack` |
| 3 | Generate at least 3 competing candidates when evidence permits | 10 on his event; 20–126 per state from the core |
| 4 | **An intent is new only when predicted behavior/target/priority differs materially. New wording is not enough.** | `intent_ledger.signature` — built from `state_change · target · constraint` and **never from the intent sentence** |
| 5 | Store new intent first as LIVE_CANDIDATE | `LIVE_CANDIDATE`; `canonical=False`, `in_bank=False` |
| 6 | Pattern extraction only after recurrence across Sequences | `promote(sequences_seen=…)`, `RECURRENCE_MIN = 2` |
| 7 | Open a parameter candidate only if existing vocabulary **repeatedly** cannot express it without semantic loss | `semantic_loss(text, failures)` — needs *both* no registry match *and* failures ≥ 2 |

**Rule 4 is the one with teeth, and it is proved by test:** re-word one of his
intents completely while leaving what it predicts unchanged → `novel: False`,
*"only the wording differs, and wording is not novelty."* Change what it predicts
→ `novel: True`.

**His promote gate** (Evidence + falsifier + recurrence + user approval) returns
`PROMOTED: False` with every unmet condition named. `new_parameter_created` is
`False` even when it passes — **new intent does not mean new parameter**, his line.

---

## 4. HIS NAMESPACE RULING — the seam I had left open, closed by him

From his gate table, verbatim:

> **Registry boundary** | This workbook retains its 2,000 source addresses |
> Current 3,204 registry can map in; **do not silently merge namespaces**

Two things this settles:

1. **He calls the 2,000 ADDRESSES himself.** That confirms the reading
   `statepacks.py` already enforced — `80 × 25 = 2,000` instantiated addresses are
   not 2,000 parameters, and are not added to the 3,204.
2. **The two banks must not be merged** — and they collide worse than I had
   noticed. Both are written `P####`:

| bank | prefix | count | unit | grid |
|---|---|---|---|---|
| ASI0001 tablet workbook | `WB-P` | 2,000 | ADDRESS | 10 × 8 × 25 |
| ASI_Claude_Parameters v1.0 | `SB-HFR-P` | 3,204 | PARAMETER | 10 × 8 × 40 (two hold 42) |

**The segment ids collide too, and mean different things.** The obvious `map_in()`
would pair `S01→SEG-01` by position. That would be a fabrication:

```
workbook S04 = Religion, Ritual & Cosmology
registry SEG-04 = Attention and Executive Control
```

So `map_in()` shows the ordinal neighbour, marks `same_subject: False`,
`mapped: False`, and **holds the real correspondence for him**. His ruling bites
at the segment level, not only at the P ids.

---

## 5. WHAT HIS WORKBOOK ACTUALLY CONTAINS — 13 findings, 0 corrections

Verified before anything was built on it. **His file is not rewritten.**

| # | where | finding |
|---|---|---|
| WBF-01 | MATCH_ENGINE | **All 100 characters score 0.** Parameter Match 0, L1–L5 Adj 0, Loop Average 0, Contradiction Penalty 0, Final Score 0, band `Weak`, decision `Hold`, proof debt `Open` — every row. |
| WBF-02 | MATCH_ENGINE!M | `=RANK(L4,$L$4:$L$103,0)+COUNTIF($L$4:L4,L4)-1` — with an all-zero column the tie-break makes **rank = row order**, so K001 Lawgiver is rank 1 because it sits in row 4. |
| WBF-03 | ASI-0001_RUN vs MATCH_ENGINE | The run sheet names **Priest-King / Divine Son** leading at *"70% param + 30% loop, high"*. The workbook's own engine names **K001 Lawgiver at 0 / Weak / Hold**. The tablet run was reasoned in prose and **never entered the machinery it was built for**. |
| WBF-04 | PARAMETER_BANK | 2,000 rows; all seven input columns empty. Weighted Value 0 for all 2,000 → every segment score 0 → the 2,000-address surface contributes **nothing**. |
| WBF-05 | PYRAMID_INDEX!G | `SUMIF(PARAMETER_BANK!$B$2:$B$2001,…)` but the data is rows 4–2003. Covers **P0001–P1998**, includes blank row 2 and header row 3. **P1999 and P2000 can never affect a score.** Off by two at both ends — same defect as his previous workbook. |
| WBF-06 | PYRAMID_INDEX!H, MATCH_ENGINE!N | `ABS(G4)` / `ABS(L4)` inside the confidence bands → a **contradicted, negative score reads "Strong" / "Very strong"**. His own rule is that contradictions must *reduce* the score. Latent today only because everything is 0. |
| WBF-07 | ARD_5_LOOPS | 60 nodes, all `Not started`; Input, Result, Evidence IDs, Contradiction IDs, Confidence empty on every row — **while ASI-0001_RUN carries LOOP 0–5 written out with verdicts and falsifiers.** |
| WBF-08 | EVIDENCE_LEDGER / MEMORY_NODES | 500 evidence rows all `Unverified`, 15 of 17 columns empty. 500 memory nodes all `Unused`, **including the Falsifier column** — the layer built to hold falsifiers is untouched, while the falsifiers he did write live on the live-intent sheet. |
| WBF-09 | DASHBOARD | Decision Gates 1–5 all read `Open`, including Gate 3 *"All five loops completed"* and Gate 4 *"Contradictions and falsifier tested"*, which the run sheet asserts are done. The gate cells are typed constants, **not formulas** — they cannot move. |
| WBF-10 | sheet counts | The file has **19** sheets. INDEX lists **18** and omits ASI-0001_RUN entirely. DASHBOARD says **16**. Three counts of the same file. |
| WBF-11 | INDEX row counts | INDEX gives SOURCEBORN_INIT 12 rows (it holds 15, four of them the new Live Intent rules) and INDEX itself 16 (it lists 18). His index did not follow his two new sheets. |
| WBF-12 | ASI-0001_RUN | The run cites **F04 Sacred** and **F08 Art**. His own KING_CHARACTERS has Sacred & Cosmological = **F03** (K021–K030) and Art & Symbol = **F07** (K061–K070); F04 is Family & Succession, F08 is Diplomacy & Society. The *segment* ids in the same rows (S04 Religion, S07 Art) are correct — the family ids appear to have been written from the segment numbering. F02 War is right in both. |
| WBF-13 | LIVE_INTENT_ENGINE / INTENT_LEDGER | Both **fully filled**: 10 candidates, 10 falsifiers, deltas 0.73–0.99, Support 1, Counterexamples 0, HOLD, Canonical NO. **The one part of the workbook that was actually run is the part that closes the killing step.** |

**The honest summary of the file:** the two new sheets are alive and they are the
best thing in it. The tablet engine around them is a complete, well-formed shell
that currently computes zero and would tell him *"K001 Lawgiver, Weak, Hold"* if
he opened the dashboard.

---

## 6. THE KILL, DEMONSTRATED

His ten candidates, three of them given verdicts:

```
LI-002  falsifier met  ("the advisor arrives with a written challenge")   -> KILLED
LI-006  counterexamples 2 >= support 1                                   -> KILLED
LI-004  falsifier stated, not met, no counterexamples                    -> SURVIVES
the other seven                                                          -> UNTESTED
```

```
generated 10 · tested 3 · killed 2 · survived 1 · untested 7 · deleted 0
```

Three things this enforces:

- **An untested candidate is UNTESTED, not a survivor.** "Nobody checked" is not
  "it held."
- **Nothing is deleted.** A killed row keeps its falsifier, its support, and the
  reason it died. That is his NO REOPEN discipline: a later reading references the
  earlier one, it never erases it.
- **Two kill routes, both his:** the falsifier is met, or counterexamples reach
  support.

---

## 7. WHAT WAS APPENDED, AND WHAT WAS NOT

Under his standing rule *"so keep adding not removing at all"*, the growth ledger
seed goes **199 → 218 rows**:

| kind | was | now | what was added |
|---|---|---|---|
| EVENT | 10 | 11 | `ADVISOR_PRIVATE_MEETING` |
| INTENT_ROUTE | 40 | 50 | his ten state-selected routes on that one event |
| RULE | 10 | 18 | his seven live-intent rules + the registry-boundary ruling |

**Not added: any parameter.** `PARAM` stays at 3 and the bank stays at
**3,204 + 3 = 3,207**. His rule 7 is why — nothing here failed to be expressible
in existing vocabulary twice over, so nothing opens a parameter candidate. His own
line: *New intent does not automatically mean new parameter.*

---

## 8. LEFT OPEN, STATED AS ABSENCES

- **His 500 memory nodes and 500 evidence rows are empty in the workbook, and this
  core has no writer for them.** The kill runs on verdicts handed in per call;
  there is no persisted evidence ledger that accumulates support and
  counterexamples across sessions. That is the next thing the survivor stage needs
  to be more than a function.
- **`ARD_5_LOOPS` — the five-loop reverse/forward walk — is his structure and is
  not in this core at all.** The tablet run shows what it looks like when run by
  hand; nothing here runs it.
- **Which workbook segment corresponds to which registry segment is held for
  him.** Ten and ten, same numbering, different subjects.
- **The pattern layer still has no recurrence counter tied to live intents.** His
  rule 6 is enforced as a *gate* (`sequences_seen`) but nothing yet counts
  sequences for him automatically.
