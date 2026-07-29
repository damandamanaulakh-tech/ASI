# FINAL CORE PLAN — Sourceborn / URR

One page. What stands, what's next, in what order, and who holds the key for
each step. This is the working plan — edits to it are edits to the plan.

## Where the engine stands (all verified on main, test-locked)

- **Per-node walk, no stages, no 70×25:** SB-N → **the seven filters** → intake
  back into SB-N → SB-N+1. 70 individual reviews per ask + a run-level sweep.
  Zero skips.
  *Req: "now we dont want 70-25 there, but i want more filters and fact kind of".*
- **The seven filters** — the path, run in order on every finding, every time:
  **Ground · Sequence · Source · Mask · Fact · Halt · Loop**.
  - **Source** is the two-witness pass. One witness caps at Medium *however
    good it is*; High needs two independent witnesses that agree; two that
    differ **HALT** — the gap goes to the human, never averaged, never picked
    between. A reprint/translation/quotation of one origin counts as **one**.
  - **Mask** is the gap itself: the space between what was said and what was
    shown. An ellipsis is treated as a witness that something was removed.
  - **Loop** hands each halt back as the next Point Zero.
- **The universal sequence** (`sequence.py`) — Ground · Pressure · Use ·
  Witness · Expression · Naming · Halt · Loop. The thing pre-exists the asking;
  the human act is step 5, finding a way to *say* it. Step 6 is where the name
  starts standing in for the thing — where the Mask forms.
- **Brains are memory, filters are method.** All 95 node brains stay
  configured and keep growing; the seven filters keep their own brains
  (FIL-1..FIL-7).
- **95 brains** with the core's parameters growing per run; pyramid filing
  (Node → Main → Sub → Micro); unparked words → human queue.
- **Identities in the core, not code:** `core/node_definitions.json` drives
  node names/purposes and the SB→URR pairing.
- **Memory forever:** every chat stored + reopenable; full-brain backup/
  restore; persistent-disk blueprint in render.yaml; optional **MongoDB**
  backend (set `SB_MONGO_URL`).
- **Weekly (Monday):** per-brain digest + NEW cross-brain connections
  learned, snapshot-first (rollback anytime).
- **Novelty pass:** hunts parameters that never existed → fresh
  `NOVELTY_<date>.md` → only the human's approval makes one real.
- **Corpus:** 217 of the user's files ship and auto-load; recall favors the
  user's own material.

## The gap that matters most (named honestly)

The words the user reads are still **one base-model draft**. The walk
verifies, files, flags, and remembers around the draft — it does not yet
**rewrite** it. Depth of answers is therefore bounded by base model + corpus,
not by the walk.

## Order of work

| # | Step | What it changes | Key holder |
|---|------|-----------------|------------|
| 1 | **Answer-shaping loop** — draft → node findings (doubt, inversion, contradictions, evidence, audit) → second model pass rewrites → re-anchor to Point Zero; loop until converged | The answer itself stops being "routine LLM" — the walk starts writing | User's go (costs 2–3 model calls/ask) |
| 2 | **Owner lock** — token login; owner-only writes; persona adapts to owner | "It must know only I am using it" | User's go |
| 3 | **Live keys + disk** — working model key, Tavily key, persistent disk mounted (or SB_MONGO_URL) | Eyes open; memory survives deploys | **User only** (dashboard actions) |
| 4 | **Node-behavior depth** — model-backed micro-pass for chosen nodes (Doubt, Witness, Inversion first) | Node findings become reasoning, not rules | User's go, node by node |
| 5 | **Corpus growth ritual** — keep feeding raw thoughts/holy books/examples; weekly digest compounds them | The clone's voice sharpens | **User only** |
| 6 | **Repo/service consolidation** — fold other project repos in | One home, more display space | Needs multi-repo session scope |
| 7 | **Dashboard redesign** — user designs from docs/DASHBOARD_DESIGN_PROMPT.md; wire to live endpoints | The cockpit matches the engine | User designs, engine wires |

## Standing rules (binding, from the session audit)

Every commit carries `Req:` lines quoting the user. No source, no insertion.
Forks in the user's own documents go to the user — never resolved silently.
"Done" only with same-message proof. Human authority absolute.
