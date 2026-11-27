"""Check the shared person-name formats and hash results."""

from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import random
import re

import pytest

from wordsmith import BinaryGender, GivenNameCulture, PersonName, PersonNameModifiers
from wordsmith.names.person_name import GivenNamePart


_CASES = json.loads(
    (
        Path(__file__).resolve().parents[3] / "spec/conformance/person-names.json"
    ).read_text(encoding="utf-8")
)
_OPTION_NAMES = {
    "givenNameFormat": "given_name_format",
    "initialPeriod": "initial_period",
    "initialSeparator": "initial_separator",
    "generationSeparator": "generation_separator",
    "credentialSeparator": "credential_separator",
    "formatWeights": "format_weights",
    "modifierWeights": "modifier_weights",
}


def _generator(configuration):
    options = {
        _OPTION_NAMES.get(key, key): value for key, value in configuration.items()
    }
    if "gender" in options:
        options["gender"] = BinaryGender(options["gender"])
    if "culture" in options:
        options["culture"] = GivenNameCulture(options["culture"])
    if "modifier_weights" in options:
        options["modifier_weights"] = [
            (weight, PersonNameModifiers(**value))
            for weight, value in options["modifier_weights"]
        ]
    return PersonName(**options)


class _Draws(random.Random):
    def __init__(self, fractions):
        super().__init__(0)
        self.fractions = iter(fractions)

    def random(self):
        return next(self.fractions)

    def choice(self, choices):
        return choices[int(self.random() * len(choices))]


@pytest.mark.parametrize("case", _CASES["draws"], ids=lambda case: case["name"])
def test_person_name_draws(case):
    rng = _Draws(case["fractions"])
    assert _generator(case["configuration"])(rng) == case["expected"]
    assert next(rng.fractions, None) is None


def test_person_name_hash_replay():
    def render(case):
        return _generator(case["configuration"]).from_hash(case["digest"])

    cases = _CASES["hashes"]
    assert [render(case) for case in cases] == [case["expected"] for case in cases]
    with ThreadPoolExecutor() as executor:
        assert list(executor.map(render, reversed(cases))) == [
            case["expected"] for case in reversed(cases)
        ]
        instance = PersonName()
        assert list(executor.map(instance.from_hash, ["ff" * 32, "00" * 32])) == [
            "Seok-mun Harding", "Kandi Santos"
        ]


@pytest.mark.parametrize("digest", ["", "0" * 63, "0" * 63 + "\n", "z" * 64])
def test_person_name_rejects_invalid_hash(digest):
    with pytest.raises(ValueError, match="SHA-256"):
        PersonName().from_hash(digest)


def test_person_name_hash_frequency():
    plain = PersonName()
    varied = PersonName(style="varied")
    modifier = re.compile(
        r"^(Dr\.|Prof\.) | (Jr\.|Sr\.|II|III|IV|V)$|, (Esq\.|PhD\.|MD)$"
    )
    changed_formats = 0
    modifiers = 0
    for number in range(1024):
        digest = f"{number:064x}"
        unmodified, count = modifier.subn("", varied.from_hash(digest))
        changed_formats += unmodified != plain.from_hash(digest)
        modifiers += count
    assert 140 <= changed_formats <= 220
    assert 16 <= modifiers <= 48


def test_person_name_snapshots_options():
    credentials = ["PhD."]
    format_weights: list[tuple[float, list[GivenNamePart]]] = [(1.0, ["full"])]
    value = PersonName(
        credentials=credentials,
        format_weights=format_weights,
    )
    credentials.clear()
    format_weights.clear()
    assert value.from_hash("0" * 64) == "Kandi Santos, PhD."


@pytest.mark.parametrize("weights", [[], [(0, ["full"])], [(-1, ["full"])]])
def test_person_name_rejects_invalid_weights(weights):
    with pytest.raises(ValueError, match="Weights"):
        PersonName(format_weights=weights)
