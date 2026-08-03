"""Town name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import one_of, weighted_one_of
from wordsmith.names.surname import Surname
from wordsmith.words.base import LocationAdjective


@dataclass(frozen=True)
class TownName(Component):
    """Generate a town name."""

    def make_text(self, rng: random.Random) -> str:
        return weighted_one_of(
            (9, Surname() | one_of("Bay", "Point", "City", "Park")),
            (10, one_of("Fort", "Port", "Cape") | Surname()),
            (5, Surname() | one_of("River", "Hill", "Town", "Beach", "Village")),
            (5, one_of("Saint", "Mount", "Lake") | Surname()),
            (
                2,
                "New" | (Surname() + one_of("ton", "burg", "ville", "town", "dale")),
            ),
            (
                4,
                LocationAdjective().first_upper()
                | one_of("Bay", "Point", "City", "Park"),
            ),
            (
                3,
                LocationAdjective().first_upper()
                | one_of("River", "Hill", "Town", "Beach", "Village"),
            ),
            (62, Surname() + one_of("ton", "burg", "ville", "town", "dale")),
        ).make_text(rng)
