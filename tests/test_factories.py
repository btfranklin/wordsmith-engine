"""Tests for factories."""

from __future__ import annotations

import random

import pytest

from wordsmith.factories import ExoticCharacterFactory


def test_exotic_character_from_set() -> None:
    rng = random.Random(0)
    value = ExoticCharacterFactory.random_character_from_set("runic", rng)
    assert value in ExoticCharacterFactory._character_sets["runic"]


def test_exotic_character_any_set() -> None:
    rng = random.Random(1)
    value = ExoticCharacterFactory.random_character(rng)
    all_chars = {
        char for char_set in ExoticCharacterFactory._character_sets.values() for char in char_set
    }
    assert value in all_chars


def test_exotic_character_invalid_set() -> None:
    with pytest.raises(ValueError):
        ExoticCharacterFactory.random_character_from_set("invalid")
