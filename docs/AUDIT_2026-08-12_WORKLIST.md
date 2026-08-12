# THE WORK LIST — audit of 2026-08-12, worked one at a time

His ask: *"i full detial so i can at least work one by one on each pending node."*

The audit itself was delivered as a report. **This file is the queue, in the repo,
next to the code, so each item's status is updated in the same commit that closes
it.** The 20 items and their titles are the audit's own, verbatim — nothing
renamed, nothing dropped, nothing reordered.

His standing order: *"go phase wise, and finish the all pending / slow and steady /
every folder also must be updated to snyc the new works."*

Discipline for every item: **build → verify on a live socket → independent
adversarial review of the diff → fold the findings → then offer it for merge.**
The review's findings are recorded here too, including my own bugs.

| # | Item (audit's words) | Ref | Size | Status |
|---:|---|---|---|---|
| **01** | One auth gate over all 37 routes | EXP-1, EXP-2 | 1 hr | **DONE** — `server.basic_auth_ok` + `_guard`; every route but `GET /health` needs Basic auth when `SB_ACCESS_PASS` is set. Unset = open, so local dev is unchanged. **His action: set `SB_ACCESS_PASS` in Render** or the lock is dormant. |
| **02** | Split the private corpus out of git | EXP-3 | decide | **HIS CALL, MADE — "make the repo private."** That is his own action in GitHub Settings → Danger Zone; I cannot flip it from here. The corpus is untouched by my word. Until it is private, `seed_corpus/` (217 files: real name, personal email, employer, papers marked *not for publication*, legal correspondence) is world-readable. |
| **03** | Record and persist the selection sequence | SEL | 4 hr | **DONE** — ordered `{a,id,at}` moves survive reload, ride to the server, land on the chat record and the master log; forced picks are never truncated away; `dropped_by_cap` is surfaced instead of hidden. |
| **04** | Make the weekly pull visible and cumulative | WKL | 1 day | **DONE** — `scheduler.run_weekly` is now the one job the daemon *and* the button both call; every run is its own dated file under `<root>/weekly/` (never overwritten, same-second collisions suffixed); `GET /weekly` + `GET /weekly/file` serve the ledger; a real panel lists every run; the pill reads three states; the permanently-blank MY PAGE row reads the truth; a failed novelty pass is now visible instead of swallowed. |
| **05** | Send a real model; stop the echo leak; stop learning it | ENG-1 | 2 hr | open |
| **06** | Wire the four dead filters to their own signals | ENG-2 | 2 days | open |
| **07** | Resolve the URR nodes — run them or retire them | ENG-3 | 1 day | open |
| **08** | Find out why 90 brains stay empty | BRN-1 | investigate | open |
| **09** | Guard MY PAGE's table renderer | PG-1 | 30 min | open |
| **10** | Fix MY PAGE's zero-library, card renderer, blank weekly row | PG-2 | 1 hr | **partly closed by 04** — the blank weekly row is fixed and tested. The zero-library and card-renderer branches remain. |
| **11** | Make THE ENGINE honest about what it fed the engine | PG-3 | 2 hr | **partly closed by 03** — one activation, real lit-set, forced picks never silently dropped. The promised upload control remains. |
| **12** | Fix the misleading labels | — | 2 hr | **partly closed by 04** — the weekly pill no longer says "active" forever after one run. The `/25`-that-is-really-`/7` and the K₉₅/K₇₀ mismatch remain. |
| **13** | Close the button traps | — | 3 hr | open |
| **14** | Wrap `do_GET` so a bad query returns an error, not a dropped connection | — | 2 hr | open |
| **15** | One correct number, everywhere | — | 2 hr | open — the test count is stale in several docs; README still advertises the killed 70×25 matrix. |
| **16** | Clean the corpus | COR-1 | ½ day | open — **blocked behind 02**; I do not touch the corpus without his word. |
| **17** | CI on pytest with a lint step | — | 1 hr | open |
| **18** | Decide where the sequence kernel enters a live answer | ENG-4 | design | **his** — `seq_kernel.py` is validated code with zero importers; the LAW-formation bridge is unbuilt by design until he places it. |
| **19** | Land the workbook to fill the 3,072 | BRN-3 | you | **his** — the importer (`ladder.save_registry`, merge-by-id, every version kept) is built and waiting for his file. 18 of 3,072 filled today, and the page says so. |
| **20** | Lock the parameter count | — | you | **his** — 2,560 / 2,592 / 3,072 still contested across his own documents. One word closes it. |

## What the honest state is, after 01 · 03 · 04

- The front door has a lock, and it is **not yet turned** — that needs his Render
  env var.
- The repo is **still public** at the time of writing. Item 02 is his hand.
- The two gaps he named himself — the selection sequence and the weekly pull —
  are both closed, tested, and verified on a live socket.
- **The reasoning core is still mostly unwired**: the offline model echoes the
  prompt (05), four of the seven filters return `"pass"` unconditionally (06),
  the 25 URR review nodes are never called (07), and 90 of 95 brains hold no
  memory (08). Items 05–08 are the ones that make the app think. Nothing in
  01/03/04 changed that, and this file will not pretend otherwise.

## Bugs of mine the reviews caught, on the record

| Item | My bug | Caught by | Fixed |
|---|---|---|---|
| 01 | A non-ASCII `SB_ACCESS_PASS` made `hmac.compare_digest` raise → uncaught → 500 → the app bricked for everyone, including him | review of the phase diff | byte-comparison; verified live returns 401, not 500 |
| 01 | RFC 7617 says the auth scheme is case-insensitive; I compared it case-sensitively | same | fixed + tested |
| 03 | The `master_log` selection write sat *after* the answer was saved — an I/O fault would 500 a request whose answer was already on disk, so his retry would duplicate it | same | wrapped; compact summary instead of the full move array (which also fixed O(N²) log growth); verified by simulating a full disk |
| 03 | Self-XSS in the unescaped verb fallback in `drawMoves` | same | escaped |
| 04 | Two pulls inside the same second produced the same filename — the second would have overwritten the first, in the very feature whose point is that nothing is overwritten | my own check before review | suffixed; tested |
