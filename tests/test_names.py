"""Tests for name generators."""

from __future__ import annotations

import random

import pytest

from wordsmith.names import (
    AncientName,
    BinaryGender,
    GivenName,
    PersonName,
    Surname,
    WeirdName,
)


def test_given_name_gendered() -> None:
    rng = random.Random(0)
    value = GivenName(gender=BinaryGender.MALE).make_text(rng)
    assert value in GivenName._male_options

    rng = random.Random(0)
    value = GivenName(gender=BinaryGender.FEMALE).make_text(rng)
    assert value in GivenName._female_options


def test_surname_from_assets() -> None:
    rng = random.Random(1)
    value = Surname().make_text(rng)
    assert value in Surname._options


def test_person_name_components() -> None:
    rng = random.Random(2)
    name = PersonName(gender=BinaryGender.MALE).make_text(rng)
    parts = name.split(" ")
    assert parts[0] in GivenName._male_options
    assert parts[-1] in Surname._options


def test_weird_name_format() -> None:
    rng = random.Random(3)
    value = WeirdName(syllable_count=3).make_text(rng)
    assert any(char.isupper() for char in value)


def test_ancient_name_format() -> None:
    rng = random.Random(4)
    value = AncientName(syllable_count=4).make_text(rng)
    assert any(char.isupper() for char in value)


def test_weird_name_requires_positive_syllables() -> None:
    with pytest.raises(ValueError):
        WeirdName(syllable_count=0)


def test_ancient_name_requires_positive_syllables() -> None:
    with pytest.raises(ValueError):
        AncientName(syllable_count=0)
