"""THE RE-READ — every example of his, read again under the new rulings.

PHASE 15. His ask, and the proof he named for it:

    every file, every example and every teaching re-read under the new rulings
    — your Q3 answer. The rain example was proved on the old body/brain ruling
    and must be re-read on the new one.

    Proof: a per-file report of what changed and what did not.

and, when he asked how many phases were done, he named this one himself:

    one was change of meaning n outcomes from the old example n quotes i
    provided

WHY A RE-READ IS NECESSARY AND NOT OPTIONAL

Every example he gave was read under the rulings that existed on the day it
arrived. The rulings have moved since — nine times, each one his. The rain
example was seated when HUMAN still meant the whole person; his correction made
Human mean the BODY, and nothing went back to re-read the rain sentence under
it. The dice game seated zero rows because there was no archetype layer. The
mall example was read before FUTURE scope existed.

So a reading recorded in the canon is a reading AT A DATE. Left alone it slowly
becomes a claim about today that nobody checked.

WHAT THIS MODULE DOES, AND WHAT IT REFUSES TO DO

For each of his examples it holds:

  THEN   the reading as it was RECORDED, with the file and line it was
         recorded in. Never reconstructed, never estimated. Where nothing was
         recorded it says NOT RECORDED — an absence, not a zero.
  NOW    the reading the live system produces today, run through every layer.
  RULING which of his rulings is responsible for the difference.

It CHANGES NOTHING. A re-read is a report: it does not re-file the example, it
does not correct the canon, and it does not decide that the new reading is the
right one. Two readings of the same example are exactly the situation his own
law covers — both are kept, the gap goes to him.

WHAT A CHANGE MEANS, AND WHAT IT DOES NOT

A number moving is not by itself a defect. `0 -> 20 rows` on the stealing
example is the archetype layer doing the job it was built for. What matters is
that every movement has a NAMED CAUSE. A movement with no ruling behind it is
the finding — that is drift, and it is reported as `UNEXPLAINED`.
"""

from __future__ import annotations

#: His rulings, in the order they landed, each with what it changed about how
#: an example is read. These are the causes a movement is checked against.
RULINGS = (
    {"id": "R-BODY", "date": "2026-08-13",
     "his_words": "Human = the physical human — body, appearance, biological "
                  "condition, safety, survival. Human is NOT the thinking/"
                  "memory/reasoning brain",
     "changed": "a body word no longer drags a cognition container in with it; "
                "SEG-01 fires only when the body is actually named",
     "where": "domains.py"},
    {"id": "R-SPLIT", "date": "2026-08-29",
     "his_words": "rebuild it complete with all 183 containers and all rows",
     "changed": "10 segments/80 containers became 27/183, and a seated row now "
                "lands on a single-meaning container instead of one carrying "
                "up to five meanings",
     "where": "sbx.py"},
    {"id": "R-ARCHETYPE", "date": "2026-08-29",
     "his_words": "now build the archetype layer from the holy books",
     "changed": "an example whose WORDS reach no row can now reach rows by "
                "SHAPE. This is the largest single mover.",
     "where": "archetype.py"},
    {"id": "R-TRIGGER", "date": "2026-08-29",
     "his_words": "below more may be repated",
     "changed": "every lit container now also reports the CONDITION it fires "
                "on, so an example reads as firing conditions and not nouns",
     "where": "trigger.py"},
    {"id": "R-LINK", "date": "2026-08-29",
     "his_words": "Diamond cut diamond becomes a stored link between two "
                  "ego-rows",
     "changed": "a reading that belongs to the MEETING of two rows can be "
                "returned at all — no row and no container could hold it",
     "where": "link.py"},
    {"id": "R-READINGS", "date": "2026-08-29",
     "his_words": "a live run on 'a man is stealing the money' producing all "
                  "nine readings where it produces zero today",
     "changed": "an event returns every intent it could carry, each naming "
                "what would refute it, instead of a list of type ids",
     "where": "readings.py"},
    {"id": "R-FRONT-BACK", "date": "2026-08-29",
     "his_words": "use new parameters in front n old in back",
     "changed": "a reached row leads with its split id and carries the source "
                "row behind it; the old bank is untouched",
     "where": "sbx.front_back"},
)

#: His examples. `then` is what was RECORDED, with the file and line it was
#: recorded at — nothing here is reconstructed from memory. `expect` names the
#: rulings that should account for any movement.
EXAMPLES = (
    {
        "id": "EX-RAIN",
        "name": "THE RAIN SENTENCE",
        "his_words": "when i want to take my kids out … the father was standing "
                     "at the door and pointed it in the air",
        "text": ("kids father was standing outside with water pipe and pointed "
                 "it in the air so that the kids inside the home thought its "
                 "raining outside"),
        "instrument": "seating",
        "then": {"recorded": "seated on Air/breathing drive and Thought "
                             "suppression; later 2 ids, and the seating "
                             "'still shows Standing balance when the father is "
                             "not balancing'",
                 "rows": 2,
                 "row_names": ["Air/breathing drive", "Thought suppression"],
                 "known_defect": "still shows Standing balance when the father "
                                 "is not balancing",
                 "source": "CLAUDE.md — the growing-phase and self-make entries"},
        "expect": ["R-BODY", "R-SPLIT"],
        "why_it_matters": "HIS OWN NAMED CASE. It was proved under the old "
                          "body/brain ruling and never re-read under the new "
                          "one.",
    },
    {
        "id": "EX-DICE",
        "name": "THE DICE GAME",
        "his_words": "betting is worst, u can loose ur pride too",
        "text": "he bet everything he had to win it all back and lost what he "
                "could never recover",
        "instrument": "seating",
        "then": {"recorded": "seated ZERO rows — the rows existed (P1873 "
                             "Sunk-cost sensitivity, P2517 Commitment "
                             "escalation risk) but no route ran from those "
                             "words to them",
                 "rows": 0,
                 "source": "docs/method/canon/THE_ARCHETYPE_LAYER.md §3"},
        "expect": ["R-ARCHETYPE", "R-SPLIT"],
        "why_it_matters": "the clearest before/after in the whole corpus.",
    },
    {
        "id": "EX-STEAL",
        "name": "A MAN IS STEALING THE MONEY",
        "his_words": "thief / opportunity / habit / saving a life",
        "text": "a man is stealing money from a shop",
        "instrument": "seating",
        "then": {"recorded": "seated ZERO rows", "rows": 0,
                 "source": "docs/method/canon/THE_ARCHETYPE_LAYER.md §3"},
        "expect": ["R-ARCHETYPE", "R-READINGS"],
        "why_it_matters": "his motto's own demonstration — one act, four "
                          "reasons, the hand identical in all four.",
    },
    {
        "id": "EX-DIAMOND",
        "name": "DIAMOND CUT DIAMOND",
        "his_words": "its ego cut ego",
        "text": "diamond cut diamond",
        "instrument": "seating",
        "then": {"recorded": "seated ZERO rows", "rows": 0,
                 "source": "docs/method/canon/THE_ARCHETYPE_LAYER.md §3"},
        "expect": ["R-ARCHETYPE", "R-LINK"],
        "why_it_matters": "the reading belongs to the MEETING; before the link "
                          "layer there was nowhere to put it.",
    },
    {
        "id": "EX-GOOD",
        "name": "THE ONE LEFT WITH MEMORIES",
        "his_words": "in the burden of such things, such personalities cant or "
                     "unable or never think about themself and at end they "
                     "left with the memories only",
        "text": "he gave everything and got nothing in return",
        "instrument": "seating",
        "then": {"recorded": "1 row by words alone",
                 "rows": 1,
                 "source": "docs/method/canon/THE_ARCHETYPE_LAYER.md §3 table"},
        "expect": ["R-ARCHETYPE"],
        "why_it_matters": "carries his refusal — a person who receives nothing "
                          "is not thereby good.",
    },
    {
        "id": "EX-MALL",
        "name": "THE MALL EXAMPLE",
        "his_words": "few days back … weekend … i'm not well",
        "text": ("I dont want to go to mall, i'm not well. i dont want to go "
                 "to mall, i'm not interested to walk. I dont like crowd. I "
                 "had visited few days back. i will b going on weekend. i will "
                 "be going with my Girlfriend."),
        "instrument": "bank_matcher",
        "then": {"recorded": "72 exact P rows · 34 / 24 / 14 · 21 of 80 "
                             "containers · 8 of 10 segments",
                 "rows": 72,
                 "source": "CLAUDE.md — HIS MALL EXAMPLE, RUN"},
        "expect": ["R-BODY", "R-SPLIT"],
        "why_it_matters": "the example that forced a THIRD time scope and the "
                          "six intent routes on one shell.",
    },
    {
        "id": "EX-SAMRATH",
        "name": "THE SAMRATH SENTENCE",
        "his_words": "he never like to go to school but today he went happy, "
                     "it's his birthday",
        "text": ("Samrath never like to go to school, he always cry, but "
                 "today is his birthday, he went very happy."),
        "instrument": "bank_matcher",
        "then": {"recorded": "18 of 3,204 · 106 exact P rows · 16 containers · "
                             "59 / 27 / 20",
                 "rows": 106,
                 "source": "CLAUDE.md — HIS SECOND RUN, and a test pins it"},
        "expect": ["R-SPLIT"],
        "why_it_matters": "a test pins this result, so a movement here is a "
                          "regression unless a ruling explains it.",
    },
    {
        "id": "EX-STUDY",
        "name": "THE STUDY / FOCUS SEQUENCE",
        "his_words": "answer your all distractions first / write down all, "
                     "answer all",
        "text": "i study late at night but i keep thinking about tomorrow",
        "instrument": "seating",
        "then": {"recorded": None, "rows": None,
                 "source": "no reading was recorded for this example"},
        "expect": [],
        "why_it_matters": "held to show what NOT RECORDED looks like — an "
                          "absence is reported, never filled with a guess.",
    },
)


def rulings() -> tuple:
    return RULINGS


def examples() -> tuple:
    return EXAMPLES


#: THE TWO INSTRUMENTS, AND WHY THEY MUST NOT BE COMPARED WITH EACH OTHER.
#:
#: The first draft of this module compared every recorded number against the
#: SEATING, and reported the mall at 72 -> 0 and Samrath at 106 -> 0. Both
#: looked like catastrophic regressions and neither was: those two numbers were
#: never produced by the seating. They came from `asi_pyramid.rows_for()`, the
#: BANK MATCHER, which is a different mechanism answering a different question.
#: Comparing them was a measurement error of mine, not a movement of his.
#:
#:   seating       `growing.place` -> `sbx.place_on_spine` — which rows the
#:                 WORDS of a sentence reach, plus what the archetype layer
#:                 reaches by shape. This is the answer path.
#:   bank_matcher  `asi_pyramid.rows_for` — which of the 3,204 rows a sentence
#:                 activates by signal, with tiers. This is the row-level
#:                 matcher his Samrath run used.
#:
#: So every example records WHICH instrument produced its `then`, and the
#: re-read runs THAT ONE for `now`. Like against like, or the comparison is
#: worthless.
INSTRUMENTS = {
    "seating": "growing.place via sbx.place_on_spine — the answer path",
    "bank_matcher": "asi_pyramid.rows_for — the row-level matcher against the "
                    "3,204",
}


def _now(text: str, instrument: str = "seating") -> dict:
    """The reading the live system produces today.

    Every layer is reported either way, because he should see the whole
    picture; but `rows_total` — the number the verdict is computed from —
    comes from the SAME instrument that produced the recorded number."""
    from . import sbx
    r = sbx.place_on_spine(text)
    out = {
        "instrument": instrument,
        "instrument_is": INSTRUMENTS.get(instrument, instrument),
        "rows_by_words": r["source_rows_seated"],
        "rows_by_archetype": r["archetype_rows_reached"],
        "rows_by_seating": r["rows_reached_total"],
        "mapped_into_split": r["mapped_into_split"],
        "steps_lit": r["steps_lit_count"],
        "steps": [s["name"] for s in r["steps_lit"]],
        "archetypes": [a["id"] for a in r["archetypes_fired"]],
        "containers_lit": r["triggers"]["containers_lit"],
        "his_triggers": r["triggers"]["his_triggers_lit"],
        "readings": r["readings"]["count"],
        "meetings": r["meetings"]["count"],
        "layers_run": r["layers_run"],
        "row_names": [h["row"] for h in r["hits"]],
        "row_ids": [h["id"] for h in r["hits"]],
        "source_ids": [h["from"]["id"] for h in r["hits"]],
        "concluded": r["concluded"],
    }
    if instrument == "bank_matcher":
        from . import asi_pyramid as P
        m = P.rows_for(text)
        out["bank_matcher"] = {
            "rows": m["counts"]["rows"],
            "containers": m["counts"]["containers"],
            "segments": m["counts"]["segments"],
            "source_grounded": m["counts"].get("source_grounded"),
            "inferred": m["counts"].get("inferred"),
            "held_open": m["counts"].get("held_open"),
        }
        out["rows_total"] = m["counts"]["rows"]
    else:
        out["rows_total"] = r["rows_reached_total"]
    return out


def read_one(eid: str) -> dict:
    """One example: what was recorded THEN, what the system says NOW, and which
    of his rulings accounts for the difference."""
    ex = next((e for e in EXAMPLES if e["id"] == eid), None)
    if ex is None:
        return {"found": False, "id": eid}
    now = _now(ex["text"], ex.get("instrument", "seating"))
    then_rows = ex["then"]["rows"]
    by_id = {r["id"]: r for r in RULINGS}
    causes = [dict(by_id[r]) for r in ex["expect"] if r in by_id]

    then_names = [n.strip().lower() for n in ex["then"].get("row_names", [])]
    now_names = [n.strip().lower() for n in now.get("row_names", [])]
    same_rows = None
    if then_names:
        same_rows = sorted(then_names) == sorted(now_names)

    if then_rows is None:
        verdict = "NOT RECORDED"
        moved = None
        note = ("no reading was recorded for this example, so there is nothing "
                "to compare. Reported as an absence, never filled in.")
    elif now["rows_total"] == then_rows and same_rows is False:
        # THE DANGEROUS CASE, and the reason this module compares identity at
        # all. His rain sentence reads 2 rows now and read 2 rows then, so a
        # count-only check called it UNCHANGED — while BOTH ROWS HAD CHANGED.
        # A count is not a meaning.
        verdict = "CHANGED — SAME COUNT, DIFFERENT ROWS"
        moved = 0
        note = ("the count did not move and the MEANING did. A count-only "
                "comparison reports this as unchanged, which is how a changed "
                "reading hides.")
    elif now["rows_total"] == then_rows:
        verdict = "UNCHANGED"
        moved = 0
        note = ("the reading stands exactly as it was recorded."
                if same_rows is not False else "")
    else:
        moved = now["rows_total"] - then_rows
        verdict = "CHANGED — EXPLAINED" if causes else "CHANGED — UNEXPLAINED"
        note = ("every movement must have a named ruling behind it. "
                if causes else
                "NO RULING OF HIS ACCOUNTS FOR THIS MOVEMENT — that is drift, "
                "and it is the finding.")
    return {
        "id": ex["id"], "name": ex["name"],
        "his_words": ex["his_words"], "text": ex["text"],
        "then": ex["then"],
        "now": now,
        "verdict": verdict,
        "rows_moved": moved,
        "same_rows": same_rows,
        "then_rows_named": ex["then"].get("row_names"),
        "now_rows_named": now.get("row_names"),
        "known_defect_then": ex["then"].get("known_defect"),
        "explained_by": causes,
        "why_it_matters": ex["why_it_matters"],
        "note": note,
        "changed_here": None,
    }


def report() -> dict:
    """THE PER-FILE REPORT he asked for: what changed and what did not.

    Nothing is re-filed, nothing is corrected, and the new reading is not
    declared the right one. Two readings of one example is exactly the case his
    own law covers — both stand, the gap goes to him."""
    rows = [read_one(e["id"]) for e in EXAMPLES]
    by_v = {}
    for r in rows:
        by_v.setdefault(r["verdict"], []).append(r["id"])
    return {
        "his_ask": "every file, every example and every teaching re-read under "
                   "the new rulings",
        "examples": rows,
        "examined": len(rows),
        "by_verdict": {k: sorted(v) for k, v in sorted(by_v.items())},
        "changed": sum(1 for r in rows if r["verdict"].startswith("CHANGED")),
        "unchanged": sum(1 for r in rows if r["verdict"] == "UNCHANGED"),
        "not_recorded": sum(1 for r in rows if r["verdict"] == "NOT RECORDED"),
        "unexplained": [r["id"] for r in rows
                        if r["verdict"] == "CHANGED — UNEXPLAINED"],
        "rulings_applied": len(RULINGS),
        "law": "a reading recorded in the canon is a reading AT A DATE. Left "
               "alone it becomes a claim about today that nobody checked. This "
               "re-reads it and REPORTS — it re-files nothing, corrects no "
               "canon, and does not decide the new reading is the right one.",
        "never": "an example with no recorded reading says NOT RECORDED. An "
                 "absence is never filled with a guess.",
        "his_call": True,
    }


def stats() -> dict:
    r = report()
    return {
        "examples": r["examined"],
        "rulings": len(RULINGS),
        "changed": r["changed"],
        "unchanged": r["unchanged"],
        "not_recorded": r["not_recorded"],
        "unexplained": len(r["unexplained"]),
        "law": "a movement with no ruling behind it is drift, and drift is the "
               "finding.",
    }


def annotations() -> list:
    return [
        ("every example re-read under the new rulings", "reread.report"),
        ("change of meaning n outcomes from the old example n quotes",
         "reread.read_one"),
        ("the rain example was proved on the old body/brain ruling",
         "reread.EXAMPLES"),
        ("a per-file report of what changed and what did not", "reread.report"),
    ]
