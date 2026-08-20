"""Sourceborn web service — a zero-dependency HTTP server (stdlib only).

Runs the engine behind a dark dashboard and a JSON API, so it can be deployed
to Render (or any host) with nothing to install but Python.

    python -m sourceborn.server          # local: http://localhost:8000
    PORT=10000 python -m sourceborn.server

Endpoints:
    GET  /            -> the dashboard UI
    GET  /health      -> model + brain status
    GET  /brains /brain /graph
    GET  /memory/report          -> what is stored in each memory node (live)
    GET  /snapshots /snapshot    -> saved memory snapshots (current vs older)
    POST /ask         -> per-node SB<->URR walk + human review queue
    POST /review      -> approve / add-data / re-loop a held node
    POST /ingest      -> feed text into the brain
    POST /upload      -> review an uploaded file (txt/md/csv/docx/xlsx/pdf)
    POST /snapshot    -> save a memory snapshot
    POST /brains/update /brain/settings

Set ANTHROPIC_API_KEY / XAI_API_KEY / OPENAI_API_KEY (env vars on Render) to turn
on real reasoning. Render's disk is ephemeral; for persistent memory mount a
Render Disk at ``.sourceborn`` or use a DB (docs/RECOMMENDATION.md, Phase 3).
"""

from __future__ import annotations

import base64
import hmac
import json
import os
import re
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from . import asi_pyramid
from . import asipage
from . import generationpage
from . import growth
from . import filemap, growing, intent_ledger, intents, selfmake
from . import artifact
from . import sysmap
from . import subjectbrains
from . import statepacks
from . import weighting
from . import enginepage
from . import exists
from . import ladder
from . import mypage
from . import patterns as patternmem
from . import readingpage
from . import human_registry
from . import senses as sensemem
from . import router as rubric_router
from . import scheduler
from .engine import SourcebornEngine, NO_LIVE
from .extract import extract_text
from .llm import (get_model, model_status, generate_image,
                  CaptureModel, LocalBridgeModel, LocalCaptured)
from .models import _now

SB_ROOT = os.environ.get("SB_ROOT", ".sourceborn")
ENGINE = SourcebornEngine(root=SB_ROOT)
SNAP_DIR = os.path.join(SB_ROOT, "_snapshots")
CHAT_DIR = os.path.join(SB_ROOT, "chats")

# --- the front-door gate ------------------------------------------------
# The whole app is private (audit item 01). If SB_ACCESS_PASS is set, every
# route requires HTTP Basic auth: the browser prompts once natively, fetch()
# reuses the credentials, and curl works with -u. If it is NOT set the app
# stays open — so local dev and the offline demo are unchanged, and nothing
# breaks until the owner deliberately turns the lock on in Render.
SB_ACCESS_USER = os.environ.get("SB_ACCESS_USER", "sourceborn")
SB_ACCESS_PASS = os.environ.get("SB_ACCESS_PASS", "")
# Render's health check hits this with no credentials, so it must stay open.
# It only reports booleans about which keys exist, never private content.
OPEN_PATHS = frozenset({"/health"})


def basic_auth_ok(auth_header: str, user: str, password: str) -> bool:
    """Pure check for an HTTP Basic `Authorization` header, constant-time.
    Kept module-level and side-effect-free so it is unit-tested directly
    (the request handler can't be exercised without a live socket).

    Compares raw bytes, so a non-ASCII password/username can never raise —
    a strong password with an accented character must not brick the app.
    The scheme token is matched case-insensitively per RFC 7617."""
    if not password:                       # no lock configured → app is open
        return True
    scheme, _, rest = auth_header.partition(" ")
    if scheme.lower() != "basic" or not rest:
        return False
    try:
        raw = base64.b64decode(rest)       # bytes, not decoded to str
    except Exception:
        return False
    got_user, sep, got_pass = raw.partition(b":")
    if not sep:                            # malformed, no colon
        return False
    ok_user = hmac.compare_digest(got_user, user.encode("utf-8"))
    ok_pass = hmac.compare_digest(got_pass, password.encode("utf-8"))
    return ok_user and ok_pass


def _save_chat(question: str, payload: dict, kind: str = "ask") -> str:
    """Persist one full exchange to disk — every chat is stored and can be
    reopened later with its complete walk, holds, and node findings."""
    os.makedirs(CHAT_DIR, exist_ok=True)
    cid = re.sub(r"[^0-9]", "", _now()) + "-" + str(len(os.listdir(CHAT_DIR)) % 1000)
    o = payload.get("output") or {}
    rec = {"id": cid, "at": _now(), "kind": kind, "question": question[:400],
           "model": payload.get("model", ""), "answer": (o.get("answer") or "")[:800],
           "confidence": o.get("confidence", ""),
           "classification": o.get("classification", ""),
           "hold_count": (payload.get("walk") or {}).get("hold_count", 0),
           "node_count": (payload.get("walk") or {}).get("node_count", 0),
           "payload": payload}
    with open(os.path.join(CHAT_DIR, cid + ".json"), "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False)
    ENGINE.memory.master_log({"event": "chat_stored", "chat": cid, "kind": kind})
    return cid


def _list_chats(limit: int = 60) -> list[dict]:
    if not os.path.isdir(CHAT_DIR):
        return []
    out = []
    for fn in sorted(os.listdir(CHAT_DIR), reverse=True)[:limit]:
        if not fn.endswith(".json"):
            continue
        try:
            with open(os.path.join(CHAT_DIR, fn), encoding="utf-8") as f:
                d = json.load(f)
            out.append({k: d.get(k, "") for k in
                        ("id", "at", "kind", "question", "model", "confidence",
                         "classification", "hold_count", "node_count")})
        except Exception:
            continue
    return out


def _get_chat(cid: str) -> dict | None:
    fp = os.path.join(CHAT_DIR, re.sub(r"[^0-9-]", "", cid) + ".json")
    if not os.path.exists(fp):
        return None
    with open(fp, encoding="utf-8") as f:
        return json.load(f)


def _export_brain() -> bytes:
    """The whole brain as one zip — brains, chats, master log, persona, wisdom,
    snapshots. "It must store data, always n keep forever": even on a host with
    an ephemeral disk, the user can download the full state and restore it."""
    import io
    import zipfile
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _dirs, files in os.walk(SB_ROOT):
            for fn in files:
                p = os.path.join(base, fn)
                z.write(p, os.path.relpath(p, SB_ROOT))
    return buf.getvalue()


def _import_brain(b64: str) -> dict:
    """Restore a previously exported brain zip into SB_ROOT (merge/overwrite)."""
    import io
    import zipfile
    raw = base64.b64decode(b64)
    if len(raw) > 200 * 1024 * 1024:
        return {"error": "backup too large"}
    n = 0
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for info in z.infolist():
            name = info.filename
            if name.startswith("/") or ".." in name or info.is_dir():
                continue
            dest = os.path.join(SB_ROOT, name)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as f:
                f.write(z.read(info))
            n += 1
    ENGINE.memory._brains.clear()          # drop cached metas; reload from disk
    ENGINE.persona._load()
    ENGINE.memory.master_log({"event": "brain_restored", "files": n})
    return {"ok": True, "files_restored": n}


def _persist_status() -> dict:
    """How much history this brain holds and since when — so data loss from an
    unmounted disk is visible immediately, not discovered weeks later."""
    oldest = ""
    p = ENGINE.memory.master_log_path
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            first = f.readline().strip()
        try:
            oldest = json.loads(first).get("at", "")
        except Exception:
            oldest = ""
    chats = len(os.listdir(CHAT_DIR)) if os.path.isdir(CHAT_DIR) else 0
    return {"root": SB_ROOT, "oldest_record": oldest, "chats": chats,
            **ENGINE.memory.stats()}


def _master_log_tail(n: int = 40) -> list[dict]:
    """The sacred Master Log, newest first — every write, merge, human decision."""
    p = ENGINE.memory.master_log_path
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        lines = f.readlines()[-n:]
    out = []
    for ln in reversed(lines):
        try:
            out.append(json.loads(ln))
        except Exception:
            continue
    return out


def _ingest_text(name: str, text: str, category: str = "") -> dict:
    """Feed one note/file into the brain — pyramid-filed and voice-learned
    ("when I add"). Persists to the corpus folder on disk if SB_INGEST_CORPUS is
    set (e.g. a Render disk) so it survives restarts."""
    from .ingest import ingest_text_entry
    res = ingest_text_entry(ENGINE.memory, ENGINE.persona, name, text,
                            category=category, origin=f"upload:{name}",
                            unfiled=ENGINE.unfiled)
    folder = os.environ.get("SB_INGEST_CORPUS")
    if folder:
        d = os.path.join(folder, category) if category else folder
        os.makedirs(d, exist_ok=True)
        safe = re.sub(r"[^A-Za-z0-9._-]", "_", name) or "note"
        with open(os.path.join(d, safe + ".txt"), "w", encoding="utf-8") as f:
            f.write(text)
    return {"memory": ENGINE.memory.stats(),
            "examples": len(ENGINE.persona.examples), "filed": res}


def _library(preview: int = 160) -> dict:
    """List the files/notes fed into the brain — the user's 'library'."""
    items = []
    folder = os.environ.get("SB_INGEST_CORPUS")
    if folder and os.path.isdir(folder):
        for fn in sorted(os.listdir(folder)):
            p = os.path.join(folder, fn)
            if os.path.isfile(p):
                try:
                    t = open(p, encoding="utf-8", errors="ignore").read()
                except Exception:
                    t = ""
                items.append({"name": fn, "chars": len(t), "preview": t[:preview]})
    if not items:                       # fallback: the clone's learned examples
        for ex in list(getattr(ENGINE.persona, "examples", []))[-50:]:
            items.append({"name": getattr(ex, "question", "note"),
                          "chars": len(getattr(ex, "answer", "") or ""),
                          "preview": (getattr(ex, "answer", "") or "")[:preview]})
    return {"files": items, "count": len(items),
            "folder": folder or "(in-memory — set SB_INGEST_CORPUS to persist files)"}


def _memory_report(limit: int = 3) -> dict:
    """A snapshot of what each memory node holds — counts, last update, and the
    most recent entries (so the user can see exactly what was added, and compare
    to older snapshots)."""
    mem = ENGINE.memory
    bdir = os.path.join(mem.root, "brains")
    nodes = []
    if os.path.isdir(bdir):
        for nid in sorted(os.listdir(bdir)):
            b = mem.brain(nid)
            if b.meta.get("entry_count", 0) == 0:
                continue
            cfg = ENGINE.brains.get(nid)
            entries = b.read_all()
            recent = [{"content": (e.content or "")[:180], "tags": e.tags,
                       "evidence_tag": e.evidence_tag, "classification": e.classification}
                      for e in entries[-limit:]]
            nodes.append({"id": nid, "name": (cfg.name if cfg else b.meta.get("name", "")),
                          "entry_count": b.meta.get("entry_count", len(entries)),
                          "last_update": b.meta.get("last_update", ""),
                          "recent": recent})
    return {"at": _now(), "totals": mem.stats(), "nodes": nodes}


def _int_arg(qs: dict, name: str, default: int, lo: int, hi: int) -> int:
    """A query integer that cannot raise. `do_GET` has no exception handler,
    so an `int('abc')` here would drop the connection instead of answering."""
    try:
        v = int((qs.get(name) or [str(default)])[0])
    except Exception:
        return default
    return max(lo, min(v, hi))


def _weekly_phrase(st: dict) -> str:
    """One honest sentence for the weekly pull — three states, not two.
    Never run is NOT the same as ran-and-overdue, and the old two-state
    pill collapsed both into 'due'.

    This is the ONLY place the label is composed. The pill, the panel and the
    MY PAGE row all display what the server sends; none of them re-derives it,
    because the same rule written three times in two languages is a rule that
    will eventually disagree with itself."""
    lr = st.get("last_weekly_update")
    if not lr:
        return "never run"
    return ("overdue — last " + str(lr) if st.get("due_now")
            else "current — last " + str(lr))


def _page_feeds() -> dict:
    """Resolve every live WHAT for MY PAGE in one call. His-owned sources
    (text, links) live inside the layout itself and are not resolved here."""
    feeds: dict = {}
    try:
        n_brains = len(ENGINE.brains.all())
        w = scheduler.status(SB_ROOT)
        # the weekly row said nothing for months because it read a key the
        # scheduler never returned. It now says the truth in three states.
        feeds["health"] = {"rows": [
            ["model", ENGINE.model.name],
            ["brains", str(n_brains)],
            ["weekly", _weekly_phrase(w)],
            ["weekly runs kept", str(w.get("runs", 0))]],
            "number": n_brains, "label": "node brains"}
    except Exception as e:
        feeds["health"] = {"rows": [["error", str(e)[:80]]]}
    try:
        t = _memory_report(limit=1).get("totals", {})
        feeds["memory"] = {"rows": [[str(k), str(v)] for k, v in
                                    list(t.items())[:8]],
                           "number": sum(v for v in t.values()
                                         if isinstance(v, int)),
                           "label": "entries kept — nothing deleted"}
    except Exception as e:
        feeds["memory"] = {"rows": [["error", str(e)[:80]]]}
    try:
        feeds["chats"] = {"rows": [[c.get("question", ""),
                                    c.get("confidence", ""),
                                    f"holds {c.get('hold_count', 0)}"]
                                   for c in _list_chats(10)],
                          "label": "last chats"}
    except Exception as e:
        feeds["chats"] = {"rows": [["error", str(e)[:80]]]}
    try:
        items = _library().get("items", [])
        feeds["library"] = {"rows": [[i.get("name", ""),
                                      f"{i.get('chars', 0)} chars"]
                                     for i in items[:12]],
                            "number": len(items), "label": "files in the library"}
    except Exception as e:
        feeds["library"] = {"rows": [["error", str(e)[:80]]]}
    feeds["brains"] = {"number": len(ENGINE.brains.all()),
                       "label": "node brains — the MEMORY; the seven filters are the METHOD"}
    feeds["ladder"] = {"rows": [list(r) for r in mypage.LADDER_ROWS],
                       "number": "3,072", "label": "parameters · Phase-1 done"}
    feeds["filters"] = {"rows": mypage.FILTERS, "number": 7,
                        "label": "in order, every finding, every time"}
    feeds["routes"] = {"rows": mypage.ROUTES, "number": 11,
                       "label": "route registry v1 — non-exhaustive"}
    feeds["phases"] = {"rows": mypage.PHASES}
    feeds["open"] = {"rows": mypage.OPEN_ITEMS, "number": len(mypage.OPEN_ITEMS),
                     "label": "open on his word"}
    return feeds


def _save_snapshot(name: str = "") -> dict:
    os.makedirs(SNAP_DIR, exist_ok=True)
    rep = _memory_report()
    sid = re.sub(r"[^0-9A-Za-z]", "", rep["at"])[:14] or str(len(os.listdir(SNAP_DIR)))
    rep["name"] = name.strip() or f"snapshot {sid}"
    rep["id"] = sid
    with open(os.path.join(SNAP_DIR, sid + ".json"), "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False)
    return {"ok": True, "id": sid, "name": rep["name"], "total": rep["totals"]}


def _list_snapshots() -> list[dict]:
    if not os.path.isdir(SNAP_DIR):
        return []
    out = []
    for fn in sorted(os.listdir(SNAP_DIR), reverse=True):
        if fn.endswith(".json"):
            try:
                with open(os.path.join(SNAP_DIR, fn), encoding="utf-8") as f:
                    d = json.load(f)
                out.append({"id": d.get("id", fn[:-5]), "name": d.get("name", fn),
                            "at": d.get("at", ""), "total": d.get("totals", {})})
            except Exception:
                continue
    return out


PAGE = r"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Sourceborn</title><style>
:root{
 --bg:#070809;--panel:#0f1219;--panel2:#0b0e14;--elev:#141826;
 --line:#1c2230;--line2:#262d3d;--ink:#eef2f8;--mut:#7d8699;--mut2:#5b6477;
 --acc:#7c8bff;--ok:#34d399;--warn:#fbbf24;--bad:#f87171;--hl:#ffb454;--gd:#7ee787;
 --grad:linear-gradient(135deg,#7c8bff,#a78bfa 60%,#f0abfc);
 --shadow:0 14px 36px -16px rgba(0,0,0,.75);--ring:0 0 0 3px rgba(124,139,255,.25)}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;color:var(--ink);font:15px/1.55 'Inter',-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;
 -webkit-font-smoothing:antialiased;
 background:radial-gradient(900px 520px at 85% -8%,rgba(124,139,255,.14),transparent 60%),
 radial-gradient(720px 520px at 0 0,rgba(167,139,250,.10),transparent 55%),var(--bg)}
::selection{background:rgba(124,139,255,.3)}
::-webkit-scrollbar{width:10px;height:10px}
::-webkit-scrollbar-thumb{background:var(--line2);border-radius:10px;border:2px solid transparent;background-clip:padding-box}
.app{max-width:1240px;margin:0 auto;padding:0 18px 60px}
.topbar{position:sticky;top:0;z-index:20;display:flex;justify-content:space-between;align-items:center;gap:12px;
 padding:14px 4px;margin-bottom:8px;flex-wrap:wrap;
 backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
 background:linear-gradient(180deg,rgba(7,8,9,.86),rgba(7,8,9,.35));border-bottom:1px solid var(--line)}
.brand{display:flex;gap:12px;align-items:center}
.logo{width:38px;height:38px;border-radius:11px;background:var(--grad);display:grid;place-items:center;overflow:hidden;
 box-shadow:0 6px 18px -6px rgba(124,139,255,.6)}
.logo img{width:38px;height:38px;object-fit:cover;display:block}
.brand .name{font-size:18px;font-weight:700;letter-spacing:-.01em}
.brand .tag{font-size:12px;color:var(--mut)}
.stats{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.pill{display:inline-flex;gap:7px;align-items:center;background:var(--panel);border:1px solid var(--line);
 border-radius:999px;padding:6px 12px;font-size:12.5px;color:var(--mut)}
.pill b{color:var(--ink);font-weight:600}
.pdot{width:8px;height:8px;border-radius:50%;background:var(--mut2)}
.pdot.live{background:var(--ok);box-shadow:0 0 0 3px rgba(52,211,153,.18)}
.grid{display:grid;grid-template-columns:300px 1fr;gap:18px;align-items:start}
@media(max-width:880px){.grid{grid-template-columns:1fr}}
.card{background:linear-gradient(180deg,var(--panel),var(--panel2));border:1px solid var(--line);
 border-radius:16px;padding:18px;margin:0 0 16px;box-shadow:var(--shadow);transition:border-color .15s}
.card:hover{border-color:var(--line2)}.side .card{padding:14px}
.k{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--mut);
 margin:0 0 11px;display:flex;align-items:center;gap:8px}.k .num{margin-left:auto;color:var(--mut2)}
.side .acc{margin:0 0 10px}
.side .acc>summary{font-size:11px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:var(--ink);
 padding:9px 0;border-bottom:1px solid var(--line)}
.side .sec{padding:11px 2px 4px}
.hero{padding:6px;background:linear-gradient(180deg,var(--elev),var(--panel2));border-color:var(--line2)}
.hero .inner{background:var(--panel2);border:1px solid var(--line);border-radius:13px;padding:14px}
textarea,input,select{font:inherit;color:var(--ink)}
#q{width:100%;background:transparent;border:0;color:var(--ink);min-height:84px;resize:vertical;outline:none;font-size:16px;line-height:1.5}
#q::placeholder{color:var(--mut2)}
.toolbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:10px;padding-top:12px;border-top:1px solid var(--line)}
.field{display:inline-flex;gap:7px;align-items:center;background:var(--panel);border:1px solid var(--line);
 border-radius:10px;padding:0 10px;height:38px;color:var(--mut);font-size:13px}
.field select,.field input{background:transparent;border:0;outline:none;color:var(--ink);font-size:13px}
.field:focus-within{border-color:var(--acc);box-shadow:var(--ring)}
button.primary{height:38px;padding:0 18px;border:0;border-radius:10px;background:var(--grad);color:#0a0f1f;
 font-weight:700;font-size:14px;cursor:pointer;display:inline-flex;gap:8px;align-items:center;
 box-shadow:0 8px 20px -8px rgba(124,139,255,.7);transition:.15s}
button.primary:hover{filter:brightness(1.08);transform:translateY(-1px)}
button.primary:disabled{opacity:.6;cursor:default;transform:none}
.btn{height:34px;padding:0 13px;border:1px solid var(--line2);border-radius:9px;background:var(--panel);
 color:var(--ink);font-weight:600;font-size:13px;cursor:pointer;transition:.15s}
.btn:hover{border-color:var(--acc);color:#fff}.btn.sm{height:30px;padding:0 10px;font-size:12px}
.iconbtn{width:38px;height:38px;border:1px solid var(--line);border-radius:10px;background:var(--panel);
 color:var(--ink);cursor:pointer;font-size:15px}.iconbtn:hover{border-color:var(--acc)}.iconbtn.on{color:var(--bad);border-color:var(--bad)}
.switch{display:inline-flex;gap:9px;align-items:center;cursor:pointer;color:var(--mut);font-size:13px;user-select:none}
.switch input{display:none}
.switch .track{width:38px;height:22px;border-radius:999px;background:var(--line2);position:relative;transition:.18s;flex:none}
.switch .track:after{content:"";position:absolute;top:2px;left:2px;width:18px;height:18px;border-radius:50%;background:#cfd6e6;transition:.18s}
.switch input:checked+.track{background:var(--acc)}
.switch input:checked+.track:after{transform:translateX(16px);background:#fff}
.spin{display:inline-block;width:15px;height:15px;border:2px solid rgba(10,15,31,.35);
 border-top-color:#0a0f1f;border-radius:50%;animation:sp .7s linear infinite}
@keyframes sp{to{transform:rotate(360deg)}}
.status{color:var(--mut);font-size:13px}
.chips{display:flex;gap:8px;flex-wrap:wrap;padding:12px 8px 6px}
.chip{font-size:12.5px;color:var(--mut);background:var(--panel);border:1px solid var(--line);
 border-radius:999px;padding:6px 12px;cursor:pointer;transition:.15s}
.chip:hover{border-color:var(--acc);color:var(--ink)}
.ans{white-space:pre-wrap;font-size:15.5px;line-height:1.65}
.badges{display:flex;gap:7px;flex-wrap:wrap;margin-top:12px}
.badge{display:inline-flex;gap:6px;align-items:center;font-size:12px;border-radius:999px;padding:4px 11px;
 background:var(--panel);border:1px solid var(--line);color:var(--mut)}
.badge b{color:var(--ink);font-weight:600}
.badge.ok{border-color:rgba(52,211,153,.4);color:#9ff0d0}
.badge.warn{border-color:rgba(251,191,36,.4);color:#ffe2a3}
.badge.bad{border-color:rgba(248,113,113,.4);color:#ffc4c4}
.meter{height:6px;border-radius:999px;background:var(--line);overflow:hidden;margin:12px 0 4px}
.meter>i{display:block;height:100%;border-radius:999px;background:var(--grad);transition:width .4s}
.lane{border-left:2px solid var(--line2);padding:4px 0 4px 13px;margin:8px 0;color:var(--ink)}
.lane b{color:#cdd5e6}
.fals{margin-top:10px;color:var(--mut);font-size:13.5px;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:9px 12px}
.why{margin-top:11px;font-size:13.5px;color:#ffe2a3;background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.32);border-radius:10px;padding:9px 12px}
.vd{font-size:11px}.vd.pass{color:var(--ok)}.vd.hold{color:var(--warn)}
.memok{font-size:11px;color:var(--gd);margin-left:6px}
.hold{border:1px solid var(--line);background:var(--panel);border-radius:11px;padding:12px;margin:9px 0}
.fivew{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;margin:8px 0;font-size:12.5px;color:var(--mut)}
.fivew b{color:var(--acc);font-weight:600;margin-right:5px}
.hactions{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}
.tag{display:inline-block;background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:2px 10px;margin:3px 4px 0 0;font-size:12px;color:var(--mut)}
.hl{color:var(--hl)}.gd{color:var(--gd)}.muted{color:var(--mut)}
.pyr{display:flex;flex-direction:column;gap:5px;align-items:center}
.plvl{border:1px solid var(--line);background:var(--panel);border-radius:9px;padding:6px 8px;text-align:center;
 font-size:11px;color:var(--mut);transition:.25s;width:100%}
.plvl.on{border-color:var(--acc);background:linear-gradient(180deg,rgba(124,139,255,.18),rgba(124,139,255,.06));
 color:var(--ink);box-shadow:0 0 18px -6px rgba(124,139,255,.5)}
.mem{display:flex;flex-direction:column;gap:9px}
.memrow{display:flex;gap:10px;align-items:center;font-size:13px;color:var(--mut)}
.memrow b{color:var(--ink);font-weight:600}
.md{width:9px;height:9px;border-radius:50%;flex:none}
.md.r{background:#7c8bff}.md.i{background:#34d399}.md.e{background:#ffb454}
.hist a{display:block;color:var(--mut);font-size:13px;padding:8px 0;border-bottom:1px solid var(--line);
 cursor:pointer;text-decoration:none;transition:.12s}.hist a:last-child{border-bottom:0}
.hist a:hover{color:var(--ink);padding-left:4px}
.in{width:100%;background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:9px 11px;outline:none;font:inherit;color:var(--ink)}
.in:focus{border-color:var(--acc);box-shadow:var(--ring)}.in::placeholder{color:var(--mut2)}
.rep{font-size:12.5px}.repn{border:1px solid var(--line);border-radius:10px;padding:9px 11px;margin:7px 0;background:var(--panel)}
.repn .h{display:flex;justify-content:space-between;color:var(--ink);font-weight:600}
.repn .e{color:var(--mut);margin-top:4px;border-top:1px dashed var(--line);padding-top:4px}
details summary{cursor:pointer;color:var(--mut);font-size:13px;padding:4px 0;list-style:none}
details summary::-webkit-details-marker{display:none}
details summary:before{content:"\25b8  ";color:var(--mut2)}
details[open]>summary:before{content:"\25be  "}
.bset{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:10px 0}
.bset select{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:6px 8px;color:var(--ink)}
.trace{font:12px/1.7 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--mut);white-space:pre-wrap;word-break:break-word}
.fade{animation:fade .35s ease}@keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
</style></head><body><div class=app>

<header class=topbar>
  <div class=brand>
    <div class=logo><img src="https://avatars.githubusercontent.com/u/284725680?v=4" alt="" onerror="this.remove()"></div>
    <div><div class=name>Sourceborn</div><div class=tag>eternal example &middot; present fact &middot; more parameters, more outcome</div></div>
  </div>
  <div class=stats>
    <span class=pill id=mpill><span class=pdot id=pdot></span> <b id=mname>offline</b></span>
    <span class=pill>brains <b id=bpill>95</b></span>
    <span class=pill id=wpill>weekly <b>&mdash;</b></span>
    <span class=pill id=ppill title="stored memory — if this resets after a deploy, mount a persistent disk at .sourceborn">memory <b>&mdash;</b></span>
  </div>
</header>

<div class=grid>
<!-- LEFT: read-only — history + library (memories, pyramid, reports, node brains) -->
<nav class=side>
  <div class=card><div class=k>His pages</div>
    <div class=hactions style="margin-top:6px;display:flex;gap:8px;flex-wrap:wrap">
      <a class="btn sm" href="/engine">⚙ THE ENGINE — ask &amp; watch the ladder</a>
      <a class="btn sm" href="/page">▦ MY PAGE — what · where · how</a>
      <a class="btn sm" href="/reading">◉ THE READING — split · match · route · correct</a>
      <a class="btn sm" href="/exists">◈ WHAT EXISTS — your understanding, in the code</a>
    </div></div>
  <div class=card><div class=k>Chats &middot; stored <span class=num id=chatn></span></div><div class=hist id=hist><span class=muted>empty</span></div></div>
  <div class=card>
    <details class=acc open><summary>Library</summary>
      <div class=sec>
        <div class=k>Three memories</div>
        <div class=mem>
          <div class=memrow><span class="md r"></span><div><b>Reflex</b> &middot; your corpus &amp; clone</div></div>
          <div class=memrow><span class="md i"></span><div><b>Instinct</b> &middot; wisdom bank</div></div>
          <div class=memrow><span class="md e"></span><div><b>Eyes</b> &middot; live fact</div></div>
        </div>
      </div>
      <details class=acc><summary>Engine pyramid</summary><div class=sec><div class=pyr id=pyr></div></div></details>
      <details class=acc><summary>Interconnection</summary><div class=sec>
        <div class=hactions><button class="btn sm" onclick=drawInterGraph()>Open graph (K&#8329;&#8325;)</button></div>
        <div class=muted style="font-size:11px;margin-top:6px">every point can connect to every other point — Principle 8</div>
      </div></details>
      <details class=acc><summary>Reports &amp; snapshots</summary><div class=sec>
        <div class=hactions><button class="btn sm" onclick=loadReport()>Memory report</button>
          <button class="btn sm" onclick=saveSnapshot()>Save snapshot</button>
          <button class="btn sm" onclick=loadMasterLog()>Master log</button>
          <button class="btn sm" onclick=loadUnfiled()>Unfiled</button>
          <button class="btn sm" onclick=runNovelty()>Novelty pass</button>
          <button class="btn sm" onclick=loadWeekly()>Weekly pull</button></div>
        <div class=hactions style="margin-top:6px"><a class="btn sm" href="/export" download>⬇ Backup brain</a>
          <label class="btn sm" style="display:inline-flex;align-items:center;cursor:pointer">⬆ Restore<input type=file id=restorefile accept=".zip" style="display:none" onchange=restoreBrain()></label></div>
        <div class=status id=repstat style="margin-top:6px"></div>
        <div id=snaps style="margin-top:6px"></div>
      </div></details>
      <details class=acc><summary>Node brains (<span id=bcount>0</span>)</summary><div class=sec>
        <div class=hactions><button class="btn sm" onclick=weeklyUpdate()>Weekly update</button><span class=status id=bstat></span></div>
        <div id=brains style="margin-top:6px"></div>
      </div></details>
      <details class=acc><summary>Files (<span id=lcount>0</span>)</summary><div class=sec>
        <div class=hactions><button class="btn sm" onclick=loadLibrary()>Refresh</button><span class=status id=lstat></span></div>
        <div id=libfiles style="margin-top:6px"></div>
      </div></details>
    </details>
  </div>
</nav>

<!-- RIGHT: editable — ask, answer, review queue, feed the brain -->
<main>
  <section class="card hero">
    <div class=inner>
      <textarea id=q placeholder="Ask anything — a question, a mess, a half-thought…   ⌘/Ctrl + Enter to run"></textarea>
      <div class=toolbar>
        <button id=go class=primary onclick=ask()><span id=goico>&#9654;</span><span id=golbl>Run engine</span></button>
        <button class=iconbtn id=mic title="voice to text" onclick=dictate()>&#127908;</button>
        <span class=field><select id=model title="base model"></select></span>
        <span class=field id=localwrap style="display:none"><select id=localmodel title="on-device model — runs on your GPU, nothing leaves your machine"></select></span>
        <label class=switch title="keep the thread — fold the last answer into the next ask"><input type=checkbox id=cont checked><span class=track></span> continue thread</label>
        <span class=status id=status></span>
      </div>
      <div class=toolbar style="border:0;padding-top:8px">
        <span class=field><input type=file id=file multiple></span>
        <button class=btn onclick=doUpload()>Review file</button>
        <button class=btn onclick=genImage()>Generate image</button>
        <span class=status id=ustat></span>
      </div>
    </div>
    <div class=chips id=examples></div>
  </section>
  <div id=out></div>
  <div class=card><div class=k>Feed the brain</div>
    <input id=fname class=in placeholder="name (optional)" style="margin-bottom:7px">
    <textarea id=ftext class=in placeholder="paste a note, thought, or core…" style="min-height:60px;resize:vertical"></textarea>
    <div class=toolbar style="border:0;padding:0;margin-top:9px"><button class=btn onclick=feed()>Add to memory</button><span class=status id=fstat></span></div>
  </div>
</main>
</div>

<style>#model option,select option{color:#0b1020;background:#fff}#model option:disabled,select option:disabled{color:#9aa3b2}</style>
<script>
const STAGES=[["1","Foundation & Intake"],["2","Human Core"],["3","Truth & Doubt"],["4","Evidence"],
["5","Connection & Memory"],["6","Synthetic & Invention"],["7","Risk & Control"],["8","Output & Update"]];
const EXAMPLES=[];
// On-device models (run in the browser on the user's own GPU via WebLLM). IDs
// come from WebLLM's prebuilt list; the engine still wraps every answer.
const LOCAL_MODELS=[
  ['Llama-3.2-1B-Instruct-q4f16_1-MLC','Llama 3.2 1B · fast (~0.9 GB)'],
  ['Qwen2-0.5B-Instruct-q4f32_1-MLC','Qwen2 0.5B · fastest (~0.6 GB)'],
  ['Phi-3-mini-4k-instruct-q4f16_1-MLC','Phi-3 mini · stronger (~2.2 GB)'],
  ['Gemma-2B-it-q4f32_1-MLC','Gemma 2B · alt (~1.4 GB)'],
];
function stageOf(id){let n=parseInt((id||'').replace('SB-',''));if(!n)return 0;
  return n<=8?1:n<=18?2:n<=28?3:n<=36?4:n<=44?5:n<=52?6:n<=60?7:8}
function esc(s){return (s||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
function confClass(c){c=(''+c).toLowerCase();return c=='high'?'ok':c=='medium'?'warn':c=='low'?'bad':''}
function confPct(c){c=(''+c).toLowerCase();return c=='high'?92:c=='medium'?62:c=='low'?32:50}
let HIST=JSON.parse(localStorage.getItem('sb_hist')||'[]');
let LASTQ='',LASTD=null,LASTANS='',THREAD=[];

const HASGPU=!!(navigator.gpu);
fetch('/health').then(r=>r.json()).then(d=>{
  const sel=document.getElementById('model');
  const labels={offline:'Offline (no key)',claude:'Claude (deep)',grok:'Grok (raw)',openai:'OpenAI',openrouter:'OpenRouter',local:'Local — private (your GPU)'};
  for(const [k,ok] of Object.entries(d.models)){
    const o=document.createElement('option');o.value=k;
    let lab=labels[k]||k;
    if(k==='local'){ lab+=HASGPU?'':' — needs WebGPU'; if(!HASGPU)o.disabled=true; }
    else { lab+=(ok?'':' — add key'); if(!ok&&k!=='offline')o.disabled=true; }
    o.textContent=lab;
    if(k===d.model)o.selected=true;sel.appendChild(o);
  }
  sel.addEventListener('change',syncLocalUI); syncLocalUI();
  document.getElementById('mname').textContent=(labels[d.model]||d.model).split(' ')[0];
  if(d.model!=='offline')document.getElementById('pdot').classList.add('live');
  document.getElementById('bpill').textContent=d.brains||95;
  // three states, not two: never run / overdue / current. The old pill said
  // "active" the moment a single run existed, even months stale. The label is
  // composed server-side (_weekly_phrase) — never re-derived here.
  drawWpill(d.weekly||{},d.weekly_phrase||'');
});
fetch('/persist').then(r=>r.json()).then(p=>{
  const el=document.getElementById('ppill'); if(!el)return;
  el.innerHTML='memory <b>'+(p.total_memory_entries||0)+'</b>'+(p.oldest_record?' <span class=muted>since '+esc(p.oldest_record.slice(0,10))+'</span>':'');
}); drawPyr(new Set(),{}); drawHist(); loadLibrary(); initLocalPicker();
document.getElementById('examples').innerHTML=EXAMPLES.map(e=>'<span class=chip>'+esc(e)+'</span>').join('');
document.querySelectorAll('#examples .chip').forEach((c,i)=>c.onclick=()=>{
  const q=document.getElementById('q');q.value=EXAMPLES[i];q.focus()});

// HIS FRAME: 1 - 10 - 8 - 40. He quit 70-25 and it was still rendering here —
// that was the defect he caught. This draws HIS ladder, and it fills from the
// Human Functional Registry (his own document), not from a hardcoded list.
var FRAME=null, LITSEG=null;   // var: drawPyr() is called from the boot sequence above this line
function drawPyr(firedStages,counts){
  const el=document.getElementById('pyr'); if(!el)return;
  if(!FRAME){ el.innerHTML='<span class=muted>loading his registry…</span>';
    fetch('/registry').then(r=>r.json()).then(d=>{FRAME=d; drawPyr(firedStages,counts);})
      .catch(()=>{el.innerHTML='<span class=muted>registry unavailable</span>';}); return; }
  const f=FRAME.stats||{}, segs=FRAME.segments||[];
  const lit=LITSEG||{};
  let html='<div class=plvl style="width:100%" title="one functional system">'+
    'SYSTEM · 1 <span class=muted>ASI</span></div>';
  const wmax=100, wmin=46;
  segs.forEach((sg,i)=>{
    const n=lit[sg.id]||0, w=wmin+(wmax-wmin)*(1-i/Math.max(1,segs.length-1));
    html+='<div class="plvl'+(n?' on':'')+'" style="width:'+w+'%" title="'+esc(sg.name)+'">'+
      esc(sg.id)+' '+esc(sg.name)+' <span class=muted>'+sg.containers+' containers · '+
      sg.parameters+'</span>'+(n?' <b>· '+n+' fired</b>':'')+'</div>';
  });
  html+='<div class=plvl style="width:100%;opacity:.7">'+
    (f.containers||80)+' CONTAINERS · '+(f.parameters||3204)+' NAMED SUB-PARAMETERS'+
    ' <span class=muted>1 - 10 - 8 - 40</span></div>'+
    '<div class=plvl style="width:100%;opacity:.55">'+(f.universal_filters||40)+
    ' universal filters · '+(f.operating_states||12)+' states · '+
    (f.failure_classes||20)+' failure classes · '+(f.operating_chain||30)+
    '-step chain</div>';
  el.innerHTML=html;
}
async function drawHist(){
  const h=document.getElementById('hist');
  try{
    const list=await (await fetch('/chats')).json();
    const n=document.getElementById('chatn'); if(n)n.textContent=list.length||'';
    if(list.length){
      h.innerHTML=list.slice(0,20).map(c=>'<a onclick="openChat(\''+esc(c.id)+'\')">'+esc((c.question||'').slice(0,56))+'<br><span class=muted style="font-size:11px">'+esc((c.at||'').slice(5,16))+' · '+esc(c.model||'')+' · '+esc(c.confidence||'')+(c.hold_count?' · '+c.hold_count+' held':'')+'</span></a>').join('');
      return;
    }
  }catch(e){}
  h.innerHTML=HIST.length?HIST.slice(0,12).map((q,i)=>`<a onclick="document.getElementById('q').value=${JSON.stringify(q).replace(/"/g,'&quot;')}">${esc(q.slice(0,60))}</a>`).join(''):'<span class=muted>empty — every ask is stored here</span>';
}
async function openChat(id){        // reopen a stored chat with its full walk
  try{const d=await (await fetch('/chat?id='+encodeURIComponent(id))).json();
    if(d&&d.payload){LASTQ=d.question||'';
      const q=document.getElementById('q'); if(q)q.value=d.question||'';
      render(d.payload); window.scrollTo({top:0,behavior:'smooth'});}
  }catch(e){}
}
function busy(on){
  const go=document.getElementById('go'),ic=document.getElementById('goico'),lb=document.getElementById('golbl');
  go.disabled=on; lb.textContent=on?'Running…':'Run engine';
  ic.className=on?'spin':''; ic.innerHTML=on?'':'&#9654;';
  document.getElementById('status').textContent=on?'running SB + URR…':'';
}
function ctx(){ if(!document.getElementById('cont').checked) return '';
  return THREAD.slice(-3).map(t=>'You asked: '+t.q+'\nReply was: '+t.a).join('\n\n'); }
function initLocalPicker(){
  const lm=document.getElementById('localmodel'); if(!lm)return;
  const saved=localStorage.getItem('sb_local_model')||LOCAL_MODELS[0][0];
  lm.innerHTML=LOCAL_MODELS.map(([v,t])=>'<option value="'+v+'">'+esc(t)+'</option>').join('');
  lm.value=saved; if(lm.value!==saved)lm.value=LOCAL_MODELS[0][0];
  lm.addEventListener('change',()=>localStorage.setItem('sb_local_model',lm.value));
}
function syncLocalUI(){
  const isLocal=document.getElementById('model').value==='local';
  const w=document.getElementById('localwrap'); if(w)w.style.display=isLocal?'':'none';
}
function waitForLocal(ms){            // the WebLLM module loads async — give it a moment
  return new Promise((res,rej)=>{
    if(window.__localLLM)return res();
    let t=0; const iv=setInterval(()=>{
      if(window.__localLLM){clearInterval(iv);res();}
      else if((t+=100)>=ms){clearInterval(iv);rej(new Error('on-device engine library still loading — try again in a moment'));}
    },100);
  });
}
async function ensureLocalModel(){
  if(!navigator.gpu)throw new Error('this browser has no WebGPU — use Chrome/Edge 121+ or Safari 18+');
  await waitForLocal(8000);
  const st=document.getElementById('status');
  await window.__localLLM.load(p=>{
    const pct=Math.round(((p&&p.progress)||0)*100);
    st.textContent=(p&&p.text)?('on-device model · '+p.text):('loading on-device model… '+pct+'%');
  });
}
async function askLocal(q){
  const st=document.getElementById('status');
  st.textContent='engine preparing prompt…';
  const r1=await fetch('/ask',{method:'POST',headers:{'content-type':'application/json'},
    body:JSON.stringify({question:q,model:'local',context:ctx()})});
  const d1=await r1.json();
  if(!d1||d1.stage!=='need_local')return d1;      // server already answered (fallback)
  await ensureLocalModel();
  st.textContent='thinking on your GPU…';
  const answer=await window.__localLLM.generate(d1.system,d1.prompt);
  st.textContent='running SB + URR…';
  const r2=await fetch('/ask',{method:'POST',headers:{'content-type':'application/json'},
    body:JSON.stringify({question:q,model:'local',context:ctx(),local_answer:answer})});
  return await r2.json();
}
async function ask(){
  const q=document.getElementById('q').value.trim(); if(!q)return; busy(true); LASTQ=q;
  const model=document.getElementById('model').value;
  try{
    let d;
    if(model==='local'){ d=await askLocal(q); }
    else{
      const r=await fetch('/ask',{method:'POST',headers:{'content-type':'application/json'},
        body:JSON.stringify({question:q,model,context:ctx()})});
      d=await r.json();
    }
    if(d){ render(d);
      HIST=[q,...HIST.filter(x=>x!==q)].slice(0,30); localStorage.setItem('sb_hist',JSON.stringify(HIST)); drawHist();
      THREAD.push({q:q,a:LASTANS}); if(THREAD.length>8)THREAD=THREAD.slice(-8);
    }
  }catch(e){document.getElementById('out').innerHTML='<div class=card>error: '+esc(''+e)+'</div>'}
  busy(false);
}
function dictate(){
  const R=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!R){document.getElementById('ustat').textContent='voice input not supported in this browser';return;}
  const rec=new R();rec.lang='en-US';rec.interimResults=false;const b=document.getElementById('mic');
  b.classList.add('on');b.textContent='●';
  rec.onresult=e=>{const t=e.results[0][0].transcript;const q=document.getElementById('q');q.value=(q.value?q.value+' ':'')+t;};
  rec.onend=()=>{b.classList.remove('on');b.innerHTML='&#127908;';};rec.onerror=rec.onend;rec.start();
}
function speak(){const s=window.speechSynthesis;if(!s){document.getElementById('status').textContent='speech not supported in this browser';return;}
  if(s.speaking){s.cancel();return;} const u=new SpeechSynthesisUtterance(LASTANS||'');u.lang='en-US';u.rate=1;s.speak(u);}
function doUpload(){
  const inp=document.getElementById('file');const files=inp.files?[].slice.call(inp.files):[];
  const st=document.getElementById('ustat'); if(!files.length){st.textContent='choose a file first';return;}
  const total=files.length;let i=0;
  const next=()=>{
    if(i>=total){busy(false);if(total>1)st.textContent='reviewed '+total+' files';return;}
    const f=files[i],n=i+1;
    const textlike=/\.(txt|md|markdown|csv|tsv|json|log|py|js|html|xml|ya?ml)$/i.test(f.name);
    const fr=new FileReader();st.textContent='reading '+n+'/'+total+' · '+f.name+'…';
    fr.onload=async()=>{
      const body={filename:f.name,model:document.getElementById('model').value};
      if(textlike)body.text=fr.result; else body.b64=(''+fr.result).split(',')[1]||'';
      st.textContent='reviewing '+n+'/'+total+'…';busy(true);LASTQ='file: '+f.name;
      try{const r=await fetch('/upload',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(body)});
        const d=await r.json(); if(d.error){st.textContent='error: '+esc(d.error);}else{render(d);
          if(total===1)st.textContent=d.upload?('read '+d.upload.chars+' chars'+(d.upload.note?' · '+d.upload.note:'')):'done';}
      }catch(e){st.textContent='error'} i++; next();
    };
    if(textlike)fr.readAsText(f); else fr.readAsDataURL(f);
  };
  next();
}
function genImage(){
  const p=document.getElementById('q').value.trim();const st=document.getElementById('ustat');
  if(!p){st.textContent='type an image prompt in the box above first';return;}
  st.textContent='generating image…';busy(true);
  fetch('/generate',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({prompt:p})})
   .then(r=>r.json()).then(d=>{
     if(d.error){st.textContent='error: '+esc(d.error);}
     else{const src=d.url||('data:image/png;base64,'+(d.b64||''));
       document.getElementById('out').innerHTML='<div class="card fade"><div class=k>Generated image</div>'+
         '<img src="'+src+'" alt="generated" style="max-width:100%;border-radius:12px">'+
         '<div class=muted style="margin-top:6px">'+esc(p)+'</div></div>';
       st.textContent='done';}
   }).catch(e=>{st.textContent='error'}).finally(()=>busy(false));
}
async function loadLibrary(){
  const st=document.getElementById('lstat');st.textContent='loading…';
  try{const d=await (await fetch('/library')).json();
    document.getElementById('lcount').textContent=d.count||0;
    document.getElementById('libfiles').innerHTML=(d.files||[]).map(f=>
      '<div class=repn><div class=h><span><b>'+esc(f.name)+'</b></span><span class=muted>'+f.chars+' chars</span></div>'+
      '<div class=e>'+esc(f.preview||'')+'</div></div>').join('')||'<span class=muted>no files yet — upload a file or feed the brain</span>';
    st.textContent='';
  }catch(e){st.textContent='error'}
}
function tally(arr){const m={};(arr||[]).forEach(x=>m[x]=(m[x]||0)+1);
  return Object.entries(m).map(([k,v])=>esc(k)+(v>1?' ×'+v:'')).join(', ')||'—';}
function confWhy(d){const o=d.output||{}; if((''+o.confidence).toLowerCase()!=='low')return '';
  const holds=(d.walk&&d.walk.holds)||[];
  if(holds.length)return 'Low because '+holds.length+' node'+(holds.length>1?'s':'')+' held — e.g. '+esc(holds[0].why)+' Clear it in the review queue to raise confidence.';
  return 'Low — doubt bit or an open gap; see the node walk below.';}
function walkRow(s){
  // "URR n/25" was wrong twice: it is a 0-to-7 FILTER count, and the 25 are gone.
  const mp=(s.matrix_pass!=null)?(' <span class="'+((s.matrix_flags||[]).length?'hl':'muted')+'" style="font-size:11px">'+s.matrix_pass+'/7 filters'+((s.matrix_flags||[]).length?' ⚑'+s.matrix_flags.length:'')+'</span>'):'';
  const fl=(s.matrix_flags&&s.matrix_flags.length)?('<br><span class=hl style="margin-left:18px;font-size:11.5px">⚑ '+esc(s.matrix_flags.join(' · '))+'</span>'):'';
  // HIS CORRECTION: "SB-1 it should show what this app taken as point zero and
  // so on, at every points only then i can correct". The row carried a
  // DESCRIPTION of the work and the actual content nowhere. TOOK is the content.
  const sub=(lbl,v)=>v?('<div class=lane style="margin-left:18px;border:0;padding:2px 0">'+
    '<span class=muted style="font-size:11px">'+lbl+'</span> '+
    '<span style="font-size:12.5px;white-space:pre-wrap">'+esc(v)+'</span></div>'):'';
  return '<div class=lane><span class="vd '+s.verdict+'">●</span> <b>'+esc(s.sb_id)+'</b> '+esc(s.sb_name)+': <b>'+esc(s.verdict)+'</b>'+mp+(s.memory_written?' <span class=memok>memory ✓</span>':'')+
    sub('ITS JOB',s.job)+sub('WHAT IT TOOK',s.took)+sub('WHAT IT MADE OF IT',s.produced)+
    (s.produced?'':'<br><span class=muted style="margin-left:18px">'+esc(s.why)+'</span>')+fl+'</div>';}
function matrixCard(d){const m=(d.walk||{}).matrix; if(!m)return '';
  const by=Object.entries(m.by_urr||{}).sort((a,b)=>b[1]-a[1]);
  return '<div class=card><div class=k>The seven filters — no skips <span class=num>'+m.total+' micro-reviews</span></div>'+
    '<div class=lane>every node reviewed by all '+m.per_node+' filters (Ground·Sequence·Source·Mask·Fact·Halt·Loop): <b class=gd>'+(m.total-m.flags)+' pass</b>'+(m.flags?' · <b class=hl>'+m.flags+' flagged</b>':' · 0 flags')+'</div>'+
    (by.length?('<div class=lane><b>flags by filter</b> '+by.map(([u,n])=>'<span class=tag>'+esc(u)+' ×'+n+'</span>').join(' ')+'</div>'):'')+
    ((m.flagged||[]).length?('<details><summary>flagged details ('+m.flagged.length+')</summary>'+m.flagged.map(f=>'<div class=lane><b>'+esc(f.sb)+'</b> ⚑ '+esc(f.urr)+' · '+esc(f.code)+'</div>').join('')+'</details>'):'')+'</div>';}
function walkCard(d){const w=d.walk; if(!w||!w.steps)return '';
  const byId={}; w.steps.forEach(s=>{byId[s.sb_id]=s;});
  // Per-node walk (no stages, no blocks): SB-N → its URR → SB-N absorbs → SB-N+1
  if(w.pairs&&w.pairs.length){
    let html='';
    w.pairs.forEach(p=>{
      const sb=p.sb[0], s=byId[sb]||{}, bad=(p.verdict==='hold'||s.verdict==='hold');
      html+='<details'+(bad?' open':'')+'><summary><span class="vd '+(bad?'hold':'pass')+'">●</span> <b>'+esc(sb)+'</b> '+esc(s.sb_name||'')+' → <b>'+esc(p.gate)+'</b> '+esc(p.name)+': <b class="'+(p.verdict==='hold'?'hl':'gd')+'">'+esc(p.verdict)+'</b> <span class=muted style="font-size:11px">↩ back to '+esc(sb)+'</span></summary>'+
        (s.sb_id?walkRow(s):'')+
        '<div class="lane muted">↩ intake → '+esc(sb)+' memory: '+esc(p.intake||'')+
        (p.issues&&p.issues.length?' · <span class=hl>'+esc(p.issues.join('; '))+'</span>':'')+'</div></details>';
    });
    let closing='';
    if(w.closing&&w.closing.length){
      closing='<div class=k style="margin-top:12px">Closing integrity sweep <span class=num>'+w.closing.length+' run-level checks</span></div>'+
        w.closing.map(c=>'<div class=lane><span class="vd '+(c.verdict==='hold'?'hold':'pass')+'">●</span> <b>'+esc(c.gate)+'</b> '+esc(c.name)+': <b>'+esc(c.verdict)+'</b><br><span class=muted style="margin-left:18px">'+esc(c.intake||'')+'</span></div>').join('');
    }
    let sup='';
    if(w.support&&w.support.length){
      sup='<details style="margin-top:8px"><summary>support verifiers ('+w.support.length+', fire on node completion)</summary>'+
        w.support.map(s2=>'<div class=lane><b>'+esc(s2.gate)+'</b> after '+esc(s2.after)+': '+esc(s2.note)+(s2.issues&&s2.issues.length?' <span class=hl>'+esc(s2.issues.join('; '))+'</span>':'')+'</div>').join('')+'</details>';
    }
    var gaps=(w.gaps&&w.gaps.length)?'<details style="margin-top:8px"><summary>masks ('+w.gaps.length+' — witnesses that differ; not averaged, not picked between)</summary>'+
      w.gaps.map(g=>'<div class=lane><b>'+esc(g.kind)+'</b> '+esc(g.what||'')+' <span class=muted>· in '+esc(g.in||'')+', not in '+esc(g.not_in||'')+' ('+esc(g.sb||'')+')</span></div>').join('')+'</details>':'';
    var loops=(w.loops&&w.loops.length)?'<details style="margin-top:8px"><summary>loops ('+w.loops.length+' — each halt handed back as the next Point Zero)</summary>'+
      w.loops.map(l=>'<div class=lane><b>'+esc(l.sb)+'</b> '+esc(l.next_ask||'')+'</div>').join('')+'</details>':'';
    return '<div class=card><div class=k>Node walk · per node: SB-N → 7 filters → SB-N → SB-N+1 <span class=num>'+w.node_count+' SB · '+(w.urr_count||0)+'/7 filters · '+w.hold_count+' holds</span></div>'+html+closing+sup+gaps+loops+'</div>';
  }
  // Legacy stored chats (block-era payloads) still render.
  const blocks=w.blocks||[];
  if(!blocks.length){
    const holds=w.steps.filter(s=>s.verdict==='hold'), passes=w.steps.filter(s=>s.verdict!=='hold');
    const head=holds.length?holds.map(walkRow).join(''):'<div class=lane><span class="vd pass">●</span> All '+w.node_count+' nodes cleared.</div>';
    const rest=passes.length?('<details style="margin-top:8px"><summary>'+passes.length+' nodes passed</summary>'+passes.map(walkRow).join('')+'</details>'):'';
    return '<div class=card><div class=k>Node walk <span class=num>'+w.node_count+' nodes · '+w.hold_count+' holds</span></div>'+head+rest+'</div>';}
  const seen=new Set(); let html='';
  blocks.forEach(b=>{
    const fresh=b.sb.filter(id=>!seen.has(id)); fresh.forEach(id=>seen.add(id));
    const nodes=fresh.map(id=>byId[id]).filter(Boolean);
    const range=b.sb.length>1?(b.sb[0]+' → '+b.sb[b.sb.length-1]):b.sb[0];
    html+='<details><summary><b>'+esc(range)+'</b> ⇒ <b>'+esc(b.gate)+'</b> '+esc(b.name)+' — '+esc(b.verdict)+' <span class=muted>(legacy block view)</span></summary>'+nodes.map(walkRow).join('')+'</details>';
  });
  return '<div class=card><div class=k>Node walk (stored, legacy) <span class=num>'+w.node_count+' nodes</span></div>'+html+'</div>';}
function auditCard(d){const L=(d.output||{}).lanes||{}, a=L.audit; if(!a)return '';
  const row=(k,v)=>'<div class=lane><b>'+esc(k)+'</b> '+esc(v)+'</div>';
  let h=row('Document',(L.domain||{}).label||'numeric / financial');
  h+=row('Numeric cells read',a.number_count);
  if(a.candidate_total!=null)h+=row('Largest figure (likely grand total)',a.candidate_total);
  if((a.stated_totals||[]).length)h+=row('Near total / amount labels',a.stated_totals.join(', '));
  if((a.gst_figures||[]).length)h+=row('GST / tax figures',a.gst_figures.join(', '));
  h+=row('Negative / correction entries',a.negative_count+((a.negative_examples||[]).length?(' — e.g. '+a.negative_examples.join(', ')):''));
  if((a.caveats||[]).length)h+='<div class=fals>Cannot certify: '+a.caveats.map(esc).join(' · ')+'</div>';
  return '<div class=card><div class=k>Numeric audit <span class=num>computed, not guessed</span></div>'+h+'</div>';}
function reviewQueue(d){const h=(d.walk&&d.walk.holds)||[]; if(!h.length)return '';
  const cards=h.map(x=>{const a=x.ask||{};
    return '<div class=hold><div><b>'+esc(x.sb_id)+'</b> '+esc(x.name)+' <span class="badge warn">hold</span></div>'+
    // HIS CORRECTION: every hold used to read identically, so a human could not
    // tell what the system was actually asking. The node's JOB and the node's
    // OWN FINDING come first now — that is the part he has to read to correct it.
    (a.job?'<div class=lane style="margin:6px 0"><span class=muted>THIS NODE\'S JOB</span> '+esc(a.job)+'</div>':'')+
    (a.found?'<div class=lane style="margin:6px 0"><span class=muted>WHAT IT FOUND</span> '+esc(a.found)+'</div>':'')+
    '<div class=fivew><div><b>What it needs</b>'+esc(a.what||x.why||'—')+'</div><div><b>Why</b>'+esc(a.why||'—')+'</div>'+
    '<div><b>How</b>'+esc(a.how||'—')+'</div><div><b>When</b>'+esc(a.when||'now')+'</div></div>'+
    ((a.options&&a.options.length)?'<div class=fivew style="margin-top:6px"><div style="grid-column:1/-1"><b>Options</b> '+a.options.map(o=>'<span class=tag>'+esc(o)+'</span>').join(' ')+'</div></div>':'')+
    '<textarea class=in id="hd_'+esc(x.sb_id)+'" placeholder="paste the data / source asked for, then Add data & re-run" style="min-height:46px"></textarea>'+
    '<div class=hactions><button class=btn onclick="review(\''+esc(x.sb_id)+'\',\'add_data\')">Add data &amp; re-run</button>'+
    '<button class=btn onclick="review(\''+esc(x.sb_id)+'\',\'reloop\')">Re-loop</button>'+
    '<button class=btn onclick="review(\''+esc(x.sb_id)+'\',\'approve\')">Approve</button></div></div>';}).join('');
  return '<div class=card><div class=k>Human review queue <span class=num>'+h.length+'</span></div>'+
    '<div class=muted style="margin-bottom:8px">Each held node tells you exactly what it needs. Add it, re-loop, or approve as-is.</div>'+cards+'</div>';}
async function review(id,action){
  const ta=document.getElementById('hd_'+id); const data=ta?ta.value.trim():'';
  const st=document.getElementById('out'); st.style.opacity=.5;
  try{const r=await fetch('/review',{method:'POST',headers:{'content-type':'application/json'},
    body:JSON.stringify({question:LASTQ,id,action,data,model:document.getElementById('model').value})});
    const d=await r.json(); if(d.resolved){st.style.opacity=1; return;} render(d);
  }catch(e){}; st.style.opacity=1;}
function render(d){
  LASTD=d; const o=d.output||{},lanes=o.lanes||{}; LASTANS=o.answer||'';
  const firedStages=new Set(),counts={};
  (d.trace||[]).forEach(t=>{const s=stageOf(t.node_id); if(s){firedStages.add(s); counts[s]=(counts[s]||0)+1;}});
  drawPyr(firedStages,counts);
  const m=(d.matched_examples||[]).map(x=>'<div class=lane>'+esc(x)+'</div>').join('')||'<span class=muted>none yet — feed your corpus</span>';
  const tr=(d.trace||[]).map(t=>{const h=t.halt?(' <span class=hl>[HALT:'+esc(t.halt)+']</span>'):'';
    return esc((t.node_id||'').padEnd(7))+' '+esc((t.action||'').padEnd(20))+' '+esc(t.status)+h+'  '+esc(t.note||'')}).join('<br>');
  document.getElementById('out').innerHTML=
    '<div class=fade>'+
    ((document.getElementById('cont').checked&&THREAD.length)?'<div class=card><div class=k>Conversation <span class=num>'+THREAD.length+'</span></div>'+THREAD.map(t=>'<div class=lane><b>You</b> '+esc(t.q)+'<br><span class=muted>'+esc((t.a||'').slice(0,240))+(t.a&&t.a.length>240?'…':'')+'</span></div>').join('')+'</div>':'')+
    (d.upload?'<div class=card><div class=k>File reviewed</div><div class=lane><b>'+esc(d.upload.filename)+'</b> · '+d.upload.chars+' chars'+(d.upload.note?' · <span class=hl>'+esc(d.upload.note)+'</span>':'')+'</div></div>':'')+
    '<div class=card><div class=k>Answer</div><div class=ans>'+esc(o.answer)+'</div>'+
      '<div class=meter><i style="width:'+confPct(o.confidence)+'%"></i></div>'+
      '<div class=badges><span class=badge>'+esc(o.classification)+'</span>'+
      '<span class=badge>evidence <b>'+esc(o.evidence_tag)+'</b></span>'+
      '<span class="badge '+confClass(o.confidence)+'">confidence <b>'+esc(o.confidence)+'</b></span>'+
      '<span class=badge>penetration <b>'+esc(o.penetration_score)+'</b></span>'+
      (confWhy(d)?'<div class=why>'+confWhy(d)+'</div>':'')+
      '<div class=fals>falsifier · '+esc(o.falsifier)+'</div>'+
      '<div class=hactions><button class="btn sm" onclick="speak()">🔊 Read aloud</button><button class="btn sm" onclick="downloadReport(\'md\')">⬇ Markdown</button><button class="btn sm" onclick="downloadReport(\'csv\')">⬇ CSV</button></div></div>'+
    auditCard(d)+walkCard(d)+matrixCard(d)+reviewQueue(d)+
    '<div class=card><div class=k>Eternal example & wisdom match</div>'+m+'</div>'+
    '<div class=card><div class=k>Core Gate · human layer (SB-10)</div>'+
      '<div class=lane>dominant lens: <b>'+esc((lanes.human_layer||{}).dominant_lens||'—')+'</b></div>'+
      Object.entries((lanes.human_layer||{}).active||{}).map(([k,v])=>'<div class=lane><b>'+esc(k)+'</b> '+esc(v)+'</div>').join('')+'</div>'+
    '<div class=card><div class=k>Output lanes (URR-07)</div>'+
      '<div class=lane><b>Reality</b> '+esc(JSON.stringify(lanes.reality_path||{}))+'</div>'+
      (((lanes.wild_path||{}).preserved||[]).length?'<div class=lane><b>Wild path (preserved)</b> '+esc(JSON.stringify(lanes.wild_path.preserved))+'</div>':'')+
      '<div class=lane><b>Re-anchor</b> '+esc(lanes.reality_reanchor||'')+'</div>'+
      (lanes.safety?'<div class=lane><b class=hl>Safety</b> '+esc(JSON.stringify(lanes.safety))+'</div>':'')+'</div>'+
    '<div class=card><div class=k>Truth & evidence (Stages 3–6)</div>'+
      '<div class=lane><b>Doubt Engine</b> '+esc((lanes.doubt||{}).verdict||'—')+' · '+(((lanes.doubt||{}).fragilities)||[]).length+' fragilities</div>'+
      '<div class=lane><b>Witness</b> '+esc(((lanes.witness||[])[0])||'—')+'</div>'+
      '<div class=lane><b>Evidence ladder</b> '+tally((lanes.evidence_ledger||[]).map(e=>e.evidence_tag))+'</div>'+
      ((lanes.connections||[]).length?'<div class=lane><b>Dot-connections</b> '+esc((lanes.connections||[]).map(c=>c.ref+' ×'+c.appears_in).join(', '))+'</div>':'')+
      (lanes.merge_proposal?'<div class=lane><b class=hl>Merge proposed</b> '+esc((lanes.merge_proposal.contributing||[]).join(' + '))+' · needs human gate</div>':'')+
      (lanes.synthetic_fuel?'<div class=lane><b>Synthetic fuel</b> ['+esc(lanes.synthetic_fuel.stall)+'] '+esc(lanes.synthetic_fuel.fuel)+' <span class=tag>SYNTHETIC</span></div>':'')+'</div>'+
    (d.halts&&d.halts.length?'<div class=card><div class=k>Halts → loops opened</div><span class=hl>'+esc(d.halts.join(', '))+'</span></div>':'')+
    '<details><summary>engine trace ('+(d.trace||[]).length+' nodes) & memory</summary>'+
      '<div class=card><div class=trace>'+tr+'</div><div class=muted style="margin-top:10px">memory: '+
      esc(JSON.stringify(d.memory))+' · clone learns 1 example each run</div></div></details>'+
    '</div>';
}
function downloadReport(fmt){
  const d=LASTD; if(!d)return; const o=d.output||{}; let body,mime,ext;
  if(fmt==='csv'){
    const rows=[['field','value'],['question',LASTQ],['answer',(o.answer||'').replace(/\n/g,' ')],
      ['classification',o.classification],['evidence',o.evidence_tag],['confidence',o.confidence],
      ['penetration',o.penetration_score],['falsifier',o.falsifier]];
    ((d.walk&&d.walk.steps)||[]).forEach(s=>rows.push(['node '+s.sb_id,s.verdict+' — '+s.why]));
    body=rows.map(r=>r.map(c=>'"'+(''+(c==null?'':c)).replace(/"/g,'""')+'"').join(',')).join('\n');
    mime='text/csv';ext='csv';
  }else{
    let md='# Sourceborn report\n\n**Ask:** '+LASTQ+'\n\n## Answer\n\n'+(o.answer||'')+'\n\n';
    md+='- classification: '+o.classification+'\n- evidence: '+o.evidence_tag+'\n- confidence: '+o.confidence+'\n- penetration: '+o.penetration_score+'\n\n**Falsifier:** '+o.falsifier+'\n\n## Node walk\n\n';
    ((d.walk&&d.walk.steps)||[]).forEach(s=>md+='- **'+s.sb_id+'** '+s.sb_name+' → '+s.verdict+' — '+s.why+'\n');
    body=md;mime='text/markdown';ext='md';
  }
  const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([body],{type:mime}));
  a.download='sourceborn-report.'+ext;a.click();
}
async function loadUnfiled(){
  const st=document.getElementById('repstat');st.textContent='loading…';
  try{const list=await (await fetch('/unfiled')).json();
    document.getElementById('out').innerHTML='<div class="card fade"><div class=k>Unfiled — your words the pyramid could not park <span class=num>'+list.length+'</span></div>'+
      '<div class=muted style="margin-bottom:8px">Human review helps here: park each into a brain category, or leave it to incubate. Nothing is discarded.</div>'+
      (list.map(u=>'<div class=lane><b>'+esc(u.item)+'</b> <span class=muted>from '+esc(u.node)+' · '+esc((u.at||'').slice(5,16))+'</span> '+
        '<button class="btn sm" onclick="parkItem(\''+esc(u.node)+'\',\''+esc(u.item)+'\',\'sub\')">Park as Sub</button> '+
        '<button class="btn sm" onclick="parkItem(\''+esc(u.node)+'\',\''+esc(u.item)+'\',\'micro\')">Park as Micro</button></div>').join('')||'<span class=muted>queue is empty — everything parked</span>')+'</div>';
    st.textContent='';
  }catch(e){st.textContent='error'}
}
async function parkItem(node,item,level){
  try{await fetch('/pyramid/park',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({node,item,level})});
    loadUnfiled();}catch(e){}
}
async function restoreBrain(){
  const inp=document.getElementById('restorefile'); const f=inp.files&&inp.files[0]; if(!f)return;
  const st=document.getElementById('repstat'); st.textContent='restoring…';
  const fr=new FileReader();
  fr.onload=async()=>{
    try{const b64=(''+fr.result).split(',')[1]||'';
      const d=await (await fetch('/import',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({b64})})).json();
      st.textContent=d.ok?('restored '+d.files_restored+' files ✓'):('error: '+(d.error||''));
      drawHist(); loadBrains();
    }catch(e){st.textContent='restore error'}
  };
  fr.readAsDataURL(f);
}
async function runNovelty(){
  const st=document.getElementById('repstat');st.textContent='hunting new parameters…';
  try{
    const d=await (await fetch('/novelty/run',{method:'POST',headers:{'content-type':'application/json'},body:'{}'})).json();
    const prev=await (await fetch('/novelty')).json();
    const cands=(d.candidates||[]).map(c=>'<div class=hold><div><b>'+esc(c.proposed_label)+'</b> <span class="badge warn">'+esc(c.status)+'</span></div>'+
      '<div class=fivew><div><b>Term</b>'+esc(c.term)+(c.variants&&c.variants.length?' ('+esc(c.variants.join(', '))+')':'')+'</div>'+
      '<div><b>Forced by</b>'+esc((c.sources||[]).slice(0,4).join(', '))+'</div>'+
      '<div><b>Nearest existing</b>'+esc(c.nearest_existing)+' ('+Math.round((c.similarity||0)*100)+'%)</div>'+
      '<div><b>Why not same</b>'+esc(c.why_not_same)+'</div></div>'+
      '<div class=hactions><button class=btn onclick="approveNovelty(\''+esc(c.term)+'\')">Approve as parameter</button></div></div>').join('');
    document.getElementById('out').innerHTML='<div class="card fade"><div class=k>Novelty pass — parameters that never existed <span class=num>'+
      (d.candidates||[]).length+' candidate(s) · scanned '+d.scanned+' terms vs '+d.universe+' known</span></div>'+
      '<div class=muted style="margin-bottom:8px">Proposals only — nothing is added without your approval. Full report: <a class=gd href="/novelty/file?name='+esc(d.file)+'" download>'+esc(d.file)+'</a></div>'+
      (cands||'<div class=lane>No parameter beyond the existing universe surfaced this pass — everything recent parked into known categories.</div>')+
      ((prev.approved||[]).length?'<div class=lane style="margin-top:10px"><b>Approved so far</b> '+prev.approved.map(a=>'<span class=tag>'+esc(a.label)+'</span>').join(' ')+'</div>':'')+
      ((prev.files||[]).length>1?'<details style="margin-top:6px"><summary>past novelty files ('+(prev.files.length-1)+')</summary>'+prev.files.slice(1).map(f=>'<div class=lane><a class=muted href="/novelty/file?name='+esc(f.file)+'" download>'+esc(f.file)+'</a></div>').join('')+'</details>':'')+
      '</div>';
    st.textContent='';
  }catch(e){st.textContent='error'}
}
async function approveNovelty(term){
  try{await fetch('/novelty/approve',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({term})});
    runNovelty();}catch(e){}
}
let IG=null;   // interconnection graph state: node positions for click → brain
async function drawInterGraph(){
  const st=document.getElementById('repstat'); if(st)st.textContent='loading…';
  try{
    const d=await (await fetch('/graph')).json();
    const W=860,H=860,cx=W/2,cy=H/2,R=370,r=205;
    const sb=d.nodes.filter(n=>n.kind==='SB'), urr=d.nodes.filter(n=>n.kind==='URR');
    const pos={};
    sb.forEach((n,i)=>{const a=-Math.PI/2+2*Math.PI*i/sb.length;
      pos[n.id]={x:cx+R*Math.cos(a),y:cy+R*Math.sin(a),n};});
    urr.forEach((n,i)=>{const a=-Math.PI/2+2*Math.PI*i/urr.length;
      pos[n.id]={x:cx+r*Math.cos(a),y:cy+r*Math.sin(a),n};});
    document.getElementById('out').innerHTML=
      '<div class="card fade"><div class=k>Interconnection — the complete network '+
      '<span class=num>K&#8327;&#8320; mesh '+d.mesh.sb_pairs.toLocaleString()+' lines · all 95: '+d.mesh.all_pairs.toLocaleString()+' · <b class=gd>learned: '+d.mesh.learned_count+'</b></span></div>'+
      '<div class=muted style="margin-bottom:8px">'+esc(d.note)+' — faint = every possible handshake; <span class=gd>green</span> = learned by the weekly pass; <span style="color:#a78bfa">violet</span> = each SB node’s own URR. Click a dot to open that brain.</div>'+
      '<canvas id=igc width='+W+' height='+H+' style="width:100%;max-width:860px;display:block;margin:0 auto;border-radius:12px;background:#0b0e14;cursor:pointer"></canvas></div>';
    const c=document.getElementById('igc'),g=c.getContext('2d');
    // the complete mesh — every possible handshake, K-graph style (the image)
    g.lineWidth=0.4;g.strokeStyle='rgba(124,139,255,0.055)';
    const ids=Object.keys(pos);
    for(let i=0;i<ids.length;i++)for(let j=i+1;j<ids.length;j++){
      g.beginPath();g.moveTo(pos[ids[i]].x,pos[ids[i]].y);g.lineTo(pos[ids[j]].x,pos[ids[j]].y);g.stroke();}
    // primary SB→URR pairing (violet, dim)
    g.lineWidth=0.8;g.strokeStyle='rgba(167,139,250,0.28)';
    (d.edges||[]).filter(e=>e.kind==='primary').forEach(e=>{
      if(pos[e.from]&&pos[e.to]){g.beginPath();g.moveTo(pos[e.from].x,pos[e.from].y);g.lineTo(pos[e.to].x,pos[e.to].y);g.stroke();}});
    // learned connections (bright emerald — the real, growing web)
    g.lineWidth=1.5;g.strokeStyle='rgba(52,211,153,0.75)';
    (d.learned||[]).forEach(e=>{
      if(pos[e.from]&&pos[e.to]){g.beginPath();g.moveTo(pos[e.from].x,pos[e.from].y);g.lineTo(pos[e.to].x,pos[e.to].y);g.stroke();}});
    // nodes + labels
    for(const id of ids){const p=pos[id],isSB=p.n.kind==='SB';
      g.beginPath();g.arc(p.x,p.y,isSB?6:7,0,7);
      g.fillStyle=isSB?'#f87171':'#a78bfa';g.fill();
      g.strokeStyle='#0b0e14';g.lineWidth=1.5;g.stroke();
      const num=parseInt(id.slice(-2));
      if((isSB&&num%5===0)||(!isSB&&num%5===0)){
        const lx=p.x+(p.x-cx)*0.07,ly=p.y+(p.y-cy)*0.07;
        g.fillStyle=isSB?'#7d8699':'#a78bfa';g.font='11px Inter,sans-serif';
        g.textAlign=lx<cx?'right':'left';g.fillText(id,lx,ly+3);}}
    g.fillStyle='#5b6477';g.font='12px Inter,sans-serif';g.textAlign='center';
    g.fillText('outer ring: SB working nodes · inner ring: URR verifiers (memory, not method)',cx,H-14);
    IG=pos;
    c.onclick=ev=>{const b=c.getBoundingClientRect(),
      mx=(ev.clientX-b.left)*(W/b.width),my=(ev.clientY-b.top)*(H/b.height);
      let best=null,bd=1e9;
      for(const id in IG){const dx=IG[id].x-mx,dy=IG[id].y-my,q=dx*dx+dy*dy;
        if(q<bd){bd=q;best=id;}}
      if(best&&bd<400)brainDetail(best);};
    if(st)st.textContent='';
  }catch(e){if(st)st.textContent='error'}
}
async function loadMasterLog(){
  const st=document.getElementById('repstat');st.textContent='loading…';
  try{const list=await (await fetch('/masterlog?n=80')).json();
    document.getElementById('out').innerHTML='<div class="card fade"><div class=k>Master log · sacred, append-only <span class=num>'+list.length+' latest</span></div>'+
      (list.map(e=>{const rest=Object.entries(e).filter(([k])=>k!=='at'&&k!=='event').map(([k,v])=>k+'='+(typeof v==='object'?JSON.stringify(v):v)).join(' ').slice(0,120);
        return '<div class=lane><span class=muted>'+esc((e.at||'').slice(5))+'</span> <b>'+esc(e.event||'?')+'</b> <span class=muted>'+esc(rest)+'</span></div>';}).join('')||'<span class=muted>empty</span>')+'</div>';
    st.textContent='';
  }catch(e){st.textContent='error'}
}
async function loadReport(){
  const st=document.getElementById('repstat');st.textContent='loading…';
  try{const d=await (await fetch('/memory/report')).json();renderReport(d,'Memory report (live)');st.textContent='';}
  catch(e){st.textContent='error'}
}
function renderReport(rep,title){
  const nodes=(rep.nodes||[]).map(n=>'<div class=repn><div class=h><span><b>'+esc(n.id)+'</b> '+esc(n.name)+'</span><span class=muted>'+n.entry_count+' entries</span></div>'+
    (n.recent||[]).map(e=>'<div class=e>'+esc(e.content)+(e.tags&&e.tags.length?' <span class=muted>['+esc(e.tags.join(', '))+']</span>':'')+'</div>').join('')+'</div>').join('');
  document.getElementById('out').innerHTML='<div class="card fade"><div class=k>'+esc(title)+
    ' <span class=num>'+((rep.totals||{}).total_memory_entries||0)+' entries · '+((rep.totals||{}).nodes_with_brains||0)+' nodes</span></div>'+
    '<div class=muted style="margin-bottom:8px">'+esc(rep.at||'')+'</div><div class=rep>'+(nodes||'<span class=muted>nothing stored yet</span>')+'</div></div>';
}
async function saveSnapshot(){
  const st=document.getElementById('repstat');st.textContent='saving…';
  try{await fetch('/snapshot',{method:'POST',headers:{'content-type':'application/json'},body:'{}'});
    st.textContent='snapshot saved'; loadSnapshots();}catch(e){st.textContent='error'}
}
async function loadSnapshots(){
  try{const list=await (await fetch('/snapshots')).json();
    document.getElementById('snaps').innerHTML=list.length?('<div class=k style="margin-top:8px">Snapshots</div>'+
      list.map(s=>'<a class="hist" style="cursor:pointer" onclick="showSnap(\''+esc(s.id)+'\')">'+esc(s.name)+' · '+((s.total||{}).total_memory_entries||0)+'</a>').join('')):'';
  }catch(e){}
}
async function showSnap(id){
  try{const d=await (await fetch('/snapshot?id='+encodeURIComponent(id))).json();renderReport(d,'Snapshot · '+(d.name||id));}catch(e){}
}
async function feed(){
  const text=document.getElementById('ftext').value.trim(); if(!text)return;
  const name=document.getElementById('fname').value.trim()||'note';
  const fstat=document.getElementById('fstat'); fstat.textContent='adding…';
  try{
    const r=await fetch('/ingest',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({name,text})});
    const d=await r.json();
    fstat.textContent='memory: '+((d.memory&&d.memory.total_memory_entries)||0)+' · clone: '+(d.examples||0);
    document.getElementById('ftext').value=''; document.getElementById('fname').value='';
  }catch(e){fstat.textContent='error'}
}
async function loadBrains(){
  try{
    const d=await (await fetch('/brains')).json(); let total=0,html='';
    for(const [g,list] of Object.entries(d)){
      total+=list.length;
      html+='<details><summary>'+esc(g)+' ('+list.length+')</summary>';
      for(const c of list){
        const flags=[c.human_review?'human-gate':'',c.urr_gate?'URR-gate':'',c.gen_params?'+params':'','risk:'+c.risk,c.write].filter(Boolean).join(' · ');
        html+='<div class=lane style="cursor:pointer" onclick="brainDetail(\''+c.id+'\')"><b>'+esc(c.id)+'</b> '+esc(c.name)+'<br><span class=muted style=font-size:11px>'+esc(flags)+'</span></div>';
      }
      html+='</details>';
    }
    document.getElementById('brains').innerHTML=html; document.getElementById('bcount').textContent=total;
  }catch(e){}
}
function _sel(name,opts,val){return '<select id=bs_'+name+'>'+opts.map(o=>'<option'+(o===val?' selected':'')+'>'+o+'</option>').join('')+'</select>'}
function _chk(name,val){return '<label class=switch><input type=checkbox id=bs_'+name+(val?' checked':'')+'><span class=track></span> '+name.replace(/_/g,' ')+'</label>'}
async function brainDetail(id){
  const d=await (await fetch('/brain?id='+encodeURIComponent(id))).json(); const c=d.config; if(!c)return;
  const P=(d.memory&&d.memory.parameters)||{};
  const specKeys=Object.keys(P).filter(k=>/^[A-Z]/.test(k)&&(typeof P[k]!=='object'));
  document.getElementById('out').innerHTML='<div class="card fade"><div class=k>Brain '+esc(c.node_id)+' — '+esc(c.name)+'</div>'+
    '<div class=lane>kind: '+esc(c.kind)+' · stage: '+c.stage+' · pyramid (Node→Main→Sub→Micro): '+esc(JSON.stringify(c.pyramid))+'</div>'+
    '<div class=lane>role: '+esc(c.role)+'</div>'+
    '<div class=lane><b>Brain parameters (grow with use)</b><br>'+(specKeys.length?specKeys.map(k=>'<span class=tag>'+esc(k)+' · '+esc(''+P[k])+'</span>').join(' '):'<span class=muted>no runs through this brain yet</span>')+'</div>'+
    '<div class=bset>risk '+_sel('risk_level',['low','medium','high'],c.risk_level)+
      ' &nbsp; write '+_sel('write_policy',['every_visit','on_finding','checkpoint'],c.write_policy)+'</div>'+
    '<div class=bset>'+_chk('urr_gate',c.urr_gate)+_chk('human_review',c.human_review)+_chk('weekly_update',c.weekly_update)+_chk('can_generate_parameters',c.can_generate_parameters)+'</div>'+
    '<div class=toolbar style="border:0;padding:0"><button class=btn onclick="saveBrain(\''+c.node_id+'\')">Save settings</button><span class=status id=savestat></span>'+
      (c.immutable_source?'<span class=tag>immutable source</span>':'')+'</div>'+
    '<div class="lane muted">tracks: '+esc((c.tracked_groups||[]).join(', '))+' · memory entries: '+((d.memory&&d.memory.entry_count)||0)+'</div></div>';
}
async function saveBrain(id){
  const g=n=>document.getElementById('bs_'+n), st=document.getElementById('savestat'); st.textContent='saving…';
  const body={id,risk_level:g('risk_level').value,write_policy:g('write_policy').value,
    urr_gate:g('urr_gate').checked,human_review:g('human_review').checked,
    weekly_update:g('weekly_update').checked,can_generate_parameters:g('can_generate_parameters').checked};
  try{const d=await (await fetch('/brain/settings',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(body)})).json();
    st.textContent=d.ok?'saved ✓':'error'; loadBrains();}catch(e){st.textContent='error'}
}
let WMSG='';                         // survives the panel being re-rendered
function _wsay(msg){                 // the button lives in two places
  WMSG=msg;
  ['bstat','bstat2'].forEach(id=>{const e=document.getElementById(id);
    if(e)e.textContent=msg;});
}
async function weeklyUpdate(){
  _wsay('running the weekly pull…');
  try{const d=await (await fetch('/brains/update',{method:'POST',headers:{'content-type':'application/json'},body:'{}'})).json();
    _wsay('updated '+d.updated+'/'+d.total);
    loadBrains(); refreshWpill();
    // Only redraw the ledger if the ledger is what he is looking at. The
    // centre column is his ANSWER pane — refreshing a side panel must never
    // destroy an answer he did not ask us to replace.
    if(document.getElementById('wpanel'))loadWeekly();
    else _wsay('updated '+d.updated+'/'+d.total+' — open Weekly pull to see the run');
  }catch(e){_wsay('error')}
}
function drawWpill(s,phrase){
  const p=document.getElementById('wpill'); if(!p)return;
  p.innerHTML='weekly <b>'+esc(String(s.state||'—'))+'</b>'+
    (s.runs?' <span class=muted>'+esc(String(s.runs))+'</span>':'');
  p.title='weekly pull — '+(phrase||'')+' · '+(s.runs||0)+
    ' run(s) kept. Click to open the ledger.';
  p.style.cursor='pointer'; p.onclick=loadWeekly;
}
async function refreshWpill(){
  try{const d=await (await fetch('/health')).json();
    drawWpill(d.weekly||{},d.weekly_phrase||'');}catch(e){}
}
// THE WEEKLY PULL, MADE VISIBLE. Before this the pull ran in a daemon thread
// and wrote one file it overwrote every time — there was no way to see that it
// had ever happened, or what it learned. Every run is now kept and listed.
// Every interpolated value is escaped: a run file can arrive from a restored
// backup, so these numbers are untrusted input, not our own arithmetic.
function _wrow(r,i){
  const num=v=>v==null?'—':esc(String(v));
  if(r.unreadable)
    return '<div class=lane><span class=muted>'+esc(String(r.file||''))+'</span> '+
      '<span class="badge bad">unreadable — the file is corrupt or was cut off mid-write</span></div>';
  const err=r.novelty_error;
  return '<div class=lane><span class=muted>'+esc(String(r.at||r.file||'').slice(0,16))+'</span> '+
    (i===0?'<span class="badge ok">latest</span> ':'')+
    '<b>'+num(r.brains)+'</b> brains refreshed · '+
    '<b>'+num(r.new_connections)+'</b> new connections · '+
    (err?'<span class="badge warn">novelty failed: '+esc(String(err))+'</span>'
        :'<b>'+num(r.candidates)+'</b> novelty candidate(s)')+
    ' <a class=muted href="/weekly/file?name='+encodeURIComponent(r.file)+'" download>'+esc(String(r.file||''))+'</a></div>';
}
async function loadWeekly(off){
  off=off||0;
  const st=document.getElementById('repstat'); if(st)st.textContent='loading…';
  try{const d=await (await fetch('/weekly?offset='+off)).json();
    const s=d.status||{}, h=d.history||[], runs=d.runs||0;
    const shown=off+h.length;
    const cls=s.state==='current'?'ok':'warn';
    // Never-run and ran-but-no-runs-kept are DIFFERENT sentences. Saying "it
    // has never run" under a badge that reads "overdue — last <date>" is the
    // same two-state lie this item exists to remove.
    const empty=s.last_weekly_update
      ? 'no runs are kept yet — this brain ran under the older code, which overwrote a single file. The ledger starts with the next pull.'
      : 'it has never run — press the button and the first run is kept forever';
    document.getElementById('out').innerHTML='<div class="card fade" id=wpanel><div class=k>Weekly pull &middot; the ledger '+
      '<span class=num>'+esc(String(runs))+' run(s) kept'+
      (shown<runs?' · showing '+(off+1)+'–'+shown:'')+'</span></div>'+
      '<div style="margin-bottom:8px"><span class="badge '+cls+'">'+esc(String(d.phrase||''))+'</span> '+
      '<span class=muted>cadence is 7 days; the pull refreshes every brain’s settings, synthesises the week into each brain’s memory, then hunts parameters that never existed. Nothing is overwritten — each run is its own dated file.</span></div>'+
      '<div class=hactions style="margin-bottom:8px"><button class=btn onclick=weeklyUpdate()>Run the pull now</button>'+
      '<span class=status id=bstat2></span></div>'+
      (h.length?h.map(_wrow).join(''):'<span class=muted>'+empty+'</span>')+
      (shown<runs?'<div class=hactions style="margin-top:8px"><button class="btn sm" onclick="loadWeekly('+shown+')">Older runs →</button></div>':'')+
      (off?'<div class=hactions style="margin-top:8px"><button class="btn sm" onclick="loadWeekly(0)">← Newest</button></div>':'')+
      '</div>';
    if(st)st.textContent='';
    const b2=document.getElementById('bstat2'); if(b2)b2.textContent=WMSG;
    drawWpill(s,d.phrase||'');
  }catch(e){if(st)st.textContent='error'}
}
loadBrains(); loadSnapshots();
document.getElementById('q').addEventListener('keydown',e=>{if(e.key==='Enter'&&(e.metaKey||e.ctrlKey))ask()});
</script></div>
<script type="module">
// On-device inference: the model runs in THIS browser on the user's GPU via
// WebGPU. The prompt never goes to a third-party LLM — only back to this app's
// own engine for SB+URR framing. Library + weights are fetched once (then cached
// by the browser) from the WebLLM CDN.
import { CreateMLCEngine } from "https://esm.run/@mlc-ai/web-llm";
let engine=null, loading=null;
const DEF="Llama-3.2-1B-Instruct-q4f16_1-MLC";
function mid(){ try{ return localStorage.getItem('sb_local_model')||DEF; }catch(e){ return DEF; } }
async function load(onp){
  if(engine && engine.__mid===mid()) return engine;     // reuse unless model changed
  loading = CreateMLCEngine(mid(), { initProgressCallback: p=>{ try{ onp&&onp(p); }catch(e){} } });
  engine = await loading; engine.__mid = mid(); loading=null; return engine;
}
async function generate(system, prompt){
  const e = await load();
  const reply = await e.chat.completions.create({
    messages:[{role:'system',content:system||''},{role:'user',content:prompt||''}],
    temperature:0.7, max_tokens:1024 });
  return (reply && reply.choices && reply.choices[0] && reply.choices[0].message.content) || '';
}
window.__localLLM = { load, generate, supported:()=>!!navigator.gpu };
</script>
</body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args) -> None:
        pass

    def _guard(self) -> bool:
        """True if the request may proceed. When SB_ACCESS_PASS is unset the
        app is open. When it is set, every path except the health check needs
        matching HTTP Basic credentials."""
        if not SB_ACCESS_PASS or urlparse(self.path).path in OPEN_PATHS:
            return True
        if basic_auth_ok(self.headers.get("Authorization", ""),
                         SB_ACCESS_USER, SB_ACCESS_PASS):
            return True
        # Close the connection: an unauthenticated POST may carry a body we
        # never read, and leaving it on a keep-alive socket desyncs the next
        # request. A fresh request (with credentials) reconnects cleanly.
        self.close_connection = True
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Sourceborn"')
        self.send_header("Content-Type", "application/json")
        self.send_header("Connection", "close")
        body = b'{"error":"authentication required"}'
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        return False

    def do_GET(self) -> None:
        if not self._guard():
            return
        route = urlparse(self.path)
        path, qs = route.path, parse_qs(route.query)
        if path in ("/", "/index.html"):
            self._send(200, PAGE.encode("utf-8"), "text/html; charset=utf-8")
        elif path == "/page":
            self._send(200, mypage.PAGE.encode("utf-8"),
                       "text/html; charset=utf-8")
        elif path == "/engine":
            self._send(200, enginepage.PAGE.encode("utf-8"),
                       "text/html; charset=utf-8")
        elif path == "/reading":
            self._send(200, readingpage.PAGE.encode("utf-8"),
                       "text/html; charset=utf-8")
        elif path == "/asi":
            # THE PYRAMID — his answer on screen, one ask over his 3,204
            self._send(200, asipage.PAGE.encode("utf-8"),
                       "text/html; charset=utf-8")
        elif path == "/generation":
            # THE GENERATION — same person, changed conditions, new brain
            self._send(200, generationpage.PAGE.encode("utf-8"),
                       "text/html; charset=utf-8")
        elif path == "/generation/packs":
            self._send(200, json.dumps(
                {"packs": statepacks.packs_index(),
                 "stats": statepacks.stats(),
                 "rubrics": list(statepacks.RUBRICS_25),
                 "events": sorted(statepacks.EVENT_FORKS)}).encode(),
                "application/json")
        elif path == "/growth":
            # the 3,204 is a floor. Everything surfaced is appended; nothing
            # is ever removed.
            self._send(200, json.dumps(growth.report(SB_ROOT)).encode(),
                       "application/json")
        elif path == "/intents":
            # the live intent generator, and the proof of his concept
            self._send(200, json.dumps(
                {"stats": intents.stats(),
                 "scaling": intents.scaling(),
                 "unlinked": intents.unlinked(),
                 "motive_rows": [m["name"] for m in intents.motive_rows()],
                 "form_rows": [f["name"] for f in intents.form_rows()],
                 "links": {k: v["reachable_from"]
                           for k, v in intents.motive_links().items()}}).encode(),
                "application/json")
        elif path == "/map":
            # the arrow graph — every number read from the live modules
            self._send(200, sysmap.arrow_chart().encode(),
                       "text/plain; charset=utf-8")
        elif path == "/map/where":
            self._send(200, json.dumps(
                sysmap.where((qs.get("q") or [""])[0])).encode(),
                "application/json")
        elif path == "/artifact":
            # reading an object without pretending to read its language
            self._send(200, json.dumps(
                {"stats": artifact.stats(),
                 "sign_groups": list(artifact.SIGN_GROUPS),
                 "meanings": list(artifact.SYNTHETIC_MEANINGS),
                 "actor_roles": list(artifact.ACTOR_ROLES),
                 "origin_distance": list(artifact.ORIGIN_DISTANCE),
                 "future_states": list(artifact.FUTURE_STATES),
                 "patterns": list(artifact.PATTERN_CANDIDATES),
                 "refused": artifact.refused(),
                 "seated": artifact.seat_on_bank(),
                 "space": artifact.combination_space()}).encode(),
                "application/json")
        elif path == "/subjects":
            # his platform superimposed on Riemann and Einstein — my own earlier
            # builds, handed back. 25 candidates, 14 halts, none answered.
            self._send(200, json.dumps(
                {"stats": subjectbrains.stats(),
                 "candidates": subjectbrains.candidates_for(),
                 "halts": subjectbrains.open_halts(),
                 "version_gap": subjectbrains.version_gap(),
                 "subjects": list(subjectbrains.SUBJECTS),
                 "cross_test": subjectbrains.cross_test(),
                 "applied": subjectbrains.apply_candidates(),
                 "generated": subjectbrains.generate_variants(),
                 "release_poles": subjectbrains.release_poles(),
                 "lone_worker": subjectbrains.lone_worker_check()}).encode(),
                "application/json")
        elif path == "/selfmake":
            # the algorithm's own body: the spine plus every step it has written
            # for itself. Not a constant.
            self._send(200, json.dumps(
                {"stats": selfmake.stats(SB_ROOT),
                 "steps": selfmake.steps(SB_ROOT),
                 "generation": selfmake.generation(SB_ROOT),
                 "bias": selfmake.bias_report(repo=".")}).encode(),
                "application/json")
        elif path == "/growing":
            # the growing phase: every file divided by what it does to the base,
            # and the motto made mechanical
            self._send(200, json.dumps(
                {"stats": growing.stats(),
                 "divide": filemap.divide("."),
                 "motto": growing.MOTTO}).encode(),
                "application/json")
        elif path == "/growing/coverage":
            # how much of his 3,204 his own examples reach. His "basic".
            paths = filemap.readable(".")
            self._send(200, json.dumps(growing.coverage(paths, ".")).encode(),
                       "application/json")
        elif path == "/ledger":
            # his LIVE_INTENT_ENGINE + INTENT_LEDGER: one event, ten states, ten
            # falsifiers, nothing chosen — and the workbook audit beside it
            self._send(200, json.dumps(
                {"stats": intent_ledger.stats(),
                 "run": intent_ledger.his_run(),
                 "from_core": intent_ledger.from_core(),
                 "audit": intent_ledger.workbook_audit()}).encode(),
                "application/json")
        elif path == "/weighting":
            # this module was reachable from nothing; it is reachable now
            self._send(200, json.dumps(weighting.stats()).encode(),
                       "application/json")
        elif path == "/asi/stats":
            self._send(200, json.dumps(asi_pyramid.stats()).encode(),
                       "application/json")
        elif path == "/patterns":
            cands = patternmem.load_candidates(SB_ROOT)
            self._send(200, json.dumps({
                "candidates": cands,
                "approved": patternmem.load_approved(SB_ROOT),
                "writebacks": patternmem.writebacks(SB_ROOT, 50),
                "stats": patternmem.stats(SB_ROOT),
                "below": patternmem.refresh_candidates(SB_ROOT)
                         .get("below_threshold", [])}).encode(),
                "application/json")
        elif path == "/registry":
            # HIS 3,204, from HIS document — the frame is 1-10-8-40
            segs = [{"id": f"SEG-{s['n']:02d}", "n": s["n"], "name": s["name"],
                     "containers": len(s.get("containers", [])),
                     "parameters": sum(len(c.get("subs", []))
                                       for c in s.get("containers", []))}
                    for s in human_registry.segments()]
            self._send(200, json.dumps({
                "stats": human_registry.stats(),
                "frame": human_registry.frame(),
                "segments": segs,
                "universal_filters": human_registry.universal_filters(),
                "operating_states": human_registry.operating_states(),
                "failure_classes": human_registry.failure_classes(),
                "operating_chain": human_registry.operating_chain()}).encode(),
                "application/json")
        elif path == "/registry/container":
            c = human_registry.container((qs.get("id") or [""])[0])
            if c is None:
                self._send(404, b'{"error":"no such container"}',
                           "application/json")
            else:
                self._send(200, json.dumps(c).encode(), "application/json")
        elif path == "/registry/activate":
            q = (qs.get("q") or [""])[0]
            self._send(200, json.dumps(
                human_registry.activate(q, _int_arg(qs, "limit", 40, 1, 400))
                ).encode(), "application/json")
        elif path == "/senses":
            self._send(200, json.dumps({
                "senses": sensemem.load(SB_ROOT),
                "writebacks": sensemem.writebacks(SB_ROOT, 50),
                "stats": sensemem.stats(SB_ROOT),
                "return_dimensions": list(sensemem.RETURN_DIMENSIONS),
                "valences": list(sensemem.MEMORY_VALENCE)}).encode(),
                "application/json")
        elif path == "/micro":
            # walk all the way back down: every micro-sequence, or one ask's
            aid = (qs.get("ask") or [""])[0]
            ms = patternmem.load_micro(SB_ROOT)
            if aid:
                ms = [m for m in ms if m.get("ask") == aid]
            self._send(200, json.dumps(ms[-_int_arg(qs, "n", 200, 1, 5000):]
                                       ).encode(), "application/json")
        elif path == "/flow":
            self._send(200, json.dumps({
                "positions": rubric_router.FLOW_POSITIONS,
                "segments": rubric_router.SEGMENT_ROLE,
                "mechanisms": rubric_router.MECHANISMS}).encode(),
                "application/json")
        elif path == "/exists":
            self._send(200, exists.PAGE.encode("utf-8"),
                       "text/html; charset=utf-8")
        elif path == "/exists/data":
            # his understanding, located in the code and CHECKED against the
            # real source on every open — so the map cannot go stale into a lie
            d = exists.verify()
            d["ladder"] = exists.ladder_reading(ladder.load_registry(SB_ROOT))
            d["at"] = _now()
            self._send(200, json.dumps(d, ensure_ascii=False).encode(),
                       "application/json")
        elif path == "/engine/registry":
            self._send(200, json.dumps(ladder.load_registry(SB_ROOT)).encode(),
                       "application/json")
        elif path == "/page/meta":
            self._send(200, json.dumps({"sources": mypage.SOURCES,
                                        "hows": list(mypage.HOWS)}).encode(),
                       "application/json")
        elif path == "/page/layout":
            self._send(200, json.dumps(mypage.load_layout(SB_ROOT)).encode(),
                       "application/json")
        elif path == "/page/data":
            self._send(200, json.dumps(_page_feeds()).encode(),
                       "application/json")
        elif path == "/page/versions":
            self._send(200, json.dumps(mypage.list_versions(SB_ROOT)).encode(),
                       "application/json")
        elif path == "/page/version":
            n = (qs.get("n") or ["0"])[0]
            d = mypage.get_version(SB_ROOT, int(n)) if n.isdigit() else None
            if d is None:
                self._send(404, b'{"error":"no such version"}',
                           "application/json")
            else:
                self._send(200, json.dumps(d).encode(), "application/json")
        elif path == "/health":
            wst = scheduler.status(SB_ROOT)
            body = json.dumps({"ok": True, "model": ENGINE.model.name,
                               "models": model_status(),
                               "brains": len(ENGINE.brains.all()),
                               "weekly": wst,
                               "weekly_phrase": _weekly_phrase(wst)})
            self._send(200, body.encode(), "application/json")
        elif path == "/diag":          # tiny connectivity self-test for one model
            name = (qs.get("model") or ["openrouter"])[0]
            m = get_model(name)
            reply = m.complete("connectivity test", "Reply with the single word: ok")
            self._send(200, json.dumps({"requested": name, "model": m.name,
                                        "reply": reply[:400]}).encode(), "application/json")
        elif path == "/memory/report":
            self._send(200, json.dumps(_memory_report()).encode(), "application/json")
        elif path == "/chats":
            self._send(200, json.dumps(_list_chats()).encode(), "application/json")
        elif path == "/chat":
            d = _get_chat((qs.get("id") or [""])[0])
            if d is None:
                self._send(404, b'{"error":"no such chat"}', "application/json")
            else:
                self._send(200, json.dumps(d).encode(), "application/json")
        elif path == "/masterlog":
            n = min(200, int((qs.get("n") or ["40"])[0] or 40))
            self._send(200, json.dumps(_master_log_tail(n)).encode(), "application/json")
        elif path == "/export":
            data = _export_brain()
            self.send_response(200)
            self.send_header("Content-Type", "application/zip")
            self.send_header("Content-Disposition",
                             'attachment; filename="sourceborn-brain.zip"')
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        elif path == "/persist":
            self._send(200, json.dumps(_persist_status()).encode(), "application/json")
        elif path == "/unfiled":
            self._send(200, json.dumps(ENGINE.unfiled.list()).encode(), "application/json")
        elif path == "/novelty":
            from .novelty import list_files, load_approved
            self._send(200, json.dumps({
                "files": list_files(SB_ROOT),
                "approved": load_approved(SB_ROOT)}).encode(), "application/json")
        elif path == "/novelty/file":
            fn = re.sub(r"[^A-Za-z0-9_.-]", "", (qs.get("name") or [""])[0])
            fp = os.path.join(SB_ROOT, "novelty", fn)
            if not (fn.startswith("NOVELTY_") and os.path.exists(fp)):
                self._send(404, b'{"error":"no such novelty file"}', "application/json")
            else:
                with open(fp, encoding="utf-8") as f:
                    body = f.read().encode()
                self.send_response(200)
                self.send_header("Content-Type", "text/markdown; charset=utf-8")
                self.send_header("Content-Disposition", f'attachment; filename="{fn}"')
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        elif path == "/weekly":
            # the accumulated pull ledger — newest first, PAGED not capped:
            # `runs` is the true count and `offset` reaches every older run, so
            # no run on disk is unreachable through the app.
            st = scheduler.status(SB_ROOT)
            lim = _int_arg(qs, "limit", 52, 1, 500)
            off = _int_arg(qs, "offset", 0, 0, 10 ** 9)
            hist = scheduler.history(SB_ROOT, limit=lim, offset=off)
            self._send(200, json.dumps({
                "status": st, "phrase": _weekly_phrase(st),
                "runs": st["runs"], "shown": len(hist),
                "limit": lim, "offset": off,
                "history": hist,
                "latest": scheduler.latest(SB_ROOT)}).encode(),
                "application/json")
        elif path == "/weekly/file":
            fn = (qs.get("name") or [""])[0]
            run = scheduler.get_run(SB_ROOT, fn)
            if run is None:
                self._send(404, b'{"error":"no such weekly run"}',
                           "application/json")
            else:
                body = json.dumps(run, ensure_ascii=False, indent=2).encode()
                safe = re.sub(r"[^0-9A-Za-z_.-]", "", fn)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Disposition",
                                 f'attachment; filename="{safe}"')
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        elif path == "/library":
            self._send(200, json.dumps(_library()).encode(), "application/json")
        elif path == "/snapshots":
            self._send(200, json.dumps(_list_snapshots()).encode(), "application/json")
        elif path == "/snapshot":
            sid = re.sub(r"[^0-9A-Za-z]", "", (qs.get("id") or [""])[0])
            fp = os.path.join(SNAP_DIR, sid + ".json")
            if not sid or not os.path.exists(fp):
                self._send(404, b'{"error":"no such snapshot"}', "application/json")
                return
            with open(fp, encoding="utf-8") as f:
                self._send(200, f.read().encode(), "application/json")
        elif path == "/brains":
            payload = {g: [{
                "id": c.node_id, "name": c.name, "kind": c.kind, "stage": c.stage,
                "human_review": c.human_review, "urr_gate": c.urr_gate,
                "risk": c.risk_level, "write": c.write_policy,
                "weekly": c.weekly_update, "gen_params": c.can_generate_parameters,
                "groups": c.tracked_groups,
            } for c in cs] for g, cs in ENGINE.brains.by_stage().items()}
            self._send(200, json.dumps(payload).encode(), "application/json")
        elif path == "/brain":
            node_id = (qs.get("id") or [""])[0]
            cfg = ENGINE.brains.get(node_id)
            if not cfg:
                self._send(404, b'{"error":"no such node"}', "application/json")
                return
            body = json.dumps({"config": asdict(cfg),
                               "memory": ENGINE.memory.brain(node_id).meta})
            self._send(200, body.encode(), "application/json")
        elif path == "/graph":
            from .nodes import SB_NODES, SB_PRIMARY_URR, URR_NODES
            nodes = ([{"id": n.sb_id, "kind": "SB", "stage": n.stage, "name": n.name}
                      for n in SB_NODES]
                     + [{"id": n.urr_id, "kind": "URR", "name": n.name} for n in URR_NODES])
            # walk order (the sequence path) + the per-node SB→URR pairing
            sb = [n.sb_id for n in SB_NODES]
            seq = [{"from": sb[i], "to": sb[i + 1], "kind": "sequence"}
                   for i in range(len(sb) - 1)]
            primary = [{"from": s, "to": u, "kind": "primary"}
                       for s, u in SB_PRIMARY_URR.items()]
            # REAL learned connections — what the weekly pass discovered
            # (Connected_Points per brain), de-duplicated as undirected pairs
            learned, seen = [], set()
            for n in nodes:
                pts = ENGINE.memory.brain(n["id"]).meta["parameters"] \
                    .get("Connected_Points") or []
                for other in pts:
                    key = tuple(sorted((n["id"], str(other))))
                    if key not in seen and key[0] != key[1]:
                        seen.add(key)
                        learned.append({"from": key[0], "to": key[1],
                                        "kind": "learned"})
            n_sb, n_all = len(SB_NODES), len(nodes)
            self._send(200, json.dumps({
                "nodes": nodes, "edges": seq + primary,
                "learned": learned[:1200],
                "mesh": {"sb_pairs": n_sb * (n_sb - 1) // 2,      # K70 = 2415
                         "all_pairs": n_all * (n_all - 1) // 2,   # K95 = 4465
                         "learned_count": len(learned)},
                "note": "full interconnection — any point can connect to any "
                        "other point (Principle 8); faint mesh = every possible "
                        "handshake, bright lines = connections actually learned"
            }).encode(), "application/json")
        else:
            self._send(404, b'{"error":"not found"}', "application/json")

    def do_POST(self) -> None:
        if not self._guard():
            return
        try:
            n = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            self._send(400, b'{"error":"bad json"}', "application/json")
            return
        if self.path == "/engine/registry":
            saved = ladder.save_registry(SB_ROOT, data,
                                         note=data.get("note", ""))
            ENGINE.memory.master_log({"event": "ladder_registry_saved",
                                      "version": saved["version"],
                                      "filled": saved["totals"]
                                      ["parameters_filled"]})
            self._send(200, json.dumps(saved["totals"] |
                                       {"version": saved["version"]}).encode(),
                       "application/json")
            return
        if self.path == "/engine/ask":
            question = (data.get("question") or "").strip()
            if not question:
                self._send(400, b'{"error":"empty question"}',
                           "application/json")
                return
            try:
                reg = ladder.load_registry(SB_ROOT)
                select = data.get("select") or []
                deselect = data.get("deselect") or []
                actions = data.get("actions") or []   # his ordered moves
                # ONE activation → the lit set and the hand are exactly what
                # the engine receives; nothing is recomputed after the answer
                # and shown as if it were the input (that used to mislead).
                lit = ladder.activate(question, reg)
                notes, hand = ladder.recall_notes(reg, lit, select, deselect)
                run_text = question
                if notes:
                    run_text += ("\n\n[recall notes from the selected "
                                 "brains]:\n" + notes)
                model = get_model(str(data.get("model", "offline")
                                      or "offline").lower())
                walk = ENGINE.run_walk(run_text, model=model)
                payload = self._walk_dict(walk["result"], walk, model.name)
                # the selection ledger travels WITH the answer: reopening the
                # chat replays exactly which brains were parked/forced, in his
                # order. This is the one human decision that used to leave no
                # trace anywhere; now it is on the chat and in the master log.
                payload["selection"] = {
                    "select": select, "deselect": deselect,
                    "actions": actions, "hand": hand}
                payload["chat_id"] = _save_chat(question, payload, "engine")
                try:
                    # summary only — the full move-by-move replay lives on the
                    # chat record; the sacred log keeps a compact trace so it
                    # doesn't accumulate the whole history on every ask. And a
                    # best-effort audit write must never sink an answer that is
                    # already saved (a disk fault here used to 500 the reply).
                    ENGINE.memory.master_log({
                        "event": "selection", "chat": payload["chat_id"],
                        "moves": len(actions), "forced": hand.get("forced", []),
                        "deselected": hand.get("deselected", []),
                        "speaking": len(hand.get("speaking", []))})
                except Exception:
                    pass
                self._send(200, json.dumps(
                    {"payload": payload, "lit": lit, "hand": hand}).encode(),
                    "application/json")
            except Exception as exc:
                self._send(500, json.dumps({"error": str(exc)}).encode(),
                           "application/json")
            return
        if self.path == "/page/save":
            layout = data.get("layout") or {}
            if not isinstance(layout.get("sections"), list):
                self._send(400, b'{"error":"layout needs sections"}',
                           "application/json")
                return
            saved = mypage.save_layout(SB_ROOT, layout,
                                       note=data.get("note", ""),
                                       references=data.get("references"))
            ENGINE.memory.master_log({"event": "mypage_saved",
                                      "version": saved["version"],
                                      "note": saved.get("note", "")})
            self._send(200, json.dumps(saved).encode(), "application/json")
            return
        if self.path == "/ingest":
            text = (data.get("text") or "").strip()
            if not text:
                self._send(400, b'{"error":"empty text"}', "application/json")
                return
            stats = _ingest_text((data.get("name") or "note").strip(), text)
            self._send(200, json.dumps({"ok": True, **stats}).encode(), "application/json")
            return
        if self.path == "/snapshot":
            self._send(200, json.dumps(_save_snapshot(data.get("name", ""))).encode(),
                       "application/json")
            return
        if self.path == "/upload":
            self._upload(data)
            return
        if self.path == "/import":
            b64 = (data.get("b64") or "").strip()
            if not b64:
                self._send(400, b'{"error":"no backup data"}', "application/json")
                return
            try:
                self._send(200, json.dumps(_import_brain(b64)).encode(),
                           "application/json")
            except Exception as exc:
                self._send(400, json.dumps({"error": f"restore failed: {exc}"}).encode(),
                           "application/json")
            return
        if self.path == "/generation/run":
            # one locked identity, one brain-state, optionally one forked event
            res = statepacks.run(
                who=(data.get("who") or "").strip(),
                pack_id=(data.get("pack") or "SP-01").strip(),
                event=(data.get("event") or "").strip(),
                rubrics=tuple(data.get("rubrics") or ()))
            self._send(200, json.dumps(res).encode(), "application/json")
            return
        if self.path == "/growth/add":
            name = (data.get("name") or "").strip()
            kind = (data.get("kind") or growth.PARAM).strip()
            if not name:
                self._send(400, json.dumps({"error": "no name"}).encode(),
                           "application/json")
                return
            row = growth.add(SB_ROOT, kind, name,
                             surfaced_by=(data.get("surfaced_by") or
                                          "added by hand"),
                             detail=(data.get("detail") or ""),
                             module=(data.get("module") or "by hand"),
                             supersedes=(data.get("supersedes") or ""))
            self._send(200, json.dumps(
                {"added": row, "counts": growth.counts(SB_ROOT)}).encode(),
                "application/json")
            return
        if self.path == "/growth/seed":
            self._send(200, json.dumps(growth.seed(SB_ROOT)).encode(),
                       "application/json")
            return
        if self.path == "/intents/run":
            res = intents.generate(
                event=(data.get("event") or "").strip(),
                active_containers=data.get("containers") or [],
                scope=(data.get("scope") or intents.CURRENT),
                conditional=bool(data.get("conditional")),
                conflict=bool(data.get("conflict")))
            self._send(200, json.dumps(res).encode(), "application/json")
            return
        if self.path == "/artifact/generate":
            # the count he asked for and never got. Gated by default.
            self._send(200, json.dumps(artifact.generate_meanings(
                max_group_size=int(data.get("size") or 3),
                limit=int(data.get("limit") or 0),
                gated=data.get("gated", True) is not False)).encode(),
                "application/json")
            return
        if self.path == "/artifact/grow":
            self._send(200, json.dumps(artifact.grow(SB_ROOT)).encode(),
                       "application/json")
            return
        if self.path == "/subjects/grow":
            # append the candidates and halts. No parameter is created.
            self._send(200, json.dumps(
                subjectbrains.grow(SB_ROOT)).encode(), "application/json")
            return
        if self.path == "/subjects/generate":
            # apply the candidates across every subject and append every setting
            # as a variant. Nothing is killed and no parameter is created.
            self._send(200, json.dumps(
                subjectbrains.grow_variants(SB_ROOT)).encode(),
                "application/json")
            return
        if self.path == "/selfmake/propose":
            # what new steps his material opens — computed, not written yet
            self._send(200, json.dumps(selfmake.propose(
                SB_ROOT, bar=int(data.get("bar") or selfmake.SUPPORT_BAR),
                repo=".")).encode(), "application/json")
            return
        if self.path == "/selfmake/extend":
            # WRITE them. The algorithm is longer afterwards. Appends only.
            self._send(200, json.dumps(selfmake.extend(
                SB_ROOT, bar=int(data.get("bar") or selfmake.SUPPORT_BAR),
                limit=int(data.get("limit") or 0), repo=".")).encode(),
                "application/json")
            return
        if self.path == "/selfmake/run":
            # run the algorithm as it currently stands
            text = (data.get("text") or "").strip()
            if not text:
                self._send(400, json.dumps({"error": "no text"}).encode(),
                           "application/json")
                return
            self._send(200, json.dumps(selfmake.run(
                SB_ROOT, text, (data.get("name") or "").strip())).encode(),
                "application/json")
            return
        if self.path == "/growing/place":
            # place one example. There is no answer here — only where it sits.
            text = (data.get("text") or "").strip()
            if not text:
                self._send(400, json.dumps({"error": "no text"}).encode(),
                           "application/json")
                return
            self._send(200, json.dumps(growing.place(
                text, (data.get("name") or "").strip())).encode(),
                "application/json")
            return
        if self.path == "/growing/grow":
            # place it AND raise the count. Appends only.
            text = (data.get("text") or "").strip()
            if not text:
                self._send(400, json.dumps({"error": "no text"}).encode(),
                           "application/json")
                return
            self._send(200, json.dumps(growing.grow(
                SB_ROOT, text, (data.get("name") or "").strip(),
                (data.get("surfaced_by") or "").strip())).encode(),
                "application/json")
            return
        if self.path == "/ledger/run":
            # his ten candidates, gated. `verdicts` is optional: with none handed
            # in, every candidate comes back UNTESTED rather than as a survivor.
            self._send(200, json.dumps(
                intent_ledger.his_run(data.get("verdicts") or None)).encode(),
                "application/json")
            return
        if self.path == "/ledger/kill":
            # the survivor stage: evidence -> contradiction -> falsification.
            # Nothing is deleted; a killed row keeps its falsifier and its reason.
            cands = [intent_ledger.candidate(c)
                     for c in (data.get("candidates") or
                               list(intent_ledger.HIS_CANDIDATES))]
            self._send(200, json.dumps(intent_ledger.survivors(
                cands, data.get("verdicts") or None)).encode(),
                "application/json")
            return
        if self.path == "/weighting/run":
            ask = (data.get("ask") or "").strip()
            if not ask:
                self._send(400, json.dumps({"error": "no ask"}).encode(),
                           "application/json")
                return
            self._send(200, json.dumps(weighting.run(ask)).encode(),
                       "application/json")
            return
        if self.path == "/asi/run":
            # one ask -> his PRIOR/CURRENT split, his two tiers over the 3,204,
            # the causal gap, his pattern candidate. The chart is generated
            # here, not typed anywhere.
            ask = (data.get("ask") or "").strip()
            if not ask:
                self._send(400, json.dumps(
                    {"error": "no ask"}).encode(), "application/json")
                return
            res = asi_pyramid.full_run(ask)
            res["chart"] = asi_pyramid.chart(res)
            self._send(200, json.dumps(res).encode(), "application/json")
            return
        if self.path == "/reading/ask":
            q = str(data.get("question", "") or "").strip()
            if not q:
                self._send(400, b'{"error":"empty ask"}', "application/json")
                return
            model = get_model(str(data.get("model", "offline") or "offline").lower())
            r = ENGINE.read(q, str(data.get("ask") or ""), model=model)
            r["flow"] = rubric_router.flow_view(r["route"])
            walk = r.pop("walk")
            payload = self._walk_dict(walk["result"], walk, model.name)
            out = payload.get("output") or {}
            r["walk"] = {"result": {"output": {
                "answer": out.get("answer"),
                "confidence": out.get("confidence"),
                "penetration_score": out.get("penetration_score")}},
                "model": model.name}
            r["chat_id"] = _save_chat(q, payload, "reading")
            try:
                ENGINE.memory.master_log({
                    "event": "reading", "ask": r["ask"],
                    "micro": len(r["micro_sequences"]),
                    "repeats": len(r["relations_to_prior"]),
                    "candidates": r["candidates"].get("created", []),
                    "mechanisms": [m["key"] for m in r["route"]["mechanisms"]]})
            except Exception:
                pass
            self._send(200, json.dumps(r, ensure_ascii=False).encode(),
                       "application/json")
            return
        if self.path == "/patterns/review":
            res = patternmem.review(SB_ROOT, str(data.get("id", "")),
                                    str(data.get("action", "")),
                                    data.get("fields") or {},
                                    str(data.get("note", "") or ""))
            if res.get("error"):
                self._send(400, json.dumps(res).encode(), "application/json")
                return
            try:
                ENGINE.memory.master_log({
                    "event": "rubric_writeback",
                    "candidate": res["candidate"]["id"],
                    "action": data.get("action"),
                    "new_version": res["candidate"]["version"],
                    "spawned": res.get("spawned", [])})
            except Exception:
                pass
            self._send(200, json.dumps(res, ensure_ascii=False).encode(),
                       "application/json")
            return
        if self.path == "/senses/teach":
            res = sensemem.teach(
                SB_ROOT, str(data.get("word", "")),
                str(data.get("his_reading", "")),
                str(data.get("default_reading", "") or ""),
                str(data.get("kind", "word_sense") or "word_sense"),
                data.get("blocks_classes"), data.get("adds_facts"),
                str(data.get("status") or sensemem.STATUS_USER),
                str(data.get("note", "") or ""),
                str(data.get("refuses", "") or ""))
            if res.get("error"):
                self._send(400, json.dumps(res).encode(), "application/json")
                return
            try:
                ENGINE.memory.master_log({
                    "event": "sense_writeback", "id": res["sense"]["id"],
                    "word": res["sense"]["word"],
                    "version": res["sense"]["version"]})
            except Exception:
                pass
            self._send(200, json.dumps(res, ensure_ascii=False).encode(),
                       "application/json")
            return
        if self.path == "/senses/reject":
            res = sensemem.reject(SB_ROOT, str(data.get("id", "")),
                                  str(data.get("note", "") or ""))
            code = 400 if res.get("error") else 200
            self._send(code, json.dumps(res, ensure_ascii=False).encode(),
                       "application/json")
            return
        if self.path == "/novelty/run":
            from .novelty import run_novelty_pass
            res = run_novelty_pass(SB_ROOT, ENGINE.memory, ENGINE.unfiled)
            self._send(200, json.dumps(res).encode(), "application/json")
            return
        if self.path == "/novelty/approve":
            term = (data.get("term") or "").strip()
            if not term:
                self._send(400, b'{"error":"need term"}', "application/json")
                return
            from .novelty import approve
            res = approve(SB_ROOT, ENGINE.memory, ENGINE.unfiled, term)
            self._send(200, json.dumps(res).encode(), "application/json")
            return
        if self.path == "/pyramid/park":
            node = (data.get("node") or "").strip()
            item = (data.get("item") or "").strip()
            level = (data.get("level") or "sub").strip()
            cat = (data.get("category") or item).strip()
            if not (node and item):
                self._send(400, b'{"error":"need node and item"}', "application/json")
                return
            b = ENGINE.memory.brain(node)
            if cat not in b.meta["pyramid"].setdefault(level, []):
                b.meta["pyramid"][level].append(cat)
            b.bump("Human_Interactions")
            b._save_meta()
            ENGINE.unfiled.park(node, item)
            ENGINE.memory.master_log({"event": "human_parked", "node": node,
                                      "item": item, "level": level, "as": cat})
            self._send(200, json.dumps({"ok": True, "left": len(ENGINE.unfiled.list())}).encode(),
                       "application/json")
            return
        if self.path == "/brain/rollback":
            node_id = (data.get("id") or "").strip()
            if not node_id:
                self._send(400, b'{"error":"need id"}', "application/json")
                return
            ok = ENGINE.memory.brain(node_id).rollback()
            ENGINE.memory.master_log({"event": "brain_rollback",
                                      "node": node_id, "ok": ok})
            self._send(200, json.dumps({"ok": ok, "node": node_id}).encode(),
                       "application/json")
            return
        if self.path == "/brains/update":
            # the manual "Weekly pull" runs the SAME full job as the scheduler
            # (settings refresh + digest + novelty), kept as a dated history
            # file — no longer the partial that skipped the novelty pass.
            res = scheduler.run_weekly(ENGINE, SB_ROOT)
            self._send(200, json.dumps(res).encode(), "application/json")
            return
        if self.path == "/brain/settings":
            node_id = (data.get("id") or "").strip()
            try:
                cfg = ENGINE.brains.update(
                    node_id, **{k: v for k, v in data.items() if k != "id"})
            except KeyError:
                self._send(404, b'{"error":"no such node"}', "application/json")
                return
            self._send(200, json.dumps({"ok": True, "config": asdict(cfg)}).encode(),
                       "application/json")
            return
        if self.path == "/review":
            self._review(data)
            return
        if self.path == "/generate":
            prompt = (data.get("prompt") or "").strip()
            if not prompt:
                self._send(400, b'{"error":"empty prompt"}', "application/json")
                return
            self._send(200, json.dumps(generate_image(prompt)).encode(), "application/json")
            return
        if self.path != "/ask":
            self._send(404, b'{"error":"not found"}', "application/json")
            return
        try:
            question = (data.get("question") or "").strip()
            if not question:
                self._send(400, b'{"error":"empty question"}', "application/json")
                return
            context = (data.get("context") or "").strip()
            if context:                      # same-chat continuation (thread)
                question = (question +
                            "\n\n[continuing our thread — your prior answer]:\n"
                            + context)
            name = str(data.get("model", "offline") or "offline").lower()
            if name == "local":              # on-device lane (browser GPU)
                self._ask_local(question, data)
                return
            model = get_model(name)
            walk = ENGINE.run_walk(question, model=model)
            payload = self._walk_dict(walk["result"], walk, model.name)
            payload["chat_id"] = _save_chat(question, payload, "ask")
            self._send(200, json.dumps(payload).encode(), "application/json")
        except Exception as exc:
            self._send(500, json.dumps({"error": str(exc)}).encode(), "application/json")

    # -- shared payload + actions -----------------------------------------
    @staticmethod
    def _walk_dict(res, walk, model_name: str, extra: dict | None = None) -> dict:
        payload = {
            "output": asdict(res.output),
            "micro_questions": res.micro_questions,
            "matched_examples": res.matched_examples,
            "trace": [asdict(t) for t in res.trace],
            "halts": res.halts,
            "memory": ENGINE.memory.stats(),
            "model": model_name,
            "walk": walk["walk"],
        }
        if extra:
            payload.update(extra)
        return payload

    @classmethod
    def _walk_payload(cls, res, walk, model_name: str,
                      extra: dict | None = None) -> bytes:
        return json.dumps(cls._walk_dict(res, walk, model_name, extra)).encode()

    def _upload(self, data: dict) -> None:
        """Phase 1: review an uploaded file. Extract text (stdlib), run the
        SB<->URR walk over it, and fold it into the brain."""
        filename = (data.get("filename") or "upload").strip()
        img_exts = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp")
        if data.get("b64") and filename.lower().endswith(img_exts):
            model = get_model(data.get("model", "offline"))
            low = filename.lower()
            mime = ("image/jpeg" if low.endswith((".jpg", ".jpeg")) else
                    "image/webp" if low.endswith(".webp") else
                    "image/gif" if low.endswith(".gif") else "image/png")
            seen = model.complete_vision(
                "You are a precise visual analyst in the user's voice.",
                f"Review the image '{filename}': what it shows, key details, and "
                "anything notable or worth flagging.", data["b64"], mime)
            _ingest_text(filename, f"[image '{filename}' seen]:\n{seen}")
            walk = ENGINE.run_walk(
                f"Review this uploaded image '{filename}':\n\n{seen}", model=model)
            self._send(200, self._walk_payload(
                walk["result"], walk, model.name,
                {"upload": {"filename": filename, "chars": len(seen),
                            "note": "vision review"}}), "application/json")
            return
        text = data.get("text")
        if text is None and data.get("b64"):
            try:
                text, note = extract_text(filename, base64.b64decode(data["b64"]))
            except Exception as exc:
                self._send(400, json.dumps({"error": f"decode failed: {exc}"}).encode(),
                           "application/json")
                return
        else:
            text, note = (text or ""), ""
        text = (text or "").strip()
        if not text:
            self._send(200, json.dumps({"error": note or "no text found in file"}).encode(),
                       "application/json")
            return
        _ingest_text(filename, text)                 # compounds the brain
        model = get_model(data.get("model", "offline"))
        ask = f"Review this uploaded file '{filename}' and respond:\n\n{text}"
        walk = ENGINE.run_walk(ask, model=model)
        payload = self._walk_dict(
            walk["result"], walk, model.name,
            {"upload": {"filename": filename, "chars": len(text), "note": note}})
        payload["chat_id"] = _save_chat(f"file: {filename}", payload, "upload")
        self._send(200, json.dumps(payload).encode(), "application/json")

    def _review(self, data: dict) -> None:
        """Human review queue: approve / add data / re-loop a held node."""
        question = (data.get("question") or "").strip()
        action = (data.get("action") or "").strip()
        node_id = (data.get("id") or "").strip()
        extra = (data.get("data") or "").strip()
        # Every human decision lands in that node's brain (Human Override
        # Ledger, per the core: Human_Interactions / Human_Decisions).
        if node_id:
            ENGINE.memory.brain(node_id).bump("Human_Interactions")
        if action == "approve":
            if node_id:
                ENGINE.memory.brain(node_id).bump("Human_Decisions")
            ENGINE.memory.master_log({"event": "human_approve", "node": node_id})
            self._send(200, json.dumps({"ok": True, "resolved": node_id}).encode(),
                       "application/json")
            return
        if not question:
            self._send(400, b'{"error":"need question to re-loop"}', "application/json")
            return
        model = get_model(data.get("model", "offline"))
        if action == "add_data" and extra:
            _ingest_text(f"review-{node_id or 'note'}", extra)
            walk = ENGINE.run_walk(question, model=model, live_override=extra)
        else:
            walk = ENGINE.run_walk(question, model=model, live_override=extra or None)
        payload = self._walk_dict(walk["result"], walk, model.name)
        payload["chat_id"] = _save_chat(question, payload, f"review-{action}")
        self._send(200, json.dumps(payload).encode(), "application/json")

    def _ask_local(self, question: str, data: dict) -> None:
        """On-device (browser-GPU) lane — two phases, so the prompt never reaches
        a third-party LLM. Phase 1: run the engine just far enough to build its
        real output prompt and hand that back to the browser. Phase 2: the
        browser returns the GPU-generated draft and the FULL SB + URR walk frames
        it. ``live_override=NO_LIVE`` keeps the private lane from phoning out
        (no Tavily), and is identical across both phases so the prompt is stable."""
        local_answer = data.get("local_answer")
        if local_answer is None:                       # phase 1 — capture prompt
            try:
                ENGINE.run_walk(question, model=CaptureModel(), live_override=NO_LIVE)
            except LocalCaptured as cap:
                self._send(200, json.dumps({
                    "stage": "need_local",
                    "system": cap.system, "prompt": cap.prompt}).encode(),
                    "application/json")
                return
            # The engine never reached the model (rare) — give the browser a sane
            # fallback so the lane still answers.
            voice = ""
            try:
                voice = ENGINE.persona.voice_guidance()
            except Exception:
                pass
            self._send(200, json.dumps({
                "stage": "need_local", "system": voice, "prompt": question}).encode(),
                "application/json")
            return
        # phase 2 — frame the on-device draft through the full walk
        walk = ENGINE.run_walk(question, model=LocalBridgeModel(str(local_answer)),
                               live_override=NO_LIVE)
        payload = self._walk_dict(walk["result"], walk, "local")
        payload["chat_id"] = _save_chat(question, payload, "ask-local")
        self._send(200, json.dumps(payload).encode(), "application/json")


def _seed_corpus_dir() -> str | None:
    """The corpus shipped with the app (raw thoughts, examples, cores). Env
    override wins; otherwise the packaged seed_corpus/ at the repo root."""
    env = os.environ.get("SB_INGEST_CORPUS")
    if env and os.path.isdir(env):
        return env
    packaged = os.path.join(os.path.dirname(__file__), "..", "..", "seed_corpus")
    packaged = os.path.abspath(packaged)
    return packaged if os.path.isdir(packaged) else None


def _maybe_ingest_on_boot() -> None:
    """Deploy-time corpus load: ingest the shipped seed_corpus (or a mounted
    SB_INGEST_CORPUS folder) once, when the brain has no corpus yet. This is how
    the user's cores/raw-thoughts/examples reach the live app automatically."""
    folder = _seed_corpus_dir()
    if not folder:
        return
    # Only auto-load if the corpus itself hasn't been ingested (idempotent).
    already = any("corpus" in e.tags
                  for e in ENGINE.memory.brain("SB-07").read_all()[:1]) \
        or any("corpus" in e.tags
               for e in ENGINE.memory.brain("SB-09").read_all()[:1])
    if already:
        return
    from .ingest import ingest_folder
    stats = ingest_folder(folder, root=os.environ.get("SB_ROOT", ".sourceborn"))
    # ingest_folder wrote through its own Memory/Persona — refresh the live
    # engine's caches so counts and voice recall see the new corpus immediately.
    ENGINE.memory._brains.clear()
    ENGINE.persona._load()
    print(f"ingested seed corpus on boot: {stats}")


def main() -> None:
    _maybe_ingest_on_boot()
    scheduler.start_weekly_scheduler(ENGINE, SB_ROOT)  # auto Monday brain update
    port = int(os.environ.get("PORT", "8000"))
    srv = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Sourceborn web service on http://0.0.0.0:{port}  (model: {ENGINE.model.name})")
    if not SB_ACCESS_PASS:
        print("!! OPEN — no SB_ACCESS_PASS set: every route is reachable by "
              "anyone with the URL. Set SB_ACCESS_PASS in the environment to "
              "lock the front door.")
    else:
        print(f"lock: on — HTTP Basic auth required (user: {SB_ACCESS_USER})")
    srv.serve_forever()


if __name__ == "__main__":
    main()
