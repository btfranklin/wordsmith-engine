"""Resource loading helpers for Wordsmith assets."""

from __future__ import annotations

from functools import lru_cache
import json
from importlib import resources
from typing import Any


@lru_cache(maxsize=None)
def load_json(filename: str) -> Any:
    """Load a JSON asset from the wordsmith package."""
    try:
        payload = resources.files("wordsmith.assets").joinpath(filename).read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    return json.loads(payload)
