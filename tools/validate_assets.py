"""Validate the canonical Wordsmith asset shapes without rewriting them."""

from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import unicodedata


ASSET_DIRECTORY = Path(__file__).resolve().parents[1] / "assets"
EXPECTED_NAMES = {
    "Adjectives.json",
    "Adverbs.json",
    "Chemical Compound Names.json",
    "Common Surnames.json",
    "Exotic Character Sets.json",
    "Given Names.json",
    "Nouns.json",
    "Verbs.json",
}
EXOTIC_SET_NAMES = [
    "aegeanNumbers",
    "alchemicalSymbols",
    "carian",
    "cuneiform",
    "glagolitic",
    "linearA",
    "linearBIdeograms",
    "linearBSyllabary",
    "oldPersian",
    "runic",
    "ugaritic",
]


def load(name: str) -> object:
    raw = (ASSET_DIRECTORY / name).read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise AssertionError(f"{name} contains a UTF-8 BOM")
    if not raw.endswith(b"\n"):
        raise AssertionError(f"{name} must end with a newline")
    return json.loads(raw)


def assert_normalized(value: object, location: str) -> None:
    if isinstance(value, str):
        if unicodedata.normalize("NFC", value) != value:
            raise AssertionError(f"Non-NFC text at {location}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            assert_normalized(item, f"{location}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            assert_normalized(key, f"{location}.<key>")
            assert_normalized(item, f"{location}.{key}")


def string_list(value: object, location: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise AssertionError(f"{location} must be a nonempty list")
    if not all(isinstance(item, str) and item for item in value):
        raise AssertionError(f"{location} must contain nonempty strings")
    result = list(value)
    if len(result) != len(set(result)):
        raise AssertionError(f"{location} contains duplicate entries")
    return result


def validate_tabular(name: str, width: int) -> None:
    value = load(name)
    if not isinstance(value, list) or not value:
        raise AssertionError(f"{name} must be a nonempty list")
    rows: list[tuple[str, ...]] = []
    for index, row in enumerate(value):
        if (
            not isinstance(row, list)
            or len(row) != width
            or not all(isinstance(item, str) and item for item in row)
        ):
            raise AssertionError(f"Invalid row at {name}[{index}]")
        rows.append(tuple(row))
    if len(rows) != len(set(rows)):
        raise AssertionError(f"{name} contains duplicate rows")


def validate_given_names() -> None:
    value = load("Given Names.json")
    if not isinstance(value, dict) or list(value) != ["_meta", "modern", "ancient"]:
        raise AssertionError("Given Names.json has unexpected top-level keys")
    metadata = value["_meta"]
    if not isinstance(metadata, dict):
        raise AssertionError("Given-name metadata must be an object")
    if list(metadata) != ["source", "source_url", "license", "refreshed_on", "notes"]:
        raise AssertionError("Given-name metadata has unexpected keys")
    if not isinstance(metadata["refreshed_on"], str):
        raise AssertionError("Given-name refresh date must be a string")
    date.fromisoformat(metadata["refreshed_on"])

    modern = value["modern"]
    if not isinstance(modern, dict) or list(modern) != [
        "english_speaking",
        "latin_american",
        "eastern",
    ]:
        raise AssertionError("Given-name modern culture keys are invalid")
    groups = [*modern.values(), value["ancient"]]
    for index, group in enumerate(groups):
        if not isinstance(group, dict) or list(group) != ["male", "female"]:
            raise AssertionError(f"Given-name gender keys are invalid at group {index}")
        string_list(group["male"], f"given-names[{index}].male")
        string_list(group["female"], f"given-names[{index}].female")


def validate_exotic_sets() -> None:
    value = load("Exotic Character Sets.json")
    if not isinstance(value, dict) or list(value) != EXOTIC_SET_NAMES:
        raise AssertionError("Exotic character set order or names changed")
    seen: set[str] = set()
    for set_name, raw_characters in value.items():
        characters = string_list(raw_characters, f"exotic.{set_name}")
        for character in characters:
            if len(character) != 1:
                raise AssertionError(f"{set_name} contains a non-character value")
            if character in seen:
                raise AssertionError(f"Exotic character {character!r} is duplicated")
            seen.add(character)


def main() -> None:
    found = {path.name for path in ASSET_DIRECTORY.glob("*.json")}
    if found != EXPECTED_NAMES:
        raise AssertionError(
            f"Expected assets {sorted(EXPECTED_NAMES)}, found {sorted(found)}"
        )

    for name in [
        "Adjectives.json",
        "Adverbs.json",
        "Chemical Compound Names.json",
        "Common Surnames.json",
    ]:
        string_list(load(name), name)
    validate_tabular("Nouns.json", 2)
    validate_tabular("Verbs.json", 5)
    validate_given_names()
    validate_exotic_sets()

    for name in EXPECTED_NAMES:
        assert_normalized(load(name), name)


if __name__ == "__main__":
    main()
