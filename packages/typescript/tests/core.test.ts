import assert from "node:assert/strict";
import { readdirSync, readFileSync } from "node:fs";
import { test } from "node:test";
import { fileURLToPath } from "node:url";
import {
  Component,
  type ComponentLike,
  component,
  concat,
  either,
  empty,
  join,
  type MaybeOptions,
  maybe,
  oneOf,
  type RandomSource,
  weightedOneOf,
  ws,
} from "../dist/core.js";

function fractionSource(fractions: readonly number[]): RandomSource {
  let index = 0;
  return {
    random() {
      const value = fractions[index];
      assert.notEqual(value, undefined);
      index += 1;
      return value as number;
    },
  };
}

interface PartFixture {
  readonly kind: "empty" | "sequence" | "probe";
  readonly label?: string;
  readonly text?: string;
  readonly separator?: string;
  readonly parts?: readonly FixturePart[];
}
type FixturePart = string | PartFixture;
interface SequenceCase {
  readonly name: string;
  readonly separator: string;
  readonly parts: FixturePart[];
  readonly expected: string;
  readonly expectedRenderOrder?: readonly string[];
  readonly expectedRandomDraws?: number;
  readonly mutationAfterConstruction?: {
    readonly index: number;
    readonly replacement: FixturePart;
  };
}
interface SequenceFixtures {
  readonly cases: readonly SequenceCase[];
}
const fixturePath = fileURLToPath(
  new URL("../../../spec/conformance/component-sequences.json", import.meta.url),
);
const fixtures = JSON.parse(readFileSync(fixturePath, "utf8")) as SequenceFixtures;

test("every shared conformance fixture is consumed", () => {
  const conformanceDirectory = new URL("../../../spec/conformance/", import.meta.url);
  assert.deepEqual(
    readdirSync(conformanceDirectory)
      .filter((name) => name.endsWith(".json"))
      .sort(),
    [
      "component-sequences.json",
      "generator-traces.json",
      "public-api.json",
      "string-transforms.json",
      "weighted-choices.json",
    ],
  );
});

function buildPart(
  part: FixturePart,
  order: string[],
  sources: RandomSource[],
): ComponentLike {
  if (typeof part === "string") return part;
  if (part.kind === "empty") return empty();
  if (part.kind === "sequence")
    return join(
      (part.parts ?? []).map((child) => buildPart(child, order, sources)),
      part.separator ?? "",
    );
  return component((rng) => {
    order.push(part.label ?? "");
    sources.push(rng);
    rng.random();
    return part.text ?? "";
  });
}

for (const fixture of fixtures.cases) {
  test(`shared sequence: ${fixture.name}`, () => {
    const order: string[] = [];
    const sources: RandomSource[] = [];
    const parts = fixture.parts.map((part) => buildPart(part, order, sources));
    const sequence = join(parts, fixture.separator);
    if (fixture.mutationAfterConstruction) {
      parts[fixture.mutationAfterConstruction.index] = buildPart(
        fixture.mutationAfterConstruction.replacement,
        order,
        sources,
      );
    }
    let draws = 0;
    const rng: RandomSource = {
      random: () => {
        draws += 1;
        return 0.25;
      },
    };
    assert.equal(sequence.render(rng), fixture.expected);
    assert.deepEqual(order, fixture.expectedRenderOrder ?? []);
    assert.equal(draws, fixture.expectedRandomDraws ?? 0);
    assert.ok(sources.every((source) => source === rng));
  });
}

test("concat and ws preserve exact text without spacing magic", () => {
  const rng = fractionSource([]);
  assert.equal(concat("Once", empty(), ".").render(rng), "Once.");
  assert.equal(
    ws`alpha ${empty()} beta\n${"gamma"}!`.render(rng),
    "alpha  beta\ngamma!",
  );
});

test("components are immutable and reject non-string output", () => {
  const value = component(() => "value");
  assert.ok(Object.isFrozen(value));
  assert.throws(
    () => component(() => 1 as unknown as string).render(fractionSource([])),
    /render strings/,
  );
});

test("choice combinators honor boundaries and forward one source", () => {
  assert.equal(oneOf("a", "b").render(fractionSource([0.999])), "b");
  assert.equal(weightedOneOf([0, "a"], [2, "b"]).render(fractionSource([0])), "b");
  assert.equal(either("a", "b", 1).render(fractionSource([0.9])), "a");
  assert.equal(maybe("a", { probability: 0 }).render(fractionSource([0])), "");
  assert.equal(maybe("a", "b", { probability: 1 }).render(fractionSource([0])), "ab");
});

test("combinators validate their domains", () => {
  assert.throws(() => oneOf(), /at least one/);
  assert.throws(() => weightedOneOf(), /at least one/);
  assert.throws(() => weightedOneOf([-1, "a"]), /non-negative/);
  assert.throws(() => weightedOneOf([0, "a"]), /positive total/);
  assert.throws(() => either("a", "b", Number.NaN), /probability/);
  assert.throws(() => maybe("a", { probability: 2 }), /Probability/);
  for (const unsupported of [[], new Date(0), new Map()]) {
    assert.throws(
      () => maybe(unsupported as unknown as ComponentLike),
      /strings or Components/,
    );
  }
});

test("maybe accepts structural options and empty plain options", () => {
  class Options implements MaybeOptions {
    get probability(): number {
      return 1;
    }
  }
  const optionsWithMetadata = { probability: 1, label: "feature" };
  for (const options of [new Options(), optionsWithMetadata]) {
    assert.equal(maybe("included", options).render(fractionSource([0.9])), "included");
  }
  assert.equal(maybe("included", {}).render(fractionSource([0.25])), "included");
  assert.equal(maybe("included", {}).render(fractionSource([0.75])), "");
  const invalidOptions = { probability: 2, label: "feature" };
  assert.throws(() => maybe("included", invalidOptions), /Probability/);
});

test("maybe keeps Components with a probability property as children", () => {
  class ProbabilityComponent extends Component {
    readonly probability = 0;

    render(): string {
      return "child";
    }
  }
  assert.equal(
    maybe("prefix-", new ProbabilityComponent()).render(fractionSource([0])),
    "prefix-child",
  );
});

test("weighted choices exclude zero weights at small totals", () => {
  for (const weight of [Number.MIN_VALUE, 2 ** -1022, 1]) {
    const choice = weightedOneOf([0, "zero"], [weight, "positive"], [0, "zero"]);
    for (const fraction of [0, 0.75, 1 - Number.EPSILON / 2]) {
      let draws = 0;
      assert.equal(
        choice.render({
          random: () => {
            draws += 1;
            return fraction;
          },
        }),
        "positive",
      );
      assert.equal(draws, 1);
    }
  }
});

test("weighted choices preserve ratios for small weights", () => {
  for (const scale of [Number.MIN_VALUE, 2 ** -1024, 1]) {
    const choice = weightedOneOf([scale, "first"], [3 * scale, "second"], [0, "zero"]);
    for (const [fraction, expected] of [
      [0, "first"],
      [0.25 - Number.EPSILON / 8, "first"],
      [0.25, "second"],
      [1 - Number.EPSILON / 2, "second"],
    ] as const) {
      let draws = 0;
      assert.equal(
        choice.render({
          random: () => {
            draws += 1;
            return fraction;
          },
        }),
        expected,
      );
      assert.equal(draws, 1);
    }
  }
});

test("fluent transforms consume the shared string fixtures", () => {
  const stringPath = fileURLToPath(
    new URL("../../../spec/conformance/string-transforms.json", import.meta.url),
  );
  const stringFixtures = JSON.parse(readFileSync(stringPath, "utf8")) as {
    readonly possessiveForm: readonly {
      readonly input: string;
      readonly expected: string;
    }[];
  };
  for (const fixture of stringFixtures.possessiveForm) {
    assert.equal(
      component(() => fixture.input)
        .possessiveForm()
        .render(fractionSource([])),
      fixture.expected,
    );
  }
});

test("fluent article and determiner prefixes use vowel-sound selection", () => {
  assert.equal(
    component(() => "unimportant detail")
      .prefixedByArticle()
      .render(fractionSource([0])),
    "an unimportant detail",
  );
  assert.equal(
    component(() => "onerous task")
      .prefixedByDeterminer()
      .render(fractionSource([0])),
    "an onerous task",
  );
});
