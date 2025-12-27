"""Composite generators for Wordsmith."""

from .band_name import BandName
from .criminal_gang_name import CriminalGangName
from .fictional_element_name import FictionalElementName
from .fictional_mineral_name import FictionalMineralName
from .nautical_ship_name import NauticalShipName
from .town_name import TownName
from .work_title import SimpleWorkTitle, UnusualWorkTitle, WorkTitle

__all__ = [
    "BandName",
    "CriminalGangName",
    "FictionalElementName",
    "FictionalMineralName",
    "NauticalShipName",
    "SimpleWorkTitle",
    "TownName",
    "UnusualWorkTitle",
    "WorkTitle",
]
