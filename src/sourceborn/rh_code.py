"""RH AS CODE — Re(s) = ½ + ti read as a build specification, not a theorem.

The owner's instruction: *"i dont wanted any proof of anything / i want to use
RH as a code."* So nothing here proves anything. This module takes the three
objects the Riemann work actually hands us — **the primes, the zeros, and the
formula that ties them** — and uses them as parts.

WHAT MAPS TO WHAT
-----------------
    primes p            the raw facts. Irreducible. Each one appears once.
    log p               that fact's own period — how long before it comes round
    zeros ½ + it        the doubts. Each one a correction to the running answer
    ½  (the real part)  HOW MUCH power any single doubt is allowed
    t  (the height)     WHEN it fires — its rhythm, not its size
    explicit formula    answer = trend − sum of the doubts
    RH holds            no single voice can ever outgrow the crowd
    a zero off the line one voice grows faster than the crowd and ends up
                        being the answer by itself — DRIFT, with a name on it

That last line is the whole reason this file exists. **RH is a stability law.**
A contributor sitting at σ = ½ grows like √n; a contributor at σ = 0.7 grows
like n^0.7, and after enough steps it is louder than everything else put
together. "Every zero on the critical line" is the same sentence as the
standing order *no single witness owns the answer* — written as a number you
can measure instead of a rule you have to remember.

THE FIVE PARTS
--------------
    half_confidence()   the static ½ — one witness caps at half; two that
                        differ HALT at ½ and the gap goes to the human
    line_check()        the growth test — fit each voice's σ; σ > ½ is drift,
                        and it says which voice
    explicit_answer()   the answer as trend − Σ doubts; nothing averaged,
                        nothing dropped, every correction visible
    periods()           the t-axis — give each voice its own rhythm
    degeneracy()        unique factorisation — two voices must not share a
                        period. If they do, they are one voice counted twice.

Run it:  ``python -m sourceborn.rh_code``  — prints a stable engine and a
drifting one side by side, so the law is something you watch, not something
you are told.

`[FACT]` the mapping of ½ to a growth exponent is the standard statement of RH.
`[READING]` applying it to nodes and witnesses is the owner's engine, not a
result about zeta. This file claims a design, never a proof.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Iterable, Sequence

# The line itself. Everything in this module is a distance from this number.
HALF = 0.5

# How far off ½ a measured exponent may sit before it is called drift. Small
# runs are noisy; this is the tolerance, and it is a knob, not a truth.
LINE_TOLERANCE = 0.08


# ------------------------------------------------------------------ the primes

def _primes(n: int) -> list[int]:
    """The first *n* primes. The atoms — one per distinct voice."""
    out: list[int] = []
    cand = 2
    while len(out) < n:
        if all(cand % p for p in out if p * p <= cand):
            out.append(cand)
        cand += 1
    return out


def periods(voices: Sequence[str]) -> dict[str, float]:
    """Give every voice its own period — the t-axis.

    A voice gets the next prime and its period is ``log p``. That is not
    decoration: it is the one property the primes have that arithmetic groups
    do not — **distinct primes have rationally independent logarithms**, so no
    two voices can ever land on the same beat by accident. Unique factorisation
    is what keeps the rhythm readable.
    """
    ps = _primes(len(voices))
    return {v: math.log(p) for v, p in zip(voices, ps)}


def degeneracy(period_map: dict[str, float], tol: float = 1e-9) -> list[list[str]]:
    """Voices that share a beat. Each returned group is ONE voice counted twice.

    Why this is a hard rule and not tidiness: where the length spectrum is
    degenerate the statistics collapse — the arithmetic surfaces show Poisson
    for exactly this reason. Duplicate a node and you have not made the engine
    louder, you have made it deaf. The registry's *"an existing node is
    returned unchanged"* is this law, already obeyed.
    """
    groups: dict[float, list[str]] = {}
    for who, t in period_map.items():
        for seen in groups:
            if abs(seen - t) <= tol:
                groups[seen].append(who)
                break
        else:
            groups[t] = [who]
    return [g for g in groups.values() if len(g) > 1]


# ------------------------------------------------------------- the static half

@dataclass
class HalfRead:
    """What one pass of the ½ rule decided."""
    confidence: float
    verdict: str                      # "capped" | "held" | "halt"
    why: str
    mask: tuple[str, str] | None = None   # the gap, when two witnesses differ

    def as_dict(self) -> dict:
        return {"confidence": round(self.confidence, 4), "verdict": self.verdict,
                "why": self.why, "mask": list(self.mask) if self.mask else None}


def half_confidence(witnesses: Sequence[str]) -> HalfRead:
    """The ½ as a ceiling on any single voice.

    - **no witness** → 0.0. Nothing to stand on.
    - **one witness** → capped at exactly ½. One voice is never the answer;
      σ = 1 is what a voice that owns the answer looks like, and no voice is
      allowed there.
    - **two or more that agree** → above ½, rising with the count but never
      reaching 1. Agreement earns, it does not conclude.
    - **two that differ** → **HALT at ½**, and the gap is returned as a Mask.
      Not averaged. The two readings go to the human as two readings.

    Averaging two differing witnesses is the exact move the critical line
    forbids: it invents a single voice at full weight out of two half ones.
    """
    seen = [w.strip() for w in witnesses if w and w.strip()]
    if not seen:
        return HalfRead(0.0, "held", "no witness — nothing to stand on")

    distinct = list(dict.fromkeys(seen))
    if len(distinct) == 1:
        if len(seen) == 1:
            return HalfRead(HALF, "capped",
                            "one witness — capped at ½; a single voice never owns the answer")
        # several sources, same reading
        conf = 1.0 - 0.5 ** len(seen)
        return HalfRead(conf, "held",
                        f"{len(seen)} witnesses agree — {conf:.3f}, and never 1.0")

    return HalfRead(HALF, "halt",
                    "two witnesses differ — HALT at ½; the gap is a Mask for the human, "
                    "not a number to average",
                    mask=(distinct[0], distinct[1]))


# ------------------------------------------------------------- the growth test

@dataclass
class LineVerdict:
    """One voice, measured against the line."""
    who: str
    sigma: float
    on_line: bool
    points: int
    why: str
    resolved: bool = True             # was the run long enough to trust this σ?
    cycles: float | None = None       # cycles of this voice's rhythm per bucket

    def as_dict(self) -> dict:
        return {"who": self.who, "sigma": round(self.sigma, 4),
                "on_line": self.on_line, "points": self.points, "why": self.why,
                "resolved": self.resolved,
                "cycles": round(self.cycles, 3) if self.cycles is not None else None}


def _exponent(steps: Sequence[float], weights: Sequence[float]) -> float:
    """Least-squares slope of log(weight) against log(step) — the σ of a voice."""
    xs, ys = [], []
    for n, w in zip(steps, weights):
        if n > 0 and w > 0:
            xs.append(math.log(n))
            ys.append(math.log(w))
    if len(xs) < 2:
        return float("nan")
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    return float("nan") if den == 0 else num / den


def envelope(steps: Sequence[float], values: Sequence[float],
             buckets: int = 6) -> tuple[list[float], list[float]]:
    """Strip the wobble before measuring the growth. **Do this or be wrong.**

    A single sample of a correction is ``x^σ · cos(t log x + φ)`` — the cosine
    can be near zero at the very x you sampled, and a line fitted through raw
    samples reads the wobble as slope. Measured raw, a voice built at exactly ½
    can come back at 0.6 and be accused of drift for nothing. That is a false
    alarm, and a drift detector that cries wolf is worse than none.

    ``|cos|`` averages to 2/π — **a constant** — so the mean of ``|value|``
    inside a bucket of nearby scales follows ``x^σ`` cleanly while any one
    sample does not. Buckets are equal-width in log x, matching how the answer
    actually grows.

    **The averaging only works if a bucket covers a whole cycle.** A voice with
    rhythm ``t`` needs bucket width ``≥ 2π/t`` in log x, so the run must span
    ``buckets · 2π/t``. Measured: at 0.21 cycles per bucket the on-line voices
    come back 0.032 off ½; at 0.76 cycles, 0.004; at 2.46 cycles, 0.0007. **The
    accuracy is set by how long the run is, not by this code** — which is why
    :func:`line_check` reports the resolution instead of quietly rounding.
    """
    pts = [(s, abs(v)) for s, v in zip(steps, values) if s > 0]
    if len(pts) < 2:
        return [p[0] for p in pts], [p[1] for p in pts]
    lo, hi = math.log(pts[0][0]), math.log(pts[-1][0])
    if hi <= lo:
        return [pts[0][0]], [sum(p[1] for p in pts) / len(pts)]
    width = (hi - lo) / buckets
    bins: list[list[tuple[float, float]]] = [[] for _ in range(buckets)]
    for s, v in pts:
        i = min(int((math.log(s) - lo) / width), buckets - 1)
        bins[i].append((s, v))
    cs, ms = [], []
    for b in bins:
        if not b:
            continue
        cs.append(math.exp(sum(math.log(s) for s, _ in b) / len(b)))
        ms.append(sum(v for _, v in b) / len(b))
    return cs, ms


def line_check(history: dict[str, Sequence[float]],
               steps: Sequence[float] | None = None,
               tolerance: float = LINE_TOLERANCE,
               smooth: bool = False,
               buckets: int = 6,
               period_map: dict[str, float] | None = None) -> list[LineVerdict]:
    """Measure every voice's growth exponent and put it on or off the line.

    *history* is ``{voice: [cumulative weight after step 1, after step 2, …]}``
    — how much of the answer that voice has moved as the run got longer.

    A voice at **σ ≈ ½** grows like √n: it stays one of the crowd forever.
    A voice at **σ > ½** grows faster than the crowd and, given enough steps,
    **is** the answer. That is drift, and this returns its name.

    Set ``smooth=True`` when the weights are instantaneous samples of an
    oscillating correction rather than a monotone running total — it buckets
    them through :func:`envelope` first. Without it the wobble is read as slope
    and voices sitting exactly on the line get accused. Feed it plenty of
    samples: buckets need something to average.

    Pass ``period_map`` (from :func:`periods`) and each verdict comes back
    saying whether the run was long enough to trust it. **An under-resolved σ
    is reported as under-resolved, not rounded to something reassuring** — the
    fix is a longer run, and the verdict says so.

    Sorted worst-first, so the top row is the thing to look at.
    """
    out: list[LineVerdict] = []
    for who, ws in history.items():
        ns = list(steps) if steps is not None else list(range(1, len(ws) + 1))
        cycles = None
        if smooth and period_map and who in period_map and len(ns) >= 2:
            lo, hi = math.log(ns[0]), math.log(ns[-1])
            if hi > lo:
                cycles = period_map[who] * ((hi - lo) / buckets) / (2 * math.pi)
        if smooth:
            ns, ws = envelope(ns, ws, buckets)
        sig = _exponent(ns, ws)
        if math.isnan(sig):
            out.append(LineVerdict(who, float("nan"), True, len(ws),
                                   "not enough movement to measure — no verdict claimed",
                                   cycles=cycles))
            continue
        on = sig <= HALF + tolerance
        why = (f"σ={sig:.3f} ≤ ½+{tolerance} — on the line, one of the crowd"
               if on else
               f"σ={sig:.3f} > ½+{tolerance} — OFF THE LINE; this voice is "
               f"outgrowing the crowd and will end up being the answer alone")
        resolved = cycles is None or cycles >= 1.0
        if not resolved:
            why += (f"  [UNDER-RESOLVED: the run covers only {cycles:.2f} of this "
                    f"voice's cycle per bucket; σ is ±0.03 at best. Lengthen the "
                    f"run to ≥ {buckets * 2 * math.pi / period_map[who]:.1f} in log x "
                    f"before trusting this row]")
        out.append(LineVerdict(who, sig, on, len(ws), why, resolved, cycles))
    out.sort(key=lambda v: (-(v.sigma if not math.isnan(v.sigma) else -1)))
    return out


def drifting(verdicts: Iterable[LineVerdict]) -> list[str]:
    """Just the names that are off the line. The short answer."""
    return [v.who for v in verdicts if not v.on_line]


# ------------------------------------------------------- the explicit formula

@dataclass
class Doubt:
    """One correction — a zero, in the engine's clothes.

    ``sigma`` is its power (½ = on the line), ``t`` its rhythm, ``phase``
    where in that rhythm it starts, ``weight`` how loud it is at all.
    """
    who: str
    t: float
    sigma: float = HALF
    phase: float = 0.0
    weight: float = 1.0

    def at(self, x: float) -> float:
        """This doubt's contribution at scale *x* — the shape of x^ρ/ρ."""
        if x <= 1.0:
            return 0.0
        modulus = math.hypot(self.sigma, self.t) or 1.0
        return (self.weight * (x ** self.sigma)
                * math.cos(self.t * math.log(x) + self.phase) / modulus)


@dataclass
class AnswerLedger:
    """The answer, with every correction still visible underneath it."""
    x: float
    trend: float
    answer: float
    corrections: dict[str, float] = field(default_factory=dict)

    @property
    def loudest(self) -> tuple[str, float] | None:
        if not self.corrections:
            return None
        who = max(self.corrections, key=lambda k: abs(self.corrections[k]))
        return who, self.corrections[who]

    @property
    def share_of_loudest(self) -> float:
        """How much of the total correction one voice is. 1.0 = it is alone."""
        total = sum(abs(v) for v in self.corrections.values())
        if total == 0:
            return 0.0
        return abs(max(self.corrections.values(), key=abs)) / total

    def as_dict(self) -> dict:
        return {"x": self.x, "trend": round(self.trend, 4),
                "answer": round(self.answer, 4),
                "share_of_loudest": round(self.share_of_loudest, 4),
                "corrections": {k: round(v, 4) for k, v in self.corrections.items()}}


def explicit_answer(trend: float, doubts: Sequence[Doubt], x: float) -> AnswerLedger:
    """**answer = trend − Σ doubts.** The formula, used as the output rule.

    This is the one structural change RH makes to how an engine answers. The
    ordinary way is *gather the votes and average*. The formula's way is:
    take the trend, then **subtract every correction, each with its own size
    and its own rhythm**, and keep them all on the page. Nothing is voted away;
    a doubt that cancels this time is still there next time with a different
    phase.
    """
    parts = {d.who: d.at(x) for d in doubts}
    return AnswerLedger(x, trend, trend - sum(parts.values()), parts)


def walk(trend_fn, doubts: Sequence[Doubt], xs: Sequence[float]) -> list[AnswerLedger]:
    """Run the formula across a range of scales — the answer as it grows."""
    return [explicit_answer(trend_fn(x), doubts, x) for x in xs]


# ------------------------------------------------------------------- the demo

def _demo() -> None:
    """Two engines. Same voices, same rhythms. One has a doubt off the line."""
    voices = ["source", "witness", "memory", "doubt", "mask"]
    per = periods(voices)

    def trend(x: float) -> float:
        return x / math.log(x)          # the smooth part — carries no arithmetic

    stable = [Doubt(v, t=per[v], sigma=HALF) for v in voices]
    drift = [Doubt(v, t=per[v], sigma=(0.72 if v == "memory" else HALF)) for v in voices]

    print("RH AS CODE — the ½ is a stability law you can watch\n")
    print(f"{'x':>10} {'stable: loudest share':>24} {'drifting: loudest share':>26}")
    for x in (1e2, 1e3, 1e4, 1e5, 1e6, 1e7):
        a = explicit_answer(trend(x), stable, x)
        b = explicit_answer(trend(x), drift, x)
        print(f"{x:>10.0e} {a.share_of_loudest:>23.3f} "
              f"{b.share_of_loudest:>25.3f}  {b.loudest[0] if b.loudest else ''}")

    print("\nOn the line every voice stays one of the crowd. One voice at σ=0.72 "
          "\nends up being the answer by itself — and line_check names it:\n")

    # Sample densely and smooth: one sample per decade reads the cosine wobble
    # as slope and accuses voices that are sitting exactly on the line.
    xs = [10 ** (2 + 5 * i / 400) for i in range(401)]
    hist = {v: [explicit_answer(trend(x), drift, x).corrections[v] for x in xs]
            for v in voices}
    for verdict in line_check(hist, steps=xs, smooth=True, period_map=per):
        flag = "  " if verdict.on_line else "→ "
        print(f"{flag}{verdict.who:<10} {verdict.why}")

    print("\nSame engine, a run long enough to resolve every voice "
          "(x to 1e60) — the σ tightens onto the truth:\n")
    long_xs = [10 ** (2 + 58 * i / 2999) for i in range(3000)]
    long_hist = {v: [explicit_answer(trend(x), drift, x).corrections[v] for x in long_xs]
                 for v in voices}
    for verdict in line_check(long_hist, steps=long_xs, smooth=True, period_map=per):
        flag = "  " if verdict.on_line else "→ "
        print(f"{flag}{verdict.who:<10} σ={verdict.sigma:.4f}  "
              f"cycles/bucket={verdict.cycles:.2f}  resolved={verdict.resolved}")

    print("\nThe static half — one witness never owns the answer:")
    for ws in (["ledger"], ["ledger", "ledger"], ["ledger", "the letter"]):
        r = half_confidence(ws)
        print(f"  {str(ws):<28} {r.confidence:.3f}  {r.verdict:<7} {r.why}")

    dup = dict(per)
    dup["copy of memory"] = per["memory"]
    print(f"\nDegeneracy check: {degeneracy(dup)}  ← same beat = one voice twice")


if __name__ == "__main__":       # pragma: no cover
    _demo()
