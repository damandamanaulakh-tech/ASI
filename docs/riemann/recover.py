"""Struck-text recovery on Riemann's draft.

Three independent attacks on the same problem:
  A. LOCAL CONTRAST (CLAHE)      — lift faint ink out of the stained parchment
  B. DIRECTIONAL SUPPRESSION      — a strike is a long, thin, near-horizontal
                                    stroke; letterforms are not. Isolate the long
                                    horizontal component morphologically and
                                    remove it, leaving what was underneath.
  C. INK-TONE SEPARATION          — if a strike was added in a later sitting the
                                    iron-gall ink can differ in tone; test the
                                    colour channels for separation.
Nothing is invented: every output is a filtered view of the same pixels.
"""
import cv2
import numpy as np
import sys

REGIONS = {
    # name            page      y0     y1     x0    x1   (fractions of the page)
    "L40_RH_final":  ("hi19r", 0.882, 0.914, 0.05, 0.99),
    "L32_longstrike": ("hi19r", 0.770, 0.800, 0.05, 0.99),
    "L39_RH_sent":   ("hi19r", 0.858, 0.888, 0.05, 0.99),
    "19v_abandoned": ("hi19v", 0.020, 0.075, 0.05, 0.99),
    "20r_gauss":     ("hi20r", 0.700, 0.760, 0.05, 0.99),
}


def clahe(g, clip=3.5, grid=16):
    return cv2.createCLAHE(clipLimit=clip, tileGridSize=(grid, grid)).apply(g)


def suppress_horizontal(ink, min_len=120, thick=3):
    """Isolate long near-horizontal strokes and remove them from the ink layer."""
    out = np.zeros_like(ink)
    for ang in (-4, -2, 0, 2, 4):                       # strikes are rarely level
        k = cv2.getStructuringElement(cv2.MORPH_RECT, (min_len, thick))
        M = cv2.getRotationMatrix2D((min_len / 2, thick / 2), ang, 1)
        kr = cv2.warpAffine(k.astype(np.float32), M, (min_len, thick))
        kr = (kr > 0.5).astype(np.uint8)
        opened = cv2.morphologyEx(ink, cv2.MORPH_OPEN, kr)
        out = np.maximum(out, opened)
    strike = cv2.dilate(out, np.ones((thick + 2, 3), np.uint8))
    residual = cv2.subtract(ink, strike)
    return strike, residual


def process(name):
    page, y0, y1, x0, x1 = REGIONS[name]
    im = cv2.imread(f"{page}.png")
    H, W = im.shape[:2]
    crop = im[int(H * y0):int(H * y1), int(W * x0):int(W * x1)]
    b, g, r = cv2.split(crop)
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    # ---- A. local contrast on the raw grey
    A = clahe(gray)

    # ---- ink layer: parchment is bright, ink dark -> invert + normalise
    inv = 255 - clahe(gray, clip=4.0, grid=24)
    inv = cv2.normalize(inv, None, 0, 255, cv2.NORM_MINMAX)
    _, ink = cv2.threshold(inv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # ---- B. directional suppression
    strike, residual = suppress_horizontal(ink)
    B = 255 - cv2.dilate(residual, np.ones((2, 2), np.uint8))   # back to ink-on-white

    # ---- C. ink-tone separation: blue channel holds iron-gall differently
    tone = cv2.normalize(cv2.subtract(b, r), None, 0, 255, cv2.NORM_MINMAX)
    C = clahe(tone, clip=4.0, grid=20)

    up = lambda m: cv2.resize(m, None, fx=1.6, fy=1.6, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(f"rec_{name}_A_contrast.png", up(A))
    cv2.imwrite(f"rec_{name}_B_destruck.png", up(B))
    cv2.imwrite(f"rec_{name}_C_tone.png", up(C))
    cv2.imwrite(f"rec_{name}_S_strikeonly.png", up(255 - strike))
    print(f"  {name}: crop {crop.shape[1]}x{crop.shape[0]} -> 4 views")


for n in (sys.argv[1:] or REGIONS.keys()):
    process(n)
print("done")
