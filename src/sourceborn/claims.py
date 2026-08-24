"""CLAIM STATUS + THE JUDGMENT GATE — do not judge the visible thing yet.

His ruling, 2026-08-13, from the rice/MBA test:

    SOURCE CLAIMS
      "he sells rice"          FACT-IN-SOURCE
      "MBA helped him scale"   CAUSAL HYPOTHESIS
      "800 crore revenue"      SOURCE-ASSERTED NUMBER, NOT VERIFIED HERE
      "no business is small"   USER VALUE / GENERALIZATION

    HIGH REVENUE ≠ automatically HIGH PROFIT ≠ automatically GOOD BUSINESS

    VISIBLE THING → DO NOT JUDGE YET → FIND SYSTEM BEHIND IT →
    IDENTIFY CAPABILITIES → IDENTIFY INPUTS → IDENTIFY EXECUTION →
    MEASURE RESULTS → COMPARE ALTERNATIVE EXPLANATIONS → THEN FORM JUDGMENT

    "That is exactly the kind of reasoning your Rubric Pyramid should FORCE
     before the ASI reaches a conclusion."

WHAT THIS MODULE REFUSES
  * It will not upgrade a number he stated into a verified fact. A figure that
    arrived in his sentence is SOURCE-ASSERTED, and it says so.
  * It will not turn "X helped Y" into "X caused Y". A causal claim is a
    HYPOTHESIS and the alternative explanations are kept beside it — his list:
    experience, market timing, capital, relationships, execution, location,
    demand, distribution, risk-taking, team, previous knowledge, luck.
  * It will not let a judgment through before the chain is walked. The gate
    reports which of his steps are unmet and what is still missing, rather than
    delivering a conclusion built on a surface reading.
"""
from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# HIS STATUSES, in his words
FACT_IN_SOURCE = "FACT-IN-SOURCE"
CAUSAL_HYPOTHESIS = "CAUSAL HYPOTHESIS"
SOURCE_ASSERTED = "SOURCE-ASSERTED / NOT VERIFIED HERE"
USER_VALUE = "USER VALUE / GENERALIZATION"
# His correction (2026-08-13, the Samrath run): an absolute about a THIRD
# PARTY is a SOURCE generalization, not the owner's value. Same refusal —
# it is not evidence either way — but the two must not wear one label.
SOURCE_GENERALIZATION = "SOURCE GENERALIZATION"
COUNTERFACTUAL = "COUNTERFACTUAL / ALTERNATIVE PATH"

# his own list of what else could explain an outcome
ALTERNATIVE_CAUSES = ("experience", "market timing", "capital",
                      "relationships", "execution", "location", "demand",
                      "distribution", "risk-taking", "team",
                      "previous knowledge", "luck")

# things that measure a business, kept apart because he separated them
OUTCOME_LEVELS = ("revenue", "profit", "growth", "scale", "efficiency",
                  "resilience", "market reach", "durability")

_CAUSAL = re.compile(
    r"\b(help\w*|caus\w*|because|due to|thanks to|led to|leads to|"
    r"made him|made her|made them|enabled|allowed|so he|so she|so they|"
    r"that'?s why|reason he|reason she)\b", re.I)
_ABSOLUTE = re.compile(
    r"\b(no \w+ is|every|always|never|all \w+ are|any \w+ is|"
    r"nothing is|everyone|nobody)\b", re.I)
_COUNTERFACTUAL = re.compile(
    r"\b(instead of|rather than|if he had|if she had|if they had|"
    r"could have|would have|otherwise|as opposed to)\b", re.I)
# a number with a scale word, or a bare large figure
_NUMBER = re.compile(
    r"\b(\d[\d,.]*)\s*(crore|lakh|lac|million|billion|thousand|k|cr|bn|mn|%)?\b",
    re.I)
_MONEY_CTX = re.compile(
    r"\b(revenue|turnover|sales|profit|income|worth|valuation|salary|"
    r"crore|lakh|million|billion|rs|inr|usd|\$|₹)\b", re.I)


def read_claims(sentence: str) -> list[dict]:
    """Every claim in the sentence, with the status HE gave that KIND of claim.

    Nothing is upgraded. A number he stated stays source-asserted; a causal
    phrasing stays a hypothesis and carries his alternative causes."""
    s = (sentence or "").strip()
    if not s:
        return []
    out: list[dict] = []

    for m in _CAUSAL.finditer(s):
        out.append({
            "text": s, "trigger": m.group(0), "status": CAUSAL_HYPOTHESIS,
            "why": "the sentence links one thing to an outcome. That is a "
                   "HYPOTHESIS about cause, not an established cause.",
            "alternatives": list(ALTERNATIVE_CAUSES),
            "refuses": "it must not be recorded as 'X caused Y'. His rule: "
                       "preserve the contribution without making a false "
                       "causal claim."})
        break

    for m in _NUMBER.finditer(s):
        raw, unit = m.group(1), (m.group(2) or "")
        if not unit and not _MONEY_CTX.search(s):
            continue                      # a bare small number is not a figure
        if len(raw.replace(",", "").replace(".", "")) < 2 and not unit:
            continue
        out.append({
            "text": (raw + " " + unit).strip(), "trigger": m.group(0),
            "status": SOURCE_ASSERTED,
            "why": "a figure that arrived in your own sentence. It is kept as "
                   "you said it and NOT upgraded to a verified fact.",
            "verified_here": False,
            "refuses": "no external verification happened, so it must never be "
                       "shown as FACT."})

    for m in _ABSOLUTE.finditer(s):
        # WHOSE absolute is it? "I never trust them" is his value. "he always
        # cry" is the SOURCE generalizing about someone else. His words:
        # "never" = source generalization / "always" = source generalization /
        # NOT automatically: every single historical school visit = crying.
        # scope the pronoun test to the CLAUSE holding the absolute, not the
        # whole ask — "No business is small." must not inherit "him"/"his"
        # from three sentences away, which is exactly what it did at first
        lo = max((s.rfind(d, 0, m.start()) for d in ".;,!?"), default=-1) + 1
        nxt = [i for i in (s.find(d, m.end()) for d in ".;,!?") if i != -1]
        clause = s[lo:(min(nxt) if nxt else len(s))]
        third = re.search(r"\b(he|she|they|him|her|them|his|their)\b",
                          clause, re.I)
        first = re.search(r"\b(i|me|my|mine|we|us|our)\b", clause, re.I)
        # a NAMED third party counts too — "Samrath never like to go to school"
        # carries no pronoun at all, and it is still not the owner's value
        from .asi_pyramid import actor_name
        named = actor_name(clause)
        about_other = (bool(third) or bool(named)) and not first
        out.append({
            "text": s, "trigger": m.group(0), "clause": clause.strip(),
            "status": SOURCE_GENERALIZATION if about_other else USER_VALUE,
            "why": ("an absolute about someone else — the SOURCE generalizing, "
                    "not a measurement and not your own value. It does NOT "
                    "assert every single instance: \"always cry\" is a gist of "
                    "history, never an enumeration of every school visit."
                    if about_other else
                    "an absolute or universal phrasing — your value or "
                    "generalization, which is a different kind of thing from a "
                    "measurement."),
            "refuses": "it is not evidence, and it is not treated as one."})
        break

    for m in _COUNTERFACTUAL.finditer(s):
        out.append({
            "text": s, "trigger": m.group(0), "status": COUNTERFACTUAL,
            "why": "a path not taken is being compared with the path taken. "
                   "Both are held; neither is declared the better one.",
            "refuses": "his rule: do not conclude entrepreneurship > "
                       "employment universally. The same education can support "
                       "different execution paths."})
        break

    if not out:
        out.append({"text": s, "trigger": "", "status": FACT_IN_SOURCE,
                    "why": "stated in your source, and kept exactly as stated. "
                           "Being in the source is not the same as being "
                           "externally verified."})
    return out


def outcome_note(sentence: str) -> dict:
    """His separation: revenue is a signal, not the whole quality."""
    low = (sentence or "").lower()
    named = [o for o in OUTCOME_LEVELS if o in low]
    if not named:
        return {}
    missing = [o for o in ("profit", "growth", "durability", "efficiency",
                           "resilience") if o not in low]
    return {"named": named, "not_stated": missing,
            "his_rule": "HIGH REVENUE ≠ automatically HIGH PROFIT ≠ "
                        "automatically GOOD BUSINESS",
            "reading": "revenue is a useful outcome signal, not the whole "
                       "business quality. What was not stated is reported as "
                       "not stated, never assumed good."}


# ---------------------------------------------------------------------------
# THE JUDGMENT GATE — his ordered chain, and nothing judges before it is walked
CHAIN = [
    ("visible_thing", "VISIBLE THING",
     "what is actually on the surface"),
    ("do_not_judge_yet", "DO NOT JUDGE YET",
     "the shortcut from surface to verdict is refused here"),
    ("find_system", "FIND SYSTEM BEHIND IT",
     "market · operations · capital · supply chain · pricing · distribution"),
    ("capabilities", "IDENTIFY CAPABILITIES",
     "planning · error detection · abstraction · scaling"),
    ("inputs", "IDENTIFY INPUTS",
     "education · experience · capital · relationships · timing"),
    ("execution", "IDENTIFY EXECUTION",
     "what was actually done, not what was known"),
    ("results", "MEASURE RESULTS",
     "revenue · profit · growth · scale · durability, each on its own"),
    ("alternatives", "COMPARE ALTERNATIVE EXPLANATIONS",
     "every other thing that could have produced this outcome"),
    ("judgment", "THEN FORM JUDGMENT",
     "and only then"),
]

# what in a sentence counts as evidence that a step was actually reached
_STEP_SIGNALS = {
    "visible_thing": r"\b(sell\w*|shop|stall|product|goods|item|rice|tea|"
                     r"food|service)\b",
    "find_system": r"\b(business|model|market|operation\w*|supply|"
                   r"distribut\w*|pricing|margin|volume|customer\w*|demand)\b",
    "capabilities": r"\b(plan\w*|find flaws?|flaw\w*|analys\w*|analyz\w*|"
                    r"strateg\w*|scal\w*|upscal\w*|manage\w*|think\w*)\b",
    "inputs": r"\b(mba|degree|educat\w*|experience|capital|money|"
              r"relationship\w*|contact\w*|famil\w*|training|skill\w*)\b",
    "execution": r"\b(built|build|ran|run|grew|grow|expand\w*|open\w*|"
                 r"launch\w*|did|doing|work\w*)\b",
    "results": r"\b(revenue|turnover|profit|crore|lakh|million|billion|"
               r"growth|scale|sales)\b",
    "alternatives": r"\b(or|other|also|maybe|could be|might be|besides|"
                    r"apart from|luck|timing)\b",
}
_JUDGMENT_WORDS = re.compile(
    r"\b(small|big|great|good|bad|better|worse|successful|failure|"
    r"just a|only a|nothing but|merely)\b", re.I)


def judgment_gate(sentence: str) -> dict:
    """Walk his chain and report what is actually met — before any judgment.

    This is the gate he asked the Rubric Pyramid to FORCE. It does not block an
    answer; it states which steps the material supports and which are missing,
    so a verdict built on a surface reading is visible as one."""
    low = (sentence or "").lower()
    steps = []
    for key, label, detail in CHAIN:
        if key == "do_not_judge_yet":
            judged = bool(_JUDGMENT_WORDS.search(low))
            steps.append({"key": key, "step": label, "detail": detail,
                          "met": True,
                          "note": ("a judgment word is present — the shortcut "
                                   "from surface to verdict is exactly what "
                                   "this step refuses"
                                   if judged else
                                   "no premature verdict in the wording")})
            continue
        if key == "judgment":
            continue
        pat = _STEP_SIGNALS.get(key, "")
        hits = sorted({m.group(0) for m in re.finditer(pat, low)}) if pat else []
        steps.append({"key": key, "step": label, "detail": detail,
                      "met": bool(hits), "evidence": hits,
                      "note": ("" if hits else
                               "nothing in the ask reaches this step yet")})
    unmet = [s["step"] for s in steps if not s["met"]]
    return {
        "chain": steps,
        "unmet": unmet,
        "may_judge": not unmet,
        "verdict": ("the chain is walked — a judgment is now supported"
                    if not unmet else
                    "JUDGMENT NOT SUPPORTED YET — " + str(len(unmet)) +
                    " step(s) unmet: " + " · ".join(unmet)),
        "his_rule": "VISIBLE THING → DO NOT JUDGE YET → FIND SYSTEM BEHIND IT "
                    "→ IDENTIFY CAPABILITIES → IDENTIFY INPUTS → IDENTIFY "
                    "EXECUTION → MEASURE RESULTS → COMPARE ALTERNATIVE "
                    "EXPLANATIONS → THEN FORM JUDGMENT",
    }


# ---------------------------------------------------------------------------
# HIS NAMED PATTERNS from this test, with the status HE gave each
HIS_PATTERNS = [
    {"name": "Surface Simplicity ≠ System Simplicity",
     "his_mark": "checked",
     "reading": "A simple visible product can sit on top of a highly "
                "sophisticated business system.",
     "applies_to": ["tea stall", "rice seller", "transport company",
                    "cleaning business", "food distribution", "repair shop",
                    "agriculture", "logistics"],
     "refuses": "simple product = small achievement is an unsupported "
                "shortcut"},
    {"name": "Product Prestige ≠ Business Performance",
     "his_mark": "checked",
     "reading": "Product (ordinary / premium / fashionable / simple) and "
                "business (revenue · profit · growth · scale · efficiency · "
                "resilience · market reach) are DIFFERENT RUBRICS.",
     "refuses": "ordinary product → ordinary business, without evidence"},
    {"name": "Evaluate at Correct Abstraction Level",
     "his_mark": "checked",
     "reading": "Judge the outcome at the level it actually lives at, not at "
                "the level it is most visible at.",
     "refuses": "comparing a product's prestige with a business's performance"},
    {"name": "MBA as Capability Amplifier",
     "his_mark": "unchecked",
     "reading": "Education may act as a capability AMPLIFIER rather than being "
                "the underlying source of the opportunity or success.",
     "refuses": "MBA → success as a cause"},
    {"name": "Entrepreneurship vs Employment Leverage",
     "his_mark": "unchecked",
     "reading": "The same education can support different execution paths. The "
                "interesting part is the application of capability.",
     "refuses": "entrepreneurship > employment, universally"},
]


def stats() -> dict:
    return {"statuses": [FACT_IN_SOURCE, CAUSAL_HYPOTHESIS, SOURCE_ASSERTED,
                         USER_VALUE, COUNTERFACTUAL],
            "alternative_causes": len(ALTERNATIVE_CAUSES),
            "chain_steps": len(CHAIN),
            "his_patterns": len(HIS_PATTERNS),
            "checked_by_him": sum(1 for p in HIS_PATTERNS
                                  if p["his_mark"] == "checked")}


# ---------------------------------------------------------------------------
# THE SUCCESS-STORY STANCE — his teaching of 2026-08-24, filed under
# "failure -", canon at docs/method/canon/IF_THEY_CAN_I_WILL_TOO.md:
#
#     "they try to copy and failed / We have to understand they built
#      something there own, how someone can re do the same. / We should take
#      the success stories 'if they can i will too' instead 'i will also do
#      the same'"
#
# This is the second half of the rice/MBA law. That one forbids JUDGING the
# visible thing as proof of the system behind it; this one forbids USING the
# visible thing as a template for action. What survives a success story is
# exactly one thing: the possibility proof.
# ---------------------------------------------------------------------------

POSSIBILITY = "POSSIBILITY — his stance: 'if they can i will too'"
TEMPLATE_COPY = "TEMPLATE COPY — refused as a conclusion: 'i will also do " \
                "the same'"
STANCE_OPEN = "STANCE UNSTATED — both readings held, neither chosen"

# what the copier never sees — the judgment gate's own hidden layers
THEIRS_NON_COPYABLE = (
    "their system (built as their own)",
    "their capabilities",
    "their inputs and context",
    "their execution and sequence",
    "their timing and luck — the alternative explanations",
)

_STORY_RE = re.compile(
    r"\b(success stor(?:y|ies)|made it|made millions?|became rich|"
    r"millionaire|built an? empire|cracked it|their success|his success|"
    r"her success|got rich|winning stor)", re.I)

_COPY_RE = re.compile(
    r"\b(do the same|copy(?:ing)? (?:them|him|her|it|that)|same steps|"
    r"follow(?:ing)? (?:their|his|her) (?:steps|path|method|exact)|"
    r"repeat what|re[- ]?do the same|also do the same|exactly (?:what|like)"
    r" (?:they|he|she))\b", re.I)

_POSS_RE = re.compile(
    r"\b(if they can|if he can|if she can|i will too|so can i|"
    r"my own (?:way|thing|path)|possible for me|it is possible)\b", re.I)


def success_story_stance(text: str) -> dict:
    """Read material carrying a success story for its STANCE.

    Nothing here judges the person — the machine refuses the CONCLUSION
    'do the same and succeed', never the human holding it. An unstated
    stance is held open with both readings shown, because two readings are
    never collapsed."""
    low = text or ""
    story = _STORY_RE.search(low)
    copy_m = _COPY_RE.search(low)
    poss_m = _POSS_RE.search(low)
    if not story:
        return {"success_story_present": False,
                "why": "no success story is named in this material"}
    if copy_m and not poss_m:
        stance = TEMPLATE_COPY
    elif poss_m and not copy_m:
        stance = POSSIBILITY
    elif poss_m and copy_m and re.search(r"\binstead\b", low, re.I):
        # both phrasings with an "instead" between them is not an unstated
        # stance — it is the FLIP itself, his teaching's own sentence: the
        # possibility reading chosen, the copy reading named to be refused
        stance = POSSIBILITY
    else:
        stance = STANCE_OPEN
    out = {
        "success_story_present": True,
        "story_marker": story.group(0),
        "stance": stance,
        "markers": {"copy": copy_m.group(0) if copy_m else None,
                    "possibility": poss_m.group(0) if poss_m else None},
        "what_was_theirs": list(THEIRS_NON_COPYABLE),
        "what_transfers": "the possibility proof — it is possible for a "
                          "human. Nothing else in the story is a method.",
        "his_flip": "take the success stories 'if they can i will too' "
                    "instead 'i will also do the same'",
        "why_the_copy_fails": "they built something their own. The visible "
                              "success compresses the system, inputs and "
                              "sequence away — re-doing 'the same' re-does "
                              "only the surface, and the surface was never "
                              "the cause.",
        "failure_reread": "under the copy stance a failure is mis-read as "
                          "the person's verdict. Their success and this "
                          "path are two different sequences — the "
                          "comparison was never valid.",
        "extends": "DO_NOT_JUDGE_THE_VISIBLE_THING — same law, both "
                   "directions: the visible thing is neither proof nor "
                   "template.",
    }
    if stance == TEMPLATE_COPY:
        out["conclusion_allowed"] = False
        out["refuses"] = "'do the same and you will succeed' can never "\
                         "stand as this machine's conclusion."
    elif stance == POSSIBILITY:
        out["conclusion_allowed"] = True
        out["kept_as"] = "his stance, applied."
    else:
        out["conclusion_allowed"] = False
        out["held_open"] = "the stance is not stated; both readings are "\
                           "shown and neither is chosen for him."
    return out
