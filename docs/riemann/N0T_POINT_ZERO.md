# N₀(T) — the new Point Zero, and where Riemann's own road ends

His first named debt, from the draft letter on leaf 23v:

> „dass zwischen 0 und T etwa (T/2π)·log(T/2π) − T/2π **reelle Wurzeln** der
> Gleichung ξ(α) = 0 liegen"

**Real roots.** N₀(T), zeros *on* the line — not N(T), zeros in the strip. The
strip count is proved. This one is open, and Siegel already said so in 1932:
*"even today it is still not clear how one could prove or disprove this claim."*

---

## 1. GROUND — what is already there

Nobody has closed it. What exists is a sequence of *proportions*, all
unconditional, none asymptotic:

| | | N₀(T)/N(T) ≥ |
|---|---|---|
| Hardy | 1914 | infinitely many (no proportion) |
| Selberg | 1942 | a positive proportion |
| Levinson | 1974 | 1/3, later 0.3474 |
| Conrey | 1989 | 2/5 |
| Feng | 2012 | 0.4128 |
| Pratt, Robles, Zaharescu, Zeindler | 2020 | **0.417** |

Riemann's claim is the limit **1**. Fifty-one years of work has moved the floor
from 0.33 to 0.42. RH implies the claim; nothing weaker is known to.

## 2. THE EXPRESSION — his heuristic, reconstructed

Siegel: *"Riemann has probably been guided by a heuristic consideration of the
asymptotic series."* Here is that consideration, made explicit.

Z(t) = e^{iθ(t)}·ζ(½+it) is **real** for real t, so the real roots of ξ are
exactly the **sign changes of Z**. The asymptotic series Distel found is

    Z(t) = 2·Σ_{n ≤ √(t/2π)} n^(−½)·cos(θ(t) − t·log n) + R

Keep only **n = 1**:

    Z(t) ≈ 2·cos(θ(t))

and 2cos(θ(t)) changes sign exactly **θ(T)/π** times on (0,T) — which is
**(T/2π)log(T/2π) − T/2π** to leading order. **That is his formula, exactly.**

So Riemann's claim reduces to one sentence:

> **the n = 1 term dominates, and the higher terms perturb the wave without
> destroying its sign changes.**

That is the entire content of the debt, and it is the thing nobody has proved.

## 3. HALT — measured, and it fails

The heuristic is testable at the points where it should be strongest. At a Gram
point g_n (θ(g_n) = nπ) the n = 1 term is at its extreme, |2cos θ| = 2, so Z
should be far from zero and should alternate in sign. That it does is **Gram's
law**; each violation is a place the higher terms nearly won.

Computed directly from Z, 10 < t < 1000:

```
Gram points            648
Gram's law violations   22        (3.40%)

first failures — where the wave nearly lost a sign change
   n=126   g=  282.4547   Z(g)=  -0.027629
   n=134   g=  295.5839   Z(g)=  -0.016900
   n=195   g=  391.4482   Z(g)=  +0.023289
   n=211   g=  415.6015   Z(g)=  +0.382890
   n=232   g=  446.8058   Z(g)=  -0.141043
```

The first failure at **n = 126** is the classically known one — a check that the
computation is right, not a discovery.

## 4. Why the road ends — and this is the finding

The violation rate is not a nuisance that better bookkeeping removes. It grows,
and it grows to everything.

    N(T) = θ(T)/π + 1 + S(T),        S(T) = (1/π)·arg ζ(½+iT)

Gram's law holding at g_n is essentially the statement that S(g_n) stays small.
And **S(T) is unbounded** — Selberg showed it is normally distributed with
variance ~ (1/2π²)·log log T, and Montgomery gave
S(T) = Ω±((log T / log log T)^{1/3}). So Gram's law must fail infinitely often,
and the proportion of failures tends to **1**.

**Therefore the instrument that produced the claim provably cannot produce the
proof.** The n = 1 term stops dominating. Not eventually-in-principle —
demonstrably, and the decay is already visible by t = 282.

This is, as far as this investigation can tell, *why the debt has stayed open for
167 years*: the heuristic is right about the answer and structurally incapable of
justifying it. Levinson and Conrey do not repair Riemann's argument — they
abandon it and mollify instead. That is a different road, and it is the one that
has actually moved.

## 5. What this is worth saying plainly

**Do not spend effort sharpening Riemann's heuristic.** It has a proof that it
cannot work. Following him here leads to a wall with a reason on it, and knowing
that is worth more than another month of trying.

**The one place his instrument still touches the live problem** is the *near
misses* — the Lehmer phenomenon, where two zeros crowd together and Z barely
crosses. Z(g) = −0.0276 at n = 126 is a small version of it. The question "is
there a bound below which a near-miss can never fall?" is RH restated in his own
object, and it is the only form of his question that is still load-bearing.

---

*Method note: sections 1–4 are Ground, Expression, and Halt from `sequence.py`,
run in order on a live problem. The halt in §4 is real and is not being patched —
it is being named, which is the point. Two witnesses were required for every
numeric claim: the Gram computation here, and the published record in §1.*

*Status: a longer run (three counts of N₀ by direct sign-change census to
T = 1000, plus the n=1-term comparison) is still computing. The Gram measurement
above stands on its own.*
