import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { fileURLToPath } from "node:url";
import type { Component, RandomSource } from "../dist/index.js";
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
} from "../dist/index.js";

interface TraceCase {
  readonly name: string;
  readonly intent: string;
  readonly generator: keyof typeof generators;
  readonly fractions: readonly number[];
  readonly repeat?: number;
  readonly cycle?: boolean;
  readonly expected: string;
  readonly expectedDraws: number;
}

const fixturePath = fileURLToPath(
  new URL("../../../spec/conformance/generator-traces.json", import.meta.url),
);
const cases = (
  JSON.parse(readFileSync(fixturePath, "utf8")) as {
    readonly cases: readonly TraceCase[];
  }
).cases;

const generators = {
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
} as const satisfies Record<string, new () => Component>;

test("shared generator trace metadata", () => {
  const names = new Set<string>();
  for (const trace of cases) {
    assert.equal(typeof trace.name, "string");
    assert.ok(trace.name.trim().length > 0);
    assert.equal(typeof trace.intent, "string");
    assert.ok(trace.intent.trim().length > 0);
    assert.ok(!names.has(trace.name), `Duplicate generator trace: ${trace.name}`);
    names.add(trace.name);
  }
});

class ScriptedRandom implements RandomSource {
  readonly #fractions: readonly number[];
  readonly #repeat: number;
  readonly #cycle: boolean;
  drawCount = 0;

  constructor(trace: TraceCase) {
    if (trace.cycle === true && trace.fractions.length === 0) {
      throw new RangeError("Cyclic scripted RNGs require at least one fraction.");
    }
    this.#fractions = trace.fractions;
    this.#repeat = trace.repeat ?? 0;
    this.#cycle = trace.cycle ?? false;
  }

  random(): number {
    const value = this.#cycle
      ? this.#fractions[this.drawCount % this.#fractions.length]
      : (this.#fractions[this.drawCount] ?? this.#repeat);
    this.drawCount += 1;
    if (value === undefined || !Number.isFinite(value) || value < 0 || value >= 1) {
      throw new RangeError("Scripted fractions must be finite values in [0, 1).");
    }
    return value;
  }
}

for (const trace of cases) {
  test(`shared generator trace: ${trace.name}: ${trace.intent}`, () => {
    const rng = new ScriptedRandom(trace);
    assert.equal(new generators[trace.generator]().render(rng), trace.expected);
    assert.equal(rng.drawCount, trace.expectedDraws);
  });
}
