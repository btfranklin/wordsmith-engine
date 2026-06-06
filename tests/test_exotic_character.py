"""Tests for exotic characters."""

from __future__ import annotations

import random

import pytest

from wordsmith.specials import ExoticCharacter


def test_exotic_character_from_set() -> None:
    rng = random.Random(0)
    value = ExoticCharacter.random_character_from_set("runic", rng)
    assert value in ExoticCharacter._character_sets["runic"]


def test_exotic_character_from_glagolitic_set() -> None:
    rng = random.Random(0)
    value = ExoticCharacter.random_character_from_set("glagolitic", rng)
    assert value in ExoticCharacter._character_sets["glagolitic"]


def test_exotic_character_any_set() -> None:
    rng = random.Random(1)
    value = ExoticCharacter.random_character(rng)
    all_chars = {
        char
        for char_set in ExoticCharacter._character_sets.values()
        for char in char_set
    }
    assert value in all_chars


def test_exotic_character_invalid_set() -> None:
    with pytest.raises(ValueError):
        ExoticCharacter.random_character_from_set("invalid")


def test_exotic_character_sets_contain_single_characters() -> None:
    for character_set in ExoticCharacter._character_sets.values():
        assert all(len(character) == 1 for character in character_set)


def test_cuneiform_set_includes_later_main_block_additions() -> None:
    cuneiform_set = ExoticCharacter._character_sets["cuneiform"]

    assert all(chr(codepoint) in cuneiform_set for codepoint in range(0x1236F, 0x1239A))


def test_cuneiform_set_keeps_visually_boring_shar2_omitted() -> None:
    assert "\U000122b9" not in ExoticCharacter._character_sets["cuneiform"]
