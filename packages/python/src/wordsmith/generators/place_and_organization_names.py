"""Tavern, landmark, and organization name generators."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import one_of, weighted_one_of
from wordsmith.generators.town_name import TownName
from wordsmith.names.given_name import GivenName
from wordsmith.names.given_name_culture import GivenNameCulture
from wordsmith.names.surname import Surname
from wordsmith.util import load_json
from wordsmith.words import (
    GuildTrade,
    LandmarkAdjective,
    LandmarkFeature,
    NaturalNameRoot,
    OrganizationSymbol,
    TavernAnimal,
    TavernObject,
)

_PARTS: dict[str, list[str]] = load_json("Place and Organization Parts.json")


@dataclass(frozen=True)
class HeraldicSymbol(Component):
    """Choose a tavern animal or object with equal probability."""

    def make_text(self, rng: random.Random) -> str:
        return one_of(TavernAnimal(), TavernObject()).make_text(rng)


@dataclass(frozen=True)
class CompoundLandmarkName(Component):
    """Join a landmark root and suffix, then apply title casing."""

    def make_text(self, rng: random.Random) -> str:
        suffix = one_of(*_PARTS["landmarkSuffixes"])
        return (NaturalNameRoot("landmark") + suffix).title_case().make_text(rng)


@dataclass(frozen=True)
class TavernName(Component):
    """Generate a tavern name."""

    def make_text(self, rng: random.Random) -> str:
        return weighted_one_of(
            (
                4,
                "The" | one_of(*_PARTS["tavernAdjectives"]) | HeraldicSymbol(),
            ),
            (3, "The" | TavernAnimal() | "and" | TavernObject()),
            (
                2,
                GivenName(culture=GivenNameCulture.ENGLISH_SPEAKING).possessive_form()
                | one_of(*_PARTS["tavernEndings"]),
            ),
            (1, TownName() | one_of("Inn", "Tavern", "Lodge")),
        ).title_case().make_text(rng)


@dataclass(frozen=True)
class LandmarkName(Component):
    """Generate a landmark name."""

    def make_text(self, rng: random.Random) -> str:
        return weighted_one_of(
            (4, LandmarkAdjective() | LandmarkFeature()),
            (
                3,
                CompoundLandmarkName(),
            ),
            (2, Surname().possessive_form() | LandmarkFeature()),
            (
                1,
                "The"
                | LandmarkAdjective()
                | one_of(*_PARTS["landmarkPluralFeatures"]),
            ),
        ).title_case().make_text(rng)


@dataclass(frozen=True)
class OrganizationName(Component):
    """Generate an organization name."""

    def make_text(self, rng: random.Random) -> str:
        return weighted_one_of(
            (
                4,
                "The Order of the"
                | one_of(*_PARTS["organizationAdjectives"])
                | OrganizationSymbol(),
            ),
            (
                3,
                TownName()
                | GuildTrade().possessive_form()
                | "Guild",
            ),
            (
                2,
                "The"
                | one_of(*_PARTS["organizationAdjectives"])
                | one_of(*_PARTS["organizationTypes"]),
            ),
            (1, "The Society of" | one_of(*_PARTS["organizationConcepts"])),
        ).title_case().make_text(rng)
