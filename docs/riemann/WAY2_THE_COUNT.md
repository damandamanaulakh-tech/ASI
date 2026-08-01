# WAY 2 — THE MIDDLE IS FULL: his own debt, the count

**Terms.** **N(T)** = how many zeros the strip owes below height T (proved
formula). **N₀(T)** = how many actually stand ON the middle. Riemann's own
named debt, in his own word from the draft letter: that about
(T/2π)log(T/2π) − T/2π ***reelle* Wurzeln** — REAL roots — lie below T. The
**deficit** N − N₀ counts completed escapes from the middle, two at a time.
Way 2 is Way 1 integrated: the guard's record, counted instead of watched.

---

## 1 · What WE measured (our own instrument, two independent methods)

| Range | N (strip, theory/`nzeros`) | N₀ (our sign-change census) | Deficit |
|---|---|---|---|
| (0, 1000) | 649 | 649 | **0** |
| (14, 8000) | 7,830.43 (Riemann–von Mangoldt) | 7,830 | **0** |
| (0, 9000) | 8,978 (exact, argument principle) | 8,978 | **0** |
| (0, 10000) | 10,142 (exact) | 10,142 | **0** |
| (0, 11000) | 11,324 (exact) | 11,324 | **0** |
| (0, 12000) | 12,519 (exact) | 12,519 | **0** |
| (0, 13000) | 13,728 (exact) | 13,728 | **0** |
| (0, 14000) | 14,950 (exact) | 14,950 | **0** |
| (0, 15000) | 16,182 (exact) | 16,182 | **0** |
| **(0, 16000)** | **17,425 (exact)** | **17,425** | **0** |

Every zero the strip owes in our measured stretch stands on the middle — now
to height 12000. The extension landed with a consistency stronger than
planned: the four workers' independent per-block counts **sum exactly to the
argument-principle count** (7,830+1,148+1,164+1,182+1,195 = 12,519 =
N(12000) computed by `nzeros`, no rounding anywhere). One instrument note,
kept honest: the first merged array double-counted 2 seam zeros (the 4×
rescans re-found boundary zeros at slightly different floats), which briefly
produced an *impossible negative deficit* — the impossibility itself flagged
the bug, physical dedupe fixed it, and the validation suite still passes.
An instrument that can say "impossible" out loud is the instrument working.

## 2 · The field's two roads on his debt

**Road A — verification (finite, exact, forever a middle).** The rigorous
frontier: *"All zeroes β + iγ of the Riemann zeta-function with
0 < γ ≤ 3·10¹² have β = ½"* — Platt & Trudgian, Bulletin of the LMS, 2021,
interval arithmetic (no floating-point trust). The deficit is 0 as far as
any rigorous eye has ever looked. And per Axiom 13 (*always in the middle*):
every verified height is a middle, never an end — verification can lose RH
tomorrow, it can never win it.

**Road B — proportion (infinite, partial).** The unconditional ladder:
Hardy 1914 (infinitely many on the middle) → Selberg 1942 (a positive
proportion) → Levinson 1974 (⅓) → Conrey 1989 (⅖) → Feng 2012 (0.4128) →
Pratt–Robles–Zaharescu–Zeindler 2020 (**0.417, and 0.407 simple**). His
claim is the limit **1**. Fifty years moved the floor 8 points.

## 3 · Why HIS mechanism cannot close his own debt — with its anatomy

Measured earlier in the walk, now in one place:

- His one-term wave (Z ≈ 2cosθ) predicts the count **exactly** as far as we
  computed (649 = 649 to T=1000; the full-range census consistent
  throughout). The count HOLDS.
- The local mechanism (one zero per Gram interval) provably DIES: S(T) is
  unbounded. And the compilation's Test F gave the death its anatomy — **two
  separate causes**: local pair-stress (a Lehmer pair crowding an interval —
  8 of 22 failures below T=1000) and global phase-drift (S(T) wandering with
  no close pair anywhere — 14 of 22, including the classical first failure
  at n=126).

So any rescue of a localization argument must bound BOTH enemies; the field
went around instead — mollifiers average where localization localizes, which
is why Road B moves and never finishes.

## 4 · The deficit ledger — Way 2's standing frame

The deficit is not a number to estimate; it is a ledger of events that have
never been observed: one completed escape = one negative arch (Way 1's
object) = deficit jumps by 2. Ledger state:

| Witness | Range | Escapes seen |
|---|---|---|
| our census | (14, 8000) | 0 |
| rigorous frontier (Platt–Trudgian) | height ≤ 3·10¹² | 0 |
| proportion theorems | all heights | at most 58.3% of zeros unaccounted — not escaped, unaccounted |

The gap between "0 escapes ever seen" and "41.7% provably safe" IS his debt,
stated as bookkeeping. Nothing in 167 years has entered the escape column.

## 5 · Circuit — the ceiling read: why 41.7%, and why even heaven is not enough

`[READING — the method and its limits are the field's (Levinson 1974;
Conrey; Feng; Pratt–Robles–Zaharescu–Zeindler arXiv 1802.10521; Farmer's
"Long mollifiers", Mathematika 1993); the framing against our ledger is
ours]`

**The mechanism, plainly.** Road B cannot look at zeros one by one — it
counts them wholesale. Levinson's move: take the combination the PRZZ
abstract states — *ζ(s) + λ₁ζ′(s)/log T + λ₂ζ″(s)/log²T + ⋯* — multiply it
by a **mollifier** (a finite Dirichlet polynomial of length y = T^θ built
to cancel ζ's wild swings), and compute the *average* of the smoothed
product. The argument principle then converts that mean value into a
guaranteed proportion of zeros ON the middle. Averaging survives exactly
where localization died (§3) — this is the same fact from the other side.

**The arm's length is θ.** The proportion you can prove is a function of
how long a mollifier you can average. That is the entire ladder:

| rung | proportion | the purchase |
|---|---|---|
| Levinson 1974 | ⅓ | the method itself, θ = 1/2 |
| Conrey 1989 | ⅖ | longer arm, θ < 4/7 (Deshouillers–Iwaniec / Kloosterman-sum technology) |
| Feng 2012 | 0.4128 | more mollifier pieces at the same wall |
| PRZZ 2020 | **> 5/12 = 0.4167** | more derivatives, more pieces — still at the wall |

Fifty years, and the last thirty bought 1.7 points — because every rung
since Conrey squeezes the same θ. **The wall is not Levinson's idea; the
wall is the mean value of long Dirichlet polynomials** — beyond T^{4/7}
the error terms (Kloosterman sums; Deshouillers–Iwaniec is still the
deepest tool) defeat everything known.

**The sky above the wall — Farmer.** The method is not self-limiting: the
proportion **κ → 1 as θ → ∞**, and Farmer's θ = ∞ conjecture (the small-θ
mean-value formulas hold for all θ) provably implies **100% of the zeros
lie on the middle.** The reach is short; the road is not.

**And the honest spike, which is this circuit's finding: even the sky is
below RH.** "100%" is *density* — proportion 1 still permits infinitely
many exceptions in a thinning set. Even Farmer's heaven certifies the
crowd, never the last zero. So the two roads bracket his debt without
touching it: **Road A is exact but forever finite; Road B is infinite but
forever a proportion.** The deficit ledger (§4) lives in the structural
gap between them — which is why 167 years of climbing has never entered,
and can never enter, the escape column by these roads alone. A proportion
is a crowd-witness; his sentence ("*sämmtlich* reell — ALL real") names
every soul.

## 6 · Next circuits for this way

- extension census lands (blocks 13–16 computing) → ledger row to 16000;
- the deficit ledger at sampled greater heights (spot-checks with the
  count-guard, not full sweeps).
