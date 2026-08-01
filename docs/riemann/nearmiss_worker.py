"""Near-miss census worker: one block [a,b) of the line. See nearmiss.py.
Usage: nm_worker.py A B OUT.json
Scans [A-1, B+1] so no zero or boundary arch is lost; keeps arches whose left
zero lies in [A, B). Count-guard per block: if found-zeros disagree with the
Riemann-von Mangoldt prediction by >2, rescan at step/4.
"""
import json
import sys
import time

import mpmath as mp

mp.mp.dps = 11
Z = mp.siegelz
STEP = 0.025
A, B, OUT = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
t0 = time.time()


def theta_pi_plus1(t):
    return float(mp.siegeltheta(t) / mp.pi) + 1


def find_zeros(a, b, step):
    zeros = []
    t, prev_t = a, a
    prev = Z(a)
    while t < b:
        t = min(t + step, b)
        cur = Z(t)
        if mp.sign(cur) != mp.sign(prev) and prev != 0:
            lo, hi = prev_t, t
            for _ in range(60):
                mid = (lo + hi) / 2
                if mp.sign(Z(mid)) == mp.sign(Z(lo)):
                    lo = mid
                else:
                    hi = mid
                if hi - lo < 1e-9:
                    break
            zeros.append(float((lo + hi) / 2))
        prev_t, prev = t, cur
    return zeros


def arch_peak(a, b):
    s = 1 if float(Z((a + b) / 2)) >= 0 else -1
    lo, hi = a, b
    for _ in range(60):
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if s * Z(m1) < s * Z(m2):
            lo = m1
        else:
            hi = m2
        if hi - lo < 1e-8:
            break
    tp = (lo + hi) / 2
    return float(abs(Z(tp))), float(tp), s


lo_scan = max(10.0, A - 1.0)
zs = find_zeros(lo_scan, B + 1.0, STEP)
inb = [z for z in zs if A <= z < B]
# (the old min(B, 8000.0) clamp here fired false-alarm rescans on every
# block above 8000 - named in WAY1 doc section 8; generalized 2026-08-01)
pred = theta_pi_plus1(B) - theta_pi_plus1(max(A, 14.0))
note = ""
if abs(len(inb) - pred) > 2:
    zs = find_zeros(lo_scan, B + 1.0, STEP / 4)
    inb = [z for z in zs if A <= z < B]
    note = "RESCANNED"

arches = []
for i in range(len(zs) - 1):
    if not (A <= zs[i] < B):
        continue
    g1, g2 = zs[i], zs[i + 1]
    peak, tp, s = arch_peak(g1, g2)
    mean_sp = float(2 * mp.pi / mp.log(g1 / (2 * mp.pi)))
    arches.append({"g1": g1, "g2": g2, "gap": g2 - g1,
                   "delta": (g2 - g1) / mean_sp,
                   "peak": peak, "t_peak": tp, "sign": s})

json.dump({"A": A, "B": B, "zeros_in_block": len(inb), "pred": pred,
           "note": note, "arches": arches,
           "secs": round(time.time() - t0)}, open(OUT, "w"))
print(f"[{A:.0f},{B:.0f}) zeros={len(inb)} pred={pred:.2f} {note} "
      f"arches={len(arches)} {time.time()-t0:.0f}s", flush=True)
