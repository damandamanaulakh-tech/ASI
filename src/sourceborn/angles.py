"""ANGLES — the position an event is read from. A PROPERTY, never a layer.

PHASE 13. His ask:

    angles applied at generation time as a property — growing with each
    example, all of them running for now.

and his definition, given in full:

    An angle is not a thing in the world and not a parameter. It is the
    position you read an event from, and the same event read from a different
    position yields a different intent.

HIS OWN FOUR, ON ONE EVENT

He wrote them himself, on Yudhishthira staking his wife and losing:

    worst          the single worst act of his life; a man gambles away a
                   human being
    best           a king who would not break his word once given, even to his
                   ruin
    emotional      a man cornered, humiliated in front of a court, unable to
                   stop
    truth/dharma   the most truthful man alive — which proves dharma is not
                   truth only

    Four positions, one event, four different intents — and none of them
    cancels the others.

WHY IT IS A PROPERTY AND NOT A LAYER — HIS ARGUMENT, NOT MINE

    if angles were a layer they would have IDs and a fixed count. You said
    they grow with each example. A property can grow without renumbering
    anything; a layer cannot.

So **there are no angle IDs in this module**. An angle is keyed by its NAME.
Adding one renumbers nothing, because there is nothing numbered. A test
enforces the absence: if an `ANG-001` ever appears here, angles have quietly
become a layer.

THE MECHANICAL PART, EXACTLY AS HE SPECIFIED IT

    each angle changes which rows light. Worst reaches the harm rows and the
    moral-responsibility rows. Best reaches loyalty, honour and commitment.
    Emotional reaches shame, face-saving and identity protection. Truth reaches
    the value rows and the value-behaviour-alignment row. Same sentence, four
    different container sets — which is your "meaning of the same sentence, and
    the response will not be the general."

Every row below was picked to that spec and verified against the live registry;
`P2561 Value-behaviour alignment` is the row he named by hand.

APPLIED AT GENERATION, AND ALL OF THEM RUN

His words: *all of them running for now*. `apply()` returns every angle on the
event — it does not choose one, and there is no code path that could. Four
readings of one event is his own law's case: they stand together, and none
cancels the others.
"""

from __future__ import annotations

#: HIS FOUR. Keyed by name — no ids, by his own argument. `reaches` are real
#: bank rows chosen to the row families he specified, each verified against the
#: live registry by a test.
HIS_ANGLES = (
    {
        "name": "worst",
        "by": "HIS",
        "position": "the act at its worst — what it destroyed and who carries "
                    "the responsibility for that",
        "his_reading": "the single worst act of his life; a man gambles away a "
                       "human being",
        "his_spec": "the harm rows and the moral-responsibility rows",
        "reaches": [
            ("SB-HFR-P1719", "Blame/responsibility attribution", "CON-043"),
            ("SB-HFR-P1279", "Blame/credit assignment", "CON-032"),
            ("SB-HFR-P2845", "Harm/care judgment", "CON-072"),
            ("SB-HFR-P2669", "Harm avoidance", "CON-067"),
            ("SB-HFR-P2262", "Guilt", "CON-057"),
            ("SB-HFR-P2855", "Moral-reasoning (deliberate)", "CON-072"),
            ("SB-HFR-P1864", "Social-consequence weighting", "CON-047"),
            ("SB-HFR-P1715", "Simulation of consequences", "CON-043"),
        ],
        "opens_intent": ["IT-01", "IT-04"],
        "refuses": "the worst reading is not the true one. It is one position, "
                   "and it does not cancel the other three.",
    },
    {
        "name": "best",
        "by": "HIS",
        "position": "the act at its best — the standing that would not bend, "
                    "and what it cost to hold it",
        "his_reading": "a king who would not break his word once given, even "
                       "to his ruin",
        "his_spec": "loyalty, honour and commitment",
        "reaches": [
            ("SB-HFR-P2553", "Loyalty motive", "CON-064"),
            ("SB-HFR-P2848", "Loyalty/in-group value", "CON-072"),
            ("SB-HFR-P2853", "Duty/obligation sense", "CON-072"),
            ("SB-HFR-P0777", "Commitment to action", "CON-020"),
            ("SB-HFR-P1869", "Choice commitment", "CON-047"),
            ("SB-HFR-P1155", "Precommitment use", "CON-029"),
            ("SB-HFR-P2820", "Reputation management", "CON-071"),
        ],
        "opens_intent": ["IT-06"],
        "refuses": "keeping a word is not the same as the word being right to "
                   "keep. His own Yudhishthira ruling: being bound by virtue "
                   "is not being virtuous in the act.",
    },
    {
        "name": "emotional",
        "by": "HIS",
        "position": "the act from inside the person doing it — what was "
                    "unbearable at that moment",
        "his_reading": "a man cornered, humiliated in front of a court, unable "
                       "to stop",
        "his_spec": "shame, face-saving and identity protection",
        "reaches": [
            ("SB-HFR-P2261", "Shame", "CON-057"),
            ("SB-HFR-P2263", "Embarrassment", "CON-057"),
            ("SB-HFR-P2435", "Shame/social-threat response", "CON-061"),
            ("SB-HFR-P2556", "Face-saving motive", "CON-064"),
            ("SB-HFR-P2138", "Face-saving interpretation", "CON-054"),
            ("SB-HFR-P2555", "Identity-protection motive", "CON-064"),
            ("SB-HFR-P2424", "Helplessness/learned helplessness", "CON-061"),
        ],
        "opens_intent": ["IT-05", "IT-07"],
        "refuses": "an explanation from inside is not an excuse, and it is not "
                   "a verdict either. His rule holds: his feeling is never "
                   "picked for him.",
    },
    {
        "name": "truth/dharma",
        "by": "HIS",
        "position": "the act against what the person actually holds — the gap "
                    "between the value and the behaviour",
        "his_reading": "the most truthful man alive — which proves dharma is "
                       "not truth only",
        "his_spec": "the value rows and the value-behaviour-alignment row",
        "reaches": [
            ("SB-HFR-P2561", "Value-behaviour alignment", "CON-064"),
            ("SB-HFR-P2554", "Moral/value-based motive", "CON-064"),
            ("SB-HFR-P2560", "Value ranking", "CON-064"),
            ("SB-HFR-P2562", "Sacred/protected values", "CON-064"),
            ("SB-HFR-P2878", "Values-clarification", "CON-072"),
            ("SB-HFR-P2879", "Moral-identity", "CON-072"),
            ("SB-HFR-P1680", "Validity-vs-truth distinction", "CON-042"),
        ],
        "opens_intent": ["IT-06", "IT-08"],
        "refuses": "holding a value is not living it — his own SGGS reading. "
                   "And a value held absolutely is what ARCH-005 warns of.",
    },
)

#: His law: *all of them running for now*. Nothing here selects.
ALL_RUN = True

#: Angles added by later examples land here. Same shape, `by` says whose it is.
#: Empty until an example demands one — his rule is that they GROW with each
#: example, not that a set was decided in advance.
GROWN_ANGLES = []


def angles() -> list:
    """Every angle in force. His four first, grown ones after."""
    return list(HIS_ANGLES) + list(GROWN_ANGLES)


def get(name: str) -> dict:
    n = (name or "").strip().lower()
    return next((a for a in angles() if a["name"].lower() == n),
                {"found": False, "name": name})


def for_hits(text: str, hits) -> dict:
    """THE SAME EVENT, READ FROM EVERY POSITION — taking hits already computed.

    Separate from `apply` for the same reason `trigger.for_hits` is: this
    module is called BY `place_on_spine`, so a version that called
    `place_on_spine` itself could not be wired into the answer path without
    recursing forever.

    His four run together and none is chosen — *all of them running for now*,
    and *none of them cancels the others*. Each returns a DIFFERENT container
    set from the same sentence, which is his own test of whether an angle is
    doing anything at all."""
    base_rows = {h["from"]["id"] for h in (hits or ())}
    base_cons = {h["container"] for h in (hits or ())}
    out = []
    for a in angles():
        rows = [{"id": p, "name": n, "container": c} for p, n, c in a["reaches"]]
        out.append({
            "angle": a["name"],
            "by": a["by"],
            "position": a["position"],
            "his_reading": a["his_reading"],
            "reaches": rows,
            "rows": len(rows),
            "containers": sorted({r["container"] for r in rows}),
            "already_reached_by_the_words": sorted(
                {r["id"] for r in rows} & base_rows),
            "opens_intent": a["opens_intent"],
            "refuses": a["refuses"],
            "chosen": None,
        })
    sets = [frozenset(x["containers"]) for x in out]
    return {
        "text": text,
        "angles_run": len(out),
        "all_run": ALL_RUN,
        "readings": out,
        "distinct_container_sets": len(set(sets)),
        "words_alone": {"rows": len(base_rows), "containers": sorted(base_cons)},
        "chosen": None,
        "law": "the same event read from a different position yields a "
               "different intent, and none of them cancels the others.",
        "never": "an angle holds nothing and owns nothing. It reads what is "
                 "already there, and it is never chosen between.",
    }


def apply(text: str) -> dict:
    """The same reading, from a bare ask. Seats it first, then reads."""
    from . import sbx
    placed = sbx.place_on_spine(text)
    return for_hits(text, placed["hits"])


def grow(name: str, position: str, his_reading: str, spec: str,
         reaches, opens_intent=(), refuses="", by="PROPOSED") -> dict:
    """Add an angle from a new example.

    His rule is that angles GROW with each example — and because there are no
    ids, adding one renumbers nothing. That is the whole reason he ruled it a
    property. An angle added here is `PROPOSED` until he says otherwise; his
    own four are `HIS`."""
    a = {"name": name, "by": by, "position": position,
         "his_reading": his_reading, "his_spec": spec,
         "reaches": list(reaches), "opens_intent": list(opens_intent),
         "refuses": refuses}
    GROWN_ANGLES.append(a)
    return {"added": name, "by": by, "angles_now": len(angles()),
            "renumbered": 0,
            "why_nothing_renumbered": "angles carry no ids — his argument for "
                                      "making this a property and not a layer"}


def verify() -> dict:
    """Every row an angle reaches must be a real row of his bank."""
    from . import asi_pyramid as AP
    flat, _ = AP._flat()
    by_id = {r["sb_id"]: r for r in flat}
    bad, checked = [], 0
    for a in angles():
        for pid, name, cid in a["reaches"]:
            checked += 1
            row = by_id.get(pid)
            if row is None:
                bad.append({"angle": a["name"], "id": pid, "problem": "not in bank"})
            elif row["name"].strip().lower() != name.strip().lower():
                bad.append({"angle": a["name"], "id": pid, "claimed": name,
                            "bank_says": row["name"]})
            elif row["container"] != cid:
                bad.append({"angle": a["name"], "id": pid, "claimed": cid,
                            "bank_says": row["container"]})
    return {"rows_checked": checked, "problems": bad, "ok": not bad}


def stats() -> dict:
    a = angles()
    return {
        "angles": len(a),
        "his": sum(1 for x in a if x["by"] == "HIS"),
        "grown": sum(1 for x in a if x["by"] != "HIS"),
        "has_ids": False,
        "all_run": ALL_RUN,
        "rows_reached": sum(len(x["reaches"]) for x in a),
        "distinct_rows": len({p for x in a for p, _, _ in x["reaches"]}),
        "law": "a property, not a layer — no ids and no fixed count, so it "
               "grows with each example without renumbering anything.",
        "never": "no angle is chosen; all of them run.",
    }


def annotations() -> list:
    return [
        ("an angle is the position you read an event from", "angles.apply"),
        ("four positions, one event, four different intents", "angles.HIS_ANGLES"),
        ("a property can grow without renumbering anything", "angles.grow"),
        ("all of them running for now", "angles.ALL_RUN"),
    ]
