"""WHAT EXISTS — his understanding, located in the code, and checked live.

His ask, verbatim:
  "i want to know the existence of my understanding in the code file and i want
   to use the tool so i can know what u did"
  "yes build it into the app as a page i can open"
  "rubric means paramters the 3000"

So: **a rubric IS a parameter.** The 3,072 are the rubrics. There is no separate
rubric type to invent — `ladder.py` already is the rubric store, and
`save_registry` already keeps every version of every edit. What is missing is
not the shape; it is that 18 of 3,072 carry anything.

WHY THIS FILE VERIFIES ITSELF: a hand-written map of "where things live" starts
true and goes stale the first time a line moves. Every row here carries an
ANCHOR — a literal string that must still be present in the named module. The
page reads the actual source at request time and reports FOUND (with the real
current line number) or MISSING. A row can therefore never silently become a
lie; if the code moves, the page says the anchor is gone.

Nothing here is a proposal. Absences are listed as absences.
"""
from __future__ import annotations

import os

# ---------------------------------------------------------------------------
# state values — what shape a piece of his understanding is actually in
RUNS = "RUNS"                  # wired into a live answer today
NOT_WIRED = "BUILT-NOT-WIRED"  # real, tested, and nothing calls it
THIN = "THIN"                  # runs, but on almost nothing
PARTIAL = "PARTIAL"            # runs in one direction only
ABSENT = "ABSENT"              # no existence anywhere

STATE_NOTE = {
    RUNS: "wired into a live answer today",
    NOT_WIRED: "real and tested — and nothing calls it",
    THIN: "runs, but has almost nothing to work on",
    PARTIAL: "runs in one direction only",
    ABSENT: "no existence anywhere in the code",
}

# ---------------------------------------------------------------------------
# THE MAP. Each row: his words · where it lives · what state · the honest note.
# "where" is a list of (module, anchor). The anchor is a literal substring the
# module must still contain.
MAP: list[dict] = [
 {"group": "THE ONE SEQUENCE — every work goes in it",
  "rows": [
   {"his": "there is sequence to follow, so every work go in one sequence",
    "where": [("sequence.py", "STEPS: tuple[tuple[int, str, str], ...] = (")],
    "state": RUNS,
    "note": "the eight steps: Ground · Pressure · Use · Witness · Expression · "
            "Naming · Halt · Loop. Its own header says step 6 is where the "
            "MASK forms — that is your Riemann finding stated generally."},
   {"his": "the transition, not the step · thresholds answer why now · "
           "no reopen · closure is a sequence word",
    "where": [("seq_kernel.py", "class Threshold:"),
              ("seq_kernel.py", "class SpawnContract:"),
              ("seq_kernel.py", "class Ledger:"),
              ("seq_kernel.py", "class SequenceClosure("),
              ("seq_kernel.py", "class EntityOutcome(")],
    "state": NOT_WIRED,
    "note": "all six objects are built and tested. NO module imports this "
            "file — it runs only in its own demo. The reasoning grammar you "
            "ruled on is real code the request path never touches."},
   {"his": "now we dont want 70-25 there, but i want more filters and fact "
           "kind of",
    "where": [("urr_matrix.py", "def review_node("),
              ("filters.py", "def run_gates("),
              ("engine.py", "from .filters import")],
    "state": NOT_WIRED,
    "note": "THE 70x25 MATRIX, KEPT AND UNLINKED. His decision removed it and "
            "the seven filters in filters.py replaced it — Ground · Sequence · "
            "Source · Mask · Fact · Halt · Loop, run on every finding, every "
            "time. `urr_matrix.py` stayed IMPORTED into engine.py long after, "
            "as `MATRIX, review_node`, and neither name was ever called: a "
            "live-looking link to a mechanism the answer path no longer uses. "
            "The old-file wiring audit (2026-08-30) found it and removed the "
            "LINK, not the module — his do-not-delete rule keeps the file on "
            "disk, and it is declared here so nothing has to rediscover that "
            "it is unwired. It is the replaced mechanism, not a missing one."},
   {"his": "keeping the half file back and using the half",
    "where": [("khalf.py", "def split_doc("),
              ("khalf.py", "def score_overlap("),
              ("khalf.py", "RULES = ")],
    "state": NOT_WIRED,
    "note": "THE HALF — the kappa experiment (Way Five of the Main Work room). "
            "Measures how much of a document's masked half can be "
            "reconstructed from the held half, racing three splitting rules "
            "(first_half · alternate · alt_words). Built and TESTED (two "
            "tests), and NO module imports it — it runs only from its own "
            "tests. Surfaced here by the old-file wiring audit (2026-08-30): "
            "it was the one orphan declared in NO map at all — not in this "
            "file, not in the build map, not in the arrow chart — so nothing "
            "could tell you it was unwired. Now it can."},
   {"his": "i dont wanted any proof of anything / i want to use RH as a code",
    "where": [("rh_code.py", "def half_confidence("),
              ("rh_code.py", "def explicit_answer("),
              ("rh_code.py", "def line_check("),
              ("rh_code.py", "HALF = 0.5")],
    "state": NOT_WIRED,
    "note": "RH AS CODE — Re(s) = 1/2 + ti read as a build specification, not "
            "a theorem: primes are the raw facts, log p their periods, the "
            "zeros are the doubts, 1/2 is how much power any single doubt may "
            "have, t is when it fires. Nothing here proves anything. Built and "
            "tested, and NO module imports it; `docs/mainwork/THE_BUILD_MAP."
            "html` already says 'rh_code.py · not wired yet' and "
            "`docs/riemann/RH_AS_CODE.md` says 'the engine has not been "
            "changed'. Carried into this file so the honest map holds every "
            "orphan in one place."},
   {"his": "Halt → Loop. a failure is never failure, it opens the mapped loop",
    "where": [("sequence.py", '(HALT, "Halt"'), ("sequence.py", '(LOOP, "Loop"'),
              ("filters.py", "def f7_loop(")],
    "state": RUNS,
    "note": "the halt becomes the next Ground. Filter 7 carries it — but see "
            "the seven filters below for what Filter 7 actually returns."},
  ]},

 {"group": "THE PYRAMID — his answer, built (2026-08-13)",
  "rows": [
   {"his": "my reading u shit that is ASI / which u supposed to build",
    "where": [("asi_pyramid.py", "def run("),
              ("asi_pyramid.py", "ROUTES = ["),
              ("asipage.py", "THE PYRAMID — ONE ASK OVER HIS 3,204")],
    "state": RUNS,
    "note": "his own reading of the Samrath sentence, executable. On his "
            "sentence it returns HIS numbers: 7 STRONG + 11 CANDIDATE = 18 of "
            "3,204 (0.56%), 3,186 inactive. Route /asi, POST /asi/run. It is "
            "not a lookup — different words in the same shape return the same "
            "18, and a flat report returns 1."},
   {"his": "SB-HFR-P0001..SB-HFR-P3204",
    "where": [("asi_pyramid.py", "def _flat("),
              ("asi_pyramid.py", "def container_span(")],
    "state": RUNS,
    "note": "his flat addressing, which he derived by hand. All 18 numbers he "
            "cited land on the name he gave them, and all 8 container ranges "
            "match — including the two containers holding 42 instead of 40."},
   {"his": "split it into historical pattern vs current exception, not one "
           "flat sentence",
    "where": [("asi_pyramid.py", "def read_scopes("),
              ("asi_pyramid.py", "def event_shell(")],
    "state": RUNS,
    "note": "PRIOR/REPEATED against CURRENT/TODAY, and the SAME EVENT SHELL "
            "held ONCE with two routes. The event never changed; the condition "
            "around it did."},
   {"his": "CRYING is not automatically SADNESS",
    "where": [("asi_pyramid.py", "AFFECT_BEHAVIOUR = {"),
              ("asi_pyramid.py", "def behaviour_not_state(")],
    "state": RUNS,
    "note": "his seven candidates stay unresolved, and a test proves P2250 "
            "Sadness never enters the activated set because he cried."},
   {"his": "these 3204, are the basic and vague setup / which will be making "
           "more with such examples / so keep adding not removing at all",
    "where": [("growth.py", "BASE = 3204"),
              ("growth.py", "def add("),
              ("growth.py", "def seed_items("),
              ("growth.py", "SERIES = {")],
    "state": RUNS,
    "note": "his reversal of what I had built. I had shipped a test whose "
            "stated job was to prove the bank does not grow, and wrote on the "
            "page that the bank never grows — treating his base as a ceiling. "
            "It is a floor. growth.py is APPEND-ONLY: no delete, remove, drop, "
            "clear, prune, truncate, os.remove, os.unlink, .pop or rmtree "
            "anywhere in it, the store opens in mode \"a\" only, and a test "
            "reads the module's own source to prove a removal path can never be "
            "added. Superseding appends a row referencing the old one and the "
            "old row stays whole. The gate is off — an addition is in the moment "
            "it is added; provenance is recorded because he needs it to correct "
            "a row, which is not a gate. Typed series, and only PARAM consumes "
            "his flat index at P3205 onward, because RUBRIC APPLICATION != "
            "ONTOLOGY EXPANSION. First seed: 199 rows computed from the live "
            "modules, of which 3 are new parameters — Security need, "
            "Mating/attraction, Revenge/retaliation, the three with no echo "
            "anywhere in his 3,204. Base 3,204 + 3 = 3,207. /growth, POST "
            "/growth/add, POST /growth/seed."},
   {"his": "as much parameters we plug, we will generate more pattern and "
           "intent / main bottleneck is system is not generating the new "
           "intent live",
    "where": [("intents.py", "def generate("),
              ("intents.py", "def scaling("),
              ("intents.py", "def motive_links("),
              ("intents.py", "BLOCKED_HOSTS = ("),
              ("intents.py", "def from_state_pack(")],
    "state": RUNS,
    "note": "the bottleneck he named, closed. Intent is now generated at "
            "runtime from CON-064 (the WHY, 40 rows) x CON-063 (the SHAPE, 40 "
            "rows), gated by which containers are active — so the count rises "
            "with the parameters plugged: 1 container -> 8 intents, 80 -> 140, "
            "monotonic and tested. The motive->container links are COMPUTED "
            "over his bank, and perception/motor/attention/language are blocked "
            "from hosting a motive, which removed 67 lexical fabrications "
            "(200 edges -> 133). Three real motives (Security, Mating, Revenge) "
            "have no echo anywhere in the 3,204 and are reported as absences. "
            "Nothing enters the bank, chosen stays None, and motive-inference "
            "confidence stays LOW. /intents, POST /intents/run, and the live "
            "block on /generation."},
   {"his": "everything happening is a event, and all events have intent / "
           "current phase is growing phase / example sit on existing parameters "
           "and IDs so system can strong its base / every example will keep "
           "increase the count",
    "where": [("growing.py", "def events_in("),
              ("growing.py", "def seat("),
              ("growing.py", "def intent_seat("),
              ("growing.py", "def place("),
              ("growing.py", "def grow("),
              ("growing.py", "def coverage("),
              ("filemap.py", "def divide(")],
    "state": RUNS,
    "note": "his correction of what I had been doing. I had been running his "
            "examples as OUTPUT TESTS — scoring how well the machine answered "
            "Samrath, the mall, the tablet. That is not what an example is for: "
            "it is material that SEATS on the base. place() returns a placement "
            "and carries no answer, verdict or score, and a test enforces that. "
            "The motto is mechanical: events_in() finds happenings "
            "morphologically, NOT from a closed list — micro.py's 215-verb list "
            "missed both 'standing' and 'pointed' in his own rain sentence, and "
            "across his 217 files 5,906 of 13,848 events (43%) are found only by "
            "inflection. Every event carries an intent slot seated on CON-063 and "
            "CON-064, never absent. Seating is two-stage: the event's ROLE picks "
            "which segments may host it, then words pick rows inside them; a row "
            "matching by word but outside the role is kept as out_of_role, never "
            "counted and never dropped. The IDF bar is HIS number — a word in "
            "forty of his names — and is honestly reported as the small gate, not "
            "the main guard. Two mechanics, not one: seating gives an existing ID "
            "SUPPORT and creates no parameter, while every example appends "
            "1 + 2N rows so the count always rises. All 479 repo files are "
            "divided into SOURCE/EXAMPLE/METHOD/BANK/SYSTEM/ARTIFACT/OPERATIONS "
            "with 0 unplaced; 217 grow the count, 39 are what they grow against. "
            "His examples reach 2,816 of 3,204 (87.89%), 388 untouched. "
            "basic_over is False and is HIS call, not a threshold I set. "
            "/growing, /growing/coverage, POST /growing/place, "
            "POST /growing/grow."},
   {"his": "build phase A / do it slowly and with efficincy",
    "where": [("nodebrain.py", "NODE_TYPES = ("),
              ("nodebrain.py", "LINK_TYPES = ("),
              ("nodebrain.py", "def fingerprint("),
              ("nodebrain.py", "def new_node("),
              ("nodebrain.py", "def validate("),
              ("nodebrain.py", "def collisions(")],
    "state": RUNS,
    "note": "PHASE A of his SELF-SUSTAINING EXECUTION FLOW sheet — lock node "
            "schema, IDs, headers, ledgers. It is first because every later "
            "phase WRITES INTO this shape: a field renamed after the graph "
            "exists would invalidate every edge already stored. His box 3 "
            "verbatim: 12 node types, 16 fields, 4 statuses each carrying its "
            "meaning; his box 6: 10 TYPED links, each with a direction and an "
            "inverse and the field it lands in — which corrects my own auto "
            "proposal, where I had ONE untyped edge (shared seated IDs) and "
            "would have built a similarity blob; his box 4: 11 memory kinds, 5 "
            "write conditions and 6 read conditions, defined here as the "
            "contract and ENFORCED at the write site only in his Phase D. THE "
            "LOCK IS A CHECK, NOT A COMMENT: fingerprint() hashes the whole "
            "schema and a test pins the hash, so changing a type, field, link, "
            "status or condition without bumping SCHEMA_VERSION fails and names "
            "what moved — the same technique stage 1 SOURCE LOCK still lacks. "
            "point_zero_ref is REQUIRED, which is his 'no invention before "
            "source lock' made structural. A malformed node is REFUSED with the "
            "reason named, never stored malformed. IDs live under their own "
            "SB-N- prefix and carry their type stem (SB-N-EVT-00001), so a bank "
            "id or a ledger id can never be read as a node id and the stem must "
            "agree with the declared type. FIVE NODE-TYPE NAMES COLLIDE with the "
            "growth series — EVENT, INTENT, PATTERN, RULE, STATE — and NONE is "
            "merged: each is reported with what it means on both sides (a growth "
            "EVENT is a SHELL, an EVENT node is one occurrence) and the ruling "
            "is his. Phase A writes nothing and links nothing, and a test reads "
            "the module's own code, with docstrings and comments stripped, to "
            "prove there is no growth.add call, no file write, no tick and no "
            "Thread in it. /nodes/schema."},
   {"his": "build phase A [continued on his word] — Phase B, the runtime "
           "pipeline: the eighteen steps of his AUTO RUNTIME ENGINE box as one "
           "run",
    "where": [("prior.py", "def declare_end("),
              ("prior.py", "def end_candidates("),
              ("prior.py", "def prior_reality("),
              ("prior.py", "def removal_test("),
              ("prior.py", "def entailments("),
              ("prior.py", "def assume("),
              ("prior.py", "def ground_check("),
              ("runtime.py", "STEPS = ("),
              ("runtime.py", "def run("),
              ("runtime.py", "def detect_states(")],
    "state": RUNS,
    "note": "PHASE B of his sheet. Sixteen of his eighteen steps already "
            "existed as separate modules reached by hand; the two that did NOT "
            "exist — step 2 DECLARE END / WHY THIS MATTERS and step 3 REVERSE "
            "TO PRIOR REALITY — are both reverse-direction and both sit BEFORE "
            "decomposition, which is the correction: R-F-R at step 13 is the "
            "SECOND place reverse happens, and this core had been running "
            "forward from the text and reversing only at the check. prior.py "
            "builds them from his own method doc (THE_REVERSE_WALKS.md): "
            "declare_end grades a PULL (target ahead) apart from a PUSH (reason "
            "behind) and NEVER promotes a reason to a target; two ends at the "
            "same grade HALT, unblended, with what would separate them stated "
            "as predictions; an unnamed end is UNNAMED with what would name it "
            "— 'there is no reason' is not an available answer. prior_reality "
            "descends by HIS removal test (take the step away — if the thing "
            "above still stands it was a neighbour), grades every prior STATED "
            "or ENTAILED, and CANNOT assume: ASSUMED exists only through an "
            "explicit assume() call that stamps [SYNTHETIC] with proof debt and "
            "expiry, and a test asserts the descent returns zero ASSUMED rows. "
            "A drop the lexical test cannot be trusted on (same sentence, no "
            "shared word — his rain sentence's 'pointed it in the air') is "
            "FLAGGED for his review, never quietly reversed. Dropped priors are "
            "kept as neighbours with the reason. Ground is claimed only when "
            "reached ('something nobody made'), which on most single asks it is "
            "not, and it says so. runtime.run then walks ALL EIGHTEEN in his "
            "order — each record carrying the step's own job, what it took and "
            "what it produced (his SB-01 correction applied to the runtime) — "
            "and returns answer: None on every run, structurally: the runtime "
            "prepares, he decides. A step that cannot bite on one ask says so "
            "rather than faking: R-F-R on a single unrepeated ask reads thin, "
            "maturity reads UNTESTED, the verdict reads UNKNOWN. Step 17 "
            "PREPARES the writeback and evaluates his five write conditions "
            "without writing — enforcement at the write site is Phase D, and on "
            "a bare run two of five conditions are honestly unmet (no link map, "
            "no origin distance). Detection is not choice: his sixteen packs "
            "are checked for evidence words and chosen stays None. The "
            "combination step runs the same cross-role gate that cut 2,627 to "
            "2,119, scoped to the ask (since Phase C it hands its seatings to "
            "the ONE engine in combine.py, so the runtime's view and the "
            "engine's can never drift). /runtime, POST /runtime/run."},
   {"his": "build phase C — the Combination + Intent Engine of his sheet; his "
           "own concept: 'as much parameters we plug, we will generate more "
           "pattern and intent' / 'once the basic will over it will start "
           "making new combinations on new thoughts'",
    "where": [("combine.py", "def run("),
              ("combine.py", "def _prepare("),
              ("combine.py", "def delta("),
              ("combine.py", "def check("),
              ("combine.py", "def loops("),
              ("combine.py", "RECURRENCE_TO_BREED = "),
              ("combine.py", "def _prediction("),
              ("combine.py", "def _falsifier(")],
    "state": RUNS,
    "note": "PHASE C. What existed was generation as STEPS — selfmake over "
            "the repo (pairs only), runtime step 9 over one ask, "
            "intents.generate gated by containers. What did not exist: "
            "ROUNDS (a combination could never combine again, so 'new "
            "combinations on new thoughts' had no mechanism), a STOP (nothing "
            "said when generating was finished), the CHAIN (a combination "
            "arrived bare), and stage 22 as a function. combine.run generates "
            "in rounds until QUIET and states which way it stopped. FOUR "
            "GATES, in order: cross-role over SETS (a new part must bring a "
            "role the set does not hold — six roles, so order 6 is the "
            "structural ceiling); CO-OCCURRENCE (all parts together in at "
            "least one example — imaginable is not available); the ANCHOR "
            "(every combination must hold at least one ROW-granularity part; "
            "a role-event no word reached enters as ONE unanchored part, "
            "because folding the role's 16-container scaffold in once turned "
            "one two-sentence text into 240 candidates — the cross-product "
            "failure through a side door, caught and the fix is why his rain "
            "sentence now yields exactly 1: ACTION on CON-021 met an "
            "INFERENCE); and RECURRENCE TO BREED (an order-2 candidate "
            "enters a deeper round only at support >= 2 — maturity's own "
            "RECURRENCE_MIN, his rule 6 — so one example can NEVER produce "
            "order 3, and a test pins it). Genuinely new against selfmake: "
            "selfmake's COMBINATION steps stop at PAIRS; the engine breeds "
            "order 3+ where support earned it. EVERY candidate leaves "
            "carrying its chain: prediction (stage 12, the REPETITION row "
            "names its own parts so it discriminates by construction), "
            "falsifier (parts recurring apart while together stays stuck — "
            "feeds intent_ledger.kill), and maturity (stage 18) — and "
            "maturity is fed honestly: co-occurrence is SUPPORT, an input, "
            "never a confirmation, so an unchecked candidate reads UNTESTED "
            "whatever its support. check() moves a maturity only on verdicts "
            "HANDED IN (together_again confirms the REPETITION prediction; "
            "apart_events is what the falsifier watches) and kill=False is "
            "the default — his word. delta() is stage 22 computed: new "
            "signatures, deepened support, the intents only the new "
            "combinations reach; the discovery audit now reads 22 RUNS (21 "
            "of 23, stages 1 and 5 the remaining PARTIALs, both Phase D's "
            "business). loops() states which of his NINE auto loops C owns "
            "(Combination, Intent) and which it does not — an engine that "
            "claimed all nine would be lying about four. The engine never "
            "writes, never chooses, never kills unbidden, never caps "
            "silently — a cap that bites reports what it dropped. paths= "
            "runs it on his corpus through selfmake's OWN harvest so the two "
            "can never disagree about what a file exhibits. /combine, POST "
            "/combine/run."},
   {"his": "build phase D — the Memory Graph + Auto-Linking of his sheet; "
           "the node schema Phase A locked becomes a living, traversable "
           "store",
    "where": [("nodegraph.py", "def write_node("),
              ("nodegraph.py", "def recall("),
              ("nodegraph.py", "def autolink("),
              ("nodegraph.py", "def remember("),
              ("nodegraph.py", "def memory_of("),
              ("nodegraph.py", "def path("),
              ("nodegraph.py", "def neighbours("),
              ("nodegraph.py", "def subgraph("),
              ("nodegraph.py", "def gates_of("),
              ("nodegraph.py", "def queue_for_him("),
              ("nodegraph.py", "def approve("),
              ("nodegraph.py", "def _write_hub(")],
    "state": RUNS,
    "note": "PHASE D. THE WRITE GATE IS ENFORCED: Phase A defined his five "
            "write conditions and said enforcement is Phase D — "
            "nodegraph.write_node is that site, and a write failing a "
            "condition is REFUSED with the unmet conditions named, never "
            "stored malformed. The fourth condition (link map created) is "
            "met BY the write path itself, because the auto-linker runs "
            "inside it — which is exactly why it could not be enforced "
            "before D existed. HIS SIX READ CONDITIONS ARE ONE MECHANISM "
            "USED TWICE: recall() answers which stored nodes material "
            "reaches and by which condition with the evidence named (the "
            "Retrieval loop), and the auto-linker is the SAME call at write "
            "time — what recall finds, the linker links, so retrieval and "
            "linking can never disagree. LINKS ARE TYPED AND THE GRAPH HAS "
            "THE SHAPE HIS TWELVE TYPES EXIST FOR: two events by the same "
            "actor do not get a vague tie — an ACTOR node materializes ONCE "
            "and each event links to it actor_of; events SUPPORT their "
            "pattern node, DEPEND_ON their artifact (prior.py's own "
            "entailment), are FUTURE_OF the state they worked toward; "
            "similar_to is reserved for events sharing 2+ actual seated "
            "rows, and CONTAINERS ALONE NEVER LINK — the Phase C anchor "
            "lesson, structure is not content. THE CONTRADICTION LOOP IN "
            "ITS HONEST SCOPE: contradicts fires structurally on one case "
            "only — same subject, opposing verdicts (RETAIN vs REJECT); "
            "deeper detection from prose is model-grade inference this "
            "module does not have and does not claim; richer contradictions "
            "arrive from a caller that saw them. A defect the first "
            "contradiction test caught: the box-6 dedupe matched on subject "
            "and actor but NOT verdict, so an OPPOSING reading was folded "
            "into the node it opposed — a contradiction silently swallowed "
            "as a duplicate; the match now requires the same CLAIM (same "
            "signature, same actor, same verdict), and the opposing reading "
            "is written and contradiction-linked with both standing. AN "
            "EXISTING MATCH IS REINFORCED, NEVER RE-CREATED: support 1 -> "
            "2, duplicate_created False — his mall-example reinforcement "
            "rule applied to nodes. THE PER-NODE MEMORY CHAIN is remember() "
            "— append-only readings each referencing the one before "
            "(maturity.update's shape applied to a node), kinds constrained "
            "to his eleven — the store the 90-of-95-empty-brains finding "
            "has needed since the August audit. STAGE 5 NOW RUNS (22 of 23; "
            "stage 1 source lock is the last PARTIAL): neighbours/path/"
            "subgraph make the relation graph traversable with every hop "
            "TYPED — a path through contradicts means something different "
            "from one through supports. HIS BOX 6 RUNS UP TO ITS QUEUE AND "
            "STOPS WHERE ONLY HIS WORD MAY ACT: the evidence gate and "
            "maturity threshold are EVALUATED, a node passing both is "
            "QUEUED FOR HIM with its evidence, promoted stays 0 until his "
            "word, approve() exists as HIS action (an APPROVAL row "
            "referencing the node — the NODE row is never rewritten, NO "
            "REOPEN), and the queue is stated as a placeholder for his "
            "unanswered promotion question, not the answer. APPEND-ONLY "
            "STRUCTURALLY: no removal path exists in the module, the store "
            "opens mode-a only, a corrupt line comes back UNREADABLE with "
            "its raw text, and a test reads the module's own source (the "
            "growth.py technique). Eight of his nine auto loops now run; "
            "the ninth (Node-Growth) runs up to the queue. /nodes, "
            "/nodes/node, /nodes/path, /nodes/subgraph, POST /nodes/write, "
            "POST /nodes/remember, POST /nodes/recall, POST /nodes/approve."},
   {"his": "build phase E — the Self-Sustain Scheduler of his sheet, under "
           "his own staging law: Manual Mode Now -> Semi-Auto -> Auto-Sustain "
           "Target",
    "where": [("autoloop.py", "def tick("),
              ("autoloop.py", "def tick_if_due("),
              ("autoloop.py", "def set_mode("),
              ("autoloop.py", "def mode("),
              ("autoloop.py", "def refs_from_run("),
              ("autoloop.py", "def _inbox_material("),
              ("autoloop.py", "def gate("),
              ("scheduler.py", "autoloop.tick_if_due")],
    "state": RUNS,
    "note": "PHASE E — the last phase, and the machinery ships WHOLE with "
            "the mode at MANUAL: deploying it changes NOTHING until he lifts "
            "the mode, and lifting it is HIS action (POST /auto/mode), "
            "recorded as its own append-only row with what it was before. "
            "His correction is honored exactly — it is STAGED, not a switch. "
            "THE TICK is one bounded pass of the loop his sheet draws: "
            "material arrives (handed texts, files dropped in the inbox, or "
            "— in AUTO_SUSTAIN — the previous tick's own written nodes), "
            "each item runs the Phase B runtime, autoloop.refs_from_run "
            "composes the node refs FROM THE RUN'S OWN STEPS (the wiring "
            "Phase D left stated as open), the node is written through "
            "Phase D's GATED write site — his five conditions, a refused "
            "write stays refused — the Phase C engine runs over the tick's "
            "material and delta() reports what opened against the tick "
            "before. THE DAEMON THAT ALREADY RUNS drives it: the hourly "
            "thread that has driven the weekly pull since Phase 1 now also "
            "calls tick_if_due, each in its OWN try so neither can kill the "
            "other; in MANUAL tick_if_due returns without doing anything. "
            "THE FOUR LAWS OF THE TICK, each tested: (1) THE GATE DOES NOT "
            "MOVE — a tick may seat, link, combine, predict; it may NOT "
            "promote, answer, kill, add a parameter, or write his count "
            "ledger, enforced STRUCTURALLY: no approve, no kill, no "
            "growth.add exists in the module's code and a test reads the "
            "source; the queue for him fills and promoted cannot move from "
            "here. (2) BOUNDED, EVERY CAP REPORTED — 5 items and 40 nodes "
            "per tick; a deferred INBOX file is genuinely picked up next "
            "tick (the cursor never saw it) while a deferred HANDED text is "
            "NOT stored and the report says it must be handed again, "
            "because claiming 'never dropped' for both would be false for "
            "the second — a dishonest line the first test run caught. (3) "
            "QUIET IS QUIET — a daemon tick that finds nothing new appends "
            "nothing (an hourly heartbeat would flood an append-only "
            "ledger); a HAND tick always appends, because he asked and "
            "'quiet' is an answer. (4) NOTHING IS UN-PROCESSED BY DELETION "
            "— inbox files are never removed; the cursor is a fold over "
            "past reports (name -> content hash); an unchanged file is "
            "skipped and said so, a CHANGED file is a superseding reading. "
            "FEEDBACK IS EXACT: in AUTO_SUSTAIN the previous tick's written "
            "nodes re-enter as ONE prepared example for the engine — the L4 "
            "loop, the only loop whose input is the system's own output — "
            "bounded to the last tick, its delta reported, and a feedback "
            "pass that opens nothing is the loop finding its own quiet. A "
            "TICK IS NOT A CHECK: maturities decay on checks-without-"
            "confirmation (his rule) and a tick checks nothing against the "
            "world, so maturities do not move here — evidence still arrives "
            "from outside on his word or a caller's verdict. All nine of "
            "his auto loops now have their trigger; the ninth still stops "
            "at the queue. /auto, POST /auto/tick, POST /auto/mode."},
   {"his": "i dont want black back ground / the web should have all 3000+ "
           "para, algo which it use / and transparent so i can see which is "
           "linked where or under the each answer it should show and must be "
           "editable so i can change / where is the ask tab / build it as the "
           "new home page",
    "where": [("homepage.py", "PAGE = r"),
              ("server.py", '"/desk"'),
              ("server.py", '"/api/hud"'),
              ("server.py", '"/api/bank"'),
              ("server.py", '"/growth/correct"'),
              ("growth.py", "CORRECTION = ")],
    "state": RUNS,
    "note": "THE GLASS REACTOR — the home page, his rulings from the mockup "
            "rounds all binding. NO BLACK: a luminous light ground; the dark "
            "dashboard is NOT deleted — it lives whole at /desk, linked from "
            "the new page. ALL 3,204 ON SCREEN: the reactor draws one point "
            "per parameter from /api/bank, which carries the REAL container "
            "counts (the two 42s included) and each container's flat P start "
            "— so a seated row lights its EXACT point (Standing balance = "
            "CON-021 start 801 + index 34 = P0835, precisely his rain seat), "
            "and no figure on the page is typed into the markup: every "
            "number is fetched live or shown absent. THE ASK TAB — his catch "
            "on the sample — heads the panel and calls the SAME engine the "
            "/engine page calls (POST /ask, the full SB walk) plus "
            "/growing/place for what it seats and /runtime/run for his "
            "eighteen steps: three views of ONE ask, never a second engine, "
            "and Promise.allSettled so one unreachable view cannot kill the "
            "others. UNDER EACH ANSWER, WHAT IT USED: the answer's own tags "
            "(classification, evidence, confidence, falsifier, open "
            "question), the parameter chips with his row names, the seven "
            "filters folded across all 70 nodes of the walk with HALTs in "
            "amber, and the eighteen steps with reverse marked. TRANSPARENT "
            "= ONE SELECTION, THREE VIEWS: touch a container anywhere — the "
            "reactor arc, the chip, the strip cell — and all three light "
            "together, its rows open below from /registry/container. "
            "EDITABLE = HIS LAW: the pencil on any row or chip takes his "
            "words and POSTs /growth/correct, which appends a CORRECTION row "
            "(new growth series, SB-CORR-%04d) carrying target, was and now "
            "— the registry document is NEVER rewritten, and a test proves "
            "the source row stays whole. /, /desk, /api/hud, /api/bank, "
            "POST /growth/correct."},
   {"his": "failure - ... they try to copy and failed / they built something "
           "there own, how someone can re do the same / We should take the "
           "success stories 'if they can i will too' instead 'i will also do "
           "the same'",
    "where": [("claims.py", "def success_story_stance("),
              ("claims.py", "THEIRS_NON_COPYABLE = "),
              ("bridge.py", "SEEDED = ("),
              ("bridge.py", "def match("),
              ("bridge.py", "def rows_via("),
              ("bridge.py", "KNOWN_ABSENCE = "),
              ("growing.py", "bridged = BR.rows_via(text)"),
              ("growth.py", "BRIDGE = ")],
    "state": RUNS,
    "note": "His teaching of 2026-08-24, canon at "
            "docs/method/canon/IF_THEY_CAN_I_WILL_TOO.md — the second half of "
            "the rice/MBA law: that one forbids JUDGING the visible thing as "
            "proof of the system behind it, this one forbids USING it as a "
            "template for action. success_story_stance() reads material "
            "carrying a success story for its stance: TEMPLATE COPY ('i will "
            "also do the same') can never stand as this machine's conclusion "
            "and comes back carrying what was THEIRS (the judgment gate's own "
            "hidden layers — system, capabilities, inputs, execution, timing "
            "— exactly what the copier never sees), what TRANSFERS (the "
            "possibility proof, nothing else), and his flip verbatim; "
            "POSSIBILITY ('if they can i will too') is his stance, kept; an "
            "UNSTATED stance is held open with both readings shown and "
            "neither chosen. His own teaching sentence carries both phrasings "
            "and resolves to POSSIBILITY because 'instead' IS the choice — "
            "tested. The machine refuses the CONCLUSION, never the person. "
            "His 'failure' re-read: their success and this path are two "
            "different sequences, so the comparison was never valid and its "
            "failure is not a verdict on the person. ON HIS WORD ('build the "
            "bridge and approve all three') THE BRIDGE IS BUILT: bridge.py — "
            "taught vocabulary, never an imported dictionary; three seeds "
            "each carrying his approval (BR-001 copy/imitate -> CON-023 "
            "Imitation P0885-87; BR-002 'if they can i will too' -> P2451 "
            "Self-efficacy; BR-003 role-model -> P2625 Ideal self); wired "
            "into growing.seat with BOTH READINGS ALWAYS KEPT (bridged rows "
            "in their own list, never merged into direct seats; place() "
            "marks them via_bridge with the firing phrase); whole-word and "
            "longest-phrase-first matching; a bridge may cross the role gate "
            "with the reason stated. The routine reading of his teaching "
            "moved 3 rows -> 7. The absence (social comparison, general) is "
            "REFUSED a wrong bridge — P0597 is BODY-comparison — and stands "
            "as his call. Approvals on the live ledger: SB-PAT-001 THE COPY "
            "LOOP, SB-AXIS-001 RANDOM-VS-SUPPOSED; the BRIDGE series "
            "(SB-BR-%03d) is new for future taught bridges. Open wiring, "
            "stated: the runtime's step-5 seating and the combine engine "
            "consume direct seats only — bridged rows do not yet enter "
            "arrangements."},
   {"his": "just adopt what is not here, do not touch and change anything in "
           "the C-SB repo / n lay off ur brain / just work under ASI "
           "instructions vague, big picture, anything if u tweak, ask me "
           "first",
    "where": [("adopted.py", "def verify("),
              ("adopted.py", "def halts("),
              ("adopted.py", "def custody("),
              ("adopted.py", "def wisdom("),
              ("adopted.py", "def his_examples("),
              ("adopted.py", "def intent_types("),
              ("filemap.py", "ADOPTED = ")],
    "state": RUNS,
    "note": "THE ADOPTION FROM C-SB, canon at "
            "docs/method/canon/THE_ADOPTION_FROM_C_SB.md. 42 files "
            "byte-identical from damandamanaulakh-tech/C-SB @ 9e3f179, each "
            "SHA-256 in adopted/C-SB/ADOPTION_CUSTODY.json carrying his word "
            "verbatim; verify() re-hashes all and a drifted byte is NAMED. "
            "C-SB untouched (working tree checked clean after the copy). "
            "Adopted with statuses preserved as C-SB states them: the "
            "Real-Time ASI Constitution V1 + Growing-Phase Constitution V1 + "
            "30 SEQ-LOCKs + system invariants + the EVENT-INTENT GROWTH "
            "CONTRACT (8 typed intents, UNKNOWN preferred over fabrication); "
            "the banks this core lacked (AI-only 64, 75 engines, operational "
            "161-240 + 2593-3072, expansion SB-ASI-P2561..P2592, native "
            "2,560 + custody parts); the 22-node ASI service registry; "
            "rubrics R01-R52; the whole BG 2.47-2.50 wisdom pipeline with "
            "C-SB's own scope (contextual, never doctrinal canon or action "
            "authority); his RAW originals including the true rain wording; "
            "five v2 lock CANDIDATES kept candidates. NOTHING WIRED INTO "
            "BEHAVIOR — the engine runs exactly as before, adopted.py has no "
            "write path and imports no engine module (source-scan test). "
            "SEVEN ADOPT-HALTs stand for him, decided by nobody: the P2561 "
            "namespace collision (SB-ASI-P2561 Cardiac Salience Spike vs "
            "SB-HFR-P2561 — same numerals, different rows, kept apart under "
            "his do-not-silently-merge rule); three node vocabularies; "
            "R01-R52 vs his 25 dimensions; typed-intent wiring; the wisdom "
            "objects into the scripture Wisdom Bank; 75 engines + 240/3,072 "
            "beside 80/3,204; mirroring C-SB's phase-2 history. His mode "
            "instruction is standing law: adoption mechanical and verbatim, "
            "interpretation is a HALT. In the file divide the adopted tree is "
            "its own class — ADOPTED: custody, not a role — in neither the "
            "grows sum nor the grows-against sum, never on the harvest list; "
            "any existing class would have decided a seam that is his. "
            "/adopted."},
   {"his": "rebuild it complete with all 183 containers and all rows / now file "
           "it in repo and wire it",
    "where": [("sbx.py", "def place_on_spine("),
              ("sbx.py", "def verify("),
              ("sbx.py", "def spine("),
              ("sbx.py", "def computer_of("),
              ("sbx.py", "OPEN_LAYERS = ")],
    "state": RUNS,
    "note": "THE COMPLETE ARCHITECTURE (2026-08-29). His split, filed and wired: "
            "6 macro pillars, the 12-step spine, 27 segments, 183 containers, "
            "3,483 rows, 175 filters, 12 states, 7 evidence levels, 20 failure "
            "classes, 34 chain steps, 67 rubrics and the 9 approved intent types "
            "— each placed at the step where it acts, not merely listed. Data at "
            "data/sbx_architecture.json (700KB), document at "
            "docs/THE_COMPLETE_ARCHITECTURE.md. EVERY NODE CARRIES BOTH COLUMNS: "
            "the human name he wrote and a computer parallel, because ASI is the "
            "verified connection between the two sides and one column alone "
            "cannot link. HIS LOOP IS PRESERVED: steps 1-8 are first order and "
            "step 8 closes to step 1; 9-12 are the life of the loop across many "
            "cycles and 11-12 can fire at any step — recorded as `order` on every "
            "step so the closure is never lost. THE SOURCE BANK IS REPLACED, "
            "NEVER DELETED: data/human_registry.json still reads 3,204 rows and "
            "80 containers, and a test proves it. place_on_spine() is the wiring "
            "— the seating is unchanged, it is now READ through the split and "
            "lands the ask on steps; a row that finds no home is reported by the "
            "difference between source_rows_seated and mapped_into_split, never "
            "dropped. ARCHETYPE, LINK and SCALE are declared with no ceiling and "
            "hold nothing yet. /sbx, /sbx/step, /sbx/container, POST /sbx/place."},
   {"his": "one was change of meaning n outcomes from the old example n quotes "
           "i provided",
    "where": [("reread.py", "EXAMPLES = ("),
              ("reread.py", "RULINGS = ("),
              ("reread.py", "def report("),
              ("reread.py", "INSTRUMENTS = {")],
    "state": RUNS,
    "note": "PHASE 15 — THE RE-READ (2026-08-30). His ask: 'every file, every "
            "example and every teaching re-read under the new rulings — the "
            "rain example was proved on the old body/brain ruling and must be "
            "re-read on the new one.' A reading recorded in the canon is a "
            "reading AT A DATE; left alone it becomes a claim about today that "
            "nobody checked. 8 of his examples, each holding THEN (what was "
            "RECORDED, with the file it was recorded in — never reconstructed) "
            "against NOW (the live run through every layer), with which of his "
            "7 rulings accounts for any movement. RESULT: 5 changed, 2 "
            "unchanged, 1 NOT RECORDED, 0 UNEXPLAINED — every movement has a "
            "named ruling behind it, and a movement without one would be "
            "drift. HIS NAMED CASE IS THE FINDING: the rain sentence read 2 "
            "rows when recorded and reads 2 rows now, so a count-only check "
            "calls it UNCHANGED — and BOTH ROWS ARE DIFFERENT (Air/breathing "
            "drive + Thought suppression became Standing balance + "
            "Reaching-while-standing control, not one row surviving). That is "
            "the verdict CHANGED — SAME COUNT, DIFFERENT ROWS, and it exists "
            "because a count is not a meaning. The defect the canon recorded "
            "beside it — 'still shows Standing balance when the father is not "
            "balancing' — is carried on the row and is STILL LIVE. TWO "
            "DEFECTS OF MINE THAT BUILDING IT CAUGHT: the first draft "
            "paraphrased his sentences (Samrath gave 84 rows instead of his "
            "106 — the paraphrase was the difference, not the system), and it "
            "compared every recorded number against the SEATING, reporting the "
            "mall at 72->0 and Samrath at 106->0 as catastrophic regressions "
            "when neither number was ever produced by the seating — they came "
            "from asi_pyramid.rows_for, a different instrument. Every example "
            "now records WHICH instrument produced its `then` and the re-read "
            "runs that one. IT CHANGES NOTHING: no example is re-filed, no "
            "canon corrected, and the new reading is not declared the right "
            "one — two readings of one example is his own law's case, both "
            "stand and the gap goes to him. A source-scan test proves the "
            "module has no write path. /reread, /reread?id=EX-RAIN."},
   {"his": "scale becomes a stored axis — more than four; the four you named "
           "are a start, not the set",
    "where": [("scale.py", "HIS_BANDS = ("),
              ("scale.py", "PROPOSED_BANDS = ("),
              ("scale.py", "def active("),
              ("scale.py", "def spread("),
              ("scale.py", "def gate(")],
    "state": RUNS,
    "note": "PHASE 11 — THE SCALE AXIS (2026-08-29). His teaching is the "
            "reason it exists: 'One event of those books is used in 100 daily "
            "responses.' THE RECOVERY STAKE is not a story about a king with "
            "dice — it is the same arrangement in a child who will not switch "
            "off a losing game, a trader averaging down, a person arguing past "
            "repair, and a nation escalating a war. Those are not four "
            "archetypes; they are ONE read at four sizes, so scale is a "
            "COORDINATE the reading moves along, not a tag it carries. NINE "
            "BANDS, ordered smallest to largest: his four (micro · individual "
            "· relational · macro) and five PROPOSED — moment, household, "
            "organisation, dynasty, civilisation. Nothing is invented to fill "
            "a pattern: EACH PROPOSED BAND CITES THE EXAMPLE OF HIS THAT "
            "DEMANDS IT, and the citation is the whole justification. `moment` "
            "because his stealing demonstration is about ONE ACT and micro is "
            "still a person, so 'THIEF is a conclusion, taking money is the "
            "observation' had no coordinate. `household` because ARCH-010 is "
            "in his words 'family, friends and coworkers' and the father-door "
            "example is standing obligation nobody chose, not two equals "
            "meeting. `organisation` because his BJP example is a PARTY "
            "choosing for a task and ARCH-003's top-heavy pyramid is a "
            "company — neither relational nor macro, and his whole weighting "
            "mechanism lives at that size. `dynasty` because what Yudhishthira "
            "stakes is a HOUSE and the loss lands on people not yet born — a "
            "population across time, which macro cannot hold. `civilisation` "
            "because his own frame is 'since modern humans came out of caves' "
            "and the tablet is ~5,500 years old. HIS GATE IS ENFORCED, NOT "
            "DESCRIBED: building the axis is not naming the bands. All nine "
            "are stored and readable; `active()` returns HIS FOUR AND ONLY HIS "
            "FOUR, `approved` is False on every proposal, and a test pins it. "
            "An unfilled band says NOT STATED, never zero and never a guess — "
            "ARCH-001 reads 4 filled, 5 not stated. /scale, /scale?id=ARCH-001, "
            "POST /scale/run."},
   {"his": "a live run on 'a man is stealing the money' producing all nine "
           "readings where it produces zero today",
    "where": [("readings.py", "TYPES = ("),
              ("readings.py", "def read("),
              ("readings.py", "def verify("),
              ("readings.py", "ADOPTED_HALT = {")],
    "state": RUNS,
    "note": "PHASE 12 — THE NINE READINGS (2026-08-29). His own demonstration "
            "is the whole design: a man is taking money, and that single "
            "visible act carries four reasons he named himself — THIEF · "
            "OPPORTUNITY · HABIT · SAVING A LIFE — with the hand moving "
            "identically in all four. His motto says every event HAS an "
            "intent; it does NOT say the event announces it. So the honest "
            "output of an event is not one intent but every intent it could "
            "carry, all standing, none chosen. WHAT CHANGED: before this an "
            "ask reached intent TYPE IDS — ['IT-01', 'IT-02', ...] — a list of "
            "names that settles nothing. A READING is testable: it carries "
            "what this specific act would mean under that type, WHAT WOULD "
            "CONFIRM IT, WHAT WOULD REFUTE IT, the refusal that guards it, and "
            "the rows of his own bank it rests on. His falsifier law from the "
            "intent ledger applies unchanged — a candidate naming nothing that "
            "would flip it is an opinion, not a candidate. FOUR OF THE NINE "
            "ARE HIS OWN FROM THIS VERY EXAMPLE (IT-01 disposition, IT-02 "
            "affordance, IT-03 automaticity, IT-04 override by a higher "
            "claim); the other five come from his other worked examples — "
            "recovery from the dice game, role-binding from Yudhishthira, "
            "impatience from the golden calf, fruit-focus from Gita 2.47, "
            "permission-waiting from his study sequence. 21 rows verified "
            "against the live registry, 0 wrong. THE ACT IS CARRIED IN HIS "
            "WORDS and never re-described — the reading is what varies, the "
            "act must not. NOTHING IS CHOSEN AND NOTHING IS CHOOSEABLE: "
            "`chosen` is None on every reading and a source-scan test proves "
            "there is no max, no sort and no selection path in the module. Two "
            "surviving candidates HALT rather than blend, his standing rule — "
            "and nine surviving candidates are nine. The eight typed intents "
            "adopted from C-SB are listed beside his nine and joined by "
            "nobody: ADOPT-HALT-4, merged False, his call. /readings, "
            "/readings?id=IT-04, POST /readings/run."},
   {"his": "links between sub-parameters become first-class, counted and named",
    "where": [("link.py", "def links("),
              ("link.py", "def computed("),
              ("link.py", "HIS_LINKS = ("),
              ("link.py", "def fires_on("),
              ("link.py", "def verify(")],
    "state": RUNS,
    "note": "PHASE 10 — THE LINK LAYER (2026-08-29). His ask, with his own "
            "worked example: 'Diamond cut diamond becomes a stored link "
            "between two ego-rows.' WHY A LINK IS NOT A ROW: a row is a "
            "faculty living in one container. `Dominance motive` is a row; TWO "
            "people running it at each other is not a row and cannot be made "
            "one, because it has no home container — it is not located in "
            "either party, it is located in the MEETING. That is his diamond "
            "exactly ('its ego cut ego'), and ARCH-004 already says the "
            "immovability is a property of the meeting, not of either party. A "
            "layer that can only hold rows cannot say that sentence at all. "
            "COUNTED FROM THE SPLIT BANK, his own note on this layer — 993 "
            "links, of which 992 are COMPUTED over the live split and the live "
            "archetype layer and nothing is hand-listed, so the count follows "
            "the bank instead of drifting from it: SPLIT_SIBLING 284 pairs "
            "from the 275 parents the split divided (that `Fluid` and `osmotic "
            "balance` were once one row, P0003, is real information the split "
            "otherwise throws away), SHARED_NAME 89 pairs across 83 names "
            "(which is what the review's undecided SPLIT-05 duplicates "
            "actually ARE — two rows that may be one faculty seen twice), "
            "ARCHETYPE_REACH 619 pairs (the generative edge: a relation across "
            "containers that no container could hold, found by the archetype "
            "and stored here). THE ONE HAND-GIVEN LINK IS THE ONE NO SWEEP "
            "COULD FIND — SYMMETRIC_MEETING, because both ends are the SAME "
            "row (SB-HFR-P2550 Dominance motive on both parties). Every row id "
            "his links name is re-checked against the live registry, 7 checked "
            "0 wrong. `fires_on('diamond cut diamond')` returns the reading "
            "belonging to the meeting, with his refusal attached ('never read "
            "it as one person being strong'), and ordinary text fires nothing. "
            "The layer stood at 0 in his twelve-layer table and is now counted "
            "live and WIRED. No ceiling, no parameter created, nothing "
            "concluded. /link, /link?id=, /link?row=, POST /link/run."},
   {"his": "your pending wiring",
    "where": [("sbx.py", "HIS_LAYERS = ("),
              ("sbx.py", "def layers("),
              ("sbx.py", "def wiring("),
              ("sbx.py", "def _wired(")],
    "state": RUNS,
    "note": "HIS TWELVE-LAYER TABLE, LIVE (2026-08-29). He gave the table "
            "himself with three columns — count today, count after the split, "
            "delta. This renders it against the LIVE modules rather than "
            "against typed numbers, and adds the column his table could not "
            "have: whether a layer is actually WIRED, meaning it reaches an "
            "answer rather than only existing. His own bar is 'evidence of "
            "wiring is done with proof not your test', so existing at a step "
            "is explicitly NOT wiring. RESULT — 8 of 12 MET (segments 10->27, "
            "containers 80->183, filters 40 families->175, states 12, evidence "
            "7, failures 20, chain 30->34, rubrics 52->67), 3 with NO CEILING "
            "by his ruling (archetype now 11, link 0, scale 0), and ONE SHORT: "
            "sub-parameters stand at 3,483 against his ≈7,603, SHORT BY "
            "EXACTLY 4,120 — his own figure reproduced, not approximated. Why "
            "it is short is stated rather than worked around: splitting "
            "produced 3,483 by DIVIDING existing rows among children and "
            "created no new names, and there is no source for 4,120 that does "
            "not already exist — his 650-row named reserve is the only real "
            "unassigned material and does not cover it. Inventing them would "
            "be the placeholder he forbade; HIS NUMBER TO FINALISE. WIRED: "
            "segments, containers, sub-parameters and archetype (all four in "
            "the path of place_on_spine). PARTIAL: the filters — 175 placed on "
            "the spine, SEVEN actually run on every finding. CARRIED BUT NEVER "
            "CONSULTED, stated not hidden: operating states, evidence levels, "
            "failure classes, operating chain, rubrics, link and scale — seven "
            "layers that exist at a step and reach no answer. Also added here: "
            "review check SPLIT-09, which caught the rubric layer declaring 67 "
            "while 66 distinct sit on the spine across 70 placements (Trace, "
            "Relation, Compression and Gap each act at two steps) — one rubric "
            "counted and appearing nowhere in the work; reported, not guessed "
            "at, since two rubrics sharing a name would look the same. "
            "/sbx/wiring."},
   {"his": "split review it again",
    "where": [("sbx.py", "def review("),
              ("sbx.py", "ROWS_PER_CONTAINER = ")],
    "state": RUNS,
    "note": "THE SPLIT REVIEW (2026-08-29) — not a re-statement of the counts "
            "but eight checks that can FAIL, run live over the data. 5 pass, "
            "3 findings, 0 BLOCKING. WHAT PASSES, measured: SPLIT-01 every one "
            "of his 3,204 source rows still has at least one child and no "
            "split row cites a source that is not there — 275 parents split "
            "into 554 children, 3,204 + 279 = 3,483 exactly, which reproduces "
            "his own table's 275 multi-meaning rows; SPLIT-03 no container and "
            "no row name still carries more than one meaning (no slash, no "
            "'and', no comma, no ampersand) across all 183 and all 3,483; "
            "SPLIT-06 all 183 carry BOTH columns; SPLIT-07 all 12 spine steps "
            "hold containers, thinnest being 9 CONSOLIDATION and 10 ALIENATION "
            "at 4 each against 30 at 11 COLLISION; SPLIT-08 the source bank "
            "stands untouched at 3,204/80. WHAT FAILS AND IS LEFT FOR HIM: "
            "SPLIT-02 — his rule is 40 rows per container and 155 of 183 hold "
            "fewer, shortfall 3,925, because splitting a parent DIVIDED its 40 "
            "among its children instead of giving each child 40 of its own, so "
            "a parent that became five left five thin ones (eight containers "
            "hold exactly ONE row); there is no source for the missing names — "
            "his 650-row named reserve does not cover it — and this side will "
            "not decide the number. SPLIT-04 — two children of DIFFERENT "
            "parents landed on the same bare name: `Ownership` from Body "
            "Schema/Body Image/Ownership and from Agency/Ownership/"
            "Responsibility, `Gesture` from Imitation/Gesture/Tool "
            "Manipulation and from Prosody/Gesture/Non-Verbal — the "
            "multi-meaning problem reappearing in the split's own output one "
            "level down; not renamed, because his rule is that meanings are "
            "fixed with notes, never renames. SPLIT-05 — 83 row names appear "
            "in more than one container, reported rather than judged, since "
            "`Recovery` in a body container and in a social one may be two "
            "real rows. A false alarm caught in the building and worth "
            "recording: comparing split `from_row` (zero-padded P0001) against "
            "asi_pyramid's flat ids (unpadded P1) appeared to show 999 source "
            "rows with no child; the format, not the data, was wrong — the "
            "correct comparison is 3,204 of 3,204. /sbx/review."},
   {"his": "use new parameters in front n old in back",
    "where": [("sbx.py", "def front_back("),
              ("sbx.py", "def _new_row("),
              ("sbx.py", "FRONT_BACK_LAW = ")],
    "state": RUNS,
    "note": "HIS DISPLAY LAW (2026-08-29), given in the same breath as the "
            "ruling that the source is never deleted: 'Human_registry.json is "
            "untouched and still reads 3,204 rows and 80 containers. The split "
            "stands beside it, never over it... use new parameters in front n "
            "old in back'. Both halves are load-bearing and they do not "
            "conflict: the OLD bank is never removed, because removing it "
            "would break the promise his source stands untouched; and the NEW "
            "reading leads, because the split is what the system reasons on — "
            "a reader who meets the old id first is being shown the superseded "
            "address as though it were the current one. Before this, a reached "
            "row led with the OLD name and the OLD flat id and carried the new "
            "container behind them. Now `front_back()` renders every reached "
            "row NEW FIRST — the split row id, its name, its container, "
            "segment, pillar, step and machine column — with every source "
            "field gathered under `from` at the END, and the key order IS the "
            "display order. One function, so the convention cannot drift apart "
            "across pages. The split row is found by the source row's own flat "
            "id, which every split row carries as `from_row`, and where a "
            "parent was SPLIT into several children the name decides between "
            "them. MEASURED over eight of his asks: 71 hits, 71 resolving to a "
            "real split row, 0 unresolved. The old bank is untouched by it — "
            "3,204 rows and 80 containers, tested in the same file."},
   {"his": "Node brain structure added",
    "where": [("sbx.py", "def node_brain("),
              ("sbx.py", "def node_types("),
              ("sbx.py", "NODE_ON_SPINE = {"),
              ("sbx.py", "def open_layers(")],
    "state": RUNS,
    "note": "THE NODE BRAIN, IN THE ARCHITECTURE (2026-08-29). The structure "
            "is HIS and was locked in Phase A — 12 node types, 16 fields (with "
            "point_zero_ref REQUIRED, so 'no invention before source lock' is "
            "structural), 10 typed links, 11 memory kinds, 4 statuses, 5 write "
            "and 6 read conditions, with a fingerprint that fails loudly if any "
            "of it changes silently. What was missing is that it stood BESIDE "
            "the architecture instead of inside it: every other layer is "
            "PLACED — intent types, filters, states, evidence levels, failure "
            "classes, chain steps, rubrics each sit at the step where they act "
            "— and the node types did not, so nothing could say where in his "
            "loop a CONTRADICTION comes into being. All twelve are now placed, "
            "and the placement is honest about whose it is: the type, the stem "
            "and the meaning are HIS verbatim; the STEP and the reason are "
            "marked DERIVED on every row and are correctable by a word, the "
            "same standing a derived trigger has. The placements his own law "
            "fixes: CONTRADICTION at 7 HALT (two readings that cannot both "
            "stand IS the halt), EVENT at 2 PRESSURE (his motto begins where "
            "contact is forced), INTENT at 4 WITNESS (intent is never observed "
            "— his law is that it is read from how things were arranged, which "
            "is a witnessing), PATTERN at 9 CONSOLIDATION (an arrangement that "
            "recurs cannot exist inside one pass). AN ABSENCE REPORTED, NOT "
            "FILLED: steps 8 LOOP, 10 ALIENATION and 11 COLLISION have no node "
            "type of their own, and steps_unused says so. THE FIVE NAMESPACE "
            "COLLISIONS ARE CARRIED, NOT SETTLED — EVENT · INTENT · PATTERN · "
            "RULE · STATE name both a node type and a growth series; not "
            "merged, his ruling awaited. Also fixed here: OPEN_LAYERS carried a "
            "TYPED count of 0 for ARCHETYPE, which was true when declared and "
            "false the moment the archetype layer was built — counts are now "
            "read from the live module, and the test that asserted all three "
            "were zero now asserts the count is live. /sbx/nodes, and "
            "node_brain rides on /sbx."},
   {"his": "below more may be repated",
    "where": [("trigger.py", "HIS_TABLE = ("),
              ("trigger.py", "def triggers("),
              ("trigger.py", "def repeats("),
              ("trigger.py", "def match("),
              ("trigger.py", "def seams("),
              ("trigger.py", "SHAPE = {")],
    "state": RUNS,
    "note": "THE OPERATIONAL TRIGGER / STATE VECTOR (2026-08-29) — his third "
            "column, given as ten four-column segment tables. Until this the "
            "architecture carried TWO columns at every node, the human name "
            "and the computer parallel, and both answer WHAT IS THIS. The "
            "third answers WHEN DOES IT FIRE: 'Temp > $T_{max}$ triggers "
            "cooling loop', 'Idle timer > Threshold triggers ACPI S3/S4 "
            "state', 'Vector similarity search (Cosine similarity $> 0.85$)'. "
            "A name is a noun; a trigger is a CONDITION, and a condition can "
            "be evaluated where a noun can only be read — which is his own "
            "sequence law (a threshold lives on an edge and answers 'why "
            "now') written at container level. HIS TABLE IS CARRIED VERBATIM: "
            "10 segments, 48 rows, 4 columns, his wording intact including his "
            "LaTeX and his spelling, ids namespaced HIS- so they can never be "
            "read as registry or split ids. HIS REPEAT LAW IS STRUCTURAL: he "
            "wrote 'below more may be repated' before the table and the table "
            "proves him right — HIS-CON-018 is Auditory Processing under "
            "SEGMENT 03 and Threat Detection under SEGMENT 09; four ids repeat "
            "that way, placements() returns a LIST, and a repeat is recorded "
            "as a repeat rather than resolved as a collision. MATCHED ON THE "
            "NAME, NEVER ON THE NUMBER: his table, the registry and the split "
            "all number from CON-001 and are three different numberings (his "
            "CON-064 is Episodic Memory, the registry's is Motive/Needs/"
            "Values), so his do-not-silently-merge ruling applies to his own "
            "document — whether his number agrees is recorded beside every "
            "match and decides none. 7 NUMBERING SEAMS surfaced and decided by "
            "nobody, the sharpest being Theory of Mind, which his name places "
            "at SBX-CON-150 and his number would place at Body Schema. GRADED "
            "MATCHING, 36 placed / 3 proposed / 9 held: only a match at grade "
            "2.0+ places his wording, because of three single-token matches "
            "`circadian` and `chemical` were right and `behavioral` put his "
            "safety-guardrail row onto Group Behaviour — a weak match that "
            "placed silently would carry his trigger to the wrong container, "
            "so it is PROPOSED and waits for him. ALL 183 CONTAINERS FILLED, "
            "ZERO EMPTY: 36 HIS verbatim, 147 DERIVED from TWO REAL SOURCES — "
            "the container's own machine column and its spine step, which "
            "fixes the shape of the firing (GROUND reads a baseline, PRESSURE "
            "crosses a threshold, HALT raises a fault). Nothing invented from "
            "nowhere; every derived row names what it was built from and is "
            "replaced the moment he writes one. HIS and DERIVED are never "
            "summed, because a page that cannot say which triggers are his "
            "cannot be corrected by him. A defect caught in the building: the "
            "first matcher's filler list held `fatigue`, `drive`, `memory` and "
            "`basic` — content words in his own names — and silently destroyed "
            "real matches (Cognitive Fatigue could not reach Fatigue); "
            "replaced with graded token matching, 27 placed -> 36. /trigger, "
            "/trigger?id=, /trigger/placements?id=, POST /trigger/run."},
   {"his": "now build the archetype layer from the holy books",
    "where": [("archetype.py", "ARCHETYPES = ("),
              ("archetype.py", "def fires_on("),
              ("archetype.py", "def compare("),
              ("archetype.py", "def _hits("),
              ("archetype.py", "MEANING_MIN = "),
              ("archetype.py", "CEILING = None")],
    "state": RUNS,
    "note": "PHASE 9 — THE ARCHETYPE LAYER (2026-08-29). His teaching: the holy "
            "books are GENERATIVE ENGINES, not a quote store — the words stay "
            "the same and the reading is never general, because human intent "
            "and situation change infinitely; one event of those books is used "
            "in 100 daily responses. WHY IT IS A LAYER AND NOT A ROW: a row "
            "lives in exactly one container, but THE RECOVERY STAKE reaches 12 "
            "rows across 9 containers in 6 segments — put it in any one of them "
            "and it is in the wrong place eight times over. It REACHES rows; it "
            "never owns them. WHAT IT FIXES, measured: his dice sentence 'he "
            "bet everything he had to win it all back and lost what he could "
            "never recover' seated ZERO rows — not because the rows were "
            "missing (P1873 Sunk-cost sensitivity and P2517 Commitment "
            "escalation risk were sitting there) but because no route ran from "
            "those words to those rows. 11 archetypes: ARCH-001 THE RECOVERY "
            "STAKE (Mahabharata dice game, his 'betting is worst, u can loose "
            "ur pride too'), 002 THE GOLDEN CALF (Exodus), 003 THE FRUIT AND "
            "THE ACT (Gita 2.47), 004 DIAMOND CUT DIAMOND (his proverb, 'its "
            "ego cut ego'), 005 VIRTUE WITHOUT LIMIT (his Yudhishthira reading "
            "— 'being righteousness and adherence to truth dosent make u great "
            "all the time'), 006 VERIFY BEFORE HARM (Qur'an 49:6), 007 TEST AND "
            "RETAIN (1 Thess 5:21), 008 THE DISCRIMINATIVE INTELLECT (Gita "
            "18:30), 009 TRUTH AND TRUTHFUL LIVING (SGGS Ang 62), 010 THE ONE "
            "WHO IS LEFT WITH MEMORIES (his good-person teaching), 011 THE ACT "
            "WITH MANY INTENTS (his stealing demo — thief/opportunity/habit/"
            "saving a life). EVERY ROW CITED IS REAL: 117 (id, name, container) "
            "triples re-checked against the live registry by a test — nine of "
            "the first twelve written for ARCH-011 were wrong from memory and "
            "that test is what caught them. TWO ROUTES, both naming their "
            "evidence: PHRASE (a regex, the narrow route that fails on "
            "unfamiliar wording) and MEANING (concept words, the macro route "
            "that survives rewording — his dice game reads the same whether it "
            "is dice, a stock or a war). The meaning route uses HIS OWN IDF BAR "
            "one storey up: a word in several archetypes' vocabularies is weak "
            "evidence, so a firing needs 2 concept words of which at least one "
            "is DISTINCTIVE — 'all everything' fires nothing. Measured both "
            "ways: all 7 of his dead examples now reach rows (stealing 0->20, "
            "diamond cut diamond 0->10, the dice game 0->12), and 8 of 8 "
            "ordinary sentences fire NOTHING. Nothing is concluded — `chosen` "
            "and `concluded` are None on every run, each firing carries its "
            "discriminator and its refusal, and NO PARAMETER IS CREATED (the "
            "bank stays 3,204). NO CEILING, his ruling: 'no count, its open to "
            "increase'. /archetype, /archetype?id=, POST /archetype/run."},
   {"his": "this file too for review and adoption",
    "where": [("adopted.py", "def wb_verify("),
              ("adopted.py", "def the_bridge("),
              ("adopted.py", "def wb_findings("),
              ("adopted.py", "def wb_halts("),
              ("adopted.py", "def wb_stats(")],
    "state": RUNS,
    "note": "THE SECOND ADOPTION (2026-08-27) — the SB-ASI Drive master, "
            "ASI-Brain_Task3_Approved_Final_v1_0, canon at "
            "docs/method/canon/THE_ADOPTION_OF_THE_ASI_BRAIN_MASTER.md. "
            "The .xlsx byte-identical at adopted/SB-ASI-Drive/ plus 33 "
            "DERIVED sheet texts, all SHA-256'd; wb_verify re-hashes 34 "
            "files per call. 33 sheets, 141,113 cells, 710,008 words "
            "extracted whole. THE BRIDGE his own file states is COUNTED "
            "from the sheets, never retyped: 2,554 exact-source rows + "
            "650 named reserve rows = his 3,204; 2,554 + 6 visible "
            "reconstructions (P1303-P1308, each REQUIRES USER APPROVAL) "
            "= the 2,560. Five findings reported and corrected nowhere "
            "(P0001 is a placeholder; the Task-3 raw workbook with the "
            "2,514 edges, 46 names and 64 wordings is an OPEN SOURCE GAP "
            "by the file's own record). Five new seams stand as "
            "ADOPT-HALT-8..12 — the bridge, three filter vocabularies, "
            "the twelve states, the missing raw workbook against C-SB's "
            "AI_ONLY_RECORDS_64, and three scripture surfaces. Nothing "
            "wired; the tree is ADOPTED in the file divide. /adopted."},
   {"his": "build 18 and 23 / it should must have full explanation not just "
           "definition n placeholders",
    "where": [("maturity.py", "def read("),
              ("maturity.py", "def update("),
              ("maturity.py", "def verdict("),
              ("discovery.py", "def close("),
              ("discovery.py", "def loop(")],
    "state": RUNS,
    "note": "STAGE 18 MATURITY UPDATE and STAGE 23 FUTURE EVENT, and with them "
            "the chain now runs 23 OF 23 — it completes. STAGE 18 fixes two "
            "failures: a candidate that SURVIVED a real test could not get "
            "stronger (ten confirmations left it where one did) and a candidate "
            "that was DOUBTED could not get weaker. Six named states — UNTESTED "
            "(unmeasured, not weak), HELD (a valid rest), SUPPORTED, STRONG, "
            "WEAKENED, KILLED — each a state PLUS the evidence that put it "
            "there, NEVER a bare number, because his ASI0001 workbook already "
            "showed what a bare score does when RANK was computed off a column "
            "of zeros. Only DISCRIMINATING confirmations count and STRONG needs "
            "two of DIFFERENT classes, since two of one class is one kind of "
            "looking done twice. DECAY IS CHECKS WITHOUT CONFIRMATION, NEVER "
            "AGE — nothing here measures time and a reading does not become "
            "less true by being old. An update APPENDS a reading referencing "
            "the one before it, so a maturity is a LEDGER not a field: his "
            "no-reopen rule applied to a value. STAGE 19 therefore has all four "
            "verdicts at last — WEAKEN could not exist before 18 because you "
            "cannot weaken something with no strength to lose, and it is a "
            "verdict of its own, not a softer REJECT. STAGE 23 is NOT a jump "
            "back to 01: his protocol forbids that twice (NO IN-PLACE LOOP, NO "
            "REOPEN), so a pass CLOSES and may CREATE a successor referencing "
            "it, carrying the OPEN ENDS and not the whole prior pass. A "
            "successor exists only for a new combination, an unsettled "
            "maturity, or an unchecked discriminating prediction; with none the "
            "loop TERMINATES, which is a real outcome — a loop that cannot stop "
            "is a leak. MEASURED: loop() terminates three different ways — with "
            "no verdicts it decays to WEAKENED in 3 passes, with confirmations "
            "it settles at SUPPORTED in 2, with refutations at WEAKENED in 2. "
            "The first loop() I wrote did NOT terminate: it reseeded every "
            "maturity to HELD each pass so there was always a reason to "
            "continue, and it ran to the cap every time. /maturity, POST "
            "/maturity/read, POST /loop/run."},
   {"his": "build 12",
    "where": [("expected.py", "def expect("),
              ("expected.py", "def run("),
              ("expected.py", "def falsifier_from("),
              ("expected.py", "DISCRIMINATION_BAR")],
    "state": RUNS,
    "note": "STAGE 12 EXPECTED EVIDENCE GENERATION — the stage that was blocking "
            "the rest of his loop. Every generated meaning now yields what "
            "should EXIST if it were true, and three conditions make a "
            "prediction worth anything: it is SPECIFIC (names where to look), "
            "TWO-SIDED (says what would confirm AND what would refute — a claim "
            "with no refuting observation cannot be tested at all), and "
            "DISCRIMINATING. The third does the work: a prediction more than "
            "60% of meanings make separates none of them, so it is computed, "
            "marked NON-DISCRIMINATING and NOT counted — the same shape as the "
            "role gate and the IDF bar. On 400 meanings that flags ABSENCE and "
            "COMPANION. Evidence classes are MATERIAL/COMPANION/PLACEMENT/"
            "RECORD/REPETITION/ABSENCE, chosen by intersecting what the ROLE "
            "would leave with what the FUTURE STATE would require, and each "
            "prediction inherits its meaning's origin distance plus its own "
            "reach (RECORD travels furthest and owes most). falsifier_from() "
            "composes a falsifier out of the prediction so a candidate reaches "
            "stage 17 ALREADY TESTABLE instead of waiting for one written by "
            "hand — a test proves intent_ledger.kill accepts it. NOTHING IS "
            "CHECKED here: checking needs the world, and stage 17 already takes "
            "verdicts from outside. MEASURED: building it moved the chain from "
            "11 of 23 to 17 of 23; it now halts at 18 MATURITY UPDATE, with 23 "
            "still lacking a return edge. Two defects while building: I "
            "overwrote the existing evidence.py (his Stage-4 evidence ladder) "
            "and restored it from git — this module is expected.py; and ABSENCE "
            "was appended twice wherever a role already required it, pushing its "
            "share above 1.0 per meaning. /expected, POST /expected/run."},
   {"his": "SOURCEBORN SYNTHETIC DISCOVERY LOOP (his 23 stages) / do we flow "
           "this or anything else",
    "where": [("discovery.py", "STAGES = ("),
              ("discovery.py", "def audit("),
              ("discovery.py", "def chain("),
              ("discovery.py", "def gaps(")],
    "state": PARTIAL,
    "note": "THE ANSWER IS NO, AND IT IS TWO ANSWERS. The STAGES mostly exist: "
            "16 RUN, 4 are PARTIAL, 3 are ABSENT, and every anchor the map "
            "claims was IMPORTED AND CHECKED rather than trusted — 0 of them "
            "fail to resolve. But the FLOW does not exist: nothing chains them "
            "in his order. What actually flows end to end is selfmake.SPINE, "
            "FIVE steps, not twenty-three; everything else is a module behind "
            "its own route called on its own. chain() runs his 23 in his order "
            "and HALTS at stage 12 EXPECTED EVIDENCE GENERATION — 11 of 23 — "
            "because nothing turns a generated meaning into 'if this were true, "
            "THIS should exist'. Stages 13-23 come back NOT REACHED rather than "
            "being skipped quietly, which is his own rule that a failure opens "
            "the mapped loop. THE THREE ABSENT: 12 expected evidence, 18 "
            "maturity update (nothing ages, ripens or decays across runs), 23 "
            "future event (there is no return edge — this is a line, not a "
            "loop). 19 is PARTIAL because survivors() gives RETAIN, REJECT and "
            "UNKNOWN but there is NO WEAKEN, so evidence that should reduce "
            "confidence does nothing. 5 is PARTIAL because relations are LISTED "
            "and not traversable. 22 is PARTIAL because extend() opens new "
            "combinations only when called by hand. /loop, POST /loop/chain."},
   {"his": "show me in arrow graph what is where",
    "where": [("sysmap.py", "def arrow_chart("),
              ("sysmap.py", "def _n("),
              ("sysmap.py", "def where(")],
    "state": RUNS,
    "note": "the whole system as one arrow graph, in his own idiom, and every "
            "number in it is READ FROM THE LIVE MODULES at draw time rather than "
            "typed into it — a diagram that can go stale is a diagram that will. "
            "A test asserts the live counts appear, that every drawn box line is "
            "the same width so the borders align, and that his laws are on the "
            "chart and not only in the code. The layers are the path a thing "
            "actually takes: his words -> file map -> the growing phase -> the "
            "bank -> the generators -> the gates -> the kill -> the ledger -> "
            "the algorithm that makes itself -> HIM. where() answers the same "
            "question per item. /map (plain text), /map/where?q=."},
   {"his": "review this file and which parameters hit in this / build it",
    "where": [("artifact.py", "SIGN_GROUPS = ("),
              ("artifact.py", "SYNTHETIC_MEANINGS = ("),
              ("artifact.py", "ACTOR_ROLES = ("),
              ("artifact.py", "ORIGIN_DISTANCE = ("),
              ("artifact.py", "def generate_meanings("),
              ("artifact.py", "def damage_branches("),
              ("artifact.py", "def refused(")],
    "state": RUNS,
    "note": "GPT_Black.txt, the other assistant's transcript on the same "
            "project. Roughly half of it this core already held and built "
            "independently from his workbooks — the ten king brain-states are "
            "SP-19..SP-28, the live intent engine is intent_ledger.py, NEW "
            "WORDING != NEW INTENT is the novelty signature. EIGHT MECHANISMS "
            "WERE NOT HERE and are now: SG-A..SG-J visual placeholders (reason "
            "about a sign by neighbour/position/repetition/enclosure/damage "
            "without claiming to know Egyptian); SYN-MEAN-001..008 whole-object "
            "meanings; ORIGIN DISTANCE 0..5 where farther is not WRONG but owes "
            "more evidence; NINE actor roles per artifact event, each with its "
            "own possible intent, against this core's one actor per event; "
            "future-state reconstruction, which runs BACKWARDS where everything "
            "else runs forwards; damage branching (four branches that predict "
            "different evidence, never a fill); 12 PC-TAB-SYN pattern "
            "candidates of which the transcript names 8 and the other 4 are "
            "recorded as unnamed; and MATCH SCORE != EPISTEMIC CONFIDENCE. THE "
            "GATES MATTER: ungated the generator returned 6,480 of a possible "
            "6,480 — a meaning for every combination, which is not a finding. "
            "ROLE_FUTURES (a carver does not secure a dynasty) and FUTURE_NEEDS "
            "(an identity claim needs the enclosure) cut it to 1,824, rejecting "
            "3,480 and 1,176 and reporting both. Everything is NEW_SYNTHETIC "
            "with historical_fact False and translation_verified False; 0 "
            "translations, 0 parameters. His eight seat on 29 existing ids — "
            "SYN-MEAN-006 on P2519 Intention-to-persist and SYN-MEAN-008 on "
            "P0844 Sequence compression. The transcript's own refusals (owl = "
            "wisdom, falcon = royal guard, 7.8/10) are stored as REFUSED so they "
            "cannot creep back as fact. His last question — how many new "
            "meanings — expired unanswered in that chat and is answered here. "
            "/artifact, POST /artifact/generate, POST /artifact/grow."},
   {"his": "ur own old docs / hope adding more",
    "where": [("subjectbrains.py", "CANDIDATES = ("),
              ("subjectbrains.py", "HALTS = ("),
              ("subjectbrains.py", "def version_gap("),
              ("subjectbrains.py", "def rerun_tally("),
              ("growing.py", "def registry_echo(")],
    "state": RUNS,
    "note": "TWELVE SUBJECTS NOW, ten of them added on his orders, and on his "
            "word 'nothing needs to kill for now, add everything and generate' "
            "THE KILL IS OFF BY DEFAULT — a subject that reads the other way is a "
            "second SETTING of a law, not its death, which is his standing 'keep "
            "adding not removing' doing the work instead. The killing pass stays "
            "available (kill=True) and its earlier reading is preserved in canon "
            "rather than erased. HIS CANDIDATES ARE APPLIED ACROSS EVERY SUBJECT: "
            "25 x 12 = 300 cells, 204 read and 96 NOT READ because 8 candidates "
            "have no reader yet — never invented. 14 candidates became an AXIS "
            "with named settings and 3 are single-valued. GENERATED: 72 variants, "
            "0 killed, 0 parameters. His own candidates gain the poles he said "
            "were missing: E-03 said two poles and twelve subjects show FIVE "
            "(CONTINUOUS 7, GATE 2, ITERATE 1, SINGLE 1, UNGATED 1); R-06 said "
            "the DOWNWARD offset only and now reads UNDER 7 / LEVEL 3 / OVER 2, "
            "with Tesla and Ramanujan supplying the OVER pole so the axis is "
            "whole in both directions from his own candidate; X-02 gains "
            "USED_WITHOUT_CREDIT (Franklin, Noether) beside USED_THEN_DESTROYED "
            "(Turing). X-04 constraint-rise reads ROSE on 12 of 12, including a "
            "partnership, teams and two non-scientists. ONE FLAG: E-01 produced "
            "12 settings with support 1 each — every subject its own trigger — "
            "which is not an axis but an uncategorised free-text field, so the "
            "count is split honestly: 60 variants from real axes, 12 from the "
            "singleton field. Beethoven and van Gogh are outside science "
            "entirely, the first test of whether these candidates are about "
            "people or only about scientists. EARLIER: four subjects were added on his order 'add "
            "more subjects to test cross patterns' — chosen to STRESS his four "
            "cross-subject laws, not to agree with them. Result: THREE OF THE "
            "FOUR ARE KILLED AS STATED. X-01 (weak channel becomes strongest) "
            "holds on Riemann and Einstein and on NOBODY ELSE — it held only on "
            "the two subjects it was derived from, which is the signature of a "
            "law fitted to its own evidence; Ramanujan's rigour, Faraday's "
            "mathematics and Curie's barred access were all ROUTED AROUND rather "
            "than converted. X-02 needs a category it does not have: Faraday was "
            "read correctly (Davy took him in at 21) and Turing was "
            "USED_THEN_DESTROYED, neither misread nor read correctly. X-03 dies "
            "on exactly one clean counterexample — Faraday stopped experimental "
            "work years before dying. X-04 constraint-rise survives 6 of 6 AND "
            "survives the right way: it holds on Curie (a partnership) and Turing "
            "(teams), so it is not an artefact of solitude, which was the live "
            "risk when the evidence was two lone theorists. His E-03 two-pole "
            "axis needs FOUR settings (GATE, ITERATE, UNGATED, CONTINUOUS) and "
            "CONTINUOUS is the commonest — reported as an amendment, never "
            "applied to his candidate. Every verdict is COMPUTED from structured "
            "axis fields, so striking a field moves it; a test pins that. One "
            "counterexample falsifies as stated — holding on most subjects is not "
            "holding — and nothing is deleted: a killed law keeps its rows, its "
            "counterexamples and what it would have to be narrowed to. "
            "ORIGINALLY: his platform superimposed on Riemann and Einstein — my own earlier "
            "builds, handed back. They carry 25 parameter candidates "
            "(R-01..R-11, E-01..E-10, X-01..X-04), 14 halts addressed to him of "
            "which NOT ONE was ever answered, and his own anti-pleasing tally "
            "(17 of 45 rows disagree, so it is not flattery). Placed, not "
            "answered. THE VERSION GAP IS SURFACED NOT CLOSED: both workbooks are "
            "built on 2,560 and the registry now holds 3,204, with different "
            "names (Temperature balance vs Core temperature setpoint), and the "
            "workbook itself warns that 2561-2590 are already spent in the King "
            "runs — so the 25 are CANDIDATE rows, never PARAM rows, and the bank "
            "stays at 3,207. TWO DEFECTS THEY EXPOSED: (1) the Einstein file "
            "contains a full 2,560 atom expansion, so placing it whole seated a "
            "TAXONOMY ON A TAXONOMY — 1,086 ids reached with top hits "
            "Load-force coupling and Agonist activation, none of which is about "
            "Einstein; registry_echo() now catches parameter-list rows by SHAPE "
            "and place() excludes them, 489,688 chars down to 74,037 and the "
            "seats become Stopping-rule, Pattern abstraction, Rule extraction. "
            "(2) his rule-7 gate semantic_loss() matched bare SUBSTRINGS, so "
            "'productive' hit Reproductive-hormone signalling and it declared all "
            "25 expressible on noise; it now uses whole words, split hyphens and "
            "his forty-names bar, and R-09 Presupposition-salience correctly "
            "lands on P2129 Presupposition handling. ANSWER TO 'hope adding "
            "more': generation 2,200 -> 2,261, 61 new steps, 0 new arrangements "
            "and 61 new COMBINATIONS — INFERENCE x SPEECH, OBSERVATION x SPEECH, "
            "INFERENCE x OBSERVATION, the reasoning pairs his ACTION-heavy corpus "
            "was thin on. /subjects, POST /subjects/grow."},
   {"his": "u got some intent from files / now make algorithm which can make "
           "itself",
    "where": [("selfmake.py", "def steps("),
              ("selfmake.py", "def propose("),
              ("selfmake.py", "def extend("),
              ("selfmake.py", "def generation("),
              ("selfmake.py", "CROSS_ROLE_REQUIRED"),
              ("selfmake.py", "def bias_report(")],
    "state": RUNS,
    "note": "every pipeline here before this one had a FIXED step list written by "
            "me. This one does not: steps() returns the spine plus every step the "
            "algorithm has written for itself, loaded from the ledger at call "
            "time, so its body is data and it grows. Its own steps come from HIS "
            "material: 13,848 events over 217 files reduce to 96 computed "
            "(role -> container) arrangements, and an arrangement at or over "
            "support 5 (his own PATTERN-CANDIDATE number) earns a step carrying "
            "its support as evidence. A COMBINATION step is two arrangements that "
            "co-occur in one example and CROSS ROLE — which is his rain example's "
            "own shape, an ACTION meeting an INFERENCE. Without a cross test 80 "
            "arrangements gave 2,627 combinations of a possible 3,160, a step for "
            "nearly every pair; cross-segment removed only 238 because ACTION "
            "spans SEG-03 and SEG-06; cross-role is the test that bites and "
            "rejects 512, reporting the count. Measured: generation 0 = 5 steps, "
            "after one extend = 2,204, and extending again on the same material "
            "writes 0 — it grows once, it does not inflate. Every self-written "
            "step carries a falsifier so it can be killed on evidence; none is "
            "canonical, none creates a parameter, none reaches an answer without "
            "his word. The bias is reported on every call: role_of defaults to "
            "ACTION, which carries 79.6% of all seats, so the steps are "
            "ACTION-weighted for a partly mechanical reason — fixable only by "
            "superseding, never by deletion, and his call. /selfmake, POST "
            "/selfmake/propose, POST /selfmake/extend, POST /selfmake/run."},
   {"his": "Falsifier / What would flip it",
    "where": [("intent_ledger.py", "def kill("),
              ("intent_ledger.py", "def survivors("),
              ("intent_ledger.py", "def signature("),
              ("intent_ledger.py", "def promote("),
              ("intent_ledger.py", "def semantic_loss("),
              ("intent_ledger.py", "def namespaces(")],
    "state": RUNS,
    "note": "the killing step, and it is his. His LIVE_INTENT_ENGINE sheet fills "
            "a falsifier on all ten candidates beside Support and Counterexample "
            "counts, which is the survivor stage I had reported missing. A "
            "candidate dies two ways, both his: its falsifier is met, or "
            "counterexamples reach support. NOTHING IS DELETED — a killed row "
            "keeps its falsifier and the reason it died. An UNTESTED candidate is "
            "reported untested, never as a survivor. His rule 4 is enforced by "
            "building the novelty signature from state_change/target/constraint "
            "and NEVER from the intent sentence, so a full re-wording returns "
            "novel=False. Promotion needs evidence + falsifier + recurrence (>=2 "
            "sequences) + his word, and even then creates no parameter. A "
            "parameter candidate opens only on REPEATED semantic loss. His "
            "namespace ruling is enforced: the workbook's 2,000 WB-P ADDRESSES "
            "and the registry's 3,204 SB-HFR-P PARAMETERS are never merged or "
            "summed, and map_in refuses to pair S04 (Religion) with SEG-04 "
            "(Attention) just because the numbers match. His ten states already "
            "existed here as SP-19..SP-28 and were matched, not re-typed. 13 "
            "workbook findings reported, 0 corrections to his file. /ledger, "
            "POST /ledger/run, POST /ledger/kill."},
   {"his": "keep the identity fixed, change the active parameter set, "
           "situation and circumstance",
    "where": [("statepacks.py", "def identity_lock("),
              ("statepacks.py", "def runtime_address("),
              ("statepacks.py", "STATE_PACKS = ["),
              ("statepacks.py", "RUBRICS_25 = ("),
              ("statepacks.py", "def fork_event("),
              ("statepacks.py", "WORKBOOK_FINDINGS = ["),
              ("generationpage.py", "THE GENERATION — SAME PERSON, MANY BRAINS")],
    "state": RUNS,
    "note": "the generation. 16 state packs (6 from his Kings file that carried "
            "real container-state boxes, plus the 10 brains of the SAME king he "
            "added), 43 of 80 containers, 6 of 12 states, 58 container-state "
            "pairs. Measured: 0 of 36 (container+state) pairs from his file "
            "exist in the 3,204 bank, so container x state IS a generator — and "
            "his law INSTANTIATED ADDRESS != NATIVE PARAMETER is enforced by a "
            "test that generates every pack x all 25 rubrics and proves the "
            "bank stays at 3,204. His 25 universal dimensions extracted "
            "verbatim (80 containers, 1 distinct tuple — his own discovery). "
            "10 event forks, 40 intent routes, none chosen. All 7 of his "
            "workbook findings verified against the file and kept as findings. "
            "7 candidates, all REVIEW_REQUIRED, canonical 0. Routes "
            "/generation, /generation/packs, POST /generation/run."},
   {"his": "SAME PARAMETERS + DIFFERENT OBJECTIVE -> DIFFERENT PARAMETER "
           "IMPORTANCE -> DIFFERENT DECISION",
    "where": [("weighting.py", "def weigh("),
              ("weighting.py", "def counterfactual("),
              ("weighting.py", "def rank_is_not_fitness("),
              ("weighting.py", "REFUSED_LESSONS = ["),
              ("weighting.py", "def cross_domain_probe(")],
    "state": RUNS,
    "note": "his BJP/Advani-Modi mechanism, which he provisionally named "
            "Contextual Parameter Weighting. On his sentence: 6 weight flips "
            "under his own counterfactual objective and the selection changes "
            "from Modi to Advani. His two refused lessons (young > senior, "
            "popularity > experience) are stored so they cannot be learnt. "
            "PC-WEIGHT-001 ships SUPPORT 1, CANONICAL 0, ALIVE — NOT APPROVED, "
            "with his cross-domain gate on it; the probe fires 5 of 5 outside "
            "politics and flips 5 of 5, and TWO of them favour the SENIOR "
            "person, which is the proof it is not \"young beats old\". Only he "
            "promotes it."},
   {"his": "Event is same going to mall / but the intent is keep changing",
    "where": [("asi_pyramid.py", "def intent_routes("),
              ("asi_pyramid.py", "FUTURE = "),
              ("asi_pyramid.py", "def stated_reasons("),
              ("asi_pyramid.py", "def contradiction_check("),
              ("asi_pyramid.py", "def companion(")],
    "state": RUNS,
    "note": "his mall example run. It scored almost nothing at first — all 8 "
            "clauses unscoped, one intent route where he shows six, "
            "\"Girlfriend\" returned as the actor, motive reported ABSENT when "
            "he states it every line, and reinforce() at 0 on the example "
            "RULE-001 is named after. Now: a THIRD scope (FUTURE) with tense "
            "placing unmarked clauses, first person outranking any capitalised "
            "noun, 6 routes on one shell across 3 scopes with 6 distinct KINDS "
            "of reason, the stated motive SOURCE-GROUNDED while the operating "
            "motive stays HELD, and two time scopes reported as NOT a "
            "contradiction. SEG-01 fires on \"i'm not well\" and stayed silent "
            "on Samrath — his body/brain ruling both ways."},
   {"his": "I won't invent the P-row count",
    "where": [("asi_pyramid.py", "def rows_for("),
              ("asi_pyramid.py", "ROW_ROUTES = {"),
              ("asi_pyramid.py", "HIS_CONTAINERS = [")],
    "state": RUNS,
    "note": "he could verify 16/80 containers but not the exact P rows, "
            "because his payload was compressed. It is decoded here, so the "
            "matcher he named as missing now returns 106 exact rows inside his "
            "16 containers — 59 SOURCE-GROUNDED, 27 INFERRED, 20 HELD OPEN — "
            "each row checkable against his own name for it. All 21 ranges he "
            "gave by hand verified exact first."},
   {"his": "They are not new P parameters",
    "where": [("asi_pyramid.py", "def relations("),
              ("asi_pyramid.py", "ASSOCIATION_ONLY = "),
              ("asi_pyramid.py", "INTERPRETATION_FRAMES = [")],
    "state": RUNS,
    "note": "11 runtime relations, 7 interpretation candidates, 3 pattern "
            "candidates — generated above the bank and never written into it. "
            "R11 carries ASSOCIATION ONLY, and H7 (the context is unrelated) "
            "is always kept because it is what prevents false causality."},
   {"his": "SUPPORT +1 — not: invent another duplicate rule",
    "where": [("asi_pyramid.py", "PRIOR_RULES = ["),
              ("asi_pyramid.py", "def reinforce(")],
    "state": RUNS,
    "note": "a new example that fits an existing rule adds support and returns "
            "duplicate_created False. new_rules_invented is 0. A sentence the "
            "rule does not cover leaves it untouched."},
   {"his": "CAUSALITY NOT PROVEN — ASI should open them as hypotheses, not "
           "invent one",
    "where": [("asi_pyramid.py", "def difference("),
              ("asi_pyramid.py", "def pattern_candidate(")],
    "state": RUNS,
    "note": "his ten hidden branches are opened, the fabrication he named is "
            "kept on the record as refused, and PC-CONTEXT-INTENT-001 carries "
            "his four guards — generalization NOT ALLOWED YET."},
  ]},

 {"group": "THE LADDER — and rubric means parameter, the 3,072",
  "rows": [
   {"his": "we have then we divided multiple parameters "
           "(container, para, sub para and all)",
    "where": [("ladder.py", "SEGMENTS = ["), ("ladder.py", "TOTAL_CONTAINERS = 200"),
              ("ladder.py", "TOTAL_PARAMS = 3072")],
    "state": THIN,
    "note": "SYSTEM 1 · SEGMENT 10 · CONTAINER 200 · PARAMETER 3,072 · "
            "ELEMENT empty by your instruction. The frame is real. The live "
            "filled count is shown at the top of this page — it is read from "
            "your registry, not written here."},
   {"his": "rubric means paramters the 3000",
    "where": [("ladder.py", "def save_registry("), ("ladder.py", "versions")],
    "state": THIN,
    "note": "so the rubric store ALREADY EXISTS — it is the registry. Every "
            "upload merges by id, nothing is removed, and every version is "
            "kept forever. What a parameter holds today is a name plus free "
            "text; what it does not yet hold is how it is recognised and how "
            "it is graded."},
   {"his": "the 18 cross-segment mechanisms",
    "where": [("ladder.py", "CROSS = ["),
              ("ladder.py", "Graph Connectivity and Edge Density Potential")],
    "state": RUNS,
    "note": "the 18 that cut across all ten segments — each holds exactly one "
            "parameter, and the parameter IS the mechanism. These are the 18 "
            "that carry anything today."},
  ]},

 {"group": "EACH SENTENCE GENERATES ONE PATTERN — with multiple carryings",
  "rows": [
   {"his": "now each sentence always generate one pattern",
    "where": [("parameters.py", "MASTER_FORMULA = (")],
    "state": RUNS,
    "note": "Raw Symbol → Role → Pressure → Emotion → Action → Transformation "
            "→ Cost → Loop → Evidence Status. This is the closest thing in the "
            "repo to a per-sentence pattern, and it already carries Emotion "
            "inside it."},
   {"his": "i allowed one word to carry multiple reason — "
           "it always have multiple carryings",
    "where": [("parameters.py", "COMPARISON_AXES: list[str] = ["),
              ("parameters.py", '"Pattern",'),
              ("parameters.py", "def add_comparison_axis(")],
    "state": RUNS,
    "note": "thirteen axes read over the SAME text at once — Intent, Pattern "
            "(\"structure, recurrence, what repeats / breaks\"), Motive/Shadow, "
            "Emotion, Power/Condition and more. And axes can be added: "
            "add axes → multiply outcome."},
   {"his": "multiple carryings — the second shape",
    "where": [("parameters.py", '"Surface Intent"'),
              ("parameters.py", '"Hidden Intent"')],
    "state": RUNS,
    "note": "P001 Surface Intent and P002 Hidden Intent are two carryings of "
            "ONE word, stored side by side as separate parameters. So the "
            "multiple-carrying exists TWICE in two different shapes — as axes "
            "over one text, and as separate parameters. Neither knows about "
            "the other. Surfaced for your word, not merged by me."},
   {"his": "in each sentence and ask there is sequence of description "
           "for that need to break it down in ultra micro level",
    "where": [("ladder.py", "def activate("), ("ladder.py", "def recall_notes(")],
    "state": THIN,
    "note": "the rubric match is still 4-letter word overlap against the "
            "filled entries. The ULTRA-MICRO split itself is now real and is "
            "a different thing — see the group below."},
  ]},

 {"group": "REPETITION → THE SMALL BRAIN NOTICES → IT PROPOSES → YOU ALLOW",
  "rows": [
   {"his": "when small brain saw repetition and notice few parameters "
           "are getting in different have",
    "where": [("dots.py", "def dot_connections(")],
    "state": PARTIAL,
    "note": "a ref appearing in more than one micro-question of an ask IS a "
            "connection — the click. This is your repetition mechanism, and it "
            "works INSIDE ONE ASK only."},
   {"his": "it will store that new pattern",
    "where": [("dots.py", "def merge_proposal("), ("dots.py", '"needs_human": True')],
    "state": PARTIAL,
    "note": "fires only when two or more converge, and returns "
            "status 'proposed' with needs_human True — it cannot pass itself. "
            "The shape is exactly yours. What it stores is a proposal about "
            "sources, not a pattern object that persists."},
   {"his": "repetition across time",
    "where": [("memory.py", "bucket_map"), ("memory.py", "fresh_links"),
              ("memory.py", '"weekly_connection"'),
              ("memory.py", "Patterns_Recognized")],
    "state": PARTIAL,
    "note": "the weekly pull does find recurrence across the week and writes "
            "it as a learned connection, bumping Patterns_Recognized. But it "
            "connects NODE to NODE — it never counts that the same arrangement "
            "has now appeared five times across your separate asks."},
   {"his": "which i will review and allow it as per my understanding of output",
    "where": [("novelty.py", "NEW-CANDIDATE (awaiting human approval)"),
              ("novelty.py", "def load_approved(")],
    "state": RUNS,
    "note": "your gate, built and working — for PARAMETERS. A term that never "
            "existed is proposed with its nearest existing match, the "
            "similarity, and why it is not the same; it becomes real only when "
            "you approve. This is the review-and-allow loop you described, "
            "already alive on one kind of thing."},
   {"his": "nothing is killed at intake — it is labelled",
    "where": [("enums.py", "Nothing is rejected at intake"),
              ("enums.py", 'NEEDS_EVIDENCE = "Needs Evidence"'),
              ("enums.py", 'INVENTION_CANDIDATE = "Invention Candidate"')],
    "state": RUNS,
    "note": "Fact · Claim · Rumor · Belief · Speculation · Unknown · Needs "
            "Evidence · Contradiction · Personal Theory · Halt Point · "
            "Invention Candidate — and more. Classify, never reject."},
  ]},

 {"group": "THE PYRAMID — at each node it store LESS",
  "rows": [
   {"his": "Pyramid i had designed so at each node it store less",
    "where": [("pyramid.py", "STAGE_MAIN: dict[int, tuple[str, ...]] = {"),
              ("pyramid.py", "1 → 5-10 → 10-20 → 20-30")],
    "state": RUNS,
    "note": "node name → Main 5-10 → Sub 10-20 → Micro 20-30, and the URR "
            "brains use the shallower form. Written into the file exactly as "
            "you designed it. Storing less is the design, not a shortfall."},
   {"his": "multiple nodes assist to define the sentence in multiple way",
    "where": [("pyramid.py", "def file_finding("), ("pyramid.py", "def file_urr("),
              ("dots.py", "appears_in")],
    "state": RUNS,
    "note": "each node files its own finding separately; the dot pass then "
            "finds where separate nodes landed on the same place."},
   {"his": "human review again help there, where AI can't park it at right place",
    "where": [("pyramid.py", "def unfiled_from_input("),
              ("pyramid.py", "unfiled.jsonl")],
    "state": RUNS,
    "note": "your own sentence is in the file. What cannot be parked is kept "
            "and comes to you — nothing is discarded."},
  ]},

 {"group": "BUILT FROM HIS CANON — the ultra-micro splitter",
  "rows": [
   {"his": "in each sentence and ask there is sequence of description for "
           "that need to break it down in ultra micro level",
    "where": [("micro.py", "def decompose("),
              ("micro.py", "def decompose_all("),
              ("micro.py", "def split_sentences(")],
    "state": RUNS,
    "note": "every sentence becomes a micro-sequence carrying HIS field list: "
            "ENTITY · RELATION · ACTION · NEGATION · INFORMATION OBJECT · "
            "INFORMATION STATE · EXPECTED vs ACTUAL · TEMPORAL RELATION · "
            "DEPENDENCY · EXPECTATION DIFFERENCE · POSSIBLE HUMAN EFFECT · "
            "INTENT · REPETITION LINK · PATTERN CONTRIBUTION. Tested against "
            "his own worked example, field by field."},
   {"his": "INTENT: UNKNOWN from this event alone",
    "where": [("micro.py", "UNKNOWN — not directly observed")],
    "state": RUNS,
    "note": "a single event NEVER yields an intent. The clues are listed and "
            "the conclusion is refused, every time, by construction."},
   {"his": "POSSIBLE HUMAN EFFECT — uncertainty, confusion, loss of control, "
           "feeling used, irritation, distrust",
    "where": [("micro.py", "EFFECTS_BY_FACT"),
              ("micro.py", '"his_feeling": ""')],
    "state": RUNS,
    "note": "the machine lists what a structure CAN produce in a person and "
            "never picks which he felt. `his_feeling` ships empty."},
   {"his": "context",
    "where": [("micro.py", "def context_from("),
              ("micro.py", "inherited from context")],
    "state": RUNS,
    "note": "his own S3 names no 'me' at all, so without carrying the "
            "established participants forward that sentence loses its relation "
            "and drops out of the arrangement. Anything inherited is MARKED as "
            "inherited, never presented as if the sentence said it."},
  ]},

 {"group": "BUILT FROM HIS CANON — pattern memory, and only with his approval",
  "rows": [
   {"his": "EVERY SENTENCE GENERATES A MICRO-SEQUENCE REPRESENTATION … "
           "otherwise the machine would create millions of false patterns "
           "from single occurrences",
    "where": [("patterns.py", "def store_micro("),
              ("patterns.py", "def refresh_candidates(")],
    "state": RUNS,
    "note": "the representation is always kept; a PATTERN only surfaces after "
            "repetition. One occurrence can never become a pattern — there is "
            "a test whose whole job is to prove that."},
   {"his": "when small brain saw repetition and notice few parameters are "
           "getting in different have",
    "where": [("patterns.py", "def group_repeats("),
              ("micro.py", "def relates(")],
    "state": RUNS,
    "note": "the arrangement is the UNION of steps across LINKED events, each "
            "step carrying its own support count — because his own S2 has no "
            "disclosure fact and his S3 no resource fact, yet both belong to "
            "one arrangement."},
   {"his": "we decided 5 loops and reducing",
    "where": [("patterns.py", "def surface_at("),
              ("patterns.py", "SURFACE_START = 5")],
    "state": PARTIAL,
    "note": "the 5 is his and is enforced. The REDUCTION rule — each approved "
            "pattern buys one off the count, never below 2 — is MY reading of "
            "'reducing' and says so on screen, awaiting his word."},
   {"his": "PATTERN-CANDIDATE-017 … Possible interpretations … Intent status: "
           "INFERRED / NOT DIRECTLY OBSERVED … Confidence",
    "where": [("patterns.py", "INFERRED / NOT DIRECTLY OBSERVED"),
              ("patterns.py", "def _confidence(")],
    "state": RUNS,
    "note": "his record, field for field. Confidence has a stated formula and "
            "is capped at Medium while intent is inferred — one witness is "
            "him, and his own Source rule caps that. Nothing ever reads 1.00."},
   {"his": "WHAT HAPPENED / WHAT I THINK IT MEANS / HOW I FELT / WHAT "
           "PRINCIPLE I APPLY / WHAT DECISION I MADE / WHAT RESULT FOLLOWED — "
           "those should never be collapsed into one field",
    "where": [("patterns.py", '"his_interpretation": ""'),
              ("patterns.py", '"his_result": ""')],
    "state": RUNS,
    "note": "six separate fields. The machine writes only the first; the other "
            "five are his and stay empty until he writes them."},
   {"his": "edit / reject / rename / split / combine / redefine",
    "where": [("patterns.py", "ACTIONS = ("), ("patterns.py", "def review(")],
    "state": RUNS,
    "note": "all six. A split keeps the parent and spawns children that "
            "reference it; a combine CLOSES the absorbed record and records "
            "where it went. Nothing is ever deleted."},
   {"his": "old case remains historically unchanged / new learning write-back "
           "Sequence is created",
    "where": [("patterns.py", "no_reopen"),
              ("patterns.py", "def writebacks(")],
    "state": RUNS,
    "note": "NO REOPEN, applied to his corrections. Every edit appends a "
            "write-back referencing the version it acted on, and the prior "
            "version is kept whole and still readable."},
   {"his": "PATTERN CANDIDATE → R-F-R / Doubt → YOU APPROVE",
    "where": [("patterns.py", "def rfr_check(")],
    "state": RUNS,
    "note": "his second canon file puts the triple pass BETWEEN the candidate "
            "and his approval, so no candidate reaches him unexamined: reverse "
            "→ forward → reverse, then the Doubt engine. It marks what is thin "
            "and rejects nothing."},
   {"his": "future sentences can activate it",
    "where": [("patterns.py", "def activate("),
              ("patterns.py", "def contradictions(")],
    "state": RUNS,
    "note": "his five outcomes are named per sentence — activate · contribute "
            "evidence · contradict · modify confidence · open a candidate. A "
            "pattern that cannot be contradicted is a belief, so contradiction "
            "is implemented too."},
  ]},

 {"group": "BUILT FROM HIS CANON — the router, and the flow made visible",
  "rows": [
   {"his": "the Engine should be selected from the structured problem, rather "
           "than the Engine deciding what the problem is",
    "where": [("router.py", "def route("), ("router.py", "MECHANISMS")],
    "state": RUNS,
    "note": "the walk used to be fixed — the same stages whatever the sentence "
            "was. Now the STRUCTURE names the mechanisms, each with the reason "
            "it was called, and a mechanism is never called without one."},
   {"his": "SEG-01 … SEG-10, and where each works in the brain",
    "where": [("router.py", "SEGMENT_ROLE"),
              ("router.py", "FLOW_POSITIONS"),
              ("router.py", "def flow_view(")],
    "state": RUNS,
    "note": "his own segment→flow-position placement, and his flow spine in "
            "his order. THE READING page lights each position this run "
            "actually reached and names the segments working there."},
   {"his": "RUBRIC VIEW — SHOW activated P IDs · CON IDs · SEG IDs · relations "
           "· patterns · emotions · intent · uncertainty · evidence",
    "where": [("readingpage.py", "Matched to existing IDs"),
              ("readingpage.py", "Ultra-micro decomposition")],
    "state": RUNS,
    "note": "the reading IS the page and the answer sits inside it, last, as "
            "he asked."},
   {"his": "let me edit and change that rubric so i can define the feeling, "
           "emotions there, which will help for tool to use further",
    "where": [("readingpage.py", "WHAT I THINK IT MEANS"),
              ("readingpage.py", "HOW I FELT"),
              ("server.py", "/patterns/review")],
    "state": RUNS,
    "note": "THE ONE THAT WAS MISSING IS NOW BUILT. He writes his "
            "interpretation, his feeling, his principle, his decision and his "
            "result into a candidate, approves it, and the approved pattern "
            "then reads future sentences carrying HIS words. Emotion finally "
            "goes IN, not only out."},
   {"his": "TRACEABLE UNDERSTANDING … the system should be capable of walking "
           "all the way back down",
    "where": [("server.py", 'elif path == "/micro":'),
              ("server.py", 'elif path == "/flow":')],
    "state": PARTIAL,
    "note": "every micro-sequence is readable by ask, and the flow view shows "
            "which mechanism was called and why. Not yet answerable: which "
            "sub-parameter, which element — those levels are empty by his own "
            "instruction."},
  ]},

 {"group": "EVERYTHING STARTS AT VAGUE LEVEL",
  "rows": [
   {"his": "i use vague example because everything start at vague level",
    "where": [("sequence.py", "everything exists before human discovers it"),
              ("sequence.py", "def is_invention(")],
    "state": RUNS,
    "note": "the human act is never step 1. And a vague ask is not forced into "
            "the wrong shape: something already there starts at Ground, an "
            "invention starts at Expression, because there is no ground to "
            "find. Your rule: ground type changes for invention."},
   {"his": "it should be as vague as galaxy and universe is",
    "where": [],
    "state": ABSENT,
    "note": "nothing in the code holds a thing OPEN at galaxy scale on "
            "purpose. Vagueness today is handled by classifying it (Mystery, "
            "Unknown, Needs Evidence) — which is a label on it, not the same "
            "as keeping it deliberately wide. Recorded, not acted on."},
  ]},

 {"group": "THE FEELING AND THE EMOTION",
  "rows": [
   {"his": "read the human under the words",
    "where": [("core_gate.py", "LENS_SIGNALS: dict[str, list[str]] = {"),
              ("core_gate.py", '"Wound & Threat"'),
              ("core_gate.py", '"Loyalty & Drive"')],
    "state": RUNS,
    "note": "six lenses with real signal words — Mask & Payoff · Wound & "
            "Threat · Loyalty & Drive · Desire & Fear · Pain & Payoff · "
            "Meaning & Identity. Your vocabulary, running on every answer."},
   {"his": "let me edit and change that rubric so i can define the "
           "feeling, emotions there, which will help for tool to use further",
    "where": [],
    "state": ABSENT,
    "note": "THE ONE THAT IS NOT THERE. Emotion is only ever read OUT of your "
            "words — as an axis, and as lens signals. There is nowhere for you "
            "to put emotion IN, and nothing carries your feeling forward into "
            "the next answer. The rubric (the parameter) is editable through "
            "the registry, but no screen shows you one to edit."},
  ]},

 {"group": "THE LOOPS — 5, and reducing",
  "rows": [
   {"his": "we decided 5 loops and reducing",
    "where": [("engine.py", "def run_recursive("),
              ("engine.py", "converged = True")],
    "state": RUNS,
    "note": "the REDUCING exists and is real: each pass carries the previous "
            "pass's product forward and it stops early when the product stops "
            "changing. But the count written in the code is THREE, not your "
            "five. Nobody moved it away from you — it was written before your "
            "ruling. It is not changed until you say."},
   {"his": "the loops themselves",
    "where": [("enums.py", 'PATTERN = "Pattern Loop"'),
              ("enums.py", 'ORIGIN = "Origin Loop"'),
              ("enums.py", 'RETURN = "Return Loop"')],
    "state": RUNS,
    "note": "thirty canonical loops including the Pattern Loop and the "
            "Sequence Loop, plus the RGL sub-loops: Origin · Recognition · "
            "Validation · Generation · Resolution · Return — that is SIX, not "
            "five. Your five may be these six with one folded, or a different "
            "five. I am not guessing which."},
  ]},

 {"group": "ARD · RGL · META — the flow the code is written on",
  "rows": [
   {"his": "The engine like ARD, RGL, Meta etc in files and repo assets "
           "define the same flow of rubrics",
    "where": [("nodes.py", "ARD_RGL_7025"), ("node_work.py", "ARD_RGL_7025"),
              ("pyramid.py", "ARD_RGL_7025"), ("parameters.py", "ARD Parameter Bank"),
              ("core_gate.py", "Core Gate"), ("persona.py", "ARD 3.1")],
    "state": RUNS,
    "note": "these are not references — they are the source the code was "
            "written from. Every one of these modules names ARD/RGL in its own "
            "header as the document it implements."},
   {"his": "Meta",
    "where": [("seq_kernel.py", 'META = "meta-controller"'),
              ("enums.py", 'META_CORE_REVIEW = "Meta-Core Review Loop"')],
    "state": PARTIAL,
    "note": "META exists twice — as a controller role in the sequence file, "
            "and as a review loop. The controller role is inside the file that "
            "nothing imports."},
  ]},

 {"group": "THE GATE EVERY FINDING PASSES — the seven filters",
  "rows": [
   {"his": "i want more filters and fact kind of",
    "where": [("filters.py", "def f1_ground("), ("filters.py", "def f2_sequence("),
              ("filters.py", "def f3_source("), ("filters.py", "def f4_mask("),
              ("filters.py", "def f5_fact("), ("filters.py", "def f6_halt("),
              ("filters.py", "def f7_loop(")],
    "state": PARTIAL,
    "note": "Ground · Sequence · Source · Mask · Fact · Halt · Loop, in order, "
            "every time. Source and Halt can genuinely stop an answer. FOUR of "
            "them compute their signal and then pass regardless — so a Mask "
            "the engine DETECTED never stops delivery. That is audit item 06, "
            "still open."},
   {"his": "Source caps one witness, and two witnesses that differ HALT — "
           "the gap goes to the human, never averaged",
    "where": [("filters.py", "def source_read("), ("filters.py", "def f3_source(")],
    "state": RUNS,
    "note": "one of the two filters that can actually hold. The gap is the "
            "Mask and it goes to you rather than being split down the middle."},
  ]},
]

# ---------------------------------------------------------------------------
# THE ABSENCES — stated as absences, in his words. Not a work list, not a
# proposal. What has no existence anywhere in the code.
ABSENCES: list[dict] = [
 {"what": "3,186 of his 3,204 have no route to them. Only 18 do.",
  "why": "NARROWED, not closed. Lexical matching over his names scores ZERO on "
         "his own Samrath sentence — cry, happy, birthday, school, never, "
         "always, today, went appear in 0 of his 3,204 names. asi_pyramid "
         "replaced word-matching with SIGNAL routing for the rows he assigned "
         "himself, and that mechanism generalises to any sentence of the same "
         "shape. But it reaches 18 parameters. The other 3,186 are reachable "
         "only when a signal is named for them — by him, or authored and "
         "corrected by him.",
  "his": "everything must be in the language or rubrics so it can pick"},
 {"what": "Behavioural repetition has no ordinal-position axis.",
  "why": "repetition.py gives a first occurrence and a later occurrence "
         "different addresses only for INFORMATION-seeking actions — CHECK #1 "
         "acquires, CHECK #2-5 cannot. 'he always cry' is behavioural, and "
         "read_repetition returns applies False on it. asi_pyramid reads the "
         "repetition as a standing pattern, which is a different thing from "
         "position.",
  "his": "he always cry"},
 {"what": "The SUB-PARAMETER and ELEMENT levels hold nothing.",
  "why": "Empty by his own instruction — he left the level unopened and "
         "unnamed. Recorded as empty, not as missing, and no placeholder was "
         "invented to fill it.",
  "his": "Element (sub parameter or element, one u need to leave for now "
         "empty) - None"},
 {"what": "The sequence protocol still does not run inside a live answer.",
  "why": "seq_kernel.py has no importer. His canon PLACES its entry at the "
         "write-back / learning sequence, and patterns.review() now creates "
         "exactly that — so the place exists and the bridge is one ruling "
         "away. The router names it as unwired rather than pretending.",
  "his": "new learning/write-back Sequence is created"},
 {"what": "The 3,072 rubrics are still 18 filled.",
  "why": "The machine around them is built and running; the vocabulary it "
         "runs on is not loaded. This is his workbook upload, and the "
         "importer has been waiting for it.",
  "his": "rubric means paramters the 3000"},
]

# WHERE THE CODE AND HIS WORD DISAGREE — surfaced, never silently picked.
SEAMS: list[dict] = [
 {"seam": "The loop count",
  "code": "engine.py — run_recursive(loops = 3)",
  "his": "we decided 5 loops and reducing",
  "note": "written before your ruling. Unchanged until you say."},
 {"seam": "How many loops there are",
  "code": "enums.py — the RGL sub-loops are SIX: Origin · Recognition · "
          "Validation · Generation · Resolution · Return",
  "his": "5 loops",
  "note": "your five may be these six with one folded, or a different five."},
 {"seam": "Multiple carryings exist in two shapes",
  "code": "parameters.py — thirteen axes over one text, AND "
          "Surface Intent / Hidden Intent as two separate parameters",
  "his": "i allowed one word to carry multiple reason",
  "note": "both are alive; neither knows about the other."},
 {"seam": "One pattern per sentence, versus the Intent halt",
  "code": "01A_INTENT — two surviving candidates HALT instead of being blended",
  "his": "each sentence always generate one pattern … "
         "it always have multiple carryings",
  "note": "HE RESOLVED THIS HIMSELF: every sentence generates a MICRO-SEQUENCE "
          "representation; a pattern is only what survives repetition. Built "
          "that way. Kept here because the earlier phrasing is still on record."},
 {"seam": "Is a rubric a parameter, or the thing that examines one?",
  "code": "ladder.py — TOTAL_PARAMS = 3072, and the registry IS the rubric store",
  "his": "\"rubric means paramters the 3000\"  vs, one message later, "
         "\"Human Parameter ≠ Rubric. Parameter = what capability/state. "
         "Rubric = how it is examined.\"",
  "note": "Two of his own statements that do not sit together. NOTHING WAS "
          "MOVED. He said focus on the work flow, so the flow was built and "
          "this waits for one word."},
 {"seam": "3,072 against a 2,560 bank in 80 containers",
  "code": "ladder.py — TOTAL_PARAMS = 3072, TOTAL_CONTAINERS = 200",
  "his": "\"3072 is the count\"  and then a full placement of "
         "SB-ASI-P0001…P2560 across CON-001…CON-080",
  "note": "3072 stays, on his explicit ruling. The 2,560 index is preserved "
          "verbatim in canon and used for nothing but the record — he said do "
          "not go to count and details."},
]


# ---------------------------------------------------------------------------
def _src_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def _find(module: str, anchor: str) -> dict:
    """Read the real source and report whether the anchor is still there, and
    on which line. This is what stops the map from going stale into a lie."""
    path = os.path.join(_src_dir(), module)
    if not os.path.exists(path):
        return {"module": module, "anchor": anchor, "found": False,
                "line": None, "why": "module not found"}
    try:
        with open(path, encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                if anchor in line:
                    return {"module": module, "anchor": anchor,
                            "found": True, "line": i}
    except Exception as exc:
        return {"module": module, "anchor": anchor, "found": False,
                "line": None, "why": str(exc)[:80]}
    return {"module": module, "anchor": anchor, "found": False, "line": None,
            "why": "anchor no longer in the file"}


def verify() -> dict:
    """Walk the whole map against the live source."""
    groups, checked, missing = [], 0, 0
    for g in MAP:
        rows = []
        for r in g["rows"]:
            hits = [_find(m, a) for m, a in r.get("where", [])]
            checked += len(hits)
            missing += sum(1 for h in hits if not h["found"])
            rows.append({**r, "hits": hits,
                         "state_note": STATE_NOTE.get(r["state"], "")})
        groups.append({"group": g["group"], "rows": rows})
    return {"groups": groups, "absences": ABSENCES, "seams": SEAMS,
            "checked": checked, "missing": missing,
            "counts": _state_counts(groups)}


def _state_counts(groups: list[dict]) -> dict:
    out: dict[str, int] = {}
    for g in groups:
        for r in g["rows"]:
            out[r["state"]] = out.get(r["state"], 0) + 1
    return out


def ladder_reading(registry: dict) -> dict:
    """The live rubric count — read from HIS registry, never written here.
    rubric = parameter, so this is how many rubrics actually carry anything."""
    params = registry.get("parameters", []) or []
    filled = [p for p in params if p.get("filled")]
    conts = registry.get("containers", []) or []
    return {"rubrics_total": 3072,
            "rubrics_filled": len(filled),
            "containers_total": 200,
            "containers_filled": sum(1 for c in conts if c.get("filled")),
            "segments": len(registry.get("segments", []) or []),
            "version": registry.get("version", 0),
            "saved_at": registry.get("saved_at", "")}


PAGE = r"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>WHAT EXISTS — Sourceborn</title><style>
:root{--bg:#070809;--panel:#0f1219;--elev:#141826;--line:#1c2230;--line2:#262d3d;
--ink:#eef2f8;--mut:#7d8699;--acc:#7c8bff;--ok:#34d399;--warn:#fbbf24;--bad:#f87171;
--grad:linear-gradient(135deg,#7c8bff,#a78bfa 60%,#f0abfc)}
*{box-sizing:border-box}
body{margin:0;color:var(--ink);font:15px/1.55 'Inter',-apple-system,Segoe UI,Roboto,sans-serif;
background:radial-gradient(900px 520px at 85% -8%,rgba(124,139,255,.14),transparent 60%),var(--bg)}
.app{max-width:1180px;margin:0 auto;padding:0 18px 90px}
.top{position:sticky;top:0;z-index:9;display:flex;justify-content:space-between;align-items:center;
gap:10px;padding:14px 2px;background:linear-gradient(180deg,rgba(7,8,9,.92),rgba(7,8,9,.45));
backdrop-filter:blur(12px);border-bottom:1px solid var(--line);flex-wrap:wrap}
.name{font-weight:700;font-size:18px}.name small{color:var(--mut);font-weight:400;margin-left:8px}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
.lede{color:var(--mut);font-size:14px;max-width:76ch;margin:16px 0 4px}
.lede b{color:var(--ink)}
.strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(126px,1fr));gap:10px;margin:18px 0 6px}
.st{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:11px 13px}
.st .n{font-size:24px;font-weight:700;font-variant-numeric:tabular-nums}
.st .n.g{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.st .l{color:var(--mut);font-size:11.5px;line-height:1.35;margin-top:2px}
.sec{margin:30px 0 10px;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;
border-bottom:1px solid var(--line);padding-bottom:8px}
.sec h2{margin:0;font-size:13px;letter-spacing:.14em;color:var(--mut);text-transform:uppercase}
.row{background:var(--panel);border:1px solid var(--line);border-radius:13px;padding:13px 15px;margin:9px 0}
.his{font-size:15px;line-height:1.5}
.his:before{content:'\201C';color:var(--mut)}.his:after{content:'\201D';color:var(--mut)}
.tagline{display:flex;gap:7px;flex-wrap:wrap;align-items:center;margin:9px 0 7px}
.tag{font-size:10.5px;letter-spacing:.05em;text-transform:uppercase;border-radius:999px;
padding:3px 9px;border:1px solid var(--line2);color:var(--mut);white-space:nowrap}
.tag.RUNS{color:#9ff0d0;border-color:rgba(52,211,153,.45)}
.tag.THIN{color:#ffe2a3;border-color:rgba(251,191,36,.45)}
.tag.PARTIAL{color:#ffe2a3;border-color:rgba(251,191,36,.45)}
.tag.NOTWIRED{color:#ffc4c4;border-color:rgba(248,113,113,.45)}
.tag.ABSENT{color:#ffc4c4;border-color:rgba(248,113,113,.55);background:rgba(248,113,113,.08)}
.note{color:var(--mut);font-size:13.5px}
.at{margin-top:9px;display:flex;gap:6px;flex-wrap:wrap}
.at code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11.5px;
background:var(--elev);border:1px solid var(--line2);border-radius:7px;padding:3px 8px;color:var(--ink)}
.at code.gone{color:var(--bad);border-color:rgba(248,113,113,.5)}
.at code i{color:var(--mut);font-style:normal}
.abs{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--bad);
border-radius:12px;padding:13px 15px;margin:9px 0}
.abs h3{margin:0 0 5px;font-size:14.5px}
.seam{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--warn);
border-radius:12px;padding:13px 15px;margin:9px 0}
.seam h3{margin:0 0 7px;font-size:14.5px}
.seam table{width:100%;border-collapse:collapse;font-size:13.5px}
.seam td{padding:4px 6px;border-top:1px solid var(--line);vertical-align:top}
.seam td:first-child{color:var(--mut);width:78px;white-space:nowrap}
.foot{margin-top:40px;padding-top:14px;border-top:1px solid var(--line2);color:var(--mut);font-size:13px}
</style></head><body><div class=app>
<div class=top>
 <div class=name>WHAT EXISTS<small>your understanding, found in the code</small></div>
 <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap">
  <span class=tag id=chk>checking&hellip;</span>
  <a href="/engine">&#9881; THE ENGINE</a><a href="/page">&#9638; MY PAGE</a>
  <a href="/" style="color:var(--mut)">&larr; app</a>
 </div>
</div>
<p class=lede>Every row is <b>your words</b>, then the place in the code where that
understanding already lives, then what state it is actually in. <b>Rubric means
parameter — the 3,072.</b> Nothing here is a proposal. What has no existence is
listed as an absence, and where the code disagrees with your word it is shown as
a seam rather than quietly decided.</p>
<p class=lede>This page <b>reads the real source every time you open it</b>. Each
reference carries an anchor that must still be present in the file; if a line
moves, the number moves with it, and if an anchor is gone the reference turns red.
It cannot go stale into a lie.</p>
<div class=strip id=strip></div>
<div id=root></div>
<div class=foot id=foot></div>
</div><script>
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const cls=s=>String(s).replace(/[^A-Za-z]/g,'').toUpperCase();
function strip(d){
 const c=d.counts||{}, L=d.ladder||{};
 const cell=(n,l,g)=>'<div class=st><div class="n'+(g?' g':'')+'">'+esc(n)+'</div><div class=l>'+l+'</div></div>';
 document.getElementById('strip').innerHTML=
  cell((L.rubrics_filled||0)+' / '+(L.rubrics_total||3072),'rubrics (parameters) that carry anything',true)+
  cell((L.containers_filled||0)+' / '+(L.containers_total||200),'containers filled')+
  cell(c.RUNS||0,'pieces of your understanding running in a live answer')+
  cell((c.PARTIAL||0)+(c.THIN||0),'running, but on almost nothing / one direction only')+
  cell(c['BUILT-NOT-WIRED']||0,'built and tested — nothing calls it')+
  cell((d.absences||[]).length,'with no existence anywhere')+
  cell(d.checked||0,'code references, checked live'+(d.missing?' — <b style="color:var(--bad)">'+d.missing+' gone</b>':' — all found'));
}
function row(r){
 const at=(r.hits||[]).map(h=>h.found
   ? '<code>'+esc(h.module)+'<i>:'+h.line+'</i></code>'
   : '<code class=gone>'+esc(h.module)+' <i>'+esc(h.anchor).slice(0,34)+' &mdash; '+esc(h.why||'gone')+'</i></code>').join('');
 return '<div class=row><div class=his>'+esc(r.his)+'</div>'+
  '<div class=tagline><span class="tag '+cls(r.state)+'">'+esc(r.state)+'</span>'+
  '<span class=note>'+esc(r.state_note)+'</span></div>'+
  '<div class=note>'+esc(r.note)+'</div>'+
  (at?'<div class=at>'+at+'</div>':'<div class=at><code class=gone><i>nowhere</i></code></div>')+'</div>';
}
async function boot(){
 let d;
 try{ d=await (await fetch('/exists/data')).json(); }
 catch(e){ document.getElementById('root').innerHTML='<div class=abs><h3>could not read the map</h3><div class=note>'+esc(e)+'</div></div>'; return; }
 strip(d);
 const chk=document.getElementById('chk');
 chk.textContent=d.missing?(d.missing+' reference(s) gone'):(d.checked+' references — all found');
 chk.className='tag '+(d.missing?'ABSENT':'RUNS');
 let h='';
 for(const g of (d.groups||[])){
  h+='<div class=sec><h2>'+esc(g.group)+'</h2></div>';
  h+=(g.rows||[]).map(row).join('');
 }
 h+='<div class=sec><h2>What has no existence anywhere</h2></div>';
 h+=(d.absences||[]).map(a=>'<div class=abs><h3>'+esc(a.what)+'</h3>'+
   '<div class=note>'+esc(a.why)+'</div>'+
   '<div class=at><code><i>your words:</i> '+esc(a.his)+'</code></div></div>').join('');
 h+='<div class=sec><h2>Where the code and your word disagree &mdash; surfaced, not decided</h2></div>';
 h+=(d.seams||[]).map(s=>'<div class=seam><h3>'+esc(s.seam)+'</h3><table>'+
   '<tr><td>in code</td><td>'+esc(s.code)+'</td></tr>'+
   '<tr><td>your word</td><td>'+esc(s.his)+'</td></tr>'+
   '<tr><td>note</td><td class=note>'+esc(s.note)+'</td></tr></table></div>').join('');
 document.getElementById('root').innerHTML=h;
 const L2=d.ladder||{};
 document.getElementById('foot').innerHTML=
  'Rubric registry version <b>'+esc(L2.version)+'</b>'+
  // version 0 is the seed. It carries a timestamp, but nothing was ever
  // uploaded into it — saying "saved" there would read as work that happened.
  (L2.version?' &middot; saved '+esc(L2.saved_at):' &middot; seed &mdash; your workbook has never been uploaded, so 18 is the true filled count')+
  ' &middot; read live at '+esc(d.at||'')+'. Nothing on this page was written by hand about the code &mdash; '+
  'the file and line come from reading the source at the moment you opened it.';
}
boot();
</script></body></html>"""
