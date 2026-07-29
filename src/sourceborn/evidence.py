"""Stage 4 — Evidence ladder + source tags.

Separates real from simulated, tags each claim by its best available source, and
sets the answer's confidence from the strongest rung reached. Source tags follow
the 7025 core: REAL_TOOL / MANUAL / MEMORY / SIMULATED.
"""

from __future__ import annotations


def build_ledger(claims: list[str], has_live: bool, corpus_refs: list[str]) -> list[dict]:
    """Tag each micro-claim by the strongest source backing it."""
    ledger: list[dict] = []
    for c in claims:
        if has_live:
            tag, source, conf = "FACT", "REAL_TOOL (live web)", "High"
        elif corpus_refs:
            tag, source, conf = "REVIEW", "MEMORY (your corpus)", "Medium"
        else:
            tag, source, conf = "OPEN", "none yet", "Low"
        ledger.append({"claim": c[:120], "evidence_tag": tag,
                       "source": source, "confidence": conf})
    return ledger


def ladder_confidence(ledger: list[dict], witnesses: int | None = None) -> str:
    """Confidence = the highest rung any claim reached, THEN capped by how many
    independent witnesses stand behind it.

    The rung alone is not enough and that was the hole: one live lookup used to
    reach High on its own, which is one rendering of a thing being mistaken for
    the thing. So a single witness now caps at Medium however good its rung is,
    and High requires two independent witnesses that agree. Pass witnesses=None
    to get the old rung-only behaviour."""
    tags = {e["evidence_tag"] for e in ledger}
    if "FACT" in tags:
        rung = "High"
    elif "REVIEW" in tags:
        rung = "Medium"
    else:
        rung = "Low"
    if witnesses is None:
        return rung
    if witnesses <= 0:
        return "Low"
    if witnesses == 1 and rung == "High":
        return "Medium"          # the cap. one source is never High.
    return rung
