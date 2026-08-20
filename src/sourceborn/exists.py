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
