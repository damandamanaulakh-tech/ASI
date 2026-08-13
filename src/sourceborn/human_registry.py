"""THE HUMAN FUNCTIONAL REGISTRY — his real 3,204, loaded from his own document.

His words, 2026-08-13:

    "we quit 70-25 things and adopt new frame work of 1-10-8-40"
    "attached details of each 3000 point, add it there instead of just ID numbers"

THE FRAME IS 1 - 10 - 8 - 40:

    1   functional system
    10  major functional segments
    8   master containers per segment          =  80 containers
    40  named sub-parameters per container     =  3,204 named (two segments
                                                  carry 322, the rest 320)
    +   40 cross-container universal filters
    +   12 operating states per parameter
    +   20 failure / distortion classes
    +   30 steps in the human operating chain

Source: `ASI_Claude_Parameters.docx` — HUMAN FUNCTIONAL REGISTRY v1.0, his
upload. Parsed whole: 10 segments, 80 containers, 3,204 named sub-parameters,
**zero containers whose parse disagreed with its stated target**. Every name in
`data/human_registry.json` is HIS text, not a generated label.

WHAT CHANGED BECAUSE OF THIS
  * The 70 SB / 25 URR pyramid is **dead on screen as well as in the engine**.
    It stayed rendering after he killed it; that was the defect he caught.
  * A parameter is no longer a bare ID. `CON-028` is "Working Memory" with 40
    named sub-parameters, its own modulating filters, and his note on what the
    container is actually for.
"""
from __future__ import annotations

import json
import os
from functools import lru_cache

_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data",
                     "human_registry.json")


@lru_cache(maxsize=1)
def registry() -> dict:
    """His document, whole. Read once and cached — 139 KB of his own text."""
    try:
        with open(_DATA, encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:                 # never take a route down
        return {"frame": {}, "segments": [], "universal_filters": [],
                "operating_states": [], "failure_classes": [],
                "operating_chain": [], "error": str(exc)[:200]}


def frame() -> dict:
    return registry().get("frame", {})


def segments() -> list[dict]:
    return registry().get("segments", [])


def universal_filters() -> list[dict]:
    return registry().get("universal_filters", [])


def operating_states() -> list[dict]:
    return registry().get("operating_states", [])


def failure_classes() -> list[dict]:
    return registry().get("failure_classes", [])


def operating_chain() -> list[dict]:
    return registry().get("operating_chain", [])


@lru_cache(maxsize=1)
def containers() -> list[dict]:
    """All 80, flat, each carrying its segment and its 40 named sub-parameters."""
    out = []
    for s in segments():
        for c in s.get("containers", []):
            out.append({
                "id": f"CON-{c['n']:03d}",
                "n": c["n"], "name": c["name"],
                "segment": f"SEG-{s['n']:02d}",
                "segment_name": s["name"],
                "target": c.get("target", 40),
                "count": len(c.get("subs", [])),
                "subs": c.get("subs", []),
                "modulators": c.get("filters", ""),
                "note": c.get("note", ""),
            })
    return out


@lru_cache(maxsize=1)
def parameters() -> list[dict]:
    """All 3,204, each with a stable id and HIS name — never a placeholder.

    The id is positional within its container (`P-028-07`), so a sub-parameter
    keeps its address even when a container's list grows: his rule is that
    nothing is removed, so positions are only ever appended to.
    """
    out = []
    for c in containers():
        for i, name in enumerate(c["subs"], start=1):
            out.append({
                "id": f"P-{c['n']:03d}-{i:02d}",
                "name": name,
                "container": c["id"],
                "container_name": c["name"],
                "segment": c["segment"],
                "segment_name": c["segment_name"],
                "modulators": c["modulators"],
                "container_note": c["note"],
                "filled": True,          # it has HIS name, so it is filled
            })
    return out


@lru_cache(maxsize=1)
def _index() -> dict:
    return {p["id"]: p for p in parameters()}


def get(pid: str) -> dict | None:
    return _index().get(pid)


def container(cid: str) -> dict | None:
    for c in containers():
        if c["id"] == cid:
            return c
    return None


def _stem(w: str) -> str:
    """Light, honest stemming so "memories" reaches "Memory" and "planning"
    reaches "plan". No dictionary, no guessing at meaning — just the endings
    that would otherwise make his own words miss each other."""
    for suf, rep in (("ies", "y"), ("ing", ""), ("ed", ""), ("es", ""),
                     ("s", "")):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            return w[:-len(suf)] + rep
    return w


def _toks(text: str) -> set:
    import re
    return {_stem(w) for w in re.findall(r"[a-z]{3,}", (text or "").lower())}


# words that carry no discriminating power in an ask
STOP = {"the", "and", "for", "with", "that", "this", "was", "were", "are",
        "have", "has", "had", "not", "but", "you", "your", "him", "her",
        "his", "she", "they", "them", "their", "what", "when", "where", "why",
        "how", "who", "there", "here", "then", "than", "from", "into", "out",
        "about", "would", "could", "should", "did", "does", "doe", "been",
        "being", "just", "only", "also", "very", "much", "more", "most",
        "some", "any", "all", "one", "two", "get", "got", "make", "made",
        "take", "took", "come", "came", "went", "say", "said", "tell", "told"}


@lru_cache(maxsize=1)
def _idf() -> dict:
    """How rare each of his words is across all 3,204 names.

    Without this, "memory" — which appears in dozens of his names — outweighs
    "beloved", which appears in almost none. A shared common word is weak
    evidence; a shared rare word is strong. This is the difference between the
    view being useful and being a wall of near-identical hits."""
    import math
    n = 0
    df: dict[str, int] = {}
    for toks, _p in _param_index():
        n += 1
        for t in toks:
            df[t] = df.get(t, 0) + 1
    return {t: math.log(1 + n / c) for t, c in df.items()}


@lru_cache(maxsize=1)
def _param_index() -> list:
    """Tokens of the SUB-PARAMETER NAME ONLY.

    The container's note is deliberately NOT included here. It was, and the
    result was that one container's whole list of 40 fired together because the
    ask happened to share a word with the container's description — a container
    match wearing a parameter match's clothes. Container matching is separate,
    below."""
    return [(_toks(p["name"]), p) for p in parameters()]


@lru_cache(maxsize=1)
def _con_index() -> list:
    """Containers match on their own NAME.

    The note and the modulators are deliberately excluded from what can CREATE
    a hit: his notes contain ordinary words like attention, context, goal and
    emotion, so matching on them fired eight containers per segment and the
    segment list became meaningless. They still appear on a hit that was earned
    another way — they explain it, they do not make it."""
    return [(_toks(c["name"]), c) for c in containers()]


def activate(text: str, limit: int = 40, per_container: int = 6) -> dict:
    """Which of HIS 3,204 the words actually touch — and separately, which of
    his 80 containers and 10 segments.

    Two levels, kept apart, because they are different claims: a PARAMETER hit
    means his own name for that ability shares words with the ask; a CONTAINER
    hit means the ask is in that area of the mind. `per_container` stops a
    single container flooding the list, and the number dropped is reported
    rather than silently cut."""
    q = {t for t in _toks(text) if t not in STOP}
    if not q:
        return {"segments": [], "containers": [], "parameters": [],
                "searched": len(parameters()), "hit_total": 0, "dropped": 0}

    # --- parameters: his name for the ability ----------------------------
    idf = _idf()
    hits = []
    for toks, p in _param_index():
        shared = q & toks
        if not shared:
            continue
        # weight by how RARE his words are, normalised by the length of his
        # name — so a tight match on an unusual word beats a stray common word
        w = sum(idf.get(t, 0.0) for t in shared)
        cover = len(shared) / max(1, len(toks))
        score = w * (0.5 + 0.5 * cover)
        # a single common word is not a hit worth showing
        if len(shared) == 1 and w < 3.0 and cover < 0.5:
            continue
        hits.append((score, len(shared), sorted(shared), p))
    hits.sort(key=lambda h: (-h[0], -h[1], h[3]["id"]))
    kept, seen_con, dropped = [], {}, 0
    for score, n, sh, p in hits:
        c = p["container"]
        if seen_con.get(c, 0) >= per_container:
            dropped += 1
            continue
        seen_con[c] = seen_con.get(c, 0) + 1
        kept.append({**p, "matched": sh, "score": round(score, 2),
                     "reason": "your words matched his name for it: "
                               + ", ".join(sh[:6])})
        if len(kept) >= limit:
            dropped += sum(1 for _ in hits[hits.index((score, n, sh, p)) + 1:])
            break

    # --- containers: the area of the mind, matched in its own right -------
    cons = []
    for toks, c in _con_index():
        shared = q & toks
        by_param = seen_con.get(c["id"], 0)
        if shared or by_param:
            why = []
            if by_param:
                why.append(f"{by_param} of its sub-parameters fired")
            if shared:
                why.append("its own name matched: " + ", ".join(
                    sorted(shared)[:5]))
            cons.append({"id": c["id"], "name": c["name"],
                         "segment": c["segment"],
                         "segment_name": c["segment_name"],
                         "note": c["note"], "modulators": c["modulators"],
                         "count": c["count"], "fired_params": by_param,
                         "matched": sorted(shared),
                         "reason": " · ".join(why)})
    cons.sort(key=lambda c: (-c["fired_params"], -len(c["matched"]), c["id"]))

    sids = []
    for c in cons:
        if c["segment"] not in sids:
            sids.append(c["segment"])
    segs = [{"id": f"SEG-{s['n']:02d}", "name": s["name"],
             "containers": len(s["containers"]),
             "fired_containers": sum(1 for c in cons
                                     if c["segment"] == f"SEG-{s['n']:02d}"),
             "reason": "its containers fired"}
            for s in segments() if f"SEG-{s['n']:02d}" in sids]
    segs.sort(key=lambda x: -x["fired_containers"])

    return {"segments": segs, "containers": cons, "parameters": kept,
            "searched": len(parameters()), "hit_total": len(hits),
            "dropped": dropped,
            "cap": {"per_container": per_container, "limit": limit,
                    "note": "capped so one container cannot flood the view; "
                            "the number dropped is stated, never hidden"}}


def stats() -> dict:
    f = frame()
    return {"frame": "1 - 10 - 8 - 40",
            "system": 1,
            "segments": len(segments()),
            "containers": len(containers()),
            "parameters": len(parameters()),
            "per_container": f.get("subparameters_per_container", 40),
            "universal_filters": len(universal_filters()),
            "operating_states": len(operating_states()),
            "failure_classes": len(failure_classes()),
            "operating_chain": len(operating_chain()),
            "source": registry().get("source", ""),
            "his_words": f.get("his_words", ""),
            "every_name_is_his": True}
