"""Shared validation tests for weighted choices."""

from __future__ import annotations

import json
from pathlib import Path
import random

import pytest

from wordsmith import Component, WeightedOneOf, weighted_one_of


_FIXTURE_PATH = (
    Path(__file__).resolve().parents[3]
    / "spec"
    / "conformance"
    / "weighted-choices.json"
)
_CASES = json.loads(_FIXTURE_PATH.read_text(encoding="utf-8"))["cases"]


class _RenderProbe(Component):
    def make_text(self, rng: random.Random) -> str:
        raise AssertionError("Construction must not render children.")


@pytest.mark.parametrize("case", _CASES, ids=[case["name"] for case in _CASES])
def test_weighted_choice_validation_at_construction(case: dict[str, object]) -> None:
    raw_weights = case["weights"]
    accepted = case["accepted"]
    assert isinstance(raw_weights, list)
    assert isinstance(accepted, bool)
    weights = tuple(float(weight) for weight in raw_weights)
    options = [_RenderProbe() for _ in weights]

    if accepted:
        WeightedOneOf(options, weights)
        weighted_one_of(*zip(weights, options))
    else:
        with pytest.raises(ValueError):
            WeightedOneOf(options, weights)
        with pytest.raises(ValueError):
            weighted_one_of(*zip(weights, options))
