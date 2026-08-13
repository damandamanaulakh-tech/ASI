"""PATTERN MEMORY — what survives repetition, and only with his approval.

His canon (docs/method/canon/THE_MACHINE_AS_HE_STATES_IT.md):

    At this point it still should not write:  FACT: A is manipulative.
    It should write something like:  PATTERN-CANDIDATE-017 …

and the pattern emerges from

    DIFFERENCE + RELATIONSHIP + REPETITION / ORDER + CONTEXT + RESULT

and these must NEVER be collapsed into one field:

    WHAT HAPPENED
    WHAT I THINK IT MEANS
    HOW I FELT
    WHAT PRINCIPLE I APPLY
    WHAT DECISION I MADE
    WHAT RESULT FOLLOWED

WHAT THIS MODULE HOLDS TO:
  * **The machine never states intent as fact.** A candidate carries
    `intent_status = "INFERRED / NOT DIRECTLY OBSERVED"` and a list of possible
    interpretations with none chosen, forever, until he writes his own.
  * **His six actions** are all real: approve · reject · rename · split ·
    combine · redefine.
  * **NO REOPEN.** Nothing he has already decided is ever mutated. Every edit
    appends a WRITE-BACK sequence that REFERENCES the prior version, and a new
    version is created. The old reading stays readable forever — which is the
    same rule `seq_kernel` holds for sequences, applied to his corrections.
  * **The threshold is 5, reducing** — his ruling. The reduction rule is stated
    in `surface_at()` and marked as my reading of "reducing" until he rules on
    it; it can never fall below 2, because a pattern from one occurrence is the
    thing he forbade.

Storage, all append-only or versioned, nothing overwritten:
    <root>/micro/micro.jsonl              every micro-sequence ever built
    <root>/patterns/candidates.json       open candidates (versioned in place)
    <root>/patterns/approved.json         his approved patterns, with versions
    <root>/patterns/writeback.jsonl       every edit he ever made, in order
"""
from __future__ import annotations

import json
import os

from . import micro
from .models import _now

# --- his ruling: 5, reducing -----------------------------------------------
SURFACE_START = 5      # his word: "we decided 5 loops and reducing"
SURFACE_FLOOR = 2      # never 1 — one occurrence is not a pattern, his rule
CONF_CAP_INFERRED = 0.75   # one witness (him) → Medium cap, his Source rule

SAVE_AS = ("occurrence only", "personal pattern", "candidate Human rubric",
           "relationship-specific rule", "general pattern")
ACTIONS = ("approve", "reject", "rename", "split", "combine", "redefine")


def _dir(root: str, name: str) -> str:
    d = os.path.join(root, name)
    os.makedirs(d, exist_ok=True)
    return d


def _micro_path(root: str) -> str:
    return os.path.join(_dir(root, "micro"), "micro.jsonl")


def _cand_path(root: str) -> str:
    return os.path.join(_dir(root, "patterns"), "candidates.json")


def _appr_path(root: str) -> str:
    return os.path.join(_dir(root, "patterns"), "approved.json")


def _wb_path(root: str) -> str:
    return os.path.join(_dir(root, "patterns"), "writeback.jsonl")


def _read_json(path: str, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _write_json(path: str, obj) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# MICRO-SEQUENCE MEMORY — append only. Nothing is ever rewritten or removed.
def store_micro(root: str, seqs: list[dict]) -> int:
    """Keep every micro-sequence. This is the memory repetition is found in."""
    if not seqs:
        return 0
    have = {m["id"] for m in load_micro(root)}
    n = 0
    with open(_micro_path(root), "a", encoding="utf-8") as f:
        for s in seqs:
            if s.get("id") in have:      # the same sentence in the same ask
                continue
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
            n += 1
    return n


def load_micro(root: str, limit: int = 0) -> list[dict]:
    p = _micro_path(root)
    if not os.path.exists(p):
        return []
    out = []
    try:
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:
                    continue          # one bad line never hides the rest
    except Exception:
        return out
    return out[-limit:] if limit else out


def count_micro(root: str) -> int:
    return len(load_micro(root))


# ---------------------------------------------------------------------------
# THE THRESHOLD — 5, reducing
def surface_at(root: str) -> int:
    """How many repeats before a candidate surfaces.

    His ruling: 5, reducing. READING OF "REDUCING" (mine, until he rules):
    every pattern he has already approved buys one off the count, because the
    machine has learned what he counts as a pattern — so the sixth pattern
    needs fewer repeats than the first. It never goes below 2, because a
    pattern from a single occurrence is exactly the false-pattern explosion he
    named."""
    approved = len(load_approved(root))
    return max(SURFACE_FLOOR, SURFACE_START - approved)


def threshold_reading(root: str) -> dict:
    a = len(load_approved(root))
    return {"start": SURFACE_START, "floor": SURFACE_FLOOR,
            "approved_patterns": a, "surface_at": surface_at(root),
            "his_ruling": "we decided 5 loops and reducing",
            "reduction_rule": "each approved pattern buys one off the count; "
                              "never below " + str(SURFACE_FLOOR),
            "status": "REDUCTION RULE IS MY READING — awaiting his word"}


# ---------------------------------------------------------------------------
# REPETITION / DIFFERENCE / RELATION DETECTION
def group_repeats(root: str, seqs: list[dict] | None = None,
                  min_facts: int = 1) -> list[dict]:
    """Find every ARRANGEMENT that recurs across SEPARATE asks.

    NOT by an identical fact set — his own worked example proves that wrong.
    His S2 ("used my car and left another person with me") carries no
    disclosure fact at all, and his S3 ("again did not explain the full plan")
    carries no resource fact. Yet both are steps of ONE arrangement:

        A needs resource/help from B
            ↓ A reveals only partial plan
            ↓ B becomes committed before full context is known
            ↓ additional burden/context appears later
            ↓ A obtains desired result

    So the arrangement is the **union of steps across LINKED events**, and each
    step carries its own support count. Requiring every fact in every event
    would have thrown away most of his example; requiring only one shared fact
    would have merged everything into one blob.

    The link test is `micro.relates()`: two or more shared facts, at least one
    of them relational. Events are then joined into connected components — the
    same single-linkage his own reading uses when he says "S4 and S5 show
    similar structural behavior".

    Separate asks matter: five sentences in one paragraph is one telling, not
    five events. An arrangement counts once per ask, never once per sentence.
    """
    all_ms = load_micro(root) if seqs is None else seqs
    rows = [m for m in all_ms
            if len(set(m.get("structural_facts", [])) & micro.CORE_RELATION_FACTS)
            >= min_facts]
    if not rows:
        return []

    # --- single-linkage components over the relates() test ------------------
    parent = list(range(len(rows)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        a, b = find(i), find(j)
        if a != b:
            parent[b] = a

    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            if micro.relates(rows[i], rows[j])["repeat"]:
                union(i, j)

    comps: dict[int, list[dict]] = {}
    for i, m in enumerate(rows):
        comps.setdefault(find(i), []).append(m)

    groups = []
    for members in comps.values():
        asks: list[str] = []
        for m in members:
            a = m.get("ask") or m.get("id")
            if a not in asks:
                asks.append(a)
        # the union of steps, each with the asks that showed it
        step_support: dict[str, list[str]] = {}
        for m in members:
            a = m.get("ask") or m.get("id")
            for f in set(m.get("structural_facts", [])) & micro.CORE_RELATION_FACTS:
                if a not in step_support.setdefault(f, []):
                    step_support[f].append(a)
        union_facts = sorted(step_support)
        # the tight core: the steps EVERY event in the arrangement shows
        tight = sorted(set.intersection(*[
            set(m.get("structural_facts", [])) & micro.CORE_RELATION_FACTS
            for m in members])) if members else []
        groups.append({
            "signature": "|".join(union_facts),
            "core_facts": union_facts,
            "tight_core": tight,
            "step_support": {f: len(v) for f, v in step_support.items()},
            "step_asks": step_support,
            "members": [m["id"] for m in members],
            "asks": asks,
            "occurrences": len(members),
            "distinct_asks": len(asks),
            "examples": [m["raw"] for m in members[:5]],
            "contribution": members[0].get("pattern_contribution", ""),
        })
    groups.sort(key=lambda g: (-g["distinct_asks"], -g["occurrences"],
                               g["signature"]))
    return groups


def _observed_pattern_with_support(group: dict) -> str:
    """His arrangement, written as steps, each carrying how many asks showed
    it. A step seen once is not hidden behind a step seen five times."""
    sup = group.get("step_support", {})
    n = max(1, group.get("distinct_asks", 1))
    lines = []
    for f in _STEP_ORDER:
        if f in group.get("core_facts", []):
            s = sup.get(f, 0)
            lines.append(f"{_STEP_TEXT[f]}   [seen in {s} of {n} asks]")
    if not lines:
        return "recurring arrangement: " + ", ".join(group.get("core_facts", []))
    return "\n        ↓\n".join(lines)


# the arrangement's steps, in the order his own reading puts them
_STEP_TEXT = {
    micro.F_RESOURCE_REQUESTED: "A needs a resource or help from B",
    micro.F_DISCLOSURE_WITHHELD: "A reveals only part of the plan",
    micro.F_ASYMMETRY_INFO: "A knows more than B throughout",
    micro.F_PARTICIPATION_BEFORE:
        "B becomes committed before the full context is known",
    micro.F_AGREEMENT_ABSENT: "no prior agreement covers it",
    micro.F_THIRD_PARTY: "an additional person or burden appears later",
    micro.F_RESOURCE_USED: "B's resource is used",
    micro.F_EXPECTATION_BROKEN: "what was expected does not happen",
    micro.F_BENEFIT_OTHER: "A obtains the desired result",
}
_STEP_ORDER = [micro.F_RESOURCE_REQUESTED, micro.F_DISCLOSURE_WITHHELD,
               micro.F_ASYMMETRY_INFO, micro.F_PARTICIPATION_BEFORE,
               micro.F_AGREEMENT_ABSENT, micro.F_THIRD_PARTY,
               micro.F_RESOURCE_USED, micro.F_EXPECTATION_BROKEN,
               micro.F_BENEFIT_OTHER]


def _observed_pattern(core_facts: list[str]) -> str:
    """The arrangement in words — the structure, not a verdict about anyone."""
    steps = [_STEP_TEXT[f] for f in _STEP_ORDER if f in core_facts]
    return "\n        ↓\n".join(steps) if steps else \
        "recurring arrangement: " + ", ".join(core_facts)


def _confidence(group: dict, at: int, his_word: bool) -> dict:
    """A real number with a stated formula — no placeholder.

    support   = distinct asks against the threshold (capped at 1)
    tightness = how many of the arrangement's facts every member shares
    conf      = (support + tightness) / 2
    cap       = Medium (0.75) while intent is INFERRED and he has not spoken —
                the evidence is one witness (him), and his Source rule caps a
                one-witness claim at Medium.
    """
    at = max(1, at)
    support = min(1.0, group["distinct_asks"] / float(at))
    n_core = len(group["core_facts"])
    tightness = min(1.0, n_core / 4.0)     # 4+ shared relational facts = tight
    raw = (support + tightness) / 2.0
    # nothing in this system ever reads 1.00. His approval is authority, not
    # certainty — the Doubt engine exists to bite exactly this overclaim.
    capped = min(raw, 0.95) if his_word else min(raw, CONF_CAP_INFERRED)
    return {"value": round(capped, 2), "uncapped": round(raw, 2),
            "basis": "his ruling — not a machine estimate" if his_word
                     else "machine estimate over repetition",
            "support": round(support, 2), "tightness": round(tightness, 2),
            "formula": "(support + tightness) / 2; support = distinct asks / "
                       "surface_at; tightness = shared relational facts / 4",
            "cap": None if his_word else CONF_CAP_INFERRED,
            "cap_reason": None if his_word else
                          "intent is INFERRED and the evidence is one witness "
                          "(him) — his Source rule caps that at Medium"}


def _interps_for(root: str, group: dict) -> list[str]:
    """Every reading the structure allows, none chosen. Pulled from the member
    micro-sequences so the list is what the events actually opened."""
    out: list[str] = []
    members = {m["id"]: m for m in load_micro(root)}
    for mid in group["members"]:
        for i in (members.get(mid, {}) or {}).get("possible_interpretations", []):
            if i not in out:
                out.append(i)
    if not out:
        for f in group["core_facts"]:
            for i in micro.INTERPRETATIONS_BY_FACT.get(f, []):
                if i not in out:
                    out.append(i)
        if out:
            out.append("other / unknown")
    return out


def _effects_for(root: str, group: dict) -> list[str]:
    out: list[str] = []
    members = {m["id"]: m for m in load_micro(root)}
    for mid in group["members"]:
        for e in (members.get(mid, {}) or {}).get("possible_human_effect", []):
            if e not in out:
                out.append(e)
    return out


def _next_cand_id(cands: list[dict]) -> str:
    n = 0
    for c in cands:
        try:
            n = max(n, int(str(c.get("id", "")).rsplit("-", 1)[-1]))
        except Exception:
            continue
    return f"PATTERN-CANDIDATE-{n + 1:03d}"


def refresh_candidates(root: str) -> dict:
    """Surface every arrangement that has now reached the threshold, and keep
    the evidence on the ones already open growing.

    A candidate is never removed and never rewritten in a way that loses what
    it said: evidence only grows, and every field he has touched is left
    exactly as he left it."""
    cands = load_candidates(root)
    by_sig = {c["signature"]: c for c in cands}
    at = surface_at(root)
    groups = group_repeats(root)
    created, grew = [], []
    for g in groups:
        cur = by_sig.get(g["signature"])
        if cur is None:
            if g["distinct_asks"] < at:
                continue                     # below threshold — stays silent
            c = {
                "id": _next_cand_id(cands),
                "signature": g["signature"],
                "core_facts": g["core_facts"],
                "tight_core": g.get("tight_core", []),
                "step_support": g.get("step_support", {}),
                # ---- HIS FIELD NAMES, exactly ----------------------------
                "observed_pattern": _observed_pattern_with_support(g),
                "evidence": list(g["members"]),
                "evidence_asks": list(g["asks"]),
                "evidence_examples": list(g["examples"]),
                "repetition_count": g["distinct_asks"],
                "possible_interpretations": _interps_for(root, g),
                "possible_human_effect": _effects_for(root, g),
                "intent_status": "INFERRED / NOT DIRECTLY OBSERVED",
                "confidence": _confidence(g, at, False),
                # ---- THE SIX THAT NEVER COLLAPSE -------------------------
                "what_happened": _observed_pattern_with_support(g),
                "his_interpretation": "",
                "his_feeling": "",
                "his_principle": "",
                "his_decision": "",
                "his_result": "",
                # ---- lifecycle -------------------------------------------
                "save_as": "",
                "status": "candidate",
                "surfaced_at_threshold": at,
                "version": 1,
                "created": _now(),
                "history": [],
            }
            c["rfr"] = rfr_check(c)
            cands.append(c)
            by_sig[c["signature"]] = c
            created.append(c["id"])
        else:
            if len(g["members"]) > len(cur.get("evidence", [])):
                cur["evidence"] = list(g["members"])
                cur["evidence_asks"] = list(g["asks"])
                cur["evidence_examples"] = list(g["examples"])
                cur["repetition_count"] = g["distinct_asks"]
                cur["step_support"] = g.get("step_support", {})
                cur["tight_core"] = g.get("tight_core", [])
                cur["observed_pattern"] = _observed_pattern_with_support(g)
                cur["what_happened"] = cur["observed_pattern"]
                cur["possible_interpretations"] = _interps_for(root, g)
                cur["possible_human_effect"] = _effects_for(root, g)
                cur["confidence"] = _confidence(
                    g, at, bool(cur.get("his_interpretation")))
                cur["rfr"] = rfr_check(cur)
                grew.append(cur["id"])
    _write_json(_cand_path(root), cands)
    return {"created": created, "grew": grew, "surface_at": at,
            "open": sum(1 for c in cands if c["status"] == "candidate"),
            "below_threshold": [{"signature": g["signature"],
                                 "distinct_asks": g["distinct_asks"],
                                 "needs": at}
                                for g in groups
                                if g["signature"] not in by_sig]}


def rfr_check(cand: dict) -> dict:
    """R-F-R / DOUBT — his flow puts this between PATTERN CANDIDATE and
    YOU APPROVE, so a candidate never reaches him unexamined.

    R-F-R is the Mahabharata Sequence: reverse → forward → reverse. Applied to
    a candidate arrangement that is exactly:

      REVERSE  from the result back: does every step have support, or is the
               arrangement leaning on a step seen once?
      FORWARD  from the first step on: does the order hold, or is a later step
               doing the work of an earlier one?
      REVERSE  again: with the weak steps removed, does the arrangement still
               stand — and if not, what is the smallest true version?

    Then the Doubt engine bites the strongest reading. Nothing here rejects a
    candidate. It marks what is thin, so his approval is informed."""
    from .doubt import doubt_engine
    sup = cand.get("step_support", {}) or {}
    n = max(1, cand.get("repetition_count", 1))
    facts = cand.get("core_facts", []) or []

    thin = sorted(f for f in facts if sup.get(f, 0) <= 1)
    strong = sorted(f for f in facts if sup.get(f, 0) >= max(2, n // 2))
    reverse_1 = {
        "pass": "reverse — from the result back",
        "asks": "does every step have support?",
        "thin_steps": thin,
        "verdict": ("every step recurs" if not thin
                    else f"{len(thin)} step(s) rest on a single ask")}
    forward = {
        "pass": "forward — from the first step on",
        "asks": "does the order hold?",
        "ordered": [f for f in _STEP_ORDER if f in facts],
        "verdict": ("the arrangement runs in order"
                    if len([f for f in _STEP_ORDER if f in facts]) >= 2
                    else "too few steps to carry an order")}
    smallest = strong or [f for f in facts if sup.get(f, 0) >= 2]
    reverse_2 = {
        "pass": "reverse — again, with the thin steps set aside",
        "asks": "does it still stand?",
        "smallest_true_version": smallest,
        "verdict": ("it still stands on " + str(len(smallest)) + " step(s)"
                    if len(smallest) >= 2 else
                    "WITHOUT the thin steps this is not yet an arrangement")}
    d = doubt_engine(cand.get("observed_pattern", ""), False, n)
    return {"r_f_r": [reverse_1, forward, reverse_2],
            "doubt": {"bites": d.get("bites"),
                      "fragilities": d.get("fragilities", [])[:6]},
            "stands": len(smallest) >= 2,
            "note": "nothing was rejected — this marks what is thin so his "
                    "approval is informed. R-F-R is the METHOD every reading "
                    "passes through, never a sequence run on its own."}


def load_candidates(root: str) -> list[dict]:
    return _read_json(_cand_path(root), [])


def load_approved(root: str) -> list[dict]:
    return _read_json(_appr_path(root), [])


def writebacks(root: str, limit: int = 200) -> list[dict]:
    p = _wb_path(root)
    if not os.path.exists(p):
        return []
    out = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except Exception:
                    continue
    return out[-limit:]


def _append_writeback(root: str, wb: dict) -> None:
    with open(_wb_path(root), "a", encoding="utf-8") as f:
        f.write(json.dumps(wb, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# HIS REVIEW — six actions, and NO REOPEN.
def review(root: str, cand_id: str, action: str, fields: dict | None = None,
           note: str = "") -> dict:
    """He edits / rejects / renames / splits / combines / redefines / approves.

    NO REOPEN: the prior reading is never mutated. Every action appends a
    write-back sequence that REFERENCES the version it acted on, and a new
    version is written. `history` on the record keeps every prior version in
    full, so the old interpretation stays readable forever."""
    action = (action or "").strip().lower()
    if action not in ACTIONS:
        return {"error": "unknown action; his six are: " + ", ".join(ACTIONS)}
    fields = fields or {}
    cands = load_candidates(root)
    idx = next((i for i, c in enumerate(cands) if c["id"] == cand_id), None)
    if idx is None:
        return {"error": "no such candidate: " + str(cand_id)}
    cur = cands[idx]

    prior = {k: v for k, v in cur.items() if k != "history"}   # frozen copy
    new = dict(cur)
    new["history"] = list(cur.get("history", [])) + [
        {"version": cur.get("version", 1), "at": _now(),
         "action_that_closed_it": action, "snapshot": prior}]
    new["version"] = int(cur.get("version", 1)) + 1
    new["reviewed_at"] = _now()

    # his six fields are only ever set by him, and only where he wrote
    for k in ("his_interpretation", "his_feeling", "his_principle",
              "his_decision", "his_result", "user_interpretation",
              "user_decision"):
        if k in fields and str(fields[k]).strip():
            new[k] = str(fields[k]).strip()
    if fields.get("save_as") in SAVE_AS:
        new["save_as"] = fields["save_as"]
    if str(fields.get("name", "")).strip():
        new["name"] = str(fields["name"]).strip()

    spawned: list[str] = []
    if action == "approve":
        new["status"] = "approved"
        # his word is the authority — the Medium cap lifts because the witness
        # is no longer only an inference
        g = {"distinct_asks": new.get("repetition_count", 0),
             "core_facts": new.get("core_facts", [])}
        new["confidence"] = _confidence(g, new.get("surfaced_at_threshold", 5),
                                        True)
        new["intent_status"] = (
            "HIS RULING — " + new.get("his_interpretation", "").strip()
            if new.get("his_interpretation")
            else "APPROVED AS STRUCTURE — intent still not observed")
        appr = load_approved(root)
        appr.append({k: v for k, v in new.items() if k != "history"})
        _write_json(_appr_path(root), appr)
    elif action == "reject":
        new["status"] = "rejected"
        new["reject_note"] = str(note or "")[:400]
    elif action == "rename":
        new["status"] = cur.get("status", "candidate")
    elif action == "redefine":
        if str(fields.get("observed_pattern", "")).strip():
            new["observed_pattern"] = str(fields["observed_pattern"]).strip()
        new["status"] = cur.get("status", "candidate")
    elif action == "split":
        # a split does NOT delete the parent — it spawns children that
        # reference it, exactly like a spawn contract in the sequence protocol
        parts = [p for p in (fields.get("into") or []) if str(p).strip()]
        if len(parts) < 2:
            return {"error": "a split needs at least two names in `into`"}
        new["status"] = "split"
        base = load_candidates(root)
        for p in parts:
            child = dict(new)
            child.pop("history", None)
            child["id"] = _next_cand_id(base + cands)
            child["name"] = str(p).strip()
            child["status"] = "candidate"
            child["version"] = 1
            child["history"] = []
            child["split_from"] = cur["id"]
            child["created"] = _now()
            cands.append(child)
            base.append(child)
            spawned.append(child["id"])
    elif action == "combine":
        others = [str(x) for x in (fields.get("with") or []) if str(x).strip()]
        if not others:
            return {"error": "a combine needs at least one id in `with`"}
        ev = list(new.get("evidence", []))
        asks = list(new.get("evidence_asks", []))
        for c in cands:
            if c["id"] in others:
                ev += [e for e in c.get("evidence", []) if e not in ev]
                asks += [a for a in c.get("evidence_asks", []) if a not in asks]
                # the absorbed one is CLOSED, not deleted, and it says where
                # it went — no reopen
                c["history"] = list(c.get("history", [])) + [
                    {"version": c.get("version", 1), "at": _now(),
                     "action_that_closed_it": "combined into " + cur["id"],
                     "snapshot": {k: v for k, v in c.items() if k != "history"}}]
                c["version"] = int(c.get("version", 1)) + 1
                c["status"] = "combined"
                c["combined_into"] = cur["id"]
        new["evidence"], new["evidence_asks"] = ev, asks
        new["repetition_count"] = len(asks)
        new["combined_with"] = others
        new["status"] = cur.get("status", "candidate")

    cands[idx] = new
    _write_json(_cand_path(root), cands)

    wb = {"at": _now(), "event": "writeback", "action": action,
          "candidate": cand_id, "acted_on_version": cur.get("version", 1),
          "new_version": new["version"], "spawned": spawned,
          "fields_he_set": sorted(k for k in fields if str(fields[k]).strip()),
          "note": str(note or "")[:400],
          "no_reopen": "the prior version is kept in full in history and is "
                       "never rewritten; this is a new sequence referencing it"}
    _append_writeback(root, wb)
    return {"ok": True, "candidate": new, "writeback": wb, "spawned": spawned}


# ---------------------------------------------------------------------------
# ACTIVATION — an approved pattern reads a future sentence
def activate(root: str, seqs: list[dict]) -> list[dict]:
    """What his approved patterns say about THIS ask, and what each new
    micro-sequence does to them: activate · contribute · contradict · modify
    confidence · or open a candidate. His five outcomes, named."""
    appr = load_approved(root)
    if not appr:
        return []
    out = []
    for p in appr:
        pf = set(p.get("core_facts", []))
        for m in seqs:
            mf = set(m.get("structural_facts", []))
            shared = sorted(pf & mf)
            core = sorted(set(shared) & micro.CORE_RELATION_FACTS)
            if not core:
                continue
            missing = sorted(pf - mf)
            if len(core) == len(pf):
                outcome, why = "activate", "every fact of the pattern is here"
            elif len(core) >= 2:
                outcome, why = ("contribute evidence",
                                "part of the arrangement recurs: " +
                                ", ".join(core))
            else:
                outcome, why = ("modify confidence",
                                "one fact only — too thin to be the pattern")
            if missing and outcome == "activate":
                outcome, why = "contribute evidence", "missing: " + ", ".join(missing)
            out.append({"pattern": p.get("id"),
                        "name": p.get("name", "") or p.get("id"),
                        "his_interpretation": p.get("his_interpretation", ""),
                        "his_principle": p.get("his_principle", ""),
                        "micro": m["id"], "sentence": m["raw"],
                        "shared": shared, "core_shared": core,
                        "missing_from_pattern": missing,
                        "outcome": outcome, "why": why,
                        "version": p.get("version")})
    return out


def contradictions(root: str, seqs: list[dict]) -> list[dict]:
    """Where a new event runs AGAINST an approved pattern — the outcome he
    named that most systems never implement. A pattern that cannot be
    contradicted is a belief, not a reading."""
    appr = load_approved(root)
    out = []
    for p in appr:
        pf = set(p.get("core_facts", []))
        opposite = set()
        if micro.F_DISCLOSURE_WITHHELD in pf:
            opposite.add(micro.F_DISCLOSURE_GIVEN)
        for m in seqs:
            mf = set(m.get("structural_facts", []))
            hit = sorted(opposite & mf)
            if hit and (pf & mf):
                out.append({"pattern": p.get("id"),
                            "name": p.get("name", "") or p.get("id"),
                            "micro": m["id"], "sentence": m["raw"],
                            "against": hit,
                            "why": "the same relation, with the pattern's key "
                                   "fact reversed — this weakens it and it is "
                                   "recorded, not discarded"})
    return out


def stats(root: str) -> dict:
    cands = load_candidates(root)
    return {"micro_sequences": count_micro(root),
            "candidates_open": sum(1 for c in cands if c["status"] == "candidate"),
            "candidates_total": len(cands),
            "approved": len(load_approved(root)),
            "rejected": sum(1 for c in cands if c["status"] == "rejected"),
            "writebacks": len(writebacks(root, limit=10 ** 6)),
            "threshold": threshold_reading(root)}
