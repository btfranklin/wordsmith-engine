"""Tests for name generators."""

from __future__ import annotations

import random

import pytest

from wordsmith.names import (
    AlienName,
    AncientGivenName,
    BinaryGender,
    FantasyName,
    GivenName,
    GivenNameCulture,
    PersonName,
    Surname,
)


def test_given_name_gendered() -> None:
    rng = random.Random(0)
    value = GivenName(
        gender=BinaryGender.MALE,
        culture=GivenNameCulture.ENGLISH_SPEAKING,
    ).make_text(rng)
    assert value in GivenName._options["english_speaking"]["male"]

    rng = random.Random(0)
    value = GivenName(
        gender=BinaryGender.FEMALE,
        culture=GivenNameCulture.ENGLISH_SPEAKING,
    ).make_text(rng)
    assert value in GivenName._options["english_speaking"]["female"]


def test_given_name_culture_groups() -> None:
    rng = random.Random(1)
    value = GivenName(
        gender=BinaryGender.FEMALE,
        culture=GivenNameCulture.LATIN_AMERICAN,
    ).make_text(rng)
    assert value in GivenName._options["latin_american"]["female"]

    value = GivenName(
        gender=BinaryGender.MALE,
        culture=GivenNameCulture.EASTERN,
    ).make_text(rng)
    assert value in GivenName._options["eastern"]["male"]


def test_curated_unisex_names_are_in_both_gender_lists() -> None:
    english_names = GivenName._options["english_speaking"]
    assert "Vesper" in english_names["male"]
    assert "Vesper" in english_names["female"]


def test_surname_from_assets() -> None:
    rng = random.Random(1)
    value = Surname().make_text(rng)
    assert value in Surname._options


def test_person_name_components() -> None:
    rng = random.Random(2)
    name = PersonName(gender=BinaryGender.MALE).make_text(rng)
    parts = name.split(" ")
    assert any(parts[0] in group["male"] for group in GivenName._options.values())
    assert parts[-1] in Surname._options


def test_person_name_passes_culture_to_given_name() -> None:
    rng = random.Random(2)
    name = PersonName(
        gender=BinaryGender.MALE,
        culture=GivenNameCulture.ENGLISH_SPEAKING,
    ).make_text(rng)
    parts = name.split(" ")
    assert parts[0] in GivenName._options["english_speaking"]["male"]
    assert parts[-1] in Surname._options


def test_ancient_given_name_gendered() -> None:
    rng = random.Random(3)
    value = AncientGivenName(gender=BinaryGender.MALE).make_text(rng)
    assert value in AncientGivenName._options["male"]

    rng = random.Random(3)
    value = AncientGivenName(gender=BinaryGender.FEMALE).make_text(rng)
    assert value in AncientGivenName._options["female"]


def test_alien_name_format() -> None:
    rng = random.Random(3)
    value = AlienName(syllable_count=3).make_text(rng)
    assert any(char.isupper() for char in value)


def test_fantasy_name_format() -> None:
    rng = random.Random(4)
    value = FantasyName(syllable_count=4).make_text(rng)
    assert any(char.isupper() for char in value)


def test_fantasy_name_has_classical_endings() -> None:
    values = {
        FantasyName(syllable_count=4).make_text(random.Random(seed)).lower()
        for seed in range(25)
    }
    assert any(
        value.endswith(("a", "an", "as", "el", "en", "ia", "ion", "is", "os", "us"))
        for value in values
    )


def test_alien_name_requires_positive_syllables() -> None:
    with pytest.raises(ValueError):
        AlienName(syllable_count=0)


def test_fantasy_name_requires_positive_syllables() -> None:
    with pytest.raises(ValueError):
        FantasyName(syllable_count=0)
