# Struck-text recovery — folios 19r, 19v, 20r

Second pass. The first pass reported "letterforms visible underneath" and stopped.
It was wrong about *how much* it had found, for two reasons I have to name because
they were both silent failures — the kind that return a confident number instead of
an error.

## Two bugs, both silent

**1. The slanted strike kernels collapsed.** A strike is never level, so the
detector opens the ink layer with a long line at several angles. I built a flat
kernel and rotated it *in place* — a 200 px line tilted 4° rises 14 px, and the box
was 3 px tall, so the rotation clipped the line away to a few stray pixels. **A
near-empty structuring element makes `MORPH_OPEN` a no-op**, which means every ink
pixel in the image came back labelled "strike". The pipeline reported tens of
thousands of strike pixels and looked like it was working. Fixed by drawing the
line into a box sized to hold it, with an assertion so it can never collapse
silently again.

**2. The ink layer was normalised to the crop maximum.** One dark scan artifact at
the page edge stretches the scale; Otsu then picks a high threshold and throws the
real ink away. Several crops came back at **0.02 % ink coverage** — blank — while
still reporting a strike. Fixed with a robust 99.5th-percentile scale, plus a
scan-border rejector.

Both bugs produced *plausible numbers*, not crashes. Recorded here so the same
shape of failure is recognisable next time.

## Method

No coordinates are guessed. Text bands come from each page's own row-ink profile;
every band is then swept.

1. **Ink** — parchment estimated by a large morphological close, subtracted,
   robust-scaled, bilateral-filtered, Otsu.
2. **Strike** — morphological opening with long thin lines at −4°…+4°.
3. **Residual** — ink minus strike.
4. **Bridge** — a struck column is refilled *only* when surviving ink is witnessed
   both above **and** below the strike. That ratio is itself the measurement: it is
   the fraction of the strike that was drawn over writing.
5. **Tone** — strike ink vs text ink separation in B−R, B−G, G−R, in pooled SDs.

## Result — 14 struck bands across 3 folios

| Folio | Band | y-range | strike px | struck columns carrying a letter | tone sep. (max, SD) |
|---|---|---|---|---|---|
| 19r | 2 | 173–318 | 4 650 | 85 / 275 — **30.9 %** | 0.31 |
| 19r | 6 | 827–858 | 5 224 | 177 / 364 — **48.6 %** | 0.06 |
| 19r | 7 | 1152–1187 | 1 603 | 104 / 229 — **45.4 %** | 0.59 |
| 19r | 11 | 1740–1812 | 2 057 | 67 / 236 — **28.4 %** | 0.03 |
| 19r | 16 | 4534–4621 | 6 083 | 190 / 535 — **35.5 %** | 0.64 |
| 19v | 1 | 245–343 | 8 485 | 293 / 670 — **43.7 %** | 0.78 |
| 19v | 4 | 614–879 | 4 965 | 175 / 487 — **35.9 %** | 0.23 |
| 19v | 11 | 4454–4623 | 3 367 | 121 / 269 — **45.0 %** | 0.54 |
| 20r | 13 | 2530–2673 | 2 432 | 21 / 222 — 9.5 % | 1.37 |
| 20r | 15 | 2856–4043 | 8 800 | 384 / 722 — **53.2 %** | 0.88 |
| 20r | 17 | 4131–4907 | 5 858 | 215 / 697 — **30.8 %** | 0.67 |
| 19r 20 · 19v 12 · 20r 19 | — | y ≈ 5790–5847 | 18–24 k | **0 / 800–1000 — 0.0 %** | — |

That last row is the control, and it validates the method: three long horizontal
lines near the foot of all three pages with **zero** columns carrying a letter. A
long level line with nothing under it is a **rule or a scan border, not a strike**.
The detector separates the two without being told to.

## Findings

**F-1 — The strikes are cancellations, not obliterations.** Every one is a *single
thin stroke*, lighter and thinner than the letterforms it crosses. Nothing is
scribbled out. On a page where he could have destroyed a line and did not, the
struck text was meant to stay readable. That is a statement about intent, and it is
measurable: 28–53 % of each strike lies over surviving writing.

**F-2 — The letterforms survive.** Ascenders and descenders cross the strike
unbroken. See `f_19r_b16.png` — the strike passes through a word whose letterforms
are fully intact on both sides, with a **second line of writing entered below it**.
The struck line was **replaced**, not merely dropped.

**F-3 — No tonal separation between strike ink and text ink.** Ten of eleven bands
come in **below 1.0 pooled SD** (median ≈ 0.55); the single exception, 20r band 13,
is 1.37 SD and is also the band with the *lowest* fraction of text underneath
(9.5 %), so it is the weakest case, not the strongest. **The strikes were made with
the same ink as the text.** He struck as he wrote — same sitting, same pen — not on
a later review with a re-dipped pen. The revisions in these folios are part of the
act of composition.

**F-4 — Some of what reads as struck text is verso show-through.** At 8000 px wide
the render makes the leaf's other side visible as faint writing running at its own
angle. Any transcription of these folios has to separate three layers, not two:
recto ink, strike, and bleed-through.

## The limit, stated plainly

Deleting the strike destroys the letter strokes it crosses, so the final render
**dims** the strike (pale red) instead of removing it. Nothing is hidden and
nothing is drawn in — every pixel shown was in the scan.

I can now see the letterforms under the strikes clearly. **I cannot confidently name
them.** That is not a photographic limit any more — the imaging has done its work —
it is my own competence with German Kurrent, and I will not invent readings to
close the gap. Naming them needs one of two things: a Kurrent paleographer reading
these enhanced images, or **multispectral imaging** of the originals at Göttingen
(the Archimedes Palimpsest technique), which separates iron-gall ink layers by
wavelength rather than by tone.

Given F-3, multispectral is the stronger option: tone separation failed *because
there is no tone difference to find*, and a wavelength method does not depend on one.

## Files

`recover.py` — the corrected pipeline (band detection, strike isolation, bridge,
tone test). Outputs `recovery_full.json` and per-band images.
