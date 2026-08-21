"""THE GENERATION — same person, changed conditions, different active brain.

His correction, and the whole point:

    Your file is about the king HIMSELF: keep the identity fixed, change the
    active parameter set, situation and circumstance, and generate different
    possible internal "brains" of that same person.

    Warrior-King  = KING-BRAIN STATE / MODEL A
    Diplomat-King = KING-BRAIN STATE / MODEL B
    Grieving-King = KING-BRAIN STATE / MODEL C

    Potentially all of them can exist inside the same human king at different
    Sequence points.

    PERSONALITY != ONE STATIC PROFILE

So a state pack is NOT a personality type. It is a hypothesis about which
containers are active, in which states, under named conditions — generated for
one locked identity.

WHAT THE GENERATION ACTUALLY MAKES, and why it is new:

His 3,204 bank holds NAMES. His King profiles hold NAME x STATE. Measured
against the real registry, 0 of 36 (container-name + state) pairs from the
18-Kings file exist anywhere in the bank; "Compensated" and "Conflicted" appear
in 0 of 3,204 names. So container x state is a generator, and his own sheet
states the capacity: 2560 sub-params x 40 filters x 12 states.

AND HIS LAW ON WHAT THAT MEANS:

    INSTANTIATED ADDRESS != NATIVE PARAMETER
    DOMAIN CONTAINER     != RUBRIC
    RUBRIC APPLICATION   != ONTOLOGY EXPANSION

    Across these 10, I would still add zero canonical parameters.

So nothing here REWRITES his source document — that stays byte-for-byte, and a
test proves human_registry still reports 3,204.

But the system GROWS. His later instruction:

    these 3204, are the basic and vague setup
    which will be making more with such examples
    so keep adding not removing at all

So every generated address is also APPENDED to the growth ledger
(`growth.py`), which is append-only and has no removal path. Base 3,204 is a
floor. The two statements are different and I had wrongly merged them into "the
bank never grows".

Canon: docs/method/canon/THE_GENERATION_SAME_PERSON_MANY_BRAINS.md
"""

from __future__ import annotations

import re
from functools import lru_cache

from . import human_registry as hr
from .asi_pyramid import HELD, INFERRED, SOURCE_GROUNDED, container_span, param

# ---------------------------------------------------------------------------
# HIS 25 UNIVERSAL DIMENSIONS — extracted verbatim from his PARAMETER_BANK.
# Verified: all 80 containers use exactly the same 25, one distinct tuple of
# 80. That is his discovery: 80 x 25 = 2,000 INSTANTIATED ADDRESSES, not 2,000
# native parameters, and it is why the 2,000 is NOT added to the 3,204.
# ---------------------------------------------------------------------------

RUBRICS_25 = (
    "Presence", "Strength", "Frequency", "Trigger Situation", "Primary Actor",
    "Primary Target", "Sequence Position", "Duration", "Repetition Pattern",
    "Geographic Scope", "Social Scope", "Material Evidence",
    "Textual Evidence", "Iconographic Evidence", "Comparative Parallel",
    "Chronological Fit", "Workshop Fit", "Family Linkage", "War Linkage",
    "Ritual Linkage", "Economic Linkage", "Contradiction Risk",
    "Alternative Explanation", "Falsifier", "Confidence",
)

# ---------------------------------------------------------------------------
# THE OPERATING STATES. Five are observed in his own King profiles; his
# skeleton says 12 exist. The seven he has not named are recorded as unnamed
# rather than invented.
# ---------------------------------------------------------------------------

DOMINANT = "Dominant"
ACTIVE = "Active"
AUTOMATIC = "Automatic"
COMPENSATED = "Compensated"
CONFLICTED = "Conflicted"
SUPPRESSED = "Suppressed"      # his arrow-down notation, named here
STATES_HIS = (DOMINANT, ACTIVE, AUTOMATIC, COMPENSATED, CONFLICTED)
STATES_TOTAL = 12
STATES_UNNAMED = STATES_TOTAL - len(STATES_HIS) - 1   # minus Suppressed

# ---------------------------------------------------------------------------
# HIS CONDITION AXES — the inputs that change the active brain while the
# identity stays locked. From his own diagram.
# ---------------------------------------------------------------------------

CONDITION_AXES = (
    "body state", "life history", "relationship", "emotion", "knowledge",
    "pressure", "status", "memory", "age/time",
)


# ---------------------------------------------------------------------------
# THE STATE PACKS. His 28 — 18 from the Kings file, 10 he added as brains of
# the SAME king. Each carries the containers HE named, in the states HE named,
# and the conditions that raise it. `model` is the neutral label he asked for:
# these are MODEL A/B/C..., not personality types.
# ---------------------------------------------------------------------------

def _P(*pairs):
    return tuple(pairs)


STATE_PACKS = [
 # --- the six from the Kings file that carried real container-state boxes ---
 {"id": "SP-01", "name": "Warrior", "model": "A",
  "conditions": ["pressure: threat", "status: contested", "body state: aroused"],
  "containers": _P((2, DOMINANT), (17, DOMINANT), (20, DOMINANT),
                   (61, DOMINANT), (66, AUTOMATIC), (68, DOMINANT)),
  "filters": ("Threat", "Status", "Power", "Stress", "Culture(Ma'at)",
              "Time(eternity)"),
  "evidence": "H4-H5", "by": "HIS — 18-Kings file"},
 {"id": "SP-02", "name": "Builder", "model": "B",
  "conditions": ["pressure: none acute", "knowledge: high", "age/time: long horizon"],
  "containers": _P((31, DOMINANT), (42, ACTIVE), (46, DOMINANT),
                   (48, ACTIVE), (80, DOMINANT), (66, DOMINANT)),
  "filters": ("Complexity", "Time(long)", "Institutional", "Knowledge",
              "Value(eternal stone)"),
  "evidence": "H5", "by": "HIS — 18-Kings file"},
 {"id": "SP-03", "name": "Ritual / Divine", "model": "C",
  "conditions": ["emotion: reverent", "knowledge: doctrinal", "relationship: priesthood"],
  "containers": _P((4, ACTIVE), (57, ACTIVE), (65, DOMINANT),
                   (66, AUTOMATIC), (72, DOMINANT), (79, ACTIVE)),
  "filters": ("Culture(religion)", "Belief", "Identity(divine)",
              "Interoceptive", "Emotional"),
  "evidence": "H4", "by": "HIS — 18-Kings file"},
 {"id": "SP-04", "name": "Family / Dynastic", "model": "D",
  "conditions": ["relationship: household", "age/time: dynasty", "memory: lineage"],
  "containers": _P((8, ACTIVE), (64, DOMINANT), (66, DOMINANT),
                   (71, DOMINANT), (73, ACTIVE), (79, ACTIVE)),
  "filters": ("Relationship", "Identity(lineage)", "Status", "Culture",
              "Time(dynasty)"),
  "evidence": "H3", "by": "HIS — 18-Kings file"},
 {"id": "SP-05", "name": "Long-Reign Endurance", "model": "E",
  "conditions": ["age/time: decades", "body state: depleted but compensating"],
  "containers": _P((2, COMPENSATED), (7, DOMINANT), (26, DOMINANT),
                   (62, DOMINANT), (66, DOMINANT), (80, DOMINANT)),
  "filters": ("Time(long horizon)", "Energy", "Practice", "Institutional",
              "Scarcity(order)"),
  "evidence": "H4-H5", "by": "HIS — 18-Kings file"},
 {"id": "SP-06", "name": "Court / Intrigue", "model": "F",
  "conditions": ["relationship: rivalrous", "pressure: social", "knowledge: partial"],
  "containers": _P((29, CONFLICTED), (32, ACTIVE), (54, DOMINANT),
                   (69, DOMINANT), (71, DOMINANT), (76, ACTIVE)),
  "filters": ("Social Presence", "Power", "Status", "Uncertainty",
              "Relationship"),
  "evidence": "H2-H3", "by": "HIS — 18-Kings file"},

 # --- the ten he added, all brains of the SAME king -----------------------
 {"id": "SP-19", "name": "Insecure-Legitimacy", "model": "G",
  "conditions": ["status: unconfirmed", "relationship: unproven acceptance"],
  "containers": _P((71, DOMINANT), (69, DOMINANT), (66, CONFLICTED),
                   (61, ACTIVE), (76, ACTIVE)),
  "filters": ("Status", "Social Presence", "Uncertainty",
              "Identity(unsettled)"),
  "chain": ["small criticism", "interpreted as status threat",
            "monitor loyalty", "seek reassurance / recognition"],
  "refuses": "not necessarily a weak king — he may be extremely capable while "
             "remaining uncertain whether his position is accepted",
  "evidence": "H2", "by": "HIS — the ten same-king brains"},
 {"id": "SP-20", "name": "Secure-Legitimacy", "model": "H",
  "conditions": ["age/time: long reign", "status: repeatedly accepted",
                 "pressure: few challengers"],
  "containers": _P((66, DOMINANT), (71, ACTIVE), (61, SUPPRESSED),
                   (46, DOMINANT), (30, ACTIVE)),
  "filters": ("Status", "Time(long)", "Institutional"),
  "chain": ["criticism", "less threatening", "more tolerance",
            "longer decision horizon"],
  "pairs_with": "SP-19",
  "pair_note": "SP-19 and SP-20 can be the SAME MAN — different accumulated "
               "history, different active brain",
  "evidence": "H3", "by": "HIS — the ten same-king brains"},
 {"id": "SP-21", "name": "Grieving", "model": "I",
  "conditions": ["relationship: loss of child/partner/relative",
                 "emotion: grief", "body state: energy down"],
  "containers": _P((71, DOMINANT), (61, DOMINANT), (33, DOMINANT),
                   (7, SUPPRESSED), (46, CONFLICTED), (64, CONFLICTED)),
  "filters": ("Relationship", "Emotional", "Time(altered)"),
  "holds": "same intelligence, same authority, same knowledge, same title — "
           "but VALUE WEIGHTS ARE NOT THE SAME. Things once important can "
           "temporarily become unimportant.",
  "evidence": "H2", "by": "HIS — the ten same-king brains"},
 {"id": "SP-22", "name": "Suspicious", "model": "J",
  "conditions": ["life history: betrayal occurred",
                 "relationship: trust model damaged"],
  "containers": _P((69, DOMINANT), (61, DOMINANT), (44, DOMINANT),
                   (38, DOMINANT), (29, ACTIVE)),
  "filters": ("Uncertainty", "Social Presence", "Power"),
  "refuses": "not 'paranoid' as a diagnosis — a candidate state",
  "reads_signal_as": "possibly strategic",
  "evidence": "H2", "by": "HIS — the ten same-king brains"},
 {"id": "SP-23", "name": "Trusting", "model": "K",
  "conditions": ["life history: long reliable relationship",
                 "relationship: repeated reliability"],
  "containers": _P((71, DOMINANT), (69, ACTIVE), (61, SUPPRESSED),
                   (70, ACTIVE)),
  "filters": ("Relationship", "Social Presence"),
  "pairs_with": "SP-22",
  "pair_note": "same king, same words, different history path",
  "reads_signal_as": "probably important/private matter",
  "evidence": "H2", "by": "HIS — the ten same-king brains"},
 {"id": "SP-24", "name": "Exhausted", "model": "L",
  "conditions": ["body state: sleep down, energy down, pain up, stress up"],
  "containers": _P((3, SUPPRESSED), (7, SUPPRESSED), (6, DOMINANT),
                   (5, DOMINANT), (28, CONFLICTED), (29, CONFLICTED),
                   (26, CONFLICTED)),
  "filters": ("Energy", "Biological", "Stress", "Interoceptive"),
  "holds": "working memory, patience, risk tolerance and attention changes are "
           "HYPOTHESES TO TEST, not automatic truths",
  "law": "DECISION DIFFERENCE MAY ORIGINATE BELOW 'REASONING'. Body state "
         "changes available cognitive capacity, which changes decision "
         "expression.",
  "evidence": "H3", "by": "HIS — the ten same-king brains"},
 {"id": "SP-25", "name": "Euphoric-Victory", "model": "M",
  "conditions": ["life history: major recent success", "emotion: elated",
                 "status: raised"],
  "containers": _P((60, DOMINANT), (44, DOMINANT), (68, DOMINANT),
                   (71, DOMINANT), (37, DOMINANT)),
  "filters": ("Reward", "Status", "Arousal"),
  "must_distinguish": ["JUSTIFIED CONFIDENCE", "OVERGENERALIZED CONFIDENCE"],
  "holds": "victory may genuinely provide better information about capability — "
           "so overconfidence is not the automatic reading",
  "evidence": "H3", "by": "HIS — the ten same-king brains"},
 {"id": "SP-26", "name": "Defeat-Shaken", "model": "N",
  "conditions": ["life history: major defeat", "emotion: shaken"],
  "containers": _P((44, CONFLICTED), (61, DOMINANT), (32, DOMINANT),
                   (43, DOMINANT), (33, DOMINANT)),
  "filters": ("Threat", "Uncertainty", "Stress"),
  "forks": ["learn -> adaptive king", "freeze -> inhibited king",
            "blame -> defensive king", "investigate -> analytical king",
            "compensate -> risk-seeking king"],
  "law": "even one brain-state must fork. The defeat itself does not tell us "
         "which king emerges.",
  "evidence": "H2", "by": "HIS — the ten same-king brains"},
 {"id": "SP-27", "name": "Divided-Loyalty", "model": "O",
  "conditions": ["relationship: competing duties", "pressure: moral"],
  "containers": _P((72, DOMINANT), (64, CONFLICTED), (71, CONFLICTED),
                   (63, CONFLICTED), (47, CONFLICTED)),
  "filters": ("Relationship", "Culture", "Power", "Value"),
  "duties": ["duty to kingdom", "duty to family", "loyalty to old friend",
             "personal promise", "religious/moral obligation"],
  "law": "NO SINGLE ROLE OWNS THE DECISION. Multiple valid intent assemblies "
         "inside one person at the same time.",
  "evidence": "H2", "by": "HIS — the ten same-king brains"},
 {"id": "SP-28", "name": "Legacy-Anxious", "model": "P",
  "conditions": ["age/time: remaining time perceived as short",
                 "memory: mortality salient"],
  "containers": _P((66, DOMINANT), (33, DOMINANT), (16, DOMINANT),
                   (71, ACTIVE), (69, ACTIVE), (72, DOMINANT),
                   (73, ACTIVE)),
  "filters": ("Time(mortality)", "Identity", "Status", "Memory"),
  "same_circumstance_different_pyramid": [
      "I've done enough.", "I will be forgotten.",
      "My children must continue me.",
      "My name doesn't matter; the kingdom must survive."],
  "law": "same external circumstance, different Pyramid",
  "evidence": "H3", "by": "HIS — the ten same-king brains"},
]

# The twelve kings in his file that carried prose meaning and NO container
# assignments. Recorded as un-generated rather than counted as brains.
PROSE_ONLY = ("Restorer / Stabiliser", "Composite Full-Human (Meta)",
              "Priest-King / High Priest of Amun",
              "Child / Young King under Regency", "Empire Conqueror",
              "Diplomat / Treaty", "Hunter / Sporting",
              "Architect of Eternity (Tomb Builder)",
              "Healer / Magician-Physician", "Father of Many",
              "Wise Elder / Final Years", "Shadow / Hidden King")


# ---------------------------------------------------------------------------
# THE IDENTITY LOCK
# ---------------------------------------------------------------------------

def identity_lock(who: str) -> dict:
    """KING-ID LOCK. One person. The packs below are states OF this person,
    never other people."""
    return {
        "identity": (who or "").strip() or "(unnamed)",
        "locked": True,
        "rule": "the identity does not change. The active parameter set, the "
                "situation and the circumstance change.",
        "not": "a personality type, and not a different person",
        "his_words": "keep the identity fixed, change the active parameter "
                     "set, situation and circumstance",
    }


# ---------------------------------------------------------------------------
# THE GENERATION — container x state -> RUNTIME ADDRESS
# ---------------------------------------------------------------------------

def _con(n: int) -> dict:
    return hr.container("CON-%03d" % int(n))


def runtime_address(container_n: int, state: str, rubric: str = None) -> dict:
    """One generated address. His law is on the object itself:

        INSTANTIATED ADDRESS != NATIVE PARAMETER

    So it carries no P id, it is never written to the bank, and it says which
    native container it hangs off."""
    c = _con(container_n)
    lo, hi = container_span(c["id"])
    addr = "%s@%s" % (c["id"], state.upper())
    if rubric:
        addr += "/" + rubric.replace(" ", "-")
    return {
        "address": addr,
        "container": c["id"],
        "container_name": c["name"],
        "segment": c["segment"],
        "segment_name": c["segment_name"],
        "native_span": [lo, hi],
        "state": state,
        "rubric": rubric,
        "kind": "RUNTIME ADDRESS",
        "is_native_parameter": False,
        "in_bank": False,
        "law": "INSTANTIATED ADDRESS != NATIVE PARAMETER",
    }


def pack(pack_id: str) -> dict:
    for p in STATE_PACKS:
        if p["id"] == pack_id:
            return p
    raise KeyError(pack_id)


def generate(who: str, pack_id: str, rubrics: tuple = None) -> dict:
    """Instantiate one brain-state of one locked identity."""
    p = pack(pack_id)
    rubs = tuple(rubrics or ())
    addrs = [runtime_address(n, s) for n, s in p["containers"]]
    crossed = []
    for n, s in p["containers"]:
        for r in rubs:
            crossed.append(runtime_address(n, s, r))
    return {
        "identity": identity_lock(who),
        "pack": {k: v for k, v in p.items() if k != "containers"},
        "containers": [{"n": n, "id": "CON-%03d" % n,
                        "name": _con(n)["name"], "state": s}
                       for n, s in p["containers"]],
        "addresses": addrs,
        "rubric_crossed": crossed,
        "counts": {
            "containers": len(p["containers"]),
            "states_used": len({s for _n, s in p["containers"]}),
            "addresses": len(addrs),
            "rubrics_applied": len(rubs),
            "rubric_addresses": len(crossed),
            "native_parameters_added": 0,
            "native_parameters_modified": 0,
        },
        "filters": list(p.get("filters", ())),
        "filter_arguments": filter_arguments(p.get("filters", ())),
    }


def filter_arguments(filters) -> dict:
    """His third generation axis, which the 40-filter list does not hold:
    Time(eternity) and Time(dynasty) are not the same filter."""
    out = {}
    for f in filters:
        m = re.match(r"([A-Za-z ]+?)\((.*?)\)$", str(f).strip())
        if m:
            out.setdefault(m.group(1).strip(), []).append(m.group(2))
    return {k: sorted(set(v)) for k, v in out.items()}


def capacity() -> dict:
    """What the generator can address, against what the bank holds."""
    n = len(hr.parameters())
    cons = len(hr.containers())
    return {
        "native_bank": n,
        "containers": cons,
        "states_named_by_him": len(STATES_HIS) + 1,
        "states_total": STATES_TOTAL,
        "states_unnamed": STATES_UNNAMED,
        "rubrics": len(RUBRICS_25),
        "container_x_state": cons * STATES_TOTAL,
        "container_x_rubric": cons * len(RUBRICS_25),
        "his_stated_capacity": 2560 * 40 * 12,
        "at_current_fill": n * 40 * STATES_TOTAL,
        "generated_by_his_packs": len({(n_, s) for p in STATE_PACKS
                                       for n_, s in p["containers"]}),
        "law": "80 x 25 = 2,000 INSTANTIATED ADDRESSES, not 2,000 native "
               "parameters. The 2,000 is NOT added to the 3,204.",
    }


# ---------------------------------------------------------------------------
# SAME SIGNAL, DIFFERENT HISTORY — his SP-22 / SP-23 pair
# ---------------------------------------------------------------------------

def same_signal_different_history(signal: str, pack_a: str = "SP-22",
                                  pack_b: str = "SP-23") -> dict:
    """His block: the same sentence read by two brains of the same king.

        "I need to speak with you privately."

        TRUSTING   -> probably important/private matter
        SUSPICIOUS -> possible manipulation/threat

    Same king. Same words. Different history path. The machine returns BOTH
    and does not choose."""
    a, b = pack(pack_a), pack(pack_b)
    return {
        "signal": signal,
        "readings": [
            {"pack": a["id"], "name": a["name"],
             "history": [c for c in a["conditions"]],
             "reads_as": a.get("reads_signal_as", "(not stated for this pack)")},
            {"pack": b["id"], "name": b["name"],
             "history": [c for c in b["conditions"]],
             "reads_as": b.get("reads_signal_as", "(not stated for this pack)")},
        ],
        "same_identity": True,
        "chosen": None,
        "law": "SAME INCOMING SIGNAL + CHANGED HISTORY = DIFFERENT "
               "INTERPRETATION",
        "refuses": "the machine does not pick between them. The history that "
                   "decides is not in the signal.",
    }


# ---------------------------------------------------------------------------
# THE EVENT FORK — his ten King sequences, as a mechanism
# ---------------------------------------------------------------------------

# Each entry: his event, his intent routes, and the refusal he attached.
EVENT_FORKS = {
 "RAISE_TAX": {
   "routes": ["war funding -> defence capacity",
              "famine reserve -> survival buffer",
              "palace / luxury -> personal benefit",
              "control / pressure -> weaken rivals"],
   "open": ["temporary?", "permanent?", "rich only?", "poor only?",
            "after invasion?", "before rebellion?",
            "where does the money actually go?"],
   "refuses": "TAX INCREASE != GREED automatically. Follow the resource flow."},
 "LOWER_TAX": {
   "routes": ["compassion", "economic stimulation", "win popularity",
              "reward loyal region", "attract merchants",
              "weaken tax collectors", "temporary succession support"],
   "open": ["who benefits?", "for how long?"],
   "refuses": "RAISE TAX and LOWER TAX can BOTH serve KINGDOM STABILITY — "
              "different action, potentially same terminal goal"},
 "RELEASE_PRISONERS": {
   "routes": ["mercy -> moral image", "political amnesty -> reconciliation",
              "need -> manpower"],
   "open": ["prison overcrowding", "lack of food", "religious festival",
            "coronation tradition", "exchange agreement",
            "wrongful convictions"],
   "refuses": "RELEASE != FORGIVENESS necessarily"},
 "CENSUS": {
   "routes": ["taxation -> revenue", "military recruitment -> army planning",
              "welfare -> distribution"],
   "open": ["migration control", "land reform", "succession planning",
            "disease response", "ethnic/religious classification"],
   "asks": ["WHAT WAS COUNTED?", "WHO REQUESTED IT?", "WHAT ACTION FOLLOWED?"],
   "refuses": "the next Sequence may reveal the intent better than the census"},
 "BUILD_ROAD": {
   "routes": ["trade -> economy", "military -> strategic reach",
              "public movement -> integration"],
   "open": ["road to border weights military up",
            "road to port weights trade up",
            "road to temple weights ritual up"],
   "refuses": "same physical object, different network function depending on "
              "what it connects"},
 "CHANGE_LANGUAGE": {
   "routes": ["unify administration", "include a population",
              "exclude an elite", "centralize authority",
              "cultural assimilation", "improve trade",
              "replace old bureaucracy", "signal new dynasty"],
   "open": ["communication", "identity", "access", "institution", "status",
            "memory", "power"],
   "refuses": "one word participates in many addresses"},
 "DESTROY_MONUMENT": {
   "routes": ["ideology -> legitimacy shift", "security -> defence",
              "reuse -> material needed"],
   "open": ["earthquake damage", "urban redevelopment", "religious change",
            "revenge", "economic necessity",
            "accidental destruction later attributed to the king"],
   "refuses": "OBJECT DISAPPEARS != KING INTENTIONALLY DESTROYED IT. "
              "Source/provenance gate first."},
 "REFUSE_WAR": {
   "routes": ["peace -> restraint", "weakness -> incapacity",
              "strategy -> delayed advantage"],
   "open": ["secret alliance", "economic dependence", "religious restraint",
            "bad season", "army unavailable", "internal rebellion",
            "enemy too strong"],
   "refuses": "absence of action is itself an event"},
 "APPOINT_RIVAL": {
   "routes": ["trust -> merit", "control -> surveillance",
              "co-option -> stability"],
   "open": ["rival has rare expertise", "appointment satisfies treaty",
            "rival controls an important region",
            "king wants shared responsibility",
            "king expects rival to fail publicly"],
   "refuses": "PROMOTION != AFFECTION, as PUNISHMENT != HATRED. Visible "
              "treatment cannot directly reveal hidden relation."},
 "ABDICATE": {
   "routes": ["age / health -> physical limit",
              "succession -> orderly transfer",
              "pressure -> loss of power"],
   "open": ["religious withdrawal", "avoid civil war", "protect family",
            "retain power behind successor", "temporary abdication",
            "legal requirement", "accept responsibility for failure"],
   "retains": ["advisers", "wealth", "army loyalty", "family influence",
               "religious authority", "information networks"],
   "refuses": "FORMAL POWER != FUNCTIONAL POWER. OFFICIAL ROLE ENDS != "
              "INFLUENCE ENDS."},
 # The eleventh, from his ASI0001_tablet_run_LIVE_INTENT_v2 workbook. Its ten
 # routes are one per brain-state of the SAME king — the only fork here where the
 # route is selected by the actor's state rather than by the resource flow, and
 # the only one where every route arrives with a falsifier. Held in full in
 # `intent_ledger.HIS_CANDIDATES`.
 "ADVISOR_PRIVATE_MEETING": {
   "routes": ["insecure legitimacy -> obtain visible confirmation of authority",
              "secure legitimacy -> gather decision-relevant information",
              "grieving -> narrow or defer to protect essential duty",
              "suspicious after betrayal -> verify the advisor's account",
              "trusting after reliability -> receive what cannot be said publicly",
              "exhausted -> defer irreversible commitments",
              "victory-elevated -> explore expansion, but check the confidence",
              "defeat-shaken -> separate controllable causes from noise",
              "divided loyalty -> expose which obligations conflict",
              "legacy-anxious -> test whether the decision survives his absence"],
   "open": ["who asked for privacy — the king or the advisor?",
            "what does the advisor gain from the setting?",
            "is the meeting about the issue or about the relationship?"],
   "asks": ["WHAT STATE IS THE KING IN?", "WHAT WOULD FLIP THIS READING?"],
   "refuses": "SAME EVENT != SAME INTENT. A private meeting reads ten different "
              "ways on ten states of the same man, and each reading names what "
              "would flip it."},
}


def fork_event(event: str) -> dict:
    """One visible action, N intent routes, none chosen."""
    key = (event or "").strip().upper().replace(" ", "_")
    spec = EVENT_FORKS.get(key)
    if not spec:
        return {"event": key, "known": False,
                "routes": [], "count": 0,
                "note": "this event shape is not one he has named. Reported "
                        "unnamed rather than forked on a guess."}
    return {
        "event": key, "known": True,
        "routes": spec["routes"], "count": len(spec["routes"]),
        "still_open": spec.get("open", []),
        "asks": spec.get("asks", []),
        "retains": spec.get("retains", []),
        "refuses": spec["refuses"],
        "chosen": None,
        "law": "VISIBLE ACTION != HIDDEN INTENT",
    }


def formal_vs_functional(role_lost: str = "", retains: list = None) -> dict:
    """His freshest candidate, from the abdication fork."""
    return {
        "formal_state": "%s ENDED" % (role_lost or "OFFICIAL ROLE"),
        "functional_state": "UNKNOWN — must be established separately",
        "may_retain": retains or EVENT_FORKS["ABDICATE"]["retains"],
        "law": "FORMAL STATE != FUNCTIONAL STATE",
        "cross_domain_to_watch": ["CEO title vs real control",
                                  "parent authority vs actual influence",
                                  "official ownership vs effective control"],
        "his_gate": "if it starts appearing repeatedly in other domains then "
                    "ASI may have a genuine new reusable pattern rather than "
                    "just another King interpretation",
    }


# ---------------------------------------------------------------------------
# THE CANDIDATE LAWS — all REVIEW_REQUIRED, none canonical
# ---------------------------------------------------------------------------

REVIEW_REQUIRED = "REVIEW_REQUIRED"

CANDIDATES = [
 {"id": "RC-DOMAIN-RUBRIC-INSTANTIATION-001",
  "form": ["INSTANTIATED ADDRESS != NATIVE PARAMETER",
           "DOMAIN CONTAINER != RUBRIC",
           "RUBRIC APPLICATION != ONTOLOGY EXPANSION"],
  "found_in": "80 containers x the SAME 25 dimensions = 2,000 addresses",
  "status": REVIEW_REQUIRED, "canonical": 0, "support": 1},
 {"id": "RC-NO-EVIDENCE-NO-RANK-001",
  "form": ["NO VALIDATED EVIDENCE -> UNRANKED",
           "not ROW 1 -> 'BEST HYPOTHESIS'"],
  "found_in": "MATCH_ENGINE: every score 0, ranks 1..100 by row order",
  "status": REVIEW_REQUIRED, "canonical": 0, "support": 1},
 {"id": "RC-SCORE-CONFIDENCE-SEPARATION-001",
  "form": ["MATCH DIRECTION != MATCH MAGNITUDE",
           "MATCH MAGNITUDE != EVIDENCE QUALITY",
           "EVIDENCE QUALITY != EPISTEMIC CONFIDENCE"],
  "found_in": '=IF(ABS(L4)<0.2,...) — a -0.80 becomes "Very strong"',
  "status": REVIEW_REQUIRED, "canonical": 0, "support": 1},
 {"id": "RC-INDEPENDENT-LOOP-001",
  "form": ["LOOP COUNT != INDEPENDENCE",
           "DIFFERENT QUESTION != DIFFERENT EVIDENCE PATH",
           "REPEATED ROUTE != CORROBORATION"],
  "found_in": "five loops, 20 edges each, 1 distinct edge-set of 5",
  "status": REVIEW_REQUIRED, "canonical": 0, "support": 1},
 {"id": "RC-VISIBLE-ACTION-001",
  "form": ["VISIBLE ACTION != HIDDEN INTENT"],
  "found_in": "the ten King event forks", "status": REVIEW_REQUIRED,
  "canonical": 0, "support": 1},
 {"id": "RC-SAME-GOAL-DIFFERENT-ACTION-001",
  "form": ["SAME TERMINAL GOAL can be reached through DIFFERENT ACTIONS"],
  "found_in": "raise tax and lower tax both serving kingdom stability",
  "status": REVIEW_REQUIRED, "canonical": 0, "support": 1},
 {"id": "RC-FORMAL-VS-FUNCTIONAL-001",
  "form": ["FORMAL STATE != FUNCTIONAL STATE"],
  "found_in": "the abdication fork — title lost, influence retained",
  "his_note": "the freshest from this batch",
  "status": REVIEW_REQUIRED, "canonical": 0, "support": 1},
]

# His seven findings against the workbook, kept as findings rather than
# silently corrected. All seven verified against the file here.
WORKBOOK_FINDINGS = [
 {"n": 1, "finding": "2,000 rows != 2,000 independent primitive parameters",
  "verified": "80 containers, 1 distinct 25-dimension tuple of 80"},
 {"n": 2, "finding": "PYRAMID_INDEX formula range is wrong",
  "verified": "formula reads $B$2:$B$2001; actual P-rows are 4..2003, so "
              "P1999 and P2000 are excluded from S10 scoring"},
 {"n": 3, "finding": "zero evidence still creates a rank",
  "verified": "all 100 Final Scores 0, Rank column filled 1..100"},
 {"n": 4, "finding": "Confidence Band uses ABS(final score)",
  "verified": '=IF(ABS(L4)<0.2,"Weak",...) — -0.80 reads "Very strong"'},
 {"n": 5, "finding": "five loops are not five independent paths",
  "verified": "20 edges per loop, 1 distinct edge-set across all five"},
 {"n": 6, "finding": "ARD loop results do not feed MATCH_ENGINE",
  "verified": "L1..L5 Adj. are literal 0 (manual) while Parameter Match and "
              "Final Score are formulas"},
 {"n": 7, "finding": "the 100 weights normalize to 1.0 with no provenance",
  "verified": "every row sums to exactly 1.0000; no provenance column exists"},
]


def run(who: str = "", pack_id: str = "SP-01", event: str = "",
        rubrics: tuple = None) -> dict:
    """One locked identity, one brain-state, optionally one forked event."""
    g = generate(who, pack_id, rubrics)
    out = {
        "generation": g,
        "capacity": capacity(),
        "candidates": CANDIDATES,
        "workbook_findings": WORKBOOK_FINDINGS,
        "prose_only": list(PROSE_ONLY),
        "promoted": {"new canonical parameters": 0,
                     "new approved patterns": 0,
                     "approved candidates": 0},
        "gate": "every candidate is REVIEW_REQUIRED. Nothing here promotes.",
    }
    # LIVE INTENT — generated from the pack's own active containers, not
    # looked up. This is the bottleneck he named: "system is not generating the
    # new intent live".
    from . import intents as _intents
    out["live_intent"] = _intents.from_state_pack(who, pack_id, event or "")
    if event:
        out["fork"] = fork_event(event)
        if out["fork"].get("known") and event.strip().upper() == "ABDICATE":
            out["formal_vs_functional"] = formal_vs_functional()
    return out


def packs_index() -> list:
    return [{"id": p["id"], "name": p["name"], "model": p["model"],
             "conditions": p["conditions"],
             "containers": len(p["containers"]),
             "states": sorted({s for _n, s in p["containers"]}),
             "evidence": p["evidence"], "by": p["by"],
             "pairs_with": p.get("pairs_with"),
             "forks": p.get("forks", []),
             "law": p.get("law", ""), "holds": p.get("holds", ""),
             "refuses": p.get("refuses", "")}
            for p in STATE_PACKS]


def stats() -> dict:
    cs = {(n, s) for p in STATE_PACKS for n, s in p["containers"]}
    return {
        "state_packs": len(STATE_PACKS),
        "prose_only_kings": len(PROSE_ONLY),
        "containers_used": len({n for n, _s in cs}),
        "containers_total": len(hr.containers()),
        "states_used": len({s for _n, s in cs}),
        "states_total": STATES_TOTAL,
        "container_state_pairs_generated": len(cs),
        "rubrics": len(RUBRICS_25),
        "event_forks": len(EVENT_FORKS),
        "intent_routes_total": sum(len(v["routes"])
                                   for v in EVENT_FORKS.values()),
        "candidates": len(CANDIDATES),
        "canonical": 0,
        "native_bank": len(hr.parameters()),
        "source": "docs/method/canon/THE_GENERATION_SAME_PERSON_MANY_BRAINS.md",
    }


def annotations() -> list:
    return [
        ("keep the identity fixed, change the active parameter set",
         "statepacks.identity_lock"),
        ("container x state is the generator", "statepacks.runtime_address"),
        ("instantiated address is not a native parameter",
         "statepacks.RUNTIME_LAW"),
        ("same signal + changed history = different interpretation",
         "statepacks.same_signal_different_history"),
        ("one visible action, N intent routes, none chosen",
         "statepacks.fork_event"),
        ("formal state is not functional state",
         "statepacks.formal_vs_functional"),
        ("his seven findings against his own workbook",
         "statepacks.WORKBOOK_FINDINGS"),
    ]


RUNTIME_LAW = "INSTANTIATED ADDRESS != NATIVE PARAMETER"
