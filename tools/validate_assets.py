"""Validate the canonical Wordsmith asset shapes without rewriting them."""

from __future__ import annotations

from datetime import date
import json
import math
from pathlib import Path
import unicodedata


ASSET_DIRECTORY = Path(__file__).resolve().parents[1] / "assets"
EXPECTED_NAMES = {
    "Adjectives.json",
    "Adverbs.json",
    "Chemical Compound Names.json",
    "Common Surnames.json",
    "Curated Word Lists.json",
    "Exotic Character Sets.json",
    "Given Names.json",
    "Literary Title Parts.json",
    "Material Name Parts.json",
    "Nouns.json",
    "Synthetic Name Parts.json",
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


def validate_named_string_lists(name: str, expected_keys: list[str]) -> None:
    value = load(name)
    if not isinstance(value, dict) or list(value) != expected_keys:
        raise AssertionError(f"{name} has unexpected keys")
    for key, options in value.items():
        string_list(options, f"{name}.{key}")


def validate_curated_word_lists() -> None:
    validate_named_string_lists(
        "Curated Word Lists.json",
        [
            "authoredArtifacts",
            "locationAdjectives",
            "martialSocialConcepts",
            "ucBerkeleyEmotions",
            "villainousPersonNouns",
            "primitiveWeapons",
            "nauticalShipNameObjects",
            "nauticalShipNameColors",
            "shipNameAdjectives",
            "timesOfDay",
        ],
    )


def validate_synthetic_name_parts() -> None:
    value = load("Synthetic Name Parts.json")
    if not isinstance(value, dict) or list(value) != ["alien", "fantasy"]:
        raise AssertionError("Synthetic Name Parts.json has unexpected top-level keys")

    expected_keys = {
        "alien": ["openEndedSyllables", "endingSounds"],
        "fantasy": ["prefixes", "middles", "endings", "compoundEndings"],
    }
    for family, keys in expected_keys.items():
        parts = value[family]
        if not isinstance(parts, dict) or list(parts) != keys:
            raise AssertionError(
                f"Synthetic Name Parts.json has unexpected {family} keys"
            )
        for key, options in parts.items():
            string_list(options, f"Synthetic Name Parts.json.{family}.{key}")


def validate_material_name_parts() -> None:
    value = load("Material Name Parts.json")
    expected_keys = [
        "elementPrefixes",
        "elementMiddles",
        "mineralPrefixes",
        "mineralMiddles",
        "realElements",
        "elementSuffixes",
        "mineralSuffixes",
    ]
    if not isinstance(value, dict) or list(value) != expected_keys:
        raise AssertionError("Material Name Parts.json has unexpected keys")

    for key in ["elementPrefixes", "mineralPrefixes", "realElements"]:
        string_list(value[key], f"Material Name Parts.json.{key}")
    for key in ["elementMiddles", "mineralMiddles"]:
        options = value[key]
        if (
            not isinstance(options, list)
            or not options
            or not all(isinstance(option, str) for option in options)
            or len(options) != len(set(options))
        ):
            raise AssertionError(
                f"Material Name Parts.json.{key} must contain unique strings"
            )

    for key in ["elementSuffixes", "mineralSuffixes"]:
        rows = value[key]
        if not isinstance(rows, list) or not rows:
            raise AssertionError(f"Material Name Parts.json.{key} must be nonempty")
        suffixes: list[str] = []
        for index, row in enumerate(rows):
            if (
                not isinstance(row, list)
                or len(row) != 2
                or not isinstance(row[0], (int, float))
                or isinstance(row[0], bool)
                or not math.isfinite(row[0])
                or row[0] <= 0
                or not isinstance(row[1], str)
                or not row[1]
            ):
                raise AssertionError(
                    "Invalid weighted suffix at "
                    f"Material Name Parts.json.{key}[{index}]"
                )
            suffixes.append(row[1])
        if len(suffixes) != len(set(suffixes)):
            raise AssertionError(f"Material Name Parts.json.{key} repeats a suffix")


def validate_literary_title_parts() -> None:
    value = load("Literary Title Parts.json")
    expected_keys = [
        "objects",
        "pluralObjects",
        "sentientObjects",
        "qualities",
        "abstractions",
        "placeSuffixes",
        "verbs",
    ]
    if not isinstance(value, dict) or list(value) != expected_keys:
        raise AssertionError("Literary Title Parts.json has unexpected keys")
    for key in expected_keys[:-1]:
        string_list(value[key], f"Literary Title Parts.json.{key}")

    verbs = value["verbs"]
    if not isinstance(verbs, list) or not verbs:
        raise AssertionError("Literary Title Parts.json.verbs must be nonempty")
    rows: list[tuple[str, str, str]] = []
    for index, row in enumerate(verbs):
        if (
            not isinstance(row, list)
            or len(row) != 3
            or not all(isinstance(form, str) and form for form in row)
        ):
            raise AssertionError(
                f"Invalid verb row at Literary Title Parts.json.verbs[{index}]"
            )
        rows.append((row[0], row[1], row[2]))
    if len(rows) != len(set(rows)):
        raise AssertionError("Literary Title Parts.json.verbs contains duplicate rows")


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
    validate_curated_word_lists()
    validate_synthetic_name_parts()
    validate_material_name_parts()
    validate_literary_title_parts()
    validate_exotic_sets()

    for name in EXPECTED_NAMES:
        assert_normalized(load(name), name)


if __name__ == "__main__":
    main()
