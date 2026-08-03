import assert from "node:assert/strict";
import { test } from "node:test";
import {
  AlbumTitle,
  BandName,
  CriminalGangName,
  FictionalElementName,
  FictionalMineralName,
  HighConceptMovieTitle,
  LiteraryTitle,
  MovieTitle,
  NauticalShipName,
  SimpleLiteraryTitle,
  SimpleMovieTitle,
  TownName,
  UnusualLiteraryTitle,
} from "../dist/generators.js";
import { seededRandom } from "../dist/random.js";

const generatorFactories = [
  () => new AlbumTitle(),
  () => new BandName(),
  () => new CriminalGangName(),
  () => new FictionalElementName(),
  () => new FictionalMineralName(),
  () => new HighConceptMovieTitle(),
  () => new LiteraryTitle(),
  () => new MovieTitle(),
  () => new NauticalShipName(),
  () => new SimpleLiteraryTitle(),
  () => new SimpleMovieTitle(),
  () => new TownName(),
  () => new UnusualLiteraryTitle(),
] as const;

test("every public generator is immutable, nonempty, and repeatable", () => {
  for (const makeGenerator of generatorFactories) {
    const generator = makeGenerator();
    assert.ok(Object.isFrozen(generator));
    const first = generator.render(seededRandom("world/ships/primary"));
    const second = makeGenerator().render(seededRandom("world/ships/primary"));
    assert.equal(first, second);
    assert.notEqual(first, "");
  }
});

test("fictional material names stay clean and use their expected endings", () => {
  for (let seed = 0; seed < 200; seed += 1) {
    const element = new FictionalElementName().render(seededRandom(seed));
    const mineral = new FictionalMineralName().render(seededRandom(seed));
    assert.match(element, /^[a-z]{4,20}$/);
    assert.match(element, /(ium|on|ine|ene|gen)$/);
    assert.match(mineral, /^[a-z]{4,20}$/);
    assert.match(mineral, /(ite|ine|spar|stone|ore|cryst|glass)$/);
  }
});

test("title generators produce clean title-shaped output", () => {
  const titleFactories = [
    () => new AlbumTitle(),
    () => new LiteraryTitle(),
    () => new MovieTitle(),
    () => new SimpleLiteraryTitle(),
    () => new UnusualLiteraryTitle(),
    () => new SimpleMovieTitle(),
    () => new HighConceptMovieTitle(),
  ] as const;

  for (let seed = 0; seed < 100; seed += 1) {
    for (const makeTitle of titleFactories) {
      const title = makeTitle().render(seededRandom(`title:${seed}`));
      assert.equal(title, title.trim());
      assert.ok(!title.includes("  "));
      assert.ok(title.length > 1);
    }
  }
});

test("a deeply layered generator has a fixed same-language replay vector", () => {
  const first = new NauticalShipName().render(seededRandom("fleet/flagship"));
  const second = new NauticalShipName().render(seededRandom("fleet/flagship"));
  assert.equal(first, second);
  assert.equal(first, "Adamantine Nightmare");
});
