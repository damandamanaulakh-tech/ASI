"""STAGE 18 — MATURITY UPDATE, and the WEAKEN his stage 19 was missing.

His instruction on this build: *it should must have full explanation not just
definition n placeholders.* So this file explains the mechanism, and every value
it returns carries the reasoning that produced it. There is no bare score
anywhere, and there is no function here that only names a thing.

────────────────────────────────────────────────────────────────────────────
WHY STAGE 18 HAD TO EXIST, IN THE SYSTEM'S OWN TERMS
────────────────────────────────────────────────────────────────────────────

Before it, a candidate had exactly two possible fates. Stage 17 could kill it —
its falsifier was met, or counterexamples reached support — or it survived
untouched. Nothing in between could happen to it. That produced two failures:

    a candidate that SURVIVED a real test could not get stronger.
    Ten confirmed predictions left it exactly where one did.

    a candidate that was DOUBTED but not refuted could not get weaker.
    Evidence that should have cost it something cost it nothing.

His own stage 19 names four outcomes — RETAIN / WEAKEN / REJECT / UNKNOWN — and
only three of them existed. WEAKEN had no implementation, which is precisely the
missing middle: the verdict for evidence that damages a reading without ending
it. Stage 18 is what makes WEAKEN possible, because you cannot weaken something
that has no strength to lose.

────────────────────────────────────────────────────────────────────────────
WHY IT IS NOT A SCORE
────────────────────────────────────────────────────────────────────────────

His ASI0001 workbook already showed what a bare number does: RANK was computed
from a column of zeros, so the dashboard reported "K001 Lawgiver" as the leading
hypothesis with a score of 0. He refused the bare 7.8/10 in the tablet transcript
for the same reason, and the rule that came out of it is on the record:

    MATCH SCORE != EPISTEMIC CONFIDENCE

So maturity here is **a named state plus the evidence that put it there**, never
a number on its own. A state you cannot argue with is a state you cannot correct,
and every state below can be argued with because it names what moved it.

────────────────────────────────────────────────────────────────────────────
THE SIX STATES, AND WHAT MOVES BETWEEN THEM
────────────────────────────────────────────────────────────────────────────

    UNTESTED     nothing has been checked. NOT a weak state — an unmeasured one.
                 "Nobody looked" is not "it held", which is already the rule in
                 the survivor stage and is repeated here so the two agree.

    HELD         evidence arrived on both sides and neither settled it. This is
                 a legitimate resting place, not a failure: his own gate says
                 OPEN/HOLD is valid.

    SUPPORTED    at least one DISCRIMINATING prediction was confirmed. The word
                 discriminating is load-bearing — a confirmed prediction that
                 every rival meaning also makes moves nothing, because it did not
                 separate this reading from any other.

    STRONG       two or more discriminating confirmations, from predictions of
                 different classes. Two confirmations of the same class are one
                 kind of looking done twice.

    WEAKENED     a discriminating prediction was refuted, or counterexamples
                 arrived without reaching support. The reading is damaged and
                 still standing. This is the state that did not exist.

    KILLED       stage 17's verdict, carried through unchanged. Maturity does not
                 get to overrule the falsifier.

────────────────────────────────────────────────────────────────────────────
HOW IT MOVES: FOUR INPUTS, EACH WITH A STATED REASON
────────────────────────────────────────────────────────────────────────────

  1. CONFIRMED PREDICTIONS   from stage 12. Only discriminating ones count, and
                             distinct classes count more than repeats of one.
  2. REFUTED PREDICTIONS     from stage 12. A refuted discriminating prediction
                             always costs, even when others were confirmed.
  3. COUNTEREXAMPLES         from stage 17's ledger. Below support they weaken;
                             at or above support they kill, and that is 17's
                             call, not 18's.
  4. RECURRENCE              how many separate sequences the same shape appeared
                             in. His rule 6: one interesting event is not a
                             pattern. Recurrence can raise a reading to STRONG
                             that evidence alone left at SUPPORTED.

DECAY, AND WHY IT IS NOT TIME-BASED

An obvious way to make maturity move is to let it fade with age. This does not,
and the reason matters: nothing in his system measures time, and a reading does
not become less true by being old. What DOES cost a reading is being repeatedly
looked for and not found. So decay here is **checks without confirmation** — if
a reading has been tested many times and never confirmed a discriminating
prediction, it drifts toward WEAKENED. Age alone does nothing.

────────────────────────────────────────────────────────────────────────────
NOTHING IS OVERWRITTEN — HIS NO-REOPEN RULE, ENFORCED
────────────────────────────────────────────────────────────────────────────

An update does not mutate a maturity. It APPENDS a new reading that references
the one before it, and `history()` returns the whole chain. That is his sequence
protocol applied to a value rather than to a sequence: a later reading references
the closed one, it never edits it. So a maturity is not a field — it is a ledger
of readings, and the current state is simply its last row.
"""

from __future__ import annotations

UNTESTED = "UNTESTED"
HELD = "HELD"
SUPPORTED = "SUPPORTED"
STRONG = "STRONG"
WEAKENED = "WEAKENED"
KILLED = "KILLED"

STATES = (UNTESTED, HELD, SUPPORTED, STRONG, WEAKENED, KILLED)

# What each state means, in one line, for anything that displays it.
MEANS = {
    UNTESTED: "nothing has been checked. Unmeasured, not weak.",
    HELD: "evidence arrived on both sides and neither settled it. A valid rest.",
    SUPPORTED: "one discriminating prediction was confirmed.",
    STRONG: "two or more discriminating confirmations, of different classes.",
    WEAKENED: "a discriminating prediction was refuted, or counterexamples "
              "arrived without reaching support. Damaged and still standing.",
    KILLED: "stage 17's verdict, carried through. Maturity does not overrule "
            "the falsifier.",
}

# His stage 19, and the mapping is deliberate: WEAKEN is a verdict of its own,
# not a softer REJECT.
RETAIN, WEAKEN, REJECT, UNKNOWN = "RETAIN", "WEAKEN", "REJECT", "UNKNOWN"

VERDICT_OF = {
    UNTESTED: UNKNOWN,
    HELD: UNKNOWN,
    SUPPORTED: RETAIN,
    STRONG: RETAIN,
    WEAKENED: WEAKEN,
    KILLED: REJECT,
}

RECURRENCE_MIN = 2          # his rule 6: one event is not a pattern
DECAY_AFTER = 3             # looked for this many times, never confirmed


def read(confirmed=(), refuted=(), counterexamples: int = 0,
         support: int = 1, sequences_seen: int = 1, checks: int = 0,
         killed: bool = False) -> dict:
    """Compute a maturity FROM ITS INPUTS, and say what each input did.

    `confirmed` and `refuted` are lists of prediction dicts from stage 12 — the
    real ones, carrying `class` and `discriminating`. Passing bare strings works
    too, but they are then treated as non-discriminating, because a prediction
    that cannot tell you whether it discriminates has not told you it does."""

    def cls_of(p):
        return p.get("class") if isinstance(p, dict) else None

    def disc(p):
        return bool(p.get("discriminating")) if isinstance(p, dict) else False

    conf_d = [p for p in confirmed if disc(p)]
    ref_d = [p for p in refuted if disc(p)]
    conf_classes = {cls_of(p) for p in conf_d if cls_of(p)}
    dropped_conf = len(confirmed) - len(conf_d)
    dropped_ref = len(refuted) - len(ref_d)

    why = []
    if killed:
        state = KILLED
        why.append("stage 17 killed it; maturity carries that through unchanged")
    elif ref_d:
        state = WEAKENED
        why.append("%d discriminating prediction(s) were REFUTED — %s. A refuted "
                   "discriminating prediction always costs, even beside "
                   "confirmations."
                   % (len(ref_d), ", ".join(sorted(
                       {cls_of(p) or "?" for p in ref_d}))))
    elif counterexamples and counterexamples < support:
        state = WEAKENED
        why.append("%d counterexample(s) against support %d — below support, so "
                   "stage 17 does not kill it, but it is damaged"
                   % (counterexamples, support))
    elif len(conf_classes) >= 2:
        state = STRONG
        why.append("%d discriminating confirmations across %d different classes "
                   "(%s) — different kinds of looking, not one kind repeated"
                   % (len(conf_d), len(conf_classes),
                      ", ".join(sorted(conf_classes))))
    elif conf_d:
        state = SUPPORTED
        why.append("1 discriminating confirmation (%s). One class of evidence "
                   "is one way of looking." % (", ".join(sorted(conf_classes))))
    elif checks >= DECAY_AFTER:
        state = WEAKENED
        why.append("looked for %d times and never confirmed a discriminating "
                   "prediction. Decay here is checks-without-confirmation, never "
                   "age: a reading does not become less true by being old."
                   % checks)
    elif confirmed or refuted or counterexamples:
        state = HELD
        why.append("evidence arrived but none of it discriminated, so nothing "
                   "was settled either way")
    else:
        state = UNTESTED
        why.append("nothing was checked. Unmeasured, not weak — nobody looked is "
                   "not it held.")

    # recurrence can lift SUPPORTED to STRONG, and says so
    lifted = False
    if state == SUPPORTED and sequences_seen >= RECURRENCE_MIN:
        state = STRONG
        lifted = True
        why.append("raised from SUPPORTED by recurrence: the same shape appeared "
                   "in %d separate sequences (his rule 6 — one interesting event "
                   "is not a pattern)" % sequences_seen)

    if dropped_conf or dropped_ref:
        why.append("%d confirmation(s) and %d refutation(s) were NOT counted "
                   "because they were non-discriminating — a prediction every "
                   "rival meaning also makes separates nothing"
                   % (dropped_conf, dropped_ref))

    return {
        "state": state,
        "means": MEANS[state],
        "verdict": VERDICT_OF[state],
        "why": why,
        "inputs": {
            "confirmed": len(confirmed), "confirmed_discriminating": len(conf_d),
            "confirmed_classes": sorted(conf_classes),
            "refuted": len(refuted), "refuted_discriminating": len(ref_d),
            "counterexamples": counterexamples, "support": support,
            "sequences_seen": sequences_seen, "checks": checks,
            "killed_by_stage_17": killed,
        },
        "raised_by_recurrence": lifted,
        "what_would_move_it_next": _next_move(state, conf_classes,
                                              sequences_seen),
        "is_a_score": False,
        "law": "a named state plus the evidence that put it there. Never a bare "
               "number — MATCH SCORE != EPISTEMIC CONFIDENCE.",
    }


def _next_move(state: str, conf_classes, sequences_seen: int) -> list:
    """What would actually change this reading. Named, so it is actionable."""
    if state == KILLED:
        return ["nothing. Stage 17 settled it, and a killed row keeps its "
                "falsifier and its reason rather than being removed."]
    out = []
    if state == UNTESTED:
        out.append("check any one discriminating prediction — either way, it "
                   "moves off UNTESTED")
    if state in (UNTESTED, HELD, WEAKENED, SUPPORTED):
        out.append("confirm a discriminating prediction of a class not yet "
                   "confirmed (%s already counted)"
                   % (", ".join(sorted(conf_classes)) or "none"))
    if state == SUPPORTED and sequences_seen < RECURRENCE_MIN:
        out.append("find the same shape in %d more sequence(s) — recurrence "
                   "alone would raise it to STRONG"
                   % (RECURRENCE_MIN - sequences_seen))
    if state in (SUPPORTED, STRONG):
        out.append("refute any discriminating prediction and it drops to "
                   "WEAKENED immediately, however many confirmations it holds")
    return out


# ---------------------------------------------------------------------------
# THE LEDGER — a maturity is a chain of readings, never a field that is edited.
# ---------------------------------------------------------------------------

def update(prior: list, **inputs) -> dict:
    """Append a new reading. NOTHING IS OVERWRITTEN.

    `prior` is the chain so far (oldest first). The new reading references the
    last one by index and records the movement, so the history says not only
    what the state is but what it was and why it changed."""
    chain = list(prior or [])
    now = read(**inputs)
    was = chain[-1]["state"] if chain else None
    now["n"] = len(chain) + 1
    now["references"] = len(chain) or None
    now["was"] = was
    if was is None:
        now["movement"] = "first reading"
    elif was == now["state"]:
        now["movement"] = "unchanged — %s, and the reasons are re-stated rather " \
                          "than assumed" % was
    else:
        now["movement"] = "%s -> %s" % (was, now["state"])
    now["overwrote_anything"] = False
    chain.append(now)
    return {
        "current": now, "chain": chain, "readings": len(chain),
        "overwrites": 0,
        "law": "an update appends a reading that references the one before it. "
               "A maturity is a ledger, not a field — his no-reopen rule applied "
               "to a value.",
    }


def history(chain: list) -> dict:
    """The whole life of one reading, with every movement named."""
    ch = list(chain or [])
    moves = [{"n": r["n"], "was": r.get("was"), "now": r["state"],
              "movement": r["movement"], "why": r["why"]} for r in ch]
    return {
        "readings": len(ch),
        "first": ch[0]["state"] if ch else None,
        "current": ch[-1]["state"] if ch else None,
        "verdict": ch[-1]["verdict"] if ch else UNKNOWN,
        "movements": moves,
        "changed": sum(1 for r in ch if r.get("was")
                       and r["was"] != r["state"]),
        "nothing_removed": True,
    }


def verdict(chain_or_state) -> dict:
    """STAGE 19 — RETAIN / WEAKEN / REJECT / UNKNOWN, all four of them.

    This is what stage 19 was missing. Before stage 18 there was no WEAKEN
    because there was no strength to lose; a candidate stood or died. Now the
    middle exists and the verdict is read off the maturity rather than guessed."""
    if isinstance(chain_or_state, list):
        state = chain_or_state[-1]["state"] if chain_or_state else UNTESTED
        why = chain_or_state[-1]["why"] if chain_or_state else []
    elif isinstance(chain_or_state, dict):
        state = chain_or_state.get("state", UNTESTED)
        why = chain_or_state.get("why", [])
    else:
        state = chain_or_state or UNTESTED
        why = []
    v = VERDICT_OF.get(state, UNKNOWN)
    return {
        "state": state, "verdict": v, "why": why,
        "means": MEANS.get(state, ""),
        "all_four": [RETAIN, WEAKEN, REJECT, UNKNOWN],
        "weaken_exists": True,
        "note": {
            RETAIN: "evidence has confirmed something that separated it from "
                    "its rivals. It stands.",
            WEAKEN: "evidence damaged it without ending it. It stands, and it "
                    "stands lower. This verdict had no implementation before "
                    "stage 18.",
            REJECT: "stage 17's falsifier was met. The row is kept with its "
                    "reason; nothing is deleted.",
            UNKNOWN: "nothing has settled it. OPEN/HOLD is a valid result — his "
                     "own gate says so.",
        }[v],
    }


def stats() -> dict:
    return {
        "states": len(STATES),
        "verdicts": 4,
        "weaken_implemented": True,
        "is_a_score": False,
        "decay_is": "checks without confirmation, never age",
        "recurrence_min": RECURRENCE_MIN,
        "decay_after": DECAY_AFTER,
        "overwrites": 0,
        "source": "docs/method/canon/THE_DISCOVERY_LOOP.md",
    }


def annotations() -> list:
    return [
        ("a candidate that survived can now get stronger", "maturity.read"),
        ("a candidate that was doubted can now get weaker", "maturity.read"),
        ("WEAKEN, the verdict stage 19 was missing", "maturity.verdict"),
        ("maturity is a ledger of readings, not a field", "maturity.update"),
        ("decay is checks without confirmation, never age", "maturity.DECAY_AFTER"),
    ]
