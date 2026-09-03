"""THE PEN — the app rewrites its own code, on his word (2026-09-03).

HIS ASK, VERBATIM:

    "as m feeding example and setting some rules in the system i want an app
     where i keep changing n it should rewrite its own code and make changes /
     but as our turn app ASI is not able to do, suggest me and discuss how
     many options i have / and accordignly the dashboard will prepared not
     what we have"

Four paths were put to him by name — rules-as-data only · staged assembly ·
self-patch full auto · agent-outside requests — each with what it trades. HE
CHOSE: **"Self-patch, full auto"**, whose stated meaning was *"Teach → the app
patches itself → tests green → merges and deploys with no word from you."*
That choice is the mode this module ships in. There is no approval step
between a green suite and the push; the approval he keeps is AFTER the fact —
the ledger shows every patch whole, and revert is one click and one new
commit.

HOW ONE TEACH RUNS, END TO END

    his teaching ──► the drafter (a real model writes the patch — the offline
    echo can never become one) ──► the parse (strict format, field check,
    compile check) ──► THE SHADOW: the whole repo is copied aside, the patch
    applied there, and the FULL suite run against it ──► red: the patch is
    FILED with the failure, never applied ──► green: committed straight to
    the deploy branch through the GitHub API ──► Render auto-deploys ──► the
    running app is now the app the pen wrote.

THE FOUR LAWS OF THE PEN

1.  THE FIELD. The pen writes only inside its field: ``src/sourceborn/*.py``
    minus five held files, plus ``README.md``. Everything else — his canon,
    his method docs, his source banks, the adopted trees under custody, his
    standing orders, the suite — is NEVER machine-rewritten. This is how his
    rule 2 ("never change the core without showing the proposed change first")
    survives full auto: THE CORE IS HIS WORDS AND HIS BANKS, and the pen
    cannot reach them structurally. Mechanisms are patchable; the law is not.

2.  THE GATE IS THE SUITE. His word is not asked before a merge — he chose
    that — so something else must hold the line, and it is the same thing
    that holds it for every phase built here: the full test suite, run
    against a shadow copy, exit status checked unmasked. Every law already
    pinned by a test (append-only ledgers, no selection paths, NOT RECORDED
    never filled, the bank never shrinking) therefore still binds the pen:
    a patch that breaks one cannot deploy. And the pen may not rewrite the
    suite (law 1), so it cannot lower the bar it must clear.

3.  APPEND ONLY, NOTHING LOST. Every teach is a ledger row carrying his
    teaching verbatim, the pen's why, every file's full BEFORE and AFTER,
    the suite verdict, and the commit. A refused patch is filed with its
    refusal; a red patch is filed with its failure; git history keeps every
    pushed version forever. ``revert()`` writes a NEW commit restoring what
    stood before — it erases nothing, and the reverted row stays whole.

4.  THE DOOR. The pen pushes into HIS GitHub with HIS token and drafts with
    HIS model key. An open door would hand that pen to anyone holding the
    URL — the repo write, not the exploration, is what must not be public.
    So ``teach`` and ``revert`` refuse until ``SB_ACCESS_PASS`` is set (the
    Phase-0 front door he already accepted). This is the lock on his
    credential, not a gate on him: with the password set, his teach deploys
    with no further word.

WHAT ARMS IT (his three switches, all in Render's Environment tab — the
machinery ships whole and inert until they exist, which keeps his staging
law true even in full auto: turning it on is HIS physical action):

    SB_GITHUB_TOKEN   a fine-grained token, Contents read/write, this repo only
    SB_REPO           owner/name of the deploy repo (e.g. damandamanaulakh-tech/ASI)
    a model key       ANTHROPIC_API_KEY / XAI_API_KEY / … (SB_PATCH_MODEL picks)

A green patch with no token is HELD-UNARMED with the whole patch kept in the
row — arm later, nothing is lost. The push lands on ``SB_BRANCH`` (default
``main``), which is the branch Render deploys.

WHAT THIS IS NOT, SAID PLAINLY: the pen runs when HE teaches. It does not
teach itself on a timer — the machine feeding its own output back into its
own code is the AUTO_SUSTAIN question, which stands at his gate untouched.
"""

from __future__ import annotations

import difflib
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

from .models import _now

#: The repo tree this running app was deployed from.
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", ".."))

#: Held inside the field — five files the pen may never rewrite, each with the
#: reason. A gate must not be editable by the thing it gates.
HELD_FROM_THE_PEN = {
    "server.py": "the front door and every route live here — the pen may not "
                 "move its own lock",
    "selfpatch.py": "the pen may not rewrite the pen — the gate is not "
                    "editable by what it gates",
    "selfhome.py": "the page that shows him every patch — the pen may not "
                   "redraw its own witness",
    "safety.py": "rule 10 of his standing orders — the safety line stays",
    "llm.py": "his keys pass through here — key handling is not the pen's",
}

#: Never touched at all — outside the field entirely, each with the reason.
#: His canon, his banks, his orders, the suite, the deploy rails.
NEVER_TOUCHED = (
    ("docs/", "his words, his canon, his method — never machine-rewritten"),
    ("adopted/", "byte-identical custody under SHA-256, frozen on his "
                 "adoption order"),
    ("data/", "his source banks — read by everything, written by nothing"),
    ("tests/", "the suite IS the gate; the pen may not rewrite the bar it "
               "must clear"),
    ("seed_corpus/", "his raw material, captured verbatim"),
    (".sourceborn/", "his private brain — git-ignored, never committed"),
    (".github/", "the deploy rails"),
    ("CLAUDE.md", "his standing orders — the anti-divert anchor"),
    ("render.yaml", "the deploy rails"),
    ("app.py", "the boot line — a broken boot bricks the deploy"),
)

MAX_FILES = 3           # one teaching = one small patch, not a rewrite spree
MAX_BYTES = 200_000     # total patch size cap, reported when it bites


def allowed(path: str) -> tuple:
    """(ok, reason). Default-deny: the field is named, everything else is not
    in it. A path that climbs out of the tree is refused before any prefix
    check can be fooled by it."""
    p = (path or "").replace("\\", "/").strip()
    if not p or p.startswith(("/", "~")):
        return False, "only a path inside the repo tree"
    norm = os.path.normpath(p).replace("\\", "/")
    if norm.startswith("..") or norm == ".":
        return False, "a path that climbs out of the tree is refused"
    for prefix, why in NEVER_TOUCHED:
        if norm == prefix.rstrip("/") or norm.startswith(prefix):
            return False, why
    if norm == "README.md":
        return True, ("maintenance surface — and the suite pins its route "
                      "list and its test count, so a false claim goes red")
    if (norm.startswith("src/sourceborn/") and norm.endswith(".py")
            and norm.count("/") == 2):
        base = norm.rsplit("/", 1)[1]
        if base in HELD_FROM_THE_PEN:
            return False, HELD_FROM_THE_PEN[base]
        return True, "inside the pen's field"
    return False, ("outside the pen's field — the field is src/sourceborn/"
                   "*.py minus the five held files, plus README.md")


def field() -> list:
    """The modules the pen may rewrite, read from disk — never a typed list."""
    d = os.path.join(ROOT, "src", "sourceborn")
    return sorted(f for f in os.listdir(d)
                  if f.endswith(".py") and f not in HELD_FROM_THE_PEN)


def door() -> dict:
    """Law 4. The pen writes into HIS GitHub with HIS keys, so the front door
    must be shut before the pen moves — anyone with the URL is not him."""
    return {
        "locked": bool(os.environ.get("SB_ACCESS_PASS", "")),
        "law": "teach and revert refuse while SB_ACCESS_PASS is unset. This "
               "locks his token against strangers; it gates nothing for him — "
               "with the password set, a green patch deploys with no further "
               "word, which is the mode he chose.",
    }


def arming() -> dict:
    """Which of his three switches exist. Presence only — a secret's value
    never leaves the environment."""
    from . import llm
    name = os.environ.get("SB_PATCH_MODEL", "").strip().lower()
    m = llm.get_model(name) if name else llm.default_model()
    token = bool(os.environ.get("SB_GITHUB_TOKEN", ""))
    repo = os.environ.get("SB_REPO", "").strip()
    return {
        "SB_GITHUB_TOKEN": token,
        "SB_REPO": repo or None,
        "SB_BRANCH": os.environ.get("SB_BRANCH", "main"),
        "drafting_model": m.name,
        "model_armed": m.name != "offline",
        "armed": token and bool(repo) and m.name != "offline",
        "values_shown": "presence only — a token value never leaves the "
                        "environment",
    }


def _pick_model():
    from . import llm
    name = os.environ.get("SB_PATCH_MODEL", "").strip().lower()
    return llm.get_model(name) if name else llm.default_model()


# ---------------------------------------------------------------------------
# THE DRAFTER — a real model writes the patch, inside the laws
# ---------------------------------------------------------------------------

_LAWS_FOR_THE_DRAFTER = """You are the patch drafter inside Sourceborn, a \
private reasoning engine whose owner teaches it by example and rule. He has \
chosen full auto: what you write, if the whole test suite passes on it, is \
committed and deployed with no human review — so write the SMALLEST change \
that genuinely carries his teaching into the code, and nothing beyond it.

REPLY FORMAT — STRICT, nothing outside these blocks:
  If you must read source before writing, reply ONLY:
      <<<NEED>>>module.py, other.py<<<END NEED>>>          (max 3)
  Otherwise reply with exactly one WHY and 1..3 FILE blocks:
      <<<WHY>>>one short paragraph: what his teaching required and what \
changed<<<END WHY>>>
      <<<FILE src/sourceborn/name.py>>>
      the ENTIRE new file content, top to bottom
      <<<END FILE>>>
  Full files only — never a fragment, never a diff. A reply that does not \
parse is filed as refused and applied to nothing.

THE FIELD: you may write only src/sourceborn/*.py (NOT server.py, \
selfpatch.py, selfhome.py, safety.py, llm.py) and README.md. Never docs/, \
tests/, data/, adopted/, seed_corpus/, CLAUDE.md, render.yaml, app.py, \
.github/. A patch outside the field is refused unrun.

HOUSE LAWS the suite will enforce on you: ledgers are append-only (no \
delete/pop/truncate paths); nothing is ever removed, a later reading \
supersedes and both stay; the source banks never shrink; nothing is chosen \
for the owner — surface candidates, never conclude; NOT RECORDED / UNTESTED \
are honest values, never filled in; matched on the name, never the number; \
his exact words are preserved verbatim where they appear. Keep every \
existing test green. Match the project's idiom: stdlib only, docstrings that \
carry the owner's words and the reason, plain data structures. Do not name \
any AI model or name yourself anywhere in the content — the code speaks for \
the system, not for its drafter."""


def parse_reply(text: str) -> dict:
    """Strict parse of a drafter reply. Refusals name what was wrong; a HELD
    refusal carries the path so the ledger can show what was reached for."""
    t = text or ""
    need = re.findall(r"<<<NEED>>>(.*?)<<<END NEED>>>", t, re.S)
    if need:
        mods = [n.strip() for n in need[0].split(",") if n.strip()]
        return {"need": mods[:3]}
    blocks = re.findall(r"<<<FILE (.*?)>>>\n(.*?)<<<END FILE>>>", t, re.S)
    why = re.findall(r"<<<WHY>>>(.*?)<<<END WHY>>>", t, re.S)
    if not blocks:
        return {"refused": "no <<<FILE ...>>> block parsed — a reply that is "
                           "not a patch is applied to nothing"}
    if len(blocks) > MAX_FILES:
        return {"refused": "%d files in one patch — the cap is %d, one "
                           "teaching is one small change" % (len(blocks),
                                                             MAX_FILES)}
    files, total = {}, 0
    for path, content in blocks:
        path = path.strip()
        ok, reason = allowed(path)
        if not ok:
            return {"refused": "HELD — %s: %s" % (path, reason), "held": path}
        if not content.endswith("\n"):
            content += "\n"
        if path.endswith(".py"):
            try:
                compile(content, path, "exec")
            except SyntaxError as exc:
                return {"refused": "does not compile — %s: %s" % (path, exc)}
        total += len(content.encode("utf-8"))
        files[path] = content
    if total > MAX_BYTES:
        return {"refused": "patch is %d bytes — the cap is %d" % (total,
                                                                  MAX_BYTES)}
    return {"files": files, "why": (why[0].strip() if why else "")}


def _module_map() -> str:
    """One line per field module — name plus its own first docstring line —
    so the drafter can aim without being handed the whole tree."""
    lines = []
    d = os.path.join(ROOT, "src", "sourceborn")
    for name in field():
        head = ""
        try:
            with open(os.path.join(d, name), encoding="utf-8") as f:
                src = f.read(4000)
            m = re.search(r'"""(.*?)$', src, re.M)
            head = (m.group(1).strip() if m else "")[:100]
        except Exception:
            pass
        lines.append("%-22s %s" % (name, head))
    return "\n".join(lines)


def _read_module(name: str) -> str | None:
    base = name.strip()
    if not base.endswith(".py"):
        base += ".py"
    base = os.path.basename(base)
    p = os.path.join(ROOT, "src", "sourceborn", base)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return f.read()


def _draft(teaching: str, target: str, model) -> dict:
    """One draft, at most one NEED round. Returns parse_reply's shape plus
    the raw head of the reply for the ledger."""
    prompt = "HIS TEACHING, VERBATIM:\n%s\n\nTHE FIELD (module -> its own " \
             "first line):\n%s\n" % (teaching, _module_map())
    if target:
        src = _read_module(target)
        if src is not None:
            prompt += "\nHE NAMED THE TARGET. CURRENT SOURCE OF %s:\n%s\n" % (
                target, src)
    reply = model.complete(_LAWS_FOR_THE_DRAFTER, prompt, max_tokens=16000)
    parsed = parse_reply(reply)
    if "need" in parsed:
        srcs = []
        for name in parsed["need"]:
            src = _read_module(name)
            if src is not None:
                srcs.append("CURRENT SOURCE OF %s:\n%s" % (name, src))
        prompt2 = prompt + "\nYOU ASKED TO READ:\n\n" + "\n\n".join(srcs) + \
            "\n\nNow reply with WHY + FILE blocks only."
        reply = model.complete(_LAWS_FOR_THE_DRAFTER, prompt2,
                               max_tokens=16000)
        parsed = parse_reply(reply)
        if "need" in parsed:
            parsed = {"refused": "the drafter asked to read twice — one NEED "
                                 "round is the cap"}
    parsed["reply_head"] = (reply or "")[:400]
    return parsed


# ---------------------------------------------------------------------------
# THE SHADOW — the full suite runs on a copy before anything is real
# ---------------------------------------------------------------------------

def _shadow(files: dict, suite: str = "tests/test_engine.py",
            timeout: int = 900) -> dict:
    """Copy the whole tree aside, write the patch there, run the suite there.
    The child runs with SB_SELFPATCH_SHADOW=1 so the pen's own shadow-running
    tests stand down inside it — a shadow may not open another shadow."""
    import shutil
    import tempfile
    top = tempfile.mkdtemp(prefix="sb-shadow-")
    dst = os.path.join(top, "tree")
    try:
        shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(
            ".git", ".sourceborn*", "__pycache__", "*.pyc", "sb-shadow-*"))
        for rel, content in files.items():
            p = os.path.join(dst, rel.replace("/", os.sep))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(content)
        env = dict(os.environ)
        env["SB_SELFPATCH_SHADOW"] = "1"
        env["PYTHONPATH"] = "src"
        try:
            r = subprocess.run([sys.executable, suite], cwd=dst, env=env,
                               capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return {"green": False, "tests": None,
                    "tail": "the suite did not finish inside %ds" % timeout}
        tail = ((r.stdout or "") + "\n" + (r.stderr or ""))[-4000:]
        m = re.search(r"(\d+)/(\d+) tests passed", tail)
        return {"green": r.returncode == 0,
                "tests": (m.group(0) if m else None), "tail": tail}
    finally:
        # the SCRATCH copy is deleted — never the ledger, never the tree.
        # 45MB per teach would otherwise eat the disk allowance.
        shutil.rmtree(top, ignore_errors=True)


# ---------------------------------------------------------------------------
# THE PUSH — straight to the deploy branch through the GitHub git-data API
# ---------------------------------------------------------------------------

def _http(method: str, url: str, payload, token: str) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "User-Agent": "sourceborn-pen",
        "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8", "ignore"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "ignore")[:300]
        raise RuntimeError("GitHub %s %s -> %s %s" % (method, url.split(
            "github.com")[-1], exc.code, body))


def _push(files: dict, message: str, transport=None) -> dict:
    """One commit on the deploy branch: blobs -> tree -> commit -> ref. A file
    whose content is None becomes a deletion entry (revert of a created file).
    force is never sent true — if the head moved underneath, the ref update
    fails and the teach is filed REFUSED-PUSH rather than clobbering anyone."""
    token = os.environ["SB_GITHUB_TOKEN"]
    repo = os.environ["SB_REPO"].strip()
    branch = os.environ.get("SB_BRANCH", "main")
    t = transport or _http
    api = "https://api.github.com/repos/" + repo
    head = t("GET", api + "/git/ref/heads/" + branch, None, token)["object"]["sha"]
    base_tree = t("GET", api + "/git/commits/" + head, None, token)["tree"]["sha"]
    entries = []
    for path in sorted(files):
        content = files[path]
        if content is None:
            entries.append({"path": path, "mode": "100644", "type": "blob",
                            "sha": None})
            continue
        blob = t("POST", api + "/git/blobs",
                 {"content": content, "encoding": "utf-8"}, token)["sha"]
        entries.append({"path": path, "mode": "100644", "type": "blob",
                        "sha": blob})
    tree = t("POST", api + "/git/trees",
             {"base_tree": base_tree, "tree": entries}, token)["sha"]
    commit = t("POST", api + "/git/commits",
               {"message": message, "tree": tree, "parents": [head]}, token)["sha"]
    t("PATCH", api + "/git/refs/heads/" + branch,
      {"sha": commit, "force": False}, token)
    return {"sha": commit, "parent": head, "repo": repo, "branch": branch}


def _scrub(text: str) -> str:
    """Nothing pushed carries a model's name — the code speaks for the
    system, not for its drafter. Applied to the drafter's WHY before it can
    enter a commit message."""
    out = text or ""
    for word in ("claude", "anthropic", "gpt", "openai", "grok", "xai",
                 "gemini", "opus", "sonnet"):
        out = re.sub(r"(?i)\b%s[\w.-]*\b" % word, "the pen", out)
    return out


def _commit_message(rid: str, teaching: str, why: str, tests) -> str:
    head = " ".join(teaching.split())[:60]
    body = _scrub(why).strip()
    return ("SELF-PATCH %s: %s\n\n" % (rid, head)
            + (body + "\n\n" if body else "")
            + "Written by the pen; the full suite ran green in shadow (%s) "
              "before this push. Taught through /selfpatch/teach; the whole "
              "row — teaching, before, after, verdict — is in the patch "
              "ledger." % (tests or "exit 0"))


# ---------------------------------------------------------------------------
# THE LEDGER — append only. There is no counterpart to _append.
# ---------------------------------------------------------------------------

def _ledger(root: str) -> str:
    d = os.path.join(root or ".", "selfpatch")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "patches.jsonl")


def _append(root: str, row: dict) -> None:
    with open(_ledger(root), "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def load(root: str) -> list:
    """Every row ever, in order. A corrupt line is reported, never dropped."""
    p = _ledger(root)
    if not os.path.exists(p):
        return []
    rows = []
    with open(p, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception as exc:
                rows.append({"kind": "UNREADABLE", "line": i,
                             "raw": line[:200], "error": str(exc)})
    return rows


# ---------------------------------------------------------------------------
# TEACH — the whole loop, his choice executed
# ---------------------------------------------------------------------------

def teach(text: str, target: str = "", root: str = ".sourceborn",
          model=None, transport=None, shadow: bool = True,
          suite: str = "tests/test_engine.py", timeout: int = 900) -> dict:
    """One teaching, end to end. Every outcome — refusal included — is a row;
    a knock at an open door is filed so he can see someone knocked."""
    rows = load(root)
    rid = "SB-PATCH-%04d" % (
        sum(1 for r in rows if r.get("kind") == "PATCH") + 1)
    row = {"id": rid, "kind": "PATCH", "at": _now(),
           "teaching": text, "target": target or None, "stages": []}

    def stage(name: str, **kw) -> None:
        row["stages"].append(dict({"stage": name}, **kw))
        row["stage"] = name

    if not door()["locked"]:
        stage("REFUSED-DOOR-OPEN", why=door()["law"])
        _append(root, row)
        return row

    m = model or _pick_model()
    if getattr(m, "name", "offline") == "offline":
        stage("REFUSED-NO-MODEL",
              why="no drafting key is set — the offline echo can never "
                  "become a patch, structurally: it does not parse as one")
        _append(root, row)
        return row

    stage("RECEIVED", drafter=m.name)
    d = _draft(text, target, m)
    if "refused" in d:
        stage("REFUSED-HELD" if "held" in d else "REFUSED-MALFORMED",
              why=d["refused"], reply_head=d.get("reply_head", ""))
        _append(root, row)
        return row

    files = d["files"]
    was = {}
    for p in files:
        fp = os.path.join(ROOT, p.replace("/", os.sep))
        was[p] = (open(fp, encoding="utf-8").read()
                  if os.path.exists(fp) else None)
    row["why_the_pen_wrote_it"] = d.get("why", "")
    row["files"] = sorted(files)
    row["was"] = was
    row["now"] = files
    stage("DRAFTED", files=sorted(files),
          bytes=sum(len(c.encode("utf-8")) for c in files.values()))

    tests = None
    if shadow:
        sh = _shadow(files, suite=suite, timeout=timeout)
        if not sh["green"]:
            stage("SHADOW-RED", tests=sh.get("tests"),
                  tail=(sh.get("tail") or "")[-1500:])
            _append(root, row)
            return row
        tests = sh.get("tests")
        stage("SHADOW-GREEN", tests=tests)

    a = arming()
    if not (a["SB_GITHUB_TOKEN"] and a["SB_REPO"]):
        stage("HELD-UNARMED",
              why="green and ready — set SB_GITHUB_TOKEN and SB_REPO in "
                  "Render to arm the push. The whole patch is kept in this "
                  "row; nothing is lost by arming later.")
        _append(root, row)
        return row

    try:
        pushed = _push(files, _commit_message(rid, text, d.get("why", ""),
                                              tests), transport)
    except Exception as exc:
        stage("REFUSED-PUSH", why=str(exc)[:400])
        _append(root, row)
        return row

    row["sha"] = pushed["sha"]
    stage("PUSHED", sha=pushed["sha"], parent=pushed["parent"],
          repo=pushed["repo"], branch=pushed["branch"],
          deploys="Render auto-deploys this branch — the running app becomes "
                  "the patched app on the next deploy, minutes, not this "
                  "instant")
    _append(root, row)
    return row


def revert(row_id: str, root: str = ".sourceborn", transport=None) -> dict:
    """His after-the-fact authority: one click, one NEW commit restoring what
    stood before the named patch. The patch row is untouched; git keeps both
    versions forever. A file the patch created is deleted by the revert —
    that too is a tree entry in a new commit, not an erasure of history."""
    if not door()["locked"]:
        return {"refused": door()["law"]}
    rows = load(root)
    tgt = next((r for r in rows if r.get("id") == row_id
                and r.get("stage") == "PUSHED"), None)
    if tgt is None:
        return {"refused": "no PUSHED row %s — only a pushed patch can be "
                           "reverted" % row_id}
    files = {p: tgt.get("was", {}).get(p) for p in tgt.get("files", [])}
    msg = ("REVERT %s on his word\n\nRestores what stood before commit %s. "
           "The patch row stays whole in the ledger and the commit stays in "
           "history — this revert is its own new commit, nothing is erased."
           % (row_id, tgt.get("sha", "")))
    try:
        pushed = _push(files, msg, transport)
    except Exception as exc:
        return {"refused": str(exc)[:400]}
    row = {"id": "SB-REVERT-%04d" % (
               sum(1 for r in rows if r.get("kind") == "REVERT") + 1),
           "kind": "REVERT", "at": _now(), "of": row_id,
           "sha": pushed["sha"], "stage": "PUSHED"}
    _append(root, row)
    return row


# ---------------------------------------------------------------------------
# WHAT THE PAGE READS
# ---------------------------------------------------------------------------

def _diff(was: str | None, now: str | None, path: str) -> str:
    a = (was or "").splitlines(keepends=True)
    b = (now or "").splitlines(keepends=True)
    out = "".join(difflib.unified_diff(a, b, fromfile="was/" + path,
                                       tofile="now/" + path, n=2))
    return out[:6000]


def report(root: str = ".sourceborn", limit: int = 30) -> dict:
    """The feed: newest first, each row with real diffs computed from its own
    was/now — the page never re-reads the tree, so a restored ledger still
    shows exactly what each patch did."""
    rows = load(root)
    out = []
    for r in reversed(rows[-limit * 2:]):
        if len(out) >= limit:
            break
        if r.get("kind") == "UNREADABLE":
            out.append(r)
            continue
        slim = {k: r.get(k) for k in ("id", "kind", "at", "teaching",
                                      "target", "stage", "stages", "files",
                                      "why_the_pen_wrote_it", "sha", "of")}
        if r.get("kind") == "PATCH" and r.get("files"):
            slim["diffs"] = [{"path": p,
                              "created": r.get("was", {}).get(p) is None,
                              "diff": _diff(r.get("was", {}).get(p),
                                            r.get("now", {}).get(p), p)}
                             for p in r["files"]]
        out.append(slim)
    return {"rows": out, "total": len(rows)}


def state(root: str = ".sourceborn") -> dict:
    rows = load(root)
    counts: dict = {}
    for r in rows:
        key = r.get("stage") or r.get("kind") or "?"
        counts[key] = counts.get(key, 0) + 1
    return {
        "mode": "FULL AUTO — his choice, 2026-09-03: tests green = merged "
                "and deployed, no approval step; his authority is the ledger "
                "and the one-click revert",
        "door": door(),
        "arming": arming(),
        "field": {"modules": len(field()), "plus": ["README.md"],
                  "held": HELD_FROM_THE_PEN,
                  "never": [{"path": p, "why": w} for p, w in NEVER_TOUCHED]},
        "patches": sum(1 for r in rows if r.get("kind") == "PATCH"),
        "pushed": sum(1 for r in rows if r.get("kind") == "PATCH"
                      and r.get("stage") == "PUSHED"),
        "reverts": sum(1 for r in rows if r.get("kind") == "REVERT"),
        "counts": counts,
        "laws": ["the field — his core is unreachable, structurally",
                 "the gate is the suite, run whole against a shadow copy",
                 "append only — refusals filed, reverts are new commits",
                 "the door — the pen moves only behind his password"],
    }


def annotations() -> list:
    return [
        ("i want an app where i keep changing n it should rewrite its own "
         "code and make changes", "selfpatch.teach"),
        ("Self-patch, full auto — tests green, merges and deploys with no "
         "word from him", "selfpatch.state"),
        ("what the pen may never touch", "selfpatch.NEVER_TOUCHED"),
        ("the gate that replaces his word is the whole suite, run in shadow",
         "selfpatch._shadow"),
        ("revert is a new commit, never an erasure", "selfpatch.revert"),
    ]
