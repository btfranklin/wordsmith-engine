"""Literary title generators."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import random
from typing import ClassVar

from wordsmith.core.base import Component
from wordsmith.core.components import maybe, one_of, weighted_one_of
from wordsmith.generators.town_name import TownName
from wordsmith.names.person_name import PersonName
from wordsmith.words.base import (
    AuthoredArtifact,
    MartialSocialConcept,
    TimeOfDay,
    UCBerkeleyEmotion,
)


class TitleVerbForm(Enum):
    """Verb form indices for title-verb rows."""

    BASE = 0
    FINITE = 1
    GERUND = 2


@dataclass(frozen=True)
class LiteraryTitleObject(Component):
    """Random literary-title object with optional pluralization."""

    is_plural: bool = False

    _singular_options: ClassVar[list[str]] = [
        "archive",
        "bell",
        "bridge",
        "camera",
        "cipher",
        "clock",
        "compass",
        "door",
        "garden",
        "harbor",
        "key",
        "lantern",
        "machine",
        "map",
        "mirror",
        "moon",
        "orchard",
        "room",
        "signal",
        "staircase",
        "station",
        "thread",
        "window",
    ]
    _plural_options: ClassVar[list[str]] = [
        "archives",
        "bells",
        "bridges",
        "cities",
        "clocks",
        "doors",
        "gardens",
        "harbors",
        "lanterns",
        "machines",
        "maps",
        "mirrors",
        "moons",
        "orchards",
        "rooms",
        "signals",
        "staircases",
        "stations",
        "threads",
        "windows",
    ]

    def make_text(self, rng: random.Random) -> str:
        options = self._plural_options if self.is_plural else self._singular_options
        return rng.choice(options)


@dataclass(frozen=True)
class SentientLiteraryTitleObject(Component):
    """Concrete image that can plausibly act in an unusual title."""

    _options: ClassVar[list[str]] = [
        "archive",
        "bell",
        "city",
        "clock",
        "door",
        "garden",
        "ghost",
        "harbor",
        "house",
        "lantern",
        "machine",
        "map",
        "mirror",
        "moon",
        "river",
        "signal",
        "station",
        "window",
    ]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class TitleQuality(Component):
    """Evocative modifier tuned for literary titles."""

    _options: ClassVar[list[str]] = [
        "borrowed",
        "bright",
        "buried",
        "distant",
        "divided",
        "forgotten",
        "hidden",
        "hollow",
        "last",
        "little",
        "lost",
        "minor",
        "paper",
        "red",
        "restless",
        "second",
        "secret",
        "silver",
        "sleeping",
        "strange",
        "summer",
        "vanishing",
        "winter",
    ]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class TitleAbstraction(Component):
    """Abstract word curated for literary-title weight."""

    _options: ClassVar[list[str]] = [
        "absence",
        "arrival",
        "beauty",
        "ceremony",
        "distance",
        "forgiveness",
        "hunger",
        "memory",
        "mercy",
        "noise",
        "patience",
        "promise",
        "silence",
        "weather",
    ]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class AbstractSubject(Component):
    """Abstract subject that may draw from existing concept components."""

    def make_text(self, rng: random.Random) -> str:
        return one_of(
            TitleAbstraction(),
            UCBerkeleyEmotion(),
            MartialSocialConcept(),
        ).make_text(rng)


@dataclass(frozen=True)
class ResonantSubject(Component):
    """Subject that reads naturally after title prepositions."""

    def make_text(self, rng: random.Random) -> str:
        return one_of(
            LiteraryTitleObject(is_plural=True),
            AbstractSubject(),
            PersonName(),
            TownName(),
        ).make_text(rng)


@dataclass(frozen=True)
class TitleNounPhrase(Component):
    """Definite noun phrase with an optional title-quality modifier."""

    wrapped: Component
    requires_modifier: bool = False
    modifier_probability: float = 0.45

    def make_text(self, rng: random.Random) -> str:
        modifier = (
            TitleQuality()
            if self.requires_modifier
            else maybe(TitleQuality(), probability=self.modifier_probability)
        )
        return ("the" | modifier | self.wrapped).make_text(rng)


@dataclass(frozen=True)
class TitleVerb(Component):
    """Verb chosen for title coherence."""

    form: TitleVerbForm = TitleVerbForm.FINITE

    _options: ClassVar[list[list[str]]] = [
        ["answer", "answers", "answering"],
        ["arrive", "arrives", "arriving"],
        ["burn", "burns", "burning"],
        ["dream", "dreams", "dreaming of"],
        ["find", "finds", "finding"],
        ["forget", "forgets", "forgetting"],
        ["listen", "listens", "listening to"],
        ["remember", "remembers", "remembering"],
        ["return", "returns", "returning to"],
        ["sing", "sings", "singing to"],
        ["speak", "speaks", "speaking with"],
        ["vanish", "vanishes", "vanishing"],
        ["wait", "waits", "waiting"],
        ["wake", "wakes", "waking"],
    ]

    def make_text(self, rng: random.Random) -> str:
        verb_row = rng.choice(self._options)
        return verb_row[self.form.value]


@dataclass(frozen=True)
class ImpossibleAction(Component):
    """Surreal but readable verb phrase."""

    def make_text(self, rng: random.Random) -> str:
        return one_of(
            TitleVerb(form=TitleVerbForm.GERUND)
            | TitleNounPhrase(LiteraryTitleObject()),
            TitleVerb(form=TitleVerbForm.GERUND) | AbstractSubject(),
            "cataloging" | LiteraryTitleObject(is_plural=True),
            "repairing" | TitleNounPhrase(LiteraryTitleObject()),
            "teaching"
            | TitleNounPhrase(SentientLiteraryTitleObject())
            | "to"
            | TitleVerb(form=TitleVerbForm.BASE),
        ).make_text(rng)


@dataclass(frozen=True)
class PlaceSuffix(Component):
    """Place-inflected title noun."""

    _options: ClassVar[list[str]] = [
        "almanac",
        "blues",
        "chronicle",
        "dispatch",
        "elegy",
        "lantern",
        "ledger",
        "nocturne",
        "parable",
        "refrain",
    ]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._options)


@dataclass(frozen=True)
class LiteraryTitle(Component):
    """Top-level literary title generator."""

    def make_text(self, rng: random.Random) -> str:
        component = weighted_one_of(
            (0.78, SimpleLiteraryTitle()),
            (0.22, UnusualLiteraryTitle()),
        )
        return component.make_text(rng)


@dataclass(frozen=True)
class SimpleLiteraryTitle(Component):
    """Generate a straightforward literary title."""

    def make_text(self, rng: random.Random) -> str:
        component = weighted_one_of(
            (3.0, TitleNounPhrase(LiteraryTitleObject(), requires_modifier=True)),
            (2.5, TitleNounPhrase(LiteraryTitleObject()) | "of" | ResonantSubject()),
            (2.5, TitleNounPhrase(LiteraryTitleObject()) | "at" | TownName()),
            (2.0, AbstractSubject() | "and" | AbstractSubject()),
            (2.0, AbstractSubject() | "in" | TownName()),
            (1.8, TitleNounPhrase(AuthoredArtifact()) | "of" | ResonantSubject()),
            (1.5, PersonName().possessive_form() | AuthoredArtifact()),
            (
                1.5,
                one_of(
                    "a field guide to",
                    "a history of",
                    "a map of",
                    "a study of",
                    "an atlas of",
                    "notes on",
                    "the book of",
                    "the grammar of",
                )
                | ResonantSubject(),
            ),
            (1.2, TimeOfDay() | "with" | ResonantSubject()),
            (
                1.2,
                one_of(
                    "passage through" | LiteraryTitleObject(is_plural=True),
                    "the road to" | AbstractSubject(),
                    "the road to" | TownName(),
                    "the voyage into" | AbstractSubject(),
                    "the voyage to" | TownName(),
                ),
            ),
            (1.0, TownName() | PlaceSuffix()),
        )
        return component.title_case().make_text(rng)


@dataclass(frozen=True)
class UnusualLiteraryTitle(Component):
    """Generate a more unusual literary title."""

    def make_text(self, rng: random.Random) -> str:
        component = weighted_one_of(
            (
                2.4,
                one_of(
                    "a manual for",
                    "a recipe for",
                    "instructions for",
                    "rules for",
                    "the practice of",
                )
                | ImpossibleAction(),
            ),
            (
                2.2,
                TitleNounPhrase(SentientLiteraryTitleObject())
                | "that"
                | TitleVerb(form=TitleVerbForm.FINITE),
            ),
            (
                2.0,
                TitleNounPhrase(LiteraryTitleObject())
                | "between"
                | LiteraryTitleObject(is_plural=True),
            ),
            (
                1.8,
                one_of("after", "before", "if", "until", "when", "while")
                | TitleNounPhrase(SentientLiteraryTitleObject())
                | TitleVerb(form=TitleVerbForm.FINITE),
            ),
            (
                1.6,
                one_of("how", "why")
                | TitleNounPhrase(SentientLiteraryTitleObject())
                | TitleVerb(form=TitleVerbForm.FINITE),
            ),
            (1.5, AbstractSubject() | "after" | AbstractSubject()),
            (1.4, PlaceSuffix() | "for" | ResonantSubject()),
            (
                1.2,
                TitleNounPhrase(AuthoredArtifact()) | "against" | AbstractSubject(),
            ),
            (
                1.0,
                TitleNounPhrase(LiteraryTitleObject())
                | "inside"
                | TitleNounPhrase(LiteraryTitleObject()),
            ),
        )
        return component.title_case().make_text(rng)
