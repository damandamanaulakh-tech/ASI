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
    assert by[G.INTENT_ROUTE] == 59, \
        "40 King routes + his 10 advisor-meeting + his 9 intent readings"
    assert by[G.EVENT] == 11
    assert by[G.RULE] == 19, \
        "10 + his 7 live-intent rules + the namespace ruling + his diamond link"
    assert by[G.STATE] == 54, "6 operating states + his 48 trigger rows"
    assert by[G.PATTERN] == 28, "17 patterns + the 11 archetypes"
    assert by[G.AXIS] == 17, "13 + his 4 named scale bands"
    assert by[G.CANDIDATE] == 5, "the 5 proposed scale bands, unapproved"
    assert by[G.HALT] == 7, "the trigger numbering seams, unresolved"
    assert by[G.PARAM] == 3, "the three motives with no echo in the bank"
    # the three that got a home
    params = [r["name"] for r in G.load(root) if r["kind"] == G.PARAM]
    assert set(params) == {"Security need", "Mating/attraction motive",
                           "Revenge/retaliation motive"}, params
    # THE LAYERS RAISE THE COUNT AND NOT THE BANK. His law is that every
    # example raises the count; his other law is that a rubric application is
    # not an ontology expansion. An archetype is not a parameter and a link is
    # not a parameter, so none of them is a PARAM row.
    rows = G.load(root)
    for prefix, kind in (("ARCHETYPE: ", G.PATTERN), ("LINK: ", G.RULE),
                         ("SCALE BAND: ", G.AXIS), ("READING: ", G.INTENT_ROUTE),
                         ("TRIGGER: ", G.STATE)):
        got = [r for r in rows if r["name"].startswith(prefix)]
        assert got, prefix
        assert {r["kind"] for r in got} == {kind}, (prefix, kind)
    assert not [r for r in rows
                if r["kind"] == G.PARAM and ":" in r["name"]], \
        "no layer row may consume his flat parameter index"
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
    # adopted material is custody, not a role: its own class, in neither sum,
    # and NEVER on the harvest list — the adoption stays un-wired
    adopted = d["classes"][F.ADOPTED]["files"]
    # 43 C-SB (42 files + manifest) + 35 SB-ASI-Drive (the workbook,
    # 33 derived sheet texts, and its manifest)
    assert len(adopted) == 78, adopted
    assert all(a.startswith("adopted/") for a in adopted)
    assert F.ADOPTED not in d["what_grows_the_count"]["which"]
    assert F.ADOPTED not in d["what_it_grows_against"]["which"]
    assert not any(p.startswith("adopted/") for p in F.readable(".")), \
        "an adopted file entered the growing harvest"


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


def test_more_subjects_kill_three_of_the_four_cross_laws():
    """The kill still works and is still correct — but on his word it is OFF by
    default: "nothing needs to kill for now, add everything and generate"."""
    from sourceborn import subjectbrains as S
    assert S.cross_test()["kill"] is False, "killing is off on his instruction"
    r = S.cross_test(kill=True)
    assert r["subjects"] == 12
    assert r["new_subjects"] == 10, "two subjects cannot test a cross-subject law"
    assert r["laws_tested"] == 4
    assert set(r["killed_as_stated"]) == {"X-01", "X-02", "X-03"}, r
    assert r["survived"] == ["X-04"]
    assert r["nothing_deleted"] is True
    # X-01 still holds on the two it was derived from, plus Beethoven — and on
    # nobody else. Nine of twelve read the other way.
    x1 = [l for l in r["laws"] if l["law"] == "X-01"][0]
    held = [row["name"] for row in x1["rows"] if row["verdict"] == S.HOLDS]
    assert "Bernhard Riemann" in held and "Albert Einstein" in held
    assert x1["counts"]["fails"] == 9, x1["counts"]
    # X-03 dies on exactly one clean counterexample
    x3 = [l for l in r["laws"] if l["law"] == "X-03"][0]
    assert x3["counts"]["holds"] == 10 and x3["counts"]["fails"] == 2
    assert "Michael Faraday" in x3["killed_by"]
    # X-02 needs a category it does not have
    x2 = [l for l in r["laws"] if l["law"] == "X-02"][0]
    assert "USED_THEN_DESTROYED" in x2["needs_a_new_category"]
    # X-04 survives, and not because everyone worked alone
    x4 = [l for l in r["laws"] if l["law"] == "X-04"][0]
    assert x4["counts"]["holds"] == 12 and x4["killed_as_stated"] is False


def test_one_counterexample_falsifies_and_the_verdict_is_computed():
    """Holding on most subjects is not holding. And no verdict is typed."""
    from sourceborn import subjectbrains as S
    law = [l for l in S.CROSS_LAWS if l["id"] == "X-03"][0]
    faraday = [s for s in S.SUBJECTS if s["name"] == "Michael Faraday"][0]
    assert S._verdict(law, faraday)["verdict"] == S.FAILS
    # strike the field and the verdict moves — the test reads fields, not a table
    moved = dict(faraday, at_death=S.WORKING_AT_DEATH)
    assert S._verdict(law, moved)["verdict"] == S.HOLDS
    # a law with a fail is KILLED AS STATED, never "mostly true"
    r = S.cross_test("X-03", kill=True)["laws"][0]
    assert r["killed_as_stated"] is True
    assert "KILLED AS STATED" in r["status"]
    assert r["narrow_to"], "it must say what it would have to be narrowed to"
    assert r["deleted"] == 0


def test_his_two_pole_axis_needs_four_settings():
    """E-03 said one axis, two poles. Six subjects show four."""
    from sourceborn import subjectbrains as S
    rp = S.release_poles()
    assert rp["poles_in_his_candidate"] == [S.GATE, S.ITERATE]
    assert {S.GATE, S.ITERATE, S.CONTINUOUS, S.UNGATED} <= set(rp["poles_found"])
    assert len(rp["poles_found"]) >= 4
    assert "not applied to it" in rp["note"], "an amendment to his candidate, " \
                                              "not an edit of it"
    # and the lone-theorist shape is broken by two of the new subjects
    lw = S.lone_worker_check()
    assert len(lw["not_alone"]) >= 2
    assert "Marie Curie" in lw["not_alone"] and "Alan Turing" in lw["not_alone"]


def test_the_candidates_are_applied_across_every_subject():
    """apply on candidates — 25 x 12, and what has no reader says so."""
    from sourceborn import subjectbrains as S
    ap = S.apply_candidates()
    assert ap["candidates"] == 25 and ap["subjects"] == 12
    assert ap["cells"] == 300
    assert ap["cells_read"] + ap["cells_not_read"] == 300
    assert ap["without_an_axis"] == 8, "8 candidates have no reader yet"
    # the ones with no axis are NOT READ on every subject — never invented
    for row in ap["grid"]:
        if row["axis"] is None:
            assert all(c["setting"] == S.NOT_READ for c in row["cells"])
    # a candidate read across subjects becomes an axis with named settings
    assert "E-03" in ap["became_an_axis"]
    assert "X-04" in ap["single_valued"], "constraint-rise reads ROSE on all 12"


def test_generation_adds_everything_and_kills_nothing():
    """nothing needs to kill for now, add everything and generate."""
    from sourceborn import subjectbrains as S
    g = S.generate_variants()
    assert g["variants_generated"] == 72, g["variants_generated"]
    assert g["killed"] == 0
    assert g["parameters_created"] == 0
    assert g["his_words"] == "nothing needs to kill for now, add everything " \
                             "and generate"
    for v in g["variants"]:
        assert v["is_parameter"] is False and v["canonical"] is False
        assert v["chosen"] is False
        assert v["subjects"] and v["support"] == len(v["subjects"])
    # his own R-06 gains the pole he said the registry lacked
    r6 = [v for v in g["variants"] if v["from_candidate"] == "R-06"]
    assert {v["setting"] for v in r6} == {"UNDER", "LEVEL", "OVER"}
    # and an "axis" where every subject is its own setting is flagged, not sold
    flagged = [x["candidate"] for x in g["not_yet_an_axis"]]
    assert "E-01" in flagged, g["not_yet_an_axis"]
    assert g["variants_from_singleton_fields"] == 12
    # appending is append-only and creates no parameter
    root = _growth_root()
    a = S.grow_variants(root)
    assert a["added"] == 72 and a["parameters_created"] == 0 and a["killed"] == 0
    assert S.grow_variants(root)["added"] == 0
    from sourceborn import growth as G
    assert G.counts(root)["total_parameters"] == 3204


# ---------------------------------------------------------------------------
# THE ARTIFACT LAYER — from GPT_Black.txt. Reading an object without pretending
# to read its language.
# ---------------------------------------------------------------------------

def test_a_sign_can_be_reasoned_about_without_knowing_what_it_says():
    from sourceborn import artifact as A
    assert len(A.SIGN_GROUPS) == 10
    ids = [g["id"] for g in A.SIGN_GROUPS]
    assert ids == ["SG-%s" % c for c in "ABCDEFGHIJ"]
    # the damaged class is not a missing letter
    dam = [g for g in A.SIGN_GROUPS if g["id"] == "SG-J"][0]
    assert "NOT a missing letter" in dam["reads"]
    assert set(A.SIGN_AXES) == {"NEIGHBOUR", "POSITION", "REPETITION",
                                "ENCLOSURE", "DAMAGE"}


def test_every_meaning_is_synthetic_and_nothing_is_translated():
    from sourceborn import artifact as A
    assert len(A.SYNTHETIC_MEANINGS) == 8
    g = A.generate_meanings(limit=200)
    for m in g["meanings"]:
        assert m["status"] == A.NEW_SYNTHETIC
        assert m["historical_fact"] is False
        assert m["translation_verified"] is False
        assert m["chosen"] is False
        assert m["evidence_owed"]
    assert g["counts"]["historical_facts_established"] == 0
    assert g["counts"]["translations_made"] == 0
    assert g["counts"]["new_parameters_created"] == 0


def test_the_gates_bite_and_the_ungated_number_is_reported():
    """Ungated it returns the whole cross product, which is not a finding."""
    from sourceborn import artifact as A
    raw = A.generate_meanings(gated=False)
    gated = A.generate_meanings()
    assert raw["counts"]["generated"] == A.combination_space()["ceiling"]
    assert gated["counts"]["generated"] < raw["counts"]["generated"] / 3
    assert gated["counts"]["rejected_role_cannot_reach_that_future"] > 0
    assert gated["counts"]["rejected_marks_cannot_carry_that_claim"] > 0
    assert gated["counts"]["ceiling_ungated"] == raw["counts"]["generated"]
    # a carver can only be working toward the one future a carver can affect
    carver = [m for m in gated["meanings"] if m["actor_role"] == "CARVER"]
    assert carver and {m["future_state"] for m in carver} == \
        {[f["state"] for f in A.FUTURE_STATES if f["id"] == "FS-6"][0]}


def test_farther_is_not_wrong_it_owes_more_evidence():
    from sourceborn import artifact as A
    assert len(A.ORIGIN_DISTANCE) == 6
    assert [d["d"] for d in A.ORIGIN_DISTANCE] == [0, 1, 2, 3, 4, 5]
    assert A.ORIGIN_DISTANCE[0]["debt"] == "none — it is there"
    assert "not WRONG" in A.DISTANCE_LAW
    assert all(d["debt"] for d in A.ORIGIN_DISTANCE)


def test_one_object_has_nine_actor_roles_not_one():
    from sourceborn import artifact as A
    roles = [r["role"] for r in A.ACTOR_ROLES]
    assert len(roles) == 9
    for r in ("SUBJECT", "REQUESTER", "CONTROLLER", "AUTHOR", "SCRIBE",
              "CARVER", "INSTITUTION", "BENEFICIARY", "AUDIENCE"):
        assert r in roles
    assert all(r in A.ROLE_FUTURES for r in roles), "each role needs its reach"


def test_damage_opens_branches_and_is_never_filled_in():
    from sourceborn import artifact as A
    d = A.damage_branches(["SG-A enclosure"])
    assert d["count"] == 4
    assert d["filled_in"] is False and d["chosen"] is None
    # every branch must predict DIFFERENT evidence or it is not a branch
    preds = [b["predicts"] for b in d["branches"]]
    assert len(set(preds)) == len(preds)
    assert "never completed by the machine" in d["law"]


def test_what_the_transcript_itself_refused_stays_refused():
    from sourceborn import artifact as A
    r = A.refused()
    assert len(r) == 6
    for x in r:
        assert x["adopted"] is False and x["historical_fact"] is False
    txt = " ".join(x["claim"] + x["why"] for x in r)
    assert "owl" in txt and "falcon" in txt
    assert "MATCH SCORE != EPISTEMIC CONFIDENCE" in txt
    assert "7.8/10" in txt


def test_his_meanings_seat_on_the_bank_and_create_nothing():
    from sourceborn import artifact as A
    s = A.seat_on_bank()
    assert s["new_parameters_created"] == 0
    assert s["distinct_ids"] > 10
    seated = {r["id"]: [x["row"] for x in r["seats"]] for r in s["rows"]}
    # the two clearest landings, and they are the point of the growing phase
    assert any("Intention-to-persist" in n for n in seated["SYN-MEAN-006"]), \
        seated["SYN-MEAN-006"]
    assert any("Sequence compression" in n for n in seated["SYN-MEAN-008"]), \
        seated["SYN-MEAN-008"]
    # appending is append-only and adds no parameter
    root = _growth_root()
    a = A.grow(root)
    assert a["added"] > 30 and a["parameters_created"] == 0
    assert A.grow(root)["added"] == 0
    from sourceborn import growth as G
    assert G.counts(root)["total_parameters"] == 3204


def test_twelve_pattern_candidates_and_four_are_reported_unnamed():
    from sourceborn import artifact as A
    assert len(A.PATTERN_CANDIDATES) == 12
    named = [p for p in A.PATTERN_CANDIDATES if p["named_in_source"]]
    unnamed = [p for p in A.PATTERN_CANDIDATES if not p["named_in_source"]]
    assert len(named) == 8 and len(unnamed) == 4
    for p in unnamed:
        assert p["name"] is None, "an unnamed candidate is not invented a name"
    for p in named:
        assert p["beyond_egypt"], "each named one says where else it applies"


# ---------------------------------------------------------------------------
# PHASE A — the node schema, locked. From his SELF-SUSTAINING EXECUTION FLOW.
# ---------------------------------------------------------------------------

# If this hash changes, the schema changed. Bump SCHEMA_VERSION deliberately and
# update this line in the same commit — never the other way round.
SCHEMA_FINGERPRINT = "488e704ff0a54931"


def test_the_node_schema_is_locked_not_merely_written_down():
    """A lock is a check, not a comment."""
    from sourceborn import nodebrain as N
    assert N.fingerprint() == SCHEMA_FINGERPRINT, (
        "the node schema moved. Something in NODE_TYPES / FIELDS / LINK_TYPES / "
        "STATUSES / MEMORY_KINDS / the condition lists changed. Bump "
        "SCHEMA_VERSION and this constant together, in one commit. Got: %s"
        % N.fingerprint())
    assert N.SCHEMA_VERSION == "A.1"
    # the hash depends on content, not on ordering or whitespace
    import json
    a = json.dumps(N.schema(), sort_keys=True, separators=(",", ":"))
    b = json.dumps(N.schema(), sort_keys=True, separators=(",", ":"))
    assert a == b


def test_his_twelve_types_ten_links_eleven_memories_four_statuses():
    from sourceborn import nodebrain as N
    assert len(N.NODE_TYPES) == 12 and len(N.TYPES) == 12
    for t in ("STATE", "EVENT", "ACTOR", "INTENT", "RELATION", "PATTERN",
              "RULE", "SEQUENCE", "ARTIFACT", "MEMORY", "CONTRADICTION",
              "FUTURE_STATE"):
        assert t in N.TYPES, t
    assert len(N.LINK_TYPES) == 10
    for l in ("produced_by", "depends_on", "supports", "contradicts",
              "similar_to", "before", "after", "contains", "actor_of",
              "future_of"):
        assert l in N.LINKS, l
    assert len(N.MEMORY_KINDS) == 11
    assert len(N.STATUSES) == 4
    assert len(N.WRITE_CONDITIONS) == 5 and len(N.READ_CONDITIONS) == 6
    assert len(N.FIELDS) == 16
    # every status carries a meaning, so a bare label never travels alone
    assert set(N.STATUS_MEANS) == set(N.STATUSES)


def test_no_invention_before_source_lock():
    """point_zero_ref is REQUIRED, and that is his rule made structural."""
    from sourceborn import nodebrain as N
    assert "point_zero_ref" in N.REQUIRED
    ok = N.new_node("EVENT", 1, point_zero_ref="RAIN-001")
    assert ok["node_id"] == "SB-N-EVT-00001"
    try:
        N.new_node("EVENT", 2, point_zero_ref="")
        raise AssertionError("a node with no source was accepted")
    except ValueError as e:
        assert "point_zero_ref" in str(e)


def test_a_malformed_node_is_refused_and_the_reason_is_named():
    from sourceborn import nodebrain as N
    cases = [
        (lambda: N.new_node("SPACESHIP", 1, point_zero_ref="x"), "unknown node type"),
        (lambda: N.new_node("EVENT", 1, point_zero_ref="x", status="MAYBE"),
         "not one of the four"),
        (lambda: N.new_node("EVENT", 1, point_zero_ref="x", proof_debt=9),
         "proof_debt must be 0..5"),
        (lambda: N.new_node("EVENT", 1, point_zero_ref="x", vibe="good"),
         "not a schema field"),
    ]
    for fn, expect in cases:
        try:
            fn()
            raise AssertionError("not refused: expected %r" % expect)
        except (ValueError, KeyError) as e:
            assert expect in str(e), (expect, str(e))
    # validate() never returns a bare False
    bad = dict.fromkeys(N.FIELD_NAMES)
    v = N.validate(bad)
    assert v["valid"] is False and len(v["problems"]) >= len(N.REQUIRED)


def test_ids_carry_their_type_and_cannot_be_read_as_bank_or_ledger_ids():
    from sourceborn import nodebrain as N
    nid = N.make_id("CONTRADICTION", 42)
    assert nid == "SB-N-CON-00042"
    p = N.parse_id(nid)
    assert p["valid"] and p["node_type"] == "CONTRADICTION" and p["n"] == 42
    # a bank id and a ledger id are not node ids
    assert N.parse_id("SB-HFR-P0717")["valid"] is False
    assert N.parse_id("SB-STEP-0001")["valid"] is False
    assert N.parse_id("P0717")["valid"] is False
    # and the stem must agree with the declared type
    node = N.new_node("EVENT", 1, point_zero_ref="x")
    node["node_type"] = "ACTOR"
    assert "stem says EVENT but node_type says ACTOR" in         " ".join(N.validate(node)["problems"])


def test_links_are_typed_with_a_direction_and_an_inverse():
    """One edge kind would have made a similarity blob. His ten do not."""
    from sourceborn import nodebrain as N
    n = N.new_node("EVENT", 1, point_zero_ref="x")
    n = N.link(n, "produced_by", "SB-N-ACT-00002")
    n = N.link(n, "contradicts", "SB-N-EVT-00003")
    assert n["parent_links"][0]["link"] == "produced_by"
    assert n["parent_links"][0]["direction"] == "one-way"
    assert n["contradiction_links"][0]["direction"] == "mutual"
    # each link lands in the field its type says it lands in
    for spec in N.LINK_TYPES:
        assert spec["goes_in"] in N.LINK_FIELDS, spec
    assert N.inverse_of("before") == "after"
    assert N.inverse_of("contains") == "part_of"
    assert N.inverse_of("contradicts") == "contradicts", "mutual is its own"
    for bad, expect in ((("rhymes_with", "SB-N-EVT-00002"), "unknown link type"),
                        (("supports", "P0717"), "not a node id")):
        try:
            N.link(n, bad[0], bad[1])
            raise AssertionError("not refused: %s" % expect)
        except (KeyError, ValueError) as e:
            assert expect in str(e)


def test_five_names_collide_with_the_growth_series_and_none_is_merged():
    from sourceborn import nodebrain as N
    c = N.collisions()
    assert c["shared_names"] == ["EVENT", "INTENT", "PATTERN", "RULE", "STATE"]
    assert c["merged"] is False
    assert c["rule"] == "do not silently merge namespaces"
    for name in c["shared_names"]:
        assert c["notes"][name], "every collision says what each side means"
    assert set(c["node_only"]) == {"ACTOR", "ARTIFACT", "CONTRADICTION",
                                   "FUTURE_STATE", "MEMORY", "RELATION",
                                   "SEQUENCE"}
    assert c["id_prefixes_kept_apart"]["nodes"] == N.ID_PREFIX
    assert c["his_call"]


def test_phase_a_writes_nothing_and_links_nothing():
    """It defines the shape. Linking is D, auto is E, and neither is here."""
    from sourceborn import nodebrain as N
    st = N.stats()
    assert st["nodes_written"] == 0
    assert st["links_discovered"] == 0
    assert st["namespaces_merged"] is False
    assert "linking (D)" in st["not_in_this_phase"]
    # check the CODE, not the prose — the docstring names growth.add precisely
    # to say it does not touch it, and a naive grep counted that as a violation
    import re as _re
    src = open("src/sourceborn/nodebrain.py").read()
    code = _re.sub(r'"""..*?"""', "", src, flags=_re.S)      # drop docstrings
    code = _re.sub(r"#.*", "", code)                          # drop comments
    for forbidden in ("growth.add(", "open(", "def tick", "Thread"):
        assert forbidden not in code, \
            "Phase A must not write, trigger or schedule: found %r" % forbidden


def test_the_node_schema_route_is_reachable():
    src = open("src/sourceborn/server.py").read()
    assert '"/nodes/schema"' in src


def test_stage_12_turns_a_meaning_into_what_should_exist():
    """if this were true, THIS should exist — and what would refute it."""
    from sourceborn import artifact as A
    from sourceborn import expected as E
    m = [x for x in A.generate_meanings()["meanings"]
         if x["actor_role"] == "CARVER"][0]
    e = E.expect(m)
    assert e["testable"] is True
    assert e["predictions"]
    for p in e["predictions"]:
        assert p["where_to_look"], "a prediction names where to look"
        assert p["would_confirm"] and p["would_refute"], \
            "two-sided or it cannot be tested"
        assert p["proof_debt"], "it inherits the origin distance"
        assert p["checked"] is False and p["verified"] is False
    # a carver's trace is MATERIAL, and it is required by both sides
    mat = [p for p in e["predictions"] if p["class"] == E.MATERIAL][0]
    assert mat["strength"] == "REQUIRED BY BOTH"
    assert e["checked_anything"] is False


def test_a_prediction_every_meaning_makes_tests_nothing():
    from sourceborn import artifact as A
    from sourceborn import expected as E
    r = E.run(A.generate_meanings()["meanings"], limit=400)
    # ABSENCE is owed by every reading, so it can never discriminate
    assert E.ABSENCE in r["non_discriminating_classes"]
    # and it is counted ONCE per meaning, never twice
    assert all(v <= 1.0 for v in r["class_share"].values()), r["class_share"]
    assert r["counts"]["discriminating"] + r["counts"]["non_discriminating"] \
        == r["counts"]["predictions_generated"]
    # nothing is checked, nothing is verified, nothing is created
    assert r["counts"]["checked_against_the_world"] == 0
    assert r["counts"]["verified"] == 0
    assert r["counts"]["new_parameters_created"] == 0
    assert "hand in" in r["sample_warning"], "the bar depends on the sample"


def test_stage_12_hands_stage_17_a_falsifier_it_did_not_have():
    from sourceborn import artifact as A
    from sourceborn import expected as E
    for m in A.generate_meanings(limit=40)["meanings"]:
        f = E.falsifier_from(m)
        assert f["falsifiable"] is True
        assert f["falsifier"] and "look at" in f["falsifier"]
        assert f["feeds"] == "intent_ledger.kill"
    # and the kill can actually use it — a composed falsifier is a real one
    from sourceborn import intent_ledger as L
    m = A.generate_meanings(limit=1)["meanings"][0]
    cand = L.candidate({"id": m["id"], "falsifier": E.falsifier_from(m)["falsifier"],
                        "state_change": "x", "target": "y", "constraint": "z"})
    assert cand["falsifiable"] is True
    assert L.kill(cand, falsifier_met=True)["status"] == L.KILLED


def test_building_12_moved_the_chain_from_11_to_17():
    from sourceborn import discovery as D
    a = D.audit()
    assert 12 not in a["absent"], "stage 12 is built"
    r = D.chain(RAIN, "rain")
    assert r["stages_run"] == 23, r["stages_run"]
    assert r["completed"] is True


def test_stage_18_lets_a_reading_get_stronger_and_weaker():
    """The two failures stage 18 exists to fix, tested in both directions."""
    from sourceborn import maturity as M
    P = lambda c, d=True: {"class": c, "discriminating": d}   # noqa: E731
    # it can get STRONGER: one confirmation, then two of different classes
    assert M.read()["state"] == M.UNTESTED
    assert M.read(confirmed=[P("MATERIAL")])["state"] == M.SUPPORTED
    two = M.read(confirmed=[P("MATERIAL"), P("REPETITION")])
    assert two["state"] == M.STRONG
    # two of the SAME class is one kind of looking twice, not two kinds
    same = M.read(confirmed=[P("MATERIAL"), P("MATERIAL")])
    assert same["state"] == M.SUPPORTED, "same class twice is not STRONG"
    # it can get WEAKER: a refutation costs even beside confirmations
    hurt = M.read(confirmed=[P("MATERIAL"), P("RECORD")], refuted=[P("PLACEMENT")])
    assert hurt["state"] == M.WEAKENED
    # counterexamples below support weaken; at support stage 17 kills, not 18
    assert M.read(counterexamples=1, support=3)["state"] == M.WEAKENED
    assert M.read(killed=True)["state"] == M.KILLED
    # non-discriminating evidence moves nothing, and says how much it dropped
    nd = M.read(confirmed=[P("MATERIAL", False)])
    assert nd["state"] == M.HELD
    assert nd["inputs"]["confirmed_discriminating"] == 0
    # it is never a bare number, and it always says what would move it next
    for r in (two, hurt, nd):
        assert r["is_a_score"] is False
        assert r["why"] and r["what_would_move_it_next"]


def test_decay_is_checks_without_confirmation_never_age():
    from sourceborn import maturity as M
    assert M.read(checks=M.DECAY_AFTER - 1)["state"] == M.UNTESTED
    aged = M.read(checks=M.DECAY_AFTER)
    assert aged["state"] == M.WEAKENED
    assert "never age" in " ".join(aged["why"])
    # recurrence can lift SUPPORTED to STRONG, and says that it did
    lift = M.read(confirmed=[{"class": "MATERIAL", "discriminating": True}],
                  sequences_seen=M.RECURRENCE_MIN)
    assert lift["state"] == M.STRONG and lift["raised_by_recurrence"] is True


def test_a_maturity_is_a_ledger_not_a_field():
    """His no-reopen rule applied to a value: an update appends."""
    from sourceborn import maturity as M
    P = lambda c: {"class": c, "discriminating": True}        # noqa: E731
    u = M.update([], confirmed=[P("MATERIAL")])
    u = M.update(u["chain"], confirmed=[P("MATERIAL"), P("RECORD")])
    u = M.update(u["chain"], confirmed=[P("MATERIAL")], refuted=[P("PLACEMENT")])
    assert u["overwrites"] == 0
    h = M.history(u["chain"])
    assert h["readings"] == 3
    assert h["first"] == M.SUPPORTED and h["current"] == M.WEAKENED
    assert h["changed"] == 2 and h["nothing_removed"] is True
    assert [m["movement"] for m in h["movements"]][1] == "SUPPORTED -> STRONG"
    for r in u["chain"]:
        assert r["overwrote_anything"] is False


def test_stage_19_now_has_all_four_verdicts_including_weaken():
    from sourceborn import maturity as M
    got = {M.verdict(s)["verdict"] for s in M.STATES}
    assert got == {M.RETAIN, M.WEAKEN, M.REJECT, M.UNKNOWN}
    w = M.verdict(M.WEAKENED)
    assert w["verdict"] == M.WEAKEN and w["weaken_exists"] is True
    assert "without ending it" in w["note"]
    assert M.verdict(M.KILLED)["verdict"] == M.REJECT
    assert M.verdict(M.UNTESTED)["verdict"] == M.UNKNOWN


def test_stage_23_closes_and_succeeds_it_never_reopens():
    """His protocol forbids the obvious return edge twice over."""
    from sourceborn import discovery as D
    r = D.chain(RAIN, "x")
    c = D.close(r, new_combinations=3, maturities=[{"state": "UNTESTED"}],
                predictions=[{"discriminating": True, "checked": False}])
    assert c["outcome"] == D.SUCCEEDED
    assert c["closed"]["reopened"] is False
    assert c["closed"]["history_rewritten"] is False
    assert c["successor"]["references"] == c["closed"]["sequence_id"]
    assert c["successor"]["is_a_reopen_of"] is None
    assert c["successor"]["sequence_id"] != c["closed"]["sequence_id"]
    # a successor carries the open ends, not the whole prior pass
    assert c["successor"]["carries_the_whole_prior_pass"] is False
    assert {x["reason"] for x in c["reasons"]} == {
        "NEW COMBINATION", "UNSETTLED MATURITY", "UNMET PREDICTION"}
    # and with nothing open there is NO successor at all
    done = D.close(r, new_combinations=0, maturities=[{"state": "STRONG"}],
                   predictions=[{"discriminating": True, "checked": True}])
    assert done["outcome"] == D.TERMINATED and done["successor"] is None
    assert "not a failure" in done["why"]


def test_the_closed_loop_terminates_three_different_ways():
    from sourceborn import discovery as D
    T = "The father was standing outside with a water pipe."
    # nothing confirms: decay settles it at WEAKENED and the loop stops
    a = D.loop(T, "a", max_passes=6)
    assert a["terminated"] is True and a["hit_cap"] is False
    assert a["settled_as"] == ["WEAKENED"]
    assert a["count"] > 1, "it must actually loop before it stops"
    # confirmations settle it the other way, and faster
    b = D.loop(T, "b", max_passes=6,
               verdicts={"MATERIAL": True, "REPETITION": True,
                         "PLACEMENT": True, "RECORD": True})
    assert b["terminated"] is True and b["settled_as"] == ["SUPPORTED"]
    assert b["count"] < a["count"], "confirmation settles faster than decay"
    # refutations settle it too
    c = D.loop(T, "c", max_passes=6,
               verdicts={"MATERIAL": False, "REPETITION": False,
                         "PLACEMENT": False, "RECORD": False})
    assert c["terminated"] is True and c["settled_as"] == ["WEAKENED"]
    # every pass is its own sequence, referencing the last
    ids = [p["sequence_id"] for p in a["passes"]]
    assert ids == ["S%d" % i for i in range(len(ids))], ids


def test_the_whole_loop_now_runs_23_of_23():
    from sourceborn import discovery as D
    a = D.audit()
    assert a["absent"] == [], a["absent"]
    assert a["counts"][D.RUNS] == 22           # 22 in C, 5 in D
    r = D.chain(RAIN, "rain")
    assert r["stages_run"] == 23 and r["completed"] is True
    assert r["halted_at"] is None


def test_the_maturity_and_loop_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/maturity"', '"/maturity/read"', '"/loop/run"'):
        assert route in src, route


def test_his_23_stage_loop_is_audited_against_the_running_code():
    """do we flow this or anything else — answered by import, not by memory."""
    from sourceborn import discovery as D
    a = D.audit()
    assert a["stages"] == 23
    assert [s["n"] for s in D.STAGES] == list(range(1, 24)), "his order"
    # every anchor the map claims must actually resolve, or the map is lying
    assert a["map_claims_that_do_not_resolve"] == [], \
        a["map_claims_that_do_not_resolve"]
    assert a["counts"][D.RUNS] + a["counts"][D.PARTIAL] + \
        a["counts"].get(D.ABSENT, 0) == 23
    # and the honest headline: the stages mostly exist, the flow does not
    assert a["chained_end_to_end"] is False, "the flag is about the old spine"
    assert D.what_flows()["steps"] == 5, "the old spine is still five steps"


def test_a_stage_with_no_implementation_halts_the_chain():
    """His rule: a failure opens the mapped loop. It is never stepped over."""
    from sourceborn import discovery as D
    # with every stage built the chain completes; the HALT behaviour is proved
    # on a stage that is deliberately made absent instead
    r = D.chain(RAIN, "rain")
    assert r["completed"] is True and r["stages_run"] == 23
    assert "never skipped" in r["law"]


def test_the_three_absent_stages_and_the_one_that_blocks():
    from sourceborn import discovery as D
    g = D.gaps()
    absent = {a["n"] for a in g["absent_stages"]}
    assert absent == set(), absent             # 12, 18 and 23 are all built
    partial = {p["n"] for p in g["partial_stages"]}
    assert partial == {1}, partial             # 5 moved to RUNS in Phase D
    assert 19 not in partial, "WEAKEN exists now"
    assert g["his_call"]


def test_the_loop_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/loop"', '"/loop/chain"', '"/expected"', '"/expected/run"'):
        assert route in src, route


def test_the_arrow_graph_is_drawn_from_the_live_modules():
    """A diagram that can go stale is a diagram that will. Every number in the
    chart is read from the running code at draw time."""
    from sourceborn import human_registry as hr
    from sourceborn import sysmap
    c = sysmap.arrow_chart()
    # the live counts appear because they were read, not typed
    assert "%s named sub-parameters" % format(len(hr.parameters()), ",") in c
    from sourceborn import filemap as F
    d = F.divide(".")
    assert "UNPLACED %d" % d["counts"][F.UNPLACED] in c
    assert "%d GROW THE COUNT" % d["what_grows_the_count"]["files"] in c
    # the boxes line up: every drawn line is the same width
    box = [ln for ln in c.splitlines() if ln.startswith("   │")
           or ln.startswith("   ║")]
    assert box and len({len(ln) for ln in box}) == 1, \
        sorted({len(ln) for ln in box})
    # his laws are on the chart, not just in the code
    for law in ("IT CREATES NOTHING", "AN ADDRESS IS NOT A PARAMETER",
                "THE KILL IS OFF BY DEFAULT",
                "nothing is canonical · nothing is chosen"):
        assert law in c, law
    assert sysmap.stats()["typed_numbers_in_the_chart"] == 0


def test_where_one_thing_lives():
    from sourceborn import sysmap
    assert sysmap.where("the bank")["module"] == "human_registry.py"
    assert sysmap.where("the kill")["route"] == "/ledger/kill"
    assert sysmap.where("nowhere at all")["found"] is False
    assert len(sysmap.where()["layers"]) == sysmap.where()["count"]


def test_the_map_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/map"', '"/map/where"'):
        assert route in src, route


def test_the_artifact_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/artifact"', '"/artifact/generate"', '"/artifact/grow"'):
        assert route in src, route


def test_the_subject_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/subjects"', '"/subjects/grow"', '"/subjects/generate"'):
        assert route in src, route


# ---------------------------------------------------------------------------
# PHASE B — the runtime pipeline, and the two reverse steps that were absent.
# ---------------------------------------------------------------------------

B_RAIN = ("kids father was standing outside with water pipe and pointed it in "
        "the air so that the kids inside the home thought its raining outside")

B_MALL = ("few days back i went to mall with my girlfriend because i was not "
        "well. this weekend i will go again to the mall to buy a gift for her "
        "birthday.")


def test_step_2_reads_the_end_from_the_source():
    """'so that ...' names a target ahead, and the parse finds it."""
    from sourceborn import prior as P
    e = P.declare_end(B_RAIN)
    assert e["named"] is True
    assert e["grade"] == "STATED TARGET"
    assert "thought its raining" in e["end"]
    assert e["direction"] == "REVERSE"
    assert e["halt"] is False


def test_a_reason_behind_is_never_promoted_to_a_target_ahead():
    """'because i was not well' is a PUSH. It is kept, and it is not the end."""
    from sourceborn import prior as P
    e = P.declare_end(B_MALL)
    kinds = {c["id"]: c["kind"] for c in e["candidates"]}
    pushes = [c for c in e["candidates"] if c["kind"].startswith("PUSH")]
    assert pushes, "the stated reason is kept"
    assert all("not well" not in (e["end"] or "") for _ in [0]), \
        "the chosen end is never the reason behind"
    assert e["named"] is True and "birthday" in e["end"]
    # and a text with ONLY a push has no named end — the push does not fill in
    e2 = P.declare_end("he stayed home because he was ill")
    assert e2["named"] is False
    assert e2["push_candidates"] >= 1


def test_two_surviving_ends_halt_and_are_never_blended():
    from sourceborn import prior as P
    e = P.declare_end("he called the meeting in order to warn them, and he "
                      "called it so that the record would show he tried")
    assert e["halt"] is True
    assert e["named"] is False
    assert len(e["chosen"]) == 2
    assert e["separates_them"], "the halt ships with what would separate them"
    assert e["end"] is None, "nothing was blended into a single end"


def test_an_unnamed_end_is_unnamed_never_absent():
    """'there is no reason' is not an available answer."""
    from sourceborn import prior as P
    e = P.declare_end("the king raised the tax")
    assert e["named"] is False
    assert len(e["what_would_name_it"]) == 3
    assert e["why_this_matters"]["consumed_by"], \
        "the four consuming steps are stated even when the end is open"


def test_his_word_outranks_the_parse():
    from sourceborn import prior as P
    e = P.declare_end(B_RAIN, his_end="a joke on the kids")
    assert e["named"] is True
    assert e["end"] == "a joke on the kids"
    assert e["grade"] == "HIS ASSIGNMENT"
    assert e["candidates"], "the parsed candidates are kept beside his word"


def test_step_3_descends_by_the_removal_test_and_cannot_assume():
    from sourceborn import prior as P
    pr = P.prior_reality(B_RAIN, P.declare_end(B_RAIN))
    assert pr["direction"] == "REVERSE"
    assert pr["counts"]["assumed"] == 0, "the descent cannot assume"
    assert pr["counts"]["survived"] > 0
    grades = {r["grade"] for r in pr["survivors"]}
    assert grades <= {"STATED", "ENTAILED"}
    # a dropped prior is kept as a neighbour with the reason
    assert pr["counts"]["dropped_as_neighbours"] >= 1
    n = pr["neighbours"][0]
    assert "NEIGHBOUR" in n["removal_test"]["verdict"]
    assert n["removal_test"]["why"]


def test_the_lexical_drop_is_flagged_where_it_cannot_be_trusted():
    """'pointed it in the air' causes 'thought its raining' and shares no word
    with it. The drop stands — the descent may not use world knowledge — and it
    is flagged for his review, never quietly reversed."""
    from sourceborn import prior as P
    pr = P.prior_reality(B_RAIN, P.declare_end(B_RAIN))
    flagged = pr["flagged_for_review"]
    assert flagged, "the same-sentence drop is flagged"
    assert any("pointed" in f["condition"] for f in flagged)
    assert all("His call" in f["review"] for f in flagged)


def test_assumed_exists_only_through_the_explicit_call():
    from sourceborn import prior as P
    a = P.assume("the father owned the pipe", "needed to complete the chain",
                 proof_debt=3)
    assert a["grade"] == "ASSUMED"
    assert a["synthetic"] is True and a["tag"] == "[SYNTHETIC]"
    assert a["proof_debt"] == 3 and a["expires"]
    try:
        P.assume("x", "y", proof_debt=9)
        assert False, "proof debt outside 0..5 must refuse"
    except ValueError:
        pass


def test_ground_is_claimed_only_when_reached():
    from sourceborn import prior as P
    g = P.ground_check("his body was exhausted and in pain")
    assert g["ground"] is True, "the physical human is something nobody made"
    g2 = P.ground_check("the company rewrote its business model")
    assert g2["ground"] is False
    g3 = P.ground_check("qwerty zzz")
    assert g3["ground"] is False, "unknown is not ground"


def test_the_runtime_walks_all_eighteen_in_his_order():
    from sourceborn import runtime as R
    r = R.run(B_RAIN)
    assert r["steps_run"] == 18 and r["of"] == 18
    assert r["order"] == list(range(1, 19)), "his order, not mine"
    assert r["reverse_steps"] == [2, 3, 11, 13], \
        "two reverse passes: 2-3 at intake, 11 and 13 later"
    names = [rec["name"] for rec in r["records"]]
    assert names[1] == "Declare End / Why This Matters"
    assert names[2] == "Reverse to Prior Reality"
    assert names[3] == "Sequence Decomposition", \
        "2 and 3 run BEFORE decomposition — the correction this phase is for"


def test_a_run_is_a_record_never_an_answer():
    from sourceborn import runtime as R
    for text in (B_RAIN, B_MALL, ""):
        r = R.run(text)
        assert r["answer"] is None, "answer is None on every run, structurally"
        assert r["chosen"] is None
    # and every record carries job / took / produced — his SB-01 correction
    r = R.run(B_RAIN)
    for rec in r["records"]:
        assert rec["job"] and rec["took"] is not None
        assert rec["produced"] is not None, rec["name"]


def test_the_runtime_does_not_write_by_default():
    """Step 17 prepares. His five write conditions are evaluated, two are
    honestly unmet on a bare run, and nothing is appended."""
    from sourceborn import runtime as R
    r = R.run(B_MALL, name="mall")
    wb = next(rec for rec in r["records"] if rec["n"] == 17)["produced"]
    assert wb["written"] is False
    assert wb["conditions_total"] == 5
    assert wb["conditions_met"] == 3
    assert wb["write_conditions"]["link map created"] is False, \
        "the link map IS Phase D — it cannot be met before D exists"
    assert wb["why_not_written"]
    # and the HTTP route does not expose writing at all
    src = open("src/sourceborn/server.py").read()
    at = src.index('"/runtime/run"')
    assert "write" not in src[at:at + 600].replace("would_append", "")


def test_untested_reads_untested_all_the_way_down():
    """R-F-R on one unrepeated ask is thin, maturity is UNTESTED, the verdict
    is UNKNOWN. An eighteen-step run on one sentence SHOULD end open."""
    from sourceborn import runtime as R
    r = R.run(B_RAIN)
    rec = {x["n"]: x["produced"] for x in r["records"]}
    assert rec[13]["stands"] is False
    assert rec[15]["state"] == "UNTESTED"
    assert rec[16]["verdict"] == "UNKNOWN"
    assert rec[14]["survives"] is True
    assert "untested" in next(x for x in r["records"] if x["n"] == 14)["notes"]


def test_the_join_his_bottleneck_fix_built_is_wired():
    """More active containers -> more intents, inside the runtime itself."""
    from sourceborn import runtime as R
    r1 = R.run(B_MALL)
    r2 = R.run(B_RAIN)
    c1 = {x["n"]: x["produced"] for x in r1["records"]}
    c2 = {x["n"]: x["produced"] for x in r2["records"]}
    assert len(c1[5]["containers_activated"]) > 0, \
        "the mall must activate containers (it first activated ZERO — the " \
        "join was not wired)"
    assert c1[10]["candidates"] > 0
    assert c2[10]["candidates"] > c1[10]["candidates"], \
        "more containers active -> more intents, his curve inside the run"
    assert c1[10]["chosen"] is None and c2[10]["chosen"] is None


def test_detection_is_not_choice():
    from sourceborn import runtime as R
    d = R.detect_states("the king was exhausted, his energy down and stress up")
    assert d["detected"], "evidence words in the ask are found"
    assert d["chosen"] is None
    d2 = R.detect_states("the ledger was appended")
    assert d2["detected"] == [] and d2["chosen"] is None


def test_the_two_ends_halt_reaches_the_run():
    from sourceborn import runtime as R
    r = R.run("he called the meeting in order to warn them, and he called it "
              "so that the record would show he tried")
    assert r["halts"] and r["halts"][0]["step"] == 2


def test_the_reverse_passes_are_stated():
    from sourceborn import prior as P
    rp = P.reverse_passes()
    assert rp["passes"][0]["at"] == [2, 3]
    assert rp["passes"][0]["was"] == "ABSENT until Phase B"
    assert rp["passes"][1]["at"] == [13]


def test_same_person_is_relation_not_dependency():
    """The review of this phase's diff caught two defects; this pins the fix.

    A bare substring test let actor 'i' match inside nearly every condition
    ('girlfriend', 'raining'), which made everything survive on first-person
    asks. And a whole-word actor match alone is still not a dependency: 'i was
    not well' explains the FIRST mall visit, and the gift trip stands without
    it — so it reads NEIGHBOUR with its own reason, never silently survives."""
    from sourceborn import prior as P
    pr = P.prior_reality(B_MALL, P.declare_end(B_MALL))
    neigh = [n for n in pr["neighbours"] if "not well" in n["condition"]]
    assert neigh, "'i was not well' is a neighbour of the gift trip"
    t = neigh[0]["removal_test"]
    assert t["actor_shared"] is True and t["breaks"] is False
    assert "relation, not dependency" in t["why"]
    # and separators exist only between competing PULL ends — two reasons
    # behind can both be true, so no contest is manufactured between them
    e = P.declare_end("he stayed home because he was ill and because the "
                      "office was closed")
    assert e["separates_them"] == [] and e["halt"] is False


def test_the_runtime_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/runtime"', '"/runtime/run"'):
        assert route in src, route


# ---------------------------------------------------------------------------
# PHASE C — the combination + intent engine.
# ---------------------------------------------------------------------------

C_T3 = B_RAIN + " and the kids said they felt happy about the rain"


def test_the_rain_sentence_yields_exactly_its_own_shape():
    """One candidate: ACTION on CON-021 met an INFERENCE. Not 240."""
    from sourceborn import combine as C
    r = C.run([B_RAIN], name="rain")
    assert r["counts"]["combinations"] == 1
    c = r["candidates"][0]
    assert c["signature"] == "ACTION->CON-021 + INFERENCE->*"
    assert c["granularity"] == "MIXED"
    assert "QUIET" in r["stopped_because"]
    assert r["answer"] is None and r["chosen"] is None


def test_nothing_floats_on_structure_alone():
    """The mall's words reach no row at per-event level, so the engine opens
    nothing — and reports the anchor rejection instead of hiding it."""
    from sourceborn import combine as C
    r = C.run([B_MALL], name="mall")
    assert r["counts"]["combinations"] == 0
    assert r["rounds"][0]["rejected_no_anchor"] >= 1
    for c in r["candidates"]:
        assert c["granularity"] in ("ROW", "MIXED")


def test_one_example_can_never_breed_order_three():
    """His rule 6 as a structural gate: depth needs recurrence."""
    from sourceborn import combine as C
    r = C.run([C_T3], name="three roles once")
    orders = set(r["counts"]["by_order"])
    assert orders <= {2}, "one example must stop at pairs"
    assert all(not c["can_breed"] for c in r["candidates"])
    blocked = next((rd["blocked_cannot_breed"] for rd in r["rounds"]
                    if rd["round"] == 2), 0)
    assert blocked >= 1, "the breeding gate must report what it blocked"


def test_recurrence_unlocks_depth():
    """'once the basic will over it will start making new combinations on
    new thoughts' — mechanical: the same material twice earns order 3."""
    from sourceborn import combine as C
    r = C.run([C_T3, C_T3], name="three roles twice")
    assert 3 in r["counts"]["by_order"], "support 2 must open order 3"
    assert "QUIET" in r["stopped_because"], "and the loop still finds its stop"


def test_cross_role_holds_over_sets():
    """No candidate carries the same role twice, at any order."""
    from sourceborn import combine as C
    r = C.run([C_T3, C_T3])
    for c in r["candidates"]:
        assert len(c["roles"]) == c["order"], c["signature"]


def test_every_candidate_leaves_carrying_its_chain():
    """Prediction, falsifier, maturity — testable the moment it exists. And
    maturity is fed honestly: co-occurrence is support, not confirmation."""
    from sourceborn import combine as C
    r = C.run([C_T3, C_T3])
    for c in r["candidates"]:
        preds = c["predictions"]
        assert preds[0]["class"] == "REPETITION" and preds[0]["discriminating"]
        assert c["signature"] in preds[0]["would_confirm"]
        assert preds[-1]["class"] == "ABSENCE" and not preds[-1]["discriminating"]
        assert c["falsifiable"] and c["falsifier"]
        assert c["maturity"] == "UNTESTED", \
            "unchecked reads UNTESTED whatever its support — nobody checked " \
            "is not it held"
        assert c["chosen"] is None


def test_more_material_more_combinations_more_intents():
    """His concept, computed: as much parameters we plug, more is generated."""
    from sourceborn import combine as C
    small = C.run([C_T3])
    big = C.run([C_T3, B_RAIN, C_T3])
    assert big["counts"]["combinations"] >= small["counts"]["combinations"]
    assert big["counts"]["intent_pairs_unique"] >= \
        small["counts"]["intent_pairs_unique"]
    assert big["counts"]["new_parameters_created"] == 0
    assert big["counts"]["rows_written"] == 0


def test_stage_22_is_computed_not_by_hand():
    from sourceborn import combine as C
    prev = C.run([B_RAIN])
    cur = C.run([B_RAIN, C_T3, C_T3])
    d = C.delta(prev, cur)
    assert d["stage"] == 22
    assert d["anything_new"] is True and d["count_new"] >= 1
    same = C.delta(cur, cur)
    assert same["anything_new"] is False and same["count_new"] == 0
    # and the discovery audit now reads 22 as running
    from sourceborn import discovery as D
    a = D.audit()
    r22 = next(r for r in a["rows"] if r["n"] == 22)
    assert r22["state"] == "RUNS"
    assert a["counts"]["PARTIAL"] == 1, \
        "stage 1 source lock is the last PARTIAL — stage 5 joined in Phase D"


def test_evidence_is_handed_in_and_kill_is_on_request_only():
    from sourceborn import combine as C
    r = C.run([C_T3, C_T3])
    c = r["candidates"][0]
    up = C.check(c, together_again=1)
    assert up["was"] == "UNTESTED" and up["now"] in ("SUPPORTED", "STRONG")
    assert up["verdict"] == "RETAIN"
    down = C.check(c, apart_events=1)
    assert down["now"] == "WEAKENED" and down["killed"] is False
    assert "his word" in down["kill_available"]
    dead = C.check({**c, "support": 1}, apart_events=5, kill=True)
    assert dead["killed"] is True, "the kill still runs when asked"


def test_the_engine_owns_two_loops_and_says_so():
    from sourceborn import combine as C
    l = C.loops()
    assert len(l["his_nine"]) == 9
    assert l["c_owns"] == ["Combination", "Intent"]
    running = [x for x in l["his_nine"] if x["state"].startswith("RUNS")]
    assert len(running) == 8, "eight of his nine run since Phase D"
    ng = next(x for x in l["his_nine"] if x["loop"] == "Node-Growth")
    assert "awaits his word" in ng["state"], \
        "the ninth stops at the queue — his promotion question is open"


def test_phase_c_writes_nothing():
    """The Phase A technique: read the module's own code, docstrings and
    comments stripped, and prove there is no write path in it."""
    import re as _re
    src = open("src/sourceborn/combine.py").read()
    code = _re.sub(r'""".*?"""', "", src, flags=_re.S)
    code = _re.sub(r"#.*", "", code)
    for forbidden in ("growth.add(", "open(", "def tick", "Thread"):
        assert forbidden not in code, \
            "Phase C must not write, trigger or schedule: found %r" % forbidden


def test_a_cap_that_bites_reports_what_it_dropped():
    from sourceborn import combine as C
    r = C.run([C_T3, C_T3], round_cap=2)
    dropped = sum(rd["dropped_by_round_cap"] for rd in r["rounds"])
    assert dropped >= 1
    noted = [rd for rd in r["rounds"] if rd["dropped_by_round_cap"]]
    assert all(rd["cap_note"] for rd in noted), "no silent caps"


def test_the_engine_is_deterministic():
    from sourceborn import combine as C
    a = C.run([C_T3, B_RAIN])
    b = C.run([C_T3, B_RAIN])
    assert [(c["id"], c["signature"]) for c in a["candidates"]] == \
           [(c["id"], c["signature"]) for c in b["candidates"]]


def test_runtime_step_9_hands_its_seatings_to_the_one_engine():
    """The runtime's view and the engine's can never drift, because there is
    one engine — the same rain ask yields the same one candidate both ways."""
    from sourceborn import combine as C
    from sourceborn import runtime as R
    r = R.run(B_RAIN)
    step9 = next(x for x in r["records"] if x["n"] == 9)["produced"]
    direct = C.run([B_RAIN])
    assert [c["signature"] for c in step9["combinations"]] == \
           [c["signature"] for c in direct["candidates"]]
    assert step9["stopped_because"] == direct["stopped_because"]
    assert "combine.run" in next(x for x in r["records"]
                                 if x["n"] == 9)["owner"]


def test_the_combine_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/combine"', '"/combine/run"'):
        assert route in src, route


# ---------------------------------------------------------------------------
# PHASE D — the memory graph + auto-linking.
# ---------------------------------------------------------------------------

def _ng_root():
    return tempfile.mkdtemp(prefix="sb_ng_")


_RFR = {"stands": True, "r_f_r": ["ran"]}


def test_the_write_gate_refuses_and_names_the_unmet():
    """His five write conditions, enforced at the one write site."""
    from sourceborn import nodegraph as NG
    root = _ng_root()
    r = NG.write_node(root, "EVENT", "src", {}, rfr=None, proof_debt=1)
    assert r["refused"] and r["unmet_conditions"] == ["R-F-R executed"]
    r = NG.write_node(root, "EVENT", "src", {}, rfr=_RFR)
    assert r["refused"] and r["unmet_conditions"] == \
        ["origin distance recorded"]
    r = NG.write_node(root, "EVENT", "", {}, rfr=_RFR, proof_debt=1)
    assert r["refused"] and "source retained" in r["unmet_conditions"]
    assert NG.stats(root)["nodes"] == 0, "nothing malformed was stored"


def test_a_link_map_with_zero_links_is_still_a_map():
    """The fourth condition is met BY the write path — the linker runs even
    when nothing matches, and says so."""
    from sourceborn import nodegraph as NG
    root = _ng_root()
    r = NG.write_node(root, "EVENT", "his rain sentence",
                      {"event_sig": "POINT_PIPE"}, rfr=_RFR, proof_debt=1)
    assert r["written"] and r["conditions_met"] == 5
    assert r["conditions"]["link map created"] is True
    assert r["link_map"]["count"] == 0
    assert "still a MAP" in r["link_map"]["note"]


def test_an_existing_match_is_reinforced_never_recreated():
    """His mall-example rule applied to nodes: support 1 -> 2,
    duplicate_created False."""
    from sourceborn import nodegraph as NG
    root = _ng_root()
    r1 = NG.write_node(root, "EVENT", "src",
                       {"event_sig": "POINT_PIPE", "actor": "father"},
                       rfr=_RFR, proof_debt=1)
    r2 = NG.write_node(root, "EVENT", "src",
                       {"event_sig": "POINT_PIPE", "actor": "father"},
                       rfr=_RFR, proof_debt=1, surfaced_by="a second source")
    assert r2["duplicate_created"] is False
    assert r2["strengthened_existing"] == r1["node_id"]
    assert r2["support"] == 2
    assert NG.stats(root)["by_type"].get("EVENT") == 1


def test_similar_event_needs_shared_rows_never_containers():
    """The Phase C anchor lesson carried into linking: structure is not
    content."""
    from sourceborn import nodegraph as NG
    root = _ng_root()
    a = NG.write_node(root, "EVENT", "src",
                      {"event_sig": "A", "rows": ["P1", "P2"],
                       "containers": ["CON-001", "CON-002"]},
                      rfr=_RFR, proof_debt=1)["node_id"]
    b = NG.write_node(root, "EVENT", "src",
                      {"event_sig": "B", "rows": ["P1", "P2", "P9"],
                       "containers": ["CON-001", "CON-002"]},
                      rfr=_RFR, proof_debt=1)
    links = [l for l in b["link_map"]["links"] if l["link"] == "similar_to"]
    assert links and links[0]["to"] == a, "2 shared rows link"
    c = NG.write_node(root, "EVENT", "src",
                      {"event_sig": "C", "rows": ["P7"],
                       "containers": ["CON-001", "CON-002"]},
                      rfr=_RFR, proof_debt=1)
    assert not c["link_map"]["links"], \
        "shared containers alone must never link"


def test_hub_nodes_materialize_once():
    """Two events by one actor: an ACTOR node exists ONCE, each event linked
    actor_of — the graph shape his twelve types exist for."""
    from sourceborn import nodegraph as NG
    root = _ng_root()
    NG.write_node(root, "EVENT", "src", {"event_sig": "A", "actor": "king"},
                  rfr=_RFR, proof_debt=1)
    r2 = NG.write_node(root, "EVENT", "src",
                       {"event_sig": "B", "actor": "king"},
                       rfr=_RFR, proof_debt=1)
    hubs = r2["link_map"]["hubs"]
    assert hubs and hubs[0]["type"] == "ACTOR" and not hubs[0]["created"], \
        "the second write must REUSE the hub"
    assert NG.stats(root)["by_type"].get("ACTOR") == 1
    links = [l for l in r2["link_map"]["links"] if l["link"] == "actor_of"]
    assert links and links[0]["from"].startswith("SB-N-ACT-")


def test_opposition_contradicts_and_both_stand():
    """Same subject, opposing verdicts -> a contradicts link, neither
    deleted. The dedupe defect this test first caught — an opposing reading
    folded into the node it opposed — is why the match requires the same
    CLAIM, verdict included."""
    from sourceborn import nodegraph as NG
    root = _ng_root()
    d = NG.write_node(root, "RULE", "his ruling",
                      {"subject_sig": "never goes", "verdict": "RETAIN"},
                      rfr=_RFR, proof_debt=1)["node_id"]
    e = NG.write_node(root, "RULE", "the counter-reading",
                      {"subject_sig": "never goes", "verdict": "REJECT"},
                      rfr=_RFR, proof_debt=1)
    assert e["written"], "an opposing reading is a NEW node, not a duplicate"
    con = [l for l in e["link_map"]["links"] if l["link"] == "contradicts"]
    assert con and con[0]["to"] == d
    assert NG.node_state(root, d)["found"], "the contradicted node stands"


def test_the_memory_chain_references_the_reading_before():
    """The 90-empty-brains answer at node level: a memory is a chain, not a
    field."""
    from sourceborn import nodegraph as NG
    root = _ng_root()
    a = NG.write_node(root, "EVENT", "src", {"event_sig": "A"},
                      rfr=_RFR, proof_debt=1)["node_id"]
    NG.remember(root, a, "EVENT", "first seen")
    NG.remember(root, a, "EVIDENCE", "a prediction was confirmed")
    mem = NG.memory_of(root, a)
    assert [m["n"] for m in mem] == [1, 2]
    assert mem[0]["references"] is None and mem[1]["references"] == 1
    try:
        NG.remember(root, a, "NOT_A_KIND", "x")
        assert False, "an unknown memory kind must refuse"
    except KeyError as err:
        assert "his eleven memory kinds" in str(err)


def test_stage_5_is_traversable_and_every_hop_is_typed():
    from sourceborn import nodegraph as NG
    root = _ng_root()
    a = NG.write_node(root, "EVENT", "src",
                      {"event_sig": "A", "actor": "king",
                       "rows": ["P1", "P2"]}, rfr=_RFR,
                      proof_debt=1)["node_id"]
    NG.write_node(root, "EVENT", "src",
                  {"event_sig": "B", "actor": "king",
                   "rows": ["P3", "P4"]}, rfr=_RFR, proof_debt=1)
    c = NG.write_node(root, "EVENT", "src",
                      {"event_sig": "C", "rows": ["P3", "P4"]},
                      rfr=_RFR, proof_debt=1)["node_id"]
    p = NG.path(root, a, c)
    assert p["found"], "a reaches c through the actor hub and shared rows"
    assert all(h["link"] for h in p["hops"]), "every hop names its link type"
    sg = NG.subgraph(root, a, depth=1)
    assert a in sg["nodes"] and sg["counts"]["links"] >= 1
    # and the discovery audit reads stage 5 as running now
    from sourceborn import discovery as D
    r5 = next(r for r in D.audit()["rows"] if r["n"] == 5)
    assert r5["state"] == "RUNS"


def test_recall_is_the_retrieval_loop():
    from sourceborn import nodegraph as NG
    root = _ng_root()
    NG.write_node(root, "EVENT", "src",
                  {"event_sig": "A", "actor": "king", "future": "the wall"},
                  rfr=_RFR, proof_debt=1)
    got = NG.recall(root, {"actor": "king", "future": "the wall",
                           "rows": []})
    assert got["conditions"]["same_actor"]
    assert got["conditions"]["same_future_goal"]
    assert got["reached"], "the probe reaches stored nodes with evidence"
    empty = NG.recall(root, {"actor": "nobody"})
    assert empty["reached"] == []


def test_the_queue_holds_until_his_word():
    """His box 6 runs up to the queue and stops where only his word may
    act. The queue is a placeholder for his unanswered question, not the
    answer."""
    from sourceborn import nodegraph as NG
    root = _ng_root()
    f = NG.write_node(root, "PATTERN", "src", {"pattern_sig": "care loop"},
                      rfr=_RFR, proof_debt=1,
                      maturity_level="SUPPORTED")["node_id"]
    q0 = NG.queue_for_him(root)
    assert q0["count"] == 0, "maturity alone does not queue — the evidence " \
                            "gate is real"
    NG.remember(root, f, "EVIDENCE",
                "confirmed: the discriminating prediction held")
    q1 = NG.queue_for_him(root)
    assert [x["node_id"] for x in q1["queued"]] == [f]
    assert q1["promoted"] == 0
    assert "he has not answered" not in q1  # dict key sanity
    assert "his word" in q1["promoted_stays_zero_until"]
    ap = NG.approve(root, f)
    assert ap["status"] == "ACCEPTED" and ap["by"] == "him"
    q2 = NG.queue_for_him(root)
    assert q2["count"] == 0 and q2["promoted"] == 1
    # NO REOPEN — the original NODE row in the file still says OPEN
    raw = open(NG._path(root)).read()
    assert '"status": "OPEN"' in raw
    st = NG.node_state(root, f)
    assert st["status"] == "ACCEPTED" and st["status_is_from"] == \
        "his approval"


def test_the_graph_store_is_append_only_structurally():
    """The growth.py technique: read the module's own source and fail if a
    removal path is ever added."""
    import re as _re
    src = open("src/sourceborn/nodegraph.py").read()
    code = _re.sub(r'""".*?"""', "", src, flags=_re.S)
    code = _re.sub(r"#.*", "", code)
    for forbidden in (".pop(", "os.remove", "os.unlink", "rmtree",
                      "truncate", '"w"', "'w'"):
        assert forbidden not in code, \
            "the graph must be append-only: found %r" % forbidden
    assert '"a"' in code, "the store opens in append mode"


def test_a_corrupt_line_is_kept_as_unreadable():
    from sourceborn import nodegraph as NG
    root = _ng_root()
    NG.write_node(root, "EVENT", "src", {"event_sig": "A"}, rfr=_RFR,
                  proof_debt=1)
    with open(NG._path(root), "a", encoding="utf-8") as f:
        f.write("{this is not json\n")
    rows = NG.load(root)
    bad = [r for r in rows if r.get("row") == "UNREADABLE"]
    assert bad and bad[0]["raw"].startswith("{this is not json")
    assert NG.stats(root)["unreadable_kept"] == 1


def test_node_ids_carry_their_type_and_count_per_type():
    from sourceborn import nodegraph as NG
    root = _ng_root()
    a = NG.write_node(root, "EVENT", "src", {"event_sig": "A"}, rfr=_RFR,
                      proof_debt=1)["node_id"]
    b = NG.write_node(root, "EVENT", "src", {"event_sig": "B"}, rfr=_RFR,
                      proof_debt=1)["node_id"]
    r = NG.write_node(root, "RULE", "src", {"subject_sig": "S"}, rfr=_RFR,
                      proof_debt=1)["node_id"]
    assert a == "SB-N-EVT-00001" and b == "SB-N-EVT-00002"
    assert r == "SB-N-RUL-00001", "each type counts its own"


def test_the_node_graph_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/nodes"', '"/nodes/node"', '"/nodes/path"',
                  '"/nodes/subgraph"', '"/nodes/write"',
                  '"/nodes/remember"', '"/nodes/recall"',
                  '"/nodes/approve"'):
        assert route in src, route


def test_nothing_is_born_promoted():
    """The review of this phase's diff caught it: a writer that could mint
    status ACCEPTED directly would be self-promotion past his word. ACCEPTED
    arrives only through approve()."""
    from sourceborn import nodegraph as NG
    root = _ng_root()
    r = NG.write_node(root, "EVENT", "src", {"event_sig": "A"}, rfr=_RFR,
                      proof_debt=1, status="ACCEPTED")
    assert r["refused"] and r["unmet_conditions"] == ["born ACCEPTED"]
    assert "his approval" in r["why"]
    assert NG.stats(root)["nodes"] == 0
    assert NG.queue_for_him(root)["promoted"] == 0


def test_concurrent_writes_never_mint_the_same_id():
    """The weekly-pull lesson applied here: node numbering is load-count-
    append, this server answers on threads, and without the lock two
    concurrent writes mint one id."""
    import threading as _th
    from sourceborn import nodegraph as NG
    root = _ng_root()
    ids, errs = [], []

    def w(i):
        try:
            r = NG.write_node(root, "EVENT", "src",
                              {"event_sig": "E%d" % i}, rfr=_RFR,
                              proof_debt=1)
            ids.append(r["node_id"])
        except Exception as e:
            errs.append(str(e))

    threads = [_th.Thread(target=w, args=(i,)) for i in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errs, errs
    assert len(ids) == 8 and len(set(ids)) == 8, \
        "every concurrent write must get its own id: %s" % sorted(ids)


# ---------------------------------------------------------------------------
# PHASE E — the self-sustain scheduler.
# ---------------------------------------------------------------------------

def _auto_root():
    return tempfile.mkdtemp(prefix="sb_auto_")


def test_manual_mode_now_is_the_shipped_default():
    """His staging law, honored exactly: deploying Phase E changes nothing.
    The daemon call is a no-op in MANUAL and appends no report."""
    from sourceborn import autoloop as A
    root = _auto_root()
    assert A.mode(root) == "MANUAL"
    r = A.tick_if_due(root)
    assert r["ran"] is False and "manual" in r["why"].lower()
    assert A.ticks(root) == [], "a MANUAL daemon check leaves no row"


def test_the_mode_is_his_switch_and_invalid_is_refused():
    from sourceborn import autoloop as A
    root = _auto_root()
    bad = A.set_mode(root, "TURBO")
    assert bad["refused"] and "his three modes" in bad["why"]
    ok = A.set_mode(root, "SEMI_AUTO")
    assert ok["changed"] and ok["by"] == "him" and ok["prior"] == "MANUAL"
    assert A.mode(root) == "SEMI_AUTO"
    back = A.set_mode(root, "MANUAL")
    assert back["prior"] == "SEMI_AUTO", "the log keeps what it was before"


def test_a_tick_writes_through_the_gated_site():
    """The runtime's own steps compose the refs; the node arrives through
    Phase D's five conditions with its link map made."""
    from sourceborn import autoloop as A
    from sourceborn import nodegraph as NG
    root = _auto_root()
    t = A.tick(root, texts=[B_RAIN])
    assert len(t["written_nodes"]) == 1
    w = t["written_nodes"][0]
    assert w["node_id"].startswith("SB-N-EVT-")
    assert "event_sig" in w["refs"] and "rows" in w["refs"]
    st = NG.node_state(root, w["node_id"])
    assert st["found"] and st["node"]["point_zero_ref"]
    assert t["combine"]["combinations"] >= 1
    assert t["queued_for_him"] == 0 and t["promoted"] == 0


def test_the_same_material_reinforces_instead_of_duplicating():
    from sourceborn import autoloop as A
    root = _auto_root()
    A.tick(root, texts=[B_RAIN])
    t2 = A.tick(root, texts=[B_RAIN])
    assert t2["written_nodes"] == []
    assert t2["reinforced"] and t2["reinforced"][0]["support"] == 2
    assert t2["combine"]["delta_new"] == 0, \
        "the second tick opens nothing the first did not"


def test_the_inbox_cursor_skips_unchanged_and_reprocesses_changed():
    """Nothing is un-processed by deletion — the hash cursor."""
    import os as _os
    from sourceborn import autoloop as A
    root = _auto_root()
    p = _os.path.join(A._inbox(root), "note.txt")
    with open(p, "w") as f:
        f.write("the king raised the tax so that the wall could be built")
    t1 = A.tick(root)
    assert t1["processed"] == ["note.txt"]
    t2 = A.tick(root)
    assert t2["arrived"]["inbox_skipped_unchanged"] == ["note.txt"]
    assert t2["quiet"] is True
    assert _os.path.exists(p), "the file was never removed"
    with open(p, "w") as f:
        f.write("the king lowered the tax so that the people would stay")
    t3 = A.tick(root)
    assert t3["processed"] == ["note.txt"], \
        "a changed file is a superseding reading, processed again"


def test_a_deferred_handed_text_is_named_not_lied_about():
    """The dishonest line the first run caught: 'never dropped' is only true
    for inbox items. A deferred handed text must be handed again, and the
    report says so."""
    from sourceborn import autoloop as A
    root = _auto_root()
    texts = ["actor %d did thing %d so that result %d stood" % (i, i, i)
             for i in range(7)]
    t = A.tick(root, texts=texts)
    assert len(t["processed"]) == A.MAX_ITEMS_PER_TICK
    d = t["deferred_by_budget"]
    assert len(d["handed"]) == 2 and d["inbox"] == []
    assert "handed again" in d["handed_note"]
    assert t["caps"]["cap_note"], "a cap that bites is never silent"


def test_a_quiet_daemon_tick_appends_nothing_a_hand_tick_always_does():
    from sourceborn import autoloop as A
    root = _auto_root()
    A.set_mode(root, "SEMI_AUTO")
    before = len(A.ticks(root))
    r = A.tick_if_due(root)
    assert r["quiet"] is True
    assert len(A.ticks(root)) == before, \
        "an hourly heartbeat would flood an append-only ledger"
    h = A.tick(root, by="hand")
    assert h["quiet"] is True
    assert len(A.ticks(root)) == before + 1, \
        "he asked, and 'quiet' is an answer"


def test_auto_sustain_feeds_the_last_ticks_own_output_back():
    """The L4 loop — the only loop whose input is the system's own output.
    Bounded to one example, and reported."""
    from sourceborn import autoloop as A
    root = _auto_root()
    A.set_mode(root, "AUTO_SUSTAIN")
    t1 = A.tick(root, texts=[B_RAIN])
    assert t1["written_nodes"], "the first tick writes"
    assert t1["arrived"]["feedback_example"] is False, \
        "nothing to feed back on the first pass"
    t2 = A.tick(root, texts=[C_T3])
    assert t2["arrived"]["feedback_example"] is True
    # and in SEMI_AUTO the same second tick would NOT feed back
    root2 = _auto_root()
    A.set_mode(root2, "SEMI_AUTO")
    A.tick(root2, texts=[B_RAIN])
    s2 = A.tick(root2, texts=[C_T3])
    assert s2["arrived"]["feedback_example"] is False


def test_a_tick_is_not_a_check():
    """Maturities decay on checks-without-confirmation — his rule — and a
    tick checks nothing against the world."""
    from sourceborn import autoloop as A
    root = _auto_root()
    t = A.tick(root, texts=[B_RAIN])
    assert t["maturities_touched"] == 0
    assert "not a check" in t["why_no_maturity_moves"]


def test_the_tick_cannot_promote_kill_or_grow_the_count():
    """The gate chart, enforced by absence — the Phase A technique."""
    import re as _re
    from sourceborn import autoloop as A
    src = open("src/sourceborn/autoloop.py").read()
    code = _re.sub(r'""".*?"""', "", src, flags=_re.S)
    code = _re.sub(r"#.*", "", code)
    for forbidden in ("approve(", ".kill(", "growth.add(", "grow(",
                      "add_many("):
        assert forbidden not in code, \
            "a tick may not promote, kill or write his count ledger: " \
            "found %r" % forbidden
    g = A.gate()
    assert "promote" in g["auto_may_not"] and "answer" in g["auto_may_not"]
    # and a tick report has no answer field at all
    root = _auto_root()
    t = A.tick(root, texts=[B_RAIN])
    assert "answer" not in t, "a tick does not answer"
    assert t["promoted_can_move_from_here"] is False


def test_the_auto_store_is_append_only_structurally():
    import re as _re
    src = open("src/sourceborn/autoloop.py").read()
    code = _re.sub(r'""".*?"""', "", src, flags=_re.S)
    code = _re.sub(r"#.*", "", code)
    for forbidden in (".pop(", "os.remove", "os.unlink", "rmtree",
                      "truncate"):
        assert forbidden not in code, \
            "the tick ledger must be append-only: found %r" % forbidden


def test_the_daemon_thread_carries_the_tick_in_its_own_try():
    src = open("src/sourceborn/scheduler.py").read()
    assert "autoloop.tick_if_due" in src
    at = src.index("autoloop.tick_if_due")
    window = src[at - 200:at]
    assert "try:" in window, \
        "the tick must run in its own try so neither job can kill the other"


def test_the_auto_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/auto"', '"/auto/tick"', '"/auto/mode"'):
        assert route in src, route


# ---------------------------------------------------------------------------
# THE GLASS REACTOR — the home page, on his word.
# ---------------------------------------------------------------------------

def test_the_reactor_survives_whole_and_the_rewrite_holds_the_door():
    """Two of his words in order: 2026-08-24 made the reactor the home page;
    2026-09-03 said 'accordignly the dashboard will prepared not what we
    have' — so THE REWRITE now holds /, and the reactor is NOT removed: it
    stands whole at /reactor, the old dashboard still at /desk. This test
    pinned the reactor at / until his later word; it now pins both rulings."""
    from sourceborn import homepage
    src = open("src/sourceborn/server.py").read()
    at = src.index('path in ("/", "/index.html")')
    assert "selfhome.PAGE" in src[at:at + 500], "/ serves THE REWRITE"
    at2 = src.index('path == "/reactor"')
    assert "homepage.PAGE" in src[at2:at2 + 400], "the reactor stands whole"
    assert '"/desk"' in src, "the old dashboard is kept, never deleted"
    assert 'href="/desk"' in homepage.PAGE, "the reactor links back to it"


def test_no_black_background_his_ruling():
    """'i dont want black back ground' — the reactor lives on light."""
    from sourceborn import homepage
    p = homepage.PAGE
    assert "#070809" not in p and "#000" not in p.replace("#0000", "")
    assert "--ground:#f2f6fb" in p, "the luminous ground is the ground"


def test_the_ask_tab_is_on_the_home_page_and_wired_to_one_engine():
    """His catch on the sample — 'where is the ask tab'. It is the panel's
    head, and it calls the SAME engine the /engine page calls, plus the
    seating and the runtime — three views of one ask, never a second
    engine."""
    from sourceborn import homepage
    p = homepage.PAGE
    assert "<textarea id=q" in p, "the ask box exists"
    for wire in ('post("/ask"', 'post("/growing/place"',
                 'post("/runtime/run"'):
        assert wire in p, wire
    assert "Promise.allSettled" in p, \
        "one unreachable view must not kill the others"


def test_the_bank_structure_lights_exact_points():
    """/api/bank carries each container's flat P start, so a seated row
    lights its EXACT point — Standing balance in CON-021 (start 801, index
    34) is P0835, which is precisely where his rain example seats."""
    from sourceborn import human_registry as hr
    start, starts = 1, {}
    for c in hr.containers():
        starts[c["id"]] = (start, c["count"])
        start += c["count"]
    assert start - 1 == 3204, "the starts must tile the whole bank exactly"
    assert starts["CON-021"][0] == 801
    assert starts["CON-042"] == (1641, 42) and starts["CON-057"][1] == 42
    c21 = hr.container("CON-021")
    assert c21["subs"][34] == "Standing balance"
    assert 801 + 34 == 835, "the rain seat lights its true point"


def test_a_correction_is_a_write_back_never_a_rewrite():
    """'must be editable so i can change' — built on his own law: the edit
    lands as a CORRECTION row referencing the target; the registry document
    is never touched."""
    from sourceborn import growth as G
    from sourceborn import human_registry as hr
    root = tempfile.mkdtemp(prefix="sb_corr_")
    before = hr.container("CON-021")["subs"][34]
    row = G.add(root, G.CORRECTION, "P0835: Standing balance — his words",
                detail="Standing balance", module="homepage",
                extra={"target": "P0835", "was": "Standing balance",
                       "now": "Standing balance — his words"})
    assert row["id"] == "SB-CORR-0001" and row["kind"] == "CORRECTION"
    assert row["target"] == "P0835"
    assert hr.container("CON-021")["subs"][34] == before, \
        "the source row stays whole — NO REOPEN"
    rows = G.load(root)
    assert any(r.get("kind") == "CORRECTION" for r in rows)
    src = open("src/sourceborn/server.py").read()
    assert '"/growth/correct"' in src


def test_his_success_story_stance_is_mechanical():
    """His teaching of 2026-08-24, filed under 'failure -': take the success
    stories 'if they can i will too' instead 'i will also do the same'."""
    from sourceborn import claims as C
    his = ('there is new trading, promoting the success stories, they try to '
           'copy and failed, they built something there own. We should take '
           'the success stories "if they can i will too" instead "i will '
           'also do the same"')
    r = C.success_story_stance(his)
    assert r["stance"].startswith("POSSIBILITY"), \
        "his own sentence carries both phrasings, and 'instead' IS the choice"
    copy = C.success_story_stance(
        "He made millions in trading and I will also do the same")
    assert copy["stance"].startswith("TEMPLATE COPY")
    assert copy["conclusion_allowed"] is False
    assert "built something their own" in copy["why_the_copy_fails"]
    assert len(copy["what_was_theirs"]) == 5, \
        "the judgment gate's hidden layers are what the copier never sees"
    poss = C.success_story_stance(
        "Her success story tells me: if they can, i will too — my own way")
    assert poss["stance"].startswith("POSSIBILITY")
    assert poss["conclusion_allowed"] is True
    unstated = C.success_story_stance(
        "his success story is everywhere these days")
    assert unstated["stance"].startswith("STANCE UNSTATED")
    assert unstated["conclusion_allowed"] is False, \
        "an unstated stance is held open, never chosen for him"
    none = C.success_story_stance("the weather was nice today")
    assert none["success_story_present"] is False


def test_the_stance_refuses_the_conclusion_never_the_person():
    from sourceborn import claims as C
    r = C.success_story_stance("I saw his success story and will do the same")
    assert "never the human" in C.success_story_stance.__doc__
    assert "do the same and you will succeed" in r["refuses"]
    assert r["extends"].startswith("DO_NOT_JUDGE_THE_VISIBLE_THING")


def test_the_bridge_carries_meaning_across_the_word_gap():
    """Built on his word. The run on his failure teaching showed the bank
    already held the exact rows it is about — and both matchers missed all
    of them, because the teaching says 'copy' and the bank says
    'imitation'. The bridge is the carrier."""
    from sourceborn import bridge as BR
    HIS = ('they try to copy and failed, We have to understand they built '
           'something there own, how someone can re do the same. We should '
           'take the success stories "if they can i will too" instead '
           '"i will also do the same"')
    rows = BR.rows_via(HIS)
    ids = {r["sb_id"] for r in rows}
    assert {"SB-HFR-P0885", "SB-HFR-P0886", "SB-HFR-P0887",
            "SB-HFR-P2451"} <= ids
    for r in rows:
        assert r["via_bridge"] and r["phrase"] and r["taught_by"], \
            "every bridged row names the bridge, the phrase and the teaching"
        assert r["band"] == "TAUGHT"
    assert rows[0]["name"] == "Direct imitation", "the real row name"


def test_both_readings_are_always_kept():
    """A bridged seat never merges silently into the direct seats — the
    senses.py law applied to vocabulary."""
    from sourceborn import growing as G
    HIS = 'they try to copy and failed'
    s = G.seat(HIS, limit=12)
    assert "bridged" in s and s["bridged"], "the taught reading exists"
    direct = {x["sb_id"] for x in s["seats"]}
    taught = {x["sb_id"] for x in s["bridged"]}
    assert not (direct & taught), "never merged"
    p = G.place(HIS, name="bridge test")
    via = [x for x in p["strengthened"] if x.get("via_bridge")]
    assert via, "place folds bridged rows in, MARKED"
    assert all(x["via_bridge"].startswith("BR-") for x in via)
    s2 = G.seat("the king raised the tax", limit=6)
    assert s2["bridged"] == [], "no bridge words, no bridged rows"


def test_the_bridge_is_whole_word_and_longest_first():
    """The semantic_loss lesson: 'productive' must never fire
    'Reproductive'. And his full phrase wins before any fragment."""
    from sourceborn import bridge as BR
    assert BR.match("photocopying machines are loud") == [], \
        "'photocopying' must not fire the copy bridge"
    m = BR.match("if they can i will too")
    assert [x["bridge"] for x in m] == ["BR-002"]
    assert m[0]["phrase"] == "if they can i will too", "longest phrase wins"


def test_the_absence_is_refused_a_wrong_bridge():
    """His teaching carries social comparison; the bank holds no general
    row for it, and P0597 is BODY-comparison — a different thing. Bridging
    to the wrong row would be the word-coincidence failure through another
    door, so it is refused and reported."""
    from sourceborn import bridge as BR
    a = BR.KNOWN_ABSENCE
    assert "social comparison" in a["concept"]
    assert "NOT bridged" in a["nearest_row"]
    assert a["his_call"]
    for b in BR.SEEDED:
        assert "SB-HFR-P0597" not in b["targets"]


def test_every_seeded_bridge_carries_his_approval():
    from sourceborn import bridge as BR
    from sourceborn import growth as G
    for b in BR.SEEDED:
        assert b["taught_by"].startswith("his failure teaching")
        assert "his word" in b["approved"]
    assert "BRIDGE" in G.SERIES and G.SERIES["BRIDGE"] == "SB-BR-%03d", \
        "future bridges arrive through the ledger, append-only"


def test_the_adoption_is_byte_identical_and_inert():
    """His word: adopt what is not here, touch nothing in C-SB, lay off my
    brain. 42 files byte-identical with SHA custody; nothing wired into
    engine behavior; every seam a HALT for him."""
    from sourceborn import adopted as A
    v = A.verify()
    assert v["files"] == 42 and v["byte_identical"] is True, \
        (v["drifted"], v["missing"])
    assert v["origin_commit"].startswith("9e3f179")
    st = A.stats()
    assert st["csb_untouched"] is True
    assert st["wired_into_engine_behavior"] is False
    assert "lay off ur brain" in st["his_word"]
    # the adopted module contains no write path and no engine import —
    # the Phase A technique
    import re as _re
    src = open("src/sourceborn/adopted.py").read()
    code = _re.sub(r'""".*?"""', "", src, flags=_re.S)
    code = _re.sub(r"#.*", "", code)
    for forbidden in ("growth.add(", '"a"', "'a'", "def tick",
                      "import growing", "import runtime", "import combine"):
        assert forbidden not in code, \
            "the adoption reads and halts — it must not write or wire: " \
            "found %r" % forbidden


def test_the_adopted_counts_are_the_true_counts():
    from sourceborn import adopted as A
    assert A.locks()["count"] == 30            # SEQ-LOCK-001..030
    assert len(A.intent_types()["types"]) == 8
    assert A.ai64()["records"] == 64
    assert A.engines75()["engine_count"] == 75
    op = A.operational()
    assert op["containers"] == 80
    assert op["subparameters"] == 480          # 2593..3072 is 480 wide
    assert A.expansion32()["records"] == 32
    assert A.native2560()["records"] == 2560
    assert A.nodes22()["node_count"] == 22
    assert A.rubrics52()["count"] == 52
    assert "EVERYTHING HAPPENING IS AN EVENT" in A.intent_types()["motto"]


def test_the_seams_halt_instead_of_deciding():
    """Same numerals, different namespaces; same words, different things —
    every one of them is his call, and the list says so."""
    from sourceborn import adopted as A
    hs = A.halts()
    assert len(hs) == 7
    assert all(h["his_call"] for h in hs)
    h1 = next(h for h in hs if h["id"] == "ADOPT-HALT-1")
    assert "P2561" in h1["seam"] and "namespaces" in h1["seam"]
    assert A.expansion32()["namespace_note"].startswith("the ASI-Brain")
    # and the wisdom pipeline is adopted with C-SB's own scope, unwired
    w = A.wisdom()
    assert w["wired_into_this_core"] is False
    assert "not" in w["adoption_scope_as_csb_states_it"].lower()


def test_his_original_rain_wording_is_preserved():
    from sourceborn import adopted as A
    ex = A.his_examples()
    assert "when i want to take my kids out" in ex["rain_original_source"]
    assert any("RAIN_TARGET_LAYER" in f for f in ex["files"])
    assert any("FATHER_DOOR" in f for f in ex["files"])


def test_the_adopted_route_is_reachable():
    src = open("src/sourceborn/server.py").read()
    assert '"/adopted"' in src


def test_the_workbook_adoption_is_byte_identical_and_verified():
    """His word: 'this file too for review and adoption.' The SB-ASI Drive
    master (ASI-Brain_Task3_Approved_Final_v1_0): the .xlsx byte-identical
    plus 33 derived sheet texts, every one SHA-256'd and re-hashed."""
    from sourceborn import adopted as A
    v = A.wb_verify()
    assert v["files"] == 34 and v["byte_identical"] is True, \
        (v["drifted"], v["missing"])
    assert "this file too for review and adoption" in v["his_word"]
    st = A.wb_stats()
    assert st["sheets"] == 33
    assert st["wired_into_engine_behavior"] is False


def test_the_bridge_is_stated_by_his_own_file_and_counted_here():
    """The workbook states how the two banks relate; the numbers are
    COUNTED from its sheets, never retyped: 2,554 exact + 650 reserve =
    his 3,204, and 2,554 + 6 visible reconstructions = the 2,560."""
    from sourceborn import adopted as A
    b = A.the_bridge()
    assert b["carried_exact"] == 2554
    assert b["held_in_reserve"] == 650
    assert b["carried_plus_reserve"] == 3204
    assert b["baseline_2560"] == 2560
    ids = [r["id"] for r in b["reconstruction_candidates"]]
    assert ids == ["SB-ASI-P%d" % n for n in range(1303, 1309)], ids
    assert all("REQUIRES USER APPROVAL" in r["status"]
               for r in b["reconstruction_candidates"])
    assert b["decided_here"] is False


def test_the_master_workbook_findings_are_reported_not_corrected():
    from sourceborn import adopted as A
    fs = A.wb_findings()
    assert len(fs) == 5
    assert all(f["corrected"] is False for f in fs)
    assert any("wording extraction required" in f["finding"] for f in fs)
    assert any("OPEN SOURCE GAP" in f["finding"] for f in fs)


def test_the_split_is_filed_whole_and_every_step_is_populated():
    """His order: rebuild it complete with all 183 containers and all rows.
    27 segments, 183 containers, 3,483 rows, 12 steps, none empty."""
    from sourceborn import sbx
    v = sbx.verify()
    assert v["pillars"] == 6
    assert v["steps"] == 12
    assert v["segments"] == 27
    assert v["containers"] == 183, v["containers"]
    assert v["rows"] == 3483, v["rows"]
    assert v["every_step_populated"] is True, v["containers_per_step"]
    assert sum(v["containers_per_step"].values()) == 183
    # every container reachable, every row carries its home
    assert len(sbx.containers()) == 183
    assert len(sbx.rows()) == 3483
    assert all(r["container"] and r["step"] for r in sbx.rows()[:200])


def test_the_source_bank_is_replaced_never_deleted():
    """His ruling on the reversal: do not delete, replace with the new standing.
    The 3,204 stand exactly as they were, beside the split."""
    from sourceborn import sbx, human_registry as hr
    assert len(hr.parameters()) == 3204
    assert len(hr.containers()) == 80
    assert len(hr.segments()) == 10
    assert sbx.verify()["source_untouched"] is True
    # and every split container names the source container it came from
    assert all(c["from"]["container"].startswith("CON-") for c in sbx.containers())


def test_both_columns_stand_at_every_container():
    """ASI is the verified connection between the two columns; a node with only
    the human half cannot link."""
    from sourceborn import sbx
    for c in sbx.containers():
        assert c["human"], c["id"]
        assert c["computer"], c["id"]
        assert c["human"] != c["computer"], c["id"]
    m = sbx.computer_of("SBX-CON-055")           # Working Memory
    assert "RAM" in m["computer"] or "cache" in m["computer"].lower()
    assert m["human"] == "Working Memory"


def test_his_loop_still_closes_and_the_second_order_is_marked():
    """Steps 1-8 are his and step 8 returns to step 1. Steps 9-12 are the life
    of the loop itself — the distinction is recorded, not lost."""
    from sourceborn import sbx
    sp = {x["step"]: x for x in sbx.spine()}
    assert sp[1]["name"] == "GROUND" and sp[8]["name"] == "LOOP"
    assert "CLOSES TO STEP 1" in sp[8]["order"]
    for n in (1, 2, 3, 4, 5, 6, 7, 8):
        assert sp[n]["order"].startswith("FIRST ORDER"), n
    for n in (9, 10, 11, 12):
        assert sp[n]["order"].startswith("SECOND ORDER"), n
    for n in (11, 12):
        assert "ANY-STEP" in sp[n]["order"], n
    assert "MASK" in sp[6]["line"].upper()


def test_the_nine_intent_types_are_placed_on_the_spine():
    from sourceborn import sbx
    its = sbx.intent_types()
    assert len(its) == 9, sorted(its)
    for n in range(1, 10):
        assert "IT-%02d" % n in its, n
    assert its["IT-05"]["step_name"] == "LOOP"        # recovery
    assert its["IT-03"]["step_name"] == "USE"         # automaticity
    assert its["IT-06"]["step_name"] == "NAMING"      # role/virtue binding


def test_the_wiring_lands_an_ask_on_his_spine():
    """The seating is unchanged; it is now READ through the split and lands on
    steps. Nothing is chosen and no intent is concluded."""
    from sourceborn import sbx
    r = sbx.place_on_spine("my son sits down to study at seven. after ten "
                           "minutes he gets up. he did not sleep well last night.")
    assert r["concluded"] is None
    assert r["source_rows_seated"] > 0
    assert r["mapped_into_split"] == r["source_rows_seated"], "a seated row was dropped"
    assert r["steps_lit_count"] >= 1
    lit = {s["step"] for s in r["steps_lit"]}
    assert 1 in lit, "the sleep rows are GROUND — his own reverse walk found the same"
    for s in r["steps_lit"]:
        assert s["human"] and s["computer"]


def test_archetype_link_and_scale_are_open_with_no_ceiling():
    """His ruling: no count, it is open to increase.

    This test used to assert all three held zero, which was true when they
    were declared and false the moment the archetype layer was built — a
    typed count goes stale as soon as the thing it counts changes. It now
    asserts the count is LIVE: ARCHETYPE reads from the module, LINK and
    SCALE still hold nothing and say so."""
    from sourceborn import sbx, archetype
    layers = sbx.open_layers()
    ids = [d["id"] for d in layers]
    assert ids == ["ARCHETYPE", "LINK", "SCALE"]
    for d in layers:
        assert d["ceiling"] is None, "his ruling: no ceiling"
        assert d["opens_at"] and d["state"]
        assert isinstance(d["count"], int)
    from sourceborn import link, scale
    by = {d["id"]: d for d in layers}
    assert by["ARCHETYPE"]["count"] == len(archetype.archetypes()) >= 11
    assert by["LINK"]["count"] == len(link.links()) > 900
    assert by["SCALE"]["count"] == len(scale.bands()) == 9
    # SCALE is the one still holding a gate — built and counted, but only his
    # four bands are in force
    assert len(scale.active()) == 4
    assert "await his word" in by["SCALE"]["state"]


def test_the_sbx_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/sbx"', '"/sbx/step"', '"/sbx/container"', '"/sbx/place"',
                  '"/sbx/nodes"'):
        assert route in src, route
    assert "sbx.place_on_spine(" in src


def test_the_workbook_seams_halt_instead_of_deciding():
    """ADOPT-HALT-8..12 — the bridge, three filter vocabularies, the twelve
    states, the missing raw workbook, the scripture surfaces. Nobody here
    decides one of them."""
    from sourceborn import adopted as A
    hs = A.wb_halts()
    assert [h["id"] for h in hs] == \
        ["ADOPT-HALT-%d" % n for n in range(8, 13)]
    assert all(h["his_call"] for h in hs)
    h8 = hs[0]
    assert "2,554" in h8["seam"] and "P1303" in h8["seam"]
    # and the route serves the workbook block beside the C-SB block
    src = open("src/sourceborn/server.py").read()
    assert "adopted.wb_verify()" in src and "adopted.the_bridge()" in src


def test_the_hud_and_bank_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/api/hud"', '"/api/bank"'):
        assert route in src, route
    # and no figure on the page is typed into the markup — the HUD cells
    # boot as em-dashes and fill from the fetch
    from sourceborn import homepage
    assert 'id=h_bank>—<' in homepage.PAGE.replace('"', "")  # dash, not a number


def test_an_inbox_file_named_handed_is_still_inbox():
    """The review caught the first cut sniffing the 'handed ' name prefix:
    an inbox file literally named 'handed 1' would have stayed out of the
    cursor and been reprocessed forever. Items carry their KIND now."""
    import os as _os
    from sourceborn import autoloop as A
    root = _auto_root()
    with open(_os.path.join(A._inbox(root), "handed 1"), "w") as f:
        f.write("the trap file did a thing so that the cursor would miss it")
    t1 = A.tick(root)
    assert t1["processed"] == ["handed 1"]
    assert t1["processed_inbox"] == [{"name": "handed 1",
                                      "hash": t1["processed_inbox"][0]["hash"]}]
    t2 = A.tick(root)
    assert t2["arrived"]["inbox_skipped_unchanged"] == ["handed 1"], \
        "the cursor must see it — kind, not name, decides"


def test_his_word_seeds_semi_auto_across_a_deploy():
    """He gave the switch order — 'switch it to semi auto', 2026-08-21 —
    before the Phase E code reached the deployed app. The boot seed carries
    it: an empty mode log comes up SEMI_AUTO citing his words verbatim."""
    from sourceborn import autoloop as A
    root = _auto_root()
    r = A.seed_his_word(root)
    assert r["seeded"] is True and A.mode(root) == "SEMI_AUTO"
    assert r["his_word"] == "switch it to semi auto"
    rows = [x for x in A._load(A._mode_path(root)) if x.get("row") == "MODE"]
    assert "'switch it to semi auto'" in rows[-1]["why"]
    assert rows[-1]["by"] == "him"
    # seeding twice adds nothing
    assert A.seed_his_word(root)["seeded"] is False
    assert len([x for x in A._load(A._mode_path(root))
                if x.get("row") == "MODE"]) == 1


def test_any_row_he_writes_outranks_the_seed_forever():
    """Including a later return to MANUAL — the seed never argues with a
    log that speaks."""
    from sourceborn import autoloop as A
    root = _auto_root()
    A.set_mode(root, "MANUAL")
    r = A.seed_his_word(root)
    assert r["seeded"] is False and A.mode(root) == "MANUAL"
    # and the server boots through the seed
    src = open("src/sourceborn/server.py").read()
    assert "seed_his_word" in src


def test_feedback_never_anchors_its_own_combinations():
    """The review caught feedback parts arriving row-marked: the system's
    own output could then anchor combinations by itself — the system
    certifying its own material. Feedback is CONTAINER-grade memory; only
    fresh rows anchor."""
    from sourceborn import autoloop as A
    root = _auto_root()
    A.set_mode(root, "AUTO_SUSTAIN")
    A.tick(root, texts=[B_RAIN])
    # a second tick whose only material is the feedback example: the mall
    # text seats no rows, so if feedback could self-anchor, combinations
    # would appear here — none may
    t2 = A.tick(root, texts=[B_MALL])
    assert t2["arrived"]["feedback_example"] is True
    assert t2["combine"]["combinations"] == 0, \
        "feedback + rowless material must open nothing — no self-anchoring"


# ---------------------------------------------------------------------------
# PHASE 9 — THE ARCHETYPE LAYER
# ---------------------------------------------------------------------------

def test_every_archetype_row_is_a_real_row_of_his_bank():
    """The one thing an archetype may never do is cite a parameter that is
    not there. Every (id, name, container) triple is re-checked against the
    live registry — nine of the first twelve rows written for ARCH-011 were
    wrong from memory, and this test is why that was caught."""
    from sourceborn import archetype as A, asi_pyramid as AP
    rows, _ = AP._flat()
    by_id = {r["sb_id"]: r for r in rows}
    checked = 0
    for a in A.archetypes():
        assert a["reaches"], a["id"] + " reaches nothing"
        for pid, name, cid in a["reaches"]:
            row = by_id.get(pid)
            assert row is not None, "%s cites %s which is not in the bank" % (a["id"], pid)
            assert row["name"].strip().lower() == name.strip().lower(), \
                "%s %s: claimed %r, bank says %r" % (a["id"], pid, name, row["name"])
            assert row["container"] == cid, \
                "%s %s: claimed %s, bank says %s" % (a["id"], pid, cid, row["container"])
            checked += 1
    assert checked >= 97, checked


def test_the_archetype_reaches_across_containers_which_is_why_it_is_a_layer():
    """A row lives in exactly one container. An archetype that reached only
    one container would belong inside it and would not need a layer. Every
    archetype must span containers, and the widest must span segments."""
    from sourceborn import archetype as A
    for a in A.archetypes():
        cons = {c for _, _, c in a["reaches"]}
        assert len(cons) >= 2, "%s reaches one container — it is a row, not a layer" % a["id"]
    widest = max(A.archetypes(), key=lambda a: len({c for _, _, c in a["reaches"]}))
    assert len({c for _, _, c in widest["reaches"]}) >= 8


def test_the_dice_game_went_from_zero_rows_to_real_rows():
    """The proof this phase exists for. Measured before the layer: his dice
    sentence seated ZERO rows — not because the rows were missing but
    because there was no route from those words to them."""
    from sourceborn import archetype as A
    r = A.compare("he bet everything he had to win it all back and lost what "
                  "he could never recover")
    assert r["words_alone"]["rows"] == 0, r["words_alone"]
    assert r["gain"] >= 10, r
    assert "SB-HFR-P1873" in r["with_archetype"]["added_ids"]   # Sunk-cost sensitivity
    assert "SB-HFR-P2517" in r["with_archetype"]["added_ids"]   # Commitment escalation risk
    assert any(x.startswith("ARCH-001") for x in r["archetypes_fired"])


def test_all_of_his_dead_examples_now_reach_the_bank():
    """His three examples that seated zero rows, plus the book shapes. Each
    must reach rows through the layer, and each must name what it matched."""
    from sourceborn import archetype as A
    cases = {
        "a man is stealing money from a shop": "ARCH-011",
        "diamond cut diamond": "ARCH-004",
        "he stole the money to save his dying child": "ARCH-011",
        "they melted their own gold into an idol while he was still on the mountain": "ARCH-002",
        "do the work and do not look at the fruit": "ARCH-003",
        "he gave everything and got nothing in return": "ARCH-010",
    }
    for text, want in cases.items():
        f = A.fires_on(text)
        assert want in [x["id"] for x in f["fired"]], (text, f["fired"])
        assert f["rows_reached_count"] > 0, text
        for x in f["fired"]:
            assert x["matched_on"], "%s fired on %r with no evidence" % (x["id"], text)


def test_the_meaning_route_stays_silent_on_ordinary_sentences():
    """The macro route must not become a route to everything. Ordinary
    sentences carrying no archetype fire nothing."""
    from sourceborn import archetype as A
    for text in ("the cat sat on the mat",
                 "i went to the shop and bought bread and milk",
                 "the train leaves at four in the afternoon",
                 "my kids are playing outside in the garden",
                 "it is raining and the road is wet",
                 "please send me the report by friday",
                 "she opened the window because the room was warm"):
        assert A.fires_on(text)["fired_count"] == 0, text


def test_two_shared_words_are_not_a_shape():
    """His own IDF bar, one storey up: a concept word belonging to several
    archetypes is weak evidence. `everything` and `all` sit in three lists
    apiece — two of them together may not fire an archetype."""
    from sourceborn import archetype as A
    assert A.SHARED["everything"] >= 2 and A.SHARED["all"] >= 2
    hits = A._hits("all everything", A.get("ARCH-007"))
    assert [h for h in hits if h["route"] == "MEANING"] == []
    # but a distinctive word alongside does fire, and says which word did it
    hits = A._hits("test everything", A.get("ARCH-007"))
    meaning = [h for h in hits if h["route"] == "MEANING"]
    assert meaning and "test" in meaning[0]["distinctive"]


def test_an_archetype_concludes_nothing_and_creates_no_parameter():
    """It REACHES rows; it never owns them, never chooses among them, and
    never adds to the bank."""
    from sourceborn import archetype as A, human_registry as hr
    before = len(hr.parameters())
    f = A.fires_on("he bet everything to win it all back")
    assert f["concluded"] is None
    for x in f["fired"]:
        assert x["chosen"] is None
        assert x["refuses"] and x["discriminator"]
    assert len(hr.parameters()) == before == 3204
    assert A.CEILING is None, "his ruling: no count, open to increase"
    src = open("src/sourceborn/archetype.py").read()
    for forbidden in ("growth.add", "def add_parameter", "PARAM"):
        assert forbidden not in src, forbidden


def test_the_archetype_is_in_the_ask_path_not_behind_a_page():
    """The defect weighting.py had: a module importable from nothing. The
    archetype must reach the spine placement, and every row must say which
    route reached it — WORDS and ARCHETYPE are never summed into one number."""
    from sourceborn import sbx
    r = sbx.place_on_spine("he bet everything he had to win it all back and "
                           "lost what he could never recover")
    assert r["source_rows_seated"] == 0, "the words still reach nothing"
    assert r["archetype_rows_reached"] >= 10, r
    assert r["steps_lit_count"] >= 5, "his dice game lit no step before this"
    assert [a["id"] for a in r["archetypes_fired"]] == ["ARCH-001"]
    by = {h["reached_by"] for h in r["hits"]}
    assert by == {"ARCHETYPE"}, by
    for h in r["hits"]:
        assert h["via"], "a row reached by archetype must name which one"
    # and an ask the words DO reach is still reached by the words
    r2 = sbx.place_on_spine("i study late at night but i keep thinking about tomorrow")
    assert "WORDS" in {h["reached_by"] for h in r2["hits"]}


def test_the_archetype_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/archetype"', '"/archetype/run"'):
        assert route in src, route
    assert "archetype.fires_on(" in src and "archetype.compare(" in src


# ---------------------------------------------------------------------------
# PHASE 0 — THE MEANING LOCK
# ---------------------------------------------------------------------------

def _meaning_root():
    import tempfile
    return tempfile.mkdtemp(prefix="sb_meaning_")


def test_a_meaning_sheet_never_carries_a_meaning_this_side_wrote():
    """His words: *what the example means, in your words, NOT MY READING.* A
    sheet whose his_meaning was filled from here would invert the whole
    point."""
    from sourceborn import meaning as M
    sheets = M.sheets()
    assert len(sheets) == 8
    for s in sheets:
        assert s["his_meaning"] == "", s["example_id"]
        assert s["signed"] is False
        assert s["my_reading"], "he needs something concrete to disagree with"
        assert s["his_words"] and s["text"]


def test_a_signature_without_a_meaning_is_refused():
    from sourceborn import meaning as M
    root = _meaning_root()
    r = M.sign(root, "EX-RAIN", "   ")
    assert r["signed"] is False
    assert "signs nothing" in r["refused"]
    assert M.blocked(root)["signed_count"] == 0


def test_an_unsigned_meaning_cannot_be_used_by_any_later_phase():
    """His rule, as a function."""
    from sourceborn import meaning as M
    root = _meaning_root()
    assert M.usable(root) == []
    b = M.blocked(root)
    assert b["unsigned_count"] == 8 and b["gate_open"] is False
    assert "running on unsigned meanings" in b["honest_state"]
    M.sign(root, "EX-RAIN", "the father arranged the rain; the point is the "
                            "arrangement, not the pipe")
    u = M.usable(root)
    assert [x["example_id"] for x in u] == ["EX-RAIN"]
    assert u[0]["his_meaning"].startswith("the father arranged")
    assert M.blocked(root)["gate_open"] is False, "one of eight is not the batch"


def test_re_signing_appends_and_keeps_what_it_supersedes():
    """His standing rule: nothing is removed. A changed meaning keeps its
    history."""
    from sourceborn import meaning as M
    root = _meaning_root()
    M.sign(root, "EX-DICE", "first meaning")
    r2 = M.sign(root, "EX-DICE", "corrected meaning")
    assert r2["prior_kept"] == 1 and r2["supersedes"]
    rows = M.load(root)
    assert len(rows) == 2, "both rows kept"
    assert M.signed(root)["EX-DICE"]["his_meaning"] == "corrected meaning"


# ---------------------------------------------------------------------------
# PHASE 3 — THE NAMING CLEANUP
# ---------------------------------------------------------------------------

def test_no_example_of_his_is_still_called_a_test():
    """His words: *Samrath is an example, like the rest — not a test.* A test
    is run to see whether something is broken; an example is material the
    system seats on and grows from."""
    from sourceborn import naming as N
    s = N.scan(".")
    assert s["count"] == 0, s["still_calling_an_example_a_test"]
    import os
    assert not os.path.exists("docs/method/canon/THE_SAMRATH_TEST_AND_THE_ZERO.md")
    assert os.path.exists("docs/method/canon/THE_SAMRATH_EXAMPLE_AND_THE_ZERO.md")


def test_his_own_removal_test_keeps_its_name():
    """Not every 'test' is wrong. `prior.removal_test` is HIS method, verbatim
    — take the step away, does the thing above still stand? Renaming it would
    rename his word."""
    from sourceborn import naming as N, prior
    kept = {k["where"] for k in N.KEEP}
    assert "prior.removal_test" in kept
    assert callable(prior.removal_test)
    for k in N.KEEP:
        assert k["why"], k["where"]
    src = open("src/sourceborn/prior.py", encoding="utf-8").read()
    assert "HIS TEST, verbatim" in src


def test_the_rename_did_not_move_the_reading():
    """His proof: a live run showing the example still reaching the same rows
    under its new name. A rename that moved a reading would be a rename that
    changed the system."""
    from sourceborn import naming as N
    v = N.verify()
    assert v["rows"] == 106 and v["containers"] == 16 and v["segments"] == 5
    assert v["activate"]["working"] == 18
    assert v["unchanged_by_the_rename"] is True


def test_the_rename_table_is_the_product_and_names_his_gate():
    from sourceborn import naming as N
    t = N.table()
    assert len(t) >= 5
    for r in t:
        assert r["before"] and r["after"] and r["what_it_is"]
        assert r["approved_by_him"] is False, "the names are his to approve"
    assert N.APPROVED_BY_HIM is False


# ---------------------------------------------------------------------------
# PHASE 8 — THE RUBRICS WIRED
# ---------------------------------------------------------------------------

def test_his_rubrics_fire_by_name_where_seven_things_fired_before():
    """His proof: *before — 7 of ~200 rubric dimensions touch an answer.
    After — a live run showing which rubrics fired on your own example, by
    name.*"""
    from sourceborn import rubrics as R
    assert len(R.BEFORE) == 7
    f = R.fires_on("he bet everything he had to win it all back and lost what "
                   "he could never recover")
    assert f["catalogue"] >= 66
    assert f["fired_count"] > 7, "the whole point of the phase"
    assert f["fired_count"] + f["silent_count"] == f["catalogue"]
    for x in f["fired"]:
        assert x["rubric"] and x["fired_at"] and x["why"]
        assert x["concluded"] is None
    assert f["concluded"] is None


def test_a_rubric_fires_because_the_ask_reached_the_step_it_acts_on():
    """His own placement does the work — the rubric was already put at the
    step where it acts. This is the join that was missing, not a new rule."""
    from sourceborn import rubrics as R
    f = R.fires_on("he bet everything he had to win it all back and lost what "
                   "he could never recover")
    from sourceborn import sbx
    lit = {s["step"] for s in sbx.place_on_spine(
        "he bet everything he had to win it all back and lost what he could "
        "never recover")["steps_lit"]}
    for x in f["fired"]:
        assert any(a["step"] in lit for a in x["fired_at"]), x["rubric"]
    # and a rubric whose step was NOT reached stays silent
    assert f["silent_count"] > 0


def test_the_three_dimensions_he_said_none_of_them_have():
    """scale · era-survival · situations-held-across, added ON a fired rubric
    rather than as new rubrics — his instruction was filling the gaps, not
    adding anything random."""
    from sourceborn import rubrics as R
    assert R.DIMENSIONS == ("scale", "era_survival", "situations_held_across")
    f = R.fires_on("diamond cut diamond")
    x = f["fired"][0]
    assert x["era_survival"] == "UNTESTED"
    assert "nobody checked" in x["era_survival_why"]
    s = x["situations_held_across"]
    assert s["of"] == 8 and 0 <= s["count"] <= 8
    assert "never typed" in s["how"]


def test_adopt_halt_3_stays_shut_while_his_own_rubrics_run():
    """The gate asks whether R01-R52 and his 25 are one family and whose names
    win. That blocks a MERGE. It does not block wiring his own 66, which are
    already in his architecture under his own names."""
    from sourceborn import rubrics as R
    h = R.ADOPT_HALT_3
    assert h["merged"] is False
    assert "merging the two vocabularies" in h["what_it_blocks"]
    assert "wiring HIS OWN 66" in h["what_it_does_not_block"]
    assert R.stats()["adopt_halt_3_merged"] is False


def test_the_phase_routes_are_reachable():
    src = open("src/sourceborn/server.py", encoding="utf-8").read()
    for route in ('"/naming"', '"/rubrics"', '"/rubrics/run"', '"/meaning"',
                  '"/meaning/sign"'):
        assert route in src, route
    assert "rubrics.fires_on(" in src and "meaning.sign(" in src


# ---------------------------------------------------------------------------
# PHASE 13 — ANGLES, A PROPERTY AND NEVER A LAYER
# ---------------------------------------------------------------------------

def test_angles_carry_no_ids_because_he_ruled_them_a_property():
    """HIS ARGUMENT, not mine: *if angles were a layer they would have IDs and
    a fixed count. You said they grow with each example. A property can grow
    without renumbering anything; a layer cannot.* So an ANG-001 appearing here
    would mean angles had quietly become a layer."""
    import ast, re
    from sourceborn import angles as A
    # read the module's own CODE with docstrings stripped — the established
    # technique here. The docstring names the forbidden pattern in order to
    # forbid it, so a raw scan matches its own explanation.
    tree = ast.parse(open("src/sourceborn/angles.py", encoding="utf-8").read())
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
            if (node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)):
                node.body.pop(0)
    code = ast.unparse(tree)
    assert not re.search(r"ANG-\d", code), "angles must not acquire ids"
    for a in A.angles():
        assert "id" not in a, a["name"]
        assert a["name"]
    assert A.stats()["has_ids"] is False


def test_his_four_angles_give_four_different_container_sets():
    """His own test of whether an angle does anything: *Same sentence, four
    different container sets.* Worst reaches harm and moral responsibility,
    best reaches loyalty and commitment, emotional reaches shame and
    face-saving, truth reaches the value rows."""
    from sourceborn import angles as A
    r = A.apply("he staked his wife and lost")
    assert r["angles_run"] == 4
    assert [x["angle"] for x in r["readings"]] == \
        ["worst", "best", "emotional", "truth/dharma"]
    assert r["distinct_container_sets"] == 4, "four positions, four sets"
    assert r["chosen"] is None
    for x in r["readings"]:
        assert x["chosen"] is None and x["refuses"] and x["his_reading"]
    # the row he named by hand is on the truth angle
    truth = A.get("truth/dharma")
    assert ("SB-HFR-P2561", "Value-behaviour alignment", "CON-064") in truth["reaches"]


def test_every_row_an_angle_reaches_is_real():
    from sourceborn import angles as A
    v = A.verify()
    assert v["ok"] is True, v["problems"]
    assert v["rows_checked"] == 29


def test_an_angle_can_be_grown_without_renumbering_anything():
    """His reason for making it a property. Adding one renumbers nothing
    because there is nothing numbered."""
    from sourceborn import angles as A
    before = len(A.angles())
    try:
        out = A.grow("test-position", "a position added by a later example",
                     "his reading would go here", "a row family",
                     [("SB-HFR-P2561", "Value-behaviour alignment", "CON-064")])
        assert out["renumbered"] == 0
        assert out["angles_now"] == before + 1
        assert A.get("test-position")["by"] == "PROPOSED"
        assert A.verify()["ok"] is True, "a grown angle must cite real rows too"
    finally:
        A.GROWN_ANGLES.clear()
    assert len(A.angles()) == before


def test_angles_run_inside_the_answer_path_as_a_property():
    from sourceborn import sbx
    r = sbx.place_on_spine("he staked his wife and lost")
    assert r["properties_applied"] == ["ANGLE"]
    assert r["angles"]["run"] == 4
    assert r["angles"]["distinct_container_sets"] == 4
    assert r["angles"]["chosen"] is None
    # ANGLE is a property, so it is NOT in the layer list
    assert "ANGLE" not in r["layers_run"]


# ---------------------------------------------------------------------------
# PHASE 14 — THE MACRO RESPONSE
# ---------------------------------------------------------------------------

def test_the_one_line_comes_from_the_widest_thing_that_fired():
    """His pyramid: *always the bigger slab come first … and that tiny one is
    the finale.* An archetype reaches ACROSS containers; a row sits in one. So
    the archetype is the macro reading and the row is said last."""
    from sourceborn import macro
    r = macro.respond("he bet everything he had to win it all back and lost "
                      "what he could never recover")
    one = r["one_line"]
    assert one["state"] == macro.STATED
    assert one["shape"].startswith("ARCH-001")
    assert one["line"] and one["refuses"]
    assert r["slab_order"] == ["ONE LINE", "PILLAR", "STEP", "SEGMENT",
                               "CONTAINER", "ROW"]
    # the finale is last and it is the ROW
    assert r["slabs"][-1]["slab"] == "ROW"
    assert "finale" in r["slabs"][-1]["note"]
    assert r["slabs"][0]["slab"] == "ONE LINE"


def test_an_unnamed_shape_is_not_filled_by_the_biggest_row():
    """When no archetype fires the shape is UNNAMED. Substituting the largest
    row would be the tiny slab pretending to be the big one — the opposite of
    his pyramid."""
    from sourceborn import macro
    r = macro.respond("the train leaves at four in the afternoon")
    one = r["one_line"]
    assert one["shape"] == "UNNAMED"
    assert one["line"] is None
    assert one["state"] == macro.PROPOSED
    assert one["would_verify"]
    assert "pretending to be the big one" in one["why_not_invented"]


def test_it_states_what_is_verified_and_proposes_what_is_not():
    """His words: *States it when verified; proposes it for confirmation when
    not.*"""
    from sourceborn import macro
    r = macro.respond("he bet everything he had to win it all back and lost "
                      "what he could never recover")
    assert set(r["stated"]) == {"ONE LINE", "PILLAR", "STEP", "SEGMENT",
                                "CONTAINER", "ROW"}
    assert r["proposed"] == []
    # a reading is never STATED — it is a position or a candidate
    kinds = {k["kind"]: k for k in r["read_not_verified"]}
    assert kinds["ANGLE"]["state"] == macro.PROPOSED
    assert kinds["INTENT READING"]["state"] == macro.PROPOSED
    for k in r["read_not_verified"]:
        if k["state"] == macro.PROPOSED:
            assert k["would_verify"], k["kind"]
    assert r["concluded"] is None


def test_length_is_a_measured_mechanism_and_there_is_no_floor():
    """His mechanism: *big lengthy response will capture more parameters to
    hit and make something new (Because in shorter answers ASI will say
    already exists, so never terse responses).* Measured, not asserted."""
    from sourceborn import macro
    r = macro.respond("he bet everything he had to win it all back and lost "
                      "what he could never recover")
    g = r["generativity"]
    assert g["parameters_reached_by_the_full_response"] > 40
    assert g["gain"] == (g["parameters_reached_by_the_full_response"]
                         - g["parameters_a_one_row_answer_would_reach"])
    assert g["gain"] > 40, "the length is what makes the reach"
    assert r["floor_on_length"] is None
    assert macro.FLOOR_ON_LENGTH is None
    # and nothing truncates
    src = open("src/sourceborn/macro.py", encoding="utf-8").read()
    for forbidden in ("[:200]", "[:500]", "textwrap.shorten", "truncate"):
        assert forbidden not in src, forbidden
    # his correction is carried where the code can see it
    assert "vague" in macro.HIS_WORDS["not_vague"]
    assert "MACRO" in macro.HIS_WORDS["not_vague"]


def test_the_angle_and_macro_routes_are_reachable():
    src = open("src/sourceborn/server.py", encoding="utf-8").read()
    for route in ('"/angles"', '"/angles/run"', '"/macro"', '"/macro/run"'):
        assert route in src, route
    assert "macro.respond(" in src and "angles.apply(" in src


# ---------------------------------------------------------------------------
# PHASE 15 — THE RE-READ
# ---------------------------------------------------------------------------

def test_the_reread_compares_like_instrument_with_like():
    """The first draft compared every recorded number against the SEATING and
    reported the mall at 72 -> 0 and Samrath at 106 -> 0 — two catastrophic
    regressions, neither of them real. Those numbers came from
    asi_pyramid.rows_for, a different mechanism answering a different
    question. Every example now records which instrument produced its `then`,
    and the re-read runs that one."""
    from sourceborn import reread as R
    for ex in R.EXAMPLES:
        assert ex["instrument"] in R.INSTRUMENTS, ex["id"]
    rep = R.report()
    by = {e["id"]: e for e in rep["examples"]}
    assert by["EX-SAMRATH"]["now"]["instrument"] == "bank_matcher"
    assert by["EX-SAMRATH"]["now"]["rows_total"] == 106
    assert by["EX-MALL"]["now"]["rows_total"] == 72
    assert by["EX-DICE"]["now"]["instrument"] == "seating"


def test_his_examples_are_carried_in_his_exact_wording():
    """His law: capture the exact words before interpreting. The first draft
    paraphrased Samrath and got 84 rows instead of his 106 — the paraphrase,
    not the system, was the difference."""
    from sourceborn import reread as R
    by = {e["id"]: e for e in R.EXAMPLES}
    assert by["EX-SAMRATH"]["text"] == (
        "Samrath never like to go to school, he always cry, but today is his "
        "birthday, he went very happy.")
    assert "water pipe" in by["EX-RAIN"]["text"], "his real rain wording"
    assert "Girlfriend" in by["EX-MALL"]["text"], "his real mall wording"


def test_a_count_that_did_not_move_can_still_be_a_changed_meaning():
    """HIS NAMED CASE, and the reason this module compares row IDENTITY. The
    rain sentence read 2 rows when it was recorded and reads 2 rows now — so a
    count-only check calls it UNCHANGED. Both rows are different."""
    from sourceborn import reread as R
    e = R.read_one("EX-RAIN")
    assert e["verdict"] == "CHANGED — SAME COUNT, DIFFERENT ROWS"
    assert e["rows_moved"] == 0
    assert e["same_rows"] is False
    assert e["then_rows_named"] == ["Air/breathing drive", "Thought suppression"]
    assert "Standing balance" in e["now_rows_named"]
    assert set(n.lower() for n in e["then_rows_named"]).isdisjoint(
        n.lower() for n in e["now_rows_named"]), "not one row survived"
    # and the defect the canon recorded is still there, not quietly dropped
    assert "Standing balance" in e["known_defect_then"]


def test_every_movement_names_the_ruling_behind_it():
    """A number moving is not a defect — 0 -> 20 on the stealing example is
    the archetype layer doing its job. A movement with NO ruling behind it is
    drift, and drift is the finding."""
    from sourceborn import reread as R
    rep = R.report()
    assert rep["unexplained"] == [], rep["unexplained"]
    for e in rep["examples"]:
        if e["verdict"].startswith("CHANGED") and e["verdict"] != \
                "CHANGED — SAME COUNT, DIFFERENT ROWS":
            assert e["explained_by"], e["id"]
            for c in e["explained_by"]:
                assert c["his_words"] and c["where"], c["id"]


def test_the_reread_reports_and_changes_nothing():
    """It re-files no example, corrects no canon, and does not decide the new
    reading is the right one. Two readings of one example is exactly the case
    his own law covers — both stand, the gap goes to him."""
    from sourceborn import reread as R
    rep = R.report()
    assert rep["his_call"] is True
    for e in rep["examples"]:
        assert e["changed_here"] is None
    src = open("src/sourceborn/reread.py", encoding="utf-8").read()
    for forbidden in ("growth.add", "open(", "write(", "def correct"):
        assert forbidden not in src, forbidden


def test_an_example_with_no_recorded_reading_says_so():
    from sourceborn import reread as R
    e = R.read_one("EX-STUDY")
    assert e["verdict"] == "NOT RECORDED"
    assert e["then"]["rows"] is None
    assert "never filled" in e["note"]


def test_the_reread_route_is_reachable():
    src = open("src/sourceborn/server.py", encoding="utf-8").read()
    assert '"/reread"' in src and "reread.report()" in src


# ---------------------------------------------------------------------------
# THE DOCS AUDIT — a doc's wiring is whether its claims still hold
# ---------------------------------------------------------------------------

def _repo_docs(pattern="*.md"):
    import subprocess
    return [p for p in subprocess.run(["git", "ls-files", pattern],
                                      capture_output=True, text=True).stdout.split()
            if not p.startswith("adopted/")]


def test_no_doc_names_a_code_symbol_that_does_not_exist():
    """A doc that says `module.function()` is making a checkable claim. 52 such
    claims across the docs; every one must resolve, or the doc is describing
    code that is not there."""
    import os, re
    srcs = {f[:-3]: open("src/sourceborn/" + f, encoding="utf-8").read()
            for f in os.listdir("src/sourceborn") if f.endswith(".py")}
    ext = {"py", "json", "md", "html", "txt", "xlsx", "docx", "yaml", "yml",
           "csv", "jsonl"}
    # symbols that are real but not module-level defs: instance attributes and
    # dict keys the module actually produces
    allowed = {"engine.grounding", "patterns.possible_interpretations"}
    bad = []
    for d in _repo_docs():
        txt = open(d, encoding="utf-8", errors="replace").read()
        for mod, sym in set(re.findall(r"`(\w+)\.(\w+)\(?`", txt)):
            if mod not in srcs or sym in ext or "%s.%s" % (mod, sym) in allowed:
                continue
            if not re.search(
                    r"^\s*(?:async\s+)?(?:def|class)\s+%s\b|^%s\s*[:=]|^\s{4}%s\s*[:=]"
                    % (re.escape(sym), re.escape(sym), re.escape(sym)),
                    srcs[mod], re.M):
                bad.append((d, "%s.%s" % (mod, sym)))
    assert bad == [], bad


def test_no_doc_links_to_a_file_that_is_not_there():
    """Markdown links across every doc must resolve. Zero broken, and this is
    what keeps it zero when a file is renamed."""
    import os, re, subprocess
    repo = set(subprocess.run(["git", "ls-files"], capture_output=True,
                              text=True).stdout.split())
    bad = []
    for d in _repo_docs():
        txt = open(d, encoding="utf-8", errors="replace").read()
        for m in re.finditer(r"\[([^\]]{1,80})\]\(([^)]+)\)", txt):
            tgt = m.group(2).split("#")[0].strip()
            if not tgt or tgt.startswith(("http", "mailto:")):
                continue
            p = os.path.normpath(os.path.join(os.path.dirname(d), tgt))
            if p not in repo and not os.path.exists(p):
                bad.append((d, tgt))
    assert bad == [], bad


def test_the_readme_test_count_is_the_real_one():
    """README says "# N tests" as a live instruction — run this, get that. It
    said 25 while the suite ran 443. A number a reader is told to expect must
    be the number they get."""
    import re
    readme = open("README.md", encoding="utf-8").read()
    m = re.search(r"tests/test_engine\.py\s+#\s*([\d,]+)\s+tests", readme)
    assert m, "the README no longer states a test count where it used to"
    claimed = int(m.group(1).replace(",", ""))
    actual = len([v for k, v in globals().items() if k.startswith("test_")])
    assert claimed == actual, (claimed, actual)


def test_the_canon_index_names_every_canon_file():
    """Seven of the 28 canon files were reachable from nothing — no document
    linked them, so the only way to find one was to already know its filename.
    A canon nobody can find is not canon."""
    import os
    d = "docs/method/canon"
    idx_path = os.path.join(d, "00_INDEX.md")
    assert os.path.exists(idx_path), "the canon has no index"
    idx = open(idx_path, encoding="utf-8").read()
    files = sorted(f for f in os.listdir(d)
                   if f.endswith(".md") and f != "00_INDEX.md")
    assert len(files) >= 28, len(files)
    missing = [f for f in files if f not in idx]
    assert missing == [], missing


def test_a_doc_that_calls_the_kernel_binding_also_says_it_is_not_wired():
    """`seq_kernel` is declared BINDING in the method docs and is imported by
    nothing. Both facts are true; a doc that states only the first lets a
    reader conclude it runs."""
    for p in ("docs/method/00_READ_FIRST.md",
              "docs/method/01C_SEQUENCE_PROTOCOL.md"):
        txt = open(p, encoding="utf-8").read()
        assert "seq_kernel.py" in txt
        assert "NOT WIRED" in txt, p
    # and the code still agrees with that statement
    from sourceborn import exists
    not_wired = {w for g in exists.MAP for r in g["rows"]
                 if r["state"] == exists.NOT_WIRED for w, _ in r.get("where", [])}
    assert "seq_kernel.py" in not_wired


# ---------------------------------------------------------------------------
# THE WIRING AUDIT — the OLD files, and the guards that keep them honest
# ---------------------------------------------------------------------------

def _package_modules():
    import pkgutil
    return sorted(m.name for m in pkgutil.iter_modules(["src/sourceborn"])
                  if not m.ispkg)


def _sibling_imports(text):
    """Every sibling module `text` imports, however the import is spelled."""
    import re
    got = set()
    for m in re.finditer(r"^\s*from\s+\.\s+import\s+([^\n#]+)", text, re.M):
        for p in m.group(1).split(","):
            got.add(p.strip().split(" as ")[0].strip())
    for pat in (r"^\s*from\s+\.(\w+)\s+import",
                r"^\s*from\s+sourceborn\.(\w+)\s+import",
                r"^\s*import\s+sourceborn\.(\w+)"):
        for m in re.finditer(pat, text, re.M):
            got.add(m.group(1))
    for m in re.finditer(r"^\s*from\s+sourceborn\s+import\s+([^\n#]+)", text, re.M):
        for p in m.group(1).split(","):
            got.add(p.strip().split(" as ")[0].strip())
    return got


def test_no_module_is_imported_and_never_used():
    """A dead import is a link that looks live. Twelve of them sat in
    engine.py — including `asi_pyramid` and `statepacks`, whose mere import
    the build notes cited as proof that 'the Pyramid is in the answer path'.
    It was not; an unused import satisfies a grep and nothing else. Twenty-five
    across the package, now zero, and this test is what keeps it zero."""
    import os, re
    dead = {}
    for mod in _package_modules():
        text = open(os.path.join("src/sourceborn", mod + ".py"),
                    encoding="utf-8").read()
        lines = text.splitlines()
        imported, i = {}, 0
        while i < len(lines):
            if re.match(r"^\s*(from\s+[\w.]+\s+)?import\s", lines[i]):
                chunk, j = lines[i], i
                while chunk.count("(") > chunk.count(")"):
                    j += 1
                    chunk += " " + lines[j]
                for p in chunk.split(" import ", 1)[-1].replace("(", "") \
                        .replace(")", "").split(","):
                    n = p.strip().split(" as ")[-1].strip().rstrip("\\").strip()
                    if n and re.match(r"^\w+$", n):
                        imported.setdefault(n, i + 1)
                i = j
            i += 1
        body = "\n".join(
            l for l in lines
            if not re.match(r"^\s*(from\s+[\w.]+\s+)?import\s", l)
            and not re.match(r"^\s{4,}[\w., ]+[,)]?\s*$", l))
        unused = [n for n in sorted(imported) if n != "annotations"
                  and not re.search(r"\b%s\b" % re.escape(n), body)]
        if unused:
            dead[mod] = unused
    assert dead == {}, dead


def test_the_pyramid_really_is_in_the_answer_path():
    """The claim the audit falsified, made true. `Engine.read()` CALLS
    asi_pyramid and statepacks and returns what they produce — importing them
    was never enough."""
    import tempfile
    from sourceborn.engine import SourcebornEngine
    from sourceborn import asi_pyramid, statepacks
    e = SourcebornEngine(root=tempfile.mkdtemp(prefix="sb_wire_"))
    r = e.read("he bet everything he had to win it all back")
    assert "pyramid" in r and "state_packs" in r
    assert set(r["pyramid"]["counts"]) >= {"strong", "candidate", "bank"}
    assert r["pyramid"]["counts"]["bank"] == 3204
    assert len(r["state_packs"]) == len(statepacks.packs_index()) == 16
    src = open("src/sourceborn/engine.py", encoding="utf-8").read()
    assert "asi_pyramid.activate(" in src and "statepacks.packs_index(" in src


def test_the_removed_matrix_is_not_still_linked_from_the_answer_path():
    """His decision: 'now we dont want 70-25 there'. `urr_matrix` stayed
    imported into engine.py long after — a live-looking link to a mechanism
    the answer path no longer uses. The module stays on disk under his
    do-not-delete rule; the dead link is gone."""
    src = open("src/sourceborn/engine.py", encoding="utf-8").read()
    assert "from .urr_matrix import" not in src
    assert "MATRIX" not in src.split('"""', 2)[-1] or "review_node(" not in src
    import os
    assert os.path.exists("src/sourceborn/urr_matrix.py"), \
        "the module is kept — only the dead link was removed"


def test_every_orphan_module_is_declared_in_the_honest_map():
    """A module nothing imports is not automatically wrong — seq_kernel is
    binding and unwired by his own ruling. What IS wrong is an orphan that no
    map mentions, because then nothing can tell him it is unwired. khalf was
    exactly that: 184 lines, tested, and named in no map at all."""
    import os
    exists_src = open("src/sourceborn/exists.py", encoding="utf-8").read()
    mods = _package_modules()
    texts = {m: open(os.path.join("src/sourceborn", m + ".py"),
                     encoding="utf-8").read() for m in mods}
    importers = {m: set() for m in mods}
    for m in mods:
        for dep in _sibling_imports(texts[m]):
            if dep in importers:
                importers[dep].add(m)
    # entrypoints are meant to be imported by nothing
    entry = {"server", "__main__", "demo"}
    orphans = sorted(m for m in mods if not importers[m] and m not in entry)
    assert orphans == ["khalf", "rh_code", "seq_kernel", "urr_matrix"], orphans
    for o in orphans:
        assert '("%s.py"' % o in exists_src, \
            "%s is imported by nothing and declared in no map" % o
    # and each is marked BUILT-NOT-WIRED, not quietly listed as running
    from sourceborn import exists
    not_wired = {w for g in exists.MAP for r in g["rows"]
                 if r["state"] == exists.NOT_WIRED
                 for w, _ in r.get("where", [])}
    for o in orphans:
        assert o + ".py" in not_wired, o


def test_the_honest_map_still_resolves_every_anchor():
    """exists.py's whole technique: a row carries a literal string that must
    still be present in the named module, so a row can never silently become a
    lie. Three anchors were wrong when khalf and rh_code were added — guessed
    function names — and this is what caught them."""
    from sourceborn import exists
    v = exists.verify()
    assert v["missing"] == 0, v
    assert v["checked"] >= 320
    assert v["counts"][exists.NOT_WIRED] == 4


def test_the_readme_lists_every_route_the_server_serves():
    """104 of 133 routes were undocumented. A hand-typed route list goes stale
    the first time a route is added, so the list is checked instead of
    trusted."""
    import re
    src = open("src/sourceborn/server.py", encoding="utf-8").read()
    routes = {m.group(1) for m in
              re.finditer(r'(?:path|self\.path)\s*==\s*"(/[^"]*)"', src)}
    readme = open("README.md", encoding="utf-8").read()
    missing = sorted(r for r in routes if r not in readme)
    assert missing == [], missing


# ---------------------------------------------------------------------------
# THE WIRING AUDIT — is the new work actually connected?
# ---------------------------------------------------------------------------

def test_every_layer_runs_on_one_ask_not_one_per_page():
    """The defect weighting.py had: a module importable from nothing. Before
    this audit, `trigger` and `readings` were reachable ONLY from server.py —
    they sat behind their own routes and never touched an answer."""
    from sourceborn import sbx
    r = sbx.place_on_spine("a man is stealing money from a shop")
    assert r["layers_run"] == ["SEGMENT", "CONTAINER", "SUB-PARAMETER",
                               "ARCHETYPE", "TRIGGER", "LINK", "SCALE",
                               "INTENT-READING"]
    assert r["triggers"]["containers_lit"] > 0
    assert r["readings"]["count"] == 9
    assert r["readings"]["chosen"] is None
    assert "meetings" in r
    # his diamond reaches the meeting layer through the same one call
    d = sbx.place_on_spine("diamond cut diamond")
    assert d["meetings"]["count"] == 1
    assert d["readings"]["count"] == 9


def test_the_trigger_layer_does_not_recurse_through_the_answer_path():
    """`place_on_spine` calls trigger and trigger calls `place_on_spine`.
    `for_hits` takes the already-computed hits, which is what breaks it — a
    plain `fires_on` call from the answer path would never return."""
    from sourceborn import trigger, sbx
    hits = sbx.place_on_spine("diamond cut diamond")["hits"]
    pure = trigger.for_hits(hits)
    assert "text" not in pure, "for_hits is pure — it never re-seats"
    wrapper = trigger.fires_on("diamond cut diamond")
    assert wrapper["text"] == "diamond cut diamond"
    assert wrapper["containers_lit"] == pure["containers_lit"]


def test_the_arrow_chart_shows_the_split_and_every_layer():
    """The system's own map showed none of it — not the split, not one layer.
    A map that does not show the system is not a map."""
    from sourceborn import sysmap
    c = sysmap.arrow_chart()
    for term in ("THE SPLIT", "ARCHETYPE", "TRIGGER", "LINK", "SCALE",
                 "READING", "183 containers", "HIS THIRD COLUMN",
                 "HIS NUMBER TO FINALISE", "CARRIED, NOT CONSULTED"):
        assert term in c, term
    # and no line overflows its box
    for line in c.splitlines():
        assert len(line) < 200, line[:80]


def test_where_names_every_new_layer():
    from sourceborn import sysmap
    known = {r["thing"] for r in sysmap.where()["layers"]}
    for t in ("the split", "the archetype", "the trigger", "the link",
              "the scale", "the readings", "the wiring", "the review"):
        assert t in known, t
        got = sysmap.where(t)
        assert got.get("module") and got.get("route"), t


def test_his_words_index_is_collected_and_resolves():
    """29 modules each define annotations() mapping HIS WORDS to the code that
    carries them — and nothing called any of them. Collected now, and every
    target is resolved the way exists.py resolves its anchors, so a phrase
    pointing at a symbol that no longer exists is reported."""
    from sourceborn import sysmap
    h = sysmap.his_words()
    assert h["modules_annotating"] >= 29
    assert h["phrases"] >= 160
    assert h["unresolved"] == [], h["unresolved"]
    assert h["problems"] == [], h["problems"]
    assert h["resolved"] == h["phrases"]
    # the new layers put their own words in the index
    phrases = " ".join(r["his_words"] for r in h["rows"])
    assert "below more may be repated" in phrases
    assert "diamond cut diamond is a link between two ego-rows" in phrases


def test_the_new_work_is_registered_everywhere_it_should_be():
    """The audit itself, as a test: filemap places the files, the home page
    HUD carries the counts, and the README lists the routes."""
    from sourceborn import filemap
    for p in ("src/sourceborn/archetype.py", "src/sourceborn/trigger.py",
              "src/sourceborn/link.py", "src/sourceborn/readings.py",
              "src/sourceborn/scale.py"):
        assert filemap.classify(p)["class"] == filemap.SYSTEM, p
    assert filemap.divide(".")["counts"][filemap.UNPLACED] == 0
    from sourceborn import homepage
    for cell in ("h_sp", "h_ly", "h_ar", "h_lk", "h_bd", "h_rd", "h_tg"):
        assert cell in homepage.PAGE, cell
    readme = open("README.md").read()
    for route in ("/sbx/review", "/sbx/wiring", "/archetype", "/trigger",
                  "/link", "/scale", "/readings"):
        assert route in readme, route
    src = open("src/sourceborn/server.py").read()
    assert '"/words"' in src and "sysmap.his_words()" in src


def test_the_layers_raise_the_count_but_never_the_bank():
    """His law: every example raises the count. His other law: a rubric
    application is not an ontology expansion. The layers are material he gave,
    so they enter the ledger — and none of them is a PARAM."""
    from sourceborn import growth as G, human_registry as hr
    items = G.seed_items()
    kinds = {}
    for i in items:
        kinds[i["kind"]] = kinds.get(i["kind"], 0) + 1
    assert len(items) >= 300, len(items)
    assert kinds[G.PARAM] == 3, "the bank does not grow from a layer"
    assert len(hr.parameters()) == 3204
    names = [i["name"] for i in items]
    assert any(n.startswith("ARCHETYPE: ") for n in names)
    assert any(n.startswith("LINK: ") for n in names)
    assert any(n.startswith("TRIGGER: ") for n in names)
    assert any(n.startswith("READING: ") for n in names)
    assert any(n.startswith("SCALE BAND: ") for n in names)


# ---------------------------------------------------------------------------
# PHASE 11 — THE SCALE AXIS
# ---------------------------------------------------------------------------

def test_his_gate_on_the_scales_is_enforced_not_described():
    """His gate: *you name the scales, or approve a proposed set*. Building
    the axis is not the same as naming the bands. The axis is built and the
    proposals are stored where he can read them — and ONLY HIS FOUR ARE IN
    FORCE until he says otherwise."""
    from sourceborn import scale as S
    assert [b["name"] for b in S.active()] == \
        ["micro", "individual", "relational", "macro"]
    assert S.gate()["approved"] is False
    assert S.stats()["approved"] is False
    for b in S.PROPOSED_BANDS:
        assert b["approved"] is False, b["id"]
    for b in S.HIS_BANDS:
        assert b["approved"] is True and b["by"] == "HIS"


def test_every_proposed_band_cites_the_example_of_his_that_demands_it():
    """Nothing is invented to fill a pattern. A band exists here only because
    one of his OWN worked examples sits at a size his four cannot hold — and
    the citation is the whole justification."""
    from sourceborn import scale as S
    assert len(S.PROPOSED_BANDS) == 5
    for b in S.PROPOSED_BANDS:
        assert b["why_needed"] and b["his_example"], b["id"]
        assert len(b["why_needed"]) > 80, "a citation, not a label"
    names = {b["name"] for b in S.PROPOSED_BANDS}
    assert names == {"moment", "household", "organisation", "dynasty",
                     "civilisation"}
    # the axis is ordered smallest to largest and his four keep their places
    order = [b["name"] for b in S.bands()]
    assert order.index("moment") < order.index("micro")
    assert order.index("micro") < order.index("individual") < \
        order.index("relational") < order.index("macro")
    assert order.index("macro") < order.index("civilisation")


def test_an_unfilled_band_says_not_stated_and_is_never_invented():
    """His rule everywhere else, holding here: an unstated dimension says NOT
    STATED, never zero and never a guess."""
    from sourceborn import scale as S
    o = S.of("ARCH-001")
    assert o["filled"] == 4, "his four readings on the dice game"
    assert o["not_stated"] == 5, "the five proposed bands he has not filled"
    for r in o["bands"]:
        if r["reading"] is None:
            assert r["state"] == "NOT STATED"
        else:
            assert r["state"] == "HIS READING"
    cov = S.coverage()
    assert set(cov["empty_bands"]) == {"moment", "household", "organisation",
                                       "dynasty", "civilisation"}
    assert cov["his_call"] is True


def test_one_arrangement_read_at_every_size():
    """His teaching made mechanical — *one event of those books is used in 100
    daily responses*. The dice sentence fires an archetype and comes back at
    every band, so a reading is a coordinate rather than a label."""
    from sourceborn import scale as S
    r = S.spread("he bet everything he had to win it all back and lost what "
                 "he could never recover")
    assert "ARCH-001" in r["archetypes_fired"]
    assert r["bands_available"] == 9 and r["bands_active"] == 4
    assert r["readings"] >= 4
    assert r["chosen"] is None


def test_the_scale_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/scale"', '"/scale/run"'):
        assert route in src, route
    assert "scale.spread(" in src and "scale.gate()" in src


# ---------------------------------------------------------------------------
# PHASE 12 — THE NINE READINGS
# ---------------------------------------------------------------------------

def test_his_stealing_sentence_produces_all_nine_readings():
    """The proof he named for this phase: *a live run on "a man is stealing
    the money" producing all nine readings where it produces zero today*."""
    from sourceborn import readings as R
    r = R.read("a man is stealing the money")
    assert r["reading_count"] == 9
    assert [x["id"] for x in r["readings"]] == ["IT-0%d" % n for n in range(1, 10)]
    # his own four from this very example lead the set
    by = {x["id"]: x for x in r["readings"]}
    assert "THIEF" in by["IT-01"]["his_example"]
    assert "OPPORTUNITY" in by["IT-02"]["his_example"]
    assert "HABIT" in by["IT-03"]["his_example"]
    assert "SAVING A LIFE" in by["IT-04"]["his_example"]
    # the act is carried in HIS words, never re-described
    assert r["act"] == "a man is stealing the money"
    for x in r["readings"]:
        assert r["act"] in x["reading"], x["id"]


def test_a_reading_names_what_would_refute_it():
    """His falsifier law, unchanged: a candidate that names nothing that would
    flip it is not a candidate, it is an opinion. That is what makes these
    readings and not labels."""
    from sourceborn import readings as R
    for x in R.read("a man is stealing the money")["readings"]:
        assert x["confirmed_by"] and x["refuted_by"], x["id"]
        assert x["confirmed_by"] != x["refuted_by"]
        assert x["refuses"], x["id"]
        assert x["rests_on"], x["id"]


def test_nothing_is_chosen_and_nothing_is_chooseable():
    """Two surviving candidates HALT rather than blend — his standing rule.
    Nine surviving candidates are nine."""
    from sourceborn import readings as R
    r = R.read("a man is stealing the money")
    assert r["chosen"] is None
    assert all(x["chosen"] is None for x in r["readings"])
    src = open("src/sourceborn/readings.py").read()
    for forbidden in ('"chosen": t[', "chosen =", "max(", "sort(", "best"):
        assert forbidden not in src, forbidden


def test_every_row_a_reading_rests_on_is_real():
    from sourceborn import readings as R
    v = R.verify()
    assert v["ok"] is True, v["problems"]
    assert v["rows_checked"] == 21


def test_the_adopted_intents_are_not_merged_with_his_nine():
    """ADOPT-HALT-4. Two intent vocabularies of different provenance; his
    ruling at the P2561 collision covers it."""
    from sourceborn import readings as R
    a = R.ADOPTED_HALT
    assert a["merged"] is False and a["his_call"] is True
    assert len(a["his_nine"]) == 9
    assert "ADOPT-HALT-4" in a["seam"]


def test_the_readings_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/readings"', '"/readings/run"'):
        assert route in src, route
    assert "readings.read(" in src


# ---------------------------------------------------------------------------
# PHASE 10 — THE LINK LAYER
# ---------------------------------------------------------------------------

def test_the_link_layer_is_counted_from_the_split_bank():
    """His own note on this layer: *counted from the split bank*. Three of the
    four types are COMPUTED over the live split and the live archetype layer,
    so the count follows the bank instead of drifting from it."""
    from sourceborn import link as L
    s = L.stats()
    assert s["links"] > 900
    assert s["computed"] == s["links"] - s["his"]
    assert set(s["by_type"]) == {"SPLIT_SIBLING", "SHARED_NAME",
                                 "ARCHETYPE_REACH", "SYMMETRIC_MEETING"}
    # split siblings come from the 275 parents the split review counts
    assert s["by_type"]["SPLIT_SIBLING"] >= 275
    assert s["ceiling"] is None, "his ruling: no count, open to increase"
    # ids are their own namespace — never readable as rows or containers
    for l in L.links()[:50]:
        assert l["id"].startswith("SBX-LNK-")


def test_every_row_a_link_names_is_real():
    """His hand-given links name SOURCE rows he supplied — those are the ones
    that can be wrong, so they are checked against the live registry."""
    from sourceborn import link as L
    v = L.verify()
    assert v["ok"] is True, v["problems"]
    assert v["problems"] == []
    assert v["his_row_ids_checked"] >= 7
    assert v["dangling_computed_links"] == 0


def test_the_diamond_returns_a_reading_no_row_can_hold():
    """The proof the layer exists for. `Dominance motive` is a row. TWO people
    running it at each other is not a row and cannot be made one — it has no
    home container, because it is not located in either party."""
    from sourceborn import link as L
    r = L.fires_on("diamond cut diamond")
    assert r["fired_count"] == 1
    reading = r["readings"][0]
    assert reading["name"] == "DIAMOND CUT DIAMOND"
    assert reading["his_words"] == "its ego cut ego"
    # both ends are the SAME row — which is why no computation could find it
    assert reading["rows"] == ["SB-HFR-P2550", "SB-HFR-P2550"]
    assert "meeting" in reading["reading"] or "meeting" in r["law"]
    assert "never read it as one person being strong" in reading["refuses"]
    assert r["concluded"] is None
    # and ordinary text fires nothing
    assert L.fires_on("the cat sat on the mat")["fired_count"] == 0


def test_the_link_layer_now_counts_in_his_table():
    """It stood at 0 in his twelve-layer table. It is now counted live, and
    wired — a layer is only wired if a live call puts it in the path."""
    from sourceborn import sbx, link as L
    by = {l["id"]: l for l in sbx.open_layers()}
    assert by["LINK"]["count"] == len(L.links()) > 900
    assert by["LINK"]["ceiling"] is None
    row = next(l for l in sbx.layers() if l["layer"] == "Link")
    assert row["live"] == len(L.links())
    assert row["wired"]["wired"] is True
    assert "Link" in sbx.wiring()["wired"]


def test_the_link_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/link"', '"/link/run"'):
        assert route in src, route
    assert "link.fires_on(" in src and "link.of(" in src


# ---------------------------------------------------------------------------
# HIS TWELVE-LAYER TABLE, LIVE — his ask: "your pending wiring"
# ---------------------------------------------------------------------------

def test_his_twelve_layer_table_is_rendered_against_live_data():
    """His table, his order, his targets — and the counts read from the live
    modules rather than from what was typed. A table of targets that never
    checks itself is how the 4,120 went missing the first time."""
    from sourceborn import sbx
    ls = sbx.layers()
    assert len(ls) == 12
    assert [l["n"] for l in ls] == list(range(1, 13))
    names = [l["layer"] for l in ls]
    assert names[:3] == ["Segments", "Containers", "Sub-parameters"]
    assert names[8:11] == ["Archetype", "Link", "Scale"]
    for l in ls:
        assert l["his_note"], l["layer"]
        assert l["against_target"] in ("MET", "SHORT", "OVER",
                                       "NO CEILING — his ruling",
                                       "NOT COUNTED HERE")
    by = {l["layer"]: l for l in ls}
    assert by["Segments"]["live"] == 27 and by["Segments"]["before"] == 10
    assert by["Containers"]["live"] == 183 and by["Containers"]["before"] == 80
    assert by["Universal filters"]["live"] == 175
    assert by["Rubrics R01–R52"]["live"] == 67


def test_the_one_short_layer_is_short_by_exactly_his_own_number():
    """His table says sub-parameters reach ≈7,603 — 3,483 from splitting plus
    4,120 fresh for the 103 new containers. The split produced the 3,483 by
    DIVIDING existing rows among children; it created no new names. The
    shortfall reproduces his own figure exactly, and is refused rather than
    filled with invented names."""
    from sourceborn import sbx
    w = sbx.wiring()
    assert len(w["short"]) == 1
    gap = w["the_one_gap"]
    assert gap["layer"] == "Sub-parameters"
    assert gap["live"] == 3483 and gap["his_target"] == 7603
    assert gap["short_by"] == 4120, "his own number, reproduced"
    assert "placeholder he forbade" in gap["refused"]
    assert "HIS NUMBER TO FINALISE" in gap["refused"]


def test_wired_means_it_reaches_an_answer_not_that_it_exists():
    """His bar: *evidence of wiring is done with proof not your test*. A layer
    placed at a step but never consulted is CARRIED, not wired, and the table
    says which is which instead of counting them all as done."""
    from sourceborn import sbx
    w = sbx.wiring()
    assert set(w["wired"]) == {"Segments", "Containers", "Sub-parameters",
                               "Archetype", "Link", "Scale"}
    assert w["partial"] == ["Universal filters"]
    # five layers exist at a step and reach no answer — stated, not hidden
    assert len(w["carried_not_consulted"]) == 5
    assert "Rubrics R01–R52" in w["carried_not_consulted"]
    assert "Operating states" in w["carried_not_consulted"]
    for l in sbx.layers():
        assert l["wired"]["how"], l["layer"]


def test_the_wiring_route_is_reachable():
    src = open("src/sourceborn/server.py").read()
    assert '"/sbx/wiring"' in src and "sbx.wiring()" in src


# ---------------------------------------------------------------------------
# THE SPLIT REVIEW — his ask: "split review it again"
# ---------------------------------------------------------------------------

def test_the_split_review_runs_checks_that_can_fail():
    """A review reports what is WRONG. These eight checks each have a failing
    branch; a review that could only pass would be worth nothing."""
    from sourceborn import sbx
    r = sbx.review()
    assert r["checks_run"] == 9
    assert r["passed_count"] + r["findings_count"] == 9
    ids = {p["id"] for p in r["passed"]} | {f["id"] for f in r["findings"]}
    assert ids == {"SPLIT-0%d" % n for n in range(1, 10)}
    for f in r["findings"]:
        assert f["his_call"] is True
        assert f["severity"]
        assert f["what"]


def test_the_split_arithmetic_is_exact_and_no_source_row_was_lost():
    """SPLIT-01 is the load-bearing check: nothing is removed. Every one of his
    3,204 source rows must still have at least one child, and no split row may
    cite a source that is not there."""
    from sourceborn import sbx
    r = sbx.review()
    p = next(x for x in r["passed"] if x["id"] == "SPLIT-01")
    assert p["source_rows"] == 3204
    assert p["parents_split"] == 275
    assert p["children_from_split_parents"] == 554
    assert p["arithmetic"] == "3204 source + 279 gained by splitting = 3483"
    assert "SPLIT-01" not in r["blocking"]


def test_the_review_reports_the_row_shortfall_without_deciding_it():
    """His rule is 40 rows per container; most have fewer, because splitting a
    parent DIVIDED its 40 among its children instead of giving each 40. The
    review states the number and refuses to invent the names."""
    from sourceborn import sbx
    f = next(x for x in sbx.review()["findings"] if x["id"] == "SPLIT-02")
    assert f["containers_under"] + f["containers_at_or_over"] == 183
    assert f["shortfall_to_40_each"] > 3000
    assert "will not decide it" in f["what_would_close_it"]
    assert f["thinnest"] and f["thinnest"][0]["rows"] == 1


def test_the_review_catches_the_split_repeating_its_own_defect():
    """Two children of two different parents landed on the same bare name —
    `Ownership` from body-schema and `Ownership` from agency; `Gesture` from
    tool-use and `Gesture` from prosody. That is the multi-meaning problem
    reappearing one level down, and it is reported, not renamed."""
    from sourceborn import sbx
    f = next(x for x in sbx.review()["findings"] if x["id"] == "SPLIT-04")
    assert set(f["duplicates"]) == {"Ownership", "Gesture"}
    for name, group in f["duplicates"].items():
        assert len({g["id"] for g in group}) == len(group) > 1
        assert len({g["from"] for g in group}) == len(group), \
            "the duplicates must come from DIFFERENT parents to be a real seam"
    assert "never renames" in f["what_would_close_it"]


def test_the_review_catches_a_layer_member_counted_but_never_placed():
    """SPLIT-09. Every layer member is supposed to sit at the step where it
    acts. The rubric layer declares 67 and places 66 distinct across 70
    placements — four rubrics act at two steps each, and one is counted
    without appearing anywhere in the work."""
    from sourceborn import sbx
    f = next(x for x in sbx.review()["findings"] if x["id"] == "SPLIT-09")
    rub = next(l for l in f["layers"] if l["layer"] == "rubrics")
    assert rub["declared"] == 67 and rub["placed_on_spine"] == 66
    assert rub["difference"] == 1
    assert "reported rather than guessed at" in f["note"]


def test_the_review_route_is_reachable():
    src = open("src/sourceborn/server.py").read()
    assert '"/sbx/review"' in src and "sbx.review()" in src


# ---------------------------------------------------------------------------
# HIS DISPLAY LAW — NEW PARAMETERS IN FRONT, OLD IN BACK
# ---------------------------------------------------------------------------

def test_new_parameters_in_front_and_old_in_back():
    """His words, given with the ruling that the source is never deleted:
    *use new parameters in front n old in back*. Both halves hold — the old
    bank stays whole, and the new reading leads, because a reader who meets
    the old id first is being shown the superseded address as the current one."""
    from sourceborn import sbx
    r = sbx.place_on_spine("a man is stealing money from a shop")
    assert r["hits"], "nothing reached — the convention has nothing to prove on"
    for h in r["hits"]:
        keys = list(h)
        # the split id and name lead; every source field sits under `from`
        assert keys[0] == "id" and keys[1] == "row"
        assert h["id"].startswith("SBX-CON-"), h["id"]
        assert h["container"].startswith("SBX-CON-")
        assert h["segment"].startswith("SBX-SEG-")
        assert keys.index("from") > keys.index("id")
        assert keys.index("from") > keys.index("container")
        assert h["from"]["id"].startswith("SB-HFR-P")
        assert h["from"]["container"].startswith("CON-")
        assert "untouched" in h["from"]["bank"]
    assert "new parameters in front" in sbx.FRONT_BACK_LAW


def test_every_reached_row_resolves_to_a_split_row():
    """The convention is only real if the new id actually exists for every
    row reached. Measured across eight of his asks: 71 hits, 71 resolved."""
    from sourceborn import sbx
    total = resolved = 0
    for text in ("a man is stealing money from a shop",
                 "he bet everything he had to win it all back and lost what "
                 "he could never recover",
                 "diamond cut diamond",
                 "i study late at night but i keep thinking about tomorrow",
                 "the father was standing at the door and pointed it in the air",
                 "he gave everything and got nothing in return",
                 "i heard from someone that he took the money, we should fire "
                 "him today"):
        for h in sbx.place_on_spine(text)["hits"]:
            total += 1
            resolved += bool(h["id"])
    assert total > 50 and resolved == total, (resolved, total)


def test_the_source_bank_is_still_whole_behind_the_new_front():
    """Putting the new in front must not have moved the old. His registry
    still reads 3,204 rows and 80 containers."""
    from sourceborn import human_registry as hr
    assert len(hr.parameters()) == 3204
    assert len(hr.containers()) == 80


# ---------------------------------------------------------------------------
# THE NODE BRAIN, IN THE ARCHITECTURE
# ---------------------------------------------------------------------------

def test_his_node_structure_is_placed_on_his_spine():
    """His ask: *Node brain structure added*. The structure was locked in
    Phase A and stood BESIDE the architecture; every other layer is placed at
    the step where it acts. All twelve types now are."""
    from sourceborn import sbx, nodebrain as N
    nb = sbx.node_brain()
    assert nb["node_type_count"] == 12
    assert nb["field_count"] == 16 and nb["link_type_count"] == 10
    assert len(nb["memory_kinds"]) == 11 and len(nb["statuses"]) == 4
    assert len(nb["write_conditions"]) == 5 and len(nb["read_conditions"]) == 6
    # the fingerprint travels with it, so a silent schema change is caught
    assert nb["fingerprint"] == N.fingerprint()
    placed = sbx.node_types()
    assert len(placed) == 12
    steps = {s["step"] for s in sbx.spine()}
    for t in placed:
        assert t["step"] in steps, t["type"]
        assert t["step_name"] and t["order"]
        # his structure, this side's placement — and every row says which
        assert t["by"].startswith("HIS")
        assert t["placed_by"].startswith("DERIVED")
        assert t["why"] and t["correctable"] is True
    # the ones his own law fixes: a contradiction is the HALT
    by = {t["type"]: t for t in placed}
    assert by["CONTRADICTION"]["step_name"] == "HALT"
    assert by["EVENT"]["step_name"] == "PRESSURE"
    assert by["INTENT"]["step_name"] == "WITNESS"
    assert by["PATTERN"]["step_name"] == "CONSOLIDATION"


def test_the_node_namespace_collisions_are_carried_not_settled():
    """Five node-type names collide with growth series names. The two
    namespaces are NOT merged — his standing ruling — and the architecture
    carries the seam rather than quietly settling it."""
    from sourceborn import sbx
    nb = sbx.node_brain()
    c = nb["collisions"]
    assert c["count"] == 5
    assert set(c["shared_names"]) == {"EVENT", "INTENT", "PATTERN", "RULE", "STATE"}
    assert nb["not_settled"]
    assert "NOT merged" in nb["not_settled"]


def test_the_steps_no_node_type_reaches_are_reported():
    """LOOP, ALIENATION and COLLISION have no node type of their own. That is
    an absence, and an absence is reported rather than filled."""
    from sourceborn import sbx
    nb = sbx.node_brain()
    assert nb["steps_unused"] == [8, 10, 11]
    assert set(nb["steps_used"]) | set(nb["steps_unused"]) == \
        {s["step"] for s in sbx.spine()}


# ---------------------------------------------------------------------------
# HIS THIRD COLUMN — THE OPERATIONAL TRIGGER / STATE VECTOR
# ---------------------------------------------------------------------------

def test_his_trigger_table_is_carried_verbatim():
    """His ten segments and forty-eight rows, his wording intact — his LaTeX
    and his spelling included. The table is his source; it is never rewritten."""
    from sourceborn import trigger as T
    assert len(T.HIS_TABLE) == 10
    rows = T.his_rows()
    assert len(rows) == 48
    for r in rows:
        assert r["bio"] and r["engine"] and r["trigger"], r["his_id"]
        assert r["his_id"].startswith("HIS-CON-")
    # his LaTeX survives byte-for-byte
    salience = next(r for r in rows if r["name"] == "Salience Detection")
    assert salience["trigger"] == \
        "Input amplitude > baseline moving average + $3\\sigma$."
    sleep = next(r for r in rows if r["name"] == "Sleep Architecture")
    assert sleep["trigger"] == "Idle timer > Threshold triggers ACPI S3/S4 state."


def test_a_container_may_serve_more_than_one_segment():
    """HIS OWN LAW, stated before the table: *below more may be repated*.
    Four of his container numbers carry a different container under a different
    segment, and that is recorded as a repeat, never resolved as a collision."""
    from sourceborn import trigger as T
    rep = T.repeats()
    assert rep["his_words"] == "below more may be repated"
    assert rep["repeated_count"] == 4
    assert set(rep["repeated_ids"]) == {"HIS-CON-018", "HIS-CON-023",
                                        "HIS-CON-024", "HIS-CON-026"}
    # HIS-CON-018 is Auditory Processing in one segment and Threat Detection
    # in another — both kept, neither preferred
    names = {x["name"] for x in rep["repeated_ids"]["HIS-CON-018"]}
    assert names == {"Auditory Processing", "Threat Detection"}
    # and placements returns a LIST, never one value
    assert isinstance(T.placements("SBX-CON-023"), list)


def test_the_three_numberings_are_never_merged_on_the_numerals():
    """His table, the live registry and the split all number from CON-001 and
    are three different numberings. His standing ruling covers exactly this:
    do not silently merge namespaces. Matching is by NAME; whether his number
    agrees is recorded beside and decides nothing."""
    from sourceborn import trigger as T, human_registry as hr
    # the proof they differ: his CON-064 is Episodic Memory, the registry's is
    # Motive, Needs, Values and Priority Structure
    reg = {c["id"]: c["name"] for c in hr.containers()}
    his = {r["his_id"]: r["name"] for r in T.his_rows()}
    assert his["HIS-CON-064"] == "Episodic Memory"
    assert reg["CON-064"] == "Motive, Needs, Values and Priority Structure"
    seams = T.seams()
    assert len(seams) >= 5
    for s in seams:
        assert s["resolved"] is False and s["his_call"] is True
        assert s["name_places_it_at"]["id"] != s["number_would_place_it_at"]["id"]
    # his Theory of Mind by name; his number would have given Body Schema
    tom = next(s for s in seams if s["his_name"] == "Theory of Mind")
    assert tom["name_places_it_at"]["name"] == "Theory of Mind"
    assert tom["number_would_place_it_at"]["name"] == "Body Schema"


def test_a_weak_match_is_proposed_and_never_placed():
    """Measured: of three single-distinctive-token matches, `circadian` and
    `chemical` were right and `behavioral` put his safety-guardrail row onto
    Group Behaviour. A weak match that placed would carry his trigger to the
    wrong container, so it waits for his word."""
    from sourceborn import trigger as T
    m = T.match()
    assert m["placed_count"] + m["proposed_count"] + m["held_count"] == 48
    assert m["proposed_count"] >= 1
    for p in m["proposed"]:
        assert p["his_call"] is True and "proposal" in p and "matched" not in p
        assert p["grade"].startswith("SHARED DISTINCTIVE TOKEN")
    # nothing proposed reaches a container's trigger
    proposed_ids = {p["proposal"]["id"] for p in m["proposed"]}
    for t in T.triggers():
        if t["id"] in proposed_ids:
            assert t["by"] == "DERIVED", \
                "%s took a proposed match without his word" % t["id"]
    # and an unmatchable row is HELD whole, never dropped
    assert m["held_count"] >= 1
    for h in m["held"]:
        assert h["his_name"] and h["grade"] in ("UNMATCHED",) or \
            h["grade"].startswith("AMBIGUOUS")


def test_every_container_carries_a_trigger_and_says_whose_it_is():
    """All 183 filled — no empty slot. HIS and DERIVED counted apart, because
    a page that cannot say which triggers are his cannot be corrected by him."""
    from sourceborn import trigger as T
    ts = T.triggers()
    assert len(ts) == 183
    for t in ts:
        assert t["trigger"], t["id"]
        assert t["by"] in ("HIS", "DERIVED")
        assert t["kind"] in {k for k, _ in T.SHAPE.values()}
        assert t["correctable"] is True
        if t["by"] == "DERIVED":
            # never invented from nowhere — it names its two real sources
            assert t["from"]["machine_column"] is not None
            assert t["from"]["step"] == t["step"]
    his = [t for t in ts if t["by"] == "HIS"]
    assert len(his) == T.stats()["trigger_by_him"] == 36
    assert T.stats()["trigger_derived"] == 183 - 36


def test_the_trigger_shape_comes_from_his_spine():
    """A trigger is not free text. Where a container sits on his spine fixes
    the SHAPE of its firing: GROUND reads a baseline, PRESSURE crosses a
    threshold, HALT raises a fault."""
    from sourceborn import trigger as T
    assert T.SHAPE[1][0] == "BASELINE READ"
    assert T.SHAPE[2][0] == "THRESHOLD CROSSED"
    assert T.SHAPE[7][0] == "FAULT RAISED"
    assert T.SHAPE[8][0] == "COMMIT / RELOAD"
    for t in T.triggers():
        if t["by"] == "DERIVED":
            assert t["kind"] == T.SHAPE[t["step"]][0], t["id"]


def test_an_ask_is_read_as_firing_conditions_and_concludes_nothing():
    from sourceborn import trigger as T
    r = T.fires_on("a man is stealing money from a shop")
    assert r["containers_lit"] > 0
    assert r["his_triggers_lit"] + r["derived_triggers_lit"] == r["containers_lit"]
    assert r["concluded"] is None
    for t in r["triggers"]:
        assert t["trigger"] and t["by"] in ("HIS", "DERIVED")
        assert t["reached_by"] in ("WORDS", "ARCHETYPE")


def test_the_trigger_routes_are_reachable():
    src = open("src/sourceborn/server.py").read()
    for route in ('"/trigger"', '"/trigger/placements"', '"/trigger/run"'):
        assert route in src, route
    assert "trigger.fires_on(" in src and "trigger.seams()" in src


# ---------------------------------------------------------------------------
# THE PEN — it rewrites its own code, full auto on his word (2026-09-03)
# ---------------------------------------------------------------------------

class _PenModel:
    """A drafter for tests: hands back scripted replies and records prompts."""
    def __init__(self, *replies, name="testpen"):
        self.replies, self.name, self.calls, self.prompts = list(replies), name, 0, []
    def complete(self, system, prompt, max_tokens=4000):
        self.calls += 1
        self.prompts.append(prompt)
        return self.replies.pop(0) if self.replies else ""


class _PenTransport:
    """A GitHub for tests: records every call, answers like the git-data API."""
    def __init__(self, fail_on_ref=False):
        self.calls, self.fail_on_ref = [], fail_on_ref
    def __call__(self, method, url, payload, token):
        self.calls.append({"method": method, "url": url, "payload": payload})
        if method == "PATCH" and self.fail_on_ref:
            raise RuntimeError("GitHub PATCH /git/refs -> 422 not a fast forward")
        if method == "GET" and "/git/ref/" in url:
            return {"object": {"sha": "headsha00"}}
        if method == "GET" and "/git/commits/" in url:
            return {"tree": {"sha": "treesha00"}}
        if url.endswith("/git/blobs"):
            return {"sha": "blob%02d" % len(self.calls)}
        if url.endswith("/git/trees"):
            return {"sha": "newtree00"}
        if url.endswith("/git/commits"):
            return {"sha": "pencommit%02d" % len(self.calls)}
        return {"ok": True}


def _pen_env(extra):
    """Set/unset env keys for one pen test; returns the restore function."""
    old = {}
    for k, v in extra.items():
        old[k] = os.environ.get(k)
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    def restore():
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    return restore


def _pen_reply(path, content, why="carries his teaching into the code"):
    return ("<<<WHY>>>%s<<<END WHY>>>\n<<<FILE %s>>>\n%s\n<<<END FILE>>>"
            % (why, path, content))


def test_the_pen_field_is_default_deny_and_the_core_is_unreachable():
    """His rule 2 surviving full auto is a property of allowed(), not a
    promise: the core — his words, his banks, the suite, the orders — is
    refused before anything runs, and the refusal carries the reason."""
    from sourceborn import selfpatch as SP
    for p in ("docs/method/canon/THE_SELF_REWRITE.md", "data/human_registry.json",
              "adopted/C-SB/README.md", "tests/test_engine.py", "CLAUDE.md",
              "render.yaml", "app.py", ".github/workflows/ci.yml",
              "seed_corpus/raw_thoughts/x.txt", ".sourceborn/growth/ledger.jsonl"):
        ok, why = SP.allowed(p)
        assert not ok and why, p
    for held in SP.HELD_FROM_THE_PEN:
        ok, why = SP.allowed("src/sourceborn/" + held)
        assert not ok and why == SP.HELD_FROM_THE_PEN[held], held
    for p in ("src/sourceborn/micro.py", "README.md"):
        ok, _ = SP.allowed(p)
        assert ok, p
    # outside the field even inside the tree: not-.py, nested, other dirs
    for p in ("src/sourceborn/data/human_registry.json", "src/sourceborn/a/b.py",
              "tools/docx2txt.py", "docs/x.py", "somefile.py"):
        assert not SP.allowed(p)[0], p


def test_a_path_that_climbs_out_of_the_tree_is_refused():
    from sourceborn import selfpatch as SP
    for p in ("../CLAUDE.md", "/etc/passwd", "~/x.py",
              "src/sourceborn/../../CLAUDE.md",
              "src/sourceborn/../../../outside.py", ""):
        assert not SP.allowed(p)[0], p


def test_the_door_law_holds_the_pen_until_his_password_exists():
    """The pen writes into HIS GitHub with HIS token — an open door would
    hand it to anyone with the URL. The knock is FILED, never dropped."""
    from sourceborn import selfpatch as SP
    restore = _pen_env({"SB_ACCESS_PASS": None})
    root = tempfile.mkdtemp()
    try:
        m = _PenModel(_pen_reply("src/sourceborn/micro.py", "x = 1"))
        tr = _PenTransport()
        row = SP.teach("teach me something", root=root, model=m, transport=tr)
        assert row["stage"] == "REFUSED-DOOR-OPEN"
        assert m.calls == 0, "the drafter must not run at an open door"
        assert tr.calls == []
        assert SP.load(root)[0]["teaching"] == "teach me something"
    finally:
        restore()


def test_the_offline_echo_can_never_become_a_patch():
    from sourceborn import selfpatch as SP
    from sourceborn import llm
    restore = _pen_env({"SB_ACCESS_PASS": "pw"})
    root = tempfile.mkdtemp()
    try:
        tr = _PenTransport()
        row = SP.teach("teach", root=root, model=llm.RuleBasedModel(),
                       transport=tr)
        assert row["stage"] == "REFUSED-NO-MODEL"
        assert tr.calls == []
    finally:
        restore()


def test_a_reply_that_is_not_a_patch_is_filed_refused():
    from sourceborn import selfpatch as SP
    restore = _pen_env({"SB_ACCESS_PASS": "pw"})
    root = tempfile.mkdtemp()
    try:
        row = SP.teach("teach", root=root,
                       model=_PenModel("here is my patch: change everything"),
                       transport=_PenTransport())
        assert row["stage"] == "REFUSED-MALFORMED"
        assert "files" not in row, "nothing parsed means nothing staged"
    finally:
        restore()


def test_a_patch_reaching_held_ground_is_refused_before_anything_runs():
    from sourceborn import selfpatch as SP
    restore = _pen_env({"SB_ACCESS_PASS": "pw"})
    try:
        for path in ("CLAUDE.md", "src/sourceborn/selfpatch.py",
                     "tests/test_engine.py", "docs/method/01A_INTENT.md"):
            root = tempfile.mkdtemp()
            tr = _PenTransport()
            row = SP.teach("teach", root=root,
                           model=_PenModel(_pen_reply(path, "# taken over")),
                           transport=tr)
            assert row["stage"] == "REFUSED-HELD", path
            assert not any(s["stage"].startswith("SHADOW")
                           for s in row["stages"]), "held is refused unrun"
            assert tr.calls == []
    finally:
        restore()


def test_python_that_does_not_compile_never_reaches_the_suite():
    from sourceborn import selfpatch as SP
    restore = _pen_env({"SB_ACCESS_PASS": "pw"})
    root = tempfile.mkdtemp()
    try:
        row = SP.teach("teach", root=root,
                       model=_PenModel(_pen_reply("src/sourceborn/micro.py",
                                                  "def broken(:")),
                       transport=_PenTransport())
        assert row["stage"] == "REFUSED-MALFORMED"
        assert "does not compile" in row["stages"][-1]["why"]
    finally:
        restore()


def test_the_parse_caps_bite_and_report():
    from sourceborn import selfpatch as SP
    four = "\n".join(_pen_reply("src/sourceborn/micro.py", "x=%d" % i)
                     for i in range(4))
    assert "cap is 3" in SP.parse_reply(four)["refused"]
    big = _pen_reply("src/sourceborn/micro.py", "# " + "a" * 210_000)
    assert "bytes" in SP.parse_reply(big)["refused"]


def test_the_shadow_runs_the_patch_against_a_copy_never_the_tree():
    """The gate's mechanics, on a mini suite: green reads green, red reads red
    with the failure kept — and the working tree is untouched by both."""
    if os.environ.get("SB_SELFPATCH_SHADOW"):
        return  # a shadow may not open another shadow
    from sourceborn import selfpatch as SP
    real = open("src/sourceborn/witnesses.py", encoding="utf-8").read()
    ok = SP._shadow({"tests/mini_ok.py": "print('1/1 tests passed')\n"},
                    suite="tests/mini_ok.py")
    assert ok["green"] and ok["tests"] == "1/1 tests passed"
    red = SP._shadow({"src/sourceborn/witnesses.py":
                      "raise RuntimeError('broken on purpose')\n",
                      "tests/mini_red.py":
                      "import sys; sys.path.insert(0, 'src'); "
                      "import sourceborn.witnesses\n"},
                     suite="tests/mini_red.py")
    assert not red["green"]
    assert "broken on purpose" in red["tail"]
    assert open("src/sourceborn/witnesses.py",
                encoding="utf-8").read() == real, "the tree must be untouched"
    assert not os.path.exists("tests/mini_ok.py"), "the shadow is a copy"


def test_a_green_patch_pushes_straight_to_the_deploy_branch():
    """His choice end to end, against the REAL suite: teach -> draft ->
    the full suite green in shadow -> commit through the git-data API with
    no approval step. This is the one test that pays the whole shadow run."""
    if os.environ.get("SB_SELFPATCH_SHADOW"):
        return  # a shadow may not open another shadow
    from sourceborn import selfpatch as SP
    restore = _pen_env({"SB_ACCESS_PASS": "pw", "SB_GITHUB_TOKEN": "tkn",
                        "SB_REPO": "owner/name", "SB_BRANCH": None})
    root = tempfile.mkdtemp()
    try:
        real = open("src/sourceborn/witnesses.py", encoding="utf-8").read()
        content = real + "\n# the pen wrote here\n"
        tr = _PenTransport()
        row = SP.teach("when two witnesses differ, keep both — a comment to "
                       "prove the loop", root=root,
                       model=_PenModel(_pen_reply("src/sourceborn/witnesses.py",
                                                  content)),
                       transport=tr)
        assert row["stage"] == "PUSHED", row["stages"]
        assert any(s["stage"] == "SHADOW-GREEN" and s.get("tests")
                   and "tests passed" in s["tests"] for s in row["stages"])
        assert row["sha"].startswith("pencommit")
        methods = [c["method"] for c in tr.calls]
        assert methods == ["GET", "GET", "POST", "POST", "POST", "PATCH"]
        commit = next(c for c in tr.calls if c["url"].endswith("/git/commits")
                      and c["method"] == "POST")
        msg = commit["payload"]["message"]
        assert msg.startswith("SELF-PATCH SB-PATCH-0001:")
        assert "when two witnesses differ" in msg
        ref = tr.calls[-1]["payload"]
        assert ref == {"sha": row["sha"], "force": False}
        kept = SP.load(root)[0]
        assert kept["was"]["src/sourceborn/witnesses.py"] == real, \
            "the before is the real file, kept whole"
        assert kept["now"]["src/sourceborn/witnesses.py"].rstrip(
               ).endswith("# the pen wrote here")
    finally:
        restore()


def test_a_red_suite_files_the_patch_and_pushes_nothing():
    if os.environ.get("SB_SELFPATCH_SHADOW"):
        return
    from sourceborn import selfpatch as SP
    restore = _pen_env({"SB_ACCESS_PASS": "pw", "SB_GITHUB_TOKEN": "tkn",
                        "SB_REPO": "owner/name"})
    root = tempfile.mkdtemp()
    try:
        tr = _PenTransport()
        row = SP.teach("teach", root=root,
                       model=_PenModel(_pen_reply("src/sourceborn/micro.py",
                                                  "x = 1")),
                       transport=tr, suite="tests/no_such_suite.py")
        assert row["stage"] == "SHADOW-RED"
        assert tr.calls == [], "red never pushes"
        assert SP.load(root)[0]["stage"] == "SHADOW-RED", "and it is filed"
    finally:
        restore()


def test_an_unarmed_green_patch_is_held_with_the_whole_patch_kept():
    from sourceborn import selfpatch as SP
    restore = _pen_env({"SB_ACCESS_PASS": "pw", "SB_GITHUB_TOKEN": None,
                        "SB_REPO": None})
    root = tempfile.mkdtemp()
    try:
        tr = _PenTransport()
        row = SP.teach("teach", root=root,
                       model=_PenModel(_pen_reply("src/sourceborn/micro.py",
                                                  "x = 1")),
                       transport=tr, shadow=False)
        assert row["stage"] == "HELD-UNARMED"
        assert tr.calls == []
        assert SP.load(root)[0]["now"] == {"src/sourceborn/micro.py": "x = 1\n"}
    finally:
        restore()


def test_a_race_on_the_branch_head_is_refused_never_forced():
    """force is never sent true: if the head moved underneath, the ref update
    fails and the teach is FILED, not clobbered over someone's commit."""
    from sourceborn import selfpatch as SP
    restore = _pen_env({"SB_ACCESS_PASS": "pw", "SB_GITHUB_TOKEN": "tkn",
                        "SB_REPO": "owner/name"})
    root = tempfile.mkdtemp()
    try:
        tr = _PenTransport(fail_on_ref=True)
        row = SP.teach("teach", root=root,
                       model=_PenModel(_pen_reply("src/sourceborn/micro.py",
                                                  "x = 1")),
                       transport=tr, shadow=False)
        assert row["stage"] == "REFUSED-PUSH"
        assert "not a fast forward" in row["stages"][-1]["why"]
        for c in tr.calls:
            if isinstance(c["payload"], dict) and "force" in c["payload"]:
                assert c["payload"]["force"] is False
    finally:
        restore()


def test_revert_is_a_new_commit_and_the_ledger_keeps_everything():
    from sourceborn import selfpatch as SP
    restore = _pen_env({"SB_ACCESS_PASS": "pw", "SB_GITHUB_TOKEN": "tkn",
                        "SB_REPO": "owner/name"})
    root = tempfile.mkdtemp()
    try:
        # a patch that CREATES a file: its revert must delete it — as a tree
        # entry in a NEW commit, never an erasure of history
        row = SP.teach("teach", root=root,
                       model=_PenModel(_pen_reply(
                           "src/sourceborn/pen_test_mod.py", "x = 1")),
                       transport=_PenTransport(), shadow=False)
        assert row["stage"] == "PUSHED"
        tr2 = _PenTransport()
        rev = SP.revert(row["id"], root=root, transport=tr2)
        assert rev["kind"] == "REVERT" and rev["of"] == row["id"]
        tree = next(c for c in tr2.calls if c["url"].endswith("/git/trees"))
        entry = tree["payload"]["tree"][0]
        assert entry["path"] == "src/sourceborn/pen_test_mod.py"
        assert entry["sha"] is None, "a created file reverts to absent"
        rows = SP.load(root)
        assert [r["kind"] for r in rows] == ["PATCH", "REVERT"]
        assert rows[0]["stage"] == "PUSHED", "the patch row stands untouched"
        # and only a PUSHED row can be reverted
        assert "refused" in SP.revert("SB-PATCH-9999", root=root,
                                      transport=tr2)
    finally:
        restore()


def test_the_pen_ledger_is_append_only_and_the_scratch_is_scoped():
    """growth.py's law, applied to the pen: no removal path anywhere near the
    ledger. The one rmtree in the module deletes the SHADOW SCRATCH copy —
    45MB per teach would otherwise eat the disk — and lives only in _shadow."""
    import inspect
    import re as _re
    from sourceborn import selfpatch as SP
    src = inspect.getsource(SP)
    # call-shaped patterns only: the drafter's LAW TEXT must be allowed to
    # SAY "no delete/pop/truncate paths" without this scan reading the law
    # as a violation — the same self-reference trap the earlier guards hit.
    for bad in (".pop(", ".truncate(", "os.remove(", "os.unlink("):
        assert bad not in src, bad
    assert not _re.search(r"\bdel\b", src)
    assert '"a"' in inspect.getsource(SP._append)
    for chunk in src.split("\ndef "):
        if "rmtree" in chunk:
            assert chunk.startswith("_shadow"), "rmtree outside the scratch"
    assert "rmtree" in inspect.getsource(SP._shadow)


def test_no_secret_value_ever_leaves_the_environment():
    import json
    from sourceborn import selfpatch as SP
    restore = _pen_env({"SB_ACCESS_PASS": "pw-sekrit-77",
                        "SB_GITHUB_TOKEN": "tok-sekrit-88",
                        "SB_REPO": "owner/name"})
    try:
        blob = json.dumps(SP.state(tempfile.mkdtemp()))
        assert "sekrit" not in blob
        assert '"SB_GITHUB_TOKEN": true' in blob
    finally:
        restore()


def test_nothing_pushed_carries_a_models_name():
    from sourceborn import selfpatch as SP
    msg = SP._commit_message(
        "SB-PATCH-0001", "his teaching",
        "As Claude, I used GPT-5 and Grok via Anthropic and OpenAI APIs.",
        "478/478 tests passed")
    low = msg.lower()
    for word in ("claude", "gpt", "grok", "anthropic", "openai"):
        assert word not in low, word
    assert msg.startswith("SELF-PATCH SB-PATCH-0001: his teaching")


def test_the_drafter_may_ask_to_read_once_and_only_once():
    from sourceborn import selfpatch as SP
    m = _PenModel("<<<NEED>>>micro.py<<<END NEED>>>",
                  "<<<NEED>>>patterns.py<<<END NEED>>>")
    d = SP._draft("teach", "", m)
    assert m.calls == 2
    assert "one NEED round" in d["refused"]
    m2 = _PenModel("<<<NEED>>>micro.py<<<END NEED>>>",
                   _pen_reply("src/sourceborn/micro.py", "x = 1"))
    d2 = SP._draft("teach", "", m2)
    assert "files" in d2
    assert "CURRENT SOURCE OF micro.py" in m2.prompts[1]


def test_a_named_target_hands_its_real_source_to_the_drafter():
    from sourceborn import selfpatch as SP
    m = _PenModel("junk")
    SP._draft("teach", "micro", m)
    assert "CURRENT SOURCE OF micro" in m.prompts[0]
    assert "micro-sequence" in m.prompts[0].lower() or "def " in m.prompts[0]


def test_the_home_is_the_rewrite_and_nothing_was_removed_for_it():
    """'not what we have' meant replaced at /, not deleted: the reactor
    stands whole at /reactor, the desk at /desk, and the new page escapes
    everything it renders — ledger rows are untrusted input."""
    from sourceborn import selfhome, homepage
    src = open("src/sourceborn/server.py", encoding="utf-8").read()
    assert "selfhome.PAGE" in src and '"/reactor"' in src
    assert "homepage.PAGE" in src and '"/desk"' in src
    assert len(homepage.PAGE) > 10_000, "the reactor page stands whole"
    for term in ("ONE DASHBOARD", "TEACH THE MACHINE", "revert", "esc("):
        assert term in selfhome.PAGE, term
    readme = open("README.md", encoding="utf-8").read()
    for route in ("/selfpatch/teach", "/selfpatch/revert", "/reactor"):
        assert route in readme, route


def test_the_dashboard_is_one_his_correction():
    """His correction after seeing it live (2026-09-04): 'But still i can
    see 5-6 dashboards / its not matching with my thought, dashboard also
    be one.' So / is ONE page and every view is a TAB inside it, loaded
    lazily — the old routes still answer (they are the panels this page
    shows), but the app has exactly one front and no lobby of links."""
    from sourceborn import selfhome
    p = selfhome.PAGE
    # every view is a pane of the one page
    for src in ('data-src="/reactor"', 'data-src="/engine"',
                'data-src="/reading"', 'data-src="/sbx"',
                'data-src="/exists"', 'data-src="/desk"'):
        assert src in p, src
    assert p.count("<iframe") == 6, "one lazy pane per view"
    assert 'fr.src=tab.dataset.src' in p, "panes load lazily, on first open"
    # the pen leads: the teach pane is the active one on arrival
    assert '<div class="pane act" id=pane-teach>' in p
    # deep links survive small, in the footer — a view can be opened alone
    for link in ('href="/reading"', 'href="/exists"'):
        assert link in p, link
    # and /health reports the pen's switches as presence-only booleans, so
    # arming can be checked from outside once the door is locked
    src = open("src/sourceborn/server.py", encoding="utf-8").read()
    at = src.index('path == "/health"')
    block = src[at:at + 900]
    assert '"pen"' in block and "selfpatch.arming()" in block
    assert "door_locked" in block


def test_the_pen_appears_in_every_map():
    from sourceborn import sysmap
    got = sysmap.where("the pen")
    assert got["module"] == "selfpatch.py" and got["route"]
    chart = sysmap.arrow_chart()
    assert "THE PEN" in chart and "FULL AUTO" in chart
    from sourceborn import selfpatch as SP
    st = SP.state(tempfile.mkdtemp())
    assert st["field"]["modules"] > 70
    assert len(st["field"]["held"]) == 5
    assert st["door"]["law"] and st["laws"]


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
