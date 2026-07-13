"""Feed the brain — ingest the user's corpus so muscle memory compounds.

"It must have the data I had given as example and filtration of thoughts."

This walks the user's cores, raw thoughts, and reference engine-outputs and,
for every file:

  * writes a high-parameter memory entry into a stage-appropriate node brain,
    **pyramid-filed** (Node → Main → Sub → Micro) exactly like a live finding;
  * learns the user's voice from raw thoughts (persona example bank);
  * routes reference outputs as "the way a good answer looks".

The same routine runs on boot over ``seed_corpus/`` (shipped with the app, so
it deploys to Render) AND every time the user adds a file — "when I add".

Binary formats are handled by ``extract.extract_text`` upstream; here we take
already-extracted text so the brain stays transparent and ownable.
"""

from __future__ import annotations

import os
from typing import Iterable

from .enums import Classification, EvidenceTag
from .memory import Memory
from .models import MemoryEntry, RawSource, _now
from .persona import Persona
from .pyramid import file_finding, unfiled_from_input, UnfiledQueue

TEXT_EXTS = {".txt", ".md", ".markdown"}

# category folder -> (node to file under, stage for the pyramid, learn voice?)
CATEGORY_ROUTE: dict[str, tuple[str, int, bool]] = {
    "raw_thoughts": ("SB-09", 2, True),    # the user's voice / affect / theory
    "examples": ("SB-64", 8, True),        # reference engine-output ("good answer")
    "cores": ("SB-07", 1, False),          # spec / core lineage → source memory
    "wisdom": ("SB-32", 4, False),         # eternal-example material
}
DEFAULT_ROUTE = ("SB-07", 1, True)


def iter_text_files(folder: str) -> Iterable[tuple[str, str]]:
    """Yield (path, category) for every text file under ``folder``. The category
    is the top-level subfolder name (raw_thoughts / examples / cores / wisdom)."""
    for dirpath, _dirs, files in os.walk(folder):
        rel = os.path.relpath(dirpath, folder)
        category = rel.split(os.sep)[0] if rel != "." else ""
        for fn in files:
            if os.path.splitext(fn)[1].lower() in TEXT_EXTS:
                yield os.path.join(dirpath, fn), category


def ingest_text_entry(memory: Memory, persona: Persona | None, name: str,
                      text: str, category: str = "", origin: str = "add",
                      unfiled: UnfiledQueue | None = None,
                      max_chars: int = 20000) -> dict:
    """Ingest ONE piece of text (a file, a note, an uploaded doc) into the brain
    — pyramid-filed, voice-learned, routed by category. This is the "when I add"
    path: called on every upload / ingest so nothing lands unfiled."""
    text = (text or "")[:max_chars].strip()
    if not text:
        return {"ok": False, "reason": "empty"}
    node_id, stage, learn_voice = CATEGORY_ROUTE.get(category, DEFAULT_ROUTE)
    raw = RawSource(text=text, origin=f"corpus:{name}").lock()
    pyr = file_finding(stage, text[:4000], {"source": name, "category": category})
    memory.write(node_id, MemoryEntry(
        node_id=node_id, raw_source_id=raw.raw_source_id,
        content=text[:4000],
        classification=Classification.REVIEW_ONLY.value,
        evidence_tag=EvidenceTag.REVIEW.value,
        tags=["corpus", category or "note", name],
        parameters={"source": name, "category": category, "chars": len(text)},
        pyramid=pyr,
    ), name="First Memory Write")
    memory.brain(node_id).bump("Patterns_Recognized")
    # the user's own words that no bucket could park → human review queue
    if unfiled is not None:
        unfiled.add(node_id, unfiled_from_input(text), _now())
    if persona is not None and learn_voice:
        persona.learn(question=name, answer=text[:1500],
                      note=f"ingested {category or 'corpus'}")
    return {"ok": True, "node": node_id, "category": category,
            "pyramid": {k: len(v) for k, v in pyr.items()}}


def ingest_folder(
    folder: str,
    root: str = ".sourceborn",
    learn_voice: bool = True,
    max_chars: int = 20000,
) -> dict[str, int]:
    """Ingest every text file under ``folder`` (categorized subfolders) into the
    brain — each pyramid-filed and routed. Returns counts."""
    memory = Memory(root)
    persona = Persona(root) if learn_voice else None
    unfiled = UnfiledQueue(root)
    files = 0
    by_cat: dict[str, int] = {}
    for path, category in iter_text_files(folder):
        try:
            with open(path, encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except Exception:
            continue
        res = ingest_text_entry(memory, persona, os.path.basename(path), text,
                                category=category, origin=f"corpus:{path}",
                                unfiled=unfiled, max_chars=max_chars)
        if res.get("ok"):
            files += 1
            by_cat[category or "other"] = by_cat.get(category or "other", 0) + 1
    memory.master_log({"event": "ingest", "folder": folder,
                       "files": files, "by_category": by_cat})
    return {"files": files, "by_category": by_cat, **memory.stats()}
