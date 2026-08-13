"""THE DOMAIN SPLIT — HUMAN means the physical human, not the brain.

His ruling, 2026-08-13:

    Human = the physical human: body, appearance, biological condition, safety,
    survival, ageing/life-extension, physical capacity.
    Human is not the thinking/memory/reasoning brain.

    MEMORY ≠ HUMAN PHYSICAL      EMOTION ≠ HUMAN PHYSICAL
    REASONING ≠ HUMAN PHYSICAL   MORALITY ≠ HUMAN PHYSICAL
    RESPONSIBILITY ≠ HUMAN PHYSICAL
    BUT bodily safety · survival · health · physical state · energy · ageing ·
    appearance · physical capability · life continuation = HUMAN

And the finding that forced this module:

    "the current 2,560 registry in the repo presently contains many cognitive
     containers — memory, reasoning, language, emotion, social cognition — not
     only body parameters. So for the architecture you are defining, we should
     not automatically treat all 2,560 as 'Human runtime brain.'"

    "we should not rename all 2,560 as 'Human physical parameters' … we
     eventually need to separate the physical Human subset from the
     brain/cognitive subset WITHOUT DELETING the original source records."

SO THIS IS AN OVERLAY, NOT A REWRITE. `human_registry.py` keeps his document
byte-for-byte — every name, every container, every count. This module sits on top
and says which DOMAIN each container serves. Nothing is renamed. Nothing is
removed. A container he considers mixed is marked MIXED and surfaced to him
rather than being quietly assigned.

WHAT WAS WRONG BEFORE: a sentence about memories routed straight into the
"Human" bank, so "memories" and "bodily survival" landed in the same place. Under
his rule those are different brains, and the reading has to show them apart.
"""
from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# HIS NODE CLASSES — taken from his own arrow chart, word for word where he
# named them.
HUMAN_PHYSICAL = "HUMAN BODY"          # physical only
BRAIN_MIND = "BRAIN / MIND"            # memory, reasoning, language, cognition
RELATION_AFFECT = "RELATION / AFFECT"  # beloved, attachment, emotion-as-relation
VALUE_WISDOM = "VALUE / WISDOM"        # good, moral, meaning
RULE_DUTY = "RULE / DUTY / ASI"        # responsibility, obligation, governance
RESULT_CONSEQUENCE = "RESULT / CONSEQUENCE"   # left with, got, outcome
ATTENTION_GOAL = "ATTENTION / PRIORITY / GOAL"
EXCLUSION = "EXCLUSION / BOUNDARY"     # "not the brain" — an explicit NOT

CLASSES = (HUMAN_PHYSICAL, BRAIN_MIND, RELATION_AFFECT, VALUE_WISDOM,
           RULE_DUTY, RESULT_CONSEQUENCE, ATTENTION_GOAL, EXCLUSION)

# ---------------------------------------------------------------------------
# HUMAN_DOMAIN_SCOPE — his lists, verbatim.
HUMAN_INCLUDE = ("physical body", "anatomy", "physiology", "appearance",
                 "health", "damage", "repair", "ageing", "longevity",
                 "survival", "physical capability")
HUMAN_EXCLUDE = ("memory", "reasoning", "language", "emotion interpretation",
                 "decision cognition", "metacognition", "abstract intelligence")

# ---------------------------------------------------------------------------
# THE CONTAINER OVERLAY. His document's 80 containers, each given a domain —
# and the ones he flagged as mixed are marked MIXED with his reason on them.
#
# NOTE ON SEG-03: he places physical execution on the Human side ("physical
# capability"), while motor PLANNING is cognitive. The containers themselves mix
# the two, so the planning ones are marked MIXED rather than claimed.
CONTAINER_DOMAIN: dict[str, str] = {}
CONTAINER_MIXED: dict[str, str] = {}


def _assign(rng, domain, mixed_note=""):
    for n in rng:
        cid = f"CON-{n:03d}"
        CONTAINER_DOMAIN[cid] = domain
        if mixed_note:
            CONTAINER_MIXED[cid] = mixed_note


# SEG-01 Biological Regulation and Internal State — his strongest Human hits.
# He named CON-001, CON-006, CON-007, CON-008 by hand for this sentence.
_assign(range(1, 9), HUMAN_PHYSICAL)

# SEG-02 Perception and Body Representation — perception is cognitive, but two
# containers touch the actual body. He flagged CON-015 himself.
_assign(range(9, 17), BRAIN_MIND)
_assign([11], HUMAN_PHYSICAL,
        "somatosensory perception is bodily signal AND its cognitive reading — "
        "he includes physical state, so the body side is Human; the perceiving "
        "side is Brain. Split not decided.")
_assign([15], HUMAN_PHYSICAL,
        "HIS OWN FLAG: 'Body Image can mean mental representation of one's "
        "body, which is brain/cognitive. Your Human definition is narrower: "
        "PHYSICAL APPEARANCE = actual visible/material body, NOT mental "
        "body-image representation.' The container name mixes both. Surfaced, "
        "not resolved.")

# SEG-03 Sensorimotor Action and Physical Execution — execution is physical
# capability (Human); planning and imitation are cognitive.
_assign(range(17, 25), HUMAN_PHYSICAL)
_assign([18], BRAIN_MIND, "motor PLANNING and sequencing is cognitive; the "
                          "execution it plans is Human. Split not decided.")
_assign([23], BRAIN_MIND, "imitation and goal inference is social cognition; "
                          "tool manipulation is physical. Split not decided.")

# SEG-04 Attention and Executive Control — cognition, and his own
# ATTENTION / PRIORITY / GOAL node
_assign(range(25, 33), ATTENTION_GOAL)

# SEG-05 Learning, Memory and Knowledge — MEMORY ≠ HUMAN PHYSICAL, his rule
_assign(range(33, 41), BRAIN_MIND)

# SEG-06 Reasoning, Planning, Decision, Creativity — REASONING ≠ HUMAN PHYSICAL
_assign(range(41, 49), BRAIN_MIND)

# SEG-07 Language and Communication — his exclusion list names language
_assign(range(49, 57), BRAIN_MIND)

# SEG-08 Emotion, Motivation, Intent and Motive — EMOTION ≠ HUMAN PHYSICAL.
# His chart routes "beloved" to RELATION / AFFECT.
_assign(range(57, 65), RELATION_AFFECT)
_assign([63], RULE_DUTY, "intent formation and COMMITMENT is where duty is "
                         "taken on — his chart sends responsibility to "
                         "RULE / DUTY / ASI, not to affect.")
_assign([64], VALUE_WISDOM, "motive, needs, VALUES and priority structure is "
                            "the value layer, not affect.")

# SEG-09 Consciousness, Self and Social Intelligence — relation and value;
# MORALITY ≠ HUMAN PHYSICAL
_assign(range(65, 73), RELATION_AFFECT)
_assign([66], BRAIN_MIND, "self-model and narrative self is cognition about "
                          "the self, not the body.")
_assign([68], RULE_DUTY, "agency, ownership and RESPONSIBILITY — his chart "
                         "routes responsibility here, to duty.")
_assign([72], VALUE_WISDOM, "morality, norms, culture and meaning is the "
                            "value / wisdom layer.")

# SEG-10 Development, Metacognition and Adaptation — his exclusion list names
# metacognition
_assign(range(73, 81), BRAIN_MIND)
_assign([73], HUMAN_PHYSICAL, "development and MATURATION is bodily as well as "
                              "cognitive — ageing sits in his Human include "
                              "list. Split not decided.")
_assign([77], HUMAN_PHYSICAL, "resilience, failure detection and REPAIR — "
                              "'damage' and 'repair' are in his Human include "
                              "list, and the container also covers coping. "
                              "Split not decided.")

# ---------------------------------------------------------------------------
# WORD → NODE CLASS. His own arrow chart, made executable.
WORD_ROUTES: list[tuple[str, str, str]] = [
    # --- HUMAN BODY: physical only ---------------------------------------
    (r"\b(safe|safety|protect\w*|harm|hurt|injur\w*|damage|wound\w*)\b",
     HUMAN_PHYSICAL, "protection from bodily harm"),
    (r"\b(alive|aliveness|surviv\w*|live|living|life|death|die|dying|dead)\b",
     HUMAN_PHYSICAL, "biological continuity"),
    (r"\b(body|bodies|bodily|physical|anatom\w*|physiolog\w*|flesh)\b",
     HUMAN_PHYSICAL, "the physical human"),
    (r"\b(appearance|looks|face|skin|weight|fitness|beaut\w*|handsome)\b",
     HUMAN_PHYSICAL, "visible / material body"),
    (r"\b(health\w*|ill\w*|sick\w*|disease|pain|ache|heal\w*|repair)\b",
     HUMAN_PHYSICAL, "bodily condition"),
    (r"\b(age|ageing|aging|old|young|longevity|life extension|"
     r"life-extension)\b", HUMAN_PHYSICAL, "ageing / life extension"),
    (r"\b(energy|tired\w*|fatigue|exhaust\w*|strength|stamina|sleep)\b",
     HUMAN_PHYSICAL, "physical resource"),
    (r"\b(person|people|human|humans|man|woman|child)\b",
     HUMAN_PHYSICAL, "identifies a living human / body object"),
    # --- BRAIN / MIND -----------------------------------------------------
    (r"\b(memor\w+|remember\w*|recall\w*|forget\w*|moment\w*)\b",
     BRAIN_MIND, "memory system — his rule: MEMORY ≠ HUMAN PHYSICAL"),
    (r"\b(think\w*|thought\w*|reason\w*|logic\w*|decide|decision|"
     r"understand\w*|know\w*|learn\w*|brain|mind|cognit\w*)\b",
     BRAIN_MIND, "reasoning / cognition — his rule: REASONING ≠ HUMAN PHYSICAL"),
    (r"\b(word\w*|language|said|say|tell|told|explain\w*|speak\w*|talk\w*)\b",
     BRAIN_MIND, "language"),
    # --- RELATION / AFFECT ------------------------------------------------
    (r"\b(beloved|loved|love|dear|family|friend\w*|partner|wife|husband|"
     r"mother|father|child\w*|attach\w*|belong\w*|bond)\b",
     RELATION_AFFECT, "relationship / attachment"),
    (r"\b(feel\w*|felt|emotion\w*|angry|sad|happy|afraid|fear|hurt inside|"
     r"lonely|jealous\w*|proud|ashamed)\b",
     RELATION_AFFECT, "affect — his rule: EMOTION ≠ HUMAN PHYSICAL"),
    # --- VALUE / WISDOM ---------------------------------------------------
    (r"\b(good|bad|right|wrong|moral\w*|ethic\w*|virtue|evil|kind\w*|"
     r"honest\w*|fair\w*|meaning|purpose|sacred)\b",
     VALUE_WISDOM, "value / wisdom — his rule: MORALITY ≠ HUMAN PHYSICAL"),
    # --- RULE / DUTY / ASI -----------------------------------------------
    (r"\b(responsib\w*|duty|oblig\w*|must|should|have to|owe|promise|"
     r"commit\w*|accountab\w*|keep them)\b",
     RULE_DUTY, "rule / duty — his rule: RESPONSIBILITY ≠ HUMAN PHYSICAL"),
    # --- RESULT / CONSEQUENCE --------------------------------------------
    (r"\b(left with|left|got|gained|received|retain\w*|remain\w*|outcome|"
     r"result|end up|ended up|nothing in return)\b",
     RESULT_CONSEQUENCE, "what remains — result / consequence"),
    # --- ATTENTION / PRIORITY / GOAL -------------------------------------
    (r"\b(looking at|looking for|focus\w*|priorit\w*|want\w*|chase|chasing|"
     r"aim\w*|goal|trying|pursu\w*|attention)\b",
     ATTENTION_GOAL, "attention / priority / goal"),
]

# an explicit NOT — "not the brain" is a boundary, not a topic
EXCLUSION_RE = re.compile(
    r"\bnot\s+(?:the\s+|a\s+|about\s+)?"
    r"(brain|mind|memory|thinking|reasoning|cognition|intelligence|"
    r"body|physical|appearance|emotion|feeling)s?\b", re.I)


# ---------------------------------------------------------------------------
# HIS NAMED CONTAINER TARGETS. He did not leave these to word overlap — he wrote
# them out: "safe" → CON-006, "alive" → CON-001 + CON-008, "keep working" →
# CON-007, "physical appearance" → CON-015 / CON-011. Lexical matching cannot
# find these (nothing in CON-006's name contains the word "safe"), so they are
# recorded as HIS assignments and marked as such wherever they appear.
HIS_CONTAINER_TARGETS: list[tuple[str, tuple[str, ...], str, str]] = [
    (r"\b(safe|safety|protect\w*|harm|hurt|injur\w*|damage)\b",
     ("CON-006",), HUMAN_PHYSICAL,
     "he named it: safe = protection from bodily harm → CON-006 Pain and "
     "Protective Signalling"),
    (r"\b(alive|surviv\w*|life|living|stay alive|keep .* alive)\b",
     ("CON-001", "CON-008"), HUMAN_PHYSICAL,
     "he named it: alive = biological continuity → CON-001 Homeostasis and "
     "Allostasis (its source definition includes survival prioritisation) and "
     "CON-008 Basic Biological Drives"),
    (r"\b(keep working|working for|effort|energy|tired\w*|fatigue|exhaust\w*)\b",
     ("CON-007",), HUMAN_PHYSICAL,
     "he named it: physical expenditure → CON-007 Energy, Fatigue and Resource "
     "Budgeting"),
    (r"\b(appearance|looks|body image|physical appearance)\b",
     ("CON-015", "CON-011"), HUMAN_PHYSICAL,
     "he named it: appearance → CON-015 Body Schema/Body Image and CON-011 "
     "Somatosensory — AND he flagged that CON-015 mixes the material body with "
     "the mental representation of it"),
    (r"\b(life extension|life-extension|longevity|age|ageing|aging)\b",
     ("CON-001", "CON-003", "CON-005", "CON-007"), HUMAN_PHYSICAL,
     "he named it: life extension = bodily maintenance and biological "
     "continuity → homeostasis, sleep/circadian, autonomic-hormonal, energy"),
    (r"\b(person|human|humans|people)\b", (), HUMAN_PHYSICAL,
     "he named it: person identifies a living human / body object"),
]


def his_targets(sentence: str) -> list[dict]:
    """The containers HE assigned to a concept, not the ones a word happens to
    spell. Each carries his reason, and every one of these is his knowledge —
    it is labelled that way so it is never mistaken for a lexical hit."""
    low = (sentence or "").lower()
    out, seen = [], set()
    for pattern, cids, cls, why in HIS_CONTAINER_TARGETS:
        m = re.search(pattern, low)
        if not m:
            continue
        for cid in cids:
            if cid in seen:
                continue
            seen.add(cid)
            out.append({"container": cid, "trigger": m.group(0),
                        "class": cls, "why": why, "source": "HIS ASSIGNMENT"})
        if not cids:
            out.append({"container": "", "trigger": m.group(0), "class": cls,
                        "why": why, "source": "HIS ASSIGNMENT"})
    return out


def route_words(sentence: str) -> dict:
    """Each word / phrase to the node class it belongs to — his arrow chart.

    Returns the routes found, the classes touched, and any EXCLUSION the
    sentence declares. An exclusion is not a topic: "not the brain" means the
    brain layer must be reported as explicitly OUT of scope for this ask, never
    as a hit."""
    low = (sentence or "").lower()
    routes: list[dict] = []
    for pattern, cls, why in WORD_ROUTES:
        for m in re.finditer(pattern, low):
            routes.append({"text": m.group(0), "class": cls, "why": why,
                           "at": m.start()})
    routes.sort(key=lambda r: r["at"])

    excluded: list[dict] = []
    for m in EXCLUSION_RE.finditer(sentence or ""):
        target = m.group(1).lower()
        cls = (BRAIN_MIND if target in ("brain", "mind", "memory", "thinking",
                                        "reasoning", "cognition",
                                        "intelligence")
               else HUMAN_PHYSICAL if target in ("body", "physical",
                                                 "appearance")
               else RELATION_AFFECT)
        excluded.append({"text": m.group(0), "excludes": cls,
                         "why": "he said NOT this — an explicit boundary, so "
                                "this layer is reported out of scope, never as "
                                "a hit"})
    ex_classes = {e["excludes"] for e in excluded}
    # a route into an excluded class is kept, but marked, never silently dropped
    for r in routes:
        if r["class"] in ex_classes:
            r["in_excluded_layer"] = True

    classes: dict[str, list[str]] = {}
    for r in routes:
        if r.get("in_excluded_layer"):
            continue
        classes.setdefault(r["class"], [])
        if r["text"] not in classes[r["class"]]:
            classes[r["class"]].append(r["text"])
    return {"routes": routes, "classes": classes,
            "his_targets": his_targets(sentence),
            "excluded": excluded,
            "excluded_classes": sorted(ex_classes),
            "scope": {"human_include": list(HUMAN_INCLUDE),
                      "human_exclude": list(HUMAN_EXCLUDE)},
            "rule": "Human = the physical human. Memory, emotion, reasoning, "
                    "morality and responsibility are NOT Human physical — they "
                    "belong to other brains (his ruling)."}


def domain_of(container_id: str) -> str:
    return CONTAINER_DOMAIN.get(container_id, BRAIN_MIND)


def mixed_note(container_id: str) -> str:
    return CONTAINER_MIXED.get(container_id, "")


def split_by_domain(containers: list[dict]) -> dict:
    """Group container hits by the node class they actually serve, so a reading
    can never show 'memories' and 'bodily survival' as one Human hit again."""
    out: dict[str, list[dict]] = {}
    for c in containers:
        d = domain_of(c.get("id", ""))
        out.setdefault(d, []).append({**c, "domain": d,
                                      "mixed": mixed_note(c.get("id", ""))})
    return out


def enforce_scope(containers: list[dict], word_routes: dict) -> dict:
    """His rule, enforced: a container may only be reported under HUMAN BODY if
    a word actually routed there.

    Before this, a sentence about memory pulled Human containers in on lexical
    overlap alone. Nothing is deleted — a container that fails the scope check
    is moved to `out_of_scope` with the reason, so he can see the machine's
    first reading beside the corrected one."""
    touched = set(word_routes.get("classes", {}))
    excluded = set(word_routes.get("excluded_classes", []))
    his = {t["container"]: t for t in word_routes.get("his_targets", [])
           if t.get("container")}
    kept, out = [], []
    # his own named targets are IN, whether or not a word happened to spell them
    for cid, t in his.items():
        if any(c.get("id") == cid for c in containers):
            continue
        from . import human_registry as _hr
        c = _hr.container(cid)
        if c:
            kept.append({"id": c["id"], "name": c["name"],
                         "segment": c["segment"],
                         "segment_name": c["segment_name"],
                         "note": c["note"], "modulators": c["modulators"],
                         "count": c["count"], "fired_params": 0,
                         "matched": [t["trigger"]],
                         "reason": t["why"],
                         "domain": t["class"], "mixed": mixed_note(cid),
                         "his_assignment": True})
    for c in containers:
        d = domain_of(c.get("id", ""))
        row = {**c, "domain": d, "mixed": mixed_note(c.get("id", ""))}
        if c.get("id") in his:                 # his word outranks the scope test
            row["his_assignment"] = True
            row["reason"] = his[c["id"]]["why"]
            kept.append(row)
            continue
        if d in excluded:
            row["why_out"] = ("he explicitly excluded this layer in this "
                              "sentence")
            out.append(row)
        elif d in touched:
            kept.append(row)
        else:
            row["why_out"] = (f"no word in the ask routed to {d} — the hit was "
                              "lexical overlap only")
            out.append(row)
    return {"in_scope": kept, "out_of_scope": out,
            "classes_touched": sorted(touched),
            "classes_excluded": sorted(excluded)}


def stats() -> dict:
    by: dict[str, int] = {}
    for cid, d in CONTAINER_DOMAIN.items():
        by[d] = by.get(d, 0) + 1
    return {"containers_classified": len(CONTAINER_DOMAIN),
            "by_domain": by,
            "mixed_flagged": len(CONTAINER_MIXED),
            "mixed": {k: v[:120] for k, v in CONTAINER_MIXED.items()},
            "his_rule": "Human = the physical human: body, appearance, "
                        "biological condition, safety, survival, "
                        "ageing/life-extension, physical capacity. Human is "
                        "not the thinking/memory/reasoning brain.",
            "overlay_only": "his 3,204 source records are untouched — nothing "
                            "renamed, nothing deleted, nothing merged"}
