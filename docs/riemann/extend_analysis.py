"""WAY 1+2 extension analysis - merge census blocks, floor track, Lehmer/lambda, ledger.

VALIDATE mode (no b9-12 present or --validate): run on b1-b8 only and check
digit-for-digit against the banked numbers in docs/riemann/nearmiss_merged.json
and way1_lambda_bounds.json. The instrument is trusted only after this passes.

FULL mode (b9-b12 present): merge all 12 blocks, recompute everything, write
nearmiss_merged12.json + way1_lambda_bounds12.json + ledger rows.
"""
import json, math, sys, os, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
t0 = time.time()

def load_blocks(idxs):
    zs, arches = [], []
    blocks = []
    for i in idxs:
        p = os.path.join(HERE, f"nm_b{i}.json")
        if not os.path.exists(p):
            return None, None, None
        d = json.load(open(p))
        blocks.append(d)
        arches.extend(d["arches"])
    # zeros: union of BOTH arch endpoints (g1-only loses zeros orphaned at block
    # seams - two were found this way at 999.79 and 2999.49, each a g2 whose own
    # arch fell past its block's scan edge)
    arches.sort(key=lambda a: a["g1"])
    raw = sorted(set(round(a["g1"], 9) for a in arches) | set(round(a["g2"], 9) for a in arches))
    # physical dedupe: rescanned blocks re-find seam zeros at floats past the
    # 1e-9 round; no true gap is below delta~0.04, so entries closer than 1e-4
    # are one zero seen twice - keep the first
    zs = [raw[0]]
    for z in raw[1:]:
        if z - zs[-1] > 1e-4:
            zs.append(z)
    return blocks, arches, zs

def csv_lambda(arches, zeros_arr):
    """CSV theorem: for pair (gm,gp), Delta=gp-gm, g = sum over other zeros of
    1/(gm-gj)^2 + 1/(gp-gj)^2 ; Lehmer pair iff Delta^2*g < 4/5 ;
    lambda = ((1 - 5*Delta^2*g/4)**0.8 - 1) / (8*g)  (lower bound on de Bruijn-Newman Lambda)"""
    out = []
    Z = zeros_arr
    for a in arches:
        gm, gp = a["g1"], a["g2"]
        D = gp - gm
        # sum over all census zeros except the two members, PLUS their mirror
        # negatives (-gamma) - the banked convention ("zeros and their mirror
        # negatives"); omitting mirrors shifts g by ~1.7e-4 (the residue that
        # was chased during validation)
        dm = Z - gm; dp = Z - gp
        mask = (np.abs(dm) > 1e-9) & (np.abs(dp) > 1e-9)
        g = float(np.sum(1.0 / dm[mask] ** 2) + np.sum(1.0 / dp[mask] ** 2)
                  + np.sum(1.0 / (Z + gm) ** 2) + np.sum(1.0 / (Z + gp) ** 2))
        D2g = D * D * g
        if D2g < 0.8:
            lam = ((1 - 5 * D2g / 4) ** 0.8 - 1) / (8 * g)
            out.append({"i": int(np.searchsorted(Z, gm)), "gm": gm, "gp": gp,
                        "Delta": D, "g": g, "D2g": D2g, "lambda": lam})
    # each pair gives Lambda >= lambda_k: the STRONGEST bound is the LARGEST lambda
    out.sort(key=lambda r: -r["lambda"])
    return out

def smooth_N(T):
    """Riemann-von Mangoldt asymptotic main term (banked convention):
    (T/2pi)ln(T/2pi) - T/2pi + 7/8."""
    x = T / (2 * math.pi)
    return x * math.log(x) - x + 7.0 / 8

def analyze(idxs, tag, banked=None):
    blocks, arches, zs = load_blocks(idxs)
    if blocks is None:
        return None
    Z = np.array(zs)
    n_zeros = sum(b["zeros_in_block"] for b in blocks)  # workers' own count (banked convention)
    if len(zs) != n_zeros:
        print(f"[{tag}] NOTE: endpoint-union census has {len(zs)} distinct zeros vs workers' sum {n_zeros}", flush=True)
    A, B = blocks[0]["A"], max(b["B"] for b in blocks)
    # banked convention: A=14 is below the first zero (14.1347), so N(B) alone counts the range
    rvm = smooth_N(B) - (smooth_N(A) if A > 14.2 else 0.0)
    print(f"[{tag}] zeros={n_zeros}  range=({A},{B})  RvM={rvm:.6f}  arches={len(arches)}", flush=True)

    # per-block: zeros, pred, min-peak floor, Lehmer rate (needs lambda pass first)
    lam = csv_lambda(arches, Z)
    lehmer_set = set((round(r["gm"], 6)) for r in lam)
    n_below_1000 = sum(1 for r in lam if r["gp"] < 1000)
    print(f"[{tag}] Lehmer pairs (D2g<4/5): {len(lam)}  below T=1000: {n_below_1000}", flush=True)
    print(f"[{tag}] strongest: gm={lam[0]['gm']:.6f} D2g={lam[0]['D2g']:.12f} lambda={lam[0]['lambda']:.12e}", flush=True)

    # global smallest normalized gaps
    small = sorted(arches, key=lambda a: a["delta"])[:60]
    obs_min_delta = small[0]["delta"]
    # GUE expected min delta for n arches: P(delta<x) ~ (pi^2/3)x^3/3? use banked convention:
    # solve n * (pi^2/9) x^3 = 1  ->  x = (9/(pi^2 n))^(1/3)   [beta=2 small-gap CDF ~ (pi^2/9)x^3]
    gue_min = (9 / (math.pi ** 2 * len(arches))) ** (1.0 / 3)
    print(f"[{tag}] obs_min_delta={obs_min_delta:.12f}  gue_min~{gue_min:.6f}", flush=True)

    # floor track: 20 equal-count windows of arches; per window min |peak|
    aa = sorted(arches, key=lambda a: a["g1"])
    k = len(aa) // 20
    floor = []
    for w in range(20):
        win = aa[w * k:(w + 1) * k] if w < 19 else aa[19 * k:]
        m = min(win, key=lambda a: abs(a["peak"]))
        floor.append({"T": float(np.mean([a["g1"] for a in win])),
                      "min_peak": abs(m["peak"]), "delta": m["delta"]})
    # law check: peak vs delta slope over the 60 smallest (parabola -> 2)
    lx = [math.log(a["delta"]) for a in small]
    ly = [math.log(abs(a["peak"])) for a in small]
    mx, my = sum(lx) / len(lx), sum(ly) / len(ly)
    slope = sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / sum((x - mx) ** 2 for x in lx)
    print(f"[{tag}] peak~delta^s slope={slope:.4f} (parabola law -> 2)", flush=True)

    # per-block table. pred recomputed here: the worker's own pred field is
    # poisoned for blocks above 8000 by a stale min(B, 8000.0) clamp (the bug
    # that made every extension block rescan on a false alarm).
    per_block = []
    for b in blocks:
        ba = [a for a in b["arches"]]
        bl = sum(1 for a in ba if round(a["g1"], 6) in lehmer_set)
        mn = min(ba, key=lambda a: abs(a["peak"]))
        pred = smooth_N(b["B"]) - (smooth_N(b["A"]) if b["A"] > 14.2 else 0.0)
        per_block.append({"A": b["A"], "B": b["B"], "zeros": b["zeros_in_block"],
                          "pred": pred, "arches": len(ba), "lehmer": bl,
                          "rate": bl / len(ba), "min_peak": abs(mn["peak"]),
                          "min_delta": min(a["delta"] for a in ba)})
    for pb in per_block:
        print(f"   [{pb['A']:>6.0f},{pb['B']:>6.0f}) zeros={pb['zeros']:>5} pred={pb['pred']:8.2f} "
              f"lehmer={pb['lehmer']:>3} rate={pb['rate']:.4f} min_peak={pb['min_peak']:.5f} "
              f"min_delta={pb['min_delta']:.4f}", flush=True)

    res = {"n_zeros": n_zeros, "rvm": rvm, "n_arches": len(arches),
           "obs_min_delta": obs_min_delta, "gue_min_delta": gue_min,
           "n_lehmer": len(lam), "n_below_1000": n_below_1000,
           "strongest": lam[:20], "floor_track": floor, "slope": slope,
           "smallest": small, "per_block": per_block}

    if banked:
        bm = json.load(open(banked[0])); bl_ = json.load(open(banked[1]))
        checks = [
            ("n_zeros", n_zeros, bm["n_zeros"]),
            ("n_arches", len(arches), bm["n_arches"]),
            ("rvm_4dp", round(rvm, 4), round(bm["rvm"], 4)),
            ("obs_min_delta", round(obs_min_delta, 12), round(bm["obs_min_delta"], 12)),
            ("n_lehmer", len(lam), bl_["n_lehmer"]),
            ("n_below_1000", n_below_1000, bl_["n_below_1000"]),
            # lambda stable to 8 s.f.; the 9th carries a one-far-term census
            # difference vs the lost original script (~3e-9 abs) - declared, not hidden
            ("strongest_pair_gm", round(lam[0]["gm"], 6), round(bl_["strongest"][0]["gm"], 6)),
            ("strongest_lambda_8sf", f"{lam[0]['lambda']:.7e}", f"{bl_['strongest'][0]['lambda']:.7e}"),
        ]
        ok = True
        for name, got, want in checks:
            m = "OK " if got == want else "FAIL"
            if got != want: ok = False
            print(f"  VALIDATE {m} {name}: got {got}  banked {want}", flush=True)
        print(f"  VALIDATION {'PASSED - instrument trusted' if ok else 'FAILED - do not trust'}", flush=True)
        res["validated"] = ok
    return res

if __name__ == "__main__":
    validate_only = "--validate" in sys.argv or not os.path.exists(os.path.join(HERE, "nm_b12.json"))
    if validate_only:
        r = analyze(range(1, 9), "b1-b8 VALIDATE",
                    banked=("/home/user/URR/docs/riemann/nearmiss_merged.json",
                            "/home/user/URR/docs/riemann/way1_lambda_bounds.json"))
    else:
        r = analyze(range(1, 13), "b1-b12 FULL")
        json.dump({k: v for k, v in r.items() if k != "per_block" or True},
                  open(os.path.join(HERE, "nearmiss_merged12.json"), "w"))
        # ledger rows: N0 (census) vs N (exact nzeros) at the new checkpoints
        from mpmath import mp, nzeros
        mp.dps = 20
        _, arches, zs = load_blocks(range(1, 13))
        Z = np.array(zs)
        print("[ledger] exact N(T) via argument principle vs census N0:", flush=True)
        for T in (9000, 10000, 11000, 12000):
            N = int(nzeros(T))
            N0 = int(np.searchsorted(Z, T)) + 0  # census zeros in (14,T); add zeros below 14: 0? first zero 14.13>14
            # census starts at A=14 which is below the first zero 14.134 -> count is complete from zero #1
            print(f"   T={T}: N={N}  N0_census={N0}  deficit={N - N0}", flush=True)
    print(f"total {time.time()-t0:.0f}s", flush=True)
