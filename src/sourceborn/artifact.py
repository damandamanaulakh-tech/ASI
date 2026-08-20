"""THE ARTIFACT LAYER — reading an object without pretending to read its language.

Source: `GPT_Black.txt`, a transcript of the other assistant working the same
project. His instruction on it: **build it.**

Roughly half of that transcript is material this core already holds and built
independently — the ten same-king brain-states are `SP-19..SP-28`, the live intent
engine is `intent_ledger.py`, `NEW WORDING != NEW INTENT` is the novelty
signature. This module is the other half: **eight mechanisms that were not here.**

WHAT CAME OUT OF IT

    SG-A..SG-J          ten VISUAL PLACEHOLDER classes, so a sign can be reasoned
                        about by neighbour, position, repetition, enclosure and
                        damage WITHOUT claiming to know Egyptian
    SYN-MEAN-001..008   eight WHOLE-TABLET meanings — the object as a structure,
                        not as a sentence
    ORIGIN DISTANCE     0..5 from the visible mark. Farther is not WRONG, it is
                        MORE INFERENCE AND MORE EVIDENCE OWED
    ACTOR ROLES         nine of them. Subject != requester != controller !=
                        author != scribe != carver != institution != beneficiary
                        != audience, and each may hold a different intent
    FUTURE-STATE        ask what future state the producer was trying to create,
                        then work BACKWARDS to the intent. Everything else in
                        this core runs forwards only
    DAMAGE BRANCHING    a damaged region opens branches; it is never filled in
    PC-TAB-SYN-001..012 twelve pattern candidates, of which the transcript names
                        eight — the other four are reported as unnamed
    MATCH != CONFIDENCE a match score is not an epistemic confidence

WHAT IS REFUSED, AND IT IS THE TRANSCRIPT'S OWN LINE

Every meaning here is `NEW_SYNTHETIC`: `historical_fact = False`,
`translation_verified = False`. The infographic readings the transcript itself
rejected — owl = wisdom, falcon = royal guard, waves = endurance, five columns =
five reign stages — are recorded as REFUSED so they can never be quietly adopted.
The `7.8/10` confidence is refused for the reason he already found in his own
ASI0001 workbook: a match score is not a confidence, and there rank was row order
at score zero.

Canon: docs/method/canon/THE_ARTIFACT_LAYER.md
"""

from __future__ import annotations

from itertools import combinations

NEW_SYNTHETIC = "NEW_SYNTHETIC"

# ---------------------------------------------------------------------------
# THE VISUAL PLACEHOLDER REGISTRY — verbatim.
# ---------------------------------------------------------------------------

SIGN_GROUPS = (
    {"id": "SG-A", "name": "enclosure-like group",
     "reads": "something is bounded off from what surrounds it"},
    {"id": "SG-B", "name": "bird-like group",
     "reads": "an animate form, orientation and completeness may matter"},
    {"id": "SG-C", "name": "reed/stroke group",
     "reads": "repeated small marks — count and spacing may carry it"},
    {"id": "SG-D", "name": "wave/bar group",
     "reads": "a horizontal repeated form"},
    {"id": "SG-E", "name": "knot/cross form", "reads": "a tied or crossed shape"},
    {"id": "SG-F", "name": "half-round form", "reads": "a partial curve"},
    {"id": "SG-G", "name": "paired/tool-like form",
     "reads": "two elements held together, or an implement shape"},
    {"id": "SG-H", "name": "recurring group",
     "reads": "the same arrangement appearing more than once"},
    {"id": "SG-I", "name": "position/order",
     "reads": "where a group sits relative to the others"},
    {"id": "SG-J", "name": "damaged/unknown",
     "reads": "the surface is gone. NOT a missing letter to be filled in."},
)

# The axes a sign can be reasoned along without knowing what it says.
SIGN_AXES = ("NEIGHBOUR", "POSITION", "REPETITION", "ENCLOSURE", "DAMAGE")

# ---------------------------------------------------------------------------
# THE EIGHT WHOLE-TABLET MEANINGS — his, verbatim in substance.
# ---------------------------------------------------------------------------

SYNTHETIC_MEANINGS = (
    {"id": "SYN-MEAN-001", "name": "Identity across multiple states",
     "from": ("SG-A", "SG-H"),
     "meaning": "repeated identity-like enclosures with different surrounding "
                "signs may describe different conditions or roles of ONE "
                "identity, rather than merely repeating a name"},
    {"id": "SYN-MEAN-002", "name": "Authority connected to different domains",
     "from": ("SG-A", "SG-I"),
     "meaning": "an authority map — this identity in relation to A, in relation "
                "to B, in relation to C — not simply 'this is King X'"},
    {"id": "SYN-MEAN-003", "name": "One event distributed across several columns",
     "from": ("SG-I", "SG-H"),
     "meaning": "no single column need contain the whole message; the intent may "
                "exist only at the tablet level"},
    {"id": "SYN-MEAN-004", "name": "Identity -> transition -> identity",
     "from": ("SG-A", "SG-G", "SG-E"),
     "meaning": "the object may preserve a CHANGE — authority transferred, "
                "confirmed, a relationship established, a status renewed, an "
                "identity connected to a successor, a responsibility assigned. "
                "None is chosen."},
    {"id": "SYN-MEAN-005", "name": "Repetition as confirmation",
     "from": ("SG-H",),
     "meaning": "first appearance establishes; repeated appearance confirms, "
                "reinforces or renews. The object may be a confirmation "
                "structure."},
    {"id": "SYN-MEAN-006", "name": "External identity memory",
     "from": ("SG-A", "SG-H", "SG-I"),
     "meaning": "durable material + repeated enclosed identity + structured "
                "sequence = an identity made to persist OUTSIDE human memory"},
    {"id": "SYN-MEAN-007", "name": "Commissioner != performer != subject",
     "from": ("SG-A", "SG-B"),
     "meaning": "who appears on it, who ordered it, who designed it, who cut it "
                "and who was meant to see it are five different questions. The "
                "object may record a CHAIN of intent, not one person's "
                "expression."},
    {"id": "SYN-MEAN-008", "name": "Event compression record",
     "from": ("SG-A", "SG-C", "SG-D", "SG-H", "SG-I"),
     "meaning": "many events, relations and states compressed into a small "
                "reusable symbol set organised around identity on a durable "
                "object. The object is EVENT COMPRESSION + IDENTITY ANCHOR + "
                "RELATION MAP + FUTURE MEMORY OBJECT — not text."},
)

# ---------------------------------------------------------------------------
# ACTOR-ROLE MULTIPLICITY — one artifact event, nine roles, each with its own
# possible intent. This core's `actor_name()` reads ONE actor per event.
# ---------------------------------------------------------------------------

ACTOR_ROLES = (
    {"role": "SUBJECT", "asks": "who is depicted or named"},
    {"role": "REQUESTER", "asks": "who asked for it to exist"},
    {"role": "CONTROLLER", "asks": "who had the power to permit or forbid it"},
    {"role": "AUTHOR", "asks": "who decided what it would say"},
    {"role": "SCRIBE", "asks": "who set the composition down"},
    {"role": "CARVER", "asks": "whose hands made the marks"},
    {"role": "INSTITUTION", "asks": "which body stood behind it"},
    {"role": "BENEFICIARY", "asks": "who gained if it worked"},
    {"role": "AUDIENCE", "asks": "who was meant to see it, and when"},
)

# ---------------------------------------------------------------------------
# ORIGIN DISTANCE — how far a reading has travelled from the visible mark.
# ---------------------------------------------------------------------------

ORIGIN_DISTANCE = (
    {"d": 0, "what": "the visible mark itself", "debt": "none — it is there"},
    {"d": 1, "what": "the mark beside another mark",
     "debt": "that the grouping is real and not an accident of layout"},
    {"d": 2, "what": "a possible actor relation",
     "debt": "that the grouping encodes a relation at all"},
    {"d": 3, "what": "a possible authority relation",
     "debt": "that the relation is one of authority rather than another kind"},
    {"d": 4, "what": "a possible command or commission",
     "debt": "that an authority relation implies an act of commissioning"},
    {"d": 5, "what": "a specific named person commissioned it",
     "debt": "every step above, plus an identification the object alone cannot "
             "give"},
)

DISTANCE_LAW = ("farther is not WRONG. Farther is MORE INFERENCE, and more "
                "inference owes more evidence.")

# ---------------------------------------------------------------------------
# FUTURE-STATE RECONSTRUCTION — the backwards read.
# ---------------------------------------------------------------------------

FUTURE_STATES = (
    {"id": "FS-1", "state": "a future observer recognises the identity"},
    {"id": "FS-2", "state": "a future institution preserves the authority"},
    {"id": "FS-3", "state": "a future priest repeats the procedure"},
    {"id": "FS-4", "state": "a future successor accepts the continuity"},
    {"id": "FS-5", "state": "a future population sees the legitimacy"},
    {"id": "FS-6", "state": "a future workshop reproduces the formula"},
)

# ---------------------------------------------------------------------------
# THE TWELVE PATTERN CANDIDATES. The transcript names eight; the other four are
# reported as unnamed rather than invented.
# ---------------------------------------------------------------------------

PATTERN_CANDIDATES = (
    {"id": "PC-TAB-SYN-003", "name": "Controller-performer separation",
     "named_in_source": True,
     "beyond_egypt": "contracts, company records, laws — who signed is not who "
                     "decided"},
    {"id": "PC-TAB-SYN-004", "name": "Intent-from-future-state reconstruction",
     "named_in_source": True,
     "beyond_egypt": "any deliberate artefact: a will, a monument, a schema"},
    {"id": "PC-TAB-SYN-006", "name": "Column-order functional difference",
     "named_in_source": True,
     "beyond_egypt": "position in a document is not the same as sequence in time"},
    {"id": "PC-TAB-SYN-007", "name": "Damage-aware meaning branching",
     "named_in_source": True,
     "beyond_egypt": "a redaction, a lost email, a missing year of records"},
    {"id": "PC-TAB-SYN-008", "name": "Actor-role multiplicity",
     "named_in_source": True,
     "beyond_egypt": "every institutional act has more actors than it names"},
    {"id": "PC-TAB-SYN-009", "name": "Public-record future-state",
     "named_in_source": True,
     "beyond_egypt": "a press release, a plaque, a public filing"},
    {"id": "PC-TAB-SYN-010",
     "name": "Restoration-vs-original production split",
     "named_in_source": True,
     "beyond_egypt": "a repaired object records two intents, not one"},
    {"id": "PC-TAB-SYN-012", "name": "Synthetic-meaning evidence-debt scaling",
     "named_in_source": True,
     "beyond_egypt": "the origin-distance ladder, applied anywhere"},
    {"id": "PC-TAB-SYN-001", "name": None, "named_in_source": False,
     "beyond_egypt": None},
    {"id": "PC-TAB-SYN-002", "name": None, "named_in_source": False,
     "beyond_egypt": None},
    {"id": "PC-TAB-SYN-005", "name": None, "named_in_source": False,
     "beyond_egypt": None},
    {"id": "PC-TAB-SYN-011", "name": None, "named_in_source": False,
     "beyond_egypt": None},
)

# ---------------------------------------------------------------------------
# WHAT IS REFUSED — the transcript's own rejections, kept so they cannot creep
# back in as fact.
# ---------------------------------------------------------------------------

REFUSED = (
    {"claim": "owl = night / truth / wisdom", "why": "an infographic reading, "
     "not a translation. NEW_SYNTHETIC at most, never fact."},
    {"claim": "falcon = sky power / royal guard", "why": "same"},
    {"claim": "waves = endurance / continuity", "why": "same"},
    {"claim": "five columns = five reign stages / five vows",
     "why": "same, and it also assumes the column count means something"},
    {"claim": "confidence 7.8/10",
     "why": "refused until the score is defined. MATCH SCORE != EPISTEMIC "
            "CONFIDENCE — the same defect his ASI0001 workbook already showed, "
            "where RANK was row order at score 0."},
    {"claim": "column 1 -> column 2 -> column 3 is chronological",
     "why": "visual adjacency is not sequence. His own sequence rule: say which "
            "order is meant."},
)


def refused() -> list:
    return [dict(r, adopted=False, historical_fact=False) for r in REFUSED]


# ---------------------------------------------------------------------------
# DAMAGE — branches, never a fill.
# ---------------------------------------------------------------------------

def damage_branches(neighbours=()) -> dict:
    """A damaged region opens branches. It is never guessed at.

    Each branch must predict DIFFERENT evidence, or it is not a branch."""
    ns = list(neighbours) or ["(no neighbour recorded)"]
    branches = [
        {"branch": "A", "reads": "the damaged group continued the neighbouring "
                                 "arrangement",
         "predicts": "traces consistent with %s at the break edge" % ns[0]},
        {"branch": "B", "reads": "the damaged group broke the arrangement",
         "predicts": "spacing or depth at the edge unlike %s" % ns[0]},
        {"branch": "C", "reads": "the damage is later than the carving",
         "predicts": "fracture cutting THROUGH finished marks"},
        {"branch": "D", "reads": "the region was never carved",
         "predicts": "an unworked surface, no tool marks"},
    ]
    return {
        "region": "SG-J damaged/unknown",
        "branches": branches, "count": len(branches),
        "filled_in": False, "chosen": None,
        "law": "damage is intelligence, not missing data. A damaged glyph is "
               "never completed by the machine.",
    }


# ---------------------------------------------------------------------------
# THE GENERATION — and the count he asked for and never received.
# ---------------------------------------------------------------------------

def _distance_of(n_groups: int, has_actor: bool, has_future: bool) -> int:
    d = 0
    if n_groups >= 1:
        d = 1
    if n_groups >= 2:
        d = 2
    if has_actor:
        d = 3
    if has_future:
        d = 4
    return d


# ---------------------------------------------------------------------------
# THE GATES. Without them the generator returns the entire cross product —
# 6,480 of a possible 6,480, a meaning for every combination, which is not a
# finding. Same defect as the self-made COMBINATION steps before cross-role was
# required. Two gates, both readable off the definitions above.
# ---------------------------------------------------------------------------

# A role can only be working toward a future state it could actually affect.
# A carver does not secure a dynasty; a controller does not reproduce a formula.
ROLE_FUTURES = {
    "SUBJECT":     ("FS-1", "FS-4", "FS-5"),
    "REQUESTER":   ("FS-1", "FS-2", "FS-4", "FS-5"),
    "CONTROLLER":  ("FS-2", "FS-4", "FS-5"),
    "AUTHOR":      ("FS-1", "FS-3", "FS-6"),
    "SCRIBE":      ("FS-3", "FS-6"),
    "CARVER":      ("FS-6",),
    "INSTITUTION": ("FS-2", "FS-3", "FS-5"),
    "BENEFICIARY": ("FS-2", "FS-4", "FS-5"),
    "AUDIENCE":    ("FS-1", "FS-3", "FS-5"),
}

# A future state can only be read off marks that could carry it. An identity
# claim needs the enclosure; a procedure claim needs repetition or order.
FUTURE_NEEDS = {
    "FS-1": ("SG-A",),                          # recognise the identity
    "FS-2": ("SG-A", "SG-B"),                   # preserve the authority
    "FS-3": ("SG-C", "SG-D", "SG-H", "SG-I"),   # repeat the procedure
    "FS-4": ("SG-A", "SG-E", "SG-G"),           # accept the continuity
    "FS-5": ("SG-A", "SG-B"),                   # see the legitimacy
    "FS-6": ("SG-C", "SG-D", "SG-H", "SG-I"),   # reproduce the formula
}


def generate_meanings(max_group_size: int = 3, limit: int = 0,
                      gated: bool = True) -> dict:
    """Generate whole-object meanings from sign groups x actor roles x future
    states. Every one is NEW_SYNTHETIC and none is a translation.

    THE COUNT IS COMPUTED, not asserted — this is the number the transcript's
    last question asked for and never got before the chat expired:

        show me how many new meaning and on that basis u created with new inputs

    With `gated=False` it returns the raw cross product, which is what the first
    build did and why the gates exist. Both numbers are reported so the gate's
    effect is visible rather than assumed."""
    readable = [g for g in SIGN_GROUPS if g["id"] != "SG-J"]   # damage branches,
    #                                                            it does not combine
    have = {tuple(sorted(m["from"])) for m in SYNTHETIC_MEANINGS}
    out, already = [], 0
    rejected_role, rejected_marks = 0, 0
    for size in range(2, max_group_size + 1):
        for combo in combinations([g["id"] for g in readable], size):
            key = tuple(sorted(combo))
            base_known = key in have
            for role in ACTOR_ROLES:
                for fs in FUTURE_STATES:
                    if gated and fs["id"] not in ROLE_FUTURES[role["role"]]:
                        rejected_role += 1
                        continue
                    if gated and not any(m in combo
                                         for m in FUTURE_NEEDS[fs["id"]]):
                        rejected_marks += 1
                        continue
                    d = _distance_of(len(combo), True, True)
                    m = {
                        "id": "GEN-%s-%s-%s" % ("".join(c[-1] for c in combo),
                                                role["role"][:3], fs["id"]),
                        "from_groups": list(combo),
                        "actor_role": role["role"],
                        "future_state": fs["state"],
                        "meaning": "IF the %s arrangement was produced "
                                   "deliberately, its %s may have been working "
                                   "toward: %s"
                                   % (" + ".join(combo), role["role"].lower(),
                                      fs["state"]),
                        "status": NEW_SYNTHETIC,
                        "historical_fact": False,
                        "translation_verified": False,
                        "origin_distance": d,
                        "evidence_owed": ORIGIN_DISTANCE[d]["debt"],
                        "restates_existing": base_known,
                        "chosen": False,
                    }
                    if base_known:
                        already += 1
                    out.append(m)
    dropped = 0
    if limit and len(out) > limit:
        dropped = len(out) - limit
        out = out[:limit]
    ceiling = combination_space()["ceiling"]
    return {
        "gated": gated,
        "sign_groups_combinable": len(readable),
        "actor_roles": len(ACTOR_ROLES),
        "future_states": len(FUTURE_STATES),
        "max_group_size": max_group_size,
        "meanings": out,
        "counts": {
            "generated": len(out),
            "ceiling_ungated": ceiling,
            "rejected_role_cannot_reach_that_future": rejected_role,
            "rejected_marks_cannot_carry_that_claim": rejected_marks,
            "restating_one_of_his_eight": already,
            "genuinely_new_shapes": len(out) - already,
            "his_named_meanings": len(SYNTHETIC_MEANINGS),
            "dropped_by_limit": dropped,
            "historical_facts_established": 0,
            "translations_made": 0,
            "new_parameters_created": 0,
        },
        "law": DISTANCE_LAW,
        "gates": {
            "role_futures": "a role can only work toward a future state it "
                            "could affect — a carver does not secure a dynasty",
            "future_needs": "a future state can only be read off marks that "
                            "could carry it — an identity claim needs the "
                            "enclosure",
        },
        "refuses": "these are combinations, not readings of Egyptian. Every one "
                   "is NEW_SYNTHETIC, none is chosen, and the object is not "
                   "claimed to say any of them.",
    }


def combination_space() -> dict:
    """The ceiling, stated separately from what is generated, so the number is
    never mistaken for a discovery."""
    n = len([g for g in SIGN_GROUPS if g["id"] != "SG-J"])
    pairs = n * (n - 1) // 2
    triples = n * (n - 1) * (n - 2) // 6
    return {
        "combinable_groups": n,
        "pairs": pairs, "triples": triples,
        "group_combinations_2_to_3": pairs + triples,
        "actor_roles": len(ACTOR_ROLES),
        "future_states": len(FUTURE_STATES),
        "ceiling": (pairs + triples) * len(ACTOR_ROLES) * len(FUTURE_STATES),
        "note": "a ceiling is an arithmetic fact about the vocabulary, not a "
                "claim that the object carries that many meanings.",
    }


def seat_on_bank(limit: int = 40) -> dict:
    """Where his eight named meanings sit on the existing 3,204.

    The point of the growing phase: this material lands on parameters that
    already exist and strengthens them. It creates none."""
    from . import growing as W
    rows = []
    for m in SYNTHETIC_MEANINGS:
        s = W.seat(m["name"] + " " + m["meaning"], limit=4)
        rows.append({"id": m["id"], "name": m["name"],
                     "seats": [{"p": x["sb_id"], "row": x["name"],
                                "container": x["container"]}
                               for x in s["seats"]],
                     "seated": len(s["seats"])})
    ids = {x["p"] for r in rows for x in r["seats"]}
    return {"rows": rows, "distinct_ids": len(ids),
            "new_parameters_created": 0,
            "law": "an example seats on existing parameters and IDs; it does not "
                   "invent them."}


def grow(root: str) -> dict:
    """Append the mechanisms and his eight meanings. Appends only."""
    from . import growth as G
    have = {(r.get("kind"), r.get("name")) for r in G.load(root)}
    added = []

    def add(kind, name, detail, extra=None):
        if (kind, name) in have:
            return
        added.append(G.add(root, kind, name, surfaced_by="GPT_Black.txt",
                           module="artifact", detail=detail, extra=extra))

    for g in SIGN_GROUPS:
        add(G.AXIS, "SIGN GROUP %s — %s" % (g["id"], g["name"]), g["reads"])
    for m in SYNTHETIC_MEANINGS:
        add(G.PATTERN, "%s %s" % (m["id"], m["name"]), m["meaning"],
            {"status": NEW_SYNTHETIC, "historical_fact": False,
             "from_groups": list(m["from"])})
    for r in ACTOR_ROLES:
        add(G.AXIS, "ARTIFACT ACTOR ROLE: " + r["role"], r["asks"])
    for f in FUTURE_STATES:
        add(G.OBJECTIVE, "FUTURE STATE %s" % f["id"], f["state"])
    for p in PATTERN_CANDIDATES:
        nm = p["name"] or "(unnamed in the source)"
        add(G.PATTERN, "%s %s" % (p["id"], nm),
            p["beyond_egypt"] or "named only by its id in the transcript",
            {"named_in_source": p["named_in_source"]})
    for d in ORIGIN_DISTANCE:
        add(G.AXIS, "ORIGIN DISTANCE %d — %s" % (d["d"], d["what"]), d["debt"])
    add(G.RULE, "MATCH SCORE IS NOT EPISTEMIC CONFIDENCE",
        "refuse a bare score until it is defined. His ASI0001 workbook is the "
        "proof: RANK was row order at score 0.")
    add(G.RULE, "FARTHER IS NOT WRONG, FARTHER OWES MORE EVIDENCE",
        DISTANCE_LAW)
    add(G.RULE, "DAMAGE IS INTELLIGENCE, NOT MISSING DATA",
        "a damaged region opens branches that predict different evidence; it is "
        "never filled in")
    return {"added": len(added), "rows": added, "counts": G.counts(root),
            "parameters_created": 0}


def stats() -> dict:
    g = generate_meanings()
    return {
        "sign_groups": len(SIGN_GROUPS),
        "his_named_meanings": len(SYNTHETIC_MEANINGS),
        "actor_roles": len(ACTOR_ROLES),
        "future_states": len(FUTURE_STATES),
        "origin_distance_levels": len(ORIGIN_DISTANCE),
        "pattern_candidates": len(PATTERN_CANDIDATES),
        "pattern_candidates_named_in_source": sum(
            1 for p in PATTERN_CANDIDATES if p["named_in_source"]),
        "refused_claims": len(REFUSED),
        "meanings_generated": g["counts"]["generated"],
        "genuinely_new_shapes": g["counts"]["genuinely_new_shapes"],
        "historical_facts_established": 0,
        "translations_made": 0,
        "new_parameters_created": 0,
        "source": "docs/method/canon/THE_ARTIFACT_LAYER.md",
    }


def annotations() -> list:
    return [
        ("reason about a sign without knowing what it says",
         "artifact.SIGN_GROUPS"),
        ("the object is a structure, not a sentence",
         "artifact.SYNTHETIC_MEANINGS"),
        ("subject is not requester is not carver", "artifact.ACTOR_ROLES"),
        ("farther is more inference, not more wrong",
         "artifact.ORIGIN_DISTANCE"),
        ("work backwards from the future state the producer wanted",
         "artifact.FUTURE_STATES"),
        ("damage opens branches, it is never filled in",
         "artifact.damage_branches"),
        ("how many new meanings, computed", "artifact.generate_meanings"),
        ("what the transcript itself refused", "artifact.refused"),
    ]
