"""Work title generators."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import either, maybe, one_of, text
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
            text(
                either(UCBerkeleyEmotion(), MartialSocialConcept()),
                "in",
                TownName(),
                sep=" ",
            ),
            text(Adjective(), Verb(tense=VerbTense.PRESENT_PERFECT), sep=" "),
            text(TimeOfDay(), Verb(tense=VerbTense.PRESENT), sep=" "),
            text(TimeOfDay(), Noun(is_plural=noun_plural_2), sep=" "),
            text(Adjective(), Noun(is_plural=noun_plural_3), sep=" "),
            text(Adjective().prefixed_by_article(), Noun(), sep=" "),
            text(Adjective().prefixed_by_determiner(), Noun(), sep=" "),
            text(MartialSocialConcept(), "and", MartialSocialConcept(), sep=" "),
            text(
                one_of(
                    "A Treatise on",
                    "On",
                    "A Discussion of",
                    "An Analysis of",
                    "Commentary on",
                    "An Examination of",
                ),
                either(MartialSocialConcept(), Noun(is_plural=True)),
                sep=" ",
            ),
            text(
                "The",
                maybe(Adjective()),
                one_of("Adventures", "Journey", "Journeys", "Travels", "Tale", "Voyage"),
                "of the",
                text("'", NauticalShipName(), "'"),
                sep=" ",
            ),
            text(
                "The",
                maybe(Adjective()),
                one_of("Adventures", "Journey", "Journeys", "Travels", "Tale", "Escapades"),
                "of",
                PersonName(),
                sep=" ",
            ),
            text(
                "The",
                maybe(Adjective()),
                Noun(is_plural=noun_plural_4),
                either("in", "of"),
                TownName(),
                sep=" ",
            ),
        )

        return component.title_case().make_text(rng)


@dataclass(frozen=True)
class UnusualWorkTitle(Component):
    """Generate a more unusual work title."""

    def make_text(self, rng: random.Random) -> str:
        component = one_of(
            text(UCBerkeleyEmotion(), Adverb(), Verb(tense=VerbTense.PRESENT), sep=" "),
            text(UCBerkeleyEmotion(), "and", UCBerkeleyEmotion(), sep=" "),
            text(
                UCBerkeleyEmotion(),
                maybe("and ", UCBerkeleyEmotion()),
                "in",
                TownName(),
                sep=" ",
            ),
            text(
                text("'", SimpleWorkTitle(), "'"),
                one_of("Revisited", "Revised", "Reimagined", "Renewed", "Rethought", "Redux"),
                sep=" ",
            ),
            text(Verb(tense=VerbTense.PRESENT_PERFECT), Noun().prefixed_by_determiner(), sep=" "),
            text(
                one_of("When", "Where", "Why", "While", "As", "Until", "Because"),
                Noun().prefixed_by_article(),
                Verb(tense=VerbTense.PRESENT),
                sep=" ",
            ),
            text(
                one_of("When", "Where", "Why", "While", "As", "Until", "Because"),
                either(
                    one_of(
                        text(
                            Pronoun(
                                is_singular=False,
                                is_third_person=rng.choice([True, False]),
                            ),
                            Verb(tense=VerbTense.BASE),
                            sep=" ",
                        ),
                        text(
                            Pronoun(is_singular=True, is_third_person=False),
                            Verb(tense=VerbTense.BASE),
                            sep=" ",
                        ),
                        text(
                            Pronoun(is_singular=True, is_third_person=True),
                            Verb(tense=VerbTense.PRESENT),
                            sep=" ",
                        ),
                    ),
                    text(
                        Pronoun(
                            is_singular=rng.choice([True, False]),
                            is_third_person=rng.choice([True, False]),
                        ),
                        Verb(tense=VerbTense.PAST),
                        sep=" ",
                    ),
                ),
                sep=" ",
            ),
            text(
                Adjective(),
                maybe(", ", Adjective(), ","),
                " and ",
                Adjective(),
                sep="",
            ),
            text(
                Noun().prefixed_by_determiner(),
                one_of(
                    Verb(tense=VerbTense.PRESENT),
                    text(one_of("Will", "Shall", "Can", "Must", "May"), Verb(), sep=" "),
                    text("Is", Verb(tense=VerbTense.PRESENT_PERFECT), sep=" "),
                    text("Has", Verb(tense=VerbTense.PAST_PARTICIPLE), sep=" "),
                ),
                sep=" ",
            ),
            either(
                text(Noun(), "and", Noun(), sep=" "),
                text(
                    Noun().prefixed_by_determiner(),
                    "and",
                    Noun().prefixed_by_determiner(),
                    sep=" ",
                ),
            ),
            text(text(MartialSocialConcept(), ":", sep=""), UnusualWorkTitle(), sep=" "),
        )

        return component.title_case().make_text(rng)
