"""The universal sequence — the one shape under hunger, gravity and RH.

The user's rule: *everything exists before human discovers it.* The human act
is never step 1. Nobody made the fuel, the falling, or the zeros. What a person
does is find a way to SAY the thing — and then the saying gets a name, and the
name starts being mistaken for the thing.

    1 GROUND      it is already there                fuel · falling · the zeros
    2 PRESSURE    something forces contact           the body empties · it falls
                                                     on someone · Gauss counts
    3 USE         used long before understood        farming · building · tables
    4 WITNESS     someone stops and LOOKS            Newton · the Encke letter
    5 EXPRESSION  a way to say it is found           "hunger" · F=Gm1m2/r² ·
                                                     xi(a)=0, a real
    6 NAMING      the name is mistaken for the thing "gravity" != the falling ·
                                                     "Re(s)=1/2" != his sentence
    7 HALT        the expression fails somewhere     Mercury · no proof
    8 LOOP        the halt is a new GROUND -> 1      Einstein · the xi expansion

Step 6 is where the Mask forms. That is not decoration — it is the Riemann
finding stated generally, and it is why the Source Pass and this sequence are
one machine and not two.

GROUND vs INVENTION: the sequence above is for things that pre-exist the
asking. An invention (cricket, a company, a rule) starts at 5 — there is no
ground to find, only an expression to build. The user's own rule: *ground type
will change for invention, not for routine asks.*
"""

from __future__ import annotations

GROUND, PRESSURE, USE, WITNESS, EXPRESSION, NAMING, HALT, LOOP = range(1, 9)

STEPS: tuple[tuple[int, str, str], ...] = (
    (GROUND, "Ground", "it is already there; nobody made it"),
    (PRESSURE, "Pressure", "something forces contact with it"),
    (USE, "Use", "it is used long before it is understood"),
    (WITNESS, "Witness", "someone stops using it and looks at it"),
    (EXPRESSION, "Expression", "a way to say it is found — the human act"),
    (NAMING, "Naming", "the name begins to stand in for the thing"),
    (HALT, "Halt", "the expression fails on some case"),
    (LOOP, "Loop", "the halt becomes the next Ground"),
)
STEP_NAME = {n: name for n, name, _ in STEPS}

# an ask that says "build/make/design" has no ground to find — it is invention.
_INVENTION = ("build", "make", "design", "create", "invent", "draft", "write me",
              "generate", "set up", "plan a", "name a", "app", "product",
              "logo", "rule for", "game")
# an ask that says "why/what is/how does" is reaching for something that is
# already there — it wants an expression, not an invention.
_GROUNDED = ("why", "what is", "what are", "how does", "how do", "explain",
             "prove", "does ", "is it true", "reason", "cause", "origin",
             "meaning", "understand")

_HALT_WORDS = ("fails", "stuck", "cannot", "can't", "doesn't work", "breaks",
               "no proof", "unproved", "unproven", "contradiction", "halt")
_NAMING_WORDS = ("called", "named", "term", "word for", "definition", "means",
                 "same as", "really mean", "actually mean")
_WITNESS_WORDS = ("source", "original", "manuscript", "who said", "his own",
                  "primary", "evidence", "letter", "paper", "check")


def is_invention(text: str) -> bool:
    """Ground type changes for invention, not for routine asks."""
    low = text.lower()
    inv = sum(1 for w in _INVENTION if w in low)
    gnd = sum(1 for w in _GROUNDED if w in low)
    return inv > gnd


def place(text: str) -> tuple[int, str]:
    """Which step is this ask standing on? Returns (step, why)."""
    low = text.lower()
    if is_invention(low):
        return EXPRESSION, "invention — no ground to find, an expression to build"
    if any(w in low for w in _HALT_WORDS):
        return HALT, "the ask names a failure — the halt is the subject"
    if any(w in low for w in _NAMING_WORDS):
        return NAMING, "the ask is about the word, not the thing — Mask territory"
    if any(w in low for w in _WITNESS_WORDS):
        return WITNESS, "the ask wants the source looked at, not used"
    if any(low.startswith(w) or f" {w}" in low for w in ("why", "how", "what")):
        return EXPRESSION, "the ask wants a way to say something already there"
    return PRESSURE, "something has forced contact; the ground is not yet named"


def next_ask(step: int, halt: str, subject: str) -> str:
    """Step 8. A halt is never an ending — it is the next Point Zero.
    This is the return: the engine hands back the ask it just opened."""
    subject = (subject or "this").strip()[:80]
    if step == HALT or halt:
        return (f"The halt on {subject} is the next Point Zero. "
                f"What is already there, underneath that failure, that nobody made?")
    if step == NAMING:
        return (f"Which word here is the thing, and which is only the name of it? "
                f"Show both for {subject}.")
    if step == EXPRESSION:
        return (f"If this expression of {subject} fails on one case, which case? "
                f"Name it now, before it is needed.")
    return f"What forced this contact with {subject}, and what was there before it?"
