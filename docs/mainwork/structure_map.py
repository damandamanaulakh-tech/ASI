#!/usr/bin/env python3
"""SOURCEBORN — THE STRUCTURE AS IT STANDS, one dark full-architecture map.

Mirrors the visual language of his SOURCEBORN ASI map, but every box here is
the structure as actually held: BUILT (green) · LOCKED by ruling (blue) ·
DRAWN pending validation (amber) · OPEN on his word (red). Nothing invented;
every panel traceable to a commit, a ruling ID in 01D, or his words.

Writes STRUCTURE_MAP.svg beside itself; render to PNG with chromium.
"""
from __future__ import annotations

import html
from pathlib import Path

# ---------------------------------------------------------------- palette
BG = "#0A0F1E"
PANEL = "#0F1728"
PANEL2 = "#0C1322"
WHITE = "#E8EDF7"
GREY = "#8A93A8"
HAIR = "#232E47"

BLUE = "#4DA3FF"     # System-1 / human side
GOLD = "#E8C24A"     # stores / holy books
PURPLE = "#B07BFF"   # vocabulary / AI side
GREEN = "#3DDC84"    # built / live engine
TEAL = "#39D0D8"     # the method / gate
RED = "#FF6B6B"      # routes / open / halt
ORANGE = "#FF9F45"   # execution flow

S_BUILT, S_LOCK, S_PEND, S_OPEN = GREEN, "#5B9BFF", "#FFC24B", RED

W, H = 3600, 2330


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def wrap(text: str, width: int) -> list[str]:
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


class Map:
    def __init__(self):
        self.o: list[str] = []

    def add(self, s: str):
        self.o.append(s)

    def text(self, x, y, s, col=WHITE, size=15.0, bold=False, anchor="start",
             spacing=None):
        w = ' font-weight="700"' if bold else ""
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        sp = f' letter-spacing="{spacing}"' if spacing else ""
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}"'
                 f'{w}{a}{sp}>{esc(s)}</text>')

    def dot(self, x, y, col, r=6.5):
        self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>')

    def panel(self, x, y, w, h, title, col, status=None, sub=None) -> float:
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" '
                 f'fill="{PANEL}" stroke="{col}" stroke-width="2.6"/>')
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="46" rx="12" '
                 f'fill="{col}" opacity="0.13"/>')
        self.text(x + 22, y + 31, title, col, 23, bold=True)
        if status:
            self.dot(x + w - 26, y + 23, status, 8)
        if sub:
            self.text(x + 22, y + 66, sub, GREY, 13.5)
            return y + 88
        return y + 72

    def bullets(self, x, y, items, col=WHITE, size=14.5, chars=70, gap=6,
                bcol=None) -> float:
        lh = size + gap
        for head, body, c in items:
            cc = c or col
            self.dot(x + 6, y - size * 0.32, bcol or cc, 3.4)
            first = True
            prefix = f"{head} — " if head and body else (head or "")
            full = prefix + (body or "")
            for ln in wrap(full, chars):
                if first and head:
                    # bold head inline: draw head bold, rest normal on same line
                    if body and ln.startswith(head):
                        rest = ln[len(head):]
                        self.text(x + 18, y, head, cc, size, bold=True)
                        self.text(x + 18 + len(head) * size * 0.62, y, rest,
                                  col if c is None else cc, size)
                    else:
                        self.text(x + 18, y, ln, cc, size, bold=True)
                else:
                    self.text(x + 18, y, ln, col if c is None else cc, size)
                y += lh
                first = False
            y += 2
        return y

    def chip(self, x, y, w, h, title, lines, col, tsize=16.0, lsize=12.5):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" '
                 f'fill="{PANEL2}" stroke="{col}" stroke-width="2"/>')
        self.text(x + w / 2, y + 26, title, col, tsize, bold=True,
                  anchor="middle")
        yy = y + 47
        for ln in lines:
            self.text(x + w / 2, yy, ln, GREY, lsize, anchor="middle")
            yy += lsize + 4

    def arrow(self, x1, y1, x2, y2, col, sw=2.4, dash=None, marker="m"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                 f'stroke="{col}" stroke-width="{sw}"{d} '
                 f'marker-end="url(#ah_{marker})"/>')


def build() -> str:
    m = Map()
    m.add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
          f'viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">')
    m.add(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    m.add('<defs>')
    for name, col in [("m", GREY), ("t", TEAL), ("o", ORANGE), ("r", RED),
                      ("g", GOLD)]:
        m.add(f'<marker id="ah_{name}" viewBox="0 0 10 10" refX="9" refY="5" '
              f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
              f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{col}"/></marker>')
    m.add('</defs>')

    # ---------------------------------------------------------- header
    m.text(W / 2, 62, "SOURCEBORN — THE STRUCTURE AS IT STANDS", WHITE, 52,
           bold=True, anchor="middle", spacing="1")
    m.text(W / 2, 100, "DIFFERENCE  +  RELATIONSHIP  +  ORDER  =  SEQUENCE",
           TEAL, 24, bold=True, anchor="middle", spacing="3")
    m.text(W / 2, 130,
           "his formula, his map answered in kind — every box below is the build as held: "
           "traceable to a commit, a ruling ID in 01D, or his words. Nothing invented.",
           GREY, 15, anchor="middle")

    # header status legend (top corners)
    for i, (col, lab) in enumerate([(S_BUILT, "BUILT & TESTED"),
                                    (S_LOCK, "LOCKED BY RULING"),
                                    (S_PEND, "DRAWN / PENDING"),
                                    (S_OPEN, "OPEN ON HIS WORD / HALT")]):
        x = 60 + i * 300
        m.dot(x, 124, col, 7)
        m.text(x + 16, 129, lab, col, 13.5, bold=True)

    LX, LW = 40, 880
    CX, CW = 960, 1680
    RX, RW = 2680, 880

    # ==================================================== LEFT COLUMN
    # LADDER
    y = m.panel(LX, 170, LW, 470, "SYSTEM-1 (ASI) — THE LADDER", BLUE,
                S_BUILT, "Phase-1 DONE on his word · 2026-08-09 · docs/mainwork/asi/LADDER.md")
    rows = [("SYSTEM", "1", "ASI"),
            ("SEGMENT", "10", "the human ten — uneven by design, 347 → 276"),
            ("CONTAINER", "200", "the frame stays 200 — filled over time, never shrunk"),
            ("PARAMETER", "3,072", "SB-ASI-P0001 … each with segment, container, slot"),
            ("ELEMENT", "—", "empty by his instruction; the name is his call")]
    yy = y + 6
    for name, count, note in rows:
        m.text(LX + 30, yy, name, WHITE, 16.5, bold=True)
        m.text(LX + 240, yy, count, BLUE, 16.5, bold=True)
        m.text(LX + 340, yy, note, GREY, 13.5)
        yy += 30
    m.add(f'<line x1="{LX+22}" y1="{yy-14}" x2="{LX+LW-22}" y2="{yy-14}" '
          f'stroke="{HAIR}" stroke-width="1.5"/>')
    yy = m.bullets(LX + 22, yy + 12, [
        ("Filling", "142 segment-owned (3,054) · 18 cross-segment (18) · 40 reserved at target 0 — named, kept", None),
        ("Second axis", "40 context filters × 12 states × 20 failure classes — multiplies the 3,072, does not nest", None),
        ("Outside", "650 held reserve · 918→1,200 external base · 64 AI-only candidates", None),
        ("His count rule 18.1", "keep only no-placeholder, no-empty-set — if all qualify, 3,072 is the number", None),
        ("Base HALT (his)", "143 ASI nodes + all P1 answers built on 80/2,560 (v0.3); this ladder is v0.4 — the base moves on his word", RED),
    ], WHITE, 14, 74)

    # CROSS-SEGMENT <-> FILTERS
    y = m.panel(LX, 660, LW, 300, "HIS CONTAINERS ↔ THE SEVEN FILTERS", GOLD,
                S_LOCK, "his 2.4 answered — the filters are the RUNTIME GATE; his cross-segment layer already carries four")
    pairs = [("Source-Conflict Preservation", "Mask", "strong"),
             ("Negative Space & Absence Mapping", "Mask", "strong"),
             ("Claim–Evidence Binding", "Fact", "strong"),
             ("Proof Debt & Evidence Ledger", "proof-debt / ledger", "strong"),
             ("Synthetic Fuel & Reality Anchor", "Ground", "plausible"),
             ("External Checkpoint & Cross-Model Audit", "Source", "plausible"),
             ("Stall Diagnostic & Critical Logic Wall", "Halt", "plausible"),
             ("— no container found", "Loop · Sequence", "unmatched")]
    yy = y + 6
    for cont, filt, grade in pairs:
        gcol = GREEN if grade == "strong" else (S_PEND if grade == "plausible" else RED)
        m.text(LX + 30, yy, cont, WHITE, 13.5)
        m.text(LX + 480, yy, "→  " + filt, GOLD, 13.5, bold=True)
        m.text(LX + 760, yy, grade, gcol, 12.5)
        yy += 25

    # TESTS
    y = m.panel(LX, 980, LW, 280, "THE TESTS — the method was EARNED on cases", BLUE, S_BUILT)
    m.bullets(LX + 22, y + 6, [
        ("T-1 GRAVITY", "11/37 fill · no boundary · 21 dark nodes ARE the finding — EMPTY is data", None),
        ("T-2 PYRAMIDS", "33/37 · requirement BORROWED from the maker · Bent Pyramid = route L3", None),
        ("T-3 BRAIN", "four clocks — execution · learning · development · transmission; carrier write-back", None),
        ("T-4 MAHABHARATA", "DEFINES the method — reverse & sequence to ease the work; never run as an instance", GOLD),
        ("T-5 UNIVERSE→HUMAN", "~30 real steps, triple-passed — NOT RUN · it validates or kills route L11", RED),
    ], WHITE, 14, 74)

    # LIVE ENGINE
    y = m.panel(LX, 1280, LW, 350, "THE LIVE ENGINE — running today", GREEN,
                S_BUILT, "tests 90/90 green · offline lane verified with every key unset · deploy is his hand (Render)")
    m.bullets(LX + 22, y + 6, [
        ("Web app", "dashboard · library · chats · upload · brains · graph · snapshots · memory reports", None),
        ("Method files", "filters.py (the seven) · sequence.py (universal sequence) · seq_kernel.py (six objects) · rh_code.py (the cap)", None),
        ("8 SB stages + RGL loop", "core gate 6 lenses · doubt/falsifier/witness · evidence ladder · merge · synthetic fuel · output + weekly update", None),
        ("Models", "Claude · Grok · OpenAI · OpenRouter · local WebGPU lane — and a no-key offline path", None),
        ("3 memories + 95 brains", "corpus · wisdom · live fact — 70 SB + 25 URR are the MEMORY; the filters are the METHOD", None),
        ("Private", ".sourceborn/ is git-ignored — his brain never enters the repo", GOLD),
    ], WHITE, 14, 74)

    # ==================================================== CENTER COLUMN
    # THE GATE
    y = m.panel(CX, 170, CW, 250, "THE MAHABHARATA SEQUENCE — THE GATE", TEAL,
                S_LOCK, 'his 2.2: "everything all response of LLM will come and go from there only (reverse, forward, reverse)"')
    steps = [("POINT ZERO", "his exact words,", "locked before reading"),
             ("PASS 0", "DECLARE THE END", "which reality counts"),
             ("PASS 1 · REVERSE", "the required chain", "what the end needed"),
             ("PASS 2 · FORWARD", "the available chain", "what was really there"),
             ("PASS 3 · REVERSE", "the attack — gap list", "every unconnected dot"),
             ("CLOSURE", "status + gap list", "the gaps go to HIM")]
    bw, gap = 250, 24
    x0 = CX + (CW - (bw * 6 + gap * 5)) / 2
    for i, (t, l1, l2) in enumerate(steps):
        bx = x0 + i * (bw + gap)
        m.chip(bx, y + 8, bw, 86, t, [l1, l2], TEAL, 15.5, 12.5)
        if i:
            m.arrow(bx - gap + 2, y + 51, bx - 3, y + 51, TEAL, 2.6, marker="t")
    m.text(CX + 24, y + 126,
           "57 stages · 22 thresholds · 6 spawns · 11 routes · 4 barriers — counts of the DRAWING, not the model (standing rule 10)",
           GREY, 13.5)
    m.dot(CX + 24 + 6, y + 148, S_OPEN, 5)
    m.text(CX + 40, y + 153,
           "gate wiring into the runtime: 16.2 = None Yet — enters code only on his per-object word",
           RED, 13.5)

    # THREE LAYERS
    y0 = 450
    m.panel(CX, y0, CW, 540, "THE THREE LAYERS — grammar · case graph · runtime (his 2.1)", TEAL, S_LOCK)
    colw = (CW - 4 * 24) / 3
    defs = [
        ("GRAMMAR", S_LOCK, BLUE, [
            ("Canon", "Universal_Sequence_Machine_Architecture_v1 — docs/method/canon/ (his 1.1)", None),
            ("Ledger", "01D SEQUENCE RULINGS — binding; 66 answers + 14 collisions", None),
            ("Orders (8)", "temporal · causal · dependency · logical · construction · discovery · control · representation — on EVERY edge; silent conversion banned, named support carries a marker at full grade", None),
            ("Relations (8)", "MAIN · ATTACHED (spawned SUB-SEQUENCE) · CHARACTER · NEXT · REFERENCE · COUNTER (held) · PARALLEL · CONVERGING", None),
            ("Thresholds (9)", "open vocabulary WITH registration · lists allowed · recheck contract on every dormant edge", None),
            ("Ground · Mask", "origin_class (FOUNDED · INVENTED · MIXED · UNKNOWN) · mask_record — wired to his own containers", None),
        ]),
        ("CASE GRAPH", S_OPEN, RED, [
            ("State", "NONE EXISTS YET — the first case is the next live ask through the gate", RED),
            ("Holds when it exists", "nodes · typed edges · actor views · seeds bound · borrowed operations with the lending sequence's ID (permanent, his 4.4)", None),
            ("First-class results", "EMPTY · UNREACHABLE · BORROWED · MERGED — kept forever (his 11.2); a case graph must name what it could not reach", None),
            ("Killed", "the 'Karna case graph' — Mahabharata DEFINES the method, it is not an instance to run", GOLD),
        ]),
        ("RUNTIME", S_BUILT, GREEN, [
            ("seq_kernel.py — six objects", "threshold-on-edge (9 types) · SequenceClosure ≠ EntityOutcome · SpawnContract (close ≠ acceptance) · Open-Sequence Ledger + barrier law · DriverOrigin (9, WANT beside NEED) · Controller (6, META)", None),
            ("THE SEVEN FILTERS = the gate", "1 Ground · 2 Sequence · 3 Source · 4 Mask · 5 Fact · 6 Halt · 7 Loop — every finding, in order, every time", None),
            ("Witness law", "one source caps at Medium · two that differ HALT — the gap is the MASK and goes to him, never averaged", None),
            ("No in-place loop · no reopen", "a retry is a NEW sub-sequence; S₁ references S₀", None),
        ]),
    ]
    for i, (t, st, col, items) in enumerate(defs):
        bx = CX + 24 + i * (colw + 24)
        m.add(f'<rect x="{bx}" y="{y0+58}" width="{colw}" height="{540-80}" '
              f'rx="10" fill="{PANEL2}" stroke="{col}" stroke-width="2"/>')
        m.dot(bx + 20, y0 + 84, st, 7)
        m.text(bx + 36, y0 + 90, t, col, 19, bold=True)
        m.bullets(bx + 14, y0 + 122, items, WHITE, 12.8, 44, gap=5)

    # ROUTE REGISTRY
    y = m.panel(CX, 1010, CW, 420, "ROUTE REGISTRY v1 — the 11 known re-sequence routes (non-exhaustive)",
                RED, S_LOCK, "every route lands as a NEW sub-sequence, never back inside the stage it left · new routes enter on case validation")
    routes = [
        ("L1", "AVAILABILITY → AVAILABILITY", "locate fails, then build fails", "T-2", S_BUILT),
        ("L2", "QUALIFICATION → SELECTION", "the fit test fails", "T-2", S_BUILT),
        ("L3", "TESTING → DECISION/CHOICE", "54° proves too steep mid-build", "T-2 · Bent Pyramid", S_BUILT),
        ("L4", "NO-branch → REQUIREMENT EMERGES", "the entity degrades — driver DAMAGE", "T-3", S_BUILT),
        ("L5", "VERIFICATION → REQUIREMENT", "result ≠ requirement — restated, never patched", "T-2", S_BUILT),
        ("L6", "FEEDBACK → PRIOR REALITY", "reality contradicts the requirement class-wide", "T-2 · name kept — era closure births a NEW era; the old stays in use (9.4)", S_BUILT),
        ("L7", "MEMORY VALIDATION → INFORMATION", "one witness only — two differing HALT", "T-2", S_BUILT),
        ("L8", "COMPRESSION → MEMORY", "the method is not recoverable", "T-2", S_BUILT),
        ("L9", "MEMORY UPDATE → ORIGIN/SOURCE", "the halt is named — next Point Zero", "all", S_BUILT),
        ("L10", "DECISION/CHOICE → SELECTION", "a HELD alternative taken up", "drawn on his word · first live case pending", S_PEND),
        ("L11", "RETURN → ENVIRONMENT/HOST", "the run changes its own ground — thresholds re-read", "UNVALIDATED — awaits T-5", S_PEND),
    ]
    yy = y + 4
    for lid, path, fires, val, st in routes:
        m.text(CX + 30, yy, lid, RED, 14, bold=True)
        m.text(CX + 92, yy, path, WHITE, 14)
        m.text(CX + 560, yy, "fires: " + fires, GREY, 13)
        m.dot(CX + 1128, yy - 4.5, st, 4.6)
        m.text(CX + 1142, yy, val, S_PEND if st == S_PEND else GREY, 12.5)
        yy += 28

    # STANDING RULES
    y = m.panel(CX, 1450, CW, 180, "STANDING RULES — each traceable to a ruling in 01D", WHITE, S_LOCK)
    rules = ["1 · nothing is ever removed — differences become sub-parameters or inject new sequences",
             "2 · fix meanings with NOTES, never renames — changes kill everything in codes",
             "3 · everything closed is WRITTEN, or it is missed — HALTs carry a written proposal",
             "4 · the Mahabharata Sequence is the METHOD, not an instance",
             "5 · named conversion only — marker alone, full grade",
             "6 · seeds are permanent — old nests under new sub-heads; [SYNTHETIC] tag stays",
             "7 · two witnesses that differ HALT, unaveraged — after the HALT, revisit",
             "8 · BEYOND-HORIZON is the invention lane — halt, that is invention",
             "9 · guarantees are verdicts about the declared graph, stated flatly",
             "10 · counts are drawings, not the model — 53 / 39 / 57 are one thing"]
    for i, r in enumerate(rules):
        col_i = i % 2
        row_i = i // 2
        m.text(CX + 30 + col_i * (CW / 2 - 10), y + 6 + row_i * 22, r, WHITE, 13)

    # ==================================================== RIGHT COLUMN
    # STORES
    y = m.panel(RX, 170, RW, 430, "THE STORES — beside the three layers", GOLD, S_LOCK)
    m.bullets(RX + 22, y + 6, [
        ("OPEN-SEQUENCE LEDGER", "row kinds as many as needed — SPAWNED (contract, blocks its edge) · CHARACTER/RIDING (no contract, intersects; terminal at the convergence window)", None),
        ("SEED REGISTRY", "a seed is not open work · seeds NEVER expire — the next sequence uses them again", None),
        ("VIEW STORE", "actor views with their own clock · false beliefs only from evidence · the engine raises candidates for his acceptance", None),
        ("HOLY BOOKS", "canon/ + holy_books/ filed verbatim · Mahabharata material cited on edges (6.3) — read, extracted, never obeyed as verdict", GREEN),
        ("MEMORY ×3", "corpus · wisdom · live fact — keep-forever, nothing deleted", GREEN),
        ("95 BRAINS", "70 SB + 25 URR — they are the MEMORY; the filters are the METHOD", GREEN),
    ], WHITE, 13.5, 68, gap=5)

    # WORDS
    y = m.panel(RX, 620, RW, 390, "THE WORDS THAT LOCKED", PURPLE, S_LOCK)
    m.bullets(RX + 22, y + 6, [
        ("ROLES (4)", "DRIVER · CONTROLLER · PERFORMER · CARRIER — performer required, NONE is a real value; META in code, Krishna is the illustration", None),
        ("ORDER LISTS", "an edge may carry several orders — the list may not grow as distance to the declared end falls; more than one at distance zero → HALT", None),
        ("REFERENCE inherits", "the ORIGINAL grade and its age, flagged UNDER-VETTING — vetting upgrades, citation never does; the thin old is kept FOR vetting", None),
        ("EPISTEMIC GRADES", "KNOWN · SUPPORTED · INFERRED · SPECULATIVE · UNKNOWN · CONTRADICTORY — on every edge; the floor is per BRANCH (the pyramid result)", None),
        ("RUNTIME STATES", "RUNNING_PARALLEL · AT_CONVERGENCE — so no word collides with the relations", None),
        ("CLOSURE", "the declared contract must terminate; the phenomenon need not — the word used of an entity HALTS to him", None),
    ], WHITE, 13.5, 68, gap=5)

    # INVARIANTS
    y = m.panel(RX, 1030, RW, 210, "THE SIX INVARIANTS — hold everywhere", WHITE, S_BUILT)
    for i, inv in enumerate([
            "BARRIER LAW — no crossing while a required return is unaccepted",
            "NO IN-PLACE LOOP — a retry is a new sub-sequence",
            "NO REOPEN — S₁ references S₀; S₀ stays closed",
            "CLOSURE IS A SEQUENCE WORD — entities persist, cohere, degrade, terminate",
            "ENCOUNTER IS CONDITIONAL — meeting is an event with a condition",
            "NEVER MANUFACTURE A SOURCE — the gap stays, and goes to him"]):
        m.text(RX + 30, y + 8 + i * 23, inv, WHITE, 13)

    # RH CAP
    y = m.panel(RX, 1260, RW, 160, "RH AS CODE — THE CAP (½)", TEAL, S_BUILT,
                "rh_code.py · the theorem spent as a build spec, not proved")
    m.bullets(RX + 22, y + 4, [
        ("", "one voice is capped at ½ — σ ≤ ½ stable, σ > ½ drift", None),
        ("", "several agreeing → 1 − 0.5ⁿ · two that differ → HALT at ½, the gap is the MASK", None),
        ("", "line_check reports its OWN resolution instead of rounding", None),
    ], WHITE, 13.5, 70, gap=4)

    # QUEUE + OPEN
    y = m.panel(RX, 1440, RW, 190, "THE QUEUE + OPEN ON HIS WORD", RED, S_OPEN,
                "16.2 = None Yet — nothing enters code without his per-object word")
    q = "queue: order-type-on-edge · ledger row kinds · seed registry · view store · performer · epistemic-status-per-edge"
    for i, ln in enumerate(wrap(q, 78)):
        m.text(RX + 30, y + 6 + i * 20, ln, S_PEND, 13.5)
    o2 = ("open: element name (18.2) · 9.3 Para ID merge/omit · Rule-5 wording · "
          "container-ID overlap 121–160 vs 081–160 · transition vs step (01B vs 01) · "
          "contamination check (13.3) · the model lock — locks on his word only")
    for i, ln in enumerate(wrap(o2, 78)):
        m.text(RX + 30, y + 52 + i * 20, ln, RED, 13.5)

    # ==================================================== FLOW BAND
    fy = 1660
    m.add(f'<rect x="40" y="{fy}" width="{W-80}" height="300" rx="14" '
          f'fill="{PANEL}" stroke="{ORANGE}" stroke-width="2.8"/>')
    m.text(64, fy + 36, "EVERY RESPONSE — HOW IT ACTUALLY RUNS", ORANGE, 23, bold=True)
    m.dot(W - 66, fy + 28, S_BUILT, 8)
    flow = [
        ("HIS ASK", "any words, any form", "nothing killed at intake"),
        ("POINT ZERO LOCK", "his exact words stored", "before any reading"),
        ("CLASSIFY", "fact · claim · belief ·", "speculation · mystery · invention"),
        ("THE GATE  R→F→R", "declare end · reverse ·", "forward · reverse-attack"),
        ("SEVEN FILTERS", "Ground Sequence Source", "Mask Fact Halt Loop — in order"),
        ("WITNESS CAP ½", "one source = Medium max", "two differ = HALT · gap = MASK"),
        ("TAGGED ANSWER", "no untagged claim leaves", "+ the gap list, on its face"),
        ("HALT NAMED", "where it fails, said plainly", "never hidden, never filled"),
    ]
    bw, gap = 396, 26
    x0 = 64
    for i, (t, l1, l2) in enumerate(flow):
        bx = x0 + i * (bw + gap)
        m.chip(bx, fy + 56, bw, 92, t, [l1, l2], ORANGE, 16.5, 12.5)
        if i:
            m.arrow(bx - gap + 3, fy + 102, bx - 4, fy + 102, ORANGE, 2.6, marker="o")
    # loop back
    lx1 = x0 + 7 * (bw + gap) + bw / 2
    lx0 = x0 + bw + gap + bw / 2
    m.add(f'<path d="M {lx1} {fy+152} L {lx1} {fy+186} L {lx0} {fy+186} '
          f'L {lx0} {fy+152}" fill="none" stroke="{RED}" stroke-width="2.6" '
          f'marker-end="url(#ah_r)"/>')
    m.text((lx0 + lx1) / 2, fy + 180,
           'HALT = THE NEXT POINT ZERO — "that point is a point zero for new loop, that is halt, that is invention"',
           RED, 14.5, bold=True, anchor="middle")
    # returns strip
    ry = fy + 208
    m.text(64, ry + 24, "RETURNS", GREY, 15, bold=True)
    m.chip(200, ry, 900, 66, "ACCEPTED — continue",
           ["the return satisfies the acceptance condition — the barrier lifts"], GREEN, 15, 12.5)
    m.chip(1130, ry, 1100, 66, "PARTIAL / UNCONNECTED DOTS — HALT to him",
           ["closure with gaps on record is allowed (9.5) — my recommendation attached each time"], S_PEND, 15, 12.5)
    m.chip(2260, ry, 1276, 66, "FAILED — repair sub-sequence",
           ["closed-not-accepted stays on the ledger · a NEW sub-sequence opens · no in-place loop, no reopen"], RED, 15, 12.5)

    # ==================================================== PHASES + CONNECTS
    py = 1990
    m.text(64, py + 20, "THE PHASES", WHITE, 18, bold=True)
    phases = [("P1 · DEFINE SEQUENCE", "DONE — his word", S_BUILT),
              ("P2 · HUMAN · AI · HOLY BOOKS · ASI", "IN PROGRESS — parameters, sub-para, containers, element", S_PEND),
              ("P2a · HIS UPLOADS", "his hand — OT sheet and .sourceborn/ never go up", GREY),
              ("P3 · NODES + BRAIN MEMORY", "waiting", GREY),
              ("P4 · EXAMPLES — RH HIS WAY", "waiting", GREY),
              ("P5 · LIVE APP — edit from inside", "waiting", GREY)]
    bw2 = 545
    for i, (t, s, col) in enumerate(phases):
        bx = 200 + i * (bw2 + 18)
        m.add(f'<rect x="{bx}" y="{py}" width="{bw2}" height="58" rx="9" '
              f'fill="{PANEL2}" stroke="{col if col!=GREY else HAIR}" stroke-width="2"/>')
        m.dot(bx + 18, py + 22, col if col != GREY else HAIR, 6)
        m.text(bx + 32, py + 26, t, WHITE, 14.5, bold=True)
        m.text(bx + 32, py + 46, s, col if col != GREY else GREY, 12.5)

    cy = 2085
    m.text(64, cy + 20, "HOW IT CONNECTS", WHITE, 18, bold=True)
    chain = ["HIS WORDS", "POINT ZERO", "THE GATE", "GRAMMAR OBJECTS",
             "RUNTIME FILTERS", "STORES + MEMORY", "ANSWER + GAPS", "HALT", "NEW LOOP"]
    x = 300
    for i, c in enumerate(chain):
        m.text(x, cy + 20, c, TEAL, 15.5, bold=True)
        x += len(c) * 9.8 + 18
        if i < len(chain) - 1:
            m.arrow(x, cy + 15, x + 34, cy + 15, GREY, 2, marker="m")
            x += 52
    m.text(300, cy + 48,
           "everything closes — and a closed sequence seeds the next: one closed line, a million inventions. The wall between exploration and the safety line stays: "
           "no weapons · no fraud · no medical-misuse · no world-guarantees · guarantees here are verdicts about the declared graph.",
           GREY, 13.5)

    # ==================================================== FOOTER LEGEND
    ly = 2185
    m.add(f'<line x1="40" y1="{ly}" x2="{W-40}" y2="{ly}" stroke="{HAIR}" '
          f'stroke-width="1.6"/>')
    m.text(64, ly + 34, "BORDERS", GREY, 14, bold=True)
    for i, (col, lab) in enumerate([(BLUE, "System-1 / tests"), (TEAL, "the method"),
                                    (GOLD, "stores / Holy Books"), (PURPLE, "locked words"),
                                    (GREEN, "built & running"), (RED, "routes / open"),
                                    (ORANGE, "execution flow")]):
        x = 200 + i * 300
        m.add(f'<rect x="{x}" y="{ly+20}" width="26" height="14" rx="3" '
              f'fill="none" stroke="{col}" stroke-width="2.4"/>')
        m.text(x + 36, ly + 32, lab, col, 13)
    m.text(64, ly + 76,
           "Sources: docs/method/01D_SEQUENCE_RULINGS.md (binding) · docs/method/canon/ · docs/method/holy_books/ · docs/mainwork/asi/LADDER.md · "
           "src/sourceborn/{filters,sequence,seq_kernel,rh_code}.py · tests 90/90. Counts are properties of drawings, not of the sequence. 2026-08-09.",
           GREY, 13)
    m.text(64, ly + 104,
           "The model is complete and NOT locked — it locks on his word only.",
           WHITE, 15, bold=True)

    # a few cross-panel connectors
    m.arrow(LX + LW, 400, CX - 6, 300, GREY, 2, "6 6")           # ladder -> gate
    m.arrow(RX - 6, 380, CX + CW + 4, 720, GREY, 2, "6 6")       # stores -> layers
    m.arrow(CX + CW / 2, 1430, CX + CW / 2, 1445, GREY, 2, "6 6")

    m.add('</svg>')
    return "\n".join(m.o)


if __name__ == "__main__":
    dest = Path(__file__).with_name("STRUCTURE_MAP.svg")
    dest.write_text(build(), encoding="utf-8")
    print(f"wrote {dest}")
