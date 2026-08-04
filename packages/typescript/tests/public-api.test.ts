import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import * as wordsmith from "../dist/index.js";

interface PublicApiFixture {
  readonly pythonRuntime: readonly string[];
  readonly typescriptRuntime: readonly string[];
  readonly typescriptTypes: readonly string[];
}

const repositoryRoot = new URL("../../../", import.meta.url);
const fixture = JSON.parse(
  readFileSync(new URL("spec/conformance/public-api.json", repositoryRoot), "utf8"),
) as PublicApiFixture;

test("the root module exposes the complete documented runtime surface", () => {
  assert.deepEqual(
    Object.keys(wordsmith).sort(),
    [...fixture.typescriptRuntime].sort(),
  );
});

test("the API document mentions every public symbol", () => {
  const apiDocument = readFileSync(new URL("spec/API.md", repositoryRoot), "utf8");
  for (const symbol of [
    ...fixture.pythonRuntime,
    ...fixture.typescriptRuntime,
    ...fixture.typescriptTypes,
  ]) {
    assert.ok(apiDocument.includes(`\`${symbol}\``), `API.md is missing ${symbol}`);
  }
});

test("the root module supports a real asset-backed composition", () => {
  const rng = wordsmith.seededRandom(5343);
  const value = wordsmith
    .join(["The", new wordsmith.Adjective(), new wordsmith.Noun()], " ")
    .titleCase()
    .render(rng);
  assert.match(value, /^The /);
});
