"""Procedural ancient name generator."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import random
from typing import ClassVar

from wordsmith.core.base import Component
from wordsmith.util import first_upper, random_bool


class _SyllablePattern(Enum):
    CONSONANT_VOWEL = "consonant_vowel"
    VOWEL_CONSONANT = "vowel_consonant"
    VOWEL_ONLY = "vowel_only"


@dataclass(frozen=True)
class AncientName(Component):
    """Generate ancient-style names with phonetic patterns."""

    syllable_count: int
    allow_hyphen: bool = True
    allow_apostrophe: bool = True

    _single_consonants: ClassVar[list[str]] = ["t", "m", "k", "h", "l", "p", "w"]
    _double_consonants: ClassVar[list[str]] = ["ph", "ch", "th"]
    _single_vowels: ClassVar[list[str]] = ["a", "i", "o", "u", "e"]
    _double_vowels: ClassVar[list[str]] = ["ai", "au", "ah"]

    def __post_init__(self) -> None:
        if self.syllable_count < 1:
            raise ValueError("Syllable count must be greater than 0")

    @staticmethod
    def _random_consonant(rng: random.Random) -> str:
        if random_bool(rng, 0.90):
            return rng.choice(AncientName._single_consonants)
        return rng.choice(AncientName._double_consonants)

    @staticmethod
    def _random_vowel(rng: random.Random) -> str:
        if random_bool(rng, 0.95):
            return rng.choice(AncientName._single_vowels)
        return rng.choice(AncientName._double_vowels)

    def make_text(self, rng: random.Random) -> str:
        will_use_hyphen = (
            self.syllable_count > 3
            and self.allow_hyphen
            and random_bool(rng, 0.25)
        )
        will_try_apostrophe = self.allow_apostrophe and rng.choice([True, False])

        hyphen_syllable = rng.randrange(3, self.syllable_count) if will_use_hyphen else 0

        text = ""
        previous_pattern: _SyllablePattern | None = None

        for current_syllable in range(1, self.syllable_count + 1):
            roll = rng.randint(1, 100)
            if roll <= 65:
                pattern = _SyllablePattern.CONSONANT_VOWEL
            elif roll <= 85:
                pattern = _SyllablePattern.VOWEL_CONSONANT
            else:
                pattern = _SyllablePattern.VOWEL_ONLY

            consonant = self._random_consonant(rng)
            vowel = self._random_vowel(rng)

            if will_try_apostrophe and previous_pattern in {
                _SyllablePattern.CONSONANT_VOWEL,
                _SyllablePattern.VOWEL_ONLY,
            } and pattern in {
                _SyllablePattern.VOWEL_CONSONANT,
                _SyllablePattern.VOWEL_ONLY,
            }:
                text += "'"
                will_try_apostrophe = False

            if pattern == _SyllablePattern.CONSONANT_VOWEL:
                text += consonant + vowel
            elif pattern == _SyllablePattern.VOWEL_CONSONANT:
                text += vowel + consonant
            else:
                text += vowel

            previous_pattern = pattern

            if current_syllable == hyphen_syllable:
                text += "-"

        if previous_pattern != _SyllablePattern.VOWEL_CONSONANT and random_bool(rng, 0.4):
            text += self._random_consonant(rng)

        return first_upper(text)
