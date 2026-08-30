# CONTEXTUAL PARAMETER WEIGHTING — HIS BJP EXAMPLE, ALIVE AND NOT APPROVED

**Filed 2026-08-13. His mechanism, his provisional name, his promotion gate.**

## HIS MECHANISM, VERBATIM

> This is a strong example because Advani was senior, but BJP was not choosing
> "the most senior BJP leader"; it was choosing a candidate for a specific
> future task: winning the 2014 Lok Sabha election.

```text
SAME PARAMETERS
+ DIFFERENT OBJECTIVE
→ DIFFERENT PARAMETER IMPORTANCE
→ DIFFERENT DECISION
```

> I would provisionally call it: **Contextual Parameter Weighting**
>
> A parameter does not have a fixed decision value. Its importance changes
> according to: current role · objective · environment · constraints ·
> available alternatives · expected outcome.

```text
ADVANI
highest seniority?   YES
              ≠
therefore highest suitability for the 2014 campaign?   NOT AUTOMATIC
```

> So seniority was one parameter, not the complete decision function.

**What it must NOT learn**, in his words:

```text
young leader > senior leader        Wrong.
popularity > experience            Also wrong.
```

**What it may learn:**

```text
PARAMETER IMPORTANCE IS ITSELF CONTEXT-DEPENDENT.
```

**And the questions it asks instead:** *Popular for what? Experienced for what?
Senior for what? Selected for what objective?*

## HIS DATE CORRECTION — HELD AT THE RIGHT STATUS

He corrected the record and gave sources:

- BJP formally announced Narendra Modi as its PM candidate on **13 September
  2013** for the 2014 election; Advani opposed the move and the party proceeded.
- By **April 2013** BJP president Rajnath Singh was publicly calling Modi the
  party's most popular leader, citing three consecutive Gujarat wins.
- Advani **resigned from party posts in June 2013** after Modi was appointed to
  head the election campaign.
- The final decision rested with BJP's **Parliamentary Board**, not seniority.

**Status: `SOURCE-ASSERTED WITH CITATION` — he cited Indian Express and Business
Standard. This engine did NOT verify them here, and the machine says so rather
than promoting them to verified fact.** That is the same ladder his rice/MBA example
set: a figure or date that arrives in the source is kept as stated and never
upgraded.

## HIS REGISTRY ALREADY NAMES THE MECHANISM

`CON-047.04` = **Attribute weighting**, inside *Decision, Judgment and Trade-off
Intelligence* (`P1843–P1882`), whose own note reads *"Humans alternate between
habitual, intuitive, deliberative and socially influenced choices."* Also present
and firing: `CON-047.03 Attribute identification`, `.07 Multi-attribute
integration`, `.08 Trade-off resolution`, `.19 Framing sensitivity`, and
`CON-064.36 Value ranking`.

He did not need a new parameter for the mechanism. He needed the **weighting** to
become a runtime object. That is what was built.

## WHAT WAS BUILT — `src/sourceborn/weighting.py`

**7 axes**, generalised out of political vocabulary so a hospital rota or a club
captaincy meets the same reader: SENIORITY / TENURE · EXPERIENCE / DOMAIN DEPTH ·
INSTITUTIONAL MEMORY / LEGACY · CURRENT POPULARITY / SUPPORT · RECENT RECORD ·
ORGANISATIONAL BACKING · MOBILISATION / CAMPAIGN REACH.

**4 objective types.** Two are HIS — `COMPETITIVE WIN` (the 2014 objective, with
his own weight ordering) and `STEWARDSHIP / COUNSEL / CONTINUITY` (the
counterfactual he named himself). Two are MINE — `THROUGHPUT / EXECUTION /
SAFETY` and `GROWTH / NEW REVENUE` — and every row says whose it is.

Bands are ordinal, in his own idiom: `DOMINANT` · `HIGH` · `RELEVANT` ·
`RELEVANT BUT NOT DOMINANT`. No invented numbers.

### ON HIS SENTENCE

```text
CANDIDATES
  L.K. Advani     SENIORITY / TENURE          HIGH   <- senior, founder, long history
                  EXPERIENCE / DOMAIN DEPTH   HIGH   <- experience
  Narendra Modi   CURRENT POPULARITY          HIGH   <- popular, most popular, cadre
                  RECENT RECORD               HIGH   <- victories, consecutive
                  ORGANISATIONAL BACKING      HIGH   <- backing, rss, organisational
                  MOBILISATION / CAMPAIGN     HIGH   <- campaign

WEIGHTS UNDER COMPETITIVE WIN            (HIS ordering)
  CURRENT POPULARITY / SUPPORT      DOMINANT
  MOBILISATION / CAMPAIGN REACH     DOMINANT
  RECENT RECORD                     DOMINANT
  ORGANISATIONAL BACKING            HIGH
  EXPERIENCE / DOMAIN DEPTH         RELEVANT
  SENIORITY / TENURE                RELEVANT BUT NOT DOMINANT

  -> the weighting favours Narendra Modi
```

### HIS COUNTERFACTUAL — THE PART THAT MAKES IT TESTABLE

> If the objective had instead been: choose elder adviser / historical party
> authority / institutional mentor — then the weighting could have been
> completely different and Advani's seniority/history might carry much greater
> importance.

```text
                          COMPETITIVE WIN     ->  STEWARDSHIP / COUNSEL
SENIORITY / TENURE        not dominant        ->  DOMINANT
CURRENT POPULARITY        DOMINANT            ->  not dominant
MOBILISATION / CAMPAIGN   DOMINANT            ->  not dominant
RECENT RECORD             DOMINANT            ->  RELEVANT
EXPERIENCE / DOMAIN DEPTH RELEVANT            ->  HIGH
ORGANISATIONAL BACKING    HIGH                ->  RELEVANT

6 weight flips.  FAVOURED: Narendra Modi  ->  L.K. Advani.  SELECTION CHANGES.
```

Same parameters. Same people. Different objective. Different decision. Executable.

**30 exact P rows** — 17 SOURCE-GROUNDED, 9 CANDIDATE, 4 HELD OPEN — across 8
containers and 5 segments. The biases seniority and popularity can set are
**named and HELD, never asserted of anyone**: `CON-076.33 Authority bias`,
`.16 Status-quo bias`, `.29 Halo effect`.

## TWO DEFECTS THE EXAMPLE CAUGHT IN MY FIRST RUN

1. **"L.K. Advani" and "Advani" were counted as two candidates** — three
   candidates reported for two people. Deduped by surname.
2. **Every candidate inherited every axis.** One sentence names both men, and my
   attribution was "the sentence mentions them", so Advani was credited with
   Modi's popularity, record, backing and campaign reach. Fixed: attribution is
   by **nearest mention** within the sentence, and each axis carries a
   **direction**, so *"Modi was less senior than Advani"* gives **LOW** seniority
   to Modi and **HIGH** to Advani. Crediting Modi with seniority there would
   have been a fabrication.

## HIS PROMOTION GATE — AND THE PROBE

> I would keep this candidate alive but not approve it yet. The next example
> should come from a completely different domain — business, family, sports,
> medicine, school, etc. If the same structure fires again without forcing it,
> then ASI has started discovering something genuinely reusable rather than
> merely explaining BJP's 2013 decision.

`PC-WEIGHT-001` ships **SUPPORT 1 · CANONICAL 0 · ALIVE — NOT APPROVED**, with
`cross_domain_required = True`, his five domains listed, and
`who_approves = "him — this module cannot promote it"`.

### THE FIRST PROBE RUN: 3 OF 5

```text
SPORTS    club captaincy      FIRES: False   fewer than two candidates
MEDICINE  emergency list      FIRES: True
BUSINESS  board seat          FIRES: True
SCHOOL    head boy            FIRES: False   no role named + no candidates
FAMILY    trustee             FIRES: True
```

Diagnosis: `candidates_in` returned **empty** for sports and school. A person
named **once** was invisible — my rule required the name to recur or carry
initials. That is the same defect as the actor being invisible in the Samrath
sentence, and it has nothing to do with weighting.

**Fixed generally**, not tuned to these cases: a full name — two capitalised
words in a row — is a person on a single mention; and `to fill / position / post
/ seat / job` are role markers.

### THE SECOND PROBE RUN: 5 OF 5

```text
SPORTS    Rahul Bose / Imran Shaikh    COMPETITIVE WIN    -> Imran Shaikh
                                       counterfactual     -> Rahul Bose      FLIPS
MEDICINE  Dr Menon / Dr Rao            THROUGHPUT/SAFETY  -> Dr Rao
                                       counterfactual     -> Dr Menon        FLIPS
BUSINESS  my uncle / my cousin         STEWARDSHIP        -> my uncle
                                       counterfactual     -> my cousin       FLIPS
SCHOOL    Aman Verma / Kabir Shah      COMPETITIVE WIN    -> Kabir Shah
                                       counterfactual     -> Aman Verma      FLIPS
FAMILY    my grandfather / my brother  STEWARDSHIP        -> my grandfather
                                       counterfactual     -> my brother      FLIPS
```

**5 of 5 fire. The selection flips under the counterfactual objective in 5 of 5.**

**And two of them favour the SENIOR person** — the family trustee and the board
seat, both STEWARDSHIP objectives. That is the proof the mechanism is not the
lesson he refused: it is not "young beats old". Under a continuity objective the
grandfather wins on the same axes that lose under a contest objective.

**It is still NOT APPROVED.** The probe cannot promote it and neither can this
module. `canonical = 0` until he says otherwise.

## WHAT IS HONESTLY WEAK

- The two objective types I added (`THROUGHPUT`, `GROWTH`) are mine. If his
  weight ordering for those differs, the medicine and business results move.
- The five probe cases are mine, written after reading his mechanism. They are
  not forced — the detector was not altered to make any of them pass, and the
  one change made was to a name parser that had failed on both — but they are
  not *his* examples either. A case he writes himself is stronger evidence than
  five I wrote.
- `RULE-002` — he lists *"Role changes active interpretation"* as an **existing**
  rule with SUPPORT +1. My ledger held only RULE-001. The nearest earlier
  teaching on record is the father/door example (`SAME_ACTION_CHANGED_FUNCTION.md`
  — same action, changed functional role). **Recorded as his, with that
  provenance, and surfaced here rather than silently backdated.**
