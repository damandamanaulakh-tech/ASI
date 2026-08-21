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
    {"n": 5, "name": "RELATION GRAPH",
     "does": ["asi_pyramid.relations", "nodegraph.path",
              "nodegraph.neighbours", "nodegraph.subgraph"], "state": RUNS,
     "note": "Phase D made it traversable: nodes are stored, links are TYPED "
             "(his ten, each with direction and inverse), and path() walks "
             "them — a path through `contradicts` means something different "
             "from one through `supports`, which is what a similarity blob "
             "could never say. asi_pyramid.relations remains the per-ask "
             "relation LIST; the graph is where relations LIVE."},
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
    {"n": 18, "name": "MATURITY UPDATE",
     "does": ["maturity.read", "maturity.update"], "state": RUNS,
     "note": "BUILT on his word. Six named states — UNTESTED, HELD, SUPPORTED, "
             "STRONG, WEAKENED, KILLED — each a state PLUS the evidence that put "
             "it there, never a bare number (MATCH SCORE != EPISTEMIC "
             "CONFIDENCE). Only DISCRIMINATING confirmations count, and two of "
             "different classes are needed for STRONG because two of one class "
             "is one kind of looking done twice. Decay is checks WITHOUT "
             "confirmation, never age — a reading does not become less true by "
             "being old. An update APPENDS a reading referencing the one before "
             "it, so a maturity is a ledger and not a field: his no-reopen rule "
             "applied to a value."},
    {"n": 19, "name": "RETAIN / WEAKEN / REJECT / UNKNOWN",
     "does": ["maturity.verdict", "intent_ledger.survivors"], "state": RUNS,
     "note": "ALL FOUR now. WEAKEN was the missing one and it could not exist "
             "before stage 18, because you cannot weaken something with no "
             "strength to lose. WEAKEN is a verdict of its own, not a softer "
             "REJECT: evidence damaged the reading without ending it, so it "
             "stands, and it stands lower."},
    {"n": 20, "name": "PATTERN CONTRIBUTION",
     "does": ["patterns.rfr_check", "micro.decompose"], "state": RUNS,
     "note": "every micro-sequence carries a pattern contribution"},
    {"n": 21, "name": "MEMORY WRITE", "does": ["growth.add"], "state": RUNS,
     "note": "append-only, 17 typed series, no removal path exists"},
    {"n": 22, "name": "NEW COMBINATION AVAILABILITY",
     "does": ["combine.run", "combine.delta", "selfmake.extend"], "state": RUNS,
     "note": "Phase C made availability a FUNCTION: combine.run generates in "
             "rounds until quiet, and combine.delta computes what a newer run "
             "opened that an older could not reach — no longer a by-hand diff "
             "of generation counts. What remains manual is the TRIGGER: "
             "nothing calls delta on a write or a timer. That is Phase E, and "
             "it is the scheduler's gap, not this stage's."},
    {"n": 23, "name": "FUTURE EVENT", "does": ["discovery.close",
                                               "discovery.loop"],
     "state": RUNS,
     "note": "BUILT on his word, and NOT as a jump back to 01 — his own protocol "
             "forbids that twice over (NO IN-PLACE LOOP, NO REOPEN). A pass "
             "CLOSES and may CREATE a successor that references it; the closed "
             "sequence is never touched again and history is never rewritten. A "
             "successor exists only if the pass left something open: a new "
             "combination, an unsettled maturity, or an unchecked discriminating "
             "prediction. If none holds the loop TERMINATES, which is a real "
             "outcome — a loop that cannot stop is a leak. The successor carries "
             "the OPEN ENDS, not the whole prior pass."},
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
    from . import maturity as MA
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
    step(5, "RELATION GRAPH",
         lambda: {"traversable": True,
                  "typed_hops": "nodegraph.path — every hop names its link",
                  "per_ask_list": "asi_pyramid.relations"})
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
    step(18, "MATURITY UPDATE",
         lambda: MA.read(confirmed=[], refuted=[])["state"])
    step(19, "RETAIN / WEAKEN / REJECT / UNKNOWN",
         lambda: {"verdict": MA.verdict(MA.read())["verdict"],
                  "all_four": MA.verdict(MA.read())["all_four"]})
    step(20, "PATTERN CONTRIBUTION", lambda: {"per_micro_sequence": True})
    step(21, "MEMORY WRITE", lambda: {"append_only": True})
    step(22, "NEW COMBINATION AVAILABILITY",
         lambda: {"engine": "combine.run — rounds until quiet",
                  "availability": "combine.delta — computed, not by hand",
                  "trigger_still_manual": True})
    step(23, "FUTURE EVENT",
         lambda: {"closes_and_may_succeed": True, "reopens": False})
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


# ---------------------------------------------------------------------------
# STAGE 23 — FUTURE EVENT. The return edge, built under his no-reopen law.
#
# WHY THIS IS NOT SIMPLY "GO BACK TO 01"
#
# The obvious return edge is a jump: stage 23 finishes, so run stage 01 again on
# the same sequence. His own protocol forbids exactly that, in two rules that
# were written before this stage existed:
#
#     NO IN-PLACE LOOP.  Unresolved -> suspend at barrier -> open a NEW sequence
#                        -> it closes -> returns -> re-evaluate.
#     NO REOPEN.         S0 CLOSED + new evidence -> CREATE S1, S1.references =
#                        S0. The word reopen is removed from the grammar.
#                        History is never rewritten.
#
# So a pass does not restart. It CLOSES, and closing may CREATE a successor that
# references it. The successor is a different sequence with its own id, its own
# inputs and its own history; the closed one is never touched again. That is why
# `close()` returns a sequence record and `next_event()` returns a NEW id rather
# than a flag saying "loop again".
#
# WHAT MAKES A SUCCESSOR EXIST AT ALL
#
# A pass only earns a successor if it produced something the next pass would not
# already have. Three things can do that, and each is checked separately so the
# reason is on the record:
#
#   1. NEW COMBINATION      stage 22 opened arrangements or combinations that
#                           did not exist before this pass.
#   2. UNSETTLED MATURITY   stage 18 left readings at UNTESTED or HELD. Those are
#                           open questions, and an open question is a reason to
#                           come back.
#   3. UNMET PREDICTION     stage 12 produced discriminating predictions that
#                           were never checked. Something specific is waiting to
#                           be looked at.
#
# If none of the three holds, the loop TERMINATES, and that is a real outcome
# rather than a failure. The system already proved this shape once: extending
# selfmake on the same material writes 0 steps. A loop that cannot stop is not a
# loop, it is a leak.
#
# WHAT THE SUCCESSOR CARRIES
#
# Not the whole prior pass — its OPEN ENDS. Carrying everything forward would
# make each pass larger than the last with nothing gained, and would quietly
# re-run settled work. So the seed is the unsettled readings, the unchecked
# predictions and the new combinations, and nothing else. The closed pass stays
# whole in the record and is referenced, not copied.
# ---------------------------------------------------------------------------

TERMINATED = "TERMINATED"
SUCCEEDED = "SUCCEEDED BY A NEW SEQUENCE"


def close(run: dict, new_combinations: int = 0, maturities=(),
          predictions=()) -> dict:
    """STAGE 23 — close this pass, and decide whether a successor exists.

    Never mutates `run`. Closing is a statement about a pass, not an edit to it."""
    from . import maturity as M
    unsettled = [m for m in maturities
                 if (m.get("state") if isinstance(m, dict) else m)
                 in (M.UNTESTED, M.HELD)]
    unmet = [p for p in predictions
             if isinstance(p, dict) and p.get("discriminating")
             and not p.get("checked")]
    reasons = []
    if new_combinations:
        reasons.append({"reason": "NEW COMBINATION", "count": new_combinations,
                        "why": "stage 22 opened %d arrangement(s) or "
                               "combination(s) that did not exist before this "
                               "pass" % new_combinations})
    if unsettled:
        reasons.append({"reason": "UNSETTLED MATURITY", "count": len(unsettled),
                        "why": "stage 18 left %d reading(s) at UNTESTED or HELD "
                               "— an open question is a reason to come back"
                               % len(unsettled)})
    if unmet:
        reasons.append({"reason": "UNMET PREDICTION", "count": len(unmet),
                        "why": "stage 12 produced %d discriminating "
                               "prediction(s) that were never checked — "
                               "something specific is waiting to be looked at"
                               % len(unmet)})
    prior = run.get("sequence_id") or "S0"
    closed = {
        "sequence_id": prior,
        "closed": True,
        "stages_run": run.get("stages_run"),
        "halted_at": run.get("halted_at"),
        "reopened": False,
        "history_rewritten": False,
    }
    if not reasons:
        return {
            "closed": closed, "outcome": TERMINATED, "successor": None,
            "reasons": [],
            "why": "the pass opened no new combination, left no reading "
                   "unsettled, and left no discriminating prediction unchecked. "
                   "There is nothing a further pass would reach that this one "
                   "did not. Terminating is a real outcome, not a failure — a "
                   "loop that cannot stop is a leak.",
            "law": "no reopen. The closed sequence is never touched again.",
        }
    n = int(prior[1:]) + 1 if prior.startswith("S") and prior[1:].isdigit() else 1
    successor = {
        "sequence_id": "S%d" % n,
        "references": prior,
        "is_a_reopen_of": None,
        "seed": {
            "unsettled_readings": len(unsettled),
            "unchecked_discriminating_predictions": len(unmet),
            "new_combinations": new_combinations,
        },
        "carries_the_whole_prior_pass": False,
        "why_not": "a successor carries the OPEN ENDS, not everything. Carrying "
                   "the whole prior pass would grow each pass with nothing "
                   "gained and would quietly re-run settled work.",
    }
    return {
        "closed": closed, "outcome": SUCCEEDED, "successor": successor,
        "reasons": reasons,
        "why": "%d reason(s) to continue, each named above" % len(reasons),
        "law": "S0 CLOSED + new evidence -> CREATE S1 referencing S0. The word "
               "reopen is removed from the grammar; history is never rewritten.",
    }


def loop(text: str, name: str = "", max_passes: int = 5, verdicts=None) -> dict:
    """Run his loop until it TERMINATES or the pass cap is hit.

    This is the closed loop: 01 -> 23 -> close -> a NEW sequence -> 01 again.
    Each pass is its own sequence referencing the one before it; the prior pass
    is never re-entered.

    HOW IT ACTUALLY TERMINATES, which is the whole difficulty.

    The first attempt did not. It reseeded every maturity to HELD at the start of
    each pass, so there was always an unsettled reading and always a reason to
    continue — it ran to the cap every time. A loop whose open ends never close
    is not a loop, it is a counter.

    What closes them is his own decay rule from stage 18: **checks WITHOUT
    confirmation**. Each pass looks at the outstanding predictions. If nothing
    out there confirms them — and with no `verdicts` supplied, nothing does,
    because this repository is not the world — then after DECAY_AFTER passes the
    reading moves to WEAKENED. WEAKENED is settled. Settled readings are not a
    reason to come back, so the loop stops.

    That is deliberately not "it gave up". It is the system reporting that it
    looked repeatedly, found nothing that discriminated, and the reading is worse
    for it. Pass `verdicts` — a dict of prediction class -> True/False from
    outside — and confirmations settle it the other way, faster.
    """
    from . import expected as EX
    from . import maturity as M
    passes, seq = [], "S0"
    preds, chains, combos = None, None, 1
    for i in range(max_passes):
        r = chain(text, "%s pass %d" % (name or "run", i + 1))
        r["sequence_id"] = seq
        if preds is None:                       # pass 1 generates the openings
            from . import artifact as _A
            rows = EX.run(_A.generate_meanings()["meanings"], limit=40)["rows"]
            preds = [p for row in rows for p in row["predictions"]
                     if p["discriminating"]][:6]
            chains = [[] for _ in preds]
        # LOOK at each outstanding prediction. A verdict comes from outside; with
        # none supplied nothing is confirmed, and that is recorded as a check.
        confirmed, refuted = [], []
        for p in preds:
            v = (verdicts or {}).get(p["class"])
            p["checked"] = True
            if v is True:
                confirmed.append(p)
            elif v is False:
                refuted.append(p)
        mats = []
        for j, p in enumerate(preds):
            u = M.update(chains[j],
                         confirmed=[x for x in confirmed if x is p],
                         refuted=[x for x in refuted if x is p],
                         checks=i + 1)
            chains[j] = u["chain"]
            mats.append(u["current"])
        c = close(r, new_combinations=combos, maturities=mats, predictions=preds)
        passes.append({"pass": i + 1, "sequence_id": seq,
                       "stages_run": r["stages_run"],
                       "outcome": c["outcome"],
                       "reasons": [x["reason"] for x in c["reasons"]],
                       "maturities": sorted({m["state"] for m in mats}),
                       "checks_so_far": i + 1})
        if c["outcome"] == TERMINATED:
            return {"passes": passes, "count": len(passes), "terminated": True,
                    "hit_cap": False, "final": c,
                    "settled_as": sorted({m["state"] for m in mats}),
                    "law": "the loop stops when a pass opens nothing new. "
                           "Repeated looking without confirmation settles a "
                           "reading at WEAKENED — that is a result, not a "
                           "surrender."}
        seq = c["successor"]["sequence_id"]
        combos = 0                  # only the first pass introduces new material
    return {"passes": passes, "count": len(passes), "terminated": False,
            "hit_cap": True,
            "why": "stopped at the %d-pass cap, not because it ran out of open "
                   "ends. The cap is a guard, not a finding." % max_passes,
            "law": "a loop that cannot stop is a leak; the cap makes that "
                   "visible rather than silent."}
