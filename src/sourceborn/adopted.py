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


def annotations() -> list:
    return [
        ("byte-identical adoption with SHA custody", "adopted.verify"),
        ("nothing wired into engine behavior", "adopted.stats"),
        ("every seam a HALT for him", "adopted.halts"),
        ("C-SB untouched", "adopted.custody"),
        ("his original rain wording, preserved", "adopted.his_examples"),
    ]
