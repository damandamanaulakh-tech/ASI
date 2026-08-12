"""THE LADDER REGISTRY + ACTIVATION — real wiring for the engine page.

His orders, verbatim:
  "yes build it into the app, real wiring"
  "when i expand each parameter must be visible under that so i can select
   that too"

What is REAL here and what is not, on the record:
  - The frame is real: 1 system · 10 segments · 200 containers · 3,072
    parameter slots (his lock, Phase-1).
  - The seed registry fills only what the repo verifiably knows: the 18
    cross-segment mechanism containers (1 parameter each — the parameter IS
    the mechanism) and CON-042 Core Reasoning's size (48). Everything else
    is an UNFILLED slot that says so, and fills from his workbook upload —
    never from invention.
  - Activation is real matching: token overlap between his question (plus
    the engine's own answer text) and the filled entries' names/contents.
    The seven gate mechanisms are always lit — they run on every answer.
  - Adoption is real: deselecting or force-selecting parameters changes the
    recall notes fed into the actual engine run, and the engine runs again.

Storage:  <SB_ROOT>/ladder/registry.json          (current)
          <SB_ROOT>/ladder/versions/vNNNN.json    (every upload, forever)
"""
from __future__ import annotations

import json
import os
import re

from .models import _now

SEGMENTS = [
    ("S1", "Reasoning, Planning, Decision and Creativity", 347),
    ("S2", "Consciousness, Self and Social Intelligence", 320),
    ("S3", "Emotion, Motivation, Intent and Motive", 316),
    ("S4", "Learning, Memory and Knowledge", 312),
    ("S5", "Attention and Executive Control", 308),
    ("S6", "Development, Metacognition and Adaptation", 300),
    ("S7", "Language and Communication", 296),
    ("S8", "Biological Regulation and Internal State", 291),
    ("S9", "Perception and Body Representation", 288),
    ("S10", "Sensorimotor Action and Physical Execution", 276),
]
# the 18 named cross-segment mechanisms — real, from his workbook's own
# catalog; each holds exactly 1 parameter, and the parameter is the mechanism.
CROSS = [
    ("X-01", "Chaos Threshold and High-Variance Nodes"),
    ("X-02", "Human-AI Divergence Under Extreme Stakes"),
    ("X-03", "Multi-Engine Interference and Fusion"),
    ("X-04", "Graph Connectivity and Edge Density Potential"),
    ("X-05", "Proof Debt and Evidence Ledger Dynamics"),
    ("X-06", "Synthetic Fuel Injection and Reality Anchor"),
    ("X-07", "Stall Diagnostic and Critical Logic Wall"),
    ("X-08", "Tiered Execution and Cost-of-Delay"),
    ("X-09", "External Checkpoint and Cross-Model Audit"),
    ("X-10", "Parameter Migration and Cross-Segment Flow"),
    ("X-11", "Negative Space and Absence Mapping"),
    ("X-12", "Benchmark-Harness Provenance"),
    ("X-13", "Uncertainty Calibration and Expression"),
    ("X-14", "Claim-Evidence Binding"),
    ("X-15", "Source-Conflict Preservation"),
    ("X-16", "Evaluation-Awareness Monitoring"),
    ("X-17", "Reasoning-Output Discrepancy"),
    ("X-18", "Tool-Hallucination Detection"),
]
# gates: the mechanisms the seven filters already live in (01D mapping).
GATES = {"X-14": "Fact — no untagged claim leaves",
         "X-15": "Mask — disagreement preserved, never averaged",
         "X-11": "Mask — what a source chose not to show",
         "X-05": "proof-debt — the halt is named",
         "X-09": "Source — the second, independent witness",
         "X-13": "calibrated confidence — never inflated",
         "X-07": "Halt — where does this fail"}

TOTAL_PARAMS = 3072
TOTAL_CONTAINERS = 200


def _dir(root: str) -> str:
    d = os.path.join(root, "ladder")
    os.makedirs(os.path.join(d, "versions"), exist_ok=True)
    return d


def seed_registry() -> dict:
    """Only what the repo verifiably knows. Unfilled slots say so."""
    containers = [{"id": "CON-042", "name": "Core Reasoning", "segment": "S1",
                   "target": 48, "filled": True}]
    for cid, name in CROSS:
        containers.append({"id": cid, "name": name, "segment": "CROSS",
                           "target": 1, "filled": True})
    named = {c["id"] for c in containers}
    slots_needed = TOTAL_CONTAINERS - len(containers)
    n = 0
    for i in range(1, TOTAL_CONTAINERS + 1):
        cid = f"CON-{i:03d}"
        if cid in named or n >= slots_needed:
            continue
        containers.append({"id": cid, "name": "", "segment": "",
                           "target": None, "filled": False})
        n += 1
    params = [{"id": f"P-{cid}", "name": name, "container": cid,
               "contains": ("cross-segment mechanism — " + name +
                            (". Gate: " + GATES[cid] if cid in GATES else "")),
               "filled": True}
              for cid, name in CROSS]
    return {"version": 0, "saved_at": _now(),
            "note": "seed — only what the repo verifiably knows",
            "system": "ASI",
            "segments": [{"id": s, "name": n, "target": t}
                         for s, n, t in SEGMENTS],
            "containers": containers,
            "parameters": params,
            "totals": {"segments": len(SEGMENTS),
                       "containers": TOTAL_CONTAINERS,
                       "parameters": TOTAL_PARAMS,
                       "parameters_filled": len(params)}}


def load_registry(root: str) -> dict:
    fp = os.path.join(_dir(root), "registry.json")
    if not os.path.exists(fp):
        return seed_registry()
    with open(fp, encoding="utf-8") as f:
        return json.load(f)


def save_registry(root: str, incoming: dict, note: str = "") -> dict:
    """Merge an upload into the registry by id — nothing removed, every
    version kept. This is where his workbook's 3,072 land (Phase-2a)."""
    cur = load_registry(root)
    for key in ("segments", "containers", "parameters"):
        have = {x["id"]: x for x in cur.get(key, [])}
        for x in incoming.get(key, []) or []:
            if not isinstance(x, dict) or not x.get("id"):
                continue
            row = have.get(x["id"], {})
            row.update({k: v for k, v in x.items() if v not in (None, "")})
            row["filled"] = bool(row.get("name"))
            have[x["id"]] = row
        cur[key] = list(have.values())
    cur["version"] = int(cur.get("version", 0)) + 1
    cur["saved_at"] = _now()
    cur["note"] = str(note or "")[:200]
    cur["totals"] = {"segments": len(cur["segments"]),
                     "containers": max(TOTAL_CONTAINERS, len(cur["containers"])),
                     "parameters": max(TOTAL_PARAMS, len(cur["parameters"])),
                     "parameters_filled":
                         sum(1 for p in cur["parameters"] if p.get("filled"))}
    d = _dir(root)
    with open(os.path.join(d, "versions", f"v{cur['version']:04d}.json"),
              "w", encoding="utf-8") as f:
        json.dump(cur, f, ensure_ascii=False)
    with open(os.path.join(d, "registry.json"), "w", encoding="utf-8") as f:
        json.dump(cur, f, ensure_ascii=False)
    return cur


def _tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]{4,}", (text or "").lower())}


def activate(question: str, registry: dict, extra_text: str = "") -> dict:
    """Real matching: which filled entries the question (plus the engine's
    own words) actually touches. Gates are always lit — they run on every
    answer. Every hit carries the tokens that caused it."""
    q = _tokens(question) | _tokens(extra_text)
    lit_params = []
    for p in registry.get("parameters", []):
        if not p.get("filled"):
            continue
        cid = p.get("container", "")
        if cid in GATES:
            lit_params.append({**p, "reason": "gate — " + GATES[cid],
                               "matched": []})
            continue
        hit = sorted(q & _tokens(p.get("name", "") + " " +
                                 p.get("contains", "")))
        if hit:
            lit_params.append({**p, "matched": hit,
                               "reason": "matched his words: " +
                                         ", ".join(hit[:6])})
    lit_cids = {p["container"] for p in lit_params}
    lit_cons = []
    for c in registry.get("containers", []):
        if c["id"] in lit_cids:
            lit_cons.append({**c, "reason": "its parameters fired"})
        elif c.get("filled") and (q & _tokens(c.get("name", ""))):
            lit_cons.append({**c, "reason": "name matched his words"})
    lit_sids = {c.get("segment") for c in lit_cons if c.get("segment")
                and c.get("segment") != "CROSS"}
    lit_segs = [{"id": s, "name": n, "target": t,
                 "reason": "its containers fired"}
                for s, n, t in SEGMENTS if s in lit_sids]
    return {"segments": lit_segs, "containers": lit_cons,
            "parameters": lit_params}


def _uniq(seq) -> list:
    """Order-preserving de-dup — his sequence is never re-sorted away."""
    seen, out = set(), []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def recall_notes(registry: dict, lit: dict, select: list[str],
                 deselect: list[str], limit: int = 40) -> tuple[str, dict]:
    """The context the real engine run receives: contents of (his forced
    selects + lit) minus his deselects. This is the adoption mechanism —
    change the hand, change the run.

    Forced picks are placed FIRST so that if the list is capped, a
    parameter he deliberately forced in is never the one silently dropped.
    The returned `hand` preserves his order, never a re-sort."""
    by_id = {p["id"]: p for p in registry.get("parameters", [])}
    des = set(deselect or [])
    chosen: dict[str, dict] = {}
    for pid in select or []:               # forced first — never truncated away
        p = by_id.get(pid)
        if p and p.get("filled") and pid not in des:
            chosen[pid] = {**p, "reason": "forced in by his hand"}
    for p in lit.get("parameters", []):    # then whatever the question lit
        if p["id"] in des:
            continue
        chosen.setdefault(p["id"], p)
    speaking = list(chosen.values())[:limit]
    kept = {p["id"] for p in speaking}
    notes = "\n".join(f"- {p['id']} {p.get('name','')}: {p.get('contains','')}"
                      for p in speaking)
    return notes, {"speaking": speaking,
                   "deselected": _uniq(deselect or []),
                   "forced": _uniq(x for x in (select or []) if x in kept),
                   "dropped_by_cap": _uniq(x for x in (select or [])
                                           if x in chosen and x not in kept)}
