# 12b · THE REAL TEST, AND THE MAN

### What would actually prove it — written out in full — and what his life and his missing paper change about the question

**The owner's ask, verbatim:** *"with your own words, if 50000 or ur test prove — it will
prove RH (need real test later, but yes full detailed), how His Biography, missed paper,
how it change meanings."*

**So this article does three things.** It answers the conditional honestly — *if* a test
proved it, what would that test have to be — and it writes that test out in full rather
than gesturing at it. It tells the man's life. And it says what the life and the missing
paper change about how the hypothesis should be read.

**In my own words**, as asked. Where I am certain I say so; where I am reading, I say
that too.

---

# PART ONE · THE HONEST ANSWER FIRST

## The census cannot prove it, and the reason is not a limitation of the machine

Our census holds **63,519 zeros to height 50,000, with an exact ledger and zero deficit.**
It could hold six billion and the situation would be identical.

**The hypothesis is a claim about a totality.** *Every* non-trivial zero. Forever. There
is no largest one; Hardy proved in 1914 that infinitely many lie on the line, and the
count grows without bound. **Any height you reach is a middle, never an end.**

So a census is not a weak proof or a partial proof. **It is not that kind of object at
all.** You cannot approach infinity by getting further along it. Every zero we verified was
already believed to be there, and verifying it changed nothing about the ones we did not
reach.

**This is not pessimism about computing. It is the shape of the problem**, and stating it
early is what lets the rest of the article be useful rather than hopeful.

## But the asymmetry is real, and it matters

**A census can never prove the hypothesis. A census could kill it in an afternoon.**

One zero found off the line, verified, ends the question permanently. That is a genuine
asymmetry and it is the honest description of what every computation in this field is
doing: **not accumulating proof, but failing to find the counterexample.**

**Our 63,519 are 63,519 failures to falsify.** That is a real thing to have, and it is not
what most people think a census is for.

---

# PART TWO · THE REAL TEST, WRITTEN OUT

If a proof exists, its final line has one of three shapes. This is the enumeration from
the reverse walk — argued, not proved, and marked as such. **For each shape I write what
the test actually is: what must be built, what would count as success, and what would
count as failure.**

## SHAPE A · The self-mirrored source

**The last line reads:** *the zeros are the spectrum of a self-adjoint operator; the
spectrum of a self-adjoint operator is real; therefore the roots are real.*

**Why this shape is attractive:** it makes the hypothesis a *consequence* rather than a
coincidence. Self-adjoint operators have real spectra by construction — you do not check
each eigenvalue, you prove one property of the object and every eigenvalue follows. **That
is what a structural proof looks like: one fact about the thing, not infinitely many facts
about its parts.**

### The real test

**Build one mechanism that holds all three corners at once, unconditionally.**

| Corner | What the mechanism must produce |
|---|---|
| **LAW** | the correct number of eigenvalues below every height — matching N(T) exactly, not asymptotically-up-to-a-constant |
| **GUARD** | the correct statistics of the spacings — the pair correlation and higher correlations, not just the density |
| **MIRROR** | genuine self-adjointness — on a real Hilbert space, with a real domain, not a formal symmetry |

**Success:** all three from one construction, with no parameter fitted to the zeros and no
step that assumes the conclusion.

**Failure — and this is the measured state of the field:** every drum built so far
**secures two corners and pays the third.** Bend the operator to fix the count and the
statistics go wrong. Prime the statistics and self-adjointness becomes formal rather than
real. Tilt it toward self-adjointness and the count drifts.

**What our walk added here:** we measured what a true drum must contain — the return comb
with periods r·ln p and weights 1/(r²pʳ) — and followed it twice. **We named the gap; we
did not close it.** `[MEASURED + READING]`

**Honest assessment of this route:** it is the one most likely to be correct and the one
furthest from being achieved. Nobody knows how to get three corners from one mechanism,
and the difficulty is not technical stubbornness — it looks structural.

## SHAPE B · The impossible intruder

**The last line reads:** *suppose one zero lies off the middle. Then a quantity Q is
forced positive. But Q is non-positive for structural reasons. Contradiction.*

**Why this shape is attractive:** it needs no operator and no new object. It needs **one
quantity with two independent handles on it.**

### The real test

**Find a quantity Q with both properties, provably, and with the two proofs independent.**

1. **Every off-line zero forces Q > 0.** The off-line zero must contribute with a
   determined sign — no cancellation, no ambiguity from the mirror twin.
2. **The ground forces Q ≤ 0**, for reasons that do not themselves assume the hypothesis.

**The trap, and it has caught many attempts:** it is easy to find a Q where property 1
holds and property 2 is *equivalent to* the hypothesis. Then you have restated the problem
in new notation and proved nothing. **The two proofs must be genuinely independent, and
that independence is the whole difficulty.**

**Success:** both properties established, independence demonstrable, the contradiction
closing without circularity.

**Failure:** every candidate so far reduces property 2 back to the hypothesis, or gets
property 1 only under an assumption that already excludes off-line zeros.

## SHAPE C · The nature of ξ

**The last line reads:** *ξ belongs to a class of functions whose roots are all real;
membership in that class survives the limiting process that constructs ξ; therefore the
roots are real.*

**Why this shape is attractive:** it is the closest to what Riemann actually wrote. He said
the roots are real. **This shape proves exactly his sentence, in his terms.**

### The real test

Two parts, and the second is where it dies.

1. **Exhibit ξ as a limit of objects each of which is provably real-rooted.** Polynomials
   with real roots, or a family of entire functions in a known real-rooted class.
2. **Prove real-rootedness is not lost in the limit.** This is the hard half. Real-rootedness
   is *not* generally preserved under limits — roots can migrate off the real axis in the
   limit even when every approximant has them all on it. **You need a uniform control, not
   a pointwise one.**

**Success:** an explicit approximating family plus a preservation theorem strong enough to
carry the property across the boundary.

**Failure mode:** approximating families are constructible; the preservation theorem is
what nobody has.

**Note the connection to §Part One of article 12a:** this shape is the only one that
literally proves *die Wurzeln sind reell* as stated, rather than proving something
equivalent to it. If his sentence is taken as the thing to prove, **C is the native
shape.**

## SHAPE D · Transfer, and why it never closes

**The last line reads:** *statement X is proved, and X ⟺ RH.*

There are dozens of known equivalents. **Transfer alone is never a proof** — it relocates
the difficulty. The proof of X must itself have shape A, B or C.

**So D collapses. The true fork is A / B / C.** That is the whole space of last lines, on
the enumeration we could construct. `[SYNTHETIC — argued, not proved. If a fourth shape
exists, this enumeration is wrong, and that is the honest status.]`

## What our test would have to become

**To be a candidate at all**, the census would have to stop being a census.

It would have to become an instrument that measures a **structural** property — something
that holds of the object rather than of a finite sample. Concretely, the nearest honest
version:

- measure the return comb precisely enough to **constrain what mechanisms could produce
  it**, and narrow the space of possible drums;
- measure the statistics finely enough to **rule out whole classes** of candidate operator;
- do it with pre-registered nulls, so that what is found is not what was hoped for.

**That is a contribution to Shape A. It is not a proof and it does not become one by being
extended.** Reaching 500,000 or five million changes the numbers and changes nothing about
the logic.

**I would rather say this plainly than let a walk that reached 50,000 be read as a step
toward a proof. It is a step toward a better instrument, and instruments are how Shape A
would eventually be found — by someone, possibly not us.**

---

# PART THREE · THE MAN

Fifteen years of working life. Eight pages on this subject. Dead at thirty-nine.

## The life

**Born 17 September 1826**, Breselenz, in the Kingdom of Hanover. His father was a
Lutheran pastor who had been a soldier; the family was poor and stayed poor. His mother
died before her children were grown. Six children; several died young; **he outlived only
some of his siblings and supported those who survived.** `[FACT — standard biography]`

He was **painfully shy**, physically frail, and prone to breakdowns under strain. He was
also, from boyhood, extraordinary at calculation — the schoolmaster's account is that he
outran what could be set for him.

**1846** — sent to Göttingen to read **theology**, at his father's wish, so he could
become a pastor and earn. He asked permission to switch to mathematics. **His father gave
it.** That permission is the hinge of the entire story: a poor pastor allowed his son to
abandon a paying vocation for a subject with no evident income.

**1847–49, Berlin** — Jacobi, Dirichlet, Steiner, Eisenstein. Dirichlet mattered most; the
relationship shaped how Riemann thought about analysis for the rest of his life.

**1851** — doctorate at Göttingen under **Gauss**, on complex function theory. Gauss, who
praised almost nobody, praised it.

**1854** — the habilitation lecture, *Über die Hypothesen, welche der Geometrie zu Grunde
liegen* — *On the hypotheses which lie at the foundations of geometry.* Gauss was present.
It is the lecture that made general relativity possible sixty years later, and it is where
Riemann **defines what he means by a hypothesis** — a point Part Four returns to.

**1857** — extraordinary professor. **1859** — full professor, succeeding Dirichlet. Also
1859: elected a corresponding member of the Berlin Academy.

**And this is the fact that changes how the eight pages read: the 1859 paper is his
thank-you for that election.** New members were expected to submit something. He was
thirty-two, newly promoted, with term starting, and he sent *"a small paper."*

**1862** — married Elise Koch. A daughter, Ida. In the same year he fell seriously ill;
**tuberculosis**, which he never shook.

He went repeatedly to Italy for the climate — the only treatment there was. He worked
there. **He died 20 July 1866 at Selasca on Lake Maggiore, aged thirty-nine.**

**Dedekind's account** has him working to the end, outdoors under a fig tree, with the
work unfinished in front of him. `[READING — Dedekind's memoir is the source; it is
affectionate and it is one witness.]`

**And then his papers were burned.** His housekeeper destroyed part of the Nachlass before
Dedekind could reach it. **We do not know what was in it.** `[READING — traditional
account, widely repeated, one chain of testimony.]`

## What survived, and what it showed sixty-six years later

**In 1932 Carl Ludwig Siegel went through what remained** of the working papers — the
sheets nobody had been able to read, dismissed for decades as chaos.

They were not chaos.

- Riemann had an **asymptotic expansion** for the function on the critical line. **Hardy
  and Littlewood rediscovered only its principal term in 1920 — sixty years later.**
- He used the **saddle-point method**, which the world did not have until Debye
  reintroduced it in **1909**.
- **He had computed zeros numerically.** He had actually calculated with it.

**This is the sharpest correction the record contains.** The paper is eight pages of
assertion with the working invisible. The working existed. It was in the drawer, in a hand
nobody could read, for sixty-six years — and it was ahead of the field by half a century
in two separate techniques.

**And Siegel's own honest counterweight, which must be quoted alongside:** *no approach to
a proof of the hypothesis exists in Riemann's papers.* He had extraordinary machinery. He
did not have a proof, and there is no sign he had one. `[FACT — Siegel 1932]`

---

# PART FOUR · THE MISSING PAPER

## What he said his main work was

`[ARCHIVE]` His own declaration, from his fragments: his **Hauptarbeit** — his main work —
was **a re-conception of the known laws of nature through different ground-concepts, in
order to explore their connection.**

Not new data. **A re-read of physics from a different set of primitives** — everything
flowing through a continuous medium; matter, force, perhaps mind, as processes in one
substrate rather than separate kinds of thing.

He drafted it. He carried its flagship a long way — the 1858 electrodynamics paper, in
which action **propagates** rather than jumping instantaneously across space, years before
that was the settled view. **And then he withheld it.** The same hand that struck words out
of his own fair copy.

**Nobody ever walked his road.** The world reached the same destinations — field theory,
unification, curved space — through Maxwell's concepts and Einstein's, not through his.

## The two things he promised and did not deliver

1. **The supplement to his 1854 lecture** — the part that would state the law behind it.
2. **The Hauptarbeit itself** — the re-conception of physical law.

**Both are missing, and the second may have been in the pages that burned.**

## What the paper we do have actually is

Given the above, the 1859 paper is **not a research programme.** It is:

- an **obligation of election**, written to a deadline;
- **eight pages**, in a form that assumes the reader will fill in the working;
- by a man whose main work was elsewhere and who thought of this as a small piece;
- with **the working deliberately not shown** — and now known to have existed;
- containing one item he explicitly marked as **provisionally left aside**;
- sent as an **enclosure** to a letter returning Gauss's unpublished prime material, which
  was open on his desk in the weeks he wrote.

---

# PART FIVE · HOW THIS CHANGES MEANINGS

## 1 · "Hypothesis" is his own defined term

He wrote *Über die **Hypothesen**, welche der Geometrie zu Grunde liegen* five years
earlier. **He had already given the word a technical meaning**: a hypothesis is a
foundational assumption a structure rests on, which experience can constrain but not
verify — and in the same lecture he speaks of *probability within the limits of
observation.*

**So when he calls this a hypothesis, he is using his own vocabulary, not hedging.** He is
naming it as *the kind of thing that grounds a structure and is answerable to observation
at the limits*. `[READING — but a well-founded one: the definition is his, in print, in
the same decade.]`

## 2 · "Probable" is not weakness

His sentence around the roots uses the language of probability — *wahrscheinlich* — and
this is usually read as tentativeness. Set beside the 1854 lecture, **it is a technical
placement**: a claim supported within the limits of observation, awaiting the structure
that would ground it.

**And set beside Siegel's finding, it is something else again: he had computed zeros.** He
was not guessing from elegance. He had looked.

## 3 · The eight pages are a fragment of a withheld body of work

**Before:** a short brilliant paper that leaves gaps.
**After:** the visible fraction of a much larger effort that was mostly never published and
partly destroyed — by a man who withheld his main work as a matter of habit.

**The gaps are not carelessness. They are the shape of what he chose to show.**

## 4 · The real gap is not mathematical

`[READING — and this is the owner's reading, which the walk confirms]`

The mathematics of the 1859 paper is not what is missing. What is missing is **what he
wanted it for.** He said his main work was a re-conception of natural law. He never said
how the primes served it.

**That is the gap. It is not a gap in a proof; it is a gap in an intention**, and it cannot
be closed by mathematics because it was never written down.

## 5 · He wanted it computed, not only proved

`[ARCHIVE]` On leaf 26r: *"it matters to me that my formula should also become known to
practical computers."* And his own unexecuted directive: **track the influence of the
individual periodic terms.**

**Change in meaning:** the entire computational tradition around this problem — every
census including ours — is closer to his stated wish than the search for a proof is. **He
asked for calculators. He got theorists.**

That does not make computation a proof. **It does mean that the instrument-building is
not a consolation prize for failing to prove; it is the thing he asked for.**

---

# WHAT THIS ARTICLE CLAIMS, AND WHAT IT DOES NOT

**Claims:**
- The census cannot prove the hypothesis, for structural reasons stated in Part One.
- Three shapes exhaust the possible last lines, on the enumeration given. `[SYNTHETIC]`
- Each shape's real test is written out with its success and failure conditions.
- The biography and the Siegel finding change how the eight pages should be read.

**Does not claim:**
- **No proof, no partial proof, no path claimed to be the path.**
- **No claim that our walk contributes to any of the three shapes yet.** It measures
  statistics among zeros already known to be on the line.
- **No claim that the enumeration is complete.** If a fourth shape exists, Part Two is
  wrong.
- Nothing about what was in the burned papers. **They are gone and speculation about them
  is not evidence.**

**The sentence I would keep if only one survived:**

> He had the machinery, he had computed with it, he had no proof, and his main work was
> somewhere else entirely — so the honest question is not why he failed to prove it, but
> what he thought it was *for*, and that is the one thing he never wrote down.
