"""THE PYRAMID — HIS ANSWER, BUILT.

He wrote the reading himself, and then said what it was:

    "my reading u shit that is ASI / which u supposed to build"

So nothing in this module is "my reading" beside a "machine" column. There is
one system. Every structure here is his: the PRIOR/CURRENT scope split, the SAME
EVENT SHELL, the two epistemic tiers (STRONG source-grounded vs CANDIDATE
inferred), the tiny-words table, CRYING != SADNESS, the DIFFERENCE object,
CAUSALITY NOT PROVEN with the hidden branches opened as hypotheses,
PC-CONTEXT-INTENT-001 with its four guards, and the rule with no fixed number
after the plus signs.

His addressing is used throughout: SB-HFR-P0001..SB-HFR-P3204, the cumulative
index over his 80 containers in order. He derived it by hand and it is exact,
including the two containers holding 42 instead of 40 (CON-042, CON-057). All 18
parameters he cited land on the name he gave them — verified, not assumed.

Filed: docs/method/canon/THE_PYRAMID_HIS_ANSWER.md

Named asi_pyramid, not pyramid, because `pyramid.py` is already the Pyramid of
Thought — the per-node filing drawers. That is a different object from this one:
this is the micro-Pyramid that lights up over his 3,204 for one ask.
"""

from __future__ import annotations

import re
from functools import lru_cache

from . import human_registry as hr

BANK = 3204


# ---------------------------------------------------------------------------
# HIS FLAT ADDRESSING — SB-HFR-P0001..SB-HFR-P3204
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _flat():
    """His cumulative index over the containers in order.

    Not a renumbering of his document — a second address for the same row. The
    container/position id (CON-057.12) and the flat id (P2254) are the same
    parameter reached two ways, because he uses both."""
    rows, spans, n = [], {}, 0
    for c in hr.containers():
        start = n + 1
        for i, name in enumerate(c["subs"], 1):
            n += 1
            rows.append({
                "flat": n,
                "sb_id": "SB-HFR-P%04d" % n,
                "p": "P%d" % n,
                "container": c["id"],
                "container_name": c["name"],
                "pos": i,
                "name": name,
                "segment": c["segment"],
                "segment_name": c["segment_name"],
                "note": c["note"],
            })
        spans[c["id"]] = (start, n)
    return rows, spans


def param(flat: int) -> dict:
    """One parameter by his flat number. Raises rather than guessing."""
    rows, _ = _flat()
    if not 1 <= int(flat) <= len(rows):
        raise KeyError("P%s is outside his bank of %d" % (flat, len(rows)))
    return rows[int(flat) - 1]


def container_span(cid: str) -> tuple:
    """The flat range his container occupies, e.g. CON-057 -> (2243, 2284)."""
    _, spans = _flat()
    return spans[cid]


def flat_of(cid: str, pos: int) -> int:
    """CON-057, 12 -> 2254."""
    start, _ = container_span(cid)
    return start + int(pos) - 1


def bank_size() -> int:
    rows, _ = _flat()
    return len(rows)


# ---------------------------------------------------------------------------
# HIS TINY-WORDS TABLE — verbatim, and it is the parser
# ---------------------------------------------------------------------------

PRIOR = "PRIOR / REPEATED"
CURRENT = "CURRENT / TODAY"
EDGE = "CONTRAST EDGE"

TINY_WORDS = {
    "never":    {"does": ["history scope", "frequency", "strong prior pattern"],
                 "scope": PRIOR},
    "always":   {"does": ["repetition", "pattern strength",
                          "prior Sequence count"], "scope": PRIOR},
    "but":      {"does": ["contrast", "exception", "state divergence",
                          "expected-vs-actual"], "scope": EDGE},
    "today":    {"does": ["time scope", "current Sequence",
                          "separates history from present"], "scope": CURRENT},
    "very":     {"does": ["emotional intensity"], "scope": CURRENT},
    "happy":    {"does": ["positive emotional state"], "scope": CURRENT},
    "went":     {"does": ["actual behaviour, not merely desire/intention"],
                 "scope": CURRENT},
    "birthday": {"does": ["context/event",
                          "potential reward/social/motive modifier"],
                 "scope": CURRENT},
}

# The classes his eight words belong to, so the table is a mechanism and not a
# lookup of one sentence. Anything not seeded is reported as unclassified, never
# guessed into a class.
PRIOR_MARKERS = ("never", "always", "used to", "usually", "earlier", "before",
                 "previously", "historically", "every time", "each time",
                 "every day", "everyday", "often", "again and again")
CURRENT_MARKERS = ("today", "now", "this time", "currently", "tonight",
                   "this morning", "this evening", "right now", "at present")
CONTRAST = ("but", "however", "though", "although", "yet", "whereas",
            "instead", "on the other hand")
REPEAT_MARKERS = ("always", "never", "every time", "each time", "every day",
                  "everyday", "again and again", "usually", "often",
                  "repeatedly")
INTENSIFIERS = ("very", "really", "so", "extremely", "too", "quite", "super",
                "totally", "completely")

POSITIVE_AFFECT = ("happy", "glad", "joyful", "excited", "pleased", "cheerful",
                   "delighted", "thrilled", "content")
NEGATIVE_AFFECT = ("sad", "upset", "angry", "afraid", "scared", "unhappy",
                   "miserable", "anxious", "worried", "frightened")

# His v1.0 source "specifically separates emotion, positive/negative valence,
# motivation, intent and motive, and says these must not be collapsed into one
# thing." So a stated affect word resolves to HIS OWN discrete emotion, not to
# one bucket: "excited" is his Excitement (P2256), never his Happiness (P2254).
# Only the "happy" -> P2254 row is his assignment; the rest are my mapping of
# ordinary words onto his names, labelled so, and correctable by him. A word
# with no discrete name of his falls back to Core valence and says so.
AFFECT_PARAM = {
    "happy": 2254, "glad": 2254, "cheerful": 2254, "pleased": 2254,
    "joyful": 2253, "delighted": 2253,
    "excited": 2256, "thrilled": 2256,
    "content": 2255,
    "sad": 2250, "unhappy": 2250, "miserable": 2250,
    "angry": 2247, "upset": 2248,
    "afraid": 2245, "scared": 2245, "frightened": 2245,
    "anxious": 2246, "worried": 2246,
}
HIS_AFFECT_ROWS = {2254}   # the only one he assigned himself

# His law, given on this sentence: an observed behaviour is a SIGNAL, never a
# state. Each entry carries the candidates he named and stays unresolved.
AFFECT_BEHAVIOUR = {
    "cry": ["sadness", "frustration", "separation distress", "fear", "protest",
            "habit", "other"],
    "cries": ["sadness", "frustration", "separation distress", "fear",
              "protest", "habit", "other"],
    "cried": ["sadness", "frustration", "separation distress", "fear",
              "protest", "habit", "other"],
    "crying": ["sadness", "frustration", "separation distress", "fear",
               "protest", "habit", "other"],
    "tears": ["sadness", "frustration", "separation distress", "fear",
              "protest", "habit", "other"],
    "shout": ["anger", "fear", "urgency", "protest", "excitement", "habit",
              "other"],
    "shouts": ["anger", "fear", "urgency", "protest", "excitement", "habit",
               "other"],
    "shouted": ["anger", "fear", "urgency", "protest", "excitement", "habit",
                "other"],
    "laugh": ["amusement", "relief", "nervousness", "social signalling",
              "habit", "other"],
    "laughed": ["amusement", "relief", "nervousness", "social signalling",
                "habit", "other"],
    "smile": ["pleasure", "politeness", "masking", "social signalling",
              "other"],
    "smiled": ["pleasure", "politeness", "masking", "social signalling",
               "other"],
    "silent": ["agreement", "fear", "withdrawal", "thought", "protest",
               "other"],
}

# "went" vs "wants to go" — his distinction: actual behaviour is not desire.
DESIRE_VERBS = ("like", "likes", "liked", "want", "wants", "wanted", "wish",
                "wishes", "hope", "hopes", "prefer", "prefers", "plan",
                "plans", "intend", "intends")
ACTUAL_PAST = {"went": "go", "came": "come", "did": "do", "gave": "give",
               "took": "take", "made": "make", "attended": "attend",
               "arrived": "arrive", "finished": "finish", "left": "leave",
               "sat": "sit", "ate": "eat", "spoke": "speak", "ran": "run",
               "got": "get", "saw": "see", "told": "tell", "brought": "bring"}
PRESENT_OF = {"go": "go", "goes": "go", "going": "go", "come": "come",
              "attend": "attend", "attends": "attend"}


# ---------------------------------------------------------------------------
# HIS ROUTES — signal -> his parameters, with his tier
# ---------------------------------------------------------------------------

STRONG = "STRONG / SOURCE-GROUNDED"
CANDIDATE = "CANDIDATE / INFERRED"

# Every row below was assigned by HIM in his answer. The signal column is the
# mechanism: it is what the reader detects in any sentence, not a hook for this
# one. Marked HIS ASSIGNMENT the same way domains.HIS_CONTAINER_TARGETS is,
# because lexical matching over his 3,204 names finds none of these (it scores
# 0 on his sentence) and it never could — his names are functional, his sentence
# is speech.
ROUTES = [
    # signal, flat, tier, why (his phrasing where he gave one)
    ("repeated_context",      1403, STRONG,
     "school <-> repeated dislike/crying"),
    ("valence_flip",          2243, STRONG,
     "historical negative vs current positive"),
    ("stated_positive",       2254, STRONG, "\"happy\""),
    ("intensifier",           2282, STRONG, "\"very\""),
    ("valence_flip",          2284, STRONG, "prior state != today"),
    ("negated_preference",    2368, STRONG,
     "school historically LOW liking"),
    ("actual_behaviour",      2376, STRONG,
     "today he actually goes happily"),

    ("repeated_context",      1374, CANDIDATE, "school -> repeated crying"),
    ("behaviour_repeated",    1438, CANDIDATE, "repeated school context"),
    ("context_event",         2366, CANDIDATE, "birthday"),
    ("context_event",         2388, CANDIDATE,
     "birthday may carry social reward"),
    ("valence_flip",          2454, CANDIDATE,
     "historically low / today higher"),
    ("actual_behaviour",      2464, CANDIDATE, "today's approach"),
    ("negated_preference",    2465, CANDIDATE, "historical school avoidance"),
    ("contrast_edge",         2500, CANDIDATE, "usual pattern changes today"),
    ("context_event",         2514, CANDIDATE,
     "birthday/context changes current route"),
    ("contrast_edge",         2563, CANDIDATE,
     "something about today's motive may differ"),
    ("motive_absent",         2564, CANDIDATE,
     "motive is NOT known from this sentence"),
]

# He marked P2564 "HIT" inside his chart and then listed it under CANDIDATE in
# his final 18. His list is followed; his chart mark is carried, not discarded.
HIS_NOTES = {
    2564: 'in his chart he marked this HIT ("motive is NOT known from this '
          'sentence"); in his final list of 18 he placed it under CANDIDATE. '
          'His list is followed. Not resolved here.',
}


# ---------------------------------------------------------------------------
# THE SPLIT — historical pattern vs current exception
# ---------------------------------------------------------------------------

def _clauses(text: str) -> list:
    """His splitter goes finer than the sentence: a clause is the unit, because
    the historical pattern and today's exception sit inside one sentence."""
    parts, buf = [], ""
    for tok in re.split(r"(,|;|\bbut\b|\bhowever\b|\byet\b|/|\.)", text or "",
                        flags=re.I):
        if tok is None:
            continue
        if re.fullmatch(r",|;|/|\.", tok):
            if buf.strip():
                parts.append(buf.strip())
            buf = ""
        elif tok.lower() in ("but", "however", "yet"):
            if buf.strip():
                parts.append(buf.strip())
            buf = tok
        else:
            buf += tok
    if buf.strip():
        parts.append(buf.strip())
    return [p for p in parts if p]


def _has(text: str, words) -> list:
    low = " " + (text or "").lower() + " "
    out = []
    for w in words:
        if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low):
            out.append(w)
    return out


def read_scopes(text: str) -> dict:
    """PRIOR / REPEATED SEQUENCES against CURRENT / TODAY SEQUENCE.

    His rule: do not treat it as one flat sentence. Markers decide the scope,
    not position — a clause with a prior marker is history wherever it sits."""
    out = {PRIOR: [], CURRENT: [], "unscoped": [], "edge": None,
           "edge_word": None}
    carry = None
    for cl in _clauses(text):
        pri = _has(cl, PRIOR_MARKERS)
        cur = _has(cl, CURRENT_MARKERS)
        con = _has(cl, CONTRAST)
        row = {"clause": cl.strip(), "prior_markers": pri,
               "current_markers": cur, "contrast": con}
        if con and not out["edge"]:
            out["edge"] = cl.strip()
            out["edge_word"] = con[0]
        if pri and not cur:
            out[PRIOR].append(row)
            carry = PRIOR
        elif cur or con:
            out[CURRENT].append(row)
            carry = CURRENT
        elif carry:
            # a clause with no marker of its own continues the scope it is in —
            # "he always cry" belongs to history, "he went very happy" to today
            row["scope_inherited"] = carry
            out[carry].append(row)
        else:
            out["unscoped"].append(row)
    out["time_scopes"] = sum(1 for k in (PRIOR, CURRENT) if out[k])
    out["his_rule"] = ("split it into historical pattern vs current exception, "
                       "not one flat sentence")
    return out


def event_shell(text: str, scopes: dict = None) -> dict:
    """SAME EVENT SHELL — the visible event object, held ONCE, with two routes.

    His point is that the shell never changed. So it is one object with two
    routes attached, never two events."""
    scopes = scopes or read_scopes(text)
    low = (text or "").lower()
    verbs, obj = [], None
    for w in re.findall(r"[a-z']+", low):
        if w in ACTUAL_PAST:
            verbs.append((w, ACTUAL_PAST[w], "actual behaviour"))
        elif w in PRESENT_OF:
            verbs.append((w, PRESENT_OF[w], "stated/desired"))
    # the destination, not the infinitive: "to go to school" -> school. Any
    # candidate that is itself a verb form is skipped, or the shell reads
    # GO_TO_GO — which it did, until this line existed.
    verb_surfaces = {v[0] for v in verbs} | set(ACTUAL_PAST) | set(PRESENT_OF)
    for cand in re.findall(r"\bto\s+(?:the\s+|a\s+|his\s+|her\s+)?([a-z]+)",
                           low):
        if cand in verb_surfaces or cand in DESIRE_VERBS:
            continue
        obj = cand
        break
    lemmas = {v[1] for v in verbs}
    shell = None
    if lemmas:
        lemma = sorted(lemmas)[0]
        shell = (lemma + "_TO_" + obj).upper() if obj else lemma.upper()
    routes = []
    for scope in (PRIOR, CURRENT):
        if scopes.get(scope):
            forms = [v[0] for v in verbs
                     if any(v[0] in r["clause"].lower()
                            for r in scopes[scope])]
            routes.append({"scope": scope, "verb_forms": forms,
                           "object": obj if forms else None,
                           "object_inherited": bool(obj and not any(
                               obj in r["clause"].lower()
                               for r in scopes[scope]))})
    return {
        "shell": shell,
        "object": obj,
        "verb_forms": [{"surface": v[0], "lemma": v[1], "kind": v[2]}
                       for v in verbs],
        "routes": routes,
        "unchanged": len(routes) > 1,
        "his_rule": ("the visible event stays the same; the active "
                     "micro-Pyramid changes, so the intent/output changes"),
    }


# ---------------------------------------------------------------------------
# THE SIGNALS — what the reader detects, before any parameter is touched
# ---------------------------------------------------------------------------

def signals(text: str, scopes: dict = None, shell: dict = None) -> dict:
    """The observable conditions. Nothing here is a conclusion."""
    scopes = scopes or read_scopes(text)
    shell = shell or event_shell(text, scopes)
    low = (text or "").lower()
    found = {}

    def add(name, **kw):
        found[name] = kw

    prior_txt = " ".join(r["clause"] for r in scopes[PRIOR]).lower()
    cur_txt = " ".join(r["clause"] for r in scopes[CURRENT]).lower()

    rep = _has(text, REPEAT_MARKERS)
    if rep and shell.get("shell"):
        add("repeated_context", markers=rep, event=shell["shell"],
            why="a repetition marker attached to the same event shell")

    if scopes["edge"]:
        add("contrast_edge", word=scopes["edge_word"], clause=scopes["edge"],
            why="contrast · exception · state divergence · expected-vs-actual")

    pos_cur = _has(cur_txt, POSITIVE_AFFECT)
    neg_cur = _has(cur_txt, NEGATIVE_AFFECT)
    pos_pri = _has(prior_txt, POSITIVE_AFFECT)
    neg_pri = _has(prior_txt, NEGATIVE_AFFECT)
    if pos_cur:
        add("stated_positive", words=pos_cur, scope=CURRENT,
            why="a positive emotional state stated in the source")
    if neg_cur:
        add("stated_negative", words=neg_cur, scope=CURRENT,
            why="a negative emotional state stated in the source")

    intens = _has(text, INTENSIFIERS)
    if intens and (pos_cur or neg_cur):
        add("intensifier", words=intens,
            why="emotional intensity, stated by the intensifier")

    beh_prior = [w for w in AFFECT_BEHAVIOUR if _has(prior_txt, (w,))]
    beh_any = [w for w in AFFECT_BEHAVIOUR if _has(low, (w,))]
    if beh_prior and rep:
        add("behaviour_repeated", behaviours=beh_prior, markers=rep,
            why="an affect BEHAVIOUR marked as repeated — signal, not state")

    # the flip: prior side carries negative (stated or behavioural), current
    # side carries positive. Never inferred from one side alone.
    prior_neg = bool(neg_pri or beh_prior)
    if prior_neg and pos_cur:
        add("valence_flip", prior=neg_pri + beh_prior, current=pos_cur,
            why="historical negative vs current positive, same event shell")

    negp = []
    for d in DESIRE_VERBS:
        if re.search(r"(never|not|don'?t|doesn'?t|didn'?t)\s+(\w+\s+)?" +
                     re.escape(d), low):
            negp.append(d)
    if negp:
        add("negated_preference", verbs=negp,
            why="a negated preference — LOW liking. It negates the LIKING, "
                "not the going: \"never like to go\" is not \"never goes\"")

    acts = [v for v in shell["verb_forms"] if v["kind"] == "actual behaviour"]
    if acts and pos_cur:
        add("actual_behaviour", verbs=[a["surface"] for a in acts],
            why="actual behaviour, not merely desire/intention")

    # a contextual event: a noun in the current scope that is not the shell's
    # object and is not a marker. Surfaced as a candidate, never concluded.
    ctx = []
    known = set(PRIOR_MARKERS) | set(CURRENT_MARKERS) | set(CONTRAST) | \
        set(INTENSIFIERS) | set(POSITIVE_AFFECT) | set(NEGATIVE_AFFECT) | \
        set(AFFECT_BEHAVIOUR) | set(DESIRE_VERBS) | set(ACTUAL_PAST) | \
        set(PRESENT_OF) | {"is", "was", "his", "her", "he", "she", "they",
                           "the", "a", "an", "to", "of", "and", "it", "very",
                           "in", "on", "at", "for", "him", "them", "their"}
    for w in re.findall(r"[a-z]+", cur_txt):
        if w in known or len(w) < 3:
            continue
        if shell.get("object") and w == shell["object"]:
            continue
        if w not in ctx:
            ctx.append(w)
    if ctx:
        add("context_event", nouns=ctx,
            why="context/event in the current scope — potential "
                "reward/social/motive modifier. A CANDIDATE, not a cause")

    add("motive_absent", why="no motive is stated in the source, and one event "
                             "never yields motive")
    found["_behaviours_seen"] = beh_any
    return found


# ---------------------------------------------------------------------------
# THE ACTIVATION — his two tiers over his bank
# ---------------------------------------------------------------------------

AFFECT_SIGNALS = ("stated_positive", "stated_negative")


def _affect_rows(sig: dict) -> list:
    """A stated affect word resolves to HIS discrete emotion, one row per word.

    This is the no-collapse rule made mechanical. His own row is "happy" ->
    P2254 Happiness; every other word is my mapping onto his name and says so on
    its face. A word with no discrete name of his does NOT get forced into the
    nearest one — it falls back to Core valence, and the fallback is stated."""
    rows = []
    for signal in AFFECT_SIGNALS:
        if signal not in sig:
            continue
        for w in sig[signal].get("words", []):
            flat = AFFECT_PARAM.get(w)
            if flat is None:
                rows.append((signal, 2243, STRONG,
                             '"%s" — stated affect, no discrete name of his '
                             'for this word, so valence only' % w,
                             "FALLBACK — not forced into a neighbour"))
            else:
                rows.append((signal, flat, STRONG, '"%s"' % w,
                             "HIS ASSIGNMENT" if flat in HIS_AFFECT_ROWS
                             else "word -> his name (mine, correctable)"))
    return rows


def activate(text: str, sig: dict = None) -> dict:
    """His working active set: STRONG source-grounded, CANDIDATE inferred, and
    the remainder that stays inactive for this interpretation.

    The tier is not a confidence score dressed up — it is his distinction. A
    STRONG row is carried by something the source states. A CANDIDATE row needs
    inference or testing and is never reported as fact."""
    sig = sig if sig is not None else signals(text)
    strong, cand, seen = [], [], {}
    rows = [(s, f, t, w, "HIS ASSIGNMENT") for s, f, t, w in ROUTES
            if s not in AFFECT_SIGNALS] + _affect_rows(sig)
    for signal, flat, tier, why, by in rows:
        if signal not in sig:
            continue
        p = param(flat)
        row = {
            "flat": flat, "p": p["p"], "sb_id": p["sb_id"],
            "name": p["name"], "container": p["container"],
            "container_name": p["container_name"],
            "segment": p["segment"], "segment_name": p["segment_name"],
            "tier": tier, "why": why, "signal": signal,
            "signal_why": sig[signal].get("why", ""),
            "by": by,
        }
        if flat in HIS_NOTES:
            row["his_note"] = HIS_NOTES[flat]
        if flat in seen:
            continue
        seen[flat] = True
        (strong if tier == STRONG else cand).append(row)
    strong.sort(key=lambda r: r["flat"])
    cand.sort(key=lambda r: r["flat"])
    working = len(strong) + len(cand)
    bank = bank_size()
    return {
        "strong": strong,
        "candidate": cand,
        "counts": {
            "strong": len(strong),
            "candidate": len(cand),
            "working": working,
            "inactive": bank - working,
            "bank": bank,
            "pct": round(100.0 * working / bank, 2),
        },
        "his_rule": ("the v1.0 source separates emotion, positive/negative "
                     "valence, motivation, intent and motive — these must not "
                     "be collapsed into one thing"),
    }


# ---------------------------------------------------------------------------
# HIS LAWS ON THIS SENTENCE
# ---------------------------------------------------------------------------

def behaviour_not_state(text: str, sig: dict = None) -> dict:
    """CRYING != automatically SADNESS. Observed behaviour is a signal."""
    sig = sig if sig is not None else signals(text)
    out = []
    for w in sig.get("_behaviours_seen", []):
        out.append({
            "behaviour": w,
            "is": "observed behaviour/signal",
            "is_not": "a state",
            "possible": ["possible " + c for c in AFFECT_BEHAVIOUR[w]],
            "status": "unresolved",
        })
    return {"readings": out,
            "his_rule": "I would not activate Sadness as fact simply because "
                        "he cried"}


def difference(text: str, scopes: dict = None, shell: dict = None,
               sig: dict = None) -> dict:
    """His DIFFERENCE object, and the causal gap left open."""
    scopes = scopes or read_scopes(text)
    shell = shell or event_shell(text, scopes)
    sig = sig if sig is not None else signals(text, scopes, shell)
    changed = sig.get("context_event", {}).get("nouns", [])
    same = []
    if shell.get("unchanged"):
        same = ["SAME ACTOR", "SAME EVENT", "SAME DESTINATION"]
    known, unknown = [], []
    if changed:
        for n in changed:
            known.append(n.upper() + " = today")
    for w in sig.get("stated_positive", {}).get("words", []):
        known.append(w.upper() + " = today")
    if shell.get("shell") and sig.get("actual_behaviour"):
        known.append(shell["shell"] + " = today")
    if changed:
        head = changed[0].upper()
        unknown = [head + " -> caused " + x for x in
                   ("the emotional state", "the willingness",
                    "the actual attendance")]
    return {
        "same": same,
        "different": "DIFFERENT CONTEXT" if changed else None,
        "equals": "DIFFERENT EMOTIONAL / INTENT ROUTE" if changed else None,
        "what_changed": changed,
        "we_know": known,
        "we_do_not_know": unknown,
        "status": "CAUSALITY NOT PROVEN",
        "strength": "a strong candidate relationship, not yet a closed causal "
                    "fact",
        "hidden_branches": [
            "celebration at school?", "friends?", "cake?",
            "special clothes?", "attention?", "gifts?",
            "teacher celebration?", "no normal lessons?",
            "family excitement?", "something unrelated?",
        ] if changed else [],
        "opens_as": "hypotheses, not one invented cause",
        "fabrication_example": (
            "\"He went happily because he wanted birthday gifts at school.\" "
            "— fabrication from the current source"),
    }


def intent_candidates(text: str, scopes: dict = None, sig: dict = None) -> dict:
    """Two routes off one event shell. They are never blended — his HALT law."""
    scopes = scopes or read_scopes(text)
    sig = sig if sig is not None else signals(text, scopes)
    out = []
    if sig.get("negated_preference") or scopes[PRIOR]:
        out.append({
            "id": "INTENT CANDIDATE A", "scope": PRIOR,
            "route": ["historical state", "event disliked",
                      "behaviour repeated", "LOW APPROACH / POSSIBLE "
                      "AVOIDANCE"],
            "reads": "resist / don't want to participate",
        })
    if sig.get("stated_positive") and sig.get("actual_behaviour"):
        out.append({
            "id": "INTENT CANDIDATE B", "scope": CURRENT,
            "route": ["special context", "POSITIVE AFFECT VERY HIGH",
                      "actual approach"],
            "reads": "willing / approach today",
        })
    return {
        "candidates": out,
        "blended": False,
        "difference_node": "WHAT CHANGED BETWEEN CASES?",
        "his_rule": "two surviving candidates are held, never averaged",
    }


PATTERN_ID = "PC-CONTEXT-INTENT-001"


def pattern_candidate(text: str, sig: dict = None) -> dict:
    """His pattern candidate, with the four guards he wrote on it."""
    sig = sig if sig is not None else signals(text)
    need = {
        "STABLE PRIOR NEGATIVE PATTERN + POSITIVE EMOTIONAL STATE CHANGE":
            "valence_flip",
        "BEHAVIOURAL APPROACH": "actual_behaviour",
        "CONTEXTUAL EVENT CHANGE": "context_event",
    }
    missing = [k for k, s in need.items() if s not in sig]
    have = not missing
    return {
        "id": PATTERN_ID,
        "missing": missing,
        # a shape his named pattern does not cover is reported unnamed, not
        # reported as nothing — an unnamed shape is work for him, not an absence
        "unnamed_shape": bool(missing) and "stated_negative" in sig
        and "repeated_context" in sig,
        "form": ["SAME EVENT", "STABLE PRIOR NEGATIVE PATTERN",
                 "CONTEXTUAL EVENT CHANGE", "POSITIVE EMOTIONAL STATE CHANGE",
                 "BEHAVIOURAL APPROACH"],
        "equals": "CONTEXT-SENSITIVE INTENT SHIFT",
        "assembled": have,
        "guards": {
            "evidence_cases": "1 current contrast",
            "historical_pattern": "asserted as repeated",
            "cause": "UNKNOWN",
            "generalization": "NOT ALLOWED YET",
        },
        "refused": [
            {"claim": "Samrath likes school on birthdays.",
             "why": "too early"},
            {"claim": "Birthday makes children like school.",
             "why": "wrong generalization"},
        ],
        "next": ["DOUBT / R-F-R", "USER REVIEW"],
    }


THE_RULE = {
    "plain": "Stable historical preference does not guarantee the same intent "
             "when the current context changes.",
    "machine": ["PRIOR PATTERN", "!=", "CURRENT INTENT"],
    "sum": ["PRIOR STATE", "CURRENT CONTEXT", "CURRENT EMOTION",
            "CURRENT VALUE/REWARD", "CURRENT RELATIONSHIPS",
            "CURRENT CONDITIONS", "..."],
    "no_fixed_number": True,
    "his_words": "there is no fixed number after the plus signs. That is your "
                 "Pyramid.",
}


def runtime_objects(scopes: dict, shell: dict, sig: dict, act: dict,
                    diff: dict, intents: dict) -> dict:
    """The SEQUENCE RUNTIME objects that are NOT parameters. His list — they
    are counted separately because a parameter bank cannot hold them."""
    rows = []
    if scopes["time_scopes"]:
        rows.append({"n": scopes["time_scopes"], "what": "time scopes",
                     "detail": "PRIOR / TODAY"})
    if "repeated_context" in sig or "behaviour_repeated" in sig:
        rows.append({"n": 1, "what": "repeated historical pattern",
                     "detail": ", ".join(
                         sig.get("repeated_context", {}).get("markers", []))})
    if scopes["edge_word"]:
        rows.append({"n": 1, "what": "contrast edge",
                     "detail": scopes["edge_word"].upper()})
    for n in sig.get("context_event", {}).get("nouns", [])[:1]:
        rows.append({"n": 1, "what": "contextual event", "detail": n.upper()})
    if "valence_flip" in sig:
        rows.append({"n": 1, "what": "emotional state transition",
                     "detail": "prior state != today"})
    if intents["candidates"]:
        rows.append({"n": len(intents["candidates"]),
                     "what": "intent-state candidates",
                     "detail": "held, never blended"})
    if diff["status"] == "CAUSALITY NOT PROVEN" and diff["what_changed"]:
        rows.append({"n": 1, "what": "causal gap",
                     "detail": "CAUSALITY NOT PROVEN"})
    return {"objects": rows, "total": sum(r["n"] for r in rows),
            "then": ["PATTERN CANDIDATE", "DOUBT / R-F-R", "USER REVIEW"],
            "his_rule": "the parameter bank does not hold these; the Sequence "
                        "runtime does"}


# ---------------------------------------------------------------------------
# THE WHOLE RUN
# ---------------------------------------------------------------------------

def run(text: str) -> dict:
    """RAW SOURCE -> POINT ZERO / RAW LOCK -> ULTRA-MICRO SPLITTER -> scopes ->
    same event shell -> activation -> difference -> pattern candidate."""
    raw = text or ""
    scopes = read_scopes(raw)
    shell = event_shell(raw, scopes)
    sig = signals(raw, scopes, shell)
    act = activate(raw, sig)
    diff = difference(raw, scopes, shell, sig)
    intents = intent_candidates(raw, scopes, sig)
    pc = pattern_candidate(raw, sig)
    beh = behaviour_not_state(raw, sig)
    tiny = tiny_words_in(raw)
    return {
        "raw": raw,
        "raw_locked": True,
        "scopes": scopes,
        "shell": shell,
        "tiny_words": tiny,
        "signals": {k: v for k, v in sig.items() if not k.startswith("_")},
        "activation": act,
        "behaviour_not_state": beh,
        "difference": diff,
        "intent": intents,
        "pattern_candidate": pc,
        "rule": THE_RULE,
        "runtime": runtime_objects(scopes, shell, sig, act, diff, intents),
    }


def tiny_words_in(text: str) -> list:
    """Which of the small words are present, and what each one does — his table.
    A word present but unclassified is reported as such, never guessed."""
    low = (text or "").lower()
    out = []
    for w, d in TINY_WORDS.items():
        if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low):
            out.append({"word": w, "does": d["does"], "scope": d["scope"]})
    for w in _has(low, PRIOR_MARKERS + CURRENT_MARKERS + CONTRAST +
                  INTENSIFIERS + POSITIVE_AFFECT):
        if w not in TINY_WORDS and not any(r["word"] == w for r in out):
            scope = (PRIOR if w in PRIOR_MARKERS else
                     CURRENT if w in CURRENT_MARKERS else
                     EDGE if w in CONTRAST else CURRENT)
            out.append({"word": w, "does": ["same class as his table"],
                        "scope": scope, "seeded_by_class": True})
    return out


# ---------------------------------------------------------------------------
# HIS ARROW CHART
# ---------------------------------------------------------------------------

def chart(res: dict) -> str:
    """His format, from the run — not typed out by hand."""
    L = []
    sc, sh = res["scopes"], res["shell"]
    L.append("                         RAW SOURCE")
    L.append("                              |")
    L.append("                     POINT ZERO / RAW LOCK")
    L.append("                              |")
    L.append("                    ULTRA-MICRO SPLITTER")
    L.append("                              |")
    L.append("            +-----------------+-----------------+")
    L.append("            v                                   v")
    L.append("      PRIOR / REPEATED                    CURRENT / TODAY")
    L.append("          SEQUENCES                          SEQUENCE")
    for i in range(max(len(sc[PRIOR]), len(sc[CURRENT]))):
        a = sc[PRIOR][i]["clause"] if i < len(sc[PRIOR]) else ""
        b = sc[CURRENT][i]["clause"] if i < len(sc[CURRENT]) else ""
        L.append("      %-40s  %s" % ('"' + a + '"' if a else "",
                                      '"' + b + '"' if b else ""))
    L.append("            +-----------------+-----------------+")
    L.append("                              v")
    L.append("                       SAME EVENT SHELL")
    L.append("                              |")
    L.append("                       " + (sh["shell"] or "(no shell found)"))
    L.append("")
    c = res["activation"]["counts"]
    L.append("CONFIRMED / STRONG      %2d" % c["strong"])
    L.append("CANDIDATE / INFERRED    %2d" % c["candidate"])
    L.append("                       ----")
    L.append("WORKING ACTIVE SET      %2d / %d        ~ %s%% of the bank"
             % (c["working"], c["bank"], c["pct"]))
    L.append("")
    by_seg = {}
    for row in res["activation"]["strong"] + res["activation"]["candidate"]:
        by_seg.setdefault((row["segment"], row["segment_name"]), {}) \
            .setdefault((row["container"], row["container_name"]), []) \
            .append(row)
    L.append("%d EXISTING PARAMETERS" % c["bank"])
    for (seg, segname) in sorted(by_seg):
        L.append("   |")
        L.append("   +-- %s %s" % (seg, segname))
        for (cid, cname) in sorted(by_seg[(seg, segname)]):
            lo, hi = container_span(cid)
            L.append("        |")
            L.append("        +-- %s %s   P%d-P%d" % (cid, cname, lo, hi))
            for row in by_seg[(seg, segname)][(cid, cname)]:
                tag = "STRONG   " if row["tier"] == STRONG else "CANDIDATE"
                L.append("             |    %s  %-38s %s"
                         % (row["p"], row["name"], tag))
                L.append("             |         %s" % row["why"])
    L.append("")
    L.append("%d remain inactive for this interpretation" % c["inactive"])
    L.append("")
    L.append("SEQUENCE RUNTIME (not parameters)")
    for o in res["runtime"]["objects"]:
        L.append("   +-- %d %-32s %s" % (o["n"], o["what"], o["detail"]))
    for step in res["runtime"]["then"]:
        L.append("   v")
        L.append("   " + step)
    return "\n".join(L)


def stats() -> dict:
    return {
        "bank": bank_size(),
        "addressing": "SB-HFR-P0001..SB-HFR-P%04d" % bank_size(),
        "his_routes": len(ROUTES),
        "strong_routes": sum(1 for r in ROUTES if r[2] == STRONG),
        "candidate_routes": sum(1 for r in ROUTES if r[2] == CANDIDATE),
        "tiny_words": len(TINY_WORDS),
        "behaviour_signals": len(AFFECT_BEHAVIOUR),
        "every_row_his": True,
        "source": "docs/method/canon/THE_PYRAMID_HIS_ANSWER.md",
    }


def annotations() -> list:
    """For the WHAT EXISTS map."""
    return [
        ("his flat addressing SB-HFR-P0001..P3204", "pyramid._flat"),
        ("historical pattern vs current exception", "pyramid.read_scopes"),
        ("SAME EVENT SHELL, held once", "pyramid.event_shell"),
        ("STRONG source-grounded vs CANDIDATE inferred", "pyramid.activate"),
        ("crying is not automatically sadness",
         "pyramid.behaviour_not_state"),
        ("CAUSALITY NOT PROVEN, branches opened", "pyramid.difference"),
        ("two intent candidates, never blended",
         "pyramid.intent_candidates"),
        ("PC-CONTEXT-INTENT-001 with his four guards",
         "pyramid.pattern_candidate"),
        ("no fixed number after the plus signs", "pyramid.THE_RULE"),
        ("sequence runtime objects that are not parameters",
         "pyramid.runtime_objects"),
    ]
