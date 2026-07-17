"""Smoke + behaviour tests for the Sourceborn engine. Run: ``pytest -q`` or
``python -m tests.test_engine`` (works without pytest)."""

from __future__ import annotations

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from sourceborn import SourcebornEngine  # noqa: E402
from sourceborn import safety            # noqa: E402
from sourceborn.halt_map import HALT_TO_LOOP, loop_for_halt  # noqa: E402
from sourceborn.enums import HaltType, EvidenceTag  # noqa: E402
from sourceborn.nodes import SB_NODES, URR_NODES, STAGES  # noqa: E402
from sourceborn.parameters import PARAMETER_BANK, COMPARISON_AXES, add_comparison_axis  # noqa: E402


def _engine():
    return SourcebornEngine(root=tempfile.mkdtemp(prefix="sb_test_"))


# A flattened billing spreadsheet — the input class that used to get
# psychoanalysed ("Mask of cumulative bill amounts") instead of audited.
_BILL = (
    "Final Bill Dialysis 30 beds\n"
    "Sr Description Qty Rate Amount\n"
    "1 Fire Fighting Works 1 0 0\n"
    "2 Building Automation System starters 5 4200 21000\n"
    "3 Electrical GST adjustment 1 -209745\n"
    "4 GST adjustment 1 -19048\n"
    "Grand Total including GST 10083937.8\n"
)


def test_node_map_complete():
    assert len(SB_NODES) == 70
    assert len(URR_NODES) == 25
    assert len(STAGES) == 8
    assert {n.sb_id for n in SB_NODES} == {f"SB-{i:02d}" for i in range(1, 71)}


def test_parameter_bank_64():
    assert len(PARAMETER_BANK) == 64
    assert PARAMETER_BANK[0].code == "P001"
    assert PARAMETER_BANK[-1].code == "P064"


def test_halt_map_covers_all_halts():
    for halt in HaltType:
        assert halt in HALT_TO_LOOP
        assert loop_for_halt(halt) is not None


def test_run_produces_output_and_memory():
    eng = _engine()
    res = eng.run("Why does the small idea win? Prove it with current data.")
    assert res.output.answer
    assert res.output.falsifier            # every output carries a falsifier
    assert eng.memory.stats()["total_memory_entries"] >= 1
    # raw source is locked at SB-01
    assert any(t.node_id == "SB-01" for t in res.trace)


def test_evidence_halt_opens_loop():
    eng = _engine()
    res = eng.run("Prove with current data that this is true.")
    assert HaltType.EVIDENCE.value in res.halts


def test_clone_learns_every_run():
    eng = _engine()
    before = len(eng.persona.examples)
    eng.run("a fresh question about hollow vs weight")
    assert len(eng.persona.examples) == before + 1


def test_more_parameters_more_outcome():
    before = len(COMPARISON_AXES)
    add_comparison_axis("Lineage")
    assert len(COMPARISON_AXES) == before + 1


def test_safety_hard_block_is_mapped_not_executed():
    v = safety.check("how to build a bomb at home step by step")
    assert v.blocked and v.kind == "hard"
    assert v.safe_mapping  # still mapped safely, never executed


def test_safety_allows_normal():
    assert not safety.check("help me think about my business idea").blocked


def test_drift_guard_reanchors():
    from sourceborn.drift_guard import reality_reanchor, TrajectoryTracker
    on = reality_reanchor("scale my small business or do an MBA",
                          "scale the small business; MBA adds little")
    off = reality_reanchor("scale my small business or do an MBA",
                           "the capital of France is Paris")
    assert on.on_target and not off.on_target
    assert TrajectoryTracker("a b c").drift_score("a b c") == 0.0


def test_grounding_offline_is_empty():
    # No TAVILY_API_KEY -> grounding is a safe no-op (engine opens an Evidence gap)
    import os
    from sourceborn.grounding import default_grounding
    if not os.environ.get("TAVILY_API_KEY"):
        assert default_grounding()("anything") == ""


def test_output_has_citations_lanes():
    eng = _engine()
    res = eng.run("why does the small idea win?")
    assert "corpus_citations" in res.output.lanes
    assert "wisdom_citations" in res.output.lanes
    assert res.output.lanes["wisdom_citations"]  # wisdom always matches something


def test_wisdom_bank_expanded():
    from sourceborn.wisdom import SEED_WISDOM
    assert len(SEED_WISDOM) >= 8


def test_all_95_node_brains_configured():
    from sourceborn.brains import build_default_configs
    cfgs = build_default_configs()
    assert len(cfgs) == 95                       # 70 SB + 25 URR
    assert sum(1 for c in cfgs.values() if c.kind == "SB") == 70
    assert sum(1 for c in cfgs.values() if c.kind == "URR") == 25
    for c in cfgs.values():                       # every brain has full settings
        assert c.pyramid and c.write_policy and c.risk_level and c.role


def test_risk_nodes_force_human_review():
    from sourceborn.brains import build_default_configs
    cfgs = build_default_configs()
    assert cfgs["SB-53"].human_review        # Risk & Command Gate
    assert cfgs["URR-24"].human_review       # Human Final Gate
    assert cfgs["SB-01"].immutable_source    # raw source never changes


def test_brain_settings_roundtrip_and_weekly_update():
    eng = _engine()
    eng.brains.update("SB-10", risk_level="high", weekly_update=False)
    assert eng.brains.get("SB-10").risk_level == "high"
    # reload from disk -> persisted
    from sourceborn.brains import BrainRegistry
    assert BrainRegistry(eng.memory.root).get("SB-10").risk_level == "high"
    res = eng.brains.weekly_update()
    assert res["total"] == 95 and res["updated"] == 94   # SB-10 opted out


def test_core_gate_six_lenses():
    from sourceborn.core_gate import six_lenses
    r = six_lenses("I need to prove my image and status, but I'm afraid I'll fail")
    assert len(r["lenses"]) == 6
    assert r["dominant_lens"] in ("Mask & Payoff", "Wound & Threat")
    assert r["active_count"] >= 2


def test_run_includes_human_layer():
    eng = _engine()
    res = eng.run("I want to prove myself and I fear failing")
    hl = res.output.lanes.get("human_layer")
    assert hl and hl["dominant_lens"]
    assert any(t.node_id == "SB-10" for t in res.trace)   # Core Gate fired


def test_weekly_scheduler_due_then_not():
    import tempfile
    from sourceborn import scheduler
    eng = _engine()
    root = eng.memory.root
    assert scheduler.due(root) is True                 # never run -> due
    res = scheduler.run_if_due(eng, root)
    assert res and res["total"] == 95
    assert scheduler.due(root) is False                # just ran -> not due
    assert scheduler.status(root)["last_weekly_update"]


def test_doubt_engine_bites_on_overclaim():
    from sourceborn.doubt import doubt_engine, falsifier, witness
    d = doubt_engine("This is obviously always true and guaranteed.", False, 0)
    assert d["bites"] and len(d["fragilities"]) >= 2
    assert falsifier("x") and witness(["SB-01"], "Mask & Payoff", False)


def test_evidence_ladder_rungs():
    from sourceborn.evidence import build_ledger, ladder_confidence
    assert ladder_confidence(build_ledger(["c"], True, [])) == "High"      # live -> FACT
    assert ladder_confidence(build_ledger(["c"], False, ["ref"])) == "Medium"
    assert ladder_confidence(build_ledger(["c"], False, [])) == "Low"


def test_dot_connections_and_merge():
    from sourceborn.dots import dot_connections, merge_proposal
    conns = dot_connections([["A", "B"], ["A", "C"], ["A", "B"]])
    refs = {c["ref"] for c in conns}
    assert "A" in refs and "B" in refs           # recur across parts
    assert merge_proposal(conns) is not None     # >=2 connections -> proposal
    assert merge_proposal([{"ref": "A", "appears_in": 2}]) is None  # 1 -> none


def test_synthetic_fuel_diagnose_and_inject():
    from sourceborn.fuel import diagnose_stall, inject
    assert diagnose_stall(["Evidence"], False, 3, False) == "Data-stall"
    assert diagnose_stall([], True, 3, False) is None   # not stuck
    f = inject("Frame-stall", "an ask")
    assert f["fuel"] == "Apostatic Inversion" and f["synthetic_tag"]["expiry"]


def test_rgl_recursive_loop():
    eng = _engine()
    rec = eng.run_recursive("why does the small idea win?", loops=3)
    assert rec["result"].output.answer
    assert rec["recursion"]["loop_count"] >= 1
    assert isinstance(rec["recursion"]["history"], list)
    assert "converged" in rec["recursion"]


def test_run_walk_per_node_urr_and_holds():
    eng = _engine()
    w = eng.run_walk("prove with current data that the small idea wins")
    walk = w["walk"]
    assert w["result"].output.answer
    assert walk["node_count"] == len(walk["steps"]) >= 5
    # every step is an SB node with its own URR review + memory write-back
    for s in walk["steps"]:
        assert s["sb_id"].startswith("SB-")
        assert s["urr_id"].startswith("URR-")
        assert s["verdict"] in ("pass", "hold")
        assert s["memory_written"] is True
        assert s["why"]
    # offline + "current data" -> at least one hold (no live source), loop-back-able
    assert walk["hold_count"] == len(walk["holds"]) >= 1
    assert all(h["sb_id"] for h in walk["holds"])
    # the SB node downloaded the URR intake into its own memory
    assert any("urr_intake" in e.tags
               for e in eng.memory.brain("SB-33").read_all())


def test_add_data_clears_evidence_hold():
    eng = _engine()
    before = eng.run_walk("prove with current data this is true")["walk"]
    # human pastes a source -> evidence hold should clear / confidence should rise
    after = eng.run_walk("prove with current data this is true",
                         live_override="2026 dataset: confirmed, n=10000, p<0.01")
    assert after["result"].output.confidence != "Low" or \
        after["walk"]["hold_count"] < before["hold_count"]


def test_stage7_embodied_and_non_resolution_present():
    eng = _engine()
    res = eng.run("prove this with current data")
    assert "embodied_check" in res.output.lanes
    assert "non_resolution" in res.output.lanes
    assert any(t.node_id == "SB-59" for t in res.trace)   # Embodied Check fired


def test_default_model_prefers_env_pref():
    import os
    from sourceborn import llm
    keys = ("ANTHROPIC_API_KEY", "XAI_API_KEY", "SB_DEFAULT_MODEL")
    old = {k: os.environ.get(k) for k in keys}
    try:
        os.environ["ANTHROPIC_API_KEY"] = "a"
        os.environ["XAI_API_KEY"] = "x"
        os.environ["SB_DEFAULT_MODEL"] = "grok"
        assert llm.default_model().name == "grok"      # env pref wins
        del os.environ["SB_DEFAULT_MODEL"]
        assert llm.default_model().name == "grok"      # else first working in order (claude no longer default)
    finally:
        for k, v in old.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)


def test_extract_text_formats():
    import io, zipfile
    from sourceborn.extract import extract_text
    t, note = extract_text("a.csv", b"x,y\n1,2")
    assert "x,y" in t and note == ""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("word/document.xml",
                   "<w:document><w:body><w:p><w:r><w:t>Hello</w:t></w:r></w:p>"
                   "<w:p><w:r><w:t>World</w:t></w:r></w:p></w:body></w:document>")
    dt, _ = extract_text("a.docx", buf.getvalue())
    assert "Hello" in dt and "World" in dt
    buf2 = io.BytesIO()
    with zipfile.ZipFile(buf2, "w") as z:
        z.writestr("xl/sharedStrings.xml",
                   "<sst><si><t>Param</t></si><si><t>Score</t></si></sst>")
        z.writestr("xl/worksheets/sheet1.xml",
                   '<worksheet><sheetData><row><c t="s"><v>0</v></c>'
                   '<c t="s"><v>1</v></c></row><row><c><v>9</v></c></row>'
                   '</sheetData></worksheet>')
    xt, _ = extract_text("t.xlsx", buf2.getvalue())
    assert "Param" in xt and "Score" in xt and "9" in xt


def test_walk_holds_carry_human_ask():
    eng = _engine()
    walk = eng.run_walk("Prove with current data that this is true.")
    holds = walk["walk"]["holds"]
    assert holds                                   # evidence gap -> at least one hold
    a = holds[0]["ask"]
    assert a["what"] and a["why"] and a["how"] and a["when"]


def test_local_bridge_frames_on_device_answer():
    # On-device lane, phase 2: the browser-GPU draft is what the full SB+URR
    # walk wraps — answer is preserved, falsifier added, the pyramid still fires.
    from sourceborn.llm import LocalBridgeModel
    eng = _engine()
    walk = eng.run_walk("why does the small idea win?",
                        model=LocalBridgeModel("Direct answer: it stays lighter."))
    out = walk["result"].output
    assert "lighter" in out.answer.lower()       # the on-device draft survived
    assert out.falsifier                          # full walk still wrapped it
    assert walk["walk"]["node_count"] >= 5        # the pyramid fired


def test_capture_model_yields_real_engine_prompt():
    # On-device lane, phase 1: CaptureModel unwinds with the genuine stage-8
    # prompt (so the browser completes exactly what a cloud model would have).
    from sourceborn.llm import CaptureModel, LocalCaptured
    from sourceborn.engine import NO_LIVE
    eng = _engine()
    try:
        eng.run("prove the small idea wins with current data",
                model=CaptureModel(), live_override=NO_LIVE)
        assert False, "CaptureModel should unwind via LocalCaptured"
    except LocalCaptured as cap:
        assert cap.system and "ASK:" in cap.prompt          # the real output prompt
        assert "LIVE FACT: none" in cap.prompt              # NO_LIVE -> no fact faked


def test_no_live_sentinel_skips_grounding_without_faking_fact():
    from sourceborn.engine import NO_LIVE
    eng = _engine()
    res = eng.run("prove this with current data", live_override=NO_LIVE)
    # private lane never invents a live fact, so confidence is not inflated High
    assert res.output.confidence != "High"


def test_local_status_always_offered():
    from sourceborn.llm import model_status
    assert model_status()["local"] is True       # lane exists; page gates on WebGPU


def test_local_not_in_registry_falls_back_offline():
    # secondary paths (/diag, /upload, /review) must degrade, never 500
    from sourceborn.llm import get_model
    assert get_model("local").name == "offline"


def test_domain_classifies_financial_document():
    from sourceborn.domain import classify_domain
    d = classify_domain(_BILL, origin="upload:bill.xlsx")
    assert d["domain"] == "numeric_financial"
    assert d["audit_applicable"] and not d["lens_applicable"]
    q = classify_domain("why does the small idea win?")     # a question is not a doc
    assert q["domain"] == "prose" and q["lens_applicable"]


def test_audit_numeric_finds_total_and_negatives():
    from sourceborn.domain import audit_numeric
    a = audit_numeric(_BILL)
    assert a["candidate_total"] == "10083937.80"            # grand total surfaced
    assert a["negative_count"] >= 2                          # the two corrections
    assert any("209745" in x for x in a["negative_examples"])
    assert a["caveats"]                                      # honest about its limits


def test_numeric_document_is_audited_not_psychoanalysed():
    eng = _engine()
    res = eng.run(_BILL, origin="upload:bill.xlsx")
    assert "audit" in res.output.lanes
    assert res.output.lanes["domain"]["domain"] == "numeric_financial"
    lens = res.output.lanes["human_layer"]["dominant_lens"]
    assert "audited" in lens
    for psych in ("Mask", "Wound", "Loyalty", "Desire", "Pain"):
        assert psych not in lens                             # no force-fit psychology
    assert res.output.lanes["audit"]["candidate_total"] == "10083937.80"


def test_private_document_no_false_evidence_hold():
    eng = _engine()
    walk = eng.run_walk(_BILL)
    # a private bill no longer opens an Evidence halt (web can't verify it) and
    # SB-59 no longer echoes it — a clean bill clears with no holds
    assert "Evidence" not in walk["result"].halts
    assert walk["walk"]["hold_count"] == 0
    # honest grade: a reviewed document is REVIEW_ONLY at Medium, never forced Low
    assert walk["result"].output.confidence == "Medium"
    assert walk["result"].output.classification.lower().startswith("review")


def test_noise_strip_word_boundary_building_not_invention():
    # "Building Automation System" must NOT be read as an invention ("build")
    ch = SourcebornEngine._noise_strip("Building Automation System starters provided")
    assert not ch.get("invention_seed")
    ch2 = SourcebornEngine._noise_strip("Please build a new tool for this project")
    assert ch2.get("invention_seed")                         # a real invention still lands


def test_prose_claim_still_uses_lenses():
    # regression: a personal claim still gets the six-lens human read, no audit
    eng = _engine()
    res = eng.run("I want to prove myself and I fear I will fail")
    assert res.output.lanes["human_layer"]["dominant_lens"] in (
        "Mask & Payoff", "Wound & Threat")
    assert "audit" not in res.output.lanes
    assert res.output.lanes["domain"]["domain"] == "prose"


def test_every_ask_runs_all_70_and_all_25_no_skips():
    # The user-stated requirements, exactly: every ask goes through all 70 SB
    # and all 25 URR with zero skips, with NO stages/blocks — each SB node is
    # reviewed by ITS OWN URR and absorbs the intake before the next node runs.
    eng = _engine()
    w = eng.run_walk("why does the small idea win?")["walk"]
    sb_fired = {s["sb_id"] for s in w["steps"]}
    assert sb_fired == {f"SB-{i:02d}" for i in range(1, 71)}   # all 70, none skipped
    assert "blocks" not in w                                   # no block grouping
    # one URR review PER NODE (SB-N → URR → SB-N absorbs → SB-N+1)
    assert len(w["pairs"]) == 70
    for p in w["pairs"]:
        assert len(p["sb"]) == 1                               # single-node review
    # SB-1 is reviewed before SB-2 even runs: pair order mirrors node order
    assert w["pairs"][0]["sb"] == ["SB-01"] and w["pairs"][1]["sb"] == ["SB-02"]
    # the intake fed back into the node's own brain (the revert)
    tags = [t for e in eng.memory.brain("SB-01").read_all() for t in e.tags]
    assert "urr_intake" in tags
    # closing integrity sweep ran (URR-19..25, run-level roles)
    assert [c["gate"] for c in w["closing"]] == [f"URR-{i}" for i in range(19, 26)]
    # every one of the 25 URR performed work this ask
    for i in range(1, 26):
        uid = f"URR-{i:02d}"
        p = eng.memory.brain(uid).meta["parameters"]
        assert p.get("Verifications_Performed", 0) >= 1, f"{uid} skipped"


def test_every_node_does_its_own_work():
    # No shared stamp: all 70 SB findings are distinct, and specific nodes
    # produce exactly their spec'd job.
    eng = _engine()
    w = eng.run_walk("prove with current data that the small idea wins")["walk"]
    whys = {s["sb_id"]: s["why"] for s in w["steps"]}
    assert len(set(whys.values())) == 70               # 70 nodes, 70 findings
    assert "sha256" in whys["SB-04"]                   # Raw Source Preservation
    assert "opposite" in whys["SB-48"].lower()         # Apostatic Inversion
    assert "walls hit" in whys["SB-54"]                # Critical Logic Wall
    assert "breakthrough score" in whys["SB-67"]       # Breakthrough Lock
    assert "kernel" in whys["SB-49"]                   # Heuristic Simplification


def test_urr_gates_have_distinct_roles():
    from sourceborn.nodes import URR_NODES
    names = {n.urr_id: n.name for n in URR_NODES}
    assert names["URR-08"] == "Entry Verification Gate"
    assert names["URR-10"] == "Doubt & Falsifier"      # Core of URR
    assert names["URR-15"] == "Human Context Gate"
    assert names["URR-25"] == "Full Run Integrity & Human Final Gate"
    eng = _engine()
    w = eng.run_walk("why does the small idea win?")["walk"]
    intakes = {p["intake"] for p in w["pairs"]} | {c["intake"] for c in w["closing"]}
    assert len(intakes) >= 15                          # each URR verifies ITS thing


def test_brain_parameters_grow_with_use():
    # ARD_RGL_7025 brain parameters (Runs_Completed, Verifications_Performed)
    # must genuinely accumulate run over run.
    eng = _engine()
    eng.run_walk("first ask")
    eng.run_walk("second ask")
    assert eng.memory.brain("SB-20").meta["parameters"]["Runs_Completed"] == 2
    # per walk: URR-10 primaries SB-19..28 (10 per-node reviews) + 70 matrix
    # sweeps = 80; two walks = 160 — its own loop, many times per run
    assert eng.memory.brain("URR-10").meta["parameters"]["Verifications_Performed"] == 160
    # feed-back into memory: block nodes hold the URR intake download
    tags = [t for e in eng.memory.brain("SB-33").read_all() for t in e.tags]
    assert "urr_intake" in tags and "node_finding" in tags


def test_chat_store_roundtrip():
    import importlib, os, tempfile
    os.environ["SB_ROOT"] = tempfile.mkdtemp(prefix="sb_chat_")
    import sourceborn.server as srv
    importlib.reload(srv)
    payload = {"output": {"answer": "direct answer", "confidence": "Medium",
                          "classification": "Review Only"},
               "model": "offline", "walk": {"hold_count": 0, "node_count": 70}}
    cid = srv._save_chat("test question", payload, "ask")
    chats = srv._list_chats()
    assert chats and chats[0]["id"] == cid
    assert chats[0]["question"] == "test question"
    full = srv._get_chat(cid)
    assert full["payload"]["output"]["answer"] == "direct answer"


def test_matrix_70x25_no_skips():
    # "every ask must go through each 70 SB and 70x25 URR without any skip"
    from sourceborn.urr_matrix import MATRIX
    assert len(MATRIX) == 25
    eng = _engine()
    w = eng.run_walk("why does the small idea win?")["walk"]
    m = w["matrix"]
    assert m["per_node"] == 25 and m["total"] == 70 * 25   # 1,750 micro-reviews
    for s in w["steps"]:                                    # every node carries its row
        assert s["matrix_pass"] + len(s["matrix_flags"]) == 25
    # every URR brain performed the full sweep (70 matrix + its gate work)
    for i in range(1, 26):
        p = eng.memory.brain(f"URR-{i:02d}").meta["parameters"]
        assert p.get("Verifications_Performed", 0) >= 70


def test_matrix_flags_real_issues():
    from sourceborn.node_work import Finding, WalkContext
    from sourceborn.urr_matrix import review_node
    ctx = WalkContext(raw_text="a claim", ladder_conf="Low", classification="Claim")
    flags = review_node("SB-24", Finding("this is always guaranteed and obviously true"), ctx)
    assert flags.get("URR-10") == "absolutes"               # Doubt filter bites
    clean = review_node("SB-01", Finding("raw source locked untouched: 7 chars"), ctx)
    assert "URR-10" not in clean


def test_pyramid_files_every_finding():
    # Pyramid of Thought (doc numbers): every node's finding is filed
    # Main -> Sub -> Micro; brains roll the tree up over time.
    eng = _engine()
    eng.run_walk("prove with current data that the small idea wins")
    for sid in ("SB-02", "SB-20", "SB-29", "SB-54", "SB-67"):
        fe = [e for e in eng.memory.brain(sid).read_all()
              if "node_finding" in e.tags][0]
        assert fe.pyramid["main"], f"{sid} finding not filed into Main"
    meta = eng.memory.brain("SB-20").meta["pyramid"]
    assert meta["main"]                                     # rolled up into the brain


def test_unfiled_queue_holds_user_words_and_parks():
    # "when some data not fitting in existing parameter... human review help there"
    eng = _engine()
    eng.run_walk("my zeropoint resonance hypothesis about consciousness")
    items = [u["item"] for u in eng.unfiled.list()]
    assert any(w in items for w in ("zeropoint", "resonance", "consciousness",
                                    "hypothesis"))
    first = eng.unfiled.list()[0]
    before = len(eng.unfiled.list())
    eng.unfiled.park(first["node"], first["item"])
    assert len(eng.unfiled.list()) == before - 1            # parked, not lost


def test_brain_export_import_keeps_data_forever():
    import importlib, os, tempfile
    os.environ["SB_ROOT"] = tempfile.mkdtemp(prefix="sb_keep_")
    import sourceborn.server as srv
    importlib.reload(srv)
    srv.ENGINE.run_walk("remember this forever")
    before = srv.ENGINE.memory.stats()["total_memory_entries"]
    assert before > 0
    backup = srv._export_brain()                            # download the whole brain
    import base64 as b64mod
    os.environ["SB_ROOT"] = tempfile.mkdtemp(prefix="sb_restore_")
    importlib.reload(srv)                                   # fresh empty instance
    assert srv.ENGINE.memory.stats()["total_memory_entries"] == 0
    out = srv._import_brain(b64mod.b64encode(backup).decode())
    assert out.get("ok") and out["files_restored"] > 0
    assert srv.ENGINE.memory.stats()["total_memory_entries"] == before


def test_wisdom_bank_richer():
    from sourceborn.wisdom import SEED_WISDOM
    assert len(SEED_WISDOM) >= 20
    sources = {w.source for w in SEED_WISDOM}
    for s in ("Bhagavad Gita", "Quran", "Tao Te Ching", "Guru Granth Sahib",
              "Gospel", "Rumi", "Kabir", "Marcus Aurelius"):
        assert s in sources


def test_persona_recall_normalized():
    import tempfile
    from sourceborn.persona import Persona
    p = Persona(root=tempfile.mkdtemp(prefix="sb_p_"))
    p.learn("small idea wins against big teams", "hollow beats weight")
    p.learn("x " * 400 + "small", "a very long unrelated file " + "y " * 400)
    got = p.recall("why does the small idea win?")
    assert got and "against big teams" in got[0].question   # similar beats long


def test_ingest_text_entry_files_and_learns():
    import tempfile
    from sourceborn.memory import Memory
    from sourceborn.persona import Persona
    from sourceborn.pyramid import UnfiledQueue
    from sourceborn.ingest import ingest_text_entry
    root = tempfile.mkdtemp(prefix="sb_ing_")
    mem, per, unf = Memory(root), Persona(root), UnfiledQueue(root)
    res = ingest_text_entry(mem, per, "my_theory.txt",
                            "Point Zero holds the raw source. The mirror structure "
                            "of odd primes carries the pattern.",
                            category="raw_thoughts", unfiled=unf)
    assert res["ok"] and res["node"] == "SB-09"            # raw thought → voice node
    assert res["pyramid"]["main"] >= 1                     # pyramid-filed
    assert per.examples and "my_theory.txt" == per.examples[-1].question
    e = [x for x in mem.brain("SB-09").read_all() if "corpus" in x.tags][0]
    assert e.pyramid["main"]                               # filed into the brain


def test_ingest_folder_categorizes():
    import os, tempfile
    from sourceborn.ingest import ingest_folder
    from sourceborn.memory import Memory
    root = tempfile.mkdtemp(prefix="sb_fold_")
    corp = tempfile.mkdtemp(prefix="corp_")
    for cat, fn, txt in (("raw_thoughts", "a.txt", "my raw thought about doubt and wound"),
                         ("examples", "b.txt", "Direct answer: hollow beats weight."),
                         ("cores", "c.txt", "SB-01 locks the raw source; URR verifies.")):
        d = os.path.join(corp, cat); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, fn), "w").write(txt)
    stats = ingest_folder(corp, root=root)
    assert stats["files"] == 3
    assert stats["by_category"] == {"raw_thoughts": 1, "examples": 1, "cores": 1}
    mem = Memory(root)
    assert any("corpus" in e.tags for e in mem.brain("SB-09").read_all())   # raw→SB-09
    assert any("corpus" in e.tags for e in mem.brain("SB-64").read_all())   # example→SB-64
    assert any("corpus" in e.tags for e in mem.brain("SB-07").read_all())   # core→SB-07


def test_weekly_digest_synthesises():
    eng = _engine()
    eng.run_walk("prove with current data that the small idea wins")
    dig = eng.memory.weekly_digest()
    assert dig["digested"] >= 1
    de = [e for e in eng.memory.brain("SB-20").read_all()
          if "weekly_digest" in e.tags]
    assert de and "weekly digest" in de[0].content
    assert de[0].parameters.get("findings", 0) >= 1
    # the digest is knowledge_gained, recorded on the brain meta
    assert eng.memory.brain("SB-20").meta["parameters"].get("Knowledge_Gained")


def test_seed_corpus_shipped_and_categorized():
    # the user's cores/examples/raw-thoughts ship with the app (deploy to Render)
    import os
    root = os.path.join(os.path.dirname(__file__), "..", "seed_corpus")
    assert os.path.isdir(root)
    for cat in ("raw_thoughts", "examples", "cores"):
        d = os.path.join(root, cat)
        assert os.path.isdir(d) and len(os.listdir(d)) > 10
    # sensitive files must NOT be shipped
    rt = os.listdir(os.path.join(root, "raw_thoughts"))
    for banned in ("Personal_Sexual", "Gavalas", "Hospital_Career", "consumer_case"):
        assert not any(banned in f for f in rt), f"{banned} leaked into seed_corpus"


def test_novelty_pass_finds_never_existed_parameters():
    # "generating new fresh file to check may be there is new parameters,
    # which never exists" — spec §10: propose in a file, never auto-add.
    import json, os
    from sourceborn.novelty import run_novelty_pass, known_universe, is_known
    eng = _engine()
    root = eng.memory.root
    q = "my zeropoint resonance chamber needs proof"
    eng.run_walk(q)
    # the server stores every ask as a chat — the term's second source
    os.makedirs(os.path.join(root, "chats"), exist_ok=True)
    with open(os.path.join(root, "chats", "1.json"), "w") as f:
        json.dump({"question": q}, f)
    res = run_novelty_pass(root, eng.memory, eng.unfiled)
    terms = {c["term"] for c in res["candidates"]}
    assert "zeropoint" in terms or "resonance" in terms   # genuinely new surfaced
    c = res["candidates"][0]
    assert c["status"].startswith("NEW-CANDIDATE")        # proposal, not auto-add
    assert c["nearest_existing"] and c["why_not_same"]    # near-dupes die at gate
    fp = os.path.join(root, "novelty", res["file"])
    assert os.path.exists(fp)                             # the fresh md file
    body = open(fp, encoding="utf-8").read()
    assert "NEW-CANDIDATE" in body and "P-NEW:" in body
    # known vocabulary is NOT novel
    uni = known_universe(root)
    assert is_known("doubt", uni) and is_known("evidence", uni)


def test_novelty_approve_promotes_to_real_parameter():
    import json, os
    from sourceborn.novelty import run_novelty_pass, approve, approved_terms
    from sourceborn.pyramid import unfiled_from_input
    eng = _engine()
    root = eng.memory.root
    q = "my zeropoint resonance chamber needs proof"
    eng.run_walk(q)
    os.makedirs(os.path.join(root, "chats"), exist_ok=True)
    with open(os.path.join(root, "chats", "1.json"), "w") as f:
        json.dump({"question": q}, f)
    run_novelty_pass(root, eng.memory, eng.unfiled)
    out = approve(root, eng.memory, eng.unfiled, "zeropoint")
    assert out["ok"] and out["label"] == "P-NEW:zeropoint"
    assert "zeropoint" in approved_terms(root)
    # approved → no longer lands unfiled
    again = unfiled_from_input("the zeropoint device hums",
                               extra_known=approved_terms(root))
    assert "zeropoint" not in again
    # approved → files into the pyramid as its own sub bucket on the next walk
    w = eng.run_walk("the zeropoint approach against entropy")
    subs = [s for e in eng.memory.brain("SB-49").read_all()
            for s in e.pyramid.get("sub", [])]
    assert "P-NEW:zeropoint" in subs
    # human decision recorded on the New Parameter Generator's brain
    assert eng.memory.brain("SB-43").meta["parameters"].get("Human_Decisions", 0) >= 1


def test_per_node_walk_no_stages():
    # Req: "i didnt asked ever to make stages on 70 nodes" + "make URR work on
    # each SB node, revert it to SB-1, then to SB-2"
    eng = _engine()
    w = eng.run_walk("prove with current data that the small idea wins")["walk"]
    assert "blocks" not in w
    assert len(w["pairs"]) == 70 and all(len(p["sb"]) == 1 for p in w["pairs"])
    order = [p["sb"][0] for p in w["pairs"]]
    assert order == [f"SB-{i:02d}" for i in range(1, 71)]   # N reviewed before N+1
    # function-matched reviewers, not positional blocks
    by_sb = {p["sb"][0]: p["gate"] for p in w["pairs"]}
    assert by_sb["SB-20"] == "URR-10"      # Doubt Engine → Doubt & Falsifier
    assert by_sb["SB-40"] == "URR-13"      # Merge Proposal → Merge Integrity
    assert by_sb["SB-58"] == "URR-20"      # Re-Anchor → Re-Anchor Verification
    assert by_sb["SB-64"] == "URR-22"      # Final Output → Output Integrity


def test_node_definitions_are_file_driven():
    # Req: "Files in core" — identities load from core/node_definitions.json
    import json, os
    path = os.path.join(os.path.dirname(__file__), "..", "core",
                        "node_definitions.json")
    assert os.path.exists(path)
    d = json.load(open(path, encoding="utf-8"))
    assert len(d["sb"]) == 70 and len(d["urr"]) == 25
    assert d["primary_urr"]["SB-20"] == "URR-10"
    from sourceborn.nodes import SB_NODES, SB_PRIMARY_URR
    assert SB_NODES[19].name == d["sb"][19]["name"]         # engine follows file
    assert SB_PRIMARY_URR == d["primary_urr"]


def test_weekly_learns_new_connections_and_can_rollback():
    # Req: real weekly update — new knowledge, governed (reversible)
    eng = _engine()
    eng.run_walk("prove with current data that the small idea wins")
    dig = eng.memory.weekly_digest()
    assert dig["digested"] >= 1
    assert dig["new_connections"] > 0                       # learned NEW links
    b = eng.memory.brain("SB-20")
    assert b.meta["parameters"].get("Connected_Points")     # links recorded
    conn = [e for e in b.read_all() if "weekly_connection" in e.tags]
    assert conn and "shares" in conn[0].content
    # governed learning: snapshot exists and rollback restores pre-digest meta
    assert b.meta.get("brain_version", 0) >= 1
    kg = b.meta["parameters"].get("Knowledge_Gained")
    assert b.rollback() is True
    assert eng.memory.brain("SB-20").meta["parameters"].get("Knowledge_Gained") != kg


def test_mongo_backend_optional_and_fallback():
    # Req: "must link on mongoDB" — adapter exists, activates on SB_MONGO_URL,
    # falls back to JSON without it (zero-dependency default untouched)
    import os
    from sourceborn.mongo_store import MongoMemory, MongoNodeBrain, make_memory
    from sourceborn.memory import Memory
    assert os.environ.get("SB_MONGO_URL", "") == ""         # CI has no Mongo
    m = make_memory(tempfile.mkdtemp(prefix="sb_mm_"))
    assert type(m) is Memory                                # clean JSON fallback
    for method in ("write", "read_all", "search", "bump", "snapshot", "rollback"):
        assert hasattr(MongoNodeBrain, method)              # full API parity
    for method in ("brain", "master_log", "search", "stats"):
        assert hasattr(MongoMemory, method)


def test_interconnection_graph_inputs():
    # Req: "this need to build" (the K-graph image) — Principle 8, Full
    # Interconnection: complete-mesh counts + a valid SB→URR pairing for every
    # node + learned connections available to draw after a weekly pass.
    from sourceborn.nodes import SB_NODES, URR_NODES, SB_PRIMARY_URR
    n_sb, n_all = len(SB_NODES), len(SB_NODES) + len(URR_NODES)
    assert n_sb * (n_sb - 1) // 2 == 2415          # K70 handshakes
    assert n_all * (n_all - 1) // 2 == 4465        # K95 handshakes
    urr_ids = {u.urr_id for u in URR_NODES}
    assert set(SB_PRIMARY_URR) == {n.sb_id for n in SB_NODES}   # all 70 paired
    assert set(SB_PRIMARY_URR.values()) <= urr_ids              # to real URRs
    eng = _engine()
    eng.run_walk("seed the web")
    eng.memory.weekly_digest()
    linked = [n.sb_id for n in SB_NODES
              if eng.memory.brain(n.sb_id).meta["parameters"].get("Connected_Points")]
    assert len(linked) >= 10                       # a real web to draw


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for fn in fns:
        fn()
        print(f"  ok  {fn.__name__}")
        passed += 1
    print(f"\n{passed}/{len(fns)} tests passed")


if __name__ == "__main__":
    _run_all()
