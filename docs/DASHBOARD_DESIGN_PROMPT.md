# Sourceborn Dashboard — Design Prompt

Paste this whole prompt into any design/build tool (Figma Make, Lovable, v0,
or a designer's brief). It describes the REAL system — every element maps to a
live API endpoint, so the design can be wired without inventing anything.

---

Design a dark, focused dashboard for **Sourceborn** — a private reasoning
engine that runs every question through **70 working nodes (SB-01..70), each
individually verified by one of 25 integrity nodes (URR-01..25)**, with
persistent per-node "brains" that grow with use. It is a private instrument
for ONE person, not a SaaS. Tone: calm, precise, sacred-technical — a
craftsman's cockpit, not a marketing page. Never use the words Stake,
Execution, Kernel, Tier, Pipeline, Ship, Deliverable. Use the system's own
vocabulary: Point Zero, Doubt, Witness, Wild Path, Halt→Loop, Intake,
Mystery, Invention, Non-Resolution.

**Layout: three vertical zones + a bottom dock.**

1. **Conversation (left, widest).** Chat thread; every past exchange is
   stored and clicking one reopens it complete with its walk. The answer card
   shows: Direct answer → Why (which of the user's own corpus files matched)
   → badges (classification · evidence tag · confidence · "70/70 nodes ·
   25/25 URR") → one falsifier line, always. For uploaded documents show a
   Numeric Audit strip (totals, negative corrections, "cannot certify
   without source contract") instead of psychology. Composer at the bottom
   with model picker (Claude / Grok / OpenAI / OpenRouter / Local-GPU).
   Data: POST /ask · GET /chats · GET /chat?id=

2. **The Walk (center) — the signature element.** A live vertical rail
   showing the per-node loop: `SB-N (name) → its URR (name): verdict ↩
   intake back to SB-N`, then SB-N+1. One row per node, 70 rows, streaming
   top to bottom as the run progresses. Each row carries a matrix chip
   ("URR 25/25" or "24/25 ⚑1"). Holds glow amber and expand into a
   What/Why/How/When card with three action buttons (Add data & re-run ·
   Re-loop · Approve). After SB-70: a compact "closing sweep URR-19..25"
   strip and a collapsible "support verifiers URR-01..07" strip.
   Data: walk.pairs / walk.closing / walk.support / walk.matrix from /ask

3. **Brain inspector (right).** Click any node id anywhere → its brain:
   name + role + which URR reviews it; the pyramid as a literal pyramid
   graphic (Node → Main 5-10 → Sub 10-20 → Micro 20-30) with real counts;
   the growing parameters (Runs_Completed, Patterns_Recognized,
   Verifications_Performed, Issues_Found, Human_Decisions,
   Connected_Points, Knowledge_Gained, brain_version) as stat tiles; a
   rollback button (restores the pre-weekly snapshot).
   Data: GET /brain?id= · POST /brain/rollback

**Bottom dock, three cards:** (a) *Your queue* — holds awaiting decision +
unfiled words with "Park as Sub/Micro" buttons (GET /unfiled, POST
/pyramid/park); (b) *Novelty* — latest NOVELTY_<date>.md with candidate
parameters and an Approve button each (GET /novelty, POST /novelty/run,
POST /novelty/approve); (c) *Master log* — sacred append-only feed
(GET /masterlog).

**Header pills:** model + status dot · brains 95 · memory <N> since <date>
(GET /persist — this is the data-loss alarm; if the date resets, make it
red) · weekly: "learned N links" (the Monday digest) · Backup ⬇ / Restore ⬆
(GET /export, POST /import).

**Style:** near-black background (#070809), one indigo→violet gradient
accent, emerald for pass, amber for holds, red only for the human-authority
line. Inter or similar. Density like a trading terminal but with generous
line-height in the conversation. Every count shown must be real — no
decorative numbers. Mobile: zones stack, walk rail collapses to
holds-plus-summary.

**The one law of this UI:** the human is the final gate. Every hold, merge,
novelty candidate, and rollback is a decision surface for the user — nothing
auto-resolves. Make those decision points the most touchable things on the
screen.
