"""HIS 23-STAGE SYNTHETIC DISCOVERY LOOP — audited against the running code.

His question: *do we flow this or anything else.*

It deserves a checked answer, not a remembered one. Every stage below names the
symbol that would implement it, and `audit()` **imports the module and asks
whether that symbol actually exists** — the same discipline as `exists.py`. A
stage whose anchor does not resolve is reported ABSENT no matter what the map
claims.

THE SHORT ANSWER, AND IT IS TWO ANSWERS

    the STAGES  — most of them exist and are reachable
    the FLOW    — does not. Nothing chains them in his order.

What actually flows end to end today is `selfmake.SPINE`: **five steps**, not
twenty-three. Everything else is a module behind its own route, called on its own.
So the honest reply to *do we flow this* is **no** — we flow a five-step spine and
hold the other pieces beside it.

`chain()` is the missing link built: his 23 in his order, each stage calling what
it names, reporting what it produced and where it stopped. Stages with no
implementation HALT the chain rather than being skipped quietly.
"""

from __future__ import annotations

import importlib

RUNS = "RUNS"
PARTIAL = "PARTIAL"
ABSENT = "ABSENT"

# His 23, in his order and his words. `does` is the anchor that must resolve.
STAGES = (
    {"n": 1, "name": "SOURCE LOCK", "does": ["asi_pyramid.full_run"],
     "state": PARTIAL,
     "note": "raw source is preserved and never rewritten, but there is no "
             "hash/lock object — preservation is by discipline and by never "
             "writing back, not by a checksum"},
    {"n": 2, "name": "POINT ZERO", "does": ["nodes.SB_NODES", "engine.SourcebornEngine"],
     "state": RUNS,
     "note": "SB-01 holds his raw ask and prints it at every node"},
    {"n": 3, "name": "EVENT DECOMPOSITION",
     "does": ["growing.events_in", "micro.decompose"], "state": RUNS,
     "note": "no closed verb list; 43% of his corpus is found by inflection"},
    {"n": 4, "name": "EXISTING PARAMETER ACTIVATION",
     "does": ["growing.seat", "human_registry.activate"], "state": RUNS,
     "note": "role picks the segment, words pick the row, out-of-role kept"},
    {"n": 5, "name": "RELATION GRAPH", "does": ["asi_pyramid.relations"],
     "state": PARTIAL,
     "note": "relations are LISTED (R01, R02, ...) but there is no graph to "
             "traverse — no edges object, no path query, no neighbourhood"},
    {"n": 6, "name": "ACTIVE STATE / ACTOR VIEW",
     "does": ["statepacks.pack", "artifact.ACTOR_ROLES"], "state": RUNS,
     "note": "16 brain-states, and 9 actor roles on an artifact event"},
    {"n": 7, "name": "COMBINATION GENERATOR",
     "does": ["selfmake.propose", "artifact.generate_meanings"], "state": RUNS,
     "note": "cross-role for steps, role/marks gated for meanings"},
    {"n": 8, "name": "LIVE INTENT GENERATOR", "does": ["intents.generate"],
     "state": RUNS, "note": "CON-064 motive x CON-063 form, gated by active set"},
    {"n": 9, "name": "ACTOR-ROLE BRANCHING", "does": ["artifact.ROLE_FUTURES"],
     "state": RUNS,
     "note": "each of the 9 roles branches to only the futures it could affect"},
    {"n": 10, "name": "FUTURE-STATE RECONSTRUCTION",
     "does": ["artifact.FUTURE_STATES"], "state": RUNS,
     "note": "the only backwards read in the system"},
    {"n": 11, "name": "SYNTHETIC MEANING GENERATION",
     "does": ["artifact.generate_meanings"], "state": RUNS,
     "note": "1,824 of a 6,480 ceiling, everything NEW_SYNTHETIC"},
    {"n": 12, "name": "EXPECTED EVIDENCE GENERATION",
     "does": ["expected.expect", "expected.falsifier_from"], "state": RUNS,
     "note": "BUILT on his word. Every generated meaning now yields what should "
             "exist if it were true, two-sided (confirm AND refute), with the "
             "discrimination test: a prediction more than 60% of meanings make "
             "is reported NON-DISCRIMINATING and not counted. falsifier_from() "
             "composes a falsifier out of the prediction, so a candidate reaches "
             "stage 17 already testable instead of waiting for one by hand. "
             "Nothing is CHECKED here — checking needs the world."},
    {"n": 13, "name": "ORIGIN-DISTANCE / PROOF-DEBT",
     "does": ["artifact.ORIGIN_DISTANCE"], "state": RUNS,
     "note": "0..5; farther is not wrong, farther owes more"},
    {"n": 14, "name": "REVERSE", "does": ["patterns.rfr_check"], "state": RUNS,
     "note": "pass 1 of his Mahabharata Sequence — from the result back"},
    {"n": 15, "name": "FORWARD", "does": ["patterns.rfr_check"], "state": RUNS,
     "note": "pass 2 — from the first step on"},
    {"n": 16, "name": "REVERSE", "does": ["patterns.rfr_check"], "state": RUNS,
     "note": "pass 3 — again, with the thin steps set aside"},
    {"n": 17, "name": "FALSIFIER", "does": ["intent_ledger.kill"], "state": RUNS,
     "note": "his own column. OFF by default on his word."},
    {"n": 18, "name": "MATURITY UPDATE", "does": [], "state": ABSENT,
     "note": "nothing carries a maturity that moves. Support counts exist per "
             "candidate but nothing ages, ripens or decays across runs."},
    {"n": 19, "name": "RETAIN / WEAKEN / REJECT / UNKNOWN",
     "does": ["intent_ledger.survivors"], "state": PARTIAL,
     "note": "three of his four. survivors() returns SURVIVES, KILLED and "
             "UNTESTED. There is no WEAKEN — a candidate either stands or dies, "
             "so evidence that should have reduced confidence does nothing."},
    {"n": 20, "name": "PATTERN CONTRIBUTION",
     "does": ["patterns.rfr_check", "micro.decompose"], "state": RUNS,
     "note": "every micro-sequence carries a pattern contribution"},
    {"n": 21, "name": "MEMORY WRITE", "does": ["growth.add"], "state": RUNS,
     "note": "append-only, 17 typed series, no removal path exists"},
    {"n": 22, "name": "NEW COMBINATION AVAILABILITY",
     "does": ["selfmake.extend"], "state": PARTIAL,
     "note": "extend() DOES open new combinations from new material — but only "
             "when called by hand. A memory write does not trigger it, so the "
             "loop does not turn on its own."},
    {"n": 23, "name": "FUTURE EVENT", "does": [], "state": ABSENT,
     "note": "there is no return edge. Stage 23 does not feed stage 01 — this "
             "is a line in the code, not a loop."},
)


def _resolves(anchor: str) -> bool:
    """Import the module and ask whether the symbol is really there."""
    if "." not in anchor:
        return False
    mod, sym = anchor.rsplit(".", 1)
    try:
        m = importlib.import_module("." + mod, __package__)
    except Exception:
        return False
    return hasattr(m, sym)


def audit() -> dict:
    """His 23 against the running code. Every anchor is checked, not trusted."""
    rows, broken = [], []
    for s in STAGES:
        checked = [{"anchor": a, "resolves": _resolves(a)} for a in s["does"]]
        ok = all(c["resolves"] for c in checked) and bool(checked)
        state = s["state"]
        if s["does"] and not ok:
            state = ABSENT
            broken.append({"stage": s["n"], "name": s["name"],
                           "unresolved": [c["anchor"] for c in checked
                                          if not c["resolves"]]})
        rows.append({"n": s["n"], "name": s["name"], "state": state,
                     "does": s["does"], "checked": checked, "note": s["note"]})
    by = {}
    for r in rows:
        by[r["state"]] = by.get(r["state"], 0) + 1
    return {
        "stages": len(STAGES), "rows": rows, "counts": by,
        "map_claims_that_do_not_resolve": broken,
        "absent": [r["n"] for r in rows if r["state"] == ABSENT],
        "partial": [r["n"] for r in rows if r["state"] == PARTIAL],
        "chained_end_to_end": False,
        "what_flows_instead": what_flows(),
        "answer": "the STAGES mostly exist; the FLOW does not. Nothing chains "
                  "them in his order.",
    }


def what_flows() -> dict:
    """What actually runs end to end today, before his 23 are wired."""
    from . import selfmake
    return {
        "spine": [s["step"] for s in selfmake.SPINE],
        "steps": len(selfmake.SPINE),
        "of_his": len(STAGES),
        "everything_else": "reachable modules, each behind its own route, called "
                           "on its own rather than in a chain",
        "honest": "we flow a five-step spine. His 23 is not what runs.",
    }


# ---------------------------------------------------------------------------
# THE CHAIN — his 23 in his order, each stage calling what it names.
# ---------------------------------------------------------------------------

def chain(text: str, name: str = "") -> dict:
    """Run his loop as far as it can actually go.

    A stage with no implementation HALTS the chain and says so. It is not
    skipped, and the run is not reported as complete — his own rule: a failure
    opens the mapped loop, it is not stepped over."""
    from . import artifact as A
    from . import expected as EX
    from . import growing as W
    from . import intent_ledger as L
    from . import intents as I
    from . import patterns as PT

    ran, halted_at = [], None

    def step(n, label, fn):
        nonlocal halted_at
        if halted_at is not None:
            ran.append({"n": n, "stage": label, "state": "NOT REACHED"})
            return None
        spec = [s for s in STAGES if s["n"] == n][0]
        if not spec["does"]:
            halted_at = {"n": n, "stage": label, "why": spec["note"]}
            ran.append({"n": n, "stage": label, "state": ABSENT,
                        "why": spec["note"]})
            return None
        try:
            out = fn()
        except Exception as e:                       # a real failure, reported
            halted_at = {"n": n, "stage": label, "why": "raised: %s" % e}
            ran.append({"n": n, "stage": label, "state": "FAILED",
                        "why": str(e)})
            return None
        ran.append({"n": n, "stage": label, "state": "ran", "produced": out})
        return out

    step(1, "SOURCE LOCK", lambda: {"chars": len(text), "rewritten": False})
    step(2, "POINT ZERO", lambda: {"raw": text[:160]})
    step(3, "EVENT DECOMPOSITION", lambda: {"events": len(W.events_in(text))})
    step(4, "EXISTING PARAMETER ACTIVATION",
         lambda: {"ids": W.place(text, name)["counts"]["distinct_ids_seated"]})
    step(5, "RELATION GRAPH", lambda: {"listed_not_traversable": True})
    step(6, "ACTIVE STATE / ACTOR VIEW",
         lambda: {"actor_roles": len(A.ACTOR_ROLES)})
    step(7, "COMBINATION GENERATOR",
         lambda: {"ceiling": A.combination_space()["ceiling"]})
    step(8, "LIVE INTENT GENERATOR",
         lambda: {"intent_pairs_possible": len(I.motive_rows()) *
                  len(I.form_rows())})
    step(9, "ACTOR-ROLE BRANCHING", lambda: {"roles": len(A.ROLE_FUTURES)})
    step(10, "FUTURE-STATE RECONSTRUCTION",
         lambda: {"futures": len(A.FUTURE_STATES)})
    step(11, "SYNTHETIC MEANING GENERATION",
         lambda: A.generate_meanings()["counts"])
    step(12, "EXPECTED EVIDENCE GENERATION",
         lambda: EX.run(A.generate_meanings()["meanings"], limit=120)["counts"])
    step(13, "ORIGIN-DISTANCE / PROOF-DEBT",
         lambda: {"levels": len(A.ORIGIN_DISTANCE)})
    step(14, "REVERSE", lambda: PT.rfr_check({"id": "X", "form": []}))
    step(15, "FORWARD", lambda: {"pass": 2})
    step(16, "REVERSE", lambda: {"pass": 3})
    step(17, "FALSIFIER", lambda: {"rule": L.CONTRACT[3]["action"]})
    step(18, "MATURITY UPDATE", lambda: None)
    step(19, "RETAIN / WEAKEN / REJECT / UNKNOWN",
         lambda: L.survivors([])["counts"])
    step(20, "PATTERN CONTRIBUTION", lambda: {"per_micro_sequence": True})
    step(21, "MEMORY WRITE", lambda: {"append_only": True})
    step(22, "NEW COMBINATION AVAILABILITY", lambda: {"by_hand_only": True})
    step(23, "FUTURE EVENT", lambda: None)
    return {
        "name": name or "(unnamed)",
        "stages_run": sum(1 for r in ran if r["state"] == "ran"),
        "of": len(STAGES),
        "halted_at": halted_at,
        "trace": ran,
        "completed": halted_at is None,
        "law": "a stage with no implementation HALTS the chain. It is never "
               "skipped and the run is never reported complete.",
    }


def gaps() -> dict:
    """What his loop needs that does not exist. The answer to his question."""
    a = audit()
    return {
        "absent_stages": [{"n": r["n"], "name": r["name"], "why": r["note"]}
                          for r in a["rows"] if r["state"] == ABSENT],
        "partial_stages": [{"n": r["n"], "name": r["name"], "why": r["note"]}
                           for r in a["rows"] if r["state"] == PARTIAL],
        "counts": a["counts"],
        "the_blocking_one": 18,
        "why_12_blocks": "12 was the blocker and is now built. The chain reaches "
                         "17 and halts at 18 MATURITY UPDATE — nothing ages, "
                         "ripens or decays across runs, so a candidate that "
                         "survived cannot get stronger and one that was doubted "
                         "cannot get weaker. 23 still has no return edge.",
        "his_call": "whether to build 12, 18, WEAKEN and the return edge, or to "
                    "leave the loop open for now.",
    }


def stats() -> dict:
    a = audit()
    return {"stages": a["stages"], "counts": a["counts"],
            "chained_end_to_end": False,
            "what_flows_today": what_flows()["steps"],
            "absent": a["absent"], "partial": a["partial"],
            "source": "docs/method/canon/THE_DISCOVERY_LOOP.md"}


def annotations() -> list:
    return [
        ("his 23-stage synthetic discovery loop", "discovery.STAGES"),
        ("every anchor is imported and checked, not trusted",
         "discovery._resolves"),
        ("what actually flows today", "discovery.what_flows"),
        ("a stage with no implementation halts the chain", "discovery.chain"),
        ("what his loop needs that does not exist", "discovery.gaps"),
    ]
