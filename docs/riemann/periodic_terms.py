"""RIEMANN'S UNEXECUTED INSTRUCTION, CARRIED OUT.

  "Bei einer etwaigen neuen Zaehlung wuerde es interessant sein, den Einfluss
   der einzelnen in dem Ausdrucke fuer die Dichtigkeit der Primzahlen
   enthaltenen periodischen Glieder zu verfolgen."
  — closing lines of the printed paper; identical in the 1876 and 1892
    editions of the Gesammelte Werke (verified against both full texts).
    NOTE: "etwaigen" = "should there ever be one". The instruction is
    conditional, not a commission — and the terms are the ones CONTAINED IN
    the expression for the density, which is what is computed below.

His own formula, nothing modern imported:

  f(x) = Li(x) - SUM_alpha [ Li(x^(1/2+alpha i)) + Li(x^(1/2-alpha i)) ]
                + INT_x^inf dt/(t(t^2-1) log t) + log xi(0)      [log xi(0) = -log 2]

  F(x) = SUM_m  mu(m)/m  f(x^(1/m))          (his own inversion)

Each root alpha gives ONE periodic term. We track each one separately:
its frequency, its wavelength in x, its amplitude, and its actual influence.
"""
import mpmath as mp

mp.mp.dps = 30
NROOTS = 50

print("=" * 96)
print("THE INDIVIDUAL PERIODIC TERMS — each root's own wave")
print("=" * 96)

roots = [mp.im(mp.zetazero(n)) for n in range(1, NROOTS + 1)]


def osc_term(alpha, x):
    """One periodic term of Riemann's f(x): -2 Re Ei(rho log x), rho = 1/2 + i*alpha."""
    rho = mp.mpf('0.5') + 1j * alpha
    return -2 * mp.re(mp.ei(rho * mp.log(x)))


def f_riemann(x, n_roots):
    """Riemann's f(x) with the first n_roots periodic terms."""
    tot = mp.li(x)
    for a in roots[:n_roots]:
        tot += osc_term(a, x)
    tot += mp.quad(lambda t: 1 / (t * (t * t - 1) * mp.log(t)), [x, mp.inf])
    tot -= mp.log(2)
    return tot


def mobius(n):
    if n == 1:
        return 1
    f, d, cnt = n, 2, 0
    while d * d <= f:
        if f % d == 0:
            f //= d
            if f % d == 0:
                return 0
            cnt += 1
        else:
            d += 1
    if f > 1:
        cnt += 1
    return -1 if cnt % 2 else 1


def pi_riemann(x, n_roots, mmax=12):
    """His F(x) = sum mu(m)/m f(x^(1/m))."""
    tot = mp.mpf(0)
    for m in range(1, mmax + 1):
        mu = mobius(m)
        if mu and x ** (1.0 / m) >= 2:
            tot += mp.mpf(mu) / m * f_riemann(mp.power(x, mp.mpf(1) / m), n_roots)
    return tot


# ---------- 1. EACH TERM'S OWN IDENTITY ----------
print("\n1. EACH PERIODIC TERM — its frequency and wave, as Riemann's formula defines it")
print("   His density term:  2 cos(alpha log x) x^(-1/2) / log x\n")
print(f"{'k':>3} {'alpha_k (frequency)':>22} {'period in log x':>17} "
      f"{'wavelength at x=1e6':>21} {'influence on pi(1e6)':>21}")
print("-" * 96)
X = mp.mpf(10) ** 6
for k, a in enumerate(roots[:20], 1):
    period_logx = 2 * mp.pi / a
    wavelength = X * (mp.e ** period_logx - 1)
    infl = osc_term(a, X)
    print(f"{k:>3} {mp.nstr(a, 12):>22} {mp.nstr(period_logx, 6):>17} "
          f"{mp.nstr(wavelength, 6):>21} {mp.nstr(infl, 8):>21}")

# ---------- 2. THE MUSIC CONVERGING ----------
print("\n\n2. THE HARMONICS AT WORK — adding one term at a time, does it reach the true count?")
for x, true_pi in [(100, 25), (1000, 168), (10000, 1229), (100000, 9592), (1000000, 78498)]:
    print(f"\n   x = {x:>9,}   true pi(x) = {true_pi:,}")
    li_only = mp.li(x)
    print(f"      Li(x) alone, no waves        {mp.nstr(li_only, 10):>16}"
          f"   error {mp.nstr(li_only - true_pi, 6):>12}")
    for n in [0, 1, 5, 20, 50]:
        est = pi_riemann(mp.mpf(x), n)
        print(f"      + first {n:>2} periodic terms      {mp.nstr(est, 10):>16}"
              f"   error {mp.nstr(est - true_pi, 6):>12}")

# ---------- 3. THE INFLUENCE OF EACH TERM, SEPARATELY ----------
print("\n\n3. THE INFLUENCE OF EACH INDIVIDUAL TERM — his exact words, at several magnitudes")
print(f"{'k':>3} " + "".join(f"{'x=' + str(10**e):>16}" for e in [2, 3, 4, 6, 8]))
print("-" * 96)
for k, a in enumerate(roots[:15], 1):
    row = f"{k:>3} "
    for e in [2, 3, 4, 6, 8]:
        row += f"{mp.nstr(osc_term(a, mp.mpf(10) ** e), 6):>16}"
    print(row)

# ---------- 4. DAMPING TEST — is every wave damped alike? ----------
print("\n\n4. THE DAMPING — RH's actual content: does every wave decay at the same rate?")
print("   amplitude of term k at x, divided by x^(1/2)/log x  (should be ~constant if all roots real)")
print(f"{'k':>3} {'alpha':>14}" + "".join(f"{'x=1e' + str(e):>14}" for e in [4, 6, 8, 10]))
print("-" * 96)
for k, a in enumerate(roots[:10], 1):
    row = f"{k:>3} {mp.nstr(a, 8):>14}"
    for e in [4, 6, 8, 10]:
        x = mp.mpf(10) ** e
        amp = abs(osc_term(a, x)) / (mp.sqrt(x) / mp.log(x))
        row += f"{mp.nstr(amp, 5):>14}"
    print(row)
print("\n   (constant across x  =  every harmonic damped by exactly x^(-1/2)  =  what he called")
print("    'alle Wurzeln reell'.  A root off the line would show a column that GROWS.)")
