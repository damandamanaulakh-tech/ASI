"""THE LEXICAL BRIDGE — taught vocabulary, so his rows are reachable by the
words people actually use.

Built on his word ("build the bridge and approve all three", 2026-08-24),
from the run on his failure teaching, canon at
docs/method/canon/IF_THEY_CAN_I_WILL_TOO.md §5: the bank already held the
exact rows that teaching is about — P0885 Direct imitation, P0886 Delayed
imitation, P0887 Emulation (goal copying), P2451 Self-efficacy, P2625 Ideal
self — and BOTH matchers missed all of them, because the teaching says
"copy" and the bank says "imitation". Surface words carried no meaning
across; this module is the carrier.

WHAT A BRIDGE IS, AND IS NOT

A bridge is a TAUGHT identity: this word or phrase, in ordinary speech,
means THAT row family in his bank. It is the senses.py principle applied to
vocabulary — user-defined semantic context, seeded from his teachings, each
entry carrying which teaching created it. It is NOT a synonym dictionary
imported from anywhere: every bridge here exists because a run of his
material exposed the gap, and every future bridge arrives the same way
(through the ledger, append-only). His own law applies to the module
itself — the form is not copied in; it is grown from his corrections.

BOTH READINGS ARE ALWAYS KEPT

A bridged seat NEVER merges silently into the direct seats. `seat()` returns
it in its own `bridged` list, carrying the bridge id, the phrase that fired
it, and the teaching it came from — so the screen can always show what the
machine read directly beside what it reached through teaching. And a bridge
may cross the role gate, stated on the row: the role gate exists to stop
WORD COINCIDENCES, and a taught bridge is the opposite of a coincidence —
it is meaning placed by him.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# THE SEEDED BRIDGES — from his failure teaching, 2026-08-24. Approved by his
# word. Targets are flat ids in HIS bank; nothing here creates a parameter.
# ---------------------------------------------------------------------------

TAUGHT_BY = "his failure teaching, 2026-08-24 — 'they try to copy and failed'"

SEEDED = (
    {"id": "BR-001",
     "phrases": ("copy", "copies", "copied", "copying", "copycat",
                 "mimic", "mimics", "mimicking", "imitate", "imitates",
                 "imitating", "re do the same", "redo the same",
                 "do the same"),
     "means": "imitation — doing what another was seen doing",
     "targets": ("SB-HFR-P0885", "SB-HFR-P0886", "SB-HFR-P0887"),
     "container": "CON-023",
     "taught_by": TAUGHT_BY,
     "approved": "his word, 2026-08-24"},
    {"id": "BR-002",
     "phrases": ("if they can i will too", "if he can i can", "if she can "
                 "i can", "if they can so can i", "i can do it too",
                 "possible for me too"),
     "means": "self-efficacy — the possibility proof taken personally",
     "targets": ("SB-HFR-P2451",),
     "container": "CON-062",
     "taught_by": TAUGHT_BY,
     "approved": "his word, 2026-08-24"},
    {"id": "BR-003",
     "phrases": ("role model", "role models", "look up to", "looks up to",
                 "looking up to", "my idol", "their idol", "hero of mine"),
     "means": "the ideal self — who one measures oneself toward",
     "targets": ("SB-HFR-P2625",),
     "container": "CON-066",
     "taught_by": TAUGHT_BY,
     "approved": "his word, 2026-08-24"},
)

# The absence the same run surfaced, kept visible rather than mis-bridged:
# his teaching also carries social comparison, and the bank holds NO general
# social-comparison row (P0597 is BODY-comparison — a different thing).
# Bridging to the wrong row would be the word-coincidence failure by another
# door, so it is refused here and reported.
KNOWN_ABSENCE = {
    "concept": "social comparison (general — status, success, standing)",
    "nearest_row": "SB-HFR-P0597 Body-comparison (social) — BODY-specific, "
                   "deliberately NOT bridged",
    "why_not": "a bridge to the wrong row is the word-coincidence failure "
               "through another door",
    "his_call": "whether this becomes a grown parameter (the P3205 path) "
                "or waits",
}


def bridges(root: str = None) -> list:
    """The seeded bridges plus any taught later through the ledger
    (kind BRIDGE, extra carrying phrases/targets). Append-only both sides."""
    out = [dict(b) for b in SEEDED]
    if root:
        from . import growth as G
        for r in G.load(root):
            if r.get("kind") == "BRIDGE" and r.get("phrases"):
                out.append({"id": r["id"], "phrases": tuple(r["phrases"]),
                            "means": r.get("detail", ""),
                            "targets": tuple(r.get("targets", ())),
                            "container": r.get("container", ""),
                            "taught_by": r.get("surfaced_by", ""),
                            "approved": r.get("approved", "")})
    return out


def match(text: str, root: str = None) -> list:
    """Every bridge this text fires, with the exact phrase that fired it.

    Phrase matching is whole-word (the semantic_loss lesson: 'productive'
    must never fire 'Reproductive'), longest phrases checked first so
    'if they can i will too' wins before any fragment could."""
    low = " ".join((text or "").lower().split())
    fired = []
    for b in bridges(root):
        for p in sorted(b["phrases"], key=len, reverse=True):
            if re.search(r"(?<![a-z])" + re.escape(p) + r"(?![a-z])", low):
                fired.append({"bridge": b["id"], "phrase": p,
                              "means": b["means"],
                              "targets": list(b["targets"]),
                              "container": b["container"],
                              "taught_by": b["taught_by"]})
                break
    return fired


def rows_via(text: str, root: str = None) -> list:
    """The bank rows this text reaches THROUGH TEACHING — each carrying the
    bridge that carried it, never merged with a direct word match."""
    from . import human_registry as hr
    flat = {}
    start = 1
    for c in hr.containers():
        flat[c["id"]] = (start, c)
        start += c["count"]
    out, seen = [], set()
    for m in match(text, root):
        for t in m["targets"]:
            if t in seen:
                continue
            seen.add(t)
            p = int(t.replace("SB-HFR-P", ""))
            name, cname, seg = "", "", ""
            for cid, (s, c) in flat.items():
                if s <= p < s + c["count"]:
                    name = c["subs"][p - s]
                    cname, seg = c["name"], c["segment"]
                    break
            out.append({"sb_id": t, "name": name, "container": m["container"],
                        "container_name": cname, "segment": seg,
                        "via_bridge": m["bridge"], "phrase": m["phrase"],
                        "taught_by": m["taught_by"],
                        "band": "TAUGHT",
                        "crosses_role": True,
                        "why_it_may_cross": "the role gate stops word "
                                            "coincidences; a taught bridge "
                                            "is meaning placed by him, not "
                                            "a coincidence"})
    return out


def stats() -> dict:
    return {
        "seeded": len(SEEDED),
        "bridge_ids": [b["id"] for b in SEEDED],
        "reachable_rows": sorted({t for b in SEEDED for t in b["targets"]}),
        "known_absence": KNOWN_ABSENCE["concept"],
        "law": "both readings always kept — a bridged seat never merges "
               "silently into the direct seats.",
        "grows_by": "the ledger (kind BRIDGE), append-only — never an "
                    "imported dictionary.",
    }


def annotations() -> list:
    return [
        ("taught vocabulary, never an imported dictionary", "bridge.SEEDED"),
        ("both readings always kept", "bridge.rows_via"),
        ("whole-word, longest phrase first", "bridge.match"),
        ("the absence is refused a wrong bridge", "bridge.KNOWN_ABSENCE"),
    ]
