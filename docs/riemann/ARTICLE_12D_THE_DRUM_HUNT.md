# 12d · THE DRUM HUNT

### Deriving the specification of the system nobody has found — and auditing every candidate against it

**What this article does.** Article 12c concluded the quantum reading is primary. Article
12b wrote the test: *one mechanism holding law, guard and mirror at once.* This article
stops surveying opinions and **derives the wanted poster**: match the two trace formulas
term by term and read off exactly what the missing system must be.

**The result is a seven-line specification**, and every line is forced. Then each candidate
is audited against it, and one case is examined where the whole architecture demonstrably
works — and turns out to be the wrong symmetry class.

**Evidence standing, stated first.** The *derivation* in §2–§4 you can check yourself with
a pen — it is arithmetic on two standard formulas. **§5b and §6b are searched and sourced**
(references at the end). The remaining *attributions* in §7–§8 are written from my own
knowledge with no search behind them — **one witness, capped at Medium by the project's own
Filter 3** — and should be verified before being cited.

**One halt in the previous version has been resolved by search, and the resolution changed
the article's conclusion.** It is marked in place at §5b rather than folded in silently.

---

# 1 · THE TWO FORMULAS

Everything follows from putting these side by side. Both are standard.

## 1.1 Gutzwiller's trace formula — quantum chaos

For a chaotic Hamiltonian system, the density of quantum energy levels is a smooth part
plus a sum over the **primitive periodic orbits** of the classical flow, each repeated r
times:

> **d(E) = d̄(E) + (1/πℏ) Σ_γ Σ_{r=1}^∞ [ T_γ / (2 sinh(r λ_γ T_γ / 2)) ] · cos( r S_γ(E)/ℏ − r μ_γ π/2 )**

- **T_γ** — the period of the primitive orbit γ
- **λ_γ** — its Lyapunov (instability) exponent
- **S_γ(E)** — its action; note **dS/dE = T**
- **μ_γ** — its Maslov index, an integer fixing the phase
- **d̄(E)** — the smooth (Weyl) term

`[FACT — standard semiclassical result]`

## 1.2 The explicit formula — Riemann

Writing the non-trivial zeros as ρ = ½ + iE, the density of the E-values is a smooth part
plus a sum over **primes p** and their powers r:

> **d(E) = d̄(E) − (1/π) Σ_p Σ_{r=1}^∞ [ log p / p^{r/2} ] · cos( r E log p )**
>
> with **d̄(E) = (1/2π) · log(E/2π)**

`[FACT — the Riemann–von Mangoldt / Weil explicit formula, in density form]`

## 1.3 The shape is identical

| Gutzwiller | Riemann |
|---|---|
| sum over primitive orbits γ | sum over primes p |
| repetitions r | powers r |
| oscillation frequency involves T_γ | oscillation frequency is log p |
| amplitude set by T_γ and λ_γ | amplitude is log p · p^(−r/2) |
| smooth Weyl term d̄(E) | smooth term (1/2π)log(E/2π) |

**This is not an analogy. It is the same functional form**, which is why Hilbert–Pólya is
a research programme and not a hope. `[FACT]`

---

# 2 · THE MATCHING, DONE TERM BY TERM

Now force the two to agree and see what the classical system must be. Each step is
mechanical.

## 2.1 The phase ⟹ the periods are log p

Gutzwiller's oscillation is cos(r S_γ(E)/ℏ − …). Riemann's is cos(r E log p).

Since **dS/dE = T**, matching the E-dependence of the phase gives S_γ(E) = E·T_γ, so:

> ### **T_p = log p**
>
> **The primitive periods are the logarithms of the primes.**

## 2.2 The amplitude ⟹ every orbit is exactly as unstable as it is long

Gutzwiller's amplitude, for large r:

> T_γ / (2 sinh(r λ_γ T_γ / 2)) ≈ **T_γ · e^(−r λ_γ T_γ / 2)**

Riemann's amplitude:

> log p / p^(r/2) = log p · e^(−(r/2)·log p) = **T_p · e^(−r T_p / 2)**

Set them equal. The prefactors already agree (both T). Matching the exponents:

> **λ_p · T_p = T_p** ⟹ ### **λ_p = 1, for every single orbit.**

**Read that again, because it is the whole difficulty of this article.**

The Lyapunov exponent — how fast nearby trajectories diverge — must be **exactly 1 for
every periodic orbit, without exception.** Not on average. Not asymptotically. Every orbit,
the same instability.

Equivalently: **each orbit's instability exponent equals its own period**, λ_γ T_γ = T_γ.
**Every orbit is exactly as unstable as it is long.**

`[READING — the derivation is mine but elementary; Berry and Keating performed the
equivalent matching and reached the same requirement.]`

## 2.3 The sign ⟹ every Maslov index is the same

Riemann's prime sum carries a **minus sign, uniformly**. Gutzwiller carries
cos(… − r μ_γ π/2), which produces a sign depending on μ_γ mod 4.

For a uniform minus across all orbits and all repetitions:

> ### **μ_γ must be the same for every orbit**, and equal to the value giving −cos.

**In a generic chaotic system Maslov indices vary from orbit to orbit.** Here they must be
rigidly identical.

## 2.4 The counting ⟹ topological entropy is 1

Primitive orbits with period ≤ T are primes with log p ≤ T, i.e. **p ≤ e^T**. By the prime
number theorem:

> **π(e^T) ~ e^T / T**

A chaotic system with topological entropy h has orbit counting **e^(hT)/(hT)**. Therefore:

> ### **h = 1**

## 2.5 The consistency check that should have failed and does not

For a system with **uniform** instability λ across all orbits, the topological entropy
equals that exponent: **h = λ.**

- §2.2 gave **λ = 1** — from the *amplitudes*.
- §2.4 gave **h = 1** — from the *counting*.

**These are independent derivations from independent parts of the formula, and they
agree.**

> **This is the strongest single piece of evidence in the entire drum programme, and it is
> almost never stated this way.**

The amplitude of the prime terms (p^(−r/2), the **½** in the exponent — *your ½*) and the
density of the primes (the prime number theorem) are logically unrelated facts about
arithmetic. Matched against a dynamical system, **they produce the same number.**

Nobody arranged that. If the correspondence were empty, there is no reason those two
should agree.

**And note where the ½ enters:** it is the exponent p^(−r/2) that gives λ = 1. **Move the
zeros off the half-line and the amplitude exponent changes, so λ ≠ h, and the system
becomes dynamically inconsistent.** `[READING]` **On this reading the half-line is not
where the zeros happen to be — it is the only place where a consistent classical system
could exist at all.** That is what "the ½ is forced rather than observed" means, made
concrete.

---

# 3 · THE WANTED POSTER

Everything above, collected. **This is the specification of the system that would prove
the Riemann Hypothesis by Shape A.**

> **WANTED: a classical dynamical system with all of the following.**
>
> 1. **Chaotic**, with isolated unstable periodic orbits.
> 2. **Primitive periods exactly T_p = log p**, one orbit per prime, no others.
> 3. **Every orbit's Lyapunov exponent λ = 1** — uniform instability, no exceptions.
> 4. **Topological entropy h = 1** (automatic given 3, and independently required by the
>    prime counting).
> 5. **No time-reversal symmetry** — the quantum statistics must be GUE, not GOE.
> 6. **All Maslov indices identical**, to give the uniform minus sign.
> 7. **Smooth term (1/2π)·log(E/2π)** — fixing the phase-space volume growth.
>
> **And its quantisation must be self-adjoint on a natural domain.**

**Seven conditions. Every one forced by the matching. None is adjustable.**

**Nobody has built it.** And the difficulty is not that seven conditions is a lot — it is
that several of them pull against each other, which §4 and §5 make precise.

---

# 4 · WHY CONDITION 3 IS THE HARD ONE

**Uniform instability is not a mild constraint. It is close to a contradiction with
condition 1.**

In a generic chaotic system, the Lyapunov exponents of individual periodic orbits are
**spread over a wide range** — this spread is what the multifractal / thermodynamic
formalism of chaos is *about*. A system in which **every** periodic orbit has identical
instability is extraordinarily rigid.

**Where does uniform instability actually occur?** In systems of **constant negative
curvature** — geodesic flow on a hyperbolic surface. There, every closed geodesic has the
same instability exponent, set by the curvature. `[FACT]`

> **So condition 3 points at hyperbolic geometry, and it points there hard.**

That is a real narrowing of the search — and it takes us straight to the one place where
this entire architecture is known to work.

---

# 5 · THE PLACE IT ALREADY WORKS — Selberg

**The Selberg trace formula** is not an analogy for Riemann's situation. It is the same
structure, **completed**. `[FACT]`

For a compact hyperbolic surface:

| Riemann's wanted poster | Selberg's actual system |
|---|---|
| a self-adjoint operator | **the Laplacian.** Genuinely self-adjoint, no regularisation |
| a discrete real spectrum | **its eigenvalues.** Real by construction |
| orbits with periods T | **closed geodesics with lengths ℓ** |
| uniform instability λ = 1 | **true** — constant curvature gives every geodesic the same exponent |
| a zeta function | **the Selberg zeta function** |
| zeros on a line | **its zeros lie on a line — and this is a THEOREM, not a conjecture** |

> ### The Riemann Hypothesis, for the Selberg zeta function, is proved.
>
> **And it is proved exactly the way Shape A says it must be: because the spectrum belongs
> to a self-adjoint operator.**

**This is the existence proof that the architecture is sound.** The programme is not
chasing a shape that has never worked. It is chasing a shape that works, in a case where
the operator is known, and trying to find the arithmetic instance.

## So what is different?

**The lengths.** Selberg's closed geodesics have lengths determined by the surface's
geometry. Riemann needs lengths **log p**.

**And the symmetry class.** Geodesic flow on a surface is **time-reversal symmetric** —
run any geodesic backwards and you get another geodesic. So its quantum statistics should
be **GOE**.

**Riemann's zeros are GUE.** `[FACT — Montgomery–Dyson, confirmed numerically to enormous
heights by Odlyzko]`

> **Selberg has the right architecture and the wrong symmetry class. Condition 5 is
> exactly what separates the solved case from the unsolved one.**

**That is the sharpest statement this article can make**, and it says where to look: a
hyperbolic-like system with uniform instability — *but with time-reversal broken.*
Magnetic fields break time reversal, and a hyperbolic surface carrying a magnetic field is
not an exotic object.

---

## 5b · THE HALT, RESOLVED — it has been done, and it works

**The previous version of this article stopped here with an honest halt: I did not know
whether anyone had tried it.** A literature search was run. **They have, it works, and the
result is recent.** `[FACT — searched, sources at the end]`

### The baseline: plain hyperbolic surfaces give GOE

**Rudnick** proved that the spectral number variance for the Laplacian of a large compact
hyperbolic surface converges — in a scaling limit, averaged over **moduli space** with the
Weil–Petersson measure — to the number variance of the **Gaussian Orthogonal Ensemble.**
The proof uses **Mirzakhani's integration formula.** Related work establishes GOE
statistics on the moduli space of surfaces of large genus, and almost-sure GOE
fluctuations at high genus.

**So condition 5 fails for untwisted surfaces, provably — exactly as §5 predicted from
time-reversal symmetry.**

### The extension: add the magnetic field and you get GUE

> ### Marklof & Monk, 2024 — *The moduli space of twisted Laplacians and random matrix theory*
> **arXiv:2407.10778**, published in *International Mathematics Research Notices*
> (doi:10.1093/imrn/rnae239).

A **twisted Laplacian** incorporates a magnetic field (an Aharonov–Bohm flux) and
**breaks time-reversal symmetry.** They extend Rudnick's method and prove:

> **the spectral number variance converges to the GAUSSIAN UNITARY ENSEMBLE.**

**And the family is complete:** the same approach gives **GSE** for Dirac operators. All
three classical symmetry classes are realised on hyperbolic surfaces, and the physical
knob that moves between them is exactly the one §5 identified.

**Condition 5 is therefore not a barrier. It is solved, in the setting where conditions
1, 3, 4 and self-adjointness already hold.** The twisted Laplacian is a genuinely
self-adjoint operator on a genuinely uniformly-hyperbolic system, with GUE statistics.

### And the machinery for the zeta function exists too

**Twisted Selberg zeta functions are defined and studied.** The Selberg and Ruelle zeta
functions are Euler products **over prime closed geodesics indexed by their lengths**;
twisting by a representation of the fundamental group gives the twisted versions, and
their relation to determinants of twisted Laplacians is active current work (Spilioti and
others). **The object that would play the role of ζ in this setting is built.**

### So why is the Riemann Hypothesis not proved?

**Two reasons, and they are both specific.**

**1 · The Marklof–Monk result makes no reference to the Riemann hypothesis or the Riemann
zeros.** `[FACT — checked directly against the paper.]` It is a theorem in spectral
geometry. **Nobody has joined it to Riemann**, and this article is not claiming the join
is available — only that half of the wanted poster now has a proof attached to it.

**2 · And this is the decisive one: the result is an AVERAGE OVER MODULI SPACE, in the
large-genus limit.** It says that a **typical, random, large-genus** twisted surface shows
GUE. It does **not** produce a single specific surface with GUE, and it says nothing about
any particular one.

> **Riemann needs one specific system whose geodesic lengths are exactly log p.** That is
> the least typical surface imaginable — it is arithmetically determined, not random.
>
> **The theorem delivers GUE for the generic case. Condition 2′ demands the arithmetic
> case. The theorem does not apply to it.**

**The halt is resolved and the gap has moved to a sharper place**, which is the best
outcome a halt can have.

---

# 6 · THE OTHER TENSION — arithmetic pushes AWAY from GUE

And here is the finding that makes this harder than §5 suggests, from a case that is
actually studied.

**Arithmetic hyperbolic surfaces** — the ones built from number theory, the modular
surface and its relatives — have a special property: their length spectra are **massively
degenerate.** Enormous numbers of distinct closed geodesics share exactly the same length,
because the lengths come from arithmetic (traces of matrices in an arithmetic group)
rather than from generic geometry. `[FACT]`

**The consequence is measured and famous: arithmetic surfaces show POISSON level
statistics, not GOE and not GUE.** The degeneracies pile up the trace formula's
contributions and destroy the random-matrix behaviour. `[FACT — "arithmetic quantum
chaos"; this is the standard result and it surprised people when found.]`

> ### So arithmetic degeneracy *destroys* random-matrix statistics in the one family where
> we can check.

**And Riemann's zeros need GUE — the most rigid random-matrix class.**

**This is the generic-versus-arithmetic tension in its sharp form**, and it is much worse
than "one system must be both":

- **Condition 2** (periods = log p) demands the length spectrum be **arithmetic**.
- **Condition 5** (GUE) demands the statistics be **random-matrix**.
- **The one studied family that has arithmetic lengths gives Poisson** — neither GOE nor
  GUE.

**How does Riemann's system have arithmetic periods and still produce GUE?**

The available answer is that Riemann's "length spectrum" {log p} is **degeneracy-free** —
each prime appears exactly once, and the logs of distinct primes are rationally
independent, so no two primitive orbits share a period. That is the opposite of the
arithmetic-surface situation, where degeneracy is the whole problem. `[READING]`

**If that is the resolution, then condition 2 needs a sharper form:**

> **2′. Periods exactly log p, one orbit each, and NO length degeneracy whatsoever.**

**A length spectrum that is simultaneously arithmetic in origin and degeneracy-free in
structure.** The known arithmetic systems fail the second half. Generic chaotic systems
satisfy the second half and cannot deliver the first.

**That, precisely, is why the drum has not been found.** Not seven hard conditions — **one
condition (2′) that the two natural families of candidate systems fail from opposite
directions.**

## 6b · AND THE LITERATURE PUTS BOTH SIDES OF THAT TENSION ON THE RECORD

With §5b's result in hand, the tension is no longer a suspicion. **Both halves are now
theorems, in incompatible settings.**

| | Setting | Statistics | Length spectrum |
|---|---|---|---|
| **Marklof–Monk 2024** | **generic** twisted surfaces, averaged over moduli space, large genus | **GUE — proved** | generic, no arithmetic structure |
| **Arithmetic quantum chaos** | **specific** arithmetic surfaces (modular surface and relatives) | **Poisson — not GOE, not GUE** | arithmetic, **massively degenerate** |
| **What Riemann needs** | **one specific system** | **GUE** | **arithmetic AND degeneracy-free** |

> **The two established results sit on opposite sides of the gap, and Riemann's case falls
> exactly between them.**
>
> Genericity buys the statistics and forbids the arithmetic. Arithmetic buys the periods
> and destroys the statistics — because arithmetic produces *degeneracy*, and degeneracy
> is what kills random-matrix behaviour.

**So condition 2′ is not merely unsatisfied. It asks for the one combination that the two
known mechanisms each rule out.** `[READING — the two results are facts; the claim that
Riemann falls between them is my reading, and it is the load-bearing claim of this
article.]`

**And it says exactly what a breakthrough would look like:** a mechanism by which an
arithmetic length spectrum can be **degeneracy-free** — so that it inherits generic
statistics without inheriting generic lengths. **The primes are degeneracy-free** (distinct
primes have rationally independent logs, by unique factorisation). **The arithmetic
surfaces are not.** Whatever makes the primes different from the trace-degeneracies of an
arithmetic group is where the answer lives.

---

# 7 · THE CANDIDATES, AGAINST THE POSTER

Each is now scored against seven explicit conditions rather than three vague corners.

## 7.1 Berry–Keating — quantised **xp**

**What it gets right:** the classical Hamiltonian H = xp has hyperbolic flow with
**uniform instability** — condition 3, for free. Its semiclassical level count, with a
phase-space cutoff, reproduces the smooth term including its logarithmic form — condition
7. The proposal is serious precisely because it satisfies the two conditions everything
else struggles with.

| Condition | |
|---|---|
| 1 chaotic, isolated orbits | **partial** — the flow is hyperbolic but the orbits are not isolated without a cutoff |
| 2′ periods log p, no degeneracy | **IMPOSED, not derived** — the periods are put in by hand |
| 3 uniform λ = 1 | **YES — this is xp's gift** |
| 4 h = 1 | follows |
| 5 no time reversal | **YES** — xp is not time-reversal symmetric |
| 6 uniform Maslov | unresolved |
| 7 smooth term | **YES**, with the cutoff |
| **self-adjoint on a natural domain** | **NO — this is what it pays** |

**What it pays, precisely:** **xp has a purely continuous spectrum.** There are no
eigenvalues to be the zeros. The phase-space cutoff |x|,|p| > ℓ that discretises it is
imposed by hand, and **different cutoffs give different spectra.** The counting comes out
right because the cutoff was chosen to make it come out right.

> **Berry–Keating is not a failed operator. It is a correct identification of the classical
> system with no quantisation.** Conditions 3, 5 and 7 are genuinely satisfied. **Condition
> 2′ and self-adjointness are the entire gap** — and 2′ is the one §6 says is hard.

## 7.2 Connes — the adelic trace formula

**What it gets right:** the explicit formula emerges as an actual trace, in a framework
that is spectral from the start.

**What it pays:** the zeros appear as an **absorption spectrum** — missing lines in a
continuum — not as the eigenvalues of an operator with discrete spectrum. And **RH becomes
equivalent to Weil positivity**, which is unproved.

**Weil's criterion**, stated so the relocation is visible: RH holds if and only if a
certain explicit quadratic functional W(f) — built from the explicit formula, summing
contributions from all primes and the archimedean place — satisfies **W(f) ≥ 0 for all
admissible test functions f.** `[FACT]`

> **The construction does not fail. It converts the problem into a positivity statement of
> exactly equal difficulty.**

That is **Shape D** from article 12b — transfer — and it never closes alone. **Saying so
is not a criticism of the work.** It is a statement of where the difficulty moved, and
Connes made the difficulty far more precise than it was.

## 7.3 de Branges — Shape C

**Not a drum at all.** This is the *nature of ξ* route: put ξ into a space of entire
functions where reality of roots is structural.

**What it pays:** the conditions required of the space were shown to fail in the case
needed — **Conrey and Li (2000)** exhibited an obstruction to the version applying to ζ.
`[READING — I am confident a specific counterexample to a required hypothesis exists;
verify the exact statement.]`

**The structural lesson is the one 12b names:** real-rootedness is not automatically
preserved under limits. You need **uniform** control across the approximating family, and
that is what is missing.

## 7.4 Bender–Brody–Müller (2017)

A PT-symmetric non-Hermitian operator, with the claim that a similarity transformation
renders it Hermitian.

**What it pays:** the transformation's validity on the required domain was **disputed
immediately**. Self-adjointness was not established in the sense the argument needs.

**Why it earns its place in the audit:** it is the cleanest recent demonstration that **the
corner paid is almost always self-adjointness, and it is paid in the domain** — the part
easiest to state loosely and hardest to establish.

## 7.5 Random matrix theory

**Not a drum, and its authors say so.** A statistical model, spectacularly successful
predictively — moments of ζ, families of L-functions, value distributions.

It supplies **condition 5's evidence** and attempts nothing else. **The GUE agreement is
evidence *for* the quantum reading; it is not an instance of it.**

## 7.6 Quantum graphs — and a concrete impossibility

The most direct attempt: build a real quantum system with orbit lengths log p.

**Here the obstruction is sharp and arithmetic.** On a quantum graph with finitely many
bonds of lengths ℓ₁ … ℓ_n, every periodic orbit's length is a **non-negative integer
combination** of the bond lengths — the additive semigroup they generate.

To realise **{log p : p prime}**, every log p must lie in that semigroup. But the numbers
log p are **rationally independent** — no log p is a rational combination of the others,
because primes are multiplicatively independent and factorisation is unique.

> **Therefore every log p must be its own generator. A finite graph cannot do it. The
> graph must have infinitely many bonds** — and finite quantum graphs are precisely the
> ones that are understood.

`[READING — the rational independence of {log p} is elementary from unique factorisation;
the semigroup argument is mine and should be checked, but I believe it is right.]`

**This is not "hard." It is a proof that the finite version cannot work**, and it explains
why the quantum-graph route has not produced a candidate rather than merely producing a
flawed one.

---

# 8 · THE PATTERN, RESTATED WITH THE POSTER IN HAND

| Candidate | Conditions satisfied | What it pays |
|---|---|---|
| Berry–Keating xp | **3, 5, 7** — the rigid ones | 2′ imposed by hand; **no self-adjoint quantisation** |
| Connes | trace structure, spectral framing | **relocates** to unproved positivity |
| de Branges | self-adjointness by construction | the limit is not controlled |
| Bender–Brody–Müller | claimed spectrum | **domain** |
| Random matrices | evidence for 5 | attempts nothing else |
| Quantum graphs | 1, 3, self-adjointness | **2′ is impossible finitely** |
| **Selberg — the working case** | **1, 2, 3, 4, 6, 7, self-adjoint. PROVED.** | **5 — wrong symmetry class** |

**Three conclusions the table supports that no single row does.**

**1 · The architecture is not in doubt.** Selberg satisfies almost the entire poster and
the theorem is proved. **Shape A is a real mechanism, demonstrated.**

**2 · The failures are not one failure, and that is the bad news.** xp pays quantisation.
Connes pays by transferring. Graphs pay an arithmetic impossibility. Selberg pays symmetry.
**Four different walls.** A single shared obstruction could be attacked; four suggests
**the conjunction is the object**, not any member of it.

**3 · Condition 2′ is the keystone.** Every route either assumes it, cannot reach it, or
reaches something like it with the wrong symmetry. **An arithmetic, degeneracy-free length
spectrum with broken time reversal is the thing that does not exist yet** — and §6 shows
the two natural families fail it from opposite sides.

---

# 9 · WHAT OUR CENSUS CAN AND CANNOT TEST

**Can:**

1. **Condition 2 directly.** `[MEASURED]` We followed the return comb twice — periods
   r·log p, weights 1/(r²pʳ). **Any proposed system can be checked against it today**, and
   the check is cheap: extract its orbit lengths and stabilities and compare. **A candidate
   with free parameters tuned to fit already fails**, because the poster has none.
2. **Condition 5's consequences.** `[MEASURED]` At reach 50,000 the small-gap behaviour
   agrees with the finite-height-corrected GUE model within a stated bound (pooled
   z = −0.75). **A candidate predicting deviation beyond that bound at these heights is
   already excluded.**
3. **Condition 3, indirectly and this is the interesting one.** Uniform instability λ = 1
   is what produces the p^(−r/2) amplitudes. **Our measurement of the small-gap statistics
   is sensitive to those amplitudes** — so the agreement in (2) is weak evidence that
   uniform instability holds. **Weak, and worth naming**, because nobody thinks of the
   census as measuring a Lyapunov exponent, and in this frame it partly does. `[READING]`

**Cannot:**

- **Nothing here builds a system, and nothing narrows which route is right.**
- **Nothing resolves §6.** The arithmetic-versus-random-matrix tension is where the
  difficulty lives, and no amount of census touches it.
- The census tests **consequences of hypothetical drums**. It cannot test the drums, which
  do not exist as objects.

---

# 10 · WHAT WOULD BREAK THE DEADLOCK

| Route | What must happen | Assessment |
|---|---|---|
| **Break Selberg's symmetry** | ~~time reversal broken~~ — **DONE (Marklof–Monk 2024).** What remains: make it a *specific* surface with an arithmetic, degeneracy-free length spectrum, not a moduli-space average | **the gap has moved**: symmetry solved, specificity open |
| **Quantise xp honestly** | a self-adjoint realisation on a natural domain, **no hand-tuned cutoff**, discrete spectrum with the right count | conditions 3, 5, 7 already hold; only this is missing |
| **Derive GUE from arithmetic** | show random-matrix statistics *follow* from a degeneracy-free arithmetic length spectrum | **the corner nobody has bought from a mechanism**; §6 says why it is hard |
| **Close the transfer** | prove Weil positivity directly | Connes's construction then stops relocating |
| **Control the limit** | Shape C's preservation theorem | different route entirely |

**Ranked by how close the target is, the first two are where I would look**, and the third
is the one that would explain rather than construct.

---

# WHAT THIS ARTICLE CLAIMS

- **The wanted poster is derived, not surveyed.** Seven conditions, each forced by matching
  two standard formulas. `[READING on the derivation; FACT on the formulas]`
- **λ = 1 from the amplitudes and h = 1 from the prime counting agree** — two independent
  derivations from unrelated arithmetic facts. `[READING — the check is elementary and
  you can do it yourself]`
- **The ½ is where that consistency comes from**, which makes the half-line the only place
  a coherent classical system could exist. `[READING]`
- **Selberg proves the architecture works and differs in exactly condition 5.** `[FACT on
  Selberg; READING on the isolation of condition 5]`
- **Arithmetic degeneracy destroys random-matrix statistics where it has been checked**, so
  condition 2 must sharpen to 2′. `[FACT on arithmetic quantum chaos; READING on 2′]`
- **A finite quantum graph provably cannot realise {log p}.** `[READING — the argument is
  short; check it]`

## WHAT IT DOES NOT CLAIM

- **No proof, and no prediction of which route succeeds.**
- **No claim the audit is complete.** Six routes plus Selberg; the literature is larger.
- **No claim any attribution is exact.** One witness, no literature search, Medium cap.
  **Check every named result before citing it.**
- **No claim our census contributes to building a drum.** §9 says so in its own section.
- **§5's magnetic-field halt is now RESOLVED** — it has been done and it works. What this
  article does **not** claim is that anyone has joined it to Riemann: **Marklof–Monk make
  no reference to the Riemann hypothesis**, and their result is a moduli-space average, not
  a statement about any particular surface.

**The sentence to keep:**

> Selberg proved this architecture works and Marklof–Monk proved that adding a magnetic
> field to it delivers the GUE statistics Riemann needs — but their theorem is an average
> over *generic* surfaces, while Riemann's periods demand a *specific arithmetic* one, and
> the arithmetic surfaces we can actually study give Poisson statistics because arithmetic
> breeds degeneracy; so the missing object must have a length spectrum that is arithmetic
> in origin and degeneracy-free in structure, and the primes are exactly that while no
> known geometry is.

---

# SOURCES

- Marklof, J. & Monk, L., *The moduli space of twisted Laplacians and random matrix
  theory* — [arXiv:2407.10778](https://arxiv.org/abs/2407.10778) ·
  [IMRN, doi:10.1093/imrn/rnae239](https://doi.org/10.1093/imrn/rnae239)
- *GOE statistics on the moduli space of surfaces of large genus* —
  [arXiv:2202.06379](https://arxiv.org/pdf/2202.06379)
- *Almost sure GOE fluctuations of energy levels for hyperbolic surfaces of high genus* —
  [arXiv:2301.05964](https://arxiv.org/pdf/2301.05964)
- Spilioti, P., *Determinants of twisted Laplacians and the twisted Selberg zeta function*
  — [arXiv:2512.16681](https://arxiv.org/html/2512.16681)
- *Twisted Ruelle zeta function at zero for compact hyperbolic surfaces* —
  [arXiv:2105.13321](https://arxiv.org/pdf/2105.13321)
- Sierra, G., *A physics pathway to the Riemann hypothesis* —
  [arXiv:1012.4264](https://arxiv.org/pdf/1012.4264)
