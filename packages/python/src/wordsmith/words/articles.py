"""Articles and determiners."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core._grammar import select_article, select_determiner
from wordsmith.core.base import Component


@dataclass(frozen=True)
class Article(Component):
    """Choose between "a"/"an" and "the" based on context."""

    is_before_vowel: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.is_before_vowel, bool):
            raise TypeError("is_before_vowel must be a boolean")

    def make_text(self, rng: random.Random) -> str:
        return select_article(rng, is_before_vowel=self.is_before_vowel)


@dataclass(frozen=True)
class Determiner(Component):
    """Choose a determiner, with vowel-aware "a"/"an" handling."""

    is_before_vowel: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.is_before_vowel, bool):
            raise TypeError("is_before_vowel must be a boolean")

    def make_text(self, rng: random.Random) -> str:
        return select_determiner(rng, is_before_vowel=self.is_before_vowel)
