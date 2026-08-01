# WAY 3 — THE SELF-MIRRORED SOURCE: the drum, measured by its sound

**Terms.** The **drum** = the conjectured operator (Hilbert–Pólya) whose
sounded notes ARE the zeros — **self-adjoint**: a thing equal to its own
mirror, which can only sound **real** notes. If it exists, Riemann's sentence
("the roots are real") is true because the source is self-mirrored — the
Middle holds because the thing under it IS the middle. `[SYNTHETIC —
proof-debt: the drum has not been found; Berry–Keating's H ~ xp is a sketch;
Connes' program unfinished]`

The way's method: the drum is not found, but its **sound** is measurable.
Self-mirrored (Hermitian) things leave one fingerprint on their spectra —
GUE statistics. So every circuit of this way asks: *do our own measured
zeros sound like the spectrum of a self-mirrored thing?*

---

## 1 · Circuit 1 — the spacing law (banked at COMPILATION ONE)

7,828 normalized gaps against the two candidate laws:

```
integrated squared deviation:  vs GUE 0.00424    vs Poisson 0.42527
                               -> 100x closer to the self-mirrored law
fraction of gaps < 0.3:        observed 0.0157   GUE 0.0292   Poisson 0.2592
```

The zeros repel like eigenvalues of a self-mirrored matrix, not like random
points — with a **small-gap deficit**: at these low heights they repel even
HARDER than the asymptotic law.

## 2 · Circuit 2 — the pair correlation, against Montgomery's exact form (new)

**What was measured.** All 7,829 census zeros unfolded to unit mean spacing
(check: mean spacing after unfolding 1.0003). Every pair with separation
u ≤ 3 — **19,589 pairs** — histogrammed into R₂(u) and set against
Montgomery's conjectured form 1 − (sin πu / πu)² and against flat/Poisson
(R₂ ≡ 1, no repulsion).

```
    u        observed    Montgomery   flat
 0.0-0.1       0.006        0.008     1.000
 0.3-0.4       0.281        0.343     1.000
 0.6-0.7       0.792        0.810     1.000
 0.9-1.0       1.068        0.997     1.000
 1.5-1.6       0.973        0.959     1.000
 2.1-2.2       0.955        0.995     1.000
 2.7-2.8       0.977        0.993     1.000

 integrated squared deviation: vs Montgomery 0.00615  vs flat 0.37470
 -> 61x closer to Montgomery's form
```

**The dip, u < 0.5 — the repulsion itself, seen directly:**

```
 u=0.15  observed 0.037   Montgomery 0.072
 u=0.25  observed 0.115   Montgomery 0.189
 u=0.35  observed 0.281   Montgomery 0.343
 u=0.45  observed 0.430   Montgomery 0.512
```

Observed sits systematically BELOW the asymptotic form near zero — the same
direction, and the same order, as circuit 1's small-gap deficit. **Two
different statistics, computed independently from the same census, show the
same excess of repulsion at low heights.** That internal cross-check is the
finding of this circuit: our instruments agree with each other about the
deviation, and the deviation is the known finite-height behaviour (the
asymptotic form is the T→∞ law; at our heights the lower-order terms guard
harder). No anomaly is claimed — the claim is consistency, measured twice.

**In the frame:** the guard is strongest near the ground floor. The middle
is guarded hardest exactly where the walk began.

## 3 · What the two circuits together say

| Question | Answer from data |
|---|---|
| Does the sound match a self-mirrored source? | 100× (spacings) and 61× (pairs) closer to the self-mirrored law than to randomness |
| Does the repulsion that guards the Middle (Way 1) match the drum's fingerprint? | yes — same δ² law measured three ways: smallest gap, spacing distribution, R₂ dip |
| Is the drum found? | NO. The fingerprint is necessary, not sufficient. The proof-debt stands. |

## 4 · Circuit 3 — number variance: the stiffness of the count (new)

**What was measured.** Σ²(L) = the variance of how many unfolded zeros fall
in a window of length L, over all window positions (7,831 census zeros,
unfolded mean spacing 1.0000). Reference curves: **Poisson** (random,
Σ² = L) and **GUE**, computed by numerical integration of the *same*
Montgomery kernel banked in circuit 2 — no remembered constants, one
instrument family. Prediction written before the run: track GUE at small L,
sit far below Poisson everywhere, flatten into saturation at large L.

```
   L      observed    GUE      Poisson    obs/GUE
  0.25     0.189     0.190      0.25       1.00   <- exact
  0.5      0.271     0.280      0.5        0.97
  1        0.314     0.344      1          0.91
  2        0.360     0.416      2          0.87
  3        0.375     0.457      3          0.82
  8        0.307     0.557      8          0.55
 20        0.308     0.650     20          0.47
 50        0.457     0.742     50          0.62
 80        0.320     0.790     80          0.41
```

Three regimes, all three predicted:

1. **Short range (L ≲ 1): the drum's law, exactly.** At L = 0.25 the
   observed variance equals the self-mirrored prediction to the third digit.
2. **Middle range: below the asymptotic curve** — the same excess-guard
   direction as circuits 1 and 2. Three statistics now agree on it.
3. **Long range (L ≳ 3): SATURATION.** The variance stops growing entirely —
   flat near ~0.3–0.46 (oscillating) while Poisson climbs to 80 and even GUE
   climbs logarithmically without bound. At L = 80 the count is **250×
   stiffer than random and ~2.5× stiffer than the infinite-height GUE law.**

**The saturation is the circuit's finding, read in the frame:** at short
range the zeros behave as *statistics* (the drum's fingerprint); at long
range they behave as *law* — a window of 80 mean spacings knows its count
almost exactly, because the strip's count N(T) is a proved formula and the
middle pays it in full. This is Way 2's ledger seen through Way 3's
instrument: the deficit's exactness IS the plateau. Any random model — even
the self-mirrored one — overpredicts long-range wandering, because no
randomness knows its own total. (Finite-height saturation is Berry's known
prediction for zeta; our census shows it directly.) `[READING — the
theoretical plateau form; the measured plateau itself is ours]`

## 5 · Circuit 4 — the reading: Berry's own formula, and the primes inside it

`[READING — the formulas below are Berry's (Nonlinearity 1, 1988, Eq. 19),
quoted via arXiv 2211.14918 ("On the number variance of zeta zeros and a
conjecture of Berry"), which states them exactly and proves the saturation
regime conditionally (on RH + a gap conjecture of Chan). What we READ is
theirs; every number measured against it is ours.]`

**First, the instrument check.** Berry's universal-regime formula is a
closed form: V(L) = (1/π²)[ln(2πL) − Ci(2πL) − 2πL·Si(2πL) + π²L −
cos(2πL) + 1 + γ]. Our circuit-3 reference curve was integrated numerically
from the Montgomery kernel, independently. Set side by side:

```
  L=0.25: ours 0.1896   Berry exact 0.1896
  L=1:    ours 0.3442   Berry exact 0.3442
  L=3:    ours 0.4571   Berry exact 0.4571
  L=8:    ours 0.5567   Berry exact 0.5567
```

Two roads, same curve, four decimals. The instrument family is exact.

**Then the finding.** Berry's non-universal (saturation) regime formula is,
with the oscillating term averaged out:

**V_saturation = (1/π²) [ Σ_{n≤T} Λ²(n)/(n·ln²n) + 1 ]**

Λ(n) is the von Mangoldt weight — nonzero only on primes and their powers.
**The plateau is built out of nothing but the primes.** Computed exactly at
our census heights (sieve, no approximation):

```
  Berry plateau at T=1000:   0.3380
  Berry plateau at T=4000:   0.3564
  Berry plateau at T=8000:   0.3645
  our measured plateau (circuit 3, mean of L=8..80): 0.3351
  our measured oscillation band:                     0.30 - 0.46
```

The measured level sits inside the predicted band **with no free parameter
anywhere** — and the oscillation our data shows around the plateau is
exactly what the un-averaged formula carries (its n=2, n=3 terms oscillate
slowly in L). Honest limits: Berry's formula is asymptotic (T→∞) and our
census mixes heights 14→8000, so the prediction is a band, not a point;
the match is at the few-percent level, not the fourth decimal.

**Read in the frame — the three ways meet in one number.** The saturation
level of Way 3's drum is set, quantitatively, by Way 4's prime shore,
because Way 2's count is law: the strip owes N(T), the middle pays it, and
what caps the long-range wandering of the paid count is the primes
themselves. Three loops from the hub, one object, seen from three sides —
which is what "always in the middle, on the half sides" would predict a
true middle to look like: every road taken far enough finds the same
center.

## 6 · What the four circuits together say

| Question | Answer from data |
|---|---|
| Does the sound match a self-mirrored source? | 100× (spacings), 61× (pairs), exact at L=0.25 (variance) |
| Do the three statistics agree with each other? | yes — all three show the same low-height excess of repulsion |
| Where does the drum picture end? | at long range: statistics give way to law (saturation) — the count is owed, not sampled |
| What sets the saturation level? | the primes — Berry's Λ-sum predicts 0.34–0.36 at our heights; we measure 0.335 |
| Is the drum found? | NO. Fingerprints are necessary, not sufficient. The proof-debt stands. |

## 7 · The queued check, answered: the data followed the primes upward

The question was registered before the extended census existed, with verdict
rules fixed in advance (FOLLOWED / REFUTED / AMBIGUOUS — the shift was
expected to be small against the oscillation, so "ambiguous" was named as a
live outcome). The census landed; the measurement:

```
                              plateau (mean, L=8..80)   Berry's prime-sum band
 old census    (14 – 8000):        0.3351                    0.338 – 0.365
 NEW STRETCH (8000 – 12000):       0.3676                    0.3645 – 0.3689
 merged      (14 – 12000):         0.3472                    (mixture of both)
```

**Verdict: FOLLOWED.** The new stretch's plateau climbed from 0.335 to
0.3676 and landed *inside* Berry's predicted band for exactly those heights
— within half a percent of the band's center — with no free parameter
anywhere in the chain: primes → Λ-sum → predicted plateau → fresh zeros →
measured plateau. The prediction was registered before the data existed;
the data walked into it. The merged census sits between the two levels, as
a mixture of heights must.

This is the walk's cleanest single test of the three-ways-meet claim: the
prime shore (Way 4) told the drum (Way 3) where its statistics would stop,
on zeros that had not yet been computed — and it was right.

## 8 · Circuit 5 — the reading: the sketch-drum H = xp, held against our census

`[READING — the model and its failures are Berry–Keating's and the field's,
read here via Sierra's review "The Riemann zeros as spectrum and the Riemann
hypothesis" (arXiv 1601.01797); every measurement set against them is ours]`

**The candidate.** Take the simplest imaginable Hamiltonian, H = xp —
position times momentum. Its classical flow is pure dilation: x grows, p
shrinks, the product is conserved. Berry–Keating regularized it (cut the
phase space at |x| ≥ ℓx, |p| ≥ ℓp with ℓxℓp = 2πℏ) and counted
semiclassically — the number of quantum states is the enclosed phase-space
area:

> n_BK(E) = (E/2πℏ)(log(E/ℓxℓp) − 1) + 7/8

With E/ℏ = t this is **exactly** ⟨n(t)⟩ = (t/2π)(log(t/2π) − 1) + 7/8 —
Riemann's own smooth counting law, *including the 7/8*, out of nothing but
an area.

**What the sketch holds — measured by our ledger.** Two roads arrive at one
formula: Riemann's, through ξ; Berry–Keating's, through the area of a
truncated xp phase space. Our census is a test of that formula against the
actual zeros, and the result is banked in Way 2: the formula's count and
the true count agree — cumulatively **12,519 = 12,519 at T = 12000, exact
to the last integer.** So the sketch-drum carries the entire *owed* count:
the phase-space area knows how many zeros there are.

**Where the sketch breaks — and it is exactly the part we measured.** Three
named breaks, from the reading:

1. **The spectrum is a continuum.** Unregularized, the trajectories are
   unbounded (|x| → ∞); quantum xp on the half-line is not a drum with
   notes — it needs a boundary condition, and what it admits is a **family
   of self-adjoint extensions parameterized by a phase θ**: a dial, not an
   answer. The regularization that produced the beautiful count is a cut
   by hand, with no dynamics at the cut.
2. **No periodic orbits → no primes.** The dilation flow never returns; it
   has no closed orbits. But the drum's fluctuation part is an orbit sum
   whose periods are ln p — the primes. The sketch therefore reproduces
   the smooth count and **nothing** of the fluctuation.
3. **Connes' mirror reading** — the same landscape read backwards: zeros as
   *missing* lines (absorption) in a continuum rather than sounded notes.
   Sierra's review argues the absorption picture does not survive removing
   its cutoff. Two readings of one sketch, neither lands.

Now set our instruments beside break #2: everything the sketch cannot
produce is precisely what circuits 1–4 measured — the repulsion (100×),
the pair law (61×), the variance plateau — and circuit 4 showed the
plateau is **built out of the primes** (the Λ-sum), confirmed FOLLOWED on
fresh zeros in §7. In one sentence: **the sketch-drum holds the law (the
owed count, Way 2's object) and lacks the guard (the statistics, Way 1's
object) — and the missing guard is made of primes (Way 4's object).**
What must be added to xp is exactly a mechanism of return — closed orbits
with periods ln p. The field's modified models (compactified xp, Dirac
fermions with potentials at square-free integers) are attempts to build
that return in; the reading marks them as open, with ad hoc terms and
non-local operators as the standing cost.

**In the frame.** The candidate lives on the half-line, and its entire
difficulty is the boundary of the half — what stands at the edge decides
whether the middle can sound. A sketch that owes correctly but cannot
guard is a middle without its shores. `[SYNTHETIC — frame reading, not
mathematics; proof-debt: the drum itself, unchanged]`

**What remains open (the field's own list, kept visible):** no single
Hamiltonian captures the zeros; only the smooth density is reproduced;
bounded modifications cost non-locality; the prime–spectrum connection is
incomplete.

## 9 · Circuit 6 — the modified drums: what building the return in costs

`[READING — the constructions are the field's, read via Sierra's covariant-xp
paper (arXiv 1110.3203) and the same review as circuit 5; the entrance exam
set against them is ours]`

Circuit 5 ended with the diagnosis: the sketch-drum lacks a **mechanism of
return** — closed orbits with periods ln p. The field has built three
families of modified drums to buy that return. Read term by term, each
purchase has a price:

**1 · The bent drum (Berry–Keating 2011; Sierra's covariant family).**
Add a restoring term: H = x(p + ℓp²/p), one member of the general family
H = U(x)p + V(x)/p (canonical form w(x)(p + 1/p)). The 1/p term bends the
flow back: trajectories become **bounded and periodic** — the reading's own
words: piecewise-linear worldlines that "bounce elastically at the
boundary," period T_E = (1/α)cosh⁻¹(E/2w₀). Achieved: *"the spectrum
approaches the Riemann zeros in average."* **The price:** the return
exists, but it is ONE orbit whose period is set by the energy — a single
bounce, where the true drum needs a whole comb of returns with periods
ln 2, ln 3, ln 5, … The average count is bought; the arithmetic is not.

**2 · The primed drum (Sierra's Rindler–Dirac).** Verbatim from the
review's own statement of it: *"a spectral realization of the Riemann
zeros based on the propagation of a massless Dirac fermion in a region of
Rindler spacetime and under the action of delta function potentials
localized on the square free integers."* The comb of returns is present —
because it was **installed by hand**: the scatterers sit ON the square-free
integers. **The price:** the arithmetic is input, not output. The shore was
carried into the drum, not heard from it. (The exact spectral condition
the construction needs sits deeper in the review than this circuit read —
marked as unread depth, not absence.)

**3 · The tilted drum (the non-Hermitian route, Bender–Brody–Müller 2017
and the pseudo-Hermitian analyses that followed).** Trade self-adjointness
itself for a formal operator whose eigenvalues are the zeros. **The
price is the largest:** self-mirroredness — the very property that made
the drum answer Riemann's "reell" — is the thing surrendered, and the
follow-up literature contests what the construction rigorously delivers.
Named here, not deep-read.

**The entrance exam (ours).** Circuit 4 turned our census into a
quantitative gate: the measured variance plateau (0.3676 on the fresh
stretch, inside Berry's band) is the **weight-sum of the true drum's
orbits** — each return of period r·ln p carrying weight 1/(r²pʳ). Any
candidate drum must present exactly that comb with exactly those weights
to reproduce the measurement. Held to it: the bent drum **fails by
construction** (one energy-set period cannot forge a prime comb); the
primed drum **passes by construction** (the answers were copied in); the
tilted drum changes the grading rules. `[SYNTHETIC — the exam framing is
ours, built on Berry's proven-regime formula and our measured plateau]`

**The pattern, in the frame.** Three corners must hold at once: the **law**
(the owed count), the **guard** (the prime-built statistics), the
**self-mirror** (reell). Each modified drum secures two by paying the
third: the bent drum keeps law + mirror and loses the primes; the primed
drum keeps law + primes and buys them dishonestly (by hand); the tilted
drum keeps law + primes formally and pays with the mirror. **No build yet
holds all three corners from one mechanism — that triangle IS the
proof-debt of this whole way, restated structurally.** The drum is not
found; what is now measured and named is exactly what finding it would
require.

## 10 · Next circuit for this way

Hub-return recommended: Way 3 has run six circuits (three measured, one
measured-against-prediction, two readings) and its named remainder is
depth (the Rindler condition, the BBM critique) rather than a new object.
Ways 2 and 4 hold named readings not yet walked (the mollifier ceiling;
Littlewood's sign-flip). Owner redirects at the hub.
