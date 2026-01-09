"""Nautical ship name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import either, weighted_one_of
from wordsmith.names.ancient_name import AncientName
from wordsmith.names.gender import BinaryGender
from wordsmith.names.given_name import GivenName
from wordsmith.names.weird_name import WeirdName
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
        possessive_name = (
            either(
                MartialSocialConcept().first_upper(),
                either(
                    GivenName(gender=BinaryGender.FEMALE),
                    GivenName(gender=BinaryGender.MALE),
                    first_probability=0.75,
                ),
                first_probability=0.33,
            ).possessive_form()
            | either(
                either(NauticalShipNameObject(), PrimitiveWeapon()),
                MartialSocialConcept(),
            )
        )

        component = weighted_one_of(
            (4, GivenName(gender=BinaryGender.FEMALE)),
            (3, MartialSocialConcept()),
            (1, TownName()),
            (1, either(WeirdName(syllable_count=3), AncientName(syllable_count=3))),
            (1, NauticalShipNameObject()),
            (1, ShipNameAdjective()),
            (
                1,
                NauticalShipNameColor()
                | either(
                    NauticalShipNameObject(),
                    PrimitiveWeapon(),
                    first_probability=0.75,
                ),
            ),
            (
                2,
                ShipNameAdjective()
                | either(
                    NauticalShipNameObject(),
                    PrimitiveWeapon(),
                    first_probability=0.85,
                ),
            ),
            (
                1,
                TimeOfDay()
                | either(
                    MartialSocialConcept(),
                    PrimitiveWeapon(),
                    first_probability=0.75,
                ),
            ),
            (
                1,
                TownName()
                | either(
                    NauticalShipNameObject(),
                    PrimitiveWeapon(),
                    first_probability=0.85,
                ),
            ),
            (
                1,
                either(NauticalShipNameObject(), PrimitiveWeapon())
                | "of"
                | either(MartialSocialConcept(), TownName()),
            ),
            (1, possessive_name),
        )

        return component.title_case().make_text(rng)
