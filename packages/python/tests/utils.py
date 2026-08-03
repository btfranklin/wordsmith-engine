"""Testing helpers for Wordsmith."""

from __future__ import annotations

import random
from typing import Iterable

from wordsmith.core.base import Component


def assert_repeatable(component: Component, seed: int = 1234, count: int = 50) -> None:
    """Assert that component output is deterministic with a seeded RNG."""
    rng_a = random.Random(seed)
    rng_b = random.Random(seed)

    results_a = [component.make_text(rng_a) for _ in range(count)]
    results_b = [component.make_text(rng_b) for _ in range(count)]

    assert results_a == results_b


def assert_nonempty(component: Component, seed: int = 99) -> None:
    """Assert that component output is non-empty."""
    rng = random.Random(seed)
    assert component.make_text(rng)


def assert_in_options(value: str, options: Iterable[str]) -> None:
    """Assert that a value is present in a set of options."""
    assert value in set(options)
