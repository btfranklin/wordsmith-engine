"""Album title generators."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import one_of, weighted_one_of
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
class AlbumTitle(Component):
    """Top-level album title generator."""

    def make_text(self, rng: random.Random) -> str:
        component = weighted_one_of(
            (0.35, ShortAlbumTitle()),
            (0.25, FragmentAlbumTitle()),
            (0.22, DocumentaryAlbumTitle()),
            (0.18, CollisionAlbumTitle()),
        )
        return component.make_text(rng)


@dataclass(frozen=True)
class ShortAlbumTitle(Component):
    """Generate a compact album title."""

    def make_text(self, rng: random.Random) -> str:
        noun_plural = rng.choice([True, False])
        component = weighted_one_of(
            (2.0, Noun(is_plural=True)),
            (2.0, Adjective() | Noun(is_plural=noun_plural)),
            (1.4, TimeOfDay() | Noun(is_plural=True)),
            (1.2, UCBerkeleyEmotion()),
            (1.2, MartialSocialConcept()),
            (1.0, AuthoredArtifact()),
        )
        return component.title_case().make_text(rng)


@dataclass(frozen=True)
class FragmentAlbumTitle(Component):
    """Generate a phrase-fragment album title."""

    def make_text(self, rng: random.Random) -> str:
        noun_plural = rng.choice([True, False])
        component = weighted_one_of(
            (
                1.8,
                one_of("no", "new", "old", "last", "first")
                | Noun(is_plural=noun_plural),
            ),
            (1.6, TimeOfDay() | "with" | Noun(is_plural=True)),
            (1.4, Noun() | "for" | Noun(is_plural=True)),
            (1.2, UCBerkeleyEmotion() | "for" | PersonName()),
            (1.0, Verb(tense=VerbTense.BASE) | "the" | Noun()),
        )
        return component.title_case().make_text(rng)


@dataclass(frozen=True)
class DocumentaryAlbumTitle(Component):
    """Generate a session or document-shaped album title."""

    def make_text(self, rng: random.Random) -> str:
        component = weighted_one_of(
            (2.0, TownName() | one_of("sessions", "recordings")),
            (1.6, PersonName().possessive_form() | AuthoredArtifact()),
            (1.4, AuthoredArtifact() | "from" | TownName()),
            (
                1.4,
                one_of("songs for", "music for")
                | one_of(
                    Noun(is_plural=True),
                    UCBerkeleyEmotion(),
                    MartialSocialConcept(),
                ),
            ),
            (1.0, TimeOfDay() | one_of("sessions", "recordings")),
        )
        return component.title_case().make_text(rng)


@dataclass(frozen=True)
class CollisionAlbumTitle(Component):
    """Generate a collision-shaped album title."""

    def make_text(self, rng: random.Random) -> str:
        component = weighted_one_of(
            (1.8, Noun() + " / " + Noun()),
            (1.6, Noun() | "and" | Noun(is_plural=True)),
            (1.4, Adjective() | "and" | Adjective()),
            (1.2, UCBerkeleyEmotion() | "and" | Noun(is_plural=True)),
            (1.0, MartialSocialConcept() | "/" | UCBerkeleyEmotion()),
        )
        return component.title_case().make_text(rng)
