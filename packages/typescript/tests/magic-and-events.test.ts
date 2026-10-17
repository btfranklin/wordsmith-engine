import assert from "node:assert/strict";
import { test } from "node:test";
import {
  ArtifactName,
  FestivalName,
  join,
  MagicalConcept,
  OperationName,
  SpellName,
  seededRandom,
} from "../dist/index.js";

test("magic and event names are clean, varied, and repeatable", () => {
  for (const Generator of [ArtifactName, SpellName, OperationName, FestivalName]) {
    const generator = new Generator();
    const rng = seededRandom(5343);
    const replay = seededRandom(5343);
    const outputs = Array.from({ length: 200 }, () => generator.render(rng));
    assert.deepEqual(
      outputs,
      Array.from({ length: 200 }, () => generator.render(replay)),
    );
    assert.ok(new Set(outputs).size > 100);
    for (const output of outputs) {
      assert.equal(output, output.trim());
      assert.ok(!output.includes("  "));
      assert.ok(!output.toLowerCase().includes("the the "));
      assert.match(output, /^[A-Z].*[a-zA-Z]$/);
    }
  }
});

test("magic and event compositions share one stream", () => {
  const rng = seededRandom(42);
  const replay = seededRandom(42);
  const parts = [
    new ArtifactName(),
    new SpellName(),
    new OperationName(),
    new FestivalName(),
  ];
  assert.equal(
    join(parts, " / ").render(rng),
    parts.map((part) => part.render(replay)).join(" / "),
  );
  assert.equal(rng.random(), replay.random());
});

test("magical concept changes reach artifacts and spells", (t) => {
  t.mock.method(MagicalConcept.prototype, "render", () => "new echoes");
  assert.equal(
    new ArtifactName().render({ random: () => 0 }),
    "The Crown of New Echoes",
  );
  assert.equal(new SpellName().render({ random: () => 0 }), "Veil of New Echoes");
});
