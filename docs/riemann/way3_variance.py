"""WAY 3, circuit 3 - number variance: the stiffness of the count.

Sigma^2(L) = variance of (number of unfolded zeros in a window of length L),
over window positions.

PREDICTION (before the run): data << Poisson (=L) at every L; tracks the GUE
curve (computed here by numerical integration of the same Montgomery kernel
as circuit 2, no remembered constants) for small L; departs BELOW the curve
into a plateau (saturation) at large L - the finite-height rigidity.
"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# census zeros: union of arch endpoints (same list the validated instrument uses)
arches = []
for i in range(1, 9):
    arches.extend(json.load(open(os.path.join(HERE, f"nm_b{i}.json")))["arches"])
zs = sorted(set(round(a["g1"], 9) for a in arches) | set(round(a["g2"], 9) for a in arches))
Z = np.array(zs)
print(f"zeros: {len(Z)}  range ({Z[0]:.3f}, {Z[-1]:.3f})", flush=True)

# unfold with the smooth count (asymptotic main term - validated convention)
def smooth_N(t):
    x = t / (2 * math.pi)
    return x * np.log(x) - x + 7.0 / 8
U = smooth_N(Z)
sp = np.diff(U)
print(f"unfolded mean spacing: {sp.mean():.4f}  (must be ~1)", flush=True)

# GUE reference by numerical integration of the Montgomery kernel:
# Sigma^2(L) = L - 2 * int_0^L (L-u) * (sin(pi u)/(pi u))^2 du
def gue_var(L, n=20000):
    u = np.linspace(1e-9, L, n)
    k = (np.sin(np.pi * u) / (np.pi * u)) ** 2
    return L - 2 * np.trapezoid((L - u) * k, u)

rows = []
for L in (0.25, 0.5, 1, 2, 3, 5, 8, 12, 20, 30, 50, 80):
    lo, hi = U[0], U[-1] - L
    step = max(L / 50, 0.02)
    starts = np.arange(lo, hi, step)
    counts = np.searchsorted(U, starts + L) - np.searchsorted(U, starts)
    v = float(np.var(counts))
    g = float(gue_var(L))
    rows.append({"L": L, "obs": v, "gue": g, "poisson": L, "windows": len(starts)})
    print(f"L={L:>5}: obs={v:7.4f}  GUE={g:7.4f}  Poisson={L:<5}  (obs/GUE={v/g:5.2f}, obs/Poisson={v/L:6.3f})", flush=True)

# where does it leave the curve - the saturation plateau
plateau = max(r["obs"] for r in rows)
follow = [r for r in rows if abs(r["obs"] - r["gue"]) / r["gue"] < 0.15]
Lf = max(r["L"] for r in follow) if follow else None
print(f"tracks GUE (within 15%) up to L~{Lf};  plateau ~{plateau:.3f}", flush=True)

json.dump({"n_zeros": len(Z), "mean_spacing": float(sp.mean()), "rows": rows,
           "tracks_to_L": Lf, "plateau": plateau},
          open(os.path.join(HERE, "way3_variance.json"), "w"), indent=1)
