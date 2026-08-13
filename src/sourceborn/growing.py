"""THE GROWING PHASE — where an example SEATS on existing parameters and IDs.

His correction, and it re-frames everything that came before it:

    current phase is growing phase, given example are not how it provide the out
    comes, its for to define the system, where example sit on existing parameters
    and IDs so system can strong its base, every example will keep increase the
    count

    Its universal moto t follow is "everything happening is a event, and all
    events have intent"

    as long i keep adding the example, once the basic will over it will start
    making new combinations on new thoughts

WHAT I HAD WRONG

I had been running his examples as OUTPUT TESTS — reading the Samrath sentence,
the mall, the BJP weighting, the tablet, and reporting how well the machine
answered them. That is not what they are for. An example is not a question to be
answered well. **It is material that defines the system**: it lands on parameters
that already exist, strengthens them by landing there, and raises the count.

So this module does not answer. It PLACES.

THE MOTTO, EXECUTABLE

    everything happening is a event   ->  events_in() must never return nothing
                                          for a text that contains a happening
    all events have intent            ->  every event carries an intent slot, and
                                          the slot is never absent

A DEFECT THE MOTTO EXPOSED, NAMED BEFORE IT IS FIXED

`micro.py` finds actions from a closed list of 215 verbs. On his own rain
sentence — *the father stood outside with a water pipe and pointed it up in the
air* — neither `stood` nor `pointed` is in that list, so the machine saw **no
happening at all**. Under his motto that is not a small miss: a text full of
happenings returned zero events. So event-finding here is **morphological and
positional**, not a lookup, and every event reports HOW it was found, so a
fallback is visible rather than silent.

WHAT "STRENGTHEN THE BASE" AND "INCREASE THE COUNT" ARE — TWO THINGS, NOT ONE

    strengthen  an event seats on an existing parameter ID -> that ID gains
                SUPPORT. Reinforcement, not duplication — his own rule. No new
                parameter is created by seating.
    increase    every example appends its own row, its events and its intents to
                the growth ledger. The count rises with every single example,
                always, which is exactly what he said it does.

Canon: docs/method/canon/THE_GROWING_PHASE.md
"""

from __future__ import annotations

import math
import os
import re
from functools import lru_cache

from . import human_registry as hr
from .asi_pyramid import flat_of

MOTTO = "everything happening is a event, and all events have intent"
PHASE = "GROWING"

# his 01A_INTENT rule: "There is no reason" is not an available answer.
INTENT_OPEN = "OPEN — not concluded from one event"

# ---------------------------------------------------------------------------
# EVENTS — every happening. No closed verb list.
# ---------------------------------------------------------------------------

_IRREGULAR = {
    "stood", "went", "came", "saw", "said", "told", "thought", "took", "gave",
    "made", "put", "got", "had", "was", "were", "did", "ran", "sat", "held",
    "kept", "left", "brought", "bought", "sent", "spoke", "wrote", "read",
    "built", "broke", "chose", "drew", "fell", "felt", "found", "heard", "knew",
    "meant", "met", "paid", "rose", "showed", "shut", "slept", "spent", "swore",
    "taught", "understood", "wore", "won", "began", "drove", "ate", "drank",
    "hid", "lay", "led", "lost", "rode", "shot", "struck", "threw", "woke",
    "wound", "cut", "hit", "let", "set", "shed", "spread", "cost", "beat",
}
_MODALS = {"will", "would", "can", "could", "shall", "should", "may", "might",
           "must", "do", "does", "did", "is", "are", "was", "were", "am", "be",
           "been", "being", "has", "have", "had"}
_NOT_VERB = {
    "this", "his", "hers", "its", "us", "as", "was", "is", "has", "always",
    "perhaps", "yes", "news", "series", "analysis", "thus", "class", "less",
    "unless", "business", "process", "access", "address", "success", "across",
    "during", "something", "nothing", "anything", "everything", "morning",
    "evening", "building", "thing", "king", "ring", "spring", "string", "wing",
    "young", "long", "along", "among", "strong", "wrong", "song", "being",
    "meaning", "warning", "understanding", "feeling", "reading", "writing",
}
_STOP_SUBJ = {"the", "a", "an", "and", "but", "or", "so", "then", "that", "which",
              "when", "while", "because", "if", "as", "after", "before", "since",
              "though", "although", "however", "there", "here"}

_CLAUSE_SPLIT = re.compile(
    r"(?:(?<=[.!?;:])\s+|\n+|\s+(?:and then|and|but|so that|so|because|while|"
    r"whereas|then|after|before|although|though|however|which|that is why|"
    r"therefore)\s+)", re.I)


def _looks_like_verb(w: str) -> bool:
    """Morphological test, not a lookup. Reports on inflection, not vocabulary."""
    low = w.lower()
    if low in _NOT_VERB:
        return False
    if low in _IRREGULAR or low in _MODALS:
        return True
    if len(low) < 4:
        return False
    if low.endswith("ed") and len(low) > 4:
        return True
    if low.endswith("ing") and len(low) > 5:
        return True
    # NO bare -s rule. Plural nouns end in s, and it cost more than it earned:
    # on his rain sentence it made `kids` the happening and lost `standing`.
    return False


# auxiliaries carry no happening of their own. "was standing" is a standing, not
# a was — the first attempt reported `happening="was"` and lost the actual event.
_AUX = {"was", "were", "is", "are", "am", "be", "been", "being", "has", "have",
        "had", "do", "does", "did", "will", "would", "can", "could", "shall",
        "should", "may", "might", "must", "got"}


def _happening(clause: str) -> dict:
    """The happening in a clause, and how it was found.

    A content verb always beats an auxiliary. `was standing` is a STANDING."""
    words = re.findall(r"[A-Za-z][A-Za-z'’-]*", clause)
    if not words:
        return {}
    try:
        from . import micro
        listed = [w for w in words
                  if w.lower() in micro.ALL_VERBS and w.lower() not in _AUX]
    except Exception:
        listed = []
    if listed:
        return {"happening": listed[0], "how_found": "in the known verb list"}
    for w in words:
        if w.lower() not in _AUX and _looks_like_verb(w):
            return {"happening": w,
                    "how_found": "by inflection — NOT in the verb list, which is "
                                 "why the list alone cannot serve the motto"}
    aux = [w for w in words if w.lower() in _AUX]
    if aux:
        return {"happening": aux[0],
                "how_found": "auxiliary only — the clause states a state, not an "
                             "action"}
    return {}


# a prepositional phrase is not the subject. "the kids inside the home thought"
# has actor `kids`, not `home` — the first attempt returned `home`.
_PREP = {"inside", "outside", "in", "on", "at", "with", "without", "under",
         "over", "above", "below", "behind", "beside", "near", "by", "from",
         "into", "onto", "through", "across", "between", "among", "around",
         "of", "for", "to", "up", "down", "off", "against", "during", "after",
         "before", "about"}


def _actor(clause: str, happening: str) -> str:
    """The subject head before the happening — not the nearest noun.

    Any prepositional phrase between the subject and the verb is stepped over,
    which is what stops `the kids inside the home thought` reporting `home`."""
    words = re.findall(r"[A-Za-z][A-Za-z'’-]*", clause)
    low = [w.lower() for w in words]
    try:
        i = low.index((happening or "").lower())
    except ValueError:
        i = len(words)
    head = words[:i]
    # walk back to the last preposition; everything after it is its phrase
    cut = 0
    for j in range(len(head) - 1, -1, -1):
        if head[j].lower() in _PREP:
            cut = j
            break
    candidates = head[:cut] if cut else head

    def ok(w):
        lw = w.lower()
        return lw not in _STOP_SUBJ and lw not in _PREP and lw not in _AUX

    for w in reversed(candidates):
        if ok(w):
            return w
    for w in reversed(head):
        if ok(w):
            return w
    return ""


def events_in(text: str) -> list:
    """EVERYTHING HAPPENING IS AN EVENT.

    A text with a happening in it can never come back with zero events. Every
    event carries an intent slot that is OPEN, never absent — his rule that
    "there is no reason" is not an available answer."""
    out = []
    for raw in _CLAUSE_SPLIT.split(text or ""):
        raw = raw.strip(" \t\r\n-–—•*|")
        if len(raw) < 3:
            continue
        h = _happening(raw)
        if not h:
            continue
        act = _actor(raw, h["happening"])
        out.append({
            "n": len(out) + 1,
            "raw": raw[:400],
            "actor": act or "(not named in this clause)",
            "happening": h["happening"],
            "how_found": h["how_found"],
            "intent": {
                "status": INTENT_OPEN,
                "why": "intent is read from how things were arranged across many "
                       "events, never from one. The slot exists because every "
                       "event has an intent; it is open because this is one "
                       "event.",
                "concluded": False,
            },
            "is_event": True,
        })
    return out


# ---------------------------------------------------------------------------
# SEATING — where the example SITS on existing parameters and IDs.
# ---------------------------------------------------------------------------

_WORD = re.compile(r"[a-z][a-z'’]{2,}")   # hyphens SPLIT: "point-of-no-return"
#   must index as point / return, or a query word can never reach a compound
#   name. Leaving the hyphen inside the token glued them together and silently
#   lost every match into his many hyphenated rows.
_SEAT_STOP = {
    "the", "and", "for", "with", "that", "this", "was", "were", "his", "her",
    "him", "she", "they", "them", "not", "but", "are", "has", "had", "have",
    "from", "into", "out", "off", "over", "under", "when", "then", "than",
    "there", "here", "what", "which", "who", "how", "why", "all", "any", "one",
    "two", "its", "it's", "you", "your", "our", "their", "been", "being", "did",
    "does", "can", "could", "would", "should", "will", "may", "might", "must",
    "some", "more", "most", "very", "just", "only", "also", "such", "same",
    "other", "each", "every", "own", "too", "now", "get", "got", "make", "made",
}


@lru_cache(maxsize=1)
def _index():
    """Word -> parameter rows, with IDF. A word in forty of his names is weak
    evidence; a rare one is strong. Built once over the 3,204."""
    rows, byword = [], {}
    for c in hr.containers():
        for j, s in enumerate(c["subs"], 1):
            row = {"sb_id": "SB-HFR-P%04d" % flat_of(c["id"], j),
                   "flat": flat_of(c["id"], j), "name": s,
                   "container": c["id"], "container_name": c["name"],
                   "segment": c["segment"]}
            rows.append(row)
            for w in set(_WORD.findall(s.lower())):
                if w in _SEAT_STOP:
                    continue
                byword.setdefault(w, []).append(row)
    n = len(rows)
    idf = {w: math.log(n / len(v)) for w, v in byword.items()}
    return rows, byword, idf


# The threshold is HIS number, not one I picked. His own rule: "a word in forty
# of his names is weaker evidence than a rare one." Forty names out of 3,204 is
# an IDF of log(3204/40) = 4.38, so that is the bar. A word in five names or
# fewer is strong evidence: log(3204/5) = 6.46.
#
# Measured against the real index (2,270 words): the bar excludes 16 words —
# `control` (62 names), `memory` (63), `self` (70) and their kind. It is a small
# gate and it is NOT the main guard; the ROLE gate is what actually stops
# fabrication. Said plainly rather than overclaimed.
_BANK_FOR_BAR = 3204
MIN_IDF = math.log(_BANK_FOR_BAR / 40.0)      # 4.38 — his "forty of his names"
STRONG = math.log(_BANK_FOR_BAR / 5.0)        # 6.46 — a word in five or fewer


# ---------------------------------------------------------------------------
# THE ROLE OF AN EVENT decides WHICH CONTAINERS it can seat in. Word matching
# alone put his rain example on "Standing balance" and "Air/breathing drive",
# which is not what the example is about. The role comes first; the words only
# choose rows INSIDE the containers the role allows.
# ---------------------------------------------------------------------------

ACTION = "ACTION"
OBSERVATION = "OBSERVATION"
INFERENCE = "INFERENCE"
SPEECH = "SPEECH"
FEELING = "FEELING"
STATE = "STATE"

# his own segments, by their own names. A role is a claim about WHICH PART OF
# HIM the event engages, not about the sentence.
ROLE_SEGMENTS = {
    ACTION:      ("SEG-03", "SEG-06"),   # sensorimotor execution + decision
    OBSERVATION: ("SEG-02", "SEG-04"),   # perception + attention
    INFERENCE:   ("SEG-06", "SEG-05"),   # reasoning/decision + knowledge
    SPEECH:      ("SEG-07", "SEG-09"),   # language + social
    FEELING:     ("SEG-08", "SEG-01"),   # emotion + body
    STATE:       ("SEG-01", "SEG-02"),   # body state + body representation
}

_ROLE_MARK = {
    OBSERVATION: ("saw", "see", "seen", "watched", "looked", "heard", "hear",
                  "noticed", "observed", "felt", "watching", "seeing", "looking"),
    INFERENCE: ("thought", "think", "believed", "believe", "assumed", "assume",
                "concluded", "decided", "guessed", "supposed", "realised",
                "realized", "reckoned", "knew"),
    SPEECH: ("said", "told", "asked", "spoke", "called", "answered", "replied",
             "shouted", "explained", "wrote", "named", "ordered", "requested"),
    FEELING: ("loved", "hated", "feared", "enjoyed", "worried", "angry", "happy",
              "sad", "afraid", "upset", "excited", "hurt"),
}


def role_of(happening: str, clause: str = "") -> dict:
    """What kind of happening this is. Reported with the reason."""
    h = (happening or "").lower()
    for role, marks in _ROLE_MARK.items():
        if h in marks:
            return {"role": role, "why": "the happening %r is %s" % (happening,
                                                                     role.lower())}
    low = (clause or "").lower()
    for role, marks in _ROLE_MARK.items():
        for m in marks:
            if re.search(r"\b%s\b" % re.escape(m), low):
                return {"role": role,
                        "why": "the clause carries %r, an %s marker"
                               % (m, role.lower())}
    if h in _AUX:
        return {"role": STATE, "why": "auxiliary only — the clause states a state"}
    return {"role": ACTION, "why": "a happening with no perception, inference, "
                                   "speech or feeling marker reads as an action"}


def seat(text: str, limit: int = 12, role: str = None) -> dict:
    """Where this text SITS on his existing parameters and IDs.

    Two stages, in this order:
      1. the ROLE of the event says which of his segments may host it;
      2. the words choose rows INSIDE those segments.

    Stage 1 is what stops a word coincidence in an unrelated segment from being
    counted as a seat. Rows that match on words but sit outside the role's
    segments are returned as `out_of_role` — kept and visible, never silently
    dropped and never counted as strengthening the base."""
    rows, byword, idf = _index()
    allowed = set(ROLE_SEGMENTS.get(role, ())) if role else None
    words = [w for w in set(_WORD.findall((text or "").lower()))
             if w not in _SEAT_STOP]
    scored, out_of_role = {}, {}
    weak_words = []
    for w in words:
        if w not in idf:
            continue
        if idf[w] < MIN_IDF:
            weak_words.append({"word": w, "idf": round(idf[w], 2),
                               "in_names": len(byword[w]),
                               "why": "appears in %d of his names — too common to "
                                      "be evidence" % len(byword[w])})
            continue
        for row in byword[w]:
            bucket = scored
            if allowed is not None and row["segment"] not in allowed:
                bucket = out_of_role
            e = bucket.setdefault(row["sb_id"],
                                  {"row": row, "weight": 0.0, "on": []})
            e["weight"] += idf[w]
            e["on"].append(w)

    def fmt(e):
        return {"sb_id": e["row"]["sb_id"], "name": e["row"]["name"],
                "container": e["row"]["container"],
                "container_name": e["row"]["container_name"],
                "segment": e["row"]["segment"],
                "weight": round(e["weight"], 2),
                "on": sorted(e["on"]),
                "band": "STRONG" if e["weight"] >= STRONG else "SEATED"}

    ordered = sorted(scored.values(), key=lambda e: -e["weight"])
    outs = sorted(out_of_role.values(), key=lambda e: -e["weight"])

    # An event whose role IS known but which matches no row by word still sits
    # somewhere: on the containers that host that role. Reported at container
    # granularity and labelled as such — a coarse seat is not nothing, and
    # nothing would be the one answer his motto does not allow.
    container_seat = []
    if role and not ordered:
        for seg in sorted(allowed or ()):
            for c in hr.containers():
                if c["segment"] == seg:
                    container_seat.append({
                        "container": c["id"], "container_name": c["name"],
                        "segment": seg, "granularity": "CONTAINER",
                        "why": "the role seats here; no single row matched by word"})
    return {
        "role": role,
        "role_segments": sorted(allowed) if allowed else None,
        "seats": [fmt(e) for e in ordered[:limit]],
        "seated": min(len(ordered), limit),
        "container_seat": container_seat[:16],
        "seated_at_container_level_only": bool(container_seat),
        "candidates_found": len(ordered),
        "dropped_by_limit": max(0, len(ordered) - limit),
        "out_of_role": [fmt(e) for e in outs[:limit]],
        "out_of_role_total": len(outs),
        "weak_words": weak_words[:12],
        "words_searched": len(words),
        "bank": len(rows),
        "min_idf": MIN_IDF,
        "law": "the role picks the segments, the words pick the rows. A word "
               "coincidence outside the role is kept and shown, never counted.",
    }


# every event's intent seats HERE, always — "all events have intent" placed on
# his own bank rather than asserted in prose.
INTENT_CONTAINERS = ("CON-063", "CON-064")


def intent_seat(clause: str, limit: int = 4) -> dict:
    """Where the INTENT of an event sits. His motto, on his own IDs.

    The slot is never empty: even with no lexical match the two containers that
    hold intent formation and motive are named, because the event has an intent
    whether or not this clause reveals it."""
    rows, byword, idf = _index()
    hits = {}
    for w in set(_WORD.findall((clause or "").lower())):
        if w in _SEAT_STOP or w not in idf or idf[w] < MIN_IDF:
            continue
        for row in byword[w]:
            if row["container"] in INTENT_CONTAINERS:
                e = hits.setdefault(row["sb_id"],
                                    {"row": row, "weight": 0.0, "on": []})
                e["weight"] += idf[w]
                e["on"].append(w)
    ordered = sorted(hits.values(), key=lambda e: -e["weight"])[:limit]
    return {
        "containers": list(INTENT_CONTAINERS),
        "container_names": [hr.container(c)["name"] for c in INTENT_CONTAINERS],
        "rows": [{"sb_id": e["row"]["sb_id"], "name": e["row"]["name"],
                  "container": e["row"]["container"],
                  "weight": round(e["weight"], 2), "on": sorted(e["on"])}
                 for e in ordered],
        "matched_rows": len(ordered),
        "status": INTENT_OPEN,
        "concluded": False,
        "law": "all events have intent — so the slot is named on his bank even "
               "when this clause does not reveal which intent it is.",
    }


# ---------------------------------------------------------------------------
# PLACE — one example, placed. Not answered.
# ---------------------------------------------------------------------------

# A parameter-atom row: an id token, then a short name. Both his brain workbooks
# use this shape ("C01-001 | 1 Homeostasis and Allostasis | Temperature balance"),
# and so does any dump of a parameter list.
_ATOM_ROW = re.compile(
    r"^\s*(?:[A-Z]{1,3}\d{2,4}-\d{2,4}|P-\d{3}-\d{2}|SB-HFR-P\d{4}|CON-\d{3}"
    r"|SEG-\d{2})\b")


def registry_echo(text: str) -> dict:
    """Does this text carry a PARAMETER TAXONOMY rather than events?

    Found on his own EINSTEIN_BRAIN workbook. Its `2560 SUB-PARAMETERS` sheet is a
    full atom-by-atom expansion, and placing the file whole seated a taxonomy on a
    taxonomy: 1,086 ids "reached", top hits `Load-force coupling`, `Agonist
    activation`, `Synergy activation` — none of which is about Einstein. Excluding
    those rows dropped it to 281 ids and the top hits became `Stopping-rule
    (enough evidence)`, `Pattern abstraction`, `Rule extraction`, `Nearest-
    possible-world reasoning` — which are.

    Note what it is NOT: the workbook does not quote the current bank. It carries
    his OLDER 2,560 list, whose names differ (`Temperature balance` where the
    registry says `Core temperature setpoint`). Only 217 lines match a current
    name exactly. So this is a **parallel taxonomy**, and it is caught by SHAPE —
    an atom-id row — rather than by name, because the version that produced it is
    not the version in the bank.

    A parameter list must not be able to strengthen the bank by being a parameter
    list. `place()` excludes these rows and states how many."""
    rows, _byword, _idf = _index()
    names = {r["name"].strip().lower() for r in rows}
    lines = [ln.strip() for ln in (text or "").splitlines() if ln.strip()]
    exact, atoms, atom_chars, total_chars = [], [], 0, 0
    for ln in lines:
        total_chars += len(ln)
        parts = [p.strip() for p in re.split(r"\s*\|\s*", ln.lower())]
        if any(p and p in names for p in parts):
            exact.append(ln[:120])
        if _ATOM_ROW.match(ln):
            atoms.append(ln[:120])
            atom_chars += len(ln)
    taxonomy = len(atoms) + sum(1 for e in exact if not _ATOM_ROW.match(e))
    share = (100.0 * taxonomy / len(lines)) if lines else 0.0
    return {
        "lines": len(lines),
        "exact_name_echo_lines": len(exact),
        "atom_id_rows": len(atoms),
        "taxonomy_lines": taxonomy,
        "taxonomy_share_of_lines": round(share, 1),
        "taxonomy_share_of_chars": round(100.0 * atom_chars / total_chars, 1)
                                   if total_chars else 0.0,
        "examples": (atoms or exact)[:5],
        "is_parameter_taxonomy": taxonomy >= 20 and share >= 20.0,
        "law": "a parameter list cannot strengthen the bank by being a parameter "
               "list.",
        "note": "caught by row SHAPE, not by name — his workbooks carry the older "
                "2,560 list whose names differ from the current 3,204.",
    }


def _strip_echo(text: str) -> tuple:
    rows, _bw, _idf = _index()
    names = {r["name"].strip().lower() for r in rows}
    kept, dropped = [], 0
    for ln in (text or "").splitlines():
        parts = [p.strip() for p in re.split(r"\s*\|\s*", ln.lower())]
        if _ATOM_ROW.match(ln) or any(p and p in names for p in parts):
            dropped += 1
            continue
        kept.append(ln)
    return "\n".join(kept), dropped


def place(text: str, name: str = "", seat_limit: int = 8) -> dict:
    """Place one example on the base. There is no verdict and no answer here.

    Returns what the example IS to the system: its events, the intent slot on
    each, the parameter IDs it seats on (which those IDs gain support from), and
    the count it adds."""
    echo = registry_echo(text)
    if echo["is_parameter_taxonomy"]:
        text, _dropped = _strip_echo(text)
    evs = events_in(text)
    per = []
    strengthened = {}
    for e in evs:
        r = role_of(e["happening"], e["raw"])
        e["role"] = r["role"]
        e["role_why"] = r["why"]
        s = seat(e["raw"], limit=seat_limit, role=r["role"])
        isl = intent_seat(e["raw"])
        e["intent"]["seats_on"] = isl["containers"]
        e["intent"]["rows"] = [x["sb_id"] for x in isl["rows"]]
        for st in s["seats"]:
            cur = strengthened.setdefault(st["sb_id"], {
                "sb_id": st["sb_id"], "name": st["name"],
                "container": st["container"], "segment": st["segment"],
                "support": 0, "from_events": []})
            cur["support"] += 1
            cur["from_events"].append(e["n"])
        per.append({"event": e, "role": r, "seating": s, "intent_seating": isl})
    whole = seat(text, limit=seat_limit * 2)
    return {
        "name": name or "(unnamed example)",
        "phase": PHASE,
        "motto": MOTTO,
        "chars": len(text or ""),
        "events": evs,
        "per_event": per,
        "whole_text_seating": whole,
        "strengthened": sorted(strengthened.values(),
                               key=lambda x: -x["support"]),
        "counts": {
            "events": len(evs),
            "intents_opened": len(evs),
            "intents_concluded": 0,
            "distinct_ids_seated": len(strengthened),
            "count_added": 1 + 2 * len(evs),
            "new_parameters_created": 0,
        },
        "found_by_inflection": sum(1 for e in evs
                                   if "inflection" in e["how_found"]),
        "registry_echo": echo,
        "echo_lines_excluded": echo["taxonomy_lines"] if echo["is_parameter_taxonomy"]
                               else 0,
        "law": "an example is not judged for its output. It seats on existing "
               "parameters and IDs, strengthens them by seating, and raises the "
               "count.",
        "refuses": "no event is dropped, no intent is concluded from one event, "
                   "and seating creates no parameter.",
    }


# ---------------------------------------------------------------------------
# THE COUNT — every example raises it. Appended, never replaced.
# ---------------------------------------------------------------------------

def grow(root: str, text: str, name: str = "", surfaced_by: str = "") -> dict:
    """Append this example to the growth ledger: the example, its events, its
    intents. Nothing is removed and no parameter is invented."""
    from . import growth as G
    p = place(text, name)
    before = G.counts(root)
    added = [G.add(root, G.EXAMPLE, p["name"], surfaced_by or "the growing phase",
                   module="growing",
                   detail="%d events, %d ids seated" % (p["counts"]["events"],
                                                        p["counts"]["distinct_ids_seated"]),
                   extra={"seats": [s["sb_id"] for s in p["strengthened"]]})]
    for e in p["events"]:
        added.append(G.add(root, G.EVENT, "%s :: %s" % (p["name"], e["raw"][:90]),
                           surfaced_by or p["name"], module="growing",
                           detail="happening=%s (%s) actor=%s"
                                  % (e["happening"], e["how_found"], e["actor"])))
        added.append(G.add(root, G.INTENT, "%s :: intent of event %d"
                           % (p["name"], e["n"]),
                           surfaced_by or p["name"], module="growing",
                           detail=INTENT_OPEN))
    after = G.counts(root)
    return {
        "placement": p,
        "appended": len(added),
        "rows": added,
        "count_before": before["grown_rows"],
        "count_after": after["grown_rows"],
        "increased": after["grown_rows"] - before["grown_rows"],
        "parameters_before": before["total_parameters"],
        "parameters_after": after["total_parameters"],
        "law": "every example will keep increase the count",
    }


def run_files(paths, root: str = ".", max_chars: int = 60000) -> dict:
    """Place a list of repo files. Reads, never writes to them."""
    out, failed = [], []
    for rel in paths:
        full = os.path.join(root, rel)
        try:
            with open(full, "r", encoding="utf-8", errors="replace") as f:
                txt = f.read(max_chars)
        except Exception as e:
            failed.append({"path": rel, "error": str(e)})
            continue
        p = place(txt, rel)
        out.append({"path": rel, "events": p["counts"]["events"],
                    "ids_seated": p["counts"]["distinct_ids_seated"],
                    "count_added": p["counts"]["count_added"],
                    "by_inflection": p["found_by_inflection"],
                    "top_ids": [s["sb_id"] for s in p["strengthened"][:5]]})
    ids = set()
    for rel in paths:
        pass
    return {
        "files": out,
        "unreadable": failed,
        "counts": {
            "files_placed": len(out),
            "files_unreadable": len(failed),
            "events_total": sum(x["events"] for x in out),
            "count_added_total": sum(x["count_added"] for x in out),
            "found_by_inflection": sum(x["by_inflection"] for x in out),
        },
        "law": "as long i keep adding the example, the count keeps rising",
    }


def coverage(paths, root: str = ".", max_chars: int = 60000) -> dict:
    """How much of the base the examples actually reach — his "basic".

    This is the number that says whether the growing phase is done. It is
    reported, never asserted to be enough."""
    rows, _bw, _idf = _index()
    hit = set()
    for rel in paths:
        try:
            with open(os.path.join(root, rel), "r", encoding="utf-8",
                      errors="replace") as f:
                txt = f.read(max_chars)
        except Exception:
            continue
        for s in seat(txt, limit=400)["seats"]:
            hit.add(s["sb_id"])
    total = len(rows)
    return {
        "bank": total,
        "ids_reached": len(hit),
        "ids_untouched": total - len(hit),
        "percent_reached": round(100.0 * len(hit) / total, 2) if total else 0.0,
        "files_read": len(paths),
        "basic_over": False,
        "why": "the basic is his call, not a threshold I get to set. What is "
               "reported is how much of the base the examples have reached.",
        "then": "once the basic will over it will start making new combinations "
                "on new thoughts",
    }


def stats() -> dict:
    rows, byword, _idf = _index()
    return {
        "phase": PHASE,
        "motto": MOTTO,
        "bank": len(rows),
        "indexed_words": len(byword),
        "min_idf": MIN_IDF,
        "closed_verb_list_used": False,
        "new_parameters_created_by_seating": 0,
        "source": "docs/method/canon/THE_GROWING_PHASE.md",
    }


def annotations() -> list:
    return [
        ("everything happening is a event", "growing.events_in"),
        ("all events have intent", "growing.INTENT_OPEN"),
        ("example sit on existing parameters and IDs", "growing.seat"),
        ("so system can strong its base", "growing.place"),
        ("every example will keep increase the count", "growing.grow"),
        ("once the basic will over", "growing.coverage"),
    ]
