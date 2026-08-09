# Migration Conflicts — Existing Node-Brain Core → ChatGPT Brain V2

Status: REVIEW / EXPLICIT MIGRATION REQUIRED

This file prevents the new integration from silently pretending that the older `docs/SOURCEBORN_CORE.md` and the newer Universal Sequence / Phase-2 architecture are identical.

| Existing branch concept | V2 position | Migration action |
|---|---|---|
| Sourceborn is a control layer around a Claude/base model | Sourceborn target architecture must not depend on an external commercial LLM/API as its core intelligence | Preserve as historical implementation mode; mark external model as optional adapter/runtime, not Sourceborn identity |
| Fixed 70 SB + 25 URR points | Universal Sequence is graph grammar; ASI Nodes are service classes and instance order is graph-selected | Preserve old IDs as legacy node templates; map to V2 service roles; do not force all cases through 95 points |
| Any point can loop back to any earlier point | Closed Sequence instances never reopen; retries/repair/retest create new Sequence IDs | Replace execution-level loop semantics with reference/attached/new Sequence semantics; keep graph references as historical links |
| Halt must always open a loop before stage closes | Failure/unknown/unavailable can be valid terminal closures when contract permits | Convert Halt types into resolution policies, not mandatory endless continuation |
| Holy books/proverbs/myths live primarily in `wisdom.py` seed examples | Holy Books become a first-class native registry with source text, translation, commentary, interpretation and Sourceborn interpretation separated | Migrate seed examples into a review queue; do not promote paraphrases to canonical scripture without source references |
| Three memories: Reflex / Instinct / Eyes | V2 memory fabric has working, trace, fact/result, path, failure, context, rule/promise, procedural, actor-view, narrative, compression and closure stores | Keep Reflex/Instinct/Eyes as optional high-level aliases/views over typed stores |
| Evidence tags FACT/REVIEW/SYNTHETIC/RUMOR/OPEN | V2 uses claim-level provenance, epistemic status, contradiction links, confidence and proof debt | Map old tags into richer claim records; retain original tag as legacy metadata |
| `Point Zero` is defined as unlimited starting position before forced selection | V2 separates raw ask/source lock, mode/end/scope lock, prior reality and observation window | Preserve legacy Point Zero semantics as a source/intake state; avoid mixing it with current-world evidence |
| RGL re-opens up to 100× | No historical reopen | Each RGL iteration becomes a new Sequence instance linked by NEXT/REFERENCE/ATTACHED relation |
| Weekly brain update every Monday | V2 learning/version changes are explicit Sequences and migration events | Keep scheduled maintenance only as an operational policy, never as a truth/learning guarantee |
| One Master Log records everything | V2 uses multiple typed ledgers plus audit/event log | Master Log becomes audit index over typed stores, not a single overloaded database row type |
| Wisdom example matching chooses deepest example | V2 may use examples, Holy Books, Human, AI and other registries as evidence/pattern sources, but must preserve source/interpretation layers and run R-F-R validation | Keep example matching as one synthesis service, not the whole reasoning definition |

## Non-destructive rule

Do not delete legacy files to make migration look complete.
Every replacement should be recorded as:

```text
legacy_object
→ v2_object
→ semantic differences
→ migration status
→ tests
→ human approval
```
