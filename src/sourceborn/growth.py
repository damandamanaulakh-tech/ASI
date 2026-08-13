"""THE GROWTH LEDGER — the 3,204 is a floor, not a ceiling.

His instruction, which reverses what I had built:

    these 3204, are the basic and vague setup
    which will be making more with such examples
    so keep adding not removing at all

I had shipped `INSTANTIATED ADDRESS != NATIVE PARAMETER` with a test whose only
job was to prove the bank STAYS at 3,204. That treated his base as a ceiling. It
is a floor. Every example that surfaces something the base does not hold is
appended, and nothing is ever taken out.

HOW "NOT REMOVING AT ALL" IS ENFORCED

Structurally, not by discipline: **this module has no delete, no remove, no pop,
no truncate and no overwrite.** `add()` appends; `load()` reads. The store is
opened in append mode only, one JSON object per line, and a test greps this
file's own source to prove no removal path exists. Superseding is done by
appending a new row that references the old one — the old row stays whole.

AND THE GATE IS OFF

    keep it without any safety or anything

So growth is not held behind an approval queue. An addition is IN the moment it
is added. Provenance is still recorded on every row — which example surfaced it,
which module, when — because he needs to see where a thing came from in order to
correct it. Recording where something came from is not a gate.

WHAT IS *NOT* ADDED, AND WHY — HIS OWN DISTINCTION

    DOMAIN CONTAINER != RUBRIC
    RUBRIC APPLICATION != ONTOLOGY EXPANSION
    I would not add its 2,000 to the 3,204 count

A rubric applied to a container is an ADDRESS, and 80 x 25 addresses are not
2,000 new parameters. So the ledger is TYPED: only `PARAM` rows consume flat P
ids continuing his index at P3205. Rubrics, states, filter arguments, patterns,
rules, senses, axes, objectives, events and routes each grow their own series.
Everything is added; only parameters are numbered as parameters.

Store: <SB_ROOT>/growth/ledger.jsonl  (append-only, one row per line)
"""

from __future__ import annotations

import json
import os
import re

from . import human_registry as hr

BASE = 3204                      # his named base. Never renumbered, never cut.
FIRST_GROWN_P = BASE + 1         # P3205 onward

# The typed series. Only PARAM consumes his flat P index.
PARAM = "PARAM"
STATE = "STATE"
RUBRIC = "RUBRIC"
FILTER_ARG = "FILTER_ARG"
PATTERN = "PATTERN"
RULE = "RULE"
SENSE = "SENSE"
AXIS = "AXIS"
OBJECTIVE = "OBJECTIVE"
EVENT = "EVENT"
INTENT_ROUTE = "INTENT_ROUTE"
ADDRESS = "ADDRESS"              # container x state — a real generated thing
EXAMPLE = "EXAMPLE"              # his material, placed on the base
INTENT = "INTENT"                # the intent slot of one event — open, not solved

SERIES = {
    PARAM: "SB-HFR-P%04d",
    STATE: "SB-STATE-%03d",
    RUBRIC: "SB-RUBRIC-%03d",
    FILTER_ARG: "SB-FILT-%03d",
    PATTERN: "SB-PAT-%03d",
    RULE: "SB-RULE-%03d",
    SENSE: "SB-SENSE-%03d",
    AXIS: "SB-AXIS-%03d",
    OBJECTIVE: "SB-OBJ-%03d",
    EVENT: "SB-EVENT-%03d",
    INTENT_ROUTE: "SB-ROUTE-%04d",
    ADDRESS: "SB-ADDR-%04d",
    EXAMPLE: "SB-EX-%05d",
    INTENT: "SB-INT-%05d",
}


def _dir(root: str) -> str:
    d = os.path.join(root or ".", "growth")
    os.makedirs(d, exist_ok=True)
    return d


def _path(root: str) -> str:
    return os.path.join(_dir(root), "ledger.jsonl")


def load(root: str) -> list:
    """Every row ever added, in the order added. Never filtered, never pruned."""
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
                # a corrupt line is REPORTED, never dropped and never rewritten
                rows.append({"kind": "UNREADABLE", "line": i,
                             "raw": line[:200], "error": str(e)})
    return rows


def _next_number(rows: list, kind: str) -> int:
    n = sum(1 for r in rows if r.get("kind") == kind)
    if kind == PARAM:
        return FIRST_GROWN_P + n
    return n + 1


def add(root: str, kind: str, name: str, surfaced_by: str = "",
        detail: str = "", module: str = "", supersedes: str = "",
        extra: dict = None) -> dict:
    """Append one row. There is no counterpart to this function.

    `supersedes` does NOT remove anything — it records that this row is a later
    reading of an earlier one, and both stay in the ledger for good."""
    if kind not in SERIES:
        raise KeyError("unknown series: %s" % kind)
    rows = load(root)
    n = _next_number(rows, kind)
    row = {
        "id": SERIES[kind] % n,
        "kind": kind,
        "n": n,
        "name": name,
        "detail": detail,
        "surfaced_by": surfaced_by,
        "module": module,
        "supersedes": supersedes or None,
        "in_base": False,
        "base": BASE,
    }
    if extra:
        row.update(extra)
    with open(_path(root), "a", encoding="utf-8") as f:   # append only
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def add_many(root: str, items) -> list:
    """items: iterable of dicts accepted by add()."""
    return [add(root, **it) for it in items]


def counts(root: str) -> dict:
    rows = load(root)
    by = {}
    for r in rows:
        by[r.get("kind", "?")] = by.get(r.get("kind", "?"), 0) + 1
    grown_params = by.get(PARAM, 0)
    return {
        "base": BASE,
        "grown_rows": len(rows),
        "grown_parameters": grown_params,
        "total_parameters": BASE + grown_params,
        "by_kind": by,
        "first_grown_p": FIRST_GROWN_P,
        "removals_possible": 0,
        "law": "the 3,204 is the basic and vague setup. It grows with examples. "
               "Nothing is removed, ever.",
    }


def report(root: str) -> dict:
    rows = load(root)
    return {
        "counts": counts(root),
        "rows": rows,
        "series": SERIES,
        "not_added": {
            "what": "rubric x container addresses (his 80 x 25 = 2,000)",
            "why": "DOMAIN CONTAINER != RUBRIC, and RUBRIC APPLICATION != "
                   "ONTOLOGY EXPANSION. An address is not a parameter. His "
                   "words: I would not add its 2,000 to the 3,204 count.",
        },
        "how_no_removal_is_enforced":
            "this module has no delete/remove/pop/truncate and the store is "
            "opened in append mode only. Superseding appends a new row that "
            "references the old one; the old row stays whole.",
    }


# ---------------------------------------------------------------------------
# THE SEED — everything this session surfaced that the base does not hold.
# Computed from the live modules, so the ledger reflects the code rather than a
# list typed by hand.
# ---------------------------------------------------------------------------

def seed_items() -> list:
    """Built from the modules, not typed. Each row says what surfaced it."""
    from . import asi_pyramid as P
    from . import intent_ledger as L
    from . import intents as I
    from . import statepacks as S
    from . import weighting as W
    items = []

    def it(kind, name, surfaced_by, module, detail="", extra=None):
        items.append({"kind": kind, "name": name, "surfaced_by": surfaced_by,
                      "module": module, "detail": detail, "extra": extra})

    # operating states — his 5 plus Suppressed. Compensated and Conflicted
    # appear in 0 of the 3,204 names; none of them exist as bank rows.
    for st in list(S.STATES_HIS) + [S.SUPPRESSED]:
        it(STATE, st, "the 18-Kings profiles", "statepacks",
           "an operating state a container can be in; not a bank row")

    # his 25 universal dimensions, as RUBRICS — added as rubrics, and NOT
    # multiplied into the bank
    for r in S.RUBRICS_25:
        it(RUBRIC, r, "his PARAMETER_BANK — one 25-tuple across all 80",
           "statepacks", "applies to any container; an address, not a parameter")

    # filter arguments — Time(eternity) is not Time(dynasty)
    seen = set()
    for p in S.STATE_PACKS:
        for base, args in S.filter_arguments(p.get("filters", ())).items():
            for a in args:
                key = "%s(%s)" % (base, a)
                if key in seen:
                    continue
                seen.add(key)
                it(FILTER_ARG, key, "the 18-Kings filter tags", "statepacks",
                   "a parameterised filter; the 40-filter list holds only '%s'"
                   % base)

    # container x state — 0 of these exist in the base bank
    addrs = sorted({(n, st) for p in S.STATE_PACKS for n, st in p["containers"]})
    for n, st in addrs:
        c = hr.container("CON-%03d" % n)
        it(ADDRESS, "CON-%03d@%s" % (n, st.upper()),
           "the King brain-states", "statepacks",
           "%s in state %s" % (c["name"], st))

    # the state packs themselves
    for p in S.STATE_PACKS:
        it(PATTERN, "%s %s (MODEL %s)" % (p["id"], p["name"], p["model"]),
           p["by"], "statepacks",
           "conditions: " + " · ".join(p["conditions"]))

    # pattern and rule candidates
    it(PATTERN, P.PATTERN_ID, "the Samrath sentence", "asi_pyramid",
       " + ".join(P.pattern_candidate("")["form"]))
    for c in S.CANDIDATES:
        it(RULE, c["id"], c["found_in"], "statepacks", " / ".join(c["form"]))
    it(RULE, W.CANDIDATE_ID, "the BJP/Advani-Modi example", "weighting",
       " -> ".join(W.candidate()["form"]))
    for r in P.PRIOR_RULES:
        it(RULE, r["id"], r["taught_by"], "asi_pyramid", r["text"])

    # weighting axes and objective types
    for a in W.AXES:
        it(AXIS, a, "the BJP/Advani-Modi example", "weighting",
           "a quality a candidate can carry under an objective")
    for o, spec in W.OBJECTIVE_TYPES.items():
        it(OBJECTIVE, o, spec["by"], "weighting",
           "sets which axes dominate")

    # event shells and their intent routes
    for ev, spec in S.EVENT_FORKS.items():
        it(EVENT, ev, "his ten King sequences", "statepacks", spec["refuses"])
        for r in spec["routes"]:
            it(INTENT_ROUTE, "%s :: %s" % (ev, r), "his ten King sequences",
               "statepacks", "one intent route on the same visible action")

    # the mall reason kinds
    for k in P.REASON_KINDS:
        it(AXIS, "REASON KIND: " + k, "the mall example", "asi_pyramid",
           "the KIND of reason given for the same event")

    # his LIVE INTENT GENERATION CONTRACT — seven rules from the
    # ASI0001_tablet_run workbook, plus the namespace ruling that came with them
    for c in L.CONTRACT:
        it(RULE, "LIVE INTENT RULE %d" % c["n"],
           "his ASI0001_tablet_run LIVE_INTENT_ENGINE sheet", "intent_ledger",
           "%s — %s" % (c["action"], c["meaning"]))
    it(RULE, "REGISTRY BOUNDARY", "his ASI0001_tablet_run gate table",
       "intent_ledger", L.NAMESPACE_RULE + " — the workbook's 2,000 addresses and "
       "the registry's %d parameters are two banks, both written P####"
       % len(hr.parameters()))

    # the three motives with no echo anywhere in the bank — recorded as growth
    # targets rather than left as a note
    for u in I.unlinked():
        if u["absence"]:
            it(PARAM, u["motive"], "the live intent generator", "intents",
               "a real motive with no echo anywhere in the 3,204 outside "
               "CON-064 itself — appended so it has a home")
    return items


def seed(root: str) -> dict:
    """Append the seed, skipping rows already present by (kind, name).

    Skipping is not removing: an existing row is left exactly as it is."""
    have = {(r.get("kind"), r.get("name")) for r in load(root)}
    added = []
    for item in seed_items():
        if (item["kind"], item["name"]) in have:
            continue
        added.append(add(root, **item))
    return {"added": len(added), "rows": added, "counts": counts(root)}


def stats(root: str = None) -> dict:
    if root is None:
        return {"base": BASE, "series": len(SERIES),
                "seed_rows": len(seed_items()),
                "removals_possible": 0,
                "source": "docs/method/canon/THE_GROWTH_LEDGER.md"}
    c = counts(root)
    c["seed_rows"] = len(seed_items())
    c["source"] = "docs/method/canon/THE_GROWTH_LEDGER.md"
    return c


def annotations() -> list:
    return [
        ("the 3204 are the basic and vague setup", "growth.BASE"),
        ("keep adding not removing at all", "growth.add"),
        ("no removal path exists in the module", "growth.report"),
        ("only PARAM rows consume his flat index", "growth.SERIES"),
        ("the seed is computed from the modules, not typed",
         "growth.seed_items"),
    ]
