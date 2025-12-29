"""Work title generators."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import either, maybe, one_of
from wordsmith.generators.criminal_gang_name import CriminalGangName
from wordsmith.generators.nautical_ship_name import NauticalShipName
from wordsmith.generators.town_name import TownName
from wordsmith.names.person_name import PersonName
from wordsmith.words.base import (
    Adjective,
    Adverb,
    MartialSocialConcept,
    Noun,
    Pronoun,
    TimeOfDay,
    UCBerkeleyEmotion,
    Verb,
    VerbTense,
)


@dataclass(frozen=True)
class WorkTitle(Component):
    """Top-level work title generator."""

    def make_text(self, rng: random.Random) -> str:
        return either(SimpleWorkTitle(), UnusualWorkTitle(), first_probability=0.85).make_text(rng)


@dataclass(frozen=True)
class SimpleWorkTitle(Component):
    """Generate a straightforward work title."""

    def make_text(self, rng: random.Random) -> str:
        noun_plural_1 = rng.choice([True, False])
        noun_plural_2 = rng.choice([True, False])
        noun_plural_3 = rng.choice([True, False])
        noun_plural_4 = rng.choice([True, False])

        component = one_of(
            Noun(is_plural=noun_plural_1),
            Noun().prefixed_by_article(),
            Noun().prefixed_by_determiner(),
            Adjective(),
            Adverb(),
            Verb(tense=VerbTense.PRESENT_PERFECT),
            PersonName(),
            TownName(),
            UCBerkeleyEmotion(),
            UCBerkeleyEmotion().prefixed_by_determiner(),
            CriminalGangName(),
            either(UCBerkeleyEmotion(), MartialSocialConcept()) | "in" | TownName(),
            Adjective() | Verb(tense=VerbTense.PRESENT_PERFECT),
            TimeOfDay() | Verb(tense=VerbTense.PRESENT),
            TimeOfDay() | Noun(is_plural=noun_plural_2),
            Adjective() | Noun(is_plural=noun_plural_3),
            Adjective().prefixed_by_article() | Noun(),
            Adjective().prefixed_by_determiner() | Noun(),
            MartialSocialConcept() | "and" | MartialSocialConcept(),
            one_of(
                "A Treatise on",
                "On",
                "A Discussion of",
                "An Analysis of",
                "Commentary on",
                "An Examination of",
            )
            | either(MartialSocialConcept(), Noun(is_plural=True)),
            "The"
            | maybe(Adjective())
            | one_of("Adventures", "Journey", "Journeys", "Travels", "Tale", "Voyage")
            | "of the"
            | ("'" + NauticalShipName() + "'"),
            "The"
            | maybe(Adjective())
            | one_of("Adventures", "Journey", "Journeys", "Travels", "Tale", "Escapades")
            | "of"
            | PersonName(),
            "The"
            | maybe(Adjective())
            | Noun(is_plural=noun_plural_4)
            | either("in", "of")
            | TownName(),
        )

        return component.title_case().make_text(rng)


@dataclass(frozen=True)
class UnusualWorkTitle(Component):
    """Generate a more unusual work title."""

    def make_text(self, rng: random.Random) -> str:
        component = one_of(
            UCBerkeleyEmotion() | Adverb() | Verb(tense=VerbTense.PRESENT),
            UCBerkeleyEmotion() | "and" | UCBerkeleyEmotion(),
            UCBerkeleyEmotion() | maybe("and " + UCBerkeleyEmotion()) | "in" | TownName(),
            ("'" + SimpleWorkTitle() + "'")
            | one_of("Revisited", "Revised", "Reimagined", "Renewed", "Rethought", "Redux"),
            Verb(tense=VerbTense.PRESENT_PERFECT) | Noun().prefixed_by_determiner(),
            one_of("When", "Where", "Why", "While", "As", "Until", "Because")
            | Noun().prefixed_by_article()
            | Verb(tense=VerbTense.PRESENT),
            one_of("When", "Where", "Why", "While", "As", "Until", "Because")
            | either(
                one_of(
                    Pronoun(
                        is_singular=False,
                        is_third_person=rng.choice([True, False]),
                    )
                    | Verb(tense=VerbTense.BASE),
                    Pronoun(is_singular=True, is_third_person=False)
                    | Verb(tense=VerbTense.BASE),
                    Pronoun(is_singular=True, is_third_person=True)
                    | Verb(tense=VerbTense.PRESENT),
                ),
                Pronoun(
                    is_singular=rng.choice([True, False]),
                    is_third_person=rng.choice([True, False]),
                )
                | Verb(tense=VerbTense.PAST),
            ),
            Adjective() + maybe(", " + Adjective() + ",") + " and " + Adjective(),
            Noun().prefixed_by_determiner()
            | one_of(
                Verb(tense=VerbTense.PRESENT),
                one_of("Will", "Shall", "Can", "Must", "May") | Verb(),
                "Is" | Verb(tense=VerbTense.PRESENT_PERFECT),
                "Has" | Verb(tense=VerbTense.PAST_PARTICIPLE),
            ),
            either(
                Noun() | "and" | Noun(),
                Noun().prefixed_by_determiner()
                | "and"
                | Noun().prefixed_by_determiner(),
            ),
            (MartialSocialConcept() + ":") | UnusualWorkTitle(),
        )

        return component.title_case().make_text(rng)
