"""Procedural fantasy name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import ClassVar

from wordsmith.core.base import Component
from wordsmith.util import first_upper, load_json, random_bool

_SYNTHETIC_NAME_PARTS: dict[str, dict[str, list[str]]] = load_json(
    "Synthetic Name Parts.json"
)


@dataclass(frozen=True)
class FantasyName(Component):
    """Generate classical-inspired fantasy names."""

    syllable_count: int
    allow_hyphen: bool = True
    allow_apostrophe: bool = True

    _prefixes: ClassVar[list[str]] = _SYNTHETIC_NAME_PARTS["fantasy"]["prefixes"]
    _middles: ClassVar[list[str]] = _SYNTHETIC_NAME_PARTS["fantasy"]["middles"]
    _endings: ClassVar[list[str]] = _SYNTHETIC_NAME_PARTS["fantasy"]["endings"]
    _compound_endings: ClassVar[list[str]] = _SYNTHETIC_NAME_PARTS["fantasy"][
        "compoundEndings"
    ]

    def __post_init__(self) -> None:
        if self.syllable_count < 1:
            raise ValueError("Syllable count must be greater than 0")
        if not isinstance(self.allow_hyphen, bool):
            raise TypeError("allow_hyphen must be a boolean")
        if not isinstance(self.allow_apostrophe, bool):
            raise TypeError("allow_apostrophe must be a boolean")

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
