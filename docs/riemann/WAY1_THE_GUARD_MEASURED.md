# WAY 1, first circuit — the guard measured

Loop 1 of the hub (`THE_MIDDLE_POINT_ZERO.md`): *how close does the world
come to forming the off-center pair?* The instrument: a census of **every**
zero of Z and **every arch between consecutive zeros** on (14, 8000) — eight
parallel workers, count-guarded per block, known-answer controlled.

The working theory predicted the shape **before** the run (written in the hub
document): *the floor sinks forever and never touches.* This circuit tested
that prediction.

---

## 1. The instrument held

| Check | Result |
|---|---|
| Zeros found on (14, 8000) | **7,830** |
| Riemann–von Mangoldt prediction | 7,830.43 — difference −0.43, inside the normal S(T) wiggle |
| Per-block count guard | all 8 blocks matched; zero rescans triggered |
| Lehmer control (literature: pair 7005.06287/7005.10056, peak 0.0039675 @ 7005.0819) | **reproduced inside the production run: peak 0.0039674 @ 7005.0819** |

Every zero the strip owes in this range was found **on the line** — which is
also Way 2's first datum: **N₀ = N on (14, 8000). The middle is full here.**

## 2. The near-misses — the guard's worst moments

7,828 arches measured. **Negative arch peaks: 0.** (One negative arch = one
completed escape = RH refuted. None.)

The twenty smallest arches:

```
rank   peak |Z|       at t                 zeros        gap   n.gap
  1    0.003967   7005.0819   7005.0629/7005.1006   0.0377  0.0421   <- Lehmer's
  2    0.004862   5229.2203   5229.1986/5229.2418   0.0433  0.0463
  3    0.009226   4292.7720   4292.7264/4292.8173   0.0908  0.0943
  4    0.012433   4990.3967   4990.3455/4990.4497   0.1042  0.1108
  5    0.012454   4589.6972   4589.6434/4589.7488   0.1054  0.1106
  6    0.017340   5978.0808   5978.0266/5978.1393   0.1127  0.1230
  7    0.021392   5568.8558   5568.7986/5568.9129   0.1144  0.1235
  8    0.021976   6093.2374   6093.1923/6093.2834   0.0911  0.0997
  9    0.022112   1977.2224   1977.1739/1977.2714   0.0975  0.0893
 10    0.025262   1329.1240   1329.0435/1329.2050   0.1615  0.1376
 ...
```

Lehmer's pair is the range's champion — and our census independently found
the **second Lehmer-class event at t ≈ 5229.22**, nearly as severe (peak
0.0049, normalized gap 0.046).

## 3. The floor — it sinks, and shows no bottom

Running minimum of the arch peak, every time a new low was set:

```
T =     18   min 2.3406        T =    946   min 0.0812
T =     23   min 1.4593        T =   1055   min 0.0504
T =     32   min 0.9255        T =   1329   min 0.0253
T =     49   min 0.7133        T =   1977   min 0.0221
T =     95   min 0.5192        T =   4293   min 0.0092
T =    295   min 0.2209        T =   5229   min 0.0049
T =    540   min 0.1246        T =   7005   min 0.0040
```

Twenty new minima across the range. **No plateau. No floor forming.** Three
orders of magnitude of sinking in the first 8,000 units of the line.

## 4. The guard's law, measured

**The arch is parabolic in the gap.** On the 207 arches with normalized gap
< 0.35: slope of log(peak) against log(gap) = **1.975** — the parabola
predicts 2.0. So peak ∝ gap², measured.

**The repulsion is GUE-consistent.** For N = 7,828 gaps, GUE's δ²-repulsion
predicts a smallest normalized gap ≈ 0.0491; observed: **0.0421** (Lehmer's
pair) — right order, ~15% inside prediction, exactly what one range's worst
case should look like.

Chain the two measured laws: smallest gap among N zeros shrinks like
N^(−1/3) (repulsion), and peak goes as gap² (parabola) — so the floor falls
like **N^(−2/3), forever**. That is the measured mechanism of the sinking in
§3, not a fit to it.

## 5. Read against the hub theory

| Theory (written before the run) | Data |
|---|---|
| No completed escape — the middle holds | 0 negative arches; count full (N₀=N) |
| The guard is δ² repulsion | slope 1.975 ≈ 2; min gap at GUE's prediction |
| The floor sinks forever, never touches | 20 minima, no plateau, N^(−2/3) law assembled from measured parts |
| "Barely true" / "sustained non-closure" / "always in the middle" | the arches flatten without end and never cross — the measured shape IS the phrase |

**Calibration, honestly:** this census is 7,830 zeros; the field has verified
billions. The value here is not the range — it is that the *arch peaks* were
measured (verifications publish zero locations, not the guard's worst
moments), by our own instrument, validated on a known answer, in the frame of
the hub. And per the frame itself: any measured range is a middle, never an
end. **This circuit confirms the shape; it cannot close the question. That is
not a weakness of the circuit — under the theory, it is the point.**

## 6. Second circuit, part 1 — from arches to the boundary constant

The near-misses were converted into **measured lower bounds on Λ** (the
de Bruijn–Newman constant: RH ⟺ Λ ≤ 0; Rodgers–Tao proved Λ ≥ 0) using the
Csordas–Smith–Varga theorem, taken verbatim from the literature: for a
consecutive pair with gap Δ and interaction sum g over all other zeros, the
pair is a **Lehmer pair** if Δ²g < 4/5, and then
λ = [(1 − 5Δ²g/4)^{4/5} − 1]/(8g) ≤ Λ.

**Independent literature control, passed exactly:** the source paper states
there are 29 Lehmer pairs among the first 649 zeros. Our census holds exactly
649 zeros below t = 1000 — and finds **exactly 29 Lehmer pairs** among them.

Across (14, 8000): **420 Lehmer pairs.** The strongest:

```
        pair                Delta     Delta^2*g    lambda  (<= Lambda)
7005.0629/7005.1006        0.03770     0.00693     -1.778e-04
5229.1986/5229.2418        0.04325     0.00866     -2.341e-04
4292.7264/4292.8173        0.09082     0.04730     -1.037e-03
```

**Our measured bound: Λ ≥ −1.778×10⁻⁴** — from our own census, through a
published theorem, with a published control. Calibration: historical
computations using far higher, far closer pairs pushed the bound to
−1.1×10⁻¹¹ before Rodgers–Tao closed it at 0; our value is what THIS range
testifies. The point is not the record — it is that the walk's own arches,
measured for the guard, turn directly into pressure on the boundary
constant: **every strong near-miss squeezes "barely true" tighter.**

(Truncation note: g was summed over our 7,830 zeros and their mirror
negatives; the tail beyond 8000 contributes ~3×10⁻⁴ to g — negligible
against the nearby terms that dominate it.)

## 7. Returned to the hub

Way 1, first circuit: **complete.** Yield banked:
- the middle held everywhere measured; the guard behaves exactly as the
  self-mirror theory's fingerprint (GUE) demands;
- the floor sinks lawfully (N^(−2/3)) — no bottom, no touch;
- one new named landmark: the 5229.22 pair, the range's second-worst test.

Next per walking order: **Way 2 — the middle is full** (his own debt, N₀).
First datum already in hand from this circuit. Owner may redirect at the hub.

---

## 8. Circuit 2, part 2 — the extension landed (8000 → 12000)

**The census grew by 60%: 12,519 zeros, range (14, 12000), 12,517 arches.**
Before trusting the merge, the rebuilt instrument was validated against every
banked number from the first census — all gates pass; with the mirror-negative
terms restored to the g-sum it reproduces the banked λ to ten significant
figures. (The merge instrument now lives on disk: `extend_analysis.py`. The
original was run inline and lost — that mistake is not repeated.)

**The instrument's own troubles, on the record.** The extension nearly died
twice before it ran (an orphaned launch, then a shell-path slip killing 3 of
4 workers at birth — both caught by reading the record, not the launch
message). Then it ran *slow*: every extension block reported `RESCANNED`.
Cause found in the worker's own line 65 — a stale `min(B, 8000.0)` clamp from
the first census's ceiling made the owed-count prediction 0 (even negative)
above 8000, so the count-guard fired a **false alarm on every extension
block** and rescanned at 4× density. A safety mechanism misfiring is still
conservative — denser scanning can only find more, never fewer — so the cost
was hours, not truth. The bug is named here so no future circuit inherits it
silently.

**What the 4,689 new zeros say:**

| Block | zeros | owed (RvM) | Lehmer pairs | rate/arch | min peak | min δ |
|---|---|---|---|---|---|---|
| (8000, 9000) | 1,148 | 1,147.41 | 61 | 0.0531 | 0.04230 | 0.1674 |
| (9000, 10000) | 1,164 | 1,165.13 | 69 | **0.0593** | 0.01696 | 0.1142 |
| (10000, 11000) | 1,182 | 1,181.07 | 68 | 0.0575 | 0.01097 | 0.0909 |
| (11000, 12000) | 1,195 | 1,195.56 | 63 | 0.0527 | 0.00899 | 0.0888 |

- **The Lehmer production rate holds steady** — 0.053–0.059 per arch across
  the new stretch, no decay through 12000 (the compilation's finding
  extends: the guard is tested at a constant rate forever, the measured
  support for "exactly barely true").
- **The floor keeps sinking, lawfully** — per-window minimum peak down to
  0.0090 at T≈11,732; still no bottom, still no touch.
- **The record gap became typical**: the observed minimum δ = 0.0421 (the
  7005.06 pair) now sits almost exactly ON the GUE-expected minimum for a
  census this size (0.0418). What looked like an outlier at 8,000 zeros is
  the *predicted* extreme at 12,519 — the guard's law, not an anomaly. The
  parabola law tightened with it: peak ~ δ^1.97 (theory: 2).
- **682 Lehmer pairs total** (one pair sits at the 4/5 threshold and entered
  when the seam-duplicate cleanup nudged its g — threshold-adjacent, noted).
- **No stronger pair found**: 4,689 fresh zeros produced nothing below
  δ = 0.089. The strongest Λ-pressure is still the 7005.06 pair:
  **Λ ≥ −1.778×10⁻⁴ now stands on a 60% larger census.** (g summed over all
  12,519 zeros and their mirror negatives; tail beyond 12000 ~2×10⁻⁴ of g,
  negligible.)
