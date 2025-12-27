"""Surname generator."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import ClassVar

from wordsmith.core.base import Component
from wordsmith.util import load_json


@dataclass(frozen=True)
class Surname(Component):
    """Random surname from the asset list."""

    _options: ClassVar[list[str]] = load_json("Common Surnames.json")

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)
