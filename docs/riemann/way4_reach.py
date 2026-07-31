"""WAY 4, circuit 2 — the reach: sieve to 1e9, band + Schoenfeld falsifier.

PREDICTION (written before the run):
  - pi(1e9) must equal 50,847,534 exactly (control; anything else = instrument broken)
  - |psi(x)-x|/sqrt(x) stays a flat band (max ~0.6), no upward drift in the new decade
  - Schoenfeld ratio |psi-x|*8*pi/(sqrt(x)*ln^2 x) < 1 everywhere (falsifier does NOT fire);
    if it fires at any x >= 74, RH is FALSE - that is the armed instrument.
"""
import numpy as np, json, math, time

N = 10**9
SEG = 10**7
t0 = time.time()

# base primes to sqrt(N)
lim = int(N**0.5) + 1
bs = np.ones(lim + 1, dtype=bool); bs[:2] = False
for p in range(2, int(lim**0.5) + 1):
    if bs[p]: bs[p*p::p] = False
base = np.nonzero(bs)[0]
base_logs = np.log(base.astype(np.float64))
base_cum = np.concatenate(([0.0], np.cumsum(base_logs)))  # theta over base primes
print(f"base primes to {lim}: {len(base)}  ({time.time()-t0:.0f}s)", flush=True)

def theta_small(x):
    """exact theta(x) for x <= lim, from base primes"""
    i = np.searchsorted(base, x, side='right')
    return float(base_cum[i])

def ipow_root(x, k):
    """floor(x**(1/k)) exactly"""
    r = int(round(x ** (1.0 / k)))
    while (r + 1) ** k <= x: r += 1
    while r ** k > x and r > 0: r -= 1
    return r

# sample points: 8 per decade, 1e3..1e9, plus exact decades
samples = sorted(set(int(v) for v in np.geomspace(1e3, 1e9, 49)) | {10**d for d in range(3, 10)})
res = {x: None for x in samples}

pi_total = 0
seg_totals = []          # per-segment sums of log p  (fsum across later)
done_theta = 0.0         # fsum of completed segments, refreshed each segment
si = 0
for lo in range(2, N + 1, SEG):
    hi = min(lo + SEG, N + 1)
    seg = np.ones(hi - lo, dtype=bool)
    if lo == 2:
        pass
    for p in base:
        if p * p >= hi: break
        start = max(p * p, ((lo + p - 1) // p) * p)
        if start < hi:
            seg[start - lo::p] = False
    if lo == 2:
        seg[:0] = False  # nothing below 2 present
    else:
        pass
    # mask out 0,1 if in range (lo==2 starts at 2 already)
    primes_seg = np.nonzero(seg)[0] + lo
    # remove composites below p*p for small p already handled; for lo==2 the base sieve marks all
    if lo == 2:
        # crossing started at p*p, so entries < p*p for each p survive wrongly only if composite<4: none (2,3 prime)
        pass
    logs = np.log(primes_seg.astype(np.float64))
    pi_total += len(primes_seg)
    # samples inside this segment
    for x in samples:
        if lo <= x < hi:
            idx = np.searchsorted(primes_seg, x, side='right')
            res[x] = done_theta + float(logs[:idx].sum())
    st = float(logs.sum())
    seg_totals.append(st)
    done_theta = math.fsum(seg_totals)
    si += 1
    if si % 10 == 0:
        print(f"  seg {si}/100  pi so far {pi_total}  ({time.time()-t0:.0f}s)", flush=True)

print(f"pi(1e9) = {pi_total}   control 50,847,534  match={pi_total==50847534}", flush=True)

# psi(x) = theta(x) + sum_{k>=2} theta(x^{1/k}); rows
rows = []
for x in samples:
    th = res[x]
    pp = 0.0
    k = 2
    while True:
        r = ipow_root(x, k)
        if r < 2: break
        pp += theta_small(r)
        k += 1
    psi = th + pp
    E = psi - x
    band = abs(E) / math.sqrt(x)
    lnx = math.log(x)
    scho = abs(E) * 8 * math.pi / (math.sqrt(x) * lnx * lnx)
    rows.append({"x": x, "psi_minus_x": E, "band": band, "schoenfeld": scho})

mx_band = max(r["band"] for r in rows)
mx_scho = max(r["schoenfeld"] for r in rows)
# raw exponent refit over full range (honesty row; expect log-factor inflation)
lx = [math.log(r["x"]) for r in rows if abs(r["psi_minus_x"]) > 1e-9]
ly = [math.log(abs(r["psi_minus_x"])) for r in rows if abs(r["psi_minus_x"]) > 1e-9]
n = len(lx); mxx = sum(lx)/n; myy = sum(ly)/n
slope = sum((a-mxx)*(b-myy) for a,b in zip(lx,ly)) / sum((a-mxx)**2 for a in lx)

out = {"N": N, "pi_1e9": pi_total, "pi_control_match": pi_total == 50847534,
       "max_band": mx_band, "max_schoenfeld": mx_scho, "raw_exponent": slope,
       "rows": rows, "secs": round(time.time()-t0)}
json.dump(out, open("way4_reach.json", "w"), indent=1)
print(f"max |psi-x|/sqrt(x) = {mx_band:.3f}   max Schoenfeld ratio = {mx_scho:.4f}   raw slope = {slope:.3f}", flush=True)
for r in rows:
    if r["x"] in (10**3,10**4,10**5,10**6,10**7,10**8,10**9):
        print(f"  x=10^{int(round(math.log10(r['x'])))}  psi-x={r['psi_minus_x']:+12.1f}  band={r['band']:.3f}  scho={r['schoenfeld']:.4f}", flush=True)
print(f"total {time.time()-t0:.0f}s", flush=True)
