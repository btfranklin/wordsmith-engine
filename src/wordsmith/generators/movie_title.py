"""Movie title generators."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import one_of, weighted_one_of
from wordsmith.generators.literary_title import LiteraryTitle
from wordsmith.generators.town_name import TownName
from wordsmith.names.person_name import PersonName
from wordsmith.words.base import (
    Adjective,
    AuthoredArtifact,
    MartialSocialConcept,
    Noun,
    TimeOfDay,
    UCBerkeleyEmotion,
    Verb,
    VerbTense,
)


@dataclass(frozen=True)
class MovieTitle(Component):
    """Top-level movie title generator."""

    def make_text(self, rng: random.Random) -> str:
        component = weighted_one_of(
            (0.55, SimpleMovieTitle()),
            (0.30, HighConceptMovieTitle()),
            (0.15, LiteraryTitle()),
        )
        return component.make_text(rng)


@dataclass(frozen=True)
class SimpleMovieTitle(Component):
    """Generate a straightforward movie title."""

    def make_text(self, rng: random.Random) -> str:
        component = weighted_one_of(
            (2.0, PersonName()),
            (1.8, TownName()),
            (1.7, "the" | Adjective() | Noun()),
            (1.7, "the" | Noun() | "of" | TownName()),
            (1.5, TimeOfDay() | "in" | TownName()),
            (1.4, MartialSocialConcept() | "at" | TownName()),
            (1.3, UCBerkeleyEmotion() | "and" | MartialSocialConcept()),
            (1.2, PersonName().possessive_form() | AuthoredArtifact()),
            (1.0, "the" | AuthoredArtifact() | "of" | PersonName()),
        )
        return component.title_case().make_text(rng)


@dataclass(frozen=True)
class HighConceptMovieTitle(Component):
    """Generate a hook-shaped movie title."""

    def make_text(self, rng: random.Random) -> str:
        component = weighted_one_of(
            (
                2.2,
                one_of(
                    "escape from",
                    "return to",
                    "the fall of",
                    "the last days of",
                )
                | TownName(),
            ),
            (
                1.8,
                one_of("before", "after", "when")
                | Noun().prefixed_by_article()
                | Verb(tense=VerbTense.PRESENT),
            ),
            (
                1.6,
                one_of("before", "after", "when")
                | PersonName()
                | Verb(tense=VerbTense.PRESENT),
            ),
            (
                1.4,
                "the"
                | one_of("case", "secret", "trial", "shadow")
                | "of"
                | TownName(),
            ),
            (
                1.2,
                "the"
                | one_of("first", "last", "final")
                | one_of(AuthoredArtifact(), Noun()),
            ),
            (1.0, "the" | Noun() | "that" | Verb(tense=VerbTense.PAST)),
        )
        return component.title_case().make_text(rng)
