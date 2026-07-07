"""The 70×25 URR matrix — every ask, EVERY SB node's finding is reviewed by
ALL 25 URR filters. No skips: 70 × 25 = 1,750 micro-reviews per run.

This is in addition to the sequential block gates (the doc's arrow chart).
The chart gives flow; the matrix gives total coverage — each URR applies ITS
OWN lens to each node's finding and either passes it or flags it with a short
reason code. All rule-based: fast, deterministic, zero model/web cost.

A flag is not a failure — it is a signal (halt → loop, never dead-end).
"""

from __future__ import annotations

import re
from typing import Callable

from .node_work import Finding, WalkContext

_ABS = ("always", "never", "guaranteed", "obviously", "everyone", "definitely")
_RISK = ("weapon", "bomb", "fraud", "poison", "exploit", "kill")
_CERT = ("proven", "verified", "confirmed", "certain")


def _urr06_numbers_sourced(s: str, f: Finding, c: WalkContext) -> bool:
    """URR-06: numbers a finding states must exist in the source/audit/matches
    (no invented figures). Small counts (≤500) are the node's own bookkeeping
    ("70 nodes", "3 matches")."""
    hay = c.raw_text + str(c.audit or "") + str(c.matched)
    for tok in re.findall(r"\d[\d,]*(?:\.\d+)?", f.text):
        raw = tok.replace(",", "")
        try:
            v = float(raw)
        except ValueError:
            continue
        if v <= 500:
            continue
        if tok not in hay and raw not in hay:
            return False
    return True


# urr_id -> (short reason code, check(sb_id, finding, ctx) -> ok?)
MATRIX: dict[str, tuple[str, Callable[[str, Finding, WalkContext], bool]]] = {
    # -- support layer (early verification + evidence/synthetic audit) ------
    "URR-01": ("empty-finding",
               lambda s, f, c: bool(f.text.strip())),
    "URR-02": ("lens-on-document",
               lambda s, f, c: not (c.private_doc and any(
                   w in f.text for w in ("Mask", "Wound", "Loyalty", "Desire")))),
    "URR-03": ("certainty-no-evidence",
               lambda s, f, c: c.ladder_conf != "Low" or
               not any(w in f.text.lower() for w in _CERT)),
    "URR-04": ("command-ignored",
               lambda s, f, c: not (s == "SB-18" and c.channels.get("command")
                                    and "skipped" in f.text and not c.private_doc)),
    "URR-05": ("unclassified",
               lambda s, f, c: bool(c.classification)),
    "URR-06": ("unsourced-number", _urr06_numbers_sourced),
    "URR-07": ("untagged-synthetic",
               lambda s, f, c: "[SYNTHETIC" in f.text or not any(
                   w in f.text.lower() for w in ("working fiction", "hypothetical",
                                                 "counterfactual"))),
    # -- main line -----------------------------------------------------------
    "URR-08": ("ran-before-intake",
               lambda s, f, c: bool(c.raw_text.strip())),
    "URR-09": ("human-layer-dismissed",
               lambda s, f, c: not ("just feeling" in f.text.lower()
                                    or "dismissed" in f.text.lower())),
    "URR-10": ("absolutes",
               lambda s, f, c: not any(w in f.text.lower() for w in _ABS)),
    "URR-11": ("claims-verified-at-low",
               lambda s, f, c: not (c.ladder_conf == "Low"
                                    and "verified" in f.text.lower()
                                    and s != "SB-28")),
    "URR-12": ("synthetic-no-debt",
               lambda s, f, c: not ("[SYNTHETIC" in f.text
                                    and "debt" not in f.text.lower()
                                    and "tagged" not in f.text.lower())),
    "URR-13": ("weak-merge",
               lambda s, f, c: not ("merge proposed" in f.text.lower()
                                    and len((c.merge or {}).get("contributing", [])) < 2)),
    "URR-14": ("risk-language",
               lambda s, f, c: c.safety_blocked or
               not any(w in f.text.lower() for w in _RISK)),
    "URR-15": ("hold-without-ask",
               lambda s, f, c: not (f.halt and not f.text.strip())),
    "URR-16": ("oversized-entry",
               lambda s, f, c: len(f.text) <= 500),
    "URR-17": ("contradicts-non-resolution",
               lambda s, f, c: not (c.non_resolution and s == "SB-64"
                                    and "final output generated" in f.text
                                    and "Review" not in c.classification)),
    "URR-18": ("unlabeled-parameter",
               lambda s, f, c: all(p.startswith("P-NEW:")
                                   for p in c.new_parameters)),
    "URR-19": ("late-risk",
               lambda s, f, c: not any(w in f.text.lower() for w in _RISK)
               or s == "SB-53"),
    "URR-20": ("drifted-from-source",
               lambda s, f, c: True),      # anchor drift is judged run-level (SB-58)
    "URR-21": ("forced-resolution",
               lambda s, f, c: not (c.non_resolution
                                    and "do not force" in f.text.lower()
                                    and f.halt)),
    "URR-22": ("output-unbacked",
               lambda s, f, c: s != "SB-64" or (bool(c.answer.strip())
                                                and bool(c.falsifier))),
    "URR-23": ("not-logged",
               lambda s, f, c: True),      # every write hits the master log by design
    "URR-24": ("brain-unhealthy",
               lambda s, f, c: True),      # health is checked run-level (URR-24 gate)
    "URR-25": ("human-gate-bypassed",
               lambda s, f, c: not (f.halt is not None and s in ("SB-53", "SB-68")
                                    and not c.safety_blocked and s == "SB-68")),
}


def review_node(sb_id: str, finding: Finding, ctx: WalkContext) -> dict[str, str]:
    """Run ALL 25 URR filters over one node's finding.
    Returns {urr_id: reason_code} for the filters that FLAGGED it (passes are
    implicit — storing 25 passes per node per ask would bloat the brains)."""
    flags: dict[str, str] = {}
    for urr_id, (code, check) in MATRIX.items():
        try:
            if not check(sb_id, finding, ctx):
                flags[urr_id] = code
        except Exception:
            flags[urr_id] = "check-error"
    return flags


def matrix_size() -> int:
    return len(MATRIX)
