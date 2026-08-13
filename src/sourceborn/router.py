"""THE RUBRIC ROUTER — the engine is chosen BY the problem, not the reverse.

His canon, verbatim:

    "So the Engine should be selected from the structured problem, rather than
     the Engine deciding what the problem is."

    Sentence → rubric activation says "this is a relation comparison" → engine
    Another portion says "this requires rule/constraint reasoning" → engine
    Another says "compare 5 historical occurrences" → pattern/memory engine
    Another says "arbitrate conflicting interpretations" → Meta mechanism

Before this module the walk was fixed: the same eight stages ran whatever the
sentence turned out to be. Here the STRUCTURE decides — the micro-sequence's own
facts name which mechanisms the ask needs, each with the reason it was called.

Every mechanism named here exists in this repo. Nothing is routed to a
mechanism that is not there, and where a mechanism is only partly wired the
route says so rather than pretending.
"""
from __future__ import annotations

from . import micro

# Every mechanism, what it is in the code, and how wired it really is.
MECHANISMS: dict[str, dict] = {
    "sequence": {
        "name": "The universal sequence (ARD/RGL flow)",
        "where": "sequence.py — Ground · Pressure · Use · Witness · "
                 "Expression · Naming · Halt · Loop",
        "wired": True},
    "relation": {
        "name": "Relation comparison",
        "where": "micro.relates() + dots.dot_connections()",
        "wired": True},
    "pattern_memory": {
        "name": "Pattern / memory engine — compare historical occurrences",
        "where": "patterns.group_repeats() + patterns.activate()",
        "wired": True},
    "rule": {
        "name": "Rule / constraint reasoning",
        "where": "wisdom.py (the wisdom bank) + safety.py (the hard line)",
        "wired": True},
    "human_layer": {
        "name": "Human read — the six lenses",
        "where": "core_gate.six_lenses()",
        "wired": True},
    "evidence": {
        "name": "Evidence ladder / proof grading",
        "where": "filters.f3_source + f5_fact, witnesses.py",
        "wired": True},
    "doubt": {
        "name": "Doubt / falsifier",
        "where": "doubt.doubt_engine() + falsifier()",
        "wired": True},
    "meta": {
        "name": "META — arbitrate conflicting interpretations",
        "where": "the Mask rule: two readings that differ are BOTH kept and "
                 "the gap goes to him. filters.f4_mask + his review.",
        "wired": True},
    "invention": {
        "name": "Invention route — nothing to find, an expression to build",
        "where": "sequence.is_invention()",
        "wired": True},
    "seq_kernel": {
        "name": "Sequence protocol — threshold · closure · spawn · ledger",
        "where": "seq_kernel.py",
        "wired": False,
        "note": "built and tested; his canon places its entry at the "
                "write-back / learning sequence, which patterns.review() now "
                "creates. Routing names it; the bridge is his to confirm "
                "(audit item 18)."},
}


# WHERE EACH HUMAN SEGMENT WORKS IN THE FLOW — his own placement, verbatim in
# substance. This is workflow, not counting: it says which segments serve which
# position, so the router can name who is being consulted at each step and the
# reading can show it. Segment names are his; the flow positions are his.
SEGMENT_ROLE: list[dict] = [
    {"seg": "SEG-01", "name": "Biological Regulation and Internal State",
     "at": ["world/human", "human nodes"],
     "serves": "current-state representation → emotion/motive support"},
    {"seg": "SEG-02", "name": "Perception and Body Representation",
     "at": ["world input", "ultra-micro splitter", "human nodes"],
     "serves": "representation of what was perceived"},
    {"seg": "SEG-03", "name": "Sensorimotor Action and Physical Execution",
     "at": ["sequence", "human nodes", "engines"],
     "serves": "action readiness → result / feedback"},
    {"seg": "SEG-04", "name": "Attention and Executive Control",
     "at": ["ultra-micro splitter", "rubric router", "human nodes",
            "meta assembly"],
     "serves": "what gets attended to, and what is held while it is examined"},
    {"seg": "SEG-05", "name": "Learning, Memory and Knowledge",
     "at": ["human nodes", "memory", "pattern memory"],
     "serves": "prior sequence retrieval — finding the previous encounters"},
    {"seg": "SEG-06", "name": "Reasoning, Planning, Decision and Creativity",
     "at": ["human nodes", "engines", "meta assembly"],
     "serves": "candidate interpretations → decision alternatives"},
    {"seg": "SEG-07", "name": "Language and Communication",
     "at": ["sentence/event", "ultra-micro splitter", "relation",
            "interpretation view"],
     "serves": "lexical / syntax / pragmatics → relations"},
    {"seg": "SEG-08", "name": "Emotion, Motivation, Intent and Motive",
     "at": ["human nodes", "rubric view", "pattern learning"],
     "serves": "intent and emotion HYPOTHESES — where he corrects them"},
    {"seg": "SEG-09", "name": "Consciousness, Self and Social Intelligence",
     "at": ["relation", "human nodes", "interpretation view"],
     "serves": "person-model / theory of mind → social-pattern comparison"},
    {"seg": "SEG-10", "name": "Development, Metacognition and Adaptation",
     "at": ["witness / self-check", "memory", "write-back",
            "pattern candidate"],
     "serves": "learning and adaptation → future rubric evolution"},
]

# the flow positions, in his order — the spine every reading is shown against
FLOW_POSITIONS = ["world/human", "sentence/event", "sequence instance",
                  "ultra-micro splitter", "relation", "parameter", "container",
                  "segment", "rubric router", "human nodes", "ai nodes",
                  "asi nodes", "engines", "memory", "local results",
                  "meta assembly", "interpretation view", "rubric view",
                  "write-back", "pattern memory", "pattern candidate",
                  "r-f-r / doubt", "approval", "new rubric version"]


def segments_at(position: str) -> list[dict]:
    """Which Human segments are working at a given position in the flow."""
    p = (position or "").strip().lower()
    return [s for s in SEGMENT_ROLE if p in s["at"]]


def flow_view(route_result: dict) -> list[dict]:
    """The whole flow, position by position, saying who works there and whether
    this run actually reached it. This is the spine of the reading view."""
    called = {c["key"] for c in route_result.get("mechanisms", [])}
    reached = {
        "world/human": True, "sentence/event": True,
        "sequence instance": True, "ultra-micro splitter": True,
        "relation": "relation" in called, "parameter": True,
        "container": True, "segment": True, "rubric router": True,
        "human nodes": "human_layer" in called, "ai nodes": True,
        "asi nodes": "meta" in called, "engines": True,
        "memory": "pattern_memory" in called, "local results": True,
        "meta assembly": "meta" in called, "interpretation view": True,
        "rubric view": True, "write-back": False, "pattern memory":
            "pattern_memory" in called, "pattern candidate": False,
        "r-f-r / doubt": "doubt" in called, "approval": False,
        "new rubric version": False,
    }
    return [{"position": p, "segments": [s["seg"] for s in segments_at(p)],
             "reached": bool(reached.get(p, False))}
            for p in FLOW_POSITIONS]


def route(seqs: list[dict], question: str = "",
          prior_repeats: int = 0, approved_hits: int = 0,
          conflicting: int = 0) -> dict:
    """Read the structured problem and name the mechanisms it needs.

    Returns them in the order they should run, each with WHY the structure
    called it. A mechanism with no reason is never called."""
    facts: set[str] = set()
    for m in seqs:
        facts.update(m.get("structural_facts", []))
    called: list[dict] = []
    seen = set()

    def call(key: str, why: str) -> None:
        if key in seen:
            for c in called:
                if c["key"] == key and why not in c["why"]:
                    c["why"].append(why)
            return
        seen.add(key)
        info = MECHANISMS[key]
        called.append({"key": key, "name": info["name"],
                       "where": info["where"], "wired": info["wired"],
                       "note": info.get("note", ""), "why": [why]})

    from .sequence import is_invention
    if question and is_invention(question):
        call("invention", "the ask builds something — there is no ground to "
                          "find, only an expression to make")
    else:
        call("sequence", "the ask reaches for something already there, so it "
                         "gets placed on the universal sequence")

    if any(len(m.get("relation", [])) for m in seqs):
        call("relation", "the sentence names a relation between people")
    if micro.F_ASYMMETRY_INFO in facts:
        call("relation", "an information asymmetry is a relation comparison")

    if prior_repeats:
        call("pattern_memory",
             f"{prior_repeats} prior micro-sequence(s) share this arrangement "
             "— compare historical occurrences")
    if approved_hits:
        call("pattern_memory",
             f"{approved_hits} of his approved patterns touch this ask")

    if micro.F_AGREEMENT_ABSENT in facts or micro.F_EXPECTATION_BROKEN in facts:
        call("rule", "an agreement or an expectation is in play — this needs "
                     "rule / constraint reasoning")

    if any(m.get("emotion_clues") for m in seqs) or micro.F_SELF_AFFECTED in facts:
        call("human_layer", "his own state is in the sentence — the six lenses "
                            "read the human under the words")

    if micro.F_DISCLOSURE_WITHHELD in facts:
        call("evidence", "something is missing from the record, so what is "
                         "known and what is only claimed must be graded")
        call("meta", "an absence has more than one reading and they must not "
                     "be averaged — the gap is a Mask and it goes to him")

    if any(m.get("uncertainty") for m in seqs):
        call("doubt", "he hedged — the strongest reading gets broken first")

    if conflicting > 1:
        call("meta", f"{conflicting} readings survive and disagree — META "
                     "arbitrates by keeping both and handing him the gap")

    if any(m.get("repeat_markers") for m in seqs):
        call("pattern_memory", "he marked the repetition himself")
        call("seq_kernel", "a repeat crossing an approved reading is where a "
                           "write-back / learning sequence begins")

    if not called:
        call("sequence", "no structural fact surfaced — the ask still gets "
                         "placed, and the emptiness is itself reported")

    return {"facts_seen": sorted(facts),
            "mechanisms": called,
            "count": len(called),
            "unwired": [c["key"] for c in called if not c["wired"]],
            "rule": "the engine is selected from the structured problem, "
                    "never the other way round (his canon)"}
