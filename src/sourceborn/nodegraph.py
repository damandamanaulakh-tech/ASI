"""PHASE D — THE MEMORY GRAPH + AUTO-LINKING.

From his SELF-SUSTAINING EXECUTION FLOW sheet, the fourth phase: the node
schema Phase A locked becomes a LIVING STORE — nodes written under his five
write conditions, linked at write time by his six read conditions, each node
carrying its own chain of readings, and the whole thing traversable.

WHAT THIS CLOSES

  * STAGE 5, RELATION GRAPH — PARTIAL since the first audit ("listed, not
    traversable"). `neighbours()`, `path()` and `subgraph()` make it a graph
    you can actually walk, with every hop TYPED.
  * THE WRITE GATE — Phase A defined his five write conditions and said
    plainly that ENFORCING them at the write site is Phase D. `write_node`
    is that site: a write that fails a condition is REFUSED with the unmet
    conditions named. The fourth condition — "link map created" — is met BY
    this write path, because the auto-linker runs inside it; that is exactly
    why the condition could not be enforced before D existed.
  * THE EMPTY BRAINS — the 2026-08-12 audit found 90 of 95 node brains hold
    no memory, and it stayed true through every build since. `remember()` is
    the per-node chain of readings (the maturity.update shape applied to a
    node): append-only, each reading referencing the one before, kinds
    constrained to his eleven.
  * THREE OF HIS NINE LOOPS — Retrieval (recall by his six read conditions),
    Memory Reinforcement (the reading chain), and the Contradiction loop in
    its honest scope (below).

THE SIX READ CONDITIONS ARE ONE MECHANISM, USED TWICE

`recall(probe)` answers "which stored nodes does this material reach, and by
which of his six conditions" — that is the Retrieval loop. The auto-linker is
the SAME call at write time: what recall finds, the linker links. One
implementation, so retrieval and linking can never disagree.

WHAT A LINK IS — TYPED, WITH THE GRAPH SHAPE HIS TWELVE TYPES EXIST FOR

His box 6 says auto-link; his Phase A gave ten TYPED links and twelve node
types including ACTOR, PATTERN, ARTIFACT and FUTURE_STATE. Those types only
do work if the linker MATERIALIZES them: two events by the same actor do not
get a vague tie to each other — an ACTOR node exists once, and each event is
linked to it with `actor_of`. Same for the pattern (events SUPPORT the
pattern node), the artifact (an event DEPENDS_ON the object it happened to —
prior.py's own entailment), and the future state (an event is FUTURE_OF the
state it worked toward). `similar_to` is reserved for two events sharing
actual seated rows — and CONTAINERS ALONE NEVER LINK, the same lesson as
Phase C's anchor gate: structure is not content, and a similarity blob is
what the typed links exist to prevent.

THE CONTRADICTION LOOP, IN ITS HONEST SCOPE

`contradicts` fires structurally in ONE case: two nodes carrying the SAME
subject whose verdicts OPPOSE (one RETAIN, one REJECT). Detecting deeper
contradiction from arbitrary prose is model-grade inference this module does
not have, and claiming it would be fake. Anything richer arrives from a
caller that saw it (a witness split, a filter HALT) and says so.

HIS BOX 6, AND THE QUESTION HE HAS NOT ANSWERED

The decision tree runs: existing match -> strengthen the existing node
(support +1, duplicate_created False — his mall-example reinforcement rule
applied to nodes); no match -> a new node is written OPEN. The evidence gate
and the maturity threshold are EVALUATED, and a node that passes both lands
in a QUEUE FOR HIM — because his sheet ends the tree at "Assign Permanent
Node ID" and I asked whether passing the gates assigns it on its own or
queues for him, and he has not answered. Until he does, the conservative
reading stands: THE QUEUE HOLDS, `promoted` stays 0, and `approve()` exists
as HIS action. This is a placeholder for his answer, not the answer.

APPEND-ONLY, STRUCTURALLY

No delete, remove, drop, clear, prune, truncate, pop or unlink path exists in
this module; the store opens in mode "a" only; a corrupt line comes back
UNREADABLE with its raw text; and a test reads this module's own source — the
growth.py technique — and fails if a removal path is ever added. NO REOPEN:
nothing is ever rewritten; an approval, a correction or a new reading is a
new row referencing what it acts on.
"""

from __future__ import annotations

import json
import os

# ---------------------------------------------------------------------------
# THE STORE — one JSONL, typed rows, append-only.
# ---------------------------------------------------------------------------

R_NODE = "NODE"
R_LINK = "LINK"
R_READING = "READING"
R_APPROVAL = "APPROVAL"


def _dir(root: str) -> str:
    d = os.path.join(root or ".", "nodes")
    os.makedirs(d, exist_ok=True)
    return d


def _path(root: str) -> str:
    return os.path.join(_dir(root), "graph.jsonl")


def load(root: str) -> list:
    """Every row ever appended, in order. Never filtered, never pruned."""
    p = _path(root)
    if not os.path.exists(p):
        return []
    rows = []
    with open(p, "r", encoding="utf-8") as f:
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


def _append(root: str, row: dict) -> dict:
    with open(_path(root), "a", encoding="utf-8") as f:   # append only
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


# ---------------------------------------------------------------------------
# REFS — what a node is ABOUT, for linking and recall. Free dict, but the
# keys the six conditions read are fixed and named here.
# ---------------------------------------------------------------------------

REF_KEYS = {
    "actor": "who acted — same actor materializes an ACTOR node",
    "event_sig": "the event shell — exact match is 'similar event' at its "
                 "strongest",
    "rows": "seated P ids — 2+ shared rows is 'similar event'; containers "
            "alone NEVER link",
    "containers": "seated containers — kept for the record, never sufficient",
    "pattern_sig": "the arrangement signature — same pattern",
    "artifact": "the object it happened to — same artifact family",
    "future": "the declared end — same future-state goal",
    "subject_sig": "what the node makes a claim about — the contradiction "
                   "check compares verdicts over the same subject",
    "verdict": "RETAIN / WEAKEN / REJECT / UNKNOWN, when the node carries one",
}


def _norm(v) -> str:
    return " ".join(str(v or "").lower().split())


# ---------------------------------------------------------------------------
# THE FOLD — a node's current state is computed from its rows. Nothing is
# ever rewritten, so history is always whole.
# ---------------------------------------------------------------------------

def nodes_of(rows: list) -> dict:
    return {r["node"]["node_id"]: r for r in rows if r.get("row") == R_NODE}


def node_state(root: str, node_id: str, rows: list = None) -> dict:
    rows = rows if rows is not None else load(root)
    base = None
    for r in rows:
        if r.get("row") == R_NODE and r["node"]["node_id"] == node_id:
            base = r
            break
    if base is None:
        return {"found": False, "node_id": node_id}
    links_out = [r for r in rows if r.get("row") == R_LINK
                 and r["from"] == node_id]
    links_in = [r for r in rows if r.get("row") == R_LINK
                and r["to"] == node_id]
    readings = [r for r in rows if r.get("row") == R_READING
                and r["node"] == node_id]
    approvals = [r for r in rows if r.get("row") == R_APPROVAL
                 and r["node"] == node_id]
    status = base["node"]["status"]
    if approvals:
        status = approvals[-1]["status_after"]
    support = 1 + sum(1 for r in readings if r["kind"] == "EVIDENCE"
                      and r.get("support_delta"))
    return {
        "found": True,
        "node": base["node"],
        "refs": base.get("refs", {}),
        "status": status,
        "status_is_from": ("his approval" if approvals
                           else "construction"),
        "support": support,
        "links_out": [{"link": r["link"], "to": r["to"],
                       "read_condition": r.get("read_condition"),
                       "evidence": r.get("evidence")} for r in links_out],
        "links_in": [{"link": r["link"], "from": r["from"],
                      "read_condition": r.get("read_condition"),
                      "evidence": r.get("evidence")} for r in links_in],
        "memory": [{"n": r["n"], "kind": r["kind"], "reading": r["reading"],
                    "references": r["references"]} for r in readings],
        "approvals": approvals,
    }


# ---------------------------------------------------------------------------
# RECALL — his six read conditions as a query. The auto-linker calls THIS.
# ---------------------------------------------------------------------------

SIMILAR_ROWS_BAR = 2     # shared seated rows for 'similar event' — containers
                         # alone never count, the Phase C anchor lesson


def recall(root: str, refs: dict, rows: list = None,
           exclude: str = "") -> dict:
    """Which stored nodes this material reaches, by which of his six
    conditions, with the evidence named. The Retrieval loop."""
    rows = rows if rows is not None else load(root)
    stored = [r for r in rows if r.get("row") == R_NODE
              and r["node"]["node_id"] != exclude]
    probe_rows = set(refs.get("rows") or [])
    hits = {k: [] for k in ("similar_event", "same_actor", "same_pattern",
                            "same_artifact_family", "same_contradiction",
                            "same_future_goal")}
    for r in stored:
        nid = r["node"]["node_id"]
        rf = r.get("refs", {})
        if refs.get("event_sig") and _norm(rf.get("event_sig")) == \
                _norm(refs["event_sig"]):
            hits["similar_event"].append(
                {"node": nid, "evidence": "same event shell: %s"
                 % refs["event_sig"], "strength": "EXACT SHELL"})
        else:
            shared = sorted(probe_rows & set(rf.get("rows") or []))
            if len(shared) >= SIMILAR_ROWS_BAR:
                hits["similar_event"].append(
                    {"node": nid, "evidence": "shared seated rows: %s"
                     % ", ".join(shared[:4]),
                     "strength": "%d shared rows" % len(shared)})
        if refs.get("actor") and _norm(rf.get("actor")) == \
                _norm(refs["actor"]):
            hits["same_actor"].append(
                {"node": nid, "evidence": "actor: %s" % refs["actor"]})
        if refs.get("pattern_sig") and _norm(rf.get("pattern_sig")) == \
                _norm(refs["pattern_sig"]):
            hits["same_pattern"].append(
                {"node": nid, "evidence": "pattern: %s" % refs["pattern_sig"]})
        if refs.get("artifact") and _norm(rf.get("artifact")) == \
                _norm(refs["artifact"]):
            hits["same_artifact_family"].append(
                {"node": nid, "evidence": "artifact: %s" % refs["artifact"]})
        if refs.get("future") and _norm(rf.get("future")) == \
                _norm(refs["future"]):
            hits["same_future_goal"].append(
                {"node": nid, "evidence": "future state: %s" % refs["future"]})
        if refs.get("subject_sig") and _norm(rf.get("subject_sig")) == \
                _norm(refs["subject_sig"]):
            va, vb = _norm(refs.get("verdict")), _norm(rf.get("verdict"))
            if {va, vb} == {"retain", "reject"}:
                hits["same_contradiction"].append(
                    {"node": nid,
                     "evidence": "same subject %r, opposing verdicts %s vs %s"
                     % (refs["subject_sig"], refs.get("verdict"),
                        rf.get("verdict"))})
    return {
        "conditions": hits,
        "reached": sorted({h["node"] for v in hits.values() for h in v}),
        "note": "containers alone never link — structure is not content. The "
                "contradiction condition fires only on opposing verdicts over "
                "the same subject; anything richer must arrive from a caller "
                "that saw it.",
    }


# ---------------------------------------------------------------------------
# THE AUTO-LINKER — what recall finds, the linker links, with the graph
# shape his node types exist for. Hub nodes materialize ONCE.
# ---------------------------------------------------------------------------

def _next_n(rows: list, node_type: str) -> int:
    from . import nodebrain as NB
    stem = NB._STEM[node_type]
    return 1 + sum(1 for r in rows if r.get("row") == R_NODE
                   and r["node"]["node_id"].split("-")[2] == stem)


def _find_hub(rows: list, node_type: str, ref_key: str, value: str):
    for r in rows:
        if r.get("row") == R_NODE and r["node"]["node_type"] == node_type \
                and _norm(r.get("refs", {}).get(ref_key)) == _norm(value):
            return r["node"]["node_id"]
    return None


def _write_hub(root: str, rows: list, node_type: str, ref_key: str,
               value: str, point_zero_ref: str) -> tuple:
    """One hub per referent. Found -> reused; absent -> written OPEN."""
    from . import nodebrain as NB
    nid = _find_hub(rows, node_type, ref_key, value)
    if nid:
        return nid, False
    node = NB.new_node(node_type, _next_n(rows, node_type),
                       point_zero_ref=point_zero_ref)
    row = {"row": R_NODE, "node": node, "refs": {ref_key: value},
           "surfaced_by": "auto-linker — %s materialized once" % node_type,
           "write_conditions": {"met": "hub — carries its referent and its "
                                       "source; it makes no claim to gate"}}
    _append(root, row)
    rows.append(row)
    return node["node_id"], True


# read condition -> (hub node type, ref key, link type, direction of link)
_HUB_LINKS = {
    "same_actor": ("ACTOR", "actor", "actor_of", "hub_to_node"),
    "same_pattern": ("PATTERN", "pattern_sig", "supports", "node_to_hub"),
    "same_artifact_family": ("ARTIFACT", "artifact", "depends_on",
                             "node_to_hub"),
    "same_future_goal": ("FUTURE_STATE", "future", "future_of",
                         "node_to_hub"),
}


def autolink(root: str, node_id: str, refs: dict, rows: list) -> dict:
    """The link map. Runs INSIDE write_node — which is what makes his fourth
    write condition meetable at all."""
    from . import nodebrain as NB
    found = recall(root, refs, rows=rows, exclude=node_id)
    links = []

    def put(frm, link, to, cond, ev):
        row = {"row": R_LINK, "from": frm, "link": link, "to": to,
               "direction": NB._LINK[link]["dir"],
               "inverse": NB._LINK[link]["inverse"],
               "read_condition": cond, "evidence": ev}
        _append(root, row)
        rows.append(row)
        links.append(row)

    for h in found["conditions"]["similar_event"]:
        put(node_id, "similar_to", h["node"], "similar_event", h["evidence"])
    for h in found["conditions"]["same_contradiction"]:
        put(node_id, "contradicts", h["node"], "same_contradiction",
            h["evidence"])

    hubs = []
    for cond, (ntype, key, link, direction) in _HUB_LINKS.items():
        value = refs.get(key)
        if not value:
            continue
        if not found["conditions"][cond] and not _find_hub(rows, ntype, key,
                                                           value):
            # nothing shares this referent yet — the hub still materializes,
            # so the NEXT node that shares it links through it
            pass
        hub_id, created = _write_hub(root, rows, ntype, key, value,
                                     point_zero_ref=refs.get("point_zero",
                                                             value))
        hubs.append({"hub": hub_id, "type": ntype, "created": created,
                     "referent": value})
        if direction == "hub_to_node":
            put(hub_id, link, node_id, cond, "%s: %s" % (key, value))
        else:
            put(node_id, link, hub_id, cond, "%s: %s" % (key, value))

    return {
        "created": True,
        "links": [{"from": l["from"], "link": l["link"], "to": l["to"],
                   "why": l["read_condition"]} for l in links],
        "hubs": hubs,
        "count": len(links),
        "note": ("a link map with zero links is still a MAP — it records "
                 "that the conditions were checked and nothing matched"
                 if not links else ""),
    }


# ---------------------------------------------------------------------------
# THE WRITE SITE — his five conditions, ENFORCED.
# ---------------------------------------------------------------------------

def write_node(root: str, node_type: str, point_zero_ref: str, refs: dict,
               rfr: dict = None, status: str = "OPEN",
               maturity_level: str = "UNTESTED", proof_debt: int = None,
               surfaced_by: str = "") -> dict:
    """The one way into the graph. A write that fails his conditions is
    REFUSED with the unmet conditions named — never stored malformed.

    An exact existing match is NOT duplicated: the existing node gains a
    support reading instead (his reinforcement rule — support 1 -> 2,
    duplicate_created False)."""
    from . import nodebrain as NB
    rows = load(root)
    refs = dict(refs or {})

    conditions = {
        "source retained": bool((point_zero_ref or "").strip()),
        "R-F-R executed": bool(rfr),
        "status assigned": status in NB.STATUSES,
        "link map created": True,    # met BY this path — the linker runs below
        "origin distance recorded": isinstance(proof_debt, int)
                                    and 0 <= proof_debt <= 5,
    }
    unmet = [k for k, v in conditions.items() if not v]
    if unmet:
        return {"written": False, "refused": True,
                "unmet_conditions": unmet,
                "conditions": conditions,
                "why": "his write conditions are the gate, and this is the "
                       "write site. Nothing is stored malformed.",
                "duplicate_created": False}

    # BOX 6, FIRST BRANCH — existing match strengthens, never duplicates.
    # A match is the same CLAIM: same signature, same actor, same verdict.
    # The verdict check is load-bearing — without it, the first test of the
    # contradiction path folded an OPPOSING reading into the node it opposed,
    # which is a contradiction silently swallowed as a duplicate.
    sig_key = "event_sig" if refs.get("event_sig") else "subject_sig"
    if refs.get(sig_key):
        for r in rows:
            if r.get("row") != R_NODE:
                continue
            if r["node"]["node_type"] != node_type.strip().upper():
                continue
            if _norm(r.get("refs", {}).get(sig_key)) == _norm(refs[sig_key]) \
                    and _norm(r.get("refs", {}).get("actor")) == \
                    _norm(refs.get("actor")) \
                    and _norm(r.get("refs", {}).get("verdict")) == \
                    _norm(refs.get("verdict")):
                existing = r["node"]["node_id"]
                remember(root, existing, "EVIDENCE",
                         "support +1 — the same %s arrived again from %s"
                         % (sig_key, surfaced_by or "(unnamed source)"),
                         support_delta=1, rows=rows)
                st = node_state(root, existing, rows=load(root))
                return {"written": False, "duplicate_created": False,
                        "strengthened_existing": existing,
                        "support": st["support"],
                        "why": "his rule: an existing match is reinforced, "
                               "never re-created. Support rose instead."}

    node = NB.new_node(node_type, _next_n(rows, node_type.strip().upper()),
                       point_zero_ref=point_zero_ref, status=status,
                       maturity_level=maturity_level, proof_debt=proof_debt)
    row = {"row": R_NODE, "node": node, "refs": refs,
           "surfaced_by": surfaced_by,
           "rfr_verdict": (rfr or {}).get("stands"),
           "write_conditions": conditions}
    _append(root, row)
    rows.append(row)
    linkmap = autolink(root, node["node_id"], refs, rows)
    return {
        "written": True, "refused": False,
        "node_id": node["node_id"],
        "conditions": conditions, "conditions_met": 5,
        "link_map": linkmap,
        "duplicate_created": False,
        "gates": gates_of(node_state(root, node["node_id"],
                                     rows=load(root))),
    }


# ---------------------------------------------------------------------------
# MEMORY — the per-node chain of readings. The 90-empty-brains answer, at
# the node level: append-only, each reading referencing the one before.
# ---------------------------------------------------------------------------

def remember(root: str, node_id: str, kind: str, reading: str,
             support_delta: int = 0, rows: list = None) -> dict:
    from . import nodebrain as NB
    if kind not in NB.MEMORY_KINDS:
        raise KeyError("not one of his eleven memory kinds: %s (they are %s)"
                       % (kind, ", ".join(NB.MEMORY_KINDS)))
    rows = rows if rows is not None else load(root)
    if not any(r.get("row") == R_NODE and r["node"]["node_id"] == node_id
               for r in rows):
        raise KeyError("no such node: %s" % node_id)
    prior = [r for r in rows if r.get("row") == R_READING
             and r["node"] == node_id]
    row = {"row": R_READING, "node": node_id, "n": len(prior) + 1,
           "kind": kind, "reading": reading,
           "references": (prior[-1]["n"] if prior else None),
           "support_delta": support_delta}
    _append(root, row)
    return {"node": node_id, "n": row["n"], "kind": kind,
            "references": row["references"],
            "chain_length": row["n"],
            "law": "a memory node is not a field that gets overwritten — it "
                   "is a chain of readings, each referencing the one before."}


def memory_of(root: str, node_id: str) -> list:
    return [{"n": r["n"], "kind": r["kind"], "reading": r["reading"],
             "references": r["references"]}
            for r in load(root)
            if r.get("row") == R_READING and r["node"] == node_id]


# ---------------------------------------------------------------------------
# TRAVERSAL — stage 5 stops being a list.
# ---------------------------------------------------------------------------

def neighbours(root: str, node_id: str, rows: list = None) -> dict:
    rows = rows if rows is not None else load(root)
    out = {}
    for r in rows:
        if r.get("row") != R_LINK:
            continue
        if r["from"] == node_id:
            out.setdefault(r["link"], []).append(
                {"to": r["to"], "evidence": r.get("evidence")})
        elif r["to"] == node_id:
            out.setdefault(r["inverse"], []).append(
                {"to": r["from"], "evidence": r.get("evidence")})
    return {"node": node_id, "by_link": out,
            "degree": sum(len(v) for v in out.values())}


def path(root: str, a: str, b: str, max_depth: int = 6) -> dict:
    """Shortest typed path a -> b. Every hop names its link type — a path
    through `contradicts` MEANS something different from one through
    `supports`, which is the whole point of typed links."""
    rows = load(root)
    if a == b:
        return {"found": True, "hops": [], "length": 0}
    frontier = {a: []}
    seen = {a}
    for _ in range(max_depth):
        nxt = {}
        for nid, hops in frontier.items():
            nb = neighbours(root, nid, rows=rows)
            for link, tos in nb["by_link"].items():
                for t in tos:
                    if t["to"] in seen:
                        continue
                    trail = hops + [{"from": nid, "link": link,
                                     "to": t["to"]}]
                    if t["to"] == b:
                        return {"found": True, "hops": trail,
                                "length": len(trail)}
                    seen.add(t["to"])
                    nxt[t["to"]] = trail
        frontier = nxt
        if not frontier:
            break
    return {"found": False, "hops": [], "length": 0,
            "why": "no typed path within %d hops" % max_depth}


def subgraph(root: str, seed: str, depth: int = 2) -> dict:
    rows = load(root)
    keep, frontier = {seed}, {seed}
    for _ in range(depth):
        nxt = set()
        for nid in frontier:
            for tos in neighbours(root, nid, rows=rows)["by_link"].values():
                nxt |= {t["to"] for t in tos}
        frontier = nxt - keep
        keep |= nxt
        if not frontier:
            break
    links = [r for r in rows if r.get("row") == R_LINK
             and r["from"] in keep and r["to"] in keep]
    return {
        "seed": seed, "depth": depth,
        "nodes": sorted(keep),
        "links": [{"from": r["from"], "link": r["link"], "to": r["to"]}
                  for r in links],
        "counts": {"nodes": len(keep), "links": len(links)},
    }


# ---------------------------------------------------------------------------
# BOX 6 GATES AND THE QUEUE FOR HIM.
# ---------------------------------------------------------------------------

def gates_of(state: dict) -> dict:
    """His two gates, evaluated — never acted on."""
    ev = [m for m in state.get("memory", [])
          if m["kind"] == "EVIDENCE" and "confirmed" in m["reading"].lower()]
    evidence_gate = bool(ev)
    mat = state.get("node", {}).get("maturity_level", "UNTESTED")
    maturity_gate = mat in ("SUPPORTED", "STRONG")
    return {
        "evidence_gate": evidence_gate,
        "evidence": [m["reading"] for m in ev][:3],
        "maturity_threshold": maturity_gate,
        "maturity": mat,
        "passes_both": evidence_gate and maturity_gate,
        "then": "QUEUED FOR HIM — his sheet ends at 'Assign Permanent Node "
                "ID' and whether that happens on its own or waits for his "
                "word is the question he has not answered. The queue holds.",
    }


def queue_for_him(root: str) -> dict:
    rows = load(root)
    queued, promoted = [], 0
    for r in rows:
        if r.get("row") != R_NODE:
            continue
        nid = r["node"]["node_id"]
        st = node_state(root, nid, rows=rows)
        if st["status"] == "ACCEPTED":
            promoted += 1
            continue
        g = gates_of(st)
        if g["passes_both"]:
            queued.append({"node_id": nid,
                           "node_type": r["node"]["node_type"],
                           "gates": g, "support": st["support"]})
    return {
        "queued": queued, "count": len(queued),
        "promoted": promoted,
        "promoted_stays_zero_until": "his word",
        "his_open_question": "does passing the evidence gate and the "
                             "maturity threshold assign a permanent ID on "
                             "its own, or does it queue for you?",
        "current_reading": "the conservative one, pending his answer: the "
                           "queue holds. This is a placeholder for his "
                           "answer, not the answer.",
    }


def approve(root: str, node_id: str) -> dict:
    """HIS action. The original node row is never rewritten — the approval is
    a new row referencing it, and the fold reads status from the approval."""
    rows = load(root)
    st = node_state(root, node_id, rows=rows)
    if not st["found"]:
        raise KeyError("no such node: %s" % node_id)
    row = {"row": R_APPROVAL, "node": node_id, "action": "approve",
           "by": "him", "status_before": st["status"],
           "status_after": "ACCEPTED",
           "references_node_row": node_id}
    _append(root, row)
    remember(root, node_id, "GLOBAL_INDEX",
             "promoted on his word — status %s -> ACCEPTED" % st["status"])
    return {"node": node_id, "status": "ACCEPTED", "by": "him",
            "no_reopen": "the NODE row is untouched; the approval is its own "
                         "row referencing it"}


# ---------------------------------------------------------------------------
# STATS.
# ---------------------------------------------------------------------------

def stats(root: str) -> dict:
    rows = load(root)
    nodes = [r for r in rows if r.get("row") == R_NODE]
    by_type = {}
    for r in nodes:
        t = r["node"]["node_type"]
        by_type[t] = by_type.get(t, 0) + 1
    q = queue_for_him(root)
    return {
        "phase": "D — memory graph + auto-linking",
        "rows": len(rows),
        "nodes": len(nodes),
        "by_type": by_type,
        "links": sum(1 for r in rows if r.get("row") == R_LINK),
        "readings": sum(1 for r in rows if r.get("row") == R_READING),
        "unreadable_kept": sum(1 for r in rows
                               if r.get("row") == "UNREADABLE"),
        "queued_for_him": q["count"],
        "promoted": q["promoted"],
        "write_gate": "his five conditions, enforced at write_node",
        "read_conditions": "his six, one mechanism for recall AND linking",
        "append_only": True,
        "no_reopen": True,
    }


def annotations() -> list:
    return [
        ("his five write conditions, enforced at the write site",
         "nodegraph.write_node"),
        ("his six read conditions — one mechanism, recall and linking",
         "nodegraph.recall"),
        ("an existing match is reinforced, never re-created",
         "nodegraph.write_node"),
        ("hub nodes materialize once — the shape his types exist for",
         "nodegraph._write_hub"),
        ("the per-node chain of readings", "nodegraph.remember"),
        ("the graph is traversable, every hop typed", "nodegraph.path"),
        ("the queue holds until his word", "nodegraph.queue_for_him"),
        ("his approval is a row, never a rewrite", "nodegraph.approve"),
    ]
