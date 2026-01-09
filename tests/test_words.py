"""Tests for base word generators."""

from __future__ import annotations

import random
from typing import Sequence

from tests.utils import assert_in_options
from wordsmith.words import (
    Adjective,
    Adverb,
    ChemicalCompoundName,
    LocationAdjective,
    MartialSocialConcept,
    NauticalShipNameColor,
    NauticalShipNameObject,
    Noun,
    PrimitiveWeapon,
    Pronoun,
    ShipNameAdjective,
    TimeOfDay,
    UCBerkeleyEmotion,
    Verb,
    VerbTense,
    VillainousPersonNoun,
)


class ChoiceRandom:
    """Deterministic RNG that always returns a chosen value."""

    def __init__(self, value: str) -> None:
        self._value = value

    def choice(self, options: Sequence[str]) -> str:
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
    assert Noun(is_plural=True).make_text(ChoiceRandom("city")) == "cities"
    assert Noun(is_plural=True).make_text(ChoiceRandom("box")) == "boxes"
    assert Noun(is_plural=True).make_text(ChoiceRandom("knife")) == "knives"
    assert Noun(is_plural=True).make_text(ChoiceRandom("human")) == "humans"
    assert Noun(is_plural=True).make_text(ChoiceRandom("fireman")) == "firemen"


def test_verb_tense_selection() -> None:
    rng = random.Random(2)
    value = Verb(tense=VerbTense.PRESENT).make_text(rng)
    assert any(row[VerbTense.PRESENT.value] == value for row in Verb._options)


def test_pronoun_outputs() -> None:
    rng = random.Random(3)
    value = Pronoun(is_singular=True, is_third_person=True).make_text(rng)
    assert value in {"he", "she", "it"}


def test_chemical_compound_from_assets() -> None:
    rng = random.Random(4)
    value = ChemicalCompoundName().make_text(rng)
    assert_in_options(value, ChemicalCompoundName._options)


def test_location_adjective_from_assets() -> None:
    rng = random.Random(5)
    value = LocationAdjective().make_text(rng)
    assert_in_options(value, LocationAdjective._options)


def test_martial_social_concept_from_assets() -> None:
    rng = random.Random(6)
    value = MartialSocialConcept().make_text(rng)
    assert_in_options(value, MartialSocialConcept._options)


def test_ship_name_vocab() -> None:
    rng = random.Random(7)
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
    rng = random.Random(8)
    value = TimeOfDay().make_text(rng)
    assert_in_options(value, TimeOfDay._options)


def test_ucb_emotion_from_assets() -> None:
    rng = random.Random(9)
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
