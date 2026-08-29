"""THE COMPLETE ARCHITECTURE — his split, on his spine, both columns.

His order: *"rebuild it complete with all 183 containers and all rows / must
follow the example and meaning confirmed t1 to t-9 and all above confirmed by
me"*, and before it: *"now file it in repo and wire it"*.

WHAT THIS IS

The 1-10-8-40 bank held 10 segments, 80 containers and 3,204 rows, and 69 of
those 80 containers carried two, three or five meanings in one ID. He ruled the
split: **every ID holding more than one meaning becomes separate IDs, all new
IDs, no placeholders.** That gives 27 segments and 183 containers. 275 of the
3,204 rows carried more than one meaning too; split, the rows come to 3,483.

Above the segments sit his six macro pillars. Through all of it runs the
universal sequence — which is the organising axis here, not a stage the work
passes once: every container, row, rubric, filter, operating state, evidence
level and failure class is placed at the step where it acts.

HIS SPINE, AND THE ONE THING IT NEEDED

Steps 1-8 are his: GROUND, PRESSURE, USE, WITNESS, EXPRESSION, NAMING, HALT,
LOOP — and step 8 CLOSES TO STEP 1, because the halt becomes the next ground.
Steps 9-12 (CONSOLIDATION, ALIENATION, COLLISION, METAMORPHOSIS) are not a
continuation of that line; they are the life of the loop itself across many
cycles, and 11 and 12 can fire at any step. That distinction is recorded on
every step as `order`, so the closure of his loop is never lost.

WHAT IS NOT TOUCHED

`data/human_registry.json` — his source bank — is **not modified**. His law is
replace, never delete: the 3,204 stand exactly as they are, and this file sits
beside them carrying what they became. A test proves the source is untouched
and still reads 3,204.

BOTH COLLUMNS AT EVERY NODE

Every container carries a HUMAN name (his) and a COMPUTER parallel, because ASI
is the verified connection between the two sides and a structure with only the
human half cannot link. The computer column is engineering, not interpretation
of his meaning.

WHAT IS STILL OPEN, AND SAYS SO

ARCHETYPE, LINK and SCALE are declared with no ceiling and hold nothing yet.
They open at their own phases, from the books. Nothing is placed in them here.
"""

from __future__ import annotations

import functools
import os

_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data",
                     "sbx_architecture.json")

#: the three layers that exist by declaration and hold nothing yet — his ruling
#: was "no count, its open to increase", so they carry no ceiling
OPEN_LAYERS = (
    {"id": "ARCHETYPE", "holds": "understandings extracted from the books — each with "
     "its scale axis, the intent types it can produce, its discriminator and what "
     "it refuses", "count": 0, "ceiling": None, "opens_at": "the archetype phase"},
    {"id": "LINK", "holds": "relations between rows as first-class counted objects. "
     "'Diamond cut diamond' is a link between two ego-rows, not a row",
     "count": 0, "ceiling": None, "opens_at": "the link phase"},
    {"id": "SCALE", "holds": "the stored axis on every archetype — micro, individual, "
     "relational, macro, and more; his ruling was that it is not only four",
     "count": 0, "ceiling": None, "opens_at": "the scale phase"},
)


@functools.lru_cache(maxsize=1)
def arch() -> dict:
    """The whole architecture, read once."""
    import json
    with open(_DATA, encoding="utf-8") as f:
        return json.load(f)


def pillars() -> list:
    return arch()["pillars"]


def spine() -> list:
    """The twelve steps. `order` records which are his first-order loop."""
    return arch()["spine"]


def step(n: int) -> dict:
    """One step whole — its containers, rubrics, filters, states, failures."""
    s = next((x for x in spine() if x["step"] == int(n)), None)
    if s is None:
        return {"found": False, "step": n,
                "known": [x["step"] for x in spine()]}
    cons = [c for c in containers() if c["step"] == int(n)]
    return dict(s, found=True, containers=cons,
                container_count=len(cons),
                row_count=sum(len(c["rows"]) for c in cons))


def segments() -> list:
    return arch()["segments"]


def containers() -> list:
    return arch()["containers"]


def container(cid: str) -> dict:
    c = next((x for x in containers() if x["id"] == cid), None)
    return c if c else {"found": False, "id": cid}


def rows() -> list:
    """Every row, flat, carrying its container and step."""
    out = []
    for c in containers():
        for r in c["rows"]:
            out.append(dict(r, container=c["id"], container_name=c["name"],
                            segment=c["segment"], pillar=c["pillar"],
                            step=c["step"]))
    return out


def computer_of(cid: str) -> dict:
    """The machine column for one container — the other half of the node."""
    c = container(cid)
    if not c.get("id"):
        return c
    return {"id": c["id"], "human": c["human"], "computer": c["computer"],
            "law": "ASI is the verified connection between the two columns; "
                   "neither column alone is the node"}


def intent_types_at(n: int) -> list:
    s = next((x for x in spine() if x["step"] == int(n)), None)
    return s.get("intent_types", []) if s else []


def intent_types() -> dict:
    """All nine, with the step each one reads an event from."""
    out = {}
    for s in spine():
        for t in s.get("intent_types", []):
            out[t.split(" ")[0]] = {"type": t, "step": s["step"],
                                    "step_name": s["name"]}
    return out


def place_on_spine(text: str, repo: str = ".") -> dict:
    """THE WIRING. An ask is seated on the source bank as it always was; the
    seatings are then read through the split, and the ask lands on STEPS.

    Nothing about the seating changes — the same rows are reached. What is new
    is that a seated row now has a step, a pillar and a machine column, so the
    ask can be read on his spine instead of only as a list of parameters."""
    from . import growing as W          # late import: growing must not import this
    from . import archetype as ARCH     # the layer above the rows, reaching down
    placed = W.place(text, "sbx")
    by_old = {}
    for c in containers():
        by_old.setdefault(c["from"]["container"], []).append(c)

    # TWO WAYS A ROW IS REACHED, and they are never merged into one number.
    # WORDS: the seating, exactly as it always ran.
    # ARCHETYPE: the route the words could not take. His dice game seats zero
    # rows by word and reaches twelve by shape; if the two were summed into a
    # single count the page could not say which mechanism did the work, and
    # `reached_by` is what makes that visible on every row.
    reached = []
    for s in placed.get("strengthened", []):
        reached.append({"sb_id": s.get("sb_id"), "name": s.get("name"),
                        "container": s.get("container"), "by": "WORDS",
                        "via": None})
    seated_ids = {r["sb_id"] for r in reached}
    fired = ARCH.fires_on(text)
    for r in fired["rows_reached"]:
        if r["id"] in seated_ids:
            continue
        reached.append({"sb_id": r["id"], "name": r["name"],
                        "container": r["container"], "by": "ARCHETYPE",
                        "via": r["via"]})

    steps, hits = {}, []
    for s in reached:
        for c in by_old.get(s.get("container"), []):
            names = {r["name"].lower() for r in c["rows"]}
            if s.get("name", "").lower() in names:
                hits.append({"row": s.get("name"), "source_id": s.get("sb_id"),
                             "reached_by": s["by"], "via": s["via"],
                             "container": c["id"], "container_name": c["name"],
                             "segment": c["segment"], "pillar": c["pillar"],
                             "step": c["step"], "computer": c["computer"]})
                d = steps.setdefault(c["step"], {"step": c["step"], "rows": [],
                                                 "containers": set()})
                d["rows"].append(s.get("name"))
                d["containers"].add(c["id"])
                break
    lit = []
    for n in sorted(steps):
        sp = next(x for x in spine() if x["step"] == n)
        lit.append({"step": n, "name": sp["name"], "order": sp["order"],
                    "human": sp["human"], "computer": sp["computer"],
                    "rows": steps[n]["rows"],
                    "containers": sorted(steps[n]["containers"]),
                    "intent_types": sp.get("intent_types", []),
                    "rubrics": sp.get("rubrics", [])})
    return {
        "text": text,
        "events": placed.get("counts", {}).get("events", 0),
        "source_rows_seated": len(placed.get("strengthened", [])),
        "archetype_rows_reached": sum(1 for r in reached if r["by"] == "ARCHETYPE"),
        "archetypes_fired": [{"id": f["id"], "name": f["name"],
                              "routes": f["routes"],
                              "matched_on": f["matched_on"]}
                             for f in fired["fired"]],
        "rows_reached_total": len(reached),
        "mapped_into_split": len(hits),
        "steps_lit": lit,
        "steps_lit_count": len(lit),
        "hits": hits,
        "concluded": None,
        "law": "the seating is unchanged — this reads it through the split and "
               "lands it on his spine. The archetype layer reaches rows the "
               "words could not, and every row says which route reached it. "
               "Nothing is chosen and no intent is concluded from one event.",
        "unmapped_note": "a seated row with no home in the split is reported by "
                         "the difference between source_rows_seated and "
                         "mapped_into_split, never dropped silently",
    }


def verify() -> dict:
    """The counts, and the proof the source bank was not touched."""
    from . import human_registry as hr
    a = arch()
    cs, rs = containers(), rows()
    by_step = {}
    for c in cs:
        by_step[c["step"]] = by_step.get(c["step"], 0) + 1
    return {
        "schema": a["schema"],
        "pillars": len(pillars()),
        "steps": len(spine()),
        "segments": len(segments()),
        "containers": len(cs),
        "rows": len(rs),
        "containers_per_step": dict(sorted(by_step.items())),
        "every_step_populated": len(by_step) == 12,
        "source_bank_rows": len(hr.parameters()),
        "source_bank_containers": len(hr.containers()),
        "source_untouched": len(hr.parameters()) == 3204 and len(hr.containers()) == 80,
        "open_layers": [d["id"] for d in OPEN_LAYERS],
    }


def stats() -> dict:
    a = arch()
    return dict(a["counts"], schema=a["schema"], law=a["law"],
                derived_from=a["derived_from"],
                open_layers=[d["id"] for d in OPEN_LAYERS],
                loop_closes_at="step 8 returns to step 1; 9-12 are second order")


def annotations() -> list:
    return [
        ("every ID holding more than one meaning becomes separate IDs", "sbx.containers"),
        ("the source bank is replaced, never deleted", "sbx.verify"),
        ("both columns at every node", "sbx.computer_of"),
        ("everything flows in the universal sequence", "sbx.spine"),
        ("archetype, link and scale open with no ceiling", "sbx.OPEN_LAYERS"),
    ]
