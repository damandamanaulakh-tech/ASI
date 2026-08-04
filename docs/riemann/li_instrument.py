"""LI INSTRUMENT - the reverse walk's measurable: Li coefficients from our census.

Li's criterion [READING]: RH <=> lambda_n >= 0 for all n, where
  lambda_n = sum over nontrivial rho of [1 - (1 - 1/rho)^n],
zeros paired (rho, conjugate, 1-rho, 1-conjugate) - our census gives gamma>0;
each gamma contributes rho = 1/2 + i*gamma and its conjugate; the functional
pair 1-rho = conjugate of rho when on the line (Re=1/2), so summing rho and
rho-bar over our gammas IS the full symmetric sum for on-line zeros.

CONTROL [READING]: lambda_1 = 1 + gamma_E/2 - ln(4*pi)/2 ~ 0.0230957.
Truncated at census height T, the predicted tail deficit for lambda_1 is
  tail_1 ~ (1/2pi) * (ln(T/2pi)+1)/T   (density * 2Re(1/rho) integrated)
and tail_n grows ~ n * tail_1 for small n (leading order). The instrument is
trusted only if the lambda_1 partial sum lands at control minus tail, within
band.

PREDICTIONS (registered before the run):
  - lambda_1_partial ~ 0.0230957 - tail_1 (calibration must land)
  - all partial lambda_n > 0 for n = 1..30 (Li positivity visible in census)
  - lambda_n rising with n (the known growth trend under RH)
"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

def load_zeros():
    arches = []
    for i in range(1, 33):
        # the banked blocks live in census/ (they were written beside the
        # script while walking, then banked into the repo under census/);
        # look in both so the instrument runs against the shipped data.
        p = os.path.join(HERE, "census", f"nm_b{i}.json")
        if not os.path.exists(p):
            p = os.path.join(HERE, f"nm_b{i}.json")
        if os.path.exists(p):
            arches.extend(json.load(open(p))["arches"])
    raw = sorted(set(round(a["g1"], 9) for a in arches) | set(round(a["g2"], 9) for a in arches))
    zs = [raw[0]]
    for z in raw[1:]:
        if z - zs[-1] > 1e-4:
            zs.append(z)
    return np.array(zs)

G = load_zeros()
T = G[-1]
print(f"census zeros: {len(G)}  to T={T:.3f}", flush=True)

rho = 0.5 + 1j * G                      # zeros above the axis
NMAX = 30
rows = []
base = 1.0 - 1.0 / rho                   # (1 - 1/rho)
powk = np.ones_like(base)
for n in range(1, NMAX + 1):
    powk = powk * base                   # (1-1/rho)^n
    # contribution of rho and its conjugate: 2*Re[1 - (1-1/rho)^n]
    lam_partial = float(np.sum(2.0 * (1.0 - powk).real))
    rows.append({"n": n, "lambda_partial": lam_partial})

# tail estimate (leading order, declared): density (1/2pi)ln(t/2pi), term ~ n * 2*Re(1/rho) ~ n/t^2 * ... integrated
tail1 = (math.log(T / (2 * math.pi)) + 1) / (2 * math.pi * T)
CONTROL = 1 + 0.5772156649015329 / 2 - math.log(4 * math.pi) / 2

print(f"control lambda_1 (exact, known): {CONTROL:.7f}", flush=True)
print(f"predicted tail_1 at T={T:.0f}:   {tail1:.7f}", flush=True)
print(f"predicted partial lambda_1:      {CONTROL - tail1:.7f}", flush=True)
print(f"measured  partial lambda_1:      {rows[0]['lambda_partial']:.7f}", flush=True)
calib_err = abs(rows[0]["lambda_partial"] - (CONTROL - tail1))
print(f"calibration miss: {calib_err:.2e}  ({'PASS' if calib_err < 3*tail1 else 'FAIL'})", flush=True)

neg = [r["n"] for r in rows if r["lambda_partial"] <= 0]
mono = all(rows[i+1]["lambda_partial"] > rows[i]["lambda_partial"] for i in range(len(rows)-1))
posmsg = "ALL POSITIVE" if not neg else "NEGATIVE AT " + str(neg)
print(f"positivity n=1..{NMAX}: {posmsg}", flush=True)
print(f"rising with n: {mono}", flush=True)
for r in rows:
    if r["n"] in (1, 2, 3, 5, 10, 20, 30):
        print(f"  n={r['n']:>2}  lambda_partial = {r['lambda_partial']:.6f}  (+tail ~ {r['n']*tail1:.5f})", flush=True)

json.dump({"n_zeros": int(len(G)), "T": float(T), "control_lambda1": CONTROL,
           "tail1_estimate": tail1, "rows": rows,
           "all_positive": not neg, "rising": mono},
          open(os.path.join(HERE, "li_lambda.json"), "w"), indent=1)
