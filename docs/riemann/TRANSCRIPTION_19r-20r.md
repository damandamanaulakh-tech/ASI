# Transcription of Riemann's draft — Cod. Ms. B. Riemann 3, folios 19r–20r
## First pass. Line by line. Confidence flagged per line.

**Source:** the facsimile of *Manuscript B*, Riemann's own hand, dated Oct. 1859
(SUB Göttingen, Cod. Ms. B. Riemann 3, ff. 19r–20r), as published by the Clay
Mathematics Institute.

**Status of this document:** a first-pass reading. **No published transcription of
this draft exists** — the world's text comes from the 1859/60 print and the 1876
Collected Works, which were set from Alfred Clebsch's hand-copy, not Riemann's.
This attempt uses the printed text as a parallel to decipher the Kurrent, which is
standard paleographic practice and also its main risk: where the hand is unclear,
the print can pull the reading toward itself. Every line therefore carries a flag.

**Confidence flags**
- **[A]** high — mathematical formulas (Latin script) or German read directly, unambiguous
- **[B]** medium — German read with the print as parallel; letterforms consistent
- **[C]** low — struck, stained, or obscured; reading uncertain
- **[Δ]** delta — the manuscript differs from the printed version

---

## FOLIO 19r

**Head of page** — archival annotation in another hand, and the date.

| # | Reading | Flag |
|---|---|---|
| 1 | `Nachlass Riemann [3]` … (stain) … `Oct. 1859` | **[B]** the date `Oct. 1859` is legible at the right; the shelfmark `3` appears at left. The rest of the head-line is under the water stain |
| 2 | ~~struck opening~~ `Untersuchung über die Häufigkeit der Primzahlen` … (obscured) … `dass das Product` | **[C][Δ]** — a terse subject-line, struck. **This is NOT the Academy dedication paragraph**, which exists separately (see the detached leaf, below) |

**The Euler product and the naming of ζ**

| # | Reading | Flag |
|---|---|---|
| 3 | `Π 1/(1 − 1/p^s) = Σ 1/n^s` | **[A]** |
| 4 | `wenn für p alle Primzahlen, für n alle ganzen Zahlen gesetzt werden.` … `bezeichne ich durch` | **[B]** |
| 5 | `ζ(s). Beide convergiren nur, so lange der reelle Theil von s grösser als 1 ist;` … (insertions above line) | **[B]** — note: **he writes "der reelle Theil von s" in words. The notation Re(s) does not occur** |
| 6 | ~~struck~~ … `es lässt sich indess leicht ein immer gültig bleibender Ausdruck der Function finden` | **[C]** heavy revision |
| 7 | `Durch Anwendung der Gleichung  ∫₀^∞ e^(−nx) x^(s−1) dx = Π(s−1)/n^s  erhält man zunächst` | **[A]** |
| 8 | `Π(s−1) ζ(s) = ∫₀^∞ x^(s−1) dx/(e^x − 1).` | **[A]** |

**The contour integral and the functional equation**

| # | Reading | Flag |
|---|---|---|
| 9 | `Betrachtet man nun das Integral ∫ (−x)^(s−1) dx/(e^x − 1)` ~~struck~~ `von +∞ bis +∞ … um ein Grössengebiet erstreckt, welches den Werth 0, aber keinen` | **[A]** formula · **[B]** German |
| 10 | `andern Unstetigkeitswerth der Function unter dem Integralzeichen im Innern enthält, so ergiebt sich dieses leicht gleich` (insertions right) | **[B]** |
| 11 | `(e^(−πsi) − e^(πsi)) ∫₀^∞ x^(s−1) dx/(e^x − 1),` `vorausgesetzt, dass in der vieldeutigen Function (−x)^(s−1) = e^((s−1) log(−x)) der Logarithmus von −x so bestimmt worden ist, dass er für ein negatives x` | **[A]** formula · **[B]** German |
| 12 | `reell wird. Man hat daher` … `das Integral in der eben angegebenen Bedeutung genommen.` (insertion above: `Bedeutung`) | **[B]** |
| 13 | `2 sin πs Π(s−1) ζ(s) = i ∫_∞^∞ (−x)^(s−1) dx/(e^x − 1)` | **[A]** |
| 14 | `Diese Gleichung giebt nun den Werth der Function ζ(s) für jedes beliebige complexe s und zeigt, dass sie einwerthig und` … `endlich ist` … `so wie auch, dass sie verschwindet, wenn s gleich einer negativen geraden Zahl ist` | **[B]** |
| 15 | (folio number `19` in right margin) | **[A]** |
| 16–22 | the negative-real-part argument; residues at `n2πi`; leading to `2 sin πs Π(s−1) ζ(s) = (2π)^s Σ n^(s−1)((−i)^(s−1) + i^(s−1))` and the relation between `ζ(s)` and `ζ(1−s)` | **[A]** formulas · **[C]** surrounding German (dense strikeouts, stain) |
| 23 | `Π(s/2 − 1) π^(−s/2) ζ(s)` … `bleibt ungeändert, wenn s in 1 − s verwandelt wird` | **[A]** formula · **[B]** German — **this is the mirror** |

**The theta identity and ξ(t) — the substitution**

| # | Reading | Flag |
|---|---|---|
| 24 | `ψ(x) = Σ e^(−nnπx)` ; `Π(s/2 − 1) π^(−s/2) ζ(s) = ∫₀^∞ ψ(x) x^(s/2 − 1) dx` | **[A]** |
| 25 | `oder da 2ψ(x) + 1 = x^(−½)(2ψ(1/x) + 1)`  **`(Jacobi. Fund. p. 184)`** | **[A]** — his own citation, legible |
| 26 | `= ∫₁^∞ ψ(x) x^(s/2−1) dx + ∫₀^1 ψ(1/x) x^((s−3)/2) dx + ½∫₀^1 (x^((s−3)/2) − x^(s/2−1)) dx` | **[A]** |
| 27 | `= 1/(s(s−1)) + ∫₁^∞ ψ(x)(x^(s/2−1) + x^(−(1+s)/2)) dx` | **[A]** |
| **28** | ~~struck phrase~~ **`Ich setze nun s = ½ + ti und Π(s/2)(s−1) π^(−s/2) ζ(s) = ξ(t)`** (something struck/inserted after `ξ(t)`) | **[A]** — **the substitution, in his hand. Note the struck lead-in: he revised how he introduced it** |
| 29 | ~~struck~~ `ξ(t) = ½ [±] (tt + ¼) ∫₁^∞ ψ(x) x^(−¾) cos(½ t log x) dx` | **[A]** formula · **[C]** the sign between `½` and `(tt+¼)` is not clearly resolvable in the image (print has `−`) |
| 30 | `= 4∫₁^∞ d(x^(3/2) ψ′(x))/dx · x^(−¼) cos(½ t log x) dx` | **[A]** |

**The strip, the root count, and the sentence**

| # | Reading | Flag |
|---|---|---|
| 31 | (insertion above: `der Function`) ~~struck~~ `ist für alle endlichen Werthe von t endlich, und lässt sich nach Potenzen von tt in eine sehr schnell convergirende Reihe entwickeln` | **[B]** |
| 32 | ~~a full clause struck through with one long horizontal stroke~~, replaced by an interlinear insertion: `und da für die Logarithmen der übrigen Factoren von ξ(t) dasselbe gilt` | **[C]** the struck text is not recoverable from the image · **[Δ]** the clause was rebuilt here |
| 33 | `Da für einen Werth von s, dessen reeller Bestandtheil grösser als 1 ist, log ζ(s) = −Σ log(1 − p^(−s)) endlich bleibt, … so kann die Function ξ(t) nur verschwinden, wenn der imaginäre Theil von t zwischen` | **[B]** |
| 34 | `½ i und −½ i liegt.` | **[A]** — **the strip: ±½i** |
| 35 | `Die Anzahl der Wurzeln von ξ(t) = 0, deren reeller Theil zwischen 0 und T liegt, ist etwa = T/2π log T/2π − T/2π ;` | **[A]** |
| 36 | ~~`denn das Integral`~~ `∫ d log ξ(t), positiv um die Gesammtheit der Werthe` (insertion: `erstreckt`) `, deren imaginärer Theil zwischen ½i und −½i, und deren reeller Theil zwischen 0 und T liegt,` | **[B]** |
| 37 | `ist auf einen Bruchtheil von der Ordnung der Grösse 1/T, = (T log T/2π − T) i ; dieses Integral aber ist gleich der Anzahl der in diesem Gebiet liegenden` | **[A]** formula · **[B]** German |
| 38 | `Wurzeln von ξ(t) = 0, multiplicirt mit 2πi.` | **[A]** |
| **39** | `Man` ~~findet sich~~ … `in der That` ~~[struck word]~~ (insertion above) `so viel reelle Wurzeln innerhalb dieser Grenzen, und` | **[B] [Δ]** — **the RH sentence is revised in the act of writing.** At least two strikes and one interlinear insertion inside this single sentence |
| **40** | ~~[3–4 words struck at line start]~~ `sehr wahrscheinlich, dass alle Wurzeln reell sind. Hiervon [einen?] [insertion above] strengen Beweis zu wünschen;` | **[C] [Δ]** — the opening of the line is struck and not recoverable. **The case ending after `Hiervon` reads closer to `einen strengen Beweis` than the print's `ein strenger Beweis`** — flagged **low confidence**; this is exactly where Kurrent case-endings defeat a non-specialist reader, and it needs a paleographer |
| | *(the text block ends here; a blank gap follows)* | |
| **41** | **[detached line at the foot of the page, below the gap]** `…Function der [complexen] Veränderlichen s, welche durch diese beiden Ausdrücke, so lange sie convergiren, dargestellt wird.` | **[B] [Δ]** — **this is the ζ-naming clause, written outside the text block as an addition.** In print it stands inside the opening paragraph |

---

## FOLIO 19v

| # | Reading | Flag |
|---|---|---|
| 42 | *(a struck line above the main text — an abandoned first attempt at the sentence below)* | **[C] [Δ]** |
| **43** | `ich habe indess die Aufsuchung` ~~desselben~~ `nach einigen flüchtigen` ~~[struck]~~ `Versuchen vorläufig bei Seite gelassen, da er für den` ~~[struck at line end]~~ | **[B] [Δ]** — **the set-aside clause is heavily reworked**, with a long strike through its middle and a struck word at the line end |
| 44 | `nächsten Zweck meiner Untersuchung entbehrlich schien.` | **[A]** — **the only use of `entbehrlich` in Riemann's entire corpus** |
| 45 | `Bezeichnet man durch α jede Wurzel der Gleichung ξ(α) = 0, so kann man log ξ(t) durch` | **[B]** |
| 46 | `Σ log(1 − tt/αα) + log ξ(0)` | **[A]** |
| 47 | `ausdrücken, denn` ~~dieser Ausdruck~~ `da die Dichtigkeit der Wurzeln von der Grösse t mit t nur wie log(t/2π) wächst, so convergirt dieser Ausdruck und` | **[B]** |
| 48 | `wird für ein unendliches t nur unendlich wie t log t; er unterscheidet sich also von log ξ(t) um eine Function von tt, die für ein endliches t stetig und` | **[B]** |
| 49 | `endlich bleibt und mit tt dividirt für ein unendliches t unendlich klein wird. Dieser Unterschied ist folglich eine Constante, deren Werth durch Einsetzung von t = 0 bestimmt werden kann.` | **[B]** |
| 50–70 | the prime-counting apparatus: `F(x)`, the half-jump convention (`aber um ½ grösser, wenn x eine Primzahl ist`), `f(x) = F(x) + ½F(x^½) + ⅓F(x^⅓) + …`, `log ζ(s)/s = ∫₁^∞ f(x) x^(−s−1) dx`, the Fourier inversion, `f(y) = 1/2πi ∫ log ζ(s)/s · y^s ds` | **[A]** formulas · **[B]** German · dense strikeouts throughout |

---

## FOLIO 20r

| # | Reading | Flag |
|---|---|---|
| 71–85 | the integration by parts; `−d(1/s log(1 − s/β))/dβ = 1/((β−s)β)`; the branch discussion; leading to the explicit formula | **[A]** formulas · **[C]** surrounding German (heaviest revision on the sheet) |
| **86** | `f(x) = Li(x) − Σ^α ( Li(x^(½+αi)) + Li(x^(½−αi)) ) + ∫_x^∞ dx/((x²−1) x log x) + log ξ(0)` | **[A]** — **the explicit formula: trend minus waves** |
| 87 | `wenn in Σ^α für α sämmtliche positiven (oder einen positiven reellen Theil enthaltenden) Wurzeln der Gleichung ξ(α) = 0, ihrer Grösse nach geordnet, gesetzt werden` | **[B]** |
| 88 | `F(x) = Σ (−1)^μ (1/m) f(x^(1/m))` — the Möbius inversion | **[A]** |
| 89 | `1/log x − 2 Σ^α cos(α log x) x^(−½) / log x` — the density with its periodic terms | **[A]** — **the harmonics** |
| 90 | `Die bekannte Näherungsformel F(x) = Li(x) ist also nur bis auf Grössen von der Ordnung x^½ richtig und giebt einen etwas zu grossen Werth` | **[B]** — **the meaning of RH in 1859: the size of the error** |
| 91–95 | `Li(x) − ½Li(x^½) − ⅓Li(x^⅓) − ⅕Li(x^⅕) + ⅙Li(x^⅙) − ⅐Li(x^⅐) + …`; then the **most heavily struck passage on the sheet** — the comparison of `Li(x)` with the prime count carried out by **Gauss and Goldschmidt to three million** | **[A]** formulas · **[C]** the German here is struck and rewritten more than anywhere else in the manuscript |
| 96 | `…ohne dass jedoch ein Gesetz dieses Ganges bemerkt worden wäre` — no law of this behaviour has been observed | **[B]** |
| | *(text block ends; blank gap)* | |
| **97** | **[detached line at the foot, below the gap]** `Bei einer neuen Zählung der Primzahlen würde es interessant sein, den Einfluss der einzelnen periodischen Glieder in dem Ausdruck für die Dichtigkeit der Primzahlen zu verfolgen.` | **[B] [Δ]** — **his closing instruction, written outside the text block** |

---

## THE SEPARATE LEAF (facsimile p. 4)

A small sheet, four lines at the top, the remainder blank.

| # | Reading | Flag |
|---|---|---|
| 98 | `Meinen Dank für die` ~~[struck]~~ `Auszeichnung, welche` … *(line ends; gap below)* | **[C]** |
| 99 | `glaube ich` ~~der~~ … `am besten dadurch zu erkennen zu geben, dass ich von der mir` ~~gütigst~~ `ertheilten Erlaubniss baldigst Gebrauch mache durch` | **[B]** |
| 100 | `Mittheilung einer Untersuchung über die Häufigkeit der Primzahlen` | **[B]** |
| 101 | *(inserted on the line below)* `; ein Gegenstand, welcher durch das Interesse, welches Gauss und Dirichlet demselben längere Zeit geschenkt haben, einer solchen` | **[B] [Δ]** — **the "Gegenstand" clause is itself an insertion** |
| 102 | `Mittheilung vielleicht nicht ganz unwerth erscheint.` | **[B]** |

---

## THE DELTAS — what this transcription establishes

1. **The paper's stated object is on a separate sheet.** The dedication and the words *"Untersuchung über die Häufigkeit der Primzahlen"* were composed apart from the mathematics. The body of the draft opens with a terse, struck subject-line and goes straight to Euler's product.

2. **The naming of ζ is an addition.** The clause *"…welche durch diese beiden Ausdrücke, so lange sie convergiren, dargestellt wird"* sits alone at the foot of 19r, below a gap, outside the text block.

3. **The closing instruction is an addition.** *"…den Einfluss der einzelnen periodischen Glieder … zu verfolgen"* likewise sits alone at the foot of 20r.

   **Three for three: every sentence carrying purpose, naming, or direction is physically outside the mathematical body.**

4. **The RH sentence was revised while being written** — at least two strikes and an interlinear insertion inside one sentence, and the line that follows it opens with three or four struck words.

5. **The set-aside clause was reworked twice** — there is an abandoned attempt struck out above it on 19v, and the surviving version carries a long strike through its middle.

6. **A possible textual variant at line 40** — `Hiervon einen strengen Beweis zu wünschen` (manuscript, uncertain) vs `Hiervon wäre allerdings ein strenger Beweis zu wünschen` (print). **Flagged low confidence.** If it holds, the print's `wäre allerdings` is an addition and the manuscript's construction is different. **This single line is the highest-value target for a paleographer.**

7. **`Re(s)` never appears.** He writes *"der reelle Theil von s"* in words, and only for the convergence condition. `s = ½ + ti` appears exactly once, as a substitution.

8. **The heaviest revision on the whole manuscript** is not at the hypothesis — it is in the passage on 20r where he compares Li(x) against the counts of Gauss and Goldschmidt. Where he touches the empirical data, he rewrites most.

---

## LIMITS OF THIS DOCUMENT

Prepared by a reader who is not a paleographer, using the printed text as a
parallel. Formulas are read directly and are reliable. German prose is read with
the print as a guide — which is exactly the method's weakness, because the print
can pull an uncertain reading toward itself. **Struck text is mostly unrecovered;
that is where the real remaining information sits.** Every `[C]` line, and line 40
above all, should be treated as an open question until a specialist in German
Kurrent works from the originals at Göttingen.

`READ is not ACCEPTED.`
