"""The Wisdom Bank + Example-Match — the "Eternal Example" heart.

SOURCEBORN_PRINCIPLE: the engine answers from the *deepest example that already
holds the pattern* of a question — humanity's oldest proven templates (holy
books, proverbs, myths, archetypes) plus the user's own corpus — then grounds it
in present fact.

This module is the instinct layer (the second of the three memories). It ships
with a small seed bank; the user feeds more via JSON. ``match`` compares a
question to the bank across the extensible ``COMPARISON_AXES`` — more axes,
more outcome.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any

from .parameters import COMPARISON_AXES


@dataclass
class WisdomExample:
    source: str          # e.g. "Bhagavad Gita", "Proverb", "Aesop"
    pattern: str         # the archetypal pattern it holds
    text: str            # the example itself
    axes: dict[str, str] = field(default_factory=dict)  # which axes it speaks to


# A small seed of cross-tradition archetypes. The point is the *mechanism*; the
# user grows this bank with their own wisdom corpus.
SEED_WISDOM: tuple[WisdomExample, ...] = (
    WisdomExample(
        source="Bhagavad Gita",
        pattern="Act without attachment to outcome; failure comes from inner ideology, not effort",
        text="You have a right to your action, never to its fruits.",
        axes={"Intent": "duty over result", "Moral/Sacred line": "non-attachment",
              "Consequence": "peace under pressure"},
    ),
    WisdomExample(
        source="Proverb",
        pattern="The obvious answer is often already in hand (key-in-hand)",
        text="Do not light a candle to look for the sun.",
        axes={"Simplicity/Key-in-hand": "stop over-engineering", "Scale": "right-size effort"},
    ),
    WisdomExample(
        source="Aesop",
        pattern="Slow, steady, grounded effort beats fast shallow brilliance",
        text="The tortoise and the hare.",
        axes={"Time": "endurance over speed", "Pattern": "consistency wins"},
    ),
    WisdomExample(
        source="Ecclesiastes",
        pattern="There is a season for everything; non-resolution / waiting is valid",
        text="To every thing there is a season, and a time to every purpose.",
        axes={"Time": "incubate, do not force", "Scale": "patience"},
    ),
    WisdomExample(
        source="Guru Granth Sahib",
        pattern="Inner quality over external rank; humility and service over caste/power",
        text="Recognise the Light within all; do not ask anyone's caste.",
        axes={"Motive/Shadow": "ego dissolves", "Moral/Sacred line": "equality"},
    ),
    WisdomExample(
        source="Tao Te Ching",
        pattern="The hollow/empty is what makes a thing useful (hollow can beat weight)",
        text="The usefulness of a cup is in its emptiness.",
        axes={"Pattern": "emptiness as function", "Opposite/Inversion": "less is more"},
    ),
    WisdomExample(
        source="Quran",
        pattern="True nobility is inner righteousness (taqwa), not birth or wealth",
        text="The most honoured of you is the most righteous, not the highest-born.",
        axes={"Moral/Sacred line": "inner over outer", "Motive/Shadow": "status illusion"},
    ),
    WisdomExample(
        source="Gospel",
        pattern="The few who truly see vs the many who follow (visionary layer is small)",
        text="The harvest is plentiful but the workers are few.",
        axes={"Scale": "rare minds", "Pattern": "visionary/implementer/follower"},
    ),
    WisdomExample(
        source="Gospel",
        pattern="The smallest seed becomes the largest tree — tiny starts carry vast outcomes",
        text="The kingdom is like a mustard seed: the smallest of seeds, yet it grows into a tree.",
        axes={"Scale": "small start, big outcome", "Time": "growth is quiet",
              "Pattern": "seed to tree"},
    ),
    WisdomExample(
        source="Marcus Aurelius",
        pattern="The obstacle itself is the way — resistance is material, not blockage",
        text="The impediment to action advances action. What stands in the way becomes the way.",
        axes={"Opposite/Inversion": "obstacle as fuel", "Pattern": "halt opens the loop",
              "Consequence": "pressure builds strength"},
    ),
    WisdomExample(
        source="Sun Tzu",
        pattern="The supreme victory needs no battle — position beats force",
        text="To win one hundred victories is not the acme of skill; to subdue the enemy without fighting is.",
        axes={"Pattern": "position over force", "Simplicity/Key-in-hand": "avoid the fight you can skip",
              "Scale": "leverage"},
    ),
    WisdomExample(
        source="Rumi",
        pattern="The wound is where the light enters — pain is a doorway, not a defect",
        text="The wound is the place where the Light enters you.",
        axes={"Motive/Shadow": "wound as entry", "Moral/Sacred line": "suffering transmutes",
              "Opposite/Inversion": "break as opening"},
    ),
    WisdomExample(
        source="Kabir",
        pattern="What you seek is already inside — the search abroad misses the near",
        text="The musk is inside the deer, but the deer runs the forest searching for it.",
        axes={"Simplicity/Key-in-hand": "already in hand", "Motive/Shadow": "blind seeking",
              "Pattern": "inner before outer"},
    ),
    WisdomExample(
        source="Upanishads",
        pattern="The unseen essence carries the whole — subtle over visible",
        text="That subtle essence which you do not perceive — of that is this great tree made. Tat tvam asi.",
        axes={"Pattern": "invisible root, visible tree", "Meaning": "essence over form",
              "Scale": "micro carries macro"},
    ),
    WisdomExample(
        source="Bhagavad Gita",
        pattern="The mind is both the ally and the enemy — mastery decides which",
        text="For him who has conquered the mind, the mind is the best of friends; unconquered, it is the greatest enemy.",
        axes={"Motive/Shadow": "self as battlefield", "Intent": "discipline first",
              "Consequence": "inner rules outer"},
    ),
    WisdomExample(
        source="Tao Te Ching",
        pattern="Soft overcomes hard; water defeats stone — persistence beats rigidity",
        text="Nothing is softer than water, yet nothing is better at overcoming the hard.",
        axes={"Opposite/Inversion": "soft beats hard", "Time": "persistence",
              "Pattern": "yield to win"},
    ),
    WisdomExample(
        source="Proverb",
        pattern="Iron sharpens iron — minds grow by friction, not comfort",
        text="As iron sharpens iron, so one person sharpens another.",
        axes={"Pattern": "friction as growth", "Consequence": "challenge refines",
              "Scale": "witness needed"},
    ),
    WisdomExample(
        source="Quran",
        pattern="With every hardship comes ease — twinned, not sequential",
        text="Verily, with hardship there is ease.",
        axes={"Time": "relief inside the trial", "Consequence": "hardship carries its exit",
              "Opposite/Inversion": "ease within hard"},
    ),
    WisdomExample(
        source="Guru Granth Sahib",
        pattern="Truth is high, but higher still is truthful living",
        text="Truth is higher than everything; but higher still is truthful living.",
        axes={"Moral/Sacred line": "practice over doctrine", "Intent": "embodiment",
              "Consequence": "lived truth compounds"},
    ),
    WisdomExample(
        source="Heraclitus",
        pattern="No one steps in the same river twice — the present fact is always new",
        text="Everything flows; you cannot step into the same river twice.",
        axes={"Time": "present fact over stale data", "Pattern": "change is the constant",
              "Reality": "re-anchor always"},
    ),
)


class WisdomBank:
    def __init__(self, root: str = ".sourceborn") -> None:
        self.path = os.path.join(root, "wisdom_bank.json")
        os.makedirs(root, exist_ok=True)
        self.examples: list[WisdomExample] = list(SEED_WISDOM)
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.path):
            with open(self.path, encoding="utf-8") as f:
                for e in json.load(f):
                    self.examples.append(WisdomExample(**e))

    def add(self, source: str, pattern: str, text: str, **axes: str) -> None:
        self.examples.append(WisdomExample(source, pattern, text, axes))

    def match(self, question: str, top: int = 2) -> list[tuple[float, WisdomExample, list[str]]]:
        """Find the deepest matching examples, scored across many axes.

        Returns (score, example, matched_axes). Score rewards both keyword
        overlap and the number of comparison axes the example speaks to —
        literally: more axes -> more outcome.
        """
        words = set(question.lower().split())
        results: list[tuple[float, WisdomExample, list[str]]] = []
        for ex in self.examples:
            blob = (ex.pattern + " " + ex.text + " " + " ".join(ex.axes.values())).lower()
            overlap = len(words & set(blob.split()))
            matched_axes = [a for a in COMPARISON_AXES if a in ex.axes]
            score = overlap + 0.5 * len(matched_axes)
            if score > 0:
                results.append((score, ex, matched_axes))
        results.sort(key=lambda r: r[0], reverse=True)
        return results[:top]
