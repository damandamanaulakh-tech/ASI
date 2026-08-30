# Sourceborn (URR / SBUR)

A **private, continuously-learning reasoning engine** that thinks by *example and
archetype* — **"eternal example, present fact; more parameters, more outcome."**

It is a **control layer around a base model** (your Claude key), not a new trained
model. It clones your voice, runs the **SB + URR** pipeline over a **pyramid of
local brains** (70 SB + 25 URR nodes), and **gets wiser every time you use it**.

## The phase programme (owner-set)

Full detail lives in Drive `ASI_BRAIN/00_README_MASTER.md` and in `docs/mainwork/`.
Status as of the current pass:

| Phase | What it is | State |
|---|---|---|
| **P-1** | The frame — 9 points. Points 6 & 7 dropped by the owner as repetitions | **RUNNING** — `docs/mainwork/asi/P1_ANSWERS_v1.md` |
| **P-2** | RH as the live running example | **HOLD** (owner) |
| **P-3** | The 50000 census walk and its rating | **LANDED** — 63,519 zeros, ledger exact, registered verdict fired |
| **P-4** | The K-style tree structure applied to RH | **HOLD** (owner) |
| **P-5** | Back to the hub for the 5 point zeros | **HOLD** (owner) |
| **P-6** | Compile everything; surface new nodes and connections | **RUNNING** — `docs/mainwork/asi/` |
| **P-7** | A new session that follows P-6 at full length | **HOLD** (owner) |
| **P-8** | The sequences, collected — SB, SB-URR, hunger, gravity and the rest | **DONE** — `docs/mainwork/THE_SEQUENCES.md` |
| **P-9** | *All files on daman.tech, for own pileup* | **THIS LINE** |
| **P-10** | Q-1 | **Yes** |
| **P-11** | The full ASI white paper | opens when the node registry stops minting new IDs |
| **P-12** | Three RH articles (a / b / c, c onward open-ended) | after P-11 |
| **P-X** | Ingest whatever he adds to repo releases, any time | `ASIwork` compiled — `docs/mainwork/asi/ASIWORK_COMPILE_v1.md` |

## The three memories
- **Reflex** — your fed corpus + example bank (*clone me*) → `persona.py`, `memory.py`
- **Instinct** — wisdom bank: holy books, proverbs, archetypes → `wisdom.py`
- **Eyes** — live fact (web/Tavily) → `engine.grounding` hook

## Try it (no install, no API key)
```bash
python -m sourceborn.demo                 # full offline walkthrough
python -m sourceborn "why does the small idea win? prove it"
PYTHONPATH=src python3 tests/test_engine.py   # 478 tests
```
Set `ANTHROPIC_API_KEY` to swap the offline stub for real Claude reasoning.

## Run it as a web service (dark chat UI)
```bash
python app.py                 # -> http://localhost:8000  (zero dependencies)
```
You get a dark chat page + a JSON API (`POST /ask`, `GET /health`) that shows the
answer **and** the engine view: matched examples, output lanes, halts, re-anchor,
and the SB/URR node trace.

## Deploy to Render (one click)
This repo ships a Render Blueprint (`render.yaml`). In Render: **New + → Blueprint
→ pick this repo**. It runs `python app.py` and binds `$PORT` automatically — no
build step (the engine is stdlib-only). Then in the Render dashboard add the env
var `ANTHROPIC_API_KEY` to turn on real Claude reasoning. (Render's disk is
ephemeral; to keep the brain's memory across deploys, enable the optional Render
Disk in `render.yaml` or move memory to a DB — see `docs/RECOMMENDATION.md`.)

**Lock the front door.** The app is private but has no password until you set one.
In the Render dashboard set **`SB_ACCESS_PASS`** to a strong password and the whole
app requires it — the browser prompts once (HTTP Basic auth), and `fetch`/`curl -u`
carry it automatically. `GET /health` stays open so Render's health check still
works. Leave `SB_ACCESS_PASS` unset and the app is open to anyone with the URL, so
**set it before you expose anything private.** Optional `SB_ACCESS_USER` (default
`sourceborn`).


## Feed your brain (continuous learning)
```bash
python tools/docx2txt.py yourfile.docx > yourfile.txt   # convert docs first
python -c "import sys; sys.path.insert(0,'src'); from sourceborn.ingest import ingest_folder; print(ingest_folder('path/to/corpus'))"
```

## Layout
| Path | What |
|------|------|
| `docs/SOURCEBORN_CORE.md` | the canonical merged spec (single source of truth) |
| `docs/RECOMMENDATION.md` | how to build it (phased) + honest "unrestricted" note |
| `engine/sourceborn_system_prompt.md` | paste-anywhere engine prompt for any chat model |
| `src/sourceborn/` | the runnable engine (nodes, params, memory, persona, wisdom, URR) |
| `tests/` · `tools/` | tests · docx→txt helper |

Your private brain is written to `.sourceborn/` (git-ignored — never committed).

## What's implemented (all 8 stages real, not scaffolded)
- **Stage 1** intake: raw-source lock, noise strip, Point Zero
- **Stage 2** Core Gate — six lenses (`core_gate.py`) → human-layer read
- **Stage 3** Doubt Engine · Falsifier · Witness (`doubt.py`)
- **Stage 4** Evidence ladder + source tags (`evidence.py`)
- **Stage 5** Dot-Connection + human-gated Merge (`dots.py`)
- **Stage 6** Synthetic Fuel Injector — 5 caged fuels (`fuel.py`)
- **Stage 7** Risk gate (`safety.py`), Reality Re-Anchor + Drift Control (`drift_guard.py`), Embodied Check, Non-Resolution Protector
- **Stage 8** Master Log, final output, weekly brain update (`scheduler.py`)
- **The loop** (`engine.run_walk`) — the real per-node walk: `SB-N → URR-N
  (review + verdict) → SB-N downloads the URR intake into memory → SB-N+1`.
  Auto-runs the whole chain, then every URR **hold** goes to a **human review
  queue** (approve / add data / re-loop). `run_recursive` (RGL) is kept too.
- **95 local brains** with full settings (`brains.py`); 3 memories (corpus/wisdom/live)
- **CI**: GitHub Actions runs the test suite on every push/PR

## HTTP API
All routes except `GET /health` require HTTP Basic auth when `SB_ACCESS_PASS` is set.
`GET /` UI · `GET /health` · `POST /ask {question,model,public}` (runs the
per-node SB↔URR walk; returns `walk.steps` + `walk.holds`) ·
`POST /review {question,id,action,data}` — the human review queue,
action = `approve` / `add_data` / `reloop` · `POST /ingest {name,text}` ·
`GET /brains` · `GET /brain?id=` · `POST /brain/settings` ·
`POST /brains/update` · `GET /graph`

**The split, and the layers standing on it** — 27 segments · 183 containers ·
3,483 rows on the 12-step spine, with the 3,204-row source bank untouched
beside it:
`GET /sbx` (the whole architecture) · `GET /sbx/step?n=` · `GET /sbx/container?id=` ·
`GET /sbx/nodes` (the node brain placed on the spine) ·
`GET /sbx/review` (nine checks that can fail) ·
`GET /sbx/wiring` (the twelve-layer table, live) · `POST /sbx/place {text}` —
one ask through every layer at once ·
`GET /archetype` · `POST /archetype/run {text}` — the books as generative
engines ·
`GET /trigger` · `GET /trigger/placements?id=` · `POST /trigger/run {text}` —
the Operational Trigger / State Vector on all 183 ·
`GET /link` · `GET /link?row=` · `POST /link/run {text}` — relations as
first-class counted objects ·
`GET /scale` · `POST /scale/run {text}` — the scale axis ·
`GET /readings` · `POST /readings/run {text}` — the nine intent readings, each
naming what would refute it

### Every route, generated from the server

A hand-typed route list goes stale the first time a route is added, so this one
is checked by a test (`test_the_readme_lists_every_route_the_server_serves`) —
if the server serves a route this list does not name, the suite fails.

**GET (84)**

`/adopted` · `/angles` · `/api/bank` · `/api/hud` · `/archetype` · `/artifact`
· `/asi` · `/asi/stats` · `/auto` · `/brain` · `/brains` · `/chat` · `/chats`
· `/combine` · `/desk` · `/diag` · `/engine` · `/exists` · `/exists/data` ·
`/expected` · `/export` · `/flow` · `/generation` · `/generation/packs` ·
`/graph` · `/growing` · `/growing/coverage` · `/growth` · `/health` ·
`/intents` · `/ledger` · `/library` · `/link` · `/loop` · `/macro` · `/map` ·
`/map/where` · `/masterlog` · `/maturity` · `/meaning` · `/memory/report` ·
`/micro` · `/naming` · `/nodes` · `/nodes/node` · `/nodes/path` ·
`/nodes/schema` · `/nodes/subgraph` · `/novelty` · `/novelty/file` · `/page` ·
`/page/data` · `/page/layout` · `/page/meta` · `/page/version` ·
`/page/versions` · `/patterns` · `/persist` · `/reading` · `/readings` ·
`/registry` · `/registry/activate` · `/registry/container` · `/reread` ·
`/rubrics` · `/runtime` · `/sbx` · `/sbx/container` · `/sbx/nodes` ·
`/sbx/review` · `/sbx/step` · `/sbx/wiring` · `/scale` · `/selfmake` ·
`/senses` · `/snapshots` · `/subjects` · `/trigger` · `/trigger/placements` ·
`/unfiled` · `/weekly` · `/weekly/file` · `/weighting` · `/words`

**POST (59)**

`/angles/run` · `/archetype/run` · `/artifact/generate` · `/artifact/grow` ·
`/asi/run` · `/auto/mode` · `/auto/tick` · `/brain/rollback` ·
`/brain/settings` · `/brains/update` · `/combine/run` · `/engine/ask` ·
`/engine/registry` · `/expected/run` · `/generate` · `/generation/run` ·
`/growing/grow` · `/growing/place` · `/growth/add` · `/growth/correct` ·
`/growth/seed` · `/import` · `/ingest` · `/intents/run` · `/ledger/kill` ·
`/ledger/run` · `/link/run` · `/loop/chain` · `/loop/run` · `/macro/run` ·
`/maturity/read` · `/meaning/sign` · `/nodes/approve` · `/nodes/recall` ·
`/nodes/remember` · `/nodes/write` · `/novelty/approve` · `/novelty/run` ·
`/page/save` · `/patterns/review` · `/pyramid/park` · `/reading/ask` ·
`/readings/run` · `/review` · `/rubrics/run` · `/runtime/run` · `/sbx/place` ·
`/scale/run` · `/selfmake/extend` · `/selfmake/propose` · `/selfmake/run` ·
`/senses/reject` · `/senses/teach` · `/snapshot` · `/subjects/generate` ·
`/subjects/grow` · `/trigger/run` · `/upload` · `/weighting/run`

Lineage: Raw Definition Engine → ARD / RGL → URR-07 → Secureborn → Sourceborn / SBUR
→ the 70-SB/25-URR "Omni" core. MIT licensed. See `docs/RECOMMENDATION.md`.
