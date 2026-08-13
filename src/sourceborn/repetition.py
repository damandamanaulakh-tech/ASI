"""SAME ACTION, CHANGED FUNCTION — and the same event seen from two positions.

Two things his father/door example exposed, both of which the machine could not
represent. He picked them himself: "go for 1 & 3".

=============================================================================
1 · SAME ACTION / CHANGED FUNCTION
=============================================================================

His discovery, from the fictional example
"A father checks the front door five times every night … he knows he already
checked it, but he goes back again":

    CHECK #1     → obtains information: "door is locked."
    CHECK #2-5   → may no longer primarily obtain new information

    identical physical action  ≠  identical functional role

    "That's a powerful ASI principle."

WHY THE PATTERN ENGINE WAS BLIND TO IT. `micro.py` derives every structural
fact from CONTENT. Five checks of the same door produce five micro-sequences
with the same entities, the same action, the same facts and the SAME SIGNATURE.
`patterns.group_repeats` clusters them as one arrangement with support 5 and
reports "this recurs" — which is the wrong reading. The difference he found is
not in the content at all. It is in the ORDINAL POSITION within the repetition:
check #4 cannot acquire what check #1 already acquired.

So this module adds the axis that was missing — WHERE in a repetition an
occurrence sits — and derives the FUNCTION from the position rather than from
the words.

The functions an occurrence can serve are held OPEN. The machine says the first
check acquired information and a later one cannot have; it does NOT say the
later one is reassurance, ritual, or habit. His list of candidates for what the
later checks might be doing is kept, unchosen:

    certainty · reassurance · ritual · responsibility expression ·
    risk reduction · habit

=============================================================================
3 · THE MASK, EXTENDED TO OBSERVER POSITION
=============================================================================

    Father's view : ACTION check door · MEANING protect family · VALUE safety
    Family's view : the SAME repeated checking · MEANING possibly excessive ·
                    RESULT irritation
    ASI view      : same behaviour + different observers = different meaning

    "BEHAVIOR ≠ MEANING. Meaning is actor/observer dependent until evidence
     resolves it."

This is not a new mechanism. It is Filter 3 / Source already in the engine:
one witness caps at Medium, and **two witnesses who differ HALT — the gap is
the Mask, it goes to him, and it is never averaged.** Here the two witnesses are
the same event seen from two positions. So the rule is reused, not reinvented,
and the same refusal applies: the machine does not pick the actor's reading over
the observer's, and it does not split the difference.
"""
from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# 1 · OCCURRENCE POSITION AND FUNCTION
FIRST = "FIRST OCCURRENCE"
LATER = "LATER OCCURRENCE"
ONLY = "SINGLE OCCURRENCE"

# what a FIRST occurrence of an information-seeking action does
FUNC_ACQUIRE = "acquires the information"
# what a LATER occurrence cannot be doing, on the source's own evidence
FUNC_CANNOT_ACQUIRE = "cannot be acquiring what the first already acquired"

# HIS list of what a later occurrence MIGHT be doing. Held open, never chosen.
LATER_FUNCTION_CANDIDATES = ("certainty", "reassurance", "ritual",
                             "responsibility expression", "risk reduction",
                             "habit")

# actions whose whole point is to obtain information — the ones where a repeat
# is structurally interesting, because the information is already in hand
INFORMATION_ACTIONS = {
    "check", "checks", "checked", "checking", "verify", "verified",
    "verifying", "confirm", "confirmed", "confirming", "ask", "asked",
    "asking", "look", "looked", "looking", "read", "reread", "re-read",
    "count", "counted", "counting", "test", "tested", "testing", "call",
    "called", "calling", "message", "messaged", "recheck", "rechecked",
    "reconfirm", "review", "reviewed", "inspect", "inspected", "watch",
    "watched", "search", "searched", "measure", "measured",
}

# a count stated in the sentence — "five times", "5 times", "twice", "again"
_NUMWORD = {"once": 1, "twice": 2, "thrice": 3, "one": 1, "two": 2,
            "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
            "eight": 8, "nine": 9, "ten": 10, "several": 3, "many": 3,
            "multiple": 3, "repeatedly": 3, "few": 3}
_COUNT_RE = re.compile(
    r"\b(\d{1,3}|once|twice|thrice|one|two|three|four|five|six|seven|eight|"
    r"nine|ten|several|many|multiple|repeatedly|few)\s+"
    r"(?:more\s+)?times?\b", re.I)
_AGAIN_RE = re.compile(
    r"\b(again|and again|over and over|back again|another time|once more|"
    r"keeps?|kept|every night|each night|every day|each day|nightly|daily)\b",
    re.I)
# the source stating the actor ALREADY knows — this is what makes a repeat
# structurally different rather than merely frequent
_ALREADY_KNOWS_RE = re.compile(
    r"\b(knows? (?:he|she|they|i)? ?(?:already|had already)?|"
    r"already (?:checked|did|done|verified|confirmed|knew|knows)|"
    r"even though (?:he|she|they) (?:knows?|knew)|"
    r"he knows|she knows|they know)\b", re.I)


def _actions_in(sentence: str) -> list[str]:
    low = (sentence or "").lower()
    return sorted({w for w in re.findall(r"[a-z-]+", low)
                   if w in INFORMATION_ACTIONS})


def stated_count(sentence: str) -> dict:
    """How many times the source itself says the action happened.

    A count in the source is evidence; an absent count is absent, not one."""
    m = _COUNT_RE.search(sentence or "")
    if m:
        raw = m.group(1).lower()
        n = int(raw) if raw.isdigit() else _NUMWORD.get(raw, 0)
        return {"count": n, "stated_as": m.group(0),
                "exact": raw.isdigit() or raw in ("once", "twice", "thrice"),
                "why": "the source states the number of occurrences"}
    m = _AGAIN_RE.search(sentence or "")
    if m:
        return {"count": 2, "stated_as": m.group(0), "exact": False,
                "why": "the source says it happened again — at least two, and "
                       "the exact number is not stated"}
    return {"count": 1, "stated_as": "", "exact": False,
            "why": "no repetition is stated, so this reads as one occurrence — "
                   "absent, not zero and not many"}


def read_repetition(sentence: str) -> dict:
    """The axis that was missing: WHERE in a repetition an occurrence sits, and
    what that position lets it do.

    Returns one row per occurrence position. The FIRST is the one that can
    acquire; the LATER ones cannot acquire what the first already did, and what
    they ARE doing is left open with his candidates listed."""
    acts = _actions_in(sentence)
    cnt = stated_count(sentence)
    knows = bool(_ALREADY_KNOWS_RE.search(sentence or ""))
    n = max(1, int(cnt["count"] or 1))

    if not acts:
        return {"applies": False,
                "why": "no information-seeking action in the sentence, so "
                       "position cannot change function here",
                "count": cnt, "actor_knows_already": knows}

    occurrences = []
    for i in range(1, min(n, 5) + 1):
        if n == 1:
            occurrences.append({
                "index": 1, "position": ONLY,
                "function": FUNC_ACQUIRE,
                "function_status": "SUPPORTED — a single occurrence of an "
                                   "information action acquires the "
                                   "information",
                "candidates": []})
            break
        if i == 1:
            occurrences.append({
                "index": 1, "position": FIRST,
                "function": FUNC_ACQUIRE,
                "function_status": "SUPPORTED by the structure — the first "
                                   "occurrence is the one that can acquire",
                "candidates": []})
        else:
            occurrences.append({
                "index": i, "position": LATER,
                "function": FUNC_CANNOT_ACQUIRE,
                "function_status": ("SUPPORTED — the source says the actor "
                                    "already knows, so this occurrence cannot "
                                    "be acquiring it"
                                    if knows else
                                    "OPEN — the source does not say whether "
                                    "the actor still knows, so acquisition "
                                    "cannot be ruled out for this occurrence"),
                "candidates": list(LATER_FUNCTION_CANDIDATES),
                "refuses": "the machine does not pick which of these it is"})

    changed = n > 1 and knows
    return {
        "applies": True,
        "actions": acts,
        "count": cnt,
        "actor_knows_already": knows,
        "occurrences": occurrences,
        "same_action_changed_function": changed,
        "reading": (
            "identical physical action ≠ identical functional role — the first "
            "occurrence acquired the information and a later one cannot have, "
            "so the later occurrences are serving something else. WHICH thing "
            "is open." if changed else
            "the action repeats, but the source does not establish that the "
            "actor already had the information, so a change of function is not "
            "supported yet"),
        "his_principle": "identical physical action ≠ identical functional role",
        "generalises_to": ["asking once vs asking a fifth time",
                           "checking once vs checking a fifth time",
                           "reading once vs rereading",
                           "confirming once vs reconfirming",
                           "calling once vs repeated calling"],
    }


def position_signature(base_signature: str, occ: dict) -> str:
    """A signature that carries POSITION, so two occurrences of one action are
    no longer the same address.

    This is the whole fix: before, five checks collapsed into one arrangement
    because their content was identical. Now the first and the later ones have
    different addresses and the pattern layer can see a difference where the
    words show none."""
    pos = occ.get("position", ONLY)
    tag = {FIRST: "occ:first", LATER: "occ:later", ONLY: "occ:only"}.get(
        pos, "occ:only")
    return (base_signature + "|" + tag) if base_signature else tag


# ---------------------------------------------------------------------------
# 3 · THE MASK BY OBSERVER POSITION
ACTOR = "ACTOR"           # the one doing it
OBSERVER = "OBSERVER"     # the one it happens around
MACHINE = "MACHINE"       # this system's own reading

# how the source marks whose reading a clause is
_ACTOR_MARK = re.compile(
    r"\b(he says|she says|they say|he said|she said|because he|because she|"
    r"he wants|she wants|they want|his reason|her reason|he feels|she feels|"
    r"in his view|in her view|he believes|she believes)\b", re.I)
_OBSERVER_MARK = re.compile(
    r"\b(family (?:gets?|is|are|feels?|found|find)|"
    r"they (?:get|got|are|were|feel|felt) (?:irritated|annoyed|angry|upset|"
    r"tired|frustrated)|"
    r"his family|her family|the others|everyone else|people (?:think|say)|"
    r"others (?:think|say|feel))\b", re.I)
_STATE_WORDS = re.compile(
    r"\b(irritated|annoyed|angry|upset|frustrated|tired|worried|scared|"
    r"safe|unsafe|calm|uncomfortable|excessive|unnecessary|pointless)\b", re.I)


def read_views(sentence: str) -> dict:
    """Whose reading of the same behaviour is present, and whether they differ.

    Reuses the Source/Mask rule already in the engine rather than inventing a
    new one: one view caps the claim; two views that differ HALT, and the gap
    goes to him. It is never averaged and neither side is preferred."""
    s = (sentence or "").strip()
    views: list[dict] = []
    # states are attributed PER SENTENCE, not by a character window. A window
    # bled the observer's "irritated" into the actor's view and the actor's
    # "safe" into the observer's — two readings that must stay apart.
    parts = [p for p in re.split(r"(?<=[.!?])\s+", s) if p.strip()]

    def states_for(pattern) -> tuple[list, str]:
        """Prefer the sentence where the marker AND a state word co-occur.
        "his family" appears in the clause about wanting them SAFE and again in
        the clause about them being IRRITATED — the second is the observer's
        reading, and picking the first match would have handed the observer the
        actor's state."""
        best = ([], "")
        for part in parts:
            m = pattern.search(part)
            if not m:
                continue
            st = sorted({x.group(0).lower()
                         for x in _STATE_WORDS.finditer(part)})
            if not best[1]:
                best = (st, m.group(0))
            if st:
                best = (st, m.group(0))
        return best

    a_states, a_mark = states_for(_ACTOR_MARK)
    a = _ACTOR_MARK.search(s)
    if a:
        states = a_states
        views.append({
            "position": ACTOR, "marker": a.group(0),
            "meaning": "the actor's own stated meaning for the behaviour",
            "states": states,
            "status": "SOURCE-STATED — he told us his reason. A stated reason "
                      "and the underlying mechanism are not necessarily the "
                      "same thing."})
    o_states, o_mark = states_for(_OBSERVER_MARK)
    o = _OBSERVER_MARK.search(s)
    if o:
        states = o_states
        views.append({
            "position": OBSERVER, "marker": o.group(0),
            "meaning": "the observer's reading of the same behaviour",
            "states": states,
            "status": "SOURCE-REPORTED — what the others experienced. It is "
                      "not evidence that the observer's reading is correct."})

    differ = len(views) >= 2
    return {
        "views": views,
        "count": len(views),
        "differ": differ,
        # the existing rule, applied to observer position
        "mask": ({"kind": "observer-position Mask",
                  "what": "one behaviour, two readings that do not agree",
                  "actor": next((v for v in views
                                 if v["position"] == ACTOR), None),
                  "observer": next((v for v in views
                                    if v["position"] == OBSERVER), None),
                  "verdict": "HALT — the gap goes to him",
                  "refuses": "it is not averaged, and neither reading is "
                             "preferred over the other. Meaning is "
                             "actor/observer dependent until evidence "
                             "resolves it."}
                 if differ else {}),
        "confidence_cap": ("Medium — one view only, which is one witness"
                           if len(views) == 1 else
                           "HALT — two views differ" if differ else
                           "no view is marked in the source"),
        "his_rule": "BEHAVIOR ≠ MEANING. The same behaviour with different "
                    "observers yields different interpreted meaning.",
    }


def stats() -> dict:
    return {"later_function_candidates": len(LATER_FUNCTION_CANDIDATES),
            "information_actions": len(INFORMATION_ACTIONS),
            "positions": [FIRST, LATER, ONLY],
            "observer_positions": [ACTOR, OBSERVER, MACHINE],
            "his_principle": "identical physical action ≠ identical "
                             "functional role",
            "mask_reused": "Filter 3 / Source — two witnesses who differ HALT "
                           "and the gap goes to him, never averaged"}
