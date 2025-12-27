"""Randomness helpers for Wordsmith."""

from __future__ import annotations

import random


def random_bool(rng: random.Random, probability: float = 0.5) -> bool:
    """Return True with the given probability."""
    if not 0.0 <= probability <= 1.0:
        raise ValueError("Probability must be in the range 0.0 to 1.0.")
    return rng.random() < probability
