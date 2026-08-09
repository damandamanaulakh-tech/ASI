#!/usr/bin/env python3
"""Two pictures of the sequence at its settled shape.

CHART A — SEQUENCE_ARROW_CHART.svg
    The sequence drawn as arrows. Every stage on the main line, every
    threshold sitting on the edge that enters a stage, every spawn out to a
    sub-sequence with its return, and every loop drawn as an arc that lands
    on the stage it actually lands on. Nothing collapsed, nothing skipped.

CHART B — SEQUENCE_CHANGES_OVERLAY.svg
    The same skeleton in black with every change superimposed, one colour
    per change, so it is visible which stage each change touches.

Both write SVG here; render to PNG with chromium.
"""
from __future__ import annotations

import html
from pathlib import Path

# ------------------------------------------------------------------ palette
BLACK = "#000000"
GREY = "#8A8A8A"
HAIR = "#DCDCDC"
FAINT = "#F2F2F2"

C1 = "#D01818"   # threshold on edges
C2 = "#4B0082"   # sequence closure != entity outcome
C3 = "#0F7B3E"   # sub-sequence contract
C4 = "#B26B00"   # open-sequence ledger + barrier law
C5 = "#C2007A"   # driver origin, Want beside Need
C6 = "#007B8A"   # controller mandatory
C7 = "#E05A00"   # PASS 0 — declare the end first
C8 = "#6D4C00"   # the Mahabharata primitives
C9 = "#8A8A8A"   # struck from earlier versions

CHANGES = [
    ("C1", C1, "THRESHOLD ON THE EDGE",
     "separated from the trigger; it is what answers WHY NOW"),
    ("C2", C2, "SEQUENCE CLOSURE ≠ ENTITY OUTCOME",
     "two statuses, never one"),
    ("C3", C3, "SUB-SEQUENCE CONTRACT",
     "close_condition ≠ acceptance_condition"),
    ("C4", C4, "OPEN-SEQUENCE LEDGER + BARRIER LAW",
     "the line cannot cross an unaccepted return"),
    ("C5", C5, "DRIVER ORIGIN — WANT beside NEED",
     "nine origins; want is not folded into need"),
    ("C6", C6, "CONTROLLER MANDATORY",
     "none-natural / self / distributed / external / joint / meta"),
    ("C7", C7, "PASS 0 — DECLARE THE END FIRST",
     "the end decides which earlier reality matters"),
    ("C8", C8, "THE MAHABHARATA PRIMITIVES",
     "thirteen named patterns — doc, deliberately not code"),
    ("C9", C9, "STRUCK FROM EARLIER VERSIONS",
     "removed, and kept visible so they cannot creep back"),
]

# ------------------------------------------------------------------- stages
# (level, name, structural note)   level 0 = main line, 1 = inside a stage
STAGES: list[tuple[int, str, str]] = [
    (0, "PRIOR REALITY", "declared by the human — not discovered by the walk"),
    (0, "ORIGIN / SOURCE", "the seed. It can be OLDER than the thing that carries it"),
    (1, "MATERIAL", "what it is made of"),
    (1, "ENERGY", "what moves it"),
    (1, "INFORMATION", "who knew what, and when"),
    (0, "ENVIRONMENT / HOST", "where it runs"),
    (1, "SUBSTRATE", "what it stands on"),
    (1, "CONDITIONS", "what must be true at that moment"),
    (1, "CONSTRAINTS", "what may not be crossed — exceptions carry terms"),
    (0, "FORMATION SEQUENCE", "how it comes together"),
    (1, "assembly", "parts put together"),
    (1, "growth", "increase from inside"),
    (1, "emergence", "appears without being assembled"),
    (0, "EXISTENCE", "it is a thing now"),
    (1, "BOUNDARY", "where it stops — can be absent, and absence is a finding"),
    (1, "IDENTITY", "what names it"),
    (1, "STATE", "its condition, readable at any point"),
    (0, "STABILITY / VIABILITY", "can it keep going"),
    (1, "YES → continuation", "it persists"),
    (1, "NO → collapse / repair / terminate", "this is the ENTITY, not the sequence"),
    (0, "REQUIREMENT EMERGES", "the driver. Nine origins — and one of them is WANT"),
    (0, "REQUIREMENT", "what is actually needed, stated in the open"),
    (0, "DEPENDENCY GRAPH", "what that needs, and what that needs"),
    (0, "AVAILABILITY", "is it there — LOCATE / BUILD / SUBSTITUTE"),
    (0, "QUALIFICATION", "does it fit"),
    (0, "TESTING", "does it hold"),
    (0, "SELECTION", "which one"),
    (0, "DECISION / CHOICE", "who decided, and by what priority"),
    (0, "ACQUISITION → ENCOUNTER", "it is met — and meeting is CONDITIONAL"),
    (0, "BOUNDARY APPROACH", "it arrives at the edge"),
    (0, "INTAKE → COUPLING", "it joins"),
    (0, "TRANSFORMATION → CONDITIONING", "it is made fit"),
    (0, "PROCESSING (+ propagation)", "the work, and how far the work carries"),
    (0, "ASSIMILATION → INCORPORATION", "it becomes the thing"),
    (0, "INTEGRATION", "same event as the row above — flagged, not deleted"),
    (0, "ACTION", "what it does outward"),
    (0, "OUTPUT", "what leaves it"),
    (0, "RETURN", "what goes back to the wider system"),
    (0, "RESULT", "what changed — can be LATENT: exists, has not fired"),
    (0, "IMPACT", "what it changed for everyone else"),
    (0, "VERIFICATION", "checked against the requirement, not against the wish"),
    (0, "FEEDBACK", "what reality taught — can end the whole class of sequence"),
    (0, "MEMORY", "what is kept"),
    (1, "FAILURE MEMORY", "what must not be done again"),
    (0, "MEMORY VALIDATION", "is the memory true — and by how many witnesses"),
    (0, "COMPRESSION", "what survives being shortened"),
    (0, "INHERITANCE", "what is handed on"),
    (1, "biological", ""),
    (1, "individual / social / technical", ""),
    (1, "PHYSICAL", "the lane the gravity walk forced open"),
    (0, "SEQUENCE CLOSURE", "SUCCESS · FAILURE · PARTIAL · UNKNOWN · UNAVAILABLE · N-A"),
    (0, "ENTITY OUTCOME", "persists · coheres · degrades · terminates — never 'closed'"),
    (0, "NEXT-SEQUENCE SEED", "S₁ REFERENCES S₀. S₀ does not reopen"),
    (0, "RE-ENTRY POINT", "where S₁ starts — not where S₀ stopped"),
    (0, "EXECUTION", "S₁ runs, on its own ledger row"),
    (0, "RE-VERIFY", "against the corrected requirement"),
    (0, "MEMORY UPDATE", "the ledger row closes, and the declared end is checked"),
]

# threshold on the edge ENTERING this stage: name -> (type, why now)
THRESHOLDS: dict[str, tuple[str, str]] = {
    "CONDITIONS": ("TIME", "the window opens"),
    "FORMATION SEQUENCE": ("COMPOSITE", "material + host + conditions all true"),
    "EXISTENCE": ("STATE", "the boundary closes"),
    "STABILITY / VIABILITY": ("EVENT", "first load applied"),
    "NO → collapse / repair / terminate": ("ABSENCE", "maintenance stops"),
    "REQUIREMENT EMERGES": ("VALUE", "the driver crosses the line into acting"),
    "AVAILABILITY": ("STATE", "the requirement is named"),
    "QUALIFICATION": ("EVENT", "a candidate is present"),
    "TESTING": ("STATE", "the candidate qualifies"),
    "SELECTION": ("CONFIDENCE", "the test returns"),
    "DECISION / CHOICE": ("COUNT·QUORUM", "authority or quorum reached"),
    "ACQUISITION → ENCOUNTER": ("EVENT", "the encounter actually happens"),
    "INTAKE → COUPLING": ("RANGE", "the boundary is reached"),
    "PROCESSING (+ propagation)": ("STATE", "coupling holds"),
    "ACTION": ("STATE", "processing complete"),
    "VERIFICATION": ("EVENT", "a result exists to check"),
    "FEEDBACK": ("CONFIDENCE", "verification returns"),
    "MEMORY VALIDATION": ("COUNT·QUORUM", "a second independent witness"),
    "SEQUENCE CLOSURE": ("LEDGER", "every required return accepted"),
    "ENTITY OUTCOME": ("STATE", "read at the moment of closure"),
    "RE-ENTRY POINT": ("EVENT", "the seed is accepted"),
    "MEMORY UPDATE": ("CONFIDENCE", "re-verify passes"),
}

# spawns: (at stage, sub-sequence name, close_condition, acceptance_condition,
#          accepted?)
SPAWNS: list[tuple[str, str, str, str, bool]] = [
    ("AVAILABILITY", "SUB-SEQ  LOCATE", "search finished",
     "material in hand", False),
    ("AVAILABILITY", "SUB-SEQ  BUILD", "attempt finished",
     "material in hand", False),
    ("AVAILABILITY", "SUB-SEQ  SUBSTITUTE", "substitute found",
     "material in hand", True),
    ("TESTING", "SUB-SEQ  RE-ANGLE", "new angle set",
     "the structure holds", True),
    ("VERIFICATION", "SUB-SEQ  REPAIR", "repair carried out",
     "the requirement is met", True),
    ("MEMORY VALIDATION", "SUB-SEQ  SECOND WITNESS", "search finished",
     "two independent accounts", False),
]

# loops: (id, from stage, to stage, name, what fires it, what it means)
LOOPS: list[tuple[str, str, str, str, str, str]] = [
    ("L1", "AVAILABILITY", "AVAILABILITY",
     "THE AVAILABILITY FAN",
     "locate fails, then build fails",
     "three SUB-SEQUENCES side by side — not one node run three times. "
     "The node closes when ANY sibling is accepted."),
    ("L2", "QUALIFICATION", "SELECTION",
     "DOES NOT FIT",
     "the fit test fails",
     "a new sub-sequence with a different candidate"),
    ("L3", "TESTING", "DECISION / CHOICE",
     "FAILS MID-SEQUENCE",
     "54° proves too steep",
     "the Bent Pyramid — the angle was changed while the thing was "
     "half-built"),
    ("L4", "NO → collapse / repair / terminate", "REQUIREMENT EMERGES",
     "DAMAGE DRIVES A NEW SEQUENCE",
     "the entity degrades",
     "driver origin = DAMAGE. The entity's outcome opens a fresh sequence"),
    ("L5", "VERIFICATION", "REQUIREMENT",
     "VERIFY FAILS",
     "result ≠ requirement",
     "the requirement is restated, never quietly patched"),
    ("L6", "FEEDBACK", "PRIOR REALITY",
     "THE ERA CLOSES",
     "every pyramid was robbed",
     "the whole class of sequence ends; the next one begins somewhere else "
     "— hidden rock-cut tombs"),
    ("L7", "MEMORY VALIDATION", "INFORMATION",
     "MEMORY UNPROVEN",
     "one witness only",
     "capped at Medium. Two witnesses that differ HALT — the gap is the "
     "Mask and it goes to the human"),
    ("L8", "COMPRESSION", "MEMORY",
     "COMPRESSION LOST THE HOW",
     "the method is not recoverable",
     "a defect in a record; the whole point in a body"),
    ("L9", "MEMORY UPDATE", "ORIGIN / SOURCE",
     "HALT BECOMES THE NEXT POINT ZERO",
     "the halt is named",
     "S₁ REFERENCES S₀. S₀ stays closed — there is no reopen"),
    ("L10", "DECISION / CHOICE", "SELECTION",
     "A HELD ALTERNATIVE TAKEN UP",
     "the chosen path is rejected downstream",
     "held alternatives are kept, never discarded — one re-enters as a NEW "
     "sub-sequence. Drawn on his word; validation pending the first live case"),
    ("L11", "RETURN", "ENVIRONMENT / HOST",
     "THE RUN CHANGES ITS OWN GROUND · UNVALIDATED",
     "the sequence alters the conditions it runs in",
     "an earlier threshold must be re-read. UNVALIDATED — awaiting T-5"),
]

# barriers sit on the main line where a return is outstanding
BARRIERS = ["AVAILABILITY", "TESTING", "VERIFICATION", "MEMORY VALIDATION"]

# ------------------------------------------------ the changes, stage by stage
ATTACH: dict[str, list[tuple[str, str]]] = {
    "PRIOR REALITY": [
        ("C7", "the END is declared BEFORE this is looked for. Without that "
               "the reverse walk expands forever."),
    ],
    "ORIGIN / SOURCE": [
        ("C8", "P1 SEED BEFORE CARRIER — the cause can be older than the "
               "thing that carries it. Karna's seed is older than Karna."),
        ("C9", "struck: the word “child”. It implied younger, and it "
               "implied software recursion. It is a SUB-SEQUENCE."),
    ],
    "INFORMATION": [
        ("C8", "P2 ACTOR VIEW — the same event is a different sequence for "
               "each actor, according to what that actor knew."),
        ("C9", "struck: filling a gap with an invented source. The gap stays a "
               "gap and goes to the human."),
    ],
    "CONDITIONS": [
        ("C1", "threshold TIME — the window opening is why it happens NOW."),
        ("C8", "P7 CONVERGENCE WINDOW — several sequences must land inside "
               "one window or nothing happens."),
    ],
    "CONSTRAINTS": [
        ("C8", "P4 EXCEPTION CONTRACT — a rule bent once, with terms. The "
               "terms are the code, not the bending."),
    ],
    "FORMATION SEQUENCE": [
        ("C1", "the threshold sits on the EDGE entering this stage. It was "
               "wrongly held inside the state before."),
    ],
    "STATE": [
        ("C8", "P6 DOWNSTREAM-CRITICAL CHANGE — small now, decisive far "
               "later."),
    ],
    "STABILITY / VIABILITY": [
        ("C1", "threshold EVENT — first load applied."),
    ],
    "NO → collapse / repair / terminate": [
        ("C2", "this is the ENTITY's outcome. It is not the sequence closing. "
               "Collapsing these two was the worst error in every earlier "
               "version."),
        ("C1", "threshold ABSENCE — what fires it is that maintenance "
               "STOPS. Absence is a threshold type."),
    ],
    "REQUIREMENT EMERGES": [
        ("C5", "nine driver origins, and WANT sits beside NEED — never "
               "folded into it. Gravity has NATURAL DYNAMICS and no driver at "
               "all; that is a real value, not a missing one."),
        ("C6", "the CONTROLLER is named here: none-natural · self · "
               "distributed-self · external · joint · meta."),
        ("C8", "P12 REPRESENTED FUTURE — a sequence acted on because it was "
               "foretold, not because it happened."),
    ],
    "REQUIREMENT": [
        ("C8", "P11 PROMISE AS CODE — a vow binds future transitions. "
               "Bhishma."),
    ],
    "AVAILABILITY": [
        ("C3", "SPAWN. close_condition ≠ acceptance_condition — a "
               "sub-sequence can close and still not be accepted."),
        ("C4", "a LEDGER row opens. BARRIER: the main line cannot cross this "
               "node while a required return is unaccepted."),
        ("C9", "struck: the in-place retry. LOCATE → BUILD → SUBSTITUTE "
               "are three sub-sequences, not one node run three times."),
    ],
    "QUALIFICATION": [
        ("C1", "threshold EVENT — a candidate is present."),
    ],
    "TESTING": [
        ("C3", "spawn RE-ANGLE: closed at “new angle set”, accepted "
               "only when the structure holds."),
    ],
    "SELECTION": [
        ("C8", "P3 PRIORITY / ARBITRATION — two rules both apply; name what "
               "decides between them."),
    ],
    "DECISION / CHOICE": [
        ("C6", "the controller is recorded here, not assumed."),
        ("C9", "struck: blending two surviving reasons. Two survivors HALT."),
    ],
    "ACQUISITION → ENCOUNTER": [
        ("C1", "threshold EVENT — and the encounter is CONDITIONAL. Two "
               "sequences meeting is never an assumption."),
    ],
    "INTAKE → COUPLING": [
        ("C1", "threshold RANGE — the boundary is reached."),
    ],
    "RESULT": [
        ("C8", "P5 LATENT RESULT — it exists and it has not fired. Waiting "
               "is a state."),
    ],
    "OUTPUT": [
        ("C8", "P13 RESULT MULTIPLICATION — one transition, many results, "
               "on many lines, at different times."),
    ],
    "VERIFICATION": [
        ("C3", "spawn REPAIR: closes when the repair is done, accepted only "
               "when the requirement is met."),
    ],
    "FEEDBACK": [
        ("C1", "threshold CONFIDENCE — verification returns."),
    ],
    "MEMORY": [
        ("C8", "P9 OBSERVER / WRITER — the record is its own sequence with "
               "its own intent. Sanjaya is not a camera."),
    ],
    "MEMORY VALIDATION": [
        ("C1", "threshold COUNT·QUORUM — a second independent witness."),
        ("C9", "struck: averaging two witnesses that differ. That HALTS; the "
               "gap is the Mask."),
    ],
    "INHERITANCE": [
        ("C8", "P10 RULE INERTIA — the rule keeps running after the reason "
               "for it is gone."),
    ],
    "SEQUENCE CLOSURE": [
        ("C2", "NEW STAGE. Six values, and they belong to the SEQUENCE."),
        ("C4", "it can only close when the ledger is empty."),
        ("C8", "P8 CLOSURE SCOPE — whose closure. A war closing is not a "
               "family closing."),
        ("C9", "struck: the word CLOSURE used of an entity."),
    ],
    "ENTITY OUTCOME": [
        ("C2", "NEW STAGE. Thirteen values — persists, coheres, degrades, "
               "terminates — and none of them is “closed”."),
    ],
    "NEXT-SEQUENCE SEED": [
        ("C9", "struck: reopening S₀. S₁ REFERENCES S₀ and S₀ "
               "stays closed."),
    ],
    "RE-ENTRY POINT": [
        ("C1", "threshold EVENT — the seed is accepted."),
    ],
    "MEMORY UPDATE": [
        ("C7", "the end PASS 0 declared is checked here: did we arrive at the "
               "reality we named at the start?"),
    ],
}

INVARIANTS = [
    "BARRIER LAW — the line cannot cross a node while a required return is "
    "unaccepted",
    "NO IN-PLACE LOOP — a sequence never re-enters a stage it has left; a "
    "retry is a new sub-sequence",
    "NO REOPEN — a closed sequence stays closed; S₁ references S₀",
    "CLOSURE IS A SEQUENCE WORD — entities persist, cohere, degrade, "
    "terminate",
    "ENCOUNTER IS CONDITIONAL — two sequences meeting is an event with a "
    "condition",
    "NEVER MANUFACTURE A SOURCE — a gap stays a gap, and the gap goes to "
    "the human",
]

H0, H1 = 54, 40      # main-line row, inside-stage row

# white halo, so a rotated label stays readable where a line crosses it
HALO = ('paint-order="stroke" stroke="#FFFFFF" stroke-width="4.5" '
        'stroke-linejoin="round" ')


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def wrap(text: str, width: int) -> list[str]:
    """Greedy wrap by character count."""
    out, line = [], ""
    for word in text.split():
        cand = f"{line} {word}".strip()
        if len(cand) > width and line:
            out.append(line)
            line = word
        else:
            line = cand
    if line:
        out.append(line)
    return out


def row_layout(heights: list[int]) -> list[float]:
    """Mid-y of each row, given a head offset applied by the caller."""
    mids, y = [], 0.0
    for h in heights:
        mids.append(y + h / 2)
        y += h
    return mids


# ============================================================== CHART A
def build_arrow_chart() -> str:
    PAD = 60
    PASS_X = [90, 124, 158]
    SPAWN_L, SPAWN_R = 210, 700
    CH_OUT, CH_IN = 752, 726
    SPINE = 900
    LABEL_X = 940
    NOTE_X = 1520
    ARC_X0 = 2210
    STUB_X = 2040        # right of every note — the only clear vertical strip
    LANE_STEP = 92
    HEAD = 320

    heights = [H0 if s[0] == 0 else H1 for s in STAGES]
    mids = [HEAD + m for m in row_layout(heights)]
    index = {s[1]: i for i, s in enumerate(STAGES)}
    body_h = sum(heights)
    lanes = {lp[0]: ARC_X0 + 60 + i * LANE_STEP for i, lp in enumerate(LOOPS)}
    W = max(lanes.values()) + 150
    foot_lines = 3 + len(INVARIANTS) + 2 + len(LOOPS)
    H = HEAD + body_h + 90 + foot_lines * 27 + 80

    y_of = {s[1]: mids[i] for i, s in enumerate(STAGES)}

    o: list[str] = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">')
    o.append(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')

    # arrowhead markers
    o.append('<defs>')
    for name, col in [("k", BLACK), ("g", GREY), ("t", C1), ("s", C3),
                      ("o", C7), ("a", C4)]:
        o.append(f'<marker id="ah{name}" viewBox="0 0 10 10" refX="9" refY="5" '
                 f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                 f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{col}"/></marker>')
    for lid, *_ in LOOPS:
        o.append(f'<marker id="ahL{lid}" viewBox="0 0 10 10" refX="9" refY="5" '
                 f'markerWidth="7.5" markerHeight="7.5" '
                 f'orient="auto-start-reverse">'
                 f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{C1}"/></marker>')
    o.append('</defs>')

    # ---- header
    o.append(f'<text x="{PAD}" y="76" font-size="50" font-weight="700" '
             f'fill="{BLACK}" letter-spacing="-1.2">THE SEQUENCE — ARROW '
             f'CHART</text>')
    o.append(f'<text x="{PAD}" y="118" font-size="22" fill="{GREY}">'
             f'Every stage on the main line. Every threshold on the edge that '
             f'enters a stage. Every spawn out to its sub-sequence, with its '
             f'return. Every loop drawn where it actually lands.</text>')
    n_thr = len(THRESHOLDS)
    o.append(f'<text x="{PAD}" y="158" font-size="21" font-weight="700" '
             f'fill="{BLACK}">{len(STAGES)} stages · {n_thr} thresholds '
             f'· {len(SPAWNS)} spawns · {len(LOOPS)} routes (registry v1, '
             f'non-exhaustive) · {len(BARRIERS)} barriers — nothing collapsed '
             f'· his name for this structure: THE MAHABHARATA SEQUENCE — the '
             f'method every response passes, reverse → forward → reverse</text>')

    # key
    ky = 196
    keys = [(BLACK, "the main line, and the transition arrow between stages"),
            (C1, "threshold on the edge — why it fires NOW"),
            (C3, "spawn out to a sub-sequence, and its return"),
            (C4, "barrier — the line is held here"),
            (C7, "PASS 0 and the three passes")]
    for i, (col, txt) in enumerate(keys):
        yy = ky + i * 24
        o.append(f'<rect x="{PAD}" y="{yy-9}" width="12" height="12" '
                 f'fill="{col}"/>')
        o.append(f'<text x="{PAD+22}" y="{yy+2}" font-size="16" fill="{col}">'
                 f'{esc(txt)}</text>')

    # PASS 0 box
    px = SPINE - 190
    o.append(f'<rect x="{px}" y="{HEAD-118}" width="640" height="66" '
             f'fill="none" stroke="{C7}" stroke-width="3"/>')
    o.append(f'<text x="{px+18}" y="{HEAD-90}" font-size="21" '
             f'font-weight="700" fill="{C7}">PASS 0 — DECLARE THE END</text>')
    o.append(f'<text x="{px+18}" y="{HEAD-66}" font-size="15.5" fill="{C7}">'
             f'name the reality claimed at the finish, before looking for any '
             f'beginning</text>')
    o.append(f'<line x1="{SPINE}" y1="{HEAD-52}" x2="{SPINE}" y2="{HEAD-8}" '
             f'stroke="{C7}" stroke-width="3" marker-end="url(#aho)"/>')

    # ---- the three passes, on the left
    top, bot = HEAD + 6, HEAD + body_h - 6
    passes = [("PASS 1  END → START   the required chain", True),
              ("PASS 2  START → END   the available chain", False),
              ("PASS 3  END → START   the gap list", True)]
    for i, (label, upward) in enumerate(passes):
        x = PASS_X[i]
        if upward:
            o.append(f'<line x1="{x}" y1="{bot}" x2="{x}" y2="{top}" '
                     f'stroke="{C7}" stroke-width="2.4" '
                     f'marker-end="url(#aho)"/>')
        else:
            o.append(f'<line x1="{x}" y1="{top}" x2="{x}" y2="{bot}" '
                     f'stroke="{C7}" stroke-width="2.4" '
                     f'marker-end="url(#aho)"/>')
        cy = (top + bot) / 2
        o.append(f'<text x="{x-7}" y="{cy}" font-size="16" font-weight="700" '
                 f'fill="{C7}" text-anchor="middle" {HALO}'
                 f'transform="rotate(-90 {x-7} {cy})">{esc(label)}</text>')

    o.append(f'<line x1="{STUB_X}" y1="{HEAD}" x2="{STUB_X}" '
             f'y2="{HEAD+body_h}" stroke="{HAIR}" stroke-width="1.4"/>')

    # ---- main line and stages
    prev_mid = None
    for i, (lvl, name, note) in enumerate(STAGES):
        mid = mids[i]
        h = heights[i]
        top_y = mid - h / 2

        if i % 2 == 0:
            o.append(f'<rect x="{LABEL_X-14}" y="{top_y}" '
                     f'width="{ARC_X0-LABEL_X-40}" height="{h}" fill="{FAINT}"/>')

        # transition arrow from the previous stage
        if prev_mid is not None:
            o.append(f'<line x1="{SPINE}" y1="{prev_mid+11}" x2="{SPINE}" '
                     f'y2="{mid-13}" stroke="{BLACK}" stroke-width="2.2" '
                     f'marker-end="url(#ahk)"/>')

        # threshold diamond sitting ON that edge
        if name in THRESHOLDS and prev_mid is not None:
            ttype, why = THRESHOLDS[name]
            ey = (prev_mid + mid) / 2
            d = 8.5
            o.append(f'<path d="M {SPINE} {ey-d} L {SPINE+d} {ey} '
                     f'L {SPINE} {ey+d} L {SPINE-d} {ey} Z" fill="#FFFFFF" '
                     f'stroke="{C1}" stroke-width="2.2"/>')
            o.append(f'<text x="{SPINE-d-8}" y="{ey+4.5}" font-size="13.5" '
                     f'font-weight="700" fill="{C1}" text-anchor="end">'
                     f'{esc(ttype)}</text>')
            o.append(f'<text x="{SPINE+d+8}" y="{ey+4.5}" font-size="13.5" '
                     f'fill="{C1}">{esc(why)}</text>')

        # the node
        if lvl == 0:
            o.append(f'<rect x="{SPINE-9}" y="{mid-9}" width="18" height="18" '
                     f'fill="{BLACK}"/>')
            o.append(f'<text x="{LABEL_X}" y="{mid+6}" font-size="19" '
                     f'font-weight="700" fill="{BLACK}">{esc(name)}</text>')
        else:
            o.append(f'<circle cx="{SPINE}" cy="{mid}" r="6" fill="none" '
                     f'stroke="{GREY}" stroke-width="2"/>')
            o.append(f'<text x="{LABEL_X+18}" y="{mid+5}" font-size="16" '
                     f'fill="{GREY}">{esc(name)}</text>')
        if note:
            col = BLACK if lvl == 0 else GREY
            o.append(f'<text x="{NOTE_X}" y="{mid+5}" font-size="15" '
                     f'fill="{col}">{esc(note)}</text>')

        # barrier — a bar laid across the outgoing edge, named in the channel
        if name in BARRIERS:
            o.append(f'<line x1="{SPINE-26}" y1="{mid+18}" '
                     f'x2="{SPINE+26}" y2="{mid+18}" stroke="{C4}" '
                     f'stroke-width="5"/>')
            o.append(f'<text x="{STUB_X-24}" y="{mid+5}" font-size="13.5" '
                     f'font-weight="700" fill="{C4}" text-anchor="end">'
                     f'BARRIER</text>')

        prev_mid = mid

    # ---- spawns, out to the left
    by_stage: dict[str, list[tuple]] = {}
    for at, sub, close_c, acc_c, ok in SPAWNS:
        by_stage.setdefault(at, []).append((sub, close_c, acc_c, ok))
    cursor = HEAD - 100          # so blocks can never sit on top of each other
    for at in [s[1] for s in STAGES if s[1] in by_stage]:
        subs = by_stage[at]
        base = y_of[at]
        n = len(subs)
        bh = 62
        gap = 8
        block = n * bh + (n - 1) * gap
        y0 = max(base - block / 2, cursor + 14)
        cursor = y0 + block
        for j, (sub, close_c, acc_c, ok) in enumerate(subs):
            byy = y0 + j * (bh + gap)
            o.append(f'<rect x="{SPAWN_L}" y="{byy}" '
                     f'width="{SPAWN_R-SPAWN_L}" height="{bh}" fill="#FFFFFF" '
                     f'stroke="{C3}" stroke-width="2.2"/>')
            o.append(f'<text x="{SPAWN_L+14}" y="{byy+22}" font-size="16" '
                     f'font-weight="700" fill="{C3}">{esc(sub)}</text>')
            o.append(f'<text x="{SPAWN_L+14}" y="{byy+40}" font-size="13" '
                     f'fill="{C3}">closes: {esc(close_c)}</text>')
            o.append(f'<text x="{SPAWN_L+14}" y="{byy+56}" font-size="13" '
                     f'fill="{C3}">accepted only if: {esc(acc_c)}</text>')
            # spawn arrow out, return arrow back — both in their own channels
            o.append(f'<path d="M {SPINE-11} {base-7} L {CH_OUT} {base-7} '
                     f'L {CH_OUT} {byy+18} L {SPAWN_R+4} {byy+18}" '
                     f'fill="none" stroke="{C3}" stroke-width="2" '
                     f'stroke-dasharray="6 4" marker-end="url(#ahs)"/>')
            o.append(f'<path d="M {SPAWN_R+4} {byy+46} L {CH_IN} {byy+46} '
                     f'L {CH_IN} {base+8} L {SPINE-11} {base+8}" '
                     f'fill="none" stroke="{C3}" stroke-width="2" '
                     f'marker-end="url(#ahs)"/>')
            tag = "ACCEPTED" if ok else "CLOSED, NOT ACCEPTED"
            o.append(f'<text x="{SPAWN_R-12}" y="{byy+22}" font-size="12.5" '
                     f'font-weight="700" text-anchor="end" '
                     f'fill="{C3 if ok else C1}">{esc(tag)}</text>')

    # ---- loops, arcs on the right.
    # Every segment lives in the clear strip right of the notes, so no arrow
    # ever crosses a word. The stub sits at the row's own mid-height and the
    # rows are striped, so the stage a loop leaves and lands on is unambiguous.
    for lid, src, dst, lname, fires, meaning in LOOPS:
        lx = lanes[lid]
        si, ti = index[src], index[dst]
        y0, y1 = mids[si], mids[ti]

        # leaves here
        o.append(f'<line x1="{STUB_X}" y1="{y0}" x2="{lx}" y2="{y0}" '
                 f'stroke="{C1}" stroke-width="1.5" stroke-dasharray="4 4"/>')
        o.append(f'<circle cx="{STUB_X}" cy="{y0}" r="4.4" fill="{C1}"/>')

        if src == dst:                        # the availability fan
            o.append(f'<path d="M {lx} {y0} C {lx+46} {y0-44} {lx+46} '
                     f'{y0+44} {lx+3} {y0+5}" fill="none" stroke="{C1}" '
                     f'stroke-width="2.6" marker-end="url(#ahL{lid})"/>')
            cy = y0 + 116
        else:
            up = y1 < y0
            r = min(18.0, abs(y1 - y0) / 2 - 3)
            stop = y1 + r if up else y1 - r
            o.append(f'<path d="M {lx} {y0} L {lx} {stop} Q {lx} {y1} '
                     f'{lx-r} {y1} L {STUB_X} {y1}" fill="none" '
                     f'stroke="{C1}" stroke-width="2.6" '
                     f'marker-end="url(#ahL{lid})"/>')
            cy = (y0 + y1) / 2

        o.append(f'<text x="{lx-9}" y="{cy}" font-size="15" font-weight="700" '
                 f'fill="{C1}" text-anchor="middle" {HALO}'
                 f'transform="rotate(-90 {lx-9} {cy})">{lid}  {esc(lname)}</text>')

    # ---- footer
    fy = HEAD + body_h + 56
    o.append(f'<line x1="{PAD}" y1="{fy-30}" x2="{W-PAD}" y2="{fy-30}" '
             f'stroke="{BLACK}" stroke-width="2.5"/>')
    o.append(f'<text x="{PAD}" y="{fy}" font-size="21" font-weight="700" '
             f'fill="{BLACK}">ROUTE REGISTRY v1 · THE {len(LOOPS)} KNOWN '
             f'RE-SEQUENCE ROUTES (non-exhaustive) — every route lands as a '
             f'NEW sub-sequence, never back inside the stage it left</text>')
    yy = fy + 30
    for lid, src, dst, lname, fires, meaning in LOOPS:
        o.append(f'<text x="{PAD}" y="{yy+14}" font-size="15.5" '
                 f'font-weight="700" fill="{C1}">{lid}</text>')
        o.append(f'<text x="{PAD+40}" y="{yy+14}" font-size="15.5" '
                 f'fill="{BLACK}">{esc(src)} → {esc(dst)}</text>')
        o.append(f'<text x="{PAD+700}" y="{yy+14}" font-size="15" '
                 f'fill="{C1}">fires when {esc(fires)}</text>')
        o.append(f'<text x="{PAD+1330}" y="{yy+14}" font-size="15" '
                 f'fill="{GREY}">{esc(meaning)}</text>')
        yy += 27
    o.append(f'<text x="{PAD}" y="{yy+14}" font-size="15" fill="{GREY}">'
             f'L6 NOTE — the name stays: era closure produces a NEW era and '
             f'the old era stays in use and referenceable (his 9.4). Meanings '
             f'are fixed with notes, never renames (his C-8). L1–L9 validated '
             f'on T-1…T-4 · L10 drawn on his word · L11 awaits T-5.</text>')
    yy += 27
    yy += 26
    o.append(f'<text x="{PAD}" y="{yy+14}" font-size="21" font-weight="700" '
             f'fill="{BLACK}">THE SIX INVARIANTS — they hold at every '
             f'stage above</text>')
    yy += 34
    for inv in INVARIANTS:
        o.append(f'<rect x="{PAD}" y="{yy+3}" width="11" height="11" '
                 f'fill="{BLACK}"/>')
        o.append(f'<text x="{PAD+22}" y="{yy+14}" font-size="15.5" '
                 f'fill="{BLACK}">{esc(inv)}</text>')
        yy += 27

    o.append('</svg>')
    return "\n".join(o)


# ============================================================== CHART B
def build_changes_overlay() -> str:
    PAD = 60
    RAIL_X0, RAIL_STEP = 76, 34
    SPINE = 76 + len(CHANGES) * RAIL_STEP + 40
    LABEL_X = SPINE + 40
    NOTE_X = LABEL_X + 470
    NOTE_CHARS = 118
    HEAD = 452

    rail = {cid: RAIL_X0 + i * RAIL_STEP for i, (cid, *_) in enumerate(CHANGES)}
    colour = {cid: col for cid, col, *_ in CHANGES}

    # dynamic row heights: a stage grows to hold its change notes
    heights: list[int] = []
    wrapped: list[list[tuple[str, list[str]]]] = []
    for lvl, name, note in STAGES:
        items = ATTACH.get(name, [])
        blocks = [(cid, wrap(txt, NOTE_CHARS)) for cid, txt in items]
        wrapped.append(blocks)
        need = sum(len(ls) for _, ls in blocks) * 23 + (len(blocks) * 9) + 16
        base = H0 if lvl == 0 else H1
        heights.append(max(base, need))
    mids = [HEAD + m for m in row_layout(heights)]
    body_h = sum(heights)
    W = NOTE_X + NOTE_CHARS * 7.55 + 80
    H = HEAD + body_h + 140

    o: list[str] = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{int(W)}" '
             f'height="{int(H)}" viewBox="0 0 {int(W)} {int(H)}" '
             f'font-family="Helvetica, Arial, sans-serif">')
    o.append(f'<rect width="{int(W)}" height="{int(H)}" fill="#FFFFFF"/>')

    o.append(f'<text x="{PAD}" y="76" font-size="50" font-weight="700" '
             f'fill="{BLACK}" letter-spacing="-1.2">ALL THE CHANGES, '
             f'SUPERIMPOSED</text>')
    o.append(f'<text x="{PAD}" y="118" font-size="22" fill="{GREY}">'
             f'The same {len(STAGES)} stages in black. Nine changes, one colour '
             f'each, each one lit only at the stages it actually touches.</text>')

    # legend
    ly = 158
    for i, (cid, col, title, sub) in enumerate(CHANGES):
        yy = ly + i * 26
        n = sum(1 for blocks in wrapped for c, _ in blocks if c == cid)
        o.append(f'<rect x="{PAD}" y="{yy-11}" width="14" height="14" '
                 f'fill="{col}"/>')
        o.append(f'<text x="{PAD+24}" y="{yy+1}" font-size="16.5" '
                 f'font-weight="700" fill="{col}">{cid}  {esc(title)}</text>')
        o.append(f'<text x="{PAD+560}" y="{yy+1}" font-size="15.5" '
                 f'fill="{col}">{esc(sub)}</text>')
        o.append(f'<text x="{PAD+1300}" y="{yy+1}" font-size="15.5" '
                 f'fill="{GREY}">touches {n} stage{"" if n == 1 else "s"}</text>')

    o.append(f'<line x1="{PAD}" y1="{HEAD-46}" x2="{W-PAD}" y2="{HEAD-46}" '
             f'stroke="{BLACK}" stroke-width="2.5"/>')
    # rail heads
    for cid, col, *_ in CHANGES:
        x = rail[cid]
        o.append(f'<text x="{x}" y="{HEAD-18}" font-size="13" '
                 f'font-weight="700" fill="{col}" text-anchor="middle">'
                 f'{cid}</text>')
        o.append(f'<line x1="{x}" y1="{HEAD}" x2="{x}" y2="{HEAD+body_h}" '
                 f'stroke="{col}" stroke-width="0.9" stroke-dasharray="2 6" '
                 f'opacity="0.5"/>')

    o.append(f'<line x1="{SPINE}" y1="{HEAD}" x2="{SPINE}" y2="{HEAD+body_h}" '
             f'stroke="{BLACK}" stroke-width="2.4"/>')

    for i, (lvl, name, note) in enumerate(STAGES):
        mid, h = mids[i], heights[i]
        top_y = mid - h / 2
        blocks = wrapped[i]

        if blocks:
            o.append(f'<rect x="{PAD}" y="{top_y+1}" width="{W-PAD*2}" '
                     f'height="{h-2}" fill="{FAINT}"/>')
        o.append(f'<line x1="{PAD}" y1="{top_y}" x2="{W-PAD}" y2="{top_y}" '
                 f'stroke="{HAIR}" stroke-width="0.8"/>')

        ny = top_y + 24
        if lvl == 0:
            o.append(f'<rect x="{SPINE-8}" y="{top_y+13}" width="16" '
                     f'height="16" fill="{BLACK}"/>')
            o.append(f'<text x="{LABEL_X}" y="{ny+2}" font-size="18" '
                     f'font-weight="700" fill="{BLACK}">{esc(name)}</text>')
        else:
            o.append(f'<circle cx="{SPINE}" cy="{top_y+21}" r="5.5" '
                     f'fill="none" stroke="{GREY}" stroke-width="2"/>')
            o.append(f'<text x="{LABEL_X+16}" y="{ny+1}" font-size="15.5" '
                     f'fill="{GREY}">{esc(name)}</text>')

        ty = top_y + 16
        for cid, lines in blocks:
            col = colour[cid]
            x = rail[cid]
            o.append(f'<circle cx="{x}" cy="{ty+6}" r="6.2" fill="{col}"/>')
            o.append(f'<line x1="{x+7}" y1="{ty+6}" x2="{SPINE-10}" '
                     f'y2="{ty+6}" stroke="{col}" stroke-width="1.6"/>')
            for k, line in enumerate(lines):
                o.append(f'<text x="{NOTE_X}" y="{ty+11+k*23}" font-size="15.5" '
                         f'fill="{col}">{esc(line)}</text>')
            o.append(f'<text x="{NOTE_X-42}" y="{ty+11}" font-size="13.5" '
                     f'font-weight="700" fill="{col}">{cid}</text>')
            ty += len(lines) * 23 + 9

    o.append(f'<line x1="{PAD}" y1="{HEAD+body_h}" x2="{W-PAD}" '
             f'y2="{HEAD+body_h}" stroke="{BLACK}" stroke-width="2.5"/>')
    o.append(f'<text x="{PAD}" y="{HEAD+body_h+40}" font-size="18" '
             f'fill="{BLACK}">Two stages are entirely new — SEQUENCE '
             f'CLOSURE and ENTITY OUTCOME. Everything else was already on the '
             f'line; what changed is what each stage is now required to '
             f'carry.</text>')
    o.append(f'<text x="{PAD}" y="{HEAD+body_h+70}" font-size="18" '
             f'fill="{GREY}">The thirteen primitives (C8) sit in the document, '
             f'not in the code. Six enforceable objects only — or the next '
             f'consolidation quietly drops half of them, as every prior one '
             f'did.</text>')
    o.append(f'<text x="{PAD}" y="{HEAD+body_h+100}" font-size="18" '
             f'fill="{GREY}">Read with the arrow chart: C1 is annotated here at '
             f'the stages where the threshold changes the reading, but all '
             f'{len(THRESHOLDS)} thresholds are drawn there, on their own '
             f'edges.</text>')

    o.append('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    here = Path(__file__).parent
    a = here / "SEQUENCE_ARROW_CHART.svg"
    b = here / "SEQUENCE_CHANGES_OVERLAY.svg"
    a.write_text(build_arrow_chart(), encoding="utf-8")
    b.write_text(build_changes_overlay(), encoding="utf-8")
    print(f"wrote {a}")
    print(f"wrote {b}")
    print(f"stages={len(STAGES)} thresholds={len(THRESHOLDS)} "
          f"spawns={len(SPAWNS)} loops={len(LOOPS)} barriers={len(BARRIERS)}")
    seen = {c for blocks in ATTACH.values() for c, _ in blocks}
    print("changes attached:", ", ".join(sorted(seen)),
          "| attachments:", sum(len(v) for v in ATTACH.values()))
