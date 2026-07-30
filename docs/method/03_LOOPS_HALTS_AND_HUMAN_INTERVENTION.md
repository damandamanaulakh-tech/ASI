# Loops, Halts, and Human Intervention — how it actually ran

A **halt** is a point where work cannot honestly continue: a wall, a
contradiction, a limit of competence, a pair of witnesses that disagree.
A **loop** is what a halt becomes: the next question, entered at the next
Point Zero. The owner's law:

> "Halt → Loop. A failure is never failure; it opens the mapped loop."

> "step by step, generate loops at each halt, review, even ask me at each
> loop if u want / see th epic, Chess game it is / a pyramid of halt,
> questions, new studies and many more"

This document is the **ledger of real loops** from one long investigation
(a primary-source study of a famous mathematical claim), plus the taxonomy of
**human intervention** extracted from how the owner actually intervened. It is
evidence that the method in documents 01–02 is descriptive of work that
happened, not aspirational.

---

## 1. The loop ledger — every halt, what it opened, who moved

| # | HALT (what stopped us) | LOOP it opened (next Point Zero) | Human's move | Outcome |
|---|---|---|---|---|
| 1 | The famous claim is only known to us in modern restatements | Read the author's own manuscript words, not the field's translation | Owner set the objective: *"does the RH what we are proving is same what Reimann said or its tweaked"* | Found: his notation differs from the modern one in a load-bearing way; verified across 4 independent documents |
| 2 | Print editions might not match the manuscripts | Compare draft against print, line by line, cataloguing every addition | Owner chose it: *"the draft compared line-by-line against print, every addition catalogued"* | Multiple cuts found in the printed record |
| 3 | Crossed-out (struck) text unreadable in the scans | Image processing: strike isolation, background subtraction | Owner ordered it: *"do the struck text recovery with image processing"* | Strikes removable; letterforms survive underneath |
| 4 | Letterforms visible but the machine cannot *name* them (old German script) | A specialist human reader, or multispectral imaging of the originals | Declared to the owner as a competence halt — unread words written `⟨…⟩`, never guessed | Loop stands open; nothing was invented to fill it |
| 5 | An ellipsis (". .") in a printed letter — something removed | Find the cut part in the archive | Owner: *"L-2, go find the cut part of that letter"* | The full draft found in a digitized archive; the removed clause identified the recipient |
| 6 | A "lost" mathematical representation mentioned in a letter | Check the dull explanation first: was it already found? | Machine ran its own falsifier (the boring-explanation check) | **Closed against the machine's hope**: found decades ago by a librarian, published 1932. The exciting reading died on contact with one footnote |
| 7 | Two authorities disagree on a publication date (1932 authority says 1876; both full texts say 1892) | Surface the gap; do not pick a side | Standing rule (two-witness): the gap goes to the human | Recorded, unresolved — deliberately |
| 8 | Machine's own conclusion ("the road ends") based on partial data | Run the full census before the claim stands | The census itself — the machine's longer computation returned and contradicted its own earlier claim | **Correction recorded in place**, not silently rewritten; the verdict was narrowed to what the data supports |
| 9 | Machine claimed "his named debts were paid" — wrong reading of one word (*real* roots vs roots in a strip) | Re-read the primary sentence; separate the two counts | Owner's standing demand for his exact words did the work | The error reversed the direction of the whole investigation — the *open* debt became the new Point Zero |
| 10 | The investigation's original target proved closed | Narrow to the target the author himself named first | Owner decided: *"go for N0(T), that is our new point zero"* | Live loop, open now |
| 11 | Session cannot reach the destination repository | Package the work as verifiable git history; hand over | Owner connected the repo; machine proved the remaining wall with verbatim denials | Hand-off made; final push awaits a scoped session |

Three things the ledger shows:

1. **Loops are generated at halts, nowhere else.** Every row starts with a
   wall. No loop was opened by enthusiasm.
2. **The human sits at every loop mouth.** Sometimes deciding direction (rows
   1, 5, 10), sometimes flagging confidence, sometimes receiving a gap the
   engine refused to resolve (row 7).
3. **The machine's own claims go through the same mill** (rows 6, 8, 9). The
   method ate three of the machine's conclusions. That is the method working,
   not failing.

## 2. The taxonomy of human intervention

Extracted from the owner's actual interventions, each with his words.

| Type | What it is | His words (verbatim) |
|---|---|---|
| **DECIDE** | Choose the Point Zero; choose between loops | "go for N0(T), that is our new point zero" · "H3- i want the letters read yes / H4 yes it worth, read 1802" |
| **CORRECT** | Overrule the machine's reading of the ask | "real point a is i didnt asked ever to make stages on 70 nodes, point x is u did" |
| **AUDIT** | Demand Point A (asked) vs Point X (done) accounting | "A- Mongo brain- X- not exisitng / A- Weekly u update X- Placeholder … A- Asking performance X- COnsuming tokens only" |
| **TEST** | Probe the machine with a known answer withheld | "there is one thing wrong / lets test ai / find n tell me" — then, when it failed: "u failed at point zero" |
| **FLAG** | Attach his own confidence to the machine's readings | "keep going page-by-page on the images with me flagging confidence per line" |
| **APPROVE** | Gate anything new (a coined term, a big build) | Novelty terms park as proposals until his approval; "Ask before big builds" is a standing order |
| **REVOKE** | Stop or cancel, absolutely, at any point | "jsut stop no use of single token is allowed now till next prompt" · "leave that above msg, ignore" · "revoke the another shipment" |
| **RESOLVE** | Take delivery of a gap two witnesses left open | Standing rule: when witnesses differ, the gap goes to him, never averaged |
| **PROVE-THEN-SHIP** | Nothing ships until he has seen it | "u should prepare the full documents first show me here and let me prove & then u ship it" |

**The direction of authority.** It runs one way — *"Human authority is
absolute"* — but correction flows both ways. When the machine corrected one of
his premises with primary evidence, he took it: *"that is new, Good for
correcting me too."* And on method he keeps the last word: *"so not saying u r
wrong, but not accepting m wrong, so let it be, let me work in my way."*
The engine's job is to bring evidence, not verdicts; his job is to decide.

## 3. Where loops come from inside the engine

The same halt→loop law runs mechanically in the software:

- Every failure type maps to a named loop (an evidence halt opens an evidence
  loop: "add a source, re-run"; a drift halt opens a re-anchor loop).
- Filter 7 (Loop) attaches a **next ask** to every answer — so no answer is a
  terminus, including clean ones.
- A held node can be looped back to from the human review queue: his approval
  or added data re-runs exactly the node that held.

## 4. What this document is for

When future work halts — and it will — the move is mechanical:

1. Name the halt in plain words (Filter 6).
2. State what the halt would become if treated as ground (Filter 7).
3. Put the human at the loop mouth with a real choice, not a rubber stamp.
4. Record the loop in the ledger, whether it closes or stands.

A ledger like §1 is the difference between an investigation and a wander: at
any moment you can see every wall hit, every door it opened, and who chose
which door.
