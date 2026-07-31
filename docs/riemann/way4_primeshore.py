"""WAY 4 — THE PRIME SHORE: Riemann's "wirkliche Zaehlung", executed.

His charter, leaf 26r, his hand: it matters to him that his formula reach
"praktische Rechner", so that one of them would undertake "eine wirkliche
Zaehlung der Primzahlen" and compare the results against the laws his formula
states. We are that calculator.

Ways 1-3 live on the zero shore. This way stands on the prime shore and asks:
is the HALF visible from here? Under RH the error of the prime count grows
like x^(1/2) (times logs) — the middle of the strip appears as an EXPONENT in
raw prime data. Off-line zeros at real part Theta > 1/2 would push the
exponent up to Theta. So: sieve the primes exactly, measure the errors,
fit the exponent.

  1. exact sieve to 10^8  (5,761,455 primes)
  2. pi(x) and psi(x) (Chebyshev: sum of log p over prime powers) exactly
     at log-spaced samples
  3. errors pi(x) - Li(x) and psi(x) - x; the exponent fit
     log|psi(x) - x| vs log x  ->  slope should sit near 1/2, never drift up
  4. his own formula (explicit formula with OUR 1000 computed roots) against
     the exact counts at x = 10^6, 10^7, 10^8
"""
import json
import math
import time

import numpy as np

t0 = time.time()
N = 100_000_000

# ---------- 1. sieve ----------
sieve = np.ones(N + 1, dtype=bool)
sieve[:2] = False
for p in range(2, int(N ** 0.5) + 1):
    if sieve[p]:
        sieve[p * p:: p] = False
primes = np.flatnonzero(sieve).astype(np.int64)
del sieve
print(f"sieve to 1e8: {len(primes)} primes   [{time.time()-t0:.0f}s]", flush=True)

logs = np.log(primes.astype(np.float64))
cumlog = np.cumsum(logs)                      # theta(x) lookup


def pi_of(x):
    return int(np.searchsorted(primes, x, side="right"))


def theta_of(x):
    i = np.searchsorted(primes, x, side="right")
    return float(cumlog[i - 1]) if i else 0.0


def psi_of(x):
    s, k = 0.0, 1
    while True:
        r = x ** (1.0 / k)
        if r < 2:
            break
        s += theta_of(r)
        k += 1
    return s


def Li(x):
    import mpmath as mp
    mp.mp.dps = 20
    return float(mp.li(x, offset=True) + mp.li(2))   # standard Li from 0; li(x)


# ---------- 2. samples & errors ----------
import mpmath as mp
mp.mp.dps = 20
samples = np.unique(np.logspace(math.log10(1e3), math.log10(N), 60).astype(np.int64))
rows = []
for x in samples:
    pi_x = pi_of(x)
    li_x = float(mp.li(x))
    psi_x = psi_of(float(x))
    e_pi = pi_x - li_x
    e_psi = psi_x - float(x)
    rows.append({"x": int(x), "pi": pi_x, "li": li_x, "e_pi": e_pi,
                 "psi": psi_x, "e_psi": e_psi,
                 "e_psi_over_sqrt": e_psi / math.sqrt(x)})
print(f"samples computed   [{time.time()-t0:.0f}s]", flush=True)

print("\n  x            pi(x)        pi-Li         psi-x      (psi-x)/sqrt(x)")
for r in rows[::6]:
    print(f"  {r['x']:>11,} {r['pi']:>12,} {r['e_pi']:>12.1f} {r['e_psi']:>13.1f} "
          f"{r['e_psi_over_sqrt']:>12.4f}")

# ---------- 3. the exponent — the half, seen from the prime shore ----------
fit = [(math.log(r["x"]), math.log(abs(r["e_psi"])))
       for r in rows if r["x"] >= 10_000 and abs(r["e_psi"]) > 1e-9]
n = len(fit)
mx = sum(a for a, _ in fit) / n
my = sum(b for _, b in fit) / n
slope = sum((a - mx) * (b - my) for a, b in fit) / sum((a - mx) ** 2 for a, _ in fit)
mx2 = max(abs(r["e_psi_over_sqrt"]) for r in rows if r["x"] >= 10_000)
print(f"\nEXPONENT FIT on log|psi(x)-x| vs log x  ({n} samples, x >= 1e4):")
print(f"  measured exponent = {slope:.4f}     (RH says: stays at 1/2; a zero off the")
print(f"  middle at real part Theta would drag it up toward Theta)")
print(f"  max |psi(x)-x|/sqrt(x) over samples = {mx2:.4f}  (bounded under RH)")

# ---------- 4. his formula, our 1000 roots, against the exact counts ----------
roots = json.load(open("roots1000.json"))
mp.mp.dps = 15


def term(a, x):
    rho = mp.mpf("0.5") + 1j * a
    return float(-2 * mp.re(mp.ei(rho * mp.log(x))))


def mobius(n):
    if n == 1:
        return 1
    f, d, c = n, 2, 0
    while d * d <= f:
        if f % d == 0:
            f //= d
            if f % d == 0:
                return 0
            c += 1
        else:
            d += 1
    if f > 1:
        c += 1
    return -1 if c % 2 else 1


def f_r(x, nr):
    t = mp.li(x)
    for a in roots[:nr]:
        t += term(a, x)
    t += mp.quad(lambda u: 1 / (u * (u * u - 1) * mp.log(u)), [x, mp.inf]) - mp.log(2)
    return t


def pi_riemann(x, nr):
    s = mp.mpf(0)
    for m in range(1, 13):
        mu = mobius(m)
        if mu and float(x) ** (1.0 / m) >= 2:
            s += mp.mpf(mu) / m * f_r(mp.power(x, mp.mpf(1) / m), nr)
    return float(s)


print(f"\nHIS FORMULA (1000 periodic terms, OUR computed roots) vs THE ACTUAL COUNT:")
print(f"  {'x':>11}  {'actual pi(x)':>13}  {'his formula':>14}  {'error':>8}")
for e in (6, 7, 8):
    x = 10 ** e
    est = pi_riemann(mp.mpf(x), 1000)
    act = pi_of(x)
    print(f"  {x:>11,}  {act:>13,}  {est:>14.2f}  {est-act:>+8.2f}", flush=True)

json.dump({"n_primes": int(len(primes)), "rows": rows, "exponent": slope,
           "max_e_psi_over_sqrt": mx2},
          open("way4_results.json", "w"), indent=1)
print(f"\nDONE {time.time()-t0:.0f}s", flush=True)
