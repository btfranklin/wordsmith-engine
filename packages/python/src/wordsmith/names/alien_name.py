"""Procedural alien name generator."""

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
class AlienName(Component):
    """Generate a synthetic alien name from open syllable fragments."""

    syllable_count: int
    allow_hyphen: bool = True
    allow_apostrophe: bool = True

    _open_ended_syllables: ClassVar[list[str]] = _SYNTHETIC_NAME_PARTS["alien"][
        "openEndedSyllables"
    ]
    _ending_sounds: ClassVar[list[str]] = _SYNTHETIC_NAME_PARTS["alien"][
        "endingSounds"
    ]

    def __post_init__(self) -> None:
        if self.syllable_count < 1:
            raise ValueError("Syllable count must be greater than 0")
        if not isinstance(self.allow_hyphen, bool):
            raise TypeError("allow_hyphen must be a boolean")
        if not isinstance(self.allow_apostrophe, bool):
            raise TypeError("allow_apostrophe must be a boolean")

    def make_text(self, rng: random.Random) -> str:
        will_use_hyphen = (
            self.syllable_count > 2
            and self.allow_hyphen
            and random_bool(rng)
        )
        will_use_apostrophe = (
            self.syllable_count > 2
            and self.allow_apostrophe
            and random_bool(rng)
        )

        hyphen_syllable = (
            rng.randrange(1, self.syllable_count) if will_use_hyphen else 0
        )
        apostrophe_syllable = (
            rng.randrange(1, self.syllable_count) if will_use_apostrophe else 0
        )

        text = ""
        for current_syllable in range(1, self.syllable_count + 1):
            text += rng.choice(self._open_ended_syllables)

            if current_syllable == apostrophe_syllable:
                text += "'"
            elif current_syllable == hyphen_syllable:
                text += "-"

        if random_bool(rng):
            text += rng.choice(self._ending_sounds)

        return first_upper(text)
