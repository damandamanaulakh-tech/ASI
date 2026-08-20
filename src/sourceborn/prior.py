"""PHASE B, PART ONE — THE TWO STEPS THAT WERE ABSENT.

His 18-step runtime, checked against the running code, resolved sixteen. Two did
not:

        2  DECLARE END / WHY THIS MATTERS      ABSENT
        3  REVERSE TO PRIOR REALITY            ABSENT

They are the two that run BACKWARDS, and they both sit BEFORE decomposition.
That ordering is the correction, and it is his:

    R-F-R at step 13 is the SECOND place reverse happens. Steps 2 and 3 are
    the FIRST. Declare the end, go back to what was true before the event, and
    only THEN decompose.

Everything this core did until now ran forward from the text and reversed only
at the check. That is why these two were missing rather than merely thin — there
was no reverse pass at intake for them to live in.

WHERE THE METHOD COMES FROM — HIS OWN DOC, NOT MINE

`docs/mainwork/THE_REVERSE_WALKS.md` already states the rule, in his frame:

    "A reverse walk starts at the thing as it stands today, finished and named,
     and descends: what must have been true *immediately* before this, without
     which this could not stand?"

    THE REMOVAL TEST. "Take the step away. Does the step above it still stand?
     If it still stands, it was never a dependency — it was a neighbour, and it
     is dropped."

    "Where the walk stops: at something nobody made. That is GROUND. A walk
     that stops at something a human built has not reached ground yet."

So step 3 is the removal test made executable, and step 2 is the "finished and
named" thing the descent starts from.

THE THREE GRADES, AND WHY THE THIRD CANNOT ARRIVE BY ITSELF

A prior condition is one of three things, and they are never merged:

    STATED     the source says so.
    ENTAILED   the event's own grammar requires it. An actor that did not exist
               cannot act. Derivable without any knowledge of the world.
    ASSUMED    I put it there. [SYNTHETIC], with proof debt and an expiry.

`prior_reality()` produces STATED and ENTAILED only. ASSUMED can enter one way —
an explicit call to `assume()` that stamps it — so the machine can never quietly
manufacture a past for him. A test runs the whole pipeline and asserts zero
ASSUMED rows.

WHAT THIS MODULE REFUSES

  * it never blends two surviving ends. Two candidates HALT — his rule.
  * it never returns "there is no end". An unnamed end is UNNAMED, and it says
    what would name it.
  * it never deletes a dropped prior. A condition that fails the removal test is
    kept as a NEIGHBOUR with the reason it was dropped.
  * it never claims ground it did not reach.
"""

from __future__ import annotations

import re

STEP_2 = "DECLARE END / WHY THIS MATTERS"
STEP_3 = "REVERSE TO PRIOR REALITY"
REVERSE = "REVERSE"

# ---------------------------------------------------------------------------
# STEP 2 — THE END.
#
# A PULL names a target AHEAD of the event. A PUSH names a reason BEHIND it.
# Both are evidence about why the event happened; only the first is an END.
# They are graded apart because his own method separates the two — intent is
# what pushes, the target is what the sequence was built toward — and collapsing
# them would let "because he was tired" be read as a goal.
# ---------------------------------------------------------------------------

PULL_PHRASE = re.compile(
    r"\b(so that|so as to|in order to|in order that|in order for)\b", re.I)

PULL_VERB = re.compile(
    r"\b(wanted|wants|want|trying|tries|try|hoping|hopes|hope|meant|"
    r"intended|intends|intend|aimed|aims|aim|planned|plans|plan|"
    r"needed|needs|need|decided|decides|decide|chose|chooses|choose|"
    r"set out|looking)\s+to\s+", re.I)

PUSH_PHRASE = re.compile(
    r"\b(because|since|as a result of|due to|owing to|on account of)\b", re.I)

# "to <verb>" — the infinitive of purpose. Only counted when the following word
# actually looks like a verb, so "to the mall" is not read as a target.
INFINITIVE = re.compile(r"\bto\s+([a-z][a-z'’]{1,})\b", re.I)

# "for <noun>" — a purpose phrase. Weakest of the pull markers and graded so.
FOR_PHRASE = re.compile(
    r"\bfor\s+(?:the\s+|a\s+|an\s+|his\s+|her\s+|their\s+|my\s+|our\s+|"
    r"its\s+)?([a-z][a-z'’]{2,})", re.I)

_CLAUSE_END = re.compile(r"[.;!?\n]|,\s+(?:and|but|so|then|because)\b")

PULL = "PULL — a target ahead"
PUSH = "PUSH — a reason behind, not a target ahead"
HIS = "HIS ASSIGNMENT"

_FOR_STOP = {"now", "this", "that", "him", "her", "them", "you", "me", "us",
             "it", "example", "instance", "sure", "long", "once", "days",
             "years", "hours", "the", "which", "what", "some", "any"}


def _tail(text: str, at: int) -> str:
    """From a marker to the end of its clause. The end is what the marker points
    at, not the whole sentence."""
    rest = text[at:]
    m = _CLAUSE_END.search(rest)
    return (rest[:m.start()] if m else rest).strip(" \t\r\n,-–—")


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower()).strip(" .,;:")


def _looks_like_verb(word: str) -> bool:
    from . import growing as G
    return G._looks_like_verb(word)


def end_candidates(text: str) -> list:
    """Every end the SOURCE names. Nothing is invented and nothing is chosen."""
    found = []

    def take(kind, marker, at, grade, why):
        body = _tail(text, at)
        if len(_norm(body)) < 3:
            return
        found.append({"end": body[:220], "marker": marker, "kind": kind,
                      "grade": grade, "at": at, "why": why})

    for m in PULL_PHRASE.finditer(text or ""):
        take(PULL, m.group(0), m.end(), "STATED TARGET",
             "the source names what it was for, in the words that name targets")
    for m in PULL_VERB.finditer(text or ""):
        take(PULL, m.group(0).strip(), m.end(), "STATED TARGET",
             "a wanting verb followed by 'to' names what was being reached for")
    for m in INFINITIVE.finditer(text or ""):
        if not _looks_like_verb(m.group(1)):
            continue
        # already covered by a wanting verb immediately before it
        if PULL_VERB.search(text[max(0, m.start() - 24):m.end()]):
            continue
        take(PULL, "to " + m.group(1), m.start(), "INFINITIVE OF PURPOSE",
             "'to <verb>' points forward. Weaker than a stated target, because "
             "it can also be plain complement, so it is graded lower")
    for m in FOR_PHRASE.finditer(text or ""):
        if m.group(1).lower() in _FOR_STOP:
            continue
        take(PULL, "for " + m.group(1), m.start(), "PURPOSE PHRASE",
             "'for <thing>' names something the act was aimed at")
    for m in PUSH_PHRASE.finditer(text or ""):
        take(PUSH, m.group(0), m.end(), "STATED REASON",
             "this names the reason BEHIND the event. It is evidence about "
             "why, and it is NOT a target ahead. Kept apart on purpose")

    out, seen = [], set()
    for c in sorted(found, key=lambda c: c["at"]):
        k = _norm(c["end"])
        if k in seen:
            continue
        seen.add(k)
        c["id"] = "END-%02d" % (len(out) + 1)
        out.append(c)
    return out


_GRADE_ORDER = {"STATED TARGET": 0, "INFINITIVE OF PURPOSE": 1,
                "PURPOSE PHRASE": 2, "STATED REASON": 3}


def declare_end(text: str, his_end: str = "") -> dict:
    """STEP 2 — declare the end this event was working toward, and say what
    turns on it.

    His word outranks the parse. When he names the end, it is taken, labelled
    HIS ASSIGNMENT, and the parsed candidates are kept beside it so he can see
    what the machine would have said."""
    cands = end_candidates(text or "")
    pulls = [c for c in cands if c["kind"] == PULL]
    pushes = [c for c in cands if c["kind"] == PUSH]

    named, end, grade, halt, chosen = False, None, None, False, []
    if (his_end or "").strip():
        named, end, grade = True, his_end.strip(), HIS
        chosen = [{"end": end, "grade": HIS, "kind": PULL,
                   "why": "he named it. His word outranks the parse."}]
    elif pulls:
        best = min(_GRADE_ORDER[c["grade"]] for c in pulls)
        chosen = [c for c in pulls if _GRADE_ORDER[c["grade"]] == best]
        if len(chosen) == 1:
            named, end, grade = True, chosen[0]["end"], chosen[0]["grade"]
        else:
            halt = True
    elif pushes:
        # A reason behind is not a target ahead. It does not name the end; it
        # is the closest thing the source gives, and it is reported as that.
        chosen = pushes

    # separators exist only between competing PULL ends. Two PUSH reasons do
    # not compete — "because X and because Y" can both be true — so producing
    # separators between them would manufacture a contest the source never had.
    separates = []
    if halt:
        for a in range(len(chosen)):
            for b in range(a + 1, len(chosen)):
                separates.append({
                    "between": [chosen[a]["id"], chosen[b]["id"]],
                    "would_separate":
                        "evidence that the actor arranged things for %r and not "
                        "for %r — a preparation, a cost paid, or an order given "
                        "that only one of the two needs"
                        % (_norm(chosen[a]["end"]), _norm(chosen[b]["end"])),
                })

    return {
        "step": 2, "name": STEP_2, "direction": REVERSE,
        "point_zero": text or "",
        "named": named, "end": end, "grade": grade,
        "candidates": cands,
        "pull_candidates": len(pulls), "push_candidates": len(pushes),
        "chosen": chosen,
        "halt": halt,
        "halt_why": ("two ends survive at the same grade. They are NOT blended "
                     "and neither is preferred — this goes to him" if halt
                     else None),
        "separates_them": separates,
        "why_this_matters": why_this_matters(named, end),
        "what_would_name_it": ([] if named else [
            "the source stating a target — 'so that', 'in order to', a wanting "
            "verb followed by 'to'",
            "him naming it (pass his_end=...); his word outranks the parse",
            "a later event in the same sequence revealing what was being "
            "reached for",
        ]),
        "law": "'there is no reason' is not an available answer. The end slot "
               "always exists; when the source does not name it, it is UNNAMED "
               "and open, never absent and never filled in.",
        "refuses": "two surviving ends are never blended, and a reason behind "
                   "is never promoted to a target ahead.",
        "reverse_pass": "this is the FIRST of two reverse passes. The second is "
                        "step 13, R-F-R.",
    }


def why_this_matters(named: bool, end) -> dict:
    """Not a sentiment — the list of steps that read differently if the end
    moves. Each one is a step that consumes the end downstream."""
    return {
        "consumed_by": [
            {"step": 3, "name": STEP_3,
             "reads": "the descent starts at the end. A wrong end makes every "
                      "prior condition below it a descent from the wrong top."},
            {"step": 11, "name": "Future-State Reconstruction",
             "reads": "the end IS the future state being reconstructed; the "
                      "candidates are filtered by what the end requires."},
            {"step": 12, "name": "Evidence Prediction",
             "reads": "what should exist if this were true is predicted FROM "
                      "the end. Change the end and the predictions change."},
            {"step": 18, "name": "Next-Sequence Seed",
             "reads": "an end that was not reached is a reason to come back. "
                      "No end, no seed."},
        ],
        "at_stake": ("four of the eighteen steps read off it, and three of them "
                     "come after decomposition — so an end declared wrong is not "
                     "caught later, it is inherited later."),
        "named": named,
        "if_unnamed": ("the four steps above still run; they run on an OPEN end "
                       "and say so. They do not run on a guessed one."),
    }


# ---------------------------------------------------------------------------
# STEP 3 — THE DESCENT.
# ---------------------------------------------------------------------------

STATED = "STATED"
ENTAILED = "ENTAILED"
ASSUMED = "ASSUMED"
GRADES = (STATED, ENTAILED, ASSUMED)

GRADE_MEANS = {
    STATED: "the source says so. It is in his words, not mine.",
    ENTAILED: "the event's own grammar requires it. An actor that did not exist "
              "cannot act. No knowledge of the world is used.",
    ASSUMED: "I put it there. [SYNTHETIC] — it carries proof debt and an expiry, "
             "and it can only enter by an explicit call.",
}

BEFORE_MARK = re.compile(
    r"\b(before|already|earlier|previously|beforehand|prior to|until then|"
    r"by then|back then|used to|in the past|"
    r"(?:few |a few |some |several |many |two |three )?(?:days?|weeks?|months?|"
    r"years?|hours?)\s+(?:back|ago|earlier)|"
    r"had\s+(?:been|already|[a-z]+ed)|first\b)", re.I)

NEGATION_MARK = re.compile(r"\b(not|never|no|n't|nothing|nobody|without)\b", re.I)
REPEAT_MARK = re.compile(r"\b(again|always|every time|each time|keeps|keep|"
                         r"repeatedly|once more|still)\b", re.I)

_PREP = {"inside", "outside", "in", "on", "at", "with", "without", "under",
         "over", "into", "onto", "from", "to", "by", "for", "about", "above",
         "below", "near", "through", "across", "around", "of"}

_SKIP = {"the", "a", "an", "and", "but", "or", "so", "then", "that", "which",
         "this", "these", "those", "there", "here", "it", "its", "his", "her",
         "their", "my", "our", "your", "him", "them", "us", "me", "he", "she",
         "they", "we", "you", "i", "was", "were", "is", "are", "am", "be",
         "been", "being", "has", "have", "had", "do", "did", "does", "very",
         "just", "also", "too", "not", "no", "as", "if", "when", "while",
         "what", "who", "how", "why", "all", "any", "some", "up", "out", "off"}

_WORD = re.compile(r"[a-z][a-z'’]{2,}")


def _content(s: str) -> set:
    return {w for w in _WORD.findall((s or "").lower()) if w not in _SKIP}


# Words that follow a verb but are not things it lands on. Without this the
# descent reported "'again' existed and was reachable" on his own mall
# sentence — an adverb turned into an object.
_NOT_OBJECT = {"again", "always", "never", "still", "very", "really", "just",
               "too", "also", "well", "better", "worse", "back", "ago", "now",
               "then", "here", "there", "today", "yesterday", "tomorrow",
               "soon", "later", "once", "twice", "more", "most", "less",
               "enough", "already", "almost", "quite", "rather", "even",
               "only", "away", "together", "apart", "again", "much", "many"}


def _object_of(clause: str, happening: str) -> str:
    """The thing the happening lands on. Taken from the clause after the verb,
    skipping prepositions, determiners and adverbs. Returns "" rather than
    guessing — an object it cannot find is one it does not claim."""
    low = (clause or "").lower()
    hap = (happening or "").lower()
    at = low.find(hap)
    if at < 0:
        return ""
    for w in _WORD.findall(low[at + len(hap):]):
        if w in _PREP or w in _SKIP or w in _NOT_OBJECT:
            continue
        if _looks_like_verb(w):
            continue
        return w
    return ""


def entailments(ev: dict) -> list:
    """What the event's OWN GRAMMAR requires to have been true before it.

    Nothing here consults the world. Every row is derivable from the parse, and
    that is precisely why removing any of them removes the event itself."""
    out = []
    raw = ev.get("raw", "")
    actor = (ev.get("actor") or "").strip()
    hap = (ev.get("happening") or "").strip()

    def row(cond, why):
        out.append({"condition": cond, "grade": ENTAILED, "why": why,
                    "from_event": ev.get("n"), "source": "the parse"})

    if actor and not actor.startswith("("):
        row("%s existed and could act" % actor,
            "the clause names %r as the one acting. An actor that did not exist "
            "cannot act, so the event asserts this whether or not it says it"
            % actor)
    if hap:
        row("the capacity for %r existed" % hap,
            "the event reports %r happening. A capacity that was absent produces "
            "no such event" % hap)
    obj = _object_of(raw, hap)
    if obj:
        row("%r existed and was reachable" % obj,
            "the happening lands on %r. Something unreachable cannot be acted "
            "on" % obj)
    if NEGATION_MARK.search(raw):
        row("the positive of %r was possible" % (hap or "this"),
            "the clause negates something. Negating what was never possible "
            "says nothing, so the negation itself asserts the possibility")
    m = REPEAT_MARK.search(raw)
    if m:
        row("an earlier occurrence of %r existed" % (hap or "this"),
            "%r marks a repetition. A repetition entails a first time"
            % m.group(0))
    return out


def stated_priors(text: str, events: list, top_n: int) -> list:
    """Clauses the SOURCE puts before the top event.

    Two ways in, both from his material and neither from world knowledge: a
    clause carrying a before-marker, and a clause that simply comes earlier in
    the source than the top event."""
    out = []
    for e in events:
        if e["n"] == top_n:
            continue
        m = BEFORE_MARK.search(e["raw"])
        if m:
            out.append({"condition": e["raw"], "grade": STATED,
                        "why": "the source marks it as before: %r" % m.group(0),
                        "marker": m.group(0), "from_event": e["n"],
                        "source": "his words"})
        elif e["n"] < top_n:
            out.append({"condition": e["raw"], "grade": STATED,
                        "why": "it stands earlier in the source than the top "
                               "event. Source order is not proof of time order, "
                               "and it is reported as order, not as time",
                        "marker": None, "from_event": e["n"],
                        "source": "his words",
                        "caution": "SOURCE ORDER, NOT TIME ORDER"})
    return out


_SENT_END = re.compile(r"[.!?\n]")


def _sentence_of(text: str, clause: str) -> int:
    """Which sentence a clause sits in. Used only to FLAG a drop, never to undo
    one."""
    at = (text or "").find((clause or "")[:40])
    if at < 0:
        return -1
    return len(_SENT_END.findall(text[:at]))


def removal_test(row: dict, top: dict) -> dict:
    """HIS TEST, verbatim: take the step away — does the thing above still stand?

    ENTAILED rows break the top by construction. STATED rows break it only if
    the top actually leans on them, and leaning is checked by what they share:
    a prior that shares neither actor nor content with the top was a NEIGHBOUR,
    and a neighbour is dropped from the walk. It is kept in the record."""
    if row["grade"] == ENTAILED:
        return {"breaks": True, "shared": [],
                "verdict": "SURVIVES — removing it removes the event itself",
                "why": "it is entailed by the event's own grammar; there is no "
                       "version of the event with this absent"}
    top_words = _content(top.get("raw", ""))
    actor = (top.get("actor") or "").lower()
    row_words = _content(row.get("condition", ""))
    shared = sorted(top_words & row_words)
    # the actor must match as a WHOLE WORD — a bare substring test let actor
    # "i" match inside nearly every condition ("girlfriend", "raining") and
    # made the removal test toothless on first-person asks. And matching, it
    # is not by itself a dependency: two clauses about the same person are
    # RELATED, and his test asks whether the top FALLS, not whether they are
    # about one man. Actor-only sharing reads NEIGHBOUR, with its own reason.
    actor_shared = False
    if actor and not actor.startswith("("):
        row_all = set(re.findall(r"[a-z'’]+",
                                 (row.get("condition") or "").lower()))
        actor_shared = actor in row_all
    breaks = bool(shared)
    if breaks:
        why = ("it shares %s with the top event, so removing it removes what "
               "the top refers to" % ", ".join(repr(s) for s in shared[:4]))
    elif actor_shared:
        why = ("it shares only the actor %r with the top. Same person is "
               "relation, not dependency — take it away and the top still "
               "stands. Kept beside the walk, never in it." % actor)
    else:
        why = ("it shares nothing with the top event. Take it away and the top "
               "still stands, so it was never a dependency — it was standing "
               "next to one. His test, and it bit here.")
    return {
        "breaks": breaks, "shared": shared, "actor_shared": actor_shared,
        "verdict": ("SURVIVES — the top leans on it"
                    if breaks else "DROPPED — NEIGHBOUR"),
        "why": why,
    }


# GROUND — "something nobody made". Read through his own node classes: the
# physical human is the nearest thing this core has to something nobody built;
# rules, duties, values and business systems are things people made.
from_domains_made_by_people = ("RULE / DUTY / ASI", "VALUE / WISDOM",
                               "BUSINESS-MODEL / SYSTEM",
                               "EDUCATION / CAPABILITY INPUT",
                               "PRODUCT / SURFACE APPEARANCE")
GROUND_CLASSES = ("HUMAN BODY",)


def ground_check(condition: str) -> dict:
    """Did the walk stop at something nobody made?

    His rule: "a walk that stops at something a human built has not reached
    ground yet." Most single-sentence descents stop on something built, and
    saying so is the answer — claiming ground would be the failure."""
    from . import domains as D
    r = D.route_words(condition or "")
    classes = list(r.get("classes", {}).keys())
    made = [c for c in classes if c in from_domains_made_by_people]
    nobody = [c for c in classes if c in GROUND_CLASSES]
    if nobody and not made:
        return {"ground": True, "classes": classes,
                "why": "it routes to %s — the physical human, which nobody "
                       "made" % ", ".join(nobody)}
    if made:
        return {"ground": False, "classes": classes, "stopped_on": made,
                "why": "it routes to %s. People made that, so this is not "
                       "ground yet" % ", ".join(made)}
    return {"ground": False, "classes": classes,
            "why": ("nothing in it routes to a node class, so whether it is "
                    "ground is unknown. Unknown is not ground.")}


def prior_reality(text: str, end: dict = None, max_depth: int = 3) -> dict:
    """STEP 3 — descend from the thing as it stands to what was true before it.

    The descent goes only where the SOURCE goes. It recurses through stated
    priors that are themselves events in the same source, and it stops when
    there is no further stated prior — because the next level down would be
    assumed, and assumption is a separate, explicit call."""
    from . import growing as G
    events = G.events_in(text or "")
    if not events:
        return {"step": 3, "name": STEP_3, "direction": REVERSE,
                "events": 0, "levels": [], "survivors": [], "neighbours": [],
                "depth_reached": 0,
                "why_it_stopped": "no event was found in the source, so there is "
                                  "nothing to descend from",
                "reached_ground": False, "assumed_rows": 0,
                "law": "the descent starts at the thing as it stands, finished "
                       "and named."}

    top = events[-1]
    started_from = "the last event in the source"
    if end and end.get("named"):
        started_from = "the declared end: %s" % end.get("end")

    levels, survivors, neighbours = [], [], []
    seen = {top["n"]}
    frontier = [top]
    depth = 0
    stopped = ""

    while frontier and depth < max_depth:
        depth += 1
        rows, nxt = [], []
        for node in frontier:
            cands = entailments(node) + stated_priors(text, events, node["n"])
            for c in cands:
                if c["grade"] == STATED and c.get("from_event") in seen:
                    continue
                t = removal_test(c, node)
                row = dict(c)
                row.update({"level": depth, "below": node["n"],
                            "removal_test": t,
                            "id": "PR-%d-%02d" % (depth, len(rows) + 1)})
                rows.append(row)
                if t["breaks"]:
                    survivors.append(row)
                    if c["grade"] == STATED and c.get("from_event"):
                        seen.add(c["from_event"])
                        nxt.append(next(e for e in events
                                        if e["n"] == c["from_event"]))
                else:
                    # THE TEST IS LEXICAL, AND WHERE IT IS LEAST TRUSTWORTHY IS
                    # SAID SO. A clause from the SAME SENTENCE as the top that
                    # shares no word can still be the thing the top depends on —
                    # his rain example does exactly that: "pointed it in the air"
                    # and "thought its raining" share no word, and the first is
                    # the cause of the second. Seeing that needs knowledge of the
                    # world, which this descent is forbidden. So the drop stands
                    # and it is FLAGGED, never quietly reversed.
                    si, st = (_sentence_of(text, c.get("condition", "")),
                              _sentence_of(text, node.get("raw", "")))
                    if si >= 0 and si == st:
                        row["review"] = ("SAME SENTENCE — dropped on words alone. "
                                         "A dependency phrased in different words "
                                         "reads as a neighbour here. His call.")
                    neighbours.append(row)
        levels.append({"level": depth, "descended_from": [n["n"] for n in frontier],
                       "candidates": len(rows),
                       "survived": sum(1 for r in rows if r["removal_test"]["breaks"]),
                       "dropped": sum(1 for r in rows
                                      if not r["removal_test"]["breaks"]),
                       "rows": rows})
        frontier = nxt
        if not frontier:
            stopped = ("no further prior is STATED in the source. The next level "
                       "down would have to be assumed, and assumption is an "
                       "explicit call, never a step the descent takes on its own")
    if frontier and depth >= max_depth:
        stopped = ("the depth limit (%d) was reached with stated priors still "
                   "open" % max_depth)

    terminals = [r for r in survivors if r["level"] == depth] or survivors
    grounds = [dict(ground_check(r["condition"]), condition=r["condition"],
                    id=r["id"]) for r in terminals[:8]]
    reached = any(g["ground"] for g in grounds)

    return {
        "step": 3, "name": STEP_3, "direction": REVERSE,
        "started_from": started_from,
        "top_event": {"n": top["n"], "raw": top["raw"], "actor": top["actor"],
                      "happening": top["happening"]},
        "events": len(events),
        "levels": levels,
        "survivors": survivors,
        "neighbours": neighbours,
        "counts": {
            "candidates": sum(l["candidates"] for l in levels),
            "survived": len(survivors),
            "dropped_as_neighbours": len(neighbours),
            "stated": sum(1 for r in survivors if r["grade"] == STATED),
            "entailed": sum(1 for r in survivors if r["grade"] == ENTAILED),
            "assumed": 0,
            "dropped_but_flagged_for_review": sum(1 for r in neighbours
                                                  if r.get("review")),
        },
        "flagged_for_review": [r for r in neighbours if r.get("review")],
        "assumed_rows": 0,
        "depth_reached": depth,
        "why_it_stopped": stopped,
        "ground": grounds,
        "reached_ground": reached,
        "ground_note": ("his rule: a walk that stops at something a human built "
                        "has not reached ground yet. This one %s"
                        % ("reached ground" if reached else "did not")),
        "grade_means": dict(GRADE_MEANS),
        "law": "the removal test, his: take the step away — if the thing above "
               "still stands, it was a neighbour, not a dependency.",
        "refuses": "a dropped prior is kept with the reason it was dropped. "
                   "Nothing here is deleted, and nothing is assumed.",
    }


def assume(condition: str, why: str, proof_debt: int = 3,
           expires: str = "when the source is checked") -> dict:
    """The ONLY way an ASSUMED row exists. It stamps itself.

    His rule 5: anything forced or assumed is [SYNTHETIC] with proof-debt and an
    expiry, and is never presented as proven fact. Making this a separate call
    is what stops the descent inventing a past — `prior_reality` cannot reach
    it."""
    if not (0 <= int(proof_debt) <= 5):
        raise ValueError("proof debt is 0..5")
    return {
        "condition": condition, "grade": ASSUMED, "synthetic": True,
        "tag": "[SYNTHETIC]", "why": why, "proof_debt": int(proof_debt),
        "expires": expires, "source": "me, not him, not the text",
        "law": "never presented as proven fact.",
    }


def reverse_passes() -> dict:
    """Where reverse happens in his eighteen. Two places, and the first one is
    the correction this module exists for."""
    return {
        "passes": [
            {"at": [2, 3], "what": "intake — declare the end, descend to the "
                                   "prior reality it came out of",
             "built_by": "prior.declare_end / prior.prior_reality",
             "was": "ABSENT until Phase B"},
            {"at": [13], "what": "R-F-R — reverse, forward, reverse over the "
                                 "candidate arrangement",
             "built_by": "patterns.rfr_check", "was": "already running"},
        ],
        "his_correction": "R-F-R at 13 is the SECOND reverse. Steps 2 and 3 are "
                          "the first, and they run before decomposition.",
        "what_this_core_did_before": "ran forward from the text and reversed "
                                     "only at the check.",
    }


def stats() -> dict:
    return {
        "phase": "B — runtime pipeline (the two absent steps)",
        "steps_built": [2, 3],
        "direction": REVERSE,
        "grades": list(GRADES),
        "assumed_reachable_from_the_descent": False,
        "method_from": "docs/mainwork/THE_REVERSE_WALKS.md — his removal test",
        "pull_markers": (len(PULL_PHRASE.pattern.split("|"))
                         + len(PULL_VERB.pattern.split("|"))),
        "reverse_passes": 2,
        "refuses": ["blending two ends", "returning 'there is no end'",
                    "deleting a dropped prior", "claiming ground not reached",
                    "assuming a past"],
    }


def annotations() -> list:
    return [
        ("declare the end, and say what turns on it", "prior.declare_end"),
        ("his removal test, executable", "prior.removal_test"),
        ("reverse to prior reality", "prior.prior_reality"),
        ("a target ahead is not a reason behind", "prior.end_candidates"),
        ("assumption is an explicit call, never a step", "prior.assume"),
        ("two reverse passes, and 2-3 are the first", "prior.reverse_passes"),
    ]
