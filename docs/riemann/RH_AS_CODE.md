# RH AS CODE

### Re(s) = ½ + ti used as a build specification. No proof of anything.

**The instruction.** *"i dont wanted any proof of anything / i want to use RH as a code /
my full work is there with u / forget about the world / i just want to use the theorem as
code, want to convert the whole work below and for that theory / so i can build something
easy."*

So this document stops arguing with mathematics and **spends** it. Articles 12a–12d asked
whether the hypothesis is true and what machine would explain it. That question is closed
here, not answered — **we take the three objects it hands us and use them as parts.**

Everything below is either **already in the engine** (RH supplies the reason it was right)
or **buildable now** (`src/sourceborn/rh_code.py`, 81 tests green). Nothing here claims a
result about zeta.

---

# 1 · THE ONE LAW

Strip the mathematics and the hypothesis is a **stability law**, and it is the only thing
from the whole Riemann walk that the engine actually needs:

> ## No single voice may ever outgrow the crowd.

A contributor sitting at **σ = ½** grows like √n. A contributor at **σ = 0.7** grows like
n^0.7 — and after enough steps it is louder than everything else *put together*. Then the
"answer" has one author wearing the costume of a council.

**"Every zero on the critical line" and "no single witness owns the answer" are the same
sentence.** One is written as a number you can measure. The other is a rule you have to
remember. This work replaces the second with the first.

That is the whole conversion. The rest is bookkeeping.

---

# 2 · THE TRANSLATION TABLE

Every object on the left is standard. Every object on the right is his, already built or
now buildable. `[READING]` — the mapping is a design decision, not a theorem.

| RH object | What it is | What it becomes here | Where it lives |
|---|---|---|---|
| **primes p** | the atoms; cannot be factored | **the raw facts / the sources** — irreducible, each counted once | `registry.add()`, corpus memory |
| **unique factorisation** | no prime is a product of others | **no node is a duplicate of another** — one ID per thing | `registry.add()` returns the existing ID |
| **log p** | the prime's period — how long before it comes round | **each voice's own rhythm** | `periods()` |
| **length degeneracy** | two orbits sharing a length kills the statistics | **two nodes sharing a beat are one node counted twice** | `degeneracy()` |
| **zeros ρ = ½ + it** | the corrections that fix the count | **the doubts** — each a correction to the running answer | `Doubt` |
| **½ — the real part** | how much power a correction carries | **the ceiling on any one voice** | `half_confidence()` |
| **t — the height** | the frequency; when it beats | **when the node fires** — the schedule, not the size | `Doubt.t` |
| **the explicit formula** | π(x) = main term − Σ over zeros | **answer = trend − Σ doubts**, ledger intact | `explicit_answer()` |
| **RH holds** | error stays inside √x | **the engine is stable; no author** | `line_check()` → all on-line |
| **a zero off the line** | one term grows like x^σ, σ>½, and swamps the rest | **DRIFT, with a name on it** | `line_check()` → `drifting()` |
| **the smooth term d̄(E)** | (1/2π)log(E/2π) — carries no arithmetic | **the trend** — the shape of the answer before any evidence | `trend` argument |
| **the oscillating term** | where every prime, every log p, the whole ½ lives | **the corrections** — where all the actual content is | `AnswerLedger.corrections` |

**The last two rows are the finding from 12d §8.1, turned into a build rule.** Every
attempt at the operator reproduced the smooth term and none ever derived the oscillating
one. In an engine that is the difference between *a fluent answer* and *an answer with
evidence in it*. **A run that only produces the trend has produced nothing** — it has
produced the shape of an answer. `explicit_answer()` will not let that pass silently: the
corrections are a separate field and you can see when they are empty.

---

# 3 · WHAT THIS SAYS ABOUT WORK ALREADY BUILT

Nothing in this section is new code. It is the reason the existing code was right, which
until now was *"because the owner said so"* — a one-witness justification, capped at
Medium by his own filter.

### 3.1 The Source filter — one witness caps at Medium

`filters.py` FIL-3. **RH's reason:** a single voice allowed full weight is a voice at
σ = 1. That is not "slightly overconfident" — it is the maximum possible drift. Capping at
½ is not caution, it is **the line itself.**

### 3.2 The Mask — two witnesses that differ HALT, and are never averaged

`witnesses.py`, FIL-4. **RH's reason:** averaging two differing half-weight voices
manufactures one full-weight voice that no source supports. It is the exact move the
critical line forbids — it *creates* a σ = 1 term out of two σ = ½ ones. The gap goes to
the human because **the human is the only thing entitled to sit above the line.**

That is also the standing order: *human authority is absolute.* RH says why the machine
must not simply take that authority for itself when the sources disagree.

### 3.3 The registry — an existing node is returned unchanged

`docs/mainwork/asi/registry.py`. **RH's reason** is 12d §8.3, and it is sharper than
tidiness: arithmetic surfaces show Poisson statistics rather than GUE **because their
length spectrum is exponentially degenerate.** Degeneracy destroys the statistics. The
primes are degeneracy-free *because of unique factorisation* — and that is exactly what
one-ID-per-thing buys. **Duplicate a node and you have not made the engine louder, you
have made it deaf.**

### 3.4 The eight steps, and why step 6 is the dangerous one

`sequence.py`. Step 6 is NAMING — the name begins to stand in for the thing. In this
translation, a name is a voice that acquired weight without acquiring sources. It is the
generic way something climbs off the line: not by lying, by **being repeated.**

### 3.5 HALT → LOOP

`halt_map.py`, FIL-6/FIL-7. **RH's reason:** a doubt that cancels at this scale is still
there at the next one with a different phase. `Doubt.at(x)` is periodic — it *returns*.
Nothing is voted away, so a halt cannot be closed by being outvoted, only by being
answered.

---

# 4 · WHAT IS NEW AND BUILDABLE — `src/sourceborn/rh_code.py`

Five parts, 428 lines, no dependencies beyond `math`. Run it:

```
PYTHONPATH=src python3 -m sourceborn.rh_code
```

### 4.1 `line_check()` — the drift detector

The one genuinely new instrument. Feed it each voice's contribution history across a
growing run; it fits the growth exponent σ and reports **on-line or off-line, by name.**

Measured on the demo — five voices, one deliberately built at σ = 0.72:

| voice | built at | measured | verdict |
|---|---|---|---|
| memory | **0.72** | **0.7201** | **OFF THE LINE — named** |
| mask | 0.5 | 0.5001 | on the line |
| doubt | 0.5 | 0.4996 | on the line |
| source | 0.5 | 0.4994 | on the line |
| witness | 0.5 | 0.4993 | on the line |

And the answer itself, at x = 10⁷: with everything on the line **no voice holds more than
0.30 of the correction**; with one voice at 0.72, that voice holds **0.914 of it.** The
engine still prints five contributors. There is one.

**That is the picture worth keeping.** Drift does not announce itself by producing a wrong
answer. It produces a *confident* answer with the crowd still visible in the margin.

### 4.2 `envelope()` — and a defect found while building it

The first version of the detector **cried wolf**: voices constructed at exactly ½ came
back at 0.596 and were accused of drift. Cause: a correction is `x^σ·cos(t log x + φ)`,
and a line fitted through raw samples reads the **wobble as slope**.

`|cos|` averages to 2/π — a constant — so bucketing nearby scales and averaging `|value|`
recovers `x^σ` cleanly. But the bucket has to cover a whole cycle, and that is a statement
about **how long the run is:**

| cycles per bucket | worst error on an on-line voice |
|---|---|
| 0.21 | 0.032 |
| 0.76 | 0.0041 |
| 2.46 | **0.0007** |

**The accuracy is set by the length of the run, not by the code.** So `line_check()`
reports its own resolution and says, per voice, how much longer the run must be:

> `[UNDER-RESOLVED: the run covers only 0.21 of this voice's cycle per bucket; σ is ±0.03
> at best. Lengthen the run to ≥ 54.4 in log x before trusting this row]`

An under-resolved σ is **reported as under-resolved, never rounded into something
reassuring.** That is FIL-6 applied to the instrument itself.

### 4.3 `explicit_answer()` — the output rule

**answer = trend − Σ doubts.** The ordinary way to combine votes is to average them, which
is the forbidden move from §3.2 performed at scale. The formula's way: take the trend, then
subtract **every** correction, each with its own size and its own rhythm, and keep them all
on the page. `AnswerLedger.corrections` survives the run.

### 4.4 `half_confidence()` — the ½ as a ceiling

| witnesses | confidence | verdict |
|---|---|---|
| none | 0.0 | nothing to stand on |
| one | **exactly ½** | capped |
| several agreeing | 1 − 2⁻ⁿ — rises, never reaches 1 | held |
| two that differ | **½, HALT** | the gap returned as a Mask |

Agreement earns. It never concludes.

### 4.5 `periods()` / `degeneracy()` — the rhythm and the duplicate check

Each voice takes the next prime; its period is `log p`. Distinct primes have rationally
independent logarithms, so **no two voices can land on the same beat by accident.**
`degeneracy()` returns any that do — each group is one voice counted twice.

---

# 5 · THE EASY THING TO BUILD

He asked for something easy. This is the smallest build that uses all of the above and is
worth having on its own.

> ## THE LINE CHECK — a drift meter on the engine he already runs.

Not a new engine. A meter bolted to the existing one.

1. **Every run, record what moved the answer.** Each node's contribution, per run. That is
   one row per node per run — the engine already computes it inside `run_walk()`.
2. **Give every node its period** from `periods()`. Once, at registry time.
3. **After every N runs, call `line_check(..., smooth=True, period_map=...)`.**
4. **Show two numbers on the dashboard:** the share held by the loudest voice, and the
   names of anything off the line.
5. **When a name appears, HALT and hand it over** — the existing FIL-6/FIL-7 path, no new
   machinery.

**What it buys:** the engine gets an answer to *"is it still mine, or has one node quietly
become the author?"* — measured, not asserted. That is the anti-divert rule with an
instrument behind it instead of a promise.

**What it costs:** one number stored per node per run, and enough runs to resolve the
slowest node. §4.2 says exactly how many, per node, and refuses to pretend before then.

**Where it goes:** `line_check` is a pure function over stored history. It needs no model
call, no key, no network. It runs offline with the rest of the engine.

---

# 6 · WHAT THIS DOES NOT CLAIM

- **No proof.** Nothing here is evidence for or against the Riemann Hypothesis, and no part
  of it depends on the hypothesis being true. What is used is the *shape* of the statement,
  which is available whether or not it holds.
- **Not his four candidates.** Article 12c's reading — quantum primary, time and
  computation its consequences, ASI its silhouette — is untouched here. This document does
  not decide it and does not need it.
- **The mapping is a reading, not a result.** `[READING]` Primes-as-facts and
  zeros-as-doubts is a design choice. It earns its place by producing a working instrument,
  not by being derived from anything.
- **The demo is a demonstration, not a measurement of his engine.** Five synthetic voices
  with a planted drift. Running it on real node histories is step 1 of §5, and has not been
  done.
- **The engine has not been changed.** `rh_code.py` is a new module with its own tests.
  Nothing in `engine.py`, `filters.py` or `witnesses.py` was touched.

---

### Files

- `src/sourceborn/rh_code.py` — the five parts, plus `python -m sourceborn.rh_code`
- `tests/test_engine.py` — 9 tests for this module; 81/81 green
- One fix taken along the way: `_run_all()` sat mid-file, so tests appended after it were
  defined too late to be collected and were silently never run. Runner moved to the end.
