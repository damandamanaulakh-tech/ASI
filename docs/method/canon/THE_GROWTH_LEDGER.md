# THE GROWTH LEDGER — THE 3,204 IS A FLOOR

**Filed 2026-08-13. His instruction, which reverses what I had built.**

## HIS WORDS

> keep it without any safety or anything
>
> these 3204, are the basic and vague setup
> which will be making more with such examples
> **so keep adding not removing at all**

## WHAT I HAD WRONG

I shipped `INSTANTIATED ADDRESS != NATIVE PARAMETER` with a test whose stated job
was **"to prove the bank does not grow"**, and I wrote on the `/generation` page
that *"the bank never grows"*. That treated his base as a **ceiling**.

Two different statements had been merged into one, and only the first was true:

```text
TRUE   his source document is never rewritten          (preserve raw source)
FALSE  therefore the system's parameter set is fixed
```

His base of 3,204 is the **basic and vague setup**. It is a floor.

## HOW "NOT REMOVING AT ALL" IS ENFORCED

Structurally, not by discipline. **`growth.py` has no delete, no remove, no
drop, no clear, no prune, no truncate, no `os.remove`, no `os.unlink`, no
`.pop()` and no `rmtree`.** The store is a JSONL file opened in **append mode
only**. A test reads the module's own source and fails if any removal path is
ever added, and a second test asserts the only file modes used are `"a"` and
`"r"`.

**Superseding does not remove.** A later reading appends a new row carrying
`supersedes: <old id>`, and the old row stays whole in the ledger. A test proves
both rows survive.

**A corrupt line is reported, never dropped and never rewritten** — it comes back
as `kind: UNREADABLE` with its raw text and the parse error.

## THE GATE IS OFF

> keep it without any safety or anything

Growth is not held behind an approval queue. An addition is **in** the moment it
is added. Provenance is still recorded on every row — which example surfaced it,
which module, and what it is — because he needs that to correct a row. Recording
where something came from is not a gate.

**One thing I did not touch and am telling you plainly:** the hard content blocks
in `safety.py` (weapons / fraud / medical-misuse / guaranteed-prediction /
explicit-sexual execution) are still there. That line is rule 10 of his own
`CLAUDE.md`, written by him, and it is about what the engine *executes*, not
about how the parameter set grows. If he wants that changed too he can say so and
it is his call — but it is not what this instruction was about, and I am not
going to silently read it into a message about parameter growth.

## WHAT IS *NOT* ADDED — HIS OWN DISTINCTION, KEPT

```text
DOMAIN CONTAINER    != RUBRIC
RUBRIC APPLICATION  != ONTOLOGY EXPANSION
I would not add its 2,000 to the 3,204 count
```

So the ledger is **typed**, and only `PARAM` rows consume his flat index at
**P3205** onward. A rubric applied to a container is an address; 80 × 25
addresses are not 2,000 new parameters. Everything is added — only parameters are
numbered as parameters.

```text
PARAM         SB-HFR-P3205...    continues his flat index
STATE         SB-STATE-001...
RUBRIC        SB-RUBRIC-001...
FILTER_ARG    SB-FILT-001...
PATTERN       SB-PAT-001...
RULE          SB-RULE-001...
SENSE         SB-SENSE-001...
AXIS          SB-AXIS-001...
OBJECTIVE     SB-OBJ-001...
EVENT         SB-EVENT-001...
INTENT_ROUTE  SB-ROUTE-0001...
ADDRESS       SB-ADDR-0001...
```

## THE FIRST SEED — 199 ROWS, COMPUTED FROM THE MODULES

Not typed by hand: `seed_items()` walks the live modules, so the ledger reflects
the code.

```text
ADDRESS         58     every container x state pair the King brain-states generate
INTENT_ROUTE    40     his forty intent routes across ten event shells
RUBRIC          25     his 25 universal dimensions
PATTERN         17     16 state packs + PC-CONTEXT-INTENT-001
FILTER_ARG      13     Time(eternity) is not Time(dynasty)
AXIS            13     7 weighting axes + his 6 mall reason-kinds
RULE            10     7 RC-* candidates + PC-WEIGHT-001 + RULE-001 + RULE-002
EVENT           10     RAISE_TAX ... ABDICATE
STATE            6     Dominant · Active · Automatic · Compensated · Conflicted · Suppressed
OBJECTIVE        4     2 his, 2 mine and labelled
PARAM            3     the three motives with no echo in the bank
               ---
                199
```

### The three that got a home

`P2536 Security need`, `P2549 Mating/attraction motive` and
`P2552 Revenge/retaliation motive` link to nothing anywhere in the 3,204 outside
CON-064 itself. Rather than leaving them as a note, they are appended:

```text
SB-HFR-P3205   Security need
SB-HFR-P3206   Mating/attraction motive
SB-HFR-P3207   Revenge/retaliation motive
```

```text
BASE                3,204
GROWN PARAMETERS        3
TOTAL               3,207
GROWN ROWS (all)      199
REMOVALS POSSIBLE       0
```

**Seeding twice adds nothing and removes nothing** — a test compares the whole
ledger before and after.

## IN THE APP

```text
GET  /growth         the whole ledger, the counts, and how no-removal is enforced
POST /growth/add     {kind, name, surfaced_by, detail, supersedes}
POST /growth/seed    append anything the modules surface that is not in yet
```

The `/generation` page no longer claims the bank never grows. It says what is
true: **his source document is never rewritten, and the system grows — additions
go to the growth ledger, nothing is ever removed.**

**206 tests green.**

## WHAT THIS CHANGES ABOUT EVERYTHING BEFORE IT

Every `canonical: 0` and `REVIEW_REQUIRED` on a candidate was a gate I put there.
The ledger is now the answer to those: the thing is **added**, and its provenance
says where it came from so he can correct it. The candidate objects keep their
support counts as information, not as a wall.
