"""Fictional mineral name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import one_of
from wordsmith.names.given_name import GivenName
from wordsmith.names.weird_name import WeirdName


@dataclass(frozen=True)
class FictionalMineralName(Component):
    """Generate a fictional mineral name."""

    def make_text(self, rng: random.Random) -> str:
        root_word = (
            one_of(
                GivenName(),
                WeirdName(syllable_count=2, allow_hyphen=False, allow_apostrophe=False),
            )
            .make_text(rng)
            .lower()
        )

        last_letter = root_word[-1]
        suffix = rng.choice(["ite", "alt", "um"])

        if last_letter in {"a", "o", "u"}:
            joining_letter = rng.choice(["b", "m", "n"])
            text = f"{root_word}{joining_letter}{suffix}"
        elif last_letter in {"e", "y", "i"}:
            text = f"{root_word[:-1]}{suffix}"
        else:
            text = f"{root_word}{suffix}"

        return text
