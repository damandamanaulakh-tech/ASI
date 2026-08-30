"""LIVE INTENT GENERATION — the bottleneck he named.

His words:

    concept is simple as much parameters we plug, we will generate more pattern
    and intent

    as of now main bottleneck is system is not generating the new intent live

He is right, and the diagnosis is exact. Before this module:

  * `statepacks.EVENT_FORKS` was a HARDCODED dict of ten events with his routes
    typed in. An event he had not named returned nothing.
  * `asi_pyramid.INTERPRETATION_FRAMES` returned SEVEN frames whatever the ask
    was — a fixed list, not a generation.

Neither of those reads the parameter bank. So plugging more parameters changed
nothing, which is the opposite of his concept.

WHAT THIS DOES INSTEAD

Intent is generated at runtime FROM HIS OWN ROWS:

    CON-064  Motive, Needs, Values and Priority Structure   40 rows  = the WHY
    CON-063  Intent Formation and Commitment                40 rows  = the SHAPE

A motive is REACHABLE from a container when that container carries a
sub-parameter echoing it — computed over the bank, never hand-typed. So the
active container set decides which motives can be raised, and the intent count
rises as more containers come active. That is his concept, made mechanical:

    more parameters active  ->  more motives reachable  ->  more intent candidates

NOTHING IS ADDED TO THE BANK. Every generated intent is a runtime object with no
P id of its own; it cites the motive row and the form row it was built from.
Motive-inference confidence is his P2564 and it stays LOW: the machine generates
candidates and never concludes one.

THE FABRICATION GUARD, AND WHY IT IS HERE

Naive head-word matching produced 200 edges, and roughly a third were lexical
coincidences of exactly the kind that scored zero on the Samrath sentence:
"Recognition/status need" linked to "Shape recognition", "Face-saving motive" to
"Face detection", "Power/control need" to "Power-grip control". Perception,
motor and language containers cannot originate a motive, so those segments are
blocked from hosting one. The gate removes 67 edges, and every surviving edge is
reported with its host segment so he can strike any of them.

Canon: docs/method/canon/LIVE_INTENT_GENERATION.md
"""

from __future__ import annotations

import re
from functools import lru_cache

from . import human_registry as hr
from .asi_pyramid import CURRENT, FUTURE, PRIOR, flat_of, param

MOTIVE_CON = "CON-064"      # his motive vocabulary — the WHY
FORM_CON = "CON-063"        # his intent forms — the SHAPE

# Segments that can HOST a motive. Perception (SEG-02), sensorimotor (SEG-03),
# attention mechanics (SEG-04) and language (SEG-07) cannot originate one —
# that is where every false edge came from.
BLOCKED_HOSTS = ("SEG-02", "SEG-03", "SEG-04", "SEG-07")

_HEAD_STOP = {"motive", "need", "the", "and", "of", "or", "vs", "a", "actual"}


def _head(name: str) -> str:
    ws = [w for w in re.findall(r"[a-z]+", (name or "").lower())
          if w not in _HEAD_STOP and len(w) > 3]
    return ws[0] if ws else ""


@lru_cache(maxsize=1)
def motive_rows() -> tuple:
    """His 40 motive rows, with their flat P ids."""
    subs = hr.container(MOTIVE_CON)["subs"]
    return tuple({"pos": i, "name": s, "flat": flat_of(MOTIVE_CON, i),
                  "p": "P%d" % flat_of(MOTIVE_CON, i)}
                 for i, s in enumerate(subs, 1))


@lru_cache(maxsize=1)
def form_rows() -> tuple:
    """His 40 intent-form rows, with their flat P ids."""
    subs = hr.container(FORM_CON)["subs"]
    return tuple({"pos": i, "name": s, "flat": flat_of(FORM_CON, i),
                  "p": "P%d" % flat_of(FORM_CON, i)}
                 for i, s in enumerate(subs, 1))


@lru_cache(maxsize=1)
def motive_links() -> dict:
    """Which containers can reach which motive — COMPUTED over his bank.

    An edge means: this container carries a sub-parameter echoing this motive,
    so an active state in that container can raise it. Every edge reports the
    sub-parameter it matched and the host segment, so a bad edge is visible
    rather than buried."""
    out = {}
    for m in motive_rows():
        h = _head(m["name"])
        edges = []
        if h:
            for c in hr.containers():
                if c["id"] == MOTIVE_CON or c["segment"] in BLOCKED_HOSTS:
                    continue
                for j, s in enumerate(c["subs"], 1):
                    if h in s.lower():
                        edges.append({
                            "container": c["id"], "container_name": c["name"],
                            "segment": c["segment"],
                            "matched": s,
                            "matched_p": "P%d" % flat_of(c["id"], j),
                            "on": h})
                        break
        out[m["name"]] = {"motive": m, "edges": edges,
                          "reachable_from": [e["container"] for e in edges]}
    return out


def unlinked() -> list:
    """Motive rows with no echo anywhere else in his 3,204.

    Two are machinery rather than motives (Stated / Operating). The other three
    are real human motives with no representation in the bank outside CON-064
    itself — reported as an absence, not filled in."""
    ml = motive_links()
    out = []
    for m in motive_rows():
        if ml[m["name"]]["edges"]:
            continue
        machinery = m["name"].lower().startswith(("stated", "operating"))
        out.append({"motive": m["name"], "p": m["p"],
                    "kind": "machinery row, not a motive" if machinery
                            else "a real motive with no echo in the bank",
                    "absence": not machinery})
    return out


# ---------------------------------------------------------------------------
# WHICH FORM the intent takes — chosen by the scope already computed upstream,
# not guessed. His own row names.
# ---------------------------------------------------------------------------

FORM_BY_SCOPE = {
    CURRENT: ("Immediate-intention formation", "Action commitment",
              "Behavioural-intention formation", "Volitional commitment"),
    FUTURE: ("Future-intention formation", "Deadline-linked intention",
             "Implementation intention (if-then)", "Precommitment",
             "Intention maintenance"),
    PRIOR: ("Intention decay over time", "Intention abandonment",
            "Intention revision", "Intention reactivation"),
}
FORM_CONDITIONAL = ("Contingent intention (only if X)",
                    "Conditional-commitment setting",
                    "Opportunity-triggered intention")
FORM_CONFLICT = ("Competing-intention arbitration",
                 "Intention conflict resolution", "Intention shielding")


def _forms_for(scope: str, conditional: bool, conflict: bool) -> list:
    want = list(FORM_BY_SCOPE.get(scope, ()))
    if conditional:
        want += list(FORM_CONDITIONAL)
    if conflict:
        want += list(FORM_CONFLICT)
    by = {f["name"]: f for f in form_rows()}
    return [by[w] for w in want if w in by]


# ---------------------------------------------------------------------------
# THE GENERATOR
# ---------------------------------------------------------------------------

CANDIDATE = "INTENT CANDIDATE"


def generate(event: str, active_containers, scope: str = CURRENT,
             states: dict = None, conditional: bool = False,
             conflict: bool = False, limit: int = 0) -> dict:
    """Generate intent candidates live, from the active parameter set.

    `active_containers` is what is currently switched on — from a state pack,
    from a reading, or handed in directly. Every motive reachable from those
    containers is raised, crossed with the forms the scope allows.

    The count is a function of the active set. That is the whole point."""
    active = [c if isinstance(c, str) else "CON-%03d" % int(c)
              for c in (active_containers or [])]
    states = states or {}
    ml = motive_links()
    raised, blocked = [], []
    for m in motive_rows():
        edges = [e for e in ml[m["name"]]["edges"] if e["container"] in active]
        if not edges:
            if ml[m["name"]]["edges"]:
                blocked.append({"motive": m["name"], "p": m["p"],
                                "why": "reachable, but none of its containers "
                                       "is active"})
            continue
        raised.append({"motive": m, "raised_by": edges})

    forms = _forms_for(scope, conditional, conflict)
    out = []
    for r in raised:
        for f in forms:
            e = r["raised_by"][0]
            out.append({
                "id": "IC-%s-%s" % (r["motive"]["p"], f["p"]),
                "status": CANDIDATE,
                "event": event or "(no event shell)",
                "why": r["motive"]["name"],
                "why_p": r["motive"]["p"],
                "shape": f["name"],
                "shape_p": f["p"],
                "scope": scope,
                "raised_by": {"container": e["container"],
                              "container_name": e["container_name"],
                              "segment": e["segment"],
                              "state": states.get(e["container"], "active"),
                              "matched_row": e["matched"],
                              "matched_p": e["matched_p"]},
                "reachable_from": [x["container"] for x in r["raised_by"]],
                "is_native_parameter": False,
                "in_bank": False,
                "concluded": False,
            })
    dropped = 0
    if limit and len(out) > limit:
        dropped = len(out) - limit
        out = out[:limit]
    conf = param(flat_of(MOTIVE_CON, 40))
    return {
        "event": event or "(no event shell)",
        "active_containers": active,
        "scope": scope,
        "candidates": out,
        "counts": {
            "active_containers": len(active),
            "motives_raised": len(raised),
            "motives_reachable_not_active": len(blocked),
            "forms_applicable": len(forms),
            "intents_generated": len(out),
            "dropped_by_cap": dropped,
            "motive_rows": len(motive_rows()),
            "form_rows": len(form_rows()),
            "native_parameters_added": 0,
        },
        "not_raised": blocked,
        "confidence": {"row": conf["name"], "p": "P%d" % conf["flat"]
                       if "flat" in conf else "P2564", "level": "LOW",
                       "why": "inferred motive must remain a hypothesis until "
                              "supported or confirmed — his own container note"},
        "chosen": None,
        "law": "MORE PARAMETERS ACTIVE -> MORE MOTIVES REACHABLE -> MORE "
               "INTENT CANDIDATES",
        "refuses": "these are generated candidates. None is concluded, none is "
                   "written to the bank, and the machine does not pick one.",
    }


def scaling(scope: str = CURRENT) -> dict:
    """Proof of his concept, computed rather than asserted: plug more
    containers, get more intent. Reported as a curve he can check."""
    cons = [c["id"] for c in hr.containers()]
    rows = []
    for n in (1, 2, 4, 8, 16, 24, 32, 48, 64, 80):
        r = generate("SCALING_TEST", cons[:n], scope=scope)
        rows.append({"active_containers": n,
                     "motives_raised": r["counts"]["motives_raised"],
                     "intents_generated": r["counts"]["intents_generated"]})
    return {
        "curve": rows,
        "monotonic": all(rows[i]["intents_generated"] <=
                         rows[i + 1]["intents_generated"]
                         for i in range(len(rows) - 1)),
        "ceiling": {"motive_rows": len(motive_rows()),
                    "form_rows": len(form_rows()),
                    "max_pairs": len(motive_rows()) * len(form_rows())},
        "law": "as much parameters we plug, we will generate more pattern and "
               "intent",
    }


def from_state_pack(who: str, pack_id: str, event: str = "",
                    scope: str = CURRENT) -> dict:
    """Generate intent live for one brain-state of one locked identity.

    This is the join his bottleneck needed: the state pack says which
    containers are active and in what state, and the intent is generated from
    that — not looked up from a table of ten events."""
    from . import statepacks as sp
    p = sp.pack(pack_id)
    active = ["CON-%03d" % n for n, _s in p["containers"]]
    states = {"CON-%03d" % n: s for n, s in p["containers"]}
    conflict = any(s == sp.CONFLICTED for _n, s in p["containers"])
    g = generate(event or p["name"].upper().replace(" ", "_"),
                 active, scope=scope, states=states, conflict=conflict)
    g["identity"] = sp.identity_lock(who)
    g["pack"] = {"id": p["id"], "name": p["name"], "model": p["model"],
                 "conditions": p["conditions"]}
    return g


def stats() -> dict:
    ml = motive_links()
    return {
        "motive_rows": len(motive_rows()),
        "form_rows": len(form_rows()),
        "max_intent_pairs": len(motive_rows()) * len(form_rows()),
        "motives_linked": sum(1 for v in ml.values() if v["edges"]),
        "link_edges": sum(len(v["edges"]) for v in ml.values()),
        "blocked_host_segments": list(BLOCKED_HOSTS),
        "unlinked": len(unlinked()),
        "real_absences": sum(1 for u in unlinked() if u["absence"]),
        "native_parameters_added": 0,
        "source": "docs/method/canon/LIVE_INTENT_GENERATION.md",
    }


def annotations() -> list:
    return [
        ("intent is generated live from the active parameter set",
         "intents.generate"),
        ("more parameters active means more intent", "intents.scaling"),
        ("the motive links are computed over his bank, not typed",
         "intents.motive_links"),
        ("perception, motor and language cannot originate a motive",
         "intents.BLOCKED_HOSTS"),
        ("motives with no echo anywhere in the bank", "intents.unlinked"),
        ("a state pack decides which intents can be generated",
         "intents.from_state_pack"),
    ]
