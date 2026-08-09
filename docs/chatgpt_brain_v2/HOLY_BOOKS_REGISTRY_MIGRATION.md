# Holy Books Registry Migration

Status: FIRST-CLASS DOMAIN / SOURCE REVIEW REQUIRED

The existing node-brain branch already contains a `src/sourceborn/wisdom.py` seed bank with examples labelled Bhagavad Gita, Ecclesiastes, Guru Granth Sahib, Quran, Gospel, Tao Te Ching, Aesop and Proverb.

These existing entries are valuable lineage, but they must **not** be treated as canonical Holy Book source records yet because the seed structure stores only:

```text
source label
pattern interpretation
short text/example
comparison axes
```

The Sourceborn Holy Books registry requires a stricter separation:

```text
RAW SOURCE TEXT
→ source identity
→ book / chapter / verse / section / location
→ language
→ edition / translation
→ textual variant if relevant
→ commentary / tafsir / exegesis source
→ historical/traditional context
→ narrative/event/person/rule/symbol extraction
→ Sourceborn interpretation
→ Sequence binding
→ ASI Node binding
→ evidence / contradiction / proof-debt state
```

## Migration rule for existing `wisdom.py`

Each old seed becomes a `HOLY_BOOK_CANDIDATE` or `WISDOM_CANDIDATE`, not an approved source item.

Required migration states:

```text
LEGACY_SEED
→ SOURCE_IDENTITY_CHECK
→ EXACT_LOCATION_CHECK
→ TEXT/PARAPHRASE CLASSIFICATION
→ TRANSLATION/EDITION CHECK
→ INTERPRETATION SPLIT
→ SOURCEBORN_BINDING
→ HUMAN REVIEW
→ APPROVED / REJECTED / RETAINED_AS_NONCANONICAL_WISDOM
```

## Domain containers to build

1. Canon / Source Identity
2. Text Units
3. Translation / Language
4. Commentary / Tafsir / Exegesis
5. Narratives / Events / Persons
6. Law / Ethics / Norms / Duties / Prohibitions / Permissions
7. Principles / Values / Meaning
8. Promise / Covenant / Commitment
9. Exception / Override / Priority Conflict
10. Ritual / Practice / Worship
11. Symbol / Metaphor / Parable / Wisdom
12. Actor View / Knowledge Distribution
13. Cause / Consequence / Test / Trial
14. Memory / Transmission / Preservation
15. Observer / Writer / Recorder Layer
16. Historical / Traditional / Jurisprudential Context
17. Era / Closure / Succession
18. Cross-Text Relations
19. Contradictions / Apparent Contradictions / Context Splits
20. Sourceborn Interpretations and Derived Pattern Candidates

## Hard separation

```text
WHAT THE SOURCE SAYS
≠
WHAT A TRANSLATION SAYS
≠
WHAT A COMMENTATOR SAYS
≠
WHAT A TRADITION SAYS
≠
WHAT SOURCEBORN INFERS
```

This separation is mandatory because Holy Books are intended to contribute civilizational memory, law, narrative, value, symbolic meaning and long-horizon patterns to Sourceborn. Collapsing them into generic embeddings or a `wisdom` prompt would reduce them back to ordinary LLM context.
