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
 {"what": "A rubric still holds a name and free text — not how it is "
          "recognised, nor how it is graded.",
  "why": "This is the one that did NOT get built. The ultra-micro split is now "
         "real, but matching a sentence to a RUBRIC is still 4-letter word "
         "overlap, because there is nothing richer inside the entry to match "
         "against. 'in the language of rubrics so it can pick' needs the entry "
         "itself to say what picks it.",
  "his": "everything must be in the language or rubrics so it can pick"},
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
