"""THE ULTRA-MICRO SPLITTER — every sentence becomes a micro-sequence.

His rule, in his own refinement of his own earlier words (canon:
docs/method/canon/THE_MACHINE_AS_HE_STATES_IT.md):

    EVERY SENTENCE GENERATES A MICRO-SEQUENCE REPRESENTATION.
    Every micro-Sequence may:
        activate an existing pattern,
        contribute evidence to an existing pattern,
        contradict an existing pattern,
        modify confidence in a pattern,
        or create a candidate new pattern.

    "Because otherwise the machine would create millions of false 'patterns'
     from single occurrences."

So a sentence ALWAYS yields a representation; a PATTERN is only what survives
DIFFERENCE + RELATIONSHIP + REPETITION/ORDER + CONTEXT + RESULT across many of
them. This module does the representation. `patterns.py` does the surviving.

His field list is the specification, taken from his own worked example of
"He didn't tell me where we were going." — ENTITY · RELATION · ACTION ·
NEGATION · INFORMATION OBJECT · INFORMATION STATE · EXPECTED INFORMATION ·
ACTUAL INFORMATION · TEMPORAL RELATION · DEPENDENCY · EXPECTATION DIFFERENCE ·
POSSIBLE HUMAN EFFECT · INTENT · REPETITION LINK · PATTERN CONTRIBUTION.
Every one of those is produced here, from rules, with no field left blank
without saying why it is empty.

TWO HARD RULES THIS MODULE KEEPS:
  1. **INTENT IS NEVER DECIDED HERE.** A single event yields
     "UNKNOWN — not directly observed from this event alone", always. Intent is
     read from arrangement across many events, and only he approves it.
  2. **POSSIBLE HUMAN EFFECTS ARE HELD OPEN, NEVER CHOSEN.** The machine lists
     what a structure could produce in a person. It never says which one he
     felt. That field is his.
"""
from __future__ import annotations

import hashlib
import re

# ---------------------------------------------------------------------------
# LEXICONS — real word lists, not samples. Each entry earns its place by being
# a word that changes the STRUCTURE of what is being said.

PRONOUN_SELF = {"i", "me", "my", "mine", "myself", "we", "us", "our", "ours"}
PRONOUN_OTHER = {"he", "him", "his", "she", "her", "hers", "they", "them",
                 "their", "theirs", "it", "its", "you", "your", "yours"}
# named social roles — an entity even when no proper noun is used
ROLE_WORDS = {"friend", "friends", "brother", "sister", "mother", "father",
              "mom", "dad", "parent", "parents", "wife", "husband", "partner",
              "boss", "manager", "colleague", "cousin", "uncle", "aunt",
              "neighbour", "neighbor", "person", "people", "someone",
              "somebody", "guy", "man", "woman", "boy", "girl", "child",
              "client", "customer", "doctor", "teacher", "student", "team",
              "family", "stranger", "driver", "passenger", "owner", "vendor",
              "landlord", "tenant", "lawyer", "buyer", "seller"}

NEGATION = {"not", "n't", "never", "no", "none", "nothing", "nobody", "nowhere",
            "without", "didn't", "doesn't", "don't", "won't", "wouldn't",
            "can't", "cannot", "couldn't", "hasn't", "haven't", "hadn't",
            "isn't", "aren't", "wasn't", "weren't", "shouldn't", "refused",
            "failed", "declined", "avoided", "omitted", "skipped", "neglected"}

# verbs that move INFORMATION between people
DISCLOSURE_VERBS = {"tell", "told", "telling", "say", "said", "saying",
                    "explain", "explained", "explaining", "mention",
                    "mentioned", "mentioning", "inform", "informed",
                    "informing", "disclose", "disclosed", "share", "shared",
                    "sharing", "warn", "warned", "warning", "announce",
                    "announced", "discuss", "discussed", "clarify",
                    "clarified", "specify", "specified", "reveal", "revealed",
                    "confirm", "confirmed", "notify", "notified", "brief",
                    "briefed", "ask", "asked", "asking"}
# verbs where something of MINE is committed. "use" belongs here — "he used my
# car" is the resource step of his own example — but a resource FACT only fires
# when the thing is actually mine and another party is in the sentence, or
# "I use this app" would read as someone taking from me.
RESOURCE_VERBS = {"use", "used", "using", "uses",
                  "drop", "dropped", "dropping", "drive", "drove", "driving",
                  "lend", "lent", "lending", "borrow", "borrowed", "give",
                  "gave", "giving", "pay", "paid", "paying", "carry",
                  "carried", "carrying", "take", "took", "taking", "bring",
                  "brought", "bringing", "help", "helped", "helping", "cover",
                  "covered", "covering", "host", "hosted", "hosting", "fund",
                  "funded", "sign", "signed", "signing", "guarantee",
                  "guaranteed", "wait", "waited", "waiting", "collect",
                  "collected", "send", "sent", "sending", "book", "booked"}
# verbs of joining in / being committed
PARTICIPATION_VERBS = {"go", "went", "going", "come", "came", "coming",
                       "join", "joined", "joining", "agree", "agreed",
                       "agreeing", "accept", "accepted", "start", "started",
                       "leave", "left", "leaving", "stay", "stayed",
                       "staying", "meet", "met", "meeting", "attend",
                       "attended", "commit", "committed", "move", "moved"}
# a general verb net so ACTION is never empty on an ordinary sentence
COMMON_VERBS = {"do", "did", "does", "doing", "make", "made", "making", "want",
                "wanted", "need", "needed", "think", "thought", "know", "knew",
                "feel", "felt", "see", "saw", "seen", "look", "looked", "find",
                "found", "get", "got", "keep", "kept", "put", "let", "ask",
                "call", "called", "use", "used", "using", "work", "worked",
                "try", "tried", "trying", "seem", "seemed", "happen",
                "happened", "become", "became", "change", "changed", "build",
                "built", "run", "ran", "hold", "held", "turn", "turned",
                "show", "showed", "shown", "expect", "expected", "assume",
                "assumed", "notice", "noticed", "decide", "decided", "choose",
                "chose", "stop", "stopped", "continue", "continued", "is",
                "was", "are", "were", "be", "been", "being", "have", "has",
                "had", "will", "would", "can", "could", "should", "must"}
ALL_VERBS = DISCLOSURE_VERBS | RESOURCE_VERBS | PARTICIPATION_VERBS | COMMON_VERBS

# what a wh-word names, when disclosure is about it
WH_INFO = {"where": "location / destination",
           "when": "time / schedule",
           "why": "reason / purpose",
           "who": "person / who else is involved",
           "whom": "person / who else is involved",
           "what": "thing / plan / content",
           "which": "which option / selection",
           "how": "method / manner",
           "how much": "cost / amount",
           "how many": "quantity",
           "how long": "duration"}
# nouns that name an information object without a wh-word
INFO_NOUNS = {"plan": "plan", "plans": "plan", "reason": "reason / purpose",
              "destination": "location / destination", "address": "location",
              "price": "cost / amount", "cost": "cost / amount",
              "amount": "cost / amount", "time": "time / schedule",
              "date": "time / schedule", "schedule": "time / schedule",
              "detail": "detail", "details": "detail", "truth": "the truth",
              "situation": "the full situation", "context": "context",
              "terms": "terms / conditions", "condition": "terms / conditions",
              "conditions": "terms / conditions", "risk": "risk",
              "risks": "risk", "problem": "problem", "issue": "problem",
              "name": "identity", "identity": "identity",
              "purpose": "reason / purpose", "intention": "intent",
              "agreement": "agreement", "deal": "agreement"}

EXPECT_WORDS = {"should", "supposed", "expected", "promised", "meant",
                "assumed", "normally", "usually", "always", "ought",
                "agreed", "said he would", "said she would", "was going to"}
TIME_BEFORE = {"before", "beforehand", "in advance", "first", "already",
               "prior", "earlier", "ahead", "upfront", "up front",
               "by the time", "until"}
TIME_AFTER = {"after", "then", "later", "afterwards", "afterward",
              "eventually", "finally", "in the end", "once"}
REPEAT_WORDS = {"again", "always", "every time", "each time", "keeps",
                "keeps doing", "repeatedly", "constantly", "usually",
                "often", "another time", "once more", "still", "never stops",
                "second time", "third time", "as usual", "same thing"}
UNCERTAIN_WORDS = {"maybe", "might", "may", "perhaps", "possibly", "seems",
                   "seemed", "i think", "i guess", "not sure", "unsure",
                   "probably", "apparently", "somehow", "kind of", "sort of",
                   "i feel like", "unclear", "confused", "don't know"}
# HIS feeling words — clues only. The machine never concludes which he felt.
EMOTION_CLUES = {"uncomfortable", "uneasy", "angry", "upset", "hurt", "used",
                 "tired", "drained", "annoyed", "irritated", "frustrated",
                 "sad", "afraid", "scared", "anxious", "worried", "betrayed",
                 "disrespected", "ignored", "small", "guilty", "ashamed",
                 "resentful", "bitter", "disappointed", "let down", "unsafe",
                 "trapped", "stuck", "helpless", "lonely", "unseen",
                 "taken for granted", "walked over", "distrust", "suspicious"}
INTENT_CLUES = {"wanted", "trying", "so that", "in order", "because",
                "to get", "to make", "purpose", "point was", "deliberately",
                "on purpose", "intentionally", "knew", "planned", "plotted",
                "used me", "using me", "benefit", "gain", "advantage"}

# ---------------------------------------------------------------------------
# STRUCTURAL FACTS — the content-free vocabulary repetition is measured in.
# The friend example repeats on these, never on "car" or "drop".
F_DISCLOSURE_WITHHELD = "disclosure:withheld"
F_DISCLOSURE_GIVEN = "disclosure:given"
F_RESOURCE_REQUESTED = "resource:requested"
F_RESOURCE_USED = "resource:used"
F_PARTICIPATION_BEFORE = "participation:before_disclosure"
F_THIRD_PARTY = "third_party:introduced"
F_AGREEMENT_ABSENT = "agreement:absent"
F_EXPECTATION_BROKEN = "expectation:broken"
F_ASYMMETRY_INFO = "asymmetry:information"
F_BENEFIT_OTHER = "benefit:other_obtains_result"
F_REPEAT_MARKED = "repeat:marked_by_him"
F_UNCERTAIN = "state:uncertain"
F_SELF_AFFECTED = "self:affected"
# from HIS correction of "left" and "nothing" (senses.py) — a return has
# dimensions, and what REMAINS is not the same as what departed
F_RETURN_RESIDUAL = "return:residual"
F_RETURN_MATERIAL_ABSENT = "return:material_absent"
F_RETURN_EMOTIONAL = "return:emotional"
F_GIVES_EFFORT = "gives:effort"
F_DUTY_CONTINUES = "duty:continues"
F_MEMORY_WEIGHTED = "memory:emotionally_weighted"

# facts that carry a RELATION between people — a repeat needs at least one of
# these, or two sentences about the same topic would look like a pattern.
CORE_RELATION_FACTS = frozenset({
    F_DISCLOSURE_WITHHELD, F_RESOURCE_REQUESTED, F_RESOURCE_USED,
    F_PARTICIPATION_BEFORE, F_THIRD_PARTY, F_AGREEMENT_ABSENT,
    F_EXPECTATION_BROKEN, F_ASYMMETRY_INFO, F_BENEFIT_OTHER,
    F_RETURN_RESIDUAL, F_RETURN_MATERIAL_ABSENT, F_RETURN_EMOTIONAL,
    F_GIVES_EFFORT, F_DUTY_CONTINUES})

# what a structure CAN produce in a person. Held open — never chosen.
EFFECTS_BY_FACT = {
    F_DISCLOSURE_WITHHELD: ["uncertainty", "confusion", "loss of control",
                            "distrust"],
    F_ASYMMETRY_INFO: ["loss of autonomy", "feeling managed"],
    F_PARTICIPATION_BEFORE: ["feeling used", "irritation", "loss of control"],
    F_RESOURCE_USED: ["feeling used", "resentment"],
    F_RESOURCE_REQUESTED: ["obligation", "pressure"],
    F_THIRD_PARTY: ["exposure", "unease with a stranger", "burden"],
    F_AGREEMENT_ABSENT: ["boundary crossed", "surprise"],
    F_EXPECTATION_BROKEN: ["disappointment", "distrust"],
    F_BENEFIT_OTHER: ["feeling used", "one-sidedness"],
    F_REPEAT_MARKED: ["accumulated tiredness", "wearing down"],
    # his teaching: what remains is emotional, and it counts either way
    F_RETURN_RESIDUAL: ["meaning", "what remains after everything"],
    F_RETURN_MATERIAL_ABSENT: ["unrewarded effort", "tiredness"],
    F_RETURN_EMOTIONAL: ["attachment", "meaning", "emotional weight"],
    F_GIVES_EFFORT: ["carrying it", "cost of care"],
    F_DUTY_CONTINUES: ["responsibility that does not end", "weight"],
}

# what a structure MIGHT mean — every reading kept, none picked.
INTERPRETATIONS_BY_FACT = {
    F_DISCLOSURE_WITHHELD: ["poor communication", "assumed familiarity",
                            "deliberate withholding",
                            "he did not know either"],
    F_PARTICIPATION_BEFORE: ["convenience-driven behavior",
                             "instrumental use of relationship",
                             "thoughtlessness under time pressure"],
    F_RESOURCE_USED: ["instrumental use of relationship",
                      "normal reciprocity in his culture",
                      "he expects to reciprocate later"],
    F_THIRD_PARTY: ["assumed familiarity", "disregard for your comfort",
                    "practical necessity"],
    F_AGREEMENT_ABSENT: ["assumed consent", "disregard for agreement",
                         "informality between friends"],
    F_EXPECTATION_BROKEN: ["carelessness", "different expectations",
                           "deliberate withholding"],
    F_BENEFIT_OTHER: ["one-sided benefit", "he does not see the imbalance"],
}

_WORD = re.compile(r"[a-z']+")


def _words(text: str) -> list[str]:
    return _WORD.findall((text or "").lower())


def _has(text_l: str, phrases: set[str]) -> list[str]:
    """Which multi-word or single-word markers are present, in text order."""
    found = []
    for p in phrases:
        if " " in p:
            if p in text_l:
                found.append(p)
        else:
            if re.search(r"\b" + re.escape(p) + r"\b", text_l):
                found.append(p)
    return sorted(set(found), key=lambda p: text_l.find(p))


def split_sentences(text: str) -> list[str]:
    """One micro-sequence per sentence — so the split has to be real."""
    t = (text or "").strip()
    if not t:
        return []
    parts = re.split(r"(?<=[.!?])\s+|\n+", t)
    out = [p.strip() for p in parts if p.strip()]
    return out or [t]


def _entities(sentence: str) -> list[dict]:
    """Who is in this. Self and other kept apart — the relation needs both."""
    ws = _words(sentence)
    ents: list[dict] = []
    seen = set()

    def add(surface: str, side: str, kind: str) -> None:
        key = (surface.lower(), side)
        if key not in seen:
            seen.add(key)
            ents.append({"surface": surface, "side": side, "kind": kind})

    for w in ws:
        if w in PRONOUN_SELF:
            add(w, "self", "pronoun")
        elif w in PRONOUN_OTHER:
            add(w, "other", "pronoun")
        elif w in ROLE_WORDS:
            add(w, "other", "role")
    # proper nouns: capitalised and not the first word of the sentence
    toks = re.findall(r"\b[A-Z][a-z]{1,}\b", sentence)
    first = (sentence.strip().split() or [""])[0].strip(".,!?")
    for t in toks:
        if t != first:
            add(t, "other", "name")
    return ents


def _actions(sentence: str) -> list[dict]:
    """Verbs, with the class that decides what the sentence DOES."""
    acts = []
    for w in _words(sentence):
        classes = []
        if w in DISCLOSURE_VERBS:
            classes.append("disclosure")
        if w in RESOURCE_VERBS:
            classes.append("resource")
        if w in PARTICIPATION_VERBS:
            classes.append("participation")
        if not classes and w in COMMON_VERBS:
            classes.append("general")
        if classes:
            acts.append({"verb": w, "classes": classes})
    return acts


def _information_object(sentence: str) -> tuple[str, str]:
    """What information is in play, and how it was named."""
    low = sentence.lower()
    for phrase in ("how much", "how many", "how long"):
        if phrase in low:
            return WH_INFO[phrase], phrase
    for wh, label in WH_INFO.items():
        if " " in wh:
            continue
        if re.search(r"\b" + wh + r"\b", low):
            return label, wh
    for noun, label in INFO_NOUNS.items():
        if re.search(r"\b" + noun + r"\b", low):
            return label, noun
    return "", ""


def _negation(sentence: str) -> list[str]:
    low = sentence.lower()
    hits = [n for n in NEGATION if n != "n't"
            and re.search(r"\b" + re.escape(n) + r"\b", low)]
    if re.search(r"n't\b", low):
        hits.append("n't")
    return sorted(set(hits), key=lambda n: low.find(n.replace("n't", "n't")))


def decompose(sentence: str, ask_id: str = "", index: int = 0,
              context: dict | None = None,
              sense_entries: list[dict] | None = None) -> dict:
    """One sentence → one micro-sequence, in HIS field names.

    CONTEXT is one of his named decomposition inputs, and it is load-bearing.
    His own S3 — "Friend again does not explain the full plan beforehand" —
    names no "me" at all, yet it is plainly about him. Without carrying the
    established participants forward, that sentence loses its relation and
    drops out of the arrangement it belongs to. Anything inherited is MARKED as
    inherited, never presented as if the sentence said it.

    Nothing here guesses intent and nothing here picks a feeling. Both are
    returned as open sets with a stated reason."""
    low = sentence.lower()
    # HIS CORRECTIONS TO THE PARSE, applied before anything is concluded.
    # "left" is not departure if he has said it means what REMAINS. Both
    # readings are carried so the screen can show what the machine would have
    # thought — the raw sentence is never altered.
    fired: list[dict] = []
    blocked: set[str] = set()
    forced_facts: set[str] = set()
    if sense_entries:
        from . import senses as _senses
        fired = _senses.applies_to(sentence, sense_entries)
        for e in fired:
            blocked.update(e.get("blocks_classes", []) or [])
            forced_facts.update(e.get("adds_facts", []) or [])
    ents = _entities(sentence)
    inherited: list[dict] = []
    if context:
        sides_here = {e["side"] for e in ents}
        # a sentence about someone, with the speaker already established
        if "other" in sides_here and "self" not in sides_here \
                and context.get("self_established"):
            inherited.append({"surface": context.get("self_surface", "me"),
                              "side": "self", "kind": "inherited from context"})
        # a sentence with only the speaker, where the other party is established
        if "self" in sides_here and "other" not in sides_here \
                and context.get("other_surface"):
            inherited.append({"surface": context["other_surface"],
                              "side": "other", "kind": "inherited from context"})
        ents = ents + inherited
    acts = _actions(sentence)
    if blocked:                      # his sense removes a wrong verb class
        for a in acts:
            kept = [c for c in a["classes"] if c not in blocked]
            a["blocked_by_his_sense"] = [c for c in a["classes"]
                                         if c in blocked]
            a["classes"] = kept or ["general"]
    neg = _negation(sentence)
    info_obj, info_named_by = _information_object(sentence)

    classes = {c for a in acts for c in a["classes"]}
    sides = {e["side"] for e in ents}
    has_self, has_other = "self" in sides, "other" in sides

    time_before = _has(low, TIME_BEFORE)
    time_after = _has(low, TIME_AFTER)
    repeats = _has(low, REPEAT_WORDS)
    uncertain = _has(low, UNCERTAIN_WORDS)
    emo_clues = _has(low, EMOTION_CLUES)
    int_clues = _has(low, INTENT_CLUES)
    expect_marks = _has(low, EXPECT_WORDS)

    # --- the structural facts (content-free) ------------------------------
    facts: list[str] = []
    disclosure = "disclosure" in classes
    withheld = disclosure and bool(neg)
    if withheld:
        facts.append(F_DISCLOSURE_WITHHELD)
    elif disclosure:
        facts.append(F_DISCLOSURE_GIVEN)
    # a resource fact needs another party AND the thing to be mine — otherwise
    # "I use this app" would read as someone taking something from me
    mine = bool(re.search(r"\b(my|mine|our|ours)\b", low)) or has_self
    if "resource" in classes and has_other and mine:
        asked = bool(re.search(r"\b(ask|asked|asks|wants?|wanted|needs?|needed|"
                               r"can you|could you|will you|would you|"
                               r"told me to|wanted me to)\b", low))
        if asked:
            facts.append(F_RESOURCE_REQUESTED)
        if not neg or not asked:
            facts.append(F_RESOURCE_USED)
    if "participation" in classes and (withheld or info_obj) and not disclosure:
        facts.append(F_PARTICIPATION_BEFORE)
    if withheld and "participation" in classes:
        facts.append(F_PARTICIPATION_BEFORE)
    # a third person put into my situation
    other_names = [e for e in ents if e["side"] == "other"]
    _tp = (r"\b(another|someone|stranger|third|with me|in my|brought|bring)\b"
           if "participation" in blocked      # his sense killed the departure
           else r"\b(left|leave|leaving|another|someone|stranger|third|"
                r"with me|in my|brought|bring)\b")
    if len(other_names) >= 2 and re.search(_tp, low):
        facts.append(F_THIRD_PARTY)
    if re.search(r"\b(without (my )?(asking|permission|consent|agreement)|"
                 r"never agreed|didn'?t agree|no agreement|without telling)\b", low):
        facts.append(F_AGREEMENT_ABSENT)
    if expect_marks and neg:
        facts.append(F_EXPECTATION_BROKEN)
    if withheld and has_self and has_other:
        facts.append(F_ASYMMETRY_INFO)
    if ("resource" in classes or F_PARTICIPATION_BEFORE in facts) and has_other:
        facts.append(F_BENEFIT_OTHER)
    if repeats:
        facts.append(F_REPEAT_MARKED)
    if uncertain:
        facts.append(F_UNCERTAIN)
    if has_self and (withheld or "resource" in classes or emo_clues):
        facts.append(F_SELF_AFFECTED)
    # structure his teaching adds that no lexicon could have found
    if re.search(r"\b(work\w*|car\w*|effort|time|protect\w*|give|gave|"
                 r"giving|look after|raised|support\w*)\b", low) and has_other:
        facts.append(F_GIVES_EFFORT)
    if re.search(r"\b(keep them safe|keep them alive|still|continu\w*|"
                 r"responsib\w*|duty|has to|have to|must)\b", low):
        facts.append(F_DUTY_CONTINUES)
    if re.search(r"\b(memor\w+|moment\w*)\b", low):
        facts.append(F_MEMORY_WEIGHTED)
    facts.extend(forced_facts)       # what HIS senses declare
    facts = sorted(set(facts))

    # --- INFORMATION STATE ------------------------------------------------
    if withheld:
        info_state = {"known_to_other": "maybe — not stated in this event",
                      "known_to_self": "false"}
    elif disclosure:
        info_state = {"known_to_other": "true", "known_to_self": "true"}
    elif info_obj:
        info_state = {"known_to_other": "unknown",
                      "known_to_self": "unknown from this event"}
    else:
        info_state = {}

    # --- EXPECTED vs ACTUAL, and the difference ---------------------------
    if withheld and info_obj:
        expected = f"{info_obj} disclosed before participation"
        actual = "not supplied"
    elif expect_marks and neg:
        expected = "what the marker '" + expect_marks[0] + "' names"
        actual = "did not happen"
    elif info_obj and disclosure:
        expected = f"{info_obj} disclosed"
        actual = "supplied"
    else:
        expected, actual = "", ""
    diff = (f"expected {expected} ≠ received {actual}"
            if expected and actual and actual != "supplied" else "")

    # --- TEMPORAL RELATION -------------------------------------------------
    if withheld and ("participation" in classes or "resource" in classes):
        temporal = "request / action preceded disclosure"
    elif time_before and time_after:
        temporal = "both a before and an after are marked: " + \
                   ", ".join(time_before + time_after)
    elif time_before:
        temporal = "marked as before: " + ", ".join(time_before)
    elif time_after:
        temporal = "marked as after: " + ", ".join(time_after)
    else:
        temporal = "no order marked in this sentence"

    # --- DEPENDENCY --------------------------------------------------------
    if withheld and ("participation" in classes or "resource" in classes):
        dependency = ("an informed decision by me depended on information "
                      "I did not have")
    elif "resource" in classes and has_other:
        dependency = "something of mine was depended on by another"
    elif info_obj and withheld:
        dependency = "my understanding depended on information not supplied"
    else:
        dependency = ""

    # --- POSSIBLE HUMAN EFFECT — open, never chosen ------------------------
    effects: list[str] = []
    for f in facts:
        for e in EFFECTS_BY_FACT.get(f, []):
            if e not in effects:
                effects.append(e)

    # --- POSSIBLE INTERPRETATIONS — open, never chosen --------------------
    interps: list[str] = []
    for f in facts:
        for i in INTERPRETATIONS_BY_FACT.get(f, []):
            if i not in interps:
                interps.append(i)
    if interps:
        interps.append("other / unknown")

    sig = signature(facts, info_obj)
    _rep = __import__("sourceborn.repetition", fromlist=["x"])
    _rr = _rep.read_repetition(sentence)
    if _rr.get("same_action_changed_function"):
        # the first occurrence and the later ones are no longer one address
        sig = _rep.position_signature(sig, _rr["occurrences"][0])
    ms_id = "MS-" + hashlib.sha256(
        (ask_id + "|" + str(index) + "|" + sentence).encode()).hexdigest()[:10]

    return {
        "id": ms_id, "ask": ask_id, "index": index, "raw": sentence,
        # his field names, in his order
        "entities": ents,
        "relation": ([f"{a['surface']} ↔ {b['surface']}"
                      for a in ents if a["side"] == "other"
                      for b in ents if b["side"] == "self"]
                     or ([f"{ents[0]['surface']} ↔ (no self named)"]
                         if ents else [])),
        "actions": acts,
        "negation": neg,
        "information_object": info_obj,
        "information_named_by": info_named_by,
        "information_state": info_state,
        "expected_information": expected,
        "actual_information": actual,
        "temporal_relation": temporal,
        "dependency": dependency,
        "expectation_difference": diff,
        "possible_human_effect": effects,
        "possible_interpretations": interps,
        # RULE 1 — never decided here
        "intent": {
            "status": "UNKNOWN — not directly observed",
            "why": "intent is read from how things were arranged across many "
                   "events, never from one. Clues in this sentence are listed "
                   "but not concluded.",
            "clues": int_clues},
        # RULE 2 — his field, left for him
        "his_feeling": "",
        "emotion_clues": emo_clues,
        "uncertainty": uncertain,
        "repeat_markers": repeats,
        # the addressing used to find prior similar events
        "inherited_from_context": inherited,
        # HIS PRINCIPLE: identical physical action ≠ identical functional role.
        # Content alone made five checks one address; position is the axis that
        # was missing. See repetition.py.
        "repetition_reading": (__import__("sourceborn.repetition",
                                          fromlist=["x"])
                               .read_repetition(sentence)),
        "views": (__import__("sourceborn.repetition", fromlist=["x"])
                  .read_views(sentence)),
        # HIS corrections that fired, with the default reading kept beside his
        "semantic_overrides": fired,
        "return_reading": (__import__("sourceborn.senses", fromlist=["x"])
                           .return_reading(sentence, fired) if fired else {}),
        "memory_reading": (__import__("sourceborn.senses", fromlist=["x"])
                           .memory_reading(sentence, fired) if fired else {}),
        "structural_facts": facts,
        "signature": sig,
        "repetition_link": ("search prior micro-sequences sharing: "
                            + ", ".join(facts)) if facts else
                           "no structural fact to search on",
        "pattern_contribution": _contribution(facts),
        "words": _words(sentence),
    }


def signature(facts: list[str], info_obj: str = "") -> str:
    """The content-free address of an arrangement. Two events with the same
    signature are the same SHAPE — which is what repeats, not the words."""
    core = sorted(f for f in facts if f in CORE_RELATION_FACTS)
    return "|".join(core) or ("noncore:" + "|".join(sorted(facts)) or "empty")


def _contribution(facts: list[str]) -> str:
    """What this event could contribute to a pattern — named from structure."""
    named = []
    if F_DISCLOSURE_WITHHELD in facts:
        named.append("partial-information behaviour")
    if F_PARTICIPATION_BEFORE in facts:
        named.append("commitment-before-context")
    if F_RESOURCE_USED in facts or F_RESOURCE_REQUESTED in facts:
        named.append("resource dependence")
    if F_THIRD_PARTY in facts:
        named.append("boundary displacement")
    if F_AGREEMENT_ABSENT in facts:
        named.append("unilateral expectation")
    if F_EXPECTATION_BROKEN in facts:
        named.append("expectation asymmetry")
    if F_GIVES_EFFORT in facts and F_RETURN_MATERIAL_ABSENT in facts:
        named.append("non-material return")
    if F_RETURN_EMOTIONAL in facts or F_MEMORY_WEIGHTED in facts:
        named.append("emotional accumulation")
    if F_DUTY_CONTINUES in facts:
        named.append("responsibility persistence")
    if F_ASYMMETRY_INFO in facts:
        named.append("information asymmetry")
    return "possible " + " + ".join(named) if named else \
        "no pattern contribution from this sentence alone"


def relates(a: dict, b: dict, min_overlap: int = 2) -> dict:
    """DIFFERENCE + RELATIONSHIP between two micro-sequences.

    A repeat needs `min_overlap` shared structural facts AND at least one of
    them from the core relation set — otherwise two sentences that merely share
    a topic would read as a pattern, which is the false-pattern explosion he
    named."""
    fa, fb = set(a.get("structural_facts", [])), set(b.get("structural_facts", []))
    shared = sorted(fa & fb)
    core = sorted(set(shared) & CORE_RELATION_FACTS)
    same_shape = len(shared) >= min_overlap and bool(core)
    return {"shared": shared, "core_shared": core,
            "only_in_a": sorted(fa - fb), "only_in_b": sorted(fb - fa),
            "same_signature": a.get("signature") == b.get("signature"),
            "repeat": same_shape,
            "why": ("same arrangement: " + ", ".join(core)) if same_shape
                   else ("shares " + str(len(shared)) + " fact(s), "
                         + ("none relational" if not core else
                            "fewer than " + str(min_overlap))
                         + " — not a repeat")}


def decompose_all(text: str, ask_id: str = "",
                  context: dict | None = None,
                  sense_entries: list[dict] | None = None) -> list[dict]:
    """Every sentence in an ask becomes its own micro-sequence, with the
    participants carried forward as each sentence establishes them.

    `context` may also come from OUTSIDE the ask — the thread's history — so a
    sentence in a long conversation does not lose who it is about."""
    ctx = dict(context or {})
    out = []
    for i, s in enumerate(split_sentences(text)):
        m = decompose(s, ask_id, i, ctx, sense_entries)
        out.append(m)
        for e in m["entities"]:
            if e["kind"] == "inherited from context":
                continue
            if e["side"] == "self":
                ctx["self_established"] = True
                ctx.setdefault("self_surface", e["surface"])
            elif e["side"] == "other":
                ctx.setdefault("other_surface", e["surface"])
    return out


def context_from(seqs: list[dict]) -> dict:
    """The participants a prior stretch of conversation established — so the
    next ask does not start blind."""
    ctx: dict = {}
    for m in seqs:
        for e in m.get("entities", []):
            if e.get("kind") == "inherited from context":
                continue
            if e["side"] == "self":
                ctx["self_established"] = True
                ctx.setdefault("self_surface", e["surface"])
            elif e["side"] == "other":
                ctx.setdefault("other_surface", e["surface"])
    return ctx
