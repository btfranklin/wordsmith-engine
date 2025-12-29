"""Full person name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.names.gender import BinaryGender
from wordsmith.names.given_name import GivenName
from wordsmith.names.surname import Surname


@dataclass(frozen=True)
class PersonName(Component):
    """Random person name composed of given name and surname."""

    gender: BinaryGender | None = None

    def make_text(self, rng: random.Random) -> str:
        return (GivenName(gender=self.gender) | Surname()).make_text(rng)
