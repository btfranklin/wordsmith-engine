"""Business, celestial-body, and creature name generators."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import one_of, text, weighted_one_of
from wordsmith.generators.town_name import TownName
from wordsmith.names.fantasy_name import FantasyName
from wordsmith.names.surname import Surname
from wordsmith.util import load_json
from wordsmith.words import (
    BodyPart,
    BusinessAnimal,
    BusinessColor,
    BusinessTrade,
    CelestialObjectType,
    CreatureType,
    Habitat,
    IndustrialTrade,
    NaturalNameRoot,
    ShopType,
    WildAnimal,
)

_CELESTIAL_PARTS: dict[str, list[str]] = load_json("Celestial Name Parts.json")
_CREATURE_PARTS: dict[str, list[str]] = load_json("Creature Name Parts.json")


@dataclass(frozen=True)
class CompoundCreatureName(Component):
    """Join a creature root and body part, then apply title casing."""

    def make_text(self, rng: random.Random) -> str:
        return (NaturalNameRoot("creature") + BodyPart()).title_case().make_text(rng)


@dataclass(frozen=True)
class BusinessName(Component):
    """Generate a business name from four weighted patterns."""

    def make_text(self, rng: random.Random) -> str:
        return weighted_one_of(
            (4, Surname() | "& Sons"),
            (
                3,
                BusinessColor() | BusinessAnimal() | BusinessTrade(),
            ),
            (2, TownName() | IndustrialTrade()),
            (1, Surname().possessive_form() | ShopType()),
        ).title_case().make_text(rng)


@dataclass(frozen=True)
class CelestialBodyName(Component):
    """Generate a name for a fictional celestial body."""

    def make_text(self, rng: random.Random) -> str:
        synthetic_name = FantasyName(
            syllable_count=3,
            allow_hyphen=False,
            allow_apostrophe=False,
        ).title_case()
        return weighted_one_of(
            (4, synthetic_name),
            (
                3,
                text(
                    synthetic_name,
                    one_of("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"),
                    sep=" ",
                ),
            ),
            (
                2,
                (
                    Surname().possessive_form() | CelestialObjectType()
                ).title_case(),
            ),
            (
                1,
                (
                    "The"
                    | CelestialObjectType()
                    | "of"
                    | one_of(*_CELESTIAL_PARTS["celestialConcepts"])
                ).title_case(),
            ),
        ).make_text(rng)


@dataclass(frozen=True)
class CreatureName(Component):
    """Generate a fantasy creature name from four weighted patterns."""

    def make_text(self, rng: random.Random) -> str:
        return weighted_one_of(
            (
                4,
                CompoundCreatureName() | CreatureType(),
            ),
            (
                3,
                one_of(*_CREATURE_PARTS["descriptors"]) | Habitat() | WildAnimal(),
            ),
            (
                2,
                one_of(*_CREATURE_PARTS["behaviorAdjectives"]) | CreatureType(),
            ),
            (
                1,
                CompoundCreatureName(),
            ),
        ).title_case().make_text(rng)
