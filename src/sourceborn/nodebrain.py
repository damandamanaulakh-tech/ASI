"""PHASE A — THE NODE SCHEMA, LOCKED.

From his SELF-SUSTAINING EXECUTION FLOW sheet, box 3 (NODE BRAIN), box 4 (MEMORY
BRAIN write/read conditions), box 6 (automatic link creation) and Phase A of his
own build proposal:

    Phase A — Registries + IDs -> lock node schema, IDs, headers, ledgers

WHY THIS IS FIRST, AND WHY IT IS ONLY THIS

His Phase A comes before the runtime, the combination engine, the memory graph
and the scheduler. That ordering is not cosmetic. Every later phase WRITES INTO
this shape, so a field added or renamed after Phase D would invalidate every edge
already stored. Locking the schema first is what makes the later phases safe to
build; it is also the reason this module deliberately does almost nothing.

    THIS MODULE DOES:      define the node, the id, the links, the memory kinds,
                           the write and read conditions, and a lock that makes a
                           silent change impossible.

    THIS MODULE DOES NOT:  link anything, write anything, trigger anything,
                           promote anything, or touch growth.add. Those are his
                           phases B through E.

WHAT "LOCKED" MEANS HERE — NOT A COMMENT, A CHECK

`fingerprint()` hashes the whole schema: every node type, every field and its
required flag, every link type and its direction, every status, every memory
kind, and both condition lists. A test pins that hash. Change any of it without
bumping `SCHEMA_VERSION` and the test fails and names what moved.

That is the same technique stage 1 SOURCE LOCK still lacks — it is PARTIAL today
precisely because raw source is preserved by discipline rather than by a
checksum. This is what the fix looks like when it is real.

THE NAMESPACE PROBLEM, SURFACED AND NOT RESOLVED

Five of his twelve node types share a NAME with one of the growth ledger's
seventeen series: STATE, EVENT, PATTERN, RULE, INTENT. **A shared name is not
evidence that they are the same thing.** His growth `STATE` rows are operating
states (Dominant, Active, Compensated...); a node of type `STATE` on this sheet
is an active-state node in a sequence. They may be the same family or they may
not.

His own ruling on exactly this shape — *do not silently merge namespaces* — has
already bitten twice: the workbook's 2,000 `WB-P` addresses against the
registry's 3,204 `SB-HFR-P` parameters, and workbook segment `S04` against
registry `SEG-04`. So node ids live in their own prefix (`SB-N-`), nothing is
merged, and `collisions()` reports all five for him to rule on.
"""

from __future__ import annotations

import hashlib
import json

SCHEMA_VERSION = "A.1"

# ---------------------------------------------------------------------------
# THE TWELVE NODE TYPES — his box 3, verbatim, with the id stem each one uses.
# ---------------------------------------------------------------------------

NODE_TYPES = (
    {"type": "STATE", "stem": "STA", "is": "an active state a node is in"},
    {"type": "EVENT", "stem": "EVT", "is": "something that happened"},
    {"type": "ACTOR", "stem": "ACT", "is": "someone or something that acts"},
    {"type": "INTENT", "stem": "INT", "is": "the reason pushing an event"},
    {"type": "RELATION", "stem": "REL", "is": "a named tie between two nodes"},
    {"type": "PATTERN", "stem": "PAT", "is": "an arrangement that recurs"},
    {"type": "RULE", "stem": "RUL", "is": "a standing constraint"},
    {"type": "SEQUENCE", "stem": "SEQ", "is": "an ordered dependency of events"},
    {"type": "ARTIFACT", "stem": "ART", "is": "an object the world left behind"},
    {"type": "MEMORY", "stem": "MEM", "is": "what a node has seen before"},
    {"type": "CONTRADICTION", "stem": "CON",
     "is": "two readings that cannot both stand"},
    {"type": "FUTURE_STATE", "stem": "FUT",
     "is": "a state something was working toward"},
)

TYPES = tuple(t["type"] for t in NODE_TYPES)
_STEM = {t["type"]: t["stem"] for t in NODE_TYPES}

# ---------------------------------------------------------------------------
# STATUS — his four, and their meanings kept apart.
# ---------------------------------------------------------------------------

ACCEPTED, PARTIAL, OPEN, REJECTED = "ACCEPTED", "PARTIAL", "OPEN", "REJECTED"
STATUSES = (ACCEPTED, PARTIAL, OPEN, REJECTED)

STATUS_MEANS = {
    ACCEPTED: "it passed the gates and became a reusable brain unit",
    PARTIAL: "some of it holds and some does not; both halves are kept",
    OPEN: "nothing has settled it. A valid resting place, not a failure",
    REJECTED: "it was ruled against. The row stays, with the reason",
}

# ---------------------------------------------------------------------------
# THE FIELDS — his box 3, in his order. `required` is enforced at construction.
# ---------------------------------------------------------------------------

FIELDS = (
    {"field": "node_id", "required": True,
     "is": "stable identity, assigned once, never reused"},
    {"field": "node_type", "required": True, "is": "one of the twelve"},
    {"field": "point_zero_ref", "required": True,
     "is": "the raw source this node came from. REQUIRED because his own rule "
           "is: no invention before source lock."},
    {"field": "event_ref", "required": False, "is": "the event it belongs to"},
    {"field": "intent_ref", "required": False, "is": "the intent it carries"},
    {"field": "state_ref", "required": False, "is": "the active state it sits in"},
    {"field": "evidence_ref", "required": False,
     "is": "what was predicted or found for it"},
    {"field": "maturity_level", "required": True,
     "is": "a maturity.py state — never a bare number"},
    {"field": "proof_debt", "required": True,
     "is": "the origin distance owed, 0..5"},
    {"field": "status", "required": True, "is": "one of the four"},
    {"field": "local_memory", "required": False,
     "is": "this node's own chain of readings"},
    {"field": "parent_links", "required": False, "is": "what it came from"},
    {"field": "child_links", "required": False, "is": "what came from it"},
    {"field": "similarity_links", "required": False, "is": "what resembles it"},
    {"field": "contradiction_links", "required": False,
     "is": "what it cannot stand beside"},
    {"field": "sequence_position", "required": False,
     "is": "where it sits in its sequence"},
)

FIELD_NAMES = tuple(f["field"] for f in FIELDS)
REQUIRED = tuple(f["field"] for f in FIELDS if f["required"])
LINK_FIELDS = ("parent_links", "child_links", "similarity_links",
               "contradiction_links")

# ---------------------------------------------------------------------------
# THE TEN LINK TYPES — his box 6. Direction and inverse are part of the type,
# because `produced_by` and `contradicts` are not the same shape of tie and a
# graph that cannot tell them apart is a similarity blob.
# ---------------------------------------------------------------------------

LINK_TYPES = (
    {"link": "produced_by", "dir": "one-way", "inverse": "produced",
     "goes_in": "parent_links",
     "is": "this node exists because that one did"},
    {"link": "depends_on", "dir": "one-way", "inverse": "supports_existence_of",
     "goes_in": "parent_links",
     "is": "this node cannot stand if that one falls"},
    {"link": "supports", "dir": "one-way", "inverse": "supported_by",
     "goes_in": "child_links",
     "is": "this node is evidence for that one"},
    {"link": "contradicts", "dir": "mutual", "inverse": "contradicts",
     "goes_in": "contradiction_links",
     "is": "both cannot stand. Neither is deleted."},
    {"link": "similar_to", "dir": "mutual", "inverse": "similar_to",
     "goes_in": "similarity_links",
     "is": "they share shape without either causing the other"},
    {"link": "before", "dir": "one-way", "inverse": "after",
     "goes_in": "child_links", "is": "sequence order, not necessarily time"},
    {"link": "after", "dir": "one-way", "inverse": "before",
     "goes_in": "parent_links", "is": "the inverse of before"},
    {"link": "contains", "dir": "one-way", "inverse": "part_of",
     "goes_in": "child_links", "is": "whole to part"},
    {"link": "actor_of", "dir": "one-way", "inverse": "acted_on",
     "goes_in": "parent_links", "is": "who did it, to what"},
    {"link": "future_of", "dir": "one-way", "inverse": "result_of",
     "goes_in": "child_links",
     "is": "the state this was working toward"},
)

LINKS = tuple(l["link"] for l in LINK_TYPES)
_LINK = {l["link"]: l for l in LINK_TYPES}

# ---------------------------------------------------------------------------
# THE ELEVEN MEMORY KINDS — his box 4.
# ---------------------------------------------------------------------------

MEMORY_KINDS = (
    "RAW", "EVENT", "INTENT", "RELATION", "PATH", "PATTERN", "EVIDENCE",
    "CONTRADICTION", "ACTOR_STATE", "SEQUENCE", "GLOBAL_INDEX",
)

# His five write conditions and six read conditions. Defined here as the
# contract; ENFORCING them at the write site is his Phase D, not this one.
WRITE_CONDITIONS = (
    "source retained", "R-F-R executed", "status assigned",
    "link map created", "origin distance recorded",
)

READ_CONDITIONS = (
    "similar event", "same actor", "same pattern", "same artifact family",
    "same contradiction", "same future-state goal",
)

# ---------------------------------------------------------------------------
# THE LOCK.
# ---------------------------------------------------------------------------

def schema() -> dict:
    """The whole shape, in one object. This is what gets hashed."""
    return {
        "version": SCHEMA_VERSION,
        "node_types": [dict(t) for t in NODE_TYPES],
        "fields": [dict(f) for f in FIELDS],
        "statuses": list(STATUSES),
        "link_types": [dict(l) for l in LINK_TYPES],
        "memory_kinds": list(MEMORY_KINDS),
        "write_conditions": list(WRITE_CONDITIONS),
        "read_conditions": list(READ_CONDITIONS),
    }


def fingerprint() -> str:
    """A stable hash of the schema. Change anything, this moves.

    Sorted and separator-fixed so the hash depends on the CONTENT and not on
    dict ordering or whitespace."""
    blob = json.dumps(schema(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def lock() -> dict:
    return {
        "version": SCHEMA_VERSION,
        "fingerprint": fingerprint(),
        "node_types": len(NODE_TYPES), "fields": len(FIELDS),
        "link_types": len(LINK_TYPES), "memory_kinds": len(MEMORY_KINDS),
        "statuses": len(STATUSES),
        "write_conditions": len(WRITE_CONDITIONS),
        "read_conditions": len(READ_CONDITIONS),
        "how_it_locks": "a test pins this fingerprint. Change a field, a type, a "
                        "link or a condition without bumping SCHEMA_VERSION and "
                        "the test fails and names what moved.",
        "why_first": "every later phase writes into this shape. A field renamed "
                     "after the graph exists would invalidate every edge already "
                     "stored.",
    }


# ---------------------------------------------------------------------------
# IDs — their own prefix, so they can never be read as bank or ledger ids.
# ---------------------------------------------------------------------------

ID_PREFIX = "SB-N"


def make_id(node_type: str, n: int) -> str:
    """`SB-N-EVT-00001`. The prefix is deliberate: `SB-HFR-P####` is the bank and
    `SB-EX-#####`/`SB-STEP-####` are ledger series. This is neither."""
    t = (node_type or "").strip().upper()
    if t not in _STEM:
        raise KeyError("unknown node type: %s" % node_type)
    if n < 1:
        raise ValueError("node numbers start at 1")
    return "%s-%s-%05d" % (ID_PREFIX, _STEM[t], n)


def parse_id(node_id: str) -> dict:
    parts = (node_id or "").split("-")
    if len(parts) != 4 or "-".join(parts[:2]) != ID_PREFIX:
        return {"valid": False, "why": "not an %s id" % ID_PREFIX}
    stem, num = parts[2], parts[3]
    types = [t for t, s in _STEM.items() if s == stem]
    if not types or not num.isdigit():
        return {"valid": False, "why": "unknown stem or non-numeric sequence"}
    return {"valid": True, "node_type": types[0], "n": int(num),
            "prefix": ID_PREFIX}


# ---------------------------------------------------------------------------
# CONSTRUCTION AND VALIDATION — a malformed node is refused, with the reason.
# ---------------------------------------------------------------------------

def new_node(node_type: str, n: int, point_zero_ref: str, status: str = OPEN,
             maturity_level: str = "UNTESTED", proof_debt: int = 0,
             **optional) -> dict:
    """Build one node against the locked schema.

    Refuses rather than storing something malformed — a node that does not
    satisfy the schema is not a weaker node, it is a different shape, and the
    whole point of Phase A is that there is only one shape."""
    t = (node_type or "").strip().upper()
    node = {f: None for f in FIELD_NAMES}
    for lf in LINK_FIELDS:
        node[lf] = []
    node["local_memory"] = []
    node.update({
        "node_id": make_id(t, n), "node_type": t,
        "point_zero_ref": point_zero_ref,
        "maturity_level": maturity_level, "proof_debt": proof_debt,
        "status": status,
    })
    for k, v in optional.items():
        if k not in FIELD_NAMES:
            raise KeyError("not a schema field: %s" % k)
        node[k] = v
    node["schema_version"] = SCHEMA_VERSION
    v = validate(node)
    if not v["valid"]:
        raise ValueError("; ".join(v["problems"]))
    return node


def validate(node: dict) -> dict:
    """Every failure named. Never a bare False."""
    problems = []
    unknown = [k for k in node
               if k not in FIELD_NAMES and k != "schema_version"]
    if unknown:
        problems.append("fields not in the schema: %s" % ", ".join(sorted(unknown)))
    for f in REQUIRED:
        if node.get(f) in (None, ""):
            problems.append("missing required field: %s" % f)
    t = node.get("node_type")
    if t and t not in TYPES:
        problems.append("node_type %r is not one of the twelve" % t)
    s = node.get("status")
    if s and s not in STATUSES:
        problems.append("status %r is not one of the four" % s)
    pd = node.get("proof_debt")
    if pd is not None and not (isinstance(pd, int) and 0 <= pd <= 5):
        problems.append("proof_debt must be 0..5, got %r" % pd)
    nid = node.get("node_id")
    if nid:
        p = parse_id(nid)
        if not p["valid"]:
            problems.append("node_id: %s" % p["why"])
        elif t and p["node_type"] != t:
            problems.append("node_id stem says %s but node_type says %s"
                            % (p["node_type"], t))
    for lf in LINK_FIELDS:
        if node.get(lf) is not None and not isinstance(node[lf], list):
            problems.append("%s must be a list" % lf)
    return {"valid": not problems, "problems": problems,
            "checked": len(FIELD_NAMES)}


def link(from_node: dict, link_type: str, to_id: str) -> dict:
    """Attach one TYPED link. Returns the node with the link added.

    Phase A defines and validates links; it does not go looking for them. Finding
    which nodes should be linked is his Phase D."""
    lt = (link_type or "").strip().lower()
    if lt not in _LINK:
        raise KeyError("unknown link type: %s (the ten are %s)"
                       % (link_type, ", ".join(LINKS)))
    spec = _LINK[lt]
    if not parse_id(to_id)["valid"]:
        raise ValueError("link target is not a node id: %s" % to_id)
    out = dict(from_node)
    field = spec["goes_in"]
    out[field] = list(out.get(field) or [])
    out[field].append({"link": lt, "to": to_id, "direction": spec["dir"],
                       "inverse": spec["inverse"]})
    return out


def inverse_of(link_type: str) -> str:
    lt = (link_type or "").strip().lower()
    if lt not in _LINK:
        raise KeyError("unknown link type: %s" % link_type)
    return _LINK[lt]["inverse"]


# ---------------------------------------------------------------------------
# THE NAMESPACE COLLISION — surfaced, never resolved by me.
# ---------------------------------------------------------------------------

def collisions() -> dict:
    """Node types whose NAME also names a growth-ledger series.

    A shared name is not evidence of a shared thing. His own ruling on this
    shape has already bitten twice — WB-P against SB-HFR-P, and workbook S04
    against registry SEG-04 — so these are reported for his decision and nothing
    is merged."""
    from . import growth as G
    shared = sorted(set(TYPES) & set(G.SERIES))
    notes = {
        "STATE": "his growth STATE rows are operating states (Dominant, Active, "
                 "Compensated...). A STATE node here is an active-state node in "
                 "a sequence. Same family? Unresolved.",
        "EVENT": "growth EVENT rows are event SHELLS (RAISE_TAX, "
                 "ADVISOR_PRIVATE_MEETING). An EVENT node is one occurrence. A "
                 "shell is not an occurrence.",
        "PATTERN": "growth PATTERN rows are pattern candidates. A PATTERN node "
                   "is an arrangement that recurs. Probably the same family.",
        "RULE": "growth RULE rows are his standing rules. A RULE node is a "
                "standing constraint. Probably the same family.",
        "INTENT": "growth INTENT rows are the intent slot of one event. An "
                  "INTENT node is the reason pushing an event. Probably the "
                  "same, but 'slot' and 'reason' are not identical words.",
    }
    return {
        "node_types": len(TYPES), "growth_series": len(G.SERIES),
        "shared_names": shared, "count": len(shared),
        "node_only": sorted(set(TYPES) - set(G.SERIES)),
        "growth_only": sorted(set(G.SERIES) - set(TYPES)),
        "notes": {k: notes[k] for k in shared},
        "merged": False,
        "id_prefixes_kept_apart": {"nodes": ID_PREFIX,
                                   "bank": "SB-HFR-P", "ledger": "SB-<series>-"},
        "rule": "do not silently merge namespaces",
        "his_call": "whether any of these five pairs is one thing or two.",
    }


def headers() -> list:
    """The column headers, for anything that displays or exports a node."""
    return [{"header": f["field"], "required": f["required"], "is": f["is"]}
            for f in FIELDS]


def stats() -> dict:
    c = collisions()
    return {
        "phase": "A — registries and IDs",
        "schema_version": SCHEMA_VERSION,
        "fingerprint": fingerprint(),
        "node_types": len(NODE_TYPES), "fields": len(FIELDS),
        "required_fields": len(REQUIRED),
        "link_types": len(LINK_TYPES), "memory_kinds": len(MEMORY_KINDS),
        "statuses": len(STATUSES),
        "write_conditions": len(WRITE_CONDITIONS),
        "read_conditions": len(READ_CONDITIONS),
        "name_collisions_with_growth": c["count"],
        "namespaces_merged": False,
        "nodes_written": 0,
        "links_discovered": 0,
        "builds_on": "his SELF-SUSTAINING EXECUTION FLOW sheet, boxes 3, 4 and 6",
        "not_in_this_phase": ["linking (D)", "memory writeback (D)",
                              "auto-trigger (E)", "promotion"],
        "source": "docs/method/canon/THE_AUTO_PROPOSAL.md",
    }


def annotations() -> list:
    return [
        ("lock node schema, IDs, headers, ledgers", "nodebrain.lock"),
        ("his twelve node types", "nodebrain.NODE_TYPES"),
        ("his ten typed links, with direction and inverse",
         "nodebrain.LINK_TYPES"),
        ("no invention before source lock", "nodebrain.REQUIRED"),
        ("a malformed node is refused with the reason", "nodebrain.validate"),
        ("do not silently merge namespaces", "nodebrain.collisions"),
    ]
