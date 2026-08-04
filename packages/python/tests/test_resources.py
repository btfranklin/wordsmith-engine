"""Resource-loading behavior tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from wordsmith.util.resources import load_json


def test_missing_asset_names_the_requested_file() -> None:
    filename = "Definitely Missing.json"

    with pytest.raises(
        FileNotFoundError,
        match=r"^Wordsmith asset not found: Definitely Missing\.json$",
    ):
        load_json(filename)


def test_invalid_asset_json_error_propagates(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    filename = "Invalid.json"
    (tmp_path / filename).write_text("not JSON", encoding="utf-8")

    def resource_root(_: str) -> Path:
        return tmp_path

    monkeypatch.setattr("wordsmith.util.resources.resources.files", resource_root)
    load_json.cache_clear()
    try:
        with pytest.raises(json.JSONDecodeError):
            load_json(filename)
    finally:
        load_json.cache_clear()
