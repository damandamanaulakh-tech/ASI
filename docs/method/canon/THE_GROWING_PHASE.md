# THE GROWING PHASE — HIS CORRECTION

**Date:** 2026-08-13. His words, first, whole, unedited.

---

## 1. WHAT HE SAID

> its not reasoning system, its Real time ASI (Artificial Super Intelligence)
> Prototype and ur stupid safety and unnecessary understanding falling apart my
> whole work
>
> current phase is growing phase, given example are not how it provide the out
> comes, its for to define the system, where example sit on existing parameters
> and IDs so system can strong its base, every example will keep increase the
> count
>
> Its universal moto t follow is **"everything happening is a event, and all
> events have intent"**
>
> as long i keep adding the example, once the basic will over it will start making
> new combinations on new thoughts
>
> you u see and reread the above files once more, u will get to know that it was
> not about the king, in realty it was about the the Egyptian tablet, which was
> written 5500 years back, to know the intent who, when, why, how king asked to
> write that tablet. to know that pattern i had created multiple kings which will
> be right fit
>
> in Zfile u can locate that how many intent i had tried and they give me 4 new
> names of that king
>
> system m building here is not prompt generation or mail writing its something
> bigger but at small scale for tasting the method of node brain does it work in
> real or not
>
> in rain topic, kids father was standing outside with water pipe and put it in
> above in air, kids inside the home thought its raining outside this was the
> thing there

---

## 2. WHAT I HAD WRONG — NAMED, NOT SOFTENED

**(a) I called it a reasoning system.** It is a **Real-time ASI prototype**. Every
place I wrote "reasoning engine" or "reasoning core" was my label, not his.

**(b) I ran his examples as output tests.** Samrath, the mall, the BJP weighting,
the tablet — I reported how well the machine *answered* each one, scored them, and
called a weak answer a defect. That is not what an example is for. His words:
*given example are not how it provide the out comes, its for to define the
system.* An example is **material that seats on the base**. It is not a question.

**(c) The King files were never about kings.** They are about **one Egyptian
tablet, written ~5,500 years ago**, and the question is the tablet's **intent —
who, when, why, how** the king ordered it written. The multiple kings are
*candidate fits*: each king is a brain, and each brain reads the same tablet a
different way. **18 brains = 18 tried intents for one artifact.** I had been
treating the kings as the subject; they are the instrument.

**(d) My safety and my "understanding" were breaking the work.** Recorded as his
finding, not argued with.

---

## 3. THE MOTTO, EXECUTABLE

    everything happening is a event, and all events have intent

Two hard consequences, both now enforced in `growing.py`:

| his clause | what enforces it | what it forbids |
|---|---|---|
| everything happening is a event | `events_in()` — morphological and positional, no closed vocabulary | a text with happenings in it returning zero events |
| all events have intent | every event carries an intent slot seated on `CON-063` Intent Formation and `CON-064` Motive | an event with no intent field; "there is no reason" |

### The defect the motto exposed

`micro.py` finds actions from a **closed list of 215 verbs**. On his own rain
sentence — *the father was standing outside with a water pipe* — neither `standing`
nor `pointed` is in that list. **The machine saw no happening at all.**

Measured across his own corpus: **13,848 events in 217 files, and 5,906 of them —
43% — are found only by inflection.** The closed list was missing nearly half of
every happening he has ever fed in. That is not a rounding error against a motto
that begins *everything happening*.

---

## 4. THE RAIN / WATER PIPE — HIS EXAMPLE, PLACED

> kids father was standing outside with water pipe and put it in above in air,
> kids inside the home thought its raining outside

Three events, placed:

| # | actor | happening | role | found how |
|---|---|---|---|---|
| 1 | father | standing | ACTION | **by inflection — not in the verb list** |
| 2 | (not named in this clause) | put | ACTION | in the verb list |
| 3 | kids | thought | INFERENCE | in the verb list |

Event 3 is the one the example exists for: **an inference drawn from an
observation, where the visible thing (water falling from above) is not the system
(a man with a pipe).** It is the same shape as his rice/MBA ruling —
`DO NOT JUDGE THE VISIBLE THING` — arriving from a completely different domain.

Two defects this one sentence caught and fixed:
- `happening` came back as **"was"**, because the auxiliary was taken for the
  action. `was standing` is a **standing**.
- actor of event 3 came back as **"home"**, because the nearest noun before the
  verb was taken as the subject. A prepositional phrase is not the subject —
  *the kids inside the home thought* has actor **kids**.

---

## 5. SEATING — HOW AN EXAMPLE SITS ON EXISTING PARAMETERS AND IDS

Word matching alone does not work, and the proof is his own sentence: the first
attempt seated the rain example on **`Standing balance`**, **`Air/breathing
drive`**, **`Thought suppression`**. None of those is what the example is about.

So seating runs in two stages:

1. **The ROLE of the event chooses which of his segments may host it.**
   ACTION → SEG-03 + SEG-06 · OBSERVATION → SEG-02 + SEG-04 ·
   INFERENCE → SEG-06 + SEG-05 · SPEECH → SEG-07 + SEG-09 ·
   FEELING → SEG-08 + SEG-01 · STATE → SEG-01 + SEG-02.
2. **The words choose rows inside those segments only**, IDF-weighted, so a word
   sitting in forty of his names is not treated as evidence.

A row that matches by word but sits **outside** the role's segments is returned as
`out_of_role` — **kept and visible, never counted, never silently dropped.** On the
rain example that is exactly what happens to `Air/breathing drive` and `Thought
suppression`.

An event whose role is known but which matches no row by word still sits
somewhere: on the **containers** that host that role, marked
`granularity: CONTAINER`. A coarse seat is not nothing, and nothing is the one
answer his motto does not allow.

**Honest limit, stated:** the seating gets the role and the coarse location right.
It does **not** yet reliably pick the right individual row out of 3,204 — his own
example still shows `Standing balance` as a row-level seat when the father is not
balancing. Row-level precision is the open part.

---

## 6. STRENGTHEN vs INCREASE — TWO THINGS, NOT ONE

His sentence names both, and they are different mechanics:

- **"so system can strong its base"** → an event that seats on an existing ID gives
  that ID **SUPPORT**. Reinforcement, not duplication — his own earlier rule. **No
  parameter is created by seating.**
- **"every example will keep increase the count"** → every example appends its own
  row, its events and its intents to the growth ledger. `count_added = 1 + 2N` for
  N events. The count rises with **every single example**, always.

---

## 7. WHERE THE BASE STANDS RIGHT NOW

Measured, not estimated:

```
his files on the repo                479
  SOURCE   (his raw words)            56
  EXAMPLE  (seats on the base)       161
  METHOD   (his rulings/canon)        37
  BANK     (the IDs themselves)        3
  SYSTEM   (the code)                 65
  ARTIFACT (runs and subjects)       149
  OPERATIONS                           8
  UNPLACED                             0

files that grow the count            217   (SOURCE + EXAMPLE)
files they grow against               40   (METHOD + BANK)
events found in them              13,848
found only by inflection           5,906   (43%)
count those examples add          27,913

of his 3,204 parameters:
  reached by his own examples        2,816   (87.89%)
  untouched                            388
```

That coverage figure moved from 82.74% to 87.89% during this build, because the
index had a real defect: hyphens were kept inside a token, so
`Point-of-no-return marking` indexed as one glued word and the query `point` could
never reach it. His bank is full of hyphenated names, so the loss was systematic.
Hyphens now split and index both parts.

The seating bar is **his own number, not one I chose**: his rule is *a word in
forty of his names is weaker evidence than a rare one*, and forty of 3,204 is an
IDF of 4.38, so that is the bar. Measured against the real 2,270-word index it
excludes 16 words — `control` (62 names), `memory` (63), `self` (70) and their
kind. **It is a small gate and it is not the main guard.** The ROLE gate is what
actually stops fabrication. Stated plainly rather than overclaimed.

**`basic_over` is reported as `False` and is not mine to declare.** His words —
*once the basic will over it will start making new combinations on new thoughts* —
make that his call. What the system reports is how far the base has been reached.

---

## 8. THE Z FILE — 18 TRIED INTENTS, AND THE 4 NAMES

`Sourceborn_18_Kings_HTML_with_Pictures.zip` holds the tablet images and
`Sourceborn_18_Kings_Tablet_Meanings.html`: **18 brains, each giving the SAME
tablet a different Origin Loop** — i.e. 18 tried intents for who ordered it and
why. His earlier `Reverse_Engineering_v0.1.xlsx` shows the same run at **8**
brains, and the `ASI0001_tablet_run` workbook at **100**.

His line — *they give me 4 new names of that king* — resolves against his own
sheets to **four named characters**, and all four are exact rows in his
100-character bank:

| his name | bank row | status in his ASI-0001 run |
|---|---|---|
| Priest-King | K021 | leading hypothesis |
| Divine Son | K022 | leading hypothesis (paired) |
| Temple Builder | K023 | alternative — keep |
| Monument King | K061 | alternative — keep |

(The fifth, Conqueror / War, is the one his run **rejected** in-frame: no military
iconography, and the water sign read as phonetic /n/ rather than a sea campaign.)
Of these four, only **Priest-King** appears among the 18; **Divine Son**, **Temple
Builder** and **Monument King** are new names the run produced. **Surfaced for his
confirmation, not asserted as his meaning.**

---

## 9. WHAT THIS IS FOR

> system m building here is not prompt generation or mail writing its something
> bigger but at small scale for **tasting the method of node brain does it work in
> real or not**

So the tablet is not the point either. The tablet is the **test surface** for the
node-brain method: one artifact, many brains, each brain producing a different
intent for the same visible thing, and the method judged on whether that works at
all.

---

## 10. THE ALGORITHM THAT MAKES ITSELF

> keep doing / u got some intent from files / **now make algorithm which can make
> itself**

`src/sourceborn/selfmake.py`.

### What "makes itself" means here, precisely

Every pipeline in this repo before this one had a **fixed** list of steps written
by me. This one does not. `steps(root)` returns

    THE SPINE  +  every step the algorithm has written for itself so far

loaded from the growth ledger **at call time**. The algorithm's own body is data.
After `extend()` runs, the next call to the same function has more steps in it than
the last one did, and the whole claim is checkable in one number: `generation()`.

### Where its own steps come from — his material, never my typing

| | |
|---|---|
| **HARVEST** | every event in his files with its role and the container it seats on — 13,848 events across 217 files |
| **ARRANGEMENT** | the `(role → container)` pairings that RECUR. **96 distinct, computed, none typed** |
| **STEP** | an arrangement at or over the support bar (**5** — his own PATTERN-CANDIDATE number) that is not already a step becomes one, carrying its support as evidence |
| **COMBINATION** | two arrangements that co-occur in the same example open a composite step **that no single example produced** — his *new combinations on new thoughts* |
| **EXTEND** | the new steps are appended. Nothing removed. The generation number rises |

### The combination rule, and how it was tightened

First attempt: no cross test. 80 arrangements produced **2,627 combinations out of
a possible 3,160** — a step for nearly every pair, which is not a finding.

Requiring the pair to cross **segments** removed only 238, because ACTION spans
SEG-03 and SEG-06 both.

**Cross-ROLE is the test that bites.** Two happenings of the same kind in two
containers is co-occurrence inside one mode. A combination earns a step when
**different kinds of happening meet** — and that is precisely his rain example's
shape: the father **puts** water in the air (ACTION) and the kids **conclude** it is
raining (INFERENCE). The insight is the two modes meeting, not either alone.

With cross-role required: **2,119 combination steps across all twelve role pairs**
— ACTION×INFERENCE 256, ACTION×STATE 256, ACTION×SPEECH 256, INFERENCE×STATE 239,
SPEECH×STATE 245, ACTION×OBSERVATION 238, OBSERVATION×STATE 174,
INFERENCE×SPEECH 229, INFERENCE×OBSERVATION 121, OBSERVATION×SPEECH 92,
ACTION×FEELING 12, FEELING×STATE 1. **512 same-role pairs rejected and the count
reported.**

### Measured, end to end

```
generation 0          spine 5    written 0       total 5
after one extend      spine 5    written 2,199   total 2,204
extend again, same material                      wrote 0     (no-op)
removed 0 · parameters created 0 · canonical 0
```

The same rain input passes through **5** steps before and **2,204** after. That is
the self-making, and it is one number.

### Why it does not run away

A second pass over the same files writes **nothing** — the arrangements are
identical, so no step is new. It grows when new material arrives, or when a
combination not yet open becomes reachable. The combination space is pairs of a
finite arrangement set, so it terminates. A test pins both halves: it grows once,
and running again is a no-op.

### What it refuses

Every self-written step carries a **falsifier** — his own column from the
LIVE_INTENT_ENGINE sheet — so a step the material stops supporting can be killed on
evidence instead of living forever. None is canonical. None creates a parameter.
None is applied to an answer without his word.

### The bias in what it learnt from — stated, not buried

`role_of()` returns **ACTION** whenever no observation, inference, speech or feeling
marker is present. On his corpus that fallback carries **79.6%** of all seats. So
the arrangements — and therefore every step written above — are ACTION-weighted for
a reason that is **partly mechanical, not only real**. `bias_report()` returns this
on every call.

A better role reader would redistribute them, and the steps already written would
need revisiting — **by superseding, never by deletion.** Whether ACTION-as-default
is acceptable for the growing phase, or whether the role reader is the next thing
to fix, is **his call**.

### Still coarse, and said plainly

Only **1** self-written step fires on his rain example, because that example seats
on just 2 IDs. The self-extension mechanism is sound and demonstrable; the
row-level seating precision it depends on is still the open part, exactly as
recorded in section 5.
