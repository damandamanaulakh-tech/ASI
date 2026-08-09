"""ASI NODE REGISTRY — bookkeeping only. The thinking is not in here.

The owner's stopping rule for this whole run:

    "once u see, with 18-20 example, from my data only stopped making new ID
     number then u start the P-11"

So "new ID number" has to be a hard count, not a feeling. This file does the
counting and nothing else: append a node, refuse a duplicate, report the curve.
Every node's CONTENT is written by hand — what merges, which human parameter,
which AI capability, which of the 8 steps it stands on. The script never
invents a node; it only stamps the next number and remembers what was already
there, so the saturation curve is a measurement instead of an opinion.

An ASI node is his definition, not mine:
    "at human when we added AI, it become one node, and at each we put brain,
     and it let everything next response with that and generate new things"

so: HUMAN side + AI side -> ONE node, carrying a brain, and every later example
runs through the nodes that already exist before it is allowed to mint new ones.
"""

from __future__ import annotations

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.join(HERE, "asi_nodes.json")

RELATIONSHIPS = ("DIRECT CLONE", "FUNCTIONAL ANALOGUE",
                 "STRUCTURAL ANALOGUE", "NO MATCH")

# his universal 8 — every node stands on exactly one of them
STEPS = ("GROUND", "PRESSURE", "USE", "WITNESS",
         "EXPRESSION", "NAMING", "HALT", "LOOP")


def load() -> dict:
    if not os.path.exists(STORE):
        return {"nodes": [], "runs": []}
    with open(STORE) as fh:
        return json.load(fh)


def save(db: dict) -> None:
    with open(STORE, "w") as fh:
        json.dump(db, fh, indent=1, ensure_ascii=False)


def _key(what: str) -> str:
    """Duplicate detection. Two nodes are the same node when the thing they
    name is the same thing — punctuation and case are not evidence."""
    return re.sub(r"[^a-z0-9 ]", "", what.lower()).strip()


def next_id(db: dict) -> str:
    n = len(db["nodes"]) + 1
    return f"ASI-{n:04d}"


def add(db: dict, *, what: str, step: str, human: str, ai: str,
        relationship: str, brain: str, born: str, note: str = "") -> tuple[str, bool]:
    """Returns (id, is_new). An existing node is returned unchanged — that is
    the whole point: a node that already covers the case is NOT a new ID, and
    those are the runs that make the curve flatten."""
    assert step in STEPS, f"unknown step {step}"
    assert relationship in RELATIONSHIPS, f"unknown relationship {relationship}"
    k = _key(what)
    for node in db["nodes"]:
        if _key(node["what"]) == k:
            if born not in node["seen_in"]:
                node["seen_in"].append(born)
            return node["id"], False
    nid = next_id(db)
    db["nodes"].append({"id": nid, "what": what, "step": step, "human": human,
                        "ai": ai, "relationship": relationship, "brain": brain,
                        "born": born, "seen_in": [born], "note": note,
                        "owner": "PENDING"})
    return nid, True


def record_run(db: dict, example: str, minted: list[str], reused: list[str]) -> None:
    db["runs"].append({"example": example, "new": minted, "reused": reused,
                       "n_new": len(minted), "n_reused": len(reused),
                       "total_after": len(db["nodes"])})


def curve(db: dict) -> str:
    out = ["run | example | new IDs | reused | total"]
    for i, r in enumerate(db["runs"], 1):
        out.append(f"{i:>3} | {r['example'][:40]:<40} | {r['n_new']:>2} | "
                   f"{r['n_reused']:>2} | {r['total_after']}")
    tail = [r["n_new"] for r in db["runs"][-6:]]
    out.append(f"\nlast six runs minted: {tail}")
    out.append(f"total nodes: {len(db['nodes'])}   runs: {len(db['runs'])}")
    dry = 0
    for r in reversed(db["runs"]):
        if r["n_new"] == 0:
            dry += 1
        else:
            break
    out.append(f"consecutive dry runs (no new ID): {dry}")
    return "\n".join(out)


if __name__ == "__main__":
    print(curve(load()))
