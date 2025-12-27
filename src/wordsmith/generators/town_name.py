"""Town name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import one_of, text
from wordsmith.names.surname import Surname
from wordsmith.words.base import LocationAdjective


@dataclass(frozen=True)
class TownName(Component):
    """Generate a town name."""

    def make_text(self, rng: random.Random) -> str:
        roll = rng.randint(1, 100)

        if 1 <= roll <= 9:
            component = text(
                Surname(),
                one_of("Bay", "Point", "City", "Park"),
                sep=" ",
            )
        elif 10 <= roll <= 19:
            component = text(
                one_of("Fort", "Port", "Cape"),
                Surname(),
                sep=" ",
            )
        elif 20 <= roll <= 24:
            component = text(
                Surname(),
                one_of("River", "Hill", "Town", "Beach", "Village"),
                sep=" ",
            )
        elif 25 <= roll <= 29:
            component = text(
                one_of("Saint", "Mount", "Lake"),
                Surname(),
                sep=" ",
            )
        elif 30 <= roll <= 31:
            component = text(
                "New",
                text(
                    Surname(),
                    one_of("ton", "burg", "ville", "town", "dale"),
                ),
                sep=" ",
            )
        elif 32 <= roll <= 35:
            component = text(
                LocationAdjective().first_upper(),
                one_of("Bay", "Point", "City", "Park"),
                sep=" ",
            )
        elif 36 <= roll <= 38:
            component = text(
                LocationAdjective().first_upper(),
                one_of("River", "Hill", "Town", "Beach", "Village"),
                sep=" ",
            )
        else:
            component = text(
                Surname(),
                one_of("ton", "burg", "ville", "town", "dale"),
            )

        return component.make_text(rng)
