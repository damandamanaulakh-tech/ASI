"""THE ALGORITHM THAT MAKES ITSELF.

His order:

    keep doing
    u got some intent from files
    now make algorithm which can make itself

and, earlier, the shape of what that means:

    as long i keep adding the example, once the basic will over it will start
    making new combinations on new thoughts

WHAT "MAKES ITSELF" MEANS HERE, PRECISELY

Every pipeline in this repo before this one had a **fixed** list of steps written
by me. This one does not. `steps()` returns

    THE SPINE  +  every step the algorithm has written for itself so far

loaded from the growth ledger at call time. So the algorithm's own body is data,
it grows, and after `extend()` runs the NEXT run of the same function has more
steps in it than the last one did. That is the whole claim, and it is checkable in
one number: `generation()`.

WHERE ITS OWN STEPS COME FROM — his material, never my typing

    1. HARVEST      every event in his files, each with its role and the container
                    it seats on. 13,848 events across his 217 files.
    2. ARRANGEMENT  the (role -> container) pairings that RECUR. 96 distinct,
                    computed, none typed.
    3. STEP         an arrangement at or over the support bar that is not already
                    a step becomes one, with its support as its evidence.
    4. COMBINATION  two arrangements that co-occur inside the same example open a
                    composite step **that no single example produced**. This is
                    the part that makes new material out of old — his "new
                    combinations on new thoughts".
    5. EXTEND       the new steps are appended. Nothing is removed. The generation
                    number rises.

WHY IT DOES NOT RUN AWAY

A second run over the same files adds **nothing** — the arrangements are the same,
so no step is new. It grows when new material arrives, or when a combination that
was not yet open becomes reachable. And the combination space is pairs of a finite
arrangement set, so it terminates rather than inflating forever. A test pins both:
it grows once, and running again is a no-op.

WHAT IT REFUSES

Every self-written step arrives with a **falsifier** — his own column from the
LIVE_INTENT_ENGINE sheet — so a step the material stops supporting can be killed
on evidence instead of living forever. None is canonical, none creates a
parameter, and none is applied to an answer without his word.

Canon: docs/method/canon/THE_GROWING_PHASE.md
"""

from __future__ import annotations

import os
from functools import lru_cache

from . import growing as W

# ---------------------------------------------------------------------------
# THE SPINE — the steps that were always here. Everything after these is written
# by the algorithm itself.
# ---------------------------------------------------------------------------

SPINE = (
    {"id": "SPINE-1", "step": "find every happening — everything happening is a "
                              "event", "does": "growing.events_in"},
    {"id": "SPINE-2", "step": "open an intent on every event — all events have "
                              "intent", "does": "growing.intent_seat"},
    {"id": "SPINE-3", "step": "read the role of the happening",
     "does": "growing.role_of"},
    {"id": "SPINE-4", "step": "seat it on existing parameters and IDs",
     "does": "growing.seat"},
    {"id": "SPINE-5", "step": "raise the count; remove nothing",
     "does": "growing.grow"},
)

# An arrangement needs this much support before it earns a step. His own number
# from the pattern work: a PATTERN-CANDIDATE opens at 5 repeats.
SUPPORT_BAR = 5
# A combination needs both halves supported and this much shared support.
COMBINE_BAR = 3
# ...and it must CROSS ROLE. Two happenings of the same kind in two containers
# is co-occurrence inside one mode, not a new thought. A combination earns a step
# when DIFFERENT KINDS of happening meet — an ACTION together with an INFERENCE,
# an OBSERVATION together with a SPEECH.
#
# This is his own rain example's shape: the father PUTS water in the air (ACTION)
# and the kids CONCLUDE it is raining (INFERENCE). The insight is the two modes
# meeting, not either one alone.
#
# Measured: without any cross test, 80 arrangements gave 2,627 combinations out of
# a possible 3,160 — a step for nearly every pair, which is not a finding.
# Cross-segment only removed 238, because ACTION spans SEG-03 and SEG-06 both.
# Cross-role is the test that bites.
CROSS_ROLE_REQUIRED = True


# ---------------------------------------------------------------------------
# 1-2. HARVEST and ARRANGEMENT — from his files, computed.
# ---------------------------------------------------------------------------

@lru_cache(maxsize=8)
def _harvest(paths_key: tuple, root: str = ".", max_chars: int = 60000) -> dict:
    """Every event in these files, reduced to its arrangement.

    Returns the arrangement counts, and which example each came from, so a step
    can always name the material that produced it."""
    arr, cooc, per_file = {}, {}, {}
    events = 0
    unreadable = []
    for rel in paths_key:
        try:
            with open(os.path.join(root, rel), "r", encoding="utf-8",
                      errors="replace") as f:
                txt = f.read(max_chars)
        except Exception as e:
            # REPORTED. A silent skip here once made the whole harvest return
            # zero files while claiming success.
            unreadable.append({"path": rel, "error": str(e)})
            continue
        seen_here = set()
        for e in W.events_in(txt):
            events += 1
            role = W.role_of(e["happening"], e["raw"])["role"]
            s = W.seat(e["raw"], limit=3, role=role)
            for st in s["seats"]:
                key = (role, st["container"])
                a = arr.setdefault(key, {"role": role,
                                         "container": st["container"],
                                         "container_name": st["container_name"],
                                         "segment": st["segment"],
                                         "support": 0, "examples": set()})
                a["support"] += 1
                a["examples"].add(rel)
                seen_here.add(key)
        per_file[rel] = sorted(seen_here)
        ordered = sorted(seen_here)
        for i, x in enumerate(ordered):
            for y in ordered[i + 1:]:
                cooc[(x, y)] = cooc.get((x, y), 0) + 1
    for a in arr.values():
        a["examples"] = sorted(a["examples"])[:6]
    return {"arrangements": arr, "cooccurrence": cooc, "events": events,
            "files": len(per_file), "per_file": per_file,
            "unreadable": unreadable}


def arrangements(paths=None, repo: str = ".") -> list:
    """The (role -> container) pairings that recur in his material."""
    paths = tuple(paths if paths is not None else W_readable(repo))
    h = _harvest(paths, repo)
    return sorted(h["arrangements"].values(), key=lambda a: -a["support"])


def W_readable(root: str = ".") -> list:
    from . import filemap
    return filemap.readable(root)


def _arr_id(role: str, container: str) -> str:
    return "ARR-%s-%s" % (role[:3], container.replace("CON-", ""))


def _step_name(role: str, container: str, cname: str) -> str:
    return "%s event seats on %s %s" % (role, container, cname)


def _falsifier(role: str, container: str) -> str:
    """What would flip this step — his own column, on a generated rule."""
    return ("a %s event that seats outside %s while the same material is present, "
            "or %s turning out to be reached only by a word coincidence rather "
            "than by the role" % (role, container, container))


# ---------------------------------------------------------------------------
# 3-4. THE STEPS THE ALGORITHM WRITES FOR ITSELF
# ---------------------------------------------------------------------------

def written_steps(root: str) -> list:
    """Every step the algorithm has already written, from the ledger."""
    from . import growth as G
    return [r for r in G.load(root) if r.get("kind") == G.STEP]


def steps(root: str) -> dict:
    """THE ALGORITHM'S OWN BODY — spine plus everything it has written.

    This is not a constant. After extend() it is longer than it was before."""
    mine = written_steps(root)
    return {
        "spine": list(SPINE),
        "written": [{"id": r["id"], "step": r["name"], "detail": r.get("detail"),
                     "from": r.get("surfaced_by"),
                     "support": r.get("support"),
                     "falsifier": r.get("falsifier"),
                     "kind_of_step": r.get("step_kind"),
                     "canonical": False}
                    for r in mine],
        "counts": {"spine": len(SPINE), "written": len(mine),
                   "total": len(SPINE) + len(mine)},
        "generation": len(mine),
        "law": "the step list is data, not a constant. It grows.",
    }


def generation(root: str) -> int:
    """How far the algorithm has extended itself. 0 = only the spine."""
    return len(written_steps(root))


def propose(root: str, paths=None, bar: int = SUPPORT_BAR,
            repo: str = ".") -> dict:
    """What new steps this material opens — computed, not written yet.

    Two kinds:
      ARRANGEMENT  an arrangement at or over the bar that is not yet a step
      COMBINATION  two arrangements that co-occur in the same example, whose
                   composite no single example produced
    """
    paths = tuple(paths if paths is not None else W_readable(repo))
    h = _harvest(paths, repo)
    arr = h["arrangements"]
    have = {r["name"] for r in written_steps(root)}
    new = []
    for key, a in sorted(arr.items(), key=lambda kv: -kv[1]["support"]):
        if a["support"] < bar:
            continue
        name = _step_name(a["role"], a["container"], a["container_name"])
        if name in have:
            continue
        new.append({
            "step_kind": "ARRANGEMENT",
            "name": name,
            "arrangement": _arr_id(a["role"], a["container"]),
            "role": a["role"], "container": a["container"],
            "container_name": a["container_name"], "segment": a["segment"],
            "support": a["support"],
            "from_examples": a["examples"],
            "falsifier": _falsifier(a["role"], a["container"]),
            "canonical": False,
        })
    combos = []
    same_shape = 0
    strong = {k for k, a in arr.items() if a["support"] >= bar}
    for (x, y), n in sorted(h["cooccurrence"].items(), key=lambda kv: -kv[1]):
        if n < COMBINE_BAR or x not in strong or y not in strong:
            continue
        if x[0] == y[0] and x[1] == y[1]:
            continue
        if CROSS_ROLE_REQUIRED and x[0] == y[0]:
            same_shape += 1
            continue
        name = ("COMBINATION: %s on %s together with %s on %s"
                % (x[0], x[1], y[0], y[1]))
        if name in have:
            continue
        combos.append({
            "step_kind": "COMBINATION",
            "name": name,
            "pair": [_arr_id(*x), _arr_id(*y)],
            "shared_support": n,
            "left": {"role": x[0], "container": x[1]},
            "right": {"role": y[0], "container": y[1]},
            "falsifier": "the two never co-occur again once more material "
                         "arrives, or their co-occurrence is explained by one "
                         "shared word rather than two arrangements",
            "crosses_role": x[0] != y[0],
            "crosses_segment": arr[x]["segment"] != arr[y]["segment"],
            "produced_by_any_single_example": False,
            "canonical": False,
        })
    return {
        "material": {"files": h["files"], "events": h["events"],
                     "arrangements": len(arr),
                     "arrangements_over_bar": len(strong),
                     "unreadable": len(h["unreadable"]),
                     "unreadable_paths": [u["path"] for u in h["unreadable"][:6]]},
        "support_bar": bar,
        "combine_bar": COMBINE_BAR,
        "new_arrangement_steps": new,
        "new_combination_steps": combos,
        "counts": {"arrangement": len(new), "combination": len(combos),
                   "total_new": len(new) + len(combos),
                   "combinations_rejected_same_role": same_shape},
        "cross_role_required": CROSS_ROLE_REQUIRED,
        "already_written": len(have),
        "law": "a step is earned by recurrence in his material, never typed by me.",
    }


def extend(root: str, paths=None, bar: int = SUPPORT_BAR,
           limit: int = 0, repo: str = ".") -> dict:
    """WRITE the new steps. The algorithm is longer afterwards than before.

    Append-only: an existing step is left exactly as it is, and nothing is ever
    removed. `limit` caps how many are written in one pass and the number left
    over is REPORTED, never silently dropped."""
    from . import growth as G
    before = generation(root)
    p = propose(root, paths, bar, repo=repo)
    queue = p["new_arrangement_steps"] + p["new_combination_steps"]
    held = 0
    if limit and len(queue) > limit:
        held = len(queue) - limit
        queue = queue[:limit]
    written = []
    for s in queue:
        extra = {k: v for k, v in s.items() if k not in ("name",)}
        written.append(G.add(root, G.STEP, s["name"],
                             surfaced_by="his files, %d events"
                                         % p["material"]["events"],
                             module="selfmake",
                             detail=s.get("falsifier", ""),
                             extra=extra))
    after = generation(root)
    return {
        "generation_before": before,
        "generation_after": after,
        "wrote": len(written),
        "held_by_limit": held,
        "held_note": ("%d proposed steps were not written in this pass — "
                      "reported, not dropped" % held) if held else None,
        "steps": [{"id": r["id"], "name": r["name"],
                   "kind_of_step": r.get("step_kind"),
                   "support": r.get("support") or r.get("shared_support"),
                   "falsifier": r.get("falsifier")} for r in written],
        "algorithm_now": steps(root)["counts"],
        "removed": 0,
        "parameters_created": 0,
        "law": "the algorithm wrote its own steps from his material and is longer "
               "than it was.",
        "refuses": "no step is canonical, none creates a parameter, and none is "
                   "applied to an answer without his word.",
    }


# ---------------------------------------------------------------------------
# 5. RUN — the algorithm executing its own current body on one input.
# ---------------------------------------------------------------------------

def run(root: str, text: str, name: str = "") -> dict:
    """Run the algorithm as it currently stands.

    The steps applied are read from the ledger, so a run after extend() applies
    more steps than a run before it. Each written step that MATCHES this input is
    reported as fired, with the support it was earned on."""
    body = steps(root)
    place = W.place(text, name)
    fired, quiet = [], 0
    seated = {(e.get("role"), st["container"])
              for x in place["per_event"]
              for e in [x["event"]]
              for st in x["seating"]["seats"]}
    for s in body["written"]:
        kind = s.get("kind_of_step")
        hit = False
        if kind == "ARRANGEMENT":
            hit = any(role and con and s["step"].startswith(
                "%s event seats on %s" % (role, con)) for role, con in seated)
        elif kind == "COMBINATION":
            # both halves must be present in THIS input for the step to fire
            hit = sum(1 for role, con in seated
                      if ("%s on %s" % (role, con)) in s["step"]) >= 2
        if hit:
            fired.append({"id": s["id"], "step": s["step"],
                          "support": s.get("support"),
                          "falsifier": s.get("falsifier"),
                          "kind_of_step": kind})
        else:
            quiet += 1
    return {
        "name": name or "(unnamed)",
        "generation": body["generation"],
        "steps_applied": body["counts"],
        "placement": place,
        "self_written_steps_fired": fired,
        "self_written_steps_quiet": quiet,
        "counts": {
            "events": place["counts"]["events"],
            "ids_seated": place["counts"]["distinct_ids_seated"],
            "count_added": place["counts"]["count_added"],
            "fired": len(fired),
            "parameters_created": 0,
        },
        "chosen": None,
        "law": "the body of the algorithm is whatever it has written for itself "
               "up to now.",
    }


def bias_report(paths=None, repo: str = ".") -> dict:
    """The honest weakness in the material this is built on.

    The role classifier defaults to ACTION when it finds no perception,
    inference, speech or feeling marker. On his corpus that default carries most
    of the events, so the arrangements are ACTION-heavy for a reason that is
    partly mechanical, not only real. Reported here rather than buried, because
    every step written above inherits it."""
    paths = tuple(paths if paths is not None else W_readable(repo))
    h = _harvest(paths, repo)
    by_role = {}
    for (role, _con), a in h["arrangements"].items():
        by_role[role] = by_role.get(role, 0) + a["support"]
    tot = sum(by_role.values()) or 1
    return {
        "seats_by_role": by_role,
        "action_share": round(100.0 * by_role.get("ACTION", 0) / tot, 1),
        "why": "role_of() returns ACTION when no OBSERVATION/INFERENCE/SPEECH/"
               "FEELING marker is present. That is a fallback, not a finding.",
        "consequence": "arrangements and therefore self-written steps are "
                       "ACTION-weighted. A better role reader would redistribute "
                       "them, and the steps already written would need revisiting "
                       "— by superseding, never by deletion.",
        "his_call": "whether ACTION-as-default is acceptable for the growing "
                    "phase, or whether the role reader is the next thing to fix.",
    }


def stats(root: str = None) -> dict:
    base = {
        "spine": len(SPINE),
        "support_bar": SUPPORT_BAR,
        "combine_bar": COMBINE_BAR,
        "steps_are_a_constant": False,
        "source": "docs/method/canon/THE_GROWING_PHASE.md",
    }
    if root:
        b = steps(root)
        base.update({"generation": b["generation"],
                     "written": b["counts"]["written"],
                     "total_steps": b["counts"]["total"]})
    return base


def annotations() -> list:
    return [
        ("now make algorithm which can make itself", "selfmake.extend"),
        ("the step list is data, not a constant", "selfmake.steps"),
        ("a step is earned by recurrence in his material", "selfmake.propose"),
        ("new combinations on new thoughts", "selfmake.propose"),
        ("every self-written step carries a falsifier", "selfmake._falsifier"),
        ("the honest bias in what it learnt from", "selfmake.bias_report"),
    ]
