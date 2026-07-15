"""MongoDB brain backend — "must link on MongoDB".

Same interface as the JSON store (``memory.NodeBrain`` / ``memory.Memory``),
different home: brains live in MongoDB collections instead of files.

    brains          one doc per node   {_id: "SB-20", meta: {...}}
    entries         one doc per memory entry (indexed by node_id)
    master_log      append-only sacred log
    brain_versions  shadow snapshots for rollback

Activation: set ``SB_MONGO_URL`` (a standard MongoDB/Atlas connection string)
and install ``pymongo`` (in requirements.txt; Render installs it via the
buildCommand). Without the URL the engine stays on the zero-dependency JSON
store — nothing changes for local/offline use. ``make_memory()`` picks.

Chats, uploads, the unfiled queue, and export zips remain on disk (SB_ROOT):
Mongo carries the BRAINS — the part the core says must scale and persist.
"""

from __future__ import annotations

import os
from typing import Any

from .memory import Memory, NodeBrain
from .models import MemoryEntry, _now


class MongoNodeBrain:
    """One node's brain in MongoDB — same methods as ``NodeBrain``."""

    def __init__(self, db, node_id: str, name: str = "") -> None:
        self._db = db
        self.node_id = node_id
        self.name = name
        doc = db.brains.find_one({"_id": node_id})
        if doc is None:
            self.meta = {"node_id": node_id, "name": name, "created_at": _now(),
                         "last_update": _now(), "entry_count": 0,
                         "pyramid": {"main": [], "sub": [], "micro": []},
                         "parameters": {}}
            db.brains.insert_one({"_id": node_id, "meta": self.meta})
        else:
            self.meta = doc["meta"]
            if name and not self.meta.get("name"):
                self.meta["name"] = name

    def _save_meta(self) -> None:
        self.meta["last_update"] = _now()
        self._db.brains.replace_one({"_id": self.node_id},
                                    {"_id": self.node_id, "meta": self.meta},
                                    upsert=True)

    def write(self, entry: MemoryEntry) -> str:
        d = entry.to_dict()
        d["_node"] = self.node_id
        self._db.entries.insert_one(d)
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
        out = []
        for d in self._db.entries.find({"_node": self.node_id}).sort("entry_id", 1):
            d.pop("_id", None)
            d.pop("_node", None)
            out.append(MemoryEntry(**d))
        return out

    def search(self, query: str) -> list[MemoryEntry]:
        q = query.lower()
        return [e for e in self.read_all()
                if q in (e.content + " " + " ".join(e.tags)).lower()]

    def bump(self, param: str, by: int = 1) -> int:
        cur = int(self.meta["parameters"].get(param, 0) or 0)
        self.meta["parameters"][param] = cur + by
        self._save_meta()
        return cur + by

    def snapshot(self) -> str:
        ver = int(self.meta.get("brain_version", 0)) + 1
        self.meta["brain_version"] = ver
        self._db.brain_versions.insert_one(
            {"node_id": self.node_id, "version": ver, "at": _now(),
             "meta": dict(self.meta)})
        self._db.brain_versions.delete_many(
            {"node_id": self.node_id, "version": {"$lt": ver - 3}})
        return f"mongo:brain_versions/{self.node_id}/v{ver}"

    def rollback(self) -> bool:
        doc = self._db.brain_versions.find_one({"node_id": self.node_id},
                                               sort=[("version", -1)])
        if not doc:
            return False
        self.meta = doc["meta"]
        self._save_meta()
        return True


class MongoMemory(Memory):
    """The whole brain on MongoDB. File-side features (chats, unfiled queue,
    export zip) keep using SB_ROOT on disk via the parent class paths."""

    def __init__(self, root: str = ".sourceborn", url: str | None = None) -> None:
        super().__init__(root)
        import pymongo                     # lazy: only needed when configured
        self._client = pymongo.MongoClient(
            url or os.environ["SB_MONGO_URL"], serverSelectionTimeoutMS=4000)
        self._db = self._client.get_default_database("sourceborn")
        self._db.entries.create_index("_node")
        self._db.brain_versions.create_index([("node_id", 1), ("version", -1)])
        self._mbrains: dict[str, MongoNodeBrain] = {}

    def brain(self, node_id: str, name: str = "") -> MongoNodeBrain:  # type: ignore[override]
        if node_id not in self._mbrains:
            self._mbrains[node_id] = MongoNodeBrain(self._db, node_id, name)
        return self._mbrains[node_id]

    def master_log(self, record: dict[str, Any]) -> None:
        self._db.master_log.insert_one({"at": _now(), **record})

    def search(self, query: str):
        q = query.lower()
        hits = []
        for d in self._db.entries.find(
                {"$or": [{"content": {"$regex": q, "$options": "i"}},
                         {"tags": {"$regex": q, "$options": "i"}}]}).limit(50):
            node = d.pop("_node", "")
            d.pop("_id", None)
            hits.append((node, MemoryEntry(**d)))
        return hits

    def stats(self) -> dict[str, Any]:
        return {"nodes_with_brains": self._db.brains.count_documents({}),
                "total_memory_entries": self._db.entries.count_documents({}),
                "backend": "mongodb"}


def make_memory(root: str = ".sourceborn") -> Memory:
    """The factory: MongoDB when SB_MONGO_URL is set and pymongo is installed,
    otherwise the zero-dependency JSON store. Failure to reach Mongo falls back
    to JSON loudly (master-logged), never crashes the engine."""
    url = os.environ.get("SB_MONGO_URL", "").strip()
    if url:
        try:
            m = MongoMemory(root, url)
            m._client.admin.command("ping")
            return m
        except Exception as exc:
            fallback = Memory(root)
            fallback.master_log({"event": "mongo_fallback",
                                 "error": str(exc)[:200]})
            return fallback
    return Memory(root)
