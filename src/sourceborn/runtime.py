"""PHASE B — THE RUNTIME PIPELINE. HIS EIGHTEEN STEPS AS ONE RUN.

From his SELF-SUSTAINING EXECUTION FLOW sheet, box 2 (AUTO RUNTIME ENGINE):
eighteen steps, in his order, two of them reverse-direction and sitting BEFORE
decomposition. Sixteen already existed as separate modules reached by hand or by
their own pages; two (Declare End, Reverse to Prior Reality) did not exist and
are `prior.py`. This module is the WIRE: one call walks all eighteen in his
order, each step consuming what the earlier steps produced.

WHAT A RUN IS, AND WHAT IT IS NOT

A run is a RECORD — eighteen step records, each carrying the step's own job,
what it took, and what it produced (his SB-01 correction: a walk that shows a
description of work with the content nowhere is not a walk). A run is NOT an
answer. `answer` is None on every run, structurally: the runtime prepares, he
decides. That is the YOUR-GATE box on his own sheet — auto may seat, link,
combine, predict and mature; it may not promote, answer, or add a parameter.

HONESTY RULES THIS MODULE KEEPS

  * a step that cannot genuinely bite on this ask SAYS SO in its record rather
    than faking a result — R-F-R on a single unrepeated ask reports thin steps,
    maturity on an unchecked run reads UNTESTED, the verdict reads UNKNOWN.
    That is not a defect; an eighteen-step run on one sentence SHOULD end open.
  * step 17 (Memory Writeback) PREPARES the rows and evaluates his five write
    conditions, and does not write. Enforcing the conditions at the write site
    is his Phase D; writing here before the gate exists would be building E
    before D. `write=True` plus a root delegates to `growing.grow`, which is
    the one writer that already exists and is append-only.
  * nothing is chosen. Detected states, generated intents, end candidates —
    every set comes back whole with `chosen: None` where a choice would go.
"""

from __future__ import annotations

FORWARD = "FORWARD"
REVERSE = "REVERSE"

# ---------------------------------------------------------------------------
# HIS EIGHTEEN — the order is his and it is load-bearing: 2 and 3 run reverse
# BEFORE decomposition, which is the correction this phase exists for.
# ---------------------------------------------------------------------------

STEPS = (
    {"n": 1, "name": "Capture Event", "dir": FORWARD,
     "owner": "growing.events_in",
     "job": "everything happening is an event; a text with a happening can "
            "never come back with zero events"},
    {"n": 2, "name": "Declare End / Why This Matters", "dir": REVERSE,
     "owner": "prior.declare_end",
     "job": "name the end the event was working toward, from the source or "
            "from him — and say which later steps turn on it"},
    {"n": 3, "name": "Reverse to Prior Reality", "dir": REVERSE,
     "owner": "prior.prior_reality",
     "job": "descend from the thing as it stands to what must have been true "
            "before it, by the removal test, without assuming"},
    {"n": 4, "name": "Sequence Decomposition", "dir": FORWARD,
     "owner": "micro.decompose_all",
     "job": "every sentence its own micro-sequence in his field names, "
            "participants carried forward, nothing concluded"},
    {"n": 5, "name": "Parameter Activation", "dir": FORWARD,
     "owner": "growing.seat",
     "job": "the role picks the segments, the words pick the rows; a word "
            "coincidence outside the role is kept and never counted"},
    {"n": 6, "name": "Relation Graph Build", "dir": FORWARD,
     "owner": "asi_pyramid.relations",
     "job": "his runtime relations, numbered as he numbered them; never "
            "written to the bank"},
    {"n": 7, "name": "Actor-Role Split", "dir": FORWARD,
     "owner": "growing.events_in + artifact.ACTOR_ROLES",
     "job": "who acts in each event; and for artifact events, subject ≠ "
            "requester ≠ author ≠ scribe ≠ carver — nine roles, each with its "
            "own possible intent"},
    {"n": 8, "name": "Active State Detection", "dir": FORWARD,
     "owner": "statepacks.STATE_PACKS",
     "job": "which of his sixteen brain-states the ask itself gives evidence "
            "for. Detected is not chosen"},
    {"n": 9, "name": "Combination Generator", "dir": FORWARD,
     "owner": "selfmake (criterion) applied to this ask",
     "job": "arrangements present in THIS ask, and the cross-role pairs among "
            "them — the same gate that cut 2,627 to 2,119"},
    {"n": 10, "name": "Live Intent Generator", "dir": FORWARD,
     "owner": "intents.generate",
     "job": "intent candidates built at runtime from CON-063 × CON-064, gated "
            "by which containers this ask activated"},
    {"n": 11, "name": "Future-State Reconstruction", "dir": REVERSE,
     "owner": "prior.declare_end + asi_pyramid.read_scopes",
     "job": "the states this ask was working toward: the declared end plus "
            "every FUTURE / PLANNED clause — reconstruction runs backwards"},
    {"n": 12, "name": "Evidence Prediction", "dir": FORWARD,
     "owner": "expected (discipline) applied to this run",
     "job": "what should exist if a reading were true — including what would "
            "separate two ends, and what every reading owes: an ABSENCE"},
    {"n": 13, "name": "R -> F -> R", "dir": REVERSE,
     "owner": "patterns.rfr_check",
     "job": "reverse, forward, reverse over the run's own arrangement; marks "
            "what is thin so his approval is informed"},
    {"n": 14, "name": "Falsifier / Doubt", "dir": FORWARD,
     "owner": "intent_ledger.kill",
     "job": "what would flip the leading candidate — and an untested candidate "
            "is reported untested, never as a survivor"},
    {"n": 15, "name": "Maturity Update", "dir": FORWARD,
     "owner": "maturity.read",
     "job": "a maturity computed from what this run confirmed and refuted — "
            "never a bare number"},
    {"n": 16, "name": "Retain / Weaken / Reject / Open", "dir": FORWARD,
     "owner": "maturity.verdict",
     "job": "all four verdicts exist; the one this run earns is read off the "
            "maturity, not guessed"},
    {"n": 17, "name": "Memory Writeback", "dir": FORWARD,
     "owner": "growth.add via growing.grow — PREPARED, not written",
     "job": "compose the rows a write would append and evaluate his five "
            "write conditions. Enforcing them at the write site is Phase D"},
    {"n": 18, "name": "Next-Sequence Seed", "dir": FORWARD,
     "owner": "discovery.close",
     "job": "close this pass and say whether a successor exists, and why. "
            "NO REOPEN — a successor references this run, never rewrites it"},
)

STEP_NAMES = tuple(s["name"] for s in STEPS)


def _rec(spec: dict, took: str, produced, notes: str = "") -> dict:
    """One step record in his shape — job · took · produced — so the run shows
    the content at every step, not a description of work."""
    return {"n": spec["n"], "name": spec["name"], "direction": spec["dir"],
            "owner": spec["owner"], "job": spec["job"],
            "took": took, "produced": produced, "notes": notes}


# ---------------------------------------------------------------------------
# STEP 8 — detection against his sixteen packs. Evidence words from the pack's
# own condition strings; a pack with no word in the ask is not detected.
# ---------------------------------------------------------------------------

_STATE_STOP = {"state", "states", "body", "down", "up", "high", "low", "the",
               "and", "with", "under", "over", "his", "her", "their", "into",
               "from", "for", "was", "were", "are", "not", "all", "one",
               "two", "level", "levels", "mode"}


def detect_states(text: str) -> dict:
    import re
    from . import statepacks as S
    words = set(re.findall(r"[a-z][a-z'’]{2,}", (text or "").lower()))
    detected = []
    for p in S.STATE_PACKS:
        vocab = set()
        for c in p.get("conditions", ()):
            vocab |= {w for w in re.findall(r"[a-z][a-z'’]{3,}", str(c).lower())
                      if w not in _STATE_STOP}
        vocab |= {w for w in re.findall(r"[a-z]{4,}", p["name"].lower())}
        hit = sorted(words & vocab)
        if hit:
            detected.append({"pack": p["id"], "name": p["name"],
                             "evidence_words": hit,
                             "conditions": list(p.get("conditions", ()))[:3]})
    detected.sort(key=lambda d: (-len(d["evidence_words"]), d["pack"]))
    return {"packs_checked": len(S.STATE_PACKS), "detected": detected,
            "chosen": None,
            "law": "detected is evidence the ask itself gives. Nothing here "
                   "asserts which state the actor was in — his SP-22/SP-23 "
                   "pair reads the same sentence two ways and chooses neither."}


# ---------------------------------------------------------------------------
# STEP 9 — the selfmake criterion scoped to one ask: arrangements are the
# (role -> container) pairs THIS ask seated, a combination is two of them that
# CROSS ROLE. Same gate, no ledger, no writes.
# ---------------------------------------------------------------------------

def combinations_in(seatings: list) -> dict:
    arrs, by_key = [], {}
    for s in seatings:
        role = s.get("role")
        for seat in s.get("seats", []):
            key = (role, seat["container"])
            if key not in by_key:
                by_key[key] = {"role": role, "container": seat["container"],
                               "support_in_ask": 0}
                arrs.append(by_key[key])
            by_key[key]["support_in_ask"] += 1
    combos, rejected = [], 0
    for i in range(len(arrs)):
        for j in range(i + 1, len(arrs)):
            a, b = arrs[i], arrs[j]
            if a["role"] == b["role"]:
                rejected += 1          # the cross-role gate — the one that bites
                continue
            combos.append({"a": "%s->%s" % (a["role"], a["container"]),
                           "b": "%s->%s" % (b["role"], b["container"]),
                           "crosses_role": True})
    return {"arrangements": arrs, "combinations": combos,
            "rejected_same_role": rejected,
            "gate": "cross-role — the criterion that cut 2,627 to 2,119. "
                    "Without it this would be a step for nearly every pair, "
                    "which is not a finding."}


# ---------------------------------------------------------------------------
# THE RUN.
# ---------------------------------------------------------------------------

def run(text: str, his_end: str = "", root: str = "", write: bool = False,
        name: str = "") -> dict:
    """Walk his eighteen, in his order. Returns the record; never an answer."""
    from . import prior as P
    from . import growing as G
    from . import micro as MI
    from . import asi_pyramid as AP
    from . import artifact as AR
    from . import intents as IN
    from . import patterns as PT
    from . import intent_ledger as IL
    from . import maturity as M
    from . import discovery as D

    text = text or ""
    recs = []

    # 1 — CAPTURE EVENT
    events = G.events_in(text)
    recs.append(_rec(STEPS[0], "the raw ask, %d chars" % len(text),
                     {"events": [{"n": e["n"], "raw": e["raw"][:120],
                                  "actor": e["actor"],
                                  "happening": e["happening"]}
                                 for e in events],
                      "count": len(events)},
                     "" if events else "no happening found — the run continues "
                                       "and every later step says what that "
                                       "leaves it without"))

    # 2 — DECLARE END (reverse pass one)
    end = P.declare_end(text, his_end=his_end)
    recs.append(_rec(STEPS[1], "the ask" + (" + his named end" if his_end else ""),
                     {"named": end["named"], "end": end["end"],
                      "grade": end["grade"], "halt": end["halt"],
                      "candidates": end["candidates"],
                      "why_this_matters": end["why_this_matters"]["at_stake"]},
                     "HALT — two ends survive; his call" if end["halt"] else ""))

    # 3 — REVERSE TO PRIOR REALITY (reverse pass one, continued)
    pr = P.prior_reality(text, end)
    recs.append(_rec(STEPS[2],
                     "the top event: %s" % (pr.get("top_event", {}) or
                                            {}).get("raw", "(none)"),
                     {"survivors": [{"grade": s["grade"], "level": s["level"],
                                     "condition": s["condition"]}
                                    for s in pr.get("survivors", [])],
                      "dropped_as_neighbours": pr["counts"]["dropped_as_neighbours"]
                      if pr.get("counts") else 0,
                      "flagged_for_review": pr.get("flagged_for_review", []),
                      "reached_ground": pr.get("reached_ground", False),
                      "why_it_stopped": pr.get("why_it_stopped", "")},
                     "assumed rows: 0 — the descent cannot assume"))

    # 4 — SEQUENCE DECOMPOSITION
    seqs = MI.decompose_all(text)
    recs.append(_rec(STEPS[3], "%d sentence(s)" % len(seqs),
                     {"micro_sequences": len(seqs),
                      "signatures": [s.get("signature", "") for s in seqs],
                      "first": {k: seqs[0].get(k) for k in
                                ("raw", "relation", "negation",
                                 "temporal_relation")} if seqs else None},
                     "intent never concluded from one event; his feeling "
                     "never picked"))

    # 5 — PARAMETER ACTIVATION — the same three seatings growing.place runs:
    # per-event rows (role-gated), the intent slot on CON-063 + CON-064 (every
    # event has one — the motto made mechanical), and the whole ask at double
    # limit, because a clause too short to clear the IDF bar can still seat as
    # part of the whole.
    seatings, activated = [], {}
    for e in events:
        r = G.role_of(e["happening"], e["raw"])
        s = G.seat(e["raw"], limit=8, role=r["role"])
        s["role"] = r["role"]
        s["event_n"] = e["n"]
        seatings.append(s)
        for st in s["seats"]:
            activated.setdefault(st["container"], set()).add(st["sb_id"])
        isl = G.intent_seat(e["raw"])
        for st in isl["rows"]:
            activated.setdefault(st["container"], set()).add(st["sb_id"])
    whole = G.seat(text, limit=16) if text else {"seats": []}
    for st in whole["seats"]:
        activated.setdefault(st["container"], set()).add(st["sb_id"])
    act_containers = sorted(activated)
    recs.append(_rec(STEPS[4], "%d event(s), role-gated, + the intent slot on "
                               "%s, + the whole ask"
                               % (len(events), " + ".join(G.INTENT_CONTAINERS)),
                     {"containers_activated": act_containers,
                      "rows_seated": sorted({i for v in activated.values()
                                             for i in v}),
                      "out_of_role_kept": sum(s.get("out_of_role_total", 0)
                                              for s in seatings)},
                     "seating gives existing IDs support and creates no "
                     "parameter"))

    # 6 — RELATION GRAPH BUILD
    scopes = AP.read_scopes(text)
    rel = AP.relations(text, scopes=scopes)
    recs.append(_rec(STEPS[5], "the ask + its scopes",
                     {"relations": rel.get("relations", rel) if isinstance(rel, dict)
                      else rel},
                     "runtime relations — not parameters, never banked. "
                     "Traversal is Phase D"))

    # 7 — ACTOR-ROLE SPLIT
    actors = sorted({e["actor"] for e in events if not e["actor"].startswith("(")})
    recs.append(_rec(STEPS[6], "%d event(s)" % len(events),
                     {"actors": actors or ["(none named)"],
                      "per_event": [{"n": e["n"], "actor": e["actor"]}
                                    for e in events],
                      "artifact_roles_available":
                          [r["role"] for r in AR.ACTOR_ROLES]},
                     "for an artifact event the nine roles each carry their own "
                     "possible intent; a plain ask carries its named actors"))

    # 8 — ACTIVE STATE DETECTION
    det = detect_states(text)
    recs.append(_rec(STEPS[7], "the ask against his 16 packs",
                     det,
                     "" if det["detected"] else "no pack finds evidence in "
                                                "this ask — reported, not "
                                                "filled in"))

    # 9 — COMBINATION GENERATOR (bounded to this ask)
    combos = combinations_in(seatings)
    recs.append(_rec(STEPS[8], "%d seating(s)" % len(seatings), combos, ""))

    # 10 — LIVE INTENT GENERATOR
    top_h = events[-1]["happening"].upper().replace(" ", "_") if events else ""
    gen = (IN.generate(top_h, act_containers) if act_containers
           else {"candidates": [], "why": "no containers activated"})
    cands = gen.get("candidates", [])
    recs.append(_rec(STEPS[9],
                     "event %r × %d active container(s)"
                     % (top_h or "(none)", len(act_containers)),
                     {"candidates": len(cands),
                      "first_six": ["%s — %s (%s) shaped as %s (%s)"
                                    % (c["id"], c.get("why", ""),
                                       c.get("why_p", ""),
                                       c.get("shape", ""), c.get("shape_p", ""))
                                    for c in cands[:6]],
                      "chosen": None},
                     "every candidate is runtime — no P id of its own; "
                     "chosen stays None"))

    # 11 — FUTURE-STATE RECONSTRUCTION (reverse)
    fut_clauses = [c["clause"] for c in scopes.get("FUTURE / PLANNED", [])]
    fut = {"declared_end": end["end"] if end["named"] else None,
           "future_scope_clauses": fut_clauses,
           "states": ([{"state": end["end"], "from": "step 2, " + (end["grade"] or "")}]
                      if end["named"] else []) +
                     [{"state": c, "from": "FUTURE / PLANNED scope"}
                      for c in fut_clauses],
           "law": "reconstruction runs backwards: from the state being worked "
                  "toward, not from the words forward"}
    recs.append(_rec(STEPS[10], "the declared end + the ask's scopes", fut,
                     "" if fut["states"] else "no future state is named — the "
                                              "slot is open, not filled"))

    # 12 — EVIDENCE PREDICTION
    preds = []
    for s in end.get("separates_them", []):
        preds.append({"class": "SEPARATOR", "would_confirm": s["would_separate"],
                      "would_refute": "the same evidence pointing the other way",
                      "discriminating": True, "checked": False,
                      "from": "step 2 — two surviving ends"})
    if end["named"]:
        preds.append({"class": "MATERIAL",
                      "would_confirm": "arrangements consistent with %r "
                                       "existing before the event"
                                       % (end["end"][:60]),
                      "would_refute": "the arrangements serving a different "
                                      "end better",
                      "discriminating": True, "checked": False,
                      "from": "step 2 — the declared end"})
    preds.append({"class": "ABSENCE",
                  "would_confirm": "nothing found that the reading forbids",
                  "would_refute": "something found that the reading forbids",
                  "discriminating": False, "checked": False,
                  "why_not": "every reading owes an ABSENCE, so finding one "
                             "separates none of them",
                  "from": "the discipline every reading owes"})
    recs.append(_rec(STEPS[11], "the run's own readings",
                     {"predictions": preds,
                      "discriminating": sum(1 for p in preds
                                            if p["discriminating"]),
                      "checked_against_the_world": 0},
                     "stage 12 says what should be found; whether it IS found "
                     "is a verdict from outside"))

    # 13 — R-F-R (reverse pass two)
    facts = sorted({f for s in seqs for f in (s.get("structural_facts") or [])})
    cand = {"core_facts": facts, "repetition_count": 1,
            "step_support": {f: 1 for f in facts},
            "observed_pattern": " + ".join(facts) or "(no structural facts)"}
    rfr = PT.rfr_check(cand)
    recs.append(_rec(STEPS[12], "%d structural fact(s), 1 occurrence" % len(facts),
                     {"r_f_r": [p["verdict"] for p in rfr["r_f_r"]],
                      "stands": rfr["stands"],
                      "doubt_bites": rfr["doubt"]["bites"]},
                     "one occurrence can never be an arrangement — R-F-R on a "
                     "single ask SHOULD read thin, and it does"))

    # 14 — FALSIFIER / DOUBT
    lead = {"intent": (cands[0].get("id") if cands else None),
            "falsifiable": bool(preds and any(p["discriminating"] for p in preds)),
            "falsifier": next((p["would_refute"] for p in preds
                               if p["discriminating"]), None),
            "support": 1, "counterexamples": 0, "status": "LIVE"}
    killed = IL.kill(lead)
    recs.append(_rec(STEPS[13], "the leading candidate + its predictions",
                     {"survives": killed.get("survives", True),
                      "cannot_be_killed": killed.get("cannot_be_killed"),
                      "why": killed.get("why", ""),
                      "falsifier": lead["falsifier"]},
                     "untested is reported untested — 'nobody checked' is not "
                     "'it held'"))

    # 15 — MATURITY UPDATE
    mat = M.read(confirmed=(), refuted=(), support=1, sequences_seen=1,
                 checks=0)
    recs.append(_rec(STEPS[14], "what this run confirmed and refuted: nothing",
                     {"state": mat["state"], "why": mat["why"]},
                     ""))

    # 16 — VERDICT
    ver = M.verdict(mat)
    recs.append(_rec(STEPS[15], "the maturity from step 15",
                     {"verdict": ver["verdict"], "state": ver["state"],
                      "all_four": ver["all_four"]},
                     ""))

    # 17 — MEMORY WRITEBACK (prepared, not written)
    conditions = {
        "source retained": bool(text),
        "R-F-R executed": True,
        "status assigned": True,
        "link map created": False,
        "origin distance recorded": False,
    }
    prepared = {"would_append": {"kind": "EXAMPLE",
                                 "name": name or "(unnamed run)",
                                 "count_added": 1 + 2 * len(events)},
                "write_conditions": conditions,
                "conditions_met": sum(1 for v in conditions.values() if v),
                "conditions_total": len(conditions),
                "written": False,
                "why_not_written": "his five write conditions are the gate, and "
                                   "enforcing them at the write site is Phase D. "
                                   "Two of five are not met on this run (no "
                                   "link map — that is Phase D itself — and no "
                                   "origin distance), and writing past an unmet "
                                   "gate is what the gate exists to stop."}
    if write and root and all(conditions.values()):
        w = G.grow(root, text, name=name, surfaced_by="runtime.run")
        prepared["written"] = True
        prepared["wrote"] = w
        prepared["why_not_written"] = None
    recs.append(_rec(STEPS[16], "the run's rows + his five write conditions",
                     prepared, ""))

    # 18 — NEXT-SEQUENCE SEED
    closed = D.close({"stages_run": 18},
                     new_combinations=len(combos["combinations"]),
                     maturities=[mat], predictions=preds)
    recs.append(_rec(STEPS[17], "the whole run",
                     {"closed": closed.get("closed", True),
                      "successor": closed.get("successor_exists",
                                              closed.get("successor")),
                      "reasons": closed.get("reasons", [])},
                     "a successor references this run. NO REOPEN"))

    reverse_steps = [r["n"] for r in recs if r["direction"] == REVERSE]
    return {
        "phase": "B — runtime pipeline",
        "steps_run": len(recs),
        "of": len(STEPS),
        "order": [r["n"] for r in recs],
        "reverse_steps": reverse_steps,
        "records": recs,
        "answer": None,
        "chosen": None,
        "halts": [{"step": r["n"], "why": r["notes"]}
                  for r in recs if r["notes"].startswith("HALT")],
        "law": "the runtime prepares; he decides. `answer` is None on every "
               "run — auto may seat, combine, predict and mature; it may not "
               "promote, answer, or add a parameter.",
        "his_order": "steps 2 and 3 run REVERSE before decomposition — the "
                     "first of two reverse passes; R-F-R at 13 is the second.",
    }


def steps() -> dict:
    """The static table — his eighteen with owner and direction."""
    return {"steps": [dict(s) for s in STEPS],
            "count": len(STEPS),
            "reverse": [s["n"] for s in STEPS if s["dir"] == REVERSE],
            "was_absent_before_phase_b": [2, 3],
            "source": "his SELF-SUSTAINING EXECUTION FLOW sheet, box 2"}


def stats() -> dict:
    return {
        "phase": "B — runtime pipeline",
        "steps": len(STEPS),
        "reverse_steps": [s["n"] for s in STEPS if s["dir"] == REVERSE],
        "built_this_phase": [2, 3],
        "wired_this_phase": "all 18 as one run",
        "answers_produced": 0,
        "writes_by_default": 0,
        "write_gate": "his five write conditions; enforcement is Phase D",
        "not_in_this_phase": ["linking (D)", "memory writeback enforcement (D)",
                              "auto-trigger (E)", "promotion"],
    }


def annotations() -> list:
    return [
        ("his eighteen steps as one run, in his order", "runtime.run"),
        ("steps 2 and 3 reverse before decomposition", "runtime.STEPS"),
        ("a run is a record, never an answer", "runtime.run"),
        ("detected is not chosen", "runtime.detect_states"),
        ("the cross-role gate scoped to one ask", "runtime.combinations_in"),
        ("writeback prepared, gated on his five conditions",
         "runtime.run"),
    ]
