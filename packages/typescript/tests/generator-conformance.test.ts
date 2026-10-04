import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { fileURLToPath } from "node:url";
import type {
  AlienNameOptions,
  AncientGivenNameOptions,
  Component,
  GivenNameOptions,
  RandomSource,
} from "../dist/index.js";
import {
  AlbumTitle,
  AlienName,
  AncientGivenName,
  BandName,
  BinaryGender,
  CriminalGangName,
  FantasyName,
  FictionalElementName,
  FictionalMineralName,
  GivenName,
  GivenNameCulture,
  HighConceptMovieTitle,
  LiteraryTitle,
  MovieTitle,
  NauticalShipName,
  PersonName,
  SimpleLiteraryTitle,
  SimpleMovieTitle,
  TownName,
  UnusualLiteraryTitle,
} from "../dist/index.js";

interface TraceMetadata {
  readonly name: string;
  readonly intent: string;
  readonly fractions: readonly number[];
  readonly repeat?: number;
  readonly cycle?: boolean;
  readonly expected: string;
  readonly expectedDraws: number;
}

type TraceCase = TraceMetadata &
  (
    | { readonly generator: keyof typeof generators; readonly configuration?: never }
    | {
        readonly generator: "GivenName" | "PersonName";
        readonly configuration?: GivenNameOptions;
      }
    | {
        readonly generator: "AncientGivenName";
        readonly configuration?: AncientGivenNameOptions;
      }
    | {
        readonly generator: "AlienName" | "FantasyName";
        readonly configuration: AlienNameOptions;
      }
  );

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

function buildGenerator(trace: TraceCase): Component {
  switch (trace.generator) {
    case "GivenName":
      return new GivenName(trace.configuration);
    case "AncientGivenName":
      return new AncientGivenName(trace.configuration);
    case "PersonName":
      return new PersonName(trace.configuration);
    case "AlienName":
      return new AlienName(trace.configuration);
    case "FantasyName":
      return new FantasyName(trace.configuration);
    default:
      return new generators[trace.generator]();
  }
}

function validateConfiguration(trace: TraceCase): void {
  const raw: unknown = trace.configuration;
  const isSynthetic =
    trace.generator === "AlienName" || trace.generator === "FantasyName";
  if (raw === undefined) {
    assert.ok(!isSynthetic, "Synthetic names require configuration.");
    return;
  }
  assert.ok(raw !== null && typeof raw === "object" && !Array.isArray(raw));
  const configuration = raw as {
    readonly syllableCount?: unknown;
    readonly allowHyphen?: unknown;
    readonly allowApostrophe?: unknown;
    readonly gender?: unknown;
    readonly culture?: unknown;
  };
  const allowedKeys = isSynthetic
    ? ["syllableCount", "allowHyphen", "allowApostrophe"]
    : trace.generator === "AncientGivenName"
      ? ["gender"]
      : trace.generator === "GivenName" || trace.generator === "PersonName"
        ? ["gender", "culture"]
        : [];
  assert.ok(Object.keys(configuration).every((key) => allowedKeys.includes(key)));
  if (isSynthetic) {
    assert.ok(Number.isSafeInteger(configuration.syllableCount));
    assert.ok((configuration.syllableCount as number) > 0);
  }
  for (const key of ["allowHyphen", "allowApostrophe"] as const) {
    if (Object.hasOwn(configuration, key)) {
      assert.equal(typeof configuration[key], "boolean");
    }
  }
  if (Object.hasOwn(configuration, "gender")) {
    assert.ok(
      Object.values(BinaryGender).some((value) => value === configuration.gender),
    );
  }
  if (Object.hasOwn(configuration, "culture")) {
    assert.ok(
      Object.values(GivenNameCulture).some((value) => value === configuration.culture),
    );
  }
}

test("shared generator trace metadata", () => {
  const names = new Set<string>();
  for (const trace of cases) {
    assert.equal(typeof trace.name, "string");
    assert.ok(trace.name.trim().length > 0);
    assert.equal(typeof trace.intent, "string");
    assert.ok(trace.intent.trim().length > 0);
    assert.ok(!names.has(trace.name), `Duplicate generator trace: ${trace.name}`);
    validateConfiguration(trace);
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
    validateConfiguration(trace);
    const rng = new ScriptedRandom(trace);
    assert.equal(buildGenerator(trace).render(rng), trace.expected);
    assert.equal(rng.drawCount, trace.expectedDraws);
  });
}
