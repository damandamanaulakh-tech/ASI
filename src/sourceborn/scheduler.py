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

Two rules this module keeps, because the whole point of it is that runs survive:
  - **A run is never overwritten.** The file is created with mode ``"x"``, so
    the filesystem itself arbitrates the name. A ``while os.path.exists(...)``
    check was not enough: this app serves requests on threads AND runs a daemon
    thread, so two pulls in the same second could both pass the check and the
    second would silently clobber the first.
  - **A corrupt run never takes a route down.** Every read is guarded. A
    process recycled mid-write leaves a truncated file behind, and ``do_GET``
    has no exception handler, so an unguarded ``json.load`` would drop the
    connection instead of returning an answer.
"""

from __future__ import annotations

import json
import os
import re
import threading
import time
from datetime import datetime, timedelta

_FMT = "%Y-%m-%d %H:%M:%S"
# weekly_<14 digits>.json, or weekly_<14 digits>_<n>.json for same-second runs
_RUN_RE = re.compile(r"^weekly_(\d{1,20})(?:_(\d{1,4}))?\.json$")


def _state_path(root: str) -> str:
    return os.path.join(root, "weekly_update.json")


def _weekly_dir(root: str) -> str:
    d = os.path.join(root, "weekly")
    os.makedirs(d, exist_ok=True)
    return d


def _sort_key(fn: str) -> tuple:
    """Order by stamp, then by the same-second suffix NUMERICALLY — plain
    lexicographic sorting would put `_10` before `_2`."""
    m = _RUN_RE.match(fn)
    if not m:
        return ("", 0)
    return (m.group(1).rjust(20, "0"), int(m.group(2) or 1))


def _run_files(root: str) -> list[str]:
    """Every kept run filename, newest first.

    The filter runs BEFORE any slice: a stray file dropped in the folder must
    not push a real run out of the ledger."""
    try:
        names = os.listdir(os.path.join(root, "weekly"))
    except Exception:
        return []
    keep = [fn for fn in names if _RUN_RE.match(fn)]
    keep.sort(key=_sort_key, reverse=True)
    return keep


def count_runs(root: str) -> int:
    """How many runs are KEPT — counted, never parsed, so it is neither capped
    by a page limit nor slowed by the size of the ledger."""
    return len(_run_files(root))


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
    plus the last-run pointer.

    Every filesystem step is guarded and its failure is REPORTED in the
    result, never raised: by the time we get here 95 brains have already been
    updated and the digest is already written, so raising would drop a request
    whose real work succeeded and invite a duplicate retry."""
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
    stamp = (re.sub(r"[^0-9]", "", at)[:14]
             or datetime.now().strftime("%Y%m%d%H%M%S"))

    fname, fh = f"weekly_{stamp}.json", None
    try:
        d = _weekly_dir(root)
        n = 1
        while True:
            try:
                # "x" = create-or-fail: the filesystem decides, so two threads
                # in the same second get two files instead of one survivor.
                fh = open(os.path.join(d, fname), "x", encoding="utf-8")
                break
            except FileExistsError:
                n += 1
                if n > 999:                         # never spin forever
                    raise RuntimeError("999 runs in one second")
                fname = f"weekly_{stamp}_{n}.json"
        with fh:
            json.dump(result, fh, ensure_ascii=False, indent=2)
    except Exception as exc:
        result["history_error"] = str(exc)[:200]    # reported, not swallowed
        fname = ""
    try:
        state = {"last_run": at}
        if fname:                                   # never point at a file we
            state["latest_file"] = fname            # failed to write
        with open(_state_path(root), "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception as exc:
        result["state_write_error"] = str(exc)[:200]
    try:
        engine.memory.master_log({
            "event": "weekly_run", "file": fname or "(not written)",
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


def history(root: str, limit: int = 52, offset: int = 0) -> list[dict]:
    """A page of past weekly runs, newest first — the accumulated pull ledger.

    Paged, not capped: ``count_runs`` is the true total and ``offset`` reaches
    every older run, so nothing on disk is unreachable through the app."""
    out = []
    limit = max(0, min(int(limit or 0), 500))
    offset = max(0, int(offset or 0))
    for fn in _run_files(root)[offset:offset + limit]:
        try:
            with open(os.path.join(root, "weekly", fn), encoding="utf-8") as f:
                r = json.load(f)
        except Exception:                           # truncated / corrupt run
            out.append({"file": fn, "at": None, "brains": None,
                        "new_connections": None, "candidates": None,
                        "novelty_error": None, "unreadable": True})
            continue
        if not isinstance(r, dict):
            r = {}
        out.append({"file": fn, "at": r.get("at"),
                    "brains": r.get("updated"),
                    "new_connections": (r.get("digest") or {}).get("new_connections"),
                    "candidates": (r.get("novelty") or {}).get("candidates"),
                    "novelty_error": (r.get("novelty") or {}).get("error")})
    return out


def latest(root: str) -> dict | None:
    """The most recent READABLE weekly result, or None if it has never run."""
    for fn in _run_files(root):
        try:
            with open(os.path.join(root, "weekly", fn), encoding="utf-8") as f:
                r = json.load(f)
            if isinstance(r, dict):
                return r
        except Exception:
            continue
    return None


def get_run(root: str, name: str) -> dict | None:
    """One dated weekly file by name, path-guarded. Returns None — never
    raises — for a missing, mis-named, or corrupt file."""
    safe = re.sub(r"[^0-9A-Za-z_.-]", "", name or "")
    if not _RUN_RE.match(safe):
        return None
    try:
        with open(os.path.join(root, "weekly", safe), encoding="utf-8") as f:
            r = json.load(f)
    except Exception:
        return None
    return r if isinstance(r, dict) else None


def state(root: str, every_days: int = 7) -> str:
    """One of three words. Never-run is NOT the same as ran-and-overdue."""
    if not last_run(root):
        return "never run"
    return "overdue" if due(root, every_days) else "current"


def status(root: str, every_days: int = 7) -> dict:
    lr = last_run(root)
    d = due(root, every_days)
    return {"last_weekly_update": lr, "due_now": d,
            "runs": count_runs(root),
            "state": "never run" if not lr else ("overdue" if d else "current")}


def start_weekly_scheduler(engine, root: str, check_every_s: int = 3600) -> threading.Thread:
    """Start the daemon loop. Runs once on boot if overdue, then hourly checks.

    Since Phase E the same hourly check also calls the self-sustain tick —
    in its OWN try, so a tick failure can never kill the weekly pull and a
    pull failure can never kill the tick. The tick is mode-gated and ships
    MANUAL: until he lifts the mode it returns without doing anything."""
    def loop() -> None:
        while True:
            try:
                run_if_due(engine, root)
            except Exception:
                pass
            try:
                from . import autoloop
                autoloop.tick_if_due(root)
            except Exception:
                pass
            time.sleep(check_every_s)

    t = threading.Thread(target=loop, daemon=True, name="sb-weekly-update")
    t.start()
    return t
