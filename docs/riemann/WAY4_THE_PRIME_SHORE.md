# WAY 4, first circuit — the prime shore: his actual count, run

The fourth loop of the hub, opened at the owner's rule (*"we had 3 now must
be 4 minimum"*), chartered by Riemann himself on leaf 26r: he wanted his
formula in the hands of **practical calculators**, so one would run **"eine
wirkliche Zählung der Primzahlen"** — an actual count — and compare it with
the laws his formula states. This circuit is that count.

Ways 1–3 watch the zeros. This way stands on the other shore: **the primes
themselves**, exactly sieved, no zeta machinery in the measurement. If the
middle (the half) is real, it must be visible from here — as an **exponent**.

---

## 1. The count

Sieve of Eratosthenes to 10⁸, exact:

| Control | Result |
|---|---|
| π(10⁸) from our sieve | **5,761,455** |
| π(10⁸), known value | 5,761,455 — **exact match** |

5.76 million primes, counted, not estimated. Errors measured at 60 log-spaced
points, two classical error functions:

- **π(x) − Li(x)** — the count against Gauss's logarithmic integral
- **ψ(x) − x** — Chebyshev's weighted count against x (the textbook object:
  under RH its size is bounded by √x·log²x/8π — Schoenfeld)

```
      x          pi(x)      pi-Li      psi-x    (psi-x)/sqrt(x)
     1,000          168       -9.6       -3.3      -0.105
    10,397        1,273      -16.1       27.1      +0.266
   108,118       10,285      -47.5      -51.1      -0.156
 1,124,210       87,466     -113.5     -119.7      -0.113
11,689,518      768,976     -246.2     +328.4      +0.096
37,693,909    2,301,503     -548.1    -1975.5      -0.322
```

## 2. The half, seen from this shore

Two measurements, and their honest reading:

**The ratio stays bounded.** |ψ(x) − x| / √x over the whole sampled range:
maximum **0.51**, oscillating in sign, no drift. If a zero stood off the
middle at real part Θ > ½, this ratio would **grow like x^(Θ−½)** — it does
not grow at all. That is the half's signature in raw prime data.

**The raw exponent fit reads 0.574** — and this number must be read
correctly, not triumphantly. The fit of log|ψ−x| against log x over a finite
oscillating signal carries two honest inflations: the error's known log
factors (under RH the envelope is √x·log²x, whose *local* slope at these
heights is ≈ 0.5 + 2/ln x ≈ 0.6), and the oscillation itself (dips near sign
changes distort the regression). The discriminating measurement is the
bounded ratio above, not the raw slope. A true Θ = 0.574 zero would make
|E|/√x drift upward by a factor ~x^0.074 ≈ 2.3 across our range — the data
shows a flat band instead.

**Verdict of the shore:** the half holds in the primes as far as this count
reaches. Same clause as every circuit: a measured range is a middle, never an
end.

## 3. His formula against his requested count — the comparison he asked for

The explicit formula, with **our own 1000 computed roots** (the same roots
from the periodic-terms execution), against the exact sieve:

| x | actual π(x) | his formula (1000 waves) | error |
|---|---|---|---|
| 10⁶ | 78,498 | 78,500.65 | +2.65 |
| 10⁷ | 664,579 | 664,580.72 | +1.72 |
| 10⁸ | 5,761,455 | 5,761,433.87 | −21.13 |

**A thousand waves land within 21 of 5.76 million** — relative error
4×10⁻⁶ — and the growth of the error with x at fixed root count is the
expected truncation behaviour, not a failure: larger x needs more waves,
exactly as his letter's framing implies (track the *einzelnen* periodic
terms — each term carries a share of the count).

This table is, as literally as we can make it, the comparison Riemann asked
an unknown future calculator to perform: **the actual count against the laws
of his formula.** The laws hold.

## 4. Returned to the hub

- Charter executed: the count run, the comparison made, the formula's laws
  confirmed at the 4×10⁻⁶ level with 1000 waves.
- The half is visible from the prime shore as a bounded ratio — the middle's
  fingerprint in data that never touches ζ.
- The raw-slope caveat is recorded so no future circuit mistakes a log
  factor for an off-middle zero.

Instruments archived: `way4_primeshore.py`, results in `way4_results.json`.
