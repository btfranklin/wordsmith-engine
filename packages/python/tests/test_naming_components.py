"""Check reusable naming components and their composed behavior."""

from dataclasses import FrozenInstanceError
import random

import pytest

from wordsmith import (
    ArtifactObject, SpellEffect, MagicalConcept, OperationColor, Season,
    BodyPart, BusinessAnimal, BusinessColor, BusinessTrade, CelestialObjectType,
    CompoundCreatureName, CompoundLandmarkName, CreatureType, GuildTrade, Habitat,
    HeraldicSymbol, IndustrialTrade, LandmarkAdjective, LandmarkFeature,
    NaturalNameRoot, OrganizationSymbol, ShopType, TavernAnimal, TavernObject,
    WildAnimal, text,
)


@pytest.mark.parametrize("component_type", [
    ArtifactObject, SpellEffect, MagicalConcept, OperationColor, Season,
    BodyPart, BusinessAnimal, BusinessColor, BusinessTrade, CelestialObjectType,
    CompoundCreatureName, CompoundLandmarkName, CreatureType, GuildTrade, Habitat,
    HeraldicSymbol, IndustrialTrade, LandmarkAdjective, LandmarkFeature,
    OrganizationSymbol, ShopType, TavernAnimal, TavernObject, WildAnimal,
])
def test_naming_components_are_immutable_and_replayable(component_type):
    component = component_type()
    with pytest.raises(FrozenInstanceError):
        component.extra = "changed"
    rng = random.Random(42)
    replay = random.Random(42)
    assert [component(rng) for _ in range(50)] == [
        component(replay) for _ in range(50)
    ]


@pytest.mark.parametrize("context", ["landmark", "creature"])
def test_natural_roots_are_immutable_and_replayable(context):
    component = NaturalNameRoot(context=context)
    with pytest.raises(FrozenInstanceError):
        component.context = "other"
    assert component(random.Random(12)) == component(random.Random(12))


@pytest.mark.parametrize("context", ["", "other", None, 1, [], {}])
def test_natural_root_rejects_invalid_context(context):
    with pytest.raises(ValueError):
        NaturalNameRoot(context=context)


def test_compound_creature_uses_public_parts_and_one_stream():
    actual_rng = random.Random(91)
    expected_rng = random.Random(91)
    expected = (
        NaturalNameRoot(context="creature") + BodyPart()
    ).title_case()
    for _ in range(100):
        assert CompoundCreatureName()(actual_rng) == expected(expected_rng)
    assert actual_rng.getstate() == expected_rng.getstate()


def test_custom_composition_preserves_stream_order():
    rng = random.Random(91)
    replay = random.Random(91)
    parts = [BusinessColor(), BusinessAnimal(), BusinessTrade()]
    composed = text(*parts, sep=" ")
    assert composed(rng) == " ".join(part(replay) for part in parts)
    assert rng.getstate() == replay.getstate()


def test_body_part_changes_reach_both_creature_branches(monkeypatch):
    from wordsmith import CreatureName
    from tests.test_generator_conformance import _ScriptedRandom

    monkeypatch.setattr(BodyPart, "make_text", lambda self, rng: "crest")
    assert CompoundCreatureName()(_ScriptedRandom([])) == "Ashcrest"
    assert CreatureName()(_ScriptedRandom([0])) == "Ashcrest Basilisk"
    assert CreatureName()(_ScriptedRandom([0.9])) == "Ashcrest"
