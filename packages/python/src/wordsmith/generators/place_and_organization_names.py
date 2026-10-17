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
from wordsmith.util.resources import load_json


_PARTS: dict[str, list[str]] = load_json("Place and Organization Parts.json")


@dataclass(frozen=True)
class _Part(Component):
    key: str

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(_PARTS[self.key])


@dataclass(frozen=True)
class TavernName(Component):
    """Generate a tavern name."""

    def make_text(self, rng: random.Random) -> str:
        return weighted_one_of(
            (
                4,
                "The"
                | _Part("tavernAdjectives")
                | one_of(_Part("animals"), _Part("tavernObjects")),
            ),
            (3, "The" | _Part("animals") | "and" | _Part("tavernObjects")),
            (
                2,
                GivenName(culture=GivenNameCulture.ENGLISH_SPEAKING).possessive_form()
                | _Part("tavernEndings"),
            ),
            (1, TownName() | one_of("Inn", "Tavern", "Lodge")),
        ).title_case().make_text(rng)


@dataclass(frozen=True)
class LandmarkName(Component):
    """Generate a landmark name."""

    def make_text(self, rng: random.Random) -> str:
        return weighted_one_of(
            (4, _Part("landmarkAdjectives") | _Part("landmarkFeatures")),
            (
                3,
                _Part("landmarkRoots") + _Part("landmarkSuffixes"),
            ),
            (2, Surname().possessive_form() | _Part("landmarkFeatures")),
            (
                1,
                "The"
                | _Part("landmarkAdjectives")
                | _Part("landmarkPluralFeatures"),
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
                | _Part("organizationAdjectives")
                | _Part("organizationSymbols"),
            ),
            (
                3,
                TownName()
                | _Part("tradesPlural").possessive_form()
                | "Guild",
            ),
            (2, "The" | _Part("organizationAdjectives") | _Part("organizationTypes")),
            (1, "The Society of" | _Part("organizationConcepts")),
        ).title_case().make_text(rng)
