"""Shared scripted-RNG conformance tests for generators."""

from __future__ import annotations

import json
import math
from pathlib import Path
import random

import pytest

from wordsmith import (
    AlienName,
    AlbumTitle,
    AncientGivenName,
    BandName,
    BinaryGender,
    CriminalGangName,
    FantasyName,
    FictionalElementName,
    FictionalMineralName,
    GivenName,
    GivenNameCulture,
    HighConceptMovieTitle,
    LiteraryTitle,
    MovieTitle,
    NauticalShipName,
    PersonName,
    SimpleLiteraryTitle,
    SimpleMovieTitle,
    TownName,
    UnusualLiteraryTitle,
)
from wordsmith.core import Component


_FIXTURE_PATH = (
    Path(__file__).resolve().parents[3]
    / "spec"
    / "conformance"
    / "generator-traces.json"
)
with _FIXTURE_PATH.open(encoding="utf-8") as fixture_file:
    _CASES = json.load(fixture_file)["cases"]

_GENERATORS: dict[str, type[Component]] = {
    generator.__name__: generator
    for generator in (
        AlbumTitle,
        BandName,
        CriminalGangName,
        FictionalElementName,
        FictionalMineralName,
        HighConceptMovieTitle,
        LiteraryTitle,
        MovieTitle,
        NauticalShipName,
        SimpleLiteraryTitle,
        SimpleMovieTitle,
        TownName,
        UnusualLiteraryTitle,
    )
}


def _build_generator(name: str, configuration: object) -> Component:
    assert isinstance(configuration, dict)
    if name in {"GivenName", "AncientGivenName", "PersonName"}:
        allowed_keys = (
            {"gender"} if name == "AncientGivenName" else {"gender", "culture"}
        )
        assert configuration.keys() <= allowed_keys
        gender = (
            BinaryGender(configuration["gender"])
            if "gender" in configuration
            else None
        )
        if name == "AncientGivenName":
            return AncientGivenName(gender=gender)
        culture = (
            GivenNameCulture(configuration["culture"])
            if "culture" in configuration
            else None
        )
        if name == "GivenName":
            return GivenName(gender=gender, culture=culture)
        return PersonName(gender=gender, culture=culture)
    if name in {"AlienName", "FantasyName"}:
        assert configuration.keys() <= {
            "syllableCount", "allowHyphen", "allowApostrophe",
        }
        syllable_count = configuration["syllableCount"]
        allow_hyphen = configuration.get("allowHyphen", True)
        allow_apostrophe = configuration.get("allowApostrophe", True)
        assert type(syllable_count) is int
        assert isinstance(allow_hyphen, bool)
        assert isinstance(allow_apostrophe, bool)
        name_type = AlienName if name == "AlienName" else FantasyName
        return name_type(
            syllable_count=syllable_count,
            allow_hyphen=allow_hyphen,
            allow_apostrophe=allow_apostrophe,
        )
    assert configuration == {}
    return _GENERATORS[name]()


class _ScriptedRandom(random.Random):
    """Adapt fixture fractions to the subset of ``random.Random`` Wordsmith uses."""

    def __init__(
        self,
        fractions: list[float],
        *,
        repeat: float = 0.0,
        cycle: bool = False,
    ) -> None:
        super().__init__(0)
        if cycle and not fractions:
            raise ValueError("Cyclic scripted RNGs require at least one fraction.")
        self._fractions = fractions
        self._repeat = repeat
        self._cycle = cycle
        self.draw_count = 0

    def random(self) -> float:
        if self._cycle:
            value = self._fractions[self.draw_count % len(self._fractions)]
        elif self.draw_count < len(self._fractions):
            value = self._fractions[self.draw_count]
        else:
            value = self._repeat
        self.draw_count += 1
        if not math.isfinite(value) or not 0.0 <= value < 1.0:
            raise ValueError("Scripted fractions must be finite values in [0, 1).")
        return value

    def choice(self, seq):  # type: ignore[no-untyped-def]
        return seq[min(int(self.random() * len(seq)), len(seq) - 1)]

    def choices(  # type: ignore[no-untyped-def]
        self,
        population,
        weights=None,
        *,
        cum_weights=None,
        k=1,
    ):
        assert k == 1
        assert weights is not None
        assert cum_weights is None
        target = self.random() * sum(weights)
        cumulative = 0.0
        for item, weight in zip(population, weights, strict=True):
            cumulative += weight
            if target < cumulative:
                return [item]
        return [population[-1]]

    def randrange(self, start, stop=None, step=1):  # type: ignore[no-untyped-def]
        values = range(start) if stop is None else range(start, stop, step)
        return values[min(int(self.random() * len(values)), len(values) - 1)]


def _case_id(case: object) -> str:
    assert isinstance(case, dict)
    name = case.get("name")
    intent = case.get("intent")
    assert isinstance(name, str)
    assert isinstance(intent, str)
    assert intent.strip()
    return f"{name}: {intent}"


def test_generator_trace_metadata() -> None:
    names = []
    for case in _CASES:
        assert isinstance(case, dict)
        name = case.get("name")
        intent = case.get("intent")
        assert isinstance(name, str)
        assert name.strip()
        assert isinstance(intent, str)
        assert intent.strip()
        names.append(name)
    assert len(names) == len(set(names))


@pytest.mark.parametrize("case", _CASES, ids=[_case_id(case) for case in _CASES])
def test_generator_trace(case: object) -> None:
    assert isinstance(case, dict)
    generator_name = case["generator"]
    fractions = case["fractions"]
    expected = case["expected"]
    expected_draws = case["expectedDraws"]
    intent = case["intent"]
    assert isinstance(generator_name, str)
    assert isinstance(fractions, list)
    assert all(isinstance(value, (int, float)) for value in fractions)
    assert isinstance(expected, str)
    assert isinstance(expected_draws, int)
    assert isinstance(intent, str)
    assert intent.strip()

    rng = _ScriptedRandom(
        [float(value) for value in fractions],
        repeat=float(case.get("repeat", 0.0)),
        cycle=case.get("cycle", False) is True,
    )

    generator = _build_generator(generator_name, case.get("configuration", {}))
    assert generator.make_text(rng) == expected
    assert rng.draw_count == expected_draws
