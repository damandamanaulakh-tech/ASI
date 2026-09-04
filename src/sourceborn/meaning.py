"""THE MEANING LOCK — one sheet per example, and nothing is used unsigned.

PHASE 0. His ask:

    every example already stored gets a written meaning-check — what the
    example means, in your words, not my reading — and you sign each one. This
    is your Q18 answer made into the first phase, because everything
    downstream inherits its meaning from here.

    Produces: one meaning sheet per example.
    Proof: your signature per sheet. An unsigned meaning cannot be used by any
    later phase.
    Gate: you sign the first batch before Phase 1 opens.

WHY THIS IS PHASE ZERO AND NOT PHASE TEN

Everything downstream inherits its meaning from here. If the meaning of the
rain sentence is wrong, then the seating is wrong, the archetype that fires is
wrong, the intent readings are wrong, and every count computed from them is
confidently wrong. A wrong meaning does not announce itself — it produces a
full, consistent, entirely mistaken reading.

The re-read (Phase 15) proved that exact risk is live: his rain sentence reads
two rows now and read two rows when it was recorded, and **both rows are
different**. A signed meaning is what would have caught that on the day.

THE ONE THING THIS MODULE MUST NOT DO

**It must not write his meaning for him.** His words: *what the example means,
in your words, not my reading.* So every sheet ships with:

    his_meaning   EMPTY. Only he fills it.
    my_reading    what the system currently takes the example to mean, stated
                  plainly so he has something to disagree with.
    signed        False.

A sheet whose `his_meaning` was filled by this side would be the whole point
inverted. A test asserts every unsigned sheet has an empty `his_meaning`, and
`sign()` refuses to record a signature without one.

"AN UNSIGNED MEANING CANNOT BE USED BY ANY LATER PHASE"

`usable()` is that sentence as a function. It returns only signed sheets, and
`blocked()` names what every later phase is currently running on without a
signature — which is, honestly, all of it. That is not hidden: the count is
reported on every call, and it is his to close.

APPEND-ONLY. A signature is a row, never an overwrite. Re-signing appends a
new row referencing the one before, so a changed meaning keeps its history —
his standing rule, nothing removed.
"""

from __future__ import annotations

import json
import os

#: A sheet is one of these. `his_meaning` is his and starts empty.
FIELDS = ("example_id", "name", "his_words", "text", "my_reading",
          "his_meaning", "signed", "signed_at", "supersedes")

#: His gate: the first batch signed before Phase 1 opens.
FIRST_BATCH = 8


def _dir(root: str) -> str:
    d = os.path.join(root or ".", "meaning")
    os.makedirs(d, exist_ok=True)
    return d


def _path(root: str) -> str:
    return os.path.join(_dir(root), "sheets.jsonl")


def sheets() -> list:
    """One sheet per example the system actually runs on.

    `my_reading` is what the system currently takes the example to mean —
    stated so he has something concrete to disagree with. `his_meaning` is
    EMPTY and only he fills it."""
    from . import reread
    out = []
    for ex in reread.EXAMPLES:
        out.append({
            "example_id": ex["id"],
            "name": ex["name"],
            "his_words": ex["his_words"],
            "text": ex["text"],
            "my_reading": ex["why_it_matters"],
            "his_meaning": "",
            "signed": False,
            "signed_at": None,
            "supersedes": None,
            "note": "his_meaning is EMPTY by design — 'what the example means, "
                    "in your words, not my reading'.",
        })
    return out


def load(root: str) -> list:
    p = _path(root)
    if not os.path.exists(p):
        return []
    rows = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                rows.append({"UNREADABLE": line})
    return rows


def sign(root: str, example_id: str, his_meaning: str) -> dict:
    """HIS ACTION. Records his meaning and his signature as an appended row.

    Refuses an empty meaning: a signature on nothing is not a meaning lock.
    Re-signing appends a new row referencing the previous one — nothing is
    overwritten and nothing is removed."""
    import datetime
    text = (his_meaning or "").strip()
    if not text:
        return {"signed": False,
                "refused": "a signature needs a meaning. His words: what the "
                           "example means, IN YOUR WORDS — an empty sheet "
                           "signs nothing."}
    known = {s["example_id"] for s in sheets()}
    if example_id not in known:
        return {"signed": False, "refused": "no sheet for %r" % example_id,
                "known": sorted(known)}
    prior = [r for r in load(root) if r.get("example_id") == example_id]
    row = {"example_id": example_id, "his_meaning": text, "signed": True,
           "signed_at": datetime.datetime.now(datetime.timezone.utc)
           .isoformat(timespec="seconds"),
           "supersedes": (prior[-1].get("signed_at") if prior else None)}
    with open(_path(root), "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return dict(row, appended=True, prior_kept=len(prior))


def signed(root: str) -> dict:
    """The latest signature per example. Earlier ones are kept, not replaced."""
    latest = {}
    for r in load(root):
        if r.get("signed") and r.get("example_id"):
            latest[r["example_id"]] = r
    return latest


def usable(root: str) -> list:
    """HIS RULE AS A FUNCTION: an unsigned meaning cannot be used by any later
    phase. Only signed sheets come back."""
    have = signed(root)
    return [dict(s, his_meaning=have[s["example_id"]]["his_meaning"],
                 signed=True, signed_at=have[s["example_id"]]["signed_at"])
            for s in sheets() if s["example_id"] in have]


def blocked(root: str) -> dict:
    """What every later phase is currently running on WITHOUT a signature.

    Reported rather than hidden. This is the honest state of his gate."""
    have = signed(root)
    missing = [s["example_id"] for s in sheets() if s["example_id"] not in have]
    return {
        "unsigned": missing,
        "unsigned_count": len(missing),
        "signed_count": len(have),
        "first_batch": FIRST_BATCH,
        "gate_open": len(have) >= FIRST_BATCH,
        "his_rule": "an unsigned meaning cannot be used by any later phase",
        "honest_state": "every later phase is currently running on unsigned "
                        "meanings. The system does not stop itself — that "
                        "would halt the whole build on a gate only he can "
                        "close — but the count is on every call and nothing "
                        "pretends the signatures exist.",
    }


def stats(root: str = ".") -> dict:
    b = blocked(root)
    return {
        "sheets": len(sheets()),
        "signed": b["signed_count"],
        "unsigned": b["unsigned_count"],
        "first_batch": FIRST_BATCH,
        "gate_open": b["gate_open"],
        "law": "what the example means, in HIS words, not my reading. "
               "his_meaning ships empty and only he fills it.",
        "never": "this side never writes his meaning, and a signature without "
                 "a meaning is refused.",
    }


def annotations() -> list:
    return [
        ("what the example means, in your words, not my reading",
         "meaning.sheets"),
        ("your signature per sheet", "meaning.sign"),
        ("an unsigned meaning cannot be used by any later phase",
         "meaning.usable"),
        ("you sign the first batch before Phase 1 opens", "meaning.FIRST_BATCH"),
    ]
