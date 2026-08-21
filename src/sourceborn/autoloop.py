"""PHASE E — THE SELF-SUSTAIN SCHEDULER.

The last phase of his SELF-SUSTAINING EXECUTION FLOW sheet, and the one his
own staging law governs:

    "Manual Mode Now -> Semi-Auto -> Auto-Sustain Target"

It is STAGED, not a switch — his correction to my proposal, which had asked
whether to switch auto on. So this module ships with the machinery whole and
the mode at MANUAL: deploying it changes NOTHING until he lifts the mode, and
lifting the mode is HIS action, recorded as its own append-only row.

WHAT A TICK IS

One bounded pass of the loop his sheet draws: material arrives (handed in by
hand, dropped in the inbox, or — in AUTO_SUSTAIN — the system's own output
from the tick before), each item runs the Phase B runtime, the run's own
steps compose the node refs, the node is written through Phase D's GATED
write site (his five conditions — a refused write stays refused), the Phase C
engine runs over the tick's material and `delta()` says what opened against
the tick before. Every tick appends a report; the report is the product.

THE FOUR LAWS OF THE TICK

  1. THE GATE DOES NOT MOVE. A tick may seat, link, combine, predict and
     mature. It may NOT promote, answer, kill, add a parameter, or write his
     count ledger. Structurally: no approve, no kill, no growth.add exists in
     this module's code, and a test reads the source to prove it. The queue
     for him fills; `promoted` cannot move from here.
  2. BOUNDED, AND EVERY CAP REPORTED. Auto plus append-only plus no delete
     is the main risk — an unbounded tick would fill his base with rows
     nobody chose. Items and nodes per tick are capped; what a cap defers is
     NAMED, and the report says which kind it is: a deferred INBOX file is
     picked up next tick (the cursor never saw it), while a deferred HANDED
     text is not stored and must be handed again — claiming "never dropped"
     for both would be false for the second.
  3. QUIET IS QUIET. A daemon tick that finds nothing new appends nothing —
     an hourly heartbeat would flood an append-only ledger with noise. A
     HAND tick always appends its report, because he asked and the answer
     "quiet" is an answer.
  4. NOTHING IS UN-PROCESSED BY DELETION. Inbox files are never removed;
     the cursor is a fold over past reports (name -> content hash). The same
     file arriving unchanged is skipped and said so; a CHANGED file is new
     material — a superseding reading, not an edit.

WHAT FEEDBACK MEANS, EXACTLY

In AUTO_SUSTAIN the previous tick's written nodes re-enter as ONE prepared
example for the Phase C engine — their (role, container) arrangements, row
parts marked. That is the L4 loop: the only loop whose input is the system's
own output. It is bounded (one example, last tick only) and its delta is
reported; a feedback pass that opens nothing new is the loop finding its own
quiet, which is the stop his sheet's target state needs.

WHAT A TICK DOES NOT DO, SAID PLAINLY

A tick is not a CHECK. Maturities decay on checks-without-confirmation — his
rule — and a tick checks nothing against the world, so maturities do not
move here. Evidence still arrives from outside, through check() and
remember(), on his word or a caller's verdict.
"""

from __future__ import annotations

import hashlib
import json
import os
import threading

_LOCK = threading.RLock()

# ---------------------------------------------------------------------------
# MODES — his staging, verbatim. MANUAL is the default and the reset state.
# ---------------------------------------------------------------------------

MANUAL = "MANUAL"
SEMI_AUTO = "SEMI_AUTO"
AUTO_SUSTAIN = "AUTO_SUSTAIN"
MODES = (MANUAL, SEMI_AUTO, AUTO_SUSTAIN)

MODE_MEANS = {
    MANUAL: "the tick runs only when called. The daemon does not drive it. "
            "This is the shipped default — deploying Phase E changes nothing "
            "until he lifts the mode.",
    SEMI_AUTO: "the daemon's hourly check runs the tick. New material is "
               "processed within budget; nothing feeds back.",
    AUTO_SUSTAIN: "his target state: the daemon runs the tick AND the "
                  "previous tick's own output re-enters as material — the "
                  "loop whose input is the system's output. Bounded, and it "
                  "stops itself at quiet.",
}

# ---------------------------------------------------------------------------
# BUDGETS — the thing that makes auto safe to switch on at all.
# ---------------------------------------------------------------------------

MAX_ITEMS_PER_TICK = 5
MAX_NODES_PER_TICK = 40


def _dir(root: str) -> str:
    d = os.path.join(root or ".", "auto")
    os.makedirs(d, exist_ok=True)
    return d


def _inbox(root: str) -> str:
    d = os.path.join(_dir(root), "inbox")
    os.makedirs(d, exist_ok=True)
    return d


def _ticks_path(root: str) -> str:
    return os.path.join(_dir(root), "ticks.jsonl")


def _mode_path(root: str) -> str:
    return os.path.join(_dir(root), "mode.jsonl")


def _load(path: str) -> list:
    if not os.path.exists(path):
        return []
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception as e:
                rows.append({"row": "UNREADABLE", "line": i,
                             "raw": line[:200], "error": str(e)})
    return rows


def _append(path: str, row: dict) -> dict:
    with open(path, "a", encoding="utf-8") as f:   # append only
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


# ---------------------------------------------------------------------------
# MODE — his switch. An append-only log; the last row wins; MANUAL when the
# log is empty.
# ---------------------------------------------------------------------------

def mode(root: str) -> str:
    rows = [r for r in _load(_mode_path(root)) if r.get("row") == "MODE"]
    return rows[-1]["mode"] if rows else MANUAL


def set_mode(root: str, new_mode: str) -> dict:
    """HIS action. Recorded with what it was before — never overwritten."""
    m = (new_mode or "").strip().upper()
    if m not in MODES:
        return {"changed": False, "refused": True,
                "why": "not one of his three modes: %s (they are %s)"
                       % (new_mode, " -> ".join(MODES))}
    with _LOCK:
        prior = mode(root)
        _append(_mode_path(root), {"row": "MODE", "mode": m, "prior": prior,
                                   "by": "him"})
    return {"changed": True, "mode": m, "prior": prior, "by": "him",
            "staging": " -> ".join(MODES)}


# ---------------------------------------------------------------------------
# THE CURSOR — a fold over past reports. Nothing is un-processed by deleting.
# ---------------------------------------------------------------------------

def ticks(root: str) -> list:
    return [r for r in _load(_ticks_path(root)) if r.get("row") == "TICK"]


def _seen_hashes(root: str) -> dict:
    seen = {}
    for t in ticks(root):
        for it in t.get("processed_inbox", []):
            seen[it["name"]] = it["hash"]
    return seen


def _hash(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()[:16]


def _inbox_material(root: str) -> tuple:
    """New or changed inbox files, and what was skipped unchanged."""
    seen = _seen_hashes(root)
    new, skipped, unreadable = [], [], []
    for fn in sorted(os.listdir(_inbox(root))):
        p = os.path.join(_inbox(root), fn)
        if not os.path.isfile(p):
            continue
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                text = f.read(60000)
        except Exception as e:
            unreadable.append({"name": fn, "error": str(e)})
            continue
        h = _hash(text)
        if seen.get(fn) == h:
            skipped.append(fn)
        else:
            new.append({"name": fn, "text": text, "hash": h,
                        "changed": fn in seen})
    return new, skipped, unreadable


# ---------------------------------------------------------------------------
# REFS FROM A RUN — the wiring Phase D left stated: the runtime's own steps
# compose the node's refs, so a written node cites what the run actually did.
# ---------------------------------------------------------------------------

def refs_from_run(run: dict, source_name: str = "") -> dict:
    rec = {x["n"]: x for x in run.get("records", [])}
    events = (rec.get(1, {}).get("produced") or {}).get("events", [])
    top = events[-1] if events else {}
    end = rec.get(2, {}).get("produced") or {}
    seats = rec.get(5, {}).get("produced") or {}
    refs = {
        "event_sig": (top.get("happening") or "").upper().replace(" ", "_"),
        "actor": (top.get("actor") or "").strip()
                 if not (top.get("actor") or "").startswith("(") else "",
        "role": "",   # filled below when the engine record carries one
        "rows": seats.get("rows_seated", []),
        "containers": seats.get("containers_activated", []),
        "future": (end.get("end") or "") if end.get("named") else "",
        "point_zero": source_name or "(handed text)",
    }
    eng = (rec.get(9, {}).get("produced") or {})
    arrs = eng.get("arrangements") or []
    if arrs:
        refs["role"] = arrs[0].get("role", "")
    return {k: v for k, v in refs.items() if v not in ("", [], None)}


# ---------------------------------------------------------------------------
# THE TICK.
# ---------------------------------------------------------------------------

def tick(root: str, texts=None, by: str = "hand") -> dict:
    """One bounded pass. Appends its report (a daemon tick only when
    something happened) and returns it. The report is the product — there is
    no answer field because a tick does not answer."""
    from . import runtime as R
    from . import combine as C
    from . import nodegraph as NG

    with _LOCK:
        m = mode(root)
        prior_ticks = ticks(root)
        n = len(prior_ticks) + 1
        last = prior_ticks[-1] if prior_ticks else None

        handed = [{"name": "handed %d" % (i + 1), "text": t, "hash": _hash(t)}
                  for i, t in enumerate(texts or []) if (t or "").strip()]
        inbox_new, inbox_skipped, inbox_unreadable = _inbox_material(root)

        # inbox first: a deferred INBOX item is genuinely picked up next tick
        # (the cursor never saw it), while a deferred HANDED text is not
        # stored anywhere and must be handed again — the report says which,
        # because "never dropped" would be a lie for the handed kind.
        material = inbox_new + handed
        overflow = material[MAX_ITEMS_PER_TICK:]
        deferred_inbox = [it["name"] for it in overflow
                          if not it["name"].startswith("handed ")]
        deferred_handed = [it["name"] for it in overflow
                           if it["name"].startswith("handed ")]
        material = material[:MAX_ITEMS_PER_TICK]

        written, reinforced, refused = [], [], []
        combine_texts = []
        for it in material:
            run = R.run(it["text"], name=it["name"])
            combine_texts.append(it["text"])
            if len(written) >= MAX_NODES_PER_TICK:
                refused.append({"name": it["name"],
                                "why": "node budget for this tick is spent — "
                                       "the item was still processed and "
                                       "combined, only the write waits"})
                continue
            refs = refs_from_run(run, source_name=it["name"])
            rfr = next((x["produced"] for x in run["records"]
                        if x["n"] == 13), {})
            w = NG.write_node(root, "EVENT",
                              point_zero_ref=it["text"][:300],
                              refs=refs,
                              rfr={"stands": rfr.get("stands"),
                                   "from": "runtime step 13"},
                              proof_debt=1,
                              surfaced_by="auto tick %d (%s) — %s"
                                          % (n, by, it["name"]))
            if w.get("written"):
                written.append({"node_id": w["node_id"], "refs": refs,
                                "links": w["link_map"]["count"]})
            elif w.get("strengthened_existing"):
                reinforced.append({"node": w["strengthened_existing"],
                                   "support": w["support"],
                                   "from": it["name"]})
            else:
                refused.append({"name": it["name"],
                                "why": "; ".join(w.get("unmet_conditions",
                                                       []))})

        # THE ENGINE, with feedback in AUTO_SUSTAIN — the L4 loop
        prepared = None
        fed_back = False
        if m == AUTO_SUSTAIN and last and last.get("written_nodes"):
            arrs, rowp = {}, set()
            for wn in last["written_nodes"]:
                rf = wn.get("refs", {})
                role = rf.get("role") or "ACTION"
                for c in rf.get("containers", []):
                    arrs[(role, c)] = arrs.get((role, c), 0) + 1
                    if rf.get("rows"):
                        rowp.add((role, c))
            if arrs:
                prepared = [{"name": "feedback from tick %d" % last["n"],
                             "arrangements": arrs, "row_parts": rowp,
                             "events": len(last["written_nodes"])}]
                fed_back = True
        if combine_texts and prepared:
            ex, gran = C._prepare(texts=combine_texts)
            ex2, gran2 = C._prepare(prepared=prepared)
            gran.update(gran2)
            eng = C.run(prepared=[{"name": e["name"],
                                   "arrangements": e["arrangements"],
                                   "row_parts": [k for k in e["arrangements"]
                                                 if gran.get(k) == C.ROW],
                                   "events": e["events"]}
                                  for e in ex + ex2],
                        name="tick %d" % n)
        elif combine_texts:
            eng = C.run(texts=combine_texts, name="tick %d" % n)
        elif prepared:
            eng = C.run(prepared=prepared, name="tick %d" % n)
        else:
            eng = None

        prev_stub = {"candidates": [
            {"signature": s, "order": 0, "support": 0, "round": 0,
             "intents": {"pairs": []}}
            for s in (last or {}).get("combine_signatures", [])]}
        delta = (C.delta(prev_stub, eng) if eng else
                 {"anything_new": False, "count_new": 0})

        q = NG.queue_for_him(root)
        something_happened = bool(written or reinforced or
                                  delta.get("anything_new") or
                                  inbox_new or handed)
        report = {
            "row": "TICK", "n": n, "mode": m, "by": by,
            "arrived": {"handed": len(handed), "inbox_new": len(inbox_new),
                        "inbox_skipped_unchanged": inbox_skipped,
                        "inbox_unreadable": inbox_unreadable,
                        "feedback_example": fed_back},
            "processed": [it["name"] for it in material],
            "processed_inbox": [{"name": it["name"], "hash": it["hash"]}
                                for it in material if "text" in it
                                and not it["name"].startswith("handed ")],
            "deferred_by_budget": {
                "inbox": deferred_inbox,
                "handed": deferred_handed,
                "inbox_note": ("picked up next tick — the cursor never saw "
                               "them" if deferred_inbox else None),
                "handed_note": ("NOT stored — a handed text the budget "
                                "deferred must be handed again; saying "
                                "'never dropped' here would be false"
                                if deferred_handed else None),
            },
            "written_nodes": written,
            "reinforced": reinforced,
            "refused_writes": refused,
            "combine": ({"combinations": eng["counts"]["combinations"],
                         "stopped_because": eng["stopped_because"],
                         "delta_new": delta.get("count_new", 0),
                         "anything_new": delta.get("anything_new", False)}
                        if eng else None),
            "combine_signatures": ([c["signature"]
                                    for c in eng["candidates"]][:200]
                                   if eng else []),
            "queued_for_him": q["count"],
            "promoted": q["promoted"],
            "promoted_can_move_from_here": False,
            "caps": {
                "items": MAX_ITEMS_PER_TICK, "nodes": MAX_NODES_PER_TICK,
                "items_deferred": len(deferred_inbox) + len(deferred_handed),
                "cap_note": ("the item cap BIT — %d inbox item(s) wait for "
                             "the next tick, %d handed text(s) must be "
                             "handed again; all named above"
                             % (len(deferred_inbox), len(deferred_handed)))
                            if (deferred_inbox or deferred_handed) else None,
            },
            "quiet": not something_happened,
            "maturities_touched": 0,
            "why_no_maturity_moves": "a tick is not a check. Decay is "
                                     "checks-without-confirmation — his rule "
                                     "— and a tick checks nothing against "
                                     "the world.",
        }
        if by == "hand" or something_happened:
            _append(_ticks_path(root), report)
        return report


def tick_if_due(root: str) -> dict:
    """What the daemon calls, hourly. MANUAL means what it says."""
    m = mode(root)
    if m == MANUAL:
        return {"ran": False, "mode": m,
                "why": "manual mode — the daemon does not drive the tick. "
                       "Lifting the mode is his action (POST /auto/mode)."}
    return tick(root, by="daemon")


# ---------------------------------------------------------------------------
# THE GATE CHART — what auto may and may not do. Displayed, and enforced by
# what this module simply does not contain.
# ---------------------------------------------------------------------------

def gate() -> dict:
    return {
        "auto_may": ["seat", "link", "combine", "predict", "mature "
                     "(read only — moves need evidence handed in)"],
        "auto_may_not": ["promote", "make canonical", "add a parameter",
                         "answer", "kill", "delete",
                         "write his count ledger"],
        "how_enforced": "structurally — no approve, no kill, no growth.add "
                        "exists in this module's code, and a test reads the "
                        "source to prove it. The write site it does use is "
                        "Phase D's, behind his five conditions.",
        "his_gate": "everything auto produces arrives at his desk as a "
                    "candidate with its evidence. Nothing crosses without "
                    "his word.",
    }


def stats(root: str) -> dict:
    ts = ticks(root)
    return {
        "phase": "E — self-sustain scheduler",
        "mode": mode(root),
        "mode_means": MODE_MEANS[mode(root)],
        "staging": " -> ".join(MODES),
        "ticks": len(ts),
        "last_tick": ({k: ts[-1][k] for k in
                       ("n", "mode", "by", "quiet", "processed",
                        "deferred_by_budget", "queued_for_him", "promoted")}
                      if ts else None),
        "budgets": {"items_per_tick": MAX_ITEMS_PER_TICK,
                    "nodes_per_tick": MAX_NODES_PER_TICK},
        "inbox": _inbox(root),
        "gate": gate(),
        "daemon": "the hourly thread that already drives the weekly pull "
                  "calls tick_if_due; in MANUAL it does nothing.",
    }


def annotations() -> list:
    return [
        ("manual mode now — shipped OFF, his switch", "autoloop.set_mode"),
        ("one bounded pass, every cap reported", "autoloop.tick"),
        ("the daemon calls, the mode decides", "autoloop.tick_if_due"),
        ("the runtime's own steps compose the node refs",
         "autoloop.refs_from_run"),
        ("the L4 feedback loop, bounded and reported", "autoloop.tick"),
        ("nothing un-processed by deletion — the hash cursor",
         "autoloop._inbox_material"),
        ("the gate chart, enforced by absence", "autoloop.gate"),
    ]
