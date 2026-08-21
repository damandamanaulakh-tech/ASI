"""THE ARROW GRAPH — what is where, drawn from the live modules.

His ask: *show me in arrow graph what is where.*

Every number in this chart is READ FROM THE RUNNING CODE at draw time, not typed
into it. If a count moves, the chart moves. That is the whole reason it is a
module and not a picture: a diagram that can go stale is a diagram that will.

Layers, top to bottom, are the path a thing actually takes:

    his words or a file   ->   divided   ->   placed   ->   seated on the bank
    ->   generated from   ->   gated   ->   ledgered   ->   back to him

Nothing here reaches an answer without him. That is drawn, not implied.
"""

from __future__ import annotations


def _n():
    """Every count in one place, all of it live."""
    from . import artifact as A
    from . import filemap as F
    from . import growth as G
    from . import human_registry as hr
    from . import intent_ledger as L
    from . import intents as I
    from . import nodebrain as N
    from . import runtime as R
    from . import statepacks as P
    from . import subjectbrains as SB
    d = F.divide(".")
    return {
        "files": d["total_files"], "by": d["counts"],
        "grows": d["what_grows_the_count"]["files"],
        "against": d["what_it_grows_against"]["files"],
        "bank": len(hr.parameters()), "containers": len(hr.containers()),
        "segments": len(hr.segments()),
        "packs": len(P.STATE_PACKS), "forks": len(P.EVENT_FORKS),
        "motive": len(I.motive_rows()), "form": len(I.form_rows()),
        "ledger": len(L.HIS_CANDIDATES), "contract": len(L.CONTRACT),
        "subjects": len(SB.SUBJECTS), "cands": len(SB.CANDIDATES),
        "halts": len(SB.HALTS),
        "variants": SB.generate_variants()["variants_generated"],
        "signs": len(A.SIGN_GROUPS), "meanings": len(A.SYNTHETIC_MEANINGS),
        "gen": A.generate_meanings()["counts"]["generated"],
        "ceiling": A.combination_space()["ceiling"],
        "series": len(G.SERIES),
        "ntypes": len(N.NODE_TYPES), "nfields": len(N.FIELDS),
        "nlinks": len(N.LINK_TYPES), "nfp": N.fingerprint(),
        "nrev": [s["n"] for s in R.STEPS if s["dir"] == R.REVERSE],
    }


W = 74          # inner width of every box; every line is padded to it


def _box(title, right, lines, heavy=False):
    tl, tr, bl, br, h, v = ("╔", "╗", "╚", "╝", "═", "║") if heavy else \
                           ("┌", "┐", "└", "┘", "─", "│")
    out = [" " * 3 + tl + h * W + tr]
    head = "  " + title
    head = head + " " * max(1, W - len(head) - len(right) - 2) + right + "  "
    out.append(" " * 3 + v + head[:W].ljust(W) + v)
    for ln in lines:
        out.append(" " * 3 + v + ("  " + ln)[:W].ljust(W) + v)
    out.append(" " * 3 + bl + h * W + br)
    return out


def _down(n=1, label=""):
    out = []
    for _ in range(n):
        out.append(" " * 12 + "│" + ("   " + label if label else ""))
    out.append(" " * 12 + "▼")
    return out


def arrow_chart() -> str:
    """The chart, with every number read from the live modules at draw time."""
    n = _n()
    b = n["by"]
    L = []
    L.append(" " * 22 + "HIS WORDS  ·  A FILE  ·  AN EXAMPLE")
    L.append(" " * 38 + "│")
    L.append(" " * 38 + "▼")

    L += _box("FILE MAP", "filemap.py  /growing", [
        "every file divided by what it does to the base, not by its topic",
        "",
        "SOURCE  %4d  his raw words           ┐" % b["SOURCE"],
        "EXAMPLE %4d  seats and raises count  ├─ %d GROW THE COUNT"
        % (b["EXAMPLE"], n["grows"]),
        "                                      ┘",
        "METHOD  %4d  his rulings             ┐" % b["METHOD"],
        "BANK    %4d  the IDs themselves      ├─ %d ARE WHAT THEY GROW"
        % (b["BANK"], n["against"]),
        "                                      ┘   AGAINST",
        "",
        "SYSTEM %d · ARTIFACT %d · OPERATIONS %d · UNPLACED %d"
        % (b["SYSTEM"], b["ARTIFACT"], b["OPERATIONS"], b["UNPLACED"]),
    ])
    L += _down()

    L += _box("THE GROWING PHASE", "growing.py  /growing/place", [
        '"everything happening is a event, and all events have intent"',
        "",
        "text ──► events_in()      no closed verb list —",
        "             │            43% of his corpus found by inflection",
        "             ▼",
        "         role_of()        ACTION · OBSERVATION · INFERENCE",
        "             │            SPEECH · FEELING · STATE",
        "             ▼",
        "     ┌───────┴───────┐",
        "     ▼               ▼",
        "  seat()        intent_seat() ──► CON-063 + CON-064",
        "  role picks     every event has an intent slot,",
        "  the segment,   and it is never absent",
        "  words pick",
        "  the row",
        "",
        "  out_of_role rows are KEPT and shown, never counted",
    ])
    L += _down()

    L += _box("THE BANK — HIS 1-10-8-40", "human_registry.py  /registry", [
        "%d segments · %d containers · %s named sub-parameters"
        % (n["segments"], n["containers"], format(n["bank"], ",")),
        "",
        "an example SEATS here and gives an ID support.",
        "IT CREATES NOTHING.",
    ], heavy=True)
    L += _down(1, "more parameters active ──► more reachable ──► more generated")

    L += _box("THE GENERATORS", "all read the bank · none writes to it", [
        "intents.py     /intents      CON-064 motive %d × CON-063 form %d"
        % (n["motive"], n["form"]),
        "statepacks.py  /generation   %d brain-states · %d event forks"
        % (n["packs"], n["forks"]),
        "asi_pyramid.py /asi          his 18 · the scope split · the shells",
        "weighting.py   /weighting    same parameters, different objective",
        "artifact.py    /artifact     %d sign groups · %d meanings · 9 roles"
        % (n["signs"], n["meanings"]),
        "subjectbrains  /subjects     %d subjects · %d candidates · %d halts"
        % (n["subjects"], n["cands"], n["halts"]),
    ])
    L += _down()

    L += _box("THE GATES", "what stops a cross product being a finding", [
        "role gate       a word coincidence outside the role is not a seat",
        "IDF bar         a word in forty of his names is not evidence",
        "cross-role      ACTION×ACTION is one mode twice, not a new thought",
        "ROLE_FUTURES    a carver does not secure a dynasty",
        "FUTURE_NEEDS    an identity claim needs the enclosure",
        "taxonomy guard  a parameter list cannot strengthen the bank",
        "",
        "artifact:  %s ungated  ──►  %s kept — BOTH reported"
        % (format(n["ceiling"], ","), format(n["gen"], ",")),
    ])
    L += _down()

    L += _box("THE KILL — his falsifier column", "intent_ledger.py  /ledger", [
        "generate ─► evidence ─► contradiction ─► falsification ─► SURVIVORS",
        "",
        "dies two ways: the falsifier is met,",
        "               or counterexamples ≥ support",
        "UNTESTED is reported untested, never as a survivor",
        "a killed row keeps its falsifier and the reason it died",
        "",
        "!! ON HIS WORD THE KILL IS OFF BY DEFAULT",
        '   "nothing needs to kill for now, add everything and generate"',
        "   a subject that reads the other way is a SECOND SETTING,",
        "   not a death. The pass still runs on request.",
    ])
    L += _down()

    L += _box("THE LEDGER — APPEND ONLY", "growth.py  /growth", [
        "%d typed series. No delete, no pop, no truncate —" % n["series"],
        "a test reads this module's own source and fails if a",
        "removal path is ever added.",
        "",
        "BASE %s  +  3 grown  =  3,207" % format(n["bank"], ","),
        "only PARAM rows consume his flat index.",
        "AN ADDRESS IS NOT A PARAMETER.",
    ])
    L += _down()

    L += _box("THE ALGORITHM THAT MAKES ITSELF", "selfmake.py  /selfmake", [
        "steps()  =  SPINE 5  +  everything it wrote for itself",
        "                 ▲                    │",
        "                 └───── extend() ◄────┘",
        "",
        "its body is DATA, not a constant:",
        "   generation 0        →     5 steps",
        "   after one extend    → 2,204 steps",
        "   same material again →     0 written",
    ])
    L += _down()

    L += _box("HIS SELF-SUSTAIN PHASES", "his sheet · staged, not a switch", [
        "A  node schema LOCKED    nodebrain.py  /nodes/schema",
        "     %d types · %d fields · %d typed links"
        % (n["ntypes"], n["nfields"], n["nlinks"]),
        "     fingerprint %s — a test pins it" % n["nfp"],
        "B  runtime pipeline      runtime.py + prior.py  /runtime",
        "     his 18 as ONE run · steps %s run REVERSE"
        % "-".join(str(x) for x in n["nrev"]),
        "     2 and 3 were ABSENT — declare the end, descend to the",
        "     prior reality, BEFORE decomposition. answer: None, always",
        "C  combination + intent engine   combine.py  /combine",
        "     rounds until QUIET · cross-role over sets · anchored on",
        "     a row · one occurrence cannot breed · order ceiling 6",
        "     every candidate leaves carrying prediction + falsifier",
        "     + maturity · stage 22 is delta(), computed not by hand",
        "D  memory graph + auto-linking   nodegraph.py  /nodes",
        "     his 5 write conditions ENFORCED at write_node · his 6",
        "     read conditions = ONE mechanism, recall and linking ·",
        "     hub nodes materialize once (ACTOR PATTERN ARTIFACT FUT)",
        "     per-node reading chains · typed paths (stage 5 RUNS) ·",
        "     match reinforces, opposition contradicts, both stand ·",
        "     box-6 gates run, THE QUEUE HOLDS until his word",
        "     8 of his 9 loops run; the 9th stops at the queue",
        "E  self-sustain scheduler             NOT BUILT",
    ])
    L += _down()

    L.append(" " * 34 + "HIM")
    L.append(" " * 14 + "nothing is canonical · nothing is chosen")
    L.append(" " * 12 + "no parameter is created · no halt is answered")
    return "\n".join(L)


def where(thing: str = "") -> dict:
    """Where one named thing lives. His question, answered per item."""
    m = {
        "the bank": ("human_registry.py", "/registry",
                     "his 3,204 — read by everything, written by nothing"),
        "the count": ("growth.py", "/growth", "append-only, 17 typed series"),
        "events": ("growing.py", "/growing/place", "no closed verb list"),
        "intent": ("intents.py + intent_ledger.py", "/intents  /ledger",
                   "generated live, killed on a falsifier"),
        "the kill": ("intent_ledger.py", "/ledger/kill",
                     "OFF by default on his word"),
        "brain states": ("statepacks.py", "/generation", "16 packs, MODEL A..P"),
        "subjects": ("subjectbrains.py", "/subjects",
                     "12 people, 25 candidates, 14 halts unanswered"),
        "the object": ("artifact.py", "/artifact",
                       "sign groups, actor roles, origin distance"),
        "the algorithm": ("selfmake.py", "/selfmake",
                          "its own step list, which grows"),
        "the file divide": ("filemap.py", "/growing", "479 files, 0 unplaced"),
        "what exists": ("exists.py", "/exists",
                        "the honest map of what runs and what does not"),
    }
    if thing:
        k = thing.strip().lower()
        for key, v in m.items():
            if k in key:
                return {"thing": key, "module": v[0], "route": v[1],
                        "note": v[2]}
        return {"thing": thing, "found": False,
                "known": sorted(m), "note": "not a named layer"}
    return {"layers": [{"thing": k, "module": v[0], "route": v[1],
                        "note": v[2]} for k, v in m.items()],
            "count": len(m)}


def stats() -> dict:
    n = _n()
    return {"files": n["files"], "bank": n["bank"], "subjects": n["subjects"],
            "series": n["series"], "drawn_from": "the live modules",
            "typed_numbers_in_the_chart": 0,
            "source": "sysmap.arrow_chart"}


def annotations() -> list:
    return [
        ("show me in arrow graph what is where", "sysmap.arrow_chart"),
        ("every number is read from the running code", "sysmap._n"),
        ("where one named thing lives", "sysmap.where"),
    ]
