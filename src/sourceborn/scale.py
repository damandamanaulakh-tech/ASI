"""THE SCALE AXIS — the same understanding, read at every size.

PHASE 11. His ask, and his ruling on it:

    scale becomes a stored axis on every archetype — more than four, as you
    said; the four you named are a start, not the set.

    Gate: you name the scales, or approve a proposed set.

WHY SCALE IS AN AXIS AND NOT A LABEL

His teaching on the books is the reason this layer exists at all:

    One event of those books is used in 100 daily responses.

An archetype that only fits one size is a story. THE RECOVERY STAKE is not a
story about a king with dice — it is the same arrangement in a child who will
not switch off a game he is losing, in a trader averaging down, in a person
arguing past the point of repair, and in a nation escalating a war rather than
admit defeat. Those are not four archetypes. They are ONE, read at four sizes.

So scale is a stored axis: a coordinate the reading moves along, not a tag it
carries.

THE FOUR ARE HIS. THE FIVE PROPOSED ARE DERIVED FROM HIS OWN MATERIAL.

He named four — micro · individual · relational · macro — and ruled that they
are a start. This module does not invent the rest. Each proposed band cites the
example OF HIS that demands it: a band exists here only because one of his own
worked examples sits at a size the four cannot hold.

**THE GATE IS HONOURED.** His four are `HIS` and active. The five proposed are
`PROPOSED` and carry `approved: False` — they are stored, readable and
attached to his examples so he can judge them, and a test proves the active set
is exactly his four until he says otherwise. Building the axis is not the same
as naming the bands, and only he names the bands.
"""

from __future__ import annotations

#: His four, in his own words, with the reading he gave each on ARCH-001.
HIS_BANDS = (
    {
        "id": "SC-01", "name": "micro", "by": "HIS",
        "size": "one person, one small moment",
        "his_example": "a kid refusing to turn off a game he is losing",
        "approved": True,
    },
    {
        "id": "SC-02", "name": "individual", "by": "HIS",
        "size": "one person, one life",
        "his_example": "a gambler; a trader averaging down on a failing stock",
        "approved": True,
    },
    {
        "id": "SC-03", "name": "relational", "by": "HIS",
        "size": "two or more people, in relation",
        "his_example": "a person arguing past the point of repair to win",
        "approved": True,
    },
    {
        "id": "SC-04", "name": "macro", "by": "HIS",
        "size": "a people, a state, a whole population",
        "his_example": "a nation escalating a war rather than admit defeat",
        "approved": True,
    },
)

#: PROPOSED, NOT APPROVED. Each exists because one of HIS OWN worked examples
#: sits at a size his four cannot hold. Nothing here is invented to fill a
#: pattern; the citation is the whole justification, and if the citation is
#: wrong the band should be struck.
PROPOSED_BANDS = (
    {
        "id": "SC-00", "name": "moment", "by": "PROPOSED",
        "size": "a single act inside one event, below the person",
        "why_needed": "his stealing demonstration is about ONE ACT — the hand "
                      "moving — and explicitly not about the man. `micro` is "
                      "still a person; this is smaller than a person. Without "
                      "it, 'THIEF is a conclusion, taking money is the "
                      "observation' has no coordinate to sit at.",
        "his_example": "a man is stealing money — thief / opportunity / habit "
                       "/ saving a life",
        "sits_below": "SC-01",
        "approved": False,
    },
    {
        "id": "SC-02b", "name": "household", "by": "PROPOSED",
        "size": "a family — the people whose burdens are not optional",
        "why_needed": "ARCH-010 is stated in his words as 'family, friends and "
                      "coworkers', and the father-and-door example is a "
                      "household, not a relation between two equals. "
                      "`relational` reads two parties meeting; a household is "
                      "standing obligation nobody chose.",
        "his_example": "a person whom family, friends and coworkers call good "
                       "— left with the memories only",
        "sits_between": ["SC-02", "SC-03"],
        "approved": False,
    },
    {
        "id": "SC-03b", "name": "organisation", "by": "PROPOSED",
        "size": "a company, a party, a team — a body with a stated purpose",
        "why_needed": "his BJP example is a PARTY choosing a leader for a task, "
                      "and ARCH-003's 'top-heavy pyramid built on lies' is a "
                      "company. Neither is relational (they are not two people "
                      "meeting) and neither is macro (they are not a "
                      "population). His own weighting mechanism lives at this "
                      "size and nowhere else.",
        "his_example": "BJP choosing for a task — highest seniority YES ≠ "
                       "highest suitability AUTOMATIC",
        "sits_between": ["SC-03", "SC-04"],
        "approved": False,
    },
    {
        "id": "SC-04b", "name": "dynasty", "by": "PROPOSED",
        "size": "a line that outlives its members — a house, a succession",
        "why_needed": "what Yudhishthira stakes is not his own life and not a "
                      "nation's: it is a HOUSE, and the loss lands on people "
                      "not yet born. `macro` reads a population now; a dynasty "
                      "is a population across time.",
        "his_example": "the dice game — a kingdom and a line lost in one "
                       "sitting",
        "sits_between": ["SC-04", "SC-05"],
        "approved": False,
    },
    {
        "id": "SC-05", "name": "civilisation", "by": "PROPOSED",
        "size": "an epoch — thousands of years, many peoples",
        "why_needed": "his own frame for the books is 'since modern humans "
                      "came out of caves', and the tablet he is reading is "
                      "~5,500 years old. If the largest band is a nation, the "
                      "thing he says the archetypes actually operate at has no "
                      "coordinate.",
        "his_example": "one event of those books is used in 100 daily "
                       "responses; the Egyptian tablet, ~5,500 years back",
        "sits_above": "SC-04",
        "approved": False,
    },
)

#: His ruling on this layer with ARCHETYPE and LINK.
CEILING = None


def bands(include_proposed: bool = True) -> list:
    """The axis, smallest to largest. His four are always in it; the proposed
    five are included for his judgement and marked unapproved."""
    order = ["SC-00", "SC-01", "SC-02", "SC-02b", "SC-03", "SC-03b", "SC-04",
             "SC-04b", "SC-05"]
    all_b = {b["id"]: b for b in HIS_BANDS + PROPOSED_BANDS}
    out = []
    for bid in order:
        b = all_b[bid]
        if b["approved"] or include_proposed:
            out.append(dict(b, position=len(out) + 1))
    return out


def active() -> list:
    """The bands that actually apply — approved only.

    HIS GATE, ENFORCED: until he names or approves, this is his four. The
    proposals are stored and readable; they are not in force."""
    return bands(include_proposed=False)


def of(archetype_id: str) -> dict:
    """One archetype's reading at every band.

    A band he has not filled says NOT STATED — it is never invented to make the
    axis look complete. That is his own rule everywhere else and it holds here:
    an unstated dimension says *not stated*, never zero."""
    from . import archetype as A
    a = A.get(archetype_id)
    if not a.get("id"):
        return {"found": False, "id": archetype_id}
    scale = a.get("scale", {})
    rows = []
    for b in bands():
        given = scale.get(b["name"])
        rows.append({
            "band": b["id"], "name": b["name"], "position": b["position"],
            "by": b["by"], "approved": b["approved"],
            "reading": given if given else None,
            "state": "HIS READING" if given else "NOT STATED",
        })
    return {
        "archetype": a["id"], "archetype_name": a["name"],
        "source": a["source"],
        "bands": rows,
        "filled": sum(1 for r in rows if r["reading"]),
        "not_stated": sum(1 for r in rows if not r["reading"]),
        "law": "a band he has not filled says NOT STATED. It is never invented "
               "to make the axis look complete.",
    }


def spread(text: str) -> dict:
    """THE PROOF: the same ask read at every size.

    His teaching made mechanical — *one event of those books is used in 100
    daily responses*. Whichever archetypes the ask fires, each is returned at
    every band, so the reading is a COORDINATE and not a label. Nothing is
    chosen: which size the ask actually sits at is not knowable from the
    sentence."""
    from . import archetype as A
    fired = A.fires_on(text)
    out = []
    for f in fired["fired"]:
        out.append(of(f["id"]))
    return {
        "text": text,
        "archetypes_fired": [f["id"] for f in fired["fired"]],
        "at_scale": out,
        "bands_available": len(bands()),
        "bands_active": len(active()),
        "readings": sum(x["filled"] for x in out),
        "chosen": None,
        "law": "one arrangement, read at every size. Which size this ask sits "
               "at is not knowable from the sentence, so nothing is chosen.",
    }


def coverage() -> dict:
    """How much of the axis his own material actually fills.

    Reported honestly: the four he named are filled on every archetype because
    he wrote them; the five proposed are empty because he has not been asked
    yet. That gap is the gate, not a defect."""
    from . import archetype as A
    per_band = {b["name"]: 0 for b in bands()}
    for a in A.archetypes():
        for name in a.get("scale", {}):
            if name in per_band:
                per_band[name] += 1
    total = len(A.archetypes())
    return {
        "archetypes": total,
        "bands": len(bands()),
        "cells": total * len(bands()),
        "filled": sum(per_band.values()),
        "per_band": per_band,
        "empty_bands": [k for k, v in per_band.items() if v == 0],
        "why_empty": "the five proposed bands hold nothing because he has not "
                     "approved them. Filling them before he names them would "
                     "be inventing his axis for him.",
        "his_call": True,
    }


def gate() -> dict:
    """The gate on this phase, stated plainly."""
    return {
        "his_words": "you name the scales, or approve a proposed set",
        "his_bands": [b["name"] for b in HIS_BANDS],
        "proposed": [{"id": b["id"], "name": b["name"], "size": b["size"],
                      "why_needed": b["why_needed"],
                      "his_example": b["his_example"]}
                     for b in PROPOSED_BANDS],
        "approved": False,
        "in_force": [b["name"] for b in active()],
        "law": "building the axis is not the same as naming the bands. The "
               "axis is built and the proposals are stored where he can read "
               "them; only his four are in force.",
    }


def stats() -> dict:
    return {
        "bands_total": len(bands()),
        "bands_his": len(HIS_BANDS),
        "bands_proposed": len(PROPOSED_BANDS),
        "bands_in_force": len(active()),
        "ceiling": CEILING,
        "approved": False,
        "law": "more than four — his ruling. Each proposed band cites the "
               "example OF HIS that demands it; nothing is invented to fill a "
               "pattern.",
        "never": "a band he has not filled says NOT STATED, never zero.",
    }


def annotations() -> list:
    return [
        ("scale is a stored axis, more than four", "scale.bands"),
        ("one event of those books is used in 100 daily responses",
         "scale.spread"),
        ("you name the scales, or approve a proposed set", "scale.gate"),
        ("a band he has not filled says NOT STATED", "scale.of"),
    ]
