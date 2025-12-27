"""Core component behavior tests."""

from __future__ import annotations

import random

from wordsmith.core.components import either, maybe, one_of, text
from wordsmith.util.strings import starts_with_vowel


def test_text_joining() -> None:
    component = text("alpha", "beta", "gamma", sep="-")
    assert component.make_text(random.Random(0)) == "alpha-beta-gamma"


def test_either_probability_extremes() -> None:
    rng = random.Random(0)
    assert either("first", "second", first_probability=1.0).make_text(rng) == "first"

    rng = random.Random(0)
    assert either("first", "second", first_probability=0.0).make_text(rng) == "second"


def test_maybe_probability_extremes() -> None:
    rng = random.Random(0)
    assert maybe("hello", probability=1.0).make_text(rng) == "hello"

    rng = random.Random(0)
    assert maybe("hello", probability=0.0).make_text(rng) == ""


def test_one_of_selection() -> None:
    rng = random.Random(3)
    assert one_of("alpha", "beta", "gamma").make_text(rng) in {"alpha", "beta", "gamma"}


def test_starts_with_vowel_heuristics() -> None:
    assert starts_with_vowel("hour") is True
    assert starts_with_vowel("honor") is True
    assert starts_with_vowel("user") is False
    assert starts_with_vowel("one") is False


def test_prefixed_by_article_respects_vowel_sound() -> None:
    rng = random.Random(1)
    assert text("hour").prefixed_by_article().make_text(rng) == "an hour"

    rng = random.Random(1)
    assert text("user").prefixed_by_article().make_text(rng) == "a user"


def test_title_case_small_words() -> None:
    assert (
        text("the", "voyage", "of", "the", "sunrise", "wrath", sep=" ")
        .title_case()
        .make_text(random.Random(0))
        == "The Voyage of the Sunrise Wrath"
    )
