"""Articles and determiners."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component


@dataclass(frozen=True)
class Article(Component):
    """Choose between "a"/"an" and "the" based on context."""

    is_before_vowel: bool = False

    def make_text(self, rng: random.Random) -> str:
        value = rng.choice(["a", "the"])
        if value == "a" and self.is_before_vowel:
            value = "an"
        return value


@dataclass(frozen=True)
class Determiner(Component):
    """Choose a determiner, with vowel-aware "a"/"an" handling."""

    is_before_vowel: bool = False

    def make_text(self, rng: random.Random) -> str:
        value = rng.choice(["a", "the", "my", "your", "our", "her", "his"])
        if value == "a" and self.is_before_vowel:
            value = "an"
        return value
