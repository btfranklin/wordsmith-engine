"""Root helpers for fictional material generators."""

from __future__ import annotations

from dataclasses import dataclass
import random
import re
from typing import ClassVar
import unicodedata

from wordsmith.core.base import Component
from wordsmith.core.components import weighted_one_of
from wordsmith.names.alien_name import AlienName
from wordsmith.names.fantasy_name import FantasyName
from wordsmith.names.surname import Surname
from wordsmith.util.resources import load_json


_CONSONANT_RUN = re.compile(r"[bcdfghjklmnpqrstvwxz]{5,}")
_NON_LETTERS = re.compile(r"[^a-z]")
MATERIAL_NAME_PARTS = load_json("Material Name Parts.json")


def clean_material_root(value: str) -> str | None:
    """Convert a generated source word into a compact material root."""
    ascii_text = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )
    root = _NON_LETTERS.sub("", ascii_text)
    if not 3 <= len(root) <= 10:
        return None
    if not any(vowel in root for vowel in "aeiou"):
        return None
    if "ii" in root or "yy" in root:
        return None
    if _CONSONANT_RUN.search(root):
        return None
    return root


def make_material_root(
    rng: random.Random,
    component: Component,
    fallback: str,
) -> str:
    """Choose a source component and return a usable material root."""
    for _ in range(24):
        root = clean_material_root(component.make_text(rng))
        if root is not None:
            return root
    return fallback


@dataclass(frozen=True)
class ElementalRoot(Component):
    """Generate a short root that reads like a fictional element source."""

    _prefixes: ClassVar[list[str]] = MATERIAL_NAME_PARTS["elementPrefixes"]
    _middles: ClassVar[list[str]] = MATERIAL_NAME_PARTS["elementMiddles"]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._prefixes) + rng.choice(self._middles)


@dataclass(frozen=True)
class MineralRoot(Component):
    """Generate a short root that reads like a fictional mineral source."""

    _prefixes: ClassVar[list[str]] = MATERIAL_NAME_PARTS["mineralPrefixes"]
    _middles: ClassVar[list[str]] = MATERIAL_NAME_PARTS["mineralMiddles"]

    def make_text(self, rng: random.Random) -> str:
        return rng.choice(self._prefixes) + rng.choice(self._middles)


def element_root_source() -> Component:
    """Root source weighted for element-like names."""
    return weighted_one_of(
        (5, ElementalRoot()),
        (1, AlienName(syllable_count=2, allow_hyphen=False, allow_apostrophe=False)),
        (1, FantasyName(syllable_count=2, allow_hyphen=False, allow_apostrophe=False)),
        (1, Surname()),
    )


def mineral_root_source() -> Component:
    """Root source weighted for mineral-like names."""
    return weighted_one_of(
        (4, MineralRoot()),
        (2, FantasyName(syllable_count=2, allow_hyphen=False, allow_apostrophe=False)),
        (1, Surname()),
    )
