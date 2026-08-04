"""Base word types used by Wordsmith generators."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import random
from typing import ClassVar

from wordsmith.core.base import Component
from wordsmith.util import load_json

_CURATED_WORD_LISTS: dict[str, list[str]] = load_json(
    "Curated Word Lists.json"
)


@dataclass(frozen=True)
class Adjective(Component):
    """Random adjective from the asset list."""

    _options: ClassVar[list[str]] = load_json("Adjectives.json")

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class Adverb(Component):
    """Random adverb from the asset list."""

    _options: ClassVar[list[str]] = load_json("Adverbs.json")

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


class NounForm(Enum):
    """Noun form indices."""

    SINGULAR = 0
    PLURAL = 1


@dataclass(frozen=True)
class Noun(Component):
    """Random noun in the requested form."""

    form: NounForm = NounForm.SINGULAR

    _options: ClassVar[list[list[str]]] = load_json("Nouns.json")

    def make_text(self, rng: random.Random) -> str:
        noun_row = rng.choice(self._options)
        return noun_row[self.form.value]


class VerbTense(Enum):
    """Verb tense indices for verb rows."""

    BASE = 0
    PAST = 1
    PAST_PARTICIPLE = 2
    PRESENT = 3
    PRESENT_PERFECT = 4


@dataclass(frozen=True)
class Verb(Component):
    """Random verb in the requested tense."""

    tense: VerbTense = VerbTense.BASE

    _options: ClassVar[list[list[str]]] = load_json("Verbs.json")

    def make_text(self, rng: random.Random) -> str:
        verb_row = rng.choice(self._options)
        return verb_row[self.tense.value]


@dataclass(frozen=True)
class Pronoun(Component):
    """Random pronoun based on person and number."""

    is_singular: bool
    is_third_person: bool

    def __post_init__(self) -> None:
        if not isinstance(self.is_singular, bool):
            raise TypeError("is_singular must be a boolean")
        if not isinstance(self.is_third_person, bool):
            raise TypeError("is_third_person must be a boolean")

    def make_text(self, rng: random.Random) -> str:
        if self.is_third_person:
            if self.is_singular:
                return rng.choice(["he", "she", "it"])
            return "they"

        if self.is_singular:
            return rng.choice(["I", "you"])
        return rng.choice(["we", "you"])


@dataclass(frozen=True)
class ChemicalCompoundName(Component):
    """Random chemical compound name."""

    _options: ClassVar[list[str]] = load_json("Chemical Compound Names.json")

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class AuthoredArtifact(Component):
    """Random authored or documented artifact."""

    _options: ClassVar[list[str]] = _CURATED_WORD_LISTS["authoredArtifacts"]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class LocationAdjective(Component):
    """Random location adjective."""

    _options: ClassVar[list[str]] = _CURATED_WORD_LISTS["locationAdjectives"]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class MartialSocialConcept(Component):
    """Random martial or social concept."""

    _options: ClassVar[list[str]] = _CURATED_WORD_LISTS["martialSocialConcepts"]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class UCBerkeleyEmotion(Component):
    """Random emotion from the UC Berkeley dataset."""

    _options: ClassVar[list[str]] = _CURATED_WORD_LISTS["ucBerkeleyEmotions"]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class VillainousPersonNoun(Component):
    """Random villainous person noun with optional pluralization."""

    is_plural: bool

    _options: ClassVar[list[str]] = _CURATED_WORD_LISTS["villainousPersonNouns"]

    def __post_init__(self) -> None:
        if not isinstance(self.is_plural, bool):
            raise TypeError("is_plural must be a boolean")

    def make_text(self, rng: random.Random) -> str:
        text = rng.choice(self._options)

        if self.is_plural:
            if text.endswith(("ay", "ey", "iy", "oy", "uy")):
                text += "s"
            elif text.endswith("y"):
                text = f"{text[:-1]}ies"
            elif text.endswith(("x", "ss", "sh", "ch")):
                text += "es"
            elif text.endswith("ife"):
                if text == "lowlife":
                    text += "s"
                else:
                    text = f"{text[:-2]}ves"
            elif text.endswith(("rf", "ief")):
                text = f"{text[:-1]}ves"
            elif text.endswith("man"):
                text = f"{text[:-2]}en"
            elif not text.endswith("s"):
                text += "s"

        return text


@dataclass(frozen=True)
class PrimitiveWeapon(Component):
    """Random primitive weapon with optional pluralization."""

    is_plural: bool = False

    _options: ClassVar[list[str]] = _CURATED_WORD_LISTS["primitiveWeapons"]

    def __post_init__(self) -> None:
        if not isinstance(self.is_plural, bool):
            raise TypeError("is_plural must be a boolean")

    def make_text(self, rng: random.Random) -> str:
        value = rng.choice(self._options)
        if self.is_plural:
            if value.endswith("ife"):
                value = f"{value[:-2]}ves"
            else:
                value += "s"
        return value


@dataclass(frozen=True)
class NauticalShipNameObject(Component):
    """Random ship name object."""

    _options: ClassVar[list[str]] = _CURATED_WORD_LISTS["nauticalShipNameObjects"]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class NauticalShipNameColor(Component):
    """Random ship name color."""

    _options: ClassVar[list[str]] = _CURATED_WORD_LISTS["nauticalShipNameColors"]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class ShipNameAdjective(Component):
    """Random ship name adjective."""

    _options: ClassVar[list[str]] = _CURATED_WORD_LISTS["shipNameAdjectives"]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class TimeOfDay(Component):
    """Random time-of-day word."""

    _options: ClassVar[list[str]] = _CURATED_WORD_LISTS["timesOfDay"]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)
