"""1000 roots · full periodic-term census · damping measured by ENVELOPE not phase."""
import json, time
import mpmath as mp

mp.mp.dps = 15
N = 1000
t0 = time.time()

# ---------- get the roots ----------
roots = []
for n in range(1, N + 1):
    roots.append(float(mp.im(mp.zetazero(n))))
    if n % 50 == 0:
        print(f"  roots {n}/{N}   {time.time()-t0:.0f}s", flush=True)
json.dump(roots, open("roots1000.json", "w"))
print(f"ROOTS DONE {time.time()-t0:.0f}s   alpha_1000 = {roots[-1]:.6f}", flush=True)


def term(alpha, x):
    """One periodic term of Riemann's f(x)."""
    rho = mp.mpf('0.5') + 1j * alpha
    return float(-2 * mp.re(mp.ei(rho * mp.log(x))))


# ---------- A. ENVELOPE-BASED DAMPING TEST ----------
# term_k(x) ~ -(2 x^sigma / (|rho| log x)) * cos(alpha log x - arg rho)
# so the ENVELOPE is  2 x^sigma / (|rho| log x).  Measure the true max over one
# full period in log x, then divide by the sigma=1/2 prediction. Constant ~1.0
# means that root is damped exactly as x^(1/2). A root at sigma>1/2 would grow.
print("\n=== A. DAMPING BY ENVELOPE (max over one full period, not a point sample) ===", flush=True)
damp = {}
for k in [1, 2, 3, 5, 10, 25, 50, 100, 250, 500, 1000]:
    a = roots[k - 1]
    rho_abs = (0.25 + a * a) ** 0.5
    row = []
    for e in [4, 6, 8, 10, 12, 14]:
        L0 = mp.log(mp.mpf(10) ** e)
        period = 2 * mp.pi / a
        # scan one full period in log x, find the true peak of |term|
        peak = max(abs(term(a, mp.e ** (L0 + period * mp.mpf(j) / 240)))
                   for j in range(240))
        x = mp.mpf(10) ** e
        predicted = float(2 * mp.sqrt(x) / (rho_abs * mp.log(x)))
        row.append(peak / predicted)
    damp[k] = row
    print(f"  k={k:>4} alpha={a:>11.5f}  " +
          "  ".join(f"1e{e}:{r:.4f}" for e, r in zip([4, 6, 8, 10, 12, 14], row)), flush=True)

# ---------- B. WHICH TERM GOVERNS WHICH STRETCH ----------
print("\n=== B. WHICH TERM GOVERNS WHICH STRETCH OF THE NUMBER LINE ===", flush=True)
govern = []
for e in range(2, 21):
    x = mp.mpf(10) ** e
    infl = [(abs(term(a, x)), i + 1, a) for i, a in enumerate(roots[:200])]
    infl.sort(reverse=True)
    top = infl[:3]
    govern.append({"x": f"1e{e}", "top": [[t[1], round(t[2], 4), round(t[0], 4)] for t in top]})
    print(f"  x=1e{e:<3} governed by  k={top[0][1]:<4}(a={top[0][2]:.3f}, |infl|={top[0][0]:.3f})"
          f"   then k={top[1][1]}, k={top[2][1]}", flush=True)

# ---------- C. CONVERGENCE WITH MANY TERMS ----------
print("\n=== C. THE COUNT REBUILT FROM THE MUSIC (more terms) ===", flush=True)


def mobius(n):
    if n == 1: return 1
    f, d, c = n, 2, 0
    while d * d <= f:
        if f % d == 0:
            f //= d
            if f % d == 0: return 0
            c += 1
        else: d += 1
    if f > 1: c += 1
    return -1 if c % 2 else 1


def f_r(x, nr):
    t = mp.li(x)
    for a in roots[:nr]:
        t += term(a, x)
    t += mp.quad(lambda u: 1 / (u * (u * u - 1) * mp.log(u)), [x, mp.inf]) - mp.log(2)
    return t


def pi_r(x, nr):
    s = mp.mpf(0)
    for m in range(1, 13):
        mu = mobius(m)
        if mu and float(x) ** (1.0 / m) >= 2:
            s += mp.mpf(mu) / m * f_r(mp.power(x, mp.mpf(1) / m), nr)
    return float(s)


conv = {}
for x, truth in [(1000, 168), (10 ** 6, 78498), (10 ** 8, 5761455)]:
    row = []
    for nr in [0, 10, 50, 100, 300, 1000]:
        est = pi_r(mp.mpf(x), nr)
        row.append((nr, est, est - truth))
        print(f"  x={x:<10} terms={nr:<5} est={est:>15.3f}  err={est-truth:>+12.4f}", flush=True)
    conv[x] = row
    print(flush=True)

json.dump({"damping": damp, "governing": govern}, open("deep_results.json", "w"), indent=1)
print(f"\nALL DONE  {time.time()-t0:.0f}s", flush=True)
