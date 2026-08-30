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

WHAT IS OPEN, AND SAYS SO

ARCHETYPE, LINK and SCALE carry no ceiling — his ruling, *no count, its open to
increase*. They were declared empty here and have since been filled at their
own phases, so their counts are READ FROM THE LIVE MODULES rather than typed:
a typed count goes stale the moment the thing it counts changes, which is
exactly what happened when ARCHETYPE stood at a hardcoded 0 while the archetype
layer was being built.

SCALE is the one still holding a gate: its axis is built and counted, but only
his four bands are IN FORCE. The five further bands are PROPOSED, each citing
the example of his that demands it, and they wait for his word.
"""

from __future__ import annotations

import functools
import os

_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data",
                     "sbx_architecture.json")

#: The layers he declared with no ceiling — his ruling was "no count, its open
#: to increase". Their counts are READ FROM THE LIVE MODULES, never typed here:
#: ARCHETYPE stood at a hardcoded 0 for exactly as long as it took to build the
#: archetype layer, at which point the number on this page was simply wrong. A
#: count that is typed goes stale the moment the thing it counts changes.
def _archetype_count() -> int:
    try:
        from . import archetype
        return len(archetype.archetypes())
    except Exception:
        return 0


def _scale_count() -> int:
    try:
        from . import scale
        return len(scale.bands())
    except Exception:
        return 0


def _link_count() -> int:
    try:
        from . import link
        return len(link.links())
    except Exception:
        return 0


OPEN_LAYERS = (
    {"id": "ARCHETYPE", "holds": "understandings extracted from the books — each with "
     "its scale axis, the intent types it can produce, its discriminator and what "
     "it refuses", "count": _archetype_count, "ceiling": None,
     "opens_at": "the archetype phase", "state": "OPEN — counted live"},
    {"id": "LINK", "holds": "relations between rows as first-class counted objects. "
     "'Diamond cut diamond' is a link between two ego-rows, not a row",
     "count": _link_count, "ceiling": None, "opens_at": "the link phase",
     "state": "OPEN — counted live from the split bank"},
    {"id": "SCALE", "holds": "the stored axis on every archetype — micro, individual, "
     "relational, macro, and more; his ruling was that it is not only four",
     "count": _scale_count, "ceiling": None, "opens_at": "the scale phase",
     "state": "OPEN — the axis is built and counted live; 4 of the 9 bands "
              "are HIS and in force, 5 are PROPOSED and await his word"},
)


def open_layers() -> list:
    """OPEN_LAYERS with every live count resolved."""
    out = []
    for l in OPEN_LAYERS:
        r = dict(l)
        if callable(r.get("count")):
            r["count"] = r["count"]()
        out.append(r)
    return out


# ---------------------------------------------------------------------------
# THE NODE BRAIN ON HIS SPINE
#
# His ask: *Node brain structure added*. The structure itself is HIS and was
# locked in Phase A — 12 node types, 16 fields, 10 typed links, 11 memory
# kinds, 4 statuses, 5 write and 6 read conditions, with a fingerprint that
# fails loudly if any of it changes silently.
#
# What was missing is that it stood beside the architecture instead of inside
# it. Every other layer is PLACED — the intent types, the filters, the states,
# the evidence levels, the failure classes, the chain steps, the rubrics each
# sit at the step where they act. The node types did not, so nothing could say
# where in his loop a CONTRADICTION node comes into being.
#
# THE PLACEMENT BELOW IS MINE, NOT HIS, AND EVERY ROW SAYS SO. His 12 types are
# verbatim; which step each acts at is a derivation with its reason written
# out, and it is correctable by a word from him — the same standing as a
# DERIVED trigger.
# ---------------------------------------------------------------------------

NODE_ON_SPINE = {
    "STATE": (1, "A state is the standing condition before anything moves — "
                 "which is what GROUND is: fuel exists before any stomach."),
    "ACTOR": (1, "Whoever is there before the first move. An actor is not "
                 "produced by the event; the event finds them already there."),
    "ARTIFACT": (1, "An object the world left behind becomes the GROUND of "
                    "whoever finds it. The tablet is the ground of the whole "
                    "king investigation, not its output."),
    "EVENT": (2, "PRESSURE is where contact is forced and the happening "
                 "occurs. His motto begins here: everything happening is an "
                 "event."),
    "SEQUENCE": (3, "USE is the running order — millennia of eating before "
                    "anyone can say what food is. A sequence runs before it is "
                    "described."),
    "INTENT": (4, "WITNESS is the step that asks WHY the body demands this, "
                  "and intent is never observed directly — his own law is that "
                  "it is read from how things were arranged around the event. "
                  "That reading is a witnessing, not an observation."),
    "RELATION": (5, "EXPRESSION is where a thing takes a structured form "
                    "another node can read. A named tie between two nodes is "
                    "exactly that form."),
    "RULE": (6, "NAMING is where a label replaces the thing — and a standing "
                "constraint is the strongest form of that. This is also where "
                "the MASK lives, which is why a rule is watched here."),
    "CONTRADICTION": (7, "HALT. Two readings that cannot both stand is the "
                         "definition of the halt, and his law is that a "
                         "failure is never failure — it opens the loop."),
    "PATTERN": (9, "CONSOLIDATION runs across many passes, and an arrangement "
                   "that recurs cannot exist inside one. His own bar is five "
                   "repeats."),
    "MEMORY": (9, "What a node has seen before is what consolidation keeps. "
                  "It is scheduled, not provoked."),
    "FUTURE_STATE": (12, "METAMORPHOSIS — a state something was working "
                         "toward changes what the thing IS, not what it "
                         "holds. It fires at any step, which is why his "
                         "second order marks 11 and 12 ANY-STEP."),
}


def node_types() -> list:
    """His 12 node types, each placed at the step where it acts.

    The type, its stem and its meaning are HIS, carried from the locked Phase A
    schema. The step and the reason are MINE and say so."""
    from . import nodebrain as N
    out = []
    for t in N.NODE_TYPES:
        step_n, why = NODE_ON_SPINE.get(t["type"], (None, ""))
        s = next((x for x in spine() if x["step"] == step_n), None)
        out.append({
            "type": t["type"], "stem": t["stem"], "is": t["is"],
            "by": "HIS — Phase A locked schema",
            "step": step_n,
            "step_name": s["name"] if s else None,
            "order": s["order"] if s else None,
            "placed_by": "DERIVED — this side's reading of his spine",
            "why": why,
            "correctable": True,
        })
    return out


def node_types_at(n: int) -> list:
    return [t for t in node_types() if t["step"] == int(n)]


def node_brain() -> dict:
    """The node brain as a layer of the architecture.

    His structure whole, with the fingerprint that proves it has not moved, its
    placement on his spine, and the five namespace collisions carried through
    rather than quietly settled."""
    from . import nodebrain as N
    placed = node_types()
    by_step = {}
    for t in placed:
        by_step.setdefault(t["step"], []).append(t["type"])
    return {
        "schema_version": N.SCHEMA_VERSION,
        "fingerprint": N.fingerprint(),
        "node_types": placed,
        "node_type_count": len(placed),
        "on_spine": {str(k): v for k, v in sorted(by_step.items())},
        "steps_used": sorted(by_step),
        "steps_unused": [s["step"] for s in spine() if s["step"] not in by_step],
        "fields": list(N.FIELDS),
        "field_count": len(N.FIELDS),
        "link_types": list(N.LINK_TYPES),
        "link_type_count": len(N.LINK_TYPES),
        "memory_kinds": list(N.MEMORY_KINDS),
        "statuses": list(N.STATUSES),
        "write_conditions": list(N.WRITE_CONDITIONS),
        "read_conditions": list(N.READ_CONDITIONS),
        "collisions": N.collisions(),
        "law": "the 12 types, 16 fields and 10 typed links are HIS and locked; "
               "the fingerprint fails loudly if any of it changes silently. "
               "WHERE each type sits on his spine is this side's reading, "
               "marked DERIVED on every row and correctable by a word.",
        "not_settled": "five node-type names collide with growth series names "
                       "(EVENT · INTENT · PATTERN · RULE · STATE). The two "
                       "namespaces are NOT merged; what each side means is "
                       "carried and his ruling is awaited.",
    }


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


# ---------------------------------------------------------------------------
# HIS DISPLAY LAW: NEW PARAMETERS IN FRONT, OLD IN BACK
#
# His words, given with the ruling that the source bank is never deleted:
#
#     Human_registry.json is untouched and still reads 3,204 rows and 80
#     containers. The split stands beside it, never over it, and a test proves
#     the source is intact — use new parameters in front n old in back
#
# Both halves are load-bearing and they are not in tension. The OLD bank is
# never removed, because removing it would break the promise that his source
# document stands untouched. And the NEW reading leads, because the split is
# what the system now reasons on — a reader who sees the old id first is being
# shown the superseded address as though it were the current one.
#
# So every row that carries both is rendered NEW FIRST, OLD LAST, in one
# function, so the convention cannot drift apart across the pages that use it.
# ---------------------------------------------------------------------------

FRONT_BACK_LAW = ("new parameters in front, old in back — the split leads "
                  "because it is what the system reasons on; the source "
                  "follows because it is never deleted.")


def _new_row(c: dict, old_flat_id: str, old_name: str) -> dict:
    """The split row a seated source row became.

    Matched on the source row's own flat id (`SB-HFR-P1132` -> `P1132`), which
    every split row carries as `from_row`. A row that was SPLIT produced more
    than one child from one parent, so the name decides between them."""
    want = (old_flat_id or "").replace("SB-HFR-", "")
    kids = [r for r in c.get("rows", ()) if r.get("from_row") == want]
    if len(kids) > 1:
        exact = [r for r in kids
                 if r["name"].strip().lower() == (old_name or "").strip().lower()]
        if exact:
            return exact[0]
    if kids:
        return kids[0]
    by_name = [r for r in c.get("rows", ())
               if r["name"].strip().lower() == (old_name or "").strip().lower()]
    return by_name[0] if by_name else {}


def front_back(c: dict, s: dict) -> dict:
    """One reached row, rendered his way: the split in front, the source behind.

    The key order is the display order — `id` and `name` are the SPLIT row, and
    everything from the source bank is gathered under `from` at the end, so no
    reader meets an old address before the new one."""
    new = _new_row(c, s.get("sb_id"), s.get("name"))
    return {
        # ---- NEW, IN FRONT --------------------------------------------------
        "id": new.get("id"),
        "row": new.get("name") or s.get("name"),
        "container": c["id"],
        "container_name": c["name"],
        "segment": c["segment"],
        "pillar": c["pillar"],
        "step": c["step"],
        "computer": c["computer"],
        "was_split": new.get("was_split"),
        # ---- how it was reached --------------------------------------------
        "reached_by": s["by"],
        "via": s["via"],
        # ---- OLD, IN BACK ---------------------------------------------------
        "from": {
            "id": s.get("sb_id"),
            "name": s.get("name"),
            "container": s.get("container"),
            "bank": "human_registry.json — 3,204 rows, untouched",
        },
        # kept because callers read it by this name; it is the SOURCE id and
        # it deliberately sits behind the split id above.
        "source_id": s.get("sb_id"),
    }


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
                hits.append(front_back(c, s))
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
    # EVERY LAYER ON ONE ASK, not one layer per page. The trigger layer says
    # WHEN each lit container fires; the readings layer says what the event
    # could mean; the link layer says what belongs to the meeting rather than
    # to either end. Each was reachable only from its own route before this,
    # which is the defect weighting.py had — a module importable from nothing.
    #
    # `trigger.for_hits` exists because this function calls that module and
    # that module calls this one: passing the already-computed hits is what
    # breaks the recursion.
    from . import trigger as TRG
    from . import readings as RD
    from . import link as LNK
    from . import angles as ANG
    fired_triggers = TRG.for_hits(hits)
    nine = RD.read(text)
    meetings = LNK.fires_on(text)
    # ANGLES are a PROPERTY applied at generation, not a layer — his ruling.
    # All of them run; none is chosen. `for_hits` again, for the same reason.
    angled = ANG.for_hits(text, hits)

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
        # ---- the layers, on this one ask -----------------------------------
        "triggers": fired_triggers,
        "readings": {"count": nine["reading_count"],
                     "readings": nine["readings"],
                     "chosen": nine["chosen"]},
        "meetings": {"count": meetings["fired_count"],
                     "readings": meetings["readings"]},
        "angles": {"run": angled["angles_run"],
                   "distinct_container_sets": angled["distinct_container_sets"],
                   "readings": angled["readings"],
                   "chosen": angled["chosen"]},
        "layers_run": ["SEGMENT", "CONTAINER", "SUB-PARAMETER", "ARCHETYPE",
                       "TRIGGER", "LINK", "SCALE", "INTENT-READING"],
        "properties_applied": ["ANGLE"],
        "concluded": None,
        "law": "the seating is unchanged — this reads it through the split and "
               "lands it on his spine. The archetype layer reaches rows the "
               "words could not, and every row says which route reached it. "
               "The trigger layer says WHEN each lit container fires, the "
               "reading layer says what the event could mean, and the link "
               "layer says what belongs to the meeting rather than to either "
               "end. Nothing is chosen and no intent is concluded from one "
               "event.",
        "unmapped_note": "a seated row with no home in the split is reported by "
                         "the difference between source_rows_seated and "
                         "mapped_into_split, never dropped silently",
    }


# ---------------------------------------------------------------------------
# THE SPLIT REVIEW
#
# His ask: *split review it again*. Not a re-statement of the counts — a set of
# checks that can FAIL, run over the live data, reporting what is wrong rather
# than what is right. Nothing here corrects anything: his standing rule is that
# meanings are fixed with notes, never renames, and that nothing is removed.
# Every finding is surfaced with what it would take to close it, and left.
# ---------------------------------------------------------------------------

#: His stated rule for a container's row count: *each new container gets its
#: own fresh 40*.
ROWS_PER_CONTAINER = 40


def review() -> dict:
    """Audit the split against checks that can fail. Findings, not assurances."""
    import collections
    cs, rs = containers(), rows()
    findings, passes = [], []

    # ---- the arithmetic: does every source row still have a child? ----------
    from . import asi_pyramid as AP
    flat, _ = AP._flat()
    source_ids = {"P%04d" % r["flat"] for r in flat}
    cited = {r["from_row"] for r in rs}
    orphaned = sorted(source_ids - cited)
    dangling = sorted(cited - source_ids)
    per_parent = collections.Counter(r["from_row"] for r in rs)
    split_parents = [p for p, n in per_parent.items() if n > 1]
    if orphaned or dangling:
        findings.append({
            "id": "SPLIT-01", "severity": "BLOCKING",
            "what": "a source row lost its child, or a split row cites a "
                    "source that does not exist",
            "orphaned_source_rows": len(orphaned),
            "dangling_split_rows": len(dangling),
            "examples": orphaned[:10] + dangling[:10],
            "his_call": True,
        })
    else:
        passes.append({
            "id": "SPLIT-01", "checked": "every one of his 3,204 source rows "
            "has at least one child in the split, and no split row cites a "
            "source that is not there",
            "source_rows": len(source_ids),
            "parents_split": len(split_parents),
            "children_from_split_parents":
                sum(n for n in per_parent.values() if n > 1),
            "arithmetic": "%d source + %d gained by splitting = %d"
                          % (len(source_ids), len(rs) - len(source_ids), len(rs)),
        })

    # ---- his 40-per-container rule -----------------------------------------
    counts = {c["id"]: len(c.get("rows", ())) for c in cs}
    under = {k: v for k, v in counts.items() if v < ROWS_PER_CONTAINER}
    if under:
        thin = sorted(under.items(), key=lambda kv: kv[1])
        by_id = {c["id"]: c for c in cs}
        findings.append({
            "id": "SPLIT-02", "severity": "OPEN — HIS NUMBER TO FINALISE",
            "what": "his rule is that each new container gets its own fresh "
                    "%d rows. Most do not have them." % ROWS_PER_CONTAINER,
            "containers_under": len(under),
            "containers_at_or_over": len(cs) - len(under),
            "shortfall_to_%d_each" % ROWS_PER_CONTAINER:
                sum(ROWS_PER_CONTAINER - v for v in under.values()),
            "thinnest": [{"id": k, "name": by_id[k]["name"], "rows": v,
                          "from": by_id[k]["from"]["name"]}
                         for k, v in thin[:10]],
            "why": "splitting a parent DIVIDED its 40 rows among its children "
                   "rather than giving each child 40 of its own. A parent that "
                   "became five containers left five thin ones.",
            "what_would_close_it": "fresh row names for the shortfall. There "
                                   "is no source for them — his 650-row named "
                                   "reserve is the only real material, and it "
                                   "does not cover this. HIS NUMBER TO "
                                   "FINALISE; this side will not decide it.",
            "his_call": True,
        })

    # ---- the split's own output re-introducing multi-meaning ---------------
    def multi(s):
        low = (s or "").lower()
        return "/" in low or " and " in low or "," in low or " & " in low
    mc = [c["id"] + " " + c["name"] for c in cs if multi(c["name"])]
    mr = [r["name"] for r in rs if multi(r["name"])]
    if mc or mr:
        findings.append({
            "id": "SPLIT-03", "severity": "BLOCKING",
            "what": "a name in the split still carries more than one meaning, "
                    "which is the thing the split exists to remove",
            "container_names": mc[:20], "row_names": mr[:20],
            "his_call": True,
        })
    else:
        passes.append({"id": "SPLIT-03", "checked": "no container name and no "
                       "row name still carries more than one meaning — no "
                       "slash, no 'and', no comma, no ampersand",
                       "containers": len(cs), "rows": len(rs)})

    # ---- duplicate names ---------------------------------------------------
    by_name = collections.defaultdict(list)
    for c in cs:
        by_name[c["name"]].append(c)
    dup_c = {k: v for k, v in by_name.items() if len(v) > 1}
    if dup_c:
        findings.append({
            "id": "SPLIT-04", "severity": "OPEN — HIS NAMES TO GIVE",
            "what": "two different containers carry the same bare name. The "
                    "split separated the PARENT names and two children landed "
                    "on the same word — the multi-meaning problem reappearing "
                    "in the split's own output, one level down.",
            "duplicates": {k: [{"id": c["id"], "segment": c["segment"],
                                "step": c["step"], "from": c["from"]["name"]}
                               for c in v] for k, v in dup_c.items()},
            "count": len(dup_c),
            "what_would_close_it": "a qualifying word on each. Not done here: "
                                   "his rule is that meanings are fixed with "
                                   "notes, never renames, so the names are "
                                   "his to give.",
            "his_call": True,
        })
    dup_r = [k for k, n in collections.Counter(r["name"] for r in rs).items()
             if n > 1]
    if dup_r:
        findings.append({
            "id": "SPLIT-05", "severity": "OPEN",
            "what": "the same row name appears in more than one container",
            "count": len(dup_r), "examples": sorted(dup_r)[:20],
            "note": "not automatically wrong — `Recovery` in a body container "
                    "and `Recovery` in a social one may be two real rows. It "
                    "is reported so he can say which are one row seen twice "
                    "and which are two.",
            "his_call": True,
        })

    # ---- both columns at every node ----------------------------------------
    no_col = [c["id"] for c in cs if not c.get("computer") or not c.get("human")]
    if no_col:
        findings.append({"id": "SPLIT-06", "severity": "BLOCKING",
                         "what": "a container is missing one of its two columns",
                         "containers": no_col[:20], "his_call": True})
    else:
        passes.append({"id": "SPLIT-06", "checked": "every one of the %d "
                       "containers carries BOTH columns — the human name he "
                       "wrote and a computer parallel" % len(cs)})

    # ---- every step reached -------------------------------------------------
    by_step = collections.Counter(c["step"] for c in cs)
    empty_steps = [s["step"] for s in spine() if s["step"] not in by_step]
    if empty_steps:
        findings.append({"id": "SPLIT-07", "severity": "BLOCKING",
                         "what": "a step of his spine holds no container",
                         "steps": empty_steps, "his_call": True})
    else:
        thin_steps = sorted(by_step.items(), key=lambda kv: kv[1])[:3]
        passes.append({"id": "SPLIT-07",
                       "checked": "all 12 steps of his spine hold containers",
                       "per_step": dict(sorted(by_step.items())),
                       "thinnest_steps": [{"step": s, "containers": n,
                                           "name": next(x["name"] for x in spine()
                                                        if x["step"] == s)}
                                          for s, n in thin_steps]})

    # ---- every declared layer member actually placed on the spine ----------
    declared = arch().get("counts", {})
    unplaced = []
    for key, label in (("filters", "universal filters"),
                       ("states", "operating states"),
                       ("evidence_levels", "evidence levels"),
                       ("failure_classes", "failure classes"),
                       ("chain_steps", "operating chain steps"),
                       ("rubrics", "rubrics"),
                       ("intent_types", "intent types")):
        seen = set()
        for s in spine():
            for x in s.get(key, ()):
                seen.add(x if isinstance(x, str) else x.get("id") or str(x))
        want = declared.get(key)
        if want is not None and len(seen) != want:
            unplaced.append({"layer": label, "declared": want,
                             "placed_on_spine": len(seen),
                             "difference": want - len(seen)})
    if unplaced:
        findings.append({
            "id": "SPLIT-09", "severity": "OPEN",
            "what": "a layer's declared count and the number actually placed "
                    "on his spine disagree. Every layer member is supposed to "
                    "sit at the step where it acts; one that is counted but "
                    "not placed exists in the total and nowhere in the work.",
            "layers": unplaced,
            "note": "the rubric layer is the one that disagrees: 67 declared, "
                    "66 distinct on the spine, 70 placements in total because "
                    "Trace, Relation, Compression and Gap each act at two "
                    "steps. Two rubrics sharing a name would also produce "
                    "this, which is why it is reported rather than guessed at.",
            "what_would_close_it": "naming the missing rubric, or confirming "
                                   "that two of the 67 share a name and the "
                                   "true distinct count is 66.",
            "his_call": True,
        })
    else:
        passes.append({"id": "SPLIT-09", "checked": "every declared member of "
                       "every layer is placed at a step of his spine"})

    # ---- the source bank untouched -----------------------------------------
    from . import human_registry as hr
    src_ok = len(hr.parameters()) == 3204 and len(hr.containers()) == 80
    if not src_ok:
        findings.append({"id": "SPLIT-08", "severity": "BLOCKING",
                         "what": "the source bank moved. It must not.",
                         "rows": len(hr.parameters()),
                         "containers": len(hr.containers()), "his_call": True})
    else:
        passes.append({"id": "SPLIT-08", "checked": "the source bank stands "
                       "untouched behind the split — 3,204 rows, 80 "
                       "containers, replaced and never deleted"})

    return {
        "reviewed": {"segments": len(segments()), "containers": len(cs),
                     "rows": len(rs), "steps": len(spine())},
        "checks_run": len(findings) + len(passes),
        "passed": passes, "passed_count": len(passes),
        "findings": findings, "findings_count": len(findings),
        "blocking": [f["id"] for f in findings if f["severity"] == "BLOCKING"],
        "law": "a review reports what is wrong, not what is right. Nothing "
               "here is corrected — meanings are fixed with notes, never "
               "renames, and nothing is removed. Every finding names what "
               "would close it and waits for him.",
    }


# ---------------------------------------------------------------------------
# HIS TWELVE-LAYER TABLE, LIVE
#
# He gave the table himself, as ask 5 — "your pending wiring" — with three
# columns: the count today, the count after the split, and the delta. This
# renders it against the LIVE data rather than against what was typed, and adds
# the one column his table could not have: whether the layer is actually WIRED,
# meaning it reaches an answer rather than only existing.
#
# Where the live number disagrees with his target, the row says so. That is the
# point of rendering it live — a table of targets that never checks itself is
# how the 4,120 went missing the first time.
# ---------------------------------------------------------------------------

#: His table, verbatim: (n, layer, before, his stated target, his note).
HIS_LAYERS = (
    (1, "Segments", 10, 27, "+17"),
    (2, "Containers", 80, 183, "+103"),
    (3, "Sub-parameters", 3204, 7603,
     "3,483 from splitting 275 multi-meaning rows · +4,120 fresh for the 103 "
     "new containers = ≈ 7,603 (+4,399)"),
    (4, "Universal filters", 40, 175,
     "40 families → 175 — the named filters are already listed inside the "
     "families; splitting frees every one of them (+135)"),
    (5, "Operating states", 12, 12,
     "every state name is single-meaning, nothing to split (0)"),
    (6, "Evidence levels", 7, 7, "H0–H6, single-meaning (0)"),
    (7, "Failure classes", 20, 20, "all single-meaning (0)"),
    (8, "Operating chain", 30, 34,
     "four steps carry two: Need or drive activation · Social and cultural "
     "filtering · Risk and reward estimation · Learning or defence (+4)"),
    (9, "Archetype", 0, None, "opens at Phase 9, no ceiling"),
    (10, "Link", 0, None, "counted from the split bank"),
    (11, "Scale", 0, None, "your axis, more than four"),
    (12, "Rubrics R01–R52", 52, 67,
     "fifteen carry two: Order/Time · Rule/Constraint · Promise/Commitment · "
     "Requirement/Contract · Qualification/Admissibility · Evidence/Test · "
     "Decision/Arbitration · Encounter/Access · Dynamics/Process · "
     "Effect/Output and five more (+15)"),
)


def _live_counts() -> dict:
    """Each layer's count as it actually stands, read from the live modules —
    never from the number typed in the architecture file."""
    c = arch().get("counts", {})
    live = {
        1: len(segments()),
        2: len(containers()),
        3: len(rows()),
        4: c.get("filters"),
        5: c.get("states"),
        6: c.get("evidence_levels"),
        7: c.get("failure_classes"),
        8: c.get("chain_steps"),
        12: c.get("rubrics"),
    }
    for l in open_layers():
        live[{"ARCHETYPE": 9, "LINK": 10, "SCALE": 11}[l["id"]]] = l["count"]
    return live


def _wired(n: int) -> dict:
    """Does the layer REACH AN ANSWER, or does it only exist?

    His own bar, given as *evidence of wiring is done with proof not your
    test*. A layer is WIRED only if a live call puts it in the path of an ask."""
    if n in (1, 2, 3):
        return {"wired": True, "how": "place_on_spine() lands an ask on "
                "segments, containers and rows, and every hit names them"}
    if n == 9:
        return {"wired": True, "how": "archetype.fires_on() runs inside "
                "place_on_spine(); a row reached that way is marked ARCHETYPE"}
    if n == 10:
        return {"wired": True, "how": "link.fires_on() returns a reading "
                "belonging to the meeting of two rows, which neither row nor "
                "either container can hold — his diamond returns it live"}
    if n == 11:
        return {"wired": True, "how": "scale.spread() returns every fired "
                "archetype at every band, so a reading is a coordinate rather "
                "than a label. HIS GATE STANDS: only his four bands are in "
                "force; the five proposed are stored, not applied."}
    if n in (5, 6, 7, 8, 12):
        return {"wired": False, "how": "placed at the step where it acts and "
                "returned by /sbx/step, but no ask is scored against it — it "
                "is carried, not consulted"}
    if n == 4:
        return {"wired": "PARTIAL", "how": "175 filters are placed on the "
                "spine; SEVEN filters run on every finding (filters.py). The "
                "other 168 are carried, not run."}
    return {"wired": False, "how": "declared with no ceiling and holds nothing"}


def layers() -> list:
    """His twelve-layer table, rendered against the live data."""
    live = _live_counts()
    out = []
    for n, name, before, target, note in HIS_LAYERS:
        now = live.get(n)
        row = {
            "n": n, "layer": name,
            "before": before,
            "his_target": target,
            "his_note": note,
            "live": now,
            "wired": _wired(n),
        }
        if target is None:
            row["against_target"] = "NO CEILING — his ruling"
            row["short_by"] = None
        elif now is None:
            row["against_target"] = "NOT COUNTED HERE"
            row["short_by"] = None
        elif now == target:
            row["against_target"] = "MET"
            row["short_by"] = 0
        elif now < target:
            row["against_target"] = "SHORT"
            row["short_by"] = target - now
        else:
            row["against_target"] = "OVER"
            row["short_by"] = target - now
        out.append(row)
    return out


def wiring() -> dict:
    """The honest state of ask 5 — what is built, what is short, what is
    carried but never consulted."""
    ls = layers()
    short = [l for l in ls if l["against_target"] == "SHORT"]
    wired = [l for l in ls if l["wired"]["wired"] is True]
    return {
        "his_ask": "your pending wiring",
        "layers": ls,
        "layer_count": len(ls),
        "met": [l["layer"] for l in ls if l["against_target"] == "MET"],
        "short": [{"layer": l["layer"], "live": l["live"],
                   "his_target": l["his_target"], "short_by": l["short_by"]}
                  for l in short],
        "no_ceiling": [l["layer"] for l in ls
                       if l["against_target"] == "NO CEILING — his ruling"],
        "wired": [l["layer"] for l in wired],
        "carried_not_consulted": [l["layer"] for l in ls
                                  if l["wired"]["wired"] is False],
        "partial": [l["layer"] for l in ls if l["wired"]["wired"] == "PARTIAL"],
        "the_one_gap": {
            "layer": "Sub-parameters",
            "live": len(rows()),
            "his_target": 7603,
            "short_by": 7603 - len(rows()),
            "why": "his target adds 4,120 fresh rows — 40 each for the 103 new "
                   "containers. Splitting produced 3,483 by dividing existing "
                   "rows among children; it created no new names, and there is "
                   "no source for 4,120 that does not already exist. His "
                   "650-row named reserve is the only real unassigned material "
                   "and it does not cover it.",
            "refused": "inventing 4,120 row names would be exactly the "
                       "placeholder he forbade. HIS NUMBER TO FINALISE.",
        },
        "law": "a layer is WIRED only if a live call puts it in the path of an "
               "ask. Existing at a step is not wiring — his own bar is "
               "evidence of wiring with proof, not a test.",
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
