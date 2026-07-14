"""The Novelty Pass — find parameters that never existed.

"When some data not fitting in existing parameter it generate the new as per
the item… and keep labeling it." — ARD_RGL_7025 §8, and the Core Specification
§10: gather candidate terms from recent work, match each against the ENTIRE
existing parameter universe, cluster what matches nothing, and emit a fresh
``NOVELTY_<date>.md`` proposing genuinely new parameters.

The discipline that keeps growth honest (the spec's own rule):
  * the pass **proposes, never auto-adds** — every candidate is
    ``NEW-CANDIDATE (awaiting human approval)``;
  * a candidate names its **nearest existing parameter and why it is NOT the
    same**, so near-duplicates die at the gate;
  * once the human approves, the term becomes a real labeled parameter
    (``P-NEW:<term>``): future filings park it, it stops landing unfiled, and
    the pyramid literally grows.

Zero dependencies: similarity via ``difflib``, no embeddings, no model calls.
"""

from __future__ import annotations

import difflib
import json
import os
import re
from typing import Any

from .models import _now
from .parameters import COMPARISON_AXES, PARAMETER_BANK
from .persona import DEFAULT_IN_WORDS, DEFAULT_OUT_WORDS
from .pyramid import STAGE_MAIN, SUB_BUCKETS, _STOP
from .wisdom import SEED_WISDOM

# difflib ratio at/above which a term counts as "already known" / same cluster.
_KNOWN_RATIO = 0.84
_CLUSTER_RATIO = 0.75


def _approved_path(root: str) -> str:
    return os.path.join(root, "approved_parameters.json")


def load_approved(root: str) -> list[dict]:
    p = _approved_path(root)
    if os.path.exists(p):
        try:
            with open(p, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def approved_terms(root: str) -> set[str]:
    return {a["term"] for a in load_approved(root)}


def known_universe(root: str) -> set[str]:
    """Every term the engine already knows as a parameter, bucket, axis, or
    vocabulary item. A candidate is only 'novel' if it matches NONE of these."""
    uni: set[str] = set()
    for p in PARAMETER_BANK:
        uni.update(w.lower() for w in p.name.split())
        uni.add(p.name.lower())
        uni.add(p.group.lower())
    uni.update(a.lower() for a in COMPARISON_AXES)
    for bucket, trigs in SUB_BUCKETS.items():
        uni.add(bucket.lower())
        for t in trigs:
            uni.update(t.lower().split())
    for mains in STAGE_MAIN.values():
        for m in mains:
            uni.update(m.lower().split())
    for w in SEED_WISDOM:
        uni.update(a.lower() for a in w.axes)
        uni.update(w.source.lower().split())
    uni.update(w.lower() for w in DEFAULT_IN_WORDS)
    uni.update(w.lower().split()[0] for w in DEFAULT_OUT_WORDS)
    uni.update(approved_terms(root))
    # hygiene: fragments under 4 chars ("it", "is") would falsely claim
    # any compound that contains them
    return {u for u in uni if len(u) >= 4}


def nearest_known(term: str, universe: set[str]) -> tuple[str, float]:
    """The closest existing parameter/term and its similarity ratio."""
    best, best_r = "", 0.0
    for k in universe:
        r = difflib.SequenceMatcher(None, term, k).ratio()
        if r > best_r:
            best, best_r = k, r
    return best, round(best_r, 3)


def is_known(term: str, universe: set[str]) -> bool:
    """Directional matching. A candidate is known when it *is* an existing term
    (inflection, stem-twin, near-identical) — NOT when it merely *contains* one:
    "chronofield" must stay novel even though "field" exists; a new compound is
    exactly what this pass hunts."""
    t = term.lower().strip()
    if not t or t in universe:
        return True
    stem = t.rstrip("s")                     # versions → version ⊂ inversion
    for k in universe:
        if t in k or stem in k:              # candidate inside a known term
            return True
        if k in t and len(k) >= len(t) - 2:  # known covers nearly all of it
            return True
        # stem twins (hypothesis/hypothetical, general/generated): a long
        # shared root covering most of the shorter word
        p = len(os.path.commonprefix((t, k)))
        if p >= 6 and p / min(len(t), len(k)) >= 0.6:
            return True
        if difflib.SequenceMatcher(None, t, k).ratio() >= _KNOWN_RATIO:
            return True
    return False


def gather_candidates(root: str, memory, unfiled) -> list[dict]:
    """Candidate terms from recent work, each with its sources:
    the unfiled queue (the user's unparked words), P-NEW generator output,
    and significant vocabulary from stored chat questions."""
    cands: dict[str, dict] = {}

    def add(term: str, source: str) -> None:
        t = term.lower().strip()
        if len(t) < 5 or t in _STOP or not re.fullmatch(r"[a-z][a-z0-9_-]{4,32}", t):
            return
        c = cands.setdefault(t, {"term": t, "sources": []})
        if source not in c["sources"]:
            c["sources"].append(source)

    for u in unfiled.list(200):
        add(u.get("item", ""), f"unfiled@{u.get('node', '?')}")
    chat_dir = os.path.join(root, "chats")
    if os.path.isdir(chat_dir):
        for fn in sorted(os.listdir(chat_dir), reverse=True)[:60]:
            if not fn.endswith(".json"):
                continue
            try:
                with open(os.path.join(chat_dir, fn), encoding="utf-8") as f:
                    q = (json.load(f).get("question") or "")
            except Exception:
                continue
            for w in re.findall(r"[a-zA-Z][a-z0-9_-]{4,32}", q.lower()):
                add(w, f"chat:{fn[:-5]}")
    try:
        for e in memory.brain("SB-43").read_all():
            for p in (e.parameters or {}).get("new_parameters", []) or []:
                add(str(p).replace("P-NEW:", ""), "SB-43 generator")
    except Exception:
        pass
    return list(cands.values())


def cluster(novel: list[dict]) -> list[dict]:
    """Group similar novel terms; a cluster's weight = its distinct sources.
    A dense cluster (≥2 sources) is a genuinely new parameter candidate."""
    clusters: list[dict] = []
    for c in sorted(novel, key=lambda x: -len(x["sources"])):
        placed = False
        for cl in clusters:
            if difflib.SequenceMatcher(None, c["term"], cl["term"]).ratio() >= _CLUSTER_RATIO:
                cl["variants"].append(c["term"])
                cl["sources"] = sorted(set(cl["sources"]) | set(c["sources"]))
                placed = True
                break
        if not placed:
            clusters.append({"term": c["term"], "variants": [],
                             "sources": list(c["sources"])})
    for cl in clusters:
        cl["weight"] = len(cl["sources"])
    clusters.sort(key=lambda x: -x["weight"])
    return clusters


def run_novelty_pass(root: str, memory, unfiled) -> dict[str, Any]:
    """The full pass. Returns the candidates and writes NOVELTY_<date>.md."""
    universe = known_universe(root)
    raw = gather_candidates(root, memory, unfiled)
    novel = [c for c in raw if not is_known(c["term"], universe)]
    clusters = cluster(novel)
    # The spec's discipline: a DENSE cluster (2+ independent sources) is a
    # genuinely new parameter; one-off words stay in the unfiled queue instead
    # of flooding the report. Cap the report at the 25 strongest.
    singles = sum(1 for cl in clusters if cl["weight"] < 2)
    clusters = [cl for cl in clusters if cl["weight"] >= 2][:25]
    candidates = []
    for cl in clusters:
        near, ratio = nearest_known(cl["term"], universe)
        candidates.append({
            "term": cl["term"], "variants": cl["variants"],
            "sources": cl["sources"], "weight": cl["weight"],
            "nearest_existing": near, "similarity": ratio,
            "why_not_same": (f"closest existing is '{near}' at {int(ratio * 100)}% — "
                             "below the identity threshold; carries meaning no "
                             "current parameter holds"),
            "proposed_label": f"P-NEW:{cl['term']}",
            "status": "NEW-CANDIDATE (awaiting human approval)",
        })

    at = _now()
    stamp = re.sub(r"[^0-9]", "", at)[:12]
    ndir = os.path.join(root, "novelty")
    os.makedirs(ndir, exist_ok=True)
    fname = f"NOVELTY_{stamp}.md"
    lines = [f"# Novelty Pass — {at}", "",
             f"Scanned {len(raw)} candidate terms from recent chats, the unfiled "
             f"queue, and the SB-43 generator against {len(universe)} known "
             "parameters/buckets/axes.", "",
             f"**Genuinely new candidates: {len(candidates)}** — every one is a "
             "proposal only; nothing is added without your approval.", ""]
    if singles:
        lines += [f"({singles} one-source words stayed in the unfiled queue — a "
                  "parameter must recur across 2+ independent sources to be "
                  "proposed here.)", ""]
    if not candidates:
        lines += ["No parameter beyond the existing universe surfaced this pass. "
                  "Everything recent parked into known categories.", ""]
    for c in candidates:
        lines += [f"## {c['proposed_label']}", "",
                  f"* term: **{c['term']}**"
                  + (f" (variants: {', '.join(c['variants'])})" if c["variants"] else ""),
                  f"* forced by: {', '.join(c['sources'][:6])}",
                  f"* nearest existing parameter: `{c['nearest_existing']}` "
                  f"(similarity {c['similarity']})",
                  f"* why it is NOT the same: {c['why_not_same']}",
                  f"* status: {c['status']}", ""]
    with open(os.path.join(ndir, fname), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    memory.master_log({"event": "novelty_pass", "scanned": len(raw),
                       "candidates": len(candidates), "file": fname})
    b = memory.brain("SB-43", "New Parameter Generator")
    b.bump("Runs_Completed")
    if candidates:
        b.bump("Patterns_Recognized", len(candidates))
    return {"at": at, "file": fname, "scanned": len(raw),
            "universe": len(universe), "singles": singles,
            "candidates": candidates}


def approve(root: str, memory, unfiled, term: str) -> dict[str, Any]:
    """Human approval: the candidate becomes a real labeled parameter. It will
    park in future filings and stops landing in the unfiled queue."""
    term = term.lower().strip()
    approved = load_approved(root)
    if term not in {a["term"] for a in approved}:
        approved.append({"term": term, "label": f"P-NEW:{term}",
                         "approved_at": _now(), "source": "novelty_pass"})
        with open(_approved_path(root), "w", encoding="utf-8") as f:
            json.dump(approved, f, indent=2, ensure_ascii=False)
    # clear it from the human queue wherever it sat
    for u in unfiled.list(500):
        if u.get("item") == term:
            unfiled.park(u.get("node", ""), term)
    b = memory.brain("SB-43", "New Parameter Generator")
    b.bump("Human_Decisions")
    b.bump("Human_Interactions")
    memory.master_log({"event": "novelty_approved", "term": term,
                       "label": f"P-NEW:{term}"})
    return {"ok": True, "term": term, "label": f"P-NEW:{term}",
            "approved_total": len(approved)}


def list_files(root: str) -> list[dict]:
    ndir = os.path.join(root, "novelty")
    if not os.path.isdir(ndir):
        return []
    out = []
    for fn in sorted(os.listdir(ndir), reverse=True):
        if fn.startswith("NOVELTY_") and fn.endswith(".md"):
            out.append({"file": fn,
                        "size": os.path.getsize(os.path.join(ndir, fn))})
    return out[:30]
