"""THE NAMING CLEANUP — an example is an example, not a test.

PHASE 3. His ask:

    removes every test-flavoured name from the code. You found them in each
    file and they are blocking new revisions. Samrath is an example, like the
    rest — not a test. Every symbol, file and docstring that calls an example a
    test gets renamed to what it is.

    Produces: a before/after list of every renamed symbol, file and reference.
    Proof: the full rename table, plus a live run showing the example still
    reaching the same rows under its new name.
    Gate: you approve the new names.

WHY THIS MATTERS AND IS NOT COSMETIC

A test is a thing you run to see whether something is broken. An EXAMPLE is
material the system seats on and grows from — his own growing-phase ruling:

    given example are not how it provide the out comes, its for to define the
    system, where example sit on existing parameters and IDs so system can
    strong its base, every example will keep increase the count

Calling Samrath a "test" quietly reclassifies his material from FUEL into
DIAGNOSTICS. A test that passes is finished; an example is never finished,
because every example raises the count. That is why the word blocks revisions.

THE DISTINCTION THIS MODULE ENFORCES

Not every occurrence of "test" is wrong, and renaming them all would rename
HIS OWN WORDS:

  KEEP  `prior.removal_test` — HIS method, verbatim: *take the step away —
        does the thing above still stand?* `docs/mainwork/THE_REVERSE_WALKS.md`
        calls it "the removal test". It IS a test, and it is his.
  KEEP  `subjectbrains.cross_test` — running a law against other subjects to
        see if it survives. A genuine test of a law, not an example.
  KEEP  the `test_*` functions in `tests/` — those are actual tests.

  RENAME anything that calls one of HIS EXAMPLES a test.

So the scan reports two lists and never merges them. Something in KEEP is
there with the reason it is there, so the next sweep does not "fix" it.
"""

from __future__ import annotations

import os
import re

#: Occurrences of "test" that are RIGHT and must not be renamed, each with why.
KEEP = (
    {"where": "prior.removal_test",
     "why": "HIS method, verbatim — 'take the step away, does the thing above "
            "still stand?'. docs/mainwork/THE_REVERSE_WALKS.md calls it the "
            "removal test. It is a test, and the word is his."},
    {"where": "subjectbrains.cross_test",
     "why": "runs a law against other subjects to see whether it survives. A "
            "genuine test OF A LAW — not an example mislabelled."},
    {"where": "tests/test_engine.py — every test_* function",
     "why": "actual tests. The suite is allowed to call its tests tests."},
    {"where": "intents.SCALING_TEST",
     "why": "a synthetic ask-id for the scaling PROOF run — plug more "
            "containers, get more intent. Not one of his examples."},
)

#: THE RENAME TABLE — before, after, and what it is. Only entries where one of
#: HIS EXAMPLES was called a test.
RENAMES = (
    {"kind": "FILE",
     "before": "docs/method/canon/THE_SAMRATH_TEST_AND_THE_ZERO.md",
     "after": "docs/method/canon/THE_SAMRATH_EXAMPLE_AND_THE_ZERO.md",
     "what_it_is": "his Samrath sentence — an example the system seats on, "
                   "not a diagnostic that passes or fails"},
    {"kind": "HEADING",
     "before": "THE SAMRATH TEST — AND THE ZERO IT SCORED",
     "after": "THE SAMRATH EXAMPLE — AND THE ZERO IT SCORED",
     "what_it_is": "the same, in the document's own title"},
    {"kind": "PHRASE",
     "before": "his fictional father/door test",
     "after": "his fictional father/door example",
     "what_it_is": "the father-at-the-door material that produced "
                   "repetition.py — his example"},
    {"kind": "PHRASE",
     "before": "his rice/MBA test",
     "after": "his rice/MBA example",
     "what_it_is": "the rice/MBA material that produced claims.py — his "
                   "example"},
    {"kind": "PHRASE",
     "before": "HIS RICE / MBA TEST",
     "after": "HIS RICE / MBA EXAMPLE",
     "what_it_is": "the same, in a canon heading"},
)

#: His gate. The names above are applied; whether they are the RIGHT names is
#: his call, and this says so rather than assuming approval.
APPROVED_BY_HIM = False

_SEARCH = ("src", "docs", "tests", "CLAUDE.md", "README.md")


def _files(root: str = ".") -> list:
    out = []
    for p in _SEARCH:
        full = os.path.join(root, p)
        if os.path.isfile(full):
            out.append(full)
            continue
        for base, dirs, files in os.walk(full):
            dirs[:] = [d for d in dirs
                       if d not in ("__pycache__", ".git", "adopted")]
            for f in files:
                if f.endswith((".py", ".md")):
                    out.append(os.path.join(base, f))
    return sorted(out)


def scan(root: str = ".") -> dict:
    """Every place an EXAMPLE of his is still called a test.

    Reports two lists and never merges them: what should be renamed, and what
    is right as it stands with the reason it is right."""
    keep_marks = tuple(k["where"].split(".")[-1] for k in KEEP)
    found = []
    for path in _files(root):
        rel = os.path.relpath(path, root)
        if rel.startswith("tests" + os.sep):
            continue                      # the suite may call its tests tests
        if os.path.basename(rel) == "naming.py":
            # this module HOLDS the rename table, so every `before` string
            # appears in it by definition. Scanning itself would report the
            # table as the defect — the same self-reference trap the angles
            # docstring hit.
            continue
        try:
            txt = open(path, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        for r in RENAMES:
            if r["kind"] == "FILE":
                continue
            for m in re.finditer(re.escape(r["before"]), txt):
                line = txt[:m.start()].count("\n") + 1
                found.append({"file": rel, "line": line,
                              "before": r["before"], "after": r["after"],
                              "what_it_is": r["what_it_is"]})
    files = [{"file": r["before"], "after": r["after"],
              "exists": os.path.exists(os.path.join(root, r["before"])),
              "what_it_is": r["what_it_is"]}
             for r in RENAMES if r["kind"] == "FILE"]
    return {
        "his_words": "Samrath is an example, like the rest — not a test",
        "still_calling_an_example_a_test": found,
        "count": len(found),
        "files_to_rename": files,
        "kept_and_why": list(KEEP),
        "kept": len(KEEP),
        "approved_by_him": APPROVED_BY_HIM,
        "law": "a test is run to see whether something is broken; an example "
               "is material the system seats on and grows from. Calling his "
               "example a test reclassifies his fuel as diagnostics.",
    }


def table() -> list:
    """THE BEFORE/AFTER LIST he asked for as the product."""
    return [dict(r, approved_by_him=APPROVED_BY_HIM) for r in RENAMES]


def verify() -> dict:
    """HIS PROOF: the example still reaches the same rows under its new name.

    A rename that changed a reading would be a rename that changed the system.
    Samrath's fixed result is pinned elsewhere at 18 · 106 rows · 16
    containers; this re-runs it and reports the numbers beside the rename."""
    from . import asi_pyramid as P
    his = ("Samrath never like to go to school, he always cry, but today is "
           "his birthday, he went very happy.")
    a = P.activate(his)["counts"]
    r = P.rows_for(his)["counts"]
    return {
        "example": "the Samrath sentence, in his exact wording",
        "activate": {"strong": a["strong"], "candidate": a["candidate"],
                     "working": a["working"], "bank": a["bank"]},
        "rows": r["rows"], "containers": r["containers"],
        "segments": r["segments"],
        "unchanged_by_the_rename": (a["working"] == 18 and r["rows"] == 106
                                    and r["containers"] == 16),
        "why": "a rename that moved a reading would be a rename that changed "
               "the system. The name changed; the reading did not.",
    }


def stats(root: str = ".") -> dict:
    s = scan(root)
    return {
        "renames": len(RENAMES),
        "files": sum(1 for r in RENAMES if r["kind"] == "FILE"),
        "phrases": sum(1 for r in RENAMES if r["kind"] != "FILE"),
        "still_found": s["count"],
        "kept_correctly": len(KEEP),
        "approved_by_him": APPROVED_BY_HIM,
        "law": "an example is an example. Only what calls HIS EXAMPLE a test "
               "is renamed; his own 'removal test' keeps its name because the "
               "word is his and it really is a test.",
    }


def annotations() -> list:
    return [
        ("Samrath is an example, like the rest — not a test", "naming.RENAMES"),
        ("a before/after list of every renamed symbol and reference",
         "naming.table"),
        ("his own removal test keeps its name", "naming.KEEP"),
        ("the example still reaches the same rows under its new name",
         "naming.verify"),
    ]
