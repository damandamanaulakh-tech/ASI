# ChatGPT Sourceborn Project — Decision Log

This log captures explicit architecture decisions from the currently accessible Sourceborn ChatGPT project conversation. It is not a substitute for raw chat transcripts.

## D-001 — Unified identity
Name: `Sourceborn ASI`.
Human, AI, Holy Books, Sequence, Nodes, Brain, Memory, examples, RH and the live app are parts of one Sourceborn ASI system rather than unrelated projects.

## D-002 — Phase structure

```text
Phase 1  — define Universal Sequence, reverse + available material
Phase 2  — define Human / AI / Holy Books / ASI parameters, sub-parameters, containers, elements
Phase 2A — upload/adopt source files into repository assets
Phase 3  — Nodes and their Brain/Memory
Phase 4  — integration examples, especially RH, linking Sequence + nodes + brain + elements + rubrics
Phase 5  — live app testing and editable IDs/links/structure
```

## D-003 — No single giant coding command
Development is split into focused code sessions/modules that converge in one repository and are tested for cross-session gaps.

## D-004 — Core intelligence ownership direction
The target Sourceborn architecture should not depend on external commercial LLM/API intelligence as its core. A small proprietary corpus is acceptable if the architecture, relationships, examples, memory and verification are Sourceborn-owned. External models may exist only as optional adapters/testing tools unless explicitly re-approved.

## D-005 — Repository becomes durable system of record
Chat context is working context. Canonical IDs, mappings, schemas, decisions, examples, tests, registries and migration history belong in the repository.

## D-006 — Human/AI/Holy Books keep native structure
Universal Sequence is the runtime grammar. Human, AI, Holy Books and other domains attach through bindings; they are not flattened into the Sequence.

## D-007 — Holy Books are mandatory first-class architecture
A Human + AI + Meta-AI + ASI technical stack without Holy Books/civilizational source memory is considered incomplete for Sourceborn and risks collapsing back toward a normal LLM architecture.

Holy Books must preserve:
- raw source,
- language/translation,
- exact source location,
- commentary/exegesis,
- narrative/rule/symbol extraction,
- Sourceborn interpretation,
- provenance and contradiction state.

## D-008 — Universal Sequence is graph grammar, not fixed stage chronology
Reverse → Forward → Reverse validation remains central, but actual instance order is chosen by the causal/dependency/logical graph.

## D-009 — Maximum rubrics, controlled sub-parameter creation
Use many orthogonal rubric dimensions to split data, but promote a split into a permanent sub-parameter only when it changes machine behaviour such as trigger, threshold, dependency, evidence, identity, controller, result, closure, memory, verification or downstream action.

## D-010 — Brain branch integration
Current ChatGPT architecture work is integrated into `damandamanaulakh-tech/ASI` branch `claude/node-brains`, not the Grok-default branch. Existing branch history is preserved; new work lives under explicit ChatGPT V2 integration paths until migration is approved.

## D-011 — Example bank is first-class
Every usable example should receive a stable example ID, source/provenance, purpose, Sequence mapping and later parameter/node/rubric bindings. Missing historical examples remain gaps rather than being regenerated from memory.

## D-012 — RH remains a major integration test
RH is intended to demonstrate the Sourceborn core by linking Sequence, nodes, brain, memory, parameters, elements, rubrics, evidence and verification. Current accessible material does not contain the complete RH example, so no synthetic reconstruction is promoted as the user's original RH reasoning.
