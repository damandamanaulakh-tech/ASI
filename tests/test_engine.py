"""Smoke + behaviour tests for the Sourceborn engine. Run: ``pytest -q`` or
``python -m tests.test_engine`` (works without pytest)."""

from __future__ import annotations

import math
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


def test_weekly_pull_accumulates_and_is_readable():
    """Item 04. The pull used to overwrite one file and run a DIFFERENT, smaller
    job when pressed by hand. Now: one shared job, every run kept, readable."""
    import os
    from sourceborn import scheduler
    eng = _engine()
    root = eng.memory.root

    st = scheduler.status(root)                        # never run
    assert st["last_weekly_update"] is None and st["runs"] == 0
    assert st["due_now"] is True
    assert scheduler.latest(root) is None
    assert scheduler.history(root) == []

    r1 = scheduler.run_weekly(eng, root)
    assert "digest" in r1 and "novelty" in r1          # the FULL job, not a bump
    assert "error" not in (r1["novelty"] or {}), r1["novelty"]
    r2 = scheduler.run_weekly(eng, root)               # a second, same second
    assert r2

    h = scheduler.history(root)
    assert len(h) == 2, h                              # accumulated, not clobbered
    files = [x["file"] for x in h]
    assert len(set(files)) == 2                        # no same-second collision
    assert all(f.startswith("weekly_") for f in files)
    assert scheduler.status(root)["runs"] == 2
    assert scheduler.status(root)["due_now"] is False   # ran -> not due

    latest = scheduler.latest(root)
    assert latest and latest.get("total") == 95
    got = scheduler.get_run(root, h[0]["file"])
    assert got and got.get("at") == h[0]["at"]

    # the reader is path-guarded: no traversal, no non-weekly file
    assert scheduler.get_run(root, "../master_log.jsonl") is None
    assert scheduler.get_run(root, "weekly_nope.json") is None
    assert scheduler.get_run(root, "") is None

    # the pull is in the sacred log
    log = os.path.join(root, "master_log.jsonl")
    if os.path.exists(log):
        with open(log, encoding="utf-8") as f:
            assert "weekly_run" in f.read()


def test_what_exists_map_resolves_to_real_code():
    """His ask: "i want to know the existence of my understanding in the code
    file". Every reference on the page must point at a line that is really
    there — a map that has gone stale is a map that lies. This test IS the
    guard: move a line the page cites and this goes red."""
    from sourceborn import exists
    v = exists.verify()
    gone = [(h["module"], h["anchor"], h.get("why"))
            for g in v["groups"] for r in g["rows"] for h in r["hits"]
            if not h["found"]]
    assert not gone, gone
    assert v["checked"] >= 60           # the map is real, not three rows
    assert v["missing"] == 0

    # every row is his words + a state + an honest note; no placeholders
    states = set()
    for g in v["groups"]:
        assert g["group"] and g["rows"]
        for r in g["rows"]:
            assert r["his"].strip() and r["note"].strip()
            assert r["state"] in exists.STATE_NOTE
            states.add(r["state"])
            # an ABSENT row must cite nowhere; anything else must cite code
            if r["state"] == exists.ABSENT:
                assert not r["hits"], r["his"]
            else:
                assert r["hits"], r["his"]
    assert exists.ABSENT in states       # the absences are stated, not hidden
    assert exists.RUNS in states

    # the absences and the seams are both present and both say his words
    assert len(v["absences"]) >= 4
    assert all(a["what"] and a["why"] and a["his"] for a in v["absences"])
    assert len(v["seams"]) >= 4
    assert all(s["code"] and s["his"] for s in v["seams"])

    # rubric = parameter: the count is read from the registry, never written
    from sourceborn import ladder
    lr = exists.ladder_reading(ladder.seed_registry())
    assert lr["rubrics_total"] == 3072
    assert lr["rubrics_filled"] == 18       # the honest number, today
    assert lr["containers_total"] == 200


def test_what_exists_notices_when_the_code_moves_away():
    """The self-check has to actually be able to fail, or it is decoration."""
    from sourceborn import exists
    h = exists._find("ladder.py", "TOTAL_PARAMS = 3072")
    assert h["found"] and isinstance(h["line"], int)
    miss = exists._find("ladder.py", "this string is not in the file anywhere")
    assert miss["found"] is False and miss["line"] is None and miss["why"]
    nofile = exists._find("no_such_module.py", "x")
    assert nofile["found"] is False and nofile["why"] == "module not found"


def test_what_exists_page_is_served_and_locked():
    import base64
    import json
    import threading
    import urllib.error
    import urllib.request
    from sourceborn import server

    eng = _engine()
    old = (server.ENGINE, server.SB_ROOT, server.SB_ACCESS_USER,
           server.SB_ACCESS_PASS)
    server.ENGINE, server.SB_ROOT = eng, eng.memory.root
    server.SB_ACCESS_USER, server.SB_ACCESS_PASS = "him", "letmein"
    httpd = server.ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % httpd.server_address[1]

    def get(p, auth=True):
        r = urllib.request.Request(base + p)
        if auth:
            r.add_header("Authorization", "Basic " +
                         base64.b64encode(b"him:letmein").decode())
        try:
            with urllib.request.urlopen(r, timeout=10) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()

    try:
        for p in ("/exists", "/exists/data"):
            assert get(p, auth=False)[0] == 401, p     # behind the lock
            assert p not in server.OPEN_PATHS
        code, body = get("/exists")
        assert code == 200 and b"WHAT EXISTS" in body
        assert b"rubric means" in body.lower() or b"Rubric means" in body
        code, body = get("/exists/data")
        assert code == 200
        d = json.loads(body)
        assert d["missing"] == 0 and d["checked"] >= 60
        assert d["ladder"]["rubrics_filled"] == 18
        assert d["ladder"]["rubrics_total"] == 3072
        assert d["at"] and d["absences"] and d["seams"]
        # the dashboard actually links to it — the gap that hid the last pages
        code, home = get("/")
        assert code == 200 and b'href="/exists"' in home
    finally:
        httpd.shutdown()
        httpd.server_close()
        (server.ENGINE, server.SB_ROOT, server.SB_ACCESS_USER,
         server.SB_ACCESS_PASS) = old


def test_weekly_ledger_is_paged_never_capped():
    """The reviewer caught this: `runs` was counted by parsing a 52-row page,
    so the pill, the panel header and MY PAGE all stopped counting at 52 and
    older runs were unreachable through the app."""
    import json
    import os
    from sourceborn import scheduler
    eng = _engine()
    root = eng.memory.root
    d = os.path.join(root, "weekly")
    os.makedirs(d, exist_ok=True)
    for i in range(60):                                # 60 > the 52 page size
        with open(os.path.join(d, f"weekly_202601{i:02d}000000.json"), "w",
                  encoding="utf-8") as f:
            json.dump({"at": f"2026-01-{i:02d} 00:00:00", "updated": i}, f)

    assert scheduler.count_runs(root) == 60            # counted, not parsed
    assert scheduler.status(root)["runs"] == 60        # the pill tells the truth
    assert len(scheduler.history(root)) == 52          # one page
    tail = scheduler.history(root, limit=52, offset=52)
    assert len(tail) == 8                             # and the rest is reachable
    assert scheduler.history(root)[0]["at"] > tail[-1]["at"]

    # a stray file must not push a real run out of the page
    with open(os.path.join(d, "notes.txt"), "w", encoding="utf-8") as f:
        f.write("hand note")
    assert scheduler.count_runs(root) == 60
    assert len(scheduler.history(root)) == 52

    # same-second suffixes sort numerically, not lexicographically
    for n in ("", "_2", "_10"):
        with open(os.path.join(d, f"weekly_20270101000000{n}.json"), "w",
                  encoding="utf-8") as f:
            json.dump({"at": "2027-01-01 00:00:00", "n": n or "1"}, f)
    assert scheduler.history(root)[0]["file"] == "weekly_20270101000000_10.json"


def test_a_corrupt_weekly_file_never_takes_a_route_down():
    """A process recycled mid-write leaves a truncated run behind. `do_GET`
    has no exception handler, so an unguarded json.load would drop the
    connection instead of answering."""
    import os
    from sourceborn import scheduler
    eng = _engine()
    root = eng.memory.root
    scheduler.run_weekly(eng, root)
    d = os.path.join(root, "weekly")
    with open(os.path.join(d, "weekly_20991231000000.json"), "w",
              encoding="utf-8") as f:
        f.write('{"at":"2099-12-31 00:00:00","updated":9')   # cut off

    h = scheduler.history(root)                     # does not raise
    assert h[0]["file"] == "weekly_20991231000000.json"
    assert h[0]["unreadable"] is True               # and it SAYS it is corrupt
    assert scheduler.latest(root) is not None       # falls back to a good run
    assert scheduler.get_run(root, "weekly_20991231000000.json") is None
    assert scheduler.count_runs(root) == 2          # still counted as kept


def test_two_pulls_in_the_same_second_never_overwrite_each_other():
    """The first fix for this was `while os.path.exists()` then open(...,'w') —
    a TOCTOU. This app is a ThreadingHTTPServer WITH a daemon thread calling
    the same function, so the reviewer reproduced 8-12 lost runs out of 24
    concurrent pulls. The filesystem has to arbitrate, not us."""
    import threading
    from sourceborn import scheduler
    eng = _engine()
    root = eng.memory.root

    class _Fixed:                       # every run claims the same second
        def __init__(self, real): self.real = real
        def weekly_update(self):
            r = self.real.weekly_update()
            r["at"] = "2026-08-12 12:00:00"
            return r

    class _Eng:
        def __init__(self, e):
            self.brains, self.memory, self.unfiled = _Fixed(e.brains), e.memory, e.unfiled

    N = 12
    gate = threading.Barrier(N)
    errs = []

    def one():
        try:
            gate.wait()
            scheduler.run_weekly(_Eng(eng), root)
        except Exception as exc:                     # noqa: BLE001
            errs.append(exc)

    ts = [threading.Thread(target=one) for _ in range(N)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert not errs, errs
    assert scheduler.count_runs(root) == N, scheduler.count_runs(root)


def test_weekly_routes_over_http_are_behind_the_lock():
    """The claims are about ROUTES, so they get tested as routes."""
    import base64
    import json
    import os
    import threading
    import urllib.error
    import urllib.request
    from sourceborn import scheduler, server

    eng = _engine()
    root = eng.memory.root
    scheduler.run_weekly(eng, root)
    run = scheduler.history(root)[0]["file"]

    old = (server.ENGINE, server.SB_ROOT, server.SB_ACCESS_USER,
           server.SB_ACCESS_PASS)
    server.ENGINE, server.SB_ROOT = eng, root
    server.SB_ACCESS_USER, server.SB_ACCESS_PASS = "him", "letmein"
    httpd = server.ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % httpd.server_address[1]

    def get(p, auth=True):
        r = urllib.request.Request(base + p)
        if auth:
            tok = base64.b64encode(b"him:letmein").decode()
            r.add_header("Authorization", "Basic " + tok)
        try:
            with urllib.request.urlopen(r, timeout=10) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()

    try:
        for p in ("/weekly", "/weekly/file?name=" + run):
            assert get(p, auth=False)[0] == 401, p   # locked, like every route
            assert p not in server.OPEN_PATHS

        code, body = get("/weekly")
        assert code == 200
        d = json.loads(body)
        assert d["runs"] == 1 and d["shown"] == 1
        assert d["status"]["state"] == "current"
        assert d["phrase"].startswith("current — last")
        assert d["history"][0]["file"] == run
        assert d["latest"]["total"] == 95

        # a bad query must answer, not drop the connection (do_GET has no
        # handler, so int('abc') here would kill the socket)
        assert get("/weekly?limit=abc&offset=zzz")[0] == 200

        assert get("/weekly/file?name=" + run)[0] == 200
        for bad in ("../master_log.jsonl", "weekly_nope.json",
                    "weekly_x.txt", ""):
            assert get("/weekly/file?name=" + bad)[0] == 404, bad

        code, body = get("/health", auth=False)       # the Render probe stays open
        assert code == 200
        h = json.loads(body)
        assert h["weekly"]["runs"] == 1
        assert h["weekly_phrase"].startswith("current")
    finally:
        httpd.shutdown()
        httpd.server_close()
        (server.ENGINE, server.SB_ROOT, server.SB_ACCESS_USER,
         server.SB_ACCESS_PASS) = old


def test_brains_update_keeps_the_shape_the_dashboard_reads():
    """The button prints `d.updated+'/'+d.total`. run_weekly must not have
    changed that contract while adding digest/novelty to the same payload."""
    from sourceborn import scheduler
    eng = _engine()
    res = scheduler.run_weekly(eng, eng.memory.root)
    assert isinstance(res.get("updated"), int)
    assert isinstance(res.get("total"), int)
    assert "digest" in res and "novelty" in res


def test_weekly_phrase_says_three_states_not_two():
    """The dashboard pill and MY PAGE both said 'active' the moment one run
    existed, however stale, and MY PAGE read a key that never existed."""
    from sourceborn.server import _weekly_phrase
    assert _weekly_phrase({"last_weekly_update": None,
                           "due_now": True}) == "never run"
    assert _weekly_phrase({"last_weekly_update": "2026-01-01 00:00:00",
                           "due_now": True}).startswith("overdue")
    assert _weekly_phrase({"last_weekly_update": "2026-08-12 00:00:00",
                           "due_now": False}).startswith("current")


def test_novelty_failure_is_visible_not_swallowed():
    """A broken novelty pass used to vanish silently — the weekly run looked
    clean while half of it had not happened."""
    from sourceborn import scheduler, novelty
    eng = _engine()
    real = novelty.run_novelty_pass
    novelty.run_novelty_pass = lambda *a, **k: (_ for _ in ()).throw(
        OSError("disk full"))
    try:
        res = scheduler.run_weekly(eng, eng.memory.root)
    finally:
        novelty.run_novelty_pass = real
    assert "disk full" in res["novelty"]["error"]
    assert scheduler.history(eng.memory.root)[0]["novelty_error"]
    assert res["updated"] is not None                  # the rest still ran


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
        assert s["urr_id"] == "FIL"          # reviewed by the seven filters
        assert s["verdict"] in ("pass", "hold")
        assert s["memory_written"] is True
        assert s["why"]
    # offline + "current data" -> at least one hold (no live source), loop-back-able
    assert walk["hold_count"] == len(walk["holds"]) >= 1
    assert all(h["sb_id"] for h in walk["holds"])
    # the SB node downloaded the filter intake into its own memory (the revert)
    assert any("filter_intake" in e.tags
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


def test_every_ask_runs_all_70_through_all_7_filters():
    # No stages, no blocks, and no 70×25. Every ask goes through all 70 SB
    # nodes, and every node's finding passes ALL SEVEN filters in order before
    # the next node runs — then absorbs the filter intake (the revert).
    from sourceborn.filters import FILTER_IDS
    eng = _engine()
    w = eng.run_walk("why does the small idea win?")["walk"]
    sb_fired = {s["sb_id"] for s in w["steps"]}
    assert sb_fired == {f"SB-{i:02d}" for i in range(1, 71)}   # all 70, none skipped
    assert "blocks" not in w                                   # no block grouping
    assert len(w["pairs"]) == 70                               # one review per node
    for p in w["pairs"]:
        assert len(p["sb"]) == 1
    assert w["pairs"][0]["sb"] == ["SB-01"] and w["pairs"][1]["sb"] == ["SB-02"]
    # every node saw all seven gates, in order, no skips
    for f in w["filters"]:
        assert [g["gate"] for g in f["gates"]] == list(FILTER_IDS)
    # the intake fed back into the node's own brain (the revert)
    tags = [t for e in eng.memory.brain("SB-01").read_all() for t in e.tags]
    assert "filter_intake" in tags
    # run-level sweep: the same seven filters over the whole run
    assert [c["gate"] for c in w["closing"]] == list(FILTER_IDS)
    # every one of the seven performed work this ask
    for fid in FILTER_IDS:
        p = eng.memory.brain(fid).meta["parameters"]
        assert p.get("Verifications_Performed", 0) >= 1, f"{fid} skipped"


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
    # the 25 URR brains stay configured as MEMORY — the filters are the METHOD
    eng = _engine()
    for i in range(1, 26):
        assert eng.memory.brain(f"URR-{i:02d}") is not None


def test_brain_parameters_grow_with_use():
    # ARD_RGL_7025 brain parameters (Runs_Completed, Verifications_Performed)
    # must genuinely accumulate run over run.
    eng = _engine()
    eng.run_walk("first ask")
    eng.run_walk("second ask")
    assert eng.memory.brain("SB-20").meta["parameters"]["Runs_Completed"] == 2
    # each filter runs once per node (70) plus once run-level = 71 per walk;
    # two walks = 142 — its own loop, many times per run
    for fid in ("FIL-1", "FIL-3", "FIL-7"):
        assert eng.memory.brain(fid).meta["parameters"]["Verifications_Performed"] == 142
    # feed-back into memory: every node holds the filter intake download
    tags = [t for e in eng.memory.brain("SB-33").read_all() for t in e.tags]
    assert "filter_intake" in tags and "node_finding" in tags


def test_present_fact_refuses_moving_numbers_without_live():
    # Born from the live failure: TCS shown at 2431 while the market said 2362.
    # A moving number with no live witness must NOT leave the engine — the
    # answer itself is the refusal, and no remembered price can slip through.
    from sourceborn.present_fact import is_present_fact
    assert is_present_fact("what is TCS current share price") is True
    assert is_present_fact("price of TCS stock") is True
    assert is_present_fact("today's nifty score") is True
    assert is_present_fact("why does the small idea win?") is False
    eng = _engine()
    res = eng.run("what is the current share price of TCS?")
    a = res.output.answer.lower()
    assert "cannot tell you this number" in a          # the refusal IS the answer
    assert "live source" in a
    assert res.output.confidence == "Low"
    assert any("present-fact" in g.description for g in res.gaps)
    # with a live witness the figure may pass — capped, and marked verify-first
    res2 = eng.run("what is the current share price of TCS?",
                   live_override="TCS trading at 2362.00 INR (NSE, 30 Jul 2026 15:12 IST)")
    assert res2.output.confidence in ("Medium", "Low")  # never High on one witness
    assert "verify" in res2.output.answer.lower()


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


def test_seven_filters_no_skips():
    # every ask goes through 70 SB nodes and all 7 filters, no skip
    from sourceborn.filters import FILTER_IDS
    assert len(FILTER_IDS) == 7
    eng = _engine()
    w = eng.run_walk("why does the small idea win?")["walk"]
    m = w["matrix"]
    assert m["per_node"] == 7 and m["total"] == 71 * 7   # 70 nodes + run-level
    for s in w["steps"]:                                 # every node carries its row
        assert s["matrix_pass"] + len(s["matrix_flags"]) == 7
    for fid in FILTER_IDS:                               # each filter's own brain grew
        p = eng.memory.brain(fid).meta["parameters"]
        assert p.get("Verifications_Performed", 0) >= 70
    assert [c["gate"] for c in w["closing"]] == list(FILTER_IDS)


def test_one_witness_never_reaches_high():
    # The cap, and the reason this whole pass exists: one rendering of a thing
    # is not the thing. However good a single source is, it stops at Medium.
    from sourceborn import witnesses as W
    solo = W.read("the small idea wins",
                  [W.Witness("the small idea wins because it moves", "live", W.WITNESSED)])
    assert solo.confidence == "Medium" and not solo.halt
    two = W.read("the small idea wins",
                 [W.Witness("the small idea wins because it moves", "live", W.WITNESSED),
                  W.Witness("the small idea wins because it moves", "corpus", W.ORIGINAL)])
    assert len(two.witnesses) == 1        # near-identical text = ONE origin restated
    from sourceborn.evidence import ladder_confidence
    led = [{"evidence_tag": "FACT"}]
    assert ladder_confidence(led) == "High"                  # rung alone
    assert ladder_confidence(led, witnesses=1) == "Medium"    # capped
    assert ladder_confidence(led, witnesses=2) == "High"


def test_mask_is_found_between_two_witnesses():
    # The real case: asserted in the letter, hedged in print. The gap IS the
    # finding — it halts, and it is never averaged or picked between.
    from sourceborn import witnesses as W
    letter = W.Witness("the roots of the equation xi are all real",
                       "draft letter", W.ORIGINAL)
    printed = W.Witness("it is very probable that all roots of xi are real",
                        "printed paper", W.CARRIED)
    r = W.read("roots of the equation xi are real", [letter, printed])
    assert r.halt is True
    assert any(m.kind == "softened" for m in r.masks)
    assert r.confidence == "Medium"          # a gap never delivers as High
    # an ellipsis is a witness that something was removed
    assert W.excisions_in("I would like ... to add the remark") == ["..."]
    # and two documents merely differing in vocabulary is NOT a mask
    a = W.Witness("the cat sat on the mat in the kitchen", "a", W.ORIGINAL)
    b = W.Witness("entirely unrelated prose about shipping", "b", W.ORIGINAL)
    assert W.read("the cat sat on the mat", [a, b]).masks == []


def test_sequence_places_the_ask():
    from sourceborn import sequence as S
    assert S.is_invention("build me a logo for a tea shop") is True
    assert S.is_invention("why does gravity pull?") is False
    assert S.place("why does the small idea win?")[0] == S.EXPRESSION
    assert S.place("the proof fails here, it is stuck")[0] == S.HALT
    assert S.place("what is it really called, the term")[0] == S.NAMING
    assert S.place("check his original manuscript")[0] == S.WITNESS
    # step 8: a halt is handed back as the next Point Zero, never as an ending
    nxt = S.next_ask(S.HALT, "evidence", "the count")
    assert "Point Zero" in nxt and "the count" in nxt


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
    # Req: "now we dont want 70-25 there, but i want more filters and fact kind
    # of" — the reviewer is the seven filters, the same seven for every node.
    assert {p["gate"] for p in w["pairs"]} == {"FIL"}
    from sourceborn.filters import FILTER_IDS, FILTER_NAMES
    for f in w["filters"]:
        assert [g["gate"] for g in f["gates"]] == list(FILTER_IDS)
        assert [g["name"] for g in f["gates"]] == [FILTER_NAMES[i] for i in FILTER_IDS]


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


def test_khalf_split_rules_partition_and_differ():
    from sourceborn.khalf import split_doc, RULES
    text = ("The chiller was replaced in thirty hours. The panels were dead. "
            "Light was rationed. The hospital reopened in five days. "
            "The record stands at 30 hours. Nobody believed it could hold.")
    seen = set()
    for rule in RULES:
        held, masked = split_doc(text, rule)
        assert held and masked, rule
        # partition: together they carry every word of the original
        joined = sorted((held + " " + masked).split())
        assert joined == sorted(text.split()), rule
        seen.add(held)
    assert len(seen) == len(RULES)  # the three rules genuinely differ


def test_khalf_scoring_two_witnesses():
    from sourceborn.khalf import score_overlap
    truth = "The chiller replacement took 30 hours and saved 70 lakhs."
    perfect = score_overlap(truth, truth)
    assert perfect["token_f1"] == 1.0
    assert perfect["number_recall"] == 1.0
    disjoint = score_overlap(truth, "completely unrelated words only here")
    assert disjoint["token_f1"] == 0.0
    assert disjoint["number_recall"] == 0.0
    # numbers are their own witness: right words, wrong number, is caught
    wrong_num = score_overlap(truth, "The chiller replacement took 45 hours and saved 90 lakhs.")
    assert wrong_num["number_recall"] == 0.0
    assert wrong_num["token_f1"] > 0.5


def test_witnesses_halt_when_the_number_differs():
    """The TCS case itself: two witnesses, same words, different figure.
    Before this, identical claim-words meant no Mask and the pair reached
    High — the exact failure the layer exists to stop."""
    from sourceborn.witnesses import Witness, read, ORIGINAL, WITNESSED
    a = Witness("TCS share price is 2362 on the exchange", "broker", ORIGINAL)
    b = Witness("TCS share price is 2431 as quoted", "model memory", WITNESSED)
    r = read("TCS share price", [a, b])
    assert r.halt is True, "two witnesses differing on the NUMBER must halt"
    assert r.confidence != "High"
    assert any(m.kind == "conflict" for m in r.masks)
    # and agreement on the figure still passes
    c = Witness("TCS share price is 2362 confirmed", "second broker", WITNESSED)
    r2 = read("TCS share price", [a, c])
    assert not any(m.kind == "conflict" for m in r2.masks)


def test_present_fact_does_not_refuse_stable_concepts():
    """'price elasticity' and 'rate of change' are concepts, not quotes.
    Substring matching used to refuse them as moving numbers."""
    from sourceborn.present_fact import is_present_fact
    assert is_present_fact("what is price elasticity?") is False
    assert is_present_fact("explain the rate of change in calculus") is False
    assert is_present_fact("explain value investing") is False
    # while real quotes still qualify
    assert is_present_fact("what is TCS current share price") is True
    assert is_present_fact("bitcoin price now") is True
    assert is_present_fact("what is the price today") is True


def test_present_fact_catches_time_marked_number_asks():
    """A time-marked ask that wants a number back is a present fact even
    when it names no market word."""
    from sourceborn.present_fact import is_present_fact
    assert is_present_fact("what is the current population of India") is True
    assert is_present_fact("how much is gold today") is True
    # but a time-marked NON-number ask is not this rule's business
    assert is_present_fact("current CEO of OpenAI") is False




# ---------------------------------------------------------------- RH as code
# Re(s) = ½ + ti used as a build specification. These test the parts, not the
# theorem — nothing here proves anything about zeta.

def test_rh_half_caps_a_single_witness():
    """One voice never owns the answer — it caps at exactly ½."""
    from sourceborn.rh_code import half_confidence, HALF
    r = half_confidence(["the ledger"])
    assert r.confidence == HALF and r.verdict == "capped"
    assert half_confidence([]).confidence == 0.0


def test_rh_two_differing_witnesses_halt_and_never_average():
    """The Mask: the gap goes to the human, it is not turned into a number."""
    from sourceborn.rh_code import half_confidence, HALF
    r = half_confidence(["2,592 parameters", "2,578 parameters"])
    assert r.verdict == "halt" and r.confidence == HALF
    assert r.mask == ("2,592 parameters", "2,578 parameters")


def test_rh_agreement_earns_but_never_concludes():
    from sourceborn.rh_code import half_confidence, HALF
    r = half_confidence(["the letter", "the letter", "the letter"])
    assert HALF < r.confidence < 1.0 and r.verdict == "held"


def test_rh_line_check_names_the_drifting_voice():
    """A voice built at σ=0.72 is measured back at 0.72 and named; every voice
    built on the line comes back on the line. This is the drift detector."""
    import math
    from sourceborn.rh_code import Doubt, explicit_answer, line_check, drifting, periods
    voices = ["source", "witness", "memory", "doubt", "mask"]
    per = periods(voices)
    doubts = [Doubt(v, t=per[v], sigma=(0.72 if v == "memory" else 0.5)) for v in voices]
    xs = [10 ** (2 + 5 * i / 400) for i in range(401)]
    hist = {v: [explicit_answer(x / math.log(x), doubts, x).corrections[v] for x in xs]
            for v in voices}
    verdicts = line_check(hist, steps=xs, smooth=True, period_map=per)
    assert drifting(verdicts) == ["memory"]
    by = {v.who: v.sigma for v in verdicts}
    assert abs(by["memory"] - 0.72) < 0.02
    # A short run resolves the on-line voices only to ~0.03; that is the run's
    # limit, not the detector's, and every row says so rather than rounding.
    for v in voices:
        if v != "memory":
            assert abs(by[v] - 0.5) < 0.05
    assert all(not r.resolved for r in verdicts)     # honest about being short


def test_rh_a_long_enough_run_tightens_sigma_and_says_so():
    """The accuracy is set by run length. Give every voice a full cycle per
    bucket and the on-line sigmas land within 0.005 of exactly one half."""
    import math
    from sourceborn.rh_code import Doubt, explicit_answer, line_check, periods
    voices = ["source", "witness", "memory", "doubt", "mask"]
    per = periods(voices)
    doubts = [Doubt(v, t=per[v], sigma=(0.72 if v == "memory" else 0.5)) for v in voices]
    xs = [10 ** (2 + 58 * i / 2999) for i in range(3000)]
    hist = {v: [explicit_answer(x / math.log(x), doubts, x).corrections[v] for x in xs]
            for v in voices}
    verdicts = line_check(hist, steps=xs, smooth=True, period_map=per)
    by = {v.who: v.sigma for v in verdicts}
    assert all(r.resolved for r in verdicts)         # long enough now
    assert abs(by["memory"] - 0.72) < 0.01
    for v in voices:
        if v != "memory":
            assert abs(by[v] - 0.5) < 0.005


def test_rh_raw_samples_would_have_cried_wolf():
    """Why envelope() exists: measured raw, voices sitting exactly on the line
    get accused of drift. The defect is real and the smoothing is the fix."""
    import math
    from sourceborn.rh_code import Doubt, explicit_answer, line_check, drifting, periods
    voices = ["source", "witness", "memory", "doubt", "mask"]
    per = periods(voices)
    doubts = [Doubt(v, t=per[v], sigma=0.5) for v in voices]     # ALL on the line
    coarse = [1e2, 1e3, 1e4, 1e5, 1e6, 1e7]
    raw = {v: [explicit_answer(x / math.log(x), doubts, x).corrections[v] for x in coarse]
           for v in voices}
    assert drifting(line_check(raw, steps=coarse)) != []          # false alarms
    xs = [10 ** (2 + 5 * i / 400) for i in range(401)]
    fine = {v: [explicit_answer(x / math.log(x), doubts, x).corrections[v] for x in xs]
            for v in voices}
    assert drifting(line_check(fine, steps=xs, smooth=True)) == []  # none, correctly


def test_rh_off_line_voice_takes_over_the_answer():
    """The law itself: on the line no voice owns the answer; off it, one does."""
    import math
    from sourceborn.rh_code import Doubt, explicit_answer, periods
    voices = ["source", "witness", "memory", "doubt", "mask"]
    per = periods(voices)
    stable = [Doubt(v, t=per[v], sigma=0.5) for v in voices]
    drift = [Doubt(v, t=per[v], sigma=(0.72 if v == "memory" else 0.5)) for v in voices]
    x = 1e7
    a = explicit_answer(x / math.log(x), stable, x)
    b = explicit_answer(x / math.log(x), drift, x)
    assert a.share_of_loudest < 0.6            # crowd
    assert b.share_of_loudest > 0.85           # one voice
    assert b.loudest[0] == "memory"


def test_rh_periods_are_distinct_and_degeneracy_is_caught():
    """Unique factorisation as an engine rule: two voices on one beat are one
    voice counted twice."""
    from sourceborn.rh_code import periods, degeneracy
    per = periods(["a", "b", "c", "d"])
    assert len(set(per.values())) == 4
    assert degeneracy(per) == []
    per["a copy"] = per["b"]
    assert degeneracy(per) == [["b", "a copy"]]


def test_rh_explicit_answer_keeps_every_correction_visible():
    """answer = trend − Σ doubts, with the ledger intact. Nothing averaged away."""
    from sourceborn.rh_code import Doubt, explicit_answer, periods
    voices = ["a", "b", "c"]
    per = periods(voices)
    doubts = [Doubt(v, t=per[v]) for v in voices]
    led = explicit_answer(1000.0, doubts, 1e4)
    assert set(led.corrections) == set(voices)
    assert abs(led.answer - (led.trend - sum(led.corrections.values()))) < 1e-9




# ------------------------------------------------------------ sequence kernel
# The owner's six corrections made executable (docs/method/01C). These test the
# contracts, not the philosophy: "Without the ledger, closure is philosophy.
# With the ledger, closure becomes machine-executable."

def test_seq_threshold_answers_why_now():
    """A condition can exist for years without a transition. Trigger and
    threshold are separate; a threshold with no evaluator stays dormant and
    says when to recheck instead of silently passing."""
    from sourceborn.seq_kernel import Edge, Threshold, ThresholdType
    e = Edge("s", "t", "moisture reading arrived",
             Threshold(ThresholdType.VALUE, "soil moisture < X",
                       lambda c: c["moisture"] < 0.2))
    assert not e.try_fire({"moisture": 0.5})       # condition exists, no fire
    assert "dormant" in e.status
    assert e.try_fire({"moisture": 0.1})           # threshold crossed
    ne = Edge("s", "t", "event", Threshold(ThresholdType.STATE, "entity in X"))
    assert not ne.try_fire({})                     # no evaluator -> dormant
    assert "recheck when" in ne.status             # never a vague "later"


def test_seq_closure_and_entity_outcome_are_orthogonal():
    """A destruction sequence closes SUCCESS with the entity TERMINATED; a
    repair sequence closes FAILURE with the entity persisting, DEGRADED."""
    from sourceborn.seq_kernel import (ClosurePacket, SequenceClosure,
                                       EntityOutcome)
    demolition = ClosurePacket(SequenceClosure.SUCCESS, EntityOutcome.TERMINATED)
    failed_repair = ClosurePacket(SequenceClosure.FAILURE, EntityOutcome.DEGRADED)
    assert demolition.sequence_closure is SequenceClosure.SUCCESS
    assert demolition.entity_outcome is EntityOutcome.TERMINATED
    assert failed_repair.sequence_closure is SequenceClosure.FAILURE
    assert failed_repair.entity_outcome is EntityOutcome.DEGRADED


def test_seq_spawn_contract_refuses_blank_reasons():
    """A child must know why it exists and what done means."""
    from sourceborn.seq_kernel import SpawnContract, ContractError
    try:
        SpawnContract("c", "p", "n", spawn_reason="  ",
                      close_condition="done", acceptance_condition="met")
        assert False, "blank spawn_reason must be refused"
    except ContractError:
        pass


def test_seq_close_condition_is_not_acceptance_condition():
    """The water example: the child closes FAILURE honestly (search completed,
    nothing found) and the parent's requirement stays unresolved until a later
    sibling's return is accepted."""
    from sourceborn.seq_kernel import (Ledger, SpawnContract, ClosurePacket,
                                       SequenceClosure, EntityOutcome,
                                       DriverOrigin, Controller)
    led = Ledger()
    led.open_root("S0", driver=DriverOrigin.NEED, controller=Controller.SELF)
    led.spawn(SpawnContract("S0.1", "S0", "DRINK", spawn_reason="no water",
                            close_condition="search completed",
                            acceptance_condition="usable water found"))
    led.close("S0.1", ClosurePacket(SequenceClosure.FAILURE,
                                    EntityOutcome.NOT_APPLICABLE))
    assert not led.can_cross("S0", "DRINK")        # closed, but not accepted
    led.spawn(SpawnContract("S0.2", "S0", "DRINK", spawn_reason="build access",
                            close_condition="dig completed",
                            acceptance_condition="usable water found"))
    led.close("S0.2", ClosurePacket(SequenceClosure.SUCCESS,
                                    EntityOutcome.NEW_INSTANTIATED))
    assert led.can_cross("S0", "DRINK")            # superseded + accepted


def test_seq_barrier_suspends_one_node_not_the_parent():
    """THE BARRIER LAW: the blocked edge cannot be crossed, but the parent's
    independent branches keep moving."""
    from sourceborn.seq_kernel import (Ledger, SpawnContract, DriverOrigin,
                                       Controller, RowState)
    led = Ledger()
    led.open_root("S0", driver=DriverOrigin.GOAL, controller=Controller.SELF)
    led.spawn(SpawnContract("S0.1", "S0", "DEP-17", spawn_reason="missing dep",
                            close_condition="dep built",
                            acceptance_condition="dep usable"))
    assert led.state("S0") is RowState.SUSPENDED
    assert not led.can_cross("S0", "DEP-17")       # barred here
    assert led.can_cross("S0", "TEST-4")           # free elsewhere


def test_seq_parent_cannot_close_over_open_children_and_no_reopen():
    from sourceborn.seq_kernel import (Ledger, SpawnContract, ClosurePacket,
                                       SequenceClosure, EntityOutcome,
                                       DriverOrigin, Controller, BarrierError,
                                       SequenceClosedError)
    led = Ledger()
    led.open_root("S0", driver=DriverOrigin.NEED, controller=Controller.SELF)
    led.spawn(SpawnContract("S0.1", "S0", "N", spawn_reason="gap",
                            close_condition="filled", acceptance_condition="ok"))
    try:
        led.close("S0", ClosurePacket(SequenceClosure.SUCCESS,
                                      EntityOutcome.PERSISTS))
        assert False, "must not close over an open required child"
    except BarrierError:
        pass
    led.close("S0.1", ClosurePacket(SequenceClosure.SUCCESS,
                                    EntityOutcome.PERSISTS))
    led.close("S0", ClosurePacket(SequenceClosure.SUCCESS,
                                  EntityOutcome.PERSISTS))
    assert led.finished() and led.archive == ["S0"]
    try:
        led.close("S0", ClosurePacket(SequenceClosure.SUCCESS,
                                      EntityOutcome.PERSISTS))
        assert False, "a closed sequence is never reopened"
    except SequenceClosedError:
        pass
    try:
        led.spawn(SpawnContract("S0.9", "S0", "N", spawn_reason="late",
                                close_condition="x", acceptance_condition="y"))
        assert False, "spawning under a closed parent is reopening"
    except SequenceClosedError:
        pass


def test_seq_new_sequence_references_closed_one():
    """S0 does not reopen. S1 references S0 — and may only reference CLOSED
    sequences."""
    from sourceborn.seq_kernel import (Ledger, ClosurePacket, SequenceClosure,
                                       EntityOutcome, DriverOrigin, Controller)
    led = Ledger()
    led.open_root("S0", driver=DriverOrigin.NEED, controller=Controller.SELF)
    try:
        led.open_root("SX", driver=DriverOrigin.GOAL, controller=Controller.SELF,
                      references=("S0",))
        assert False, "may not reference an OPEN sequence"
    except ValueError:
        pass
    led.close("S0", ClosurePacket(SequenceClosure.SUCCESS, EntityOutcome.PERSISTS))
    led.open_root("S1", driver=DriverOrigin.GOAL, controller=Controller.SELF,
                  references=("S0",))
    assert led.state("S1").value == "open"


def test_seq_homeostasis_is_episodes_not_an_immortal_loop():
    """Repeated threshold-bounded regulation episodes, each closed — never one
    forever-open loop."""
    from sourceborn.seq_kernel import (Ledger, SpawnContract, ClosurePacket,
                                       SequenceClosure, EntityOutcome,
                                       DriverOrigin, Controller, RowState)
    led = Ledger()
    led.open_root("BODY", driver=DriverOrigin.NEED,
                  controller=Controller.DISTRIBUTED_SELF)
    for episode in ("REG.1", "REG.2"):
        led.spawn(SpawnContract(episode, "BODY", "TEMP",
                                spawn_reason="band exceeded",
                                close_condition="back in band",
                                acceptance_condition="variable within band"),
                  driver=DriverOrigin.DAMAGE)
        led.close(episode, ClosurePacket(SequenceClosure.SUCCESS,
                                         EntityOutcome.REPAIRED))
    assert led.state("REG.1") is RowState.CLOSED
    assert led.state("REG.2") is RowState.CLOSED
    assert led.state("BODY") is RowState.OPEN      # the entity's line continues
    assert led.can_cross("BODY", "TEMP")


def test_seq_want_is_a_driver_never_a_stage():
    """Want opens its own sequence beside the need-driven one; it never joins
    it. Both close independently."""
    from sourceborn.seq_kernel import (Ledger, ClosurePacket, SequenceClosure,
                                       EntityOutcome, DriverOrigin, Controller)
    led = Ledger()
    led.open_root("EAT", driver=DriverOrigin.NEED, controller=Controller.SELF)
    led.close("EAT", ClosurePacket(SequenceClosure.SUCCESS,
                                   EntityOutcome.PERSISTS))
    led.open_root("COOK", driver=DriverOrigin.WANT, controller=Controller.SELF,
                  references=("EAT",))
    led.close("COOK", ClosurePacket(SequenceClosure.SUCCESS,
                                    EntityOutcome.NEW_INSTANTIATED))
    assert led.finished() and led.archive == ["EAT", "COOK"]


def test_mypage_every_save_is_a_new_version_and_all_are_kept():
    """MY PAGE obeys the house law: every save is a new version, none is
    lost, and restoring an old layout references it instead of reopening."""
    import shutil
    import tempfile
    from sourceborn import mypage
    root = tempfile.mkdtemp(prefix="sb_mypage_")
    try:
        first = mypage.load_layout(root)
        assert first["version"] == 0 and first["sections"]
        v1 = mypage.save_layout(root, first, note="one")
        v2 = mypage.save_layout(root, v1, note="two")
        assert (v1["version"], v2["version"]) == (1, 2)
        versions = mypage.list_versions(root)
        assert [v["version"] for v in versions] == [1, 2]
        restored = mypage.save_layout(root, mypage.get_version(root, 1),
                                      note="back", references=1)
        assert restored["version"] == 3 and restored["references"] == 1
        assert mypage.get_version(root, 1)["note"] == "one"  # untouched
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_mypage_blocks_are_parked_never_deleted_and_unknowns_are_flagged():
    """A parked block survives the save, and an unknown WHAT/HOW is kept
    with a flag instead of being dropped — classify, don't reject."""
    import shutil
    import tempfile
    from sourceborn import mypage
    root = tempfile.mkdtemp(prefix="sb_mypage_")
    try:
        lay = mypage.default_layout()
        lay["sections"][0]["blocks"][0]["parked"] = True
        lay["sections"][0]["blocks"].append(
            {"id": "bx", "title": "?", "what": "no-such-feed",
             "how": "card", "parked": False})
        saved = mypage.save_layout(root, lay)
        blocks = saved["sections"][0]["blocks"]
        assert blocks[0]["parked"] is True          # parked, still present
        assert blocks[-1]["flag"].startswith("unknown what")
        again = mypage.load_layout(root)
        assert again["sections"][0]["blocks"][0]["parked"] is True
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_ladder_seed_registry_is_honest_about_what_it_knows():
    """The seed fills only what the repo verifiably knows: 18 cross-segment
    mechanisms (1 parameter each) + CON-042's size. Slots stay slots."""
    from sourceborn import ladder
    reg = ladder.seed_registry()
    assert reg["totals"] == {"segments": 10, "containers": 200,
                             "parameters": 3072, "parameters_filled": 18}
    assert len(reg["containers"]) == 200
    con42 = next(c for c in reg["containers"] if c["id"] == "CON-042")
    assert con42["target"] == 48 and con42["filled"]
    assert sum(1 for c in reg["containers"] if not c["filled"]) == 181
    assert all(p["filled"] for p in reg["parameters"])


def test_ladder_upload_merges_by_id_and_keeps_every_version():
    """His workbook lands by merge — nothing removed, every version kept."""
    import shutil
    import tempfile
    from sourceborn import ladder
    root = tempfile.mkdtemp(prefix="sb_ladder_")
    try:
        v1 = ladder.save_registry(root, {"parameters": [
            {"id": "SB-ASI-P0431", "name": "Proof-shape recognition",
             "container": "CON-042", "contains": "claim form recognition"}]},
            note="workbook slice")
        assert v1["version"] == 1
        assert v1["totals"]["parameters_filled"] == 19
        v2 = ladder.save_registry(root, {"containers": [
            {"id": "CON-001", "name": "Attention Gate", "segment": "S5"}]})
        assert v2["version"] == 2
        c1 = next(c for c in v2["containers"] if c["id"] == "CON-001")
        assert c1["filled"] and c1["segment"] == "S5"
        assert len(ladder.load_registry(root)["containers"]) == 200
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_ladder_activation_gates_always_lit_and_matches_are_named():
    """Gates run on every answer; a content match names the tokens that
    caused it — the reasoning is never a mystery."""
    from sourceborn import ladder
    reg = ladder.seed_registry()
    lit = ladder.activate("what is the Riemann hypothesis about zeros",
                          reg, extra_text="the zeta line one half")
    ids = {p["id"] for p in lit["parameters"]}
    assert {"P-X-14", "P-X-15", "P-X-09"} <= ids       # gates present
    gate = next(p for p in lit["parameters"] if p["id"] == "P-X-14")
    assert gate["reason"].startswith("gate")
    lit2 = ladder.activate("stall diagnostic of the critical logic wall", reg)
    hit = next(p for p in lit2["parameters"] if p["id"] == "P-X-07")
    assert hit["reason"].startswith("gate")             # gate wins over match


def test_ladder_hand_deselect_and_force_change_the_recall_notes():
    """Adoption is real: the notes fed to the engine change with his hand."""
    from sourceborn import ladder
    reg = ladder.seed_registry()
    lit = ladder.activate("any question at all", reg)
    base, hand = ladder.recall_notes(reg, lit, [], [])
    assert "P-X-14" in base and hand["deselected"] == []
    dropped, hand2 = ladder.recall_notes(reg, lit, [], ["P-X-14"])
    assert "P-X-14" not in dropped and hand2["deselected"] == ["P-X-14"]
    forced, hand3 = ladder.recall_notes(reg, lit, ["P-X-08"], [])
    assert "P-X-08" in forced and "P-X-08" in hand3["forced"]


def test_front_door_auth_gate():
    """Audit item 01 — the app is lockable. basic_auth_ok is the pure check
    behind the request guard; every credential path is asserted here so the
    lock is covered by the suite, not just eyeballed."""
    import base64 as _b64
    from sourceborn.server import basic_auth_ok

    def hdr(user, pw):
        return "Basic " + _b64.b64encode(f"{user}:{pw}".encode()).decode()

    # no password configured → the app is open, any header passes
    assert basic_auth_ok("", "sourceborn", "") is True
    assert basic_auth_ok(hdr("x", "y"), "sourceborn", "") is True
    # locked: correct credentials pass
    assert basic_auth_ok(hdr("sourceborn", "s3cret"), "sourceborn", "s3cret")
    # locked: wrong password, wrong user, missing header, non-basic scheme,
    # malformed base64, and a value with no colon all fail
    assert not basic_auth_ok(hdr("sourceborn", "nope"), "sourceborn", "s3cret")
    assert not basic_auth_ok(hdr("intruder", "s3cret"), "sourceborn", "s3cret")
    assert not basic_auth_ok("", "sourceborn", "s3cret")
    assert not basic_auth_ok("Bearer s3cret", "sourceborn", "s3cret")
    assert not basic_auth_ok("Basic !!!notbase64!!!", "sourceborn", "s3cret")
    assert not basic_auth_ok("Basic " + _b64.b64encode(b"nocolon").decode(),
                             "sourceborn", "s3cret")
    # a non-ASCII password must never raise (compare bytes, not str) — a
    # strong password with an accent must lock, not brick the app
    assert basic_auth_ok(hdr("sourceborn", "pä55wörd"), "sourceborn", "pä55wörd")
    assert not basic_auth_ok(hdr("sourceborn", "wrong"), "sourceborn", "pä55wörd")
    # the scheme token is case-insensitive per RFC 7617
    good = hdr("sourceborn", "s3cret")
    assert basic_auth_ok(good.replace("Basic", "basic"), "sourceborn", "s3cret")
    assert basic_auth_ok(good.replace("Basic", "BASIC"), "sourceborn", "s3cret")
    # the health path stays open by policy so Render's probe never 401s
    from sourceborn.server import OPEN_PATHS
    assert "/health" in OPEN_PATHS


def test_recall_notes_keeps_his_order_and_never_drops_a_forced_pick():
    """The selection ledger must not be re-sorted, and a parameter he
    forced in must never be the one silently cut by the cap."""
    from sourceborn import ladder
    reg = {"parameters": [{"id": f"P-{i}", "name": f"n{i}", "container": "C",
                           "filled": True, "contains": "x"} for i in range(50)]}
    lit = {"parameters": [{"id": f"P-{i}"} for i in range(40)]}
    notes, hand = ladder.recall_notes(
        reg, lit, select=["P-49", "P-45"], deselect=["P-3", "P-1"], limit=40)
    ids = [p["id"] for p in hand["speaking"]]
    assert ids[0] == "P-49" and ids[1] == "P-45"        # forced first
    assert hand["forced"] == ["P-49", "P-45"]           # his order, not sorted
    assert hand["deselected"] == ["P-3", "P-1"]         # his order, not sorted
    assert "P-3" not in ids and "P-1" not in ids        # deselected gone
    assert hand["dropped_by_cap"] == []                 # forced never dropped
    # under a tight cap the forced picks still survive; lit is what yields
    _, h2 = ladder.recall_notes(reg, lit, select=["P-49", "P-45"],
                                deselect=[], limit=3)
    assert h2["speaking"][0]["id"] == "P-49"
    assert h2["speaking"][1]["id"] == "P-45"
    assert h2["dropped_by_cap"] == []


# ===========================================================================
# THE MACHINE HE SPECIFIED — micro-sequences, pattern memory, the router.
# His canon: docs/method/canon/THE_MACHINE_AS_HE_STATES_IT.md
# ===========================================================================

HIS_FIVE = [
    ("S1", "My friend asked me to drop him somewhere. "
           "He didn't tell me where we were going."),
    ("S2", "He used my car again and left another person with me."),
    ("S3", "He again did not explain the full plan beforehand."),
    ("S4", "He asked me to drive him and didn't say where."),
    ("S5", "He didn't tell me the reason and I had already committed to go."),
]
HIS_CTX = {"self_established": True, "self_surface": "me",
           "other_surface": "he"}


def test_micro_reproduces_his_own_worked_example():
    """His spec IS the test: "He didn't tell me where we were going." must
    decompose into the exact fields he listed, and INTENT must stay unknown."""
    from sourceborn import micro
    d = micro.decompose("He didn't tell me where we were going.", "Q-1", 0)
    assert [e["side"] for e in d["entities"]].count("other") >= 1
    assert [e["side"] for e in d["entities"]].count("self") >= 1
    assert d["relation"] and "↔" in d["relation"][0]
    assert any(a["verb"] == "tell" and "disclosure" in a["classes"]
               for a in d["actions"])
    assert "didn't" in d["negation"]
    assert d["information_object"] == "location / destination"
    assert d["information_state"]["known_to_self"] == "false"
    assert "maybe" in d["information_state"]["known_to_other"]
    assert "before participation" in d["expected_information"]
    assert d["actual_information"] == "not supplied"
    assert d["temporal_relation"] == "request / action preceded disclosure"
    assert "informed decision" in d["dependency"]
    assert "≠" in d["expectation_difference"]
    # every effect he named is offered, and NONE is chosen
    for e in ("uncertainty", "confusion", "loss of control", "feeling used",
              "irritation", "distrust"):
        assert e in d["possible_human_effect"], e
    assert d["his_feeling"] == ""              # his field, never filled by us
    # RULE 1 — intent is never concluded from one event
    assert d["intent"]["status"] == "UNKNOWN — not directly observed"
    assert d["repetition_link"].startswith("search prior")
    assert "partial-information" in d["pattern_contribution"]


def test_one_sentence_never_becomes_a_pattern():
    """His reason for the whole refinement: "otherwise the machine would create
    millions of false patterns from single occurrences."
    """
    import tempfile
    from sourceborn import micro, patterns
    root = tempfile.mkdtemp()
    patterns.store_micro(root, micro.decompose_all(
        "He didn't tell me where we were going.", "S1", HIS_CTX))
    r = patterns.refresh_candidates(root)
    assert r["created"] == []                        # nothing surfaced
    assert patterns.load_candidates(root) == []
    assert patterns.count_micro(root) == 1           # but the reading is kept
    assert r["surface_at"] == 5                      # his ruling
    assert r["below_threshold"] and r["below_threshold"][0]["needs"] == 5


def test_his_five_events_surface_exactly_one_candidate_at_the_fifth():
    """The arrangement is the UNION of steps across linked events — his own S2
    carries no disclosure fact and his S3 no resource fact, yet both belong."""
    import tempfile
    from sourceborn import micro, patterns
    root = tempfile.mkdtemp()
    created_at = None
    for i, (ask, text) in enumerate(HIS_FIVE, start=1):
        patterns.store_micro(root, micro.decompose_all(text, ask, HIS_CTX))
        r = patterns.refresh_candidates(root)
        if r["created"]:
            created_at = i
    assert created_at == 5, f"surfaced at event {created_at}, not the fifth"
    cands = patterns.load_candidates(root)
    assert len(cands) == 1
    c = cands[0]
    assert c["id"] == "PATTERN-CANDIDATE-001"
    assert c["repetition_count"] == 5
    assert sorted(c["evidence_asks"]) == ["S1", "S2", "S3", "S4", "S5"]
    # the arrangement carries his steps IN ORDER, each with its own support
    op = c["observed_pattern"]
    for step in ("A needs a resource or help from B",
                 "A reveals only part of the plan",
                 "B becomes committed before the full context is known",
                 "A obtains the desired result"):
        assert step in op, step
    assert "seen in" in op and "of 5 asks" in op
    # the machine does NOT conclude
    assert c["intent_status"] == "INFERRED / NOT DIRECTLY OBSERVED"
    assert "manipulative" not in op.lower()
    assert len(c["possible_interpretations"]) >= 4
    assert "other / unknown" in c["possible_interpretations"]
    # one witness (him) → Medium cap, his own Source rule
    assert c["confidence"]["cap"] == patterns.CONF_CAP_INFERRED
    assert c["confidence"]["value"] <= patterns.CONF_CAP_INFERRED
    # the six that never collapse — five of them still empty, and they are his
    assert c["what_happened"]
    for f in ("his_interpretation", "his_feeling", "his_principle",
              "his_decision", "his_result"):
        assert c[f] == "", f
    # R-F-R / Doubt ran BEFORE he ever sees it — his flow puts it there
    assert len(c["rfr"]["r_f_r"]) == 3
    assert c["rfr"]["r_f_r"][0]["pass"].startswith("reverse")
    assert c["rfr"]["r_f_r"][1]["pass"].startswith("forward")
    assert c["rfr"]["r_f_r"][2]["pass"].startswith("reverse")
    assert "thin_steps" in c["rfr"]["r_f_r"][0]


def test_his_review_writes_back_and_never_reopens():
    """His six actions, and the no-reopen rule applied to his corrections."""
    import tempfile
    from sourceborn import micro, patterns
    root = tempfile.mkdtemp()
    for ask, text in HIS_FIVE:
        patterns.store_micro(root, micro.decompose_all(text, ask, HIS_CTX))
    patterns.refresh_candidates(root)
    cid = patterns.load_candidates(root)[0]["id"]

    res = patterns.review(root, cid, "approve", {
        "name": "Instrumental-use pattern",
        "his_interpretation": "Instrumental-use / exploitative relationship.",
        "his_feeling": "Used / disrespected / taken for granted.",
        "his_principle": "I do not want this relationship pattern.",
        "his_decision": "Reduce/cut contact.",
        "save_as": "personal pattern"}, note="APPROVED FOR MY PERSONAL RUBRIC")
    k = res["candidate"]
    assert k["status"] == "approved" and k["version"] == 2
    assert k["his_feeling"].startswith("Used")
    assert k["intent_status"].startswith("HIS RULING")
    assert k["confidence"]["value"] <= 0.95       # never 1.00, ever
    assert k["confidence"]["basis"].startswith("his ruling")
    # NO REOPEN: v1 is kept whole and still says what it said
    assert len(k["history"]) == 1
    assert k["history"][0]["snapshot"]["status"] == "candidate"
    assert k["history"][0]["snapshot"]["his_interpretation"] == ""
    # the write-back is its own record, referencing the version it acted on
    wb = res["writeback"]
    assert wb["acted_on_version"] == 1 and wb["new_version"] == 2
    assert "his_feeling" in wb["fields_he_set"]
    assert patterns.writebacks(root)[-1]["candidate"] == cid

    # his ruling reduces the threshold — "5 loops and reducing"
    assert patterns.surface_at(root) == 4

    # the approved pattern now reads a NEW sentence, carrying HIS words
    seqs = micro.decompose_all(
        "My cousin asked me to lend my car and didn't tell me why.", "Q-9",
        HIS_CTX)
    hits = patterns.activate(root, seqs)
    assert hits, "an approved pattern must read a future sentence"
    assert hits[0]["outcome"] in ("activate", "contribute evidence",
                                 "modify confidence")
    assert hits[0]["his_interpretation"].startswith("Instrumental-use")

    # bad action is refused, unknown id is refused
    assert patterns.review(root, cid, "obliterate")["error"]
    assert patterns.review(root, "nope", "approve")["error"]


def test_split_and_combine_close_records_without_deleting_them():
    import tempfile
    from sourceborn import micro, patterns
    root = tempfile.mkdtemp()
    for ask, text in HIS_FIVE:
        patterns.store_micro(root, micro.decompose_all(text, ask, HIS_CTX))
    patterns.refresh_candidates(root)
    cid = patterns.load_candidates(root)[0]["id"]
    res = patterns.review(root, cid, "split",
                          {"into": ["Partial disclosure", "Resource dependence"]})
    assert len(res["spawned"]) == 2
    cands = {c["id"]: c for c in patterns.load_candidates(root)}
    assert cands[cid]["status"] == "split"          # parent kept, not deleted
    for sid in res["spawned"]:
        assert cands[sid]["split_from"] == cid      # children reference it
        assert cands[sid]["status"] == "candidate"
    a, b = res["spawned"]
    res2 = patterns.review(root, a, "combine", {"with": [b]})
    assert res2["ok"]
    cands = {c["id"]: c for c in patterns.load_candidates(root)}
    assert cands[b]["status"] == "combined"
    assert cands[b]["combined_into"] == a           # says where it went
    assert cands[b]["history"], "the absorbed record keeps its own history"
    assert patterns.review(root, a, "combine", {"with": []})["error"]


def test_the_router_picks_mechanisms_from_the_structure():
    """His rule: "the Engine should be selected from the structured problem,
    rather than the Engine deciding what the problem is."
    """
    from sourceborn import micro, router
    seqs = micro.decompose_all("He didn't tell me where we were going.",
                               "Q-1", HIS_CTX)
    r = router.route(seqs, "why do I feel uncomfortable with this person?")
    keys = [m["key"] for m in r["mechanisms"]]
    assert "sequence" in keys                # something already there
    assert "relation" in keys                # a relation is named
    assert "evidence" in keys                # something is missing from record
    assert "meta" in keys                    # an absence has >1 reading
    assert all(m["why"] for m in r["mechanisms"])   # never called without why
    assert "selected from the structured problem" in r["rule"]

    # an INVENTION routes differently — no ground to find
    inv = router.route(micro.decompose_all("Build me a pricing app.", "Q-2"),
                       "Build me a pricing app.")
    assert "invention" in [m["key"] for m in inv["mechanisms"]]
    assert "sequence" not in [m["key"] for m in inv["mechanisms"]]

    # a repeat marked by him calls the pattern engine and names the unwired one
    rep = router.route(micro.decompose_all(
        "He again did not explain the full plan.", "Q-3", HIS_CTX), "again?")
    assert "pattern_memory" in [m["key"] for m in rep["mechanisms"]]
    assert "seq_kernel" in rep["unwired"]     # honest about what is not wired


def test_the_flow_view_shows_every_position_and_which_segments_work_there():
    """His SEG→flow placement, and his flow spine, both real."""
    from sourceborn import micro, router
    seqs = micro.decompose_all("He didn't tell me where we were going.",
                               "Q-1", HIS_CTX)
    fv = router.flow_view(router.route(seqs, "why?"))
    assert [r["position"] for r in fv] == router.FLOW_POSITIONS
    at = {r["position"]: r for r in fv}
    assert "SEG-07" in at["ultra-micro splitter"]["segments"]
    assert "SEG-08" in at["rubric view"]["segments"]
    assert "SEG-05" in at["memory"]["segments"]
    assert "SEG-10" in at["write-back"]["segments"]
    assert len(router.SEGMENT_ROLE) == 10
    assert all(s["at"] and s["serves"] for s in router.SEGMENT_ROLE)
    assert router.segments_at("pattern candidate")


def test_engine_read_runs_his_whole_flow():
    from sourceborn import patterns
    eng = _engine()
    r = eng.read("My friend asked me to drop him somewhere and "
                 "he didn't tell me where we were going.", "Q-1")
    assert len(r["micro_sequences"]) == 1        # one sentence, one micro-seq
    assert r["stored"] == 1
    assert r["route"]["mechanisms"]
    assert r["threshold"]["surface_at"] == 5
    assert r["walk"]["result"].output.answer     # the answer still happens
    assert r["stats"]["micro_sequences"] == 1
    # a second, DIFFERENT ask compares against the first
    r2 = eng.read("He again did not explain the full plan beforehand.", "Q-2")
    assert r2["relations_to_prior"], "prior asks must be compared"
    assert r2["relations_to_prior"][0]["prior_ask"] == "Q-1"
    # this ask can never corroborate itself
    assert all(x["prior_ask"] != "Q-2" for x in r2["relations_to_prior"])


def test_reading_page_and_pattern_routes_are_served_and_locked():
    import base64
    import json
    import threading
    import urllib.error
    import urllib.request
    from sourceborn import micro, patterns, server

    eng = _engine()
    root = eng.memory.root
    for ask, text in HIS_FIVE:
        patterns.store_micro(root, micro.decompose_all(text, ask, HIS_CTX))
    patterns.refresh_candidates(root)

    old = (server.ENGINE, server.SB_ROOT, server.SB_ACCESS_USER,
           server.SB_ACCESS_PASS)
    server.ENGINE, server.SB_ROOT = eng, root
    server.SB_ACCESS_USER, server.SB_ACCESS_PASS = "him", "letmein"
    httpd = server.ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % httpd.server_address[1]

    def req(p, body=None, auth=True):
        r = urllib.request.Request(
            base + p, data=json.dumps(body).encode() if body is not None else None,
            headers={"content-type": "application/json"} if body is not None else {})
        if auth:
            r.add_header("Authorization", "Basic " +
                         base64.b64encode(b"him:letmein").decode())
        try:
            with urllib.request.urlopen(r, timeout=30) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()

    try:
        for p in ("/reading", "/patterns", "/micro", "/flow"):
            assert req(p, auth=False)[0] == 401, p
            assert p not in server.OPEN_PATHS
        code, body = req("/reading")
        assert code == 200 and b"THE READING" in body
        assert b"WHAT I THINK IT MEANS" in body and b"HOW I FELT" in body

        code, body = req("/patterns")
        assert code == 200
        d = json.loads(body)
        assert len(d["candidates"]) == 1
        assert d["stats"]["approved"] == 0

        code, body = req("/reading/ask", {"question": "He didn't tell me "
                                          "where we were going."})
        assert code == 200
        r = json.loads(body)
        assert r["micro_sequences"][0]["information_object"] == \
            "location / destination"
        assert r["flow"] and len(r["flow"]) == len(
            __import__("sourceborn.router", fromlist=["x"]).FLOW_POSITIONS)
        assert r["route"]["mechanisms"]
        assert r["walk"]["result"]["output"]["answer"]
        assert req("/reading/ask", {"question": "   "})[0] == 400

        cid = d["candidates"][0]["id"]
        code, body = req("/patterns/review",
                         {"id": cid, "action": "approve",
                          "fields": {"his_interpretation": "Instrumental use.",
                                     "his_feeling": "Used.",
                                     "save_as": "personal pattern"}})
        assert code == 200
        assert json.loads(body)["candidate"]["status"] == "approved"
        assert req("/patterns/review", {"id": cid, "action": "nope"})[0] == 400

        # walk-all-the-way-back-down: the micro-sequences are readable by ask
        code, body = req("/micro?ask=S1")
        assert code == 200 and len(json.loads(body)) >= 1
        assert req("/micro?n=abc")[0] == 200      # bad query answers, no drop

        code, home = req("/")
        assert code == 200 and b'href="/reading"' in home
    finally:
        httpd.shutdown()
        httpd.server_close()
        (server.ENGINE, server.SB_ROOT, server.SB_ACCESS_USER,
         server.SB_ACCESS_PASS) = old



def test_his_correction_of_left_and_nothing_changes_the_parse():
    """His teaching, 2026-08-13: "left" is not departure, it is what REMAINS;
    "nothing" is not zero, it is zero MATERIAL return. Filed in
    docs/method/canon/LEFT_AND_NOTHING_HIS_CORRECTION.md."""
    import tempfile
    from sourceborn import micro, senses
    root = tempfile.mkdtemp()
    S = senses.active(root)
    sent = ("A good person left with memories of their beloved and "
            "responsibility keep them safe and alive")

    # without his correction, "left" is a departure verb
    plain = micro.decompose(sent, "Q", 0)
    assert any(a["verb"] == "left" and "participation" in a["classes"]
               for a in plain["actions"])

    # with it, the departure reading is BLOCKED and both readings are kept
    d = micro.decompose(sent, "Q", 0, {"self_established": True}, S)
    left = next(a for a in d["actions"] if a["verb"] == "left")
    assert "participation" not in left["classes"]
    assert "participation" in left["blocked_by_his_sense"]
    ids = {o["id"] for o in d["semantic_overrides"]}
    assert "SENSE-001" in ids
    o = next(o for o in d["semantic_overrides"] if o["id"] == "SENSE-001")
    assert "departed" in o["default_reading"]          # what it WOULD have read
    assert "remains with the person" in o["his_reading"]
    assert o["status"] == senses.STATUS_USER

    # the raw sentence is never altered
    assert d["raw"] == sent

    # his structure, found because he taught it
    assert micro.F_RETURN_RESIDUAL in d["structural_facts"]
    assert micro.F_DUTY_CONTINUES in d["structural_facts"]
    assert micro.F_MEMORY_WEIGHTED in d["structural_facts"]
    assert "emotional accumulation" in d["pattern_contribution"]
    assert "responsibility persistence" in d["pattern_contribution"]
    # and the false readings his correction removes
    assert micro.F_THIRD_PARTY not in d["structural_facts"]
    assert micro.F_REPEAT_MARKED not in d["structural_facts"]


def test_nothing_is_never_read_as_zero_overall():
    """His rule: "'nothing' itself must not be interpreted literally without
    its dimension." An unstated dimension says unstated, never zero."""
    import tempfile
    from sourceborn import micro, senses
    root = tempfile.mkdtemp()
    S = senses.active(root)
    d = micro.decompose("He worked for them and got nothing, only memories "
                        "and moments.", "Q", 0, {"self_established": True}, S)
    rr = d["return_reading"]["dimensions"]
    assert "near zero" in rr["material"]
    assert "does NOT mean zero overall" in rr["material"]
    assert rr["emotional"] == "present"
    assert rr["memory"] == "present"
    assert rr["experiential"] == "present"
    # dimensions he did not speak to are UNSTATED, not zero
    assert rr["practical"] == "not stated"
    assert set(rr) == set(senses.RETURN_DIMENSIONS)


def test_memory_valence_is_never_used_as_value():
    """His rule: "Good or bad, memories are always emotional count for human."
    pleasantness != importance; pain != worthlessness."""
    import tempfile
    from sourceborn import micro, senses
    root = tempfile.mkdtemp()
    S = senses.active(root)
    for text, want in (
            ("I keep the good memories of her.", "positive"),
            ("Only painful memories are left of that time.", "negative"),
            ("The memories are still with me.", "unknown")):
        d = micro.decompose(text, "Q", 0, {"self_established": True}, S)
        mr = d["memory_reading"]
        assert mr, text
        assert mr["valence"] == want, (text, mr["valence"])
        # significance NEVER varies with valence — that is the whole rule
        assert mr["significance"] == \
            "emotionally weighted regardless of valence"
        assert "pain ≠ worthlessness" in mr["never"]


def test_he_refuses_the_overgeneralisation_himself_and_it_is_recorded():
    """He named the danger: "A person who gets nothing in return is
    automatically good. That would be a dangerous overgeneralization." The
    refusal lives ON the rule that could have produced it."""
    import tempfile
    from sourceborn import senses
    root = tempfile.mkdtemp()
    good = next(e for e in senses.active(root) if e["word"] == "good person")
    assert good["status"] == senses.STATUS_REVIEW      # not fact yet
    assert "NOT automatically good" in good["refuses"]
    assert "dangerous overgeneralization" in good["refuses"]
    assert "behavioural structure" in good["his_reading"]
    mem = next(e for e in senses.active(root) if e["word"] == "memory")
    assert "SEPARATELY from" in mem["his_reading"]
    assert senses.stats(root)["with_refusal"] >= 2


def test_teaching_a_sense_writes_back_and_never_reopens():
    import tempfile
    from sourceborn import senses
    root = tempfile.mkdtemp()
    r = senses.teach(root, "carry", "to hold responsibility over time, not to "
                     "physically lift", "to physically lift something",
                     note="his words")
    assert r["ok"] and r["sense"]["version"] == 1
    r2 = senses.teach(root, "carry", "to hold responsibility AND the cost of it",
                      note="refined")
    s = r2["sense"]
    assert s["version"] == 2
    assert len(s["history"]) == 1
    assert s["history"][0]["snapshot"]["his_reading"].endswith("physically lift")
    assert r2["writeback"]["acted_on_version"] == 1
    assert r2["writeback"]["new_version"] == 2
    assert senses.writebacks(root)[-1]["word"] == "carry"

    # rejection CLOSES, never deletes
    rj = senses.reject(root, s["id"], note="wrong after all")
    assert rj["sense"]["status"] == "REJECTED BY HIM"
    assert rj["sense"]["reject_note"] == "wrong after all"
    assert any(e["id"] == s["id"] for e in senses.load(root))     # still there
    assert not any(e["id"] == s["id"] for e in senses.active(root))

    assert senses.teach(root, "", "x")["error"]
    assert senses.teach(root, "x", "")["error"]
    assert senses.teach(root, "x", "y", kind="nope")["error"]
    assert senses.reject(root, "SENSE-999")["error"]


def test_senses_routes_serve_and_teach_over_http():
    import base64
    import json
    import threading
    import urllib.error
    import urllib.request
    from sourceborn import server

    eng = _engine()
    old = (server.ENGINE, server.SB_ROOT, server.SB_ACCESS_USER,
           server.SB_ACCESS_PASS)
    server.ENGINE, server.SB_ROOT = eng, eng.memory.root
    server.SB_ACCESS_USER, server.SB_ACCESS_PASS = "him", "letmein"
    httpd = server.ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % httpd.server_address[1]

    def req(p, body=None, auth=True):
        r = urllib.request.Request(
            base + p, data=json.dumps(body).encode() if body is not None else None,
            headers={"content-type": "application/json"} if body is not None else {})
        if auth:
            r.add_header("Authorization", "Basic " +
                         base64.b64encode(b"him:letmein").decode())
        try:
            with urllib.request.urlopen(r, timeout=30) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()

    try:
        assert req("/senses", auth=False)[0] == 401
        assert "/senses" not in server.OPEN_PATHS
        code, body = req("/senses")
        assert code == 200
        d = json.loads(body)
        assert len(d["senses"]) >= 4
        assert d["stats"]["with_refusal"] >= 2
        assert len(d["return_dimensions"]) == 8

        code, body = req("/senses/teach",
                         {"word": "left", "his_reading": "what remains, and "
                          "the weight that stays with it",
                          "note": "sharpened"})
        assert code == 200
        assert json.loads(body)["sense"]["version"] == 2   # write-back, not new
        assert req("/senses/teach", {"word": "", "his_reading": "x"})[0] == 400

        # and the reading now shows his corrections
        code, body = req("/reading/ask", {"question": "A good person left with "
                                          "memories of their beloved."})
        assert code == 200
        r = json.loads(body)
        assert r["senses_fired"], "his corrections must appear in the reading"
        assert any(o["id"] == "SENSE-001" for o in r["senses_fired"])
        assert r["senses"]["senses"] >= 4

        code, page = req("/reading")
        assert b"DEFAULT LANGUAGE INTERPRETATION" in page
        assert b"YOUR CORRECTION" in page
    finally:
        httpd.shutdown()
        httpd.server_close()
        (server.ENGINE, server.SB_ROOT, server.SB_ACCESS_USER,
         server.SB_ACCESS_PASS) = old



def test_human_means_the_physical_human_not_the_brain():
    """His ruling: "Human = the physical human: body, appearance, biological
    condition, safety, survival, ageing/life-extension, physical capacity.
    Human is not the thinking/memory/reasoning brain."
    """
    from sourceborn import domains as D, human_registry as HR
    q = ("A good person left with memories of their beloved and "
         "responsibility keep them safe and alive")
    w = D.route_words(q)
    cls = w["classes"]
    # his arrow chart, word for word
    assert "good" in cls[D.VALUE_WISDOM]
    assert "person" in cls[D.HUMAN_PHYSICAL]
    assert "safe" in cls[D.HUMAN_PHYSICAL]
    assert "alive" in cls[D.HUMAN_PHYSICAL]
    assert "memories" in cls[D.BRAIN_MIND]
    assert "beloved" in cls[D.RELATION_AFFECT]
    assert "responsibility" in cls[D.RULE_DUTY]
    assert "left with" in cls[D.RESULT_CONSEQUENCE]
    # and the five things that are NOT Human physical, by his rule
    for word in ("memories", "beloved", "responsibility", "good"):
        assert word not in cls.get(D.HUMAN_PHYSICAL, []), word

    # the containers HE named by hand — lexical overlap cannot find these
    named = {t["container"] for t in w["his_targets"] if t["container"]}
    assert {"CON-006", "CON-001", "CON-008"} <= named
    sc = D.enforce_scope(HR.activate(q)["containers"], w)
    human = [c for c in sc["in_scope"] if c["domain"] == D.HUMAN_PHYSICAL]
    hids = {c["id"] for c in human}
    assert {"CON-001", "CON-006", "CON-008"} <= hids
    assert any(c.get("his_assignment") for c in human)
    # memory stays in its own brain, never under Human
    brain = {c["id"] for c in sc["in_scope"] if c["domain"] == D.BRAIN_MIND}
    assert "CON-033" in brain               # Episodic Memory
    assert not (brain & hids)               # the two never overlap


def test_not_the_brain_is_an_explicit_boundary():
    """His second test sentence, and the EXCLUSION / BOUNDARY node it needs."""
    from sourceborn import domains as D, human_registry as HR
    q = ("Humans are looking at their physical appearance and body life "
         "extension, not the brain")
    w = D.route_words(q)
    assert D.BRAIN_MIND in w["excluded_classes"]
    assert w["excluded"] and "not the brain" in w["excluded"][0]["text"].lower()
    for word in ("physical", "appearance", "body"):
        assert word in w["classes"][D.HUMAN_PHYSICAL], word
    assert "looking at" in w["classes"][D.ATTENTION_GOAL]

    sc = D.enforce_scope(HR.activate(q)["containers"], w)
    # brain containers are reported OUT of scope with his reason, not deleted
    out_brain = [c for c in sc["out_of_scope"] if c["domain"] == D.BRAIN_MIND]
    assert out_brain
    assert all("excluded this layer" in c["why_out"] for c in out_brain)
    assert not any(c["domain"] == D.BRAIN_MIND for c in sc["in_scope"])
    # and the body containers he pointed at are in
    assert any(c["id"] in ("CON-015", "CON-011", "CON-001", "CON-007")
               for c in sc["in_scope"])


def test_the_overlay_never_touches_his_source_records():
    """His instruction: separate the physical subset from the cognitive subset
    "WITHOUT DELETING the original source records."
    """
    from sourceborn import domains as D, human_registry as HR
    assert len(HR.parameters()) == 3204          # his count, unchanged
    assert len(HR.containers()) == 80
    c = HR.container("CON-015")
    # his own name, not renamed to fit the split
    assert c["name"] == "Body Schema, Body Image and Ownership"
    assert len(c["subs"]) == 40
    st = D.stats()
    assert st["containers_classified"] == 80     # every one placed
    assert st["mixed_flagged"] >= 8              # the ambiguous ones surfaced
    assert "CON-015" in st["mixed"]              # the one HE flagged himself
    assert "mental" in st["mixed"]["CON-015"].lower()
    assert "untouched" in st["overlay_only"]
    # every class he named exists and is used
    used = set(D.CONTAINER_DOMAIN.values())
    assert D.HUMAN_PHYSICAL in used and D.BRAIN_MIND in used
    assert D.RELATION_AFFECT in used and D.RULE_DUTY in used
    assert D.VALUE_WISDOM in used and D.ATTENTION_GOAL in used
    # his scope lists, verbatim
    assert "life continuation" in " ".join(D.HUMAN_INCLUDE) or \
        "longevity" in D.HUMAN_INCLUDE
    assert "memory" in D.HUMAN_EXCLUDE and "reasoning" in D.HUMAN_EXCLUDE


def test_the_reading_reports_the_split():
    eng = _engine()
    r = eng.read("Humans are looking at their physical appearance and body "
                 "life extension, not the brain", "Q-dom")
    from sourceborn import domains as D
    assert D.BRAIN_MIND in r["word_routes"]["excluded_classes"]
    assert D.HUMAN_PHYSICAL in r["rubrics_lit"]["by_domain"]
    assert r["rubrics_lit"]["out_of_scope"]
    assert r["domains"]["containers_classified"] == 80
    assert r["registry"]["parameters"] == 3204



RICE = ("Do not judge him because he sells just rice, judge the idea of "
        "business. His MBA helped him find flaws, think and plan better and "
        "upscale to 800 crore revenue, instead of working for big firms. "
        "No business is small.")


def test_his_rice_mba_sentence_routes_to_his_own_node_classes():
    """His arrow chart for this sentence, and his own observation that it has
    almost zero Human-body activation."""
    from sourceborn import domains as D
    w = D.route_words(RICE)
    cls = w["classes"]
    assert "do not judge" in cls[D.JUDGMENT_BIAS]
    assert "rice" in cls[D.PRODUCT_SURFACE]
    assert "business" in cls[D.BUSINESS_SYSTEM]
    assert "mba" in cls[D.EDUCATION_CAPABILITY]
    assert "upscale" in cls[D.SCALE_GROWTH]
    assert "revenue" in cls[D.RESULT_MEASUREMENT]
    assert "instead of" in cls[D.COUNTERFACTUAL_PATH]
    assert "find flaws" in cls[D.BRAIN_MIND]
    # HIS OWN READING: "this sentence has almost zero Human-body activation"
    assert D.HUMAN_PHYSICAL not in cls


def test_a_stated_number_is_never_upgraded_to_a_verified_fact():
    from sourceborn import claims as C
    rows = C.read_claims(RICE)
    by = {r["status"]: r for r in rows}
    assert C.SOURCE_ASSERTED in by
    assert "800" in by[C.SOURCE_ASSERTED]["text"]
    assert by[C.SOURCE_ASSERTED]["verified_here"] is False
    assert "never be shown as FACT" in by[C.SOURCE_ASSERTED]["refuses"]

    # "MBA helped him" is a HYPOTHESIS and his alternatives are kept beside it
    assert C.CAUSAL_HYPOTHESIS in by
    alts = by[C.CAUSAL_HYPOTHESIS]["alternatives"]
    for a in ("market timing", "capital", "luck", "team", "execution"):
        assert a in alts, a
    assert "must not be recorded as" in by[C.CAUSAL_HYPOTHESIS]["refuses"]

    # "no business is small" is his value, not evidence
    assert C.USER_VALUE in by
    # "instead of working for big firms" is a counterfactual, not a verdict
    assert C.COUNTERFACTUAL in by
    assert "universally" in by[C.COUNTERFACTUAL]["refuses"]

    # a plain statement with no figure and no causal word stays FACT-IN-SOURCE
    plain = C.read_claims("He sells rice.")
    assert plain[0]["status"] == C.FACT_IN_SOURCE
    assert "not the same as being" in plain[0]["why"]


def test_revenue_is_not_profit_is_not_a_good_business():
    from sourceborn import claims as C
    o = C.outcome_note(RICE)
    assert "revenue" in o["named"]
    assert "profit" in o["not_stated"]      # never assumed
    assert "durability" in o["not_stated"]
    assert o["his_rule"].startswith("HIGH REVENUE")
    assert C.outcome_note("I feel tired today") == {}


def test_the_judgment_gate_refuses_a_verdict_until_his_chain_is_walked():
    """His words: "That is exactly the kind of reasoning your Rubric Pyramid
    should FORCE before the ASI reaches a conclusion."
    """
    from sourceborn import claims as C
    g = C.judgment_gate(RICE)
    steps = {s["key"]: s for s in g["chain"]}
    for k in ("visible_thing", "find_system", "capabilities", "inputs",
              "execution", "results"):
        assert steps[k]["met"], k
    # his own reasoning never compared the alternatives, so the gate holds
    assert steps["alternatives"]["met"] is False
    assert g["may_judge"] is False
    assert "JUDGMENT NOT SUPPORTED YET" in g["verdict"]
    assert "COMPARE ALTERNATIVE EXPLANATIONS" in g["unmet"]
    # the premature-verdict wording is caught by the second step
    assert "shortcut" in steps["do_not_judge_yet"]["note"]

    # a bare surface sentence reaches almost nothing
    bare = C.judgment_gate("He just sells rice, small business.")
    assert bare["may_judge"] is False
    assert len(bare["unmet"]) >= 4


def test_his_five_named_patterns_keep_the_mark_he_gave_them():
    from sourceborn import claims as C
    names = [p["name"] for p in C.HIS_PATTERNS]
    assert "Surface Simplicity ≠ System Simplicity" in names
    assert "Product Prestige ≠ Business Performance" in names
    assert "MBA as Capability Amplifier" in names
    checked = {p["name"] for p in C.HIS_PATTERNS if p["his_mark"] == "checked"}
    unchecked = {p["name"] for p in C.HIS_PATTERNS if p["his_mark"] != "checked"}
    assert len(checked) == 3 and len(unchecked) == 2      # his own marks
    assert "MBA as Capability Amplifier" in unchecked
    amp = next(p for p in C.HIS_PATTERNS if "Amplifier" in p["name"])
    assert "AMPLIFIER" in amp["reading"]
    assert amp["refuses"] == "MBA → success as a cause"
    surf = next(p for p in C.HIS_PATTERNS if "Surface" in p["name"])
    assert "tea stall" in surf["applies_to"] and "logistics" in surf["applies_to"]


def test_the_reading_carries_the_gate_and_the_statuses():
    eng = _engine()
    r = eng.read(RICE, "Q-rice")
    assert r["judgment_gate"]["may_judge"] is False
    assert any(c["status"] == "SOURCE-ASSERTED / NOT VERIFIED HERE"
               for c in r["claims"])
    assert r["outcome_note"]["not_stated"]
    assert len(r["his_named_patterns"]) == 5
    from sourceborn import domains as D
    assert D.HUMAN_PHYSICAL not in r["word_routes"]["classes"]



FATHER = ("A father checks the front door five times every night. Their house "
          "was robbed once years ago. The lock has since been replaced and he "
          "knows he already checked it, but he goes back again because he says "
          "he wants his family safe. His family gets irritated.")


def test_same_action_changed_function():
    """HIS principle: "identical physical action ≠ identical functional role."
    CHECK #1 obtains information; CHECK #2-5 cannot obtain what #1 already did.
    The pattern engine was blind to this because it keys on CONTENT, and five
    checks have identical content — the difference is ORDINAL POSITION.
    """
    from sourceborn import repetition as R
    r = R.read_repetition(FATHER)
    assert r["applies"]
    assert "checks" in r["actions"]
    assert r["count"]["count"] == 5                 # from "five times"
    assert r["count"]["exact"] is False or r["count"]["stated_as"]
    assert r["actor_knows_already"] is True         # the source says so
    assert r["same_action_changed_function"] is True

    occ = r["occurrences"]
    assert occ[0]["position"] == R.FIRST
    assert occ[0]["function"] == R.FUNC_ACQUIRE
    assert occ[0]["candidates"] == []               # the first is not open
    for o in occ[1:]:
        assert o["position"] == R.LATER
        assert o["function"] == R.FUNC_CANNOT_ACQUIRE
        assert "already knows" in o["function_status"]
        # HIS candidates, held open and NONE chosen
        for c in ("certainty", "reassurance", "ritual", "habit"):
            assert c in o["candidates"], c
        assert "does not pick" in o["refuses"]

    assert "identical physical action" in r["his_principle"]
    assert "rereading" in " ".join(r["generalises_to"])


def test_position_gives_the_first_and_later_different_addresses():
    """The fix itself: before this, five identical checks collapsed into ONE
    signature and the pattern layer reported "this recurs"."""
    from sourceborn import repetition as R
    r = R.read_repetition(FATHER)
    base = "resource:requested|disclosure:withheld"
    first = R.position_signature(base, r["occurrences"][0])
    later = R.position_signature(base, r["occurrences"][1])
    assert first != later
    assert first.endswith("occ:first") and later.endswith("occ:later")
    assert base in first and base in later          # the content is preserved

    # a single occurrence is not dressed up as a repetition
    one = R.read_repetition("He checked the door.")
    assert one["count"]["count"] == 1
    assert one["occurrences"][0]["position"] == R.ONLY
    assert one["same_action_changed_function"] is False
    assert "absent, not zero" in one["count"]["why"]

    # repetition WITHOUT the source saying he already knows is not a
    # changed-function claim — it stays open
    unknown = R.read_repetition("He checks the door five times every night.")
    assert unknown["count"]["count"] == 5
    assert unknown["actor_knows_already"] is False
    assert unknown["same_action_changed_function"] is False
    assert "OPEN" in unknown["occurrences"][1]["function_status"]

    # a sentence with no information-action does not get this reading at all
    none = R.read_repetition("He drove to work five times.")
    assert none["applies"] is False


def test_the_mask_extended_to_observer_position():
    """HIS rule: BEHAVIOR ≠ MEANING. Two readings of ONE behaviour, and the
    existing Source/Mask rule reused — two witnesses who differ HALT, the gap
    goes to him, never averaged."""
    from sourceborn import repetition as R
    v = R.read_views(FATHER)
    assert v["count"] == 2 and v["differ"] is True
    by = {x["position"]: x for x in v["views"]}
    assert R.ACTOR in by and R.OBSERVER in by
    # the states must NOT bleed between the two readings
    assert by[R.ACTOR]["states"] == ["safe"]
    assert by[R.OBSERVER]["states"] == ["irritated"]
    assert "SOURCE-STATED" in by[R.ACTOR]["status"]
    assert "not necessarily the same thing" in by[R.ACTOR]["status"]
    assert "not evidence" in by[R.OBSERVER]["status"]

    m = v["mask"]
    assert m["verdict"] == "HALT — the gap goes to him"
    assert "not averaged" in m["refuses"]
    assert "neither reading is preferred" in m["refuses"]
    assert v["confidence_cap"].startswith("HALT")
    assert "BEHAVIOR ≠ MEANING" in v["his_rule"]

    # one view only → capped at Medium, his one-witness rule
    solo = R.read_views("He goes back again because he says he wants them safe.")
    assert solo["count"] == 1 and solo["differ"] is False
    assert solo["mask"] == {}
    assert "Medium" in solo["confidence_cap"]

    # no marked view at all → says so, rather than inventing one
    bare = R.read_views("The door was checked.")
    assert bare["count"] == 0
    assert "no view is marked" in bare["confidence_cap"]


def test_the_reading_carries_position_and_the_two_views():
    from sourceborn import micro
    m = micro.decompose("He checks the door five times and he knows he "
                        "already checked it.", "Q", 0)
    assert m["repetition_reading"]["same_action_changed_function"] is True
    assert "occ:first" in m["signature"]        # position is in the address now

    eng = _engine()
    r = eng.read(FATHER, "Q-father")
    # THE BUG A BROWSER FOUND AND THE UNIT TESTS MISSED: the engine splits the
    # ask into sentences, so "checks five times" (sentence 1) and "he knows he
    # already checked it" (sentence 3) never met, and the reading said "not
    # supported yet" on the exact example it was built for. Both of these must
    # be read at ASK level.
    assert r["repetition"], "the reading must carry the position analysis"
    rr = r["repetition"][0]
    assert rr["count"]["count"] == 5, "the count is in sentence 1"
    assert rr["actor_knows_already"] is True, "the knowledge is in sentence 3"
    assert rr["same_action_changed_function"] is True

    assert r["views"], "the reading must carry the observer split"
    v = r["views"][0]
    assert v["differ"] is True
    st = {x["position"]: x["states"] for x in v["views"]}
    assert st["ACTOR"] == ["safe"], "his stated goal is in sentence 3"
    assert st["OBSERVER"] == ["irritated"], "their state is in sentence 4"
    assert v["mask"]["verdict"].startswith("HALT")

    # the per-sentence rows are still kept — they are what the signature uses
    assert r["repetition_per_sentence"]
    assert r["repetition_stats"]["later_function_candidates"] == 6

# ---------------------------------------------------------------------------
# THE PYRAMID — his answer, built. docs/method/canon/THE_PYRAMID_HIS_ANSWER.md
# ---------------------------------------------------------------------------

HIS_SENTENCE = ("Samrath never like to go to school, he always cry, "
                "but today is his birthday, he went very happy.")


def test_his_flat_addressing_is_exact():
    """SB-HFR-P0001..P3204 — he derived this by hand. Every number he cited must
    land on the name he gave it, including the two containers holding 42."""
    from sourceborn import asi_pyramid as P
    assert P.bank_size() == 3204
    assert P.container_span("CON-035") == (1361, 1400)
    assert P.container_span("CON-036") == (1401, 1440)
    assert P.container_span("CON-057") == (2243, 2284), "CON-042 holds 42"
    assert P.container_span("CON-060") == (2365, 2404), "CON-057 holds 42 too"
    assert P.container_span("CON-064") == (2525, 2564)
    his = {1374: "Context-cued habit", 1403: "Context association",
           1438: "Conditioned emotional response", 2243: "Core valence",
           2254: "Happiness", 2282: "Emotional intensity",
           2284: "Emotional-state transition", 2366: "Reward anticipation",
           2368: "Hedonic", 2376: "Approach behaviour", 2388: "Social reward",
           2454: "Effort willingness", 2464: "Approach motivation",
           2465: "Avoidance motivation", 2500: "Intention revision",
           2514: "Opportunity-triggered intention",
           2563: "Motive stability vs shift",
           2564: "Motive-inference confidence"}
    for flat, name in his.items():
        got = P.param(flat)["name"]
        assert name.lower() in got.lower(), f"P{flat}: his '{name}' vs '{got}'"
    assert P.flat_of("CON-057", 12) == 2254
    assert P.param(2254)["sb_id"] == "SB-HFR-P2254"


def test_his_eighteen_on_his_sentence():
    """His count, not near his count: 7 strong + 11 candidate = 18 / 3204."""
    from sourceborn import asi_pyramid as P
    a = P.activate(HIS_SENTENCE)
    c = a["counts"]
    assert c["strong"] == 7, c
    assert c["candidate"] == 11, c
    assert c["working"] == 18
    assert c["inactive"] == 3186
    assert c["pct"] == 0.56
    strong = {r["flat"] for r in a["strong"]}
    assert strong == {1403, 2243, 2254, 2282, 2284, 2368, 2376}, strong
    cand = {r["flat"] for r in a["candidate"]}
    assert cand == {1374, 1438, 2366, 2388, 2454, 2464, 2465, 2500, 2514,
                    2563, 2564}, cand
    # his chart marked P2564 HIT while his list places it under CANDIDATE —
    # carried, not silently resolved
    note = [r for r in a["candidate"] if r["flat"] == 2564][0]
    assert "his chart" in note["his_note"]


def test_prior_and_current_are_two_scopes_not_one_flat_sentence():
    from sourceborn import asi_pyramid as P
    s = P.read_scopes(HIS_SENTENCE)
    assert s["time_scopes"] == 2
    prior = [r["clause"] for r in s[P.PRIOR]]
    cur = [r["clause"] for r in s[P.CURRENT]]
    assert any("never" in c for c in prior)
    assert any("always cry" in c for c in prior)
    assert any("birthday" in c for c in cur)
    assert any("went very happy" in c for c in cur), \
        "a clause with no marker of its own continues the scope it is in"
    assert s["edge_word"] == "but"


def test_same_event_shell_is_one_object_with_two_routes():
    from sourceborn import asi_pyramid as P
    sh = P.event_shell(HIS_SENTENCE)
    assert sh["shell"] == "GO_TO_SCHOOL", sh["shell"]
    assert sh["object"] == "school", "'to go' is the infinitive, not the place"
    assert sh["unchanged"] is True
    kinds = {v["surface"]: v["kind"] for v in sh["verb_forms"]}
    assert kinds["went"] == "actual behaviour"
    assert kinds["go"] == "stated/desired"


def test_crying_is_never_upgraded_to_sadness():
    from sourceborn import asi_pyramid as P
    r = P.run(HIS_SENTENCE)
    beh = r["behaviour_not_state"]["readings"]
    assert beh and beh[0]["behaviour"] == "cry"
    assert beh[0]["status"] == "unresolved"
    assert "possible sadness" in beh[0]["possible"]
    assert len(beh[0]["possible"]) == 7, "his seven, including 'possible other'"
    # and Sadness itself must not be in the activated set
    flats = {x["flat"] for x in r["activation"]["strong"]} | \
            {x["flat"] for x in r["activation"]["candidate"]}
    assert 2250 not in flats, "P2250 Sadness is not a fact because he cried"


def test_causality_is_not_closed_and_the_branches_are_opened():
    from sourceborn import asi_pyramid as P
    d = P.run(HIS_SENTENCE)["difference"]
    assert d["status"] == "CAUSALITY NOT PROVEN"
    assert d["what_changed"] == ["birthday"]
    assert "BIRTHDAY = today" in d["we_know"]
    assert any("caused" in x for x in d["we_do_not_know"])
    assert len(d["hidden_branches"]) == 10, "his ten"
    assert "gifts?" in d["hidden_branches"]
    assert "fabrication" in d["fabrication_example"]


def test_two_intent_candidates_are_never_blended():
    from sourceborn import asi_pyramid as P
    i = P.run(HIS_SENTENCE)["intent"]
    assert len(i["candidates"]) == 2
    assert i["blended"] is False
    ids = {c["id"] for c in i["candidates"]}
    assert ids == {"INTENT CANDIDATE A", "INTENT CANDIDATE B"}


def test_pattern_candidate_carries_his_four_guards():
    from sourceborn import asi_pyramid as P
    pc = P.run(HIS_SENTENCE)["pattern_candidate"]
    assert pc["id"] == "PC-CONTEXT-INTENT-001"
    assert pc["assembled"] is True
    assert pc["guards"]["evidence_cases"] == "1 current contrast"
    assert pc["guards"]["cause"] == "UNKNOWN"
    assert pc["guards"]["generalization"] == "NOT ALLOWED YET"
    refused = {x["claim"] for x in pc["refused"]}
    assert "Birthday makes children like school." in refused
    assert pc["next"] == ["DOUBT / R-F-R", "USER REVIEW"]


def test_the_rule_has_no_fixed_number_after_the_plus_signs():
    from sourceborn import asi_pyramid as P
    assert P.THE_RULE["no_fixed_number"] is True
    assert P.THE_RULE["sum"][-1] == "..."
    assert "PRIOR PATTERN" in P.THE_RULE["machine"]


def test_sequence_runtime_objects_are_not_parameters():
    from sourceborn import asi_pyramid as P
    rt = P.run(HIS_SENTENCE)["runtime"]
    got = {o["what"]: o["n"] for o in rt["objects"]}
    assert got["time scopes"] == 2
    assert got["contrast edge"] == 1
    assert got["contextual event"] == 1
    assert got["emotional state transition"] == 1
    assert got["intent-state candidates"] == 2
    assert got["causal gap"] == 1
    assert rt["then"] == ["PATTERN CANDIDATE", "DOUBT / R-F-R", "USER REVIEW"]


def test_it_is_a_mechanism_not_a_lookup_of_his_sentence():
    """Different words, same shape -> the same 18. A flat report -> almost
    nothing. This is the test that fails if the routes are hard-wired to the
    literal words 'Samrath', 'school' or 'birthday'."""
    from sourceborn import asi_pyramid as P
    other = ("Ravi never wants to go to the gym, he always shouted, "
             "but today is his match, he went really excited.")
    a = P.activate(other)
    assert a["counts"]["strong"] == 7
    assert a["counts"]["candidate"] == 11
    assert P.event_shell(other)["shell"] == "GO_TO_GYM"
    assert P.run(other)["difference"]["what_changed"] == ["match"]

    flat = P.activate("He went to school today.")
    assert flat["counts"]["strong"] == 0, "no flip, no history, no claim"
    assert flat["counts"]["working"] == 1


def test_positive_words_do_not_all_collapse_into_happiness():
    """His v1.0 source separates the emotions and says they must not be
    collapsed. "excited" is his Excitement, never his Happiness."""
    from sourceborn import asi_pyramid as P
    a = P.activate("Ravi never wants to go to the gym, he always shouted, "
                   "but today is his match, he went really excited.")
    flats = {r["flat"]: r for r in a["strong"]}
    assert 2256 in flats, "P2256 Excitement"
    assert 2254 not in flats, "P2254 Happiness must not fire on 'excited'"
    assert flats[2256]["by"] == "word -> his name (mine, correctable)"
    b = P.activate(HIS_SENTENCE)
    his = {r["flat"]: r for r in b["strong"]}
    assert his[2254]["by"] == "HIS ASSIGNMENT", "'happy'->Happiness is his row"


def test_a_shape_he_has_not_named_is_reported_unnamed_not_empty():
    from sourceborn import asi_pyramid as P
    pc = P.run("Meera always laughed about the exam, but today is her result, "
               "she went very worried.")["pattern_candidate"]
    assert pc["assembled"] is False
    assert pc["missing"], "it must say which part of his form is absent"
    assert pc["unnamed_shape"] is True, \
        "positive prior -> negative today is a real shape he has not named"


def test_his_chart_is_generated_from_the_run_not_typed_out():
    from sourceborn import asi_pyramid as P
    text = P.chart(P.run(HIS_SENTENCE))
    for must in ("PRIOR / REPEATED", "CURRENT / TODAY", "SAME EVENT SHELL",
                 "GO_TO_SCHOOL", "WORKING ACTIVE SET      18 / 3204",
                 "3186 remain inactive", "P2243-P2284", "DOUBT / R-F-R"):
        assert must in text, must



# --- HIS SECOND RUN: the 16 containers, the row matcher, the ASI additions ---

def test_his_sixteen_containers_and_every_range_he_gave():
    """He gave 16 container ranges and 5 segment ranges by hand. All 21 exact,
    including CON-043 at P1683 which needs the CON-042 offset of 42 carried."""
    from sourceborn import asi_pyramid as P
    his = {"CON-017": (641, 680), "CON-020": (761, 800),
           "CON-033": (1281, 1320), "CON-035": (1361, 1400),
           "CON-043": (1683, 1722), "CON-044": (1723, 1762),
           "CON-045": (1763, 1802), "CON-052": (2043, 2082),
           "CON-054": (2123, 2162), "CON-057": (2243, 2284),
           "CON-058": (2285, 2324), "CON-060": (2365, 2404),
           "CON-061": (2405, 2444), "CON-062": (2445, 2484),
           "CON-063": (2485, 2524), "CON-064": (2525, 2564)}
    for cid, span in his.items():
        assert P.container_span(cid) == span, cid
    assert [c for c, _ in P.HIS_CONTAINERS] == sorted(his), "his 16, his order"
    # his per-segment container counts: 2 / 2 / 3 / 2 / 7
    from collections import Counter
    got = Counter(P.param(P.container_span(c)[0])["segment"]
                  for c, _ in P.HIS_CONTAINERS)
    assert dict(got) == {"SEG-03": 2, "SEG-05": 2, "SEG-06": 3,
                         "SEG-07": 2, "SEG-08": 7}, dict(got)


def test_the_row_level_matcher_resolves_what_he_would_not_invent():
    """His line: "I won't invent the P-row count." The payload is decoded here,
    so the count is real, per-container, and checkable row by row."""
    from sourceborn import asi_pyramid as P
    r = P.rows_for(HIS_SENTENCE)
    c = r["counts"]
    assert c["containers"] == 16, "all 16 of his regions fire"
    assert c["segments"] == 5
    assert c["rows"] > 80, "16 containers != 16 parameters"
    assert c["rows"] == c["source_grounded"] + c["inferred"] + c["held_open"]
    assert c["untouched"] == c["bank"] - c["rows"]
    # every row must resolve to a real name inside its own container's span
    for row in r["rows"]:
        lo, hi = P.container_span(row["container"])
        assert lo <= row["flat"] <= hi, row
        assert row["name"] == P.param(row["flat"])["name"]
        assert row["by"] in ("HIS ASSIGNMENT", "resolved here (correctable)")
    # the guard row against false causality must be present and source-grounded
    corr = [x for x in r["rows"]
            if "Correlation-vs-causation" in x["name"]]
    assert corr and corr[0]["tier"] == P.SOURCE_GROUNDED
    # Sadness must still be HELD, never source-grounded
    sad = [x for x in r["rows"] if x["name"] == "Sadness"]
    assert sad and sad[0]["tier"] == P.HELD


def test_the_named_actor_is_no_longer_invisible():
    from sourceborn import asi_pyramid as P
    assert P.actor_name(HIS_SENTENCE) == "Samrath"
    assert P.actor_name("but today is his birthday") == "", \
        "no name present, so none is invented"


def test_eleven_runtime_relations_and_the_last_one_is_association_only():
    from sourceborn import asi_pyramid as P
    rel = P.relations(HIS_SENTENCE)
    assert rel["count"] == 11, rel["count"]
    assert rel["not_parameters"] is True
    ids = [x["id"] for x in rel["relations"]]
    assert ids[0] == "R01" and ids[-1] == "R11"
    last = rel["relations"][-1]
    assert last["note"] == P.ASSOCIATION_ONLY
    assert last["rel"] == "<->", "association is symmetric, not an arrow"
    rep = [x for x in rel["relations"] if "repeated historical" in x["to"]]
    assert rep and "not an enumeration" in rep[0]["note"]


def test_seven_interpretations_and_h7_prevents_false_causality():
    from sourceborn import asi_pyramid as P
    i = P.interpretations(HIS_SENTENCE)
    assert i["count"] == 7
    assert i["none_concluded"] is True
    h = {x["id"]: x for x in i["candidates"]}
    assert h["H1"]["status"] == "REVIEW"
    assert h["H2"]["status"] == "SYNTHETIC CANDIDATE"
    assert "unrelated" in h["H7"]["title"]
    assert "PREVENTS FALSE CAUSALITY" in h["H7"]["detail"]
    assert "always kept" in h["H7"]["status"]
    # the frames are general — the context word is substituted, not hard-coded
    other = P.interpretations("Ravi never wants to go to the gym, he always "
                             "shouted, but today is his match, he went really "
                             "excited.")
    assert "match" in {x["id"]: x for x in other["candidates"]}["H7"]["title"]


def test_three_pattern_candidates_from_his_run():
    from sourceborn import asi_pyramid as P
    pcs = P.pattern_candidates(HIS_SENTENCE)
    assert pcs["count"] == 3
    got = {x["id"]: x for x in pcs["candidates"]}
    assert got["PC-01"]["equals"].startswith("DIFFERENT AFFECT")
    assert "does not destroy" in got["PC-02"]["equals"]
    assert "DIFFERENT INTENT" in got["PC-03"]["equals"]


def test_learning_strengthens_the_prior_rule_and_never_duplicates_it():
    from sourceborn import asi_pyramid as P
    r = P.reinforce(HIS_SENTENCE)
    # two prior rules now apply here — RULE-001 (same event, different path)
    # and RULE-002 (role changes active interpretation), which he named as
    # already existing in the BJP message
    assert r["strengthened"] == 2, [x["id"] for x in r["rules"]]
    assert r["new_rules_invented"] == 0
    assert {x["id"] for x in r["rules"]} == {"RULE-001", "RULE-002"}
    rule = r["rules"][0]
    assert rule["applies_here"] is True
    assert rule["support"] == 1 and rule["support_after"] == 2
    assert rule["action"] == "SUPPORT +1"
    assert rule["duplicate_created"] is False
    assert rule["taught_by"] == "the mall example"
    # a sentence the rule does not cover must leave it untouched
    flat = P.reinforce("He went to school today.")
    assert flat["strengthened"] == 0
    assert flat["rules"][0]["action"] == "not touched"


def test_the_three_counters_and_nothing_is_promoted_without_him():
    from sourceborn import asi_pyramid as P
    r = P.full_run(HIS_SENTENCE)
    ex = dict(r["counters"]["existing"])
    assert ex["Total registered P rows"] == 3204
    assert ex["Candidate containers hit"] == 16
    assert ex["Existing parameters added"] == 0
    assert ex["Existing parameters modified"] == 0
    gen = dict(r["counters"]["generated"])
    assert gen["Parent Sequence"] == 1
    assert gen["Child comparison Sequences"] == 2
    assert gen["Runtime relations"] == 11
    assert gen["Interpretation candidates"] == 7
    assert gen["Pattern candidates"] == 3
    assert gen["Existing deep rule strengthened"] == 2
    assert all(v == 0 for _k, v in r["counters"]["promoted"]), \
        "nothing is promoted until he approves"


def test_a_third_party_absolute_is_a_source_generalization_not_his_value():
    """His correction: "never"/"always" here are SOURCE generalizations, and
    they do not assert every single historical visit."""
    from sourceborn import claims
    third = claims.read_claims("Samrath never like to go to school, "
                              "he always cry.")
    assert third and third[0]["status"] == claims.SOURCE_GENERALIZATION
    assert "never an enumeration" in third[0]["why"]
    mine = claims.read_claims("I never trust a number without a source.")
    assert mine and mine[0]["status"] == claims.USER_VALUE



# --- HIS MALL EXAMPLE: three scopes, six routes, and the stated motive -----

MALL = ("I dont want to go to mall, i'm not well. "
        "i dont want to go to mall, i'm not interested to walk. "
        "I dont like crowd. "
        "I had visited few days back. "
        "i will b going on weekend. "
        "i will be going with my Girlfriend.")


def test_the_mall_needs_a_third_time_scope():
    """Samrath needed PRIOR vs CURRENT. The mall needs FUTURE, and it needs
    TENSE to place a clause when none of his markers appear — "few days back"
    and "weekend" are in neither of his lists."""
    from sourceborn import asi_pyramid as P
    sc = P.read_scopes(MALL)
    assert sc["time_scopes"] == 3, sc["time_scopes"]
    assert not sc["unscoped"], "every clause must land somewhere"
    prior = [r["clause"] for r in sc[P.PRIOR]]
    fut = [r["clause"] for r in sc[P.FUTURE]]
    cur = [r["clause"] for r in sc[P.CURRENT]]
    assert any("few days back" in c for c in prior)
    assert len(fut) == 2 and all("will" in c for c in fut)
    assert any("dont like crowd" in c for c in cur)
    assert P.event_shell(MALL, sc)["shell"] == "GO_TO_MALL"


def test_a_companion_is_not_the_actor():
    """The first version returned "Girlfriend" as the actor of his own six
    sentences. First person wins, and a name after "with my" is a companion."""
    from sourceborn import asi_pyramid as P
    assert P.first_person(MALL) is True
    assert P.actor_name(MALL) == "", "no third-party actor here — it is him"
    assert P.companion(MALL) == "Girlfriend"
    # and the Samrath case must not regress
    assert P.actor_name("Samrath never like to go to school, he always cry.") \
        == "Samrath"
    assert P.companion("Samrath never like to go to school.") == ""


def test_six_intent_routes_on_one_event_shell():
    """His point: "Event is same going to mall / but the intent is keep
    changing." Six positions, one shell, six distinct KINDS of reason, and they
    are never averaged into one attitude to the mall."""
    from sourceborn import asi_pyramid as P
    ir = P.intent_routes(MALL)
    assert ir["shell"] == "GO_TO_MALL"
    assert ir["count"] == 6, ir["count"]
    assert len(ir["distinct_reason_kinds"]) == 6, ir["distinct_reason_kinds"]
    assert ir["blended"] is False and ir["collapsed"] is False
    assert len(ir["scopes_used"]) == 3
    kinds = [r["reason_kinds"][0] for r in ir["routes"]]
    assert kinds == ["BODY / PHYSICAL CONDITION", "EFFORT / INCLINATION",
                     "STANDING PREFERENCE", "RECENCY / ALREADY DONE",
                     "SCHEDULE / PLAN", "COMPANION / RELATIONSHIP"], kinds
    # the refusal negates the WANTING, not the going — his "left" law again
    assert "negates the WANTING" in ir["routes"][0]["stance"]
    # a route unit is (sentence, scope): Samrath is ONE sentence and still
    # yields TWO routes, because the scope changes inside it
    sam = P.intent_routes("Samrath never like to go to school, he always cry, "
                          "but today is his birthday, he went very happy.")
    assert sam["count"] == 2, sam["count"]
    assert P.intent_routes("He went to school today.")["count"] == 1


def test_the_reason_is_stated_here_and_never_upgraded_to_verified():
    """Samrath's source never says why. His mall source says why every time —
    so CON-064.01 Stated motive is SOURCE-GROUNDED while CON-064.02 Operating
    (actual) motive stays HELD. Saying a reason is not verifying it."""
    from sourceborn import asi_pyramid as P
    rs = P.stated_reasons(MALL)
    assert len(rs) == 6
    assert all(r["status"] == "STATED IN SOURCE" for r in rs)
    assert all(r["verified"] is False for r in rs)
    rows = {r["flat"]: r for r in P.rows_for(MALL)["rows"]}
    stated = P.flat_of("CON-064", 1)
    operating = P.flat_of("CON-064", 2)
    assert rows[stated]["tier"] == P.SOURCE_GROUNDED
    assert rows[stated]["name"] == "Stated motive"
    assert rows[operating]["tier"] == P.HELD
    assert rows[operating]["name"] == "Operating (actual) motive"
    # and on Samrath the motive is ABSENT, not merely unverified
    sam = P.signals("Samrath never like to go to school, he always cry, but "
                    "today is his birthday, he went very happy.")
    assert "motive_absent" in sam
    assert "stated_reason" not in P._mall_signals(
        "Samrath never like to go to school.", P.read_scopes(""),
        {"shell": None}, {})


def test_two_time_scopes_are_not_a_contradiction():
    from sourceborn import asi_pyramid as P
    cc = P.contradiction_check(MALL)
    assert cc["count"] >= 1
    assert cc["same_scope_count"] == 0, "there is no same-scope clash here"
    f = cc["findings"][0]
    assert f["looks_like"] == "CONTRADICTION"
    assert f["verdict"].startswith("NOT A CONTRADICTION")
    assert f["scope_a"] == P.CURRENT and f["scope_b"] == P.FUTURE


def test_the_body_fires_here_and_stayed_silent_on_samrath():
    """His ruling both ways: Human = the body. Samrath never reports a body and
    SEG-01 must not fire. "i'm not well" IS a body report, so it must."""
    from sourceborn import asi_pyramid as P
    mall = {r["segment"] for r in P.rows_for(MALL)["rows"]}
    assert "SEG-01" in mall, "\"i'm not well\" is a body statement"
    sam = {r["segment"] for r in P.rows_for(
        "Samrath never like to go to school, he always cry, but today is his "
        "birthday, he went very happy.")["rows"]}
    assert "SEG-01" not in sam, "no body is reported in the Samrath sentence"
    # and "not well" must not be upgraded into a named condition
    body = {r["name"]: r for r in P.rows_for(MALL)["rows"]
            if r["container"] == "CON-004"}
    assert body["Fatigue sensation"]["tier"] == P.HELD
    assert body["Body-signal interpretation"]["tier"] == P.SOURCE_GROUNDED
    # pain is never claimed — it is not stated anywhere in his six lines
    assert not [r for r in P.rows_for(MALL)["rows"]
                if r["container"] == "CON-006"], "pain is not stated"


def test_the_rule_recognises_its_own_founding_example_as_the_origin():
    """RULE-001 says taught_by "the mall example". The first version demanded a
    valence flip — a Samrath-shaped test — and scored 0 on the mall, the very
    example the rule is named after. Re-running the origin must also NOT inflate
    its own support."""
    from sourceborn import asi_pyramid as P
    mall = P.reinforce(MALL)["rules"][0]
    assert mall["shell"] == "GO_TO_MALL"
    assert mall["routes_seen"] == 6
    assert mall["is_origin"] is True
    assert mall["action"].startswith("ORIGIN")
    assert mall["support_after"] == mall["support"], "origin adds no support"
    sam = P.reinforce("Samrath never like to go to school, he always cry, but "
                      "today is his birthday, he went very happy.")
    assert sam["strengthened"] == 2, "RULE-001 and RULE-002 both apply"
    assert sam["rules"][0]["action"] == "SUPPORT +1"
    assert sam["rules"][0]["support_after"] == 2
    assert sam["new_rules_invented"] == 0
    flat = P.reinforce("He went to school today.")
    assert flat["strengthened"] == 0
    assert flat["rules"][0]["action"] == "not touched"


def test_the_samrath_numbers_do_not_move_when_the_mall_layer_is_added():
    """His 18, his 16 containers and the 106 rows are a fixed result. Anything
    added for the mall that changes them is a regression, not a feature."""
    from sourceborn import asi_pyramid as P
    a = P.activate(HIS_SENTENCE)["counts"]
    assert (a["strong"], a["candidate"], a["working"]) == (7, 11, 18)
    r = P.rows_for(HIS_SENTENCE)["counts"]
    assert r["rows"] == 106 and r["containers"] == 16 and r["segments"] == 5
    assert r["source_grounded"] == 59 and r["inferred"] == 27
    assert r["held_open"] == 20


def test_negations_are_not_reported_as_contextual_events():
    from sourceborn import asi_pyramid as P
    ctx = P.signals(MALL).get("context_event", {}).get("nouns", [])
    for junk in ("dont", "not", "im", "well", "going"):
        assert junk not in ctx, junk
    assert P.signals(HIS_SENTENCE)["context_event"]["nouns"] == ["birthday"]



# --- CONTEXTUAL PARAMETER WEIGHTING: his BJP example, alive not approved -----

BJP = ("BJP had one role available: prime-ministerial candidate for the 2014 "
       "Lok Sabha election. L.K. Advani was very senior, a party founder with "
       "a long history and experience. Narendra Modi was less senior than "
       "Advani, but Modi was the most popular leader with three consecutive "
       "Gujarat election victories and strong organisational backing including "
       "the RSS, and the cadre enthusiasm and campaign mobilisation were his. "
       "The objective was to win the 2014 election. "
       "Advani opposed the move and had resigned from party posts.")

OTHER_DOMAINS = {
 "SPORTS": ("The club had one captain's job to fill. Rahul Bose had played the "
            "most matches and was the longest serving player in the squad. "
            "Imran Shaikh had won the last three tournaments and the dressing "
            "room followed him. The season target was promotion."),
 "MEDICINE": ("One surgeon was needed for Friday's emergency list. Dr Menon "
              "had thirty years in the department and deep expertise. Dr Rao "
              "had done the most of these cases in the last year. The "
              "objective was to clear the backlog safely."),
 "BUSINESS": ("There was one seat on the board to fill. My uncle founded the "
              "firm and carries its institutional memory. My cousin brought "
              "in the last four clients. The board's aim for the year was new "
              "revenue."),
 "SCHOOL": ("The school had one head-boy position to fill. Aman Verma was the "
            "oldest student and had been there longest. Kabir Shah was the "
            "most popular boy and had won the last two debate victories. The "
            "objective was to win the inter-school championship."),
 "FAMILY": ("The family had to choose one trustee for the property. My "
            "grandfather started the house and knows how it was built. My "
            "brother had brought in the last four tenants. The aim was "
            "continuity and to be a custodian of the place."),
}


def test_each_candidate_keeps_only_its_own_attributed_axes():
    """One sentence naming both people made every candidate inherit every
    quality — Advani was credited with Modi's popularity. Attribution is by
    nearest mention, and "less senior than" gives LOW, not HIGH."""
    from sourceborn import weighting as W
    sel = W.read_selection(BJP)
    assert sel["candidate_count"] == 2, "L.K. Advani and Advani are one person"
    by = {c["who"]: {a["axis"]: a["direction"] for a in c["axes"]}
          for c in sel["candidates"]}
    adv = [k for k in by if "Advani" in k][0]
    modi = [k for k in by if "Modi" in k][0]
    assert by[adv]["SENIORITY / TENURE"] == "HIGH"
    assert "CURRENT POPULARITY / SUPPORT" not in by[adv], "no leakage"
    assert "RECENT RECORD" not in by[adv], "no leakage"
    assert by[modi]["CURRENT POPULARITY / SUPPORT"] == "HIGH"
    assert by[modi]["RECENT RECORD"] == "HIGH"
    assert by[modi].get("SENIORITY / TENURE") != "HIGH", \
        "\"less senior than Advani\" must never credit Modi with seniority"


def test_the_objective_sets_the_weights_and_a_different_objective_flips_them():
    """SAME PARAMETERS + DIFFERENT OBJECTIVE -> DIFFERENT IMPORTANCE ->
    DIFFERENT DECISION. His mechanism, and his own counterfactual."""
    from sourceborn import weighting as W
    w = W.weigh(BJP)
    assert w["objective_type"] == "COMPETITIVE WIN"
    assert w["weights"]["SENIORITY / TENURE"] == W.NOT_DECISIVE
    assert w["weights"]["CURRENT POPULARITY / SUPPORT"] == W.DOMINANT
    assert [x for x in w["favoured"] if "Modi" in x], w["favoured"]
    cf = W.counterfactual(BJP)
    assert cf["counterfactual_objective"] == "STEWARDSHIP / COUNSEL / CONTINUITY"
    assert cf["flip_count"] >= 5
    flips = {f["axis"]: f for f in cf["weight_flips"]}
    assert flips["SENIORITY / TENURE"][
        "under_STEWARDSHIP / COUNSEL / CONTINUITY"] == W.DOMINANT
    assert cf["selection_changes"] is True
    assert [x for x in cf["favoured_counterfactual"] if "Advani" in x]
    assert "not a claim about history" in cf["refuses"]


def test_rank_on_one_axis_is_not_fitness_for_the_role():
    from sourceborn import weighting as W
    rf = W.rank_is_not_fitness(BJP)
    assert any("Advani" in x for x in rf["highest_on_axis"])
    assert rf["answer"].startswith("YES")
    assert rf["therefore_most_suitable"] == "NOT AUTOMATIC"
    assert rf["asks_instead"] == ["Popular for what?", "Experienced for what?",
                                 "Senior for what?",
                                 "Selected for what objective?"]


def test_the_two_lessons_he_refused_cannot_be_learnt():
    from sourceborn import weighting as W
    claims = {r["claim"] for r in W.REFUSED_LESSONS}
    assert "young leader > senior leader" in claims
    assert "popularity > experience" in claims
    assert W.MAY_LEARN == "PARAMETER IMPORTANCE IS ITSELF CONTEXT-DEPENDENT."
    for r in W.REFUSED_LESSONS:
        assert r["his_verdict"], r


def test_the_candidate_is_alive_and_not_approved_and_cannot_self_promote():
    from sourceborn import weighting as W
    c = W.candidate(BJP)
    assert c["id"] == "PC-WEIGHT-001"
    assert c["status"] == "ALIVE — NOT APPROVED"
    assert c["support"] == 1 and c["canonical"] == 0
    assert c["gate"]["cross_domain_required"] is True
    assert set(c["gate"]["domains_he_named"]) == {
        "business", "family", "sports", "medicine", "school"}
    assert c["gate"]["who_approves"].startswith("him")
    assert W.stats()["canonical"] == 0


def test_it_fires_outside_politics_in_every_domain_he_named():
    """His gate: the next example must come from a completely different domain
    and the structure must fire again without being forced. Five cases, five
    domains, and the selection must flip under the counterfactual objective in
    every one — otherwise the mechanism is only re-describing the outcome."""
    from sourceborn import weighting as W
    p = W.cross_domain_probe(OTHER_DOMAINS)
    assert p["fired"] == 5, [c for c in p["cases"] if not c["fires"]]
    assert p["flipped_under_counterfactual"] == 5
    assert set(p["domains_fired"]) == set(OTHER_DOMAINS)
    assert p["still_not_approved"] is True
    by = {c["case"]: c for c in p["cases"]}
    # the objective is read from the case, not assumed — two of these are
    # STEWARDSHIP objectives and there the SENIOR person must win, which is
    # the proof the mechanism is not "young beats old"
    assert by["FAMILY"]["objective_type"] == \
        "STEWARDSHIP / COUNSEL / CONTINUITY"
    assert by["FAMILY"]["favoured"] == ["My grandfather"]
    assert by["BUSINESS"]["favoured"] == ["My uncle"]
    assert by["MEDICINE"]["objective_type"] == "THROUGHPUT / EXECUTION / SAFETY"
    assert by["SPORTS"]["objective_type"] == "COMPETITIVE WIN"
    assert by["SPORTS"]["favoured"] == ["Imran Shaikh"]


def test_no_objective_means_no_weighting_is_legal():
    from sourceborn import weighting as W
    flat = ("There was one seat to fill. Aman Verma was the oldest. "
            "Kabir Shah was the most popular.")
    w = W.weigh(flat)
    assert w["weights"] == {}
    assert w["verdict"].startswith("NO WEIGHTING")
    assert "cannot be read without an objective" in w["refuses"]
    assert W.read_selection(flat)["applies"] is False
    assert "no objective is named" in W.read_selection(flat)["why_not"]


def test_his_registry_already_names_the_mechanism():
    from sourceborn import asi_pyramid as P, weighting as W
    assert P.param(P.flat_of("CON-047", 4))["name"] == "Attribute weighting"
    rows = {r["name"]: r for r in W.rows_for(BJP)["rows"]}
    assert rows["Attribute weighting"]["tier"] == P.SOURCE_GROUNDED
    assert rows["Value ranking"]["tier"] == P.SOURCE_GROUNDED
    # the biases seniority and popularity can set are NAMED, never asserted
    assert rows["Authority bias"]["tier"] == P.HELD
    assert rows["Halo effect"]["tier"] == P.HELD
    assert W.rows_for(BJP)["counts"]["containers"] >= 7



# --- THE GENERATION: same person, changed conditions, different brain -------

def test_the_identity_is_locked_and_a_pack_is_not_a_person():
    from sourceborn import statepacks as S
    lk = S.identity_lock("The King")
    assert lk["identity"] == "The King" and lk["locked"] is True
    assert "does not change" in lk["rule"]
    assert "personality type" in lk["not"]
    # every pack is a state OF one identity, carrying a neutral MODEL label
    models = [p["model"] for p in S.STATE_PACKS]
    assert len(models) == len(set(models)), "each model letter is distinct"
    assert all(len(m) == 1 for m in models)


def test_container_times_state_generates_a_runtime_address_not_a_parameter():
    """His law: INSTANTIATED ADDRESS != NATIVE PARAMETER."""
    from sourceborn import statepacks as S
    a = S.runtime_address(6, S.DOMINANT)
    assert a["address"] == "CON-006@DOMINANT"
    assert a["container_name"] == "Pain and Protective Signalling"
    assert a["is_native_parameter"] is False and a["in_bank"] is False
    assert a["law"] == S.RUNTIME_LAW
    assert a["native_span"] == [201, 240], "it says which native rows it hangs off"
    # crossed with one of his 25 rubrics it is still an address
    b = S.runtime_address(6, S.DOMINANT, "Falsifier")
    assert b["address"] == "CON-006@DOMINANT/Falsifier"
    assert b["in_bank"] is False


def test_the_bank_never_grows_however_much_is_generated():
    """The one test whose only job is to prove the generation adds nothing."""
    from sourceborn import statepacks as S, human_registry as hr
    before = len(hr.parameters())
    for p in S.STATE_PACKS:
        r = S.generate("The King", p["id"], rubrics=S.RUBRICS_25)
        assert r["counts"]["native_parameters_added"] == 0
        assert r["counts"]["native_parameters_modified"] == 0
        assert r["counts"]["rubric_addresses"] == \
            r["counts"]["containers"] * len(S.RUBRICS_25)
    assert len(hr.parameters()) == before == 3204


def test_his_twenty_five_rubrics_are_the_same_for_every_container():
    """His discovery: 80 x 25 = 2,000 INSTANTIATED ADDRESSES, and the 2,000 is
    NOT added to the 3,204."""
    from sourceborn import statepacks as S
    assert len(S.RUBRICS_25) == 25
    assert S.RUBRICS_25[0] == "Presence"
    assert S.RUBRICS_25[-1] == "Confidence"
    assert "Falsifier" in S.RUBRICS_25 and "Contradiction Risk" in S.RUBRICS_25
    cap = S.capacity()
    assert cap["container_x_rubric"] == 80 * 25 == 2000
    assert cap["native_bank"] == 3204, "the 2,000 was not added"
    assert cap["at_current_fill"] == 3204 * 40 * 12
    assert "NOT added to the 3,204" in cap["law"]


def test_same_signal_two_brains_and_the_machine_does_not_choose():
    from sourceborn import statepacks as S
    r = S.same_signal_different_history("I need to speak with you privately.")
    reads = {x["pack"]: x["reads_as"] for x in r["readings"]}
    assert "strategic" in reads["SP-22"]
    assert "important/private" in reads["SP-23"]
    assert r["same_identity"] is True
    assert r["chosen"] is None, "the history that decides is not in the signal"
    assert "CHANGED HISTORY" in r["law"]


def test_the_pairs_that_are_the_same_man():
    from sourceborn import statepacks as S
    a, b = S.pack("SP-19"), S.pack("SP-20")
    assert b["pairs_with"] == "SP-19"
    assert "SAME MAN" in b["pair_note"]
    assert S.pack("SP-23")["pairs_with"] == "SP-22"
    # and a state that itself forks
    assert len(S.pack("SP-26")["forks"]) == 5
    assert "even one brain-state must fork" in S.pack("SP-26")["law"]


def test_the_body_pack_reaches_below_reasoning():
    """His SP-24: decision difference may originate below 'reasoning'."""
    from sourceborn import statepacks as S
    g = S.generate("The King", "SP-24")
    segs = {a["segment"] for a in g["addresses"]}
    assert "SEG-01" in segs, "sleep, energy, pain, autonomic are body containers"
    assert "SEG-04" in segs, "and they change working memory and inhibition"
    names = {a["container_name"] for a in g["addresses"]}
    assert "Working Memory" in names
    assert "Pain and Protective Signalling" in names
    assert "HYPOTHESES TO TEST" in g["pack"]["holds"]


def test_ten_event_forks_and_none_is_chosen():
    from sourceborn import statepacks as S
    # ten from his King sequences + ADVISOR_PRIVATE_MEETING from the
    # ASI0001_tablet_run workbook. Nothing was removed to make room for it.
    assert len(S.EVENT_FORKS) == 11
    tot = 0
    for name in S.EVENT_FORKS:
        f = S.fork_event(name)
        assert f["known"] is True and f["count"] >= 3
        assert f["chosen"] is None
        assert f["refuses"]
        assert f["law"] == "VISIBLE ACTION != HIDDEN INTENT"
        tot += f["count"]
    assert tot == 50, tot
    adv = S.fork_event("ADVISOR_PRIVATE_MEETING")
    assert adv["count"] == 10, "one route per brain-state of the same king"
    assert "SAME EVENT != SAME INTENT" in adv["refuses"]
    tax = S.fork_event("RAISE_TAX")
    assert "GREED automatically" in tax["refuses"]
    assert "where does the money actually go?" in tax["still_open"]
    cen = S.fork_event("CENSUS")
    assert "WHAT WAS COUNTED?" in cen["asks"]
    mon = S.fork_event("DESTROY_MONUMENT")
    assert "INTENTIONALLY DESTROYED" in mon["refuses"]
    # a shape he has not named is reported unnamed, not forked on a guess
    unk = S.fork_event("BUILD_A_SHIP")
    assert unk["known"] is False and unk["count"] == 0
    assert "unnamed" in unk["note"]


def test_formal_state_is_not_functional_state():
    from sourceborn import statepacks as S
    fv = S.formal_vs_functional()
    assert fv["law"] == "FORMAL STATE != FUNCTIONAL STATE"
    assert fv["functional_state"].startswith("UNKNOWN")
    assert "army loyalty" in fv["may_retain"]
    assert any("CEO" in x for x in fv["cross_domain_to_watch"])
    assert "repeatedly in other domains" in fv["his_gate"]


def test_all_seven_of_his_workbook_findings_are_kept_with_verification():
    from sourceborn import statepacks as S
    assert len(S.WORKBOOK_FINDINGS) == 7
    for f in S.WORKBOOK_FINDINGS:
        assert f["verified"], f
    text = " ".join(f["verified"] for f in S.WORKBOOK_FINDINGS)
    assert "P1999" in text and "$B$2:$B$2001" in text
    assert "ABS(L4)" in text
    assert "1 distinct edge-set" in text
    assert "manual" in text


def test_every_candidate_is_review_required_and_nothing_is_canonical():
    from sourceborn import statepacks as S
    assert len(S.CANDIDATES) == 7
    for c in S.CANDIDATES:
        assert c["status"] == S.REVIEW_REQUIRED, c["id"]
        assert c["canonical"] == 0, c["id"]
        assert c["form"] and c["found_in"]
    ids = {c["id"] for c in S.CANDIDATES}
    assert "RC-DOMAIN-RUBRIC-INSTANTIATION-001" in ids
    assert "RC-NO-EVIDENCE-NO-RANK-001" in ids
    assert "RC-FORMAL-VS-FUNCTIONAL-001" in ids
    r = S.run("The King", "SP-01", "ABDICATE")
    assert all(v == 0 for v in r["promoted"].values())
    assert S.stats()["canonical"] == 0


def test_the_twelve_prose_only_kings_are_not_counted_as_brains():
    from sourceborn import statepacks as S
    assert len(S.PROSE_ONLY) == 12
    assert "Shadow / Hidden King" in S.PROSE_ONLY
    packs = {p["name"] for p in S.STATE_PACKS}
    for name in S.PROSE_ONLY:
        assert name not in packs, name


def test_the_generation_and_weighting_routes_are_reachable():
    """weighting was importable and reachable from nothing. Both are wired."""
    from sourceborn import server
    src = open("src/sourceborn/server.py").read()
    for route in ('"/generation"', '"/generation/packs"', '"/generation/run"',
                  '"/weighting"', '"/weighting/run"'):
        assert route in src, route
    assert "statepacks" in src and "weighting" in src
    eng = open("src/sourceborn/engine.py").read()
    assert "asi_pyramid" in eng, "the Pyramid must be in the answer path"
    assert "statepacks" in eng



# --- LIVE INTENT GENERATION: the bottleneck he named -----------------------

def test_intent_is_generated_from_his_own_rows_not_a_table():
    from sourceborn import intents as I
    assert len(I.motive_rows()) == 40, "CON-064 is the WHY"
    assert len(I.form_rows()) == 40, "CON-063 is the SHAPE"
    m = {x["name"]: x for x in I.motive_rows()}
    assert m["Stated motive"]["p"] == "P2525"
    assert m["Motive-inference confidence"]["p"] == "P2564"
    f = {x["name"]: x for x in I.form_rows()}
    assert f["Immediate-intention formation"]["p"] == "P2485"


def test_more_parameters_active_means_more_intent():
    """His concept, and it must be computed, not asserted:
    'as much parameters we plug, we will generate more pattern and intent'."""
    from sourceborn import intents as I
    sc = I.scaling()
    assert sc["monotonic"] is True
    first, last = sc["curve"][0], sc["curve"][-1]
    assert first["active_containers"] == 1 and last["active_containers"] == 80
    assert last["intents_generated"] > first["intents_generated"] * 5, \
        (first, last)
    assert last["motives_raised"] > first["motives_raised"]
    assert sc["ceiling"]["max_pairs"] == 40 * 40


def test_the_motive_links_are_computed_and_the_fabrications_are_gated():
    """Naive head-word matching gave 200 edges and about a third were lexical
    coincidences — 'Face-saving motive' -> 'Face detection'. Perception, motor,
    attention-mechanics and language cannot originate a motive."""
    from sourceborn import intents as I
    assert set(I.BLOCKED_HOSTS) == {"SEG-02", "SEG-03", "SEG-04", "SEG-07"}
    ml = I.motive_links()
    for name, v in ml.items():
        for e in v["edges"]:
            assert e["segment"] not in I.BLOCKED_HOSTS, (name, e)
            assert e["matched"] and e["matched_p"], e
    st = I.stats()
    assert st["link_edges"] == 133, st["link_edges"]
    assert st["motives_linked"] == 35
    # the specific fabrications must be gone
    faces = [e["matched"] for e in ml["Face-saving motive"]["edges"]]
    assert "Face detection" not in faces
    rec = [e["matched"] for e in ml["Recognition/status need"]["edges"]]
    assert "Shape recognition" not in rec


def test_motives_with_no_echo_in_the_bank_are_reported_as_absences():
    from sourceborn import intents as I
    u = {x["motive"]: x for x in I.unlinked()}
    assert len(u) == 5
    assert u["Stated motive"]["absence"] is False, "machinery, not a motive"
    assert u["Operating (actual) motive"]["absence"] is False
    for real in ("Security need", "Mating/attraction motive",
                 "Revenge/retaliation motive"):
        assert u[real]["absence"] is True, real
    assert I.stats()["real_absences"] == 3


def test_a_different_brain_state_generates_different_intent():
    """The join his bottleneck needed: the state pack decides which containers
    are active, and the intent is generated from those."""
    from sourceborn import intents as I
    a = I.from_state_pack("The King", "SP-27", "ABDICATE")
    b = I.from_state_pack("The King", "SP-24")
    assert a["counts"]["motives_raised"] > b["counts"]["motives_raised"], \
        "divided loyalty raises social motives; exhaustion raises body ones"
    assert a["counts"]["intents_generated"] != b["counts"]["intents_generated"]
    segs_b = {c["raised_by"]["segment"] for c in b["candidates"]}
    assert segs_b == {"SEG-01"}, "the exhausted pack raises only body motives"
    assert a["identity"]["locked"] is True
    assert b["identity"]["locked"] is True


def test_generated_intent_never_concludes_and_never_enters_the_bank():
    from sourceborn import intents as I, human_registry as hr
    before = len(hr.parameters())
    g = I.generate("ABDICATE", ["CON-071", "CON-072", "CON-063"])
    assert g["chosen"] is None
    assert g["confidence"]["level"] == "LOW"
    assert g["counts"]["native_parameters_added"] == 0
    for c in g["candidates"]:
        assert c["status"] == "INTENT CANDIDATE"
        assert c["in_bank"] is False and c["is_native_parameter"] is False
        assert c["concluded"] is False
        assert c["why_p"].startswith("P") and c["shape_p"].startswith("P")
        assert c["raised_by"]["matched_row"], "every intent cites its evidence"
    assert len(hr.parameters()) == before == 3204


def test_the_scope_chooses_the_intent_form_not_a_guess():
    from sourceborn import intents as I
    cur = I.generate("GO", ["CON-071"], scope=I.CURRENT)
    fut = I.generate("GO", ["CON-071"], scope=I.FUTURE)
    cs = {c["shape"] for c in cur["candidates"]}
    fs = {c["shape"] for c in fut["candidates"]}
    assert "Immediate-intention formation" in cs
    assert "Future-intention formation" in fs
    assert "Future-intention formation" not in cs
    cond = I.generate("GO", ["CON-071"], scope=I.CURRENT, conditional=True)
    assert any("Contingent intention" in c["shape"] for c in cond["candidates"])


def test_live_intent_reaches_the_generation_run_and_its_routes():
    from sourceborn import statepacks as S
    r = S.run("The King", "SP-27", "ABDICATE")
    assert "live_intent" in r
    li = r["live_intent"]
    assert li["counts"]["intents_generated"] > 0
    assert "MORE PARAMETERS ACTIVE" in li["law"]
    src = open("src/sourceborn/server.py").read()
    assert '"/intents"' in src and '"/intents/run"' in src
    assert "intents" in src



# --- THE GROWTH LEDGER: the 3,204 is a floor -------------------------------

def _growth_root(tmp="growth_test"):
    import tempfile, os
    d = os.path.join(tempfile.mkdtemp(prefix="sb_growth_"), tmp)
    os.makedirs(d, exist_ok=True)
    return d


def test_the_module_has_no_removal_path_at_all():
    """His instruction: 'keep adding not removing at all'. Enforced by the
    shape of the code, not by discipline — so it is checked by reading the
    source, and a future edit that adds a delete fails this test."""
    import re
    src = open("src/sourceborn/growth.py").read()
    body = src[src.index("def _dir("):]      # skip the docstring
    for banned in ("def delete", "def remove", "def drop", "def clear",
                   "def prune", "def truncate", "os.remove", "os.unlink",
                   ".pop(", "shutil.rmtree"):
        assert banned not in body, banned
    # and the store must only ever be opened for append or read
    modes = re.findall(r'open\([^)]*?,\s*"([arw+bx]+)"', body)
    assert set(modes) <= {"a", "r"}, modes


def test_growth_appends_and_the_base_is_never_renumbered():
    from sourceborn import growth as G, human_registry as hr
    root = _growth_root()
    assert G.BASE == 3204
    assert G.FIRST_GROWN_P == 3205
    r1 = G.add(root, G.PARAM, "Test motive one", "a unit test", module="tests")
    r2 = G.add(root, G.PARAM, "Test motive two", "a unit test", module="tests")
    assert r1["id"] == "SB-HFR-P3205", r1["id"]
    assert r2["id"] == "SB-HFR-P3206", r2["id"]
    assert r1["in_base"] is False
    c = G.counts(root)
    assert c["base"] == 3204
    assert c["grown_parameters"] == 2
    assert c["total_parameters"] == 3206
    assert c["removals_possible"] == 0
    # his source document is untouched — that is a different statement from
    # "the bank never grows", which is what I had wrongly written
    assert len(hr.parameters()) == 3204


def test_only_parameters_consume_his_flat_index():
    """DOMAIN CONTAINER != RUBRIC. Rubrics, states, addresses and the rest grow
    their own series and do not inflate the parameter count."""
    from sourceborn import growth as G
    root = _growth_root()
    G.add(root, G.RUBRIC, "Presence", "his 25", module="tests")
    G.add(root, G.STATE, "Conflicted", "his profiles", module="tests")
    G.add(root, G.ADDRESS, "CON-006@DOMINANT", "a brain-state", module="tests")
    c = G.counts(root)
    assert c["grown_rows"] == 3
    assert c["grown_parameters"] == 0
    assert c["total_parameters"] == 3204, "addresses are not parameters"
    ids = [r["id"] for r in G.load(root)]
    assert ids == ["SB-RUBRIC-001", "SB-STATE-001", "SB-ADDR-0001"], ids


def test_superseding_keeps_the_old_row_whole():
    from sourceborn import growth as G
    root = _growth_root()
    old = G.add(root, G.RULE, "RULE-X", "first reading", module="tests",
                detail="the first way he put it")
    new = G.add(root, G.RULE, "RULE-X revised", "his correction",
                module="tests", supersedes=old["id"],
                detail="the later way he put it")
    rows = G.load(root)
    assert len(rows) == 2, "superseding appends; it does not replace"
    assert rows[0]["detail"] == "the first way he put it"
    assert new["supersedes"] == old["id"]
    assert G.counts(root)["grown_rows"] == 2


def test_the_seed_is_computed_from_the_modules_and_is_idempotent():
    from sourceborn import growth as G
    root = _growth_root()
    s1 = G.seed(root)
    assert s1["added"] > 150, s1["added"]
    by = s1["counts"]["by_kind"]
    assert by[G.ADDRESS] == 58, "every container x state pair generated"
    assert by[G.RUBRIC] == 25, "his 25 universal dimensions"
    assert by[G.INTENT_ROUTE] == 50, "40 King routes + his 10 advisor-meeting ones"
    assert by[G.EVENT] == 11
    assert by[G.RULE] == 18, "10 + his 7 live-intent rules + the namespace ruling"
    assert by[G.STATE] == 6
    assert by[G.PARAM] == 3, "the three motives with no echo in the bank"
    # the three that got a home
    params = [r["name"] for r in G.load(root) if r["kind"] == G.PARAM]
    assert set(params) == {"Security need", "Mating/attraction motive",
                           "Revenge/retaliation motive"}, params
    # seeding again adds nothing and removes nothing
    before = G.load(root)
    s2 = G.seed(root)
    assert s2["added"] == 0
    assert G.load(root) == before


def test_every_grown_row_carries_where_it_came_from():
    """Recording provenance is not a gate — he needs it to correct a row."""
    from sourceborn import growth as G
    root = _growth_root()
    G.seed(root)
    for r in G.load(root):
        assert r["surfaced_by"], r
        assert r["module"], r
        assert r["kind"] in G.SERIES, r
        assert r["base"] == 3204


def test_the_growth_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/growth"', '"/growth/add"', '"/growth/seed"'):
        assert route in src, route
    assert "growth" in src


# ---------------------------------------------------------------------------
# THE LIVE INTENT LEDGER AND THE KILL — his ASI0001_tablet_run_LIVE_INTENT_v2
# workbook. The falsifier column he filled is the survivor stage.
# ---------------------------------------------------------------------------

def test_his_ten_candidates_are_one_event_ten_states_none_chosen():
    from sourceborn import intent_ledger as L
    r = L.his_run()
    assert len(L.HIS_CANDIDATES) == 10
    assert r["one_event"] is True
    assert r["event"] == "Advisor requests a private meeting"
    assert r["chosen"] is None
    assert len({c["state"] for c in r["candidates"]}) == 10, "ten distinct states"
    assert len({c["event"] for c in r["candidates"]}) == 1, "one event"
    # HOLD is a valid resting state — his own gate says so
    assert all(c["user_decision"] == "HOLD" for c in r["candidates"])
    assert all(c["canonical"] is False for c in r["candidates"])
    assert all(c["in_bank"] is False for c in r["candidates"])


def test_every_candidate_names_what_would_flip_it():
    """The killing step needs a target. His sheet supplies one per row."""
    from sourceborn import intent_ledger as L
    r = L.his_run()
    assert r["all_falsifiable"] is True
    for c in r["candidates"]:
        assert c["falsifier"], c["id"]
        assert c["falsifiable"] is True


def test_a_candidate_with_no_falsifier_cannot_be_killed_and_says_so():
    from sourceborn import intent_ledger as L
    bare = dict(L.HIS_CANDIDATES[0])
    bare["falsifier"] = ""
    c = L.candidate(bare)
    assert c["falsifiable"] is False
    out = L.kill(c, falsifier_met=True, counterexamples=99)
    assert out["cannot_be_killed"] is True
    assert out["survives"] is True, "nothing can reach it"
    assert "defect in the candidate, not a strength" in out["why"]


def test_the_kill_eliminates_on_evidence_and_deletes_nothing():
    """generate -> evidence -> contradiction -> falsification -> survivor set."""
    from sourceborn import intent_ledger as L
    r = L.his_run(verdicts={
        "LI-002": {"falsifier_met": True,
                   "evidence": "the advisor arrives with a written challenge"},
        "LI-004": {"falsifier_met": False, "counterexamples": 0},
        "LI-006": {"counterexamples": 2, "evidence": "two reports of normal work"},
    })
    assert r["counts"]["generated"] == 10
    assert r["counts"]["killed"] == 2, r["counts"]
    assert r["counts"]["survived"] == 1, r["counts"]
    assert r["counts"]["untested"] == 7, "not tested is not survived"
    assert r["counts"]["deleted"] == 0
    assert r["survivor_set"] == ["LI-004"]
    assert set(r["killed_set"]) == {"LI-002", "LI-006"}
    dead = [c for c in r["candidates"] if c["status"] == L.KILLED]
    for d in dead:
        assert d["deleted"] is False and d["row_kept"] is True
        assert d["falsifier"], "a killed row keeps what would have flipped it"
        assert d["killed_by"]
    # killed two different ways, both his
    by = {d["id"]: d["why"] for d in dead}
    assert "falsifier met" in by["LI-002"]
    assert "counterexamples (2) reached support (1)" in by["LI-006"]


def test_new_wording_is_not_novelty():
    """His rule 4, and the reason the signature excludes the intent sentence."""
    from sourceborn import intent_ledger as L
    base = dict(L.HIS_CANDIDATES[3])
    reworded = dict(base, id="X-REWORDED",
                    intent="Treat the private meeting as a chance to check "
                           "whether the advisor can be relied on before handing "
                           "him more power.")
    n = L.novelty(reworded, [base])
    assert n["novel"] is False
    assert n["collides_with"] == base["id"]
    assert n["wording_differs"] is True
    assert "wording is not novelty" in n["why"]
    # change what it PREDICTS and it is new
    changed = dict(base, id="X-CHANGED",
                   state_change="remove the advisor from the channel entirely",
                   target="the court, not the advisor")
    assert L.novelty(changed, [base])["novel"] is True
    assert "intent" not in L.BEHAVIOUR_FIELDS, "novelty is never judged on wording"


def test_promotion_requires_recurrence_evidence_falsifier_and_his_word():
    from sourceborn import intent_ledger as L
    c = L.candidate(dict(L.HIS_CANDIDATES[0]))
    p = L.promote(c)
    assert p["promoted"] is False and p["canonical"] is False
    assert p["new_parameter_created"] is False
    joined = " | ".join(p["unmet"])
    assert "recurrence" in joined and "user approval" in joined
    assert "R-F-R" in joined and "evidence" in joined
    # one sequence is not recurrence
    assert L.promote(c, sequences_seen=1, evidence=True, rfr_passed=True,
                     user_approved=True)["promoted"] is False
    ok = L.promote(c, sequences_seen=2, evidence=True, rfr_passed=True,
                   user_approved=True)
    assert ok["promoted"] is True and ok["unmet"] == []
    assert ok["new_parameter_created"] is False, "new intent != new parameter"


def test_a_parameter_opens_only_on_repeated_semantic_loss():
    from sourceborn import intent_ledger as L
    # expressible in his existing rows -> no new parameter, however often it fails
    have = L.semantic_loss("reduce hidden-threat uncertainty before granting "
                           "influence", failures=5)
    assert have["expressible_in_existing_vocabulary"] is True
    assert have["opens_parameter_candidate"] is False
    assert have["matched_rows"]
    # nowhere in the bank, but only one failure -> his rule says REPEATEDLY
    once = L.semantic_loss("flarnak the zibbering wompus", failures=1)
    assert once["expressible_in_existing_vocabulary"] is False
    assert once["opens_parameter_candidate"] is False
    assert "REPEATEDLY" in once["why"] or "Not yet" in once["why"]
    twice = L.semantic_loss("flarnak the zibbering wompus", failures=2)
    assert twice["opens_parameter_candidate"] is True


def test_the_two_banks_are_never_merged():
    """His ruling: do not silently merge namespaces."""
    from sourceborn import intent_ledger as L
    ns = L.namespaces()
    assert ns["merged"] is False
    assert ns["workbook"]["count"] == 2000 and ns["workbook"]["unit"] == "ADDRESS"
    assert ns["registry"]["count"] == 3204 and ns["registry"]["unit"] == "PARAMETER"
    assert ns["workbook"]["count"] + ns["registry"]["count"] != 3204 + 0
    assert "must never be summed" in ns["collision"]
    # and the segment ids collide too — ordinal position is NOT a mapping
    m = L.map_in("S04")
    assert m["workbook_name"] == "Religion, Ritual & Cosmology"
    assert m["registry_same_ordinal_name"] == "Attention and Executive Control"
    assert m["same_subject"] is False and m["mapped"] is False
    assert m["merged"] is False
    assert "Ordinal position is not a mapping" in m["held_for_him"]


def test_his_ten_states_already_exist_in_the_core():
    """mostly wording meaning are are exist in the core — so match, don't retype."""
    from sourceborn import intent_ledger as L
    r = L.from_core()
    assert r["counts"]["his_candidates"] == 10
    assert r["counts"]["states_matched_to_packs"] == 10
    assert r["counts"]["states_missing_from_core"] == 0
    assert r["counts"]["native_parameters_added"] == 0
    packs = [row["pack"] for row in r["rows"]]
    assert packs == ["SP-%d" % n for n in range(19, 29)]
    # the generated count is a function of what is plugged in, per state
    counts = {row["pack"]: row["intents_generated"] for row in r["rows"]}
    assert counts["SP-24"] < counts["SP-27"], "exhausted raises fewer than divided"
    assert all(v > 0 for v in counts.values())


def test_the_workbook_findings_are_reported_not_corrected():
    from sourceborn import intent_ledger as L
    a = L.workbook_audit()
    assert a["sheets"] == 19
    assert a["counts"]["corrections_made_to_his_file"] == 0
    assert a["counts"]["findings"] == a["counts"]["verified"] == 13
    txt = " ".join(f["finding"] + f["consequence"] for f in L.WORKBOOK_FINDINGS)
    assert "K001 Lawgiver" in txt, "the dashboard's leading hypothesis at score 0"
    assert "P1999 and P2000" in txt, "the SUMIF range is off by two"
    assert "ABS(" in txt, "a contradicted score reads as strong"
    assert "16 / 18 / 19" in txt, "three counts of the same file"
    assert "F04" in txt and "F03" in txt, "his family ids against his own sheet"


def test_the_ledger_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/ledger"', '"/ledger/run"', '"/ledger/kill"'):
        assert route in src, route


# ---------------------------------------------------------------------------
# THE GROWING PHASE — "everything happening is a event, and all events have
# intent". An example is not judged for its output; it seats on the base.
# ---------------------------------------------------------------------------

RAIN = ("The kids father was standing outside with a water pipe and put it up in "
        "the air. The kids inside the home thought it was raining outside.")


def test_everything_happening_is_an_event():
    """His motto's first half. A text full of happenings can never return none."""
    from sourceborn import growing as W
    evs = W.events_in(RAIN)
    assert len(evs) >= 3, evs
    assert all(e["is_event"] for e in evs)
    # and the closed verb list alone would have MISSED his own sentence
    from sourceborn import micro
    assert "standing" not in micro.ALL_VERBS
    assert "pointed" not in micro.ALL_VERBS
    assert any("inflection" in e["how_found"] for e in evs), \
        "his rain sentence is exactly the case the verb list cannot serve"


def test_all_events_have_intent_and_the_slot_is_never_absent():
    """His motto's second half, and his rule that 'no reason' is not available."""
    from sourceborn import growing as W
    p = W.place(RAIN, "rain")
    assert p["counts"]["events"] == p["counts"]["intents_opened"]
    assert p["counts"]["intents_concluded"] == 0
    for e in p["events"]:
        assert e["intent"]["status"] == W.INTENT_OPEN
        assert e["intent"]["concluded"] is False
        # seated on his OWN bank, not asserted in prose
        assert e["intent"]["seats_on"] == list(W.INTENT_CONTAINERS)
    isl = W.intent_seat("he went because it was his birthday")
    assert isl["containers"] == ["CON-063", "CON-064"]
    assert isl["concluded"] is False


def test_the_auxiliary_is_not_the_happening():
    """`was standing` is a STANDING. The first attempt reported `was`."""
    from sourceborn import growing as W
    evs = W.events_in("The father was standing outside.")
    assert evs and evs[0]["happening"].lower() == "standing", evs
    # and a plural noun is not a verb — `kids` had been taken as the happening
    assert all(e["happening"].lower() != "kids" for e in W.events_in(RAIN))


def test_a_prepositional_phrase_is_not_the_actor():
    """`the kids inside the home thought` has actor kids, never home."""
    from sourceborn import growing as W
    evs = [e for e in W.events_in(RAIN) if e["happening"].lower() == "thought"]
    assert evs, "the inference event must be found"
    assert evs[0]["actor"].lower() == "kids", evs[0]
    assert evs[0]["role"] if "role" in evs[0] else True


def test_the_role_gates_the_seating_and_keeps_what_it_excludes():
    """Word matching alone seated his rain example on Air/breathing drive."""
    from sourceborn import growing as W
    r = W.role_of("thought", "the kids thought it was raining")
    assert r["role"] == W.INFERENCE, r
    s = W.seat("the kids inside the home thought it was raining",
               role=W.INFERENCE)
    assert s["role_segments"] == ["SEG-05", "SEG-06"]
    names = [x["name"] for x in s["seats"]]
    excluded = [x["name"] for x in s["out_of_role"]]
    assert "Thought suppression" not in names, "SEG-04 is outside the role"
    assert s["out_of_role_total"] >= 1
    assert excluded, "what the role excludes is kept and shown, never dropped"
    # a role with no row match still sits on the role's containers
    assert s["seats"] or s["container_seat"], "nothing is the one answer the " \
                                              "motto does not allow"
    # his own rule: a word in forty of his names is weak evidence. The bar is
    # derived from that number, not picked.
    assert abs(W.MIN_IDF - math.log(3204 / 40.0)) < 1e-9
    ungated = W.seat("control memory self")
    weak = {w["word"] for w in ungated["weak_words"]}
    assert {"control", "memory", "self"} <= weak, ungated["weak_words"]
    assert all(w["in_names"] >= 40 for w in ungated["weak_words"])


def test_every_example_increases_the_count_and_creates_no_parameter():
    """so system can strong its base / every example will keep increase the
    count — two mechanics, not one."""
    from sourceborn import growing as W
    root = _growth_root()
    a = W.grow(root, RAIN, "rain")
    assert a["increased"] == a["placement"]["counts"]["count_added"] > 0
    assert a["parameters_before"] == a["parameters_after"] == 3204, \
        "seating strengthens; it does not invent a parameter"
    b = W.grow(root, "Samrath went to school happily today.", "samrath")
    assert b["count_after"] > b["count_before"], "the count keeps rising"
    assert b["parameters_after"] == 3204
    from sourceborn import growth as G
    by = G.counts(root)["by_kind"]
    assert by[G.EXAMPLE] == 2 and by[G.EVENT] >= 3 and by[G.INTENT] >= 3
    assert G.counts(root)["removals_possible"] == 0
    # strengthening is support on an existing ID, never a duplicate row
    for s in a["placement"]["strengthened"]:
        assert s["sb_id"].startswith("SB-HFR-P")
        assert s["support"] >= 1


def test_an_example_is_placed_not_answered():
    """given example are not how it provide the out comes."""
    from sourceborn import growing as W
    p = W.place(RAIN, "rain")
    for banned in ("answer", "verdict", "score", "correct", "quality"):
        assert banned not in p, "placement carries no answer and no score"
    assert p["phase"] == "GROWING"
    assert p["motto"] == W.MOTTO
    assert p["counts"]["new_parameters_created"] == 0


def test_every_repo_file_is_divided_and_none_is_unplaced():
    from sourceborn import filemap as F
    d = F.divide(".")
    assert d["total_files"] > 400, d["total_files"]
    assert d["counts"][F.UNPLACED] == 0, d["unplaced"]
    assert sum(d["counts"].values()) == d["total_files"], "every file placed once"
    # his own words and his examples are what grow the count
    assert d["what_grows_the_count"]["which"] == [F.SOURCE, F.EXAMPLE]
    assert d["counts"][F.SOURCE] > 0 and d["counts"][F.EXAMPLE] > 0
    # his rulings are never run as examples against themselves
    method = d["classes"][F.METHOD]["files"]
    assert "CLAUDE.md" in method
    assert any("canon/" in m for m in method)
    assert all(not m.startswith("docs/method/canon/") for m in
               d["classes"][F.EXAMPLE]["files"]), "canon is METHOD, not EXAMPLE"
    # the bank is the bank, not a document about it
    assert any(b.endswith("human_registry.json") for b in
               d["classes"][F.BANK]["files"])
    assert F.PHASE == "GROWING"


def test_the_basic_being_over_is_his_call_not_a_threshold():
    from sourceborn import filemap as F, growing as W
    c = W.coverage(F.readable(".")[:12], ".")
    assert c["bank"] == 3204
    assert c["ids_reached"] + c["ids_untouched"] == 3204
    assert c["basic_over"] is False
    assert "his call" in c["why"]
    assert "new combinations" in c["then"]


def test_the_growing_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/growing"', '"/growing/coverage"', '"/growing/place"',
                  '"/growing/grow"'):
        assert route in src, route


# ---------------------------------------------------------------------------
# THE ALGORITHM THAT MAKES ITSELF — "now make algorithm which can make itself".
# The claim is that its own step list grows. These tests are the claim.
# ---------------------------------------------------------------------------

_SM_FILES = None


def _sm_files():
    """A small, fixed slice of his material — enough to produce arrangements
    without reading all 217 files in every test."""
    global _SM_FILES
    if _SM_FILES is None:
        from sourceborn import filemap as F
        _SM_FILES = tuple(F.readable(".")[:25])
    return _SM_FILES


def test_the_step_list_is_not_a_constant():
    from sourceborn import selfmake as S
    root = _growth_root()
    before = S.steps(root)
    assert before["counts"]["written"] == 0
    assert before["counts"]["total"] == len(S.SPINE)
    assert S.generation(root) == 0
    S.extend(root, _sm_files(), repo=".")
    after = S.steps(root)
    assert after["counts"]["written"] > 0, "it wrote nothing for itself"
    assert after["counts"]["total"] > before["counts"]["total"]
    assert S.generation(root) == after["counts"]["written"]
    # the spine is untouched — growth is additive
    assert after["spine"] == before["spine"] == list(S.SPINE)


def test_it_grows_once_and_re_running_is_a_no_op():
    """It must not inflate itself by being called again on the same material."""
    from sourceborn import selfmake as S
    root = _growth_root()
    a = S.extend(root, _sm_files(), repo=".")
    assert a["wrote"] > 0
    b = S.extend(root, _sm_files(), repo=".")
    assert b["wrote"] == 0, "same material must open no new step"
    assert b["generation_before"] == b["generation_after"] == a["generation_after"]
    assert b["removed"] == 0


def test_every_self_written_step_names_its_evidence_and_its_falsifier():
    from sourceborn import selfmake as S
    root = _growth_root()
    S.extend(root, _sm_files(), repo=".")
    written = S.written_steps(root)
    assert written
    for r in written:
        assert r["surfaced_by"], r
        assert r.get("falsifier"), "a step with no falsifier can never be killed"
        assert r.get("step_kind") in ("ARRANGEMENT", "COMBINATION"), r
        assert r.get("canonical") is False
        if r["step_kind"] == "ARRANGEMENT":
            assert r["support"] >= S.SUPPORT_BAR
        else:
            assert r["shared_support"] >= S.COMBINE_BAR


def test_a_combination_must_cross_role_and_no_example_produced_it():
    """his 'new combinations on new thoughts' — different KINDS of happening
    meeting, which is his own rain example's shape."""
    from sourceborn import selfmake as S
    root = _growth_root()
    p = S.propose(root, _sm_files(), repo=".")
    assert p["cross_role_required"] is True
    combos = p["new_combination_steps"]
    if combos:
        for c in combos:
            assert c["left"]["role"] != c["right"]["role"], c
            assert c["crosses_role"] is True
            assert c["produced_by_any_single_example"] is False
    # same-role pairs are rejected, and the number rejected is reported
    assert "combinations_rejected_same_role" in p["counts"]


def test_the_algorithm_applies_more_steps_after_it_extends_itself():
    from sourceborn import selfmake as S
    root = _growth_root()
    a = S.run(root, RAIN, "rain")
    assert a["generation"] == 0
    assert a["counts"]["fired"] == 0
    S.extend(root, _sm_files(), repo=".")
    b = S.run(root, RAIN, "rain")
    assert b["generation"] > a["generation"]
    assert b["steps_applied"]["total"] > a["steps_applied"]["total"], \
        "the same input must now pass through more algorithm"
    assert b["counts"]["parameters_created"] == 0
    assert b["chosen"] is None


def test_the_material_it_learnt_from_is_reported_with_its_bias():
    """The role reader defaults to ACTION. Said out loud, because every
    self-written step inherits it."""
    from sourceborn import selfmake as S
    br = S.bias_report(_sm_files(), repo=".")
    assert br["seats_by_role"]
    assert br["action_share"] > 0
    assert "fallback, not a finding" in br["why"]
    assert "superseding, never by deletion" in br["consequence"]
    assert br["his_call"]


def test_the_harvest_reports_unreadable_files_instead_of_skipping():
    """A silent skip once made the whole harvest return zero files."""
    from sourceborn import selfmake as S
    root = _growth_root()
    p = S.propose(root, ("no/such/file/anywhere.txt",), repo=".")
    assert p["material"]["unreadable"] == 1, p["material"]
    assert p["material"]["unreadable_paths"] == ["no/such/file/anywhere.txt"]


def test_the_selfmake_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/selfmake"', '"/selfmake/propose"', '"/selfmake/extend"',
                  '"/selfmake/run"'):
        assert route in src, route


# ---------------------------------------------------------------------------
# THE SUBJECT BRAINS — "ur own old docs / hope adding more".
# ---------------------------------------------------------------------------

def test_the_two_subject_brains_carry_25_candidates_and_14_open_halts():
    from sourceborn import subjectbrains as S
    st = S.stats()
    assert st["candidates"] == 25
    assert st["riemann_candidates"] == 11
    assert st["einstein_candidates"] == 10
    assert st["cross_subject_candidates"] == 4
    assert st["halts_open"] == 14
    assert st["halts_answered"] == 0, "not one of them was ever answered"
    assert st["parameters_created"] == 0
    for h in S.open_halts():
        assert h["answered"] is False
        assert h["yours"], "a halt names the decision that is his"


def test_the_two_banks_in_his_workbooks_are_not_merged_either():
    """2,560 then, 3,204 now — two versions, and he warned about the numbers."""
    from sourceborn import subjectbrains as S
    v = S.version_gap()
    assert v["workbooks_built_on"] == 2560
    assert v["registry_now"] == 3204
    assert v["merged"] is False
    assert v["names_differ"] is True
    assert "2561-2590" in v["his_own_warning_in_the_file"]
    # so nothing becomes a parameter
    assert all(c.get("id") for c in S.CANDIDATES)
    root = _growth_root()
    g = S.grow(root)
    assert g["parameters_created"] == 0
    from sourceborn import growth as G
    by = G.counts(root)["by_kind"]
    assert by[G.CANDIDATE] == 25 and by[G.HALT] == 14
    assert G.counts(root)["total_parameters"] == 3204, \
        "a candidate is not a parameter"
    # appending twice adds nothing
    assert S.grow(root)["added"] == 0


def test_the_anti_pleasing_tally_he_demanded():
    from sourceborn import subjectbrains as S
    r = S.rerun_tally()
    assert r["total"] == 45
    assert r["disagreement_mass"] == 17
    assert r["anti_pleasing_check"] is True
    assert "flattery" in r["his_test"]


def test_a_parameter_list_cannot_strengthen_the_bank_by_being_one():
    """His EINSTEIN workbook is 2,560 atom rows; placed whole it seated a
    taxonomy on a taxonomy."""
    from sourceborn import growing as W
    taxonomy = "\n".join(
        "C%02d-%03d | %d Homeostasis and Allostasis | Temperature balance | "
        "[REGISTRY-NAMED]" % (i % 80 + 1, i, i % 80 + 1) for i in range(1, 60))
    e = W.registry_echo(taxonomy)
    assert e["is_parameter_taxonomy"] is True
    assert e["atom_id_rows"] >= 50
    assert "cannot strengthen the bank by being a parameter list" in e["law"]
    # ordinary prose is NOT flagged
    plain = W.registry_echo(RAIN)
    assert plain["is_parameter_taxonomy"] is False
    # and place() reports what it excluded rather than hiding it
    p = W.place(taxonomy + "\nThe father was standing outside.", "mixed")
    assert p["echo_lines_excluded"] >= 50
    assert p["registry_echo"]["is_parameter_taxonomy"] is True


def test_rule_seven_no_longer_matches_on_substrings():
    """The gate declared all 25 candidates 'expressible' on noise: `productive`
    matched Reproductive-hormone signalling."""
    from sourceborn import intent_ledger as L
    s = L.semantic_loss("Combinatory-play engine: pre-verbal imagistic "
                        "recombination as the primary productive mechanism")
    names = [m["name"] for m in s["matched_rows"]]
    assert "Reproductive-hormone signalling" not in names, names
    assert "Sexual physiological response" not in names, names
    assert "how_matched" in s and "whole words only" in s["how_matched"]
    # a real one still lands
    r = L.semantic_loss("Presupposition-salience: attention captured by what a "
                        "field treats as given")
    assert any("Presupposition" in m["name"] for m in r["matched_rows"]), \
        r["matched_rows"]


def test_the_subject_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/subjects"', '"/subjects/grow"'):
        assert route in src, route


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
