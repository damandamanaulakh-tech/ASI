# 12d · THE DRUM HUNT

### Deriving the specification of the system nobody has found — and auditing every candidate against it

**What this article does.** Article 12c concluded the quantum reading is primary. Article
12b wrote the test: *one mechanism holding law, guard and mirror at once.* This article
stops surveying opinions and **derives the wanted poster**: match the two trace formulas
term by term and read off exactly what the missing system must be.

**The result is a seven-line specification**, and every line is forced. Then each candidate
is audited against it, and one case is examined where the whole architecture demonstrably
works — and turns out to be the wrong symmetry class.

**Evidence standing.** The *derivation* in §2 you can check yourself with a pen — it is
arithmetic on two standard formulas. **Everything else is now searched and sourced**
(full reference list at the end). The previous version carried a Medium cap on §7–§8
because it was written from memory with no search; **that cap is lifted, and two things
it got wrong are corrected in place** rather than folded in silently:

- **§5b — a halt resolved.** The magnetic-field question was open. It has been answered,
  and the answer changed the article's conclusion.
- **§7.4 — an overstatement corrected.** Bender–Brody–Müller was described as effectively
  refuted. It is **contested**, with both sides published and neither withdrawn.

**And the search produced two findings that were not in the previous version at all** —
§8.1 (the smooth/oscillating split) and §8.2 (the negative sign, three times). They are
the reason this rewrite exists.

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

**This section is now searched and sourced**, not written from memory. Each candidate is
scored against seven explicit conditions rather than three vague corners, and the reasons
for failure are the published ones.

## 7.1 The **xp** family — Berry–Keating, and what it actually buys

### The original construction

**Berry and Keating (1999)** showed that a *regularised* classical **H = xp**
reproduces, semiclassically, the **smooth counting function** of the Riemann zeros.

**The regularisation is specific and worth stating**, because its shape is the whole
story. They introduce a minimal length **ℓ_x** and a minimal momentum **ℓ_p** with

> **ℓ_x · ℓ_p = 2πℏ**

and impose **|x| ≥ ℓ_x** and **|p| ≥ ℓ_p**. This cuts a hyperbolic region out of phase
space, bounds the trajectories, and makes the phase-space area finite — from which the
**E log E** form of the counting function drops out.

`[FACT — sourced]`

### The failure is at the CLASSICAL level, before quantisation

This is the correction the previous version of this article did not have, and it matters
more than the domain question.

> **The classical trajectories of regularised xp are not closed.**

A trajectory of xp is a hyperbola; the cutoff bounds it but does not close it. **A
trace formula sums over CLOSED orbits.** If there are none, there is no oscillating
term at all — no periods, no log p, nothing arithmetic.

**So the model is incomplete at step one of the wanted poster**, not at the last step.
`[FACT — sourced]`

### The repair, and exactly what it does and does not buy

**Sierra and Rodríguez-Laguna (Phys. Rev. Lett. 106, 200201, 2011)** modified the
Hamiltonian to

> **H = x( p + ℓ_p² / p )**

which **does contain closed periodic orbits**, and whose spectrum **coincides with the
average Riemann zeros**. The construction extends to Dirichlet L-functions using
**different self-adjoint extensions** of H. `[FACT — sourced]`

**Read the phrase "average Riemann zeros" carefully. It is the crux.**

### THE SMOOTH/OSCILLATING SPLIT — the finding this section exists for

Go back to §1.2. The explicit formula has two parts:

> **d(E) = d̄(E) − (1/π) Σ_p Σ_r [ log p / p^(r/2) ] cos( r E log p )**
> &nbsp;&nbsp;&nbsp;&nbsp;↑ smooth &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ↑ **the oscillating part — where every prime lives**

**Every xp model, from Berry–Keating 1999 through Sierra 2011, reproduces d̄(E).**
Berry–Keating get the smooth counting function. Sierra gets the **average** zeros.

> ### The xp family has bought the half of the formula that contains no arithmetic.
>
> **d̄(E) = (1/2π)log(E/2π) knows nothing about primes.** It is a phase-space volume. You
> can reproduce it with a suitably shaped billiard and never touch number theory.
>
> **The oscillating term is the entire arithmetic content** — it is where log p appears,
> where λ = 1 is forced (§2.2), where the ½ enters as p^(−r/2). **No xp model has produced
> it.**

`[READING — the split is mine; the two facts it rests on are sourced]`

**This reframes twenty-five years of the programme.** The xp models are not "nearly
there with a domain problem." They have reproduced the smooth background and have never
touched the signal.

### Scored

| Condition | |
|---|---|
| 1 chaotic, isolated **closed** orbits | **NO** in Berry–Keating; **YES** in Sierra's repair |
| 2′ periods log p, degeneracy-free | **NOT ACHIEVED — the oscillating term is absent** |
| 3 uniform λ = 1 | **YES** — xp's genuine gift; hyperbolic flow, uniform instability |
| 4 h = 1 | follows |
| 5 no time reversal | **YES** — xp is not time-reversal symmetric |
| 6 uniform Maslov | not reached |
| **7 smooth term** | **YES — and this is what the family has actually delivered** |
| self-adjoint on a natural domain | multiple self-adjoint extensions exist; **which one is not determined by the physics** |

## 7.2 Connes — and the negative sign that reappears

### What it is

The explicit formulas of number theory are interpreted as a **trace formula on the
noncommutative space of adele classes**, reducing the Riemann Hypothesis to the validity
of that trace formula. `[FACT — sourced]`

### The absorption spectrum, and WHY

Here is the detail that ties this section to §2.3, and I did not have it before:

> **"A crucial negative sign in the analysis of the statistical fluctuations of the zeros
> of zeta indicates that the spectral interpretation should be as an ABSORPTION spectrum,
> or equivalently should be of a COHOMOLOGICAL nature."**

`[FACT — sourced; Connes's own reasoning]`

**The zeros are not emission lines of an operator. They are missing lines in a
continuum.** And the thing that forces that reading is **the sign** — the same minus sign
that §2.3 showed requires every Maslov index to be identical.

### Weil positivity

**Weil positivity — the positivity of the associated quadratic form on a suitable class
of test functions — is equivalent to the Riemann Hypothesis**, and proving positivity of
the Weil distribution gives RH **for all L-functions with Grössencharakter.**
`[FACT — sourced]`

**Work continues on it as a live programme:** Connes and Consani have attacked the
**archimedean place** specifically (2020), and more recent work reduces the Weil form to
concrete finite objects — an explicit **(2N+1)×(2N+1) Galerkin matrix** whose spectrum is
a finite-rank window on Weil positivity. `[FACT — sourced]`

### Scored

**The construction does not fail. It converts the problem into a positivity statement of
equal difficulty** — Shape D of article 12b, transfer, which never closes alone.

**But the conversion is not worthless and it should not be dismissed as merely
relocating.** It moved the difficulty from *"find an operator"* — an unbounded search —
to *"prove one inequality"* — a bounded, attackable, finitely-approximable statement.
**That is a real narrowing**, and the Galerkin work is what a narrowing looks like when
someone starts computing with it.

## 7.3 de Branges — and the counterexample

### What it is

**De Branges showed that the Riemann Hypothesis would follow from a positivity condition
on a certain Hilbert space of entire functions**, proposing the approach for the
generalized Riemann Hypothesis in 1986. This is Shape C — *the nature of ξ.*
`[FACT — sourced]`

### What killed that version

**Conrey and Li** (*IMRN* 2000, No. 18; arXiv:math/9812166) gave **explicit examples
showing that de Branges's positivity conditions are NOT SATISFIED** by the defining
functions of the reproducing-kernel Hilbert spaces associated with the Riemann zeta
function. `[FACT — sourced]`

**That is a counterexample to the hypotheses of the argument**, not a gap in it — a
different and more final kind of failure.

### And the connection nobody mentions in the same breath

**De Branges's theory is related to Lax–Phillips scattering theory** — and **Lax and
Phillips themselves explained the difficulty of approaching RH by scattering.**
`[FACT — sourced]`

> **So Shape C's failure has been diagnosed twice, independently, by different
> communities:** once as a positivity condition that the actual zeta function violates,
> and once as a structural obstruction in the scattering framework the theory generalises.

**And it is not dead:** work on de Branges's conjecture continues (e.g. 2025). The
*specific route* was closed; the *space* remains a live object.

## 7.4 Bender–Brody–Müller — a dispute, not a refutation

**I got this one wrong by overstating it in the previous version.** The accurate account:

- **Bender, Brody & Müller (2017)** proposed a Hamiltonian whose eigenvalues would be the
  imaginary parts of the zeros.
- **Bellissard** submitted a Comment (arXiv:1704.02644, **9 April 2017**) arguing the
  proposed strategy **does not work**.
- A separate note also appeared (arXiv:1704.04705).
- **Bender, Brody & Müller replied** (arXiv:1705.06767, **18 May 2017**), stating the
  issues raised had already been discussed in the paper and **do not affect its
  conclusions.**

`[FACT — sourced; all three documents exist and are dated]`

> **The correct status is CONTESTED, not refuted.** Both sides published, neither
> withdrew, and I have not found a resolution in the literature I can reach. **The
> previous version of this article said "disputed immediately" and implied it was settled
> against them. That was one witness overreaching, and it is corrected here.**

## 7.5 Random matrix theory — a model, and its authors say so

Supplies condition 5's evidence and attempts nothing else. **Montgomery's pair
correlation** matched the GUE; **Odlyzko's computations** confirmed it at great height.

**It tells you what the answer looks like. It does not tell you what the object is.** The
GUE agreement is evidence **for** the quantum reading, not an instance of it.

## 7.6 Quantum graphs — a clean impossibility

On a quantum graph with finitely many bonds of lengths ℓ₁…ℓ_n, **every periodic orbit's
length lies in the additive semigroup generated by those bond lengths.**

To realise **{log p : p prime}**, every log p must lie in that semigroup. But **the
numbers log p are rationally independent** — a consequence of unique factorisation.
Therefore **each log p must be its own generator**, and a finite graph cannot supply
infinitely many.

> **This is a proof that the finite version cannot work**, not a difficulty with it.

`[READING — the argument is short and elementary; I believe it is correct and it should
be checked]`

---

# 8 · THREE SYNTHESES

These are what the audit produces that no individual row contains.

## 8.1 The whole programme has bought the smooth term and never the fluctuations

From §7.1. **Berry–Keating 1999: the smooth counting function. Sierra 2011: the average
zeros.** Both are **d̄(E)**.

**d̄(E) = (1/2π)log(E/2π) contains no arithmetic.** It is a statement about phase-space
volume. The primes appear **only** in the oscillating sum — and **no candidate has
produced the oscillating sum from a mechanism.**

> **Every route either assumes the periods log p as an input, or does not reach them at
> all.**

- xp: assumes them (Berry–Keating build the required orbit periods in by hand) or misses
  them (the smooth term contains none).
- Connes: gets the whole explicit formula as a trace — **and then needs positivity**, so
  the arithmetic arrives correctly and the proof does not close.
- Quantum graphs: **provably cannot** reach them finitely.
- Selberg: reaches its *own* length spectrum, which is not the primes.

**The arithmetic content has never been derived. It has been imported, avoided, or proved
unreachable.**

## 8.2 The negative sign is the same obstruction, seen three times

| Where | What the sign does |
|---|---|
| **§2.3, the matching** | forces **every Maslov index to be identical** — a rigidity generic systems do not have |
| **Connes** | forces the spectral interpretation to be **absorption, not emission** — *"a crucial negative sign… indicates that the spectral interpretation should be as an absorption spectrum, or equivalently should be of a cohomological nature"* |
| **Hilbert–Pólya as usually stated** | assumes **emission** — eigenvalues of an operator, present lines |

> ### The sign may be telling us the naive Hilbert–Pólya framing is wrong.
>
> An emission spectrum is a set of eigenvalues. An absorption spectrum is a set of
> **missing** eigenvalues — a cohomological object, not an operator's point spectrum.
>
> **If Connes is right about what the sign means, then "find the self-adjoint operator" is
> the wrong instruction**, and the wanted poster's conditions 3 and 6 are describing the
> rigidity of a thing that is not a spectrum in the ordinary sense.

`[READING — the synthesis is mine; the two ingredients are sourced. This is the most
speculative claim in the article and the one I would most want attacked.]`

## 8.3 The degeneracy dichotomy, now with both sides sourced

| | Length spectrum | Statistics |
|---|---|---|
| **Generic hyperbolic (twisted)** — Marklof–Monk | generic, no arithmetic | **GUE — proved** |
| **Arithmetic hyperbolic** — modular surface and relatives | **exponentially degenerate** | **Poisson** |
| **The primes** | **arithmetic AND degeneracy-free** | **GUE — observed** |

**The middle row's mechanism is explicit in the literature:** *"the high degeneracy of the
length spectrum is responsible for the Poissonian behaviour of the eigenvalues,"* and
arithmetic properties *"lead to an exponential degeneracy of the lengths of periodic
orbits."* `[FACT — sourced]`

> **So the primes are the anomaly, and that is the good news.**
>
> Arithmetic *normally* produces exponential length degeneracy, and degeneracy *normally*
> destroys random-matrix statistics. **The primes are arithmetic and carry no degeneracy
> at all** — distinct primes have rationally independent logarithms, by unique
> factorisation.
>
> **Unique factorisation is exactly the property that makes the prime length spectrum
> degeneracy-free.** It is the difference between the primes and the trace-degeneracies of
> an arithmetic group.

**That is the sharpest thing this article can say about where to look.** The wanted
system is not "arithmetic like the modular surface." It is arithmetic **in the way the
primes are** — multiplicatively free, additively rigid in their logarithms.

---

# 9 · WHAT OUR CENSUS CAN AND CANNOT TEST

**Can:**

1. **Condition 2 directly.** `[MEASURED]` We followed the return comb twice — periods
   r·log p, weights 1/(r²pʳ). **Any proposed system can be checked against it today.** A
   candidate with free parameters tuned to fit already fails; the poster has none.
2. **Condition 5's consequences.** `[MEASURED]` At reach 50,000, small-gap behaviour
   agrees with the finite-height-corrected GUE model within a stated bound, pooled
   z = −0.75 over 63,515 arches. A candidate predicting deviation beyond that at these
   heights is excluded.
3. **Condition 3, indirectly.** Uniform instability λ = 1 is what produces the p^(−r/2)
   amplitudes, and the small-gap statistics depend on those amplitudes. **The census is
   weakly sensitive to a Lyapunov exponent**, which is not how anyone thinks of it.
   `[READING]`
4. **§8.3's dichotomy, in principle.** Degeneracy in a length spectrum produces
   **Poisson** statistics. Our census measured GUE-consistent behaviour with no sign of
   Poisson contamination — **weak positive evidence that the prime length spectrum really
   is degeneracy-free at these heights**, which is the anomaly §8.3 rests on. `[READING]`

**Cannot:**

- **Build a system, or narrow which route is right.**
- **Resolve §8.1.** Deriving the oscillating term from a mechanism is the whole problem
  and no census touches it.
- **Test any drum.** The census tests *consequences* of drums; the drums do not exist.

---

# 10 · WHAT WOULD BREAK THE DEADLOCK

| Route | What must happen | Status after this audit |
|---|---|---|
| **Derive the oscillating term** | produce Σ_p log p · p^(−r/2) cos(rE log p) **from a mechanism**, not by construction | **§8.1 — nobody has ever done this. The single most important target.** |
| **Close Connes's transfer** | prove Weil positivity | live, narrowing, finitely approximable — the Galerkin work |
| **Break Selberg's symmetry on a SPECIFIC surface** | Marklof–Monk give GUE for *generic* twisted surfaces; make it one arithmetic, degeneracy-free surface | **symmetry solved; specificity open** |
| **Quantise xp with closed orbits AND fluctuations** | Sierra fixed the orbits; the oscillating term is still missing | narrower than it was |
| **Test §8.2** | decide whether the sign means the object is cohomological rather than spectral | **would redirect the whole programme if answered** |

---

# WHAT THIS ARTICLE CLAIMS

- **The wanted poster is derived**, seven conditions, each forced by matching two standard
  formulas. `[READING on the derivation; FACT on the formulas]`
- **λ = 1 from the amplitudes and h = 1 from the prime counting agree** — independent
  derivations, unrelated arithmetic facts, same number. Checkable with a pen.
- **The ½ is where that consistency comes from.** `[READING]`
- **The xp family has reproduced the smooth term and never the fluctuations** — §8.1.
  `[READING on the framing; FACT on both underlying results]`
- **The negative sign appears in the matching and in Connes's absorption reading, and may
  mean the naive spectral framing is wrong** — §8.2. **The most speculative claim here.**
- **Arithmetic normally produces exponential length degeneracy and Poisson statistics; the
  primes are degeneracy-free by unique factorisation, and that is the anomaly to exploit**
  — §8.3. `[FACT on both halves; READING on the synthesis]`
- **A finite quantum graph provably cannot realise {log p}.** `[READING — check it]`

## WHAT IT DOES NOT CLAIM

- **No proof, and no prediction of which route succeeds.**
- **No claim that the audit is complete.** Six routes plus Selberg; the field is larger.
- **Bender–Brody–Müller is CONTESTED, not refuted** — corrected from the previous version,
  which overstated it.
- **Marklof–Monk make no reference to the Riemann hypothesis.** Their theorem is a
  moduli-space average over generic large-genus surfaces, and Riemann needs one specific
  arithmetic system. **Nobody has joined them.**
- **Nothing our census did contributes to building a drum.**

**The sentence to keep:**

> Every route to the operator has reproduced the smooth term, which contains no
> arithmetic, and none has ever derived the oscillating term, which contains all of it —
> and the reason the arithmetic is so hard to reach is that arithmetic normally brings
> exponential degeneracy and Poisson statistics with it, while the primes bring none at
> all, because unique factorisation makes their logarithms rationally independent; so the
> object being hunted must be arithmetic in the one way the primes are arithmetic and
> nothing else in geometry is.

---

# SOURCES

**Searched 2026-08-05. Section 2's derivation is checkable by hand; everything below is
where the attributions come from.**

**Hyperbolic surfaces, symmetry classes and random matrix theory**
- Marklof, J. & Monk, L., *The moduli space of twisted Laplacians and random matrix
  theory* — [arXiv:2407.10778](https://arxiv.org/abs/2407.10778) ·
  [IMRN, doi:10.1093/imrn/rnae239](https://doi.org/10.1093/imrn/rnae239)
- *GOE statistics on the moduli space of surfaces of large genus* —
  [arXiv:2202.06379](https://arxiv.org/pdf/2202.06379)
- *Almost sure GOE fluctuations of energy levels for hyperbolic surfaces of high genus* —
  [arXiv:2301.05964](https://arxiv.org/pdf/2301.05964)

**Arithmetic quantum chaos and the degeneracy mechanism**
- Bogomolny, Georgeot, Giannoni & Schmit, *Arithmetical chaos*, Physics Reports —
  [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0370157397000161)
- *Arithmetical quantum chaos* — [Scholarpedia](http://www.scholarpedia.org/article/Arithmetical_quantum_chaos)
- *Some studies on arithmetical chaos in classical and quantum mechanics* —
  [arXiv:chao-dyn/9305005](https://arxiv.org/pdf/chao-dyn/9305005)
- *The correlation between multiplicities of closed geodesics on the modular surface* —
  [arXiv:math/0104234](https://arxiv.org/pdf/math/0104234)

**The xp family**
- Sierra, G. & Rodríguez-Laguna, J., *H = xp model revisited and the Riemann zeros*,
  Phys. Rev. Lett. **106**, 200201 (2011) —
  [arXiv:1102.5356](https://arxiv.org/pdf/1102.5356) ·
  [APS](https://link.aps.org/doi/10.1103/PhysRevLett.106.200201)
- Sierra, G., *A quantum mechanical model of the Riemann zeros* —
  [arXiv:0712.0705](https://arxiv.org/pdf/0712.0705)
- Sierra, G., *A physics pathway to the Riemann hypothesis* —
  [arXiv:1012.4264](https://arxiv.org/pdf/1012.4264)
- *Physics of the Riemann Hypothesis* — [arXiv:1101.3116](https://arxiv.org/pdf/1101.3116)

**Connes and Weil positivity**
- Connes, A., *Trace formula in noncommutative geometry and the zeros of the Riemann zeta
  function*, Selecta Math. —
  [Springer](https://link.springer.com/article/10.1007/s000290050042)
- Connes, Consani & Marcolli, *The Weil proof and the geometry of the adeles class space*
  — [PDF](https://math.nyu.edu/~tschinke/.manin/submitted/ConnesConsaniMarcolli.pdf)
- Connes & Consani, *Weil positivity and trace formula: the archimedean place* —
  [arXiv:2006.13771](https://arxiv.org/pdf/2006.13771)

**de Branges and the counterexample**
- Conrey, J. B. & Li, X.-J., *A note on some positivity conditions related to zeta- and
  L-functions*, IMRN 2000 No. 18 —
  [arXiv:math/9812166](https://arxiv.org/abs/math/9812166)
- de Branges, L., *The Riemann hypothesis for Hilbert spaces of entire functions* —
  [Purdue](https://www.math.purdue.edu/~branges/riemann-hilbert.pdf)
- *On a conjecture of de Branges* (2025) — [arXiv:2507.12576](https://arxiv.org/pdf/2507.12576)

**Bender–Brody–Müller and the dispute**
- Bellissard, J., *Comment on "Hamiltonian for the zeros of the Riemann zeta function"* —
  [arXiv:1704.02644](https://arxiv.org/abs/1704.02644) (9 Apr 2017)
- *A note on "Hamiltonian for the zeros of the Riemann zeta function"* —
  [arXiv:1704.04705](https://arxiv.org/pdf/1704.04705)
- Bender, Brody & Müller, *Comment on 'Comment on…'* —
  [arXiv:1705.06767](https://arxiv.org/abs/1705.06767) (18 May 2017)

**Twisted Selberg zeta machinery**
- Spilioti, P., *Determinants of twisted Laplacians and the twisted Selberg zeta function*
  — [arXiv:2512.16681](https://arxiv.org/html/2512.16681)
- *Twisted Ruelle zeta function at zero for compact hyperbolic surfaces* —
  [arXiv:2105.13321](https://arxiv.org/pdf/2105.13321)
