import cv2, numpy as np, sys
def enh(p, out, scale=2.4, gamma=1.25):
    im = cv2.imread(p); g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    bg = cv2.GaussianBlur(cv2.morphologyEx(g, cv2.MORPH_CLOSE,
         cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(41,41))), (61,61), 0)
    d = np.clip(bg.astype(np.int16)-g.astype(np.int16),0,None).astype(np.float32)
    d /= max(np.percentile(d,99.6),1.0); d = np.clip(d,0,1)**gamma
    o = np.clip(255-d*255,0,255).astype(np.uint8)
    o = cv2.resize(o, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(out, o); print(f"  {out}  {o.shape[1]}x{o.shape[0]}")
for f in sys.argv[1:]:
    enh(f"pages/{f}.jpg", f"e_{f}.png")
