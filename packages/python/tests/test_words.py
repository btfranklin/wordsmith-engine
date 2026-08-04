"""Tests for base word generators."""

from __future__ import annotations

import random
from typing import TypeVar

import pytest

from tests.utils import assert_in_options
from wordsmith.words import (
    Adjective,
    Adverb,
    Article,
    AuthoredArtifact,
    ChemicalCompoundName,
    Determiner,
    LocationAdjective,
    MartialSocialConcept,
    NauticalShipNameColor,
    NauticalShipNameObject,
    Noun,
    NounForm,
    PrimitiveWeapon,
    Pronoun,
    ShipNameAdjective,
    TimeOfDay,
    UCBerkeleyEmotion,
    Verb,
    VerbTense,
    VillainousPersonNoun,
)


ChoiceValue = TypeVar("ChoiceValue")


class ChoiceRandom:
    """Deterministic RNG that always returns a chosen value."""

    def __init__(self, value: ChoiceValue) -> None:
        self._value = value

    def choice(self, options: list[ChoiceValue]) -> ChoiceValue:
        return self._value


def test_adjective_from_assets() -> None:
    rng = random.Random(0)
    value = Adjective().make_text(rng)
    assert_in_options(value, Adjective._options)


def test_adverb_from_assets() -> None:
    rng = random.Random(1)
    value = Adverb().make_text(rng)
    assert_in_options(value, Adverb._options)


def test_noun_pluralization_rules() -> None:
    plural_noun = Noun(form=NounForm.PLURAL)

    assert plural_noun.make_text(ChoiceRandom(["city", "cities"])) == "cities"
    assert plural_noun.make_text(ChoiceRandom(["box", "boxes"])) == "boxes"
    assert plural_noun.make_text(ChoiceRandom(["knife", "knives"])) == "knives"
    assert plural_noun.make_text(ChoiceRandom(["human", "humans"])) == "humans"
    assert plural_noun.make_text(ChoiceRandom(["fireman", "firemen"])) == "firemen"


def test_noun_irregular_pluralization_rules() -> None:
    plural_noun = Noun(form=NounForm.PLURAL)

    assert plural_noun.make_text(ChoiceRandom(["child", "children"])) == "children"
    assert plural_noun.make_text(ChoiceRandom(["foot", "feet"])) == "feet"
    assert plural_noun.make_text(ChoiceRandom(["tooth", "teeth"])) == "teeth"
    assert plural_noun.make_text(ChoiceRandom(["mouse", "mice"])) == "mice"
    assert plural_noun.make_text(ChoiceRandom(["person", "people"])) == "people"
    assert plural_noun.make_text(ChoiceRandom(["woman", "women"])) == "women"
    assert plural_noun.make_text(ChoiceRandom(["man", "men"])) == "men"
    assert plural_noun.make_text(ChoiceRandom(["goose", "geese"])) == "geese"
    assert plural_noun.make_text(ChoiceRandom(["ox", "oxen"])) == "oxen"
    assert plural_noun.make_text(ChoiceRandom(["criterion", "criteria"])) == "criteria"
    assert plural_noun.make_text(ChoiceRandom(["medium", "media"])) == "media"
    assert plural_noun.make_text(ChoiceRandom(["foot", "feet"])) != "feets"


def test_noun_source_uses_canonical_singular_irregulars() -> None:
    noun_rows = {row[NounForm.SINGULAR.value]: row for row in Noun._options}

    assert noun_rows["child"][NounForm.PLURAL.value] == "children"
    assert noun_rows["foot"][NounForm.PLURAL.value] == "feet"
    assert noun_rows["tooth"][NounForm.PLURAL.value] == "teeth"
    assert noun_rows["mouse"][NounForm.PLURAL.value] == "mice"
    assert noun_rows["person"][NounForm.PLURAL.value] == "people"
    assert noun_rows["woman"][NounForm.PLURAL.value] == "women"
    assert noun_rows["criterion"][NounForm.PLURAL.value] == "criteria"
    assert noun_rows["medium"][NounForm.PLURAL.value] == "media"

    assert "children" not in noun_rows
    assert "feet" not in noun_rows
    assert "teeth" not in noun_rows
    assert "mice" not in noun_rows
    assert "people" not in noun_rows
    assert "women" not in noun_rows
    assert "criteria" not in noun_rows
    assert "media" not in noun_rows


def test_noun_source_rows_match_noun_forms() -> None:
    assert all(len(row) == len(NounForm) for row in Noun._options)


def test_verb_tense_selection() -> None:
    rng = random.Random(2)
    value = Verb(tense=VerbTense.PRESENT).make_text(rng)
    assert any(row[VerbTense.PRESENT.value] == value for row in Verb._options)


def test_pronoun_outputs() -> None:
    rng = random.Random(3)
    value = Pronoun(is_singular=True, is_third_person=True).make_text(rng)
    assert value in {"he", "she", "it"}


def test_articles_and_determiners_apply_vowel_context() -> None:
    assert Article(is_before_vowel=True).make_text(ChoiceRandom("a")) == "an"
    assert Article().make_text(ChoiceRandom("a")) == "a"
    assert Determiner(is_before_vowel=True).make_text(ChoiceRandom("a")) == "an"


def test_chemical_compound_from_assets() -> None:
    rng = random.Random(4)
    value = ChemicalCompoundName().make_text(rng)
    assert_in_options(value, ChemicalCompoundName._options)


def test_authored_artifact_from_options() -> None:
    rng = random.Random(5)
    value = AuthoredArtifact().make_text(rng)
    assert_in_options(value, AuthoredArtifact._options)


def test_location_adjective_from_assets() -> None:
    rng = random.Random(6)
    value = LocationAdjective().make_text(rng)
    assert_in_options(value, LocationAdjective._options)


def test_martial_social_concept_from_assets() -> None:
    rng = random.Random(7)
    value = MartialSocialConcept().make_text(rng)
    assert_in_options(value, MartialSocialConcept._options)


def test_ship_name_vocab() -> None:
    rng = random.Random(8)
    assert_in_options(
        NauticalShipNameColor().make_text(rng),
        NauticalShipNameColor._options,
    )
    assert_in_options(
        NauticalShipNameObject().make_text(rng),
        NauticalShipNameObject._options,
    )
    assert_in_options(ShipNameAdjective().make_text(rng), ShipNameAdjective._options)


def test_time_of_day_from_assets() -> None:
    rng = random.Random(9)
    value = TimeOfDay().make_text(rng)
    assert_in_options(value, TimeOfDay._options)


def test_ucb_emotion_from_assets() -> None:
    rng = random.Random(10)
    value = UCBerkeleyEmotion().make_text(rng)
    assert_in_options(value, UCBerkeleyEmotion._options)


def test_villainous_person_pluralization_rules() -> None:
    assert (
        VillainousPersonNoun(is_plural=True).make_text(ChoiceRandom("lowlife"))
        == "lowlifes"
    )
    assert (
        VillainousPersonNoun(is_plural=True).make_text(ChoiceRandom("thief"))
        == "thieves"
    )
    assert (
        VillainousPersonNoun(is_plural=True).make_text(ChoiceRandom("bandit"))
        == "bandits"
    )


def test_primitive_weapon_pluralization_rules() -> None:
    assert PrimitiveWeapon(is_plural=True).make_text(ChoiceRandom("knife")) == "knives"
    assert PrimitiveWeapon(is_plural=True).make_text(ChoiceRandom("spear")) == "spears"


def test_public_word_boolean_options_require_booleans() -> None:
    invalid_components = (
        lambda: Pronoun(is_singular=1, is_third_person=False),
        lambda: Pronoun(is_singular=True, is_third_person="no"),
        lambda: Article(is_before_vowel=1),
        lambda: Determiner(is_before_vowel="yes"),
        lambda: VillainousPersonNoun(is_plural=1),
        lambda: PrimitiveWeapon(is_plural="yes"),
    )

    for make_component in invalid_components:
        with pytest.raises(TypeError, match="must be a boolean"):
            make_component()

    with pytest.raises(TypeError):
        Pronoun()  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        VillainousPersonNoun()  # type: ignore[call-arg]
