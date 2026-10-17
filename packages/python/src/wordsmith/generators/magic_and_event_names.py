"""Artifact, spell, operation, and festival name generators."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import one_of, weighted_one_of
from wordsmith.generators.fictional_mineral_name import FictionalMineralName
from wordsmith.generators.place_and_organization_names import (
    CompoundLandmarkName,
    HeraldicSymbol,
    LandmarkName,
)
from wordsmith.generators.town_name import TownName
from wordsmith.names.surname import Surname
from wordsmith.util import load_json
from wordsmith.words import (
    ArtifactObject,
    MagicalConcept,
    OperationColor,
    PrimitiveWeapon,
    Season,
    SpellEffect,
    TimeOfDay,
    OrganizationSymbol,
    WildAnimal,
)

_SPELL_PARTS: dict[str, list[str]] = load_json("Spell Name Parts.json")
_OPERATION_PARTS: dict[str, list[str]] = load_json("Operation Name Parts.json")
_FESTIVAL_PARTS: dict[str, list[str]] = load_json("Festival Name Parts.json")


@dataclass(frozen=True)
class ArtifactName(Component):
    """Generate a fictional artifact name from four weighted patterns."""

    def make_text(self, rng: random.Random) -> str:
        return weighted_one_of(
            (
                4,
                "The" | ArtifactObject() | "of" | MagicalConcept(),
            ),
            (3, Surname().possessive_form() | ArtifactObject()),
            (2, FictionalMineralName() | PrimitiveWeapon()),
            (1, "The" | ArtifactObject() | "of" | LandmarkName()),
        ).title_case().make_text(rng)


@dataclass(frozen=True)
class SpellName(Component):
    """Generate a spell name from four weighted patterns."""

    def make_text(self, rng: random.Random) -> str:
        return weighted_one_of(
            (4, SpellEffect() | "of" | MagicalConcept()),
            (
                3,
                Surname().possessive_form()
                | one_of(*_SPELL_PARTS["spellModifiers"])
                | SpellEffect(),
            ),
            (
                2,
                one_of(*_SPELL_PARTS["spellCommands"])
                | "the"
                | one_of(*_SPELL_PARTS["spellTargets"]),
            ),
            (1, SpellEffect() | "of" | TimeOfDay()),
        ).title_case().make_text(rng)


@dataclass(frozen=True)
class OperationName(Component):
    """Generate a fictional operation codename from four patterns."""

    def make_text(self, rng: random.Random) -> str:
        return weighted_one_of(
            (
                4,
                "Operation"
                | one_of(*_OPERATION_PARTS["operationAdjectives"])
                | HeraldicSymbol(),
            ),
            (3, "Project" | OperationColor() | WildAnimal()),
            (2, "Operation" | CompoundLandmarkName()),
            (1, LandmarkName() | "Expedition"),
        ).title_case().make_text(rng)


@dataclass(frozen=True)
class FestivalName(Component):
    """Generate a festival name from four weighted patterns."""

    def make_text(self, rng: random.Random) -> str:
        return weighted_one_of(
            (
                4,
                "The"
                | one_of(*_FESTIVAL_PARTS["festivalTypes"])
                | "of"
                | one_of(*_FESTIVAL_PARTS["festivalThemes"]),
            ),
            (3, TownName() | Season() | one_of(*_FESTIVAL_PARTS["festivalTypes"])),
            (2, TimeOfDay() | one_of(*_FESTIVAL_PARTS["festivalTypes"])),
            (
                1,
                OrganizationSymbol()
                + one_of(*_FESTIVAL_PARTS["festivalSuffixes"]),
            ),
        ).title_case().make_text(rng)
