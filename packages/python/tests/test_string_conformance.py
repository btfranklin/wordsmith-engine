"""Conformance tests for shared English-oriented string behavior."""

from __future__ import annotations

import json
from pathlib import Path
import random

import pytest

from wordsmith.core.components import Literal
from wordsmith.util.strings import starts_with_vowel


FIXTURE_PATH = (
    Path(__file__).resolve().parents[3]
    / "spec"
    / "conformance"
    / "string-transforms.json"
)
with FIXTURE_PATH.open(encoding="utf-8") as fixture_file:
    CASES = json.load(fixture_file)


@pytest.mark.parametrize("case", CASES["capitalized"])
def test_capitalized_conformance(case: dict[str, str]) -> None:
    assert Literal(case["input"]).capitalized().make_text(random.Random(0)) == case[
        "expected"
    ]


@pytest.mark.parametrize("case", CASES["firstUpper"])
def test_first_upper_conformance(case: dict[str, str]) -> None:
    assert Literal(case["input"]).first_upper().make_text(random.Random(0)) == case[
        "expected"
    ]


@pytest.mark.parametrize("case", CASES["titleCase"])
def test_title_case_conformance(case: dict[str, str]) -> None:
    assert Literal(case["input"]).title_case().make_text(random.Random(0)) == case[
        "expected"
    ]


@pytest.mark.parametrize("case", CASES["possessiveForm"])
def test_possessive_conformance(case: dict[str, str]) -> None:
    assert Literal(case["input"]).possessive_form().make_text(random.Random(0)) == case[
        "expected"
    ]


@pytest.mark.parametrize("case", CASES["startsWithVowel"])
def test_starts_with_vowel_conformance(case: dict[str, object]) -> None:
    assert starts_with_vowel(str(case["input"])) is case["expected"]
