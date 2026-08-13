# HUMAN = THE PHYSICAL HUMAN, NOT THE BRAIN — HIS ONTOLOGY CORRECTION

**Provenance.** Owner, 2026-08-13, across two messages, with his own arrow charts
and his own container assignments. Filed unedited in substance. He closed with:
*"a stick for blind person, as u r blind to explore"* — his charts are the spec,
not illustration.

## THE RULE

```text
Human = the physical human: body, appearance, biological condition, safety,
        survival, ageing/life-extension, physical capacity.
Human is NOT the thinking/memory/reasoning brain.

MEMORY         ≠ HUMAN PHYSICAL
EMOTION        ≠ HUMAN PHYSICAL
REASONING      ≠ HUMAN PHYSICAL
MORALITY       ≠ HUMAN PHYSICAL
RESPONSIBILITY ≠ HUMAN PHYSICAL

BUT
bodily safety · survival · health · physical state · energy · ageing ·
appearance · physical capability · life continuation  = HUMAN
```

## HUMAN_DOMAIN_SCOPE — his lists

```text
INCLUDE: physical body · anatomy · physiology · appearance · health · damage ·
         repair · ageing · longevity · survival · physical capability
EXCLUDE: memory · reasoning · language · emotion interpretation ·
         decision cognition · metacognition · abstract intelligence
```

*"Those excluded things still exist in C-SB — they simply belong to Brain / AI /
ASI / other cognitive nodes, not your Human physical registry."*

## THE FINDING THAT FORCED THIS

> *"the current 2,560 registry in the repo presently contains many cognitive
> containers — memory, reasoning, language, emotion, social cognition — not only
> body parameters. So for the architecture you are defining, we should not
> automatically treat all 2,560 as 'Human runtime brain.'"*

> *"we should not rename all 2,560 as 'Human physical parameters' … we eventually
> need to separate the physical Human subset from the brain/cognitive subset
> **without deleting the original source records**."*

## HIS WORD-LEVEL ROUTING — sentence one

```text
"A good person left with memories of their beloved
 and responsibility keep them safe and alive"
   ├── GOOD            → WISDOM / VALUE NODE
   ├── PERSON          → HUMAN BODY NODE
   ├── LEFT WITH / GOT → RESULT / CONSEQUENCE NODE
   ├── MEMORIES        → MEMORY NODE
   ├── BELOVED         → RELATION / AFFECT NODE
   ├── RESPONSIBILITY  → RULE / DUTY / WISDOM NODE
   ├── KEEP SAFE       → HUMAN BODY PROTECTION → CON-006
   └── KEEP ALIVE      → HUMAN BODY SURVIVAL   → CON-001 · CON-008
```

Plus, on his clarification *"he keeps working for them"* → physical expenditure
→ **CON-007 Energy, Fatigue and Resource Budgeting**.

*"So this sentence does not 'hit the 2,560' as one block. It hits only a few
Human-body addresses, while other words go to other cognitive systems."*

## HIS ROUTING — sentence two, and the EXCLUSION node

```text
"Humans are looking at their physical appearance and body life extension,
 not the brain"
   ├── HUMAN               → physical human/body entity
   ├── "looking at"        → ATTENTION / PRIORITY / GOAL
   ├── "physical appearance"→ HUMAN BODY (visible body state, ageing appearance)
   ├── "body"              → HUMAN PHYSICAL SYSTEM
   ├── "life extension"    → HUMAN SURVIVAL / BIOLOGICAL CONTINUITY
   └── "not the brain"     → EXCLUSION / BOUNDARY
                              BRAIN/COGNITION explicitly NOT target
```

## THE SPLIT HE DISCOVERED IN HIS OWN DOCUMENT

> *"`CON-015 Body Schema, Body Image and Ownership` currently mixes physical and
> cognitive concepts."* — because **PHYSICAL APPEARANCE = actual visible/material
> body, NOT mental body-image representation.**

---

## WHAT WAS BUILT — `src/sourceborn/domains.py`

**An overlay. His 3,204 source records are untouched** — nothing renamed, nothing
deleted, nothing merged. `human_registry.py` still returns his document
byte-for-byte; this module sits on top and says which brain each container serves.

* **His eight node classes**, from his charts: HUMAN BODY · BRAIN / MIND ·
  RELATION / AFFECT · VALUE / WISDOM · RULE / DUTY / ASI · RESULT / CONSEQUENCE ·
  ATTENTION / PRIORITY / GOAL · EXCLUSION / BOUNDARY.
* **All 80 containers classified**: 18 HUMAN BODY · 39 BRAIN / MIND ·
  11 RELATION / AFFECT · 8 ATTENTION / GOAL · 2 RULE / DUTY · 2 VALUE / WISDOM.
* **11 containers marked MIXED**, each with the reason, including the one HE
  flagged — CON-015 — carrying his own words. Marked and surfaced, **not
  resolved**.
* **`route_words()`** is his arrow chart executable: every word to its own brain.
  Verified on his sentence: good→VALUE, person/safe/alive→HUMAN BODY,
  left with→RESULT, memories→BRAIN, beloved→RELATION,
  responsibility/keep them→RULE/DUTY.
* **`HIS_CONTAINER_TARGETS`** — the containers he named by hand. Lexical matching
  could never find them (nothing in CON-006's name contains "safe"), so they are
  recorded as **HIS ASSIGNMENT** and labelled that way wherever shown:
  safe→CON-006 · alive→CON-001+CON-008 · keep working→CON-007 ·
  appearance→CON-015+CON-011 · life extension→CON-001/003/005/007.
* **`enforce_scope()`** — a container may only be reported under HUMAN BODY if a
  word actually routed there. Before this, a sentence about memory pulled Human
  containers in on lexical overlap alone. A container that fails the check is
  **moved to `out_of_scope` with the reason**, so his first machine reading stays
  visible beside the corrected one.
* **The exclusion works**: on *"not the brain"*, BRAIN / MIND is reported OUT of
  scope and every brain container is moved out with his reason — never counted as
  a hit.

Four tests hold it, including one whose only job is to prove that the Human set
and the Brain set never overlap.

## STILL OPEN — surfaced, not decided

1. **The 11 MIXED containers.** His own document's names carry both a physical
   and a cognitive sense. He said preserve the distinction before building
   further; the overlay marks them, and which side each belongs to is his word.
2. **His registry is a broader organism+cognition model** than his Human role
   needs. The physical subset is now *addressable* through the overlay, but the
   source bank is still one bank — by his instruction.
