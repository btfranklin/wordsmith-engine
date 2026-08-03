"""Band name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import one_of
from wordsmith.names.given_name import GivenName
from wordsmith.names.given_name_culture import GivenNameCulture
from wordsmith.words.base import Adjective, Noun, NounForm


@dataclass(frozen=True)
class BandName(Component):
    """Generate a band name."""

    def make_text(self, rng: random.Random) -> str:
        return (
            one_of(
                "The" | Adjective(),
                "The" | Noun(),
                "The" | Noun(form=NounForm.PLURAL),
                Adjective() | Noun(),
                "The" | Adjective() | Noun(form=NounForm.PLURAL),
                GivenName(culture=GivenNameCulture.ENGLISH_SPEAKING)
                | "and the"
                | Noun(form=NounForm.PLURAL),
                GivenName(culture=GivenNameCulture.ENGLISH_SPEAKING).possessive_form()
                | Noun(form=NounForm.PLURAL),
            )
            .title_case()
            .make_text(rng)
        )
