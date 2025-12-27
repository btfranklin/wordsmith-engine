"""Base types for the Wordsmith DSL."""

from __future__ import annotations

import abc
import random


class Component(abc.ABC):
    """Base class for all text-generating components."""

    @abc.abstractmethod
    def make_text(self, rng: random.Random) -> str:
        """Render text using the provided random number generator."""

    def __call__(self, rng: random.Random | None = None) -> str:
        """Render text, using a system RNG when none is provided."""
        if rng is None:
            rng = random.SystemRandom()
        return self.make_text(rng)

    def capitalized(self) -> Component:
        """Return a component that capitalizes each word of this component."""
        from .components import Capitalized

        return Capitalized(self)

    def first_upper(self) -> Component:
        """Return a component that uppercases the first alphabetic character."""
        from .components import FirstUppercased

        return FirstUppercased(self)

    def title_case(self) -> Component:
        """Return a component that applies title casing to this component."""
        from .components import TitleCased

        return TitleCased(self)

    def prefixed_by_article(self) -> Component:
        """Return a component prefixed by an appropriate article."""
        from .components import PrefixedByArticle

        return PrefixedByArticle(self)

    def prefixed_by_determiner(self) -> Component:
        """Return a component prefixed by a suitable determiner."""
        from .components import PrefixedByDeterminer

        return PrefixedByDeterminer(self)

    def possessive_form(self) -> Component:
        """Return a component rendered in the possessive form."""
        from .components import PossessiveForm

        return PossessiveForm(self)
