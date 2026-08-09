# ChatGPT Brain V2 Integration Layer

Status: ACTIVE INTEGRATION / NOT YET CANONICAL REPLACEMENT

This directory records the Sourceborn ASI architecture developed in the ChatGPT Sourceborn project and integrated into the existing `claude/node-brains` branch without deleting or rewriting the older lineage.

## Authority
- Raw project/source files remain immutable source material.
- This integration does not silently rewrite existing `docs/SOURCEBORN_CORE.md`.
- Conflicts between the older 70-SB/25-URR control-layer architecture and the newer Universal Sequence / Phase-2 architecture are explicit migration work.
- No Grok branch content is treated as authority for this integration.
- No external LLM/API is assumed to be the permanent Sourceborn brain.

## Current integration set
1. `SOURCEBORN_UNIVERSAL_SEQUENCE_V2_FINAL_REVIEW.md`
2. `SOURCEBORN_ASI_PHASE2_ADOPTION_CONFIG.md`
3. `AI_CAPABILITY_FAMILIES_TO_SOURCEBORN_CONTAINERS.md`
4. `FULL_ARCHITECTURE_FLOW.md`
5. `/examples/chatgpt_brain/` — example bank extracted from currently accessible ChatGPT project material and uploaded Sourceborn files.

## Core relationship
Universal Sequence = execution grammar.
Human / Holy Books / AI / other registries = native domain knowledge and parameter registries.
ASI Nodes = runtime services.
Memory / claims / evidence / gaps / contradictions / proof debt = persistent control fabrics.
Holy Books are a first-class source/civilizational knowledge layer, with source text, commentary, interpretation and Sourceborn interpretation kept separate.

## Migration rule
Do not delete the older core merely because V2 exists.
Create explicit migration mappings:
OLD_OBJECT -> V2_OBJECT -> STATUS -> REASON -> TESTS -> APPROVAL.
