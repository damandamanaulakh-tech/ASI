# SAME ACTION / CHANGED FUNCTION — and the MASK by OBSERVER POSITION

**Provenance.** Owner, 2026-08-13, from his fictional father/door example. He chose
these two himself: *"go for 1 & 3"*. Filed with his source untouched.

**HIS RAW SOURCE — `SRC-001`, immutable:**

```text
"A father checks the front door five times every night.
 Their house was robbed once years ago.
 The lock has since been replaced and he knows he already
 checked it, but he goes back again because he says he wants
 his family safe.
 His family gets irritated."
```

## 1 · SAME ACTION / CHANGED FUNCTION

His words:

```text
CHECK #1      → obtains information: "door is locked."
CHECK #2–5    → may no longer primarily obtain new information

identical physical action  ≠  identical functional role
```

> *"That's a powerful ASI principle."*
> Generalises to: asking once vs asking a fifth time · checking once vs checking
> a fifth time · reading once vs rereading · confirming once vs reconfirming ·
> calling once vs repeated calling.

**Why the machine could not hold this.** `micro.py` derives every structural fact
from CONTENT. Five checks of one door produce five micro-sequences with the same
entities, same action, same facts and the **same signature** — so
`group_repeats` clustered them as one arrangement with support 5 and reported
"this recurs", which is the wrong reading. The difference he found is not in the
content. It is the **ordinal position within the repetition**.

**What was built — `repetition.py`:**

* `read_repetition()` adds the missing axis: **where** an occurrence sits.
  `stated_count()` takes the number from the source ("five times" → 5; "again" →
  at least 2, exact number not stated; nothing → one occurrence, *absent, not
  zero and not many*).
* The FIRST occurrence **acquires**. A LATER one **cannot be acquiring what the
  first already acquired** — but only when the source says the actor already
  knows. Without that, the later occurrence is `OPEN`, because acquisition
  cannot be ruled out.
* What the later checks ARE doing is **held open with his six candidates and
  none chosen**: certainty · reassurance · ritual · responsibility expression ·
  risk reduction · habit. The row carries *"the machine does not pick which of
  these it is."*
* `position_signature()` is the fix: the first occurrence and the later ones now
  have **different addresses** (`…|occ:first` vs `…|occ:later`), so the pattern
  layer can see a difference where the words show none. The content part of the
  signature is preserved.

## 3 · THE MASK, BY OBSERVER POSITION

His words:

```text
Father's view : check door · MEANING protect family · VALUE safety
Family's view : the SAME behaviour · possibly excessive · RESULT irritation
ASI view      : same behaviour + different observers = different meaning

BEHAVIOR ≠ MEANING
Meaning is actor/observer dependent until evidence resolves it.
```

**No new mechanism.** This is Filter 3 / Source, already running: one witness
caps at Medium; **two witnesses who differ HALT, the gap is the Mask, it goes to
him, and it is never averaged.** Here the two witnesses are one event seen from
two positions, so the rule is reused rather than reinvented.

`read_views()` returns:

| position | marker | state | status |
|---|---|---|---|
| ACTOR | "because he" | safe | SOURCE-STATED — *a stated reason and the underlying mechanism are not necessarily the same thing* |
| OBSERVER | "his family" | irritated | SOURCE-REPORTED — *not evidence that the observer's reading is correct* |

→ **HALT — the gap goes to him.** *"It is not averaged, and neither reading is
preferred over the other."* One view only → capped at **Medium**. No marked view
→ it says so rather than inventing one.

---

## TWO BUGS FOUND WHILE BUILDING, BOTH RECORDED

1. **States bled between the two views.** A character-window search handed the
   observer the actor's "safe". Fixed by attributing states **per sentence**, and
   by preferring the sentence where the marker and a state word co-occur —
   because "his family" appears both in the clause about wanting them SAFE and in
   the clause about them being IRRITATED.

2. **The browser caught what the unit tests missed.** The engine splits an ask
   into sentences, so `"checks five times"` (sentence 1) and `"he knows he
   already checked it"` (sentence 3) never met — and on the exact example this
   was built for, the app displayed **"not supported yet"**. The unit test passed
   only because it called the function on the whole paragraph, which the engine
   never does. Both readings now run at **ASK level**; the per-sentence reading is
   kept because that is what the position signature uses. A test now asserts the
   count comes from sentence 1 and the knowledge from sentence 3, so this cannot
   regress silently.
