"""Nautical ship name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import either
from wordsmith.names.ancient_name import AncientName
from wordsmith.names.gender import BinaryGender
from wordsmith.names.given_name import GivenName
from wordsmith.names.weird_name import WeirdName
from wordsmith.util import random_bool
from wordsmith.words.base import (
    MartialSocialConcept,
    NauticalShipNameColor,
    NauticalShipNameObject,
    PrimitiveWeapon,
    ShipNameAdjective,
    TimeOfDay,
)
from wordsmith.generators.town_name import TownName


@dataclass(frozen=True)
class NauticalShipName(Component):
    """Generate a nautical ship name."""

    def make_text(self, rng: random.Random) -> str:
        roll = rng.randint(1, 18)

        if 1 <= roll <= 4:
            component = GivenName(gender=BinaryGender.FEMALE)
        elif 5 <= roll <= 7:
            component = MartialSocialConcept()
        elif roll == 8:
            component = TownName()
        elif roll == 9:
            component = either(WeirdName(syllable_count=3), AncientName(syllable_count=3))
        elif roll == 10:
            component = NauticalShipNameObject()
        elif roll == 11:
            component = ShipNameAdjective()
        elif roll == 12:
            component = (
                NauticalShipNameColor()
                | either(
                    NauticalShipNameObject(),
                    PrimitiveWeapon(),
                    first_probability=0.75,
                )
            )
        elif 13 <= roll <= 14:
            component = (
                ShipNameAdjective()
                | either(
                    NauticalShipNameObject(),
                    PrimitiveWeapon(),
                    first_probability=0.85,
                )
            )
        elif roll == 15:
            component = (
                TimeOfDay()
                | either(MartialSocialConcept(), PrimitiveWeapon(), first_probability=0.75)
            )
        elif roll == 16:
            component = (
                TownName()
                | either(
                    NauticalShipNameObject(),
                    PrimitiveWeapon(),
                    first_probability=0.85,
                )
            )
        elif roll == 17:
            component = (
                either(NauticalShipNameObject(), PrimitiveWeapon())
                | "of"
                | either(MartialSocialConcept(), TownName())
            )
        else:
            gender = BinaryGender.FEMALE if random_bool(rng, 0.75) else BinaryGender.MALE
            component = (
                either(
                    MartialSocialConcept().first_upper(),
                    GivenName(gender=gender),
                    first_probability=0.33,
                ).possessive_form()
                | either(
                    either(NauticalShipNameObject(), PrimitiveWeapon()),
                    MartialSocialConcept(),
                )
            )

        return component.title_case().make_text(rng)
