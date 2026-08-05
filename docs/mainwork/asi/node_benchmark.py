"""GAP-CORE-006 — score the 70 SB nodes. His registered required action:

    "Execute SB70/URR25 traces against approved examples and score source
     fidelity, drift, usefulness and proof debt."      [GAP-CORE-006, HIGH, OPEN]

Registered 2026-07-19 in his own gap register and never executed. The 70 nodes
run, the suite passes, and no node has ever been measured for whether it HELPS.

WHAT IS MEASURED, and why each one is the honest version of his four words:

  SOURCE FIDELITY  — does the node's own finding contain material from the raw
                     ask, or only boilerplate? Measured as the share of runs
                     whose finding text carries a content word from the input.
                     A node can score 0 and still be correct (SB-04 emits a
                     hash); 0 is a flag to read, not a verdict.

  DRIFT (inverted)  — his word, measured as INPUT-SENSITIVITY: how many
                     distinct findings does the node produce across N different
                     examples? A node emitting one identical string for every
                     input is not reasoning about the input. This is the
                     decisive column and the one nobody has run.

  USEFULNESS       — does it emit structured params a later node could consume,
                     and does it ever halt? Prose that nothing downstream can
                     read is decoration.

  PROOF DEBT       — does it assert without tagging? Counts findings that make
                     a claim and carry neither params nor a halt nor a hedge.

NOT MEASURED, and said plainly: whether the node's judgement is CORRECT. That
needs a human or an external checkpoint (his ENG-SUP-006), and this harness is
judge-and-party by construction — it is the engine scoring itself. The numbers
below are mechanical properties, not quality.
"""

from __future__ import annotations

import sys, os, json, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "src"))

from sourceborn.nodes import SB_NODES
from sourceborn.node_work import SB_WORK, WalkContext
from sourceborn.engine import SourcebornEngine

# His own example bank — every one from his record, none invented for the test.
EXAMPLES = [
    ("hunger+work", "A person is hungry and physically tired but continues working "
                    "because completing the task is more important right now."),
    ("hunger",      "Hunger is calling fuel for the body. It is not just cook and eat. "
                    "Earth is point zero, then land, water, seeds, season."),
    ("gravity",     "Newton did not invent gravity. He was observing, reverse engineering "
                    "is done, and he found a sequence and a permanent bond in that."),
    ("water cycle", "Sun, water vaporization, cloud, rain, river and sea again."),
    ("the bet",     "Mahabharat betting lead to end of era but we took it as lead by women pride."),
    ("RH",          "Prove that all nontrivial zeros of the zeta function lie on the "
                    "middle line. Re(s) = 1/2 + ti."),
    ("K",           "Half everytime, keeping the half file back and using the half. It "
                    "will not change the answer, it will increase the speed."),
    ("present fact","What is the current share price of TCS today?"),
    ("cricket",     "Cricket is an invention. Consider it as invention, not a discovery."),
    ("language",    "Language is bigger than science, so it came first."),
    ("holo",        "There is something here. A feeling with no clear start, end, or name, "
                    "but it keeps pulling my mind back."),
    ("stake",       "I am making the sequence itself, not the product at each stage."),
]


def run() -> dict:
    eng = SourcebornEngine()
    # findings[node_id] = list of (example_name, finding)
    findings: dict[str, list] = collections.defaultdict(list)

    for name, text in EXAMPLES:
        # Populate the context exactly as run_walk does: run the pipeline first
        # so every node scores against REAL working state, not an empty shell.
        eng.run(text, origin="benchmark")
        rc = dict(eng._ctx)
        rc.pop("engine", None)
        ctx = WalkContext(**{k: v for k, v in rc.items()
                             if k in WalkContext.__dataclass_fields__})
        for node in SB_NODES:
            fn = SB_WORK.get(node.sb_id)
            if fn is None:
                findings[node.sb_id].append((name, None))
                continue
            try:
                findings[node.sb_id].append((name, fn(ctx)))
            except Exception as exc:                       # a node must not kill the run
                findings[node.sb_id].append((name, ("ERROR", repr(exc)[:120])))

    stop = set("the a an of is not and or to for it in as with that this what no none "
               "raw source locked untouched origin chars".split())
    rows = []
    for node in SB_NODES:
        got = findings[node.sb_id]
        live = [(n, f) for n, f in got if f is not None and not isinstance(f, tuple)]
        errs = [n for n, f in got if isinstance(f, tuple)]
        missing = len([1 for n, f in got if f is None])
        if not live:
            rows.append({"id": node.sb_id, "name": node.name, "status": "NO WORK FN"
                         if missing else "ERROR", "errors": len(errs)})
            continue

        texts = [f.text for _, f in live]
        distinct = len(set(texts))
        # source fidelity: finding echoes a content word from its own input
        hits = 0
        for (n, f), (_, src) in zip(live, [(n, dict(EXAMPLES)[n]) for n, _ in live]):
            words = {w.strip(".,?").lower() for w in src.split() if len(w) > 4}
            words -= stop
            if any(w in f.text.lower() for w in words):
                hits += 1
        with_params = sum(1 for _, f in live if f.params)
        with_halt = sum(1 for _, f in live if f.halt)
        # proof debt: asserts, but carries no params, no halt, and no hedge word
        hedges = ("may", "might", "not forced", "honest", "n/a", "none", "no ")
        debt = sum(1 for _, f in live
                   if not f.params and not f.halt
                   and not any(h in f.text.lower() for h in hedges))
        rows.append({
            "id": node.sb_id, "name": node.name, "status": "ok",
            "runs": len(live), "distinct": distinct,
            "sensitivity": round(distinct / len(live), 2),
            "fidelity": round(hits / len(live), 2),
            "params": round(with_params / len(live), 2),
            "halts": with_halt,
            "proof_debt": debt,
            "errors": len(errs),
        })
    return {"examples": [n for n, _ in EXAMPLES], "rows": rows}


if __name__ == "__main__":
    out = run()
    ok = [r for r in out["rows"] if r.get("status") == "ok"]
    print(f"examples: {len(out['examples'])}   nodes scored: {len(ok)}/{len(out['rows'])}\n")

    flat = [r for r in ok if r["distinct"] == 1]
    print(f"=== FLAT NODES — one identical finding for all {len(out['examples'])} inputs: "
          f"{len(flat)}/{len(ok)} ===")
    for r in flat:
        print(f"  {r['id']} {r['name'][:46]:<46} fidelity={r['fidelity']}")

    print(f"\n=== MOST INPUT-SENSITIVE ===")
    for r in sorted(ok, key=lambda x: -x["distinct"])[:12]:
        print(f"  {r['distinct']:>2}/{r['runs']} distinct  {r['id']} {r['name'][:44]:<44} "
              f"fid={r['fidelity']} params={r['params']} halts={r['halts']}")

    print(f"\n=== ZERO SOURCE FIDELITY (never echoes its own input) ===")
    for r in [x for x in ok if x["fidelity"] == 0.0]:
        print(f"  {r['id']} {r['name'][:50]:<50} distinct={r['distinct']}")

    print(f"\n=== NEVER HALTS, NEVER EMITS PARAMS ===")
    for r in [x for x in ok if x["halts"] == 0 and x["params"] == 0.0]:
        print(f"  {r['id']} {r['name'][:50]:<50} distinct={r['distinct']}")

    tot = len(ok)
    print(f"\n=== TOTALS over {tot} scored nodes ===")
    print(f"  mean input-sensitivity : {sum(r['sensitivity'] for r in ok)/tot:.2f}")
    print(f"  mean source fidelity   : {sum(r['fidelity'] for r in ok)/tot:.2f}")
    print(f"  nodes that ever halt   : {sum(1 for r in ok if r['halts'])}")
    print(f"  nodes emitting params  : {sum(1 for r in ok if r['params'] > 0)}")
    print(f"  total proof-debt hits  : {sum(r['proof_debt'] for r in ok)}")
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "node_benchmark.json"), "w"), indent=1)
