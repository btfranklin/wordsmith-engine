import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { component, type WeightedOption, weightedOneOf } from "../dist/core.js";

interface WeightCase {
  readonly name: string;
  readonly weights: readonly (number | "NaN" | "Infinity" | "-Infinity")[];
  readonly accepted: boolean;
}

const fixture = JSON.parse(
  readFileSync(
    new URL("../../../spec/conformance/weighted-choices.json", import.meta.url),
    "utf8",
  ),
) as { readonly cases: readonly WeightCase[] };

for (const weightCase of fixture.cases) {
  test(`shared weight validation: ${weightCase.name}`, () => {
    const option = component(() => {
      throw new Error("Construction must not render children.");
    });
    const pairs: WeightedOption[] = weightCase.weights.map((weight) => [
      Number(weight),
      option,
    ]);

    if (weightCase.accepted) {
      assert.doesNotThrow(() => weightedOneOf(...pairs));
    } else {
      assert.throws(() => weightedOneOf(...pairs), RangeError);
    }
  });
}
