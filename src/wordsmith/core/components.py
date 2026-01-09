"""Core components and combinators for the Wordsmith DSL."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Iterable

from wordsmith.core.base import Component
from wordsmith.util.strings import first_upper, starts_with_vowel, title_case
from wordsmith.words.articles import Article, Determiner

ComponentLike = Component | str


def _coerce_component(value: ComponentLike) -> Component:
    if isinstance(value, Component):
        return value
    if isinstance(value, str):
        return Literal(value)
    raise TypeError(f"Unsupported component type: {type(value)!r}")


def _normalize_components(values: Iterable[ComponentLike]) -> tuple[Component, ...]:
    return tuple(_coerce_component(value) for value in values)


def _roll_probability(rng: random.Random, probability: float) -> bool:
    if not 0.0 <= probability <= 1.0:
        raise ValueError("Probability must be in the range 0.0 to 1.0.")
    return rng.random() < probability


@dataclass(frozen=True)
class Literal(Component):
    """A fixed string component."""

    text: str

    def make_text(self, rng: random.Random) -> str:
        return self.text


@dataclass(frozen=True)
class Empty(Component):
    """A component that renders as an empty string."""

    def make_text(self, rng: random.Random) -> str:
        return ""


@dataclass(frozen=True)
class Text(Component):
    """Join multiple components into a single text value."""

    parts: tuple[Component, ...]
    sep: str = ""

    def make_text(self, rng: random.Random) -> str:
        rendered_parts = []
        for part in self.parts:
            rendered = part.make_text(rng)
            if rendered == "":
                continue
            rendered_parts.append(rendered)
        return self.sep.join(rendered_parts)


@dataclass(frozen=True)
class OneOf(Component):
    """Choose one of the provided components at random."""

    options: tuple[Component, ...]

    def __post_init__(self) -> None:
        if not self.options:
            raise ValueError("OneOf requires at least one option.")

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self.options).make_text(rng)


@dataclass(frozen=True)
class WeightedOneOf(Component):
    """Choose one of the provided components using weighted probabilities."""

    options: tuple[Component, ...]
    weights: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.options:
            raise ValueError("WeightedOneOf requires at least one option.")
        if len(self.options) != len(self.weights):
            raise ValueError("WeightedOneOf requires matching options and weights.")
        if any(weight < 0.0 for weight in self.weights):
            raise ValueError("WeightedOneOf requires non-negative weights.")
        if not any(weight > 0.0 for weight in self.weights):
            raise ValueError("WeightedOneOf requires at least one positive weight.")

    def make_text(self, rng: random.Random) -> str:
        choice = rng.choices(self.options, weights=self.weights, k=1)[0]
        return choice.make_text(rng)


@dataclass(frozen=True)
class Either(Component):
    """Choose between two options based on the provided probability."""

    first: Component
    second: Component
    first_probability: float = 0.5

    def __post_init__(self) -> None:
        if not 0.0 <= self.first_probability <= 1.0:
            raise ValueError(
                "First option probability must be in the range 0.0 to 1.0."
            )

    def make_text(self, rng: random.Random) -> str:
        choice = (
            self.first
            if _roll_probability(rng, self.first_probability)
            else self.second
        )
        return choice.make_text(rng)


@dataclass(frozen=True)
class Maybe(Component):
    """Conditionally render a component based on a probability."""

    option: Component
    probability: float = 0.5

    def __post_init__(self) -> None:
        if not 0.0 <= self.probability <= 1.0:
            raise ValueError("Probability must be in the range 0.0 to 1.0.")

    def make_text(self, rng: random.Random) -> str:
        return (
            self.option.make_text(rng)
            if _roll_probability(rng, self.probability)
            else ""
        )


@dataclass(frozen=True)
class Capitalized(Component):
    """Capitalize each word of the wrapped component."""

    wrapped: Component

    def make_text(self, rng: random.Random) -> str:
        return self.wrapped.make_text(rng).title()


@dataclass(frozen=True)
class FirstUppercased(Component):
    """Uppercase the first alphabetic character of the wrapped component."""

    wrapped: Component

    def make_text(self, rng: random.Random) -> str:
        return first_upper(self.wrapped.make_text(rng))


@dataclass(frozen=True)
class TitleCased(Component):
    """Apply title casing to the wrapped component."""

    wrapped: Component

    def make_text(self, rng: random.Random) -> str:
        return title_case(self.wrapped.make_text(rng))


@dataclass(frozen=True)
class PrefixedByArticle(Component):
    """Prefix the wrapped component with an article."""

    wrapped: Component

    def make_text(self, rng: random.Random) -> str:
        text = self.wrapped.make_text(rng)
        article = Article(is_before_vowel=starts_with_vowel(text)).make_text(rng)
        return f"{article} {text}"


@dataclass(frozen=True)
class PrefixedByDeterminer(Component):
    """Prefix the wrapped component with a determiner."""

    wrapped: Component

    def make_text(self, rng: random.Random) -> str:
        text = self.wrapped.make_text(rng)
        determiner = Determiner(is_before_vowel=starts_with_vowel(text)).make_text(rng)
        return f"{determiner} {text}"


@dataclass(frozen=True)
class PossessiveForm(Component):
    """Render the wrapped component in the possessive form."""

    wrapped: Component

    def make_text(self, rng: random.Random) -> str:
        text = self.wrapped.make_text(rng)
        if text.endswith("s"):
            return f"{text}'"
        return f"{text}'s"


def text(*parts: ComponentLike, sep: str = "") -> Text:
    """Build a Text component from parts."""
    return Text(parts=_normalize_components(parts), sep=sep)


def one_of(*options: ComponentLike) -> OneOf:
    """Build a OneOf component from options."""
    return OneOf(options=_normalize_components(options))


def weighted_one_of(*pairs: tuple[float, ComponentLike]) -> WeightedOneOf:
    """Build a WeightedOneOf component from weighted pairs."""
    if not pairs:
        raise ValueError("WeightedOneOf requires at least one option.")
    weights, options = zip(*pairs)
    return WeightedOneOf(
        options=_normalize_components(options),
        weights=tuple(float(weight) for weight in weights),
    )


def either(
    first: ComponentLike,
    second: ComponentLike,
    first_probability: float = 0.5,
) -> Either:
    """Build an Either component from two options."""
    return Either(
        first=_coerce_component(first),
        second=_coerce_component(second),
        first_probability=first_probability,
    )


def maybe(*parts: ComponentLike, probability: float = 0.5) -> Maybe:
    """Build a Maybe component from one or more parts."""
    return Maybe(option=text(*parts), probability=probability)
