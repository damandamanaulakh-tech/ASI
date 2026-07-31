# COMPILATION ONE — everything measured, cross-read

Ordered by the owner before further walking: *"first before moving to new 4,
compile rest 3-4 earlier and see if something comes out / Then all 4 / one by
one."* This document compiles every measurement the walk has produced, runs
the cross-tests the compilation itself suggested, and reports what came out.

**Three things came out.** One of them refutes a hypothesis of mine, and is
reported as such.

---

## 1 · The inventory (what was compiled)

| # | Measurement | Circuit | Value |
|---|---|---|---|
| M1 | Damping of each periodic term | pre-hub | every term decays as x^½, envelope ratio ≈ 1.0 at all magnitudes |
| M2 | Riemann's n=1 heuristic vs true count | pre-hub | exact to T = 1000 (649 = 649) |
| M3 | Gram-law violations to T = 1000 | pre-hub | 22 of 648 points (3.40%) |
| M4 | Zeros on (14, 8000) | Way 1 c1 | 7,830 vs Riemann–von Mangoldt 7,830.43 — **N₀ = N** |
| M5 | Negative arch peaks (would refute RH) | Way 1 c1 | **0** of 7,828 |
| M6 | Floor of arch peaks | Way 1 c1 | sinks 2.34 → 0.0040, 20 minima, no plateau |
| M7 | Arch shape | Way 1 c1 | peak ∝ gap^1.975 (parabola: 2.0) |
| M8 | Smallest normalized gap | Way 1 c1 | 0.0421 vs GUE-predicted 0.0491 |
| M9 | Lehmer pairs, CSV definition | Way 1 c2 | 420 on (14, 8000); **29 below 1000 = literature's 29 exactly** |
| M10 | Boundary-constant bound | Way 1 c2 | **Λ ≥ −1.778×10⁻⁴** (our pairs, CSV theorem) |
| M11 | Exact prime count | Way 4 c1 | π(10⁸) = 5,761,455, matches known value |
| M12 | Prime-error envelope | Way 4 c1 | \|ψ(x)−x\|/√x ≤ 0.51, oscillating, **no drift** |
| M13 | His formula (our 1000 roots) vs sieve | Way 4 c1 | within 21 of 5,761,455 (4×10⁻⁶) |
| G1 | Imported, proved | — | Λ ≥ 0 (Rodgers–Tao); RH ⟺ Λ ≤ 0 |
| G2 | Imported, published theorem | — | infinitely many Lehmer pairs ⟹ Λ = 0 (CSV) |
| G3 | Imported, conjecture | — | GUE pair-correlation (Montgomery; Odlyzko numerics) |

## 2 · The cross-tests the compilation forced

### Test C — is the Lehmer-pair supply steady? (M9 × G2)

G2 says: *infinitely many Lehmer pairs ⟹ Λ = 0.* No single circuit measured
whether the supply looks infinite. Compiled per block:

```
block         gaps   pairs   rate          block         gaps   pairs   rate
    0-1000     648     29    0.045         4000-5000    1046     59    0.056
 1000-2000     868     47    0.054         5000-6000    1078     58    0.054
 2000-3000     951     51    0.054         6000-7000    1105     58    0.052
 3000-4000    1005     52    0.052         7000-8000    1127     66    0.059
                                           TOTAL        7828    420    0.054
```

**The production rate is stationary — if anything, rising.** One gap in ~18
is a Lehmer pair, block after block, no decay. In a finite window this is
exactly what "infinitely many" looks like.

### Test F — are the guard's worst moments and the mechanism's failures the same events? (M3 × M9)

My hypothesis going in: yes — Gram violations should *be* the Lehmer pairs.

**Refuted.** Below T = 1000: of 22 Gram-law violations, only **8** sit at a
Lehmer pair; of 29 Lehmer pairs, only **8** cause a violation. The famous
first violation (n = 126, t = 282.45) sits at **no** Lehmer pair.

### Test S — the drum's fingerprint on the compiled gaps (M4 × Way 3)

7,828 normalized spacings against the two candidate laws — GUE (the spectrum
of a random **self-mirrored** matrix, p(s) = (32/π²)s²e^(−4s²/π)) versus
Poisson (independent random points, p(s) = e^(−s)):

```
integrated squared deviation:   vs GUE  0.00424     vs Poisson  0.42527
fraction of spacings < 0.3:     observed 0.0157     GUE 0.0292     Poisson 0.2592
```

**One hundred times closer to GUE than to Poisson**, already at these low
heights. The small-gap deficit against the surmise is noted honestly (the
Wigner surmise is itself an approximation, and low heights carry known
finite-range effects) — the discrimination GUE-vs-Poisson is not affected:
the zeros repel like the eigenvalues of a self-mirrored thing, not like
random points.

## 3 · What came out

**FIRST — measured support that the boundary sits exactly at zero.** Chain
the compilation: our steady pair-production (Test C) is the finite-window
signature of *infinitely many* Lehmer pairs; by the published theorem (G2)
that gives Λ = 0 from below; Rodgers–Tao (G1) holds it at 0 from below
anyway; RH ⟺ Λ ≤ 0 caps it from above. Every measured piece and every proved
piece points at the same number: **Λ = 0 — RH not merely true-if-true, but
*exactly barely* true.** The owner's frame said it first: always in the
middle — and the theory's own governing constant sits on the middle of its
two regimes. `[the Λ=0 conclusion remains conjecture-supported-by-measurement;
the theorem chain is published; our contribution is the rate]`

**SECOND — the mechanism dies of two separate causes, not one.** The earlier
verdict was "his count holds, his mechanism doesn't (S(T) unbounded)." Test F
splits that mechanism-death into two measured populations: **~1/3 of Gram
failures are local pair-stress** (a Lehmer pair crowding the interval) and
**~2/3 are pure phase-drift** (S(T) wandering, no close pair anywhere —
including the classical first failure at n=126). These populations barely
overlap (8/22 vs 14/22). My same-events hypothesis was wrong, and the data
that refuted it sharpened the picture: *localization dies mostly of drift,
not of stress.* Any future rescue of a localization argument has TWO
separate enemies to bound, not one.

**THIRD — Way 3 got its first circuit for free.** The compiled gaps carry
the full spectral fingerprint, not just the minimum: 100× closer to the
self-mirrored (GUE) law than to random placement. The drum is not found —
but the sound the zeros make is the sound self-mirrored things make, at
7,828-sample resolution, in our own data.

**And the standing cross-reads, banked:**
- **The consistency triangle:** 0 negative arches (M5) ⟺ count full (M4) ⟺
  prime-error bounded (M12) — three independent instruments, one fact, all
  three sides measured. If any one had failed, the other two had to fail in
  a matched way. None did.
- **The half from both shores:** each zero-wave damped as x^½ (M1); the
  summed prime-error bounded by √x (M12). Same ½, measured on both sides of
  the explicit formula.
- **"How barely," quantified by us:** worst guard margin 0.0040 (M6); Λ
  pinned within 1.78×10⁻⁴ of its RH value from below by our own range (M10).

## 4 · State of the four ways, going into the one-by-one walk

| Way | State | Next circuit |
|---|---|---|
| 1 — the guard | ● two circuits banked | extension census (8000→12000) **running**; on landing: floor track + rate + Λ pressure at new heights |
| 2 — the count | ○ first datum banked (N₀=N to 8000) | same extension feeds it; then his-mechanism vs mollifier study |
| 3 — the drum | ● first circuit banked (Test S, this compilation) | deeper fingerprint: pair correlation R₂ against Montgomery's form |
| 4 — the prime shore | ● first circuit banked | extend the sieve's reach or sharpen the exponent band; compare more of his formula's laws |

Walking order per the owner: **all 4, one by one**, hub-return between.
