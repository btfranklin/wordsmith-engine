"""Criminal gang name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import either, one_of, text
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
            component = text(
                GivenName().possessive_form(),
                either(VillainousPersonNoun(is_plural=True), PrimitiveWeapon(is_plural=True)),
                sep=" ",
            ).title_case()
        else:
            component = text(
                "the",
                one_of(
                    text(MartialSocialConcept(), VillainousPersonNoun(is_plural=True), sep=" "),
                    text(PrimitiveWeapon(), VillainousPersonNoun(is_plural=True), sep=" "),
                    text(VillainousPersonNoun(is_plural=True), "of", TownName(), sep=" "),
                    text(TownName(), VillainousPersonNoun(is_plural=True), sep=" "),
                    text(Adjective(), VillainousPersonNoun(is_plural=True), sep=" "),
                    text(
                        Adjective(),
                        VillainousPersonNoun(is_plural=True),
                        "of",
                        TownName(),
                        sep=" ",
                    ),
                ).title_case(),
                sep=" ",
            )

        return component.make_text(rng)
