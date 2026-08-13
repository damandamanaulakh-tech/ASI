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
| **04** | Make the weekly pull visible and cumulative | WKL | 1 day | **DONE** — `scheduler.run_weekly` is now the one job the daemon *and* the button both call; every run is its own dated file under `<root>/weekly/`, created with mode `"x"` so the filesystem — not a check-then-write — guarantees nothing is overwritten; `GET /weekly` (paged, `?offset=`) + `GET /weekly/file` serve the ledger; the panel lists runs with an *Older runs* page and states the true kept count; the pill reads three states; the permanently-blank MY PAGE row reads the truth; a failed novelty pass, a failed history write and a corrupt run file are all reported instead of swallowed. |
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
| **18** | Decide where the sequence kernel enters a live answer | ENG-4 | design | **HE PLACED IT** — his canon puts the entry at the **write-back / learning sequence**, and `patterns.review()` now creates exactly that (no reopen, prior version kept whole, new version references it). The place exists; the last step is his word that the bridge is confirmed. |
| **19** | Land the workbook to fill the 3,072 | BRN-3 | you | **his** — the importer (`ladder.save_registry`, merge-by-id, every version kept) is built and waiting for his file. 18 of 3,072 filled today, and the page says so. |
| **20** | Lock the parameter count | — | you | **CLOSED BY HIS RULING 2026-08-13: "3072 is the count."** The base HALT that stood since the 80/2,560 work is answered — he moved the base. Version ladder kept as versions, not drift. |

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
| 04 | Two pulls inside the same second produced the same filename — the second would have overwritten the first, in the very feature whose point is that nothing is overwritten | my own check before review | suffixed |
| 04 | **My suffix fix was still wrong**, and I called it done. `while os.path.exists()` then `open(...,"w")` is a check-then-write race; this app answers on threads *and* runs a daemon thread calling the same function. The reviewer reproduced 8–12 runs lost out of 24 concurrent pulls; I reproduced 7 of 12 lost. Real trigger: an hourly tick landing on a button press, or a double-click | review of the phase diff | mode `"x"` — the filesystem arbitrates; 12/12 survive under a thread barrier, and that test now guards it |
| 04 | `get_run` was the one reader without a `try/except`, so a run file truncated by a recycled process (which my own best-effort write can create) 500'd → and since `do_GET` has no handler, the connection just dropped | same | guarded; corrupt runs now show as `unreadable` in the ledger instead of breaking it |
| 04 | I claimed the panel "lists every run" — it silently stopped at 52, and `runs` was counted by parsing that same page, so the pill, the header and MY PAGE would all have started lying after a year (or 52 button presses), with the older runs unreachable | same | counted by `listdir`, never parsed; `?offset=` + an *Older runs* button reach the rest |
| 04 | The panel printed "it has never run" *under* a badge reading "overdue — last 2026-07-01" — on the exact upgrade path his live app is on. The two-state lie this item exists to remove, reintroduced in the empty-list branch | same | the two states now have two different sentences |
| 04 | Three numbers went into `innerHTML` unescaped. They come from disk, and `POST /restore` accepts `weekly/*.json` from any zip — so a restored backup could have run script in his dashboard | same | escaped; verified in a browser that a payload renders as text and injects zero nodes |
| 04 | I claimed one shared helper composed the label; it was three implementations in two languages that happened to agree | same | the server sends the phrase and the state word; the pill and MY PAGE only display them |

## WHAT EXISTS — the page he asked for (2026-08-13)

His words: *"i want to know the existence of my understanding in the code file and
i want to use the tool so i can know what u did"* → *"yes build it into the app as
a page i can open"* → *"rubric means paramters the 3000"*.

`GET /exists` — his understanding located in the code, row by row: **his words →
the file and line where it already lives → what state it is actually in** (RUNS ·
BUILT-NOT-WIRED · THIN · PARTIAL · ABSENT). Plus the four **absences** stated as
absences, and the four **seams** where the code and his word disagree, surfaced
rather than quietly decided.

**His ruling recorded: rubric = parameter = the 3,072.** So the rubric store was
never missing — `ladder.py` is it, and `save_registry` already versions every
edit. What is missing is that **18 of 3,072 carry anything**, and that a rubric
holds a name plus free text rather than how it is recognised and how it is graded.
The page reads that count from his registry live; it is never written by hand.

**The page verifies itself.** Every reference carries an anchor that must still be
present in the named module; the source is read on each open and the real current
line number is reported, or the reference turns red. A hand-written map of "where
things live" goes stale the first time a line moves — this one cannot. It caught
one of my own errors while being built (`file_item` does not exist; the function
is `file_finding`). 70 references, all resolving.

Two seams worth his word: `run_recursive(loops = 3)` against his *"we decided 5
loops and reducing"* — the **reducing is real** (it stops early when the product
stops changing), only the count differs, and it is unchanged until he says; and
the RGL sub-loops are **six**, not five.
