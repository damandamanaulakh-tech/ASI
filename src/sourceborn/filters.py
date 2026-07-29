"""The seven filters — the path, replacing the 70×25 walk.

The 70 SB nodes still run and still write into their own brains: the memory is
untouched and keeps growing. What changed is what REVIEWS them. Instead of a
25-wide matrix sweeping every node, every node's finding now passes seven
gates, in order, every time:

    1 GROUND     does this pre-exist the asking?
                 yes -> we are hunting an expression, not inventing one
                 no  -> invention; different ground
    2 SEQUENCE   which of the 8 steps is this standing on?
    3 SOURCE     two witnesses. one caps at Medium. two that differ HALT.
    4 MASK       is the word we use the word the source used?
    5 FACT       every claim tagged; an untagged claim does not leave
    6 HALT       where does this fail — named, not hidden
    7 LOOP       the halt becomes the next Point Zero, and is handed back

Filters 3 and 4 are what found everything in the Riemann work. Filter 6 is what
stopped readings being invented to fill a gap. Filter 7 is what turned a dead
end into the next ask instead of a shrug.

This is method. The brains are memory. The filters consult them; the answer
grows them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from . import sequence as seq
from . import witnesses as wit

FILTER_IDS = ("FIL-1", "FIL-2", "FIL-3", "FIL-4", "FIL-5", "FIL-6", "FIL-7")
FILTER_NAMES = {
    "FIL-1": "Ground", "FIL-2": "Sequence", "FIL-3": "Source",
    "FIL-4": "Mask", "FIL-5": "Fact", "FIL-6": "Halt", "FIL-7": "Loop",
}

# words that name a thing vs words that name the name of a thing
_NAME_WORDS = ("called", "known as", "termed", "so-called", "what we call",
               "the name", "labelled", "labeled", "referred to as")


@dataclass
class FilterResult:
    gate: str
    name: str
    sb: str
    verdict: str = "pass"             # pass | hold
    why: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {"gate": self.gate, "name": self.name, "sb": self.sb,
                "verdict": self.verdict, "why": self.why, "detail": self.detail}


# ---------------------------------------------------------------- the gates

def f1_ground(ctx, sb: str, finding) -> FilterResult:
    invention = seq.is_invention(getattr(ctx, "raw_text", ""))
    why = ("invention — no ground to find, an expression to build"
           if invention else
           "grounded — the thing pre-exists the asking; we are after an expression")
    return FilterResult("FIL-1", "Ground", sb, "pass", why,
                        {"mode": "invention" if invention else "ground"})


def f2_sequence(ctx, sb: str, finding) -> FilterResult:
    step, why = seq.place(getattr(ctx, "raw_text", ""))
    return FilterResult("FIL-2", "Sequence", sb, "pass",
                        f"step {step} · {seq.STEP_NAME[step]} — {why}",
                        {"step": step, "step_name": seq.STEP_NAME[step]})


def source_read(ctx):
    """The source state of the RUN, computed once.

    A node's finding is the engine's own bookkeeping ("raw source locked, 42
    chars") — it makes no claim about the world, and testing it against sources
    is meaningless. What has witnesses is the ASK and the answer given to it. So
    the read is done once, on the real claim, and every node sees the same
    verdict — which is right: the source situation belongs to the run, not to
    node 37."""
    cached = getattr(ctx, "_source_read", None)
    if cached is not None:
        return cached
    claim = ((getattr(ctx, "answer", "") or "") + " "
             + (getattr(ctx, "raw_text", "") or "")).strip()
    r = wit.read(claim, wit.collect(ctx))
    try:
        ctx._source_read = r
    except Exception:
        pass
    return r


def f3_source(ctx, sb: str, finding) -> FilterResult:
    r = source_read(ctx)
    n = len(r.witnesses)
    if r.halt:
        return FilterResult("FIL-3", "Source", sb, "hold",
                            f"{n} witnesses differ on this claim — the gap is the "
                            f"finding, not noise to average away",
                            r.as_dict())
    if n == 0:
        return FilterResult("FIL-3", "Source", sb, "hold",
                            "no witness speaks to this claim — Low, and it should "
                            "not leave the engine as fact", r.as_dict())
    if n == 1:
        return FilterResult("FIL-3", "Source", sb, "pass",
                            f"one witness ({r.witnesses[0].origin}) — capped at "
                            f"{r.confidence}; one source can never reach High",
                            r.as_dict())
    return FilterResult("FIL-3", "Source", sb, "pass",
                        f"{n} independent witnesses agree ("
                        + ", ".join(w.origin for w in r.witnesses[:3])
                        + f") — {r.confidence}", r.as_dict())


def f4_mask(ctx, sb: str, finding) -> FilterResult:
    """Is a name standing in for a thing?

    Judged on what actually reaches the user — the answer against his own
    words — not on a node's internal note. "Re(s)=1/2" is the name; "alpha
    real" is what the source wrote; both are kept, neither is swapped in
    silently."""
    cached = getattr(ctx, "_mask_read", None)
    if cached is None:
        answer = (getattr(ctx, "answer", "") or "")
        raw = (getattr(ctx, "raw_text", "") or "")
        low = answer.lower()
        masks: list[str] = []
        for w in _NAME_WORDS:
            if w in low:
                masks.append(f"'{w}' — a name is standing in for a thing")
        ours = {t for t in wit._tokens(answer) if len(t) > 7}
        his = wit._tokens(raw)
        swapped = sorted(ours - his)[:3]
        if swapped and his and len(ours) > 4:
            masks.append("our words, not yours: " + ", ".join(swapped))
        excis = wit.excisions_in(answer)
        if excis:
            masks.append("excision mark — something was removed: " + ", ".join(excis))
        cached = masks
        try:
            ctx._mask_read = masks
        except Exception:
            pass
    if cached:
        return FilterResult("FIL-4", "Mask", sb, "pass",
                            "; ".join(cached)[:200], {"masks": list(cached)})
    return FilterResult("FIL-4", "Mask", sb, "pass",
                        "no name standing in for a thing", {"masks": []})


def f5_fact(ctx, sb: str, finding) -> FilterResult:
    ledger = getattr(ctx, "ledger", None) or []
    untagged = [e for e in ledger if not e.get("evidence_tag")]
    has_live = bool(getattr(ctx, "live", ""))
    conf = getattr(ctx, "ladder_conf", "Low")
    if untagged:
        return FilterResult("FIL-5", "Fact", sb, "hold",
                            f"{len(untagged)} claim(s) carry no source tag — "
                            f"an untagged claim does not leave the engine",
                            {"untagged": len(untagged)})
    return FilterResult("FIL-5", "Fact", sb, "pass",
                        f"{len(ledger)} claim(s) tagged · ladder {conf}"
                        + ("" if has_live else " · no live eyes on present fact"),
                        {"claims": len(ledger), "live": has_live, "ladder": conf})


def f6_halt(ctx, sb: str, finding) -> FilterResult:
    halt = getattr(finding, "halt", None)
    if halt:
        return FilterResult("FIL-6", "Halt", sb, "hold",
                            f"{halt}: {(getattr(finding, 'text', '') or '')[:140]}",
                            {"halt": halt})
    return FilterResult("FIL-6", "Halt", sb, "pass",
                        "no failure surfaced at this node", {"halt": None})


def f7_loop(ctx, sb: str, finding) -> FilterResult:
    halt = getattr(finding, "halt", None)
    step, _ = seq.place(getattr(ctx, "raw_text", ""))
    ask = seq.next_ask(step, halt or "", getattr(ctx, "raw_text", "")[:60])
    return FilterResult("FIL-7", "Loop", sb, "pass", ask,
                        {"next_ask": ask, "from_halt": bool(halt), "step": step})


GATES = (f1_ground, f2_sequence, f3_source, f4_mask, f5_fact, f6_halt, f7_loop)


def run_gates(ctx, sb: str, finding) -> list[FilterResult]:
    """All seven, in order, every time. A gate that throws must never kill the
    run — it reports the failure and the walk goes on."""
    out: list[FilterResult] = []
    for gate in GATES:
        try:
            out.append(gate(ctx, sb, finding))
        except Exception as exc:                     # a gate never kills the walk
            fid = getattr(gate, "__name__", "?").split("_")[0].upper().replace("F", "FIL-")
            out.append(FilterResult(fid, FILTER_NAMES.get(fid, fid), sb,
                                    "hold", f"filter error: {exc}"))
    return out
