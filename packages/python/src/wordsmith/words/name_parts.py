"""Reusable word components for procedural name generation."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import ClassVar, Literal

from wordsmith.core.base import Component
from wordsmith.util import load_json

_PLACE_PARTS: dict[str, list[str]] = load_json("Place and Organization Parts.json")
_BUSINESS_PARTS: dict[str, list[str]] = load_json("Business Name Parts.json")
_CELESTIAL_PARTS: dict[str, list[str]] = load_json("Celestial Name Parts.json")
_CREATURE_PARTS: dict[str, list[str]] = load_json("Creature Name Parts.json")


class _OptionPart(Component):
    _options: ClassVar[list[str]]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class TavernAnimal(_OptionPart):
    """Random animal used in tavern names."""

    _options: ClassVar[list[str]] = _PLACE_PARTS["animals"]


@dataclass(frozen=True)
class TavernObject(_OptionPart):
    """Random object used in tavern names."""

    _options: ClassVar[list[str]] = _PLACE_PARTS["tavernObjects"]


@dataclass(frozen=True)
class BusinessAnimal(_OptionPart):
    """Random animal used in business names."""

    _options: ClassVar[list[str]] = _BUSINESS_PARTS["animals"]


@dataclass(frozen=True)
class WildAnimal(_OptionPart):
    """Random animal used in creature names."""

    _options: ClassVar[list[str]] = _CREATURE_PARTS["animals"]


@dataclass(frozen=True)
class BusinessColor(_OptionPart):
    """Random color used in business names."""

    _options: ClassVar[list[str]] = _BUSINESS_PARTS["colors"]


@dataclass(frozen=True)
class LandmarkAdjective(_OptionPart):
    """Random adjective used in landmark names."""

    _options: ClassVar[list[str]] = _PLACE_PARTS["landmarkAdjectives"]


@dataclass(frozen=True)
class LandmarkFeature(_OptionPart):
    """Random feature used in landmark names."""

    _options: ClassVar[list[str]] = _PLACE_PARTS["landmarkFeatures"]


@dataclass(frozen=True)
class Habitat(_OptionPart):
    """Random creature habitat."""

    _options: ClassVar[list[str]] = _CREATURE_PARTS["habitats"]


@dataclass(frozen=True)
class BodyPart(_OptionPart):
    """Random creature body part."""

    _options: ClassVar[list[str]] = _CREATURE_PARTS["bodyParts"]


@dataclass(frozen=True)
class CreatureType(_OptionPart):
    """Random creature type."""

    _options: ClassVar[list[str]] = _CREATURE_PARTS["creatureTypes"]


@dataclass(frozen=True)
class GuildTrade(_OptionPart):
    """Random plural trade name used by a guild."""

    _options: ClassVar[list[str]] = _PLACE_PARTS["tradesPlural"]


@dataclass(frozen=True)
class BusinessTrade(_OptionPart):
    """Random trade used in business names."""

    _options: ClassVar[list[str]] = _BUSINESS_PARTS["trades"]


@dataclass(frozen=True)
class IndustrialTrade(_OptionPart):
    """Random industrial trade used in business names."""

    _options: ClassVar[list[str]] = _BUSINESS_PARTS["industrialTrades"]


@dataclass(frozen=True)
class ShopType(_OptionPart):
    """Random shop type used in business names."""

    _options: ClassVar[list[str]] = _BUSINESS_PARTS["shopTypes"]


@dataclass(frozen=True)
class CelestialObjectType(_OptionPart):
    """Random celestial object type."""

    _options: ClassVar[list[str]] = _CELESTIAL_PARTS["celestialObjects"]


@dataclass(frozen=True)
class OrganizationSymbol(_OptionPart):
    """Random symbol used in organization names."""

    _options: ClassVar[list[str]] = _PLACE_PARTS["organizationSymbols"]


@dataclass(frozen=True)
class ArtifactObject(_OptionPart):
    """Random ritual object used in artifact names."""

    _options: ClassVar[list[str]] = load_json("Artifact Objects.json")


@dataclass(frozen=True)
class SpellEffect(_OptionPart):
    """Random magical effect used in spell names."""

    _options: ClassVar[list[str]] = load_json("Spell Effects.json")


@dataclass(frozen=True)
class MagicalConcept(_OptionPart):
    """Random magical concept used in artifact and spell names."""

    _options: ClassVar[list[str]] = load_json("Magical Concepts.json")


@dataclass(frozen=True)
class OperationColor(_OptionPart):
    """Random short codename color used in operation names."""

    _options: ClassVar[list[str]] = load_json("Operation Colors.json")


@dataclass(frozen=True)
class Season(_OptionPart):
    """Random season used in festival names."""

    _options: ClassVar[list[str]] = load_json("Seasons.json")


@dataclass(frozen=True)
class NaturalNameRoot(Component):
    """Random root for a landmark or creature name."""

    context: Literal["landmark", "creature"]

    def __post_init__(self) -> None:
        if self.context not in ("landmark", "creature"):
            raise ValueError("context must be 'landmark' or 'creature'")

    def make_text(self, rng: random.Random) -> str:
        key = "landmarkRoots" if self.context == "landmark" else "appearanceRoots"
        if self.context == "landmark":
            options = _PLACE_PARTS[key]
        else:
            options = _CREATURE_PARTS[key]
        return rng.choice(options)
