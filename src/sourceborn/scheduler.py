"""Weekly brain update scheduler (Principle 12: local brains update weekly).

A zero-dependency daemon thread: it checks hourly and, if a week has passed
since the last update (or it never ran), runs the full weekly job. The last-run
timestamp is persisted on disk so the cadence survives restarts (important on
Render, where the process can recycle).

Every run is kept as its own dated file under ``<root>/weekly/`` — the pull
ACCUMULATES instead of overwriting a single file, so the history is real and
readable. ``run_weekly`` is the one job; both the scheduler and the manual
"Weekly pull" button call it, so a hand-triggered pull does exactly what the
automatic one does (novelty pass included).
"""

from __future__ import annotations

import json
import os
import re
import threading
import time
from datetime import datetime, timedelta

_FMT = "%Y-%m-%d %H:%M:%S"


def _state_path(root: str) -> str:
    return os.path.join(root, "weekly_update.json")


def _weekly_dir(root: str) -> str:
    d = os.path.join(root, "weekly")
    os.makedirs(d, exist_ok=True)
    return d


def last_run(root: str) -> str | None:
    path = _state_path(root)
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f).get("last_run")
        except Exception:
            return None
    return None


def due(root: str, every_days: int = 7) -> bool:
    lr = last_run(root)
    if not lr:
        return True
    try:
        return datetime.now() - datetime.strptime(lr, _FMT) >= timedelta(days=every_days)
    except Exception:
        return True


def run_weekly(engine, root: str) -> dict:
    """The full weekly job — callable by the scheduler AND the manual button,
    so both do the same work. Refresh brain settings, synthesise each brain's
    week, hunt novelty, then write a DATED history file (never overwritten)
    plus the last-run pointer."""
    result = engine.brains.weekly_update()          # refresh brain settings
    result["digest"] = engine.memory.weekly_digest()  # synthesise each week
    try:                                            # weekly novelty hunt
        from .novelty import run_novelty_pass
        nov = run_novelty_pass(root, engine.memory, engine.unfiled)
        result["novelty"] = {"file": nov["file"],
                             "candidates": len(nov["candidates"])}
    except Exception as exc:                        # visible, never swallowed
        result["novelty"] = {"error": str(exc)[:200]}
    at = result.get("at") or datetime.now().strftime(_FMT)
    stamp = re.sub(r"[^0-9]", "", at)[:14] or str(int(time.time()))
    d = _weekly_dir(root)
    fname = f"weekly_{stamp}.json"
    # two runs inside the same second must not collide — nothing is overwritten
    n = 1
    while os.path.exists(os.path.join(d, fname)):
        n += 1
        fname = f"weekly_{stamp}_{n}.json"
    try:
        with open(os.path.join(d, fname), "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    except Exception:
        pass                                        # history is best-effort
    with open(_state_path(root), "w", encoding="utf-8") as f:
        json.dump({"last_run": at, "latest_file": fname}, f, indent=2)
    try:
        engine.memory.master_log({
            "event": "weekly_run", "file": fname,
            "brains": result.get("updated"),
            "new_connections": (result.get("digest") or {}).get("new_connections"),
            "candidates": (result.get("novelty") or {}).get("candidates")})
    except Exception:
        pass
    return result


def run_if_due(engine, root: str, every_days: int = 7) -> dict | None:
    if not due(root, every_days):
        return None
    return run_weekly(engine, root)


def history(root: str, limit: int = 52) -> list[dict]:
    """Every past weekly run, newest first — the accumulated pull ledger."""
    d = os.path.join(root, "weekly")
    if not os.path.isdir(d):
        return []
    out = []
    for fn in sorted(os.listdir(d), reverse=True)[:limit]:
        if not fn.endswith(".json"):
            continue
        try:
            with open(os.path.join(d, fn), encoding="utf-8") as f:
                r = json.load(f)
            out.append({"file": fn, "at": r.get("at"),
                        "brains": r.get("updated"),
                        "new_connections": (r.get("digest") or {}).get("new_connections"),
                        "candidates": (r.get("novelty") or {}).get("candidates"),
                        "novelty_error": (r.get("novelty") or {}).get("error")})
        except Exception:
            continue
    return out


def latest(root: str) -> dict | None:
    """The most recent full weekly result, or None if it has never run."""
    d = os.path.join(root, "weekly")
    if os.path.isdir(d):
        for fn in sorted(os.listdir(d), reverse=True):
            if not fn.endswith(".json"):
                continue
            try:
                with open(os.path.join(d, fn), encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                continue
    return None


def get_run(root: str, name: str) -> dict | None:
    """One dated weekly file by name, path-guarded."""
    safe = re.sub(r"[^0-9A-Za-z_.-]", "", name or "")
    if not safe.startswith("weekly_"):
        return None
    p = os.path.join(root, "weekly", safe)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def status(root: str, every_days: int = 7) -> dict:
    lr = last_run(root)
    return {"last_weekly_update": lr, "due_now": due(root, every_days),
            "runs": len(history(root))}


def start_weekly_scheduler(engine, root: str, check_every_s: int = 3600) -> threading.Thread:
    """Start the daemon loop. Runs once on boot if overdue, then hourly checks."""
    def loop() -> None:
        while True:
            try:
                run_if_due(engine, root)
            except Exception:
                pass
            time.sleep(check_every_s)

    t = threading.Thread(target=loop, daemon=True, name="sb-weekly-update")
    t.start()
    return t
