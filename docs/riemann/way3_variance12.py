"""WAY 3 - variance plateau RE-MEASURED on the extended census (his question:
'does the data follow the primes upward?').

Verdict rules, pre-registered before this run:
  FOLLOWED  - new-stretch plateau rises above the old measured 0.3351 and
              lands inside Berry's band for its heights (~0.365-0.369)
  REFUTED   - falls clearly below the old level / leaves the band downward
  AMBIGUOUS - shift smaller than the oscillation spread (~+-0.08)
"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

def load_zeros(idxs):
    arches = []
    for i in idxs:
        arches.extend(json.load(open(os.path.join(HERE, f"nm_b{i}.json")))["arches"])
    raw = sorted(set(round(a["g1"], 9) for a in arches) | set(round(a["g2"], 9) for a in arches))
    zs = [raw[0]]
    for z in raw[1:]:
        if z - zs[-1] > 1e-4:
            zs.append(z)
    return np.array(zs)

def smooth_N(t):
    x = t / (2 * math.pi)
    return x * np.log(x) - x + 7.0 / 8

def plateau_of(Z, tag):
    U = smooth_N(Z)
    print(f"[{tag}] zeros={len(Z)}  mean spacing={np.diff(U).mean():.4f}", flush=True)
    rows = []
    for L in (8, 12, 20, 30, 50, 80):
        lo, hi = U[0], U[-1] - L
        starts = np.arange(lo, hi, max(L / 50, 0.02))
        counts = np.searchsorted(U, starts + L) - np.searchsorted(U, starts)
        rows.append({"L": L, "obs": float(np.var(counts))})
        print(f"   L={L:>3}: obs={rows[-1]['obs']:.4f}", flush=True)
    m = sum(r["obs"] for r in rows) / len(rows)
    print(f"[{tag}] plateau mean (L=8..80) = {m:.4f}", flush=True)
    return m, rows

# Berry plateau from the primes, exact sieve
def berry_plateau(T):
    T = int(T)
    sieve = np.ones(T + 1, dtype=bool); sieve[:2] = False
    for p in range(2, int(T ** 0.5) + 1):
        if sieve[p]: sieve[p * p::p] = False
    s = 0.0
    for p in np.nonzero(sieve)[0]:
        pk = p
        while pk <= T:
            s += (math.log(p) ** 2) / (pk * math.log(pk) ** 2)
            pk *= p
    return (s + 1) / math.pi ** 2

Z_all = load_zeros(range(1, 13))
Z_new = Z_all[(Z_all >= 8000) & (Z_all <= 12000)]

m_all, r_all = plateau_of(Z_all, "merged 14-12000")
m_new, r_new = plateau_of(Z_new, "new stretch 8000-12000")
b8k, b12k = berry_plateau(8000), berry_plateau(12000)
print(f"\nBerry band (old census heights, T=1000..8000):  0.338 - {b8k:.4f}")
print(f"Berry band (new stretch, T=8000..12000):        {b8k:.4f} - {b12k:.4f}")
print(f"old measured plateau (b1-b8):  0.3351")
print(f"new-stretch measured plateau:  {m_new:.4f}")
print(f"merged measured plateau:       {m_all:.4f}")

verdict = ("FOLLOWED" if m_new > 0.3351 and 0.34 <= m_new <= 0.40
           else "REFUTED" if m_new < 0.31 else "AMBIGUOUS")
print(f"\nVERDICT (pre-registered rules): {verdict}", flush=True)

json.dump({"merged": {"plateau": m_all, "rows": r_all},
           "new_stretch": {"plateau": m_new, "rows": r_new},
           "berry": {"T8000": b8k, "T12000": b12k},
           "old_measured": 0.3351, "verdict": verdict},
          open(os.path.join(HERE, "way3_variance12.json"), "w"), indent=1)
