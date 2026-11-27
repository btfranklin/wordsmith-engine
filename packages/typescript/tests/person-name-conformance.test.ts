import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import {
  type GivenNamePart,
  PersonName,
  type PersonNameOptions,
} from "../dist/index.js";

interface PersonNameCase {
  readonly configuration: PersonNameOptions;
  readonly expected: string;
}

const cases = JSON.parse(
  readFileSync(
    new URL("../../../spec/conformance/person-names.json", import.meta.url),
    "utf8",
  ),
) as {
  readonly draws: readonly (PersonNameCase & {
    readonly name: string;
    readonly fractions: readonly number[];
  })[];
  readonly hashes: readonly (PersonNameCase & { readonly digest: string })[];
};

for (const row of cases.draws) {
  test(`PersonName draw case ${row.name}`, () => {
    let index = 0;
    const rng = {
      random() {
        const fraction = row.fractions[index];
        index += 1;
        assert.notEqual(fraction, undefined);
        return fraction as number;
      },
    };
    assert.equal(new PersonName(row.configuration).render(rng), row.expected);
    assert.equal(index, row.fractions.length);
  });
}

test("PersonName reproduces hash cases out of order and concurrently", async () => {
  for (const row of cases.hashes) {
    assert.equal(
      await new PersonName(row.configuration).fromHash(row.digest),
      row.expected,
    );
  }
  const reversed = [...cases.hashes].reverse();
  assert.deepEqual(
    await Promise.all(
      reversed.map((row) => new PersonName(row.configuration).fromHash(row.digest)),
    ),
    reversed.map((row) => row.expected),
  );

  const instance = new PersonName();
  assert.deepEqual(
    await Promise.all([
      instance.fromHash("ff".repeat(32)),
      instance.fromHash("00".repeat(32)),
      instance.fromHash("FF".repeat(32)),
    ]),
    ["Seok-mun Harding", "Kandi Santos", "Seok-mun Harding"],
  );
});

test("PersonName rejects invalid hash digests", async () => {
  for (const digest of ["", "0".repeat(63), `${"0".repeat(63)}\n`, "z".repeat(64)]) {
    await assert.rejects(new PersonName().fromHash(digest), /SHA-256/);
  }
});

test("PersonName hash frequencies approximate the default weights", async () => {
  const plain = new PersonName();
  const varied = new PersonName({ style: "varied" });
  const modifier = /^(Dr\.|Prof\.) | (Jr\.|Sr\.|II|III|IV|V)$|, (Esq\.|PhD\.|MD)$/gu;
  let changedFormats = 0;
  let modifiers = 0;
  for (let number = 0; number < 1024; number += 1) {
    const digest = number.toString(16).padStart(64, "0");
    const rendered = await varied.fromHash(digest);
    const unmodified = rendered.replace(modifier, () => {
      modifiers += 1;
      return "";
    });
    changedFormats += Number(unmodified !== (await plain.fromHash(digest)));
  }
  assert.ok(changedFormats >= 140 && changedFormats <= 220, String(changedFormats));
  assert.ok(modifiers >= 16 && modifiers <= 48, String(modifiers));
});

test("PersonName snapshots options and rejects invalid weights", async () => {
  const credentials = ["PhD."];
  const format: GivenNamePart[] = ["full"];
  const formatWeights = [[1, format] as const];
  const value = new PersonName({ credentials, formatWeights });
  credentials.length = 0;
  format.length = 0;
  formatWeights.length = 0;
  assert.equal(await value.fromHash("0".repeat(64)), "Kandi Santos, PhD.");
  for (const weight of [0, -1, Number.NaN, Number.POSITIVE_INFINITY]) {
    assert.throws(
      () => new PersonName({ formatWeights: [[weight, ["full"]]] }),
      /Weights/,
    );
  }
});
