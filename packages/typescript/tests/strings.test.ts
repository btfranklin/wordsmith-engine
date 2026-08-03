import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { fileURLToPath } from "node:url";
import {
  capitalized,
  firstUpper,
  startsWithVowel,
  titleCase,
} from "../dist/strings.js";

interface StringCase<Expected> {
  readonly input: string;
  readonly expected: Expected;
}
interface StringFixtures {
  readonly capitalized: readonly StringCase<string>[];
  readonly firstUpper: readonly StringCase<string>[];
  readonly titleCase: readonly StringCase<string>[];
  readonly possessiveForm: readonly StringCase<string>[];
  readonly startsWithVowel: readonly StringCase<boolean>[];
}

const fixturePath = fileURLToPath(
  new URL("../../../spec/conformance/string-transforms.json", import.meta.url),
);
const fixtures = JSON.parse(readFileSync(fixturePath, "utf8")) as StringFixtures;

test("shared capitalized cases", () => {
  for (const fixture of fixtures.capitalized)
    assert.equal(capitalized(fixture.input), fixture.expected);
});

test("shared firstUpper cases", () => {
  for (const fixture of fixtures.firstUpper)
    assert.equal(firstUpper(fixture.input), fixture.expected);
});

test("shared titleCase cases", () => {
  for (const fixture of fixtures.titleCase)
    assert.equal(titleCase(fixture.input), fixture.expected);
});

test("shared startsWithVowel cases", () => {
  for (const fixture of fixtures.startsWithVowel)
    assert.equal(startsWithVowel(fixture.input), fixture.expected);
});

test("every string-transform fixture section is consumed", () => {
  assert.deepEqual(Object.keys(fixtures).sort(), [
    "capitalized",
    "firstUpper",
    "possessiveForm",
    "startsWithVowel",
    "titleCase",
  ]);
});
