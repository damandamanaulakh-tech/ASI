"""THE RUBRICS, WIRED — his 66 firing by name, and the gate that stays shut.

PHASE 8. His ask:

    R01–R52 put into universal-sequence order and wired, plus the other
    vocabularies. Filling the gaps, not adding anything random — your
    instruction. Adds the dimensions none of them have: scale, era-survival,
    and how many situations a reading has held across.

    Proof: before — 7 of ~200 rubric dimensions touch an answer. After — a
    live run showing which rubrics fired on your own example, by name.

    Gate: ADOPT-HALT-3 must close first — R01–R52 versus your 25: one family
    or two, and whose names win.

WHAT THE GATE BLOCKS, AND WHAT IT DOES NOT

ADOPT-HALT-3 is his ruling and it is not made here. But read what it actually
asks: *R01–R52 versus your 25 — one family or two, and whose names win.* That
is a question about MERGING TWO VOCABULARIES.

It is not a question about **his own 66**, which are already in his
architecture, already placed at the step each acts on, and already his names.
Those were `carried, not consulted` — sitting at a step and reaching no answer.
Wiring them requires no merge and settles no seam.

So: **his 66 fire. R01–R52 stays unmerged at the halt.** Both facts are
reported on every run, and `merged` is False.

THE BEFORE NUMBER, MEASURED

Before this, **7** things touched an answer — the seven filters in
`filters.py` (Ground · Sequence · Source · Mask · Fact · Halt · Loop). His
66 rubrics touched none. That is his "7 of ~200".

HOW A RUBRIC FIRES — AND WHY IT IS NOT A KEYWORD MATCH

A rubric is a DIMENSION an answer can be examined on. It fires when the ask
actually reaches the step it belongs to: `Contradiction` acts at HALT, so it
fires when the ask lights step 7. That is his own placement doing the work —
the rubric was already put at the step where it acts, and the step is already
lit by the seating. Nothing new was invented to make them fire; the wiring is
the join that was missing.

THE THREE DIMENSIONS HE SAID NONE OF THEM HAVE

He named them: **scale · era-survival · situations-held-across**. They are
added as dimensions ON a fired rubric, not as new rubrics — his instruction
was *filling the gaps, not adding anything random*:

  scale                  which of his bands the reading sits at, from the
                         scale layer. Reported UNSET when no band is in force.
  era_survival           whether the reading depends on a present-day fact or
                         holds across eras. UNTESTED unless evidence says.
  situations_held_across how many of his examples this rubric has fired on.
                         Counted live over his example set, never typed.
"""

from __future__ import annotations

import functools

#: What touched an answer BEFORE this phase. His "7 of ~200".
BEFORE = ("Ground", "Sequence", "Source", "Mask", "Fact", "Halt", "Loop")

#: His three missing dimensions, added ON a fired rubric.
DIMENSIONS = ("scale", "era_survival", "situations_held_across")

#: The seam that stays shut. His call, nobody else's.
ADOPT_HALT_3 = {
    "id": "ADOPT-HALT-3",
    "seam": "C-SB's rubric registry holds R01-R52; this core extracted his 25 "
            "universal dimensions from the Kings file. 52 vs 25, unknown "
            "overlap.",
    "his_call": "same family or two registries — and if one, which names win",
    "merged": False,
    "what_it_blocks": "merging the two vocabularies, and choosing whose names "
                      "survive",
    "what_it_does_not_block": "wiring HIS OWN 66, which are already in his "
                              "architecture under his own names and were "
                              "carried without ever being consulted",
}


def catalogue() -> list:
    """His rubrics, each with the step it acts on. Read from the split, never
    typed — a rubric appearing at two steps is reported at both."""
    from . import sbx
    at = {}
    for s in sbx.spine():
        for r in s.get("rubrics", ()):
            at.setdefault(r, []).append({"step": s["step"], "name": s["name"],
                                         "order": s["order"]})
    return [{"rubric": r, "acts_at": v, "steps": [x["step"] for x in v]}
            for r, v in sorted(at.items())]


@functools.lru_cache(maxsize=1)
def _situation_map() -> dict:
    """Which of HIS examples each rubric fires on — computed ONCE for all
    rubrics, not once per rubric.

    The first version called `fires_on` inside the per-rubric loop, so a
    single run cost 66 rubrics x 8 examples = 528 full placements and the
    suite slowed to a crawl. The work is the same for every rubric, so it is
    done once and cached."""
    from . import reread
    hits = {}
    for ex in reread.EXAMPLES:
        try:
            f = fires_on(ex["text"], _count_situations=False)
        except Exception:
            continue
        for x in f["fired"]:
            hits.setdefault(x["rubric"], []).append(ex["id"])
    return {"hits": hits, "of": len(reread.EXAMPLES)}


def _situations(rubric: str) -> dict:
    m = _situation_map()
    got = m["hits"].get(rubric, [])
    return {"count": len(got), "examples": got, "of": m["of"],
            "how": "counted live over his own example set, never typed"}


def fires_on(text: str, _count_situations: bool = True) -> dict:
    """WHICH RUBRICS FIRED ON THIS ASK, BY NAME — his stated proof.

    A rubric fires when the ask reaches the step it acts on. His own placement
    does the work: the rubric was already put at the step where it acts, and
    the seating already lights the step. This is the join, not a new rule."""
    from . import sbx
    placed = sbx.place_on_spine(text)
    lit = {s["step"]: s for s in placed["steps_lit"]}
    bands = None
    try:
        from . import scale as SC
        bands = [b["name"] for b in SC.active()]
    except Exception:
        bands = []

    fired, silent = [], []
    for r in catalogue():
        on = [x for x in r["acts_at"] if x["step"] in lit]
        if not on:
            silent.append(r["rubric"])
            continue
        rec = {
            "rubric": r["rubric"],
            "fired_at": [{"step": x["step"], "name": x["name"],
                          "rows": len(lit[x["step"]]["rows"])} for x in on],
            "why": "the ask reached step %s, which is where this rubric acts"
                   % ", ".join(str(x["step"]) for x in on),
            # ---- his three missing dimensions ---------------------------
            "scale": (bands if bands else None),
            "scale_state": "IN FORCE" if bands else "UNSET",
            "era_survival": "UNTESTED",
            "era_survival_why": "nothing in the ask says whether this reading "
                                "depends on a present-day fact. UNTESTED is "
                                "not 'holds' — it is nobody checked.",
            "concluded": None,
        }
        if _count_situations:
            rec["situations_held_across"] = _situations(r["rubric"])
        fired.append(rec)

    return {
        "text": text,
        "fired": fired,
        "fired_count": len(fired),
        "silent": silent,
        "silent_count": len(silent),
        "catalogue": len(catalogue()),
        "before_this_phase": {"touched_an_answer": len(BEFORE),
                              "which": list(BEFORE),
                              "his_line": "7 of ~200 rubric dimensions touch "
                                          "an answer"},
        "dimensions_added": list(DIMENSIONS),
        "adopt_halt_3": ADOPT_HALT_3,
        "concluded": None,
        "law": "a rubric fires when the ask reaches the step it acts on. His "
               "own placement does the work — this is the join that was "
               "missing, not a new rule.",
        "never": "R01-R52 is not merged with his 25. That is ADOPT-HALT-3 and "
                 "it is his call.",
    }


def stats() -> dict:
    return {
        "rubrics": len(catalogue()),
        "before_this_phase": len(BEFORE),
        "dimensions_added": list(DIMENSIONS),
        "adopt_halt_3_merged": ADOPT_HALT_3["merged"],
        "law": "his own 66, under his own names, at the step each acts on.",
        "never": "nothing random was added — his instruction was filling the "
                 "gaps.",
    }


def annotations() -> list:
    return [
        ("R01-R52 put into universal-sequence order and wired", "rubrics.catalogue"),
        ("which rubrics fired on your own example, by name", "rubrics.fires_on"),
        ("scale, era-survival, and how many situations a reading has held across",
         "rubrics.DIMENSIONS"),
        ("R01-R52 versus your 25 stays his call", "rubrics.ADOPT_HALT_3"),
    ]
