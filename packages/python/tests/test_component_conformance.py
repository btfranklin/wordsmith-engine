"""Conformance tests for the language-neutral component contract."""

from __future__ import annotations

import json
from pathlib import Path
import random

import pytest

from wordsmith.core import Component, Empty, text


_CONFORMANCE_ROOT = (
    Path(__file__).resolve().parents[3] / "spec" / "conformance"
)
_CONSUMED_FIXTURES = {
    "component-sequences.json",
    "generator-traces.json",
    "public-api.json",
    "string-transforms.json",
}


class _CountingRandom(random.Random):
    """Record how many random draws conformance probes consume."""

    def __init__(self, seed: int) -> None:
        super().__init__(seed)
        self.draw_count = 0

    def random(self) -> float:
        self.draw_count += 1
        return super().random()


class _Probe(Component):
    """Test-only component that records rendering and consumes one draw."""

    def __init__(
        self,
        label: str,
        output: str,
        render_order: list[str],
        random_source_ids: list[int],
    ) -> None:
        self._label = label
        self._output = output
        self._render_order = render_order
        self._random_source_ids = random_source_ids

    def make_text(self, rng: random.Random) -> str:
        self._render_order.append(self._label)
        self._random_source_ids.append(id(rng))
        rng.random()
        return self._output


def _load_fixture(filename: str) -> dict[str, object]:
    with (_CONFORMANCE_ROOT / filename).open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


_SEQUENCE_FIXTURE = _load_fixture("component-sequences.json")
_SEQUENCE_CASES = _SEQUENCE_FIXTURE["cases"]
assert isinstance(_SEQUENCE_CASES, list)


def _build_part(
    fixture_part: object,
    render_order: list[str],
    random_source_ids: list[int],
) -> Component | str:
    if isinstance(fixture_part, str):
        return fixture_part

    assert isinstance(fixture_part, dict)
    kind = fixture_part.get("kind")

    if kind == "empty":
        return Empty()

    if kind == "sequence":
        separator = fixture_part.get("separator")
        raw_parts = fixture_part.get("parts")
        assert isinstance(separator, str)
        assert isinstance(raw_parts, list)
        parts = [
            _build_part(part, render_order, random_source_ids)
            for part in raw_parts
        ]
        return text(*parts, sep=separator)

    if kind == "probe":
        label = fixture_part.get("label")
        output = fixture_part.get("text")
        assert isinstance(label, str)
        assert isinstance(output, str)
        return _Probe(label, output, render_order, random_source_ids)

    raise AssertionError(f"Unsupported conformance part kind: {kind!r}")


def _case_name(case: object) -> str:
    assert isinstance(case, dict)
    name = case.get("name")
    assert isinstance(name, str)
    return name


def test_every_conformance_fixture_is_consumed() -> None:
    fixture_files = {
        path.name for path in _CONFORMANCE_ROOT.glob("*.json")
    }
    assert fixture_files == _CONSUMED_FIXTURES


@pytest.mark.parametrize(
    "case",
    _SEQUENCE_CASES,
    ids=[_case_name(case) for case in _SEQUENCE_CASES],
)
def test_component_sequence_conformance(case: object) -> None:
    assert isinstance(case, dict)
    separator = case.get("separator")
    raw_parts = case.get("parts")
    expected = case.get("expected")
    assert isinstance(separator, str)
    assert isinstance(raw_parts, list)
    assert isinstance(expected, str)

    render_order: list[str] = []
    random_source_ids: list[int] = []
    parts = [
        _build_part(part, render_order, random_source_ids)
        for part in raw_parts
    ]
    component = text(*parts, sep=separator)

    assert render_order == []
    assert random_source_ids == []

    mutation = case.get("mutationAfterConstruction")
    if mutation is not None:
        assert isinstance(mutation, dict)
        index = mutation.get("index")
        assert isinstance(index, int)
        parts[index] = _build_part(
            mutation.get("replacement"),
            render_order,
            random_source_ids,
        )

    rng = _CountingRandom(20260728)
    assert component.make_text(rng) == expected

    expected_render_order = case.get("expectedRenderOrder", [])
    expected_random_draws = case.get("expectedRandomDraws", 0)
    assert isinstance(expected_render_order, list)
    assert all(isinstance(label, str) for label in expected_render_order)
    assert isinstance(expected_random_draws, int)
    assert expected_random_draws >= 0
    assert render_order == expected_render_order
    assert rng.draw_count == expected_random_draws
    assert random_source_ids == [id(rng)] * expected_random_draws
