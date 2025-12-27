"""Given name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import ClassVar

from wordsmith.core.base import Component
from wordsmith.names.gender import BinaryGender
from wordsmith.util import load_json


@dataclass(frozen=True)
class GivenName(Component):
    """Random given name with optional gender selection."""

    gender: BinaryGender | None = None

    _male_options: ClassVar[list[str]] = load_json(
        "Common Male Given Names.json"
    )
    _female_options: ClassVar[list[str]] = load_json(
        "Common Female Given Names.json"
    )

    def make_text(self, rng: random.Random) -> str:
        gender = self.gender or (
            BinaryGender.MALE if rng.choice([True, False]) else BinaryGender.FEMALE
        )

        if gender == BinaryGender.MALE:
            return rng.choice(self._male_options)
        return rng.choice(self._female_options)
