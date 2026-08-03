"""Procedural fantasy name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import ClassVar

from wordsmith.core.base import Component
from wordsmith.util import first_upper, random_bool


@dataclass(frozen=True)
class FantasyName(Component):
    """Generate classical-inspired fantasy names."""

    syllable_count: int
    allow_hyphen: bool = True
    allow_apostrophe: bool = True

    _prefixes: ClassVar[list[str]] = [
        "ael",
        "am",
        "ant",
        "bel",
        "cal",
        "cass",
        "cor",
        "daph",
        "dor",
        "el",
        "eph",
        "gal",
        "hel",
        "il",
        "is",
        "lys",
        "mar",
        "mel",
        "myr",
        "ner",
        "or",
        "pel",
        "sar",
        "sel",
        "ser",
        "soph",
        "tal",
        "ther",
        "val",
    ]
    _middles: ClassVar[list[str]] = [
        "a",
        "ae",
        "an",
        "ar",
        "ath",
        "el",
        "en",
        "er",
        "ia",
        "il",
        "in",
        "ir",
        "or",
        "ra",
        "ren",
        "the",
        "um",
        "ur",
        "yra",
    ]
    _endings: ClassVar[list[str]] = [
        "a",
        "ae",
        "an",
        "ar",
        "as",
        "el",
        "en",
        "eth",
        "ia",
        "iel",
        "ion",
        "is",
        "or",
        "os",
        "oth",
        "um",
        "us",
    ]
    _compound_endings: ClassVar[list[str]] = [
        "adon",
        "ander",
        "ara",
        "arius",
        "astra",
        "athon",
        "eia",
        "eron",
        "etor",
        "ion",
        "oria",
        "orian",
    ]

    def __post_init__(self) -> None:
        if self.syllable_count < 1:
            raise ValueError("Syllable count must be greater than 0")

    def make_text(self, rng: random.Random) -> str:
        pieces = [rng.choice(self._prefixes)]

        for _ in range(max(0, self.syllable_count - 2)):
            pieces.append(rng.choice(self._middles))

        if self.syllable_count > 1:
            if self.syllable_count > 3 and random_bool(rng, 0.25):
                pieces.append(rng.choice(self._compound_endings))
            else:
                pieces.append(rng.choice(self._endings))

        text = "".join(pieces)
        if self.allow_hyphen and self.syllable_count > 4 and random_bool(rng, 0.12):
            split_at = rng.randrange(2, len(text) - 2)
            text = f"{text[:split_at]}-{text[split_at:]}"
        if self.allow_apostrophe and self.syllable_count > 4 and random_bool(rng, 0.04):
            split_at = rng.randrange(2, len(text) - 2)
            text = f"{text[:split_at]}'{text[split_at:]}"

        return first_upper(text)
