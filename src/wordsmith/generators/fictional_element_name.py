"""Fictional element name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import one_of
from wordsmith.names.given_name import GivenName
from wordsmith.names.surname import Surname
from wordsmith.names.weird_name import WeirdName
from wordsmith.util import random_bool


@dataclass(frozen=True)
class FictionalElementName(Component):
    """Generate a fictional element name."""

    def make_text(self, rng: random.Random) -> str:
        root_word = (
            one_of(
                GivenName(),
                Surname(),
                WeirdName(syllable_count=2, allow_hyphen=False, allow_apostrophe=False),
                WeirdName(syllable_count=3, allow_hyphen=False, allow_apostrophe=False),
            )
            .make_text(rng)
            .lower()
        )

        last_letter = root_word[-1]

        if last_letter in {"a", "o", "u"}:
            text = f"{root_word}{'gen' if random_bool(rng) else 'n'}"
        elif last_letter == "e":
            text = f"{root_word[:-1]}ium" if random_bool(rng) else f"{root_word}on"
        elif last_letter in {"h", "v", "x"}:
            text = (
                f"{root_word[:-1]}ion"
                if random_bool(rng)
                else f"{root_word}{rng.choice(['ium', 'ine'])}"
            )
        elif last_letter in {"k", "m", "n"}:
            text = f"{root_word}{rng.choice(['ium', 'ine', 'ion'])}"
        elif last_letter in {"y", "i"}:
            text = f"{root_word}gen" if random_bool(rng) else f"{root_word[:-1]}ium"
        else:
            text = f"{root_word}{rng.choice(['ium', 'ine', 'on'])}"

        return text
