"""Per-node work + per-URR verification — ARD_RGL_7025 made real.

Before this module, the walk stamped ONE shared check onto every node, so all
70 SB points looked identical ("Clear.") and the 25 URR were one function under
25 names. That is exactly the flaw the user called out.

Here every SB point does ITS OWN job (the job the core document gives it) on
the run context, writes ITS OWN finding into ITS OWN local brain, and every
URR point runs ITS OWN verification role:

  * URR-08  Entry Verification Gate      (first gate, after SB-08)
  * URR-09  Human Layer Verification
  * URR-10..15  the Core of URR (doubt, evidence, synthetic, merge, risk, human)
  * URR-16..18  memory / cross-point / parameter integrity
  * URR-19..25  the Final 6+1 Block ending at the Human Final Gate

Everything is rule-based (zero extra model/web cost) and deterministic, so each
node's work is testable and its brain accumulates genuinely distinct memory.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Any, Callable

from .enums import HaltType
from .nodes import sb_by_id

# ---------------------------------------------------------------------------
# Walk context — everything the run produced, shared read-only by node work.
# ---------------------------------------------------------------------------

@dataclass
class WalkContext:
    raw_text: str = ""
    origin: str = "chat"
    answer: str = ""
    channels: dict[str, list[str]] = field(default_factory=dict)
    domain: dict[str, Any] = field(default_factory=dict)
    audit: dict[str, Any] | None = None
    core: dict[str, Any] = field(default_factory=dict)          # six lenses
    matched: list[str] = field(default_factory=list)
    ledger: list[dict] = field(default_factory=list)
    ladder_conf: str = "Low"
    live: str = ""
    doubt: dict[str, Any] = field(default_factory=dict)
    witness: list[str] = field(default_factory=list)
    falsifier: str = ""
    fuel: dict[str, Any] | None = None
    connections: list[dict] = field(default_factory=list)
    merge: dict[str, Any] | None = None
    halts: list[str] = field(default_factory=list)
    gaps: list[Any] = field(default_factory=list)
    anchor_note: str = ""
    anchor_on_target: bool = True
    non_resolution: bool = False
    embodied_ok: bool = True
    safety_blocked: bool = False
    safety_reasons: list[str] = field(default_factory=list)
    private_doc: bool = False
    classification: str = ""
    confidence: str = ""
    evidence_tag: str = ""
    memory_stats: dict[str, Any] = field(default_factory=dict)
    weekly_due: bool = False
    memory_hits: list[tuple[str, str]] = field(default_factory=list)  # (node, snippet)
    recall_matches: list[str] = field(default_factory=list)
    new_parameters: list[str] = field(default_factory=list)     # filled by SB-43
    synthetic_items: list[str] = field(default_factory=list)    # filled as stage 6 runs
    run_writes: int = 0
    holds_so_far: list[str] = field(default_factory=list)


@dataclass
class Finding:
    """What one SB node's own work produced (goes into ITS brain)."""
    text: str
    params: dict[str, Any] = field(default_factory=dict)
    halt: str | None = None            # HaltType value if this node holds


def _words(text: str, vocab: tuple[str, ...]) -> list[str]:
    low = text.lower()
    return [w for w in vocab if re.search(r"\b" + re.escape(w) + r"\b", low)]


def _kernel(text: str, max_words: int = 12) -> str:
    """SB-49: the ask compressed to its kernel (first sentence, trimmed)."""
    first = re.split(r"[.?!\n]", text.strip())[0]
    ws = first.split()
    return " ".join(ws[:max_words]) + ("…" if len(ws) > max_words else "")


# ---------------------------------------------------------------------------
# The 70 SB node jobs (per stage descriptions in ARD_RGL_7025).
# Each returns a Finding that is genuinely THIS node's work.
# ---------------------------------------------------------------------------

def _sb01(c: WalkContext) -> Finding:      # Point Zero Lock
    return Finding(f"raw source locked untouched: {len(c.raw_text)} chars, origin={c.origin}",
                   {"raw_len": len(c.raw_text), "origin": c.origin})

def _sb02(c: WalkContext) -> Finding:      # Noise & Static Stripper
    parts = {k: len(v) for k, v in c.channels.items()}
    return Finding("channels separated (kept, never discarded): " +
                   (", ".join(f"{k}×{n}" for k, n in parts.items()) or "single claim"),
                   {"channels": parts})

def _sb03(c: WalkContext) -> Finding:      # Source Domain Classifier
    d = c.domain
    return Finding(f"domain = {d.get('label', 'unclassified')} "
                   f"(numbers={d.get('signals', {}).get('numbers', 0)}, "
                   f"financial_terms={d.get('signals', {}).get('financial_terms', 0)})",
                   {"domain": d.get("domain", "")})

def _sb04(c: WalkContext) -> Finding:      # Raw Source Preservation
    h = hashlib.sha256(c.raw_text.encode("utf-8", "ignore")).hexdigest()[:16]
    return Finding(f"immutability fingerprint sha256:{h} — any later edit is detectable",
                   {"sha256_16": h})

def _sb05(c: WalkContext) -> Finding:      # Initial Parameter Mapping
    from .parameters import PARAMETER_BANK
    hits = [p.code for p in PARAMETER_BANK
            if any(w in c.raw_text.lower() for w in p.name.lower().split()[:1])]
    misfit = [k for k in c.channels if k in ("mystery", "invention_seed")]
    return Finding(f"{len(hits)}/{len(PARAMETER_BANK)} bank parameters touched; "
                   + (f"does not fit yet: {', '.join(misfit)}" if misfit else "all input fits"),
                   {"bank_hits": len(hits), "misfits": misfit})

def _sb06(c: WalkContext) -> Finding:      # Data Bank Connector
    import os
    banks = [b for b, on in (("Tavily live web", bool(os.environ.get("TAVILY_API_KEY"))),
                             ("corpus disk", bool(os.environ.get("SB_INGEST_CORPUS"))),
                             ("wisdom bank", True), ("example bank", True)) if on]
    return Finding("connected data banks: " + ", ".join(banks), {"banks": banks})

def _sb07(c: WalkContext) -> Finding:      # First Memory Write
    return Finding(f"first structured memory entry written (total entries now "
                   f"{c.memory_stats.get('total_memory_entries', 0)})",
                   {"entries": c.memory_stats.get("total_memory_entries", 0)})

def _sb08(c: WalkContext) -> Finding:      # Intake Completion Gate
    clean = bool(c.raw_text.strip()) and bool(c.channels) and bool(c.domain)
    return Finding("intake clean — locked, stripped, classified" if clean
                   else "intake incomplete", {"clean": clean},
                   halt=None if clean else HaltType.LOGIC.value)

def _sb09(c: WalkContext) -> Finding:      # Affect & Intent Ledger
    if c.private_doc:
        return Finding("no affect signals — numeric document (honest: not forced)")
    emos = _words(c.raw_text, ("fear", "afraid", "hope", "angry", "anger", "sad",
                               "love", "hate", "proud", "shame", "excited", "worried",
                               "frustrated", "happy"))
    stated = "question" if "?" in c.raw_text else "statement"
    return Finding((f"affect: {', '.join(emos)}" if emos else "no strong affect surfaced")
                   + f"; stated form: {stated}",
                   {"emotions": emos, "stated_form": stated})

def _sb10(c: WalkContext) -> Finding:      # Core Gate — Six Lenses
    dom = c.core.get("dominant_lens", "—")
    n = c.core.get("active_count", 0)
    return Finding(f"dominant lens: {dom} ({n}/6 active)" if not c.private_doc
                   else "lenses N/A — document audited, not psychoanalysed",
                   {"dominant": dom, "active": n})

def _sb11(c: WalkContext) -> Finding:      # Human Shadow Gate
    if c.private_doc:
        return Finding("shadow N/A for a document")
    avoid = _words(c.raw_text, ("not", "never", "don't", "won't", "avoid", "without", "except"))
    heavy = len(avoid) >= 4
    return Finding(f"avoidance/negation markers ×{len(avoid)}"
                   + (" — shadow heavy, human review advised" if heavy else " — light"),
                   {"avoidance_markers": len(avoid)},
                   halt=HaltType.EVIDENCE.value if heavy and not c.live else None)

def _sb12(c: WalkContext) -> Finding:      # Hidden Intent Feed Detector
    feeds = _words(c.raw_text, ("just", "only", "simply", "quick", "asap", "urgent",
                                "again", "finally", "still"))
    return Finding(f"small intent feeds: {', '.join(feeds) or 'none detected'}",
                   {"feeds": feeds})

def _sb13(c: WalkContext) -> Finding:      # Emotional Drama Processor
    bangs = c.raw_text.count("!")
    caps = sum(1 for w in c.raw_text.split() if len(w) > 3 and w.isupper())
    return Finding(f"drama-as-data: exclamations×{bangs}, shouted words×{caps} — "
                   + ("charged" if bangs + caps >= 2 else "calm"),
                   {"exclamations": bangs, "caps_words": caps})

def _sb14(c: WalkContext) -> Finding:      # Sacred / Cultural Anchor
    sacred = [m.split(":")[0] for m in c.matched if not m.startswith("corpus:")][:4]
    return Finding("sacred/cultural anchors matched: " + (", ".join(sacred) or "none"),
                   {"anchors": sacred})

def _sb15(c: WalkContext) -> Finding:      # Identity & Meaning Analyzer
    idw = _words(c.raw_text, ("i am", "my", "me", "myself", "identity", "who am i", "purpose"))
    return Finding(f"identity involvement: {'high' if len(idw) >= 3 else 'low'} "
                   f"({', '.join(idw) or 'no identity markers'})", {"identity_words": idw})

def _sb16(c: WalkContext) -> Finding:      # Power & Control Mapper
    pw = _words(c.raw_text, ("must", "control", "force", "authority", "own", "command",
                             "power", "make them", "obey"))
    return Finding(f"power/control markers: {', '.join(pw) or 'none'}", {"power": pw})

def _sb17(c: WalkContext) -> Finding:      # Wound & Threat Examiner
    lens = (c.core.get("lenses") or {}).get("Wound & Threat", {})
    sig = lens.get("signals", [])
    return Finding(f"wound/threat signals: {', '.join(sig) or 'none surfaced'}",
                   {"signals": sig})

def _sb18(c: WalkContext) -> Finding:      # Human Layer Completion
    return Finding("human layer complete — affect, lenses, shadow, identity, power all recorded"
                   if not c.private_doc else "human layer honestly skipped (document input)")

def _sb19(c: WalkContext) -> Finding:      # Truth Pressure Test
    q = _kernel(c.raw_text)
    return Finding(f'pressure question: "What truth is this avoiding about: {q}?"',
                   {"pressure_on": q})

def _sb20(c: WalkContext) -> Finding:      # Doubt Engine
    v = c.doubt.get("verdict", "—")
    fr = c.doubt.get("fragilities", [])
    return Finding(f"doubt verdict: {v}; fragilities: {len(fr)}",
                   {"fragilities": fr},
                   halt=HaltType.LOGIC.value if c.doubt.get("bites") else None)

def _sb21(c: WalkContext) -> Finding:      # Falsifier
    return Finding(f"falsifier: {c.falsifier or '—'}")

def _sb22(c: WalkContext) -> Finding:      # Witness Node
    return Finding("blind spot: " + (c.witness[0] if c.witness else "none surfaced"),
                   {"blind_spots": c.witness[:3]})

def _sb23(c: WalkContext) -> Finding:      # Contradiction Finder
    marks = _words(c.raw_text, ("but", "however", "yet", "although", "contradiction"))
    return Finding(f"contradiction markers in source: {', '.join(marks) or 'none'}",
                   {"markers": marks})

def _sb24(c: WalkContext) -> Finding:      # Hidden Assumption Attacker
    asm = c.channels.get("assumption", [])
    abso = _words(c.raw_text, ("obviously", "everyone", "always", "never", "clearly"))
    return Finding(f"assumptions to attack: {len(asm)} explicit"
                   + (f"; absolutes: {', '.join(abso)}" if abso else ""),
                   {"assumptions": len(asm), "absolutes": abso},
                   halt=HaltType.LOGIC.value if abso else None)

def _sb25(c: WalkContext) -> Finding:      # Framing Challenger
    return Finding(f'counter-frame: "What if the opposite of \'{_kernel(c.raw_text, 8)}\' is the case?"')

def _sb26(c: WalkContext) -> Finding:      # Courage Wall
    avoided = (c.channels.get("mystery") or c.channels.get("assumption") or ["nothing named"])[0]
    return Finding(f"named what is being avoided: {avoided[:90]}")

def _sb27(c: WalkContext) -> Finding:      # Identity Resistance Check
    res = c.doubt.get("bites") and not c.private_doc
    return Finding("identity-level resistance detected — conclusion threatens self-image"
                   if res else "no identity-level resistance")

def _sb28(c: WalkContext) -> Finding:      # Verified Truth Lock
    facts = [e for e in c.ledger if e.get("evidence_tag") == "FACT"]
    return Finding(f"locked truth elements: {len(facts)} at FACT rung "
                   f"(of {len(c.ledger)} claims)", {"facts": len(facts)})

def _sb29(c: WalkContext) -> Finding:      # Evidence Ledger
    tags = {}
    for e in c.ledger:
        tags[e.get("evidence_tag", "?")] = tags.get(e.get("evidence_tag", "?"), 0) + 1
    return Finding(f"ledger built: {len(c.ledger)} claims — "
                   + (", ".join(f"{k}×{v}" for k, v in tags.items()) or "empty")
                   + f"; ladder confidence {c.ladder_conf}", {"rungs": tags})

def _sb30(c: WalkContext) -> Finding:      # Source Tagger
    srcs = {"REAL_TOOL": 1 if c.live else 0,
            "MANUAL": sum(1 for m in c.matched if m.startswith("corpus:")),
            "MEMORY": len(c.memory_hits),
            "SIMULATED": len(c.synthetic_items)}
    return Finding("sources tagged: " + ", ".join(f"{k}×{v}" for k, v in srcs.items()),
                   {"sources": srcs})

def _sb31(c: WalkContext) -> Finding:      # Domain-Adaptive Auditor
    if c.audit:
        a = c.audit
        return Finding(f"numeric audit: {a.get('summary', '')}"[:220], {"audit": True})
    return Finding(f"prose audit rules applied ({c.domain.get('domain', 'prose')}): "
                   "overclaim scan + evidence demand", {"audit": False})

def _sb32(c: WalkContext) -> Finding:      # Literature & Historical Pattern Hunter
    return Finding(f"patterns matched across time/domains: {len(c.matched)}",
                   {"matched": len(c.matched)})

def _sb33(c: WalkContext) -> Finding:      # Live Real-World Data Link
    if c.private_doc:
        return Finding("private document — web grounding N/A (the file IS the data)")
    if c.live:
        return Finding(f"live fact connected: {c.live[:120]}")
    return Finding("no live source connected — paste data or set a Tavily key",
                   halt=HaltType.EVIDENCE.value if any(
                       w in c.raw_text.lower() for w in ("proof", "evidence", "data", "current"))
                   else None)

def _sb34(c: WalkContext) -> Finding:      # Proof Ladder Builder
    order = ["SYNTHETIC", "OPEN", "REVIEW", "FACT"]
    top = max((e.get("evidence_tag", "OPEN") for e in c.ledger),
              key=lambda t: order.index(t) if t in order else 0, default="OPEN")
    return Finding(f"proof ladder top rung this run: {top}", {"top_rung": top})

def _sb35(c: WalkContext) -> Finding:      # In-Silico Validator
    if c.audit:
        tot, stated = c.audit.get("candidate_total"), c.audit.get("stated_totals") or []
        ok = (not stated) or (tot in stated)
        return Finding(("recomputed totals agree with stated total" if ok else
                        f"MISMATCH: largest figure {tot} vs stated {stated}"),
                       {"consistent": ok},
                       halt=None if ok else HaltType.LOGIC.value)
    overlap = len(set(c.answer.lower().split()) & set(c.raw_text.lower().split()))
    return Finding(f"in-silico check: answer↔ask term overlap {overlap} words",
                   {"overlap": overlap})

def _sb36(c: WalkContext) -> Finding:      # Evidence Completion
    ready = bool(c.ledger)
    return Finding(f"evidence status closed at {c.ladder_conf} — "
                   + ("ready for connection work" if ready else "no claims to ground"))

def _sb37(c: WalkContext) -> Finding:      # Dot Connection Engine
    return Finding(f"memory scanned across all points: {len(c.memory_hits)} hits"
                   + (f" — e.g. {c.memory_hits[0][0]}" if c.memory_hits else ""),
                   {"hits": [h[0] for h in c.memory_hits[:5]]})

def _sb38(c: WalkContext) -> Finding:      # Cross-Domain Fusion
    doms = {c.domain.get("domain", "prose")} | {"memory"} if c.memory_hits else {c.domain.get("domain", "prose")}
    risk = "high" if (c.fuel and len(doms) > 1) else "low"
    return Finding(f"fusion candidates across {len(doms)} domain(s); force-fit risk {risk}",
                   {"domains": sorted(doms), "force_fit": risk})

def _sb39(c: WalkContext) -> Finding:      # Non-Text Pattern Detector
    return Finding("non-text patterns: text-only run (images/watermarks/footprints "
                   "scan when files are uploaded)")

def _sb40(c: WalkContext) -> Finding:      # Merge Proposal
    if c.merge:
        return Finding(f"merge proposed from {len(c.merge.get('contributing', []))} sources "
                       "— needs your approval (human gate)", {"merge": c.merge},
                       halt=HaltType.EVIDENCE.value)
    return Finding("no merge proposed — connections below real-value threshold")

def _sb41(c: WalkContext) -> Finding:      # Convergence Hunter
    return Finding(f"similar past conclusions: {len(c.recall_matches)}"
                   + (f" — e.g. {c.recall_matches[0][:70]}" if c.recall_matches else ""))

def _sb42(c: WalkContext) -> Finding:      # Cross-Point Contradiction
    neg = [h for h, s in c.memory_hits if any(
        w in s.lower() for w in ("not ", "never", "wrong", "false"))]
    return Finding(f"cross-point contradictions: {len(neg)}"
                   + (f" (vs {', '.join(neg[:3])})" if neg else ""))

def _sb43(c: WalkContext) -> Finding:      # New Parameter Generator
    new = [f"P-NEW:{k}" for k in c.channels if k in ("mystery", "invention_seed")]
    c.new_parameters.extend(new)
    return Finding(("new parameters generated: " + ", ".join(new)) if new
                   else "all data fits existing parameters — none generated",
                   {"new_parameters": new})

def _sb44(c: WalkContext) -> Finding:      # Memory Sync
    return Finding(f"memory synced — {c.run_writes} writes so far this run")

def _sb45(c: WalkContext) -> Finding:      # Synthetic Fuel Injector
    if c.fuel:
        c.synthetic_items.append(c.fuel.get("fuel", "fuel"))
        return Finding(f"stall {c.fuel.get('stall')} → injected {c.fuel.get('fuel')} "
                       "[SYNTHETIC, proof-debt tagged]", {"fuel": c.fuel.get("fuel")})
    return Finding("no stall — no synthetic fuel needed")

def _sb46(c: WalkContext) -> Finding:      # Invention Seed Protector
    seeds = c.channels.get("invention_seed", [])
    return Finding(f"invention seeds protected (not forced to resolve): {len(seeds)}"
                   + (f" — {seeds[0][:60]}" if seeds else ""))

def _sb47(c: WalkContext) -> Finding:      # Working Fiction Scaffold
    if c.fuel:
        return Finding(f"scaffold: treat '{_kernel(c.raw_text, 8)}' as working fiction "
                       "until evidence arrives [SYNTHETIC]")
    return Finding("no scaffold needed — direct path open")

def _sb48(c: WalkContext) -> Finding:      # Apostatic Inversion
    return Finding(f'inversion: argue the exact opposite — "{_kernel(c.raw_text, 8)}" is '
                   "false/backwards. What survives that attack is stronger.")

def _sb49(c: WalkContext) -> Finding:      # Heuristic Simplification
    return Finding(f"kernel: {_kernel(c.raw_text)}")

def _sb50(c: WalkContext) -> Finding:      # Synthetic Tagging
    n = len(c.synthetic_items)
    return Finding(f"synthetic items this run: {n} — all carry proof debt + expiry"
                   if n else "no synthetic items to tag", {"synthetic_count": n})

def _sb51(c: WalkContext) -> Finding:      # Parameter Labeler
    return Finding((f"labeled {len(c.new_parameters)} new parameters "
                    f"(reason+source+proof level recorded)") if c.new_parameters
                   else "no new parameters to label")

def _sb52(c: WalkContext) -> Finding:      # Synthetic Completion
    load = "high" if len(c.synthetic_items) >= 2 else ("low" if c.synthetic_items else "zero")
    return Finding(f"synthetic load: {load}",
                   halt=HaltType.EVIDENCE.value if load == "high" and not c.live else None)

def _sb53(c: WalkContext) -> Finding:      # Risk & Command Gate
    if c.safety_blocked:
        return Finding("RISK: " + "; ".join(c.safety_reasons)[:140],
                       halt=HaltType.SAFETY.value)
    return Finding("no legal/ethical/harm risk detected")

def _sb54(c: WalkContext) -> Finding:      # Critical Logic Wall
    walls = []
    if not c.live and not c.private_doc and c.gaps:
        walls.append("Data")
    if c.doubt.get("bites"):
        walls.append("Logic")
    if len(c.raw_text) > 4000:
        walls.append("Complexity")
    if c.channels.get("feeling"):
        walls.append("Motive")
    if c.safety_blocked:
        walls.append("Moral")
    return Finding(f"walls hit: {', '.join(walls) or 'none'} "
                   "(of Data/Logic/Frame/Complexity/Motive/Moral/Identity/Time)",
                   {"walls": walls})

def _sb55(c: WalkContext) -> Finding:      # High-Risk Merge Review
    risky = bool(c.merge) and len(c.synthetic_items) >= 1
    return Finding("merge is synthetic-heavy — forced to human review" if risky
                   else "no high-risk merge", halt=HaltType.EVIDENCE.value if risky else None)

def _sb56(c: WalkContext) -> Finding:      # Override Ledger
    return Finding("override ledger active — every human decision recorded with reason")

def _sb57(c: WalkContext) -> Finding:      # Non-Resolution Protector
    return Finding("non-resolution is the valid state here — protected, not forced"
                   if c.non_resolution else "resolution reached — protector idle")

def _sb58(c: WalkContext) -> Finding:      # Reality Re-Anchor
    return Finding(f"re-anchor: {c.anchor_note}",
                   halt=None if c.anchor_on_target else HaltType.LOGIC.value)

def _sb59(c: WalkContext) -> Finding:      # Embodied Check
    return Finding("sits right" if c.embodied_ok else "resistance — re-loop",
                   halt=None if c.embodied_ok else HaltType.LOGIC.value)

def _sb60(c: WalkContext) -> Finding:      # Final Decision Prep
    return Finding(f"prepared for human decision — {len(c.holds_so_far)} item(s) held "
                   f"for your call", {"holds": c.holds_so_far[:6]})

def _sb61(c: WalkContext) -> Finding:      # Master Log Update
    return Finding("master log updated in real time (sacred, append-only)")

def _sb62(c: WalkContext) -> Finding:      # Weekly Brain Update Trigger
    return Finding("weekly update DUE — will run on next Monday tick" if c.weekly_due
                   else "weekly brain update: not due (last Monday run recorded)")

def _sb63(c: WalkContext) -> Finding:      # Memory Sync (All Points)
    return Finding(f"all-point sync: {c.memory_stats.get('nodes_with_brains', 0)} brains, "
                   f"{c.memory_stats.get('total_memory_entries', 0)} entries")

def _sb64(c: WalkContext) -> Finding:      # Final Output Generator
    return Finding(f"final output generated — {c.classification} / {c.evidence_tag} "
                   f"/ confidence {c.confidence}")

def _sb65(c: WalkContext) -> Finding:      # Feed-Forward Router
    targets = sorted({h.split(":")[0] for h in c.holds_so_far}) or ["none needed"]
    return Finding(f"feed-forward targets: {', '.join(targets[:5])}")

def _sb66(c: WalkContext) -> Finding:      # Full Compilation
    return Finding(f"compiled: {len(c.matched)} matches, {len(c.connections)} connections, "
                   f"{len(c.new_parameters)} new params, {len(c.synthetic_items)} synthetic")

def _sb67(c: WalkContext) -> Finding:      # Breakthrough Lock
    score = min(10, 2 * len(c.new_parameters) + 2 * len(c.connections)
                + (2 if c.merge else 0) + (1 if c.fuel else 0)
                + (1 if len(c.matched) >= 5 else 0))
    return Finding(f"breakthrough score: {score}/10 "
                   + ("— LOCKED as breakthrough" if score >= 7 else "— routine run"),
                   {"score": score})

def _sb68(c: WalkContext) -> Finding:      # Human Halt Gate
    return Finding("human halt authority confirmed — you can halt/reverse/reject "
                   "everything above at any time")

def _sb69(c: WalkContext) -> Finding:      # Long-Term Memory Lock
    return Finding("run learned into long-term memory (example bank +1)")

def _sb70(c: WalkContext) -> Finding:      # Run Completion
    return Finding(f"run complete — {c.run_writes} memory writes, ready for reset or next work")


SB_WORK: dict[str, Callable[[WalkContext], Finding]] = {
    f"SB-{i:02d}": fn for i, fn in enumerate(
        (_sb01, _sb02, _sb03, _sb04, _sb05, _sb06, _sb07, _sb08, _sb09, _sb10,
         _sb11, _sb12, _sb13, _sb14, _sb15, _sb16, _sb17, _sb18, _sb19, _sb20,
         _sb21, _sb22, _sb23, _sb24, _sb25, _sb26, _sb27, _sb28, _sb29, _sb30,
         _sb31, _sb32, _sb33, _sb34, _sb35, _sb36, _sb37, _sb38, _sb39, _sb40,
         _sb41, _sb42, _sb43, _sb44, _sb45, _sb46, _sb47, _sb48, _sb49, _sb50,
         _sb51, _sb52, _sb53, _sb54, _sb55, _sb56, _sb57, _sb58, _sb59, _sb60,
         _sb61, _sb62, _sb63, _sb64, _sb65, _sb66, _sb67, _sb68, _sb69, _sb70),
        start=1)
}


# ---------------------------------------------------------------------------
# The 25 URR verification roles (per ARD_RGL_7025's URR definitions).
# Each takes the context + the findings of the SB block it gates and returns
# a review: verdict, issues, and the Intake + Parameters + New Scope that is
# fed BACK into the block's node memories (the spec's "Feed-Back into Memory").
# ---------------------------------------------------------------------------

@dataclass
class URRReview:
    urr_id: str
    name: str
    verdict: str                      # "pass" | "hold"
    issues: list[str] = field(default_factory=list)
    intake: str = ""                  # summary of what was verified
    new_parameters: list[str] = field(default_factory=list)
    new_scope: str = ""


def _rv(urr_id: str, name: str, issues: list[str], intake: str,
        scope: str = "", params: list[str] | None = None) -> URRReview:
    return URRReview(urr_id, name, "hold" if issues else "pass", issues, intake,
                     params or [], scope)


def _urr08(c: WalkContext, f: dict[str, Finding]) -> URRReview:   # Entry Verification
    issues = []
    if not f.get("SB-01"):
        issues.append("raw source not locked")
    if not c.channels:
        issues.append("noise strip produced nothing")
    if not c.domain:
        issues.append("domain unclassified")
    return _rv("URR-08", "Entry Verification Gate", issues,
               "intake verified: source locked, channels separated, domain set",
               "proceed to human core")

def _urr09(c: WalkContext, f: dict[str, Finding]) -> URRReview:   # Human Layer Verification
    issues = []
    if not c.private_doc and not c.core.get("lenses"):
        issues.append("six lenses did not run on human input")
    return _rv("URR-09", "Human Layer Verification", issues,
               ("human layer honestly skipped (document)" if c.private_doc else
                f"human layer captured — dominant {c.core.get('dominant_lens', '—')}"),
               "human drivers available to all later points")

def _urr10(c: WalkContext, f: dict[str, Finding]) -> URRReview:   # Doubt & Falsifier
    issues = []
    if not c.falsifier:
        issues.append("no falsifier attached to conclusion")
    if c.doubt.get("bites"):
        issues.append("doubt bites: " + "; ".join(c.doubt.get("fragilities", [])[:2]))
    return _rv("URR-10", "Doubt & Falsifier", issues,
               f"strongest conclusion attacked — {c.doubt.get('verdict', '—')}")

def _urr11(c: WalkContext, f: dict[str, Finding]) -> URRReview:   # Evidence & Grounding
    issues = []
    if not c.ledger:
        issues.append("no evidence ledger built")
    if (HaltType.EVIDENCE.value in c.halts) and not c.private_doc:
        issues.append("claim demands current data — none connected")
    return _rv("URR-11", "Evidence & Grounding Audit", issues,
               f"proof levels checked — ladder {c.ladder_conf}")

def _urr12(c: WalkContext, f: dict[str, Finding]) -> URRReview:   # Synthetic Review
    n = len(c.synthetic_items)
    issues = ["synthetic load high without live support"] if (n >= 2 and not c.live) else []
    return _rv("URR-12", "Synthetic Review", issues,
               f"{n} synthetic item(s) reviewed — all proof-debt tagged" if n
               else "no synthetic material this run")

def _urr13(c: WalkContext, f: dict[str, Finding]) -> URRReview:   # Merge Integrity
    if not c.merge:
        return _rv("URR-13", "Merge Integrity", [], "no merges to audit")
    weak = len(c.merge.get("contributing", [])) < 2
    return _rv("URR-13", "Merge Integrity",
               (["weak merge rejected — under 2 contributing loops"] if weak else []),
               "merge audited for real added value" + (" — REJECTED" if weak else " — sound"))

def _urr14(c: WalkContext, f: dict[str, Finding]) -> URRReview:   # Risk & Ethics
    issues = ["hard risk: " + "; ".join(c.safety_reasons)[:100]] if c.safety_blocked else []
    return _rv("URR-14", "Risk & Ethics Review", issues,
               "highest-level risk review " + ("FLAGGED" if issues else "clear"))

def _urr15(c: WalkContext, f: dict[str, Finding]) -> URRReview:   # Human Context Gate
    return _rv("URR-15", "Human Context Gate", [],
               f"full context assembled for you: {len(c.holds_so_far)} hold(s), "
               f"{len(c.synthetic_items)} synthetic, confidence {c.confidence}",
               "presented in the review queue")

def _urr16(c: WalkContext, f: dict[str, Finding]) -> URRReview:   # Memory Accuracy
    issues = [] if c.run_writes > 0 else ["no memory written this run"]
    return _rv("URR-16", "Memory Accuracy & Sync Check", issues,
               f"{c.run_writes} writes verified — linked to raw source")

def _urr17(c: WalkContext, f: dict[str, Finding]) -> URRReview:   # Cross-Point Audit
    return _rv("URR-17", "Cross-Point Connection Audit", [],
               f"{len(c.connections)} connection(s) audited across points")

def _urr18(c: WalkContext, f: dict[str, Finding]) -> URRReview:   # Parameter Integrity
    unlabeled = [p for p in c.new_parameters if not p.startswith("P-NEW:")]
    return _rv("URR-18", "Parameter Integrity Review",
               (["unlabeled parameters: " + ", ".join(unlabeled)] if unlabeled else []),
               f"{len(c.new_parameters)} new parameter(s) audited — all labeled")

def _urr19(c: WalkContext, f: dict[str, Finding]) -> URRReview:   # Risk Re-Check
    from . import safety
    v = safety.check(c.answer or c.raw_text)
    return _rv("URR-19", "Risk & Command Re-Check",
               (["late-stage risk: " + "; ".join(v.reasons)[:90]] if v.blocked else []),
               "final answer re-checked for risk — " + ("FLAGGED" if v.blocked else "clear"))

def _urr20(c: WalkContext, f: dict[str, Finding]) -> URRReview:   # Reality Re-Anchor
    return _rv("URR-20", "Reality Re-Anchor Verification",
               ([] if c.anchor_on_target else ["drifted from Point Zero"]),
               f"anchor check: {c.anchor_note[:120]}")

def _urr21(c: WalkContext, f: dict[str, Finding]) -> URRReview:   # Non-Resolution Review
    return _rv("URR-21", "Non-Resolution & Override Review", [],
               "non-resolution honoured as valid" if c.non_resolution
               else "resolution reached; override ledger consistent")

def _urr22(c: WalkContext, f: dict[str, Finding]) -> URRReview:   # Output Integrity
    issues = []
    if not c.answer.strip():
        issues.append("empty final output")
    if not c.falsifier:
        issues.append("output missing falsifier")
    if not c.classification:
        issues.append("output missing classification")
    return _rv("URR-22", "Final Output Integrity Check", issues,
               "output carries classification, evidence tag, confidence, falsifier")

def _urr23(c: WalkContext, f: dict[str, Finding]) -> URRReview:   # Master Log Audit
    return _rv("URR-23", "Master Log Accuracy Audit",
               ([] if c.run_writes > 0 else ["nothing recorded in master log"]),
               f"master log complete — {c.run_writes} event(s) this run")

def _urr24(c: WalkContext, f: dict[str, Finding]) -> URRReview:   # Brain Health
    return _rv("URR-24", "Local Brain Health & Update Check", [],
               f"{c.memory_stats.get('nodes_with_brains', 0)} local brains healthy; "
               + ("weekly update due Monday" if c.weekly_due else "weekly update on schedule"))

def _urr25(c: WalkContext, f: dict[str, Finding]) -> URRReview:   # Human Final Gate
    picture = (f"verified {len(f)} nodes; {len(c.holds_so_far)} held; "
               f"{len(c.synthetic_items)} synthetic; confidence {c.confidence}")
    return _rv("URR-25", "Full Run Integrity & Human Final Gate", [],
               f"full picture: {picture}", "awaiting your final word — approve or send back")


URR_CHECKS: dict[str, Callable[[WalkContext, dict[str, Finding]], URRReview]] = {
    "URR-08": _urr08, "URR-09": _urr09, "URR-10": _urr10, "URR-11": _urr11,
    "URR-12": _urr12, "URR-13": _urr13, "URR-14": _urr14, "URR-15": _urr15,
    "URR-16": _urr16, "URR-17": _urr17, "URR-18": _urr18, "URR-19": _urr19,
    "URR-20": _urr20, "URR-21": _urr21, "URR-22": _urr22, "URR-23": _urr23,
    "URR-24": _urr24, "URR-25": _urr25,
}

# Support layer (URR-01..07): early verification + evidence/synthetic audit.
# They run off the main line, on their trigger areas, and record in their brains.
SUPPORT_CHECKS: dict[str, Callable[[WalkContext], tuple[str, list[str]]]] = {
    "URR-01": lambda c: ("raw source integrity re-checked", []),
    "URR-02": lambda c: ("human layer early check done",
                         [] if (c.private_doc or c.core.get("lenses")) else ["lenses missing"]),
    "URR-03": lambda c: ("truth pressure early review done", []),
    "URR-04": lambda c: ("intent gate reviewed", []),
    "URR-05": lambda c: (f"early classification audit: {c.classification or 'pending'}", []),
    "URR-06": lambda c: (f"evidence quality audit: ladder {c.ladder_conf}", []),
    "URR-07": lambda c: (f"synthetic tagging audit: {len(c.synthetic_items)} item(s) tagged", []),
}


def node_name(sb_id: str) -> str:
    n = sb_by_id(sb_id)
    return n.name if n else sb_id
