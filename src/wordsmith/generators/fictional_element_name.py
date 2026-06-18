"""Fictional element name generator."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import ClassVar

from wordsmith.core.base import Component
from wordsmith.core.components import weighted_one_of
from wordsmith.generators._material_roots import (
    element_root_source,
    make_material_root,
)


@dataclass(frozen=True)
class FictionalElementName(Component):
    """Generate a fictional element name."""

    _real_element_names: ClassVar[set[str]] = {
        "actinium",
        "aluminium",
        "americium",
        "antimony",
        "argon",
        "arsenic",
        "astatine",
        "barium",
        "berkelium",
        "beryllium",
        "bismuth",
        "bohrium",
        "boron",
        "bromine",
        "cadmium",
        "caesium",
        "calcium",
        "californium",
        "carbon",
        "cerium",
        "chlorine",
        "chromium",
        "cobalt",
        "copernicium",
        "copper",
        "curium",
        "darmstadtium",
        "dubnium",
        "dysprosium",
        "einsteinium",
        "erbium",
        "europium",
        "fermium",
        "flerovium",
        "fluorine",
        "francium",
        "gadolinium",
        "gallium",
        "germanium",
        "gold",
        "hafnium",
        "hassium",
        "helium",
        "holmium",
        "hydrogen",
        "indium",
        "iodine",
        "iridium",
        "iron",
        "krypton",
        "lanthanum",
        "lawrencium",
        "lead",
        "lithium",
        "livermorium",
        "lutetium",
        "magnesium",
        "manganese",
        "meitnerium",
        "mendelevium",
        "mercury",
        "molybdenum",
        "moscovium",
        "neodymium",
        "neon",
        "neptunium",
        "nickel",
        "nihonium",
        "niobium",
        "nitrogen",
        "nobelium",
        "oganesson",
        "osmium",
        "oxygen",
        "palladium",
        "phosphorus",
        "platinum",
        "plutonium",
        "polonium",
        "potassium",
        "praseodymium",
        "promethium",
        "protactinium",
        "radium",
        "radon",
        "rhenium",
        "rhodium",
        "roentgenium",
        "rubidium",
        "ruthenium",
        "rutherfordium",
        "samarium",
        "scandium",
        "seaborgium",
        "selenium",
        "silicon",
        "silver",
        "sodium",
        "strontium",
        "sulfur",
        "tantalum",
        "technetium",
        "tellurium",
        "tennessine",
        "terbium",
        "thallium",
        "thorium",
        "thulium",
        "tin",
        "titanium",
        "tungsten",
        "uranium",
        "vanadium",
        "xenon",
        "ytterbium",
        "yttrium",
        "zinc",
        "zirconium",
    }

    def make_text(self, rng: random.Random) -> str:
        for _ in range(16):
            root = make_material_root(rng, element_root_source(), "lumin")
            text = _join_element_suffix(root, _element_suffix().make_text(rng))
            if text not in self._real_element_names:
                return text
        return "luminum"


def _element_suffix() -> Component:
    return weighted_one_of(
        (4, "ium"),
        (2, "on"),
        (1, "ine"),
        (1, "ene"),
        (1, "gen"),
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
