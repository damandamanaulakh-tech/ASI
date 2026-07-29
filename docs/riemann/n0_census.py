"""N_0(T) — Riemann's own first named debt, and the heuristic behind it.

His letter: "dass zwischen 0 und T etwa (T/2pi)log(T/2pi) - T/2pi REELLE Wurzeln
der Gleichung xi(a)=0 liegen".  Real roots. Zeros ON the line, not in the strip.
The strip count is proved. This one is open.

Siegel, 1932: "Riemann has probably been guided by a heuristic consideration of
the asymptotic series."  This reconstructs that heuristic and measures where it
breaks, using only what Riemann had.

  Z(t) = e^{i theta(t)} zeta(1/2 + it)   is REAL for real t, so the real zeros
  of xi are exactly the sign changes of Z.

  The asymptotic series (the thing Distel found and Siegel worked out):
      Z(t) = 2 * SUM_{n <= sqrt(t/2pi)} n^{-1/2} cos(theta(t) - t log n) + R

  THE HEURISTIC: keep only n = 1.  Then Z(t) ~ 2 cos(theta(t)), whose sign
  changes are counted exactly by theta(T)/pi.  And theta(T)/pi IS
  (T/2pi)log(T/2pi) - T/2pi to leading order.

  So Riemann's claim is: THE n=1 TERM DOMINATES, and the n>=2 terms perturb the
  wave without destroying its sign changes.  That is the whole content, and it
  is exactly what nobody has proved.

So the question becomes measurable: how often do the higher terms actually eat a
sign change?  Each failure is a Gram-block anomaly.  This counts them.
"""
import json
import time

import mpmath as mp

mp.mp.dps = 15
T_MAX = 1000.0
t0 = time.time()


def theta(t):
    return mp.siegeltheta(t)


def Z(t):
    return mp.siegelz(t)


# ---------- 1. the three counts ----------------------------------------------
print("=" * 92)
print("1. THREE COUNTS OF THE SAME STRETCH — his formula, the strip, the line")
print("=" * 92)
print(f"{'T':>7} {'theta(T)/pi+1':>15} {'N(T) strip':>12} {'N_0(T) line':>13} "
      f"{'N-N_0':>7} {'N_0/N':>8}")
print("-" * 92)


def count_sign_changes(a, b, step):
    """Real zeros of xi = sign changes of Z. Nothing cleverer; his own object."""
    n = 0
    t = a
    prev = mp.sign(Z(t))
    xs = []
    while t < b:
        t += step
        s = mp.sign(Z(t))
        if s != prev and s != 0:
            n += 1
            xs.append(float(t))
            prev = s
        elif s != 0:
            prev = s
    return n, xs


rows = []
for T in (50, 100, 200, 400, 700, 1000):
    predicted = float(theta(T) / mp.pi) + 1
    strip = int(mp.nzeros(T))
    line, _ = count_sign_changes(0.5, T, 0.02)
    rows.append({"T": T, "riemann": predicted, "N": strip, "N0": line})
    print(f"{T:>7} {predicted:>15.3f} {strip:>12} {line:>13} "
          f"{strip - line:>7} {line/max(strip,1):>8.4f}")
    print(f"        ({time.time()-t0:.0f}s)", flush=True)

# ---------- 2. the heuristic itself ------------------------------------------
print()
print("=" * 92)
print("2. THE HEURISTIC — does the n=1 term alone already carry the count?")
print("=" * 92)
print("   2 cos(theta(t)) changes sign exactly theta(T)/pi times. If Riemann's")
print("   claim holds, the full Z has the same number. Where it doesn't, a")
print("   higher term ate a sign change.\n")


def first_term(t):
    return 2 * mp.cos(theta(t))


for T in (100, 300, 1000):
    n1, _ = count_sign_changes(0.5, T, 0.02)
    # sign changes of the n=1 term alone
    n2 = 0
    t = 0.5
    prev = mp.sign(first_term(t))
    while t < T:
        t += 0.02
        s = mp.sign(first_term(t))
        if s != prev and s != 0:
            n2 += 1
        if s != 0:
            prev = s
    print(f"   T={T:<6} full Z: {n1:<6} sign changes    n=1 term alone: {n2:<6}"
          f"    difference: {n1-n2:+d}")

# ---------- 3. where the wave nearly dies ------------------------------------
print()
print("=" * 92)
print("3. WHERE THE HEURISTIC IS CLOSEST TO FAILING")
print("=" * 92)
print("   Gram points g_n solve theta(g_n) = n*pi. At a Gram point the n=1 term")
print("   is at its extreme, |2 cos theta| = 2, so Z should be far from zero and")
print("   should alternate in sign. Gram's law = it does. Each violation is a")
print("   place the higher terms nearly won.\n")


def gram(n):
    """g_n: theta(g_n) = n*pi."""
    return mp.findroot(lambda t: theta(t) - n * mp.pi, mp.mpf(2 * mp.pi) * mp.e
                       ** (1 + mp.lambertw((8 * n + 1) / (8 * mp.e))))


viol = []
gvals = []
n = 0
g = None
while True:
    try:
        g = gram(n)
    except Exception:
        n += 1
        continue
    if float(g) > T_MAX:
        break
    z = Z(g)
    expect = 1 if n % 2 == 0 else -1        # (-1)^n Z(g_n) > 0 is Gram's law
    ok = (float(z) * expect) > 0
    gvals.append({"n": n, "g": float(g), "Z": float(z), "ok": ok})
    if not ok:
        viol.append({"n": n, "g": float(g), "Z": float(z)})
    n += 1

print(f"   Gram points below T={T_MAX:.0f}: {len(gvals)}")
print(f"   Gram's law violations:          {len(viol)}"
      f"   ({100*len(viol)/max(len(gvals),1):.2f}%)")
if viol:
    print("\n   first violations — the wave nearly lost a sign change here:")
    for v in viol[:12]:
        print(f"      n={v['n']:<5} g={v['g']:>10.4f}   Z(g)={v['Z']:>+10.5f}")

json.dump({"counts": rows, "gram_total": len(gvals),
           "gram_violations": viol}, open("n0_results.json", "w"), indent=1)
print(f"\nDONE {time.time()-t0:.0f}s")
