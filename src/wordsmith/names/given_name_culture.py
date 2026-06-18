"""Cultural grouping definitions used by given-name generators."""

from __future__ import annotations

from enum import Enum


class GivenNameCulture(Enum):
    """Supported modern cultural groupings for given-name selection."""

    ENGLISH_SPEAKING = "english_speaking"
    LATIN_AMERICAN = "latin_american"
    EASTERN = "eastern"
