"""Composite generators for Wordsmith."""

from .album_title import AlbumTitle
from .band_name import BandName
from .criminal_gang_name import CriminalGangName
from .fictional_element_name import FictionalElementName
from .fictional_mineral_name import FictionalMineralName
from .nautical_ship_name import NauticalShipName
from .movie_title import HighConceptMovieTitle, MovieTitle, SimpleMovieTitle
from .town_name import TownName
from .literary_title import LiteraryTitle, SimpleLiteraryTitle, UnusualLiteraryTitle

__all__ = [
    "AlbumTitle",
    "BandName",
    "CriminalGangName",
    "FictionalElementName",
    "FictionalMineralName",
    "HighConceptMovieTitle",
    "NauticalShipName",
    "LiteraryTitle",
    "MovieTitle",
    "SimpleLiteraryTitle",
    "SimpleMovieTitle",
    "TownName",
    "UnusualLiteraryTitle",
]
