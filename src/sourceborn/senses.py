"""USER-DEFINED SEMANTIC CONTEXT — where he corrects the parse itself.

His teaching, 2026-08-13, filed verbatim in
`docs/method/canon/LEFT_AND_NOTHING_HIS_CORRECTION.md`:

    SOURCE WORD: left
    DEFAULT LANGUAGE INTERPRETATION: departure / previous-state
    USER CORRECTION: residual possession / outcome —
        "what remains with the person after everything"
    STATUS: USER-DEFINED SEMANTIC CONTEXT

    SOURCE: "got nothing"
    LITERAL INTERPRETATION: zero return
    USER CLARIFICATION: zero/low tangible return; memories and moments remain

    MEMORY RULE — USER: Good and bad memories both carry emotional
    significance for humans.
    ASI CANDIDATE: Memory significance should be evaluated separately from
    positive/negative valence.

    "This is exactly the type of correction that should create a write-back
     Sequence."

WHAT THIS MODULE IS FOR
  A first linguistic parse is a guess. "left" reads as departure; he means what
  REMAINS. "nothing" reads as zero; he means zero *material* return while the
  emotional return is intact. Without a place for him to correct the parse, the
  machine keeps making the same wrong reading forever and the whole editable
  layer is decoration.

THE RULES IT HOLDS
  * **RAW SOURCE IS NEVER TOUCHED.** An override changes how a word is READ.
    The sentence he wrote stays byte-for-byte what he wrote.
  * **BOTH READINGS ARE KEPT.** Every override records the default reading AND
    his reading, so the screen can show what the machine would have thought.
    Nothing is silently replaced.
  * **NO REOPEN.** Editing an override appends a write-back referencing the
    version it acted on; the prior version is kept whole.
  * **VALENCE IS NOT VALUE.** His rule is enforced as two separate fields, not
    one signed number: `pleasantness ≠ importance`, `pain ≠ worthlessness`.
  * **NO OVERGENERALISING.** He named the danger himself — "A person who gets
    nothing in return is automatically good" is refused, and the refusal is
    recorded on the rule that could have produced it.

Storage:  <root>/senses/senses.json         current, versioned
          <root>/senses/writeback.jsonl     every edit he ever made
"""
from __future__ import annotations

import json
import os
import re

from .models import _now

KINDS = ("word_sense", "return_dimension", "human_rule")
STATUS_USER = "USER-DEFINED SEMANTIC CONTEXT"
STATUS_REVIEW = "REVIEW / USER-CLARIFIED"

# HIS RETURN DIMENSIONS — because "he got nothing" is not one number.
# "Therefore 'nothing' itself must not be interpreted literally without its
#  dimension." — his words.
RETURN_DIMENSIONS = ("material", "practical", "emotional", "relational",
                     "experiential", "identity", "meaning", "memory")

# HIS MEMORY RULE, as two fields that must never be collapsed into one.
MEMORY_VALENCE = ("positive", "negative", "mixed", "painful", "beautiful",
                  "unknown")


def _dir(root: str) -> str:
    d = os.path.join(root, "senses")
    os.makedirs(d, exist_ok=True)
    return d


def _path(root: str) -> str:
    return os.path.join(_dir(root), "senses.json")


def _wb(root: str) -> str:
    return os.path.join(_dir(root), "writeback.jsonl")


def seed() -> list[dict]:
    """His three teachings, in his words, as the first entries. These are HIS,
    not defaults I invented — each carries the status he gave it."""
    return [
        {"id": "SENSE-001", "kind": "word_sense", "word": "left",
         "default_reading": "departure / previous-state — "
                            "departed, died, walked away",
         "his_reading": "residual possession / outcome — what remains with the "
                        "person after all their effort, care, time and "
                        "responsibility",
         "status": STATUS_USER,
         "blocks_classes": ["participation"],
         "adds_facts": ["return:residual"],
         "his_words": "LEFT ≠ departed ≠ died ≠ walked away. "
                      "LEFT = what remains with the person = residual outcome "
                      "= what the person ultimately receives/retains",
         "version": 1, "at": _now(), "history": []},
        {"id": "SENSE-002", "kind": "return_dimension", "word": "nothing",
         "default_reading": "zero return, literally",
         "his_reading": "zero or low MATERIAL return, while the emotional and "
                        "experiential return remains — memories and moments",
         "status": STATUS_USER,
         "blocks_classes": [],
         "adds_facts": ["return:material_absent", "return:emotional"],
         "his_words": '"He got nothing." can simultaneously mean '
                      "material_return = near zero, but "
                      "emotional/experiential_return = memories + moments. "
                      "Therefore 'nothing' itself must not be interpreted "
                      "literally without its dimension.",
         "version": 1, "at": _now(), "history": []},
        {"id": "SENSE-003", "kind": "human_rule", "word": "memory",
         "default_reading": "valence and value are the same axis — a negative "
                            "memory is a low-value memory",
         "his_reading": "memory significance is evaluated SEPARATELY from "
                        "positive/negative valence. Good or bad, memories are "
                        "always emotional count for human.",
         "status": STATUS_REVIEW,
         "blocks_classes": [],
         "adds_facts": ["memory:emotionally_weighted"],
         "his_words": "pleasantness ≠ importance · pain ≠ worthlessness · "
                      "negative emotion ≠ unwanted memory · "
                      "memory value ≠ material value",
         "refuses": "a bad memory may still be significant, and a painful "
                    "memory may still be cherished — so valence must never be "
                    "used as a stand-in for value",
         "version": 1, "at": _now(), "history": []},
        {"id": "SENSE-004", "kind": "human_rule", "word": "good person",
         "default_reading": "a moral label",
         "his_reading": "a behavioural structure: takes responsibility · "
                        "continues contributing · protects others · does not "
                        "measure everything by personal return · their "
                        "retained value may be memories and moments",
         "status": STATUS_REVIEW,
         "blocks_classes": [],
         "adds_facts": ["gives:effort", "duty:continues"],
         "his_words": "So ASI should investigate whether 'good' in your rubric "
                      "contains dimensions such as: care, responsibility, "
                      "sacrifice, continuity, protection, giving, low demand "
                      "for return, emotional attachment, duty.",
         # HE NAMED THIS DANGER HIMSELF — it is recorded as a refusal on the
         # rule, so the rule can never quietly grow into it.
         "refuses": "A person who gets nothing in return is NOT automatically "
                    "good. He called this a dangerous overgeneralization. The "
                    "sentence supports only the subtler reading: a good "
                    "person's reward may sometimes be non-material while "
                    "their responsibility toward loved ones continues.",
         "version": 1, "at": _now(), "history": []},
    ]


def load(root: str) -> list[dict]:
    p = _path(root)
    if not os.path.exists(p):
        return seed()
    try:
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, list) else seed()
    except Exception:
        return seed()


def save(root: str, entries: list[dict]) -> None:
    with open(_path(root), "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def writebacks(root: str, limit: int = 200) -> list[dict]:
    p = _wb(root)
    if not os.path.exists(p):
        return []
    out = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except Exception:
                    continue
    return out[-limit:]


def _next_id(entries: list[dict]) -> str:
    n = 0
    for e in entries:
        try:
            n = max(n, int(str(e.get("id", "")).rsplit("-", 1)[-1]))
        except Exception:
            continue
    return f"SENSE-{n + 1:03d}"


def teach(root: str, word: str, his_reading: str,
          default_reading: str = "", kind: str = "word_sense",
          blocks_classes: list[str] | None = None,
          adds_facts: list[str] | None = None,
          status: str = STATUS_USER, note: str = "",
          refuses: str = "") -> dict:
    """He corrects the parse. NO REOPEN — a new version, prior kept whole, and
    a write-back sequence recording what it acted on."""
    word = (word or "").strip().lower()
    if not word or not str(his_reading).strip():
        return {"error": "a sense needs a word and your reading of it"}
    if kind not in KINDS:
        return {"error": "kind must be one of: " + ", ".join(KINDS)}
    entries = load(root)
    idx = next((i for i, e in enumerate(entries) if e["word"] == word
                and e["kind"] == kind), None)
    if idx is None:
        e = {"id": _next_id(entries), "kind": kind, "word": word,
             "default_reading": str(default_reading or
                                    "(no default recorded)").strip(),
             "his_reading": str(his_reading).strip(),
             "status": status,
             "blocks_classes": list(blocks_classes or []),
             "adds_facts": list(adds_facts or []),
             "his_words": str(note or "").strip(),
             "refuses": str(refuses or "").strip(),
             "version": 1, "at": _now(), "history": []}
        entries.append(e)
        acted_on, new = 0, e
    else:
        cur = entries[idx]
        prior = {k: v for k, v in cur.items() if k != "history"}
        new = dict(cur)
        new["history"] = list(cur.get("history", [])) + [
            {"version": cur.get("version", 1), "at": _now(),
             "snapshot": prior}]
        new["version"] = int(cur.get("version", 1)) + 1
        new["his_reading"] = str(his_reading).strip()
        if default_reading:
            new["default_reading"] = str(default_reading).strip()
        if blocks_classes is not None:
            new["blocks_classes"] = list(blocks_classes)
        if adds_facts is not None:
            new["adds_facts"] = list(adds_facts)
        if note:
            new["his_words"] = str(note).strip()
        if refuses:
            new["refuses"] = str(refuses).strip()
        new["status"] = status
        new["at"] = _now()
        entries[idx] = new
        acted_on = cur.get("version", 1)
    save(root, entries)
    wb = {"at": _now(), "event": "sense_writeback", "id": new["id"],
          "word": word, "kind": kind,
          "acted_on_version": acted_on, "new_version": new["version"],
          "default_reading": new["default_reading"],
          "his_reading": new["his_reading"], "note": str(note or "")[:400],
          "no_reopen": "the prior reading is kept whole in history; this is a "
                       "new sequence referencing it, never a rewrite"}
    with open(_wb(root), "a", encoding="utf-8") as f:
        f.write(json.dumps(wb, ensure_ascii=False) + "\n")
    return {"ok": True, "sense": new, "writeback": wb}


def reject(root: str, sense_id: str, note: str = "") -> dict:
    """He throws one out. It is CLOSED, never deleted — the record of what he
    refused is itself information."""
    entries = load(root)
    idx = next((i for i, e in enumerate(entries) if e["id"] == sense_id), None)
    if idx is None:
        return {"error": "no such sense: " + str(sense_id)}
    cur = entries[idx]
    new = dict(cur)
    new["history"] = list(cur.get("history", [])) + [
        {"version": cur.get("version", 1), "at": _now(),
         "snapshot": {k: v for k, v in cur.items() if k != "history"}}]
    new["version"] = int(cur.get("version", 1)) + 1
    new["status"] = "REJECTED BY HIM"
    new["reject_note"] = str(note or "")[:400]
    entries[idx] = new
    save(root, entries)
    with open(_wb(root), "a", encoding="utf-8") as f:
        f.write(json.dumps({"at": _now(), "event": "sense_rejected",
                            "id": sense_id, "note": str(note or "")[:400],
                            "new_version": new["version"]},
                           ensure_ascii=False) + "\n")
    return {"ok": True, "sense": new}


def active(root: str) -> list[dict]:
    return [e for e in load(root) if e.get("status") != "REJECTED BY HIM"]


def applies_to(sentence: str, entries: list[dict]) -> list[dict]:
    """Which of his corrections fire on this sentence. Both readings are
    returned — the machine's default AND his — so the screen can show what it
    would have thought."""
    low = (sentence or "").lower()
    out = []
    for e in entries:
        w = e.get("word", "")
        if not w:
            continue
        if " " in w:
            hit = w in low
        else:
            # inflections, precisely — "memory" must catch "memories", without
            # a loose prefix match that would also catch unrelated words
            alts = {w, w + "s", w + "es"}
            if w.endswith("y"):
                alts.add(w[:-1] + "ies")
            if w.endswith("e"):
                alts.add(w[:-1] + "ing")
            hit = bool(re.search(r"\b(" + "|".join(
                sorted((re.escape(a) for a in alts), key=len, reverse=True))
                + r")\b", low))
        if hit:
            out.append({"id": e["id"], "word": w, "kind": e["kind"],
                        "default_reading": e.get("default_reading", ""),
                        "his_reading": e.get("his_reading", ""),
                        "status": e.get("status", ""),
                        "his_words": e.get("his_words", ""),
                        "refuses": e.get("refuses", ""),
                        "blocks_classes": e.get("blocks_classes", []),
                        "adds_facts": e.get("adds_facts", []),
                        "version": e.get("version", 1)})
    return out


def return_reading(sentence: str, fired: list[dict]) -> dict:
    """His RETURN dimensions. "He got nothing" is not one number — it is a
    reading per dimension, and the unstated ones say unstated rather than zero.
    """
    facts = {f for e in fired for f in e.get("adds_facts", [])}
    low = (sentence or "").lower()
    dims: dict[str, str] = {d: "not stated" for d in RETURN_DIMENSIONS}
    if "return:material_absent" in facts or re.search(
            r"\b(nothing|no money|unpaid|without pay|no reward|"
            r"got nothing|no return)\b", low):
        dims["material"] = "near zero — and this does NOT mean zero overall"
    if "return:emotional" in facts or re.search(
            r"\b(memor\w+|moment\w*|love|attach\w*|meaning)\b", low):
        dims["emotional"] = "present"
        dims["memory"] = "present"
        dims["experiential"] = "present"
    if "return:residual" in facts:
        dims["meaning"] = "present — what remains after everything"
    if re.search(r"\b(who i am|identity|made me|became)\b", low):
        dims["identity"] = "present"
    if re.search(r"\b(togeth\w*|relationship|bond|belong\w*)\b", low):
        dims["relational"] = "present"
    return {"dimensions": dims,
            "rule": "'nothing' is never read literally without its dimension "
                    "(his correction). An unstated dimension says unstated, "
                    "never zero."}


def memory_reading(sentence: str, fired: list[dict]) -> dict:
    """His memory rule, as TWO fields. Valence is not value."""
    low = (sentence or "").lower()
    if not re.search(r"\b(memor\w+|moment\w*|remember\w*|recall\w*)\b", low):
        return {}
    val = "unknown"
    if re.search(r"\b(good|beautiful|happy|warm|joy\w*)\b", low):
        val = "positive"
    if re.search(r"\b(bad|pain\w*|hurt|sad|loss|grief|hard)\b", low):
        val = "negative" if val == "unknown" else "mixed"
    return {"valence": val,
            "significance": "emotionally weighted regardless of valence",
            "his_rule": "Good or bad, memories are always emotional count "
                        "for human.",
            "never": "valence must NOT be used as a stand-in for value — "
                     "pleasantness ≠ importance, pain ≠ worthlessness",
            "fired_from": [e["id"] for e in fired
                           if e["kind"] == "human_rule"]}


def stats(root: str) -> dict:
    e = load(root)
    return {"senses": len(e),
            "by_kind": {k: sum(1 for x in e if x["kind"] == k) for k in KINDS},
            "user_defined": sum(1 for x in e if x.get("status") == STATUS_USER),
            "review": sum(1 for x in e if x.get("status") == STATUS_REVIEW),
            "rejected": sum(1 for x in e
                            if x.get("status") == "REJECTED BY HIM"),
            "with_refusal": sum(1 for x in e if x.get("refuses")),
            "writebacks": len(writebacks(root, 10 ** 6))}
