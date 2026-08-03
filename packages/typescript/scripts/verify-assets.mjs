import assert from "node:assert/strict";
import { readdirSync, readFileSync } from "node:fs";

const canonicalRoot = new URL("../../../assets/", import.meta.url);
const packageRoot = new URL("../src/assets/", import.meta.url);

function jsonNames(root) {
  return readdirSync(root)
    .filter((name) => name.endsWith(".json"))
    .sort();
}

const expected = jsonNames(canonicalRoot);
assert.ok(expected.length > 0, "no canonical JSON assets were found");
assert.deepEqual(jsonNames(packageRoot), expected, "package asset names differ");

for (const name of expected) {
  assert.deepEqual(
    readFileSync(new URL(name, packageRoot)),
    readFileSync(new URL(name, canonicalRoot)),
    `package asset bytes differ for ${name}`,
  );
}
