"""THE LIVE INTENT LEDGER — AND THE KILL HE SUPPLIED.

`ASI0001_tablet_run_LIVE_INTENT_v2.xlsx`, his words: *merge this one too / and read
the file as well*.

Two of that workbook's nineteen sheets are new, and between them they close the one
gap I had reported open at the end of the last build:

    the killing step. Nothing eliminates a fork on evidence. 154 intents come back
    as 154 whatever is known; generate -> evidence -> contradiction ->
    falsification -> survivor set has no survivor stage, in the code or in his
    workbook.

It has one now, and it is his, not mine. His LIVE_INTENT_ENGINE sheet carries a
column I never had:

    Falsifier / What would flip it

and it is FILLED on all ten of his candidates — beside Support Count and
Counterexample Count. That is the survivor stage: a candidate that names what would
flip it can be flipped. A candidate that names nothing cannot be killed, and this
module refuses to call such a thing a candidate at all.

WHAT HE RAN

ONE stable actor ("Same King"), ONE stable event ("Advisor requests a private
meeting"), ten brain-states, ten different intents, and `User Decision = HOLD` on
every one. Same man, same event, ten readings, none chosen. His ten states are
already in this core as SP-19..SP-28 — his own rule holds:

    its not required that it should make new everytime, mostly wording meaning are
    are exist in the core

so the states are matched to the packs rather than re-typed as new things. What IS
new is the EVENT (his ten King sequences did not contain it), the ten routes on it,
the ten falsifiers, his seven-rule generation contract, and the namespace ruling.

HIS NAMESPACE RULING — the seam I had left open, closed by him

    Registry boundary | This workbook retains its 2,000 source addresses |
    Current 3,204 registry can map in; do not silently merge namespaces

He calls the 2,000 ADDRESSES himself, which settles the reading `statepacks.py`
already enforced (80 x 25 addresses are not 2,000 parameters). And it adds a rule
that was NOT enforced anywhere: the workbook's `P0001..P2000` and the registry's
`SB-HFR-P0001..P3204` are two banks whose ids look alike and mean different things.
`map_in()` maps without merging, and a test proves workbook P0001 is not registry
P0001.

Canon: docs/method/canon/THE_LIVE_INTENT_LEDGER_AND_THE_KILL.md
"""

from __future__ import annotations

from . import human_registry as hr
from .asi_pyramid import bank_size, flat_of, param

# ---------------------------------------------------------------------------
# HIS RUN — verbatim. Field names are his column headers.
# ---------------------------------------------------------------------------

HIS_ACTOR = "Same King"
HIS_EVENT = "Advisor requests a private meeting"
EVENT_SHELL = "ADVISOR_PRIVATE_MEETING"

# LI-001..LI-010 exactly as his LIVE_INTENT_ENGINE sheet has them. `pack` is the
# state pack in this core that already carries the same brain-state.
HIS_CANDIDATES = (
    {"id": "LI-001", "state": "Insecure legitimacy", "pack": "SP-19",
     "params": "status uncertainty; self-model; social prediction; threat "
               "sensitivity; comparison",
     "trigger": "acceptance of rule is uncertain",
     "state_change": "increase visible confirmation of legitimacy",
     "target": "high-status ally / court",
     "constraint": "challenge may spread if ambiguity stays unresolved",
     "history": "prior contested acceptance",
     "intent": "Use the meeting to obtain or test visible confirmation that "
               "authority is recognized before allowing the challenge to spread.",
     "novelty": 0.88,
     "falsifier": "If the king already has strong independent legitimacy evidence "
                  "and treats the meeting as ordinary information exchange."},
    {"id": "LI-002", "state": "Secure legitimacy", "pack": "SP-20",
     "params": "stable self-model; low status uncertainty; decision/judgment; "
               "confidence",
     "trigger": "long accepted reign",
     "state_change": "improve decision quality without defending status",
     "target": "issue raised by advisor",
     "constraint": "no immediate legitimacy pressure",
     "history": "repeated acceptance / low challenge history",
     "intent": "Use the meeting primarily to gather decision-relevant information "
               "rather than to defend or prove authority.",
     "novelty": 0.73,
     "falsifier": "If the meeting contains direct evidence of a legitimacy "
                  "challenge."},
    {"id": "LI-003", "state": "Grieving", "pack": "SP-21",
     "params": "attachment/loss; episodic memory; energy; future-model; affect "
               "regulation",
     "trigger": "recent major personal loss",
     "state_change": "reduce immediate emotional/cognitive load while preserving "
                     "essential duties",
     "target": "meeting scope / timing",
     "constraint": "limited emotional capacity",
     "history": "recent loss changes value weights",
     "intent": "Narrow, defer, or structure the meeting so essential duty "
               "continues without forcing unnecessary emotional load.",
     "novelty": 0.91,
     "falsifier": "If behavior and capacity are unchanged despite the loss, or the "
                  "meeting is urgent and willingly prioritized."},
    {"id": "LI-004", "state": "Suspicious after betrayal", "pack": "SP-22",
     "params": "theory of mind; uncertainty; threat memory; conflict monitoring; "
               "inhibitory control",
     "trigger": "previous betrayal changed trust prior",
     "state_change": "reduce hidden-threat uncertainty before granting influence",
     "target": "advisor / information channel",
     "constraint": "risk of manipulation or concealed coordination",
     "history": "betrayal memory remains active",
     "intent": "Use the meeting as a verification opportunity: test the "
               "reliability of the advisor's account before expanding trust or "
               "authority.",
     "novelty": 0.95,
     "falsifier": "If independent evidence already verifies the advisor and no "
                  "threat-relevant cues appear."},
    {"id": "LI-005", "state": "Trusting after repeated reliability", "pack": "SP-23",
     "params": "trust history; attachment/relationship; social prediction; "
               "pragmatics",
     "trigger": "long reliable relationship",
     "state_change": "increase information quality through candid exchange",
     "target": "trusted advisor",
     "constraint": "need for unfiltered information",
     "history": "repeated reliability raises trust prior",
     "intent": "Use the private setting to receive information that may not be "
               "stated openly in a public court.",
     "novelty": 0.82,
     "falsifier": "If the private setting repeatedly produces distorted or "
                  "self-serving information."},
    {"id": "LI-006", "state": "Exhausted / low physical capacity", "pack": "SP-24",
     "params": "energy/fatigue; sleep; pain; working memory; inhibitory control; "
               "task management",
     "trigger": "body-state capacity is reduced",
     "state_change": "preserve decision quality by reducing irreversible load",
     "target": "decision timing / task size",
     "constraint": "fatigue may reduce processing capacity",
     "history": "same person, changed physical state",
     "intent": "Limit the meeting to essential facts and defer irreversible "
               "commitments until decision capacity is restored.",
     "novelty": 0.96,
     "falsifier": "If objective performance remains normal and delay would create "
                  "greater verified risk."},
    {"id": "LI-007", "state": "Victory-elevated confidence", "pack": "SP-25",
     "params": "reward; confidence; agency; status; recent-success memory; risk "
               "monitoring",
     "trigger": "major recent success",
     "state_change": "convert new opportunity into advantage without letting "
                     "success erase risk checks",
     "target": "next strategic opportunity",
     "constraint": "overgeneralization from recent success",
     "history": "recent victory raises confidence prior",
     "intent": "Explore expansion created by the victory, but require an explicit "
               "check that the new confidence is supported outside the winning "
               "context.",
     "novelty": 0.94,
     "falsifier": "If the opportunity is independently supported and not dependent "
                  "on extrapolating from the recent win."},
    {"id": "LI-008", "state": "Defeat-shaken", "pack": "SP-26",
     "params": "error monitoring; counterfactual reasoning; threat/loss; "
               "confidence; repair/resilience",
     "trigger": "major recent failure",
     "state_change": "identify controllable causes and reduce recurrence",
     "target": "failed decision chain",
     "constraint": "risk of blame/freeze/overreaction",
     "history": "recent defeat changes confidence and attention",
     "intent": "Use the meeting to separate controllable causes from noise before "
               "choosing whether to repair, change course, or accept the loss.",
     "novelty": 0.97,
     "falsifier": "If the loss has a known external cause that does not change the "
                  "decision model."},
    {"id": "LI-009", "state": "Divided loyalty", "pack": "SP-27",
     "params": "role conflict; family attachment; duty; promise; morality/norms; "
               "decision trade-off",
     "trigger": "multiple valid obligations are simultaneously active",
     "state_change": "find a decision that makes the conflict explicit rather than "
                     "hiding one obligation",
     "target": "kingdom / family / promise holders",
     "constraint": "no single role owns the decision",
     "history": "prior commitments remain active",
     "intent": "Use the meeting to expose which obligations conflict, what each "
               "requires, and which cost is accepted if one cannot be satisfied.",
     "novelty": 0.98,
     "falsifier": "If one obligation is actually non-binding or the conflict "
                  "disappears when facts are clarified."},
    {"id": "LI-010", "state": "Legacy-anxious / finite-horizon", "pack": "SP-28",
     "params": "age/time horizon; self-model; memory; identity; social prediction; "
               "mortality/meaning",
     "trigger": "remaining time becomes salient",
     "state_change": "increase continuity beyond the current self",
     "target": "succession / institutions / future memory",
     "constraint": "limited personal time horizon",
     "history": "age and legacy history alter future weighting",
     "intent": "Use the meeting to test whether current decisions still work after "
               "the king is absent, not merely while his personal authority "
               "remains.",
     "novelty": 0.99,
     "falsifier": "If succession/continuity is already robust and the decision has "
                  "no long-horizon consequence."},
)

# His seven-rule LIVE INTENT GENERATION CONTRACT, verbatim.
CONTRACT = (
    {"n": 1, "action": "Do not select only from the 100 prewritten King "
                       "characters.",
     "meaning": "Static characters are comparison anchors, not the ceiling of "
                "intent."},
    {"n": 2, "action": "At runtime, activate parameters/addresses from the current "
                       "Sequence.",
     "meaning": "A word/parameter may participate in many domains at once."},
    {"n": 3, "action": "Generate at least 3 competing intent candidates when "
                       "evidence permits.",
     "meaning": "Different active subsets should produce different target-state "
                "changes."},
    {"n": 4, "action": "An intent is new only when predicted behavior/target/"
                       "priority differs materially.",
     "meaning": "New wording is not enough."},
    {"n": 5, "action": "Store new intent first as LIVE_CANDIDATE.",
     "meaning": "No automatic canonical write."},
    {"n": 6, "action": "Pattern extraction happens after recurrence across "
                       "Sequences.",
     "meaning": "One interesting event does not equal a permanent pattern."},
    {"n": 7, "action": "If existing vocabulary repeatedly cannot express the live "
                       "intent without semantic loss, open parameter/rubric/"
                       "sub-parameter candidate.",
     "meaning": "Deep generation, conservative promotion."},
)

# His gate table, verbatim (LIVE_INTENT_ENGINE columns D-F).
GATES = (
    {"gate": "Generate", "meaning": "Create competing live intents",
     "rule": "Allowed immediately from current active structure"},
    {"gate": "Novelty", "meaning": "Compare to existing intent ledger",
     "rule": "New wording alone is not novelty; behavior/state-change must differ"},
    {"gate": "Pattern", "meaning": "Compare across Sequences",
     "rule": "Recurrence + behavior difference before pattern candidate"},
    {"gate": "Promote", "meaning": "Reusable intent/rubric/sub-parameter",
     "rule": "Evidence + falsifier + recurrence + user approval"},
    {"gate": "Keep open", "meaning": "Unresolved candidate",
     "rule": "OPEN/HOLD is valid"},
    {"gate": "Registry boundary",
     "meaning": "This workbook retains its 2,000 source addresses",
     "rule": "Current 3,204 registry can map in; do not silently merge namespaces"},
)

# ---------------------------------------------------------------------------
# THE NAMESPACE BOUNDARY — his ruling, enforced.
# ---------------------------------------------------------------------------

WORKBOOK_NS = "WB-P"          # his tablet workbook: 10 x 8 x 25 = 2,000 ADDRESSES
REGISTRY_NS = "SB-HFR-P"      # his human functional registry: 3,204 PARAMETERS
WORKBOOK_ADDRESSES = 2000
WORKBOOK_GRID = (10, 8, 25)

NAMESPACE_RULE = ("Current 3,204 registry can map in; do not silently merge "
                  "namespaces")


def namespaces() -> dict:
    """The two banks, side by side, with the collision named.

    Both use a bare `P` prefix in his files, and they are NOT the same thing:
    workbook P0001 is segment S01's first of 2,000 tablet addresses, registry
    P0001 is the first of his 3,204 human sub-parameters."""
    return {
        "workbook": {
            "ns": WORKBOOK_NS, "count": WORKBOOK_ADDRESSES,
            "grid": "%d segments x %d containers x %d = %d" % (
                WORKBOOK_GRID[0], WORKBOOK_GRID[1], WORKBOOK_GRID[2],
                WORKBOOK_ADDRESSES),
            "unit": "ADDRESS", "source": "ASI0001_tablet_run workbook",
            "his_word": "This workbook retains its 2,000 source addresses",
        },
        "registry": {
            "ns": REGISTRY_NS, "count": bank_size(),
            "grid": "10 segments x 8 containers x 40 (two hold 42) = %d"
                    % bank_size(),
            "unit": "PARAMETER", "source": "ASI_Claude_Parameters.docx v1.0",
            "his_word": "Current 3,204 registry can map in",
        },
        "collision": "both are written P####. Workbook P0001 is NOT registry "
                     "P0001 and the two counts must never be summed.",
        "rule": NAMESPACE_RULE,
        "merged": False,
    }


# His tablet workbook's ten segments. NOT the registry's ten — different subject
# entirely, and both are numbered 01..10.
WORKBOOK_SEGMENTS = (
    ("S01", "Kingship & Authority"),
    ("S02", "Family, Lineage & Household"),
    ("S03", "War, Security & Expansion"),
    ("S04", "Religion, Ritual & Cosmology"),
    ("S05", "Economy, Labor & Resources"),
    ("S06", "Knowledge, Engineering & Records"),
    ("S07", "Art, Language & Symbol System"),
    ("S08", "Society, Diplomacy & Culture"),
    ("S09", "Psychology, Emotion & Behavior"),
    ("S10", "Artifact Provenance & Reality Check"),
)


def map_in(workbook_segment: str) -> dict:
    """Report a workbook segment beside the registry — WITHOUT inventing a link.

    The obvious implementation maps S01 to SEG-01 by position. That would be a
    fabrication, and it is worth naming why: the workbook's S01 is *Kingship &
    Authority* and the registry's SEG-01 is *Biological Regulation and Internal
    State*. The two tens are different taxonomies that happen to be numbered the
    same way. So the ordinal neighbour is shown as a NEIGHBOUR, marked unmapped,
    and which workbook segment corresponds to which registry segment — if any —
    is held for him.

    This is his ruling doing work: `do not silently merge namespaces` bites at the
    segment level too, not only at the P ids."""
    seg = (workbook_segment or "").strip().upper()
    wb = dict(WORKBOOK_SEGMENTS).get(seg)
    n = int(seg[1:]) if seg[1:].isdigit() else 0
    regs = hr.segments()
    neighbour = regs[n - 1] if 1 <= n <= len(regs) else None
    rid = "SEG-%02d" % n if neighbour else None
    return {
        "workbook_segment": seg,
        "workbook_name": wb,
        "workbook_addresses": WORKBOOK_GRID[1] * WORKBOOK_GRID[2],
        "known_workbook_segment": wb is not None,
        "registry_same_ordinal": rid,
        "registry_same_ordinal_name": (neighbour or {}).get("name"),
        "registry_parameters_there": sum(len(c["subs"]) for c in hr.containers()
                                         if rid and c["segment"] == rid),
        "same_subject": False,
        "mapped": False,
        "merged": False,
        "rule": NAMESPACE_RULE,
        "held_for_him": "which registry segment (if any) this workbook segment "
                        "corresponds to. Ordinal position is not a mapping: "
                        "%s is %r, %s is %r." % (
                            seg, wb, rid, (neighbour or {}).get("name")),
    }


# ---------------------------------------------------------------------------
# THE CANDIDATE — and his rule 4: novelty is behavioural, not verbal.
# ---------------------------------------------------------------------------

LIVE_CANDIDATE = "LIVE_CANDIDATE"
KILLED = "KILLED"
HOLD = "HOLD"

# The structured fields novelty is judged on. The intent SENTENCE is deliberately
# not among them — that is his rule 4.
BEHAVIOUR_FIELDS = ("state_change", "target", "constraint")


def signature(cand: dict) -> tuple:
    """What a candidate PREDICTS, with its wording stripped out.

    His rule: an intent is new only when predicted behavior/target/priority
    differs materially. New wording is not enough. So the signature is built from
    the behavioural fields and never from `intent`."""
    return tuple(" ".join((cand.get(f) or "").lower().split())
                 for f in BEHAVIOUR_FIELDS)


def novelty(cand: dict, ledger) -> dict:
    """Is this candidate NEW against what the ledger already holds?

    Reports the reason either way, and names the ledger row it collided with."""
    sig = signature(cand)
    for row in ledger or ():
        if signature(row) == sig:
            same_words = (row.get("intent") or "").strip() == \
                         (cand.get("intent") or "").strip()
            return {
                "novel": False,
                "collides_with": row.get("id"),
                "why": "same predicted behaviour, target and constraint"
                       + ("" if same_words else " — only the wording differs, "
                                                "and wording is not novelty"),
                "wording_differs": not same_words,
            }
    return {"novel": True, "collides_with": None,
            "why": "no ledger row predicts this behaviour/target/constraint",
            "wording_differs": None}


def candidate(cand: dict, ledger=None, support: int = 1,
              counterexamples: int = 0) -> dict:
    """One live candidate, gated by his contract.

    A candidate with no falsifier is marked as such and cannot pass the promote
    gate — it names nothing that would flip it, so no evidence can reach it."""
    fals = (cand.get("falsifier") or "").strip()
    nov = novelty(cand, ledger or ())
    return {
        "id": cand.get("id"),
        "status": LIVE_CANDIDATE,
        "actor": cand.get("actor") or HIS_ACTOR,
        "event": cand.get("event") or HIS_EVENT,
        "state": cand.get("state"),
        "pack": cand.get("pack"),
        "params": cand.get("params"),
        "trigger": cand.get("trigger"),
        "state_change": cand.get("state_change"),
        "target": cand.get("target"),
        "constraint": cand.get("constraint"),
        "history": cand.get("history"),
        "intent": cand.get("intent"),
        "novelty_delta": cand.get("novelty"),
        "behaviour_signature": signature(cand),
        "novelty": nov,
        "falsifier": fals or None,
        "falsifiable": bool(fals),
        "support": support,
        "counterexamples": counterexamples,
        "epistemic_status": "SYNTHETIC / REVIEW",
        "user_decision": HOLD,
        "promotion_state": HOLD,
        "canonical": False,
        "in_bank": False,
        "is_native_parameter": False,
        "chosen": False,
    }


# ---------------------------------------------------------------------------
# THE KILL — the survivor stage. His falsifier column, made operational.
# ---------------------------------------------------------------------------

def kill(cand: dict, falsifier_met: bool = False, counterexamples: int = None,
         evidence: str = "") -> dict:
    """Eliminate a candidate on evidence — or say why it survives.

    NOTHING IS DELETED. The candidate comes back with a status and a reason
    appended; the row itself, its falsifier and its support are all still there
    to read. That is his NO REOPEN discipline: a later reading references the
    earlier one, it does not erase it.

    A candidate dies two ways, both of them his:
      * its falsifier is met — the condition it named as flipping it is true;
      * counterexamples reach or pass support — his Support / Counterexample
        columns, read as a comparison rather than as decoration.
    """
    out = dict(cand)
    ce = cand.get("counterexamples", 0) if counterexamples is None \
        else counterexamples
    out["counterexamples"] = ce
    sup = cand.get("support", 0)
    reasons = []
    if not cand.get("falsifiable"):
        out["status"] = LIVE_CANDIDATE
        out["survives"] = True
        out["cannot_be_killed"] = True
        out["why"] = ("no falsifier — nothing was named that would flip it, so no "
                      "evidence can reach it. It survives by default, which is a "
                      "defect in the candidate, not a strength.")
        return out
    out["cannot_be_killed"] = False
    if falsifier_met:
        reasons.append("falsifier met: " + (cand.get("falsifier") or ""))
    if ce and ce >= sup:
        reasons.append("counterexamples (%d) reached support (%d)" % (ce, sup))
    if reasons:
        out["status"] = KILLED
        out["survives"] = False
        out["killed_by"] = reasons
        out["evidence"] = evidence or None
        out["why"] = " AND ".join(reasons)
        out["row_kept"] = True
        out["deleted"] = False
    else:
        out["status"] = LIVE_CANDIDATE
        out["survives"] = True
        out["why"] = ("falsifier stated and not met; counterexamples (%d) below "
                      "support (%d)" % (ce, sup))
    return out


def survivors(cands, verdicts: dict = None) -> dict:
    """Run the kill over a candidate set and report the survivor set.

    `verdicts` maps candidate id -> {"falsifier_met": bool,
    "counterexamples": int, "evidence": str}. Ids absent from it are simply
    untested — and are reported as UNTESTED rather than as survivors, because
    "nobody checked" is not the same as "it held."""
    verdicts = verdicts or {}
    ran, alive, dead, untested, unkillable = [], [], [], [], []
    for c in cands:
        v = verdicts.get(c.get("id"))
        r = kill(c, falsifier_met=bool((v or {}).get("falsifier_met")),
                 counterexamples=(v or {}).get("counterexamples"),
                 evidence=(v or {}).get("evidence", ""))
        r["tested"] = v is not None
        ran.append(r)
        if r.get("cannot_be_killed"):
            unkillable.append(r)
        elif not r["survives"]:
            dead.append(r)
        elif v is None:
            untested.append(r)
        else:
            alive.append(r)
    return {
        "candidates": ran,
        "counts": {
            "generated": len(ran),
            "tested": len(ran) - len(untested),
            "survived": len(alive),
            "killed": len(dead),
            "untested": len(untested),
            "no_falsifier": len(unkillable),
            "deleted": 0,
        },
        "survivor_set": [r["id"] for r in alive],
        "killed_set": [r["id"] for r in dead],
        "untested_set": [r["id"] for r in untested],
        "law": "generate -> evidence -> contradiction -> falsification -> "
               "survivor set",
        "refuses": "an untested candidate is UNTESTED, not a survivor. Nothing is "
                   "deleted — a killed row keeps its falsifier and its reason.",
    }


# ---------------------------------------------------------------------------
# PROMOTION — his rules 5, 6 and 7. Conservative on purpose.
# ---------------------------------------------------------------------------

PROMOTE_REQUIREMENTS = ("evidence", "falsifier", "recurrence", "user_approval")
RECURRENCE_MIN = 2          # "recurrence across Sequences" — one is not recurrence


def promote(cand: dict, sequences_seen: int = 1, evidence: bool = False,
            rfr_passed: bool = False, user_approved: bool = False) -> dict:
    """Can this candidate become reusable/canonical? Almost always: not yet.

    His gate: Evidence + falsifier + recurrence + user approval. Every unmet
    condition is named, so it is obvious what is missing rather than simply
    refused."""
    unmet = []
    if not evidence:
        unmet.append("evidence: no supporting observation recorded")
    if not cand.get("falsifiable"):
        unmet.append("falsifier: none stated, so it can never be tested")
    if sequences_seen < RECURRENCE_MIN:
        unmet.append("recurrence: seen in %d sequence(s), needs %d — one "
                     "interesting event does not equal a permanent pattern"
                     % (sequences_seen, RECURRENCE_MIN))
    if not rfr_passed:
        unmet.append("R-F-R / URR: not run")
    if not user_approved:
        unmet.append("user approval: his word is required and has not been given")
    ok = not unmet
    return {
        "id": cand.get("id"),
        "promoted": ok,
        "promotion_state": "PROMOTED" if ok else HOLD,
        "canonical": ok,
        "unmet": unmet,
        "requirements": list(PROMOTE_REQUIREMENTS),
        "new_parameter_created": False,
        "rule": "Live intent may be generated immediately. Reusable/canonical "
                "promotion requires recurrence, evidence, counterexamples/"
                "falsifier, R-F-R/URR, and human approval. New intent does not "
                "automatically mean new parameter.",
    }


def semantic_loss(text: str, failures: int = 1) -> dict:
    """His rule 7 — the ONLY road to a new parameter, and it is a narrow one.

    A new parameter/rubric candidate opens when existing vocabulary REPEATEDLY
    cannot express the live intent without semantic loss. So two things are
    checked, not one: whether the registry has words for it at all, and whether
    the attempt has failed more than once.

    THE FIRST VERSION OF THIS FUNCTION WAS WORTHLESS AND THE FAILURE IS ON THE
    RECORD. It matched any word over four letters as a bare SUBSTRING, with no
    word boundaries, no IDF and no minimum evidence — so `productive` matched
    **Re**productive-hormone signalling, `personal` matched Peri**personal**-space
    touch, and `protective` matched Guarding/**protective** posture. Run over the
    25 candidates in the Einstein and Riemann brain workbooks it declared **all 25
    already expressible** and opened nothing, entirely on noise. A gate that
    always says no is not a gate.

    It now uses the same index the seating uses: hyphens split, whole words only,
    and his own bar — a word in forty of his names is not evidence. A row must
    also carry real weight (his STRONG band, a word in five names or fewer, or two
    qualifying words meeting on the same row) before it counts as carrying the
    meaning. Everything below that is reported as `weak_matches` so a bad match is
    visible rather than decisive."""
    from . import growing as _g
    s = _g.seat(text, limit=12)
    strong = [x for x in s["seats"]
              if x["band"] == "STRONG" or len(x["on"]) >= 2]
    weak = [x for x in s["seats"] if x not in strong]
    hits = [{"p": x["sb_id"], "name": x["name"], "container": x["container"],
             "on": x["on"], "weight": x["weight"], "band": x["band"]}
            for x in strong[:8]]
    expressible = bool(hits)
    repeated = failures >= 2
    return {
        "text": text,
        "expressible_in_existing_vocabulary": expressible,
        "matched_rows": hits,
        "weak_matches": [{"p": x["sb_id"], "name": x["name"], "on": x["on"],
                          "weight": x["weight"]} for x in weak[:6]],
        "words_too_common_to_be_evidence": s["weak_words"][:6],
        "failures": failures,
        "repeated": repeated,
        "opens_parameter_candidate": (not expressible) and repeated,
        "why": ("existing rows can carry it — no new parameter" if expressible
                else ("no existing row carries it and the failure has repeated — "
                      "a parameter candidate opens"
                      if repeated else
                      "no existing row carries it, but it has failed only once. "
                      "His rule says REPEATEDLY. Not yet.")),
        "how_matched": "whole words only, hyphens split, and a word in forty of "
                       "his names is not evidence. A row needs his STRONG band or "
                       "two qualifying words to count.",
        "rule": CONTRACT[6]["action"],
    }


# ---------------------------------------------------------------------------
# HIS RUN, EXECUTED — and the same run through this core's own generator.
# ---------------------------------------------------------------------------

def his_run(verdicts: dict = None) -> dict:
    """His ten candidates on one event, gated, killed and counted.

    With no verdicts handed in, nothing is killed and nothing is claimed to have
    survived — all ten come back UNTESTED, which is the true state of his sheet:
    Support 1, Counterexamples 0, Decision HOLD on every row."""
    ledger, cands = [], []
    for row in HIS_CANDIDATES:
        c = candidate(row, ledger=ledger)
        ledger.append(row)
        cands.append(c)
    res = survivors(cands, verdicts)
    res["actor"] = HIS_ACTOR
    res["event"] = HIS_EVENT
    res["event_shell"] = EVENT_SHELL
    res["one_event"] = True
    res["states"] = [c["state"] for c in cands]
    res["all_novel"] = all(c["novelty"]["novel"] for c in cands)
    res["all_falsifiable"] = all(c["falsifiable"] for c in cands)
    res["chosen"] = None
    res["packs_in_core"] = [c["pack"] for c in cands]
    res["contract"] = list(CONTRACT)
    res["gates"] = list(GATES)
    res["namespaces"] = namespaces()
    res["refuses"] = ("same man, same event, ten readings. None is chosen, and "
                      "HOLD is a valid resting state — his own gate says so.")
    return res


def from_core(scope: str = None) -> dict:
    """The same event run through THIS core's live generator, per state pack.

    His ten brain-states are already SP-19..SP-28 here, so the run is a join, not
    a re-typing: each pack supplies the active containers, `intents.generate`
    raises the motives those containers can reach, and the candidate count is a
    function of the parameters plugged in."""
    from . import intents as I
    from . import statepacks as S
    sc = scope or I.CURRENT
    rows = []
    for row in HIS_CANDIDATES:
        try:
            p = S.pack(row["pack"])
        except Exception:
            rows.append({"his_id": row["id"], "pack": row["pack"],
                         "error": "pack not found in the core"})
            continue
        g = I.from_state_pack(HIS_ACTOR, row["pack"], event=EVENT_SHELL, scope=sc)
        rows.append({
            "his_id": row["id"],
            "his_state": row["state"],
            "pack": p["id"], "pack_name": p["name"], "model": p["model"],
            "active_containers": g["counts"]["active_containers"],
            "motives_raised": g["counts"]["motives_raised"],
            "intents_generated": g["counts"]["intents_generated"],
            "his_intent": row["intent"],
            "his_falsifier": row["falsifier"],
        })
    ok = [r for r in rows if "error" not in r]
    return {
        "event": HIS_EVENT, "event_shell": EVENT_SHELL, "actor": HIS_ACTOR,
        "scope": sc,
        "rows": rows,
        "counts": {
            "his_candidates": len(HIS_CANDIDATES),
            "states_matched_to_packs": len(ok),
            "states_missing_from_core": len(rows) - len(ok),
            "total_generated_from_core": sum(r["intents_generated"] for r in ok),
            "native_parameters_added": 0,
        },
        "law": "his ten states already exist here as SP-19..SP-28 — matched, not "
               "re-created",
        "note": "the generated count is this core's motive x form expansion under "
                "each pack; his ten are the named readings ON TOP of it, not a "
                "replacement for it.",
    }


# ---------------------------------------------------------------------------
# WHAT THE WORKBOOK ACTUALLY CONTAINS — verified before anything was built on it.
# Findings. Not corrections: his file is not rewritten.
# ---------------------------------------------------------------------------

WORKBOOK_FINDINGS = (
    {"id": "WBF-01", "where": "MATCH_ENGINE",
     "finding": "all 100 characters score 0. Parameter Match 0, L1-L5 Adj 0, Loop "
                "Average 0, Contradiction Penalty 0, Final Score 0, Confidence "
                "Band 'Weak', Decision 'Hold', Proof Debt 'Open' — every row.",
     "consequence": "the ranking is not a ranking",
     "verified": True},
    {"id": "WBF-02", "where": "MATCH_ENGINE!M (Rank)",
     "finding": "=RANK(L4,$L$4:$L$103,0)+COUNTIF($L$4:L4,L4)-1 — with an all-zero "
                "score column the tie-break makes rank equal ROW ORDER, so K001 "
                "Lawgiver is rank 1 because it sits in row 4.",
     "consequence": "DASHBOARD reports 'Rank 1 · K001 Lawgiver · 0 · Hold' as the "
                    "leading hypothesis",
     "verified": True},
    {"id": "WBF-03", "where": "ASI-0001_RUN vs MATCH_ENGINE",
     "finding": "the run sheet names Priest-King / Divine Son as the leading "
                "hypothesis at '70% param + 30% loop, high'. The workbook's own "
                "engine names K001 Lawgiver at 0 / Weak / Hold.",
     "consequence": "the tablet run was reasoned in prose and never entered the "
                    "machinery it was built for",
     "verified": True},
    {"id": "WBF-04", "where": "PARAMETER_BANK",
     "finding": "2,000 rows present; all seven input columns empty (Observed "
                "Match, Confidence, Situation/Trigger, Evidence Source, "
                "Chronological Horizon, Artifact ID, Notes/Contradictions). "
                "Weighted Value therefore 0 for all 2,000.",
     "consequence": "PYRAMID_INDEX Input Evidence Score is 0 for all 10 segments, "
                    "so the 2,000-address surface contributes nothing to any score",
     "verified": True},
    {"id": "WBF-05", "where": "PYRAMID_INDEX!G",
     "finding": "=SUMIF(PARAMETER_BANK!$B$2:$B$2001,...) but the bank's data is "
                "rows 4..2003. The range covers P0001..P1998 and includes the "
                "blank row 2 and the header row 3.",
     "consequence": "P1999 and P2000 can never affect a segment score. Off by two "
                    "at both ends. Same defect as his previous workbook.",
     "verified": True},
    {"id": "WBF-06", "where": "PYRAMID_INDEX!H and MATCH_ENGINE!N",
     "finding": "ABS(G4) and ABS(L4) inside the confidence bands.",
     "consequence": "a contradicted, negative score reads as 'Strong' / 'Very "
                    "strong'. His own rule is that contradictions must REDUCE the "
                    "score; ABS() erases the sign. Latent today only because every "
                    "score is 0.",
     "verified": True},
    {"id": "WBF-07", "where": "ARD_5_LOOPS",
     "finding": "60 loop nodes, all 'Not started'. Input, Result, Supporting "
                "Evidence IDs, Contradiction IDs and Confidence are empty on every "
                "row — while ASI-0001_RUN carries LOOP 0-5 written out with "
                "verdicts and falsifiers.",
     "consequence": "README steps 3-7 were executed as text, not as nodes",
     "verified": True},
    {"id": "WBF-08", "where": "EVIDENCE_LEDGER / MEMORY_NODES",
     "finding": "500 evidence rows, all 'Unverified', 15 of 17 columns empty. 500 "
                "memory nodes, all 'Unused', including the Falsifier column.",
     "consequence": "the falsifiers he DID write live on the live-intent sheet; "
                    "the memory layer that was built to hold them is untouched",
     "verified": True},
    {"id": "WBF-09", "where": "DASHBOARD gates",
     "finding": "Decision Gates 1-5 all read 'Open', including Gate 3 'All five "
                "loops completed' and Gate 4 'Contradictions and falsifier "
                "tested', which the run sheet asserts are done. The gate cells are "
                "typed constants, not formulas.",
     "consequence": "the gates cannot move, so they neither confirm nor block "
                    "anything",
     "verified": True},
    {"id": "WBF-10", "where": "sheet counts",
     "finding": "the file has 19 sheets. INDEX lists 18 and omits ASI-0001_RUN "
                "entirely. DASHBOARD says 'Workbook sheets 16'.",
     "consequence": "three counts of the same file: 16 / 18 / 19",
     "verified": True},
    {"id": "WBF-11", "where": "INDEX row counts",
     "finding": "INDEX gives SOURCEBORN_INIT 12 rows (it holds 15 points, four of "
                "them the new Live Intent rules) and INDEX itself 16 (it lists "
                "18).",
     "consequence": "his own index did not follow his two new sheets",
     "verified": True},
    {"id": "WBF-12", "where": "ASI-0001_RUN character match",
     "finding": "the run cites 'F04 Sacred' and 'F08 Art'. His own "
                "KING_CHARACTERS has Sacred & Cosmological = F03 (K021-K030) and "
                "Art & Symbol = F07 (K061-K070); F04 is Family & Succession and "
                "F08 is Diplomacy & Society. The SEGMENT ids in the same rows "
                "(S04 Religion, S07 Art) are correct.",
     "consequence": "family ids appear to have been written from the segment "
                    "numbering. F02 War is right in both. Reported, not corrected "
                    "— his file stands as written.",
     "verified": True},
    {"id": "WBF-13", "where": "LIVE_INTENT_ENGINE / INTENT_LEDGER",
     "finding": "both are fully filled: 10 candidates, 10 falsifiers, novelty "
                "deltas 0.73-0.99, Support 1, Counterexamples 0, Decision HOLD, "
                "Canonical NO on every row.",
     "consequence": "the one part of the workbook that was actually run is the "
                    "part that closes the killing step. This is where the new "
                    "mechanism came from.",
     "verified": True},
)


def workbook_audit() -> dict:
    return {
        "file": "ASI0001_tablet_run_LIVE_INTENT_v2.xlsx",
        "sheets": 19,
        "new_sheets": ["LIVE_INTENT_ENGINE", "INTENT_LEDGER"],
        "run_sheet": "ASI-0001_RUN",
        "findings": list(WORKBOOK_FINDINGS),
        "counts": {"findings": len(WORKBOOK_FINDINGS),
                   "verified": sum(1 for f in WORKBOOK_FINDINGS if f["verified"]),
                   "corrections_made_to_his_file": 0},
        "rule": "preserve raw source. His workbook is not rewritten; what it "
                "contains is reported.",
    }


def stats() -> dict:
    r = his_run()
    return {
        "his_candidates": len(HIS_CANDIDATES),
        "one_event": HIS_EVENT,
        "states": len(HIS_CANDIDATES),
        "all_falsifiable": r["all_falsifiable"],
        "all_novel": r["all_novel"],
        "contract_rules": len(CONTRACT),
        "gates": len(GATES),
        "workbook_findings": len(WORKBOOK_FINDINGS),
        "namespaces_merged": False,
        "canonical_intents": 0,
        "parameters_added_by_this_module": 0,
        "source": "docs/method/canon/THE_LIVE_INTENT_LEDGER_AND_THE_KILL.md",
    }


def annotations() -> list:
    return [
        ("the falsifier is the killing step", "intent_ledger.kill"),
        ("an untested candidate is untested, not a survivor",
         "intent_ledger.survivors"),
        ("new wording is not novelty", "intent_ledger.signature"),
        ("promotion needs recurrence, evidence, falsifier and his word",
         "intent_ledger.promote"),
        ("a new parameter opens only on repeated semantic loss",
         "intent_ledger.semantic_loss"),
        ("do not silently merge namespaces", "intent_ledger.namespaces"),
        ("what his workbook actually computes", "intent_ledger.workbook_audit"),
    ]
