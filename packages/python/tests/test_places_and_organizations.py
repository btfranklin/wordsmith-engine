"""Check the quality and composition of place and organization names."""

from dataclasses import FrozenInstanceError
import random

import pytest

from wordsmith import (
    BusinessName, CelestialBodyName, CreatureName,
    LandmarkName, OrganizationName, TavernName, text,
)


@pytest.mark.parametrize("generator_type", [
    TavernName, LandmarkName, OrganizationName,
    BusinessName, CelestialBodyName, CreatureName,
])
def test_names_are_immutable_clean_and_repeatable(generator_type):
    generator = generator_type()
    with pytest.raises(FrozenInstanceError):
        generator.extra = "changed"
    first = random.Random(5343)
    second = random.Random(5343)
    outputs = [generator(first) for _ in range(100)]
    assert outputs == [generator(second) for _ in range(100)]
    assert len(set(outputs)) > 50
    for output in outputs:
        assert output == output.strip()
        assert "  " not in output
        assert output[0].isupper()


def test_nested_names_use_one_stream_in_order():
    rng = random.Random(42)
    expected_rng = random.Random(42)
    components = [
        TavernName(), LandmarkName(), OrganizationName(),
        BusinessName(), CelestialBodyName(), CreatureName(),
    ]
    combined = text(*components, sep=" / ")
    assert combined(rng) == " / ".join(part(expected_rng) for part in components)
    assert rng.getstate() == expected_rng.getstate()
