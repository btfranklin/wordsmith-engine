"""Given name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import ClassVar

from wordsmith.core.base import Component
from wordsmith.names.gender import BinaryGender
from wordsmith.names.given_name_culture import GivenNameCulture
from wordsmith.util import load_json


@dataclass(frozen=True)
class GivenName(Component):
    """Random given name with optional gender selection."""

    gender: BinaryGender | None = None
    culture: GivenNameCulture | None = None

    _options: ClassVar[dict[str, dict[str, list[str]]]] = load_json(
        "Given Names.json"
    ).get("modern", {})

    def make_text(self, rng: random.Random) -> str:
        gender = self.gender or rng.choice([BinaryGender.MALE, BinaryGender.FEMALE])
        culture = self.culture or rng.choice(list(GivenNameCulture))
        return rng.choice(self._options[culture.value][gender.value])
