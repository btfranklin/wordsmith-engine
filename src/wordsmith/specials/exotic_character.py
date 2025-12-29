"""Exotic character picker."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import ClassVar

from wordsmith.util import load_json


@dataclass(frozen=True)
class ExoticCharacter:
    """Pick random exotic characters."""

    _character_sets: ClassVar[dict[str, list[str]]] = load_json(
        "Exotic Character Sets.json"
    )

    @classmethod
    def random_character(cls, rng: random.Random | None = None) -> str:
        if rng is None:
            rng = random.SystemRandom()

        character_set = rng.choice(list(cls._character_sets.values()))
        return rng.choice(character_set)

    @classmethod
    def random_character_from_set(
        cls,
        set_name: str,
        rng: random.Random | None = None,
    ) -> str:
        if rng is None:
            rng = random.SystemRandom()

        if set_name not in cls._character_sets:
            raise ValueError(f"Invalid character set requested: {set_name}")
        return rng.choice(cls._character_sets[set_name])
