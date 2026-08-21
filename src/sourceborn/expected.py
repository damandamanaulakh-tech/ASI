"""STAGE 12 — EXPECTED EVIDENCE GENERATION.

NOTE ON THE NAME: this is `expected.py`, not `evidence.py`. `evidence.py` already
exists and is his Stage-4 evidence ladder (REAL_TOOL / MANUAL / MEMORY /
SIMULATED). I overwrote it while building this and restored it from git; the two
are different jobs and must not share a name.

His loop stage 12, and the one that was blocking the rest of it:

    nothing turns a generated meaning into "if this were true, THIS should
    exist". Without it stages 17-19 have nothing to test against and the loop
    cannot close on evidence.

WHAT A PREDICTION HAS TO BE TO BE WORTH ANYTHING

Three conditions, and the third is the one that does the work:

    1. SPECIFIC     it names where to look, not "more research is needed"
    2. TWO-SIDED    it says what would CONFIRM and what would REFUTE. A claim
                    with no refuting observation cannot be tested at all — his
                    own falsifier rule, applied one stage earlier
    3. DISCRIMINATING
                    a prediction that EVERY meaning makes tests nothing. If
                    1,824 meanings all predict "the object exists", finding the
                    object separates none of them. Non-discriminating
                    predictions are computed, marked, and NOT counted as
                    evidence — the same shape as the role gate and the IDF bar.

WHAT THIS DOES NOT DO

It does not check anything. Checking needs the world, and the world is not in
this repository. Stage 12 generates what *should* be found; whether it *is* found
is a verdict handed in from outside, and stage 17 already accepts those.

So nothing here is verified, nothing is concluded, and no parameter is created.

Canon: docs/method/canon/THE_DISCOVERY_LOOP.md
"""

from __future__ import annotations

MATERIAL = "MATERIAL"          # traces on or in the object itself
COMPANION = "COMPANION"        # other objects that should exist alongside it
PLACEMENT = "PLACEMENT"        # where it should have stood, and how visible
RECORD = "RECORD"              # a separate record that should mention it
REPETITION = "REPETITION"      # the same formula appearing elsewhere
ABSENCE = "ABSENCE"            # what should NOT be found if this is true

CLASSES = (MATERIAL, COMPANION, PLACEMENT, RECORD, REPETITION, ABSENCE)

# What kind of trace each ROLE's activity would leave behind. A carver leaves
# tool marks; an institution leaves records. Read off the roles themselves.
ROLE_EVIDENCE = {
    "SUBJECT":     (PLACEMENT, REPETITION),
    "REQUESTER":   (RECORD, COMPANION),
    "CONTROLLER":  (RECORD, ABSENCE),
    "AUTHOR":      (REPETITION, MATERIAL),
    "SCRIBE":      (MATERIAL, REPETITION),
    "CARVER":      (MATERIAL,),
    "INSTITUTION": (RECORD, COMPANION, PLACEMENT),
    "BENEFICIARY": (COMPANION, RECORD),
    "AUDIENCE":    (PLACEMENT,),
}

# What a FUTURE STATE would require to have been left behind if it was the aim.
FUTURE_EVIDENCE = {
    "FS-1": (PLACEMENT, REPETITION),   # a future observer recognises it
    "FS-2": (RECORD, COMPANION),       # an institution preserves the authority
    "FS-3": (REPETITION, COMPANION),   # a priest repeats the procedure
    "FS-4": (RECORD, COMPANION),       # a successor accepts the continuity
    "FS-5": (PLACEMENT, COMPANION),    # a population sees the legitimacy
    "FS-6": (REPETITION, MATERIAL),    # a workshop reproduces the formula
}

# What each class means as an instruction: where to look, and what settles it.
_LOOK = {
    MATERIAL: ("the worked surface itself",
               "tool marks, finish and inlay consistent with a single "
               "controlled hand",
               "marks from several inconsistent hands, or a finish that "
               "postdates the carving"),
    COMPANION: ("whatever was found with it, or should have been",
                "at least one further object of the same programme",
                "an isolated object with nothing of its kind anywhere near"),
    PLACEMENT: ("the findspot and how visible the object was",
                "a setting where the intended audience could actually see it",
                "a sealed or private context the intended audience could never "
                "reach"),
    RECORD: ("any separate record of the commissioning",
             "a mention outside the object itself",
             "silence in every record that would have had reason to mention it"),
    REPETITION: ("other objects carrying the same arrangement",
                 "the same formula on at least one other object",
                 "a formula that appears exactly once and nowhere else"),
    ABSENCE: ("what should be missing if this reading is right",
              "the absence holds",
              "the thing that should be absent is present"),
}


def _distance(cls: str, base: int) -> int:
    """A prediction inherits its meaning's distance and adds its own reach.

    RECORD and COMPANION reach outside the object, so they travel further and
    owe more. MATERIAL is on the object and owes least."""
    add = {MATERIAL: 0, PLACEMENT: 1, REPETITION: 1,
           COMPANION: 1, RECORD: 2, ABSENCE: 1}[cls]
    return min(5, base + add)


def expect(meaning: dict) -> dict:
    """Turn ONE generated meaning into what should exist if it were true.

    Classes come from the intersection of what the ROLE would leave and what the
    FUTURE STATE would require — plus ABSENCE, which every reading owes, because
    a claim that forbids nothing cannot be wrong."""
    from . import artifact as A
    role = meaning.get("actor_role", "")
    fstate = meaning.get("future_state", "")
    fid = next((f["id"] for f in A.FUTURE_STATES if f["state"] == fstate), "")
    rc = set(ROLE_EVIDENCE.get(role, ()))
    fc = set(FUTURE_EVIDENCE.get(fid, ()))
    both = rc & fc
    either = (rc | fc) - both
    base = meaning.get("origin_distance", 3)
    preds = []
    # ABSENCE is owed by every reading — but only once. Appending it blindly
    # double-counted it wherever a role or future already required it, which is
    # why its share came out above 1.0 per meaning.
    order = sorted(both) + sorted(either)
    if ABSENCE not in order:
        order.append(ABSENCE)
    for cls in order:
        where, confirm, refute = _LOOK[cls]
        preds.append({
            "class": cls,
            "strength": "REQUIRED BY BOTH" if cls in both else
                        ("owed by one side" if cls in either else
                         "owed by every reading"),
            "where_to_look": where,
            "would_confirm": confirm,
            "would_refute": refute,
            "origin_distance": _distance(cls, base),
            "proof_debt": A.ORIGIN_DISTANCE[_distance(cls, base)]["debt"],
            "checked": False,
            "verified": False,
        })
    return {
        "meaning_id": meaning.get("id"),
        "actor_role": role, "future_state": fstate, "future_id": fid,
        "predictions": preds,
        "counts": {"predictions": len(preds),
                   "required_by_both": len(both),
                   "owed_by_one_side": len(either)},
        "testable": bool(preds),
        "checked_anything": False,
        "law": "a prediction must say what would REFUTE it, or it cannot be "
               "tested at all.",
    }


# A prediction shared by more than this fraction of all meanings separates
# nothing. His own shape: a word in forty of his names is not evidence.
DISCRIMINATION_BAR = 0.60


def run(meanings=None, limit: int = 0) -> dict:
    """Stage 12 over a whole generated set, with the discrimination test.

    The test is the point: a prediction that nearly every meaning makes is
    reported NON-DISCRIMINATING and is not counted as evidence, however true it
    might be."""
    from . import artifact as A
    ms = list(meanings if meanings is not None
              else A.generate_meanings()["meanings"])
    if limit:
        ms = ms[:limit]
    rows, freq = [], {}
    for m in ms:
        e = expect(m)
        rows.append(e)
        for p in e["predictions"]:
            freq[p["class"]] = freq.get(p["class"], 0) + 1
    n = max(1, len(ms))
    share = {c: freq.get(c, 0) / n for c in CLASSES}
    non_disc = sorted(c for c in CLASSES if share[c] >= DISCRIMINATION_BAR)
    for e in rows:
        for p in e["predictions"]:
            p["discriminating"] = p["class"] not in non_disc
            if not p["discriminating"]:
                p["why_not"] = ("%d%% of all meanings make this same prediction, "
                                "so finding it separates none of them"
                                % round(100 * share[p["class"]]))
    kept = sum(1 for e in rows for p in e["predictions"] if p["discriminating"])
    total = sum(len(e["predictions"]) for e in rows)
    return {
        "meanings_in": len(ms),
        "sample_warning": ("the discrimination bar is computed over the set you "
                           "hand in. A small or skewed sample changes which "
                           "classes cross it — on 400 meanings 2 classes are "
                           "non-discriminating, on the first 120 it is more, "
                           "because the first 120 all come from the same few "
                           "group combinations. Judge it on a full run."),
        "rows": rows,
        "counts": {
            "predictions_generated": total,
            "discriminating": kept,
            "non_discriminating": total - kept,
            "per_meaning": round(total / n, 2),
            "checked_against_the_world": 0,
            "verified": 0,
            "new_parameters_created": 0,
        },
        "class_share": {c: round(share[c], 3) for c in CLASSES},
        "non_discriminating_classes": non_disc,
        "bar": DISCRIMINATION_BAR,
        "law": "a prediction every meaning makes tests nothing.",
        "refuses": "nothing here is checked. Stage 12 says what should be found; "
                   "whether it IS found is a verdict from outside, and stage 17 "
                   "already accepts those.",
    }


def falsifier_from(meaning: dict) -> dict:
    """Stage 12 feeding stage 17 — the link that was missing.

    His falsifier column was filled by hand. This composes one from what the
    meaning itself predicts, so a generated candidate arrives already testable."""
    e = expect(meaning)
    disc = [p for p in e["predictions"] if p["class"] != ABSENCE]
    if not disc:
        return {"meaning_id": meaning.get("id"), "falsifier": None,
                "falsifiable": False,
                "why": "nothing was predicted, so nothing can flip it"}
    first = disc[0]
    return {
        "meaning_id": meaning.get("id"),
        "falsifier": "%s — %s" % (first["would_refute"],
                                  "look at " + first["where_to_look"]),
        "falsifiable": True,
        "from_prediction": first["class"],
        "origin_distance": first["origin_distance"],
        "proof_debt": first["proof_debt"],
        "feeds": "intent_ledger.kill",
        "law": "a candidate should arrive carrying what would flip it, not wait "
               "for one to be written by hand.",
    }


def stats() -> dict:
    r = run(limit=200)
    return {
        "classes": len(CLASSES),
        "roles_mapped": len(ROLE_EVIDENCE),
        "futures_mapped": len(FUTURE_EVIDENCE),
        "bar": DISCRIMINATION_BAR,
        "sample_of": r["meanings_in"],
        "predictions_per_meaning": r["counts"]["per_meaning"],
        "non_discriminating_classes": r["non_discriminating_classes"],
        "checked_against_the_world": 0,
        "new_parameters_created": 0,
        "source": "docs/method/canon/THE_DISCOVERY_LOOP.md",
    }


def annotations() -> list:
    return [
        ("if this were true, THIS should exist", "expected.expect"),
        ("a prediction must say what would refute it", "expected._LOOK"),
        ("a prediction every meaning makes tests nothing", "expected.run"),
        ("a candidate arrives carrying its own falsifier",
         "expected.falsifier_from"),
    ]
