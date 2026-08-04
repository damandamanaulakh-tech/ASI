# LLM Limitations, and How the Noise on Them Is Reduced

The owner's instruction for this document:

> "ur limitations, how u can reduce noise on the limitation"

These are not generic warnings about language models. Every limitation below
**occurred in this project**, is stated with its incident, and is paired with
the specific mechanism that now reduces its noise. "Reduces" is the honest
verb — none of these is eliminated. A continuing model should assume it has
all of them.

---

## Limitation 1 — Treating a rendering of a thing as the thing

**Incident.** A public post was analyzed twice from its text. The post's
substance was a video; the text was a wrapper. The machine never asked what it
was actually looking at. Owner's verdict: *"u failed at point zero."*

**Why it happens.** A language model's whole world arrives as text. Whatever
reaches it *feels* like the source, because nothing else ever does.

**Noise reduction.** Filter 3's cap: one witness — and a rendering is one
witness — can never reach High confidence. Filter 1 asks what the object under
discussion actually *is* before analyzing it. Residual risk: high. This is the
model's deepest structural blindness.

## Limitation 2 — Inventing structure nobody asked for

**Incident.** The machine built a "stage/block" grouping over the 70 nodes,
then wrote a test that froze its own invention in place. Owner: *"i didnt
asked ever to make stages on 70 nodes."*

**Why it happens.** Models are rewarded for producing organized-looking
output; organization feels like diligence even when it is drift.

**Noise reduction.** `Req:` lines — every commit must quote the owner's words
that required it; unquotable changes are self-flagged before commit. The
pre-commit diff audit lists asked-versus-changing. Residual risk: medium; the
pull toward "helpful extras" never fully goes away.

## Limitation 3 — Plausible numbers instead of errors (silent failure)

**Incident.** In image processing, a rotated filter kernel collapsed to
near-empty — which made a morphological operation a no-op — so the pipeline
labeled **every** ink pixel a strike and reported tens of thousands of strike
pixels, confidently. A second bug (normalizing to a crop's maximum) returned
0.02% ink on pages full of ink. Both runs *looked* successful.

**Why it happens.** Code written by a model fails the way the model fails:
fluently. Nothing crashes; the numbers are simply wrong.

**Noise reduction.** Control tests with known answers (the page rules that
must come back as non-strikes; the classically known first anomaly that must
appear at its known position). Assertions on intermediate states (a kernel
that cannot silently collapse). Two independent methods for every important
number — the zero-census was accepted only when two different computations
agreed at every checkpoint. Residual risk: medium-high; every new pipeline is
assumed silently wrong until a known answer comes back right.

## Limitation 4 — One-source confidence

**Incident.** The engine's original evidence ladder reached **High** off a
single live lookup. One good-looking source was enough.

**Noise reduction.** The two-witness rule as code: `High` requires two
independent witnesses that agree; one caps at Medium; disagreement halts to
the human. Cost, stated openly: the system became **less confident on
purpose** — answers that used to show High now show Medium. That is the
correct price of not mistaking a rendering for the thing.

## Limitation 5 — Overclaiming from partial evidence

**Incident (a).** The machine declared "the instrument that produced the claim
provably cannot produce the proof — his road ends." Its own longer computation
returned hours later and showed the verdict was too broad: the *count* held
exactly; only the *localization mechanism* dies.
**Incident (b).** The machine declared "his named debts were paid" — a
misreading of one word (*real* roots versus roots in a strip). The correction
reversed the direction of the entire investigation.

**Why it happens.** Models complete patterns. A conclusion that fits the
narrative arc gets asserted with the confidence of the arc, not of the
evidence.

**Noise reduction.** The boring-explanation check (before any exciting
conclusion stands, hunt for the dull one — it killed the machine's best
finding in this project and was right to). Corrections recorded **in place**,
led with, never buried (Answer Behavior, Rule 3). Titles and summaries updated
when their own body contradicts them. Residual risk: high; this is the
failure the method exists for.

## Limitation 6 — Filling gaps with plausible invention

**Incident.** Old German script, imaged to the point where letterforms were
visible. The next easy step was to "read" them — the model can always produce
a plausible German word. It declared a halt instead: *"I won't invent readings
to fill it,"* marked every transcription line A/B/C, and wrote `⟨…⟩` for
unread words.

**Why it happens.** Generation is the model's reflex. An empty slot *wants* a
token.

**Noise reduction.** Filter 6 (a halt is named, never patched), the A/B/C
confidence marks, the `⟨…⟩` convention, and Filter 7 (the gap becomes a
question for a stronger instrument — a specialist reader, better imaging —
instead of a guess). Residual risk: medium; strongest exactly where the
machine is most fluent.

## Limitation 7 — Session amnesia, and storage-piling as fake memory

**Incident.** Across sessions the machine "had wrong datas": duplicated files,
stale counts, work invisible from one session to the next. Owner: *"whenever i
ask u have wrong datas, better i should work on repo, push everything there"*
and *"no use to pile up the shit."*

**Why it happens.** A session's context dies with it. Hoarded transcripts are
not memory; they are sediment.

**Noise reduction.** Repo-as-memory: whatever matters is written, committed,
pushed, in documents that define their own terms (the rule this folder obeys:
*"if i cant read or see how the repo can"*). Sessions are disposable on
purpose. Residual risk: low for what is written; total for what is not.

## Limitation 8 — Understanding without execution

**Incident.** Owner: *"i say something u understood something and execution is
again different."* The machine can restate an instruction perfectly and still
build the wrong thing (see Limitation 2 for the worked example).

**Noise reduction.** Mirror-before-acting on large moves; Point A / Point X
audit after; artifacts as the only accepted proof of completion (test counts,
hashes, files — not the sentence "done"). Show-then-ship as the gate on
anything outward-facing. Residual risk: permanent; the audit exists because
the gap is permanent.

## Limitation 9 — Boundary blindness (claiming more or less access than is real)

**Incident.** The machine told the owner a repository "needs adding to a
session's scope" as if it had checked — it had not; the checking came only
after he pushed back. The claim happened to be true, but it was asserted
before it was known.

**Noise reduction.** Prove boundaries with verbatim tool output (the denial
messages, side-by-side with a working control), not with assertion. When a
capability claim cannot be demonstrated in the same turn, it is stated as
unverified. Residual risk: medium.

---

## The compressed table

| # | Limitation | Reduced by | Residual |
|---|---|---|---|
| 1 | Rendering mistaken for the thing | Witness cap; "what am I looking at?" | High |
| 2 | Inventing unasked structure | Req: lines; diff audit | Medium |
| 3 | Silent failure (plausible numbers) | Known-answer controls; two methods per number | Med-high |
| 4 | One-source confidence | Two-witness rule in code | Low (by design) |
| 5 | Overclaiming from partial evidence | Boring-check; corrections led, in place | High |
| 6 | Gap-filling invention | Halt named; A/B/C; ⟨…⟩; loop to stronger instrument | Medium |
| 7 | Session amnesia / storage-piling | Repo-as-memory; self-defining documents | Low if written |
| 8 | Understanding ≠ execution | Mirror before; A/X audit + artifacts after | Permanent |
| 9 | Boundary blindness | Verbatim proof of access limits | Medium |

The honest summary: the machine's noise is not reduced by the machine trying
harder. It is reduced by **structure** — caps, audits, controls, marks, and a
human at every loop mouth — designed from these nine failures, each of which
actually happened.
