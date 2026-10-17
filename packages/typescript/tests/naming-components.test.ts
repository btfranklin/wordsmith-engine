import assert from "node:assert/strict";
import { test } from "node:test";
import {
  ArtifactObject,
  BodyPart,
  BusinessAnimal,
  BusinessColor,
  BusinessTrade,
  CelestialObjectType,
  CompoundCreatureName,
  CompoundLandmarkName,
  CreatureName,
  CreatureType,
  concat,
  GuildTrade,
  Habitat,
  HeraldicSymbol,
  IndustrialTrade,
  join,
  LandmarkAdjective,
  LandmarkFeature,
  MagicalConcept,
  NaturalNameRoot,
  type NaturalNameRootOptions,
  OperationColor,
  OrganizationSymbol,
  Season,
  ShopType,
  SpellEffect,
  seededRandom,
  TavernAnimal,
  TavernObject,
  WildAnimal,
} from "../dist/index.js";

test("reusable naming components are immutable and replayable", () => {
  for (const Constructor of [
    ArtifactObject,
    SpellEffect,
    MagicalConcept,
    OperationColor,
    Season,
    BodyPart,
    BusinessAnimal,
    BusinessColor,
    BusinessTrade,
    CelestialObjectType,
    CompoundCreatureName,
    CompoundLandmarkName,
    CreatureType,
    CreatureName,
    GuildTrade,
    Habitat,
    HeraldicSymbol,
    IndustrialTrade,
    LandmarkAdjective,
    LandmarkFeature,
    OrganizationSymbol,
    ShopType,
    TavernAnimal,
    TavernObject,
    WildAnimal,
  ]) {
    const component = new Constructor();
    assert.ok(Object.isFrozen(component));
    const rng = seededRandom(42);
    const replay = seededRandom(42);
    assert.deepEqual(
      Array.from({ length: 50 }, () => component.render(rng)),
      Array.from({ length: 50 }, () => component.render(replay)),
    );
  }
});

test("natural root contexts are immutable and validated", () => {
  for (const context of ["landmark", "creature"] as const) {
    const root = new NaturalNameRoot({ context });
    assert.ok(Object.isFrozen(root));
    assert.equal(root.render(seededRandom(12)), root.render(seededRandom(12)));
  }
  for (const context of ["", "other", null, 1, [], {}]) {
    assert.throws(
      () => new NaturalNameRoot({ context } as unknown as NaturalNameRootOptions),
      RangeError,
    );
  }
});

test("compound creature names use public parts and one stream", () => {
  const rng = seededRandom(91);
  const replay = seededRandom(91);
  const expected = concat(
    new NaturalNameRoot({ context: "creature" }),
    new BodyPart(),
  ).titleCase();
  for (let index = 0; index < 100; index += 1) {
    assert.equal(new CompoundCreatureName().render(rng), expected.render(replay));
  }
  assert.equal(rng.random(), replay.random());
});

test("custom naming compositions preserve stream order", () => {
  const rng = seededRandom(91);
  const replay = seededRandom(91);
  const parts = [new BusinessColor(), new BusinessAnimal(), new BusinessTrade()];
  assert.equal(
    join(parts, " ").render(rng),
    parts.map((part) => part.render(replay)).join(" "),
  );
  assert.equal(rng.random(), replay.random());
});

test("body part changes reach both creature branches", (t) => {
  t.mock.method(BodyPart.prototype, "render", () => "crest");
  assert.equal(new CompoundCreatureName().render({ random: () => 0 }), "Ashcrest");
  for (const [first, expected] of [
    [0, "Ashcrest Basilisk"],
    [0.9, "Ashcrest"],
  ] as const) {
    let next: number = first;
    const rng = {
      random() {
        const fraction = next;
        next = 0;
        return fraction;
      },
    };
    assert.equal(new CreatureName().render(rng), expected);
  }
});
