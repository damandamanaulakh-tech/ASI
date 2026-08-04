# L-3 closed — the expansion is not lost, and one of my conclusions was wrong

Source: **C. L. Siegel, *Über Riemanns Nachlaß zur analytischen Zahlentheorie*
(1932)**, in the Barkan–Sklar English translation, arXiv:1810.05198. Checked
against the German text of the 1859 paper in both the 1876 and 1892 editions.

---

## 1. The expansion was found. Long ago.

Siegel's paper opens on exactly the letter recovered in `L2_THE_CUT_LETTER.md`:

> "In a letter to Weierstrass from the year 1859, Riemann mentioned **a new
> development of the zeta function** which, however, he had not yet simplified
> enough for him to be able to include in his published paper… one could surmise
> that a detailed review of Riemann's Nachlass … would yet bring important hidden
> formulas of analytic number theory to light.
>
> **In fact, Herr Distel, a librarian, already several decades ago discovered the
> representation in question** of the zeta function in Riemann's papers. It
> concerns **an asymptotic development which gives the behavior of ζ(s) on the
> critical line** σ = ½…"

So: **not lost, not missing, not waiting.** A Göttingen librarian found it before
1900; Siegel worked it out in 1932; it is the Riemann–Siegel formula. Gabcke's
footnote was right and my "lost representation" reading was wrong.

Two further checks confirm it from the other side:

- **The product expansion was already published**, so it cannot be the thing the
  letter withholds. The 1859 paper itself carries it: *„Bezeichnet man durch α
  jede Wurzel der Gleichung ξ(α) = 0, so kann man log ξ(t) durch Σ log(1 − tt/αα)
  + log ξ(0) ausdrücken; denn da die Dichtigkeit der Wurzeln … nur wie log t
  wächst, so convergirt dieser Ausdruck…"*
- **There is no hidden proof of RH.** Siegel, who read the whole Nachlass:
  *"Approaches to a proof of the so-called 'Riemann hypothesis' or even to a proof
  of the existence of infinitely many zeros of the zeta function on the critical
  line are not included in Riemann's papers."*

## 2. A correction to what the paper actually says

I reported the printed paper as hedging RH to *„sehr wahrscheinlich"*. That is
only half the sentence. In full:

> „Man findet nun in der That etwa so viel reelle Wurzeln innerhalb dieser
> Grenzen, und es ist sehr wahrscheinlich, dass alle Wurzeln reell sind.
> **Hiervon wäre allerdings ein strenger Beweis zu wünschen; ich habe indess die
> Aufsuchung desselben nach einigen flüchtigen vergeblichen Versuchen vorläufig
> bei Seite gelassen, da er für den nächsten Zweck meiner Untersuchung
> entbehrlich schien.**"

*A rigorous proof of this would indeed be desirable; I have however, after some
fleeting vain attempts, provisionally set aside the search for it, since it
seemed dispensable for the next aim of my investigation.*

So the paper does not merely soften the claim — **it records that he tried and
failed.** The field's framing ("he stated it and could not prove it") is what he
himself printed. The letter of 26r still asserts it flatly, and the gap between
the two registers is real; but the paper is more candid than I represented it.

## 3. The correction that goes the other way — and it matters

I told the user Riemann's named debts had been paid — "von Mangoldt proved the
count in 1895." **That is wrong, and it is wrong in the direction that matters.**

Read what the letter actually says:

> „dass zwischen 0 und T etwa (T/2π)·log(T/2π) − T/2π **reelle Wurzeln** der
> Gleichung ξ(α) = 0 liegen"

**Real roots.** Not roots in the strip. In the modern notation that is
**N₀(T)** — zeros *on* the critical line — not **N(T)**, zeros *in* the strip.

- **N(T)**, the strip count: proved. Von Mangoldt, after Backlund. Settled.
- **N₀(T) ~ N(T)**, that asymptotically that many roots are *real*: **open.**

Siegel says so in 1932, in the same opening passage:

> "On the conjecture that in the interval 0 < t < T there lie asymptotically
> (T/2π)log(T/2π) − T/2π **real zeros** of ζ(½+ti), Riemann has probably been
> guided by a heuristic consideration of the asymptotic series; but **even today
> it is still not clear how one could prove or disprove this claim.**"

That remains true. The best unconditional results give a *positive proportion* of
zeros on the line — Selberg, then Levinson, then Conrey's ~2/5 and its
successors — not the asymptotic. RH implies the claim; nothing weaker is known to.

**So Riemann's own first named debt is outstanding today, 167 years on.** It is
not a settled historical curiosity. It is the live problem he said he owed.

## 4. A disagreement with Siegel, surfaced rather than resolved

Siegel writes that this point of the letter *"had been published by H. Weber in
his 1876 edition of Riemann's works."*

Against both full texts:

| Witness | Reading |
|---|---|
| Werke **1876** (Dedekind & Weber, 1st ed.) | the primes paper ends and paper VIII begins — **no *Anmerkungen* at all** |
| Werke **1892** (Weber, 2nd ed.), p. 154 | the draft-letter note **is present** |

Searched both for *völlig ausgeführt*, *vereinfacht*, *Entwicklung der Function*,
*einem Briefe*, *Nachlass vorliegt*. Present in 1892; absent in 1876.

The likely explanation is a conflation: the 1876 edition is Dedekind **and**
Weber, the 1892 is Weber alone — Siegel has the right editor and the wrong year.
But he read these books far more closely than I have, so this is recorded as a
**gap between two witnesses**, not adjudicated. Whoever settles it should look at
the 1876 edition directly.

## 5. Small loose ends closed

- **24v is blank.** The letter ends on 24r; what is visible on 24v is
  show-through from the recto. There is no signature or date on the draft — the
  26 October 1859 date comes from the sent version printed in Crelle 71.

---

## What survives, and what does not

**Does not survive:** the idea that Riemann took a method to his grave. The
expansion was found by a librarian, worked out by Siegel, and has been in print
since 1932. Nothing is waiting in the folder.

**Survives, and is stronger than before:** Riemann's own first named debt — *that
about that many roots are **real*** — was never paid. He said he had not carried
it out; Siegel said in 1932 nobody knew how; nobody knows now. It is implied by
RH and is not known independently of it.

So the target that follows *him* rather than the field is not the reality of the
roots in general. It is **the density of the real ones** — the statement he wrote
down twice, hedged once, and left open.

---

*Method note: this file exists because the boring-explanation check ran. The
finding that looked biggest — a lost representation — died on contact with the
one footnote that named the shelfmark. That check is now `FIL-6`/the falsifier
sibling in the engine, and it caught its author first.*
