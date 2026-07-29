"""The Source Pass — two witnesses, and the Mask between them.

The old evidence ladder rated a claim by the KIND of source behind it, and one
good source was enough to reach High. That is the hole: one rendering of a
thing is not the thing. The whole Riemann result came from something the ladder
could not express — two witnesses of the same fact, read against each other.

So this module rates a claim by DISTANCE FROM THE EVENT, and by HOW MANY
INDEPENDENT witnesses stand behind it:

    ORIGINAL    the thing itself                 (the user's own words/corpus)
    WITNESSED   something that observed it       (a live check)
    CARRIED     a copy, edition, translation     (our own memory of a reading)
    REPORTED    prose repeating a carrier        (nothing behind it)

One witness caps at Medium, however good it is. Two independent witnesses that
agree reach High. Two that DIFFER do not get averaged and do not get picked
between — the difference is the finding. That gap is the **Mask**: the space
between what was said and what was shown.
"""

from __future__ import annotations

from dataclasses import dataclass, field

ORIGINAL, WITNESSED, CARRIED, REPORTED = "ORIGINAL", "WITNESSED", "CARRIED", "REPORTED"
RUNG_ORDER = (REPORTED, CARRIED, WITNESSED, ORIGINAL)

# words that assert, and the words that pull an assertion back. A claim that is
# asserted in one witness and hedged in another has been SOFTENED — that is
# exactly what happened between Riemann's letter and his printed paper.
ASSERTS = ("is", "are", "was", "were", "all", "every", "always", "proves",
           "shows", "establishes", "confirms", "obviously", "evidently", "clearly")
HEDGES = ("probably", "likely", "very probable", "wahrscheinlich", "seems",
          "appears", "suggests", "may", "might", "could", "perhaps",
          "presumably", "arguably", "possibly", "tends to")

# an editorial mark is itself a witness that something was taken out.
EXCISION_MARKS = ("...", "…", ". .", "[…]", "[...]", "extract from",
                  "auszug", "excerpt", "abridged", "in part", "[omitted]")


@dataclass
class Witness:
    """One account of a claim, and how far it stands from the event."""
    text: str
    origin: str                       # where it came from, named
    rung: str = REPORTED

    @property
    def weight(self) -> int:
        return RUNG_ORDER.index(self.rung) if self.rung in RUNG_ORDER else 0


@dataclass
class Mask:
    """What moved between two witnesses. Never resolved here — it goes out."""
    kind: str                         # cut | softened | renamed | added
    what: str
    in_witness: str
    not_in: str

    def as_dict(self) -> dict:
        return {"kind": self.kind, "what": self.what,
                "in": self.in_witness, "not_in": self.not_in}


@dataclass
class SourceRead:
    claim: str
    witnesses: list[Witness] = field(default_factory=list)
    masks: list[Mask] = field(default_factory=list)
    confidence: str = "Low"
    halt: bool = False
    excisions: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {"claim": self.claim[:160],
                "witnesses": [{"origin": w.origin, "rung": w.rung} for w in self.witnesses],
                "n_independent": len(self.witnesses),
                "masks": [m.as_dict() for m in self.masks],
                "excisions": self.excisions,
                "confidence": self.confidence, "halt": self.halt}


def _tokens(text: str) -> set[str]:
    return {w.strip(".,;:!?()[]\"'").lower()
            for w in text.split() if len(w.strip(".,;:!?()[]\"'")) > 3}


def independent(a: Witness, b: Witness) -> bool:
    """Two witnesses are independent only if they trace to different acts of
    observation. A reprint, a translation, a quotation of the same origin is
    ONE witness wearing two coats — that is the trap this whole module exists
    to avoid."""
    if a.origin == b.origin:
        return False
    ta, tb = _tokens(a.text), _tokens(b.text)
    if not ta or not tb:
        return a.origin != b.origin
    overlap = len(ta & tb) / max(1, min(len(ta), len(tb)))
    return overlap < 0.85          # near-identical text = one origin restated


def bears_on(w: Witness, claim: str) -> bool:
    """Is this witness actually speaking to THIS claim, or merely present?

    Two documents in the same run are not two witnesses to every sentence in
    it. A witness bears on a claim only if it shares the claim's own terms.
    Without this test every pair of texts 'disagrees' about everything, which
    is how the first cut of this module held all 70 nodes at once."""
    tc = _tokens(claim)
    if not tc:
        return False
    return len(tc & _tokens(w.text)) >= max(1, min(2, len(tc) // 6))


def find_masks(a: Witness, b: Witness, claim: str = "") -> list[Mask]:
    """What moved between two witnesses — measured ON THE CLAIM, not across
    the whole of two different documents. Softenings and cuts of the claim's
    OWN terms are reported; everything else is left alone rather than guessed
    at, because a difference in vocabulary is not a Mask."""
    masks: list[Mask] = []
    tc = _tokens(claim)
    if not tc:
        return masks
    ta, tb = _tokens(a.text) & tc, _tokens(b.text) & tc
    if not ta or not tb:
        return masks                 # one of them does not speak to this claim
    la, lb = a.text.lower(), b.text.lower()

    a_asserts = any(f" {w} " in f" {la} " for w in ASSERTS)
    b_hedges = any(h in lb for h in HEDGES)
    a_hedges = any(h in la for h in HEDGES)
    b_asserts = any(f" {w} " in f" {lb} " for w in ASSERTS)
    if a_asserts and b_hedges and not a_hedges:
        masks.append(Mask("softened", "asserted here, hedged there", a.origin, b.origin))
    elif b_asserts and a_hedges and not b_hedges:
        masks.append(Mask("softened", "asserted there, hedged here", b.origin, a.origin))

    # a term OF THE CLAIM that one witness carries and the other drops
    gone = sorted(ta - tb)
    if gone and len(ta) >= 3 and len(gone) < len(ta):
        masks.append(Mask("cut", ", ".join(gone[:4]), a.origin, b.origin))
    added = sorted(tb - ta)
    if added and len(tb) >= 3 and len(added) < len(tb):
        masks.append(Mask("added", ", ".join(added[:4]), b.origin, a.origin))
    return masks


def excisions_in(text: str) -> list[str]:
    """An ellipsis is not punctuation, it is a report that something was
    removed. Weber's two dots hid the one clause that named the recipient."""
    low = text.lower()
    return [m for m in EXCISION_MARKS if m in low]


def read(claim: str, witnesses: list[Witness]) -> SourceRead:
    """The cap rule. One witness never reaches High. Two that differ HALT."""
    r = SourceRead(claim=claim, witnesses=list(witnesses))
    for w in witnesses:
        r.excisions.extend(x for x in excisions_in(w.text) if x not in r.excisions)

    # only witnesses that actually speak to THIS claim count as witnesses to it
    speaking = [w for w in witnesses if bears_on(w, claim)]
    indep: list[Witness] = []
    for w in speaking:
        if all(independent(w, k) for k in indep):
            indep.append(w)
    r.witnesses = indep

    if not indep:
        r.confidence = "Low"
        return r
    if len(indep) == 1:
        # however good it is. this is the cap, and it is the point.
        r.confidence = "Medium" if indep[0].rung in (ORIGINAL, WITNESSED) else "Low"
        return r

    for i in range(len(indep)):
        for j in range(i + 1, len(indep)):
            r.masks.extend(find_masks(indep[i], indep[j], claim))
    if r.masks:
        r.halt = True                # do not average, do not pick. it goes out.
        r.confidence = "Medium"
    else:
        r.confidence = "High"
    return r


def collect(ctx) -> list[Witness]:
    """Every independent account this run actually has. Nothing invented — if
    the run has one source, it gets one witness and it caps."""
    ws: list[Witness] = []
    if getattr(ctx, "raw_text", ""):
        ws.append(Witness(ctx.raw_text, "your own words", ORIGINAL))
    if getattr(ctx, "matched", None):
        ws.append(Witness(" ".join(ctx.matched)[:400], "your corpus", ORIGINAL))
    if getattr(ctx, "live", ""):
        ws.append(Witness(str(ctx.live)[:400], "live check", WITNESSED))
    hits = getattr(ctx, "memory_hits", None) or []
    if hits:
        ws.append(Witness(" ".join(s for _, s in hits)[:400],
                          "engine memory", CARRIED))
    if getattr(ctx, "recall_matches", None):
        ws.append(Witness(" ".join(ctx.recall_matches)[:300], "past asks", CARRIED))
    if getattr(ctx, "answer", "") and len(ws) == 0:
        ws.append(Witness(str(ctx.answer)[:400], "model prose", REPORTED))
    return ws
