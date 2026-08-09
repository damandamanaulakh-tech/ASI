#!/usr/bin/env python3
"""Draw the Universal Sequence Graph with T-1 Gravity and T-2 Pyramids
superimposed, so the breaks are visible at a glance.

Black   = the graph as given
Red     = T-1 GRAVITY
Indigo  = T-2 THE PYRAMIDS

Writes docs/method/SEQUENCE_TESTS_OVERLAY.svg. Render to PNG with chromium.
"""
from __future__ import annotations

import html
from pathlib import Path

BLACK = "#000000"
GREY = "#8A8A8A"
HAIR = "#D8D8D8"
RED = "#D01818"
IND = "#4B0082"
BAND = "#FFF4F4"       # break band, gravity side
BAND_I = "#F4F0FB"     # break band, pyramid side

# status codes
FULL, PART, EMPTY, UNREACH, BORROW, MERGE, NEW = "F", "P", "E", "U", "B", "M", "N"

# (level, label, g_status, g_note, p_status, p_note, break_flag)
#   level 0 = spine node, 1 = sub-node
#   break_flag: "g", "p", "both", or ""
ROWS: list[tuple] = [
    (0, "PRIOR REALITY", FULL, "gravity SEPARATES OUT, not formed", FULL, "Nile surplus · mastaba · Djoser", ""),
    (0, "ORIGIN / SOURCE", PART, "", FULL, "", ""),
    (1, "MATERIAL", MERGE, "one slot with ENERGY — E=mc²", FULL, "Giza + Tura limestone, Aswan granite", "g"),
    (1, "ENERGY", MERGE, "collapsed into MATERIAL", FULL, "muscle, paid in grain", "g"),
    (1, "INFORMATION", EMPTY, "no information channel", FULL, "seked · stellar alignment · Merer's diary", "g"),
    (0, "ENVIRONMENT / HOST", FULL, "", FULL, "", ""),
    (1, "SUBSTRATE", PART, "spacetime — substrate IS the entity", FULL, "Giza bedrock — and the quarry too", "g"),
    (1, "CONDITIONS", FULL, "mass-energy and its distribution", FULL, "flood window · aridity · Memphis", ""),
    (1, "CONSTRAINTS", FULL, "c · equivalence · conservation", FULL, "no iron · KING'S LIFESPAN = deadline", ""),
    (0, "FORMATION SEQUENCE", PART, "", PART, "", ""),
    (1, "assembly", EMPTY, "nothing is put together", FULL, "~2.3 million blocks placed", ""),
    (1, "growth", EMPTY, "does not increase", EMPTY, "assembled, not grown", ""),
    (1, "emergence", FULL, "the only one that fills", EMPTY, "— exact mirror of gravity", "both"),
    (0, "EXISTENCE", PART, "", FULL, "", ""),
    (1, "BOUNDARY", EMPTY, "infinite range, 1/r² — NO boundary", FULL, "sharp; it IS the thing", "g"),
    (1, "IDENTITY", FULL, "the metric", FULL, "Khufu — cartouche in relieving chambers", ""),
    (1, "STATE", FULL, "curvature at every point", FULL, "~138 m now, ~146.6 m originally", ""),
    (0, "STABILITY / VIABILITY", PART, "", FULL, "", ""),
    (1, "YES → continuation", FULL, "cannot fail to persist", FULL, "4,500 years", ""),
    (1, "NO → collapse/repair/term", UNREACH, "UNREACHABLE — no maintenance cost", FULL, "Meidum collapsed · casing stripped", "g"),
    (0, "REQUIREMENT EMERGES", EMPTY, "NO STAKE — 21 nodes go dark here", BORROW, "BORROWED from Khufu / the state", "both"),
    (0, "REQUIREMENT", EMPTY, "gravity needs nothing", FULL, "blocks · flood window · ~20 yrs of state", ""),
    (0, "DEPENDENCY GRAPH", PART, "mass-energy only", FULL, "quarries · Nile · harvest · named gangs", ""),
    (0, "AVAILABILITY", EMPTY, "", FULL, "IMPORT granite · BUILD harbour · WAIT flood", ""),
    (0, "QUALIFICATION", EMPTY, "nothing qualifies anything", FULL, "sound stone? does it fit? is it level?", ""),
    (0, "TESTING", EMPTY, "no test, no tester", FULL, "BENT PYRAMID: 54°→43° MID-BUILD", ""),
    (0, "SELECTION", EMPTY, "no chooser", FULL, "site · ~51.8° · chamber plan", ""),
    (0, "DECISION / CHOICE", EMPTY, "", FULL, "rejected plans still visible in the fabric", ""),
    (0, "ACQUISITION → ENCOUNTER", EMPTY, "masses encounter, they do not acquire", FULL, "quarry / haul / levy", "g"),
    (0, "BOUNDARY APPROACH", EMPTY, "", FULL, "block arrives at the course", ""),
    (0, "INTAKE → COUPLING", EMPTY, "nothing is taken in", FULL, "the block COUPLES to the structure", "g"),
    (0, "TRANSFORMATION → CONDITIONING", EMPTY, "", FULL, "dressing · squaring · polishing", ""),
    (0, "PROCESSING (+propagation)", FULL, "field updates at c — propagation", FULL, "coursing · levelling · load path", ""),
    (0, "ASSIMILATION → INCORPORATION", EMPTY, "", FULL, "the block becomes structure", ""),
    (0, "INTEGRATION", EMPTY, "", FULL, "SAME EVENT AS ASSIMILATION — duplicate", "both"),
    (0, "ACTION", EMPTY, "", PART, "7 of 8 empty — only COMMUNICATE", "p"),
    (0, "OUTPUT", FULL, "gravitational radiation — real energy loss", FULL, "debris · workforce · bureaucracy", ""),
    (0, "RETURN", FULL, "radiation into the wider universe", FULL, "casing stripped for MEDIEVAL CAIRO", ""),
    (0, "RESULT", FULL, "orbit decayed, geometry changed", FULL, "tomb · king buried · plateau altered", ""),
    (0, "IMPACT", PART, "effects yes — 'intended' EMPTY", FULL, "ADVERTISED WHERE THE TREASURE WAS", ""),
    (0, "VERIFICATION", EMPTY, "no requirement to check against", FULL, "FAILED — every pyramid was robbed", ""),
    (0, "FEEDBACK", EMPTY, "reality teaches nobody", FULL, "→ hidden rock-cut tombs. PYRAMIDS END.", ""),
    (0, "MEMORY", FULL, "physical record: CMB · waves · decay", FULL, "all six memory types fill", ""),
    (1, "FAILURE MEMORY", EMPTY, "", FULL, "Meidum collapsed; 54° too steep", ""),
    (0, "MEMORY VALIDATION", EMPTY, "", PART, "PARTLY NO — the HOW was lost", ""),
    (0, "COMPRESSION", FULL, "no-hair theorem — mass, spin, charge only", PART, "'tombs' — method not recoverable", ""),
    (0, "INHERITANCE", PART, "", FULL, "", ""),
    (1, "biological", EMPTY, "", EMPTY, "", ""),
    (1, "individual / social / technical", EMPTY, "none of the four lanes fits", FULL, "guild skill · scribal record · tools", ""),
    (1, "PHYSICAL  ← new lane needed", NEW, "initial conditions: angular momentum, mass", EMPTY, "", "g"),
    (0, "NEXT-SEQUENCE SEED", PART, "", FULL, "", ""),
    (0, "RE-ENTRY POINT", EMPTY, "", FULL, "Sneferu → Khufu at the corrected angle", ""),
    (0, "EXECUTION", EMPTY, "", FULL, "", ""),
    (0, "RE-VERIFY", EMPTY, "", FULL, "", ""),
    (0, "MEMORY UPDATE", EMPTY, "", FULL, "", ""),
]

# ---------------------------------------------------------------- geometry
COL_W = 1060
LABEL_X = 24
DOT_G_X = 402
DOT_P_X = 428
NOTE_G_X = 452
NOTE_P_X = 762
ROW_H0 = 40          # spine row
ROW_H1 = 30          # sub row
HEAD_H = 250
PAD = 62
GUT = 74


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def dot(x: float, y: float, code: str, colour: str) -> str:
    """Status glyph. F filled · P half · E hollow · U slashed · B ringed · M linked
    · N starred."""
    r = 7.0
    if code == FULL:
        return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{colour}"/>'
    if code == PART:
        return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{colour}" '
                f'stroke-width="1.8"/>'
                f'<path d="M {x} {y-r} A {r} {r} 0 0 0 {x} {y+r} Z" fill="{colour}"/>')
    if code == EMPTY:
        return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{colour}" '
                f'stroke-width="1.8" stroke-dasharray="2.2 2.2"/>')
    if code == UNREACH:
        return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{colour}" '
                f'stroke-width="1.8"/>'
                f'<line x1="{x-r-1.5}" y1="{y+r+1.5}" x2="{x+r+1.5}" y2="{y-r-1.5}" '
                f'stroke="{colour}" stroke-width="2"/>')
    if code == BORROW:
        return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{colour}" '
                f'stroke-width="1.8"/>'
                f'<circle cx="{x}" cy="{y}" r="2.6" fill="{colour}"/>')
    if code == MERGE:
        return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{colour}" '
                f'stroke-width="1.8"/>'
                f'<line x1="{x-r+1}" y1="{y}" x2="{x+r-1}" y2="{y}" '
                f'stroke="{colour}" stroke-width="2.4"/>')
    # NEW
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{colour}"/>'
            f'<circle cx="{x}" cy="{y}" r="{r+3.5}" fill="none" stroke="{colour}" '
            f'stroke-width="1.2" stroke-dasharray="1.8 1.8"/>')


def build() -> str:
    # split into two columns at a spine boundary near the middle
    total = sum(ROW_H0 if r[0] == 0 else ROW_H1 for r in ROWS)
    split, run = 0, 0
    for i, r in enumerate(ROWS):
        run += ROW_H0 if r[0] == 0 else ROW_H1
        if run >= total / 2 and r[0] == 0:
            split = i
            break
    cols = [ROWS[:split], ROWS[split:]]

    def col_height(rows) -> float:
        return sum(ROW_H0 if r[0] == 0 else ROW_H1 for r in rows)

    body_h = max(col_height(c) for c in cols)
    W = PAD * 2 + COL_W * 2 + GUT
    H = HEAD_H + body_h + 250

    out: list[str] = []
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
               f'viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">')
    out.append(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')

    # ---- header
    out.append(f'<text x="{PAD}" y="72" font-size="46" font-weight="700" '
               f'fill="{BLACK}" letter-spacing="-1">UNIVERSAL SEQUENCE GRAPH '
               f'— TWO TESTS SUPERIMPOSED</text>')
    out.append(f'<text x="{PAD}" y="112" font-size="21" fill="{GREY}">'
               f'The graph in black. Where each test fills a node, and where it '
               f'breaks.</text>')

    lx = PAD
    out.append(f'<rect x="{lx}" y="140" width="16" height="16" fill="{RED}"/>')
    out.append(f'<text x="{lx+26}" y="154" font-size="21" font-weight="700" '
               f'fill="{RED}">T-1  GRAVITY</text>')
    out.append(f'<text x="{lx+215}" y="154" font-size="19" fill="{RED}">'
               f'11 of 37 fill</text>')
    out.append(f'<rect x="{lx+400}" y="140" width="16" height="16" fill="{IND}"/>')
    out.append(f'<text x="{lx+426}" y="154" font-size="21" font-weight="700" '
               f'fill="{IND}">T-2  THE PYRAMIDS</text>')
    out.append(f'<text x="{lx+665}" y="154" font-size="19" fill="{IND}">'
               f'33 of 37 fill</text>')

    # ---- key
    ky = 196
    key = [(FULL, "fills"), (PART, "partial"), (EMPTY, "empty"),
           (UNREACH, "unreachable"), (BORROW, "borrowed"),
           (MERGE, "merged"), (NEW, "new lane")]
    kx = PAD
    out.append(f'<text x="{kx}" y="{ky+5}" font-size="17" font-weight="700" '
               f'fill="{BLACK}">KEY</text>')
    kx += 52
    for code, name in key:
        out.append(dot(kx, ky, code, BLACK))
        out.append(f'<text x="{kx+14}" y="{ky+5}" font-size="16" fill="{GREY}">'
                   f'{esc(name)}</text>')
        kx += 26 + len(name) * 8.6 + 22
    out.append(f'<text x="{kx+10}" y="{ky+5}" font-size="16" fill="{BLACK}" '
               f'font-weight="700">tinted band = a structural break</text>')

    out.append(f'<line x1="{PAD}" y1="{HEAD_H-26}" x2="{W-PAD}" y2="{HEAD_H-26}" '
               f'stroke="{BLACK}" stroke-width="2"/>')

    # ---- columns
    for ci, rows in enumerate(cols):
        ox = PAD + ci * (COL_W + GUT)
        y = HEAD_H
        # column header
        out.append(f'<text x="{ox+DOT_G_X-8}" y="{y-6}" font-size="14" '
                   f'font-weight="700" fill="{RED}">G</text>')
        out.append(f'<text x="{ox+DOT_P_X-7}" y="{y-6}" font-size="14" '
                   f'font-weight="700" fill="{IND}">P</text>')
        # continuous spine rule
        out.append(f'<line x1="{ox+14}" y1="{y}" x2="{ox+14}" y2="{y+col_height(rows)}" '
                   f'stroke="{HAIR}" stroke-width="2"/>')

        for lvl, label, gs, gn, ps, pn, brk in rows:
            h = ROW_H0 if lvl == 0 else ROW_H1
            mid = y + h / 2

            if brk in ("g", "both"):
                out.append(f'<rect x="{ox+NOTE_G_X-14}" y="{y+1}" '
                           f'width="{NOTE_P_X-NOTE_G_X}" height="{h-2}" fill="{BAND}"/>')
            if brk in ("p", "both"):
                out.append(f'<rect x="{ox+NOTE_P_X-14}" y="{y+1}" '
                           f'width="{COL_W-NOTE_P_X}" height="{h-2}" fill="{BAND_I}"/>')

            if lvl == 0:
                out.append(f'<rect x="{ox+14}" y="{mid-9}" width="7" height="18" '
                           f'fill="{BLACK}"/>')
                out.append(f'<text x="{ox+LABEL_X+8}" y="{mid+6}" font-size="17" '
                           f'font-weight="700" fill="{BLACK}">{esc(label)}</text>')
            else:
                out.append(f'<line x1="{ox+14}" y1="{mid}" x2="{ox+LABEL_X+14}" '
                           f'y2="{mid}" stroke="{GREY}" stroke-width="1.4"/>')
                out.append(f'<text x="{ox+LABEL_X+22}" y="{mid+5}" font-size="15" '
                           f'fill="{GREY}">{esc(label)}</text>')

            out.append(dot(ox + DOT_G_X, mid, gs, RED))
            out.append(dot(ox + DOT_P_X, mid, ps, IND))

            if gn:
                out.append(f'<text x="{ox+NOTE_G_X}" y="{mid+5}" font-size="14" '
                           f'fill="{RED}">{esc(gn)}</text>')
            if pn:
                out.append(f'<text x="{ox+NOTE_P_X}" y="{mid+5}" font-size="14" '
                           f'fill="{IND}">{esc(pn)}</text>')

            out.append(f'<line x1="{ox+14}" y1="{y+h}" x2="{ox+COL_W-10}" y2="{y+h}" '
                       f'stroke="{HAIR}" stroke-width="0.8"/>')
            y += h

    # ---- the gravity-dark bracket: the run starts in one column and finishes
    # in the next, so bracket whatever part of it each column holds.
    DARK_START, DARK_END = "REQUIREMENT EMERGES", "ACTION"
    for ci, rows in enumerate(cols):
        labels = [r[1] for r in rows]
        started = any(l == DARK_START for l in labels)
        # is the run already open when this column begins?
        prior = [r[1] for c in cols[:ci] for r in c]
        open_at_top = (DARK_START in prior) and (DARK_END not in prior)
        if not (started or open_at_top):
            continue
        ox = PAD + ci * (COL_W + GUT)
        yy = HEAD_H
        first = HEAD_H if open_at_top else None
        last = None
        for lvl, label, gs, gn, ps, pn, brk in rows:
            h = ROW_H0 if lvl == 0 else ROW_H1
            if label == DARK_START:
                first = yy
            if label == DARK_END:
                last = yy + h
            yy += h
        if first is None:
            continue
        if last is None:
            last = yy
        bx = ox - 20
        out.append(f'<path d="M {bx} {first} L {bx-13} {first} L {bx-13} {last} '
                   f'L {bx} {last}" fill="none" stroke="{RED}" stroke-width="3"/>')
        cy = (first + last) / 2
        tag = ("GRAVITY DARK — 21 NODES" if ci == 0 else "\u2026 STILL DARK")
        out.append(f'<text x="{bx-22}" y="{cy}" font-size="14.5" '
                   f'font-weight="700" fill="{RED}" text-anchor="middle" '
                   f'transform="rotate(-90 {bx-22} {cy})">{tag}</text>')

    # ---- footer findings
    fy = HEAD_H + body_h + 44
    out.append(f'<line x1="{PAD}" y1="{fy-26}" x2="{W-PAD}" y2="{fy-26}" '
               f'stroke="{BLACK}" stroke-width="2"/>')
    out.append(f'<text x="{PAD}" y="{fy}" font-size="18" font-weight="700" '
               f'fill="{BLACK}">WHAT BREAKS</text>')
    findings = [
        (RED, "GRAVITY  ·  no BOUNDARY · MATERIAL and ENERGY are one slot · the NO "
              "branch is unreachable · no stake, so 21 nodes go dark at once"),
        (IND, "PYRAMIDS  ·  the REQUIREMENT is not its own, it is BORROWED from its "
              "maker · ACTION collapses to signalling, 7 of 8 empty"),
        (BLACK, "BOTH  ·  ASSIMILATION and INTEGRATION are the same event · "
                "hunger-minted words fail: intake→COUPLING, cooking→CONDITIONING, "
                "harvest→ENCOUNTER, +PHYSICAL inheritance lane"),
    ]
    for i, (col, txt) in enumerate(findings):
        out.append(f'<rect x="{PAD}" y="{fy+18+i*26}" width="11" height="11" '
                   f'fill="{col}"/>')
        out.append(f'<text x="{PAD+20}" y="{fy+28+i*26}" font-size="15.5" '
                   f'fill="{col}">{esc(txt)}</text>')

    out.append('</svg>')
    return "\n".join(out)


if __name__ == "__main__":
    dest = Path(__file__).with_name("SEQUENCE_TESTS_OVERLAY.svg")
    dest.write_text(build(), encoding="utf-8")
    print(f"wrote {dest}")
