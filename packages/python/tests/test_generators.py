"""Tests for composite generators."""

from __future__ import annotations

import random
import re

import pytest

from wordsmith.specials import ReadableUniqueIdentifier
from wordsmith.generators import (
    AlbumTitle,
    BandName,
    CriminalGangName,
    FictionalElementName,
    FictionalMineralName,
    MovieTitle,
    NauticalShipName,
    TownName,
    LiteraryTitle,
)
from wordsmith.names import AlienName, FantasyName
from tests.utils import assert_nonempty, assert_repeatable


def test_band_name_repeatable() -> None:
    assert_repeatable(BandName())


def test_album_title_repeatable() -> None:
    assert_repeatable(AlbumTitle())


def test_criminal_gang_name_repeatable() -> None:
    assert_repeatable(CriminalGangName())


def test_fictional_element_name_repeatable() -> None:
    assert_repeatable(FictionalElementName())


def test_fictional_mineral_name_repeatable() -> None:
    assert_repeatable(FictionalMineralName())


def test_fictional_material_names_are_clean_tokens() -> None:
    rng = random.Random(923)
    names = [
        *(FictionalElementName().make_text(rng) for _ in range(250)),
        *(FictionalMineralName().make_text(rng) for _ in range(250)),
    ]

    assert all(re.fullmatch(r"[a-z]+", name) is not None for name in names)
    assert all("iium" not in name for name in names)
    assert all(3 < len(name) <= 20 for name in names)


def test_fictional_material_names_use_distinct_suffixes() -> None:
    rng = random.Random(924)
    element_names = [FictionalElementName().make_text(rng) for _ in range(250)]
    mineral_names = [FictionalMineralName().make_text(rng) for _ in range(250)]

    assert all(
        name not in FictionalElementName._real_element_names
        for name in element_names
    )
    assert all(
        name.endswith(("ium", "on", "ine", "ene", "gen"))
        for name in element_names
    )
    assert all(
        name.endswith(("ite", "ine", "spar", "stone", "ore", "cryst", "glass"))
        for name in mineral_names
    )
    assert any(
        name.endswith(("spar", "stone", "ore", "cryst", "glass"))
        for name in mineral_names
    )


def test_nautical_ship_name_repeatable() -> None:
    assert_repeatable(NauticalShipName())


def test_nautical_ship_names_use_fantasy_not_alien_names(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    marker = "fantasy provenance"

    monkeypatch.setattr(
        FantasyName,
        "make_text",
        lambda self, rng: marker,
    )

    def reject_alien_name(self: AlienName, rng: random.Random) -> str:
        raise AssertionError("NauticalShipName rendered AlienName")

    monkeypatch.setattr(AlienName, "make_text", reject_alien_name)

    rng = random.Random(20260713)
    outputs = [NauticalShipName().make_text(rng) for _ in range(500)]

    assert "Fantasy Provenance" in outputs


def test_movie_title_repeatable() -> None:
    assert_repeatable(MovieTitle())


def test_town_name_repeatable() -> None:
    assert_repeatable(TownName())


def test_literary_title_repeatable() -> None:
    assert_repeatable(LiteraryTitle())


def test_literary_title_has_fixed_deep_replay_vector() -> None:
    assert (
        LiteraryTitle().make_text(random.Random(22))
        == "A Manual for Teaching the Garden to Vanish"
    )


def test_literary_titles_have_title_shape() -> None:
    rng = random.Random(20260617)
    titles = [LiteraryTitle().make_text(rng) for _ in range(250)]

    assert all(title == title.strip() for title in titles)
    assert all("  " not in title for title in titles)
    assert all(len(title.split()) >= 2 for title in titles)
    assert all(not title.lower().endswith("ly") for title in titles)
    assert all("''" not in title and "\"\"" not in title for title in titles)


def test_literary_titles_avoid_bare_singular_motifs_after_of() -> None:
    rng = random.Random(6789)
    titles = [LiteraryTitle().make_text(rng) for _ in range(500)]
    singular_motifs = (
        "Archive",
        "Bell",
        "Bridge",
        "Camera",
        "Cipher",
        "Clock",
        "Compass",
        "Door",
        "Garden",
        "Harbor",
        "Key",
        "Lantern",
        "Machine",
        "Map",
        "Mirror",
        "Moon",
        "Orchard",
        "Room",
        "Signal",
        "Staircase",
        "Station",
        "Thread",
        "Window",
    )
    awkward_pattern = re.compile(rf" of ({'|'.join(singular_motifs)})(?:$|\\b)")

    assert all(awkward_pattern.search(title) is None for title in titles)


def test_album_titles_have_shape_variety() -> None:
    rng = random.Random(31415)
    titles = [AlbumTitle().make_text(rng) for _ in range(120)]

    assert all(title == title.strip() for title in titles)
    assert all(title for title in titles)
    assert all("  " not in title for title in titles)
    assert any(len(title.split()) == 1 for title in titles)
    assert any(len(title.split()) > 1 for title in titles)


def test_movie_titles_include_hook_shapes() -> None:
    rng = random.Random(27182)
    titles = [MovieTitle().make_text(rng) for _ in range(160)]
    hook_prefixes = (
        "Escape from ",
        "Return to ",
        "The Fall of ",
        "The Last Days of ",
        "Before ",
        "After ",
        "When ",
    )

    assert all(title == title.strip() for title in titles)
    assert all(title for title in titles)
    assert all("  " not in title for title in titles)
    assert any(title.startswith(hook_prefixes) for title in titles)


def test_identifier_format() -> None:
    identifier = ReadableUniqueIdentifier.make_identifier(random.Random(0))
    parts = identifier.split("_")
    assert len(parts) >= 3
    assert parts[-1].isalnum()
    assert parts[-1].upper() == parts[-1]


def test_nonempty_outputs() -> None:
    assert_nonempty(AlbumTitle())
    assert_nonempty(BandName())
    assert_nonempty(CriminalGangName())
    assert_nonempty(FictionalElementName())
    assert_nonempty(FictionalMineralName())
    assert_nonempty(NauticalShipName())
    assert_nonempty(TownName())
    assert_nonempty(LiteraryTitle())
    assert_nonempty(MovieTitle())
