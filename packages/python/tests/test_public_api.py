"""Tests for the complete public package surface."""

from __future__ import annotations

import json
from pathlib import Path

import wordsmith


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
FIXTURE = json.loads(
    (REPOSITORY_ROOT / "spec" / "conformance" / "public-api.json").read_text(
        encoding="utf-8"
    )
)


def test_root_exports_match_shared_inventory() -> None:
    expected = FIXTURE["pythonRuntime"]
    assert sorted(wordsmith.__all__) == sorted(expected)
    assert len(wordsmith.__all__) == len(set(wordsmith.__all__))
    assert all(hasattr(wordsmith, name) for name in expected)


def test_api_document_mentions_every_public_symbol() -> None:
    api_document = (REPOSITORY_ROOT / "spec" / "API.md").read_text(encoding="utf-8")
    symbols = {
        *FIXTURE["pythonRuntime"],
        *FIXTURE["typescriptRuntime"],
        *FIXTURE["typescriptTypes"],
    }
    assert all(f"`{symbol}`" in api_document for symbol in symbols)
