# N₀(T) — the new Point Zero: his count holds, his mechanism doesn't

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

## 3. HALT — measured at the points where it should be strongest

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

## 4. The census — and a correction to §3's reading

The direct count, run to T = 1000. Real roots by sign-change census of Z, against
mpmath's independent `nzeros` for the strip:

```
      T   theta(T)/pi+1   N(T) strip   N_0(T) line   N-N_0    N_0/N
     50           9.423           10            10       0   1.0000
    100          29.002           29            29       0   1.0000
    200          79.193           79            79       0   1.0000
    400         201.639          202           202       0   1.0000
    700         414.557          414           414       0   1.0000
   1000         648.616          649           649       0   1.0000
```

Two independent methods, same number at every checkpoint — the census is sound.
And N − N₀ = 0 throughout, as expected in a range where RH is long verified.

Now the heuristic against the truth. Counting sign changes of the **n = 1 term
alone**, 2cos(θ(t)), against the full Z:

```
   T=100    full Z: 29     n=1 term alone: 29     (from t=7 or t=14)
   T=100    full Z: 29     n=1 term alone: 30     (from t=0.5 — artifact)
```

The extra crossing from t = 0.5 is a **start-of-range artifact**: θ(t) has a
minimum near t ≈ 6.29 (θ = −3.531) and cos θ turns there, while Z does not. Begun
above it, the counts agree exactly.

**So the n = 1 term predicts the count exactly, at every T tested, to 1000.**

### The correction

An earlier draft of this file said: *S(T) is unbounded, Gram's law therefore fails
almost always, therefore the instrument that produced the claim provably cannot
produce the proof.* **The first two clauses are right. The third does not follow,
and the data above shows it doesn't.**

Gram's law fails at 3.40% of Gram points by T = 1000 — and the count is still
exactly right. **A Gram's law violation redistributes zeros between intervals
without losing any**: two land in one Gram interval, none in the next, and the
tally survives. What the unboundedness of S(T) kills is the **localization**
argument — one zero per Gram interval — not the count itself.

That distinction matters, and it makes the situation more interesting rather than
less:

> **Riemann's answer holds exactly throughout the computable range, while the only
> visible mechanism for it is already breaking.**

That is the signature of a genuinely deep problem, and it explains the shape of
the field's response. Levinson and Conrey do not localize — they **average**
(mollify), because averaging survives where localization does not. They are not
repairing Riemann's argument; they are routing around the exact thing that dies.

## 5. What this is worth saying plainly

**Riemann's claim is not in doubt in any range anyone can compute. His mechanism
is.** The gap between "the count is exactly right" and "no localization argument
can establish it" *is* the open problem, stated in his own object.

Do not spend effort trying to make the one-zero-per-Gram-interval argument work:
S(T) unbounded is a proof that it cannot. But that is a much narrower verdict
than "his road ends", which is what this file said before the census came back.

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

*Status: census complete (1415s). Its result forced the correction in §4 — the
finding this file opened with did not survive its own data, and the file now says
so rather than being quietly rewritten.*
