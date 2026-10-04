"""Core component behavior tests."""

from __future__ import annotations

from pathlib import Path
import math
import random
import sys

import pytest

from wordsmith.core.components import (
    Literal,
    OneOf,
    Text,
    WeightedOneOf,
    either,
    maybe,
    one_of,
    text,
    weighted_one_of,
)
from wordsmith.util.strings import starts_with_vowel


class _CountingRandom(random.Random):
    def __init__(self) -> None:
        super().__init__(0)
        self.draw_count = 0

    def random(self) -> float:
        self.draw_count += 1
        return super().random()


def test_core_layer_does_not_depend_on_words() -> None:
    core_root = Path(__file__).resolve().parents[1] / "src" / "wordsmith" / "core"
    sources = "\n".join(
        path.read_text(encoding="utf-8") for path in core_root.glob("*.py")
    )
    assert "wordsmith.words" not in sources


def test_text_joining() -> None:
    component = text("alpha", "beta", "gamma", sep="-")
    assert component.make_text(random.Random(0)) == "alpha-beta-gamma"


def test_text_constructor_snapshots_list_parts() -> None:
    parts = [Literal("alpha"), Literal("beta")]
    component = Text(parts, sep="-")
    parts[0] = Literal("changed")
    parts.append(Literal("gamma"))

    assert component.parts == (Literal("alpha"), Literal("beta"))
    assert component.make_text(random.Random(0)) == "alpha-beta"
    assert Text(component.parts, sep="-").make_text(random.Random(0)) == "alpha-beta"


def test_one_of_constructor_snapshots_list_options() -> None:
    options = [Literal("alpha")]
    component = OneOf(options)
    options[0] = Literal("changed")
    options.clear()

    assert component.options == (Literal("alpha"),)
    assert component.make_text(random.Random(0)) == "alpha"
    assert OneOf(component.options).make_text(random.Random(0)) == "alpha"


def test_weighted_one_of_constructor_snapshots_options_and_weights() -> None:
    options = [Literal("zero"), Literal("positive")]
    weights = [0.0, 1.0]
    component = WeightedOneOf(options, weights)
    options[1] = Literal("changed")
    options.clear()
    weights[:] = [1.0, 0.0]

    assert component.options == (Literal("zero"), Literal("positive"))
    assert component.weights == (0.0, 1.0)
    rng = _CountingRandom()
    assert component.make_text(rng) == "positive"
    assert rng.draw_count == 1
    assert (
        WeightedOneOf(component.options, component.weights).make_text(random.Random(0))
        == "positive"
    )


def test_direct_constructors_preserve_collection_validation() -> None:
    assert Text([]).make_text(random.Random(0)) == ""
    with pytest.raises(ValueError, match="at least one option"):
        OneOf([])
    with pytest.raises(ValueError, match="at least one option"):
        WeightedOneOf([], [])
    with pytest.raises(ValueError, match="matching options and weights"):
        WeightedOneOf([Literal("alpha")], [])


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


def test_probability_extremes_each_consume_one_draw() -> None:
    for probability, expected in ((0.0, "second"), (1.0, "first")):
        rng = _CountingRandom()
        assert (
            either("first", "second", first_probability=probability).make_text(rng)
            == expected
        )
        assert rng.draw_count == 1

    for probability, expected in ((0.0, ""), (1.0, "hello")):
        rng = _CountingRandom()
        assert maybe("hello", probability=probability).make_text(rng) == expected
        assert rng.draw_count == 1


def test_probability_validation_messages_are_preserved() -> None:
    with pytest.raises(
        ValueError,
        match=r"^First option probability must be in the range 0\.0 to 1\.0\.$",
    ):
        either("first", "second", first_probability=-0.1)

    with pytest.raises(
        ValueError,
        match=r"^Probability must be in the range 0\.0 to 1\.0\.$",
    ):
        maybe("hello", probability=1.1)


def test_one_of_selection() -> None:
    rng = random.Random(3)
    assert one_of("alpha", "beta", "gamma").make_text(rng) in {"alpha", "beta", "gamma"}


def test_weighted_one_of_respects_zero_weight() -> None:
    rng = random.Random(4)
    component = weighted_one_of((1.0, "alpha"), (0.0, "beta"))
    assert component.make_text(rng) == "alpha"


@pytest.mark.parametrize("weight", [math.ulp(0.0), sys.float_info.min, 1.0])
def test_weighted_one_of_excludes_zero_weights_at_small_totals(weight: float) -> None:
    component = weighted_one_of((0.0, "zero"), (weight, "positive"), (0.0, "zero"))
    for fraction in (0.0, 0.75, math.nextafter(1.0, 0.0)):
        rng = _FractionRandom(fraction)
        assert component.make_text(rng) == "positive"
        assert rng.draw_count == 1


class _FractionRandom(random.Random):
    def __init__(self, fraction: float) -> None:
        super().__init__(0)
        self.fraction = fraction
        self.draw_count = 0

    def random(self) -> float:
        self.draw_count += 1
        return self.fraction


@pytest.mark.parametrize("scale", [math.ulp(0.0), sys.float_info.min / 4, 1.0])
def test_weighted_one_of_preserves_ratios_for_small_weights(scale: float) -> None:
    component = weighted_one_of((scale, "first"), (3 * scale, "second"), (0.0, "zero"))
    for fraction, expected in (
        (0.0, "first"),
        (math.nextafter(0.25, 0.0), "first"),
        (0.25, "second"),
        (math.nextafter(1.0, 0.0), "second"),
    ):
        rng = _FractionRandom(fraction)
        assert component.make_text(rng) == expected
        assert rng.draw_count == 1


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

    rng = random.Random(1)
    assert (
        text("unimportant detail").prefixed_by_article().make_text(rng)
        == "an unimportant detail"
    )


def test_prefixed_by_determiner_respects_vowel_sound() -> None:
    rng = random.Random(14)
    assert (
        text("onerous task").prefixed_by_determiner().make_text(rng)
        == "an onerous task"
    )


def test_title_case_small_words() -> None:
    assert (
        text("the", "voyage", "of", "the", "sunrise", "wrath", sep=" ")
        .title_case()
        .make_text(random.Random(0))
        == "The Voyage of the Sunrise Wrath"
    )


def test_operator_or_joins_with_space() -> None:
    component = Literal("alpha") | Literal("beta")
    assert component.make_text(random.Random(0)) == "alpha beta"


def test_operator_or_supports_strings() -> None:
    component = Literal("alpha") | "beta"
    assert component.make_text(random.Random(0)) == "alpha beta"

    component = "alpha" | Literal("beta")
    assert component.make_text(random.Random(0)) == "alpha beta"


def test_operator_add_joins_with_no_space() -> None:
    component = Literal("alpha") + Literal("beta")
    assert component.make_text(random.Random(0)) == "alphabeta"


def test_operator_add_supports_strings() -> None:
    component = Literal("alpha") + "beta"
    assert component.make_text(random.Random(0)) == "alphabeta"

    component = "alpha" + Literal("beta")
    assert component.make_text(random.Random(0)) == "alphabeta"


def test_operator_chain_mixes_space_and_no_space() -> None:
    component = Literal("alpha") | (Literal("beta") + Literal("gamma"))
    assert component.make_text(random.Random(0)) == "alpha betagamma"
