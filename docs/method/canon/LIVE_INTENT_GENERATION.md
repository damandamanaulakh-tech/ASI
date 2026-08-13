# LIVE INTENT GENERATION — THE BOTTLENECK HE NAMED

**Filed 2026-08-13.**

## HIS WORDS

> concept is simple as much parameters we plug, we will generate more pattern
> and intent
>
> **as of now main bottleneck is system is not generating the new intent live**

He is right, and the diagnosis was exact. Before this:

- `statepacks.EVENT_FORKS` was a **hardcoded dict of ten events** with his
  routes typed in. An event he had not named returned nothing.
- `asi_pyramid.INTERPRETATION_FRAMES` returned **seven frames whatever the ask
  was** — a fixed list, not a generation.

Neither read the parameter bank. So plugging more parameters changed nothing,
which is the opposite of his concept.

## WHAT GENERATES IT NOW

Intent is built at runtime from **his own rows**:

```text
CON-064  Motive, Needs, Values and Priority Structure   40 rows   = the WHY
CON-063  Intent Formation and Commitment                40 rows   = the SHAPE
                                                       -------
                                        ceiling          1,600 pairs
```

A motive is **reachable** from a container when that container carries a
sub-parameter echoing it — **computed over the bank, never hand-typed**. The
active container set therefore decides which motives can be raised:

```text
more parameters active -> more motives reachable -> more intent candidates
```

## HIS CONCEPT, COMPUTED RATHER THAN ASSERTED

`intents.scaling()` walks the container set and reports the curve:

| active containers | motives raised | intents generated |
|---|---|---|
| 1 | 2 | 8 |
| 4 | 5 | 20 |
| 8 | 12 | 48 |
| 48 | 21 | 84 |
| 64 | 27 | 108 |
| 80 | 35 | 140 |

**Monotonic.** A test asserts it, and asserts the 80-container figure is more
than five times the 1-container figure.

## THE FABRICATION GUARD — AND WHAT IT REMOVED

Naive head-word matching gave **200 edges**, and about a third were lexical
coincidences of exactly the kind that scored zero on the Samrath sentence:

```text
Recognition/status need   ->  "Shape recognition"          WRONG
Face-saving motive        ->  "Face detection"             WRONG
Power/control need        ->  "Power-grip control"         WRONG
Meaning/purpose need      ->  "Word-meaning retrieval"     WRONG
Motive-inference conf.    ->  "Wetness/moisture inference" WRONG
```

Perception (SEG-02), sensorimotor (SEG-03), attention mechanics (SEG-04) and
language (SEG-07) **cannot originate a motive**, so those segments are blocked
from hosting one. **The gate removes 67 edges: 200 → 133.** Every surviving edge
reports the sub-parameter it matched, its P id and its host segment, so a bad
edge is visible and strikeable rather than buried.

**Residual noise, stated:** a few coincidences survive the gate —
`Recognition/status need → CON-072 "Rights recognition"` and
`Motive stability vs shift → CON-003 "Sleep-wake switch stability"`. They are on
screen with their evidence so he can strike them. Not claimed clean.

## THREE REAL MOTIVES HAVE NO ECHO IN THE BANK

Five motive rows link to nothing. Two are machinery rather than motives —
`P2525 Stated motive`, `P2526 Operating (actual) motive`. **The other three are
real human motives with no representation anywhere in the 3,204 outside CON-064
itself:**

```text
P2536  Security need
P2549  Mating/attraction motive
P2552  Revenge/retaliation motive
```

Reported as absences. Not filled in.

## THE JOIN THE BOTTLENECK NEEDED

`intents.from_state_pack()` is where the generation meets the brain-state: the
pack says which containers are active and in which state, and the intent is
generated from **that**, not from a table.

```text
SP-27 Divided-Loyalty   5 active containers -> 18 motives x 7 forms = 126 candidates
   Loyalty motive        <- CON-072 Dominant   (SEG-09) matched "Loyalty/in-group value"
   Belonging need        <- CON-071 Conflicted (SEG-09) matched "Belonging need"
   Fairness motive       <- CON-072 Dominant   (SEG-09) matched "Fairness/justice judgment"
   Care/nurturance       <- CON-072 Dominant   (SEG-09) matched "Harm/care judgment"

SP-24 Exhausted         7 active containers ->  3 motives x 7 forms =  21 candidates
   Avoidance motive      <- CON-006 Dominant   (SEG-01) matched "Avoidance learning"
   Power/control need    <- CON-007 Suppressed (SEG-01) matched "Willpower/ego-depletion signal"
```

**Different brain-state, different intents.** A test asserts the exhausted pack
raises **only SEG-01** motives — the body ones — and that the two packs do not
produce the same count.

## THE FORM IS CHOSEN BY THE SCOPE, NOT GUESSED

```text
CURRENT -> Immediate-intention formation · Action commitment · Volitional commitment
FUTURE  -> Future-intention formation · Deadline-linked · Implementation (if-then) · Precommitment
PRIOR   -> Intention decay · Intention abandonment · Intention revision · Intention reactivation
conditional -> Contingent intention (only if X) · Conditional-commitment setting
conflict    -> Competing-intention arbitration · Intention conflict resolution
```

All his own row names. A test asserts `Future-intention formation` does **not**
appear under a CURRENT scope.

## THE LAWS THAT STAY ON

- Every generated intent is a **runtime object**: `in_bank: False`,
  `is_native_parameter: False`, no P id of its own. It cites the motive P and
  the form P it was built from.
- `native_parameters_added: 0`, and a test proves the bank stays at **3,204**
  after generation.
- `chosen: None`. `Motive-inference confidence` (his P2564) is **LOW**, with his
  own container note as the reason: *inferred motive must remain a hypothesis
  until supported or confirmed.*
- Every candidate carries the **evidence that raised it** — which container,
  which state, which sub-parameter row.

## IN THE APP

```text
GET  /intents        stats, the scaling curve, the link table, the unlinked motives
POST /intents/run    {event, containers, scope, conditional, conflict}
GET  /generation     now shows LIVE INTENT for the selected brain-state
```

Browser-verified on SP-27 + ABDICATE: no page errors, the live-intent block
renders with the motive rows, their P ids, the state that raised each one and
the matched evidence row. **199 tests green.**

## STILL MISSING — THE SAME GAP, NOW SHARPER

Generation is live and it scales. **Nothing kills a candidate.** 154 intents come
back as 154 whatever is known. His chain is generate → evidence →
contradiction → falsification → **survivor set**, and the survivor stage does
not exist in the code or in his workbook. That is now the one bottleneck left,
and it is the next thing worth building.
