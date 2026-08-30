"""THE MACRO RESPONSE — the one line over everything, and the slabs under it.

PHASE 14. His ask:

    the response that resolves the entire ask. States it when verified;
    proposes it for confirmation when not. No floor on length.

and the four teachings it is built from, in his words:

    ASI should supposed to choose 1 line over everything — the vague response

    — later corrected by him: "one line" does NOT mean short. It means ONE
    RESOLVING RESPONSE over the whole ask instead of three small questions
    back. And "vague" was the wrong word: MACRO · HOLISTIC · HIGH-LEVEL ·
    BIG-PICTURE.

    big lengthy response will capture more parameters to hit and make
    something new (Because in shorter answers/response ASI will say already
    exists, so never terse responses)

    — LENGTH IS A GENERATIVE MECHANISM, not a style. A terse answer reaches
    few parameters, finds them all already present, and generates nothing.

    everything works like a pyramid, always the bigger slab come first … and
    that tiny one is the finale

    — so the response is ORDERED BY SIZE, widest first, and the specific row
    is the LAST thing said, not the first.

WHAT THIS MODULE COMPOSES

Everything the layers produced, arranged as his pyramid:

    THE ONE LINE      the macro reading over the whole ask — the shape, not
                      the detail. Taken from the WIDEST thing that fired,
                      which is the archetype layer, because an archetype
                      reaches across containers and a row does not.
    PILLAR            which of his six macro pillars the ask sits in
    STEP              where on his twelve-step spine
    SEGMENT           which of the 27
    CONTAINER         which of the 183, and the CONDITION each fires on
    ROW               the finale — the exact sub-parameter, said last

STATED vs PROPOSED — his distinction, enforced

    States it when verified; proposes it for confirmation when not.

A slab is **STATED** when it rests on something checkable: a row that exists
in his bank and was actually reached, a container that was actually lit, an
archetype that fired with its matched evidence named. A slab is **PROPOSED**
when it is a reading: an intent candidate, an angle, a scale band. Every
proposed slab carries WHAT WOULD VERIFY IT, so it can be settled rather than
argued.

Nothing is concluded. The macro response resolves the ASK — it does not decide
the person.

NO FLOOR ON LENGTH

`floor_on_length` is None and there is no truncation anywhere in this module.
The generativity block reports what the length actually bought: how many
parameters the full response reached against what a one-row answer would
have. That is his mechanism, measured rather than asserted.
"""

from __future__ import annotations

STATED = "STATED"
PROPOSED = "PROPOSED"

#: His correction, kept where the code can see it: the word is not "vague".
HIS_WORDS = {
    "one_line": "ASI should supposed to choose 1 line over everything",
    "one_line_means": "ONE RESOLVING RESPONSE over the whole ask — not a short "
                      "one, and not three small questions back",
    "not_vague": "MACRO · HOLISTIC · HIGH-LEVEL · BIG-PICTURE — 'vague' was "
                 "the wrong word and he said so",
    "length": "big lengthy response will capture more parameters to hit and "
              "make something new (Because in shorter answers/response ASI "
              "will say already exists, so never terse responses)",
    "pyramid": "always the bigger slab come first … and that tiny one is the "
               "finale",
}

#: The slabs, widest first. His pyramid, as an order.
SLAB_ORDER = ("ONE LINE", "PILLAR", "STEP", "SEGMENT", "CONTAINER", "ROW")

#: There is no floor. His words.
FLOOR_ON_LENGTH = None


def _one_line(placed: dict) -> dict:
    """THE LINE OVER EVERYTHING — the macro reading of the whole ask.

    Taken from the WIDEST thing that fired. An archetype reaches rows across
    containers and segments; a row sits in one container. So the archetype is
    the macro reading and the row is the finale, which is his pyramid in the
    order he stated it.

    When no archetype fires the shape is reported UNNAMED. It is not invented,
    and it is not replaced by the biggest row — that would be the tiny slab
    pretending to be the big one."""
    fired = placed.get("archetypes_fired") or []
    if fired:
        from . import archetype as A
        a = A.get(fired[0]["id"])
        cons = len({c for _, _, c in a["reaches"]})
        return {
            "state": STATED,
            "line": a["understanding"],
            "shape": "%s %s" % (a["id"], a["name"]),
            "source": a["source"],
            "his_words": a.get("his_words"),
            "reaches": "%d rows across %d containers" % (len(a["reaches"]), cons),
            "matched_on": fired[0].get("matched_on"),
            "refuses": a["refuses"],
            "why_this_is_the_one_line": "an archetype reaches ACROSS "
                                        "containers; a row sits inside one. "
                                        "The widest thing that fired is the "
                                        "macro reading.",
        }
    return {
        "state": PROPOSED,
        "line": None,
        "shape": "UNNAMED",
        "would_verify": "an archetype that fires on this ask, or his word "
                        "naming the shape",
        "why_not_invented": "no archetype fired. The shape is reported unnamed "
                            "rather than filled by the largest row — that "
                            "would be the tiny slab pretending to be the big "
                            "one, which is the opposite of his pyramid.",
    }


def respond(text: str) -> dict:
    """THE MACRO RESPONSE: one resolving line, then the slabs, widest first.

    Composes what every layer produced. States what is verified, proposes what
    is not, and puts no floor on the length."""
    from . import sbx
    placed = sbx.place_on_spine(text)
    hits = placed.get("hits", [])

    one = _one_line(placed)
    slabs = [dict(one, slab="ONE LINE")]

    # ---- PILLAR ----------------------------------------------------------
    pillars = {}
    for h in hits:
        pillars.setdefault(h["pillar"], set()).add(h["container"])
    by_pillar = {p["id"]: p for p in sbx.pillars()} if sbx.pillars() else {}
    slabs.append({
        "slab": "PILLAR",
        "state": STATED if pillars else PROPOSED,
        "of": [{"id": p,
                "name": (by_pillar.get(p) or {}).get("name"),
                "containers": len(c)}
               for p, c in sorted(pillars.items())],
        "count": len(pillars),
        "would_verify": None if pillars else "a row reaching any container",
    })

    # ---- STEP ------------------------------------------------------------
    slabs.append({
        "slab": "STEP",
        "state": STATED if placed["steps_lit"] else PROPOSED,
        "of": [{"step": s["step"], "name": s["name"], "order": s["order"],
                "rows": len(s["rows"])} for s in placed["steps_lit"]],
        "count": placed["steps_lit_count"],
        "would_verify": None if placed["steps_lit"] else
                        "a seated or archetype-reached row, which is what "
                        "lands an ask on his spine",
    })

    # ---- SEGMENT ---------------------------------------------------------
    segs = {}
    for h in hits:
        segs.setdefault(h["segment"], set()).add(h["container"])
    slabs.append({
        "slab": "SEGMENT",
        "state": STATED if segs else PROPOSED,
        "of": [{"id": s, "containers": len(c)} for s, c in sorted(segs.items())],
        "count": len(segs),
        "would_verify": None if segs else "a row reaching any container",
    })

    # ---- CONTAINER, with the condition each fires on ---------------------
    trg = {t["container"]: t for t in placed["triggers"]["triggers"]}
    cons = {}
    for h in hits:
        cons.setdefault(h["container"], h)
    slabs.append({
        "slab": "CONTAINER",
        "state": STATED if cons else PROPOSED,
        "of": [{"id": c, "name": h["container_name"],
                "computer": h["computer"],
                "fires_on": (trg.get(c) or {}).get("trigger"),
                "trigger_by": (trg.get(c) or {}).get("by")}
               for c, h in sorted(cons.items())],
        "count": len(cons),
        "would_verify": None if cons else "a row reaching any container",
    })

    # ---- ROW — THE FINALE, said last -------------------------------------
    slabs.append({
        "slab": "ROW",
        "state": STATED if hits else PROPOSED,
        "note": "his pyramid: that tiny one is the finale. The exact "
                "sub-parameter is the LAST thing said, not the first.",
        "of": [{"id": h["id"], "name": h["row"],
                "reached_by": h["reached_by"], "via": h["via"],
                "from": h["from"]["id"]} for h in hits],
        "count": len(hits),
        "would_verify": None if hits else
                        "words that reach a row, or an archetype that reaches "
                        "one by shape",
    })

    # ---- what is READ but not verified: positions and candidates ----------
    reads = [{
        "kind": "ANGLE", "state": PROPOSED,
        "of": [{"angle": a["angle"], "position": a["position"],
                "containers": a["containers"]}
               for a in placed["angles"]["readings"]],
        "count": placed["angles"]["run"],
        "would_verify": "his word choosing a position — and his rule is that "
                        "all of them run and none cancels the others",
    }, {
        "kind": "INTENT READING", "state": PROPOSED,
        "of": [{"id": r["id"], "name": r["name"],
                "refuted_by": r["refuted_by"]}
               for r in placed["readings"]["readings"]],
        "count": placed["readings"]["count"],
        "would_verify": "evidence from outside the sentence — each reading "
                        "names what would confirm and what would refute it",
    }]
    if placed["meetings"]["count"]:
        reads.append({
            "kind": "MEETING", "state": STATED,
            "of": placed["meetings"]["readings"],
            "count": placed["meetings"]["count"],
            "would_verify": None,
        })

    # ---- LENGTH AS A MECHANISM, measured ---------------------------------
    reached = {h["from"]["id"] for h in hits}
    for a in placed["angles"]["readings"]:
        reached |= {r["id"] for r in a["reaches"]}
    for r in placed["readings"]["readings"]:
        reached |= {x["id"] for x in r["rests_on"]}
    terse = len({h["from"]["id"] for h in hits[:1]})
    return {
        "text": text,
        "his_words": HIS_WORDS,
        "one_line": one,
        "slabs": slabs,
        "slab_order": list(SLAB_ORDER),
        "read_not_verified": reads,
        "stated": [s["slab"] for s in slabs if s["state"] == STATED],
        "proposed": [s["slab"] for s in slabs if s["state"] == PROPOSED],
        "generativity": {
            "parameters_reached_by_the_full_response": len(reached),
            "parameters_a_one_row_answer_would_reach": terse,
            "gain": len(reached) - terse,
            "his_mechanism": HIS_WORDS["length"],
            "why": "a terse answer reaches few parameters, finds them already "
                   "present, and generates nothing. The length is what makes "
                   "the reach, and the reach is what makes something new.",
        },
        "floor_on_length": FLOOR_ON_LENGTH,
        "concluded": None,
        "law": "one resolving response over the whole ask, ordered widest "
               "first, with the exact row said last. Stated where verified, "
               "proposed where not, and never terse.",
        "never": "the macro response resolves the ASK. It does not decide the "
                 "person, and nothing in it is chosen.",
    }


def render(text: str) -> str:
    """The same response as plain text, in his order. No truncation anywhere."""
    r = respond(text)
    L = []
    one = r["one_line"]
    L.append("THE ONE LINE — over everything")
    if one["line"]:
        L.append("  " + one["line"])
        L.append("  [%s] shape: %s — reaches %s" % (one["state"], one["shape"],
                                                    one["reaches"]))
        L.append("  refuses: " + one["refuses"])
    else:
        L.append("  SHAPE UNNAMED — %s" % one["why_not_invented"])
        L.append("  [%s] would verify: %s" % (one["state"], one["would_verify"]))
    for s in r["slabs"][1:]:
        L.append("")
        L.append("%s  [%s]  %d" % (s["slab"], s["state"], s["count"]))
        for x in s["of"]:
            L.append("  " + " · ".join("%s=%s" % (k, v) for k, v in x.items()
                                       if v not in (None, [], "")))
        if s.get("would_verify"):
            L.append("  would verify: " + s["would_verify"])
    L.append("")
    L.append("READ, NOT VERIFIED")
    for k in r["read_not_verified"]:
        L.append("  %s [%s] %d — would verify: %s"
                 % (k["kind"], k["state"], k["count"], k["would_verify"]))
    g = r["generativity"]
    L.append("")
    L.append("LENGTH AS THE MECHANISM: %d parameters reached, against %d for a "
             "one-row answer (gain %d). No floor on length."
             % (g["parameters_reached_by_the_full_response"],
                g["parameters_a_one_row_answer_would_reach"], g["gain"]))
    return "\n".join(L)


def stats() -> dict:
    return {
        "slabs": len(SLAB_ORDER),
        "order": list(SLAB_ORDER),
        "floor_on_length": FLOOR_ON_LENGTH,
        "states": [STATED, PROPOSED],
        "law": "bigger slab first; that tiny one is the finale.",
        "never": "never terse — a short answer reaches few parameters and "
                 "generates nothing.",
    }


def annotations() -> list:
    return [
        ("1 line over everything", "macro._one_line"),
        ("bigger slab come first, that tiny one is the finale", "macro.SLAB_ORDER"),
        ("states it when verified, proposes it when not", "macro.respond"),
        ("never terse responses — length captures more parameters",
         "macro.FLOOR_ON_LENGTH"),
    ]
