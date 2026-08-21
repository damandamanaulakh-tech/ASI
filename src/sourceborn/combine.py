"""PHASE C — THE COMBINATION + INTENT ENGINE.

From his SELF-SUSTAINING EXECUTION FLOW sheet: after A (registries + IDs,
locked) and B (the runtime pipeline), C is the engine that makes combinations
and intents A LOOP rather than a step — his own concept, in his words:

    "concept is simple as much parameters we plug, we will generate more
     pattern and intent"
    "as long i keep adding the example, once the basic will over it will
     start making new combinations on new thoughts"

WHAT EXISTED, AND WHAT WAS MISSING

Combination generation existed twice (selfmake over the repo, runtime step 9
over one ask) and intent generation existed once (intents.generate, gated by
active containers). What did NOT exist:

  * ROUNDS. A combination could never combine again — "new combinations on
    new thoughts" had no mechanism, because nothing fed a round's output back
    in as the next round's input.
  * A STOP. Nothing said when generating was finished. The loop-until-quiet
    discipline existed as evidence (extend() writes 0 on the same material)
    but not as a loop.
  * THE CHAIN ON EVERY CANDIDATE. A combination arrived bare. Now every
    candidate leaves the engine carrying its prediction (stage 12), its
    falsifier (stage 17's food), and its maturity (stage 18) — generate ->
    evidence -> falsification -> maturity as ONE object, so a candidate is
    testable the moment it exists.
  * STAGE 22 AS A FUNCTION. "New combination availability" was a by-hand
    diff of generations. `delta()` computes it.

THE GATES — WHY THE ROUNDS DO NOT EXPLODE

Every ungated cross product here has been the wrong answer (6,480 of 6,480
meanings; 2,627 of 3,160 pairs). The engine's gates, in order:

  1. CROSS-ROLE, EXTENDED TO SETS. A combination's roles are a SET, and a new
     part must bring a role the set does not hold. ACTION x ACTION is one mode
     twice; ACTION+INFERENCE+INFERENCE is the same failure at order 3. Six
     roles exist, so order six is the structural ceiling.
  2. CO-OCCURRENCE. All parts must appear together in at least one example.
     A combination nothing exhibited is not available — it is imaginable, and
     the engine does not deal in imaginable.
  3. THE ANCHOR. Seating on a short ask mostly lands at CONTAINER granularity
     — the role's own containers, which are STRUCTURE: any two-role text
     exhibits them, whatever it says. A coarse x coarse pair is therefore the
     cross-product failure wearing a role mask, and it is refused: every
     combination must hold at least one ROW-granularity part — a row an
     actual word reached. Nothing floats on structure alone. (The same
     principle as the taxonomy guard: a parameter list cannot strengthen the
     bank, and a role's own scaffolding cannot combine with itself.)
  4. RECURRENCE TO BREED. An order-2 combination may enter a deeper round
     ONLY at support >= 2 — the same RECURRENCE_MIN maturity uses, his rule 6:
     one interesting event is not a pattern. One example can therefore never
     produce order 3, and a test pins that. This is what makes "once the basic
     will over" mechanical: depth unlocks exactly where material recurred.

AND WHAT IS GENUINELY NEW AGAINST SELFMAKE: selfmake's COMBINATION steps stop
at PAIRS. The engine breeds order 3 and beyond — but only where support
earned it, which is his "new combinations on new thoughts" with the brake
built in.

WHAT THE ENGINE REFUSES

  * it never writes. No ledger row, no file, no parameter — a run is a report.
    (A test reads this module's own source, the Phase A technique.)
  * it never chooses. `chosen` is None; intents stay candidates.
  * it never kills on its own. His word — "nothing needs to kill for now" —
    so `check()` accepts verdicts handed in and `kill=False` is the default.
  * it never caps silently. A cap that bites reports what it dropped.
  * maturity is fed honestly: co-occurrence is SUPPORT, an input — not a
    confirmation. An unchecked candidate reads UNTESTED whatever its support,
    because "nobody checked" is not "it held".
"""

from __future__ import annotations

MAX_ROUNDS_DEFAULT = 4
ROUND_CAP_DEFAULT = 400
RECURRENCE_TO_BREED = 2      # = maturity.RECURRENCE_MIN — one occurrence
                             # cannot breed. His rule 6.
INTENT_SHOW = 4              # candidates shown per combination; the count is
                             # always the full count.


# ---------------------------------------------------------------------------
# MATERIAL — texts (or pre-seated arrangement sets) become per-example
# arrangement maps. The example is the unit of co-occurrence, exactly as the
# file is in selfmake's harvest.
# ---------------------------------------------------------------------------

ROW = "ROW"                  # a word reached an actual row in the 3,204
CONTAINER = "CONTAINER"      # the role was present, no row was reached
UNANCHORED = "*"             # the container slot of such a part: the role
                             # happened, and that is ALL the part claims


def _prepare(texts=None, prepared=None, paths=None, repo: str = ".",
             seat_limit: int = 3) -> tuple:
    """Material -> (examples, granularity map).

    Each example is {name, arrangements: {(role, container): count}, events};
    the granularity map says, per (role, container), whether ANY word ever
    reached a row there (ROW) or it only ever appeared as the role's own
    scaffolding (CONTAINER). The example is the unit of co-occurrence, exactly
    as the file is in selfmake's harvest.

    `paths` runs on his corpus through selfmake's own harvest, so a corpus run
    and a selfmake run can never disagree about what a file exhibits.
    `prepared` lets a caller that already seated hand the arrangements in."""
    gran = {}
    if prepared is not None:
        ex = []
        for i, p in enumerate(prepared):
            arrs = dict(p["arrangements"])
            for k in arrs:
                gran[k] = ROW if k in set(p.get("row_parts", arrs)) \
                    else gran.get(k, CONTAINER)
            ex.append({"name": p.get("name") or ("example %d" % (i + 1)),
                       "arrangements": arrs, "events": p.get("events", 0)})
        return ex, gran
    if paths is not None:
        from . import selfmake as S
        h = S._harvest(tuple(paths), repo)
        ex = [{"name": rel, "arrangements": {k: 1 for k in keys},
               "events": 0}
              for rel, keys in sorted(h["per_file"].items())]
        for e in ex:
            for k in e["arrangements"]:
                gran[k] = ROW       # harvest seats are matched rows
        if ex:
            ex[0]["events"] = h["events"]
        return ex, gran
    from . import growing as G
    out = []
    for i, t in enumerate(texts or []):
        arrs = {}
        events = 0
        for e in G.events_in(t or ""):
            events += 1
            role = G.role_of(e["happening"], e["raw"])["role"]
            s = G.seat(e["raw"], limit=seat_limit, role=role)
            if s["seats"]:
                for st in s["seats"]:
                    key = (role, st["container"])
                    arrs[key] = arrs.get(key, 0) + 1
                    gran[key] = ROW
            else:
                # An event no word anchored still HAPPENED, and its role is
                # real — but it is ONE fact, not sixteen. Folding the role's
                # whole container scaffold in here once multiplied one
                # two-sentence text into 240 candidates, which is the
                # cross-product failure through a side door. One part: the
                # role was present, no row was reached.
                key = (role, UNANCHORED)
                arrs[key] = arrs.get(key, 0) + 1
                gran.setdefault(key, CONTAINER)
        out.append({"name": "example %d" % (i + 1), "arrangements": arrs,
                    "events": events})
    return out, gran


def _sig(parts) -> str:
    """The identity of a combination is its PARTS, sorted — never its prose.
    His rule 4: new wording is not a new combination."""
    return " + ".join("%s->%s" % (r, c) for r, c in sorted(parts))


def _cooccur(parts, examples) -> list:
    """Indices of the examples where EVERY part appears."""
    ps = set(parts)
    return [i for i, ex in enumerate(examples)
            if ps <= set(ex["arrangements"])]


def _apart(parts, examples) -> dict:
    """Per part: how often it appears WITHOUT the full set. This is what the
    falsifier watches — parts recurring apart while together stays stuck."""
    ps = set(parts)
    out = {}
    for p in sorted(ps):
        alone = sum(1 for ex in examples
                    if p in ex["arrangements"]
                    and not (ps <= set(ex["arrangements"])))
        out["%s->%s" % p] = alone
    return out


# ---------------------------------------------------------------------------
# THE CHAIN EVERY CANDIDATE CARRIES — prediction, falsifier, maturity.
# ---------------------------------------------------------------------------

def _prediction(sig: str) -> list:
    """Stage 12 on a combination: what should exist if it is real.

    The REPETITION row names THIS candidate's parts, so it discriminates by
    construction; the ABSENCE row is owed by every reading and says why it
    does not discriminate."""
    return [
        {"class": "REPETITION",
         "would_confirm": "the parts of %s appear TOGETHER in later material"
                          % sig,
         "would_refute": "the parts recur apart, repeatedly, while together "
                         "never recurs",
         "discriminating": True, "checked": False},
        {"class": "ABSENCE",
         "would_confirm": "nothing found that the combination forbids",
         "would_refute": "something found that it forbids",
         "discriminating": False, "checked": False,
         "why_not": "every reading owes an ABSENCE, so finding one separates "
                    "none of them"},
    ]


def _falsifier(sig: str, support: int) -> dict:
    return {
        "falsifier": "the parts of %s each recur in new material while the "
                     "full set never recurs together — apart evidence reaching "
                     "support (%d) with together stuck" % (sig, support),
        "falsifiable": True,
        "from_prediction": "REPETITION",
        "feeds": "intent_ledger.kill",
    }


def _maturity_of(support: int, seen_in: int):
    from . import maturity as M
    return M.read(confirmed=(), refuted=(), support=support,
                  sequences_seen=seen_in, checks=0)


# ---------------------------------------------------------------------------
# INTENTS — what a combination's container set reaches. The mechanism stays
# intents.py's; the engine only feeds it and reports honestly: the union of
# two containers opens the union of their motives, nothing extra is invented
# for the pairing.
# ---------------------------------------------------------------------------

def _intents_for(containers: tuple, cache: dict) -> dict:
    from . import intents as I
    key = tuple(sorted(c for c in containers if c != UNANCHORED))
    if not key:
        return {"count": 0, "show": [], "pairs": [],
                "why_none": "no real container in this candidate — an "
                            "unanchored role opens nothing"}
    if key not in cache:
        g = I.generate("COMBINATION", list(key))
        cands = g.get("candidates", [])
        cache[key] = {
            "count": len(cands),
            "show": ["%s — %s (%s) shaped as %s (%s)"
                     % (c["id"], c.get("why", ""), c.get("why_p", ""),
                        c.get("shape", ""), c.get("shape_p", ""))
                     for c in cands[:INTENT_SHOW]],
            "pairs": sorted({(c.get("why_p"), c.get("shape_p"))
                             for c in cands}),
        }
    return cache[key]


# ---------------------------------------------------------------------------
# THE ENGINE.
# ---------------------------------------------------------------------------

def run(texts=None, prepared=None, paths=None, repo: str = ".",
        name: str = "", max_rounds: int = MAX_ROUNDS_DEFAULT,
        round_cap: int = ROUND_CAP_DEFAULT) -> dict:
    """Rounds until quiet. Returns a report; writes nothing; answers nothing.

    Round 1: cross-role pairs of arrangements that co-occur in an example,
    anchored by at least one ROW-granularity part.
    Round r: a candidate at support >= RECURRENCE_TO_BREED takes on one more
    part whose ROLE it does not already hold, if the whole set co-occurs.
    The loop stops the round nothing new opens — and says which way it
    stopped."""
    examples, gran = _prepare(texts=texts, prepared=prepared, paths=paths,
                              repo=repo)
    arrs = {}
    for ex in examples:
        for key, cnt in ex["arrangements"].items():
            arrs[key] = arrs.get(key, 0) + cnt
    arr_list = sorted(arrs)              # deterministic order

    def anchored(parts) -> bool:
        return any(gran.get(p) == ROW for p in parts)

    icache = {}
    by_sig = {}
    rounds = []
    frontier = []
    stopped_because = None

    for rnd in range(1, max_rounds + 1):
        opened, rejected_role, rejected_cooc, blocked_breed = [], 0, 0, 0
        rejected_anchor = 0
        if rnd == 1:
            pool = []
            for i in range(len(arr_list)):
                for j in range(i + 1, len(arr_list)):
                    a, b = arr_list[i], arr_list[j]
                    if a[0] == b[0]:
                        rejected_role += 1
                        continue
                    if not anchored((a, b)):
                        rejected_anchor += 1
                        continue
                    seen = _cooccur((a, b), examples)
                    if not seen:
                        rejected_cooc += 1
                        continue
                    pool.append(((a, b), seen))
        else:
            pool = []
            breeders = [c for c in frontier
                        if c["support"] >= RECURRENCE_TO_BREED]
            blocked_breed = len(frontier) - len(breeders)
            in_pool = set()
            for c in breeders:
                held_roles = {r for r, _ in c["parts"]}
                for a in arr_list:
                    if a[0] in held_roles:
                        rejected_role += 1
                        continue
                    parts = tuple(sorted(c["parts"] + (a,)))
                    sig = _sig(parts)
                    # two parents can breed the same set in one round — one
                    # pool entry, or duplicates burn cap slots for nothing
                    if sig in by_sig or sig in in_pool:
                        continue
                    seen = _cooccur(parts, examples)
                    if not seen:
                        rejected_cooc += 1
                        continue
                    in_pool.add(sig)
                    pool.append((parts, seen))

        # deterministic: strongest first, ties on signature
        pool.sort(key=lambda x: (-len(x[1]), _sig(x[0])))
        dropped_by_cap = max(0, len(pool) - round_cap)
        for parts, seen in pool[:round_cap]:
            sig = _sig(parts)
            if sig in by_sig:
                continue
            containers = tuple(sorted({c for _, c in parts
                                       if c != UNANCHORED}))
            support = len(seen)
            mat = _maturity_of(support, support)
            g = sorted({gran.get(p, CONTAINER) for p in parts})
            cand = {
                "id": "CB-%03d" % (len(by_sig) + 1),
                "signature": sig,
                "order": len(parts),
                "parts": tuple(parts),
                "roles": sorted({r for r, _ in parts}),
                "containers": list(containers),
                "granularity": g[0] if len(g) == 1 else "MIXED",
                "round": rnd,
                "support": support,
                "seen_in": [examples[i]["name"] for i in seen],
                "apart": _apart(parts, examples),
                "can_breed": support >= RECURRENCE_TO_BREED,
                "intents": _intents_for(containers, icache),
                "predictions": _prediction(sig),
                **_falsifier(sig, support),
                "maturity": mat["state"],
                "maturity_why": mat["why"],
                "chosen": None,
            }
            by_sig[sig] = cand
            opened.append(cand)

        rounds.append({
            "round": rnd,
            "opened": len(opened),
            "rejected_same_role": rejected_role,
            "rejected_no_anchor": rejected_anchor,
            "rejected_no_cooccurrence": rejected_cooc,
            "blocked_cannot_breed": blocked_breed,
            "dropped_by_round_cap": dropped_by_cap,
            "cap_note": ("the cap BIT — %d candidate(s) at the weak end were "
                         "dropped and are being reported, not hidden"
                         % dropped_by_cap) if dropped_by_cap else None,
        })
        frontier = opened
        if not opened:
            stopped_because = ("QUIET — round %d opened nothing new. The "
                               "material is spent at this depth" % rnd)
            break
    if stopped_because is None:
        stopped_because = ("ROUND CAP — %d round(s) ran and the last still "
                          "opened candidates; deeper rounds exist and were "
                          "not taken" % max_rounds)

    cands = sorted(by_sig.values(), key=lambda c: (c["round"], c["id"]))
    unique_intents = sorted({p for c in cands for p in c["intents"]["pairs"]})
    return {
        "phase": "C — combination + intent engine",
        "name": name or "(unnamed run)",
        "examples": len(examples),
        "events": sum(ex["events"] for ex in examples),
        "arrangements": [{"role": r, "container": c, "support": arrs[(r, c)]}
                         for r, c in arr_list],
        "rounds": rounds,
        "rounds_run": len(rounds),
        "stopped_because": stopped_because,
        "candidates": cands,
        "counts": {
            "arrangements": len(arr_list),
            "combinations": len(cands),
            "by_order": {o: sum(1 for c in cands if c["order"] == o)
                         for o in sorted({c["order"] for c in cands})},
            "can_breed": sum(1 for c in cands if c["can_breed"]),
            "intent_candidates_total": sum(c["intents"]["count"]
                                           for c in cands),
            "intent_pairs_unique": len(unique_intents),
            "new_parameters_created": 0,
            "rows_written": 0,
            "killed": 0,
        },
        "answer": None,
        "chosen": None,
        "law": "a combination nothing exhibited is not available. Depth "
               "unlocks exactly where material recurred — one occurrence can "
               "never breed.",
        "refuses": "no write, no choice, no kill without a verdict handed in, "
                   "no silent cap.",
    }


# ---------------------------------------------------------------------------
# STAGE 22 — NEW COMBINATION AVAILABILITY, as a function instead of a by-hand
# diff of generations.
# ---------------------------------------------------------------------------

def delta(prev: dict, cur: dict) -> dict:
    """What the newer run opened that the older could not reach.

    His stage 22 asks one question — is anything NEW available? — and until
    now the answer was read by hand off two generation counts. This computes
    it: new signatures, deepened orders, and the intents only the new
    combinations reach."""
    p = {c["signature"]: c for c in prev.get("candidates", [])}
    q = {c["signature"]: c for c in cur.get("candidates", [])}
    new = [q[s] for s in sorted(set(q) - set(p))]
    gone_quiet = sorted(set(p) - set(q))
    deepened = [q[s] for s in q if s in p
                and q[s]["support"] > p[s]["support"]]
    prev_pairs = {t for c in prev.get("candidates", [])
                  for t in c["intents"]["pairs"]}
    new_pairs = sorted({t for c in new for t in c["intents"]["pairs"]}
                       - prev_pairs)
    return {
        "stage": 22, "name": "NEW COMBINATION AVAILABILITY",
        "newly_available": [{"signature": c["signature"], "order": c["order"],
                             "support": c["support"], "round": c["round"]}
                            for c in new],
        "count_new": len(new),
        "support_deepened": [{"signature": c["signature"],
                              "support": c["support"]} for c in deepened],
        "no_longer_reached": gone_quiet,
        "intents_only_the_new_reach": new_pairs,
        "anything_new": bool(new or deepened),
        "note": "computed, not diffed by hand. CALLING this on a write or a "
                "timer is Phase E — the function is the stage, the trigger is "
                "the scheduler.",
    }


# ---------------------------------------------------------------------------
# THE CHECK — evidence arrives from outside, the maturity moves, and a kill
# happens only on a verdict handed in. His default stands: kill=False.
# ---------------------------------------------------------------------------

def check(cand: dict, together_again: int = 0, apart_events: int = 0,
          kill: bool = False) -> dict:
    """Re-read one candidate against evidence HANDED IN.

    `together_again` — times the full set co-occurred in new material (this
    confirms the REPETITION prediction). `apart_events` — times parts recurred
    without the set (this is what the falsifier watches). Nothing here goes
    looking for evidence; stage 12 says where to look, and the verdicts come
    from outside."""
    from . import maturity as M
    confirmed = []
    if together_again > 0:
        pred = dict(cand["predictions"][0])
        pred["checked"] = True
        confirmed = [pred]
    mat = M.read(confirmed=confirmed, refuted=(),
                 counterexamples=apart_events,
                 support=cand["support"] + together_again,
                 sequences_seen=cand["support"] + together_again,
                 checks=1)
    out = {
        "id": cand["id"], "signature": cand["signature"],
        "was": cand["maturity"], "now": mat["state"],
        "verdict": mat["verdict"], "why": mat["why"],
        "killed": False,
    }
    if kill:
        from . import intent_ledger as IL
        k = IL.kill({"intent": cand["signature"], "falsifiable": True,
                     "falsifier": cand["falsifier"],
                     "support": cand["support"] + together_again,
                     "counterexamples": apart_events, "status": "LIVE"},
                    falsifier_met=(apart_events >= cand["support"]
                                   + together_again and together_again == 0),
                    counterexamples=apart_events)
        out["killed"] = not k.get("survives", True)
        out["kill_reading"] = k.get("why", "")
    else:
        out["kill_available"] = ("on request only — his word: 'nothing needs "
                                 "to kill for now, add everything and "
                                 "generate'")
    return out


# ---------------------------------------------------------------------------
# HIS NINE AUTO LOOPS — which ones this engine is, which already run
# elsewhere, and which wait for D and E. Stated, so C cannot quietly claim
# loops it does not own.
# ---------------------------------------------------------------------------

def loops() -> dict:
    return {
        "his_nine": [
            {"loop": "Combination", "where": "combine.run — THIS ENGINE",
             "state": "RUNS (started by hand; the trigger is E)"},
            {"loop": "Intent", "where": "combine.run -> intents.generate — "
                                        "THIS ENGINE feeds it per candidate",
             "state": "RUNS (started by hand; the trigger is E)"},
            {"loop": "Evidence", "where": "expected.py / combine._prediction",
             "state": "RUNS as prediction; checking is handed in"},
            {"loop": "R-F-R", "where": "patterns.rfr_check, runtime step 13",
             "state": "RUNS"},
            {"loop": "Next-Sequence", "where": "discovery.close, runtime "
                                               "step 18", "state": "RUNS"},
            {"loop": "Retrieval", "where": "his six read conditions, "
                                           "nodebrain.READ_CONDITIONS",
             "state": "DEFINED — reading by similarity is Phase D"},
            {"loop": "Contradiction", "where": "nodebrain contradiction_links",
             "state": "DEFINED — finding them is Phase D"},
            {"loop": "Memory Reinforcement", "where": "growth ledger + "
                                                      "node local_memory",
             "state": "WAITS FOR D — the per-node chain of readings"},
            {"loop": "Node-Growth", "where": "his box 6 decision tree",
             "state": "WAITS FOR D AND HIS ANSWER — the promotion policy "
                      "question is still open"},
        ],
        "c_owns": ["Combination", "Intent"],
        "note": "an engine that claimed all nine would be lying about four of "
                "them.",
    }


def stats() -> dict:
    return {
        "phase": "C — combination + intent engine",
        "gates": ["cross-role over SETS (a new part brings a new role)",
                  "co-occurrence (imaginable is not available)",
                  "recurrence to breed (support >= %d)" % RECURRENCE_TO_BREED],
        "structural_ceiling": "order 6 — six roles exist",
        "chain_on_every_candidate": ["prediction (stage 12)",
                                     "falsifier (feeds stage 17)",
                                     "maturity (stage 18)"],
        "stage_22": "delta() — computed, no longer by hand",
        "loops_owned": ["Combination", "Intent"],
        "writes": 0, "answers": 0, "kills_by_default": 0,
        "trigger": "by hand or from the runtime. Attaching it to a write or "
                   "the daemon is Phase E.",
    }


def annotations() -> list:
    return [
        ("rounds until quiet, with the stop stated", "combine.run"),
        ("one occurrence can never breed", "combine.RECURRENCE_TO_BREED"),
        ("cross-role extended to sets", "combine.run"),
        ("every candidate leaves carrying its chain", "combine._prediction"),
        ("stage 22 computed, not by hand", "combine.delta"),
        ("evidence handed in, kill on request only", "combine.check"),
        ("his nine loops, owned and not owned", "combine.loops"),
    ]
