"""Composite generators for Wordsmith."""

from .band_name import BandName
from .criminal_gang_name import CriminalGangName
from .fictional_element_name import FictionalElementName
from .fictional_mineral_name import FictionalMineralName
from .nautical_ship_name import NauticalShipName
from .town_name import TownName
from .literary_title import LiteraryTitle, SimpleLiteraryTitle, UnusualLiteraryTitle

__all__ = [
    "BandName",
    "CriminalGangName",
    "FictionalElementName",
    "FictionalMineralName",
    "NauticalShipName",
    "LiteraryTitle",
    "SimpleLiteraryTitle",
    "TownName",
    "UnusualLiteraryTitle",
]
