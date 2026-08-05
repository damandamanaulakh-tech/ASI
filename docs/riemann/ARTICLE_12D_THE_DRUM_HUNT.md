# 12d · THE DRUM HUNT

### Every candidate operator, which two corners it buys, which one it pays — and the test our census can apply

**Why this article exists.** Article 12c concluded that the quantum reading is primary,
because it is the only one that would *explain* the ½ rather than restate it. Article 12b
wrote the test: **build one mechanism holding law, guard and mirror at once,
unconditionally.**

**This article audits the attempts.** Not to rank them — to find what their failures have
in common, because a pattern across independent failures is worth more than any single
one.

**Evidence standing, stated first.** This audit is written from my own knowledge of the
literature. **No live search was available in this session.** By the project's own
Filter 3 that makes it **one witness, capped at Medium** — the structure of the argument
is sound and individual attributions should be checked against primary sources before
being relied on. Where I am unsure, I say so in the row.

---

# 1 · WHAT A DRUM MUST DO

| Corner | Requirement | Why it is hard |
|---|---|---|
| **LAW** | eigenvalue count matches **N(T)** exactly | not asymptotically-up-to-a-constant — exactly, including the constant |
| **GUARD** | spacing statistics match **GUE** | pair correlation *and* higher correlations; GUE not GOE |
| **MIRROR** | genuine **self-adjointness** | on a real Hilbert space with a stated domain — not a formal symmetry |

**Get all three from one construction, with nothing fitted to the zeros and no step that
assumes the conclusion.**

---

# 2 · THE TEST OUR CENSUS SUPPLIES

From 12c §6, and this is the part that is actually checkable **today** against any
proposed operator:

> **The closed orbits must have periods r·log p with weights 1/(r²pʳ). No free
> parameters.**

`[MEASURED]` We followed this comb twice in the census. Any candidate whose orbit
structure differs — different periods, different weights, or free parameters tuned to fit
— **is not it**, regardless of how well it does on the other corners.

**This is a cheap, decisive filter and it is underused.** Most proposals are assessed on
whether they produce roughly the right level counting. The comb is a stricter and more
specific requirement.

---

# 3 · THE ONE THING THAT ALREADY WORKS — and it is why the programme is serious

Before the failures, the success that keeps everyone at it.

**In a chaotic dynamical system**, the number of closed orbits with period up to T grows
like **e^(hT)/hT**, where h is the topological entropy. `[FACT]`

**In Riemann's world**, the "orbits" would have periods log p. The number of primes with
log p ≤ T is π(e^T), and by the prime number theorem:

> **π(e^T) ≈ e^T / T**

**That is exactly the orbit-counting law of a chaotic system with entropy h = 1.**
`[FACT — this is elementary once both sides are written down, and it is the observation
that makes the whole Hilbert–Pólya programme respectable rather than wishful.]`

**The primes have precisely the right abundance to be the periodic orbits of a chaotic
system.** Not approximately — the growth law matches on the nose.

**This is the strongest single piece of evidence for 12c's answer**, and it is worth being
clear about why: it is not a statistical resemblance like the GUE match. **It is a
structural count that comes out right for a reason nobody arranged.**

---

# 4 · THE CANDIDATES

## 4.1 Berry–Keating — the quantised **xp**

**The proposal:** the classical Hamiltonian **H = xp**, quantised, with a phase-space
cutoff.

| Corner | Verdict |
|---|---|
| **LAW** | **BOUGHT** — with the cutoff, the semiclassical level count reproduces the leading terms of N(T), including the log correction. This is the proposal's real achievement. |
| **GUARD** | **PARTIAL** — the required statistics need the orbit structure to be right; Berry and Keating identified that the periods must be log p, which is the correct requirement rather than a derivation of it |
| **MIRROR** | **PAID** — this is where it fails |

**What it pays, precisely:** **xp has a continuous spectrum, not a discrete one.** The
cutoff that makes the spectrum discrete is imposed by hand, and different cutoffs give
different answers. **There is no known self-adjoint realisation on a natural domain whose
spectrum is the zeros.**

**Against the comb test:** the periods are *required* to be log p by the construction —
they are an input, not an output. **The comb does not discriminate here because the
proposal assumes it.**

`[READING — my characterisation. The xp proposal and the regularisation problem are
well documented; the precise state of current variants I would want checked.]`

## 4.2 Connes — the adelic trace formula

**The proposal:** a trace formula on the space of adele classes, in which the explicit
formula appears as a trace.

| Corner | Verdict |
|---|---|
| **LAW** | **BOUGHT** — the explicit formula emerges as a trace, which is exactly the right shape |
| **MIRROR** | **BOUGHT in form** — the framework is spectral and self-adjointness is available |
| **GUARD** | **PAID** — and in an unusual way |

**What it pays:** in Connes's picture the zeros appear as an **absorption** spectrum —
**missing lines in a continuum**, not emission lines of a discrete operator. And crucially,
**RH becomes equivalent to a positivity statement (Weil positivity) that is not proved.**

> **The construction does not fail. It relocates.** You get a beautiful trace formula whose
> validity is equivalent to the thing you were trying to prove.

**This is Shape D of article 12b in action** — transfer, which never closes on its own.
**Recognising that is not a criticism of the work**; it is a statement of where the
difficulty went.

`[READING — the absorption-spectrum characterisation and the equivalence to positivity are
as I understand them; worth checking against the primary source.]`

## 4.3 de Branges — the real-rooted class

**The proposal:** Shape C. Place ξ inside a space of entire functions where reality of
roots is structural.

| Corner | Verdict |
|---|---|
| **MIRROR** | **BOUGHT by construction** — the whole framework is built on it |
| **LAW** | **PARTIAL** |
| **GUARD** | **PAID** |

**What it pays:** the required conditions on the space were shown to fail for the specific
case needed — **Conrey and Li (2000) exhibited an obstruction** to the version of the
argument that would apply to ζ. `[READING — I am confident a specific counterexample to a
required hypothesis was produced; the exact statement should be checked.]`

**The structural lesson is the important part**, and it is the same one 12b names for
Shape C: **real-rootedness is not automatically preserved in a limit.** You need uniform
control, and the space that gives you the property for the approximants does not
automatically give it at the boundary.

## 4.4 Bender–Brody–Müller (2017) — the PT-symmetric operator

**The proposal:** a non-Hermitian operator, PT-symmetric, whose eigenvalues would be the
imaginary parts of the zeros, with the claim that a similarity transformation makes it
Hermitian.

| Corner | Verdict |
|---|---|
| **LAW** | **CLAIMED** |
| **MIRROR** | **PAID — and this is the disputed point** |

**What it pays:** the self-adjointness rests on the similarity transformation being valid
on an appropriate domain, and **that was disputed immediately.** The operator is not
established as self-adjoint in the sense the argument requires.

**Why it belongs in this audit even so:** it is the cleanest recent illustration of the
pattern — **the corner that gets paid is almost always MIRROR**, and it gets paid in the
domain, which is the part easiest to state loosely.

`[READING — the proposal is real and dated 2017; the criticism was prompt and substantive.
The current status I would want verified.]`

## 4.5 Keating–Snaith and random matrix theory — not a drum at all

**Included because it is often mistaken for one.**

Random matrix theory has been **spectacularly successful predictively** — moments of
zeta, value distributions, families of L-functions. `[FACT]`

| Corner | Verdict |
|---|---|
| **GUARD** | **BOUGHT completely** — this is where the GUE match lives |
| **LAW** | not attempted |
| **MIRROR** | not attempted |

**It is a statistical model, not a mechanism**, and its authors say so. **Two things can
share statistics without being the same thing.** RMT tells you what the answer looks like.
It does not tell you what the object is.

**This distinction matters for 12c's answer**: the GUE agreement is evidence *for* the
quantum reading, and it is not itself an instance of it.

## 4.6 Quantum graphs and billiards — the direct attempt

**The proposal:** construct an actual chaotic system whose closed orbits have lengths
log p.

| Corner | Verdict |
|---|---|
| **LAW** | in principle achievable — §3 shows the counting works |
| **MIRROR** | available — real quantum systems are self-adjoint |
| **GUARD** | **PAID — and the obstruction is specific and instructive** |

**What it pays, and this is the most concrete obstruction in the whole audit:**

**GUE, not GOE, means the system must break time-reversal symmetry.** `[FACT — this is
standard: GOE statistics belong to time-reversal-invariant systems, GUE to those without
it.]`

**A system whose orbit lengths are log p and which breaks time-reversal symmetry, with the
right orbit multiplicities and the right Maslov phases, has not been constructed.**

**And the multiplicities are the sharp part.** In the explicit formula each prime appears
with its powers pʳ carrying weight 1/(r²pʳ) — **a very specific degeneracy structure.** In
a generic chaotic system, orbits of the same length are rare accidents. Here they are
forced by arithmetic. **The system would have to be arithmetically special, not generically
chaotic** — and that is exactly the tension: the statistics say *generic chaos*, the
periods say *arithmetic*.

> **This is the deepest form of the two-of-three problem: the guard wants genericity and
> the law wants arithmetic, and one system has to be both.**

---

# 5 · THE PATTERN ACROSS ALL OF THEM

| Candidate | Bought | Paid |
|---|---|---|
| Berry–Keating xp | law, part of guard | **mirror** (continuous spectrum; hand-imposed cutoff) |
| Connes | law, mirror-in-form | **guard** (absorption spectrum; relocates to unproved positivity) |
| de Branges | mirror | **guard** (obstruction to the required condition) |
| Bender–Brody–Müller | law (claimed) | **mirror** (domain; disputed) |
| Random matrices | guard | law, mirror **not attempted** |
| Quantum graphs | law, mirror | **guard** (needs broken time-reversal *and* arithmetic degeneracies) |

**Three things this table says that no single row says.**

**1 · MIRROR is paid most often, and always in the domain.** Not in the symmetry — a
symmetric operator is easy. **In the domain**, which is where self-adjointness actually
lives and which is the easiest thing to state loosely. `[READING]`

**2 · Nobody has bought GUARD from a mechanism.** RMT buys it by *being* a statistical
model. Every mechanism that tries to derive the statistics from structure ends up needing
a system that is simultaneously generically chaotic and arithmetically rigid.

**3 · The failures are not the same failure.** They fail at different corners for different
reasons — and that is worse news, not better. **A single common obstruction could be
attacked. Three different obstructions suggests the constraint is the conjunction itself:
holding all three at once may be the hard thing, not any one of them.**

`[READING — this is the audit's own conclusion and it is exactly the sort of claim that
should be attacked. It rests on six rows written from memory.]`

---

# 6 · WHAT OUR CENSUS CONTRIBUTES, AND WHAT IT DOES NOT

**Contributes:**

1. **The comb, measured.** `[MEASURED]` Periods r·log p, weights 1/(r²pʳ), followed twice.
   Any proposed operator can be checked against it today. **This is the audit's one
   usable instrument.**
2. **A bound on the statistical side.** `[MEASURED]` At 50,000 the small-gap behaviour
   agrees with the finite-height-corrected model within a stated bound — pooled z = −0.75.
   **A candidate predicting a deviation larger than that bound at these heights is already
   excluded.**
3. **63,519 failures to falsify.** No off-line zero. Every drum candidate must be
   consistent with that, and all of them are.

**Does not contribute:**

- **Nothing here builds an operator or narrows which of the six routes is right.**
- **Nothing here resolves the generic-versus-arithmetic tension of §4.6**, which is where
  the real difficulty sits.
- The census tests **consequences** of candidate drums. **It cannot test the drums
  themselves**, because they do not exist as objects yet.

---

# 7 · WHAT WOULD BREAK THE DEADLOCK

| Route | What would have to happen |
|---|---|
| **Fix the domain** | a self-adjoint realisation of an xp-type operator on a *natural* domain — no hand-tuned cutoff — whose spectrum is discrete with the right count |
| **Derive the statistics** | show the GUE behaviour *follows* from the arithmetic degeneracies rather than being imposed alongside them. **This is the one that would matter most**, because it is the corner nobody has bought from a mechanism |
| **Close the transfer** | prove Weil positivity directly. Connes's construction then stops relocating and starts closing |
| **Repair the limit** | for Shape C, a preservation theorem strong enough to carry real-rootedness across the boundary |
| **Build the system** | an explicit chaotic system, time-reversal-breaking, orbits of length log p with the arithmetic multiplicities. **If it exists, §3 says the counting will work** |

**§3 is the reason to keep going.** The orbit-counting law matches exactly, for no reason
anyone arranged. Something with that structure is unlikely to be a coincidence — and
"unlikely to be a coincidence" is not a proof, which is the honest position after every
row of §5.

---

# WHAT THIS ARTICLE CLAIMS

- **The two-of-three pattern is real and the paid corner varies.** `[READING]`
- **MIRROR is paid most often, and in the domain.** `[READING]`
- **The sharpest obstruction is generic-chaos versus arithmetic-rigidity** (§4.6).
  `[READING]`
- **The prime counting matches the chaotic orbit-counting law exactly** (§3). `[FACT]`
- **The comb is a usable discriminator today.** `[MEASURED]`

## WHAT IT DOES NOT CLAIM

- **No proof, and no assessment of which route will succeed.**
- **No claim that the audit is complete.** Six routes are covered; the literature is
  larger, and an approach I have not named could already have addressed §5's pattern.
- **No claim that any attribution here is exact.** Written from one witness with no
  literature search, capped at Medium by the project's own rule. **Every named result
  should be checked against its primary source before being cited.**
- **Nothing our census did contributes to building a drum**, and §6 says so in its own
  section rather than in a footnote.

**The sentence to keep:**

> The primes have exactly the right abundance to be the closed orbits of a chaotic system —
> that is a fact and it is why the hunt is serious — but the system would have to be
> generically chaotic in its statistics and arithmetically rigid in its periods at the same
> time, and every candidate so far has bought one of those and paid for it with the other.
