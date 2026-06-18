"""Asset-backed ancient given-name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import ClassVar

from wordsmith.core.base import Component
from wordsmith.names.gender import BinaryGender
from wordsmith.util import load_json


@dataclass(frozen=True)
class AncientGivenName(Component):
    """Random ancient given name with optional gender selection."""

    gender: BinaryGender | None = None

    _options: ClassVar[dict[str, list[str]]] = load_json("Given Names.json").get(
        "ancient",
        {},
    )

    def make_text(self, rng: random.Random) -> str:
        gender = self.gender or (
            BinaryGender.MALE if rng.choice([True, False]) else BinaryGender.FEMALE
        )
        return rng.choice(self._options[gender.value])
