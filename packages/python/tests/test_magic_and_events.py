"""Check magic and event generator quality and shared components."""

from dataclasses import FrozenInstanceError
import random

import pytest

from wordsmith import (
    ArtifactName, FestivalName, MagicalConcept, OperationName, SpellName, text,
)
from tests.test_generator_conformance import _ScriptedRandom


@pytest.mark.parametrize("generator_type", [
    ArtifactName, SpellName, OperationName, FestivalName,
])
def test_names_are_immutable_clean_varied_and_repeatable(generator_type):
    generator = generator_type()
    with pytest.raises(FrozenInstanceError):
        generator.extra = "changed"
    rng = random.Random(5343)
    replay = random.Random(5343)
    outputs = [generator(rng) for _ in range(200)]
    assert outputs == [generator(replay) for _ in range(200)]
    assert len(set(outputs)) > 100
    for output in outputs:
        assert output == output.strip()
        assert "  " not in output
        assert "the the " not in output.lower()
        assert output[0].isupper()
        assert output[-1].isalpha()


def test_magic_and_event_compositions_share_one_stream():
    rng = random.Random(42)
    replay = random.Random(42)
    parts = [ArtifactName(), SpellName(), OperationName(), FestivalName()]
    assert text(*parts, sep=" / ")(rng) == " / ".join(part(replay) for part in parts)
    assert rng.getstate() == replay.getstate()


def test_magical_concept_changes_reach_artifacts_and_spells(monkeypatch):
    monkeypatch.setattr(MagicalConcept, "make_text", lambda self, rng: "new echoes")
    assert ArtifactName()(_ScriptedRandom([])) == "The Crown of New Echoes"
    assert SpellName()(_ScriptedRandom([])) == "Veil of New Echoes"
