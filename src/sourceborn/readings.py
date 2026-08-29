"""THE NINE READINGS — one event, every intent type it could carry.

PHASE 12. His ask, and the proof he named for it:

    IT-01 through IT-09, all approved, joined to the eight adopted types as
    you ruled, with the archetype property carrying its own registry.

    Proof: a live run on "a man is stealing the money" producing all nine
    readings where it produces zero today.

WHAT A READING IS, AND WHY NINE OF THEM

His own demonstration is the whole design. A man is taking money. That single
visible act carries four reasons he named himself — **thief · opportunity ·
habit · saving a life** — and the hand moves identically in all four. The act
cannot say which.

His motto is that *everything happening is a event, and all events have
intent*. It does NOT say the event announces its intent. So the honest output
of an event is not one intent — it is **every intent the event could carry, all
standing, none chosen**, each with what would separate it from the others.

That is a READING: the intent type, what this specific event would mean under
it, **what would confirm it**, **what would refute it**, and the row in his own
bank the reading rests on. Nine types, so nine readings.

WHY THIS IS NOT A LIST OF LABELS

Before this, an ask reached intent TYPE IDS — `["IT-01", "IT-02", ...]` — which
is a list of names and settles nothing. A reading is testable: it names the
evidence that would decide it. His own falsifier law from the intent ledger
applies unchanged — a candidate that names nothing that would flip it is not a
candidate, it is an opinion.

FOUR OF THE NINE ARE HIS OWN FROM THIS VERY EXAMPLE. `THIEF` is IT-01
disposition, `OPPORTUNITY` is IT-02 affordance, `HABIT` is IT-03 automaticity,
`SAVING A LIFE` is IT-04 override by a higher claim. The other five come from
his other worked examples — recovery from the dice game, role-binding from
Yudhishthira, impatience from the golden calf, fruit-focus from the Gita,
permission-waiting from his study sequence.

NOTHING IS CHOSEN. `chosen` is None on every run, and it is None by
construction: there is no code path that picks one. Two surviving candidates
HALT rather than being blended — his standing rule — and nine surviving
candidates are nine.
"""

from __future__ import annotations

#: The nine, each with the discriminator that separates it from its neighbours,
#: the evidence that would confirm it, the evidence that would refute it, and
#: the rows in his own bank the reading rests on. The verbs are what the
#: reading says about an ACT — filled in per event at read time.
TYPES = (
    {
        "id": "IT-01",
        "name": "DISPOSITION",
        "means": "the act flows from what the actor IS",
        "step": 1,
        "step_name": "GROUND",
        "his_example": "THIEF — the man takes money because taking is what he "
                       "does",
        "reads_as": "%s is read as flowing from the kind of person the actor is",
        "confirmed_by": "the same act by the same actor across unrelated "
                        "situations, with no shared trigger",
        "refuted_by": "a first occurrence, or a situation that supplies its "
                      "own sufficient reason",
        "rests_on": [("SB-HFR-P2672", "Dominance (trait)", "CON-067"),
                     ("SB-HFR-P2648", "Assertiveness", "CON-067")],
        "refuses": "an act is not a character. THIEF is a conclusion; taking "
                   "money is the observation.",
    },
    {
        "id": "IT-02",
        "name": "AFFORDANCE",
        "means": "the moment offered it",
        "step": 2,
        "step_name": "PRESSURE",
        "his_example": "OPPORTUNITY — the till was open and nobody was looking",
        "reads_as": "%s is read as a situation opening and the opening being "
                    "taken",
        "confirmed_by": "an opening that was present and is not usually "
                        "present; the act tracking the opening rather than the "
                        "actor",
        "refuted_by": "the act occurring where no opening existed, or "
                      "persisting after the opening closed",
        "rests_on": [("SB-HFR-P1132", "Temptation resistance", "CON-029"),
                     ("SB-HFR-P2530", "Approach motive", "CON-064")],
        "refuses": "an opening is not a cause. Most people meet the same "
                   "opening and do not act.",
    },
    {
        "id": "IT-03",
        "name": "AUTOMATICITY",
        "means": "ran with no live reason at all",
        "step": 3,
        "step_name": "USE",
        "his_example": "HABIT — the hand moved before any reason formed",
        "reads_as": "%s is read as running with no reason live at the moment — "
                    "the sequence ran itself",
        "confirmed_by": "repetition without variation, insensitivity to the "
                        "stakes, and no reported deliberation",
        "refuted_by": "the act being adjusted to the situation, or the actor "
                      "being able to say why at the time",
        "rests_on": [("SB-HFR-P2854", "Moral-intuition (fast)", "CON-072"),
                     ("SB-HFR-P1874", "Intuitive (System-1) judgment", "CON-047")],
        "refuses": "no live reason is not the same as no reason. A habit had a "
                   "reason once.",
    },
    {
        "id": "IT-04",
        "name": "OVERRIDE BY A HIGHER CLAIM",
        "means": "a larger obligation outranked the rule",
        "step": 7,
        "step_name": "HALT",
        "his_example": "SAVING A LIFE — the child was dying and the rule lost",
        "reads_as": "%s is read as something the actor holds higher outranking "
                    "the rule that was broken",
        "confirmed_by": "a named higher claim present at the time, the act "
                        "being the minimum that serves it, and the rule being "
                        "kept everywhere the claim is absent",
        "refuted_by": "the higher claim appearing only afterwards as an "
                      "explanation, or the act exceeding what the claim needs",
        "rests_on": [("SB-HFR-P2869", "Moral-dilemma resolution", "CON-072"),
                     ("SB-HFR-P2870", "Utilitarian-vs-deontological weighting",
                      "CON-072"),
                     ("SB-HFR-P2547", "Survival motive", "CON-064")],
        "refuses": "a stated higher claim is not a verified one. His own rule: "
                   "saying a reason is not verifying it.",
    },
    {
        "id": "IT-05",
        "name": "RECOVERY",
        "means": "acting to restore what is already lost",
        "step": 8,
        "step_name": "LOOP",
        "his_example": "the dice game — staking more because the loss is "
                       "already there; 'betting is worst, u can loose ur pride "
                       "too'",
        "reads_as": "%s is read as an attempt to get back to a state that "
                    "existed before a loss",
        "confirmed_by": "a loss preceding the act, the act aiming at the "
                        "pre-loss state, and the stake rising as the loss "
                        "deepens",
        "refuted_by": "nothing lost beforehand, or the act being indifferent "
                      "to whether the loss is repaired",
        "rests_on": [("SB-HFR-P1873", "Sunk-cost sensitivity", "CON-047"),
                     ("SB-HFR-P2517", "Commitment escalation risk", "CON-063"),
                     ("SB-HFR-P2724", "Agency-restoration", "CON-068")],
        "refuses": "never read the rising stake as confidence.",
    },
    {
        "id": "IT-06",
        "name": "ROLE / VIRTUE BINDING",
        "means": "compelled by the actor's own standing",
        "step": 6,
        "step_name": "NAMING",
        "his_example": "Yudhishthira — 'being righteousness and adherence to "
                       "truth dosent make u great all the time'",
        "reads_as": "%s is read as compelled, because refusing would have "
                    "contradicted who the actor is held to be",
        "confirmed_by": "the actor being known for the quality that produced "
                        "the act, a witness whose regard is at stake, and no "
                        "personal gain in it",
        "refuted_by": "personal gain present, or the same actor refusing an "
                      "identical demand where nobody was watching",
        "rests_on": [("SB-HFR-P2555", "Identity-protection motive", "CON-064"),
                     ("SB-HFR-P2554", "Moral/value-based motive", "CON-064"),
                     ("SB-HFR-P2853", "Duty/obligation sense", "CON-072")],
        "refuses": "being bound by a virtue is not the same as being virtuous "
                   "in the act.",
    },
    {
        "id": "IT-07",
        "name": "IMPATIENCE / VISIBLE PROOF",
        "means": "cannot hold through the long invisible process",
        "step": 2,
        "step_name": "PRESSURE",
        "his_example": "the golden calf — 'sacrificing long-term stability and "
                       "truth for an immediate, shiny illusion of wealth'",
        "reads_as": "%s is read as waiting through an invisible process "
                    "becoming unbearable, and a visible substitute being taken",
        "confirmed_by": "a long process underway that gives no sign, and the "
                        "thing taken being visible rather than valuable",
        "refuted_by": "no process underway, or the thing taken being the "
                      "actual object rather than a proxy for it",
        "rests_on": [("SB-HFR-P2545", "Consistency motive", "CON-064"),
                     ("SB-HFR-P1875", "Deliberative (System-2) judgment",
                      "CON-047")],
        "refuses": "never read impatience as greed. They reach for different "
                   "things in different directions.",
    },
    {
        "id": "IT-08",
        "name": "FRUIT-FOCUS",
        "means": "acting for the reward, not the rightness of the act",
        "step": 8,
        "step_name": "LOOP",
        "his_example": "Gita 2.47 — 'they create a top-heavy pyramid built on "
                       "lies'",
        "reads_as": "%s is read as aimed at what the act pays rather than at "
                    "the act being right",
        "confirmed_by": "a metric standing in for the thing it was meant to "
                        "measure, and the act optimising the metric where the "
                        "two come apart",
        "refuted_by": "the act being unchanged when the reward is removed",
        "rests_on": [("SB-HFR-P2529", "Extrinsic motive", "CON-064"),
                     ("SB-HFR-P0548", "Reward-history bias", "CON-014")],
        "refuses": "not 'rewards are bad'. The reading is about which one is "
                   "aimed at, not whether reward exists.",
    },
    {
        "id": "IT-09",
        "name": "PERMISSION-WAITING",
        "means": "stalled on a permission never asked for",
        "step": 4,
        "step_name": "WITNESS",
        "his_example": "his study sequence — the distraction that is really a "
                       "question nobody answered",
        "reads_as": "%s is read as stalled on a permission that was never "
                    "actually requested from anyone",
        "confirmed_by": "capability present, the act delayed, and no request "
                        "on record to the person who could grant it",
        "refuted_by": "a refusal actually received, or the capability being "
                      "absent",
        "rests_on": [("SB-HFR-P2535", "Autonomy need", "CON-064"),
                     ("SB-HFR-P2484", "Persistence-vs-quit arbitration",
                      "CON-062")],
        "refuses": "waiting is not consent and it is not refusal. Nobody was "
                   "asked.",
    },
)

#: The eight typed intents adopted from C-SB, kept as their own vocabulary.
#: His ruling stands: DO NOT SILENTLY MERGE NAMESPACES. They are listed beside
#: his nine and joined by nobody here.
ADOPTED_HALT = {
    "seam": "ADOPT-HALT-4 — wiring C-SB's eight typed intents into events_in",
    "his_nine": [t["id"] for t in TYPES],
    "adopted_eight": "the EVENT-INTENT GROWTH CONTRACT's typed intents, held "
                     "under custody at adopted/C-SB/",
    "merged": False,
    "why": "two intent vocabularies of different provenance. His ruling at the "
           "P2561 collision covers it: namespaces are not merged silently. "
           "Which of the eight are the same intent as which of his nine is his "
           "call and nobody else's.",
    "his_call": True,
}


def types() -> tuple:
    return TYPES


def get(tid: str) -> dict:
    tid = (tid or "").strip().upper()
    return next((t for t in TYPES if t["id"] == tid),
                {"found": False, "id": tid})


def _act_of(text: str) -> str:
    """The visible act, in the source's own words — never re-described.

    His law: capture the exact words before interpreting. The reading is what
    varies; the act must not."""
    return (text or "").strip().rstrip(".")


def read(text: str) -> dict:
    """ALL NINE READINGS OF ONE EVENT. None chosen, and none chooseable.

    Each reading names what would confirm it and what would refute it, so the
    set is testable rather than decorative. Which reading holds is decided by
    evidence from outside the sentence, which is not available here — so
    `chosen` is None, and there is no code path that could set it."""
    from . import archetype as A
    act = _act_of(text)
    fired = A.fires_on(text)
    by_arch = {}
    for f in fired["fired"]:
        for it in f["intents"]:
            by_arch.setdefault(it, []).append(f["id"])
    out = []
    for t in TYPES:
        out.append({
            "id": t["id"],
            "name": t["name"],
            "means": t["means"],
            "step": t["step"],
            "step_name": t["step_name"],
            "reading": t["reads_as"] % ("the act — " + act + " —")
                       if "%s" in t["reads_as"] else t["reads_as"],
            "confirmed_by": t["confirmed_by"],
            "refuted_by": t["refuted_by"],
            "refuses": t["refuses"],
            "rests_on": [{"id": p, "name": n, "container": c}
                         for p, n, c in t["rests_on"]],
            "his_example": t["his_example"],
            "raised_by_archetype": by_arch.get(t["id"], []),
            "chosen": None,
        })
    return {
        "text": text,
        "act": act,
        "readings": out,
        "reading_count": len(out),
        "raised_by_archetypes": sorted({f["id"] for f in fired["fired"]}),
        "chosen": None,
        "law": "his motto says every event HAS an intent. It does not say the "
               "event announces it. So the honest output is every intent the "
               "event could carry, all standing, each naming what would "
               "confirm and what would refute it.",
        "never": "two surviving candidates HALT rather than blend — his "
                 "standing rule. Nine surviving candidates are nine.",
        "adopted_seam": ADOPTED_HALT,
    }


def verify() -> dict:
    """Every row a reading rests on must be a real row of his bank."""
    from . import asi_pyramid as AP
    flat, _ = AP._flat()
    by_id = {r["sb_id"]: r for r in flat}
    bad, checked = [], 0
    for t in TYPES:
        for pid, name, cid in t["rests_on"]:
            checked += 1
            row = by_id.get(pid)
            if row is None:
                bad.append({"type": t["id"], "id": pid, "problem": "not in bank"})
            elif row["name"].strip().lower() != name.strip().lower():
                bad.append({"type": t["id"], "id": pid, "claimed": name,
                            "bank_says": row["name"]})
            elif row["container"] != cid:
                bad.append({"type": t["id"], "id": pid, "claimed": cid,
                            "bank_says": row["container"]})
    return {"rows_checked": checked, "problems": bad, "ok": not bad}


def stats() -> dict:
    return {
        "types": len(TYPES),
        "steps_covered": sorted({t["step"] for t in TYPES}),
        "rows_rested_on": sum(len(t["rests_on"]) for t in TYPES),
        "his_own_from_the_stealing_example": ["IT-01", "IT-02", "IT-03", "IT-04"],
        "adopted_merged": ADOPTED_HALT["merged"],
        "law": "a reading names what would confirm it and what would refute "
               "it. A candidate that names nothing that would flip it is not a "
               "candidate — his own falsifier law.",
        "never": "nothing is chosen, and nothing is chooseable from here.",
    }


def annotations() -> list:
    return [
        ("all events have intent — but the event does not announce it",
         "readings.read"),
        ("thief · opportunity · habit · saving a life", "readings.TYPES"),
        ("a reading names what would refute it", "readings.read"),
        ("the eight adopted intents are not merged with his nine",
         "readings.ADOPTED_HALT"),
    ]
