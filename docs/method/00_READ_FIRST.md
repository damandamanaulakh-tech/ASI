# READ FIRST — what this folder is, and every term it uses

This folder is the **method** of the Sourceborn project, written so that a
reader with zero context — a person, or a model in a fresh session — can read
it and work correctly. Nothing in here assumes you were present when it was
built.

**The rule this folder obeys, set by the owner:**

> "when u r making any documents it must b clear / u mentioned 7 nos, what is
> that 7, if i cant read or see how the repo can, so make proper documents"

So: **every term is defined at first use, in the document that uses it.** No
document points at a conversation. If a number is named, the things counted are
listed. If a shorthand appears, it is spelled out beside it.

---

## The project in one paragraph

**Sourceborn** is a private, continuously-learning reasoning engine built around
a base language model. It is not a new trained model; it is a **control layer**:
the model does the language work, and Sourceborn decides what counts as known,
what must halt, what goes to the human, and what is remembered. It clones its
owner's way of thinking and gets wiser with every use.

## Every term, defined once

| Term | Meaning |
|---|---|
| **Point Zero** | The owner's original ask, preserved in his exact words before any interpretation. Every run starts by locking it, and every answer is checked against it before delivery. |
| **SB node** | One of **70 "Sourceborn" working nodes** (SB-01 … SB-70). Each has one job (e.g. SB-01 locks the raw source; SB-20 runs the Doubt Engine) and its own on-disk brain that grows with use. |
| **URR node** | One of **25 "UnReal-to-Real" verifier nodes** (URR-01 … URR-25). Historically they reviewed the SB nodes' work. Today they are kept as **memory** (their brains still exist and grow) while reviewing is done by the seven filters below. |
| **The 95 brains** | 70 SB + 25 URR. Each is a JSON memory on disk with parameters that only grow (runs completed, patterns recognized, verifications performed). Nothing is ever deleted; only relative strength changes. |
| **The seven filters** | The method that reviews every piece of work, in order, every time: **1 Ground · 2 Sequence · 3 Source · 4 Mask · 5 Fact · 6 Halt · 7 Loop.** Each is defined one line down and fully in document 02. |
| **1 Ground** | Asks: does the thing being asked about exist before the asking? If yes, we are hunting a way to *say* it, not making it. If no, it is an invention and is treated differently. |
| **2 Sequence** | Asks: which step of the universal sequence (document 01) is this ask standing on? An ask about a failure needs the failure named, not patched. |
| **3 Source** | The two-witness rule. One source — however good — caps confidence at Medium. Two independent sources that agree reach High. Two that differ **halt**: the difference goes to the human, never averaged. |
| **4 Mask** | The owner's word for the gap between what was said and what was shown — a name standing in for a thing, a cut, a softening, an ellipsis hiding a clause. Masks are surfaced, never silently resolved. |
| **5 Fact** | Every claim in an answer carries a tag naming its source. An untagged claim does not leave the engine. |
| **6 Halt** | Where does this fail? The failure is named in the answer. A halt is never hidden and never "fixed" by inventing something to fill it. |
| **7 Loop** | The halt becomes the next Point Zero. The engine hands back the next question instead of pretending the road ended. In the owner's words: *"U need always a end point to verify, but that point is a point zero for new loop, that is halt, that is invention."* |
| **The universal sequence** | The owner's 8-step law of how anything comes to be known — Ground · Pressure · Use · Witness · Expression · Naming · Halt · Loop. Fully worked in document 01 with his own examples. |
| **Intent** | A **property of every event**, not a step. Every event, at every second, has one real reason that pushes it — whether or not it produced anything, and whether or not it was worth doing. Intent is *motivation*, not a stated plan, and it is read from how everything around the event was arranged. Full instruction in document 01A; **binding on every answer**. |
| **Witness (evidence sense)** | One independent account of a claim. A reprint, translation, or quotation of the same origin is **one** witness wearing two coats, not two. |
| **Confidence marks A/B/C** | Used in transcription and reading work: **A** confident · **B** probable, sense secure · **C** uncertain, flagged. An unreadable word is written `⟨…⟩`, never guessed. |
| **[READING] vs fact** | Anything the engine infers (rather than quotes) is marked as a reading. A reading can be overturned without anyone having lied. |
| **P-NEW** | A newly coined parameter (a term for something that fit no existing parameter). It exists only as a proposal until the human approves it. |
| **Req: lines** | Every commit message quotes the owner's exact words that required the change. If no words can be quoted, the change was not asked for. |
| **The owner** | The human. His authority is absolute: he can halt, reverse, or reject anything on his word. The engine proposes; he decides. |

## The documents in this folder

| Doc | What it holds |
|---|---|
| **01 THE UNIVERSAL SEQUENCE** | The 8 steps, defined; then worked fully on the owner's own examples: hunger, gravity, the Riemann Hypothesis, string theory, the water cycle, and the invention case (cricket). |
| **01A INTENT** | **Intent is a property of every event, not a step.** His paragraph as given, reframed with the depth on the surface, then each phrase with what it means and what an answer may no longer do. **Binding on every answer.** |
| **02 THE SEVEN FILTERS** | Each filter: the question it asks, what pass and hold mean, and a real incident from this project where it worked. |
| **03 LOOPS, HALTS, AND HUMAN INTERVENTION** | How and where loops were actually generated in live work — a ledger of real halts, the loop each opened, and where the human stepped in. |
| **04 ANSWER BEHAVIOR** | How the system answers — each rule fetched from a real final answer, quoted as the specimen. |
| **05 HOW THE OWNER PREPARED THE ASI** | His teaching method, in his own words: example-then-correction, Point A vs Point X audits, withholding until acceptance, testing the machine. Private content is not here — only the method. |
| **06 LLM LIMITATIONS AND NOISE REDUCTION** | The machine's observed failure modes in this project — each one a real incident — and the specific mechanism that reduces its noise. |

## Reading order

Read **01A before 01** — intent is a property of every event, so it applies
before any step does. Then 01 before 02 (the filters are the sequence turned
into gates), and 03 after 02 (the loops are the filters running on live work).
Documents 04–06 can be read in any order.

## What is deliberately NOT in this folder

- The owner's private corpus and personal documents. They live outside git, in
  a directory the repository ignores, and are loaded privately at runtime.
- The Riemann Hypothesis research itself. That investigation produced this
  method, and the method is what ships. The research record stays in its own
  archive.
