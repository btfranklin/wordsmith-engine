"""Tests for composite generators."""

from __future__ import annotations

import random

from wordsmith.factories import ReadableUniqueIdentifierFactory
from wordsmith.generators import (
    BandName,
    CriminalGangName,
    FictionalElementName,
    FictionalMineralName,
    NauticalShipName,
    TownName,
    WorkTitle,
)
from tests.utils import assert_nonempty, assert_repeatable


def test_band_name_repeatable() -> None:
    assert_repeatable(BandName())


def test_criminal_gang_name_repeatable() -> None:
    assert_repeatable(CriminalGangName())


def test_fictional_element_name_repeatable() -> None:
    assert_repeatable(FictionalElementName())


def test_fictional_mineral_name_repeatable() -> None:
    assert_repeatable(FictionalMineralName())


def test_nautical_ship_name_repeatable() -> None:
    assert_repeatable(NauticalShipName())


def test_town_name_repeatable() -> None:
    assert_repeatable(TownName())


def test_work_title_repeatable() -> None:
    assert_repeatable(WorkTitle())


def test_identifier_format() -> None:
    identifier = ReadableUniqueIdentifierFactory.make_identifier(random.Random(0))
    parts = identifier.split("_")
    assert len(parts) >= 3
    assert parts[-1].isalnum()
    assert parts[-1].upper() == parts[-1]


def test_nonempty_outputs() -> None:
    assert_nonempty(BandName())
    assert_nonempty(CriminalGangName())
    assert_nonempty(FictionalElementName())
    assert_nonempty(FictionalMineralName())
    assert_nonempty(NauticalShipName())
    assert_nonempty(TownName())
    assert_nonempty(WorkTitle())
