"""SourcebornEngine — the control layer that binds the three memories.

It runs the SOURCEBORN operating flow (PRINCIPLE §IV) over the SB+URR node map:

    read & protect -> analyse true ask -> decompose -> bigger-picture triage
    -> example & wisdom match -> live grounding -> URR verify -> place -> deliver

The three memories it binds:
  * reflex  = the user's fed corpus + example bank (``Persona`` + ``Memory``)
  * instinct= the wisdom bank (``WisdomBank``)
  * eyes    = live fact (``grounding`` hook; pluggable)

Everything is written to the pyramid brains + Master Log, and every run teaches
the clone one more example (it gets wiser with use).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Callable

from . import safety
from .brains import BrainRegistry
from .core_gate import six_lenses
from .domain import classify_domain, audit_numeric
from .doubt import doubt_engine, falsifier as make_falsifier, witness
from .dots import dot_connections, merge_proposal
from .drift_guard import reality_reanchor
from .evidence import build_ledger, ladder_confidence
from .fuel import diagnose_stall, inject as inject_fuel
from .grounding import default_grounding
from .enums import (
    Classification, EvidenceTag, ForceFitRisk, HaltType, LoopType, PenetrationScore,
)
from .halt_map import loop_for_halt
from .llm import BaseModel, default_model
from .memory import Memory
from .models import (
    GapItem, MemoryEntry, Output, PointZero, ProofItem, RawSource, TraceEntry,
    URRPacket, _now,
)
from .node_work import (Finding, SB_WORK, SUPPORT_CHECKS, URR_CHECKS, URRReview,
                        WalkContext)
from .nodes import (FINAL_BLOCK_SB, FINAL_BLOCK_URR, SB_NODES, URR_NODES,
                    WALK_BLOCKS, sb_by_id)
from .pyramid import UnfiledQueue, file_finding, file_urr, unfiled_from_input
from .urr_matrix import MATRIX, review_node
from .parameters import COMPARISON_AXES, PARAMETER_BANK
from .persona import Persona
from .wisdom import WisdomBank

# ``live_override`` sentinel for the on-device private lane: skip live grounding
# entirely (never phone a third party like Tavily) WITHOUT faking a live fact —
# ``live`` stays empty, so the engine stays honest about having no current data.
NO_LIVE = "__no_live__"


@dataclass
class RunResult:
    output: Output
    micro_questions: list[str]
    matched_examples: list[str]
    trace: list[TraceEntry]
    gaps: list[GapItem]
    proofs: list[ProofItem]
    halts: list[str]


@dataclass
class NodeStep:
    """One SB checkpoint in the SB<->URR walk (your core loop diagram):
    the SB node does its work, a URR review verifies *that* node, and the node
    downloads the URR intake into its own memory before the walk advances
    (SB-N -> URR-N -> SB-N absorbs intake -> SB-N+1). A held node can be looped
    back to from the human review queue."""
    sb_id: str
    sb_name: str
    action: str
    urr_id: str
    verdict: str            # "pass" | "hold"
    halt: str | None
    why: str
    memory_written: bool
    can_loop_back: bool
    matrix_pass: int = 0                    # of the 25 URR filters (70×25 matrix)
    matrix_flags: list[str] = field(default_factory=list)   # "URR-10:absolutes"


class SourcebornEngine:
    def __init__(
        self,
        root: str = ".sourceborn",
        model: BaseModel | None = None,
        grounding: Callable[[str], str] | None = None,
    ) -> None:
        self.memory = Memory(root)
        self.brains = BrainRegistry(root)   # settings of all 70 SB + 25 URR brains
        self.persona = Persona(root)
        self.wisdom = WisdomBank(root)
        self.model = model or default_model()
        # live-fact hook (the "eyes"): Tavily if TAVILY_API_KEY set, else no-op.
        self.grounding = grounding or default_grounding()
        self.unfiled = UnfiledQueue(root)   # pyramid items awaiting the human
        self.trace: list[TraceEntry] = []

    # -- helpers -----------------------------------------------------------
    def _t(self, node_id: str, action: str, status: str = "running",
           halt: str | None = None, note: str = "") -> None:
        self.trace.append(TraceEntry(node_id, action, status, halt, note))

    @staticmethod
    def _decompose(text: str) -> list[str]:
        """Split a messy ask into micro-questions/claims (PRINCIPLE step 3)."""
        import re
        parts = re.split(r"(?<=[.?!;])\s+|\n+|\band\b|\bthen\b", text.strip())
        return [p.strip(" -•\t") for p in parts if len(p.strip()) > 3] or [text.strip()]

    @staticmethod
    def _noise_strip(text: str) -> dict[str, list[str]]:
        """SB-02: separate the raw ask into channels (kept, never discarded).

        Whole-word matching only — otherwise "Building Automation" lands in the
        invention channel (it contains "build") and a spec sheet's cells get
        dumped into the Wild Path. Word boundaries stop that misfire.
        """
        import re
        buckets: dict[str, list[str]] = {
            "fact": [], "feeling": [], "assumption": [], "pressure": [],
            "claim": [], "mystery": [], "invention_seed": [], "command": [],
        }

        def hit(low: str, words: tuple[str, ...]) -> bool:
            return any(re.search(r"\b" + re.escape(w) + r"\b", low) for w in words)

        for line in SourcebornEngine._decompose(text):
            low = line.lower()
            if hit(low, ("i feel", "thrill", "fear", "ego", "pain", "love")):
                buckets["feeling"].append(line)
            elif hit(low, ("must", "need", "want", "should", "have to")):
                buckets["command"].append(line)
            elif hit(low, ("maybe", "what if", "could", "consider")):
                buckets["assumption"].append(line)
            elif hit(low, ("invent", "new tool", "build", "create")):
                buckets["invention_seed"].append(line)
            elif hit(low, ("why", "mystery", "unknown", "how come")):
                buckets["mystery"].append(line)
            else:
                buckets["claim"].append(line)
        return {k: v for k, v in buckets.items() if v}

    # -- URR micro-pass ----------------------------------------------------
    def urr_micropass(self, urr_id: str, sb_node_id: str, content: str,
                      synthetic: bool = False, live: str | None = None,
                      private_doc: bool = False) -> URRPacket:
        """A verification gate: classify, score force-fit, detect halts.

        This is the rule-based URR. A model-backed URR can subclass / replace it.
        ``live`` lets a caller pass already-resolved live fact (or human-added
        data) so the evidence check honours it instead of re-querying.
        ``private_doc`` marks a provided file: the web cannot verify a private
        bill, so an Evidence halt there is the wrong gate (it would hold forever)
        — the document *is* the data; we review it, not chase a live source.
        """
        low = content.lower()
        classification = Classification.REVIEW_ONLY.value if private_doc \
            else Classification.CLAIM.value
        evidence = EvidenceTag.REVIEW.value
        force_fit = ForceFitRisk.LOW.value
        halt: str | None = None

        if synthetic:
            classification = Classification.SPECULATION.value
            evidence = EvidenceTag.SYNTHETIC.value
        if any(w in low for w in ("always", "everyone", "never", "guaranteed", "obviously")):
            force_fit = ForceFitRisk.HIGH.value
            halt = HaltType.LOGIC.value
        has_live = live if live is not None else self.grounding(content)
        if not private_doc and any(
                w in low for w in ("proof", "evidence", "data", "fact", "current")):
            if not has_live:
                halt = HaltType.EVIDENCE.value
        verdict = safety.check(content)
        risk_flags: list[str] = []
        if verdict.blocked:
            halt = HaltType.SAFETY.value
            risk_flags = verdict.reasons

        return URRPacket(
            urr_id=urr_id, sb_node_id=sb_node_id, classification=classification,
            evidence_tag=evidence, force_fit_risk=force_fit,
            halt_triggered=halt is not None, halt_type=halt, risk_flags=risk_flags,
            recommended_action="open_loop" if halt else "proceed",
            trace_note=f"URR {urr_id} on {sb_node_id}",
        )

    # -- the run -----------------------------------------------------------
    def run(self, raw_text: str, origin: str = "chat", public_safe: bool = False,
            learn: bool = True, model: BaseModel | None = None,
            live_override: str | None = None) -> RunResult:
        active_model = model or self.model
        self.trace = []
        gaps: list[GapItem] = []
        proofs: list[ProofItem] = []
        halts: list[str] = []

        # 0. SAFETY (hard boundary, mapped not executed) ------------------
        verdict = safety.check(raw_text)
        if verdict.blocked:
            self._t("SB-53", "risk_gate", "held", HaltType.SAFETY.value,
                    "; ".join(verdict.reasons))

        # 1. READ & PROTECT — SB-01 Point Zero Lock, SB-04 preserve --------
        raw = RawSource(text=raw_text, origin=origin).lock()
        self.memory.write("SB-01", MemoryEntry(
            node_id="SB-01", raw_source_id=raw.raw_source_id, content=raw_text,
            classification=Classification.REVIEW_ONLY.value,
            evidence_tag=EvidenceTag.OPEN.value, tags=["raw_source", "locked"],
        ), name="Point Zero Lock")
        pz = PointZero(raw_source_id=raw.raw_source_id, literal_ask=raw_text[:200])
        pz.locked = True
        self._t("SB-01", "point_zero_lock", "running", note="raw source locked")

        # 2. NOISE STRIP — SB-02 ------------------------------------------
        channels = self._noise_strip(raw_text)
        self.memory.write("SB-02", MemoryEntry(
            node_id="SB-02", raw_source_id=raw.raw_source_id,
            content="noise-stripped channels", parameters={"channels": channels},
            pyramid={"main": list(channels.keys()), "sub": [], "micro": []},
        ), name="Noise & Static Stripper")
        self._t("SB-02", "noise_strip", "running", note=",".join(channels))

        # 3. DECOMPOSE into micro-questions -------------------------------
        micro = self._decompose(raw_text)
        self._t("SB-02", "decompose", "running", note=f"{len(micro)} micro-questions")

        # 4. SOURCE-DOMAIN CLASSIFY (SB-03): what KIND of source is this? -
        # A numeric/financial document is audited; prose/a claim is read by the
        # lenses. This is the split that stops a bill being psychoanalysed.
        dom = classify_domain(raw_text, origin)
        private_doc = dom["audit_applicable"]
        audit = audit_numeric(raw_text) if private_doc else None
        self._t("SB-03", "source_domain", "running", note=dom["label"])

        # TRIAGE routine vs deep
        deep = len(micro) > 1 or any(
            w in raw_text.lower() for w in ("why", "prove", "mystery", "invent", "rh", "theory")
        )
        self._t("SB-03", "triage", "running", note="deep" if deep else "routine")

        # 4b. CORE GATE — SB-10. Read the human under the words ONLY for prose /
        # a claim. A numeric document is audited, not psychoanalysed — force-
        # fitting a lens onto numbers is exactly the divert the core forbids.
        if dom["lens_applicable"]:
            core = six_lenses(raw_text)
        else:
            core = {"lenses": {}, "active_count": 0,
                    "dominant_lens": f"{dom['label']} — audited, not psychoanalysed"}
        self.memory.write("SB-10", MemoryEntry(
            node_id="SB-10", raw_source_id=raw.raw_source_id,
            content=f"core gate dominant lens: {core['dominant_lens']}",
            parameters={"lenses": core["lenses"], "domain": dom["domain"]},
            pyramid={"main": [k for k, v in core["lenses"].items() if v["active"]],
                     "sub": [], "micro": []},
            tags=["core_gate", "human_layer"],
        ), name="Core Gate — Six Lenses")
        self._t("SB-10", "core_gate", "running",
                note=(f"dominant: {core['dominant_lens']} ({core['active_count']}/6 lenses)"
                      if dom["lens_applicable"]
                      else f"numeric audit — {audit['summary'] if audit else ''}"))

        # 5. EXAMPLE & WISDOM MATCH (the heart) ---------------------------
        matched: list[str] = []
        seen: set[str] = set()
        per_part_refs: list[list[str]] = []
        for mq in micro:
            refs: list[str] = []
            for ex in self.persona.recall(mq):            # reflex (your corpus)
                refs.append(ex.question[:60])
                item = f"corpus: {ex.question[:60]}"
                if item not in seen:
                    seen.add(item); matched.append(item)
            for score, w, axes in self.wisdom.match(mq):  # instinct (wisdom)
                item = f"{w.source}: {w.pattern[:70]} [axes: {', '.join(axes) or '—'}]"
                if item not in seen:
                    seen.add(item); matched.append(item)
            per_part_refs.append(refs)
        self.memory.write("SB-32", MemoryEntry(
            node_id="SB-32", raw_source_id=raw.raw_source_id,
            content="example & wisdom match", parameters={"matched": matched},
            tags=["example_match"],
        ), name="Literature & Historical Pattern Hunter")
        self._t("SB-32", "example_wisdom_match", "running", note=f"{len(matched)} matches")

        # 5b. DOT CONNECTION + MERGE (SB-37/40): sources recurring across parts
        connections = dot_connections(per_part_refs)
        merge = merge_proposal(connections)
        if connections:
            self._t("SB-37", "dot_connection", "running",
                    note=f"{len(connections)} cross-links")
        if merge:
            self.memory.master_log({"event": "merge_proposal",
                                    "contributing": merge["contributing"]})
            self._t("SB-40", "merge_proposal", "held", note="needs human gate")

        # 6. LIVE GROUNDING — SB-33 (pluggable eyes; human-added data wins) -
        if live_override == NO_LIVE:        # on-device private lane: never phone out
            live = ""                       # honest: no live fact, and none faked
        elif private_doc:                   # a private file: the web can't see it
            live = ""                       # we review the document, not chase Tavily
        else:
            live = live_override or self.grounding(raw_text)
        # Only a public claim opens an Evidence gap. A provided document IS the
        # data — demanding a live web source for a private bill holds it forever.
        if not live and deep and not private_doc:
            gaps.append(GapItem("No live fact source connected", "Evidence", "Medium",
                                LoopType.EVIDENCE.value))
        if private_doc:
            self._t("SB-33", "live_grounding", "running",
                    note="private document — internal-consistency checked; web grounding N/A")
        else:
            self._t("SB-33", "live_grounding", "running" if live else "gap_open",
                    note="live data" if live else "no live source")

        # Stage 4 — Evidence ladder + source tags (SB-29)
        corpus_refs = [m[8:] for m in matched if m.startswith("corpus:")]
        ledger = build_ledger(micro, bool(live), corpus_refs)
        ladder_conf = ladder_confidence(ledger)
        self._t("SB-29", "evidence_ledger", "running",
                note=f"ladder confidence {ladder_conf}")

        # 7. URR VERIFY ----------------------------------------------------
        packet = self.urr_micropass("URR-08", "SB-08", raw_text, live=live,
                                    private_doc=private_doc)
        if packet.halt_triggered:
            halts.append(packet.halt_type or "")
            loop = loop_for_halt(HaltType(packet.halt_type))
            self.memory.master_log({"event": "halt", "type": packet.halt_type,
                                    "new_loop": loop.value})
            self._t("URR-08", "verify", "held", packet.halt_type,
                    f"opened {loop.value}")
            if packet.halt_type == HaltType.EVIDENCE.value:
                gaps.append(GapItem("Evidence halt at URR-08", "Evidence", "High",
                                    loop.value))
        else:
            self._t("URR-08", "verify", "passed", note=packet.classification)

        # 8. PLACE — build the output prompt. A numeric/financial document gets
        # an AUDIT instruction plus the figures computed in Python, so even a
        # weak or offline model states real numbers, never psychology. Prose / a
        # claim keeps the direct-answer + falsifier shape.
        if private_doc:
            prompt = (
                "You are reviewing a NUMERIC / FINANCIAL DOCUMENT, not a personal "
                "claim. Do NOT psychoanalyse it (no Mask/Wound/loyalty language). "
                "Be concrete and use the AUDIT figures below — invent nothing.\n"
                "1) 'Direct answer:' — in 1-2 sentences, what this document is and "
                "its headline figure (the likely grand total).\n"
                "2) 'Reads:' — the key figures: total, any GST/tax, and the "
                "negative/correction entries and what they do to the payable.\n"
                "3) 'Cannot verify:' — state plainly what can't be confirmed "
                "without the structured sheet or the source contract/BOQ; never "
                "claim the bill is correct.\n"
                "4) End with one 'Falsifier:' line.\n"
                f"DOCUMENT (excerpt): {raw_text[:1500]}\n"
                f"AUDIT (computed, trustworthy): {audit}\n"
                f"MATCHED EXAMPLES: {matched[:3]}"
            )
        else:
            prompt = (
                "Answer in the user's voice. These RULES fix known weak spots — be "
                "DIRECT, BRIEF, technically precise, and name your evidence:\n"
                "1) Open with 'Direct answer:' — 1-3 sentences that answer the literal "
                "ASK concretely (the key-in-hand). No preamble, no throat-clearing.\n"
                "2) Then at most ONE short 'Why:' paragraph — the deeper reason from "
                "the matched example. Stop there; do not pad, repeat, or sermonise.\n"
                "3) Name any structure / number / figure you used as evidence. If there "
                "is no live fact, say so in one clause — never invent it.\n"
                "4) End with one 'Falsifier:' line — the fact that would prove it wrong.\n"
                f"ASK: {raw_text}\n"
                f"MATCHED EXAMPLES (eternal): {matched}\n"
                f"LIVE FACT: {live or 'none — say so, do not invent'}\n"
                f"CORE GATE dominant lens: {core['dominant_lens']}; active: "
                f"{[k for k, v in core['lenses'].items() if v['active']]}\n"
                f"EVIDENCE: {ladder_conf} (rungs {[e['evidence_tag'] for e in ledger]})"
            )
        draft = active_model.complete(system=self.persona.voice_guidance(), prompt=prompt)

        # Stage 3 — Doubt Engine + Witness (SB-20/22): attack before delivery
        doubt = doubt_engine(draft, bool(live), len(matched))
        blind = witness([t.node_id for t in self.trace],
                        core["dominant_lens"], bool(live))
        self._t("SB-20", "doubt_engine", "held" if doubt["bites"] else "passed",
                note=doubt["verdict"])
        self._t("SB-22", "witness", "running", note=blind[0])

        # Stage 6 — Synthetic Fuel if stalled (SB-45): force motion, never fake fact
        stall = diagnose_stall(halts, bool(live), len(matched), doubt["bites"])
        fuel_item = inject_fuel(stall, raw_text) if stall else None
        if fuel_item:
            self._t("SB-45", "synthetic_fuel", "synthetic_assumption_active",
                    note=fuel_item["fuel"])

        # Stage 7 — Embodied Check (SB-59) + Non-Resolution Protector (SB-57).
        # The body resists on real doubt or a hard halt (safety/logic) — NOT
        # merely because no web source was attached. That old echo turned one
        # missing-source gap into two separate holds.
        hard_halt = any(h in (HaltType.SAFETY.value, HaltType.LOGIC.value)
                        for h in halts)
        embodied_ok = not (doubt["bites"] or hard_halt)
        self._t("SB-59", "embodied_check", "passed" if embodied_ok else "held",
                note="sits right" if embodied_ok else "resistance — re-loop")
        non_resolution = bool(halts) and not live and doubt["bites"]
        if non_resolution:                     # Principle 2: holding is valid
            self._t("SB-57", "non_resolution_protector", "running",
                    note="valid hold / incubate — do not force a product")

        lanes = {
            "reality_path": {
                "known": (audit["summary"] if (private_doc and audit)
                          else (live or "needs live source")),
                "what_would_prove_it": ("the structured sheet / source contract (BOQ)"
                                        if private_doc else "live web grounding (Tavily)")},
            # Cap the wild path and never feed a document's raw cells into it.
            "wild_path": {"preserved": [] if private_doc else
                          (channels.get("invention_seed", []) +
                           channels.get("mystery", []))[:8]},
            "classification": packet.classification,
            "sequence_path": [n.sb_id for n in SB_NODES[:8]],
            # citations — every claim is backed below it (the grounding pyramid)
            "corpus_citations": [m[8:] for m in matched if m.startswith("corpus:")][:5],
            "wisdom_citations": [m for m in matched if not m.startswith("corpus:")][:5],
            # Core Gate reading (the human under the words)
            "human_layer": {"dominant_lens": core["dominant_lens"],
                            "active": {k: v["reading"] for k, v in
                                       core["lenses"].items() if v["active"]}},
            # Stage 3-6 depth
            "evidence_ledger": ledger,
            "connections": connections,
            "merge_proposal": merge,
            "doubt": doubt,
            "witness": blind,
            "synthetic_fuel": fuel_item,
            "embodied_check": "sits right" if embodied_ok else "resistance — re-loop",
            "non_resolution": non_resolution,
            "domain": {"domain": dom["domain"], "label": dom["label"]},
        }
        if audit is not None:
            lanes["audit"] = audit
        if verdict.blocked:
            lanes["safety"] = verdict.safe_mapping

        # 8b. REALITY RE-ANCHOR — anti-divert (SB-58): did we drift from Point Zero?
        # A document audit is anchored to the document by construction, so it
        # cannot "drift" the way a free reasoning chain can.
        anchor = reality_reanchor(pz.literal_ask, draft)
        on_target = anchor.on_target or private_doc
        anchor_note = "audit anchored to the document" if private_doc else anchor.note
        lanes["reality_reanchor"] = anchor_note
        self._t("SB-58", "reality_reanchor",
                "passed" if on_target else "held", note=anchor_note)

        # 9. DELIVER -------------------------------------------------------
        # A reviewed document is REVIEW_ONLY at Medium (we read and checked what
        # it states) — honest, not the forced Low it used to get for lacking a
        # web source, and never High (we can't certify it without the contract).
        if private_doc:
            classification_out = Classification.REVIEW_ONLY.value
            confidence_out = "Low" if doubt["bites"] else "Medium"
        else:
            classification_out = (Classification.REVIEW_ONLY.value if non_resolution
                                  else packet.classification)
            confidence_out = "Low" if (doubt["bites"] or gaps or halts) else ladder_conf
        out = Output(
            answer=draft,
            lanes=lanes,
            evidence_tag=packet.evidence_tag,
            classification=classification_out,
            confidence=confidence_out,
            falsifier=make_falsifier(raw_text),
            penetration_score=(PenetrationScore.PENETRATED.value if deep
                               else PenetrationScore.SHALLOW.value),
            open_question=("Held — non-resolution is valid here; needs evidence or "
                           "incubation (Principle 2)." if non_resolution
                           else (channels.get("mystery", [""])[0]
                                 if "mystery" in channels else "")),
            public_safe=public_safe,
            matched_examples=matched,
        )
        self.memory.write("SB-64", MemoryEntry(
            node_id="SB-64", raw_source_id=raw.raw_source_id, content=out.answer,
            classification=out.classification, evidence_tag=out.evidence_tag,
            parameters={"penetration": out.penetration_score, "confidence": out.confidence},
            tags=["final_output"],
        ), name="Final Output Generator")
        self._t("SB-64", "deliver", "passed", note=out.evidence_tag)

        # COMPOUND: the clone learns one more example (gets wiser with use) -
        if learn:
            self.persona.learn(raw_text, out.answer, note="auto-learned from run",
                               classification=out.classification)
            self._t("SB-69", "long_term_memory_lock", "passed",
                    note="example bank +1")

        # Stash the run's working state so run_walk can drive every node's OWN
        # work from real data (ARD_RGL_7025: every node does its own job).
        from . import scheduler as _sched
        self._ctx = {
            "raw_text": raw_text, "origin": origin, "answer": out.answer,
            "channels": channels, "domain": dom, "audit": audit, "core": core,
            "matched": matched, "ledger": ledger, "ladder_conf": ladder_conf,
            "live": live, "doubt": doubt, "witness": blind,
            "falsifier": out.falsifier, "fuel": fuel_item,
            "connections": connections, "merge": merge, "halts": halts,
            "gaps": gaps, "anchor_note": anchor_note,
            "anchor_on_target": on_target, "non_resolution": non_resolution,
            "embodied_ok": embodied_ok, "safety_blocked": verdict.blocked,
            "safety_reasons": verdict.reasons, "private_doc": private_doc,
            "classification": out.classification, "confidence": out.confidence,
            "evidence_tag": out.evidence_tag,
            "weekly_due": _sched.due(self.memory.root),
        }

        return RunResult(out, micro, matched, list(self.trace), gaps, proofs, halts)

    # -- RGL: Recursive Genesis Loop ---------------------------------------
    def run_recursive(self, raw_text: str, loops: int = 3,
                      model: BaseModel | None = None, converge: float = 0.30) -> dict:
        """The RGL (RGL.txt): the loop's shape is invariant, the content
        compounds. Each pass's Point Zero carries the previous pass's product;
        it re-opens up to ``loops`` times, stopping early when the product stops
        changing (convergence). Only the final pass teaches the clone.
        """
        history: list[dict] = []
        product = ""
        last: RunResult | None = None
        converged = False
        n = max(1, loops)
        for i in range(n):
            text = raw_text if not product else (
                f"{raw_text}\n\n[carry-forward from loop {i}] {product[:400]}")
            last = self.run(text, learn=(i == n - 1), model=model)
            history.append({
                "loop": i + 1, "answer": last.output.answer,
                "confidence": last.output.confidence,
                "penetration": last.output.penetration_score,
            })
            if product:
                drift = reality_reanchor(product, last.output.answer).drift_score
                if drift < converge:
                    converged = True
                    product = last.output.answer
                    break
            product = last.output.answer
        return {"result": last, "recursion": {
            "loop_count": len(history), "converged": converged, "history": history}}

    @staticmethod
    def _walk_ask(node_id: str, halt: str | None, target: str) -> dict:
        """The human gate, made explicit: tell the user exactly *what* to give,
        *why*, *how*, and *when* — so a hold is never a blank 'Evidence'."""
        h = halt or ""
        if h == HaltType.EVIDENCE.value or node_id == "SB-33":
            return {"what": "A current source or data point that backs the claim",
                    "why": "The claim isn't grounded in live fact yet (stays Low)",
                    "how": "Paste a link, figure or number below — or upload the source file",
                    "when": "Now — before it can be rated FACT",
                    "options": ["Paste a source/number, then Add data & re-run",
                                "Mark it a Belief (unproven) and continue",
                                "Re-loop this node to search again"],
                    "for": target}
        if h == HaltType.SAFETY.value:
            return {"what": "The legitimate context / authorization",
                    "why": "This touches a hard safety line — it is mapped, never executed",
                    "how": "State who you are and the lawful purpose",
                    "when": "Before anything proceeds",
                    "options": ["State who you are + lawful purpose",
                                "Keep it mapped only (don't execute)",
                                "Drop this line and re-loop"],
                    "for": target}
        if h == HaltType.LOGIC.value:
            return {"what": "Proof for the absolute claim, or softer wording",
                    "why": "An over-claim (always / never / guaranteed) was detected",
                    "how": "Give a counter-example test, or qualify the statement",
                    "when": "Now",
                    "options": ["Soften the absolute (drop always/never)",
                                "Give a counter-example test",
                                "Approve as a Claim, not a Fact"],
                    "for": target}
        if node_id == "SB-40":
            return {"what": "Your approval to merge the connected sources",
                    "why": "Two or more sources recur — a merge needs a human gate",
                    "how": "Approve to combine them, or re-loop to keep them separate",
                    "when": "Now",
                    "options": ["Approve the merge",
                                "Keep sources separate (re-loop)",
                                "Add a third source first"],
                    "for": target}
        return {"what": "Your read on whether this holds",
                "why": "Doubt bit or the node didn't sit right",
                "how": "Add a note/data, re-loop, or approve as-is",
                "when": "Now",
                "options": ["Approve as-is",
                            "Add a note/data, then re-run",
                            "Re-loop this node"],
                "for": target}

    def run_walk(self, raw_text: str, model: BaseModel | None = None,
                 live_override: str | None = None) -> dict:
        """The real ARD_RGL_7025 walk — the 6+1 sequential arrow chart:

            SB-01..08 → URR-08 (Entry Verification, first gate)
            SB-09..14 → URR-09 (Human Layer) … blocks of six …
            SB-69..70 → URR-19..25 (the Final 6+1 Block → Human Final Gate)

        Every SB point runs ITS OWN job on the run context and writes ITS OWN
        finding into ITS OWN local brain — no shared stamp. Every URR gate runs
        ITS OWN verification role over its block, then returns Intake +
        Parameters + New Scope which each block node downloads into memory
        (the spec's Feed-Back into Memory). URR-01..07 run as the support
        layer on their trigger areas. Brain parameters from the core document
        (Runs_Completed, Verifications_Performed, Issues_Found, …) update on
        every pass, so each brain's storage genuinely grows with use.
        """
        res = self.run(raw_text, model=model, live_override=live_override)
        rc = getattr(self, "_ctx", {})
        ctx = WalkContext(**rc)
        ctx.memory_stats = self.memory.stats()
        # Dot-connection inputs: cross-brain memory hits + similar past asks.
        try:
            key = " ".join(w for w in raw_text.split()[:4] if len(w) > 3) or raw_text[:24]
            ctx.memory_hits = [(nid, (e.content or "")[:80])
                               for nid, e in self.memory.search(key)[:8]]
        except Exception:
            ctx.memory_hits = []
        try:
            ctx.recall_matches = [ex.question[:80] for ex in self.persona.recall(raw_text)][:5]
        except Exception:
            ctx.recall_matches = []

        steps: list[NodeStep] = []
        holds: list[dict] = []
        blocks: list[dict] = []
        findings: dict[str, Finding] = {}
        matrix_by_urr: dict[str, int] = {}
        matrix_flagged: list[dict] = []
        matrix_total_flags = 0

        def run_sb(sb_id: str, gate: str) -> None:
            nonlocal matrix_total_flags
            cfg = self.brains.get(sb_id)
            name = cfg.name if cfg else sb_id
            node = sb_by_id(sb_id)
            try:
                f = SB_WORK[sb_id](ctx)
            except Exception as exc:                 # a node must never kill the walk
                f = Finding(f"node error: {exc}", halt=HaltType.LOGIC.value)
            findings[sb_id] = f
            # 70×25 matrix: ALL 25 URR filters review THIS node's finding.
            flags = review_node(sb_id, f, ctx)
            matrix_total_flags += len(flags)
            for uid, code in flags.items():
                matrix_by_urr[uid] = matrix_by_urr.get(uid, 0) + 1
                if len(matrix_flagged) < 60:
                    matrix_flagged.append({"sb": sb_id, "urr": uid, "code": code})
            # Pyramid of Thought: file the finding (Main → Sub → Micro).
            pyr = file_finding(node.stage if node else 8, f.text, f.params)
            # approved new parameters file as their own sub buckets — the
            # pyramid genuinely grows once the human approves a novelty term
            low_text = f.text.lower()
            for term in approved:
                if term in low_text and f"P-NEW:{term}" not in pyr["sub"]:
                    pyr["sub"].append(f"P-NEW:{term}")
            params = dict(f.params)
            if flags:
                params["urr_matrix_flags"] = flags
            params["matrix_pass"] = len(MATRIX) - len(flags)
            # THIS node's own finding goes into THIS node's brain.
            self.memory.write(sb_id, MemoryEntry(
                node_id=sb_id, raw_source_id="", content=f.text[:500],
                parameters=params, pyramid=pyr, tags=["node_finding"]), name=name)
            self.memory.brain(sb_id).bump("Runs_Completed")
            if f.params:
                self.memory.brain(sb_id).bump("Patterns_Recognized")
            ctx.run_writes += 1
            verdict = "hold" if f.halt else "pass"
            if f.halt:
                ctx.holds_so_far.append(f"{sb_id}: {f.text[:60]}")
                holds.append({"sb_id": sb_id, "name": name, "urr_id": gate,
                              "why": f.text[:180], "halt": f.halt,
                              "ask": self._walk_ask(sb_id, f.halt, name)})
            steps.append(NodeStep(
                sb_id=sb_id, sb_name=name, action="node_work", urr_id=gate,
                verdict=verdict, halt=f.halt, why=f.text[:220],
                memory_written=True, can_loop_back=(verdict == "hold"),
                matrix_pass=len(MATRIX) - len(flags),
                matrix_flags=[f"{u}:{c}" for u, c in flags.items()]))

        def run_urr(urr_id: str, block_sb: tuple[str, ...]) -> URRReview:
            review = URR_CHECKS[urr_id](ctx, findings)
            ub = self.memory.brain(urr_id, review.name)
            ub.bump("Verifications_Performed")
            if review.issues:
                ub.bump("Issues_Found", len(review.issues))
            if review.verdict == "hold":
                ub.bump("Human_Reviews_Triggered")
            self.memory.write(urr_id, MemoryEntry(
                node_id=urr_id, raw_source_id="",
                content=f"[{review.verdict}] {review.intake}"[:400],
                parameters={"issues": review.issues, "scope": review.new_scope},
                tags=["urr_review"]), name=review.name)
            ctx.run_writes += 1
            # Feed-Back into Memory: every block node downloads the URR intake.
            for sb_id in block_sb:
                self.memory.write(sb_id, MemoryEntry(
                    node_id=sb_id, raw_source_id="",
                    content=f"URR intake [{review.verdict}] from {urr_id}: "
                            f"{review.intake}"[:300],
                    parameters={"urr_id": urr_id, "verdict": review.verdict,
                                "new_scope": review.new_scope},
                    tags=["urr_intake"]), name="URR Intake Download")
                ctx.run_writes += 1
            if review.verdict == "hold":
                ctx.holds_so_far.append(f"{urr_id}: {'; '.join(review.issues)[:60]}")
                halt = (HaltType.SAFETY.value if urr_id in ("URR-14", "URR-19")
                        else HaltType.EVIDENCE.value)
                holds.append({"sb_id": urr_id, "name": review.name,
                              "urr_id": urr_id,
                              "why": "; ".join(review.issues)[:180], "halt": halt,
                              "ask": self._walk_ask(urr_id, halt, review.name)})
            blocks.append({"gate": urr_id, "name": review.name,
                           "sb": list(block_sb), "verdict": review.verdict,
                           "issues": review.issues, "intake": review.intake,
                           "new_scope": review.new_scope})
            return review

        # Human-approved new parameters (novelty pass): they park from now on.
        from .novelty import approved_terms
        approved = approved_terms(self.memory.root)

        # The USER's words the pyramid cannot park yet → the human review
        # queue at SB-02 (where input is separated). Never discarded.
        self.unfiled.add("SB-02",
                         unfiled_from_input(raw_text, extra_known=approved),
                         _now())

        # ---- the main sequential line (6+1 grouping) ----------------------
        for gate, block_sb in WALK_BLOCKS:
            for sb_id in block_sb:
                run_sb(sb_id, gate)
            run_urr(gate, block_sb)
            # support layer triggers (per the spec's summary table)
            if gate == "URR-09":                      # after Stage 1-2
                for uid in ("URR-01", "URR-02", "URR-03", "URR-04", "URR-05"):
                    note, issues = SUPPORT_CHECKS[uid](ctx)
                    ub = self.memory.brain(uid)
                    ub.bump("Verifications_Performed")
                    if issues:
                        ub.bump("Issues_Found", len(issues))
            if gate == "URR-14":                      # after Stage 4-5
                for uid in ("URR-06", "URR-07"):
                    note, issues = SUPPORT_CHECKS[uid](ctx)
                    ub = self.memory.brain(uid)
                    ub.bump("Verifications_Performed")
                    if issues:
                        ub.bump("Issues_Found", len(issues))

        # ---- closing: SB-69..70 then the Final 6+1 Block (URR-19..25) -----
        for sb_id in FINAL_BLOCK_SB:
            run_sb(sb_id, "URR-25")
        for urr_id in FINAL_BLOCK_URR:
            run_urr(urr_id, FINAL_BLOCK_SB)

        # ---- 70×25 matrix close-out: each URR brain records ITS sweep -----
        urr_names = {n.urr_id: n.name for n in URR_NODES}
        n_nodes = len(steps)
        for uid in MATRIX:
            nflags = matrix_by_urr.get(uid, 0)
            ub = self.memory.brain(uid, urr_names.get(uid, uid))
            ub.bump("Verifications_Performed", n_nodes)
            if nflags:
                ub.bump("Issues_Found", nflags)
            codes = sorted({m["code"] for m in matrix_flagged if m["urr"] == uid})
            self.memory.write(uid, MemoryEntry(
                node_id=uid, raw_source_id="",
                content=f"matrix sweep over {n_nodes} nodes: "
                        f"{n_nodes - nflags} pass, {nflags} flagged"
                        + (f" ({', '.join(codes[:4])})" if codes else ""),
                parameters={"flagged": nflags},
                pyramid=file_urr(urr_names.get(uid, uid),
                                 "flag" if nflags else "pass", codes),
                tags=["urr_matrix"]), name=urr_names.get(uid, uid))
            ctx.run_writes += 1

        self.memory.master_log({"event": "walk_complete",
                                "nodes": len(steps), "urr_gates": len(blocks),
                                "matrix_reviews": n_nodes * len(MATRIX),
                                "matrix_flags": matrix_total_flags,
                                "holds": len(holds)})
        return {"result": res, "walk": {
            "steps": [asdict(s) for s in steps], "holds": holds,
            "blocks": blocks,
            "matrix": {"per_node": len(MATRIX),
                       "total": n_nodes * len(MATRIX),
                       "flags": matrix_total_flags,
                       "by_urr": matrix_by_urr,
                       "flagged": matrix_flagged},
            "node_count": len(steps), "hold_count": len(holds),
            "urr_count": len(blocks)}}
