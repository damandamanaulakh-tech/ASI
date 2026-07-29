"""Struck-text recovery — full sweep, every text band on all three folios.

Two bugs killed the earlier passes, both now fixed and both worth naming:

  * The slanted strike kernels were built flat and rotated in place, which
    clipped the line out of its own box. A near-empty kernel makes MORPH_OPEN a
    no-op, so EVERY ink pixel came back labelled "strike". Fixed by drawing the
    line into a box tall enough to hold it (`slanted_line_kernel`), with an
    assert so it can never silently collapse again.
  * The ink layer was normalised to the crop maximum. One dark scan artifact in
    a crop stretches the scale, Otsu then picks a high threshold, and the real
    ink is thrown away — which is why several crops came back at 0.02% ink.
    Fixed with a robust 99.5th-percentile scale.

No coordinates are guessed here. Text bands are found from the page's own row
profile, then every band is swept for long near-horizontal strokes. A band is
reported as struck only if the evidence says so.

Stages per band: INK -> STRIKE -> RESIDUAL -> BRIDGE -> TONE.
BRIDGE refills a struck column only when surviving ink is witnessed BOTH above
and below the strike. Nothing is drawn in that was not already there twice.
"""
import cv2
import numpy as np
import json

PAGES = ("hi19r", "hi19v", "hi20r")
XL, XR = 0.06, 0.94                       # inside the scan border


def ink_layer(bgr):
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    bg = cv2.morphologyEx(g, cv2.MORPH_CLOSE,
                          cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (61, 61)))
    bg = cv2.GaussianBlur(bg, (81, 81), 0)
    d = np.clip(bg.astype(np.int16) - g.astype(np.int16), 0, None).astype(np.float32)
    hi = np.percentile(d, 99.5)           # robust scale, not the crop max
    ink = np.clip(d * (255.0 / max(hi, 1.0)), 0, 255).astype(np.uint8)
    ink = cv2.bilateralFilter(ink, 9, 60, 60)
    _, bw = cv2.threshold(ink, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    return bw, ink


def slanted_line_kernel(length, ang_deg, thick=3):
    rise = int(abs(np.tan(np.radians(ang_deg))) * length)
    h = rise + thick
    k = np.zeros((h, length), np.uint8)
    y0, y1 = (thick // 2, h - 1 - thick // 2) if ang_deg >= 0 else (h - 1 - thick // 2, thick // 2)
    cv2.line(k, (0, y0), (length - 1, y1), 1, thick)
    return k


def strike_layer(bw, min_len=200, thick=3):
    acc = np.zeros_like(bw)
    for ang in (-4, -2.5, -1, 0, 1, 2.5, 4):
        kr = slanted_line_kernel(min_len, ang, thick)
        assert kr.sum() >= min_len * 0.9, f"kernel collapsed at {ang} deg"
        acc = np.maximum(acc, cv2.morphologyEx(bw, cv2.MORPH_OPEN, kr))
    return cv2.dilate(acc, np.ones((5, 3), np.uint8))


def bridge(residual, strike, reach=26):
    H, W = residual.shape
    out = residual.copy()
    refilled = ncols = 0
    for x in range(W):
        ys = np.flatnonzero(strike[:, x])
        if ys.size == 0:
            continue
        ncols += 1
        y0, y1 = ys.min(), ys.max()
        if residual[max(0, y0 - reach):y0, x].any() and \
           residual[y1 + 1:min(H, y1 + 1 + reach), x].any():
            out[y0:y1 + 1, x] = 255
            refilled += 1
    return out, refilled, ncols


def tone_test(bgr, strike, bw):
    b, g, r = cv2.split(bgr.astype(np.float32))
    text = cv2.subtract(bw, strike)
    sm, tm = strike > 0, text > 0
    if sm.sum() < 400 or tm.sum() < 400:
        return None
    o = {}
    for nm, ch in (("b-r", b - r), ("b-g", b - g), ("g-r", g - r)):
        sv, tv = ch[sm], ch[tm]
        pooled = float(np.sqrt((sv.var() + tv.var()) / 2)) + 1e-9
        o[nm] = round(float(abs(sv.mean() - tv.mean()) / pooled), 3)
    return o


def bands_of(page_bw, H):
    prof = (page_bw > 0).mean(axis=1)
    thr = max(0.012, prof.max() * 0.10)
    on, out, s = prof > thr, [], None
    for y, v in enumerate(on):
        if v and s is None:
            s = y
        elif not v and s is not None:
            if y - s > 28:
                out.append((s, y))
            s = None
    if s is not None and H - s > 28:
        out.append((s, H))
    return out


report = {}
for page in PAGES:
    im = cv2.imread(f"{page}.png")
    H, W = im.shape[:2]
    x0, x1 = int(W * XL), int(W * XR)
    full = im[:, x0:x1]
    fbw, _ = ink_layer(full)
    bands = bands_of(fbw, H)
    print(f"\n=== {page}  {W}x{H}  {len(bands)} text bands "
          f"(ink {100*(fbw>0).mean():.2f}%) ===", flush=True)
    report[page] = []
    for i, (a, b) in enumerate(bands, 1):
        pad = 12
        crop = full[max(0, a - pad):min(H, b + pad)]
        bw, _ = ink_layer(crop)
        st = strike_layer(bw)
        stk = int((st > 0).sum())
        if stk < 1500:                    # nothing long and level in this band
            report[page].append({"band": i, "y": [a, b], "struck": False,
                                 "strike_pixels": stk})
            continue
        resid = cv2.subtract(bw, st)
        fixed, refilled, ncols = bridge(resid, st)
        pct = round(100.0 * refilled / ncols, 1) if ncols else 0.0
        rec = {"band": i, "y": [a, b], "struck": True, "strike_pixels": stk,
               "struck_columns": ncols, "columns_carrying_a_letter": refilled,
               "pct_strike_over_text": pct, "ink_pct": round(100 * float((bw > 0).mean()), 2),
               "tone_separation_sd": tone_test(crop, st, bw)}
        report[page].append(rec)
        tag = f"{page}_b{i:02d}"
        up = lambda m, f=1.6: cv2.resize(m, None, fx=f, fy=f, interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(f"x_{tag}_raw.png", up(crop))
        cv2.imwrite(f"x_{tag}_strikeonly.png", up(255 - st))
        cv2.imwrite(f"x_{tag}_recovered.png", up(255 - fixed))
        gap = np.full((16, bw.shape[1]), 190, np.uint8)
        cv2.imwrite(f"x_{tag}_beforeafter.png",
                    up(np.vstack([255 - bw, gap, 255 - fixed])))
        print(f"  band {i:>2} y{a:>5}-{b:<5} STRUCK  strike {stk:>7}px  "
              f"{refilled}/{ncols} struck columns carried a letter ({pct:>5.1f}%)  "
              f"tone {rec['tone_separation_sd']}", flush=True)

json.dump(report, open("recovery_full.json", "w"), indent=1)
tot = sum(1 for p in report.values() for r in p if r["struck"])
print(f"\n{tot} struck bands across {len(PAGES)} folios. Images written as x_*.png")
