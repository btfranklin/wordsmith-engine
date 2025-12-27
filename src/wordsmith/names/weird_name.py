"""Procedural weird name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import ClassVar

from wordsmith.core.base import Component
from wordsmith.util import first_upper


@dataclass(frozen=True)
class WeirdName(Component):
    """Generate a synthetic name from syllable fragments."""

    syllable_count: int
    allow_hyphen: bool = True
    allow_apostrophe: bool = True

    _open_ended_syllables: ClassVar[list[str]] = [
        "a",
        "ba",
        "be",
        "bi",
        "bo",
        "bu",
        "by",
        "ca",
        "cha",
        "che",
        "chi",
        "co",
        "cho",
        "chu",
        "chy",
        "da",
        "de",
        "di",
        "do",
        "du",
        "dy",
        "e",
        "fa",
        "fe",
        "fi",
        "fo",
        "fu",
        "fy",
        "ga",
        "ge",
        "gi",
        "go",
        "gu",
        "gy",
        "ha",
        "he",
        "hi",
        "ho",
        "hu",
        "hy",
        "i",
        "ja",
        "je",
        "ji",
        "jo",
        "ju",
        "jy",
        "ka",
        "ke",
        "ki",
        "ko",
        "ku",
        "ky",
        "la",
        "le",
        "li",
        "lo",
        "lu",
        "ly",
        "ma",
        "me",
        "mi",
        "mo",
        "mu",
        "my",
        "na",
        "ne",
        "ni",
        "no",
        "nu",
        "ny",
        "o",
        "pa",
        "pe",
        "pi",
        "po",
        "pu",
        "py",
        "qua",
        "que",
        "ra",
        "re",
        "ri",
        "ro",
        "ru",
        "ry",
        "sa",
        "se",
        "si",
        "so",
        "su",
        "ta",
        "te",
        "ti",
        "to",
        "tu",
        "ty",
        "u",
        "va",
        "ve",
        "vi",
        "vo",
        "vu",
        "vy",
        "wa",
        "we",
        "wi",
        "wo",
        "wu",
        "wy",
        "xa",
        "xe",
        "xi",
        "xo",
        "xu",
        "ya",
        "ye",
        "yi",
        "yo",
        "yu",
        "za",
        "ze",
        "zi",
        "zo",
        "zu",
    ]
    _ending_sounds: ClassVar[list[str]] = [
        "bb",
        "c",
        "ck",
        "ch",
        "d",
        "dd",
        "l",
        "ll",
        "m",
        "mm",
        "n",
        "nn",
        "p",
        "pp",
        "r",
        "rr",
        "s",
        "ss",
        "t",
        "tt",
        "w",
        "x",
    ]

    def __post_init__(self) -> None:
        if self.syllable_count < 1:
            raise ValueError("Syllable count must be greater than 0")

    def make_text(self, rng: random.Random) -> str:
        will_use_hyphen = (
            self.syllable_count > 2
            and self.allow_hyphen
            and rng.choice([True, False])
        )
        will_use_apostrophe = (
            self.syllable_count > 2
            and self.allow_apostrophe
            and rng.choice([True, False])
        )

        hyphen_syllable = rng.randrange(1, self.syllable_count) if will_use_hyphen else 0
        apostrophe_syllable = rng.randrange(1, self.syllable_count) if will_use_apostrophe else 0

        text = ""
        for current_syllable in range(1, self.syllable_count + 1):
            text += rng.choice(self._open_ended_syllables)

            if current_syllable == apostrophe_syllable:
                text += "'"
            elif current_syllable == hyphen_syllable:
                text += "-"

        if rng.choice([True, False]):
            text += rng.choice(self._ending_sounds)

        return first_upper(text)
