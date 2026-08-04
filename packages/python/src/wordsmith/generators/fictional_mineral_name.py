"""Fictional mineral name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wordsmith.core.base import Component
from wordsmith.core.components import weighted_one_of
from wordsmith.generators._material_roots import (
    MATERIAL_NAME_PARTS,
    make_material_root,
    mineral_root_source,
)


@dataclass(frozen=True)
class FictionalMineralName(Component):
    """Generate a fictional mineral name."""

    def make_text(self, rng: random.Random) -> str:
        root = make_material_root(rng, mineral_root_source(), "aurel")
        return _join_mineral_suffix(root, _mineral_suffix().make_text(rng))


def _mineral_suffix() -> Component:
    return weighted_one_of(
        *(
            (weight, suffix)
            for weight, suffix in MATERIAL_NAME_PARTS["mineralSuffixes"]
        )
    )


def _join_mineral_suffix(root: str, suffix: str) -> str:
    if suffix in {"ite", "ine"} and root.endswith(("e", "i", "y")):
        root = root[:-1]

    if root.endswith(suffix):
        return root
    if root[-1] == suffix[0]:
        suffix = suffix[1:]
    return root + suffix
