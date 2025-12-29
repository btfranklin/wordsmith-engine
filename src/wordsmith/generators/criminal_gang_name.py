"""Criminal gang name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import either, one_of
from wordsmith.names.given_name import GivenName
from wordsmith.util import random_bool
from wordsmith.words.base import (
    Adjective,
    MartialSocialConcept,
    PrimitiveWeapon,
    VillainousPersonNoun,
)
from wordsmith.generators.town_name import TownName


@dataclass(frozen=True)
class CriminalGangName(Component):
    """Generate a criminal gang name."""

    def make_text(self, rng: random.Random) -> str:
        begins_with_person_name = random_bool(rng, 0.25)

        if begins_with_person_name:
            component = (
                GivenName().possessive_form()
                | either(VillainousPersonNoun(is_plural=True), PrimitiveWeapon(is_plural=True))
            ).title_case()
        else:
            component = (
                "the"
                | one_of(
                    MartialSocialConcept() | VillainousPersonNoun(is_plural=True),
                    PrimitiveWeapon() | VillainousPersonNoun(is_plural=True),
                    VillainousPersonNoun(is_plural=True) | "of" | TownName(),
                    TownName() | VillainousPersonNoun(is_plural=True),
                    Adjective() | VillainousPersonNoun(is_plural=True),
                    Adjective() | VillainousPersonNoun(is_plural=True) | "of" | TownName(),
                ).title_case()
            )

        return component.make_text(rng)
