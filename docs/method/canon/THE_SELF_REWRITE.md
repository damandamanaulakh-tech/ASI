# THE SELF-REWRITE — his goal named, four paths put to him, his choice: FULL AUTO

**Date:** 2026-09-03 · **Status:** his decision, executed the same day
**Code:** `src/sourceborn/selfpatch.py` (the pen) · `src/sourceborn/selfhome.py`
(the new home page) · routes `/`, `/selfpatch`, `POST /selfpatch/teach`,
`POST /selfpatch/revert`, `/reactor`

---

## 1. His words, verbatim

> forget the MOM and review the previous and tell me whr we r
> actually i will tell u what m looking
> as m feeding example and setting some rules in the system i want an app
> where i keep changing n it should rewrite its own code and make changes
> but as our turn app ASI is not able to do, suggest me and discuss how many
> options i have
> and accordignly the dashboard will prepared not what we have

Three facts inside that message, kept apart:

1. **The goal** — as he feeds examples and sets rules, the app should rewrite
   **its own code**, not only its own data.
2. **The honest state he named** — the app as it stood could not. True:
   `selfmake.py` grows a step *list* as data, `senses.py` and `growth.py`
   change behaviour through data, and every change to an actual `.py` file
   had come through a chat session, never from the app.
3. **The order of work** — options first, discussion, then the dashboard
   *prepared accordingly, "not what we have."*

## 2. The four paths put to him, as presented

| path | stated meaning | stated trade |
|---|---|---|
| **Staged assembly** (recommended to him) | data teaching live now; the app writes code patches, tests them, waits at a queue for his word; he lifts areas to self-merge later | his own Manual → Semi-Auto → Auto-Sustain law, applied to code |
| **Rules-as-data only** | no self-written code; teachings become live rows instantly, free, offline | new mechanisms still come through chat sessions |
| **Self-patch, full auto** | teach → the app patches itself → tests green → merges and deploys **with no word from you** | *collides with your rule 2 unless you relax it; guards/tests/canon stay protected at GitHub level* |
| **Agent-outside requests** | the app records change-requests; a coding agent turns them into PRs; his merge stays the gate | real code of any depth, but the app is not rewriting itself |

## 3. His choice

**"Self-patch, full auto."** Chosen with the collision named in the option
text he selected. His authority is rule 1 and it is absolute; the choice is
recorded here with its provenance, and reversing it is one word.

## 4. How rule 2 survives the choice — the reconciliation, on the record

Rule 2 of his standing orders: *"Never change the core without showing the
proposed change first and getting approval."* Its own text names what the
core is: **the spec, the principles, the node map — his words and his
banks.** The reconciliation is structural, not interpretive courtesy:

- **THE FIELD (law 1).** The pen writes only `src/sourceborn/*.py` minus
  five held files (`server.py` — the lock; `selfpatch.py` — the pen itself;
  `selfhome.py` — its witness; `safety.py` — rule 10; `llm.py` — the keys),
  plus `README.md`. `docs/` (canon and method), `data/` (his banks),
  `adopted/` (custody), `tests/` (the gate), `seed_corpus/`, `CLAUDE.md`,
  `render.yaml`, `app.py`, `.github/` are **default-deny, refused before
  anything runs**. Mechanisms are patchable without his word — that is what
  he chose. The law is not patchable at all.
- **THE GATE IS THE SUITE (law 2).** His word is not asked before a merge,
  so the whole test suite replaces it: the entire tree is copied aside, the
  patch applied to the copy, the full suite run there, exit status checked.
  Every law already pinned by a test — append-only ledgers, no selection
  paths, the bank never shrinking, NOT RECORDED never filled — therefore
  still binds every patch. And the pen may not edit `tests/`, so it cannot
  lower the bar it must clear.
- **APPEND ONLY (law 3).** Every teach is a ledger row: his teaching
  verbatim, the pen's why, full before/after of every file, the verdict, the
  commit sha. Refusals are filed with their reasons — a knock at an open
  door included. Git history keeps every pushed version; `revert()` is a
  **new commit** restoring what stood before, and the reverted row stays
  whole.
- **THE DOOR (law 4).** The pen drafts with his model key and pushes with
  his GitHub token. `teach`/`revert` refuse while `SB_ACCESS_PASS` is unset,
  because an open door would hand that pen to anyone with the URL. This is
  the Phase-0 front door he already accepted, on his credential — it gates
  strangers, not him. With the password set, his teach deploys with no
  further word, exactly as chosen.

## 5. What arms it — his three switches, in his hand

The machinery shipped whole and **inert**: it cannot push until he sets, in
Render's Environment tab, `SB_GITHUB_TOKEN` (fine-grained, Contents
read/write, the one repo), `SB_REPO` (owner/name), and a model key
(`ANTHROPIC_API_KEY` or another; `SB_PATCH_MODEL` picks the drafter). A
green patch before arming is **HELD-UNARMED with the whole patch kept in its
row** — arm later, lose nothing. So even in full auto, his staging law holds
in the only form left to it: turning the pen on is his physical action.

## 6. What this is NOT, said plainly

The pen runs **when he teaches**. It does not teach itself on a timer, and a
tick of the Phase-E scheduler cannot reach it — the machine feeding its own
output back into its own code is the **AUTO_SUSTAIN** question, which stands
at his gate untouched. The offline echo can never become a patch
(structurally: it does not parse as one), one teaching is at most three
files and 200KB, a race on the branch head is refused rather than forced,
and nothing pushed carries any model's name.

## 7. The dashboard, prepared accordingly

`/` is now **THE REWRITE**: the teach box; the arming panel (presence only —
no value ever leaves the environment); the never-touched map; and the feed —
every patch with its real diff computed from its own row, its suite verdict
or refusal, its commit link, and the one-click revert. *"Not what we have"*
did not mean deletion: the reactor stands whole at `/reactor`, the old desk
at `/desk`.

## 8. Left open, stated

- **AUTO_SUSTAIN for code** — the pen on the scheduler's loop — is not
  built and waits at his gate with the promotion question.
- A patch the suite cannot judge (behaviour no test pins) deploys on green
  like any other; the bar is exactly as high as the suite is. Raising the
  bar means adding tests, which reach the repo through sessions like this
  one — the pen cannot write them for itself.
- The ledger lives on the app's disk (`SB_ROOT/selfpatch/`). On Render the
  persistent disk keeps it across deploys; without one it resets — the git
  history, which cannot reset, remains the record of what actually shipped.
