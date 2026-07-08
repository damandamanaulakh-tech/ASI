"""The Pyramid of Thought — ARD_RGL_7025 §11-13, made real.

Every node files what it captures into its own pyramid of filters:

    Level 1  — the Node name itself
    Main     — 5-10 broad categories for that node's stage
    Sub      — 10-20 buckets under the mains (keyword-triggered)
    Micro    — 20-30 fine-grained concrete details (numbers, tags, terms)

URR brains use the shallower 5 → 10-15 form. "Its just define the data,
dividing in micro keep in main cat so context memory issue can't be problem."

Anything the engine cannot park lands in the **unfiled queue** for the human —
"human review again help there, where AI can't park it at right place." Nothing
is discarded (classify, don't reject).
"""

from __future__ import annotations

import json
import os
import re
from typing import Any

# Main categories per stage (5-10 each) — the broad drawers of every SB brain
# in that stage. Names follow the stage descriptions in the core document.
STAGE_MAIN: dict[int, tuple[str, ...]] = {
    1: ("Source", "Structure", "Domain", "Parameters", "Data Banks", "Memory", "Gate"),
    2: ("Emotion", "Intent", "Shadow", "Identity", "Power", "Wound", "Culture", "Drama"),
    3: ("Pressure", "Doubt", "Falsifier", "Blind Spot", "Contradiction",
        "Assumption", "Framing", "Truth Lock"),
    4: ("Proof Level", "Source Tag", "Audit", "Pattern", "Live Data",
        "Validation", "Completion"),
    5: ("Connection", "Fusion", "Merge", "Convergence", "New Parameter", "Sync"),
    6: ("Synthetic Fuel", "Invention", "Scaffold", "Inversion", "Simplification",
        "Tagging", "Labeling"),
    7: ("Risk", "Wall", "Override", "Non-Resolution", "Anchor", "Embodied", "Decision"),
    8: ("Master Log", "Update", "Output", "Feed-Forward", "Compilation",
        "Breakthrough", "Halt", "Long-Term"),
}

# Sub buckets (10-20 reachable per stage): bucket name -> trigger words.
SUB_BUCKETS: dict[str, tuple[str, ...]] = {
    "locked": ("locked", "lock", "untouched", "immutab"),
    "channels": ("channel", "fact", "feeling", "claim", "command", "assumption"),
    "numeric": ("numeric", "financial", "total", "gst", "figure", "amount"),
    "prose": ("prose", "question", "claim"),
    "fingerprint": ("sha256", "fingerprint", "hash"),
    "banks": ("bank", "tavily", "corpus", "wisdom", "example"),
    "written": ("memory", "written", "entry", "stored", "recorded", "synced"),
    "clean": ("clean", "complete", "confirmed", "ready"),
    "affect": ("affect", "emotion", "fear", "hope", "anger", "love", "shame"),
    "motive": ("intent", "motive", "hidden", "feed", "urgent"),
    "avoidance": ("avoid", "negation", "not saying", "protect", "shadow"),
    "self": ("identity", "meaning", "who", "self", "purpose"),
    "control": ("power", "control", "authority", "command", "force"),
    "threat": ("wound", "threat", "hurt", "attack"),
    "sacred": ("sacred", "cultural", "anchor", "gita", "quran", "tao", "gospel",
               "granth", "proverb", "ecclesiastes", "aesop"),
    "attack": ("pressure", "attack", "avoiding", "break", "challenge"),
    "fragile": ("doubt", "fragil", "bites", "survives"),
    "counter": ("falsifier", "counterexample", "prove it wrong", "opposite", "inversion"),
    "blind": ("blind", "witness", "unseen"),
    "conflict": ("contradiction", "but", "however", "mismatch"),
    "absolute": ("always", "never", "obviously", "everyone", "guaranteed", "absolutes"),
    "evidence": ("evidence", "proof", "ledger", "rung", "ladder", "fact"),
    "tags": ("real_tool", "manual", "memory", "simulated", "tag"),
    "grounding": ("live", "web", "grounding", "source connected", "n/a"),
    "audit": ("audit", "recomputed", "consistent", "mismatch", "verify"),
    "links": ("connection", "cross", "hits", "scanned", "link"),
    "merge": ("merge", "contributing", "propos"),
    "similar": ("convergence", "similar", "conclusion"),
    "new-param": ("new parameter", "p-new", "generated", "labeled"),
    "fiction": ("synthetic", "fiction", "hypothetical", "counterfactual",
                "heuristic", "apostatic", "fuel", "scaffold"),
    "seed": ("invention", "seed", "protected"),
    "kernel": ("kernel", "simplif"),
    "debt": ("proof debt", "expiry", "tagged"),
    "danger": ("risk", "harm", "legal", "ethical", "safety"),
    "stall": ("wall", "stall", "data", "logic", "complexity", "moral"),
    "human-gate": ("human", "review", "override", "decision", "halt", "authority"),
    "held": ("non-resolution", "hold", "held", "incubate", "resistance"),
    "anchored": ("anchor", "point zero", "drift", "re-anchor"),
    "body": ("embodied", "sits right", "intuition"),
    "log": ("master log", "append-only", "sacred"),
    "weekly": ("weekly", "monday", "update", "due"),
    "final": ("final output", "generated", "deliver", "classification"),
    "forward": ("feed-forward", "targets", "router"),
    "compiled": ("compiled", "compilation", "matches"),
    "score": ("breakthrough", "score", "locked as"),
    "closure": ("run complete", "reset", "next work", "long-term"),
}

_STOP = {"the", "and", "with", "from", "this", "that", "have", "been", "into",
         "over", "under", "your", "their", "them", "then", "than", "were",
         "when", "what", "which", "will", "must", "does", "doing", "here",
         "there", "these", "those", "each", "every", "none", "nothing"}

# Micro extractors: concrete details — numbers, [TAGS], Node-IDs, quoted bits.
_MICRO_RE = re.compile(
    r"\[[A-Z][A-Z _-]+\]"            # [SYNTHETIC], [HALT:...]
    r"|\b(?:SB|URR)-\d{2}\b"         # node ids
    r"|sha256:[0-9a-f]+"             # fingerprints
    r"|-?\d[\d,]*(?:\.\d+)?"         # numbers
    r"|\"[^\"]{3,40}\"|'[^']{3,40}'" # short quoted strings
)


def file_finding(stage: int, text: str, params: dict[str, Any] | None = None
                 ) -> tuple[dict[str, list[str]], list[str]]:
    """File one node finding into the pyramid. Returns (pyramid, unfiled):
    pyramid = {"main": [...], "sub": [...], "micro": [...]} per the doc's
    1 → 5-10 → 10-20 → 20-30 shape; unfiled = significant words the rules
    could not park (goes to the human review queue — never discarded)."""
    low = (text or "").lower()
    mains = STAGE_MAIN.get(stage, STAGE_MAIN[8])
    main_hits = [m for m in mains if any(w in low for w in m.lower().split())]
    sub_hits, sub_words = [], set()
    for bucket, trigs in SUB_BUCKETS.items():
        for t in trigs:
            if t in low:
                sub_hits.append(bucket)
                sub_words.update(t.split())
                break
    if not main_hits:                      # every finding gets at least a drawer
        main_hits = [mains[0]]
    micro = []
    for m in _MICRO_RE.findall(text or ""):
        if m not in micro:
            micro.append(m)
        if len(micro) >= 30:               # 20-30 micro cap per the doc
            break
    if params:
        for k, v in list(params.items())[:6]:
            item = f"{k}={v}" if not isinstance(v, (dict, list)) else k
            if item not in micro and len(micro) < 30:
                micro.append(str(item)[:48])
    return {"main": main_hits[:10], "sub": sub_hits[:20], "micro": micro}


def unfiled_from_input(text: str, limit: int = 5) -> list[str]:
    """The USER's words that no pyramid bucket can park — §"when some data not
    fitting in existing parameter… keep labeling it" + "human review again help
    there". Runs on the raw ask/document, never on the engine's own vocabulary,
    so the queue holds the human's unparked thought, not machine noise."""
    low = (text or "").lower()
    out = []
    for w in re.findall(r"[a-z]{6,}", low):
        if w in _STOP:
            continue
        parked = any(w in t or t in w
                     for trigs in SUB_BUCKETS.values() for t in trigs)
        if not parked and not any(w in m.lower() for ms in STAGE_MAIN.values()
                                  for m in ms):
            if w not in out:
                out.append(w)
        if len(out) >= limit:
            break
    return out


def file_urr(role_name: str, verdict: str, issues: list[str]
             ) -> dict[str, list[str]]:
    """URR pyramid (5 → 10-15): main = role area, sub = verdict + issue kinds."""
    area = role_name.split(" ")[0] if role_name else "Verification"
    subs = [f"verdict:{verdict}"] + [i[:32] for i in issues[:14]]
    return {"main": [area], "sub": subs[:15], "micro": []}


class UnfiledQueue:
    """What the engine could not park — kept for the human, never dropped."""

    def __init__(self, root: str) -> None:
        self.path = os.path.join(root, "unfiled.jsonl")

    def add(self, node_id: str, items: list[str], at: str) -> None:
        if not items:
            return
        with open(self.path, "a", encoding="utf-8") as f:
            for it in items:
                f.write(json.dumps({"node": node_id, "item": it, "at": at},
                                   ensure_ascii=False) + "\n")

    def list(self, limit: int = 100) -> list[dict]:
        if not os.path.exists(self.path):
            return []
        with open(self.path, encoding="utf-8") as f:
            rows = [json.loads(ln) for ln in f if ln.strip()]
        seen, out = set(), []
        for r in reversed(rows):                    # newest first, de-duped
            key = (r.get("node"), r.get("item"))
            if key not in seen:
                seen.add(key)
                out.append(r)
            if len(out) >= limit:
                break
        return out

    def park(self, node_id: str, item: str) -> None:
        """Human parked it — remove from the queue (it now lives in a brain)."""
        if not os.path.exists(self.path):
            return
        with open(self.path, encoding="utf-8") as f:
            rows = [json.loads(ln) for ln in f if ln.strip()]
        rows = [r for r in rows
                if not (r.get("node") == node_id and r.get("item") == item)]
        with open(self.path, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
