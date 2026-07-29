"""Final render: grey ink layer, strike shown as colour instead of deleted.

Deleting the strike destroys the letter strokes it crosses. Dimming it instead
keeps every pixel and lets the eye separate the two layers. Text renders black,
strike renders pale red. Nothing removed, nothing drawn in.
"""
import cv2, numpy as np, sys

def grey_ink(bgr, gamma=1.6):
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    bg = cv2.GaussianBlur(cv2.morphologyEx(g, cv2.MORPH_CLOSE,
         cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(61,61))), (81,81), 0)
    d = np.clip(bg.astype(np.int16)-g.astype(np.int16), 0, None).astype(np.float32)
    d /= max(np.percentile(d, 99.5), 1.0)
    d = np.clip(d, 0, 1) ** gamma            # gamma>1 pushes the parchment grain down
    return d                                  # 0 = parchment, 1 = full ink

def line_k(length, ang, thick=3):
    rise = int(abs(np.tan(np.radians(ang)))*length); h = rise+thick
    k = np.zeros((h,length), np.uint8)
    y0,y1 = (thick//2, h-1-thick//2) if ang>=0 else (h-1-thick//2, thick//2)
    cv2.line(k,(0,y0),(length-1,y1),1,thick); return k

def strike_of(d, min_len=200):
    # threshold the ink map the same way the detector did: Otsu, not a magic number
    u = np.clip(d*255,0,255).astype(np.uint8)
    u = cv2.bilateralFilter(u, 9, 60, 60)
    _, bw = cv2.threshold(u, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, np.ones((2,2), np.uint8))
    acc = np.zeros_like(bw)
    for a in (-4,-2.5,-1,0,1,2.5,4):
        acc = np.maximum(acc, cv2.morphologyEx(bw, cv2.MORPH_OPEN, line_k(min_len,a)))
    return cv2.dilate(acc, np.ones((5,3), np.uint8)) > 0

def render(page, y0, y1, tag):
    im = cv2.imread(f"{page}.png"); H,W = im.shape[:2]
    crop = im[y0:y1, int(W*0.06):int(W*0.94)]
    d = grey_ink(crop); st = strike_of(d)
    out = np.full((*d.shape,3), 255, np.uint8)
    text = d*(~st)                                   # ink that is not strike
    strk = d*st                                      # ink that is strike
    for c in range(3):
        out[...,c] = np.clip(255 - text*255, 0, 255)
    # paint strike pale red on top, at a third of its weight
    out[...,0] = np.clip(out[...,0].astype(np.float32) - strk*40,  0,255)   # B down a little
    out[...,1] = np.clip(out[...,1].astype(np.float32) - strk*40,  0,255)   # G down a little
    out[...,2] = np.clip(out[...,2].astype(np.float32) - strk*10,  0,255)   # R barely
    f = 2.2
    big = cv2.resize(out, None, fx=f, fy=f, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(f"f_{tag}.png", big)
    print(f"  f_{tag}.png  {big.shape[1]}x{big.shape[0]}  strike covers "
          f"{100*st.mean():.2f}% of the band")

for tag,(p,a,b) in {
    "19v_top":   ("hi19v", 233, 355),
    "19r_b16":   ("hi19r", 4522, 4633),
    "19r_b06":   ("hi19r", 815,  870),
    "20r_b13":   ("hi20r", 2518, 2685),
}.items():
    render(p,a,b,tag)
