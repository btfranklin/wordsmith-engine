"""Composite generators for Wordsmith."""

from .album_title import AlbumTitle
from .band_name import BandName
from .business_celestial_creature import (
    BusinessName,
    CelestialBodyName,
    CompoundCreatureName,
    CreatureName,
)
from .criminal_gang_name import CriminalGangName
from .fictional_element_name import FictionalElementName
from .fictional_mineral_name import FictionalMineralName
from .magic_and_event_names import ArtifactName, FestivalName, OperationName, SpellName
from .nautical_ship_name import NauticalShipName
from .place_and_organization_names import (
    CompoundLandmarkName,
    HeraldicSymbol,
    LandmarkName,
    OrganizationName,
    TavernName,
)
from .movie_title import HighConceptMovieTitle, MovieTitle, SimpleMovieTitle
from .town_name import TownName
from .literary_title import LiteraryTitle, SimpleLiteraryTitle, UnusualLiteraryTitle

__all__ = [
    "AlbumTitle",
    "ArtifactName",
    "BandName",
    "BusinessName",
    "CelestialBodyName",
    "CompoundCreatureName",
    "CompoundLandmarkName",
    "CriminalGangName",
    "CreatureName",
    "FictionalElementName",
    "FictionalMineralName",
    "FestivalName",
    "HighConceptMovieTitle",
    "HeraldicSymbol",
    "LandmarkName",
    "NauticalShipName",
    "OrganizationName",
    "OperationName",
    "LiteraryTitle",
    "MovieTitle",
    "SimpleLiteraryTitle",
    "SimpleMovieTitle",
    "SpellName",
    "TownName",
    "TavernName",
    "UnusualLiteraryTitle",
]
