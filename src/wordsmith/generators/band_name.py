"""Band name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import one_of
from wordsmith.names.given_name import GivenName
from wordsmith.words.base import Adjective, Noun


@dataclass(frozen=True)
class BandName(Component):
    """Generate a band name."""

    def make_text(self, rng: random.Random) -> str:
        return (
            one_of(
                "The" | Adjective(),
                "The" | Noun(),
                "The" | Noun(is_plural=True),
                Adjective() | Noun(),
                "The" | Adjective() | Noun(is_plural=True),
                GivenName() | "and the" | Noun(is_plural=True),
                GivenName().possessive_form() | Noun(is_plural=True),
            )
            .title_case()
            .make_text(rng)
        )
