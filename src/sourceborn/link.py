"""THE LINK LAYER — relations between rows, first-class and counted.

PHASE 10. His ask, and his own worked example:

    links between sub-parameters become first-class, counted and named.
    Diamond cut diamond becomes a stored link between two ego-rows.

and, on the layer's count in his twelve-layer table:

    Link — counted from the split bank

WHY A LINK IS NOT A ROW

A row is a faculty: one thing a human does, living in one container. A LINK is
not a faculty — it is a relation between two of them, and it belongs to neither
end. `Dominance motive` is a row. **Two people both running `Dominance motive`
at each other** is not a row and cannot be made one: it has no home container,
because it is not located in either party. It is located in the MEETING.

That is his diamond, exactly: *"its ego cut ego"* — and his own archetype says
the immovability is **a property of the meeting, not of either party**. A layer
that can only hold rows cannot say that sentence at all.

COUNTED FROM THE SPLIT BANK, NOT TYPED

Three of the four link types are COMPUTED over the live split and the live
archetype layer. Nothing is hand-listed, so the count follows the bank instead
of drifting from it:

  SPLIT_SIBLING     two rows that came out of one source row when it was split.
                    `Fluid` and `osmotic balance` were one row, P0003, and the
                    fact that they were once one thing is real information that
                    the split otherwise throws away. 284 pairs from 275 parents.

  SHARED_NAME       the same row name in two different containers. Reported by
                    the split review as SPLIT-05 and left undecided there; here
                    each is a link, which is what an undecided duplicate
                    actually is — two rows that may be one faculty seen twice.
                    89 pairs across 83 names.

  ARCHETYPE_REACH   two rows the same archetype reaches. This is the layer's
                    generative edge: the archetype found a relation between
                    rows in different containers that no container could hold.
                    619 pairs over 11 archetypes.

  SYMMETRIC_MEETING HIS, hand-given, and the one that needed a human: a row lit
                    on BOTH parties at once. There is no computation that finds
                    this, because both ends are the same row.

NOTHING IS CONCLUDED. A link that fires says a relation is available, names its
two ends and its evidence, and stops. It never says the relation held.

NO CEILING. His ruling on this layer with ARCHETYPE and SCALE: *no count, its
open to increase*.
"""

from __future__ import annotations

SPLIT_SIBLING = "SPLIT_SIBLING"
SHARED_NAME = "SHARED_NAME"
ARCHETYPE_REACH = "ARCHETYPE_REACH"
SYMMETRIC_MEETING = "SYMMETRIC_MEETING"

TYPES = {
    SPLIT_SIBLING: {
        "means": "two rows that came out of one source row when it was split",
        "symmetric": True,
        "by": "COMPUTED over the split bank",
        "keeps": "that they were once one thing — information the split would "
                 "otherwise throw away",
    },
    SHARED_NAME: {
        "means": "the same row name standing in two different containers",
        "symmetric": True,
        "by": "COMPUTED over the split bank",
        "keeps": "an open question, not an answer: they may be one faculty "
                 "seen twice or two real rows. The link is what an undecided "
                 "duplicate actually is.",
    },
    ARCHETYPE_REACH: {
        "means": "two rows the same archetype reaches",
        "symmetric": True,
        "by": "COMPUTED over the archetype layer",
        "keeps": "a relation across containers that no container can hold — "
                 "the archetype found it, and this is where it is stored",
    },
    SYMMETRIC_MEETING: {
        "means": "one row lit on BOTH parties at once — the relation is "
                 "located in the meeting, not in either party",
        "symmetric": True,
        "by": "HIS — hand-given",
        "keeps": "the reading his diamond needs. No computation finds this, "
                 "because both ends are the same row.",
    },
}

#: His own links, given by hand with his words on them. These are the ones no
#: sweep over the bank could produce.
HIS_LINKS = (
    {
        "name": "DIAMOND CUT DIAMOND",
        "type": SYMMETRIC_MEETING,
        "his_words": "its ego cut ego",
        "source": "his own worked teaching; ARCH-004",
        "ends": [("SB-HFR-P2550", "Dominance motive", "CON-064"),
                 ("SB-HFR-P2550", "Dominance motive", "CON-064")],
        "reading": "the SAME row is running on both parties, and neither will "
                   "yield because yielding is the one thing the row does not "
                   "do. What follows is a property of the meeting: an outcome "
                   "neither party's own reading predicts.",
        "refuses": "never read it as one person being strong. If one side "
                   "would yield under pressure this link is not present.",
        "also_lights": [("SB-HFR-P2264", "Pride", "CON-057"),
                        ("SB-HFR-P2555", "Identity-protection motive", "CON-064"),
                        ("SB-HFR-P2556", "Face-saving motive", "CON-064"),
                        ("SB-HFR-P2672", "Dominance (trait)", "CON-067"),
                        ("SB-HFR-P2824", "Dominance signalling", "CON-071")],
        "triggers": ["diamond cut diamond", "diamond cuts diamond",
                     "ego cut ego", "neither would back down",
                     "both refused", "neither will yield"],
    },
)

#: His ruling, given with ARCHETYPE and SCALE.
CEILING = None


def _rows():
    from . import sbx
    return sbx.rows()


def _container_of(row_id: str) -> str:
    """`SBX-CON-056-13` -> `SBX-CON-056`."""
    return row_id.rsplit("-", 1)[0]


def _pairs(group: list) -> list:
    out = []
    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            out.append((group[i], group[j]))
    return out


def computed() -> list:
    """Every link the bank itself carries. Counted from the split, never typed."""
    import collections
    from . import archetype as A
    rs = _rows()
    out = []

    by_parent = collections.defaultdict(list)
    for r in rs:
        by_parent[r["from_row"]].append(r)
    for parent, group in sorted(by_parent.items()):
        if len(group) < 2:
            continue
        for a, b in _pairs(group):
            out.append({
                "type": SPLIT_SIBLING,
                "ends": [{"id": a["id"], "name": a["name"],
                          "container": _container_of(a["id"])},
                         {"id": b["id"], "name": b["name"],
                          "container": _container_of(b["id"])}],
                "evidence": {"shared_parent": parent,
                             "parent_name": a.get("from_name")},
                "by": "COMPUTED",
            })

    by_name = collections.defaultdict(list)
    for r in rs:
        by_name[r["name"]].append(r)
    for name, group in sorted(by_name.items()):
        if len({_container_of(r["id"]) for r in group}) < 2:
            continue
        for a, b in _pairs(group):
            if _container_of(a["id"]) == _container_of(b["id"]):
                continue
            out.append({
                "type": SHARED_NAME,
                "ends": [{"id": a["id"], "name": a["name"],
                          "container": _container_of(a["id"])},
                         {"id": b["id"], "name": b["name"],
                          "container": _container_of(b["id"])}],
                "evidence": {"shared_name": name},
                "by": "COMPUTED",
            })

    for arch in A.archetypes():
        for (pa, na, ca), (pb, nb, cb) in _pairs(list(arch["reaches"])):
            out.append({
                "type": ARCHETYPE_REACH,
                "ends": [{"id": pa, "name": na, "container": ca},
                         {"id": pb, "name": nb, "container": cb}],
                "evidence": {"archetype": arch["id"],
                             "archetype_name": arch["name"]},
                "by": "COMPUTED",
            })
    return out


def his() -> list:
    """His hand-given links, with his words on them."""
    out = []
    for l in HIS_LINKS:
        out.append({
            "type": l["type"],
            "name": l["name"],
            "his_words": l["his_words"],
            "source": l["source"],
            "ends": [{"id": p, "name": n, "container": c}
                     for p, n, c in l["ends"]],
            "also_lights": [{"id": p, "name": n, "container": c}
                            for p, n, c in l["also_lights"]],
            "reading": l["reading"],
            "refuses": l["refuses"],
            "triggers": list(l["triggers"]),
            "evidence": {"given_by": "him"},
            "by": "HIS",
        })
    return out


def links() -> list:
    """The whole layer, with ids. HIS links lead — new in front, and his in
    front of anything computed."""
    out = []
    for i, l in enumerate(his() + computed(), 1):
        out.append(dict(l, id="SBX-LNK-%05d" % i))
    return out


def get(lid: str) -> dict:
    lid = (lid or "").strip().upper()
    return next((l for l in links() if l["id"] == lid),
                {"found": False, "id": lid})


def of(row_id: str) -> list:
    """Every link one row stands in."""
    row_id = (row_id or "").strip()
    return [l for l in links() if any(e["id"] == row_id for e in l["ends"])]


def fires_on(text: str) -> dict:
    """THE PROOF THIS LAYER EXISTS FOR: a reading no row alone can give.

    His links carry triggers. When one fires, the reading it returns is a
    statement about the MEETING — which is not stored in either end and cannot
    be, because neither container owns it. Nothing is concluded: the link says
    the relation is available and names its evidence."""
    import re
    low = " " + (text or "").lower() + " "
    fired = []
    for l in links():
        if l["by"] != "HIS":
            continue
        hit = [t for t in l.get("triggers", ()) if re.search(t, low)]
        if hit:
            fired.append(dict(l, matched_on=hit))
    return {
        "text": text,
        "fired": fired,
        "fired_count": len(fired),
        "readings": [{"link": f["id"], "name": f["name"],
                      "reading": f["reading"], "refuses": f["refuses"],
                      "his_words": f["his_words"],
                      "rows": [e["id"] for e in f["ends"]],
                      "also_lights": [e["id"] for e in f["also_lights"]]}
                     for f in fired],
        "concluded": None,
        "law": "the reading belongs to the MEETING and is stored in neither "
               "end. That is why it is a link and not a row.",
    }


def verify() -> dict:
    """Every row id a link names must be a real row.

    Computed links name split rows and are true by construction. HIS links
    name SOURCE rows, which he gave by hand — those are the ones that can be
    wrong, so they are checked against the live registry."""
    from . import asi_pyramid as AP
    flat, _ = AP._flat()
    by_id = {r["sb_id"]: r for r in flat}
    bad, checked = [], 0
    for l in his():
        for e in list(l["ends"]) + list(l["also_lights"]):
            checked += 1
            row = by_id.get(e["id"])
            if row is None:
                bad.append({"link": l["name"], "id": e["id"],
                            "problem": "not in the bank"})
            elif row["name"].strip().lower() != e["name"].strip().lower():
                bad.append({"link": l["name"], "id": e["id"],
                            "claimed": e["name"], "bank_says": row["name"]})
            elif row["container"] != e["container"]:
                bad.append({"link": l["name"], "id": e["id"],
                            "claimed": e["container"],
                            "bank_says": row["container"]})
    split_ids = {r["id"] for r in _rows()}
    dangling = [l["id"] for l in links() if l["by"] == "COMPUTED"
                and l["type"] in (SPLIT_SIBLING, SHARED_NAME)
                and any(e["id"] not in split_ids for e in l["ends"])]
    return {"his_row_ids_checked": checked, "problems": bad,
            "ok": not bad and not dangling,
            "dangling_computed_links": len(dangling)}


def stats() -> dict:
    import collections
    ls = links()
    by_type = collections.Counter(l["type"] for l in ls)
    return {
        "links": len(ls),
        "ceiling": CEILING,
        "by_type": dict(sorted(by_type.items())),
        "his": sum(1 for l in ls if l["by"] == "HIS"),
        "computed": sum(1 for l in ls if l["by"] == "COMPUTED"),
        "rows_touched": len({e["id"] for l in ls for e in l["ends"]}),
        "types": {k: v["means"] for k, v in TYPES.items()},
        "law": "counted from the split bank — his own note on this layer. "
               "Nothing is hand-listed except the links he gave by hand, so "
               "the count follows the bank instead of drifting from it.",
        "never": "a link creates no parameter and concludes no relation held.",
    }


def annotations() -> list:
    return [
        ("links between sub-parameters become first-class, counted and named",
         "link.links"),
        ("diamond cut diamond is a link between two ego-rows", "link.HIS_LINKS"),
        ("counted from the split bank", "link.computed"),
        ("the reading belongs to the meeting, not to either end",
         "link.fires_on"),
        ("no count, open to increase", "link.CEILING"),
    ]
