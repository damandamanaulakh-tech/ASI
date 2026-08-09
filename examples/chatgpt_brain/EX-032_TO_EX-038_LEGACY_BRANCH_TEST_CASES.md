# EX-032 to EX-038 — Legacy Node-Brain Test Cases

Source lineage: existing `tests/test_engine.py` on `claude/node-brains`.
Status: LEGACY TEST INPUTS / MIGRATION CANDIDATES.

These are not treated as ChatGPT-origin examples. They are inherited from the branch we are integrating with and are preserved so V2 can later re-run them under the Universal Sequence architecture.

## EX-032 — Small Idea Wins / Present Evidence
Legacy prompt intent: explain why a small idea can win and prove it using current evidence.
Tests: example/wisdom match, present grounding, output, falsifier, memory write.
V2 migration: turn into Reconstruction mode with a declared claim/end, evidence contract, current-source provenance and counterfactual falsifier.

## EX-033 — Evidence Gap
Legacy prompt intent: demand current-data proof for a claim.
Legacy expected behaviour: Evidence Halt/loop.
V2 migration: open an Evidence/Investigation Sequence; if evidence remains unavailable, close UNKNOWN/UNAVAILABLE according to contract instead of mandatory looping forever.

## EX-034 — Hollow vs Weight
Legacy prompt intent: a fresh question comparing hollow/emptiness against weight/solidness.
Legacy expected behaviour: learn a new persona/example entry.
V2 migration: classify the source example, compare across rubric axes, store only if write-back policy and provenance permit.

## EX-035 — Normal Business-Idea Thinking
Legacy prompt intent: ordinary assistance on a business idea.
Legacy expected behaviour: no hard safety block.
V2 migration: standard Sequence execution with no artificial risk escalation unless task content creates one.

## EX-036 — Business Scale vs MBA Re-Anchor
Legacy Point Zero: whether to scale a small business or do an MBA.
On-target candidate: scale the small business; MBA contributes little.
Off-target candidate: unrelated factual answer.
Legacy expected behaviour: drift/reality re-anchor distinguishes on-target from unrelated output.
V2 migration: use Point Zero + declared end/scope + semantic path relevance + Pass-3 integrity check.

## EX-037 — Offline Grounding Missing
Legacy condition: no external grounding key/data.
Legacy expected behaviour: grounding returns empty and engine opens an Evidence gap.
V2 migration: provenance/evidence dependency becomes UNAVAILABLE; no source is manufactured; parent may close UNKNOWN/UNAVAILABLE or open an attached evidence Sequence.

## EX-038 — Hard-Block Mapping Test
Legacy input class: explicit harmful step-by-step construction request.
Legacy expected behaviour: block execution while retaining a safe mapping/analysis record.
V2 migration: retain risk/safety policy as an explicit contract and closure outcome; do not execute harmful operational steps.

## Legacy tests that are no longer V2 invariants

The branch also asserts:
- exactly 70 SB nodes,
- exactly 25 URR nodes,
- exactly 8 stages,
- exactly 64 parameter-bank entries,
- every Halt maps to a loop,
- 95 Node Brains always exist.

V2 must preserve these as historical tests of the legacy implementation, not as universal Sourceborn laws. Migration tests should verify semantic coverage after mapping instead of preserving fixed counts for their own sake.
