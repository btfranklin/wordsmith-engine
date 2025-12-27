"""Band name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import one_of, text
from wordsmith.names.given_name import GivenName
from wordsmith.words.base import Adjective, Noun


@dataclass(frozen=True)
class BandName(Component):
    """Generate a band name."""

    def make_text(self, rng: random.Random) -> str:
        return (
            one_of(
                text("The", Adjective(), sep=" "),
                text("The", Noun(), sep=" "),
                text("The", Noun(is_plural=True), sep=" "),
                text(Adjective(), Noun(), sep=" "),
                text("The", Adjective(), Noun(is_plural=True), sep=" "),
                text(GivenName(), "and the", Noun(is_plural=True), sep=" "),
                text(GivenName().possessive_form(), Noun(is_plural=True), sep=" "),
            )
            .title_case()
            .make_text(rng)
        )
