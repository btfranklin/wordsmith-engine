"""Static consumer exercising representative public Python API types."""

from __future__ import annotations

import random

from wordsmith import (
    Adjective,
    AlienName,
    Article,
    BinaryGender,
    Component,
    Determiner,
    FantasyName,
    GivenName,
    GivenNameCulture,
    Literal,
    Noun,
    NounForm,
    OneOf,
    PersonName,
    PrimitiveWeapon,
    Pronoun,
    Text,
    Verb,
    VerbTense,
    VillainousPersonNoun,
    WeightedOneOf,
    either,
    maybe,
    one_of,
    text,
    weighted_one_of,
)


def render_public_components(rng: random.Random) -> list[str]:
    """Construct and render the typed public component surface."""
    noun = Noun(form=NounForm.PLURAL)
    verb = Verb(tense=VerbTense.PAST_PARTICIPLE)
    person = PersonName(
        gender=BinaryGender.FEMALE,
        culture=GivenNameCulture.ENGLISH_SPEAKING,
    )
    literal_parts = [Literal("quiet"), Literal("bright")]
    direct_text = Text(literal_parts, sep=" ")
    stored_parts: tuple[Component, ...] = direct_text.parts
    direct_choice = WeightedOneOf(literal_parts, [2.0, 1.0])
    stored_options: tuple[Component, ...] = direct_choice.options
    stored_weights: tuple[float, ...] = direct_choice.weights

    components: list[Component] = [
        direct_text,
        Text(stored_parts, sep=" "),
        OneOf(literal_parts),
        OneOf(stored_parts),
        direct_choice,
        WeightedOneOf(stored_options, stored_weights),
        Literal("the"),
        text("the", Adjective(), noun, sep=" "),
        one_of("quiet", Adjective()),
        weighted_one_of((2.0, "quiet"), (1.0, Adjective())),
        either("past", verb, first_probability=0.25),
        maybe("very", Adjective(), probability=0.75),
        ("the" | noun).title_case().possessive_form(),
        (Literal("hour") + "glass").first_upper(),
        Literal("artifact").capitalized().prefixed_by_article(),
        Literal("engine").prefixed_by_determiner(),
        Article(is_before_vowel=True),
        Determiner(is_before_vowel=False),
        Pronoun(is_singular=True, is_third_person=False),
        PrimitiveWeapon(is_plural=True),
        VillainousPersonNoun(is_plural=False),
        GivenName(gender=BinaryGender.MALE, culture=GivenNameCulture.EASTERN),
        person,
        AlienName(
            syllable_count=3,
            allow_hyphen=True,
            allow_apostrophe=False,
        ),
        FantasyName(
            syllable_count=4,
            allow_hyphen=False,
            allow_apostrophe=True,
        ),
    ]
    return [component(rng) for component in components]
