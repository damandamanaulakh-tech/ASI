"""THE ADOPTION FROM C-SB — what the sibling holds that this core did not.

His word (2026-08-24, verbatim in the custody manifest):

    "just adopt what is not here, do not touch and change anything in the
     C-SB repo / n lay off ur brain / just work under ASI instructions
     vague, big picture, anything if u tweak, ask me first"

WHAT ADOPTION MEANS HERE, AND WHAT IT DOES NOT

42 files were copied BYTE-IDENTICAL from damandamanaulakh-tech/C-SB at
commit 9e3f179 into `adopted/C-SB/<original path>`, each with its SHA-256
recorded in `adopted/C-SB/ADOPTION_CUSTODY.json`. C-SB itself was not
touched — its working tree was verified clean after the copy.

This module READS the adopted material and exposes it. It interprets
nothing, renames nothing, and wires nothing into the engine's behavior:
seating, the runtime, the combine engine, the graph and the scheduler all
run exactly as before this file existed, and the test suite pins that.
Every place where the adopted material MEETS this core's material — same
numbers in different namespaces, same words for different things — is a
HALT addressed to him, not a decision made here. `halts()` is that list.

WHAT WAS ADOPTED (all verbatim, statuses preserved as C-SB states them):

  LAW        the Real-Time ASI Constitution V1, the Growing-Phase
             Constitution V1, the 30 LOCKED DECISIONS (SEQ-LOCK-001..030),
             the system invariants contract, the EVENT-INTENT GROWTH
             CONTRACT with its 8 typed intents
  BANKS      AI-only 64 approved records + AI rubric · the 75-engine
             library + segment bindings · operational containers 161-240
             (80 records) + operational sub-parameters 2593-3072 · the
             expansion band P2561-P2592 (32 records, ASI-Brain workbook
             namespace) · the native 2,560 registry + its 4 compressed
             custody parts · the container index 80 materialization
  NODES      the 22-node ASI service registry (ASI-NODE-00..21), the
             node-brain template, NODE_BRAINS_18_21
  RUBRICS    the machine rubric registry R01-R52
  WISDOM     the whole holy-book pipeline: BG 2.47-2.50 source, claims,
             interpretations, counter-cases, candidates, wisdom objects,
             the source-to-wisdom contract, the wisdom registry, the
             narrative adapter schema, the Mahabharata batch + contract
  EXAMPLES   his raw words as C-SB holds them: the ORIGINAL rain source,
             the father-door 3204 run, the source-sovereignty filter
  V2         the five v2 lock CANDIDATES (kept as candidates — C-SB has
             not locked them and neither does this)

WHAT WAS DELIBERATELY NOT ADOPTED (already here, or C-SB's own history):
the 3,204 functional registry (this core's live bank IS that registry);
C-SB's generated indexes and rebuild tools (they rebuild C-SB's tree, not
this one); C-SB's checkpoints, closures and RFR history (its own proof
record — mirroring it wholesale is a decision for him, HALT-7).

THE SECOND ADOPTION (2026-08-27) — THE SB-ASI DRIVE MASTER WORKBOOK

His word: "this file too for review and adoption". The file:
ASI-Brain_Task3_Approved_Final_v1_0 — the SB-ASI Google Drive project's
final Task-3 master (33 sheets; Task 2 approved on his word "brain
approved", Task 3 approved, Tasks 4-5 blocked by his gates). It lives at
`adopted/SB-ASI-Drive/` — the .xlsx byte-identical, plus a DERIVED
tab-separated text file per sheet so the binary is reviewable in the
repo (mechanical extraction; on any disagreement the .xlsx wins), all
SHA-256'd in that tree's own ADOPTION_CUSTODY.json.

The load-bearing content, read not interpreted: the workbook states in
writing how his two banks relate — ASI_Claude_Parameters.docx supplied
3,204 names; 2,554 were carried into the 2,560 baseline, 650 held in a
named reserve (2,554 + 650 = 3,204), and 6 rows were visibly added to
complete Core Reasoning's target of 48 (2,554 + 6 = 2,560), each marked
REQUIRES USER APPROVAL. `the_bridge()` COUNTS this from the file rather
than repeating it. `wb_findings()` carries what the review caught,
corrected nowhere; `wb_halts()` carries the new seams (ADOPT-HALT-8..12),
decided by nobody here.
"""

from __future__ import annotations

import hashlib
import json
import os

ORIGIN = "damandamanaulakh-tech/C-SB"
ORIGIN_COMMIT = "9e3f179190824248ce657097c70e3c7bf7c6ade6"


def _root(repo: str = ".") -> str:
    return os.path.join(repo, "adopted", "C-SB")


def custody(repo: str = ".") -> dict:
    p = os.path.join(_root(repo), "ADOPTION_CUSTODY.json")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def _read(repo: str, rel: str):
    p = os.path.join(_root(repo), rel)
    with open(p, "r", encoding="utf-8") as f:
        if rel.endswith(".json"):
            return json.load(f)
        return f.read()


def verify(repo: str = ".") -> dict:
    """Re-hash every adopted file against the custody manifest.

    The C-SB technique (source custody by SHA) applied to the adoption
    itself: a byte that drifts is NAMED, never silently accepted."""
    c = custody(repo)
    ok, bad, missing = [], [], []
    for f in c["files"]:
        p = os.path.join(_root(repo), f["path"])
        if not os.path.exists(p):
            missing.append(f["path"])
            continue
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        (ok if h == f["sha256"] else bad).append(f["path"])
    return {"origin": ORIGIN, "origin_commit": c["origin_commit"],
            "files": len(c["files"]), "intact": len(ok),
            "drifted": bad, "missing": missing,
            "byte_identical": not bad and not missing}


# ---------------------------------------------------------------------------
# ACCESSORS — read and count. Nothing here changes what the engine does.
# ---------------------------------------------------------------------------

def locks(repo: str = ".") -> dict:
    txt = _read(repo, "docs/LOCKED_DECISIONS.md")
    ids = sorted(set(__import__("re").findall(r"SEQ-LOCK-\d{3}", txt)))
    return {"file": "docs/LOCKED_DECISIONS.md", "locks": ids,
            "count": len(ids)}


def intent_types(repo: str = ".") -> dict:
    d = _read(repo, "machine/runtime/EVENT_INTENT_GROWTH_CONTRACT_V1.json")
    return {"motto": d.get("universal_motto"),
            "types": d.get("intent_types", []),
            "hard_separations": d.get("hard_separations", []),
            "status_as_csb_states_it": d.get("status")}


def ai64(repo: str = ".") -> dict:
    d = _read(repo, "registries/ai/AI_ONLY_RECORDS_64_APPROVED_V1.json")
    recs = d.get("records", [])
    return {"registry_id": d.get("registry_id"), "records": len(recs),
            "status": d.get("status"),
            "source_workbook": d.get("source_workbook")}


def engines75(repo: str = ".") -> dict:
    d = _read(repo, "registries/asi/ENGINE_LIBRARY_75_APPROVED_V1.json")
    return {"registry_id": d.get("registry_id"),
            "engine_count": d.get("engine_count"),
            "status": d.get("status"),
            "source_workbook": d.get("source_workbook")}


def operational(repo: str = ".") -> dict:
    c = _read(repo,
              "registries/asi/OPERATIONAL_CONTAINERS_161_240_APPROVED_V1.json")
    s = _read(repo,
              "generated/registry_views/"
              "operational_subparameters_2593_3072_v1.json")
    sub = s.get("records", s.get("parameters", []))
    con = c.get("records", c.get("container_count"))
    return {"containers": (len(con) if isinstance(con, (list, dict)) else con),
            "container_range": "161-240",
            "subparameters": (len(sub) if isinstance(sub, (list, dict))
                              else sub),
            "subparameter_range": "2593-3072",
            "status": c.get("status")}


def expansion32(repo: str = ".") -> dict:
    d = _read(repo,
              "registries/expansion/"
              "EXPANSION_PARAMETERS_2561_2592_APPROVED_V1.json")
    recs = d.get("records", d.get("record_count"))
    return {"registry_id": d.get("registry_id"),
            "records": (len(recs) if isinstance(recs, (list, dict))
                        else recs),
            "first_id": (recs[0][0] if isinstance(recs, list) and recs
                         else None),   # SB-ASI-P2561 — the OTHER namespace
            "band": "2561-2592",
            "namespace_note": "the ASI-Brain workbook's numbering — NOT this "
                              "core's SB-HFR-P2561..P2592, which are "
                              "different rows wearing the same numerals. "
                              "HALT-1.",
            "status": d.get("status")}


def native2560(repo: str = ".") -> dict:
    d = _read(repo,
              "generated/registry_views/human_native_2560_registry_v1.json")
    recs = d.get("records", d.get("parameters", []))
    parts = [f["path"] for f in custody(repo)["files"]
             if "native/compressed" in f["path"]]
    return {"registry_id": d.get("registry_id"),
            "records": (len(recs) if isinstance(recs, list) else recs),
            "custody_parts": len(parts),
            "note": "the immutable legacy bank (SB-ASI-P0001..P2560) the "
                    "3,204 functional registry succeeded. Grok wrote it "
                    "container by container on the Grok-ASS branch."}


def nodes22(repo: str = ".") -> dict:
    d = _read(repo, "registries/asi/asi_node_registry.json")
    return {"node_count": d.get("node_count", len(d.get("nodes", []))),
            "nodes": [{"id": n["asi_node_id"], "role": n["service_role"]}
                      for n in d.get("nodes", [])],
            "note_as_csb_states_it": d.get("note")}


def rubrics52(repo: str = ".") -> dict:
    d = _read(repo, "machine/rubrics/RUBRIC_REGISTRY_R01_R52.json")
    rs = d.get("rubrics", d.get("records", d))
    return {"count": (len(rs) if isinstance(rs, (list, dict)) else rs),
            "range": "R01-R52",
            "names_sample": ([rs[k].get("name") for k in sorted(rs)[:5]]
                             if isinstance(rs, dict) else [])}


def wisdom(repo: str = ".") -> dict:
    w = _read(repo, "registries/wisdom/WISDOM_OBJECTS_BG_2_47_2_50_V1.json")
    return {"registry_id": w.get("registry_id"),
            "adoption_scope_as_csb_states_it": w.get("adoption_scope"),
            "pipeline_files": sorted(
                f["path"] for f in custody(repo)["files"]
                if "wisdom" in f["path"] or "holy_book" in f["path"]),
            "separation_law": "Source Text != Source Claim != Interpretation "
                              "!= Wisdom != Law/Guidance",
            "wired_into_this_core": False}


def his_examples(repo: str = ".") -> dict:
    rain = _read(repo,
                 "phase2/examples/RAIN_TARGET_LAYER_ACTION_EXAMPLE_V1.md")
    at = rain.find("> when i want")
    return {"files": [f["path"] for f in custody(repo)["files"]
                      if f["path"].startswith("phase2/examples/")],
            "rain_original_source": (rain[at:at + 140].lstrip("> ").strip()
                                     if at >= 0 else "(see file)"),
            "note": "his ORIGINAL rain wording — this core received the "
                    "retold version. Both stand; neither replaces the other."}


# ---------------------------------------------------------------------------
# THE HALTS — every seam between the adopted material and this core.
# Adopted and INERT until his word. Nothing below was decided.
# ---------------------------------------------------------------------------

def halts() -> list:
    return [
        {"id": "ADOPT-HALT-1",
         "seam": "P2561-P2592 exists twice: C-SB's expansion band (ASI-Brain "
                 "workbook namespace, 32 records) and this core's "
                 "SB-HFR-P2561..P2592 (32+ different rows, same numerals). "
                 "His standing rule — do not silently merge namespaces — "
                 "keeps them apart today.",
         "his_call": "whether the bands ever cross-reference, and which "
                     "namespace owns the numerals where they meet."},
        {"id": "ADOPT-HALT-2",
         "seam": "three node vocabularies now stand: C-SB's 22 ASI service "
                 "nodes (ASI-NODE-00..21), this core's 12 node types "
                 "(SB-N-), and the 95 configured brains.",
         "his_call": "which are one thing, which are three, and what links "
                     "them."},
        {"id": "ADOPT-HALT-3",
         "seam": "C-SB's rubric registry holds R01-R52; this core extracted "
                 "his 25 universal dimensions from the Kings file. 52 vs 25, "
                 "unknown overlap.",
         "his_call": "same family or two registries — and if one, which "
                     "names win."},
        {"id": "ADOPT-HALT-4",
         "seam": "C-SB types every event's intent (8 types, UNKNOWN "
                 "preferred over fabrication); this core's intent slot is "
                 "OPEN/never-absent but untyped.",
         "his_call": "wire the typing into events_in / the intent slot, or "
                     "keep it adopted-only."},
        {"id": "ADOPT-HALT-5",
         "seam": "the BG 2.47-2.50 wisdom objects are adopted with C-SB's "
                 "own scope (contextual, not doctrinal canon, not action "
                 "authority). This core's wisdom bank / Instinct memory "
                 "does not read them.",
         "his_call": "whether the scripture Wisdom Bank he named as a next "
                     "candidate starts from these objects."},
        {"id": "ADOPT-HALT-6",
         "seam": "the 75 engines and the 240/3,072 operational layer stand "
                 "beside this core's 80/3,204. His earlier word '3072 is "
                 "the count' closed item 20; the full registry of that "
                 "count now sits here, inert.",
         "his_call": "the relationship — bindings, or two banks that never "
                     "sum (like WB-P vs SB-HFR-P)."},
        {"id": "ADOPT-HALT-7",
         "seam": "C-SB's phase-2 history (checkpoints, closures, RFR runs) "
                 "was NOT mirrored — it is C-SB's own proof record.",
         "his_call": "whether to mirror it wholesale or leave it where it "
                     "lives."},
    ]


def stats(repo: str = ".") -> dict:
    c = custody(repo)
    return {
        "origin": ORIGIN, "origin_commit": c["origin_commit"][:7],
        "adopted_files": c["file_count"],
        "total_bytes": c["total_bytes"],
        "his_word": c["his_word"],
        "csb_untouched": c["csb_untouched"],
        "wired_into_engine_behavior": False,
        "halts_awaiting_him": len(halts()),
        "law": "byte-identical, statuses preserved, nothing interpreted. "
               "Every seam is his call, not a choice made here.",
    }


# ---------------------------------------------------------------------------
# THE SECOND ADOPTION — the SB-ASI Drive master workbook (2026-08-27).
# Same law: byte-identical custody, read-only accessors, seams HALT.
# ---------------------------------------------------------------------------

def _wb_root(repo: str = ".") -> str:
    return os.path.join(repo, "adopted", "SB-ASI-Drive")


def wb_custody(repo: str = ".") -> dict:
    p = os.path.join(_wb_root(repo), "ADOPTION_CUSTODY.json")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def wb_verify(repo: str = ".") -> dict:
    """Re-hash the workbook and every derived sheet against its manifest."""
    c = wb_custody(repo)
    entries = [c["source_file"]] + c["derived_files"]
    ok, bad, missing = [], [], []
    for f in entries:
        p = os.path.join(repo, f["path"])
        if not os.path.exists(p):
            missing.append(f["path"])
            continue
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        (ok if h == f["sha256"] else bad).append(f["path"])
    return {"adoption": c["adoption"], "his_word": c["his_word"],
            "files": len(entries), "intact": len(ok), "drifted": bad,
            "missing": missing, "byte_identical": not bad and not missing,
            "source_wins": "the .xlsx is the source; derived_text is its "
                           "mechanical, reviewable face"}


def _wb_sheet(repo: str, prefix: str) -> str:
    d = os.path.join(_wb_root(repo), "derived_text")
    for name in sorted(os.listdir(d)):
        if name.startswith(prefix):
            with open(os.path.join(d, name), "r", encoding="utf-8") as f:
                return f.read()
    raise FileNotFoundError(prefix)


def the_bridge(repo: str = ".") -> dict:
    """What HIS OWN FILE states about the 2,560 and the 3,204 — counted
    from the sheets, not retyped. The seam it feeds is ADOPT-HALT-8."""
    params = [r.split("\t") for r in
              _wb_sheet(repo, "05_").splitlines()[1:] if r]
    exact = sum(1 for r in params if len(r) > 14
                and r[14].startswith("EXACT SOURCE WORDING"))
    recon = [r for r in params if len(r) > 14
             and "RECONSTRUCTION" in r[14]]
    reserve = [r for r in _wb_sheet(repo, "06_").splitlines()[1:] if r]
    return {
        "his_document": "ASI_Claude_Parameters.docx — the 3,204 this core's "
                        "live bank IS",
        "carried_exact": exact,
        "held_in_reserve": len(reserve),
        "carried_plus_reserve": exact + len(reserve),
        "reconstruction_candidates": [
            {"id": r[1], "wording": r[9],
             "status": "REQUIRES USER APPROVAL — the file's own flag"}
            for r in recon],
        "baseline_2560": exact + len(recon),
        "identity": "%d + %d = 3,204 (his document) · %d + %d = 2,560 "
                    "(the workbook baseline)" % (exact, len(reserve),
                                                 exact, len(recon)),
        "decided_here": False,
    }


def wb_stats(repo: str = ".") -> dict:
    c = wb_custody(repo)
    return {"adoption": c["adoption"], "his_word": c["his_word"],
            "date": c["date"], "sheets": c["extraction_totals"]["sheets"],
            "filled_cells": c["extraction_totals"]["filled_cells"],
            "words": c["extraction_totals"]["words"],
            "files": 1 + len(c["derived_files"]),
            "source_sha256": c["source_file"]["sha256"][:16],
            "wired_into_engine_behavior": False,
            "halts_awaiting_him": len(wb_halts())}


def wb_findings() -> list:
    """What the review caught IN the file. Reported, corrected nowhere."""
    return [
        {"id": "WBF-M1",
         "finding": "SB-ASI-P0001's wording cell reads 'Source parameter "
                    "row 1 — wording extraction required' — a placeholder — "
                    "while its classification column says EXACT SOURCE "
                    "WORDING. One row of 2,560, and it is the first row.",
         "corrected": False},
        {"id": "WBF-M2",
         "finding": "the Task-3 body is elsewhere: the 2,514 parameter-level "
                    "Human-AI edges, the 46 Human-only names and the 64 "
                    "AI-only wordings live by reference in ASI-Brain_Task3_"
                    "Human_AI_Parallel_v0_3.xlsx, which the file itself "
                    "records as not Drive-readable — 'OPEN SOURCE GAP. No AI "
                    "wording reconstructed.' The counts are approved; the "
                    "rows are not present.",
         "corrected": False},
        {"id": "WBF-M3",
         "finding": "target 2,560 + reserve 650 = 3,210, not 3,204 — "
                    "consistent, because the target already contains the 6 "
                    "added reconstructions; the true identity is 2,554 + 650 "
                    "= 3,204 and 2,554 + 6 = 2,560.",
         "corrected": False},
        {"id": "WBF-M4",
         "finding": "the 3,905 formulas are Google-Sheets imports frozen as "
                    "cached DUMMYFUNCTION values — displayed values intact, "
                    "formulas inert outside Sheets.",
         "corrected": False},
        {"id": "WBF-M5",
         "finding": "the external cognitive source base reads 918 concepts, "
                    "loaded 0 — Task 4 material, correctly held behind his "
                    "gate ('Discuss every sentence first').",
         "corrected": False},
    ]


def wb_halts() -> list:
    """The new seams the workbook opens against this core. Numbering
    continues from the C-SB seven. Decided by nobody here."""
    return [
        {"id": "ADOPT-HALT-8",
         "seam": "the bridge: his file states 3,204 = 2,554 carried + 650 "
                 "held reserve (650 NAMED rows), and 2,560 = 2,554 + 6 "
                 "visible reconstructions (P1303-P1308, each flagged "
                 "REQUIRES USER APPROVAL). The live 3,204 and the 2,560 "
                 "banks share 2,554 rows by his file's own account.",
         "his_call": "approve/replace/omit the six reconstructions, and "
                     "whether the stated bridge becomes a recorded "
                     "correspondence between the banks."},
        {"id": "ADOPT-HALT-9",
         "seam": "three filter vocabularies now stand: the workbook's "
                 "FLT-01..40, the live registry's 40 universal filters, and "
                 "the seven method filters.",
         "his_call": "same family or separate layers — and which names win "
                     "where they meet."},
        {"id": "ADOPT-HALT-10",
         "seam": "the workbook names all 12 operating states (ST-01..12); "
                 "the live registry holds 12 operating states and the Kings "
                 "file named only 6.",
         "his_call": "whether these are the same 12 — the unnamed six may "
                     "already have his names here."},
        {"id": "ADOPT-HALT-11",
         "seam": "the canonical Task-3 raw workbook (2,514 edges, 46 "
                 "Human-only names, 64 AI-only wordings) is missing by the "
                 "file's own record — and C-SB's adopted AI_ONLY_RECORDS_64 "
                 "carries 64 records WITH wording, which looks like the "
                 "later closing of exactly this gap.",
         "his_call": "confirm or refuse that identification; locate or "
                     "supply the raw workbook."},
        {"id": "ADOPT-HALT-12",
         "seam": "the Holy Books Source Ledger (four anchors, the four-layer "
                 "never-merge law) sits beside C-SB's BG 2.47-2.50 wisdom "
                 "pipeline and this core's seeded wisdom bank — three "
                 "scripture surfaces, none reading the others.",
         "his_call": "whether the scripture Wisdom Bank he named starts "
                     "from this ledger's law (extends ADOPT-HALT-5)."},
    ]


def annotations() -> list:
    return [
        ("byte-identical adoption with SHA custody", "adopted.verify"),
        ("nothing wired into engine behavior", "adopted.stats"),
        ("every seam a HALT for him", "adopted.halts"),
        ("C-SB untouched", "adopted.custody"),
        ("his original rain wording, preserved", "adopted.his_examples"),
        ("the workbook adoption, custody-verified", "adopted.wb_verify"),
        ("the bridge his file states, counted not retyped",
         "adopted.the_bridge"),
        ("review findings reported, corrected nowhere",
         "adopted.wb_findings"),
    ]
