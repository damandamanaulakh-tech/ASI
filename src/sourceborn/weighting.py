"""CONTEXTUAL PARAMETER WEIGHTING — his BJP/Advani-Modi example, built as a
CANDIDATE and deliberately NOT approved.

His words:

    SAME PARAMETERS
    + DIFFERENT OBJECTIVE
    -> DIFFERENT PARAMETER IMPORTANCE
    -> DIFFERENT DECISION

    I would provisionally call it: Contextual Parameter Weighting

    A parameter does not have a fixed decision value. Its importance changes
    according to: current role · objective · environment · constraints ·
    available alternatives · expected outcome.

And the gate he put on it himself:

    I would keep this candidate alive but not approve it yet. The next example
    should come from a completely different domain — business, family, sports,
    medicine, school, etc. If the same structure fires again without forcing it,
    then ASI has started discovering something genuinely reusable rather than
    merely explaining BJP's 2013 decision.

So `PC-WEIGHT-001` ships at SUPPORT 1, CANONICAL 0, with `cross_domain_required`
True and the domains he named listed on it. It cannot be promoted from this
module — only he promotes.

His registry already names the mechanism: CON-047.04 **Attribute weighting**,
inside "Decision, Judgment and Trade-off Intelligence", whose own note reads
"Humans alternate between habitual, intuitive, deliberative and socially
influenced choices." The rows are his; the objective->weight table is mine and
says so on every row.

Canon: docs/method/canon/CONTEXTUAL_PARAMETER_WEIGHTING.md
"""

from __future__ import annotations

import re

from .asi_pyramid import (HELD, INFERRED, SOURCE_GROUNDED, container_span,
                          flat_of, param)

# ---------------------------------------------------------------------------
# THE AXES — the qualities a candidate can carry. His own list from the
# Advani/Modi comparison, generalised out of the political vocabulary so the
# same reader can meet a hospital rota or a club captaincy.
# ---------------------------------------------------------------------------

AXES = {
    "SENIORITY / TENURE": (
        "senior", "seniority", "most senior", "veteran", "founder", "founded",
        "started the", "oldest", "longest serving", "long history", "elder",
        "years in", "decades", "first joined"),
    "EXPERIENCE / DOMAIN DEPTH": (
        "experience", "experienced", "expertise", "expert", "handled",
        "has done", "had done", "practised", "practiced", "trained"),
    "INSTITUTIONAL MEMORY / LEGACY": (
        "institutional memory", "legacy", "tradition", "history of the",
        "party legacy", "custodian", "archive", "knows how it was"),
    "CURRENT POPULARITY / SUPPORT": (
        "popular", "popularity", "most popular", "groundswell", "followed him",
        "followed her", "following", "well liked", "public support",
        "dressing room", "cadre", "enthusiasm", "momentum"),
    "RECENT RECORD": (
        "won", "wins", "victories", "victory", "record", "brought in",
        "delivered", "consecutive", "last three", "last four", "last year",
        "recent", "track record", "most of these cases"),
    "ORGANISATIONAL BACKING": (
        "backing", "backed", "endorsed", "endorsement", "rss", "board",
        "management", "organisational", "organizational", "high command",
        "parliamentary board", "sponsor"),
    "MOBILISATION / CAMPAIGN REACH": (
        "campaign", "mobilis", "mobiliz", "visibility", "rally", "outreach",
        "canvass", "publicity", "reach"),
}

# ---------------------------------------------------------------------------
# THE OBJECTIVE TYPES. He supplied TWO of these himself — the competitive win
# ("winning the 2014 Lok Sabha election") and its counterfactual ("choose elder
# adviser / historical party authority / institutional mentor"). The rest are
# MINE, extended so the mechanism is not a political special case, and each one
# says whose it is. He can rewrite any row.
# ---------------------------------------------------------------------------

DOMINANT, HIGH, RELEVANT, NOT_DECISIVE = ("DOMINANT", "HIGH", "RELEVANT",
                                          "RELEVANT BUT NOT DOMINANT")

OBJECTIVE_TYPES = {
    "COMPETITIVE WIN": {
        "markers": ("win", "winning", "election", "tournament", "promotion",
                    "beat", "defeat", "contest", "market share", "championship",
                    "vote", "poll"),
        "weights": {
            "CURRENT POPULARITY / SUPPORT": DOMINANT,
            "MOBILISATION / CAMPAIGN REACH": DOMINANT,
            "RECENT RECORD": DOMINANT,
            "ORGANISATIONAL BACKING": HIGH,
            "EXPERIENCE / DOMAIN DEPTH": RELEVANT,
            "SENIORITY / TENURE": NOT_DECISIVE,
            "INSTITUTIONAL MEMORY / LEGACY": NOT_DECISIVE,
        },
        "by": "HIS — the 2014 objective, and his own weight ordering",
    },
    "STEWARDSHIP / COUNSEL / CONTINUITY": {
        "markers": ("adviser", "advisor", "mentor", "counsel", "custodian",
                    "trustee", "chair", "chairman", "guide", "elder",
                    "institutional", "authority", "continuity", "succession"),
        "weights": {
            "SENIORITY / TENURE": DOMINANT,
            "INSTITUTIONAL MEMORY / LEGACY": DOMINANT,
            "EXPERIENCE / DOMAIN DEPTH": HIGH,
            "ORGANISATIONAL BACKING": RELEVANT,
            "CURRENT POPULARITY / SUPPORT": NOT_DECISIVE,
            "MOBILISATION / CAMPAIGN REACH": NOT_DECISIVE,
            "RECENT RECORD": RELEVANT,
        },
        "by": "HIS — the counterfactual objective he named himself",
    },
    "THROUGHPUT / EXECUTION / SAFETY": {
        "markers": ("clear the backlog", "backlog", "safely", "safety",
                    "deliver", "throughput", "operate", "list", "deadline",
                    "on time", "output", "volume", "quality"),
        "weights": {
            "RECENT RECORD": DOMINANT,
            "EXPERIENCE / DOMAIN DEPTH": DOMINANT,
            "SENIORITY / TENURE": RELEVANT,
            "ORGANISATIONAL BACKING": RELEVANT,
            "CURRENT POPULARITY / SUPPORT": NOT_DECISIVE,
            "MOBILISATION / CAMPAIGN REACH": NOT_DECISIVE,
            "INSTITUTIONAL MEMORY / LEGACY": RELEVANT,
        },
        "by": "MINE — extended from his mechanism, correctable",
    },
    "GROWTH / NEW REVENUE": {
        "markers": ("revenue", "growth", "new clients", "new customers",
                    "sales", "expand", "expansion", "scale", "pipeline"),
        "weights": {
            "RECENT RECORD": DOMINANT,
            "MOBILISATION / CAMPAIGN REACH": HIGH,
            "CURRENT POPULARITY / SUPPORT": HIGH,
            "EXPERIENCE / DOMAIN DEPTH": RELEVANT,
            "ORGANISATIONAL BACKING": RELEVANT,
            "SENIORITY / TENURE": NOT_DECISIVE,
            "INSTITUTIONAL MEMORY / LEGACY": NOT_DECISIVE,
        },
        "by": "MINE — extended from his mechanism, correctable",
    },
}

# What flips into what, when the machine is asked "and if the objective were
# different?" His own pairing is the first row.
COUNTERFACTUAL_PAIRS = {
    "COMPETITIVE WIN": "STEWARDSHIP / COUNSEL / CONTINUITY",
    "STEWARDSHIP / COUNSEL / CONTINUITY": "COMPETITIVE WIN",
    "THROUGHPUT / EXECUTION / SAFETY": "STEWARDSHIP / COUNSEL / CONTINUITY",
    "GROWTH / NEW REVENUE": "THROUGHPUT / EXECUTION / SAFETY",
}

ROLE_MARKERS = ("candidate", "one role", "role available", "one seat",
                "one position", "one job", "to fill", "position", "post",
                "seat", "job", "vacancy", "choose", "choosing",
                "chose", "select", "selecting", "selected", "appoint",
                "appointed", "hire", "hiring", "nominate", "nominated",
                "pick", "picked", "captain", "who should", "the post",
                "was needed", "elevation")
OBJECTIVE_MARKERS = ("objective", "aim", "target", "goal", "task", "purpose",
                     "in order to", "so as to", "for winning", "to win",
                     "was to", "brief")


def _has(text: str, words) -> list:
    low = " " + (text or "").lower() + " "
    return [w for w in words
            if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low)]


def _sentences(text: str) -> list:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\s+/\s+", text or "")
            if s.strip()]


# ---------------------------------------------------------------------------
# READ THE SELECTION
# ---------------------------------------------------------------------------

_TITLE = r"(?:Dr|Mr|Mrs|Ms|Shri|Smt|Prof)\.?"
_KIN = ("uncle", "cousin", "father", "brother", "sister", "aunt", "mother",
        "son", "daughter", "nephew", "niece", "grandfather")


def _surname(who: str) -> str:
    return re.sub(r"^(?:" + _TITLE + r"|my|his|her|our|their)\s+", "", who,
                  flags=re.I).split()[-1].lower()


def candidates_in(text: str) -> list:
    """Who is being compared. Named people, titled people, or kinship terms —
    a family case names "my uncle", not a proper noun, and the mechanism has to
    survive that or it is a politics-only reader.

    Deduped by SURNAME: "L.K. Advani" and "Advani" are one person, and counting
    them twice made the first run report three candidates for two people."""
    found, by_surname = [], {}
    stop = {"the", "he", "she", "they", "his", "her", "one", "and", "but",
            "there", "it", "this", "that", "was", "had", "who", "dr", "mr",
            "mrs", "ms", "prof", "shri", "smt", "by", "in", "on", "at", "for",
            "lok", "sabha", "bjp", "rss", "gujarat"}

    def add(who, kind):
        key = _surname(who)
        if key in stop:
            return
        prev = by_surname.get(key)
        if prev is None:
            row = {"who": who, "kind": kind, "surname": key,
                   "forms": [who]}
            by_surname[key] = row
            found.append(row)
        else:
            if who not in prev["forms"]:
                prev["forms"].append(who)
            # keep the longest surface form as the display name
            if len(who) > len(prev["who"]):
                prev["who"] = who

    for m in re.finditer(_TITLE + r"\s+([A-Z][a-z]+)", text or ""):
        add(m.group(0), "titled")
    for m in re.finditer(r"\b(?:my|his|her|our|their)\s+(" +
                         "|".join(_KIN) + r")\b", text or "", re.I):
        add(m.group(0), "kinship")
    # A FULL NAME — two capitalised words in a row — is a person on a single
    # mention. Requiring recurrence made "Rahul Bose" and "Aman Verma"
    # invisible, which is the same defect as the actor being invisible in the
    # Samrath sentence: a person named once is still a person.
    for m in re.finditer(r"\b((?:[A-Z]\.\s?){0,2}[A-Z][a-z]{2,}"
                         r"(?:\s+[A-Z][a-z]{2,})?)\b", text or ""):
        who = m.group(1).strip()
        parts = who.split()
        if any(w.lower() in stop for w in parts):
            continue
        if re.search(_TITLE + r"\s+" + re.escape(who), text or ""):
            continue
        initials = bool(re.match(r"[A-Z]\.", who))
        full_name = len(parts) >= 2
        recurs = len(re.findall(r"\b" + re.escape(parts[-1]) + r"\b",
                               text or "")) >= 2
        if initials or full_name or recurs or _surname(who) in by_surname:
            add(who, "named")
    return found


LOWER_MARKERS = ("less", "not", "no", "junior", "fewer", "lacked", "lacks",
                 "without", "least", "lower", "weaker", "behind")


def _mentions(text: str, cand: dict) -> list:
    """Every character offset where this candidate is named."""
    out = []
    for form in set(cand["forms"] + [cand["surname"]]):
        for m in re.finditer(r"\b" + re.escape(form) + r"\b", text or "",
                             re.I):
            out.append(m.start())
    return sorted(set(out))


def attributes_for(text: str, cand: dict, others: list = None) -> list:
    """Which axes the source attributes to THIS candidate.

    Attribution is by NEAREST MENTION inside the sentence, not by "the sentence
    mentions them" — one sentence naming both people made every candidate
    inherit every quality, which is the leak this closes. Each axis also
    carries a DIRECTION, because "Modi was less senior than Advani" attributes
    LOW seniority to Modi and HIGH seniority to Advani, and crediting Modi with
    seniority there would be a fabrication."""
    others = [o for o in (others or []) if o["surname"] != cand["surname"]]
    out = {}
    for s in _sentences(text):
        mine = _mentions(s, cand)
        theirs = {o["surname"]: _mentions(s, o) for o in others}
        if not mine:
            continue
        for axis, words in AXES.items():
            for w in words:
                for m in re.finditer(r"(?<![a-z])" + re.escape(w) +
                                     r"(?![a-z])", s.lower()):
                    at = m.start()
                    d_mine = min(abs(at - x) for x in mine)
                    nearest_other, d_other = None, 10 ** 9
                    for sn, pos in theirs.items():
                        if not pos:
                            continue
                        d = min(abs(at - x) for x in pos)
                        if d < d_other:
                            nearest_other, d_other = sn, d
                    # a comparative — "less senior than Advani" — gives the
                    # LOW side to the nearer name and HIGH to the one after
                    # "than"
                    window = s.lower()[max(0, at - 40):at]
                    lower = bool(_has(window, LOWER_MARKERS))
                    after = s.lower()[m.end():m.end() + 40]
                    than = re.search(r"\bthan\s+(?:[a-z]\.\s?){0,2}"
                                     r"([a-z]+)", after)
                    if than and lower:
                        target = than.group(1)
                        if target == cand["surname"]:
                            out.setdefault(axis, {"axis": axis, "evidence": [],
                                                  "direction": "HIGH",
                                                  "clause": s})
                            out[axis]["direction"] = "HIGH"
                            out[axis]["evidence"].append(w)
                            continue
                        if d_mine <= d_other:
                            row = out.setdefault(axis, {
                                "axis": axis, "evidence": [],
                                "direction": "LOW", "clause": s})
                            row["direction"] = "LOW"
                            row["evidence"].append(w)
                            continue
                    if d_mine > d_other:
                        continue
                    row = out.setdefault(axis, {
                        "axis": axis, "evidence": [],
                        "direction": "LOW" if lower else "HIGH",
                        "clause": s})
                    if w not in row["evidence"]:
                        row["evidence"].append(w)
                    if lower and row["direction"] == "HIGH":
                        row["direction"] = "LOW"
    return list(out.values())


def objective_in(text: str) -> dict:
    """The objective the role is being filled FOR. His whole point is that this
    is the thing that sets the weights, so if it is absent the machine must say
    so rather than assume one."""
    stated, marker = None, None
    for s in _sentences(text):
        m = _has(s, OBJECTIVE_MARKERS)
        if m:
            stated, marker = s, m[0]
            break
    kinds = []
    for name, spec in OBJECTIVE_TYPES.items():
        hit = _has(text, spec["markers"])
        if hit:
            kinds.append({"type": name, "evidence": hit, "by": spec["by"]})
    return {
        "stated": stated,
        "marker": marker,
        "types": kinds,
        "type": kinds[0]["type"] if len(kinds) == 1 else
                (kinds[0]["type"] if kinds else None),
        "ambiguous": len(kinds) > 1,
        "absent": not kinds,
        "held": ("no objective is named, so no weighting is legal — the "
                 "importance of a parameter cannot be read without one"
                 if not kinds else ""),
    }


def read_selection(text: str) -> dict:
    """One role, two or more candidates, their axes, and the objective."""
    role = _has(text, ROLE_MARKERS)
    cands = candidates_in(text)
    rows = []
    for c in cands:
        attrs = attributes_for(text, c, cands)
        if attrs:
            rows.append({**c, "axes": attrs})
    obj = objective_in(text)
    return {
        "role_markers": role,
        "role_named": bool(role),
        "candidates": rows,
        "candidate_count": len(rows),
        "objective": obj,
        "applies": bool(role) and len(rows) >= 2 and not obj["absent"],
        "why_not": ([] if bool(role) and len(rows) >= 2 and not obj["absent"]
                    else
                    ([] if role else ["no role or selection is named"]) +
                    ([] if len(rows) >= 2 else
                     ["fewer than two candidates carry attributed qualities"]) +
                    ([] if not obj["absent"] else ["no objective is named"])),
    }


# ---------------------------------------------------------------------------
# THE WEIGHTING
# ---------------------------------------------------------------------------

def weigh(text: str, objective_type: str = None) -> dict:
    """His mechanism: the objective activates the weights, and the SAME axes
    carry different importance under a different objective."""
    sel = read_selection(text)
    obj_type = objective_type or sel["objective"].get("type")
    if not obj_type or obj_type not in OBJECTIVE_TYPES:
        return {"selection": sel, "objective_type": obj_type,
                "weights": {}, "per_candidate": [],
                "verdict": "NO WEIGHTING — no objective type is established",
                "refuses": "a parameter's importance cannot be read without an "
                           "objective. Nothing is scored."}
    spec = OBJECTIVE_TYPES[obj_type]
    axes_present = sorted({a["axis"] for c in sel["candidates"]
                           for a in c["axes"]})
    weights = {ax: spec["weights"].get(ax, RELEVANT) for ax in axes_present}
    per = []
    for c in sel["candidates"]:
        held = [a["axis"] for a in c["axes"] if a["direction"] == "HIGH"]
        deficit = [a["axis"] for a in c["axes"] if a["direction"] == "LOW"]
        dom = [ax for ax in held if weights.get(ax) == DOMINANT]
        hi = [ax for ax in held if weights.get(ax) == HIGH]
        low = [ax for ax in held if weights.get(ax) == NOT_DECISIVE]
        per.append({
            "who": c["who"], "kind": c["kind"],
            "axes_held": held, "axes_low": deficit,
            "dominant_axes": dom, "high_axes": hi, "not_decisive_axes": low,
            "band": (DOMINANT if dom else HIGH if hi else RELEVANT),
        })
    per.sort(key=lambda r: (-len(r["dominant_axes"]), -len(r["high_axes"])))
    favoured = [r for r in per
                if (len(r["dominant_axes"]), len(r["high_axes"])) ==
                (len(per[0]["dominant_axes"]), len(per[0]["high_axes"]))] \
        if per else []
    return {
        "selection": sel,
        "objective_type": obj_type,
        "objective_by": spec["by"],
        "weights": weights,
        "per_candidate": per,
        "favoured": [r["who"] for r in favoured],
        "tied": len(favoured) > 1,
        "verdict": ("the weighting under this objective favours "
                    + " and ".join(r["who"] for r in favoured)
                    if favoured else "no candidate carries a weighted axis"),
        "refuses": "this is what the WEIGHTING favours. It is not a claim about "
                   "why the decision was actually made, and it is not a ranking "
                   "of the people.",
    }


def counterfactual(text: str) -> dict:
    """His own falsifier: "If the objective had instead been: choose elder
    adviser / historical party authority / institutional mentor then the
    weighting could have been completely different."

    This is the part that makes the candidate testable rather than a
    restatement of what happened."""
    a = weigh(text)
    if not a["objective_type"]:
        return {"available": False,
                "why": "no objective, so there is nothing to vary"}
    other = COUNTERFACTUAL_PAIRS.get(a["objective_type"])
    b = weigh(text, other)
    flips = []
    for ax in sorted(set(a["weights"]) | set(b["weights"])):
        wa, wb = a["weights"].get(ax), b["weights"].get(ax)
        if wa != wb:
            flips.append({"axis": ax, "under_" + a["objective_type"]: wa,
                          "under_" + other: wb})
    return {
        "available": True,
        "actual_objective": a["objective_type"],
        "counterfactual_objective": other,
        "counterfactual_by": OBJECTIVE_TYPES[other]["by"],
        "weight_flips": flips,
        "flip_count": len(flips),
        "favoured_actual": a["favoured"],
        "favoured_counterfactual": b["favoured"],
        "selection_changes": sorted(a["favoured"]) != sorted(b["favoured"]),
        "his_words": "the weighting could have been completely different",
        "refuses": "this is a counterfactual, not a claim about history. "
                   "Nothing here says the other objective was on the table.",
    }


# ---------------------------------------------------------------------------
# THE REFUSALS — his two named wrong lessons, stored so they cannot be learnt
# ---------------------------------------------------------------------------

REFUSED_LESSONS = [
    {"claim": "young leader > senior leader", "his_verdict": "Wrong."},
    {"claim": "popularity > experience", "his_verdict": "Also wrong."},
    {"claim": "Modi was more popular, therefore he was the better leader",
     "his_verdict": "shallower than the actual finding"},
]

MAY_LEARN = "PARAMETER IMPORTANCE IS ITSELF CONTEXT-DEPENDENT."


def rank_is_not_fitness(text: str) -> dict:
    """His block, made mechanical:

        highest seniority?  YES
              !=
        therefore highest suitability for this task?  NOT AUTOMATIC
    """
    sel = read_selection(text)
    top = []
    for c in sel["candidates"]:
        for a in c["axes"]:
            if a["axis"] == "SENIORITY / TENURE" and \
                    a["direction"] == "HIGH":
                top.append(c["who"])
    return {
        "highest_on_axis": sorted(set(top)),
        "axis": "SENIORITY / TENURE",
        "answer": "YES — the source attributes it" if top else
                  "not attributed in this source",
        "therefore_most_suitable": "NOT AUTOMATIC",
        "why": "suitability is scored against what the ROLE requires, and the "
               "role is defined by the objective. Rank on one axis is one "
               "parameter, not the decision function.",
        "asks_instead": ["Popular for what?", "Experienced for what?",
                         "Senior for what?", "Selected for what objective?"],
        "his_words": "So seniority was one parameter, not the complete "
                     "decision function.",
    }


# ---------------------------------------------------------------------------
# HIS REGISTRY ROWS FOR THIS SHAPE
# ---------------------------------------------------------------------------

ROW_ROUTES = {
 "CON-047": [(3, "axes_present", SOURCE_GROUNDED,
              "the attributes are identified from the source"),
             (4, "weights_set", SOURCE_GROUNDED,
              "ATTRIBUTE WEIGHTING — his registry's own name for this mechanism"),
             (7, "two_or_more_candidates", SOURCE_GROUNDED,
              "more than one attribute is integrated per candidate"),
             (8, "two_or_more_candidates", SOURCE_GROUNDED,
              "a trade-off between candidates is resolved"),
             (19, "weights_set", SOURCE_GROUNDED,
              "the frame — the objective — changes what matters"),
             (18, "weights_set", INFERRED,
              "the reference point moves with the objective"),
             (36, "backing_named", INFERRED,
              "the choice is group-influenced where backing is named"),
             (40, "counterfactual_ran", INFERRED,
              "the decision's quality is being monitored against the objective"),
             (26, "contested", HELD,
              "confidence in the choice is not stated — it was contested")],
 "CON-045": [(2, "role_named", SOURCE_GROUNDED, "the problem is defined as a role to fill"),
             (4, "objective_named", SOURCE_GROUNDED, "the goal is clarified"),
             (28, "weights_set", SOURCE_GROUNDED, "the key variable is which axis dominates"),
             (32, "objective_named", INFERRED, "the objective function is named"),
             (38, "seniority_axis", SOURCE_GROUNDED,
              "\"who is most senior\" would be the WRONG PROBLEM")],
 "CON-046": [(9, "two_or_more_candidates", SOURCE_GROUNDED, "two routes compared"),
             (14, "counterfactual_ran", SOURCE_GROUNDED,
              "the other objective is simulated"),
             (33, "objective_named", INFERRED, "a long-horizon objective")],
 "CON-064": [(36, "weights_set", SOURCE_GROUNDED,
              "VALUE RANKING — the axes are ranked, not scored absolutely"),
             (34, "weights_set", SOURCE_GROUNDED,
              "a priority structure over the axes"),
             (33, "contested", SOURCE_GROUNDED,
              "competing motives are detected — the decision was contested")],
 "CON-076": [(33, "seniority_axis", HELD,
              "AUTHORITY BIAS is the trap seniority sets — named, not asserted"),
             (16, "seniority_axis", HELD,
              "STATUS-QUO BIAS — held, not claimed of anyone"),
             (29, "popularity_axis", HELD,
              "HALO EFFECT — popularity spilling onto unrelated axes, held")],
 "CON-078": [(16, "seniority_axis", INFERRED,
              "the boundary of competence is what the objective tests"),
             (28, "objective_named", INFERRED,
              "expert intuition is unreliable when the environment changes"),
             (23, "record_axis", INFERRED, "adaptive rather than routine expertise")],
 "CON-034": [(15, "experience_axis", SOURCE_GROUNDED, "domain knowledge is attributed"),
             (14, "memory_axis", SOURCE_GROUNDED, "world knowledge / institutional memory")],
 "CON-071": [(19, "seniority_axis", SOURCE_GROUNDED,
              "a rank/hierarchy is being perceived"),
             (18, "popularity_axis", INFERRED, "status seeking within the group"),
             (24, "backing_named", SOURCE_GROUNDED, "a coalition is formed around a choice")],
}


def signals(text: str) -> dict:
    sel = read_selection(text)
    cf = counterfactual(text)
    w = weigh(text)
    axes = {a["axis"] for c in sel["candidates"] for a in c["axes"]}
    out = {}

    def add(k, why):
        out[k] = {"why": why}

    if sel["role_named"]:
        add("role_named", "a role or selection is named")
    if sel["candidate_count"] >= 2:
        add("two_or_more_candidates", "%d candidates carry attributed qualities"
            % sel["candidate_count"])
    if not sel["objective"]["absent"]:
        add("objective_named", "an objective is named: %s"
            % sel["objective"]["type"])
    if axes:
        add("axes_present", "%d axes attributed" % len(axes))
    if w.get("weights"):
        add("weights_set", "the objective activated a weighting")
    if cf.get("available"):
        add("counterfactual_ran", "the other objective was simulated")
    if "SENIORITY / TENURE" in axes:
        add("seniority_axis", "seniority is attributed")
    if "CURRENT POPULARITY / SUPPORT" in axes:
        add("popularity_axis", "popularity is attributed")
    if "RECENT RECORD" in axes:
        add("record_axis", "a recent record is attributed")
    if "EXPERIENCE / DOMAIN DEPTH" in axes:
        add("experience_axis", "experience is attributed")
    if "INSTITUTIONAL MEMORY / LEGACY" in axes:
        add("memory_axis", "institutional memory is attributed")
    if "ORGANISATIONAL BACKING" in axes:
        add("backing_named", "organisational backing is attributed")
    if _has(text, ("opposed", "contested", "resigned", "objection",
                   "disagreed", "against the move", "internal")):
        add("contested", "the decision is stated to have been contested")
    return out


def rows_for(text: str) -> dict:
    """The exact P rows this shape reaches, in his addressing."""
    sig = signals(text)
    out, tiers = [], {SOURCE_GROUNDED: 0, INFERRED: 0, HELD: 0}
    seen = set()
    for cid, table in ROW_ROUTES.items():
        for pos, signal, tier, why in table:
            if signal not in sig:
                continue
            flat = flat_of(cid, pos)
            if flat in seen:
                continue
            seen.add(flat)
            p = param(flat)
            out.append({"flat": flat, "p": p["p"], "sb_id": p["sb_id"],
                        "name": p["name"], "pos": pos, "container": cid,
                        "container_name": p["container_name"],
                        "span": container_span(cid),
                        "segment": p["segment"],
                        "segment_name": p["segment_name"],
                        "tier": tier, "signal": signal, "why": why,
                        "by": "resolved here (correctable)"})
            tiers[tier] += 1
    out.sort(key=lambda r: r["flat"])
    return {"rows": out, "counts": {
        "rows": len(out), "source_grounded": tiers[SOURCE_GROUNDED],
        "inferred": tiers[INFERRED], "held_open": tiers[HELD],
        "containers": len({r["container"] for r in out}),
        "segments": len({r["segment"] for r in out}),
        "bank": 3204, "untouched": 3204 - len(out)}}


# ---------------------------------------------------------------------------
# THE CANDIDATE — ALIVE, NOT APPROVED
# ---------------------------------------------------------------------------

CANDIDATE_ID = "PC-WEIGHT-001"
HIS_DOMAINS = ("business", "family", "sports", "medicine", "school")


def candidate(text: str = None) -> dict:
    """`PC-WEIGHT-001` at SUPPORT 1, CANONICAL 0, with his own promotion gate
    on it. Nothing in this module can approve it."""
    fired = bool(text) and read_selection(text)["applies"]
    return {
        "id": CANDIDATE_ID,
        "name": "Contextual Parameter Weighting",
        "provisional_name_by": "HIS",
        "form": ["SAME PARAMETERS", "DIFFERENT OBJECTIVE",
                 "DIFFERENT PARAMETER IMPORTANCE", "DIFFERENT DECISION"],
        "statement": "A parameter does not have a fixed decision value. Its "
                     "importance changes according to: current role · "
                     "objective · environment · constraints · available "
                     "alternatives · expected outcome.",
        "may_learn": MAY_LEARN,
        "refused": REFUSED_LESSONS,
        "support": 1,
        "support_from": ["BJP 2013 — one strong political case"],
        "canonical": 0,
        "status": "ALIVE — NOT APPROVED",
        "gate": {
            "cross_domain_required": True,
            "domains_he_named": list(HIS_DOMAINS),
            "condition": "the next example must come from a completely "
                         "different domain, and the same structure must fire "
                         "again WITHOUT being forced",
            "who_approves": "him — this module cannot promote it",
        },
        "fired_on_this_ask": fired,
    }


def cross_domain_probe(cases: dict) -> dict:
    """Does the structure fire outside politics without being forced?

    Honest by construction: it reports whatever it gets, per case, including a
    NO. The detector was written from his BJP structure and was not tuned to
    any case passed in here."""
    out = []
    for label, text in cases.items():
        sel = read_selection(text)
        w = weigh(text)
        cf = counterfactual(text)
        out.append({
            "case": label,
            "domain": label.split(":")[0].strip() if ":" in label else label,
            "fires": sel["applies"],
            "why_not": sel["why_not"],
            "candidates": [c["who"] for c in sel["candidates"]],
            "objective_type": sel["objective"].get("type"),
            "favoured": w.get("favoured", []),
            "counterfactual_objective": cf.get("counterfactual_objective"),
            "favoured_counterfactual": cf.get("favoured_counterfactual", []),
            "selection_changes": cf.get("selection_changes"),
        })
    fired = [r for r in out if r["fires"]]
    flipped = [r for r in fired if r["selection_changes"]]
    return {
        "cases": out,
        "total": len(out),
        "fired": len(fired),
        "flipped_under_counterfactual": len(flipped),
        "domains_fired": sorted({r["domain"] for r in fired}),
        "verdict": ("the structure fires in %d of %d non-political cases and "
                    "the selection flips under the counterfactual objective in "
                    "%d of them" % (len(fired), len(out), len(flipped))),
        "still_not_approved": True,
        "who_approves": "him",
    }


def run(text: str) -> dict:
    """The whole reading for a selection-under-objective ask."""
    sel = read_selection(text)
    return {
        "selection": sel,
        "weighting": weigh(text),
        "counterfactual": counterfactual(text),
        "rank_is_not_fitness": rank_is_not_fitness(text),
        "row_level": rows_for(text),
        "candidate": candidate(text),
        "may_learn": MAY_LEARN,
        "refused": REFUSED_LESSONS,
        "asks_instead": ["Popular for what?", "Experienced for what?",
                         "Senior for what?", "Selected for what objective?"],
    }


def stats() -> dict:
    return {"axes": len(AXES), "objective_types": len(OBJECTIVE_TYPES),
            "his_objective_types": sum(1 for v in OBJECTIVE_TYPES.values()
                                       if v["by"].startswith("HIS")),
            "refused_lessons": len(REFUSED_LESSONS),
            "candidate": CANDIDATE_ID, "canonical": 0,
            "source": "docs/method/canon/CONTEXTUAL_PARAMETER_WEIGHTING.md"}


def annotations() -> list:
    return [
        ("same parameters + different objective = different importance",
         "weighting.weigh"),
        ("his counterfactual objective, which makes it testable",
         "weighting.counterfactual"),
        ("highest seniority != highest suitability",
         "weighting.rank_is_not_fitness"),
        ("the two lessons he refused", "weighting.REFUSED_LESSONS"),
        ("alive, not approved, cross-domain gate on it",
         "weighting.candidate"),
        ("does it fire outside politics without forcing",
         "weighting.cross_domain_probe"),
    ]
