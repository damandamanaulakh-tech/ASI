"""THE FILE MAP — every file in the repo divided by the job it does in the
GROWING PHASE.

His order:

    Now u make list of all file on repo
    reread each single extract for above motive
    do not try to use ur fucking stupid brain
    devide all files as per the above requirement

THE REQUIREMENT HE STATED, IN HIS WORDS

    current phase is growing phase, given example are not how it provide the out
    comes, its for to define the system, where example sit on existing parameters
    and IDs so system can strong its base, every example will keep increase the
    count

    Its universal moto t follow is "everything happening is a event, and all
    events have intent"

    as long i keep adding the example, once the basic will over it will start
    making new combinations on new thoughts

So a file is not divided by topic. It is divided by **what it does to the base**:

    SOURCE      his own raw words. The origin. Never interpreted, never flattened.
    EXAMPLE     material that SEATS on existing parameters and IDs and raises the
                count. This is the growing phase's fuel.
    METHOD      his rulings and canon. Defines HOW, and is never itself run as an
                example.
    BANK        the parameters and IDs themselves — what an example seats onto.
    SYSTEM      the code that does the seating.
    ARTIFACT    a run, a subject the system was pointed at, or an output.
    OPERATIONS  hosting, config, tests, licence — carries no intent to read.

`SOURCE` and `EXAMPLE` are what grow the count. `METHOD` and `BANK` are what they
grow against. Nothing is dropped and nothing is ranked — a file with no job here
is reported `UNPLACED`, not deleted and not guessed at.

This module reads the git tree. It does not contain a typed list of 479 names.
"""

from __future__ import annotations

import os
import subprocess

MOTTO = "everything happening is a event, and all events have intent"
PHASE = "GROWING"

SOURCE = "SOURCE"
EXAMPLE = "EXAMPLE"
METHOD = "METHOD"
BANK = "BANK"
SYSTEM = "SYSTEM"
ARTIFACT = "ARTIFACT"
OPERATIONS = "OPERATIONS"
UNPLACED = "UNPLACED"

CLASSES = (SOURCE, EXAMPLE, METHOD, BANK, SYSTEM, ARTIFACT, OPERATIONS, UNPLACED)

JOB = {
    SOURCE: "his own words, captured before interpretation. The origin of every "
            "parameter that follows.",
    EXAMPLE: "seats on existing parameters and IDs, strengthens the base, and "
             "raises the count. The fuel of the growing phase.",
    METHOD: "his rulings and canon — defines the system. Never run as an example "
            "against itself.",
    BANK: "the parameters and IDs themselves. What an example seats onto.",
    SYSTEM: "the code that finds the events, opens the intent, and does the "
            "seating.",
    ARTIFACT: "a run, or a subject the system was pointed at. An output, not an "
              "input.",
    OPERATIONS: "hosting, packaging, tests, licence. Carries no intent to read.",
    UNPLACED: "no job established here. Reported, never dropped, never guessed.",
}


def _tree(root: str = ".") -> list:
    """The real file list, from git. Not a typed inventory."""
    try:
        out = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True,
                             text=True, timeout=60)
        if out.returncode == 0 and out.stdout.strip():
            return sorted(p for p in out.stdout.splitlines() if p.strip())
    except Exception:
        pass
    found = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", ".sourceborn")]
        for f in files:
            found.append(os.path.relpath(os.path.join(base, f), root))
    return sorted(found)


# The bank files by name — the parameters and IDs themselves, not text about them.
_BANK_FILES = ("data/human_registry.json",)
_BANK_MODULES = ("human_registry.py", "registry.py")


def classify(path: str) -> dict:
    """One file -> the job it does to the base. Rules read the path, in order."""
    p = path.replace("\\", "/")
    low = p.lower()
    base = os.path.basename(p)
    ext = os.path.splitext(base)[1].lower()

    def r(cls, why):
        return {"path": p, "class": cls, "why": why, "job": JOB[cls]}

    # the bank first — it is what everything else seats onto
    if p.endswith(_BANK_FILES) or base in _BANK_MODULES:
        return r(BANK, "the parameter/ID bank itself — his 3,204 named rows")

    # his method: rulings, canon, the core spec
    if low.startswith("docs/method/"):
        if "/canon/" in low:
            return r(METHOD, "canon — his teaching, filed in his words")
        if ext in (".py",):
            return r(SYSTEM, "draws his method; code, not doctrine")
        if ext in (".png", ".svg"):
            return r(METHOD, "his sequence chart — the method drawn")
        return r(METHOD, "his binding method document")
    if base in ("CLAUDE.md",):
        return r(METHOD, "his standing orders — the anti-divert anchor")
    if low in ("docs/sourceborn_core.md", "docs/final_core_plan.md",
               "docs/recommendation.md"):
        return r(METHOD, "the canonical core spec")

    # his raw words
    if low.startswith("seed_corpus/raw_thoughts/"):
        return r(SOURCE, "his raw thoughts — captured verbatim, never flattened")

    # examples: what seats on the bank and raises the count
    if low.startswith("seed_corpus/examples/"):
        return r(EXAMPLE, "an example — seats on existing parameters and IDs")
    if low.startswith("seed_corpus/cores/"):
        return r(EXAMPLE, "a core he fed in as material; read as an example, "
                          "because it is not one of his rulings")
    if low.startswith("docs/method/holy_books/"):
        return r(EXAMPLE, "eternal-example material — seats, never rules")

    # subjects the system was pointed at, and its outputs
    if low.startswith("docs/riemann/"):
        return r(ARTIFACT, "the RH walk — a subject the engine was run on, not "
                           "the project")
    if low.startswith("docs/mainwork/"):
        return r(ARTIFACT, "a run, report or working record produced by the work")
    if low.startswith("docs/") and "audit" in low:
        return r(ARTIFACT, "an audit output — a run, not an input")
    if low.startswith("docs/"):
        return r(ARTIFACT, "a produced document")

    # the code
    if low.startswith("src/") and ext == ".py":
        return r(SYSTEM, "the engine — finds events, opens intent, seats them")
    if low.startswith("engine/") or low.startswith("core/") or base == "app.py":
        return r(SYSTEM, "entrypoint / engine surface")
    if low.startswith("tools/"):
        return r(SYSTEM, "tooling around the engine")
    if low.startswith("tests/"):
        return r(OPERATIONS, "tests — they pin the system, they do not grow it")

    if base in ("render.yaml", "requirements.txt", "pyproject.toml", ".gitignore",
                "LICENSE", "README.md") or low.startswith(".github/"):
        return r(OPERATIONS, "hosting, packaging, licence or repo furniture")

    return r(UNPLACED, "no rule placed it — surfaced for him, not guessed")


def divide(root: str = ".") -> dict:
    """Every file in the repo, divided. Counts first, then the rows."""
    rows = [classify(p) for p in _tree(root)]
    by = {}
    for row in rows:
        by.setdefault(row["class"], []).append(row)
    counts = {c: len(by.get(c, ())) for c in CLASSES}
    grows = counts[SOURCE] + counts[EXAMPLE]
    return {
        "phase": PHASE,
        "motto": MOTTO,
        "total_files": len(rows),
        "counts": counts,
        "classes": {c: {"job": JOB[c], "count": counts[c],
                        "files": [x["path"] for x in by.get(c, ())]}
                    for c in CLASSES},
        "rows": rows,
        "what_grows_the_count": {
            "files": grows,
            "which": [SOURCE, EXAMPLE],
            "why": "an example seats on existing parameters and IDs; that is what "
                   "strengthens the base and raises the count.",
        },
        "what_it_grows_against": {
            "files": counts[METHOD] + counts[BANK],
            "which": [METHOD, BANK],
            "why": "his rulings define the system and the bank holds the IDs. "
                   "Neither is run as an example.",
        },
        "unplaced": [x["path"] for x in by.get(UNPLACED, ())],
        "law": "a file is divided by what it does to the base, not by its topic.",
    }


def readable(root: str = ".") -> list:
    """The SOURCE + EXAMPLE files, in the order the growing phase should eat
    them: his own words first, then the examples."""
    d = divide(root)
    return ([x["path"] for x in d["rows"] if x["class"] == SOURCE] +
            [x["path"] for x in d["rows"] if x["class"] == EXAMPLE])


def stats(root: str = ".") -> dict:
    d = divide(root)
    return {"phase": d["phase"], "motto": d["motto"],
            "total_files": d["total_files"], "counts": d["counts"],
            "readable_for_growth": len(readable(root)),
            "unplaced": len(d["unplaced"]),
            "source": "docs/method/canon/THE_GROWING_PHASE.md"}


def annotations() -> list:
    return [
        ("everything happening is a event, and all events have intent",
         "filemap.MOTTO"),
        ("current phase is growing phase", "filemap.PHASE"),
        ("divide all files by what they do to the base", "filemap.divide"),
        ("his raw words are SOURCE, never flattened", "filemap.classify"),
        ("a file with no job is reported, never dropped", "filemap.UNPLACED"),
    ]
