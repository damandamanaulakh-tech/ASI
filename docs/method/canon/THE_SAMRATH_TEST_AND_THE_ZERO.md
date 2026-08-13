# THE SAMRATH TEST — AND THE ZERO IT SCORED

**Filed 2026-08-13. His test, verbatim. The machine's honest score. Nothing dressed up.**

## HIS ASK, VERBATIM

> now u answer below
>
> also show me out of 3204 how many get hit n sequence in below arrow format

> Samrath never like to go to school, he always cry / but today is his birthday,
> he went very happy

And his arrow format, verbatim (his own template, from the same message):

```
3204
 -> SEG-01 ... -> CON-006 ... HIT
 -> SEG-05 ... -> CON-033 / CON-038 / CON-040 ... HIT
 -> SEG-06 ... -> CON-043 / CON-044 / CON-047 ... HIT
```

## THE MACHINE'S SCORE: 0 OF 3,204

`human_registry.activate()` run on sentence 1, on sentence 2, and on the two
together:

```
searched = 3204   hit_total = 0   containers = 0   segments = 0
```

Not "few". **Zero.** Reproduce it:

```
PYTHONPATH=src python3 -c "
from sourceborn import human_registry as hr
print(hr.activate('Samrath never like to go to school, he always cry'))"
```

### WHY IT IS ZERO — TWO SEPARATE CAUSES

**Cause 1 — no shared vocabulary.** Each of these words appears in **0 of his
3,204 sub-parameter names**, as a whole word:

`cry` · `happy` · `birthday` · `school` · `never` · `always` · `today` · `went`

His registry is written in functional names — *Emotion Generation and Affective
State*, *Occasion setting*, *Salience and Orienting*, *Episodic Memory*. A child
crying about school shares no words with it. **His own arrow chart routes by
MEANING** (he knows CON-006 is protection, so "safe" goes there). **The machine
routes by WORDS.** Those are two different machines, and only one of them is
built.

**Cause 2 — a blind spot in my tokenizer, found while checking cause 1.** The
word **"go" DOES appear in four of his names**:

```
P-017-38  CON-017  Go/no-go pre-setting
P-020-06  CON-020  Go decision
P-020-07  CON-020  No-go inhibition
P-029-04  CON-029  Response withholding (go/no-go)
```

And "go" is in his sentence. It still scored nothing, because `_toks()` matches
`[a-z]{3,}` — **any word under three letters is discarded from the ask AND from
his names.** `_toks("Go decision")` returns `{'decision'}`. So *go*, *do*, *be*,
*am*, *is*, *if*, *no* can never match anything, in either direction. That is my
bug, not a property of his registry, and it is separate from the vocabulary gap.

This is the absence already on the record in WHAT EXISTS:

> *a rubric still holds a name and free text — not how it is recognised, nor how
> it is graded.*

The Samrath sentence is the cleanest proof of it so far, because his sentence is
ordinary human speech and his registry is clinical vocabulary. Nothing in between
exists yet.

## WHAT THE STRUCTURAL LAYER ACTUALLY PRODUCED — AND THE EIGHT DEFECTS IT EXPOSED

Run through `micro.decompose`, machine output, not description:

| # | Defect | Evidence |
|---|---|---|
| 1 | **"Samrath" is invisible.** The named actor of the whole story is not an entity — only pronouns are found. | `entities: [{'surface':'he','kind':'pronoun'}]` |
| 2 | **"cry" is not an action.** The behaviour the sentence is about is dropped. | `actions: [{'verb':'go'}]` — no `cry` |
| 3 | **"very happy" produces no emotion clue.** The one explicitly stated feeling in the ask is missed. | `emotion_clues: []` on S2 |
| 4 | **"today" is not a temporal marker.** The sentence whose whole meaning is *today* reads as timeless. | `temporal_relation: 'no order marked in this sentence'` on S2 |
| 5 | **The expectation break is put on the wrong sentence, with invented content.** S1 is the standing state; the break is in S2. | S1: `expected_information: "what the marker 'always' names"` / `actual_information: 'did not happen'` — nothing in S1 says anything did not happen |
| 6 | **`possible_human_effect` is a template from another case.** | S1 → `['disappointment','distrust','accumulated tiredness','wearing down']` — the disclosure/withholding list, applied to a child and school |
| 7 | **"but" is not read as the pivot.** The contrast marker that carries the entire ask is not recorded anywhere. | no pivot field, no discourse marker |
| 8 | **`claims` misfires on "never".** It flags a *reported behaviour of a third party* as the owner's own value generalization. | `status: 'USER VALUE / GENERALIZATION', trigger: 'never'` |

Also confirmed: `repetition.read_repetition` returns `applies: False` — "go to
school" is not an information-seeking action, so the ordinal-position machinery
(CHECK #1 acquires, CHECK #2-5 cannot) covers **information repetition only, not
behavioural repetition**. Samrath's "always cry" is behavioural. That axis is not
built.

## THE PARSE ERROR AT THE CENTRE OF THE SENTENCE

**"never like to go" ≠ "never goes".**

The negation attaches to *liking*, not to *going*. The source never says he does
not attend. A machine that concludes *refusal* has added a fact. This is the same
law as his own correction on "left": **the word does not mean the obvious thing**
(`docs/method/canon/LEFT_AND_NOTHING_HIS_CORRECTION.md`). So
`CON-061.13 Avoidance behaviour` is **HELD, not hit**.

## THE ANSWER TO THE SENTENCE ITSELF

Same actor. Same event — going to school. Opposite outcome.

**The event did not change. The condition around it changed.**

- `never` / `always` set a **standing state** — the rule as of yesterday.
- `today` / `birthday` set a **one-day condition** that overrides it.
- `but` is the hinge that says the second sentence is the exception to the first.
- `went very happy` is the **same physical action** as every crying morning —
  same going, different function. The going was never the thing. The condition
  was.

This is his mall principle exactly: *"Event is same going to mall / but the
intent is keep changing."* And his registry already names the trap: **CON-069.23
Situational vs dispositional attribution** and **CON-069.24
Fundamental-attribution-error tendency** — is Samrath a crying kind of child, or
is school the condition? The sentence answers it: **the condition**.

**Why he cried is NOT in this text.** Fear, sadness, frustration, separation,
something at school — the source does not say, and one event never yields intent.
`intent: UNKNOWN — not directly observed`, and it stays that way.

## THE ARROW CHART — MY READING, LABELLED AS MINE

Machine-lexical: 0. Below is the reading a semantic router *would* have to
produce, written in **his own parameter names**, tiered so he can correct any
row. Marked **MY READING** the same way `HIS ASSIGNMENT` is marked in
`domains.HIS_CONTAINER_TARGETS`.

- **word-carried** — the words themselves carry it.
- **pivot-carried** — only appears when both sentences are held together.
- **HELD** — named, never concluded.

```
3204
 -> SEG-02 Perception and Body Representation                [HIT 7]
      -> CON-014 Salience and Orienting                       [HIT 4]
           HIT  CON-014.23 Habituation to repeats             (word)
           HIT  CON-014.11 Change detection                   (pivot)
           HIT  CON-014.24 Dishabituation on change           (pivot)
           HIT  CON-014.32 Prediction-error salience          (pivot)
      -> CON-016 Spatial, Temporal and Environmental Mapping  [HIT 3]
           HIT  CON-016.23 Temporal-order coding              (word)
           HIT  CON-016.26 Time-of-day sense                  (word)
           HIT  CON-016.29 Event-boundary detection           (word)
 -> SEG-03 Sensorimotor Action and Physical Execution        [HIT 3]
      -> CON-020 Action Selection and Initiation              [HIT 3]
           HIT  CON-020.06 Go decision                        (pivot)
           HIT  CON-020.15 Approach-vs-avoid selection        (pivot)
           HIT  CON-020.27 Habitual-vs-goal arbitration       (pivot)
 -> SEG-04 Attention and Executive Control                   [HIT 1]
      -> CON-030 Cognitive Flexibility                        [HIT 1]
           HIT  CON-030.21 Context-dependent switching        (pivot)
 -> SEG-05 Learning, Memory and Knowledge                    [HIT 17 | HELD 2]
      -> CON-033 Episodic Memory                              [HIT 5]
           HIT  CON-033.03 What-happened coding               (word)
           HIT  CON-033.04 Where (place) coding               (word)
           HIT  CON-033.05 When (time) coding                 (word)
           HIT  CON-033.06 Who (participants) coding          (word)
           HIT  CON-033.07 Event-order coding                 (word)
      -> CON-035 Procedural and Habit Memory                  [HIT 2 | HELD 2]
           HIT  CON-035.07 Stimulus-response habit            (word)
           HIT  CON-035.14 Context-cued habit                 (word)
           HELD CON-035.31 Ritual/routine storage
           HELD CON-035.39 Habit-reversal capacity            (one day is not a reversal)
      -> CON-036 Associative Learning and Conditioning        [HIT 4]
           HIT  CON-036.03 Context association                (pivot)
           HIT  CON-036.16 Contingency detection              (pivot)
           HIT  CON-036.25 Renewal (context)                  (pivot)
           HIT  CON-036.27 Occasion setting                   (pivot)   <- the birthday, by his own name for it
      -> CON-037 Reinforcement and Reward Learning            [HIT 3]
           HIT  CON-037.01 Reward prediction                  (pivot)
           HIT  CON-037.02 Reward-prediction error            (pivot)
           HIT  CON-037.03 Positive-prediction-error learning (pivot)
      -> CON-038 Emotional and Threat Memory                  [HIT 3]
           HIT  CON-038.04 Affective tagging                  (pivot)
           HIT  CON-038.11 Positive-emotional memory          (pivot)
           HIT  CON-038.25 Mood-congruent encoding            (pivot)
 -> SEG-06 Reasoning, Planning, Decision and Creativity      [HIT 5]
      -> CON-043 Causal, Counterfactual and Predictive        [HIT 3]
           HIT  CON-043.19 Enabling-condition reasoning       (pivot)
           HIT  CON-043.24 Outcome prediction                 (pivot)
           HIT  CON-043.31 Prediction-error checking          (pivot)
      -> CON-044 Uncertainty, Probability and Confidence      [HIT 2]
           HIT  CON-044.38 Surprise quantification            (pivot)
           HIT  CON-044.39 Belief-strength tracking           (pivot)
 -> SEG-07 Language and Communication                        [HIT 10 | HELD 1]
      -> CON-052 Comprehension and Discourse Integration      [HIT 9]
           HIT  CON-052.03 Cross-sentence linkage             (word)
           HIT  CON-052.05 Pronoun/anaphora resolution        (word)
           HIT  CON-052.06 Coreference tracking               (word)
           HIT  CON-052.16 Situation-model construction       (word)
           HIT  CON-052.17 Mental-model updating              (word)
           HIT  CON-052.19 Temporal-connective processing     (word)
           HIT  CON-052.20 Discourse-marker use               (word)   <- "but"
           HIT  CON-052.26 Inconsistency detection            (pivot)
           HIT  CON-052.34 Ambiguity holding                  (pivot)
      -> CON-054 Pragmatics and Implied Meaning               [HELD 1]
           HELD CON-054.23 Deixis resolution (I/you/here/now) ("today" has no date)
      -> CON-055 Prosody, Gesture and Non-Verbal              [HIT 1]
           HIT  CON-055.12 Facial-expression production       (word)   <- the crying, as signal
 -> SEG-08 Emotion, Motivation, Intent and Motive            [HIT 6 | HELD 16]
      -> CON-057 Emotion Generation and Affective State       [HIT 4 | HELD 5]
           HIT  CON-057.01 Core valence (positive/negative)   (word)
           HIT  CON-057.12 Happiness                          (word)   <- stated
           HIT  CON-057.40 Emotional intensity                (word)   <- "very"
           HIT  CON-057.42 Emotional-state transition         (pivot)
           HELD CON-057.03 Fear
           HELD CON-057.04 Anxiety
           HELD CON-057.06 Frustration
           HELD CON-057.08 Sadness
           HELD CON-057.10 Disappointment
              -- "cry" is the behaviour. WHICH of these five it is, is NOT stated.
      -> CON-058 Emotion Recognition and Labelling            [HELD 2]
           HELD CON-058.17 Emotion-cause attribution
           HELD CON-058.22 Masked-emotion detection
      -> CON-060 Positive Valence and Reward                  [HIT 2 | HELD 1]
           HIT  CON-060.12 Approach behaviour                 (pivot)
           HIT  CON-060.35 Reward contrast (better/worse)     (pivot)
           HELD CON-060.06 Anticipatory pleasure
      -> CON-061 Negative Valence, Threat and Loss            [HELD 4]
           HELD CON-061.13 Avoidance behaviour   <- HELD: "never like to go" is not "never goes"
           HELD CON-061.18 Frustration (goal blockage)
           HELD CON-061.22 Worry/anticipatory dread
           HELD CON-061.26 Safety-seeking
      -> CON-063 Intent Formation and Commitment              [HELD 1]
           HELD CON-063.24 Contingent intention (only if X)
      -> CON-064 Motive, Needs, Values and Priority Structure [HELD 3]
           HELD CON-064.01 Stated motive                       (none stated)
           HELD CON-064.03 Hidden-motive hypothesis
           HELD CON-064.40 Motive-inference confidence         (LOW — one event)
 -> SEG-09 Consciousness, Self and Social Intelligence       [HIT 2 | HELD 2]
      -> CON-069 Theory of Mind and Social Prediction         [HIT 2]
           HIT  CON-069.23 Situational vs dispositional attribution   (pivot)
           HIT  CON-069.24 Fundamental-attribution-error tendency     (pivot)
      -> CON-071 Attachment, Belonging, Status and Group      [HELD 2]
           HELD CON-071.11 Belonging need     (birthday -> attention is world knowledge, not source)
           HELD CON-071.15 Inclusion seeking
 -> SEG-10 Development, Metacognition and Adaptation         [HELD 2]
      -> CON-073 Development and Maturation                    [HELD 2]
           HELD CON-073.16 Emotion-regulation development     (his age is not stated)
           HELD CON-073.18 Peer-relationship development
```

### THE COUNT

| | machine, today | MY READING |
|---|---|---|
| **of 3,204 sub-parameters** | **0 HIT** | **51 HIT · 23 HELD OPEN = 74 touched** |
| of 80 containers | 0 | 16 hit · 7 held-only · **23 touched** |
| of 10 segments | 0 | 8 hit · **9 touched** |

**SEG-01 Biological Regulation and Internal State is the only one silent** — and
that is correct. Crying has a physiology, but the sentence does not report a
body. Under his own ruling (**Human = the body, not the brain**), the Human
physical brain must not fire on a sentence that never mentions a body. It
doesn't. That part holds.

## THE ROUTE FROM 0 TO HIS CHART — SURFACED, NOT BUILT

Word-matching cannot get there and no amount of tuning will fix it. But there is
a route that needs no guessing, and it is already half-present:

**`micro.py` extracts FIELDS. His registry NAMES those exact fields.**

| micro.py field | his own parameter name |
|---|---|
| ENTITY | CON-033.06 Who (participants) coding |
| TEMPORAL RELATION | CON-033.05 When (time) coding · CON-016.23 Temporal-order coding |
| place | CON-033.04 Where (place) coding |
| EXPECTED vs ACTUAL | CON-037.02 Reward-prediction error · CON-043.31 Prediction-error checking · CON-044.38 Surprise quantification |
| REPETITION LINK | CON-014.23 Habituation to repeats · CON-035.14 Context-cued habit |
| NEGATION + condition | CON-036.27 Occasion setting |
| INTENT (held) | CON-064.40 Motive-inference confidence |

So the router is **field → parameter**, not word → parameter. That is mechanical,
it is checkable, and every row above under *(word)* or *(pivot)* was produced by
exactly that logic by hand.

**Nothing has been built for this. It waits on his word.** The eight parse
defects above are a separate, smaller job and also wait on his word.

## OPEN, NOT DECIDED

- Whether the field→parameter table is authored by me and corrected by him, or
  authored by him from the start.
- His standing seam, untouched: *"rubric means paramters the 3000"* against
  *"Human Parameter ≠ Rubric"*.
- Behavioural repetition has no ordinal-position axis; only information
  repetition does.
