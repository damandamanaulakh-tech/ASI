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


# ===========================================================================
# HIS SECOND RUN (2026-08-13) — the 16 containers, the row-level matcher, and
# the ASI additions layer.
#
# He revised the container set himself and drew the line honestly:
#
#   "I can currently verify the container-level hits exactly enough to show
#    16/80 active regions. I cannot yet truthfully say something like 'P2251,
#    P2267…' because the 3,204 row payload is compressed and the metadata alone
#    does not expose each individual parameter name. I won't invent the P-row
#    count."
#
# The payload IS decoded here (data/human_registry.json, all 3,204 names), so
# the row-level matcher below is the thing he left open. Every row states which
# signal reached it and who assigned it — his rows say HIS ASSIGNMENT, mine say
# so and are correctable.
#
# All 16 of his container ranges and all 5 of his segment ranges were verified
# exact against his document before any of this was written, including CON-043
# starting at P1683, which only lands if the CON-042 offset of 42 is carried.
# ===========================================================================

SOURCE_GROUNDED = "SOURCE-GROUNDED"
INFERRED = "CANDIDATE / INFERRED"
HELD = "HELD OPEN"

# His 16, with the HIT label he wrote on each one.
HIS_CONTAINERS = [
    ("CON-017", "readiness to go to school"),
    ("CON-020", "he actually went today"),
    ("CON-033", "usual school history vs today"),
    ("CON-035", 'repeated "always cry" history'),
    ("CON-043", "what changed between usual and today?"),
    ("CON-044", "WHY happy today? cause unknown"),
    ("CON-045", "SAME EVENT DIFFERENT STATE"),
    ("CON-052", '"usual dislike + crying" versus "today happy"'),
    ("CON-054", '"never" "always" "but today"'),
    ("CON-057", "cry / very happy"),
    ("CON-058", "crying = observed emotional signal, "
                "happy = explicit affect label"),
    ("CON-060", '"very happy"'),
    ("CON-061", '"doesn\'t like" / crying'),
    ("CON-062", "usual willingness vs today's participation"),
    ("CON-063", "GO -> SCHOOL under two different states"),
    ("CON-064", "asks WHY today's willingness changed — "
                "BUT actual motive remains OPEN"),
]

# THE ROW-LEVEL MATCHER. (container, position) -> the signal that reaches it,
# its tier, and the reason. Positions are into HIS OWN sub-parameter list, so
# the flat P id is computed from his addressing, never typed by hand.
ROW_ROUTES = {
 "CON-017": [(9, "actual_behaviour", SOURCE_GROUNDED, "an action was available"),
             (10, "context_event", INFERRED, "the context read as an opening"),
             (23, "actual_behaviour", SOURCE_GROUNDED, "today's approach"),
             (24, "negated_preference", INFERRED, "the usual side"),
             (36, "valence_flip", INFERRED, "the cost was paid today"),
             (38, "actual_behaviour", SOURCE_GROUNDED, "go/no-go was pre-set"),
             (40, "context_event", INFERRED, "opportunity against the usual")],
 "CON-020": [(6, "actual_behaviour", SOURCE_GROUNDED, '"went" is a Go decision'),
             (7, "negated_preference", INFERRED, "the usual no-go"),
             (15, "valence_flip", SOURCE_GROUNDED, "approach vs avoid, both present"),
             (17, "actual_behaviour", SOURCE_GROUNDED, "he committed and went"),
             (27, "repeated_context", INFERRED, "habit against today's goal"),
             (29, "context_event", INFERRED, "a cue in the current scope"),
             (32, "repeated_context", INFERRED, "the default the history set")],
 "CON-033": [(3, "same_event", SOURCE_GROUNDED, "what happened is stated"),
             (4, "same_event", SOURCE_GROUNDED, '"school" is the place'),
             (5, "current_scope", SOURCE_GROUNDED, '"today" is the time'),
             (6, "actor_named", SOURCE_GROUNDED, "the actor is named"),
             (7, "contrast_edge", SOURCE_GROUNDED, "usual before today"),
             (11, "stated_affect", SOURCE_GROUNDED, "the affect is on the record"),
             (13, "prior_scope", SOURCE_GROUNDED, "two time contexts"),
             (23, "generalization", SOURCE_GROUNDED,
              '"never"/"always" is a GIST of history, not an enumeration '
              'of every visit')],
 "CON-035": [(7, "repeated_context", SOURCE_GROUNDED, "school -> crying, stated as repeated"),
             (13, "repeated_context", INFERRED, "how strong the habit is, not stated"),
             (14, "repeated_context", SOURCE_GROUNDED, "context-cued — HIS ROW"),
             (28, "repeated_context", INFERRED, "what triggers it is not stated"),
             (31, "repeated_context", HELD, "routine vs habit is not decided"),
             (32, "repeated_context", INFERRED, "the default behaviour")],
 "CON-043": [(1, "context_event", HELD, "cause and effect are not separated yet"),
             (2, "context_event", SOURCE_GROUNDED,
              "co-occurrence is not causation — this row IS the guard"),
             (6, "context_event", HELD, "a confound is possible and unnamed"),
             (9, "context_event", HELD, "more than one cause may hold"),
             (13, "contrast_edge", INFERRED, "the usual day is the counterfactual"),
             (17, "contrast_edge", INFERRED, "but-for the birthday, unknown"),
             (19, "context_event", INFERRED, "the context may only enable"),
             (39, "context_event", HELD, "a hidden variable is live — his H7")],
 "CON-044": [(9, "context_event", SOURCE_GROUNDED, "this is ambiguity, not risk"),
             (10, "context_event", SOURCE_GROUNDED, "the ambiguity is held, not closed"),
             (11, "motive_absent", SOURCE_GROUNDED, "the unknown is quantified as unknown"),
             (28, "context_event", HELD, "unknown unknowns remain"),
             (30, "motive_absent", SOURCE_GROUNDED, "the hedge is appropriate here"),
             (36, "motive_absent", SOURCE_GROUNDED, "evidence is NOT enough to stop"),
             (38, "valence_flip", SOURCE_GROUNDED, "the flip is the surprise")],
 "CON-045": [(9, "context_event", SOURCE_GROUNDED, "crying is the symptom, not the cause"),
             (11, "generalization", SOURCE_GROUNDED, "the assumptions are surfaced"),
             (12, "motive_absent", SOURCE_GROUNDED, "given separated from unknown"),
             (14, "contrast_edge", SOURCE_GROUNDED, "same event, two frames"),
             (28, "context_event", SOURCE_GROUNDED, "the changed variable is the key one"),
             (31, "motive_absent", SOURCE_GROUNDED, "this is ill-defined and says so"),
             (38, "context_event", SOURCE_GROUNDED,
              '"why does he like school now" would be the wrong problem')],
 "CON-052": [(3, "contrast_edge", SOURCE_GROUNDED, "the two clauses are linked"),
             (5, "actor_named", SOURCE_GROUNDED, '"he"/"his" resolve to the named actor'),
             (6, "actor_named", SOURCE_GROUNDED, "one actor across both scopes"),
             (16, "same_event", SOURCE_GROUNDED, "one situation model, two states"),
             (17, "contrast_edge", SOURCE_GROUNDED, "today updates the model"),
             (19, "current_scope", SOURCE_GROUNDED, '"today" is the connective'),
             (20, "contrast_edge", SOURCE_GROUNDED, '"but" is the marker'),
             (26, "valence_flip", SOURCE_GROUNDED, "the two states are inconsistent"),
             (34, "motive_absent", SOURCE_GROUNDED, "the ambiguity is held open")],
 "CON-054": [(7, "generalization", SOURCE_GROUNDED, '"never like" presupposes he goes'),
             (8, "prior_scope", SOURCE_GROUNDED, "the history is the given"),
             (19, "generalization", SOURCE_GROUNDED,
              '"never"/"always" read as source generalization, NOT as every '
              'single historical visit'),
             (23, "current_scope", HELD, '"today" has no date to resolve to'),
             (27, "contrast_edge", SOURCE_GROUNDED, "the exception is appropriate"),
             (30, "motive_absent", HELD, "the subtext is not concluded"),
             (31, "generalization", SOURCE_GROUNDED, "literal vs meant, reconciled")],
 "CON-057": [(1, "valence_flip", SOURCE_GROUNDED, "historical negative vs current positive"),
             (12, "stated_affect", SOURCE_GROUNDED, '"happy" — HIS ROW'),
             (39, "repeated_context", INFERRED, "a standing mood is possible"),
             (40, "intensifier", SOURCE_GROUNDED, '"very" — HIS ROW'),
             (42, "valence_flip", SOURCE_GROUNDED, "prior state != today — HIS ROW"),
             (3, "affect_behaviour", HELD, "one of his seven, none chosen"),
             (4, "affect_behaviour", HELD, "one of his seven, none chosen"),
             (6, "affect_behaviour", HELD, "one of his seven, none chosen"),
             (8, "affect_behaviour", HELD,
              "Sadness stays HELD — he cried, that is all the source says"),
             (10, "affect_behaviour", HELD, "one of his seven, none chosen")],
 "CON-058": [(12, "stated_affect", SOURCE_GROUNDED, "the valence is identifiable"),
             (14, "stated_affect", SOURCE_GROUNDED, '"happy" is an explicit label'),
             (17, "context_event", HELD, "the cause of the affect is not attributed"),
             (26, "stated_affect", SOURCE_GROUNDED, "affect read from text"),
             (32, "valence_flip", SOURCE_GROUNDED, "context congruence checked"),
             (34, "valence_flip", SOURCE_GROUNDED, "the shift is detected"),
             (22, "affect_behaviour", HELD,
              "crying may mask something — not decided")],
 "CON-060": [(2, "context_event", INFERRED, "birthday -> anticipation — HIS ROW"),
             (4, "negated_preference", SOURCE_GROUNDED,
              "historically LOW liking — HIS ROW"),
             (12, "actual_behaviour", SOURCE_GROUNDED,
              "today he actually goes happily — HIS ROW"),
             (22, "context_event", INFERRED, "novelty — his H4"),
             (24, "context_event", INFERRED, "social reward — HIS ROW"),
             (35, "valence_flip", SOURCE_GROUNDED, "better than expected")],
 "CON-061": [(13, "negated_preference", HELD,
              '"never like to go" is NOT "never goes" — avoidance stays HELD'),
             (18, "affect_behaviour", HELD, "goal blockage is not stated"),
             (28, "affect_behaviour", HELD, "withdrawal is not stated")],
 "CON-062": [(3, "actual_behaviour", INFERRED, "commitment today"),
             (4, "valence_flip", INFERRED, "the task's value may have changed"),
             (10, "valence_flip", INFERRED,
              "historically low / today higher — HIS ROW"),
             (20, "actual_behaviour", INFERRED, "today's approach — HIS ROW"),
             (21, "negated_preference", INFERRED,
              "historical avoidance — HIS ROW")],
 "CON-063": [(16, "contrast_edge", INFERRED,
              "the usual pattern changes today — HIS ROW"),
             (24, "context_event", INFERRED, "an intention conditional on the day"),
             (30, "context_event", INFERRED,
              "opportunity-triggered — HIS ROW"),
             (40, "motive_absent", SOURCE_GROUNDED,
              "intent is separated from motive, which is the point")],
 "CON-064": [(1, "motive_absent", SOURCE_GROUNDED, "no motive is stated"),
             (3, "motive_absent", HELD, "the hidden motive stays a hypothesis"),
             (33, "context_event", HELD, "competing motives are possible"),
             (39, "contrast_edge", INFERRED,
              "motive stability vs shift — HIS ROW"),
             (40, "motive_absent", SOURCE_GROUNDED,
              "motive-inference confidence is LOW — HIS ROW")],
}

# Signals his 16 containers need that the first pass did not produce.
def _extra_signals(text: str, scopes: dict, shell: dict, sig: dict) -> dict:
    out = dict(sig)
    if scopes.get(PRIOR):
        out["prior_scope"] = {"why": "a historical scope is present"}
    if scopes.get(CURRENT):
        out["current_scope"] = {"why": "a current scope is present"}
    if shell.get("shell"):
        out["same_event"] = {"why": "one event object across both scopes"}
    name = actor_name(text)
    if name:
        out["actor_named"] = {"name": name,
                              "why": "a named actor, not only pronouns"}
    gen = _has(text, ("never", "always", "every time", "everyone", "all",
                      "every day", "everyday"))
    if gen:
        out["generalization"] = {
            "words": gen,
            "why": "source generalization — NOT an enumeration. \"always cry\" "
                   "does not assert every single historical school visit "
                   "ended in crying"}
    if sig.get("stated_positive") or sig.get("stated_negative"):
        out["stated_affect"] = {"why": "an affect is stated in the source"}
    if sig.get("_behaviours_seen"):
        out["affect_behaviour"] = {"behaviours": sig["_behaviours_seen"],
                                   "why": "an affect BEHAVIOUR, which is a "
                                          "signal and never a state"}
    return out


def actor_name(text: str) -> str:
    """The named actor. micro.py finds only pronouns, so "Samrath" — the
    subject of the whole story — was invisible. A capitalised token that is not
    a sentence-initial function word and matches nothing in any lexicon is
    reported as a NAME; anything else is left alone rather than guessed."""
    known = set(PRIOR_MARKERS) | set(CURRENT_MARKERS) | set(CONTRAST) | \
        set(INTENSIFIERS) | set(POSITIVE_AFFECT) | set(NEGATIVE_AFFECT) | \
        set(AFFECT_BEHAVIOUR) | set(DESIRE_VERBS) | set(ACTUAL_PAST) | \
        set(PRESENT_OF) | {"the", "he", "she", "they", "it", "his", "her",
                           "their", "a", "an", "and", "is", "was", "to"}
    for tok in re.findall(r"\b[A-Z][a-z]{2,}\b", text or ""):
        if tok.lower() not in known:
            return tok
    return ""


def rows_for(text: str, sig: dict = None, scopes: dict = None,
             shell: dict = None) -> dict:
    """THE ROW-LEVEL MATCHER — the exact P rows inside his 16 containers.

    This is the number he would not invent. Each row carries the signal that
    reached it, its tier, and whether he named it."""
    scopes = scopes or read_scopes(text)
    shell = shell or event_shell(text, scopes)
    sig = _extra_signals(text, scopes, shell,
                         sig if sig is not None else
                         signals(text, scopes, shell))
    his_named = {(s, f) for s, f, _t, _w in ROUTES}
    his_flats = {f for _s, f, _t, _w in ROUTES}
    out, tiers = [], {SOURCE_GROUNDED: 0, INFERRED: 0, HELD: 0}
    for cid, label in HIS_CONTAINERS:
        for pos, signal, tier, why in ROW_ROUTES.get(cid, []):
            if signal not in sig:
                continue
            flat = flat_of(cid, pos)
            p = param(flat)
            out.append({
                "flat": flat, "p": p["p"], "sb_id": p["sb_id"],
                "name": p["name"], "pos": pos,
                "container": cid, "container_name": p["container_name"],
                "container_label": label,
                "segment": p["segment"], "segment_name": p["segment_name"],
                "tier": tier, "signal": signal, "why": why,
                "by": "HIS ASSIGNMENT" if flat in his_flats
                      else "resolved here (correctable)",
            })
            tiers[tier] += 1
    out.sort(key=lambda r: r["flat"])
    by_con, by_seg = {}, {}
    for r in out:
        by_con[r["container"]] = by_con.get(r["container"], 0) + 1
        by_seg[r["segment"]] = by_seg.get(r["segment"], 0) + 1
    return {
        "rows": out,
        "counts": {
            "rows": len(out),
            "source_grounded": tiers[SOURCE_GROUNDED],
            "inferred": tiers[INFERRED],
            "held_open": tiers[HELD],
            "containers": len(by_con),
            "containers_total": 80,
            "segments": len(by_seg),
            "segments_total": 10,
            "bank": bank_size(),
            "untouched": bank_size() - len(out),
            "pct": round(100.0 * len(out) / bank_size(), 2),
        },
        "by_container": by_con,
        "by_segment": by_seg,
        "his_line": "16 containers != 16 parameters. Several individual P rows "
                    "inside each container can fire.",
        "resolved": "the row payload IS decoded here, so the count he would "
                    "not invent is now a real number he can check row by row",
    }


# ---------------------------------------------------------------------------
# THE ASI ADDITIONS — above the 3,204, and they are not new parameters
# ---------------------------------------------------------------------------

ASSOCIATION_ONLY = "ASSOCIATION ONLY — not causality"


def relations(text: str, scopes: dict = None, shell: dict = None,
              sig: dict = None) -> dict:
    """His runtime relations. Generated from the parse, numbered as he numbered
    them. They are NOT new P parameters and are never written to the bank."""
    scopes = scopes or read_scopes(text)
    shell = shell or event_shell(text, scopes)
    sig = sig if sig is not None else signals(text, scopes, shell)
    name = actor_name(text) or "(actor)"
    obj = shell.get("object") or "(object)"
    verb = (shell.get("verb_forms") or [{"lemma": "(action)"}])[0]["lemma"]
    beh = (sig.get("_behaviours_seen") or [None])[0]
    pos = sig.get("stated_positive", {}).get("words") or \
        sig.get("stated_negative", {}).get("words") or []
    ctx = sig.get("context_event", {}).get("nouns") or []
    rep = sig.get("repeated_context", {}).get("markers") or []
    R = []

    def add(a, arrow, b, note=""):
        R.append({"id": "R%02d" % (len(R) + 1), "from": a, "rel": arrow,
                  "to": b, "note": note})

    add(name, "->", obj)
    add(name, "->", verb)
    if scopes.get(PRIOR):
        add("usual-state", "->", obj)
        if sig.get("negated_preference"):
            add("usual-state", "->", "dislike")
        if beh:
            add("usual-state", "->", beh)
            if rep:
                add(beh, "->", "repeated historical observation",
                    "from %s — a generalization, not an enumeration"
                    % ", ".join(rep))
    if scopes.get(CURRENT):
        for c in ctx[:1]:
            add("today", "->", c)
        if sig.get("actual_behaviour"):
            add("today", "->", "%s-going" % obj)
        for w in pos[:1]:
            add("today", "->", w)
    if scopes.get(PRIOR) and scopes.get(CURRENT):
        add("usual Sequence", "<->", "today Sequence", "comparison")
        if ctx and pos:
            add("%s-context" % ctx[0], "<->", "changed affect",
                ASSOCIATION_ONLY)
    return {"relations": R, "count": len(R),
            "not_parameters": True,
            "his_rule": "They are not new P parameters."}


# His seven interpretation frames. The context word is substituted; the frames
# themselves are general, and H7 is structural — it is what stops the machine
# closing a cause.
INTERPRETATION_FRAMES = [
    ("H1", "{ctx} changed the meaning of {obj}",
     "normally {obj} = ordinary/undesired activity; "
     "today {obj} + {ctx} = special experience", "REVIEW"),
    ("H2", "the social surrounding changed",
     "friends · classmates · teachers · attention · celebration — "
     "none are in the source", "SYNTHETIC CANDIDATE"),
    ("H3", "reward expectation",
     "cake · gifts · celebration · recognition", "OPEN / SYNTHETIC"),
    ("H4", "novelty",
     "ordinary day vs special day", "OPEN"),
    ("H5", "relationship effect",
     "he may have wanted to see a particular person", "UNKNOWN"),
    ("H6", "a different activity",
     "normal work may not have been expected today", "UNKNOWN"),
    ("H7", "{ctx} is unrelated",
     "{ctx} happens today AND the affect happens today, but some completely "
     "different factor could explain it. THIS CANDIDATE PREVENTS FALSE "
     "CAUSALITY.", "COUNTEREXAMPLE — always kept"),
]


def interpretations(text: str, sig: dict = None, shell: dict = None) -> dict:
    shell = shell or event_shell(text)
    sig = sig if sig is not None else signals(text)
    ctx = (sig.get("context_event", {}).get("nouns") or ["(context)"])[0]
    obj = shell.get("object") or "(event)"
    out = []
    for hid, title, detail, status in INTERPRETATION_FRAMES:
        out.append({"id": hid,
                    "title": title.format(ctx=ctx, obj=obj),
                    "detail": detail.format(ctx=ctx, obj=obj),
                    "status": status})
    return {"candidates": out, "count": len(out),
            "none_concluded": True,
            "his_rule": "ASI can generate possible explanations. It must not "
                        "invent one."}


# His three pattern candidates from this run.
def pattern_candidates(text: str, sig: dict = None) -> dict:
    sig = sig if sig is not None else signals(text)
    flip = "valence_flip" in sig
    ctx = "context_event" in sig
    out = [
     {"id": "PC-01", "title": "Context-dependent affect/willingness",
      "form": ["SAME EVENT", "CHANGED CONTEXT"],
      "equals": "DIFFERENT AFFECT / PARTICIPATION STATE",
      "strength": "very strong" if (flip and ctx) else "not assembled",
      "assembled": flip and ctx},
     {"id": "PC-02", "title": "Baseline with an exception",
      "form": ["BASELINE: event -> dislike / negative behaviour",
               "EXCEPTION: event + today's context -> positive affect"],
      "equals": "EXCEPTION does not destroy BASELINE, and BASELINE does not "
                "invalidate EXCEPTION",
      "strength": "the rule this teaches", "assembled": flip},
     {"id": "PC-03", "title": "Intent is not permanently attached to the event",
      "form": ["GO -> SCHOOL cannot permanently mean \"I don't want to go\"",
               "because today the same event exists under a different active "
               "Pyramid configuration"],
      "equals": "SAME EVENT + DIFFERENT ACTIVE PYRAMID PATH = DIFFERENT INTENT",
      "strength": "supports his earlier rule", "assembled": flip and ctx},
    ]
    return {"candidates": out, "count": len(out),
            "assembled": sum(1 for c in out if c["assembled"])}


# ---------------------------------------------------------------------------
# LEARNING = REINFORCEMENT, NOT DUPLICATION
# ---------------------------------------------------------------------------

# His prior rules, with the example that taught each. A new example that fits
# an existing rule adds SUPPORT — it never creates a second copy of the rule.
PRIOR_RULES = [
    {"id": "RULE-001",
     "text": "Same event + different Pyramid path = different intent",
     "taught_by": "the mall example",
     "support": 1},
]


def reinforce(text: str, sig: dict = None) -> dict:
    """His instruction, exactly: strengthened, not newly created.

        PRIOR USER RULE: Same event + different Pyramid path = different intent
        CURRENT EXAMPLE: SUPPORT +1

        Not: invent another duplicate rule
    """
    sig = sig if sig is not None else signals(text)
    out = []
    for r in PRIOR_RULES:
        applies = "valence_flip" in sig and "context_event" in sig
        out.append({**r,
                    "applies_here": applies,
                    "support_after": r["support"] + (1 if applies else 0),
                    "action": "SUPPORT +1" if applies else "not touched",
                    "duplicate_created": False})
    return {"rules": out,
            "strengthened": sum(1 for r in out if r["applies_here"]),
            "new_rules_invented": 0,
            "his_rule": "I call it strengthened rather than newly created "
                        "because you already taught this rule with the mall "
                        "example. That is exactly how learning should work. "
                        "Not: invent another duplicate rule."}


def counters(rowres: dict, rel: dict, interp: dict, pcs: dict,
             reinf: dict, scopes: dict) -> dict:
    """His three boxes, in his order and with his labels."""
    c = rowres["counts"]
    return {
     "existing": [
      ("Total registered P rows", c["bank"]),
      ("Total containers", c["containers_total"]),
      ("Candidate containers hit", c["containers"]),
      ("Exact P-row hits", c["rows"]),
      ("  of which SOURCE-GROUNDED", c["source_grounded"]),
      ("  of which CANDIDATE / INFERRED", c["inferred"]),
      ("  of which HELD OPEN", c["held_open"]),
      ("Existing parameters added", 0),
      ("Existing parameters modified", 0),
     ],
     "generated": [
      ("Parent Sequence", 1),
      ("Child comparison Sequences",
       sum(1 for k in (PRIOR, CURRENT) if scopes.get(k))),
      ("Runtime relations", rel["count"]),
      ("Interpretation candidates", interp["count"]),
      ("Pattern candidates", pcs["count"]),
      ("Existing deep rule strengthened", reinf["strengthened"]),
     ],
     "promoted": [
      ("New canonical parameters", 0),
      ("New approved patterns", 0),
      ("New approved rubrics", 0),
      ("User corrections", 0),
     ],
     "gate": "PROMOTED KNOWLEDGE stays at zero until he approves. Nothing here "
             "writes to his bank.",
    }


def full_run(text: str) -> dict:
    """HIS STANDARD DISPLAY FORMAT, in his order:

        3,204 hits -> two Sequences -> differences -> ASI additions ->
        existing-pattern reinforcement / new candidate -> answer
    """
    base = run(text)
    scopes, shell = base["scopes"], base["shell"]
    sig = signals(text, scopes, shell)
    rowres = rows_for(text, sig, scopes, shell)
    rel = relations(text, scopes, shell, sig)
    interp = interpretations(text, sig, shell)
    pcs = pattern_candidates(text, sig)
    reinf = reinforce(text, sig)
    return {
        **base,
        "sequences": {
            "parent": {"id": "PARENT", "event": shell.get("shell"),
                       "children": 2 if (scopes.get(PRIOR) and
                                         scopes.get(CURRENT)) else 1},
            "seq_a": {"id": "SEQ-A / USUAL", "scope": PRIOR,
                      "chain": [c["clause"] for c in scopes.get(PRIOR, [])]},
            "seq_b": {"id": "SEQ-B / TODAY", "scope": CURRENT,
                      "chain": [c["clause"] for c in scopes.get(CURRENT, [])]},
        },
        "his_containers": [{"id": cid, "label": lab,
                            "span": container_span(cid),
                            "rows": rowres["by_container"].get(cid, 0)}
                           for cid, lab in HIS_CONTAINERS],
        "row_level": rowres,
        "relations": rel,
        "interpretations": interp,
        "pattern_candidates": pcs,
        "reinforcement": reinf,
        "counters": counters(rowres, rel, interp, pcs, reinf, scopes),
        "format": "3,204 hits -> two Sequences -> differences -> ASI additions "
                  "-> existing-pattern reinforcement / new candidate -> answer",
    }
