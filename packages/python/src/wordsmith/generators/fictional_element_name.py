"""Fictional element name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import ClassVar

from wordsmith.core.base import Component
from wordsmith.core.components import weighted_one_of
from wordsmith.generators._material_roots import (
    MATERIAL_NAME_PARTS,
    element_root_source,
    make_material_root,
)


@dataclass(frozen=True)
class FictionalElementName(Component):
    """Generate a fictional element name."""

    _real_element_names: ClassVar[set[str]] = set(
        MATERIAL_NAME_PARTS["realElements"]
    )

    def make_text(self, rng: random.Random) -> str:
        for _ in range(16):
            root = make_material_root(rng, element_root_source(), "lumin")
            text = _join_element_suffix(root, _element_suffix().make_text(rng))
            if text not in self._real_element_names:
                return text
        return "luminum"


def _element_suffix() -> Component:
    return weighted_one_of(
        *(
            (weight, suffix)
            for weight, suffix in MATERIAL_NAME_PARTS["elementSuffixes"]
        )
    )


def _join_element_suffix(root: str, suffix: str) -> str:
    if suffix == "ium":
        if root.endswith("on"):
            root = root[:-2]
        while len(root) > 2 and root.endswith(("a", "e", "i", "y")):
            root = root[:-1]
        return root + suffix

    if suffix == "gen":
        return root + ("gen" if root[-1] in "aeiou" else "ogen")

    if root.endswith("e"):
        root = root[:-1]
    if root.endswith(suffix):
        return root
    return root + suffix
