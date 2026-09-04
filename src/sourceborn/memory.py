"""The pyramid-of-brains memory store.

Every node (SB or URR) owns a *local brain* — a folder on disk that accumulates
high-parameter memory entries and organises them with pyramid filtering
(Node -> Main -> Sub -> Micro). There is one shared *Master Log* that records
everything (Principle 13: Master Log is Sacred).

Storage is plain JSON files so the user fully owns and can read their brain with
no database and no vendor lock-in. A DB backend can implement the same interface
later without touching the engine.
"""

from __future__ import annotations

import json
import os
from typing import Any

from .models import MemoryEntry, _now


class NodeBrain:
    """One node's local, self-updating brain."""

    def __init__(self, root: str, node_id: str, name: str = "") -> None:
        self.node_id = node_id
        self.name = name
        self.dir = os.path.join(root, "brains", node_id)
        os.makedirs(self.dir, exist_ok=True)
        self._meta_path = os.path.join(self.dir, "_brain.json")
        self.meta = self._load_meta()

    def _load_meta(self) -> dict[str, Any]:
        if os.path.exists(self._meta_path):
            with open(self._meta_path, encoding="utf-8") as f:
                return json.load(f)
        return {
            "node_id": self.node_id,
            "name": self.name,
            "created_at": _now(),
            "last_update": _now(),
            "entry_count": 0,
            "pyramid": {"main": [], "sub": [], "micro": []},
            "parameters": {},
        }

    def _save_meta(self) -> None:
        self.meta["last_update"] = _now()
        with open(self._meta_path, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, indent=2, ensure_ascii=False)

    def write(self, entry: MemoryEntry) -> str:
        """Automatic memory write (Principle 10)."""
        path = os.path.join(self.dir, f"{entry.entry_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(entry.to_dict(), f, indent=2, ensure_ascii=False)
        # roll the node's pyramid up from the entry's pyramid
        for level in ("main", "sub", "micro"):
            for item in entry.pyramid.get(level, []):
                if item not in self.meta["pyramid"][level]:
                    self.meta["pyramid"][level].append(item)
        for k, v in entry.parameters.items():
            self.meta["parameters"][k] = v
        self.meta["entry_count"] = self.meta.get("entry_count", 0) + 1
        self._save_meta()
        return entry.entry_id

    def read_all(self) -> list[MemoryEntry]:
        out: list[MemoryEntry] = []
        for fn in sorted(os.listdir(self.dir)):
            # memory entries are <entry_id>.json; skip _brain.json / _config.json
            # and any other underscore-prefixed metadata sharing the node folder
            if fn.endswith(".json") and not fn.startswith("_"):
                with open(os.path.join(self.dir, fn), encoding="utf-8") as f:
                    out.append(MemoryEntry(**json.load(f)))
        return out

    def search(self, query: str) -> list[MemoryEntry]:
        q = query.lower()
        return [e for e in self.read_all() if q in (e.content + " " + " ".join(e.tags)).lower()]

    def snapshot(self) -> str:
        """Shadow copy of this brain's meta before a governed change (weekly
        pass). Keeps the last 4 versions so any update can be rolled back."""
        import shutil
        ver = int(self.meta.get("brain_version", 0)) + 1
        self.meta["brain_version"] = ver
        snap = os.path.join(self.dir, f"_brain.v{ver}.json")
        if os.path.exists(self._meta_path):
            shutil.copyfile(self._meta_path, snap)
        old = sorted(f for f in os.listdir(self.dir)
                     if f.startswith("_brain.v") and f.endswith(".json"))
        for f in old[:-4]:
            try:
                os.remove(os.path.join(self.dir, f))
            except OSError:
                pass
        return snap

    def rollback(self) -> bool:
        """Restore the most recent shadow snapshot — the weekly pass is
        governed learning: reversible, never a one-way mutation."""
        snaps = sorted(f for f in os.listdir(self.dir)
                       if f.startswith("_brain.v") and f.endswith(".json"))
        if not snaps:
            return False
        import shutil
        shutil.copyfile(os.path.join(self.dir, snaps[-1]), self._meta_path)
        self.meta = self._load_meta()
        return True

    def bump(self, param: str, by: int = 1) -> int:
        """Increment one of the core brain parameters from ARD_RGL_7025
        (Runs_Completed, Patterns_Recognized, Verifications_Performed,
        Issues_Found, Human_Reviews_Triggered, Human_Interactions, …). This is
        how a local brain's stats genuinely grow with use."""
        cur = int(self.meta["parameters"].get(param, 0) or 0)
        self.meta["parameters"][param] = cur + by
        self._save_meta()
        return cur + by


class Memory:
    """The whole brain: all node brains + the Master Log + cross-node search."""

    def __init__(self, root: str = ".sourceborn") -> None:
        self.root = root
        os.makedirs(root, exist_ok=True)
        self.master_log_path = os.path.join(root, "master_log.jsonl")
        self._brains: dict[str, NodeBrain] = {}

    def brain(self, node_id: str, name: str = "") -> NodeBrain:
        if node_id not in self._brains:
            self._brains[node_id] = NodeBrain(self.root, node_id, name)
        return self._brains[node_id]

    def write(self, node_id: str, entry: MemoryEntry, name: str = "") -> str:
        entry_id = self.brain(node_id, name).write(entry)
        self.master_log(
            {"event": "memory_write", "node": node_id, "entry": entry_id,
             "classification": entry.classification, "evidence_tag": entry.evidence_tag}
        )
        return entry_id

    def master_log(self, record: dict[str, Any]) -> None:
        """Append-only sacred log."""
        record = {"at": _now(), **record}
        with open(self.master_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def search(self, query: str) -> list[tuple[str, MemoryEntry]]:
        """Cross-node memory search — the basis of Dot Connection (SB-37)."""
        hits: list[tuple[str, MemoryEntry]] = []
        brains_dir = os.path.join(self.root, "brains")
        if not os.path.isdir(brains_dir):
            return hits
        for node_id in sorted(os.listdir(brains_dir)):
            for e in self.brain(node_id).search(query):
                hits.append((node_id, e))
        return hits

    def stats(self) -> dict[str, Any]:
        brains_dir = os.path.join(self.root, "brains")
        nodes = sorted(os.listdir(brains_dir)) if os.path.isdir(brains_dir) else []
        total = sum(self.brain(n).meta.get("entry_count", 0) for n in nodes)
        return {"nodes_with_brains": len(nodes), "total_memory_entries": total}

    def weekly_digest(self) -> dict[str, Any]:
        """The Monday clog, made real. Each brain (1) SYNTHESISES its week —
        top pyramid categories, findings, recurring flags — and (2) LEARNS new
        cross-brain connections: its most distinctive sub-buckets are searched
        across all OTHER brains, and previously unknown links are written as
        connection entries and added to Connected_Points. The brain gains
        knowledge it did not have before the pass — not just counters.
        A shadow snapshot of each brain's meta is kept before mutation so any
        weekly change can be rolled back (see NodeBrain.snapshot/rollback)."""
        import collections
        brains_dir = os.path.join(self.root, "brains")
        if not os.path.isdir(brains_dir):
            return {"digested": 0, "at": _now()}
        digested = 0
        new_links_total = 0
        # sub-bucket → brains that filed under it this week (built once, cheap)
        bucket_map: dict[str, set[str]] = collections.defaultdict(set)
        per_brain: dict[str, dict] = {}
        node_ids = sorted(os.listdir(brains_dir))
        for node_id in node_ids:
            b = self.brain(node_id)
            entries = [e for e in b.read_all() if "weekly_digest" not in e.tags
                       and "weekly_connection" not in e.tags]
            if not entries:
                continue
            mains, subs, flags = (collections.Counter() for _ in range(3))
            for e in entries:
                for m in e.pyramid.get("main", []):
                    mains[m] += 1
                for s in e.pyramid.get("sub", []):
                    subs[s] += 1
                    bucket_map[s].add(node_id)
                for k, v in (e.parameters or {}).items():
                    if k == "urr_matrix_flags" and isinstance(v, dict):
                        for code in v.values():
                            flags[code] += 1
            per_brain[node_id] = {"entries": len(entries), "mains": mains,
                                  "subs": subs, "flags": flags}
        for node_id, agg in per_brain.items():
            b = self.brain(node_id)
            b.snapshot()                    # shadow copy → rollback possible
            known = set(b.meta["parameters"].get("Connected_Points") or [])
            fresh_links: dict[str, list[str]] = {}
            for s, _n in agg["subs"].most_common(5):
                others = bucket_map.get(s, set()) - {node_id}
                new = sorted(o for o in others if o not in known)
                if new:
                    fresh_links[s] = new[:6]
                    known.update(new)
            top_main = ", ".join(f"{m}×{n}" for m, n in agg["mains"].most_common(4)) or "—"
            top_flag = ", ".join(f"{c}×{n}" for c, n in agg["flags"].most_common(3)) or "none"
            link_note = ("; NEW links: " + "; ".join(
                f"{s}→{','.join(v)}" for s, v in list(fresh_links.items())[:3])
                if fresh_links else "; no new links this week")
            summary = (f"weekly digest — {agg['entries']} findings; "
                       f"top: {top_main}; flags: {top_flag}{link_note}")
            b.write(MemoryEntry(
                node_id=node_id, raw_source_id="",
                content=summary, tags=["weekly_digest", "knowledge_gained"],
                parameters={"findings": agg["entries"],
                            "top_main": dict(agg["mains"].most_common(4)),
                            "new_links": fresh_links},
            ))
            if fresh_links:
                n_new = sum(len(v) for v in fresh_links.values())
                new_links_total += n_new
                b.write(MemoryEntry(
                    node_id=node_id, raw_source_id="",
                    content="new cross-brain connections learned: " + "; ".join(
                        f"shares '{s}' with {', '.join(v)}"
                        for s, v in fresh_links.items()),
                    tags=["weekly_connection"],
                    parameters={"links": fresh_links}))
                b.bump("Patterns_Recognized", n_new)
            b.meta["parameters"]["Connected_Points"] = sorted(known)[:40]
            b.meta["parameters"]["Knowledge_Gained"] = summary[:200]
            b.bump("Last_Brain_Update_Count")
            b._save_meta()
            digested += 1
        self.master_log({"event": "weekly_digest", "brains": digested,
                         "new_connections": new_links_total})
        return {"digested": digested, "new_connections": new_links_total,
                "at": _now()}
